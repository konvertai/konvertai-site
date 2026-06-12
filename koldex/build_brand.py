"""
KOLDEX — Sistema de geração de brand assets
Cria SVG + PNG de todos os arquivos do manual de identidade visual.

Símbolo: K geométrico
- Haste vertical: roxo #4C1D95
- Braço superior: gradiente #4C1D95 → #FF2800
- Braço inferior: #FF2800 com corte diagonal
- Tipografia: Space Grotesk (Google Fonts)
"""
import subprocess
import os

ASSETS = r'd:\_Projetos\_WEB\koldex-site\koldex\assets'
INKSCAPE = r'C:\Program Files\Inkscape\bin\inkscape.exe'

# ── CORES ──
ROXO = '#4C1D95'
VERMELHO = '#FF2800'
GRAFITE = '#16161B'
BRANCO = '#FFFFFF'

# ── GRADIENTE OFICIAL (135°) ──
# Em SVG, 135° = da esquerda-baixo para direita-cima
# gradientTransform="rotate(135, 0.5, 0.5)" com gradientUnits="objectBoundingBox"

GRAD_DEFS = '''<defs>
  <linearGradient id="grad-brand" x1="0%" y1="100%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#4C1D95"/>
    <stop offset="100%" stop-color="#FF2800"/>
  </linearGradient>
  <linearGradient id="grad-arm-top" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#4C1D95"/>
    <stop offset="100%" stop-color="#FF2800"/>
  </linearGradient>
</defs>'''

# ══════════════════════════════════════════════
# SÍMBOLO K — Geometria
# Canvas: 512x512
# 
# Estrutura (baseada na referência):
#   Haste vertical: retângulo x=80 a x=158, y=40 a y=472
#   Braço superior: diagonal saindo do meio da haste,
#                   vai até o canto superior direito (gradiente)
#   Braço inferior: diagonal saindo do meio, vai para baixo-direita
#                   com corte diagonal na ponta (vermelho)
#   Os braços se cruzam com um "cut" que cria espaço negativo no K
# ══════════════════════════════════════════════

def build_k_symbol(bg_color=None, haste_color=ROXO, arm_top_fill='url(#grad-arm-top)', arm_bot_color=VERMELHO):
    """
    Constrói o símbolo K geométrico.
    
    Geometria observada na referência:
    - Haste: larga, à esquerda, vai do topo ao fundo
    - Braço superior: sai do centro da haste, vai para cima-direita em diagonal
      termina em ponta (triângulo)
    - Braço inferior: sai do centro, vai para baixo-direita
      tem um recorte diagonal na face que dá o visual sofisticado
    - Espaço negativo: entre haste e braços
    """
    
    # Fundo (se houver)
    bg = ''
    if bg_color:
        bg = f'<rect width="512" height="512" fill="{bg_color}"/>'
        if bg_color not in ('#FFFFFF', '#ffffff'):
            bg = f'<rect width="512" height="512" rx="56" fill="{bg_color}"/>'
    
    # ── HASTE VERTICAL ──
    # x: 72 a 162 (largura 90)
    # y: 40 a 472
    haste = f'<rect x="72" y="40" width="90" height="432" fill="{haste_color}"/>'
    
    # ── BRAÇO SUPERIOR ──
    # Parallelogram saindo do centro da haste (y~256) para cima-direita
    # Tem largura uniforme (~80px perpendicular à diagonal)
    # Termina em ponta triangular no canto superior direito
    # 
    # Pontos (sentido horário):
    # A: junção topo da haste (162, 40) — topo da haste
    # B: ponto extremo superior (460, 40) — canto superior
    # C: ponta superior da seta (460, 120) 
    # D: retorna para haste pelo centro
    # O espaço entre haste e braço é o "corte"
    arm_top = f'''<polygon points="
      162,40
      460,40
      460,120
      162,220
      162,40
    " fill="{arm_top_fill}"/>'''
    
    # ── BRAÇO INFERIOR ──
    # Sai do centro-baixo da haste, vai para baixo-direita
    # Termina com ponta diagonal (cut) — não é retangular, tem corte
    # 
    # Pontos:
    arm_bot = f'''<polygon points="
      162,292
      460,472
      460,392
      162,212
      162,292
    " fill="{arm_bot_color}"/>'''
    
    # ── ESPAÇO NEGATIVO (recorte) entre braços ──
    # O "corte" diagonal que dá o visual sofisticado
    # É um triângulo/trapézio que "recorta" o centro do K
    # Usando fill="bg_color" para simular corte, ou clipPath
    cut_color = bg_color if bg_color else GRAFITE
    cut = f'''<polygon points="
      162,220
      370,130
      370,210
      162,292
      162,220
    " fill="{cut_color}"/>'''
    
    return bg, haste, arm_top, arm_bot, cut

