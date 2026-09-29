import ctypes
import os
import queue
import re
import shutil
import string
import sys
import threading
import unicodedata
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
from yt_dlp.postprocessor import PostProcessor
from yt_dlp.utils import sanitize_filename, DownloadCancelled
from modules.assets.ascii import ascii

# fora da pasta do programa: no .exe ela é temporária
DADOS = os.path.join(os.environ.get('LOCALAPPDATA') or os.path.expanduser('~'), 'H-Tube')
# acima de 192 não ganha nada: o áudio do YouTube já vem comprimido (~130-160 kbps)
BITRATES = [64, 80, 96, 112, 128, 160, 192]
RESOLUCOES = [1080, 720, 480, 360]
MODOS = {
    'musica': {'lista': 'musicas.txt', 'pasta': 'Musicas',
               'legenda': (('# gênero', 'genero'), ('artista', 'artista'), ('link', 'link')),
               'dica': 'qualidade automática: o maior MP3 que couber no destino'},
    'video': {'lista': 'videos.txt', 'pasta': 'Videos',
              'legenda': (('# pasta', 'genero'), ('subpasta', 'artista'), ('link', 'link')),
              'dica': 'cole os links, um por linha · playlist também funciona · pastas são opcionais'},
}
# visor de som de carro antigo: preto quente + âmbar
COR = {'fundo': '#16110d', 'painel': '#221a14', 'borda': '#3a2c20', 'texto': '#f2e3cc',
       'apagado': '#a8957f', 'ambar': '#ffae1a', 'ambar_escuro': '#c77800',
       'genero': '#ffae1a', 'artista': '#ff6a3d', 'link': '#a8957f'}
FONTE = 'Bahnschrift'


def ler_lista(texto):
    """'# Gênero' vira pasta numerada, linha com nome vira subpasta, links vão pra ela."""
    itens, genero, artista, n = [], '', '', 0
    for linha in texto.splitlines():
        linha = linha.strip()
        if linha.startswith('http'):
            itens.append((genero, artista, linha))
        elif linha.startswith('#'):
            n += 1
            genero, artista = f"{n} {linha.lstrip('#').strip()}", ''
        elif linha:
            artista = linha
    return itens


def limpar_titulo(titulo, limite=60):
    t = re.sub(r'[(\[{【].*?[)\]}】]', '', titulo)       # (Ao Vivo) [HD] {Oficial}
    t = re.split(r'\s*[|•]', t)[0]                      # "Música | Canal Oficial"
    t = re.sub(r'[#@]\S+', '', t)                       # #hashtags e @canal
    t = ''.join(c for c in t if unicodedata.category(c) not in ('So', 'Cf', 'Cs', 'Co')
                and c != '️')                      # emojis e símbolos
    t = re.sub(r'(\s*-\s*){2,}', ' - ', t)              # "A -  - B" que sobra
    t = re.sub(r'\s+', ' ', t).strip(' -_.,')
    if t.isupper():
        t = t.title()
    if len(t) > limite:
        t = t[:limite].rsplit(' ', 1)[0].strip(' -_.,')
    return t or titulo[:limite]


def escolher_bitrate(bytes_livres, segundos):
    kbps = bytes_livres * 0.95 * 8 / 1000 / max(segundos, 1)  # 5% de folga
    cabem = [b for b in BITRATES if b <= kbps]
    return cabem[-1] if cabem else None


def formato_video(altura):
    # H.264 + AAC primeiro: é o que TV, som de carro e celular antigo tocam
    return (f'bv*[height<={altura}][vcodec^=avc1]+ba[ext=m4a]/'
            f'bv*[height<={altura}]+ba/b[height<={altura}]/w')


def unidades():
    return [f'{l}:\\' for l in string.ascii_uppercase if os.path.exists(f'{l}:\\')]


def pen_drives():
    if os.name != 'nt':
        return []
    return [u for u in unidades() if ctypes.windll.kernel32.GetDriveTypeW(u) == 2]  # 2 = removível


