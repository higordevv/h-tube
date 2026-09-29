from htube import ler_lista, escolher_bitrate, limpar_titulo, formato_video

assert ler_lista('# Sertanejo\nhttps://s\nBruno\nhttps://a\n\n https://b \n# Brega\nRossi\nhttps://c') == [
    ('1 Sertanejo', '', 'https://s'), ('1 Sertanejo', 'Bruno', 'https://a'),
    ('1 Sertanejo', 'Bruno', 'https://b'), ('2 Brega', 'Rossi', 'https://c')]
assert ler_lista('https://x') == [('', '', 'https://x')]
assert ler_lista('Rossi\n? reginaldo rossi ao vivo') == [('', 'Rossi', 'ytsearch1:reginaldo rossi ao vivo')]

assert limpar_titulo('CALCINHA PRETA - AO VIVO EM SALVADOR (DVD COMPLETO) [HD] | Oficial') == \
    'Calcinha Preta - Ao Vivo Em Salvador'
assert limpar_titulo('Show 🔥 #forro #brega - Parte 1') == 'Show - Parte 1'
assert limpar_titulo('DESEJO DE MENINA - CD RELÍQUIA @IsmaelDivulgacoes') == 'Desejo De Menina - Cd Relíquia'
assert limpar_titulo('Silvanno Salles: As Melhores ⛹️‍♂️ ♪') == 'Silvanno Salles: As Melhores'
assert limpar_titulo('Rosa de Jasmim + Irreverência') == 'Rosa de Jasmim + Irreverência'
assert not limpar_titulo('Heitor Costa - Só As Melhores Do Momento - Pra Tomar Cana - Sei La').endswith('-')
assert limpar_titulo('(Ao Vivo)') == '(Ao Vivo)'  # não sobra nada: mantém o original
assert len(limpar_titulo('palavra ' * 20)) <= 60

h = 3600
assert escolher_bitrate(8e9, 70 * h) == 192      # 70h em 8 GB: sobra
assert escolher_bitrate(8e9, 120 * h) == 128     # 120h: ~140 kbps -> 128
assert escolher_bitrate(8e9, 400 * h) is None    # não cabe nem em 64
assert formato_video(720).startswith('bv*[height<=720][vcodec^=avc1]')
print('ok')
