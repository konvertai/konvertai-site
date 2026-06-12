"""
KOLDEX — Regenerar TODOS os assets do zero com pipeline correto.
Fonte: Logo-recraft.svg
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
bg_dark_path = all_paths[1]   # fundo arredondado escuro original
content_paths = all_paths[2:] # K + letras (sem os 2 fundos)

# Ícone K isolado: paths com fill #5702B2 e #FA0907
k_symbol_raw = [p for p in all_paths if re.search(r'fill="(#5702B2|#FA0907)"', p)]
k_vb = "80 10 165 190"  # crop no K

def apply(paths, txt_color, k_color, red_color, hole_color):
    result = []
    for p in paths:
        m = re.search(r'fill="([^"]+)"', p)
        if not m:
            result.append(p); continue
        f = m.group(1)
        if f == '#5702B2':   p = p.replace(f, k_color)
        elif f == '#F8F8F7': p = p.replace(f, txt_color)
        elif f == '#07070C': p = p.replace(f, hole_color)
        elif f in ('#FA0907','#FC0402'): p = p.replace(f, red_color)
        result.append(p)
    return result

def logo(bg_type, bg_fill, txt, k_col, red, hole, br=14):
    paths = apply(content_paths, txt, k_col, red, hole)
    ps = '\n  '.join(paths)
    if bg_type == 'path':
        bg = bg_dark_path.replace('#07070C', bg_fill)
    elif bg_type == 'rect':
        bg = f'<rect width="717" height="207" rx="{br}" fill="{bg_fill}"/>'
    else:
        bg = ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="717" height="207" viewBox="0 0 717 207">\n  {bg}\n  {ps}\n</svg>'

def icon(bg_type, bg_fill, k_col, br=32):
    kp = []
    for p in k_symbol_raw:
        m = re.search(r'fill="([^"]+)"', p)
        f = m.group(1) if m else ''
        if f == '#5702B2': p = p.replace(f, k_col)
        elif f in ('#FA0907','#FC0402'): p = p.replace(f, VERM)
        kp.append(p)
    ks = '\n  '.join(kp)
    if bg_type == 'dark':
        bg = f'<rect x="80" y="10" width="165" height="190" rx="{br}" fill="{bg_fill}"/>'
    elif bg_type == 'white':
        bg = f'<rect x="80" y="10" width="165" height="190" rx="0" fill="{BRANCO}"/>'
    else:
        bg = ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="{k_vb}">\n  {bg}\n  {ks}\n</svg>'

# ── Definição de todos os SVGs ──
SVGS = {
    # LOGOS COM CORES (K roxo + x vermelho)
    'logo.svg':               logo('path', '#07070C', BRANCO, ROXO, VERM,  '#07070C'),
    'logo-dark.svg':          logo('path', '#07070C', BRANCO, ROXO, VERM,  '#07070C'),
    'logo-grafite.svg':       logo('rect', GRAFT,     BRANCO, ROXO, VERM,  GRAFT),
    'logo-light.svg':         logo('rect', BRANCO,    '#1A1A2C', ROXO, VERM, BRANCO),
    'logo-white.svg':         logo(None,  None,       BRANCO, ROXO, VERM,  BRANCO),

    # LOGOS MONOCROMÁTICAS (sem vermelho — uso formal)
    'logo-preto.svg':         logo('rect', BRANCO, PRETO, PRETO, PRETO, BRANCO),
    'logo-black.svg':         logo('rect', BRANCO, PRETO, PRETO, PRETO, BRANCO),
    'logo-institucional.svg': logo(None,   None,   GRAFT, GRAFT, GRAFT, BRANCO),
    'logo-cinza.svg':         logo(None,   None,   CINZA, CINZA, CINZA, BRANCO),

    # ÍCONES
    'icon.svg':               icon('dark',  '#07070C', ROXO, 32),
    'icon-dark.svg':          icon('dark',  '#07070C', ROXO, 32),
    'icon-rounded.svg':       icon('dark',  '#07070C', ROXO, 48),
    'icon-light.svg':         icon('white', BRANCO,    ROXO, 0),
    'icon-transparent.svg':   icon(None,    None,      ROXO, 0),
    'favicon.svg':            icon('dark',  '#07070C', ROXO, 0),
}

print("="*50)
print("KOLDEX — Regenerando TODOS os assets")
print("="*50)

print("\nGerando SVGs...")
for name, svg in SVGS.items():
    with open(os.path.join(ASSETS, name), 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"  {name} ✓")

# ── PNGs ──
print("\nExportando PNGs...")
PNGS = [
    # Logos coloridas
    ('logo.svg',              'logo.png',              717,  207),
    ('logo-dark.svg',         'logo-dark.png',         717,  207),
    ('logo-light.svg',        'logo-light.png',        717,  207),
    ('logo-white.svg',        'logo-branco.png',       717,  207),
    ('logo-grafite.svg',      'logo-grafite.png',      717,  207),
    # Logos monocromáticas
    ('logo-preto.svg',        'logo-preto.png',        717,  207),
    ('logo-black.svg',        'logo-black.png',        717,  207),
    ('logo-institucional.svg','logo-institucional.png',717,  207),
    ('logo-cinza.svg',        'logo-cinza.png',        717,  207),
    # Alta resolução
    ('logo.svg',              'logo-horizontal.png',  1434,  414),
    ('logo-preto.svg',        'logo-preto-hd.png',    1434,  414),
    # Ícones
    ('icon.svg',              'icon.png',              512,  512),
    ('icon.svg',              'icon-2000.png',        2000, 2000),
    ('icon-rounded.svg',      'icon-rounded.png',      512,  512),
    ('icon-light.svg',        'icon-light.png',        512,  512),
    ('icon-transparent.svg',  'icon-transparent.png',  512,  512),
    # Avatares
    ('icon.svg',              'avatar-instagram.png',  320,  320),
    ('icon.svg',              'avatar-whatsapp.png',   192,  192),
    # Favicons
    ('favicon.svg',           'favicon-32.png',         32,   32),
    ('favicon.svg',           'favicon-48.png',          48,  48),
    # Vertical (só ícone)
    ('icon.svg',              'logo-vertical.png',     512,  512),
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

print(f"\n✓ {len(PNGS)} PNGs gerados. Todos atualizados!")
print("="*50)