def make_symbol_svg(bg_color=None, haste_color=ROXO, arm_fill='url(#grad-arm-top)'):
    """Gerar SVG completo do símbolo."""
    bg, haste, arm_top, arm_bot, cut = build_k_symbol(bg_color, haste_color, arm_fill, VERMELHO)
    
    cut_color = bg_color if bg_color else GRAFITE
    # Recalcular cut com cor correta
    cut = f'''<polygon points="
      162,220
      370,130
      370,210
      162,292
      162,220
    " fill="{cut_color}"/>'''
    
    defs = '''<defs>
  <linearGradient id="grad-arm-top" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#4C1D95"/>
    <stop offset="100%" stop-color="#8B3FD8"/>
  </linearGradient>
</defs>'''
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  {defs}
  {bg}
  {haste}
  {arm_top}
  {arm_bot}
  {cut}
</svg>'''

def make_logo_svg(bg_color=GRAFITE, text_color=BRANCO, wordmark='Koldex'):
    """Gerar logo completa: símbolo + wordmark."""
    
    # Logo tem proporção: símbolo (100%) + wordmark (82% de altura)
    # Canvas: 900x200
    
    defs = '''<defs>
  <linearGradient id="grad-arm-top" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#4C1D95"/>
    <stop offset="100%" stop-color="#8B3FD8"/>
  </linearGradient>
</defs>'''
    
    bg = ''
    if bg_color:
        bg = f'<rect width="900" height="200" fill="{bg_color}"/>'
    
    # Símbolo escalado para 200x200 (scale = 200/512 ≈ 0.39)
    s = 200 / 512
    
    haste = f'<rect x="{72*s:.1f}" y="{40*s:.1f}" width="{90*s:.1f}" height="{432*s:.1f}" fill="{ROXO}"/>'
    
    arm_fill = f'url(#grad-arm-top)'
    arm_top = f'''<polygon points="
      {162*s:.1f},{40*s:.1f}
      {460*s:.1f},{40*s:.1f}
      {460*s:.1f},{120*s:.1f}
      {162*s:.1f},{220*s:.1f}
    " fill="{arm_fill}"/>'''
    
    arm_bot = f'''<polygon points="
      {162*s:.1f},{292*s:.1f}
      {460*s:.1f},{472*s:.1f}
      {460*s:.1f},{392*s:.1f}
      {162*s:.1f},{212*s:.1f}
    " fill="{VERMELHO}"/>'''
    
    cut_color = bg_color if bg_color else GRAFITE
    cut = f'''<polygon points="
      {162*s:.1f},{220*s:.1f}
      {370*s:.1f},{130*s:.1f}
      {370*s:.1f},{210*s:.1f}
      {162*s:.1f},{292*s:.1f}
    " fill="{cut_color}"/>'''
    
    # Wordmark: Space Grotesk Bold, tamanho proporcional
    # Símbolo altura = 200px, wordmark = 82% = 164px
    # Mas para texto, usamos font-size proporcional
    font_size = 120  # ajustado para look premium
    text_x = 220  # após o símbolo + espaçamento
    text_y = 150  # baseline vertically centered
    
    wordmark_el = f'''<text x="{text_x}" y="{text_y}"
      font-family="Space Grotesk, Inter, -apple-system, sans-serif"
      font-size="{font_size}"
      font-weight="700"
      fill="{text_color}"
      letter-spacing="-2">{wordmark}</text>'''
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="200" viewBox="0 0 900 200">
  {defs}
  {bg}
  {haste}
  {arm_top}
  {arm_bot}
  {cut}
  {wordmark_el}
