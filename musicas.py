import ctypes
import os
import queue
import re
import shutil
import string
import threading
import unicodedata
import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp
from yt_dlp.postprocessor import PostProcessor
from yt_dlp.utils import sanitize_filename
from modules.assets.ascii import ascii

LISTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'musicas.txt')
# acima de 192 não ganha nada: o áudio do YouTube já vem comprimido (~130-160 kbps)
BITRATES = [64, 80, 96, 112, 128, 160, 192]
# visor de som de carro antigo: preto quente + âmbar
COR = {'fundo': '#16110d', 'painel': '#221a14', 'borda': '#3a2c20', 'texto': '#f2e3cc',
       'apagado': '#8c7a66', 'ambar': '#ffae1a', 'ambar_escuro': '#c77800',
       'genero': '#ffae1a', 'artista': '#ff6a3d', 'link': '#7d6c5a'}
FONTE = 'Bahnschrift'


def ler_lista(texto):
    """'# Gênero' vira pasta numerada, linha com nome vira artista, links vão pra ela."""
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


def unidades():
    return [f'{l}:\\' for l in string.ascii_uppercase if os.path.exists(f'{l}:\\')]


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


def baixar(itens, unidade, fila):
    if not shutil.which('ffmpeg'):
        fila.put('Preparando ffmpeg...')
        import static_ffmpeg
        static_ffmpeg.add_paths()

    # ponytail: mede tudo de novo a cada execução, inclusive o que já foi baixado;
    # numa retomada o bitrate sai um pouco menor que o necessário
    total = 0
    with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True,
                           'extract_flat': 'in_playlist', 'ignoreerrors': True}) as ydl:
        for i, (_, _, url) in enumerate(itens, 1):
            fila.put(('progresso', i, len(itens), f'Medindo duração  ·  {i} de {len(itens)}'))
            info = ydl.extract_info(url, download=False) or {}
            total += info.get('duration') or sum(e.get('duration') or 0 for e in info.get('entries') or [])

    livre = shutil.disk_usage(unidade).free
    kbps = escolher_bitrate(livre, total)
    if not kbps:
        fila.put(f'ERRO: {total / 3600:.1f}h de música não cabem em {livre / 1e9:.1f} GB livres')
        return
    fila.put(f'{total / 3600:.1f}h de música, {livre / 1e9:.1f} GB livres: MP3 {kbps} kbps '
             f'(~{total * kbps / 8e6:.1f} GB)')

    destino = os.path.join(unidade, 'Musicas')
    faixa, falhas, n = {}, 0, len(itens)
    for i, (genero, artista, url) in enumerate(itens, 1):
        nome = artista or genero
        fila.put(('progresso', i - 1, n, f'Baixando {nome}  ·  {i} de {n}'))

        def baixando(d):
            if d['status'] != 'downloading':
                return
            tamanho = d.get('total_bytes') or d.get('total_bytes_estimate')
            parte = d['downloaded_bytes'] / tamanho if tamanho else 0
            fila.put(('progresso', i - 1 + parte, n, f'Baixando {nome}  ·  {i} de {n}  ·  '
                      f'{parte:.0%}  ·  {(d.get("speed") or 0) / 1e6:.1f} MB/s'))

        def convertendo(d):
            if d['status'] == 'started' and d['postprocessor'] == 'ExtractAudio':
                fila.put(('progresso', i, n, f'Convertendo {nome} pra MP3  ·  {i} de {n}'))

        pasta = os.path.join(destino, *[sanitize_filename(p) for p in (genero, artista) if p])
        faixa[pasta] = faixa.get(pasta, 0) + 1  # numera por pasta: ordem certa no som e sem nome repetido
        opcoes = {
            'format': 'bestaudio/best',
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
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': str(kbps)},
                {'key': 'FFmpegMetadata'},
            ],
        }
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.add_post_processor(Etiquetar(artista, genero), when='pre_process')
            if ydl.download([url]):
                falhas += 1
                fila.put(f'Falhou, pulando: {artista or genero} {url}')
    fila.put(f'Pronto! {len(itens) - falhas} de {len(itens)} baixados.')


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


def icone_cassete():
    """Fita cassete 32x32 desenhada com retângulos, sem arquivo de imagem."""
    img = tk.PhotoImage(width=32, height=32)
    for cor, caixa in ((COR['ambar'], (1, 6, 31, 26)),           # corpo
                       (COR['ambar_escuro'], (8, 22, 24, 26)),   # base
                       (COR['texto'], (4, 8, 28, 14)),           # etiqueta
                       (COR['artista'], (6, 10, 20, 12)),        # risco na etiqueta
                       (COR['fundo'], (8, 16, 24, 21)),          # janela
                       (COR['ambar'], (10, 17, 13, 20)),         # carretel esq.
                       (COR['ambar'], (19, 17, 22, 20))):        # carretel dir.
        img.put(cor, to=caixa)
    for x, y in ((1, 6), (30, 6), (1, 25), (30, 25)):              # cantos arredondados
        img.transparency_set(x, y, True)
    return img


