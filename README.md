# Htube(Youtube Downloader)
<img src="https://img.shields.io/badge/-Linux-white?style=for-the-badge&logo=Linux&logoColor=red"> <img src="https://img.shields.io/badge/-Windows-white?style=for-the-badge&logo=windows&logoColor=red"> <img src="https://img.shields.io/badge/-Python-white?style=for-the-badge&logo=python&logoColor=red"> <img src="https://img.shields.io/badge/-Terminal-white?style=for-the-badge&logo=GNU%20Bash&logoColor=red">

Dois jeitos de usar:

- **`htube.py`**: terminal, baixa um vídeo ou playlist na resolução escolhida
- **`musicas.py`**: janela, baixa uma lista de músicas em MP3 direto no pen drive, separadas por gênero e artista

### setup
<b>Instalação de Modulos</b>: ```pip3 install -r requirements.txt```<br>
<b>Modulos</b>: ```yt-dlp```, ```colorama``` e ```static-ffmpeg``` (baixa o ffmpeg sozinho se ele não estiver instalado)<br>

## Terminal
![imagem](/.screenshot/screenshot.png)

```python3 htube.py```

Cole a url, escolha a pasta e a resolução. Acima de 360p precisa do ```ffmpeg``` pra juntar vídeo e áudio.

## Músicas pro pen drive
![musicas](/.screenshot/musicas.png)

```python3 musicas.py```

Escreva a lista, uma coisa por linha:

```
# Sertanejo
Bruno e Marrone
https://youtu.be/...
https://youtu.be/...

# Forro
Calcinha Preta
https://youtu.be/...
```

- `# Nome` vira pasta de gênero, numerada pela ordem: `1 Sertanejo`, `2 Forro`
- a linha de baixo é o artista (subpasta); os links abaixo dele vão pra ela
- link direto embaixo do gênero, sem artista, fica na pasta do gênero

Escolha o pen drive e clique em **GRAVAR**. Resultado:

```
E:\Musicas\1 Sertanejo\Bruno e Marrone\01 Bruno E Marrone - Só As Melhores Antigas.mp3
```

- **Cabe no pen:** antes de baixar ele mede a duração de tudo e escolhe o maior bitrate MP3 que cabe no espaço livre (64 a 192 kbps). Se não couber nem em 64 kbps, avisa e não baixa
- **Título curto:** tira `(Ao Vivo)`, `[HD]`, `| Canal`, `@canal`, `#tags`, emojis e CAIXA ALTA; corta em 60 letras
- **Tags:** grava título, artista e gênero no MP3 (é o que o som do carro mostra)
- **Retoma:** anota o que já baixou em `Musicas\baixados.txt`; se parar no meio, é só clicar de novo
- A lista fica salva em `musicas.txt` (fora do git)

Vídeos com restrição de idade falham e são pulados.

### teste
```python3 test_musicas.py```
