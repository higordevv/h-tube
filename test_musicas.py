from musicas import ler_lista, escolher_bitrate

assert ler_lista('Forro\nhttps://a\n\n https://b \nSertanejo\nhttps://c') == [
    ('Forro', 'https://a'), ('Forro', 'https://b'), ('Sertanejo', 'https://c')]
assert ler_lista('https://x') == [('Outros', 'https://x')]

h = 3600
assert escolher_bitrate(8e9, 70 * h) == 192      # 70h em 8 GB: sobra
assert escolher_bitrate(8e9, 120 * h) == 128     # 120h: ~140 kbps -> 128
assert escolher_bitrate(8e9, 400 * h) is None    # não cabe nem em 64
print('ok')
