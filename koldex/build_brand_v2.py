"""
KOLDEX — Brand Assets v2
Símbolo K reconstruído com geometria precisa baseada na referência:
- Haste vertical estreita à esquerda
- Braço superior: diagonal slim, largo na haste, estreito na ponta → gradiente roxo
- Braço inferior: diagonal slim, vermelho sólido
- Espaço negativo: triângulo escuro entre os braços
- Efeito de sobreposição (layered) que cria profundidade
"""
import subprocess, os, shutil

ASSETS = r'd:\_Projetos\_WEB\koldex-site\koldex\assets'
INKSCAPE = r'C:\Program Files\Inkscape\bin\inkscape.exe'

ROXO       = '#4C1D95'
ROXO_MID   = '#6B21A8'  # roxo médio para gradiente
VERMELHO   = '#FF2800'
GRAFITE    = '#16161B'
BRANCO     = '#FFFFFF'

def k_symbol_svg(bg_color=GRAFITE, border_radius=0):
    """
    K Koldex — geometria refinada.
    
    Analisando a referência:
    - Canvas: 512x512
    - Haste vertical: ~x 72-130, full height (y 48-464)
    - Braço superior (roxo): sai do centro-direita da haste,
      vai em diagonal acentuada até o canto superior-direito
      Forma: trapézio com base na haste e ponta fina no topo-direito
    - Braço inferior (vermelho): sai abaixo do centro,
      vai em diagonal para baixo-direita
      Forma: paralelogramo estreito
    - Entre os braços: espaço negativo (triângulo) com cor do fundo
    - Sobreposição sutil: braço superior "sobre" o inferior
    """
    
    # Fundo
    if bg_color:
        if border_radius > 0:
            bg = f'<rect width="512" height="512" rx="{border_radius}" fill="{bg_color}"/>'
        else:
            bg = f'<rect width="512" height="512" fill="{bg_color}"/>'
    else:
        bg = ''
    
    cut = bg_color if bg_color else GRAFITE

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <!-- Gradiente roxo: da haste (baixo-esquerda) até a ponta (cima-direita) -->
    <linearGradient id="grad-top" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#4C1D95"/>
      <stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>
    <!-- Sombra interna para efeito de profundidade -->
    <filter id="inner-shadow">
      <feDropShadow dx="-4" dy="4" stdDeviation="8" flood-color="#000" flood-opacity="0.4"/>
    </filter>
  </defs>

  <!-- Fundo -->
  {bg}

  <!-- ═══ HASTE VERTICAL ═══ -->
  <!-- Estreita, do topo ao fundo, roxo escuro -->
  <rect x="72" y="48" width="68" height="416" fill="{ROXO}"/>

  <!-- ═══ BRAÇO SUPERIOR (roxo/gradiente) ═══ -->
  <!-- Sai da haste no centro (y≈256), vai para cima-direita -->
  <!-- Base larga na haste, afunila até virar uma linha fina na ponta -->
  <polygon points="
    140,48
    440,48
    440,170
    140,270
  " fill="url(#grad-top)"/>

  <!-- ═══ BRAÇO INFERIOR (vermelho) ═══ -->
  <!-- Sai da haste abaixo do centro, vai para baixo-direita -->
  <polygon points="
    140,290
    440,420
    440,464
    140,344
  " fill="{VERMELHO}"/>

  <!-- ═══ ESPAÇO NEGATIVO entre os braços ═══ -->
  <!-- Triângulo que cria o "corte" sofisticado entre os braços -->
  <polygon points="
    140,270
    440,170
    440,250
    140,344
  " fill="{cut}"/>

  <!-- ═══ SOBREPOSIÇÃO: sombra no braço inferior para profundidade ═══ -->
  <polygon points="
    140,290
    200,290
    200,310
    140,310
  " fill="rgba(0,0,0,0.2)"/>
</svg>'''


def k_logo_svg(bg_color=GRAFITE, text_color=BRANCO, border_radius=0):
    """Logo completa: símbolo + wordmark Koldex."""
    
    if bg_color:
        if border_radius > 0:
            bg = f'<rect width="860" height="200" rx="{border_radius}" fill="{bg_color}"/>'
        else:
            bg = f'<rect width="860" height="200" fill="{bg_color}"/>'
    else:
        bg = ''
    
    cut = bg_color if bg_color else GRAFITE
    
    # Símbolo K escalado para 200px de altura, posicionado à esquerda com padding
    s = 160 / 512  # scale: 160px de altura para o símbolo dentro da logo
    ox = 20        # offset x
    oy = 20        # offset y (padding vertical)
    
    def p(x, y): return f"{ox + x*s:.1f},{oy + y*s:.1f}"
    
    haste    = f'<rect x="{ox+72*s:.1f}" y="{oy+48*s:.1f}" width="{68*s:.1f}" height="{416*s:.1f}" fill="{ROXO}"/>'
    arm_top  = f'<polygon points="{p(140,48)} {p(440,48)} {p(440,170)} {p(140,270)}" fill="url(#logo-grad-top)"/>'
    arm_bot  = f'<polygon points="{p(140,290)} {p(440,420)} {p(440,464)} {p(140,344)}" fill="{VERMELHO}"/>'
    neg_space= f'<polygon points="{p(140,270)} {p(440,170)} {p(440,250)} {p(140,344)}" fill="{cut}"/>'
    
    # Largura do símbolo ≈ (440-72)*s + ox*2 ≈ 115 + 40 = ~155
    text_x = ox + 440*s + 20  # logo text começa após o símbolo
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="200" viewBox="0 0 860 200">
  <defs>
    <linearGradient id="logo-grad-top" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#4C1D95"/>
      <stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>
  </defs>
  {bg}
  {haste}
  {arm_top}
  {arm_bot}
  {neg_space}
  <text x="{text_x:.0f}" y="138"
    font-family="Space Grotesk, Inter, -apple-system, sans-serif"
    font-size="108"
    font-weight="700"
    fill="{text_color}"
    letter-spacing="-2">Koldex</text>
</svg>'''


# ══════════════════════════════════════════════
print("=" * 50)
print("KOLDEX v2 — Gerando brand assets")
print("=" * 50)

# SVGs do símbolo
svgs = {
    'icon.svg':             k_symbol_svg(GRAFITE, 0),
    'icon-rounded.svg':     k_symbol_svg(GRAFITE, 80),
    'icon-dark.svg':        k_symbol_svg(GRAFITE, 80),
    'icon-light.svg':       k_symbol_svg(BRANCO, 0),
    'icon-transparent.svg': k_symbol_svg(None, 0),
    'favicon.svg':          k_symbol_svg(GRAFITE, 0),
}

# SVGs da logo
logo_svgs = {
    'logo.svg':       k_logo_svg(GRAFITE, BRANCO),
    'logo-dark.svg':  k_logo_svg(GRAFITE, BRANCO),
    'logo-light.svg': k_logo_svg(BRANCO, GRAFITE),
    'logo-white.svg': k_logo_svg(None, BRANCO),
    'logo-black.svg': k_logo_svg(None, '#000000'),
}

for name, svg in {**svgs, **logo_svgs}.items():
    path = os.path.join(ASSETS, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"  {name} ✓")

# ══════════════════════════════════════════════
print("\nExportando PNGs...")

exports = [
    # símbolo
    ('icon.svg',             'icon.png',              512,  512),
    ('icon-rounded.svg',     'icon-rounded.png',      512,  512),
    ('icon-rounded.svg',     'icon-2000.png',         2000, 2000),
    ('icon-rounded.svg',     'avatar-instagram.png',  320,  320),
    ('icon-rounded.svg',     'avatar-whatsapp.png',   192,  192),
    ('icon-transparent.svg', 'icon-transparent.png',  512,  512),
    ('icon-light.svg',       'icon-light.png',        512,  512),
    ('favicon.svg',          'favicon-48.png',        48,   48),
    # logo
    ('logo.svg',             'logo.png',              860,  200),
    ('logo-dark.svg',        'logo-dark.png',         860,  200),
    ('logo-light.svg',       'logo-light.png',        860,  200),
    ('logo-white.svg',       'logo-white.png',        860,  200),
    ('logo-black.svg',       'logo-black.png',        860,  200),
]

for svg_name, png_name, w, h in exports:
    svg_path = os.path.join(ASSETS, svg_name)
    png_path = os.path.join(ASSETS, png_name)
    cmd = [INKSCAPE, svg_path, '--export-type=png',
           f'--export-filename={png_path}',
           f'--export-width={w}', f'--export-height={h}',
           '--export-background-opacity=0']
    subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    kb = os.path.getsize(png_path)//1024 if os.path.exists(png_path) else 0
    print(f"  {png_name} ({w}x{h}) — {kb}KB {'✓' if kb>0 else 'FALHOU'}")

print("\n✓ Pronto! Abra preview.html para conferir.")
print("=" * 50)
