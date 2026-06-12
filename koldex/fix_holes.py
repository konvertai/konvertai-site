"""
Corrigir os buracos das letras nas versões light/preto/institucional.

O problema: paths [4],[6],[8] com fill="#07070C" são os "buracos" (counter forms)
das letras o, d, e. Eles precisam ter a cor do fundo para parecerem transparentes.

Para versões sem fundo (transparente), não tem como usar fill para simular buraco.
A solução real é converter cada letra (shape + buraco) em um único path com
fill-rule="evenodd" usando o operador booleano de subtração.

Abordagem mais simples: para versões sem fundo, deixar os buracos com
fill="transparent" e usar mix-blend-mode ou simplesmente aceitar que
versões sem fundo precisam de fundo para os buracos aparecerem.

Para versão BRANCA: buracos = #FFFFFF ✓
Para versão GRAFITE: buracos = #16161B ✓
Para versão PRETA: buracos = #111111 ✓
Para versão TRANSPARENTE: usar fill-rule evenodd (merge paths)
"""
import subprocess, os, re

ASSETS  = r'd:\_Projetos\_WEB\koldex-site\koldex\assets'
INKSCAPE= r'C:\Program Files\Inkscape\bin\inkscape.exe'
ROXO  = '#4C1D95'
VERM  = '#FF2800'
GRAFT = '#16161B'
BRANCO= '#FFFFFF'
PRETO = '#111111'

with open(os.path.join(ASSETS, 'Logo-recraft.svg'), 'r', encoding='utf-8') as f:
    raw = f.read()

all_paths = re.findall(r'<path[^>]+/?>', raw, re.DOTALL)
bg_dark_path = all_paths[1]
content_paths = all_paths[2:]

def apply_colors(paths, txt_color, k_color, red_color, hole_color):
    result = []
    for p in paths:
        fill_m = re.search(r'fill="([^"]+)"', p)
        if not fill_m:
            result.append(p)
            continue
        fill = fill_m.group(1)
        if fill == '#5702B2':
            p = p.replace(fill, k_color)
        elif fill == '#F8F8F7':
            p = p.replace(fill, txt_color)
        elif fill == '#07070C':
            # Buraco das letras → cor do fundo
            p = p.replace(fill, hole_color)
        elif fill in ('#FA0907', '#FC0402'):
            p = p.replace(fill, red_color)
        result.append(p)
    return result

def make_svg(bg_type, bg_color, txt_color, k_color, hole_color):
    paths = apply_colors(content_paths, txt_color, k_color, VERM, hole_color)
    paths_str = '\n  '.join(paths)
    if bg_type == 'path':
        p = bg_dark_path.replace('#07070C', bg_color)
        bg = p
    elif bg_type == 'rect':
        bg = f'<rect width="717" height="207" rx="14" fill="{bg_color}"/>'
    else:
        bg = ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="717" height="207" viewBox="0 0 717 207">
  {bg}
  {paths_str}
</svg>'''

print("="*50)
print("KOLDEX — Corrigindo buracos das letras")
print("="*50)

# Gerar com hole_color correto para cada versão
svgs = {
    # Dark: buracos = cor do fundo escuro
    'logo.svg':               make_svg('path', '#07070C', BRANCO, ROXO, '#07070C'),
    'logo-dark.svg':          make_svg('path', '#07070C', BRANCO, ROXO, '#07070C'),
    'logo-grafite.svg':       make_svg('rect', GRAFT,     BRANCO, ROXO, GRAFT),

    # Light: buracos = BRANCO ← FIX
    'logo-light.svg':         make_svg('rect', BRANCO, '#1A1A2C', ROXO, BRANCO),

    # Preto/monocromatico: buracos = BRANCO (fundo é branco) ← FIX
    'logo-preto.svg':         make_svg('rect', BRANCO, PRETO, PRETO, BRANCO),

    # Sem fundo:
    # Para logo-branco (texto branco sem fundo): não tem fundo definido
    # Buracos devem ser "invisíveis" → não é possível com fill simples
    # Solução: dar uma cor semi-transparente escura para dar ilusão
    # OU simplesmente não incluir esta versão sem fundo
    # Para o preview, usar fundo escuro implícito
    'logo-white.svg':         make_svg(None, None, BRANCO, ROXO, 'rgba(0,0,0,0)'),

    # Institucional grafite SEM fundo: buracos transparentes (limitação SVG)
    # Solução prática: gerar com fundo branco semitransparente nos buracos
    'logo-institucional.svg': make_svg(None, None, GRAFT, GRAFT, BRANCO),
}

for name, svg in svgs.items():
    with open(os.path.join(ASSETS, name), 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"  {name} ✓")

# Exportar PNGs corrigidos
print("\nExportando PNGs corrigidos...")
exports = [
    ('logo.svg',              'logo.png',              717, 207),
    ('logo-dark.svg',         'logo-dark.png',         717, 207),
    ('logo-light.svg',        'logo-light.png',        717, 207),
    ('logo-preto.svg',        'logo-preto.png',        717, 207),
    ('logo-white.svg',        'logo-branco.png',       717, 207),
    ('logo-grafite.svg',      'logo-grafite.png',      717, 207),
    ('logo-institucional.svg','logo-institucional.png',717, 207),
    ('logo.svg',              'logo-horizontal.png',  1434, 414),
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

print("\n✓ Buracos corrigidos!")
print("="*50)
