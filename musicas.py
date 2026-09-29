import os
import queue
import shutil
import string
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import yt_dlp
from yt_dlp.utils import sanitize_filename

LISTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'musicas.txt')
# acima de 192 não ganha nada: o áudio do YouTube já vem comprimido (~130-160 kbps)
BITRATES = [64, 80, 96, 112, 128, 160, 192]


def ler_lista(texto):
    """Linha com nome vira pasta, links abaixo dela vão pra essa pasta."""
    itens, pasta = [], 'Outros'
    for linha in texto.splitlines():
        linha = linha.strip()
        if linha.startswith('http'):
            itens.append((pasta, linha))
        elif linha:
            pasta = linha
    return itens


def escolher_bitrate(bytes_livres, segundos):
    kbps = bytes_livres * 0.95 * 8 / 1000 / max(segundos, 1)  # 5% de folga
    cabem = [b for b in BITRATES if b <= kbps]
    return cabem[-1] if cabem else None


def unidades():
    return [f'{l}:\\' for l in string.ascii_uppercase if os.path.exists(f'{l}:\\')]


def baixar(itens, unidade, fila):
    if not shutil.which('ffmpeg'):
        fila.put('Preparando ffmpeg (só na primeira vez)...')
        import static_ffmpeg
        static_ffmpeg.add_paths()

    # ponytail: mede tudo de novo a cada execução, inclusive o que já foi baixado;
    # numa retomada o bitrate sai um pouco menor que o necessário
    total = 0
    with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': 'in_playlist', 'ignoreerrors': True}) as ydl:
        for i, (_, url) in enumerate(itens, 1):
            fila.put(f'Medindo duração {i}/{len(itens)}...')
            info = ydl.extract_info(url, download=False) or {}
            total += info.get('duration') or sum(e.get('duration') or 0 for e in info.get('entries') or [])

    livre = shutil.disk_usage(unidade).free
    kbps = escolher_bitrate(livre, total)
    if not kbps:
        fila.put(f'ERRO: {total / 3600:.1f}h de música não cabem em {livre / 1e9:.1f} GB livres')
        return
    fila.put(f'{total / 3600:.1f}h de música, {livre / 1e9:.1f} GB livres: MP3 {kbps} kbps')

    destino = os.path.join(unidade, 'Musicas')
    for i, (pasta, url) in enumerate(itens, 1):
        fila.put(f'[{i}/{len(itens)}] {pasta}: {url}')
        pasta = sanitize_filename(pasta).replace('%', '%%')
        opcoes = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(destino, pasta, '%(title)s.%(ext)s'),
            'windowsfilenames': True,
            'ignoreerrors': True,
            'quiet': True,
            'noprogress': True,
            'download_archive': os.path.join(destino, 'baixados.txt'),  # pula o que já baixou
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3',
                                'preferredquality': str(kbps)}],
        }
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            if ydl.download([url]):
                fila.put('   falhou, pulando')
    fila.put('Pronto!')


def main():
    root = tk.Tk()
    root.title('H-Tube Músicas')

    ttk.Label(root, text='Nome da pasta numa linha, links embaixo:').pack(anchor='w', padx=8, pady=(8, 0))
    texto = ScrolledText(root, width=80, height=20)
    texto.pack(fill='both', expand=True, padx=8, pady=4)
    if os.path.exists(LISTA):
        with open(LISTA, encoding='utf-8') as f:
            texto.insert('1.0', f.read())

    barra = ttk.Frame(root)
    barra.pack(fill='x', padx=8, pady=4)
    ttk.Label(barra, text='Unidade:').pack(side='left')
    # postcommand relista ao abrir, pra pegar o pen drive plugado depois
    unidade = ttk.Combobox(barra, values=unidades(), state='readonly', width=6,
                           postcommand=lambda: unidade.config(values=unidades()))
    unidade.pack(side='left', padx=4)
    livre = ttk.Label(barra)
    livre.pack(side='left')
    unidade.bind('<<ComboboxSelected>>', lambda e: livre.config(
        text=f'{shutil.disk_usage(unidade.get()).free / 1e9:.1f} GB livres'))
    botao = ttk.Button(barra, text='Baixar')
    botao.pack(side='right')

    log = ScrolledText(root, height=10, state='disabled')
    log.pack(fill='both', padx=8, pady=(0, 8))
    fila = queue.Queue()

    def trabalhar(itens, un):
        try:
            baixar(itens, un, fila)
        except Exception as e:
            fila.put(f'ERRO: {e}')

    def iniciar():
        itens = ler_lista(texto.get('1.0', 'end'))
        if not unidade.get() or not itens:
            messagebox.showwarning('H-Tube', 'Escolha a unidade e coloque pelo menos um link.')
            return
        with open(LISTA, 'w', encoding='utf-8') as f:
            f.write(texto.get('1.0', 'end-1c'))
        botao.config(state='disabled')
        threading.Thread(target=trabalhar, args=(itens, unidade.get()), daemon=True).start()

    def atualizar():
        while not fila.empty():
            msg = fila.get()
            log.config(state='normal')
            log.insert('end', msg + '\n')
            log.see('end')
            log.config(state='disabled')
            if msg == 'Pronto!' or msg.startswith('ERRO'):
                botao.config(state='normal')
        root.after(200, atualizar)

    botao.config(command=iniciar)
    atualizar()
    root.mainloop()


if __name__ == '__main__':
    main()
