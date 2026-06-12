"""
KOLDEX — Build final usando Logo-recraft.svg como fonte
O SVG tem tudo vetorizado: símbolo K + texto "Koldex" com x vermelho.

Estrutura identificada:
- [0] fill=#F8F8F7 → fundo branco (REMOVER)
- [1] fill=#07070C → fundo arredondado escuro (GUARDAR como bg dark)
- [2] fill=#5702B2 → K roxo parte 1 (haste/corpo esquerdo)
- [3] fill=#F8F8F7 → letra "o" (branca)
- [4] fill=#07070C → parte interna "o" (buraco)
- [5] fill=#F8F8F7 → letra "l"? 
- ... continuação das letras
- fill=#FA0907 → x vermelho (partes)
- fill=#5702B2 → K roxo parte 2

Abordagem:
1. Remover paths [0] (fundo branco) e [1] (fundo escuro)
2. Usar viewBox ajustado para centrar o conteúdo
3. Gerar variações trocando cores
"""
import subprocess, os, re

ASSETS  = r'd:\_Projetos\_WEB\koldex-site\koldex\assets'
INKSCAPE= r'C:\Program Files\Inkscape\bin\inkscape.exe'

# Cores oficiais
ROXO  = '#4C1D95'  # Roxo Principal
VERM  = '#FF2800'  # Vermelho Ferrari
GRAFT = '#16161B'  # Grafite
BRANCO= '#FFFFFF'
BG_DK = '#07070C'  # fundo escuro original (quase preto)

print("="*50)
print("KOLDEX — Build a partir do Logo-recraft.svg")
print("="*50)

with open(os.path.join(ASSETS, 'Logo-recraft.svg'), 'r', encoding='utf-8') as f:
    raw = f.read()

# Extrair todos os paths
all_paths = re.findall(r'<path[^>]+/?>', raw, re.DOTALL)
print(f"\nPaths encontrados: {len(all_paths)}")
for i, p in enumerate(all_paths):
    fill = re.search(r'fill="([^"]+)"', p)
    print(f"  [{i:2d}] {fill.group(1) if fill else 'none'}")

# Identificar grupos:
# [0] #F8F8F7 → FUNDO (SKIP)
# [1] #07070C → FUNDO ARREDONDADO (opcional para bg dark)
# [2] #5702B2 → K roxo body 1
# [3+] letras em #F8F8F7 (branco) e #07070C (buracos das letras)
# Vermelho #FA0907 → partes do x

# Paths do K (símbolo) = paths com fill #5702B2
# Paths do texto = o resto (excluindo fundos)

# Extrair paths SEM o fundo branco [0]
# [1] = fundo escuro arredondado → útil para versão dark
bg_dark_path = all_paths[1]  # fundo escuro arredondado

# Todos os outros paths = conteúdo (K + texto)
content_paths = all_paths[2:]  # excluir [0] fundo branco e [1] fundo escuro

print(f"\nPaths de conteúdo: {len(content_paths)}")

# Função para substituir cores no conteúdo
def apply_colors(paths, txt_color=BRANCO, k_color=ROXO, red_color=VERM, hole_color=None):
    """
    paths: lista de paths SVG
    txt_color: cor do texto (branco ou escuro)
    k_color: cor do K
    red_color: cor vermelha
    hole_color: cor dos buracos das letras (None = inverso do txt)
    """
    result = []
    if hole_color is None:
        # Os buracos precisam ter a cor do fundo
        hole_color = BG_DK  # padrão fundo escuro
    
    for p in paths:
        fill_m = re.search(r'fill="([^"]+)"', p)
        if not fill_m:
            result.append(p)
            continue
        fill = fill_m.group(1)
        
        if fill in ('#5702B2',):  # K roxo
            p = p.replace(fill, k_color)
        elif fill in ('#F8F8F7',):  # texto branco
            p = p.replace(fill, txt_color)
        elif fill in ('#07070C',):  # buracos das letras
            p = p.replace(fill, hole_color)
        elif fill in ('#FA0907', '#FC0402'):  # vermelho
            p = p.replace(fill, red_color)
        
        result.append(p)
    return result

# ── Gerar versões ──

def make_svg(include_bg, bg_color, txt_color, k_color, hole_color, width=717, height=207, br=0):
    """Construir SVG completo."""
    
    paths = apply_colors(content_paths, txt_color, k_color, VERM, hole_color)
    paths_str = '\n  '.join(paths)
    
    if include_bg == 'rect':
        bg = f'<rect width="{width}" height="{height}" rx="{br}" fill="{bg_color}"/>'
    elif include_bg == 'path':
        # Usar o path arredondado original do Recraft mas com cor customizada
        p = bg_dark_path.replace('#07070C', bg_color)
        bg = p
    else:
        bg = ''
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 717 207">
  {bg}
  {paths_str}