def preparar_ffmpeg(fila):
    if shutil.which('ffmpeg') and shutil.which('ffprobe'):
        return
    import static_ffmpeg
    from static_ffmpeg.run import get_platform_key
    pasta = os.path.join(DADOS, 'ffmpeg', get_platform_key())
    if not os.path.exists(os.path.join(pasta, 'installed.crumb')):
        fila.put('Baixando ffmpeg (só na primeira vez, ~80 MB)...')
    static_ffmpeg.add_paths(weak=True, download_dir=pasta)


class Etiquetar(PostProcessor):
    """Antes de salvar: título curto e tags que o som do carro mostra."""
    def __init__(self, artista, genero):
        super().__init__()
        self.artista, self.genero = artista, genero

    def run(self, info):
        info['title'] = limpar_titulo(info.get('title') or '')
        if self.artista:
            info['artist'] = self.artista
        if self.genero:
            info['genre'] = self.genero.split(' ', 1)[1]  # sem o número
        return [], info


def baixar(itens, raiz, fila, modo, altura, parar):
    preparar_ffmpeg(fila)
    n = len(itens)
    kbps = None
    if modo == 'musica':
        # ponytail: mede tudo de novo a cada execução, inclusive o que já foi baixado;
        # numa retomada o bitrate sai um pouco menor que o necessário
        total = 0
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True,
                               'extract_flat': 'in_playlist', 'ignoreerrors': True}) as ydl:
            for i, (_, _, url) in enumerate(itens, 1):
                if parar.is_set():
                    return fila.put(('fim', 'Parado.'))
                fila.put(('progresso', i, n, f'Medindo duração  ·  {i} de {n}'))
                info = ydl.extract_info(url, download=False) or {}
                total += info.get('duration') or sum(e.get('duration') or 0 for e in info.get('entries') or [])
        livre = shutil.disk_usage(raiz).free
        kbps = escolher_bitrate(livre, total)
        if not kbps:
            return fila.put(('fim', f'Não cabe: {total / 3600:.1f}h de música em {livre / 1e9:.1f} GB livres'))
        fila.put(f'{total / 3600:.1f}h de música, {livre / 1e9:.1f} GB livres: MP3 {kbps} kbps '
                 f'(~{total * kbps / 8e6:.1f} GB)')
    # ponytail: vídeo não confere espaço antes; se encher, os próximos falham e são pulados

    destino = os.path.join(raiz, MODOS[modo]['pasta'])
    faixa, falhas = {}, 0
    for i, (genero, artista, url) in enumerate(itens, 1):
        nome = artista or genero or url
        fila.put(('progresso', i - 1, n, f'Baixando {nome}  ·  {i} de {n}'))

        def baixando(d):
            if parar.is_set():
                raise DownloadCancelled('parado pelo usuário')
            if d['status'] != 'downloading':
                return
            tamanho = d.get('total_bytes') or d.get('total_bytes_estimate')
            parte = d['downloaded_bytes'] / tamanho if tamanho else 0
            fila.put(('progresso', i - 1 + parte, n, f'Baixando {nome}  ·  {i} de {n}  ·  '
                      f'{parte:.0%}  ·  {(d.get("speed") or 0) / 1e6:.1f} MB/s'))

        def convertendo(d):
            if d['status'] == 'started' and d['postprocessor'] in ('ExtractAudio', 'Merger'):
                acao = 'Convertendo pra MP3' if modo == 'musica' else 'Juntando vídeo e áudio'
                fila.put(('progresso', i, n, f'{acao}  ·  {nome}  ·  {i} de {n}'))

        pasta = os.path.join(destino, *[sanitize_filename(p) for p in (genero, artista) if p])
        faixa[pasta] = faixa.get(pasta, 0) + 1  # numera por pasta: ordem certa no som e sem nome repetido
        opcoes = {
            # ponytail: playlist num link só leva o mesmo número + índice da playlist
            'outtmpl': os.path.join(pasta.replace('%', '%%'),
                                    f'{faixa[pasta]:02d}%(playlist_index&-{{}}|)s %(title)s.%(ext)s'),
            'windowsfilenames': True,
            'ignoreerrors': True,
            'quiet': True,
            'no_warnings': True,
            'noprogress': True,
            'progress_hooks': [baixando],
            'postprocessor_hooks': [convertendo],
            'download_archive': os.path.join(destino, 'baixados.txt'),  # pula o que já baixou
        }
        if modo == 'musica':
            opcoes['format'] = 'bestaudio/best'
            opcoes['postprocessors'] = [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': str(kbps)},
                {'key': 'FFmpegMetadata'}]
        else:
            opcoes['format'] = formato_video(altura)
            opcoes['merge_output_format'] = 'mp4'
            opcoes['postprocessors'] = [{'key': 'FFmpegMetadata'}]
        try:
            with yt_dlp.YoutubeDL(opcoes) as ydl:
                ydl.add_post_processor(Etiquetar(artista, genero), when='pre_process')
                if ydl.download([url]):
                    falhas += 1
                    fila.put(f'Falhou, pulando: {nome} {url}')
        except DownloadCancelled:
            return fila.put(('fim', 'Parado. Clique em baixar pra continuar de onde parou.'))
    dica = f' {falhas} falharam: clique em baixar de novo pra tentar só esses.' if falhas else ''
    fila.put(('fim', f'Pronto! {n - falhas} de {n} baixados.{dica}', destino))


