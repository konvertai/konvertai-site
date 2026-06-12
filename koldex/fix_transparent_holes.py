"""
Correção definitiva dos buracos para versões sem fundo.

Problema: o, d, e têm dois paths cada:
  - path exterior (fill=#F8F8F7 = letra)
  - path interior (fill=#07070C = buraco/counter)

Para versão sem fundo, precisamos que o buraco seja TRANSPARENTE.
A técnica: para cada par (letra+buraco), combinar os dois paths em um
único path com fill-rule="evenodd". Isso cria um buraco real/transparente.

Mapeamento dos paths (identificado pela posição/tamanho):
  [2]  #5702B2  → K roxo parte 1
  [3]  #F8F8F7  → letra exterior (o/l/etc)
  [4]  #07070C  → buraco da letra [3]
  [5]  #F8F8F7  → letra exterior
  [6]  #07070C  → buraco da letra [5]
  [7]  #F8F8F7  → letra exterior
  [8]  #07070C  → buraco da letra [7]
  [9]  #FA0907  → x vermelho parte
  [10] #5702B2  → K roxo parte 2
  [11] #F8F8F7  → letra (sem buraco)
  [12] #F8F8F7  → letra (sem buraco)
  [13] #F8F8F7  → letra (sem buraco)
  [14] #F8F8F7  → letra (sem buraco)
  [15] #FA0907  → x vermelho parte 2
"""
import subprocess, os, re

ASSETS  = r'd:\_Projetos\_WEB\koldex-site\koldex\assets'
INKSCAPE= r'C:\Program Files\Inkscape\bin\inkscape.exe'

ROXO  = '#4C1D95'
VERM  = '#FF2800'
GRAFT = '#16161B'
BRANCO= '#FFFFFF'
PRETO = '#111111'
CINZA = '#4A5568'

with open(os.path.join(ASSETS, 'Logo-recraft.svg'), 'r', encoding='utf-8') as f:
    raw = f.read()

all_paths = re.findall(r'<path[^>]+/?>', raw, re.DOTALL)
bg_dark_path = all_paths[1]
content_paths = all_paths[2:]  # índices 0..13 dentro desta lista

def get_d(path_str):
    """Extrair o atributo d= de um path."""
    m = re.search(r'\bd="([^"]+)"', path_str)
    return m.group(1) if m else ''

def make_combined_path(outer_path, inner_path, fill_color):
    """
    Combina dois paths (exterior + buraco) num único path com
    fill-rule='evenodd', criando buraco transparente real.
    """
    d_outer = get_d(outer_path)
    d_inner = get_d(inner_path)
    combined_d = d_outer + ' ' + d_inner
    return f'<path fill="{fill_color}" fill-rule="evenodd" d="{combined_d}"/>'

# Pares letra+buraco nos content_paths:
# [1] + [2] = letra "o" + seu buraco
# [3] + [4] = letra "d"? + buraco  
# [5] + [6] = letra "e"? + buraco
# Os outros ([7..]) não têm buraco

def build_paths_for_nobg(txt_color, k_color, red_color):
    """
    Para versão sem fundo:
    - pares com buraco → combined path evenodd (buraco transparente)
    - letras sem buraco → path normal
    - K → cor do K
    - vermelho → cor vermelha
    """
    result = []
    cp = content_paths
    i = 0
    while i < len(cp):
        p = cp[i]
        m = re.search(r'fill="([^"]+)"', p)
        fill = m.group(1) if m else ''
        
        # Verificar se o próximo path é um buraco (#07070C) para este
        next_is_hole = (i + 1 < len(cp) and 
                        re.search(r'fill="#07070C"', cp[i+1]))
        
        if fill == '#5702B2':
            result.append(p.replace(fill, k_color))
            i += 1
        elif fill == '#F8F8F7' and next_is_hole:
            # Letra com buraco → combinar com fill-rule evenodd
            result.append(make_combined_path(p, cp[i+1], txt_color))
            i += 2  # pular o path do buraco
        elif fill == '#F8F8F7':
            # Letra sem buraco
            result.append(p.replace(fill, txt_color))
            i += 1
        elif fill in ('#FA0907', '#FC0402'):
            result.append(p.replace(fill, red_color))
            i += 1
        elif fill == '#07070C':
            # Buraco orphan (não deveria acontecer se a lógica estiver correta)
            i += 1  # pular
        else:
            result.append(p)
            i += 1
    
    return result

