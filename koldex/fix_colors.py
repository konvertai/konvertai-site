"""
Aplicar cores oficiais do Manual de Identidade Visual Koldex:
- ROXO PRINCIPAL #4C1D95 → em TODOS os shapes roxos do K
- VERMELHO FERRARI #FF2800 → shape vermelho
- Remover todos os gradientes de cor do K (manter só o gradiente de fundo)
"""
import subprocess, os, re

ASSETS  = r'd:\_Projetos\_WEB\koldex-site\koldex\assets'
INKSCAPE= r'C:\Program Files\Inkscape\bin\inkscape.exe'

ROXO    = '#4C1D95'  # Roxo Principal — Manual v1.0
VERM    = '#FF2800'  # Vermelho Ferrari — Manual v1.0
GRAFITE = '#16161B'
BRANCO  = '#FFFFFF'

print("="*50)
print("KOLDEX — Aplicando cores oficiais")
print("="*50)

with open(os.path.join(ASSETS, 'k-symbol-recraft.svg'), 'r', encoding='utf-8') as f:
    raw = f.read()

# Extrair paths
paths = re.findall(r'<path[^>]+>', raw)

# Extrair APENAS o gradient_0 (fundo escuro) — manter
defs_bg_match = re.search(r'(<defs><linearGradient id="gradient_0".*?</defs>)', raw, re.DOTALL)
defs_bg = defs_bg_match.group(1) if defs_bg_match else ''

# Ajustar cores do fundo para ainda mais escuro
defs_bg = defs_bg.replace('#000406', '#08021A').replace('#160032', '#100228')

# Scale
scale = min(512/533, 512/573)
ox = (512 - 533*scale) / 2
oy = (512 - 573*scale) / 2
transform = f"translate({ox:.2f},{oy:.2f}) scale({scale:.4f})"

# K scale para logo
kls = 120 / 573
k_ox, k_oy = 20, 20
k_transform_logo = f"translate({k_ox},{k_oy}) scale({kls:.4f})"

# Substituir cores:
# [3] #4F019B → ROXO oficial
# [4] #210156 → ROXO oficial  
# [5] gradient_1 → ROXO oficial (trocar fill para cor sólida)
# [6] #4F019B → ROXO oficial
# [7] #FC0402 → VERMELHO oficial

def fix(p):
    p = p.replace('#4F019B', ROXO)
    p = p.replace('#210156', ROXO)
    p = p.replace('#FC0402', VERM)
    # gradient_1 → cor sólida ROXO
    p = p.replace('fill="url(#gradient_1)"', f'fill="{ROXO}"')
    return p

k_paths = [fix(paths[i]) for i in [3, 4, 5, 6, 7]]
k_paths_str = '\n  '.join(k_paths)
bg_path = paths[1]  # fundo gradiente escuro (gradient_0)

def icon_svg(br=80, with_bg=True, white_bg=False):
    if white_bg:
        bg = f'<rect width="512" height="512" rx="{br}" fill="{BRANCO}"/>'
        d = ''
    elif with_bg:
        bg = f'<rect width="512" height="512" rx="{br}" fill="url(#gradient_0)"/>'
        d = defs_bg
    else:
        bg = ''
        d = ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  {d}
  {bg}
  <g transform="{transform}">
    {k_paths_str}
  </g>
</svg>'''

def logo_svg(bg_fill=GRAFITE, txt=BRANCO, br=14, white_bg=False):
    if white_bg:
        bg = f'<rect width="840" height="160" rx="{br}" fill="{BRANCO}"/>'
    elif bg_fill:
        bg = f'<rect width="840" height="160" rx="{br}" fill="{bg_fill}"/>'
    else:
        bg = ''
    k_w = 533 * kls + k_ox
    tx = k_w + 16
    txt_color = GRAFITE if white_bg else txt
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="160" viewBox="0 0 840 160">
  {defs_bg}
  {bg}
  <g transform="{k_transform_logo}">
    {k_paths_str}
  </g>
  <text x="{tx:.0f}" y="112"
    font-family="Space Grotesk, Inter, -apple-system, sans-serif"
    font-size="86" font-weight="700" fill="{txt_color}" letter-spacing="-1">Kolde</text>
  <text x="{tx+268:.0f}" y="112"
    font-family="Space Grotesk, Inter, -apple-system, sans-serif"
    font-size="86" font-weight="700" fill="{VERM}" letter-spacing="-1">x</text>
</svg>'''

# Gerar SVGs
svgs = {
    'icon.svg':             icon_svg(80, True),
    'icon-dark.svg':        icon_svg(80, True),
    'icon-light.svg':       icon_svg(0, False, True),
    'icon-transparent.svg': icon_svg(0, False),
    'favicon.svg':          icon_svg(0, True),
    'logo.svg':             logo_svg(GRAFITE, BRANCO),
    'logo-dark.svg':        logo_svg(GRAFITE, BRANCO),
    'logo-light.svg':       logo_svg(None, None, 14, True),
    'logo-white.svg':       logo_svg(None, BRANCO),
    'logo-black.svg':       logo_svg(None, '#111111'),
}

for name, svg in svgs.items():
    with open(os.path.join(ASSETS, name), 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"  {name} ✓")

# Exportar PNGs
print("\nExportando PNGs...")

exports = [
    ('icon.svg',             'icon.png',              512,  512),
    ('icon.svg',             'icon-2000.png',         2000, 2000),
    ('icon.svg',             'avatar-instagram.png',  320,  320),
    ('icon.svg',             'avatar-whatsapp.png',   192,  192),
    ('icon-light.svg',       'icon-light.png',        512,  512),
    ('icon-transparent.svg', 'icon-transparent.png',  512,  512),
    ('favicon.svg',          'favicon-48.png',         48,   48),
    ('logo.svg',             'logo.png',              840,  160),
    ('logo-dark.svg',        'logo-dark.png',         840,  160),
    ('logo-light.svg',       'logo-light.png',        840,  160),
    ('logo-white.svg',       'logo-white.png',        840,  160),
    ('logo-black.svg',       'logo-black.png',        840,  160),
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

print(f"\n✓ Cores oficiais aplicadas! Confira preview.html")
print("="*50)