</svg>'''

# Dicionário de SVGs a gerar
# Formato: (include_bg, bg_color, txt_color, k_color, hole_color)

svgs = {
    'logo.svg':               make_svg('path', '#07070C', BRANCO, ROXO, '#07070C'),
    'logo-dark.svg':          make_svg('path', '#07070C', BRANCO, ROXO, '#07070C'),
    'logo-grafite.svg':       make_svg('rect', GRAFT, BRANCO, ROXO, GRAFT),
    'logo-light.svg':         make_svg('rect', BRANCO, '#1A1A2C', ROXO, BRANCO),
    'logo-white.svg':         make_svg(None, None, BRANCO, ROXO, 'transparent'),
    'logo-preto.svg':         make_svg(None, None, '#111111', '#111111', 'transparent'),
    'logo-institucional.svg': make_svg(None, None, GRAFT, GRAFT, 'transparent'),
}

# Símbolo K isolado (só os paths do K)
k_only_paths = [p for p in content_paths if re.search(r'fill="#5702B2"', p) or 
                (re.search(r'fill="#F[A8]0[90][07]"', p) and 
                 not any(c in p for c in ['l', 'K', 'e', 'd', 'x']))]

# Na verdade, o K está nos paths com fill #5702B2 (dois deles)
# e o triângulo vermelho também faz parte do K (#FA0907)
k_symbol_paths_raw = [p for p in all_paths if re.search(r'fill="(#5702B2|#FA0907)"', p)]
print(f"\nPaths do símbolo K: {len(k_symbol_paths_raw)}")

# O K ocupa do canto esq até ~x=230 no viewBox 0 0 717 207
# Vamos criar SVG do ícone com crop/viewBox ajustado
k_vb = "80 10 165 190"  # crop no K apenas

def make_icon_svg(bg_type, bg_color, br, k_color=ROXO):
    k_paths_colored = []
    for p in k_symbol_paths_raw:
        fill_m = re.search(r'fill="([^"]+)"', p)
        fill = fill_m.group(1) if fill_m else ''
        if fill == '#5702B2':
            p = p.replace(fill, k_color)
        elif fill == '#FA0907':
            p = p.replace(fill, VERM)
        k_paths_colored.append(p)
    
    k_str = '\n  '.join(k_paths_colored)
    
    if bg_type == 'dark':
        # Usar fundo do Recraft mas com crop para 512x512
        bg_p = bg_dark_path.replace('#07070C', bg_color)
        # Scale o bg para 512x512
        bg_el = f'<rect width="512" height="512" rx="{br}" fill="{bg_color}"/>'
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="{k_vb}">
  <rect x="80" y="10" width="165" height="190" rx="{br}" fill="{bg_color}"/>
  {k_str}
</svg>'''
    elif bg_type == 'white':
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="{k_vb}">
  <rect x="80" y="10" width="165" height="190" rx="0" fill="{BRANCO}"/>
  {k_str}
</svg>'''
    else:
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="{k_vb}">
  {k_str}
</svg>'''

icon_svgs = {
    'icon.svg':              make_icon_svg('dark', '#07070C', 32),
    'icon-dark.svg':         make_icon_svg('dark', '#07070C', 32),
    'icon-rounded.svg':      make_icon_svg('dark', '#07070C', 48),
    'icon-light.svg':        make_icon_svg('white', BRANCO, 0),
    'icon-transparent.svg':  make_icon_svg('transparent', None, 0),
    'favicon.svg':           make_icon_svg('dark', '#07070C', 0),
}

print("\nGerando SVGs...")
for name, svg in {**svgs, **icon_svgs}.items():
    with open(os.path.join(ASSETS, name), 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"  {name} ✓")

# ── Exportar PNGs ──
print("\nExportando PNGs...")

exports = [
    # Logos
    ('logo.svg',              'logo.png',              717, 207),
    ('logo-dark.svg',         'logo-dark.png',         717, 207),
    ('logo-light.svg',        'logo-light.png',        717, 207),
    ('logo-white.svg',        'logo-branco.png',       717, 207),
    ('logo-preto.svg',        'logo-preto.png',        717, 207),
    ('logo-grafite.svg',      'logo-grafite.png',      717, 207),
    ('logo-institucional.svg','logo-institucional.png',717, 207),
    # Alta resolução
    ('logo.svg',              'logo-horizontal.png',  1434, 414),
    # Ícones
    ('icon.svg',              'icon.png',              512, 512),
    ('icon.svg',              'icon-2000.png',        2000,2000),
    ('icon-rounded.svg',      'icon-rounded.png',      512, 512),
    ('icon-light.svg',        'icon-light.png',        512, 512),
    ('icon-transparent.svg',  'icon-transparent.png',  512, 512),
    ('icon.svg',              'avatar-instagram.png',  320, 320),
    ('icon.svg',              'avatar-whatsapp.png',   192, 192),
    ('favicon.svg',           'favicon-32.png',         32,  32),
    ('favicon.svg',           'favicon-48.png',         48,  48),
    # logo-vertical = ícone (só o K)
    ('icon.svg',              'logo-vertical.png',     512, 512),
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

# ── Identificar fonte ──
print("\n" + "="*50)
print("ANÁLISE DA FONTE")
print("="*50)
print("O SVG usa paths vetorizados (não tem tag <text> ou font-family).")
print("Isso significa que a fonte foi convertida em curvas pelo Recraft.")
print("")
print("Analisando o estilo visual do wordmark 'Koldex':")
print("- Letras geométricas, sem serifa")
print("- Altura-x uniforme, terminações planas")
print("- Peso Bold/Heavy")
print("- Espaçamento condensado")
print("- Muito similar à: Orbitron Bold, Exo 2 Bold, Space Grotesk Bold")
print("  ou Rajdhani Bold")
print("")
print("Recomendação para o Manual:")
print("  FONTE PRIMÁRIA: Space Grotesk Bold (Google Fonts)")
print("  Alternativa: Exo 2 Bold (Google Fonts)")
print("  URL: https://fonts.google.com/specimen/Space+Grotesk")
print("="*50)
