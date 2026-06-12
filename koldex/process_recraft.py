"""
KOLDEX — Processar SVG do Recraft e gerar todos os brand assets.
"""
import subprocess, os, re

ASSETS  = r'd:\_Projetos\_WEB\koldex-site\koldex\assets'
INKSCAPE= r'C:\Program Files\Inkscape\bin\inkscape.exe'

ROXO_ESC = '#4C1D95'
VERMELHO = '#FF2800'
GRAFITE  = '#16161B'
BG_DARK  = '#120B2A'
BRANCO   = '#FFFFFF'

print("="*50)
print("KOLDEX — Processando SVG do Recraft")
print("="*50)

with open(os.path.join(ASSETS, 'k-symbol-recraft.svg'), 'r', encoding='utf-8') as f:
    raw = f.read()

# Extrair gradientes do Recraft e adaptar para cores oficiais
# gradient_0: fundo escuro (manter similar)
# gradient_1: roxo do K → ajustar para paleta oficial

# Extrair todos os paths
paths = re.findall(r'<path[^/]*/>', raw, re.DOTALL)
if not paths:
    paths = re.findall(r'<path[^>]+/>', raw, re.DOTALL)
if not paths:
    # Tentar formato diferente
    paths = re.findall(r'<path[^>]+>', raw)

print(f"Paths: {len(paths)}")

# ViewBox original: 0 0 533 573
# Vamos normalizar para 512x512 via transform/scale

# Índices:
# [0] #EEE → fundo branco SKIP
# [1] gradient_0 → fundo arredondado dark KEEP para versão dark
# [2] #BFBDBE → borda SKIP
# [3] #4F019B → K roxo KEEP
# [4] #210156 → K roxo escuro KEEP
# [5] gradient_1 → K gradiente KEEP
# [6] #4F019B → K roxo KEEP
# [7] #FC0402 → vermelho KEEP → mudar para #FF2800

def fix_colors(path_str):
    """Corrigir cores do Recraft para cores oficiais."""
    # Manter gradientes originais (são bons) mas ajustar vermelho
    path_str = path_str.replace('#FC0402', VERMELHO)
    path_str = path_str.replace('#FC0402', VERMELHO)
    return path_str

# Extrair defs (gradientes)
defs_raw = re.findall(r'<defs>.*?</defs>', raw, re.DOTALL)
defs_str = '\n'.join(defs_raw)

# Ajustar gradiente_0 para fundo mais escuro/profundo
defs_str = defs_str.replace('#000406', '#0A0118')
defs_str = defs_str.replace('#160032', '#120B2A')
# Manter gradient_1 (roxo) como está (ficou bom)

# Paths do K symbol (índices 3,4,5,6,7)
k_paths = [fix_colors(paths[i]) for i in [3, 4, 5, 6, 7]]
bg_path = paths[1]  # fundo arredondado

k_paths_str = '\n  '.join(k_paths)

# Scale para 512x512: original é 533x573
# scale_x = 512/533 ≈ 0.9606, scale_y = 512/573 ≈ 0.8936
# Para manter proporção e centralizar, usamos uniform scale
# scale_uniform = min(512/533, 512/573) = 512/573 ≈ 0.8936
# Offset x para centralizar: (512 - 533*0.8936)/2 ≈ (512-476.3)/2 ≈ 17.8
sx = 512/533
sy = 512/573
scale = min(sx, sy)  # 0.8936
ox = (512 - 533*scale) / 2  # centralizar horizontalmente
oy = (512 - 573*scale) / 2  # centralizar verticalmente

transform = f"translate({ox:.2f},{oy:.2f}) scale({scale:.4f})"

def make_icon_svg(include_bg=True, bg_color=BG_DARK, border_radius=80, bg_white=False):
    """Gerar SVG do ícone."""
    if bg_white:
        bg_el = f'<rect width="512" height="512" rx="{border_radius}" fill="{BRANCO}"/>'
        bg_defs = defs_str
    elif include_bg:
        # Usar fundo arredondado do Recraft (gradient_0) + ajuste de border radius
        bg_el = f'''<rect width="512" height="512" rx="{border_radius}" fill="url(#gradient_0)"/>'''
        bg_defs = defs_str
    else:
        bg_el = ''
        bg_defs = defs_str

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  {bg_defs}
  {bg_el}
  <g transform="{transform}">
    {k_paths_str}
  </g>
</svg>'''


def make_logo_svg(bg_color=GRAFITE, text_color=BRANCO, border_radius=14, bg_white=False):
    """Gerar logo: símbolo K + wordmark Koldex."""
    # Canvas: 840x160
    # K symbol: altura 120px (scale = 120/573 ≈ 0.2094)
    # Posição: padding 20px
    
    k_scale = 120 / 573
    k_ox = 20
    k_oy = 20
    k_transform = f"translate({k_ox},{k_oy}) scale({k_scale:.4f})"
    
    if bg_white:
        bg_el = f'<rect width="840" height="160" rx="{border_radius}" fill="{BRANCO}"/>'
    elif bg_color:
        bg_el = f'<rect width="840" height="160" rx="{border_radius}" fill="{bg_color}"/>'
    else:
        bg_el = ''
    
    # Largura do K na logo: 533 * k_scale ≈ 112px
    k_width = 533 * k_scale + k_ox
    text_x = k_width + 16
    
    # Wordmark: "Kolde" + "x" vermelho
    wordmark = f'''<text x="{text_x:.0f}" y="112"
    font-family="Space Grotesk, Inter, -apple-system, sans-serif"
    font-size="86" font-weight="700" fill="{text_color}"
    letter-spacing="-1">Kolde</text>
  <text x="{text_x + 268:.0f}" y="112"
    font-family="Space Grotesk, Inter, -apple-system, sans-serif"
    font-size="86" font-weight="700" fill="{VERMELHO}"
    letter-spacing="-1">x</text>'''
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="160" viewBox="0 0 840 160">
  {defs_str}
  {bg_el}
  <g transform="{k_transform}">
    {k_paths_str}
  </g>
  {wordmark}
</svg>'''


# ── Gerar SVGs ──
print("\nGerando SVGs...")

svgs = {
    'icon.svg':              make_icon_svg(True, BG_DARK, 80),
    'icon-dark.svg':         make_icon_svg(True, BG_DARK, 80),
    'icon-light.svg':        make_icon_svg(False, bg_white=True, border_radius=0),
    'icon-transparent.svg':  make_icon_svg(include_bg=False, border_radius=0),
    'icon-square.svg':       make_icon_svg(True, BG_DARK, 0),
    'favicon.svg':           make_icon_svg(True, BG_DARK, 0),
    'logo.svg':              make_logo_svg(GRAFITE, BRANCO),
    'logo-dark.svg':         make_logo_svg(GRAFITE, BRANCO),
    'logo-light.svg':        make_logo_svg(bg_white=True, text_color=GRAFITE),
    'logo-white.svg':        make_logo_svg(bg_color=None, text_color=BRANCO),
    'logo-black.svg':        make_logo_svg(bg_color=None, text_color='#111111'),
}

for name, svg in svgs.items():
    path = os.path.join(ASSETS, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"  {name} ✓")

# ── Exportar PNGs ──
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

print(f"\n✓ Pronto! Abra preview.html para conferir.")
print("="*50)
