# H-Tube
<img src="https://img.shields.io/badge/-Windows-white?style=for-the-badge&logo=windows&logoColor=red"> <img src="https://img.shields.io/badge/-Python-white?style=for-the-badge&logo=python&logoColor=red">

Baixa música (MP3) ou vídeo (MP4) do YouTube direto no pen drive, separado em pastas.

![H-Tube](/.screenshot/htube.png)

## Usar

Baixe o `H-Tube.exe` e abra. Na primeira vez ele baixa o ffmpeg (~80 MB) sozinho.

Ou pelo Python:
```
pip install -r requirements.txt
python htube.py
```

1. Escolha **♫ MÚSICA** ou **▶ VÍDEO** no topo
2. Escreva a lista, uma coisa por linha
3. Escolha o destino (o pen drive plugado já vem escolhido) e clique em **▶ BAIXAR**

```
# Sertanejo
Bruno e Marrone
https://youtu.be/...
https://youtu.be/...

# Forro
Calcinha Preta
https://youtu.be/...
```

- `# Nome` vira pasta numerada pela ordem: `1 Sertanejo`, `2 Forro`
- a linha de baixo vira subpasta (artista); os links abaixo dela vão pra ela
- no vídeo as pastas são opcionais: pode colar só os links. Playlist também funciona

Resultado:
```
D:\Musicas\1 Sertanejo\Bruno e Marrone\01 Bruno E Marrone - Só As Melhores Antigas.mp3
D:\Videos\01 Nome Do Video.mp4
```

### Música
- **Cabe no pen:** mede a duração de tudo e escolhe o maior MP3 que cabe no espaço livre (64 a 192 kbps). Se não couber nem em 64 kbps, avisa e não baixa
- **Tags:** grava título, artista e gênero no MP3 (é o que o som do carro mostra)

### Vídeo
- Qualidade 1080p, 720p, 480p ou 360p (ou a melhor abaixo disso)
- Prefere H.264 + AAC, que toca em TV, som de carro e celular antigo

### Nos dois
- **Título curto:** tira `(Ao Vivo)`, `[HD]`, `| Canal`, `@canal`, `#tags`, emojis e CAIXA ALTA; corta em 60 letras
- **Parar e continuar:** o botão vira **■ PARAR** durante o download. O que já foi baixado fica anotado em `baixados.txt`; clicar de novo continua de onde parou e tenta de novo os que falharam
- As listas ficam salvas em `%LOCALAPPDATA%\H-Tube`

Vídeos com restrição de idade falham e são pulados.

## Desenvolvimento

```
python test_htube.py
```

Gerar o `.exe` (precisa de `pillow` e `pyinstaller`):
```
python build_ico.py
python -m PyInstaller --onefile --windowed --name H-Tube --icon htube.ico htube.py
```
Sai em `dist\H-Tube.exe`.
