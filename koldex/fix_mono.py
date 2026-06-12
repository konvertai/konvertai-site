"""
Versões monocromáticas: sem vermelho no x, tudo em uma cor.
- logo-preto.svg/png: fundo branco, tudo #111111
- logo-institucional.svg/png: sem fundo, tudo grafite #16161B
- logo-cinza.svg/png: sem fundo, tudo cinza elegante #4A5568
"""
import subprocess, os, re

ASSETS  = r'd:\_Projetos\_WEB\koldex-site\koldex\assets'
INKSCAPE= r'C:\Program Files\Inkscape\bin\inkscape.exe'

BRANCO = '#FFFFFF'
PRETO  = '#111111'
GRAFT  = '#16161B'
CINZA  = '#4A5568'

with open(os.path.join(ASSETS, 'Logo-recraft.svg'), 'r', encoding='utf-8') as f:
    raw = f.read()

all_paths = re.findall(r'<path[^>]+/?>', raw, re.DOTALL)
bg_dark_path = all_paths[1]
content_paths = all_paths[2:]

def make_mono(txt_color, hole_color, bg_type=None, bg_color=None):
    """
    Versão monocromática: K, texto e x todos na mesma cor.
    O vermelho do x é substituído pela mesma cor do texto.
    """
    result = []
    for p in content_paths:
        fill_m = re.search(r'fill="([^"]+)"', p)
        if not fill_m:
            result.append(p)
            continue
        fill = fill_m.group(1)
        if fill == '#5702B2':            # K roxo → cor mono
            p = p.replace(fill, txt_color)
        elif fill == '#F8F8F7':          # texto branco → cor mono
            p = p.replace(fill, txt_color)
        elif fill == '#07070C':          # buraco das letras → cor do fundo
            p = p.replace(fill, hole_color)
        elif fill in ('#FA0907', '#FC0402'):  # vermelho x → cor mono (sem vermelho!)
            p = p.replace(fill, txt_color)
        result.append(p)

    paths_str = '\n  '.join(result)

    if bg_type == 'rect':
        bg = f'<rect width="717" height="207" rx="14" fill="{bg_color}"/>'
    else:
        bg = ''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="717" height="207" viewBox="0 0 717 207">
  {bg}
  {paths_str}
</svg>'''

print("="*50)
print("KOLDEX — Versões monocromáticas (sem vermelho)")
print("="*50)

svgs = {
    # Fundo branco, tudo preto
    'logo-preto.svg':           make_mono(PRETO, BRANCO, 'rect', BRANCO),
    # Sem fundo, tudo grafite
    'logo-institucional.svg':   make_mono(GRAFT, BRANCO, None),
    # Sem fundo, tudo cinza elegante
    'logo-cinza.svg':           make_mono(CINZA, BRANCO, None),
}

for name, svg in svgs.items():
    with open(os.path.join(ASSETS, name), 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"  {name} ✓")

print("\nExportando PNGs...")
exports = [
    ('logo-preto.svg',         'logo-preto.png',         717, 207),
    ('logo-institucional.svg', 'logo-institucional.png', 717, 207),
    ('logo-cinza.svg',         'logo-cinza.png',         717, 207),
    # Alta res também
    ('logo-preto.svg',         'logo-preto-hd.png',     1434, 414),
]

for svg_n, png_n, w, h in exports:
    sp = os.path.join(ASSETS, svg_n)
    pp = os.path.join(ASSETS, png_n)
    subprocess.run([INKSCAPE, sp, '--export-type=png',
                    f'--export-filename={pp}',
                    f'--export-width={w}', f'--export-height={h}',
                    '--export-background-opacity=0'],
                   capture_output=True, text=True, timeout=30)
    kb = os.path.getsize(pp)//1024 if os.path.exists(pp) else 0
    print(f"  {png_n} ({w}x{h}) — {kb}KB {'✓' if kb>0 else 'FALHOU'}")

print("\n✓ Versões mono prontas!")
print("="*50)
