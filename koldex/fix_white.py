import subprocess, os, re

ASSETS   = r'd:\_Projetos\_WEB\koldex-site\koldex\assets'
INKSCAPE = r'C:\Program Files\Inkscape\bin\inkscape.exe'
ROXO     = '#4C1D95'
VERM     = '#FF2800'
BRANCO   = '#FFFFFF'

with open(os.path.join(ASSETS, 'Logo-recraft.svg'), 'r', encoding='utf-8') as f:
    raw = f.read()

all_paths = re.findall(r'<path[^>]+/?>', raw, re.DOTALL)
content_paths = all_paths[2:]

def get_d(p):
    m = re.search(r'\bd="([^"]+)"', p)
    return m.group(1) if m else ''

def make_combined(outer, inner, fill):
    return f'<path fill="{fill}" fill-rule="evenodd" d="{get_d(outer)} {get_d(inner)}"/>'

result = []
i = 0
while i < len(content_paths):
    p = content_paths[i]
    m = re.search(r'fill="([^"]+)"', p)
    fill = m.group(1) if m else ''
    next_hole = (i + 1 < len(content_paths) and
                 re.search(r'fill="#07070C"', content_paths[i + 1]))

    if fill == '#5702B2':
        result.append(p.replace(fill, ROXO))
        i += 1
    elif fill == '#F8F8F7' and next_hole:
        result.append(make_combined(p, content_paths[i + 1], BRANCO))
        i += 2
    elif fill == '#F8F8F7':
        result.append(p.replace(fill, BRANCO))
        i += 1
    elif fill in ('#FA0907', '#FC0402'):
        result.append(p.replace(fill, VERM))
        i += 1
    elif fill == '#07070C':
        i += 1  # pular buracos orphan
    else:
        result.append(p)
        i += 1

ps = '\n  '.join(result)
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" '
       f'width="717" height="207" viewBox="0 0 717 207">\n  {ps}\n</svg>')

svg_path = os.path.join(ASSETS, 'logo-white.svg')
with open(svg_path, 'w', encoding='utf-8') as f:
    f.write(svg)

png_path = os.path.join(ASSETS, 'logo-white.png')
subprocess.run([INKSCAPE, svg_path,
                '--export-type=png',
                f'--export-filename={png_path}',
                '--export-width=717',
                '--export-height=207',
                '--export-background-opacity=0'],
               capture_output=True, text=True, timeout=30)

kb = os.path.getsize(png_path) // 1024
print(f'logo-white.svg + logo-white.png — {kb}KB ✓')
