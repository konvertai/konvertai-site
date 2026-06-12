"""
KOLDEX — Brand Assets v3
Geometria correta baseada na referência visual.

O K é composto de 3 shapes:
1. Shape ROXO GRANDE: diagonal do canto sup-esq até baixo-centro (forma de paralelogramo grande)
2. Shape ROXO MÉDIO: faixa diagonal estreita sobreposta, do centro para cima-direita
3. Shape VERMELHO: triângulo/paralelogramo no canto inferior direito

Fundo: gradiente escuro roxo-preto radial
"""
import subprocess, os

ASSETS  = r'd:\_Projetos\_WEB\koldex-site\koldex\assets'
INKSCAPE= r'C:\Program Files\Inkscape\bin\inkscape.exe'

ROXO_ESC = '#2D0B6E'   # roxo escuro base
ROXO_MED = '#5B21B6'   # roxo médio
ROXO_VIB = '#7C3AED'   # roxo vibrante (ponta superior)
VERMELHO = '#FF2800'
BG_ESC   = '#120B2A'   # fundo quase-preto roxo
BG_MED   = '#1E0E3E'   # fundo médio
BRANCO   = '#FFFFFF'
GRAFITE  = '#16161B'

def symbol_svg(bg_type='dark', border_radius=80):
    """
    K Koldex — 3 shapes sobrepostos.

    Canvas 512x512. K centrado com padding ~56px todos os lados.
    
    Analisando referência pixel a pixel:
    
    Shape 1 (roxo grande - base):
      Paralelogramo que forma o corpo principal do K
      Cobre a maior parte: de cima-esquerda descendo até baixo-centro
      Ocupa: (80,60) → (320,60) → (180,452) → (80,452)
      
    Shape 2 (roxo médio/grad - braço sup):
      Faixa estreita diagonal sobreposta ao shape 1
      Vai do centro para cima-direita
      (220,200) → (432,60) → (432,130) → (220,280)
      
    Shape 3 (vermelho - braço inf):
      Triângulo no canto inf-direito
      (220,300) → (380,460) → (220,460)
      
    Overlap/cut:
      Onde shape 2 se encontra com shape 1, há um escurecimento sutil
    """
    
    # Fundo
    if bg_type == 'dark':
        bg = f'''<defs>
    <radialGradient id="bg-grad" cx="40%" cy="35%" r="70%">
      <stop offset="0%" stop-color="{BG_MED}"/>
      <stop offset="100%" stop-color="{BG_ESC}"/>
    </radialGradient>
    <linearGradient id="k-grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6D28D9"/>
      <stop offset="100%" stop-color="#2D0B6E"/>
    </linearGradient>
    <linearGradient id="k-grad2" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#4C1D95"/>
      <stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" rx="{border_radius}" fill="url(#bg-grad)"/>'''
    elif bg_type == 'white':
        bg = f'''<defs>
    <linearGradient id="k-grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6D28D9"/>
      <stop offset="100%" stop-color="#2D0B6E"/>
    </linearGradient>
    <linearGradient id="k-grad2" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#4C1D95"/>
      <stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" rx="{border_radius}" fill="{BRANCO}"/>'''
    else:  # transparent
        bg = f'''<defs>
    <linearGradient id="k-grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6D28D9"/>
      <stop offset="100%" stop-color="#2D0B6E"/>
    </linearGradient>
    <linearGradient id="k-grad2" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#4C1D95"/>
      <stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>
  </defs>'''

    cut = BG_ESC if bg_type == 'dark' else (BRANCO if bg_type == 'white' else 'transparent')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  {bg}

  <!-- Shape 1: Corpo principal roxo (diagonal grande, esq→direita-baixo) -->
  <polygon points="
    84,64
    284,64
    284,108
    156,452
    84,452
  " fill="url(#k-grad1)"/>

  <!-- Shape 2: Braço superior (faixa diagonal estreita, roxo vibrante) -->
  <polygon points="
    232,64
    440,64
    440,140
    232,256
  " fill="url(#k-grad2)"/>

  <!-- Corte/sombra entre shape 1 e 2 (espaço negativo sutil) -->
  <polygon points="
    284,108
    284,64
    232,64
    232,108
  " fill="{cut}" opacity="0.8"/>

  <!-- Shape 3: Braço inferior vermelho (triângulo) -->
  <polygon points="
    232,296
    400,452
    232,452
  " fill="{VERMELHO}"/>

</svg>'''


def logo_svg(bg_type='dark', border_radius=14):
    """Logo: símbolo K + wordmark Koldex (x em vermelho)."""

    if bg_type == 'dark':
        bg_fill = GRAFITE
        txt_color = BRANCO
    elif bg_type == 'white':
        bg_fill = BRANCO
        txt_color = GRAFITE
    else:
        bg_fill = None
        txt_color = BRANCO

    bg_el = ''
    if bg_fill:
        bg_el = f'<rect width="760" height="160" rx="{border_radius}" fill="{bg_fill}"/>'

    # K escalado para 130px altura (s = 130/512 ≈ 0.254)
    s  = 130 / 512
    ox = 24   # padding esq
    oy = 15   # padding top

    def p(x, y):
        return f"{ox + x*s:.1f},{oy + y*s:.1f}"

    k_shapes = f'''
  <defs>
    <linearGradient id="lg1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6D28D9"/>
      <stop offset="100%" stop-color="#2D0B6E"/>
    </linearGradient>
    <linearGradient id="lg2" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#4C1D95"/>
      <stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>
  </defs>
  <!-- Shape 1 -->
  <polygon points="{p(84,64)} {p(284,64)} {p(284,108)} {p(156,452)} {p(84,452)}" fill="url(#lg1)"/>
  <!-- Shape 2 -->
  <polygon points="{p(232,64)} {p(440,64)} {p(440,140)} {p(232,256)}" fill="url(#lg2)"/>
  <!-- Shape 3 vermelho -->
  <polygon points="{p(232,296)} {p(400,452)} {p(232,452)}" fill="{VERMELHO}"/>'''

    # Wordmark: "Koldex" onde "x" é vermelho
    # K symbol width ≈ 440*s + ox + gap = ~136
    tx = ox + 440*s + 20
    ty = 108  # baseline

    wordmark = f'''
  <text x="{tx:.0f}" y="{ty}" font-family="Space Grotesk, Inter, sans-serif"
    font-size="88" font-weight="700" fill="{txt_color}" letter-spacing="-1">Kolde</text>
  <text x="{tx+270:.0f}" y="{ty}" font-family="Space Grotesk, Inter, sans-serif"
    font-size="88" font-weight="700" fill="{VERMELHO}" letter-spacing="-1">x</text>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="160" viewBox="0 0 760 160">
  {bg_el}
  {k_shapes}
  {wordmark}
</svg>'''


# ── Gerar SVGs ──
print("="*50)
print("KOLDEX v3 — Build")
print("="*50)

files = {
    'icon.svg':              symbol_svg('dark', 80),
    'icon-dark.svg':         symbol_svg('dark', 80),
    'icon-light.svg':        symbol_svg('white', 0),
    'icon-transparent.svg':  symbol_svg('transparent', 0),
    'favicon.svg':           symbol_svg('dark', 0),
    'logo.svg':              logo_svg('dark'),
    'logo-dark.svg':         logo_svg('dark'),
    'logo-light.svg':        logo_svg('white'),
    'logo-white.svg':        logo_svg('transparent'),
    'logo-black.svg':        logo_svg('white'),
}

for name, svg in files.items():
    with open(os.path.join(ASSETS, name), 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"  {name} ✓")

# ── Exportar PNGs ──
print("\nExportando PNGs...")

exports = [
    ('icon.svg',             'icon.png',             512,  512),
    ('icon.svg',             'icon-2000.png',         2000, 2000),
    ('icon.svg',             'avatar-instagram.png',  320,  320),
    ('icon.svg',             'avatar-whatsapp.png',   192,  192),
    ('icon-light.svg',       'icon-light.png',        512,  512),
    ('icon-transparent.svg', 'icon-transparent.png',  512,  512),
    ('favicon.svg',          'favicon-48.png',         48,   48),
    ('logo.svg',             'logo.png',              760,  160),
    ('logo-dark.svg',        'logo-dark.png',         760,  160),
    ('logo-light.svg',       'logo-light.png',        760,  160),
    ('logo-white.svg',       'logo-white.png',        760,  160),
    ('logo-black.svg',       'logo-black.png',        760,  160),
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

print(f"\n✓ Abra koldex/assets/preview.html")
print("="*50)
