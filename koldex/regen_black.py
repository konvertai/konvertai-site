import subprocess, os, re

ASSETS  = r'd:\_Projetos\_WEB\koldex-site\koldex\assets'
INKSCAPE= r'C:\Program Files\Inkscape\bin\inkscape.exe'
BRANCO = '#FFFFFF'
PRETO  = '#111111'

with open(os.path.join(ASSETS, 'Logo-recraft.svg'), 'r', encoding='utf-8') as f:
    raw = f.read()

all_paths = re.findall(r'<path[^>]+/?>', raw, re.DOTALL)
content_paths = all_paths[2:]

result = []
for p in content_paths:
    fill_m = re.search(r'fill="([^"]+)"', p)
    if not fill_m:
        result.append(p)
        continue
    fill = fill_m.group(1)
    if fill in ('#5702B2', '#F8F8F7'):
        p = p.replace(fill, PRETO)
    elif fill == '#07070C':
        p = p.replace(fill, BRANCO)
    elif fill in ('#FA0907', '#FC0402'):
        p = p.replace(fill, PRETO)  # x sem vermelho
    result.append(p)

paths_str = '\n  '.join(result)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="717" height="207" viewBox="0 0 717 207">
  <rect width="717" height="207" rx="14" fill="{BRANCO}"/>
  {paths_str}
</svg>'''

with open(os.path.join(ASSETS, 'logo-black.svg'), 'w', encoding='utf-8') as f:
    f.write(svg)

pp = os.path.join(ASSETS, 'logo-black.png')
subprocess.run([INKSCAPE, os.path.join(ASSETS, 'logo-black.svg'),
                '--export-type=png', f'--export-filename={pp}',
                '--export-width=717', '--export-height=207',
                '--export-background-opacity=0'],
               capture_output=True, text=True, timeout=30)
print(f"logo-black.png — {os.path.getsize(pp)//1024}KB ✓")
print("x sem vermelho, tudo preto!")