def caixa_texto(pai, **kw):
    quadro = tk.Frame(pai, bg=COR['painel'], highlightthickness=1, highlightbackground=COR['borda'])
    texto = tk.Text(quadro, bg=COR['painel'], fg=COR['texto'], insertbackground=COR['ambar'],
                    selectbackground=COR['ambar_escuro'], relief='flat', borderwidth=0,
                    padx=12, pady=10, wrap='none', **kw)
    barra = ttk.Scrollbar(quadro, command=texto.yview)
    texto.config(yscrollcommand=barra.set)
    barra.pack(side='right', fill='y')
    texto.pack(side='left', fill='both', expand=True)
    return quadro, texto


# fita cassete 32x32: (cor, retângulo). Também gera o .ico do executável (build_ico.py)
CASSETE = (('ambar', (1, 6, 31, 26)),          # corpo
           ('ambar_escuro', (8, 22, 24, 26)),  # base
           ('texto', (4, 8, 28, 14)),          # etiqueta
           ('artista', (6, 10, 20, 12)),       # risco na etiqueta
           ('fundo', (8, 16, 24, 21)),         # janela
           ('ambar', (10, 17, 13, 20)),        # carretel esq.
           ('ambar', (19, 17, 22, 20)))        # carretel dir.
CANTOS = ((1, 6), (30, 6), (1, 25), (30, 25))


def icone_cassete():
    img = tk.PhotoImage(width=32, height=32)
    for cor, caixa in CASSETE:
        img.put(COR[cor], to=caixa)
    for x, y in CANTOS:
        img.transparency_set(x, y, True)
    return img


