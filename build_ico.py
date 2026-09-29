"""Gera htube.ico a partir do mesmo desenho do ícone da janela. Uso: python build_ico.py (precisa de Pillow)."""
from PIL import Image, ImageDraw
from htube import CASSETE, CANTOS, COR

img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
for cor, (x1, y1, x2, y2) in CASSETE:
    d.rectangle((x1, y1, x2 - 1, y2 - 1), fill=COR[cor])  # PhotoImage.put exclui a borda final
for canto in CANTOS:
    img.putpixel(canto, (0, 0, 0, 0))
# pixel art: amplia sem suavizar
img.resize((256, 256), Image.NEAREST).save('htube.ico', sizes=[(16, 16), (32, 32), (48, 48), (256, 256)])
