"""
KOLDEX — Build final conforme Manual de Identidade Visual
Arquivos: logo.svg, logo-dark.svg, logo-light.svg, icon.svg, favicon.svg,
          logo-horizontal.png, logo-vertical.png, logo-preto.png, logo-branco.png,
          avatar-instagram.png, avatar-whatsapp.png, icon.png, favicon-32.png, favicon-48.png

"x": só a perna superior direita em vermelho → usar SVG path inline para o "x"
"""
import subprocess, os, re

ASSETS  = r'd:\_Projetos\_WEB\koldex-site\koldex\assets'
INKSCAPE= r'C:\Program Files\Inkscape\bin\inkscape.exe'

ROXO  = '#4C1D95'
VERM  = '#FF2800'
GRAFT = '#16161B'
BRANCO= '#FFFFFF'

# ── Ler e processar o SVG do Recraft ──
with open(os.path.join(ASSETS, 'k-symbol-recraft.svg'), 'r', encoding='utf-8') as f:
    raw = f.read()

paths = re.findall(r'<path[^>]+>', raw)
defs_bg_m = re.search(r'(<defs><linearGradient id="gradient_0".*?</defs>)', raw, re.DOTALL)
defs_bg = defs_bg_m.group(1) if defs_bg_m else ''
defs_bg = defs_bg.replace('#000406', '#08021A').replace('#160032', '#100228')

def fix(p):
    p = p.replace('#4F019B', ROXO).replace('#210156', ROXO)
    p = p.replace('#FC0402', VERM)
    p = p.replace('fill="url(#gradient_1)"', f'fill="{ROXO}"')
    return p

k_paths = [fix(paths[i]) for i in [3,4,5,6,7]]
k_str = '\n  '.join(k_paths)

scale = min(512/533, 512/573)
ox = (512-533*scale)/2
oy = (512-573*scale)/2
T512 = f"translate({ox:.2f},{oy:.2f}) scale({scale:.4f})"

kls = 120/573
kT_logo = f"translate(20,20) scale({kls:.4f})"
k_w_logo = 533*kls + 20 + 16  # x start of text

# ── "x" com perna vermelha ──
# O "x" em Space Grotesk é formado por duas diagonais que se cruzam.
# A "perna superior direita" é a diagonal que vai do centro para cima-direita.
# Vou usar dois tspan: "Kolde" + "x" dividido em dois paths inline no SVG.
# Abordagem: "Koldex" mas o "x" usa um SVG path artesanal com duas cores.
# Mais simples e mais preciso: usar textPath ou dois textos sobrepostos.
#
# Estratégia: escrever "Koldex" com cor do texto normalmente,
# depois sobrepor um "x" com clip na perna superior direita em vermelho.
# 
# Na prática: usar duas tags <text> na mesma posição:
# 1. "Koldex" na cor base
# 2. "x" na mesma posição, cor vermelha, com clip-path que mostra só a diagonal sup-dir
# 
# Clip-path para "x" (tamanho ~60px): triângulo superior direito
# Para font-size 86px, o "x" tem ~54px de largura e ~54px de altura
# A perna superior direita vai do centro (27,27 relativo) para canto sup-dir (54,0)
# Clip = triângulo (27,27), (54,0), (54,54) — lado direito superior

def x_accent(tx, ty, fs, txt_color):
    """
    Gera o 'x' com a perna superior direita em vermelho.
    tx, ty = posição base do "x"
    fs = font-size
    txt_color = cor base do texto
    """
    # "x" em fonte ~86px:
    # Largura aproximada: 0.58 * fs ≈ 50px
    # Centro do x: tx + 25, ty - 30 (aprox)
    # Clip triangle: perna sup-dir = triângulo no lado direito superior do x
    xw = fs * 0.58  # largura do "x"
    xh = fs * 0.65  # altura do "x" acima da baseline
    cx = tx + xw / 2  # centro x do glifo
    cy = ty - xh / 2  # centro y do glifo

    # clipPath: triângulo cobre a metade superior direita do x
    clip_id = 'x-clip'
    return f'''
  <!-- x base na cor do texto -->
  <text x="{tx:.0f}" y="{ty}"
    font-family="Space Grotesk, Inter, -apple-system, sans-serif"
    font-size="{fs}" font-weight="700" fill="{txt_color}" letter-spacing="-1">x</text>
  <!-- x perna superior-direita em vermelho via clip -->
  <defs>
    <clipPath id="{clip_id}">
      <polygon points="{cx:.1f},{cy:.1f} {tx+xw:.1f},{ty-xh:.1f} {tx+xw:.1f},{cy:.1f}"/>
    </clipPath>
  </defs>
  <text x="{tx:.0f}" y="{ty}"
    font-family="Space Grotesk, Inter, -apple-system, sans-serif"
    font-size="{fs}" font-weight="700" fill="{VERM}" letter-spacing="-1"
    clip-path="url(#{clip_id})">x</text>'''