def estilizar(root):
    root.configure(bg=COR['fundo'])
    s = ttk.Style(root)
    s.theme_use('clam')
    s.configure('.', background=COR['fundo'], foreground=COR['texto'], font=(FONTE, 10),
                bordercolor=COR['borda'], troughcolor=COR['fundo'], focuscolor=COR['ambar'])
    s.configure('Apagado.TLabel', foreground=COR['apagado'])
    s.configure('Rotulo.TLabel', foreground=COR['apagado'], font=(FONTE, 9, 'bold'))
    s.configure('Logo.TLabel', foreground=COR['ambar'], font=('Consolas', 7))
    s.configure('TCombobox', fieldbackground=COR['painel'], background=COR['painel'],
                foreground=COR['texto'], arrowcolor=COR['ambar'], bordercolor=COR['borda'],
                lightcolor=COR['painel'], darkcolor=COR['painel'], padding=6)
    s.map('TCombobox', fieldbackground=[('readonly', COR['painel'])],
          background=[('readonly', COR['painel']), ('active', COR['borda'])],
          foreground=[('readonly', COR['texto'])], selectbackground=[('readonly', COR['painel'])],
          selectforeground=[('readonly', COR['ambar'])])
    root.option_add('*TCombobox*Listbox.background', COR['painel'])
    root.option_add('*TCombobox*Listbox.foreground', COR['texto'])
    root.option_add('*TCombobox*Listbox.selectBackground', COR['ambar'])
    root.option_add('*TCombobox*Listbox.selectForeground', COR['fundo'])
    s.configure('Play.TButton', background=COR['ambar'], foreground=COR['fundo'], borderwidth=0,
                font=(FONTE, 12, 'bold'), padding=(22, 8), lightcolor=COR['ambar'], darkcolor=COR['ambar'])
    s.map('Play.TButton', background=[('disabled', COR['borda']), ('active', '#ffc24d')],
          foreground=[('disabled', COR['apagado'])])
    s.configure('Sec.TButton', background=COR['painel'], foreground=COR['texto'], borderwidth=1,
                bordercolor=COR['borda'], lightcolor=COR['painel'], darkcolor=COR['painel'], padding=(10, 5))
    s.map('Sec.TButton', background=[('active', COR['borda'])])
    # segmentado: radiobutton sem a bolinha, selecionado fica âmbar
    for estilo, fonte, pad in (('Aba.TRadiobutton', (FONTE, 11, 'bold'), (18, 7)),
                               ('Chip.TRadiobutton', (FONTE, 10), (12, 5))):
        s.layout(estilo, [('Radiobutton.padding', {'sticky': 'nswe', 'children': [
            ('Radiobutton.label', {'sticky': 'nswe'})]})])
        s.configure(estilo, background=COR['painel'], foreground=COR['apagado'], font=fonte,
                    padding=pad, anchor='center')
        s.map(estilo, background=[('selected', COR['ambar']), ('active', COR['borda'])],
              foreground=[('selected', COR['fundo']), ('active', COR['texto'])])
    s.configure('Horizontal.TProgressbar', background=COR['ambar'], troughcolor=COR['painel'],
                bordercolor=COR['borda'], lightcolor=COR['ambar'], darkcolor=COR['ambar'], thickness=8)
    s.configure('Vertical.TScrollbar', background=COR['borda'], troughcolor=COR['painel'],
                bordercolor=COR['painel'], arrowcolor=COR['apagado'], lightcolor=COR['borda'],
                darkcolor=COR['borda'])
    s.map('Vertical.TScrollbar', background=[('disabled', COR['painel']), ('active', COR['ambar_escuro'])])


def barra_de_titulo_escura(root):
    root.update()
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    r, g, b = (int(COR['fundo'][i:i + 2], 16) for i in (1, 3, 5))
    for atributo, valor in ((20, 1), (35, r | g << 8 | b << 16)):  # modo escuro, cor da barra (Win11)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, atributo, ctypes.byref(ctypes.c_int(valor)), 4)


def ler_arquivo(modo):
    caminho = os.path.join(DADOS, MODOS[modo]['lista'])
    if not os.path.exists(caminho):
        return ''
    with open(caminho, encoding='utf-8-sig') as f:  # -sig: ignora BOM do Bloco de Notas
        return f.read()


def salvar_arquivo(modo, texto):
    os.makedirs(DADOS, exist_ok=True)
    with open(os.path.join(DADOS, MODOS[modo]['lista']), 'w', encoding='utf-8') as f:
        f.write(texto)