def estilizar(root):
    root.configure(bg=COR['fundo'])
    s = ttk.Style(root)
    s.theme_use('clam')
    s.configure('.', background=COR['fundo'], foreground=COR['texto'], font=(FONTE, 10),
                bordercolor=COR['borda'], troughcolor=COR['fundo'], focuscolor=COR['ambar'])
    s.configure('Apagado.TLabel', foreground=COR['apagado'])
    s.configure('Logo.TLabel', foreground=COR['ambar'], font=('Consolas', 7))
    s.configure('TCombobox', fieldbackground=COR['painel'], background=COR['painel'],
                foreground=COR['texto'], arrowcolor=COR['ambar'], bordercolor=COR['borda'],
                lightcolor=COR['painel'], darkcolor=COR['painel'], padding=6)
    s.map('TCombobox', fieldbackground=[('readonly', COR['painel'])],
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
    s.configure('Horizontal.TProgressbar', background=COR['ambar'], troughcolor=COR['painel'],
                bordercolor=COR['borda'], lightcolor=COR['ambar'], darkcolor=COR['ambar'], thickness=8)
    s.configure('Vertical.TScrollbar', background=COR['borda'], troughcolor=COR['painel'],
                bordercolor=COR['painel'], arrowcolor=COR['apagado'], lightcolor=COR['borda'],
                darkcolor=COR['borda'])
    s.map('Vertical.TScrollbar', background=[('disabled', COR['painel']), ('active', COR['ambar_escuro'])])


def barra_de_titulo_escura(root):
    if os.name != 'nt':
        return
    root.update()
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    r, g, b = (int(COR['fundo'][i:i + 2], 16) for i in (1, 3, 5))
    for atributo, valor in ((20, 1), (35, r | g << 8 | b << 16)):  # modo escuro, cor da barra (Win11)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, atributo, ctypes.byref(ctypes.c_int(valor)), 4)


def main():
    if os.name == 'nt':  # ícone próprio na barra de tarefas em vez do Python
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('htube.musicas')
    root = tk.Tk()
    root.title('H-Tube')
    root.geometry('880x760')
    root.minsize(660, 580)
    estilizar(root)
    icone = icone_cassete()
    root.iconphoto(True, icone)

    topo = ttk.Frame(root, padding=(24, 18, 24, 6))
    topo.pack(fill='x')
    logo = '\n'.join(l.rstrip() for l in ascii[1].splitlines() if '█' in l)
    ttk.Label(topo, text=logo, style='Logo.TLabel', justify='left').pack(side='left')
    ttk.Label(topo, text='fita pro som do carro\nmp3 separado por gênero', style='Apagado.TLabel',
              justify='right').pack(side='right', anchor='s')

    dica = ttk.Frame(root, padding=(24, 10, 24, 6))
    dica.pack(fill='x')
    for rotulo, cor in (('# gênero', 'genero'), ('artista', 'artista'), ('link', 'link')):
        ttk.Label(dica, text=rotulo, foreground=COR[cor], font=(FONTE, 10, 'bold')).pack(side='left', padx=(0, 16))
    ttk.Label(dica, text='uma coisa por linha', style='Apagado.TLabel').pack(side='right')

    quadro, texto = caixa_texto(root, font=('Consolas', 10), height=16, undo=True)
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

    texto.bind('<KeyRelease>', colorir)
    if os.path.exists(LISTA):
        with open(LISTA, encoding='utf-8-sig') as f:  # -sig: ignora BOM do Bloco de Notas
            texto.insert('1.0', f.read())
        colorir()

    controles = ttk.Frame(root, padding=(24, 14, 24, 4))
    controles.pack(fill='x')
    ttk.Label(controles, text='PEN DRIVE', style='Apagado.TLabel', font=(FONTE, 9, 'bold')).pack(side='left')
    # postcommand relista ao abrir, pra pegar o pen drive plugado depois
    unidade = ttk.Combobox(controles, values=unidades(), state='readonly', width=5, font=(FONTE, 11),
                           postcommand=lambda: unidade.config(values=unidades()))
    unidade.pack(side='left', padx=10)
    livre = ttk.Label(controles, style='Apagado.TLabel')
    livre.pack(side='left')
    unidade.bind('<<ComboboxSelected>>', lambda e: livre.config(
        text=f'{shutil.disk_usage(unidade.get()).free / 1e9:.1f} GB livres'))
    botao = ttk.Button(controles, text='▶  GRAVAR', style='Play.TButton', cursor='hand2')
    botao.pack(side='right')

    andamento = ttk.Frame(root, padding=(24, 10, 24, 0))
    andamento.pack(fill='x')
    status = ttk.Label(andamento, text='parado', foreground=COR['ambar'], font=('Consolas', 10))
    status.pack(anchor='w')
    barra = ttk.Progressbar(andamento)
    barra.pack(fill='x', pady=(6, 0))

    quadro_log, log = caixa_texto(root, font=('Consolas', 9), height=6, state='disabled')
    log.config(fg=COR['apagado'])
    quadro_log.pack(fill='both', padx=24, pady=(12, 20))
    fila = queue.Queue()

    def trabalhar(itens, un):
        try:
            baixar(itens, un, fila)
        except Exception as e:
            fila.put(f'ERRO: {e}')

    def iniciar():
        itens = ler_lista(texto.get('1.0', 'end'))
        if not unidade.get() or not itens:
            messagebox.showwarning('H-Tube', 'Escolha o pen drive e coloque pelo menos um link.')
            return
        with open(LISTA, 'w', encoding='utf-8') as f:
            f.write(texto.get('1.0', 'end-1c'))
        botao.config(state='disabled')
        threading.Thread(target=trabalhar, args=(itens, unidade.get()), daemon=True).start()

    def atualizar():
        while not fila.empty():
            msg = fila.get()
            if isinstance(msg, tuple):
                _, valor, maximo, texto_status = msg
                barra.config(maximum=maximo, value=valor)
                status.config(text=texto_status)
                continue
            log.config(state='normal')
            log.insert('end', msg + '\n')
            log.see('end')
            log.config(state='disabled')
            if msg.startswith(('Pronto!', 'ERRO')):
                status.config(text=msg)
                botao.config(state='normal')
        root.after(200, atualizar)

    botao.config(command=iniciar)
    try:
        barra_de_titulo_escura(root)
    except (AttributeError, OSError):
        pass  # Windows antigo: fica a barra padrão
    atualizar()
    root.mainloop()


if __name__ == '__main__':
    main()