def build_paths_for_bg(txt_color, k_color, red_color, hole_color):
    """Para versões COM fundo: buracos com a cor do fundo."""
    result = []
    for p in content_paths:
        m = re.search(r'fill="([^"]+)"', p)
        fill = m.group(1) if m else ''
        if fill == '#5702B2':   p = p.replace(fill, k_color)
        elif fill == '#F8F8F7': p = p.replace(fill, txt_color)
        elif fill == '#07070C': p = p.replace(fill, hole_color)
        elif fill in ('#FA0907','#FC0402'): p = p.replace(fill, red_color)
        result.append(p)
    return result

def make_logo_nobg(txt_color, k_color, red_color):
    paths = build_paths_for_nobg(txt_color, k_color, red_color)
    ps = '\n  '.join(paths)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="717" height="207" viewBox="0 0 717 207">\n  {ps}\n</svg>'

def make_logo_bg(bg_type, bg_fill, txt_color, k_color, red_color, hole_color, br=14):
    paths = build_paths_for_bg(txt_color, k_color, red_color, hole_color)
    ps = '\n  '.join(paths)
    if bg_type == 'path':
        bg = bg_dark_path.replace('#07070C', bg_fill)
    elif bg_type == 'rect':
        bg = f'<rect width="717" height="207" rx="{br}" fill="{bg_fill}"/>'
    else:
        bg = ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="717" height="207" viewBox="0 0 717 207">\n  {bg}\n  {ps}\n</svg>'

print("="*50)
print("KOLDEX — Fix definitivo dos buracos (evenodd)")
print("="*50)

# Diagnóstico rápido
print("\nDiagnóstico dos pares letra+buraco:")
for i, p in enumerate(content_paths):
    m = re.search(r'fill="([^"]+)"', p)
    f = m.group(1) if m else '?'
    next_hole = (i+1 < len(content_paths) and 
                 re.search(r'fill="#07070C"', content_paths[i+1]))
    mark = " ← par com buraco" if f == '#F8F8F7' and next_hole else ""
    print(f"  [{i:2d}] {f}{mark}")

SVGS = {
    # Com fundo → buraco = cor do fundo
    'logo.svg':               make_logo_bg('path', '#07070C', BRANCO, ROXO, VERM,  '#07070C'),
    'logo-dark.svg':          make_logo_bg('path', '#07070C', BRANCO, ROXO, VERM,  '#07070C'),
    'logo-grafite.svg':       make_logo_bg('rect', GRAFT,     BRANCO, ROXO, VERM,  GRAFT),
    'logo-light.svg':         make_logo_bg('rect', BRANCO,    '#1A1A2C', ROXO, VERM, BRANCO),
    'logo-preto.svg':         make_logo_bg('rect', BRANCO,    PRETO,  PRETO, PRETO, BRANCO),
    'logo-black.svg':         make_logo_bg('rect', BRANCO,    PRETO,  PRETO, PRETO, BRANCO),
    
    # Sem fundo → fill-rule evenodd (buraco transparente real)
    'logo-white.svg':         make_logo_nobg(BRANCO, ROXO,  VERM),
    'logo-institucional.svg': make_logo_nobg(GRAFT,  GRAFT, GRAFT),
    'logo-cinza.svg':         make_logo_nobg(CINZA,  CINZA, CINZA),
}

print("\nGerando SVGs...")
for name, svg in SVGS.items():
    with open(os.path.join(ASSETS, name), 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"  {name} ✓")

print("\nExportando PNGs...")
PNGS = [
    ('logo.svg',              'logo.png',              717, 207),
    ('logo-dark.svg',         'logo-dark.png',         717, 207),
    ('logo-light.svg',        'logo-light.png',        717, 207),
    ('logo-white.svg',        'logo-branco.png',       717, 207),
    ('logo-grafite.svg',      'logo-grafite.png',      717, 207),
    ('logo-preto.svg',        'logo-preto.png',        717, 207),
    ('logo-black.svg',        'logo-black.png',        717, 207),
    ('logo-institucional.svg','logo-institucional.png',717, 207),
    ('logo-cinza.svg',        'logo-cinza.png',        717, 207),
    ('logo.svg',              'logo-horizontal.png',  1434, 414),
    ('logo-preto.svg',        'logo-preto-hd.png',    1434, 414),
]

for svg_n, png_n, w, h in PNGS:
    sp = os.path.join(ASSETS, svg_n)
    pp = os.path.join(ASSETS, png_n)
    subprocess.run([INKSCAPE, sp, '--export-type=png',
                    f'--export-filename={pp}',
                    f'--export-width={w}', f'--export-height={h}',
                    '--export-background-opacity=0'],
                   capture_output=True, text=True, timeout=30)
    kb = os.path.getsize(pp)//1024 if os.path.exists(pp) else 0
    print(f"  {png_n} ({w}x{h}) — {kb}KB {'✓' if kb>0 else 'FALHOU'}")

print("\n✓ Buracos corrigidos com fill-rule evenodd!")
print("="*50)