def main():
    for nome in ('stdout', 'stderr'):  # .exe sem console: print() e yt-dlp não podem escrever em None
        if getattr(sys, nome) is None:
            setattr(sys, nome, open(os.devnull, 'w'))
    if os.name == 'nt':  # ícone próprio na barra de tarefas em vez do Python
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('htube.app')

    root = tk.Tk()
    root.title('H-Tube')
    root.geometry('900x780')
    root.minsize(700, 600)
    estilizar(root)
    icone = icone_cassete()
    root.iconphoto(True, icone)
    modo = tk.StringVar(value='musica')
    altura = tk.IntVar(value=720)
    destino = tk.StringVar()
    parar = threading.Event()
    rodando = [False]
    fila = queue.Queue()

    # topo: logo + escolha do modo
    topo = ttk.Frame(root, padding=(24, 18, 24, 12))
    topo.pack(fill='x')
    logo = '\n'.join(l.rstrip() for l in ascii[1].splitlines() if '█' in l)
    ttk.Label(topo, text=logo, style='Logo.TLabel', justify='left').pack(side='left')
    abas = ttk.Frame(topo)
    abas.pack(side='right', anchor='s')
    for valor, rotulo in (('musica', '♫  MÚSICA'), ('video', '▶  VÍDEO')):
        ttk.Radiobutton(abas, text=rotulo, value=valor, variable=modo, style='Aba.TRadiobutton',
                        cursor='hand2').pack(side='left', padx=(2, 0))

    # lista
    cabecalho = ttk.Frame(root, padding=(24, 4, 24, 6))
    cabecalho.pack(fill='x')
    legenda = ttk.Frame(cabecalho)
    legenda.pack(side='left')
    resumo = ttk.Label(cabecalho, style='Apagado.TLabel')
    resumo.pack(side='right')

    quadro, texto = caixa_texto(root, font=('Consolas', 10), height=14, undo=True)
    quadro.pack(fill='both', expand=True, padx=24)
    texto.tag_config('genero', foreground=COR['genero'], font=('Consolas', 11, 'bold'))
    texto.tag_config('artista', foreground=COR['artista'])
    texto.tag_config('link', foreground=COR['link'])

    def colorir(_=None):
        for tag in ('genero', 'artista', 'link'):
            texto.tag_remove(tag, '1.0', 'end')
        for n, linha in enumerate(texto.get('1.0', 'end').splitlines(), 1):
            linha = linha.strip()
            tag = 'link' if linha.startswith('http') else 'genero' if linha.startswith('#') else 'artista'
            if linha:
                texto.tag_add(tag, f'{n}.0', f'{n}.end')
        itens = ler_lista(texto.get('1.0', 'end'))
        grupos = len({g for g, _, _ in itens if g})
        pastas = len({(g, a) for g, a, _ in itens if a})
        nomes = ('gêneros', 'artistas') if modo.get() == 'musica' else ('pastas', 'subpastas')
        resumo.config(text='  ·  '.join([f'{len(itens)} links'] +
                                        [f'{q} {nome}' for q, nome in zip((grupos, pastas), nomes) if q]))
        atualizar_botao()

    texto.bind('<KeyRelease>', colorir)

    # opções do modo: dica da música ou resolução do vídeo
    opcoes = ttk.Frame(root, padding=(24, 10, 24, 0))
    opcoes.pack(fill='x')
    dica = ttk.Label(opcoes, style='Apagado.TLabel')
    qualidade = ttk.Frame(opcoes)
    ttk.Label(qualidade, text='QUALIDADE', style='Rotulo.TLabel').pack(side='left', padx=(0, 10))
    for r in RESOLUCOES:
        ttk.Radiobutton(qualidade, text=f'{r}p', value=r, variable=altura, style='Chip.TRadiobutton',
                        cursor='hand2').pack(side='left', padx=(0, 2))

    # destino + ação
    controles = ttk.Frame(root, padding=(24, 14, 24, 4))
    controles.pack(fill='x')
    ttk.Label(controles, text='DESTINO', style='Rotulo.TLabel').pack(side='left')
    # postcommand relista ao abrir, pra pegar o pen drive plugado depois
    combo = ttk.Combobox(controles, textvariable=destino, values=unidades(), state='readonly', width=18,
                         font=(FONTE, 11), postcommand=lambda: combo.config(values=unidades()))
    combo.pack(side='left', padx=(10, 6))
    ttk.Button(controles, text='pasta…', style='Sec.TButton', cursor='hand2',
               command=lambda: destino.set(filedialog.askdirectory() or destino.get())).pack(side='left')
    livre = ttk.Label(controles, style='Apagado.TLabel')
    livre.pack(side='left', padx=10)
    botao = ttk.Button(controles, style='Play.TButton', cursor='hand2', width=12)
    botao.pack(side='right')

    andamento = ttk.Frame(root, padding=(24, 12, 24, 0))
    andamento.pack(fill='x')
    status = ttk.Label(andamento, text='pronto para baixar', foreground=COR['ambar'], font=('Consolas', 10))
    status.pack(anchor='w')
    barra = ttk.Progressbar(andamento)
    barra.pack(fill='x', pady=(6, 0))

    quadro_log, log = caixa_texto(root, font=('Consolas', 9), height=4, state='disabled')
    log.config(fg=COR['apagado'])
    quadro_log.pack(fill='x', padx=24, pady=(12, 20))

    def atualizar_botao():
        if rodando[0]:
            botao.config(text='■  PARAR', state='normal')
        else:
            pronto = destino.get() and ler_lista(texto.get('1.0', 'end'))
            botao.config(text='▶  BAIXAR', state='normal' if pronto else 'disabled')

    def mudou_destino(*_):
        try:
            livre.config(text=f'{shutil.disk_usage(destino.get()).free / 1e9:.1f} GB livres')
        except OSError:
            livre.config(text='')
        atualizar_botao()

    atual = [None]  # None = abrindo: ainda não tem lista carregada pra salvar

    def mudou_modo(*_):
        if rodando[0]:  # não troca no meio do download
            modo.set(atual[0])
            return
        if atual[0]:
            salvar_arquivo(atual[0], texto.get('1.0', 'end-1c'))
        atual[0] = modo.get()
        cfg = MODOS[atual[0]]
        for w in legenda.winfo_children():
            w.destroy()
        for rotulo, cor in cfg['legenda']:
            ttk.Label(legenda, text=rotulo, foreground=COR[cor], font=(FONTE, 10, 'bold')).pack(side='left', padx=(0, 16))
        dica.config(text=cfg['dica'])
        if atual[0] == 'musica':
            qualidade.pack_forget()
            dica.pack(anchor='w')
        else:
            dica.pack_forget()
            qualidade.pack(anchor='w')
        texto.delete('1.0', 'end')
        texto.insert('1.0', ler_arquivo(atual[0]))
        texto.edit_reset()
        colorir()

    def clique():
        if rodando[0]:
            parar.set()
            botao.config(text='parando…', state='disabled')
            return
        itens = ler_lista(texto.get('1.0', 'end'))
        salvar_arquivo(modo.get(), texto.get('1.0', 'end-1c'))
        parar.clear()
        rodando[0] = True
        atualizar_botao()
        log.config(state='normal')
        log.delete('1.0', 'end')
        log.config(state='disabled')

        def trabalhar():
            try:
                baixar(itens, destino.get(), fila, modo.get(), altura.get(), parar)
            except Exception as e:
                fila.put(('fim', f'Erro: {e}'))

        threading.Thread(target=trabalhar, daemon=True).start()

    def escrever_log(msg):
        log.config(state='normal')
        log.insert('end', msg + '\n')
        log.see('end')
        log.config(state='disabled')

    def atualizar():
        while not fila.empty():
            msg = fila.get()
            if isinstance(msg, str):
                escrever_log(msg)
            elif msg[0] == 'progresso':
                _, valor, maximo, texto_status = msg
                barra.config(maximum=maximo, value=valor)
                status.config(text=texto_status)
            else:  # ('fim', texto[, pasta pra abrir])
                status.config(text=msg[1])
                escrever_log(msg[1])
                rodando[0] = False
                atualizar_botao()
                mudou_destino()
                if len(msg) > 2 and os.name == 'nt':
                    os.startfile(msg[2])
        root.after(200, atualizar)

    destino.trace_add('write', mudou_destino)
    modo.trace_add('write', mudou_modo)
    botao.config(command=clique)
    root.protocol('WM_DELETE_WINDOW', lambda: (salvar_arquivo(modo.get(), texto.get('1.0', 'end-1c')),
                                               root.destroy()))
    mudou_modo()
    pens = pen_drives()
    if pens:  # pen drive plugado: já vem escolhido
        destino.set(pens[0])
    if os.name == 'nt':
        try:
            barra_de_titulo_escura(root)
        except (AttributeError, OSError):
            pass  # Windows antigo: fica a barra padrão
    atualizar()
    root.mainloop()


if __name__ == '__main__':
    main()