</svg>'''

# ══════════════════════════════════════════════
# GERAR TODOS OS SVGs
# ══════════════════════════════════════════════
print("=" * 50)
print("KOLDEX — Gerando brand assets")
print("=" * 50)

files_to_export = []

# 1. icon.svg — símbolo em fundo grafite
svg = make_symbol_svg(GRAFITE)
path = os.path.join(ASSETS, 'icon.svg')
with open(path, 'w') as f: f.write(svg)
files_to_export.append(('icon.svg', 512, 512))
print("  icon.svg ✓")

# 2. icon-dark.svg — símbolo fundo grafite (= icon)
import shutil
shutil.copy(path, os.path.join(ASSETS, 'icon-dark.svg'))
files_to_export.append(('icon-dark.svg', 512, 512))
print("  icon-dark.svg ✓")

# 3. icon-light.svg — símbolo fundo branco
svg = make_symbol_svg(BRANCO)
path = os.path.join(ASSETS, 'icon-light.svg')
with open(path, 'w') as f: f.write(svg)
files_to_export.append(('icon-light.svg', 512, 512))
print("  icon-light.svg ✓")

# 4. icon-transparent.svg — símbolo sem fundo
svg = make_symbol_svg(None)
path = os.path.join(ASSETS, 'icon-transparent.svg')
with open(path, 'w') as f: f.write(svg)
files_to_export.append(('icon-transparent.svg', 512, 512))
print("  icon-transparent.svg ✓")

# 5. favicon.svg
svg = make_symbol_svg(GRAFITE)
path = os.path.join(ASSETS, 'favicon.svg')
with open(path, 'w') as f: f.write(svg)
print("  favicon.svg ✓")

# 6. logo.svg — grafite + branco
svg = make_logo_svg(GRAFITE, BRANCO)
path = os.path.join(ASSETS, 'logo.svg')
with open(path, 'w') as f: f.write(svg)
files_to_export.append(('logo.svg', 900, 200))
print("  logo.svg ✓")

# 7. logo-dark.svg — grafite fundo (= logo)
shutil.copy(path, os.path.join(ASSETS, 'logo-dark.svg'))
files_to_export.append(('logo-dark.svg', 900, 200))
print("  logo-dark.svg ✓")

# 8. logo-light.svg — fundo branco, texto grafite
svg = make_logo_svg(BRANCO, GRAFITE)
path = os.path.join(ASSETS, 'logo-light.svg')
with open(path, 'w') as f: f.write(svg)
files_to_export.append(('logo-light.svg', 900, 200))
print("  logo-light.svg ✓")

# 9. logo-white.svg — fundo transparente, texto branco
svg = make_logo_svg(None, BRANCO)
path = os.path.join(ASSETS, 'logo-white.svg')
with open(path, 'w') as f: f.write(svg)
files_to_export.append(('logo-white.svg', 900, 200))
print("  logo-white.svg ✓")

# 10. logo-black.svg — fundo transparente, texto preto (monocromático)
svg = make_logo_svg(None, '#000000')
path = os.path.join(ASSETS, 'logo-black.svg')
with open(path, 'w') as f: f.write(svg)
files_to_export.append(('logo-black.svg', 900, 200))
print("  logo-black.svg ✓")

# ══════════════════════════════════════════════
# EXPORTAR PNGs via Inkscape
# ══════════════════════════════════════════════
print("\nExportando PNGs via Inkscape...")

png_exports = [
    # (svg_name, png_name, width, height)
    ('icon.svg', 'icon.png', 512, 512),
    ('icon.svg', 'icon-2000.png', 2000, 2000),        # social avatar
    ('icon.svg', 'avatar-instagram.png', 320, 320),
    ('icon.svg', 'avatar-whatsapp.png', 192, 192),
    ('icon.svg', 'favicon-32.png', 32, 32),
    ('icon.svg', 'favicon-48.png', 48, 48),
    ('icon-light.svg', 'icon-light.png', 512, 512),
    ('icon-transparent.svg', 'icon-transparent.png', 512, 512),
    ('logo.svg', 'logo.png', 900, 200),
    ('logo-dark.svg', 'logo-dark.png', 900, 200),
    ('logo-light.svg', 'logo-light.png', 900, 200),
    ('logo-white.svg', 'logo-white.png', 900, 200),
    ('logo-black.svg', 'logo-black.png', 900, 200),
]

for svg_name, png_name, width, height in png_exports:
    svg_path = os.path.join(ASSETS, svg_name)
    png_path = os.path.join(ASSETS, png_name)
    cmd = [
        INKSCAPE, svg_path,
        '--export-type=png',
        f'--export-filename={png_path}',
        f'--export-width={width}',
        f'--export-height={height}',
        '--export-background-opacity=0',
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    size = os.path.getsize(png_path) // 1024 if os.path.exists(png_path) else 0
    status = f"{size}KB ✓" if size > 0 else "FALHOU"
    print(f"  {png_name} ({width}x{height}) — {status}")

print("\n✓ Brand assets Koldex gerados em koldex/assets/")
print("=" * 50)