def logo_svg(bg_fill=GRAFT, txt=BRANCO, br=14, white_bg=False):
    if white_bg:
        bg = f'<rect width="840" height="160" rx="{br}" fill="{BRANCO}"/>'
        tc = GRAFT
    elif bg_fill:
        bg = f'<rect width="840" height="160" rx="{br}" fill="{bg_fill}"/>'
        tc = txt
    else:
        bg = ''
        tc = txt

    x_tx = k_w_logo + 268  # posição do "x"
    fs = 86

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="160" viewBox="0 0 840 160">
  {defs_bg}
  {bg}
  <g transform="{kT_logo}">{k_str}</g>
  <text x="{k_w_logo:.0f}" y="112"
    font-family="Space Grotesk, Inter, -apple-system, sans-serif"
    font-size="{fs}" font-weight="700" fill="{tc}" letter-spacing="-1">Kolde</text>
  {x_accent(x_tx, 112, fs, tc)}
</svg>'''

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
  {d}{bg}
  <g transform="{T512}">{k_str}</g>
</svg>'''

# ══════════════════════════════════════════════
print("="*50)
print("KOLDEX — Build Final")
print("="*50)

svgs = {
    # Ícones
    'icon.svg':              icon_svg(80, True),
    'icon-dark.svg':         icon_svg(80, True),
    'icon-light.svg':        icon_svg(0, False, True),
    'icon-transparent.svg':  icon_svg(0, False),
    'favicon.svg':           icon_svg(0, True),
    # Logos
    'logo.svg':              logo_svg(GRAFT, BRANCO),
    'logo-dark.svg':         logo_svg(GRAFT, BRANCO),
    'logo-light.svg':        logo_svg(None, None, 14, True),
    'logo-white.svg':        logo_svg(None, BRANCO),
    'logo-black.svg':        logo_svg(None, GRAFT),
    # Versão monocromática (grafite)
    'logo-institucional.svg': logo_svg(None, GRAFT),
}

for name, svg in svgs.items():
    with open(os.path.join(ASSETS, name), 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"  {name} ✓")

# ── PNGs conforme o manual ──
print("\nExportando PNGs...")

exports = [
    # Manual: icon.png, favicon, avatares
    ('icon.svg',             'icon.png',              512,  512),
    ('icon.svg',             'icon-2000.png',         2000, 2000),
    ('icon.svg',             'avatar-instagram.png',  320,  320),  # social-avatar.png
    ('icon.svg',             'avatar-whatsapp.png',   192,  192),
    ('favicon.svg',          'favicon-32.png',         32,   32),
    ('favicon.svg',          'favicon-48.png',         48,   48),
    ('icon-light.svg',       'icon-light.png',        512,  512),
    ('icon-transparent.svg', 'icon-transparent.png',  512,  512),
    # Manual: logo-horizontal.png (logo padrão horizontal)
    ('logo.svg',             'logo-horizontal.png',  1680,  320),  # 2x para qualidade
    ('logo-dark.svg',        'logo-dark.png',         840,  160),
    ('logo-light.svg',       'logo-light.png',        840,  160),
    # Manual: logo-branco.png (branco = texto branco, sem fundo)
    ('logo-white.svg',       'logo-branco.png',       840,  160),
    # Manual: logo-preto.png (monocromático escuro)
    ('logo-black.svg',       'logo-preto.png',        840,  160),
    ('logo-institucional.svg','logo-institucional.png',840, 160),
    # logo-vertical.png: símbolo em cima, texto em baixo
    # (geramos como ícone grande por ora — o vertical requer layout diferente)
    ('icon.svg',             'logo-vertical.png',     512,  512),
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

print(f"\n✓ Todos os arquivos do manual gerados!")
print(f"   Pasta: {ASSETS}")
print("="*50)
