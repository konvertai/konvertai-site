# KOLDEX — Manual de Identidade Visual
**Versão 1.0** | Gerado automaticamente

---

## POSICIONAMENTO

| | |
|---|---|
| **Nome** | Koldex |
| **Segmento** | Inteligência Artificial · Automação Corporativa · Agentes de Atendimento · SaaS |
| **Arquétipo** | O Mago (primário) · O Governante (secundário) |

---

## PALETA OFICIAL

| Cor | HEX | RGB | CMYK | Pantone |
|---|---|---|---|---|
| **Roxo Principal** | `#4C1D95` | 76 29 149 | 49 81 0 42 | 2685 C |
| **Vermelho Ferrari** | `#FF2800` | 255 40 0 | 0 84 100 0 | 485 C |
| **Grafite** | `#16161B` | 22 22 27 | 19 19 0 89 | — |
| **Branco** | `#FFFFFF` | 255 255 255 | 0 0 0 0 | — |

### Gradiente Oficial
- **Início:** `#4C1D95`
- **Fim:** `#FF2800`
- **Ângulo:** 135°
- **Uso máximo:** 25% da composição

---

## TIPOGRAFIA

### Primária — Wordmark
**Recharge Bold**
- Fundição: Typodermic (Ray Larabie)
- Licença: Comercial (myfonts.com/fonts/typodermic/recharge)
- Uso: Logo, wordmark "Koldex"
- Nota: O wordmark nos arquivos SVG está vetorizado (curvas), independente da fonte instalada.

### Secundária — Interface e Documentação
**Inter** (Google Fonts — gratuita)
- Pesos: 400 Regular · 500 Medium · 600 SemiBold
- Uso: Textos, contratos, documentação, website
- URL: https://fonts.google.com/specimen/Inter

---

## SÍMBOLO

O símbolo K é formado por **3 shapes sobrepostos**:
1. **Shape esquerdo** (roxo): corpo diagonal, haste visual do K
2. **Shape direito superior** (roxo): braço diagonal superior
3. **Shape inferior** (vermelho #FF2800): triângulo inferior direito

Arquivo fonte: `k-symbol-recraft.svg` (vetorizado pelo Recraft.ai)

---

## WORDMARK

"**Kolde**" + "**x**" onde:
- "Kolde" = cor do contexto (branco no dark, grafite no claro)
- "x" = perna superior direita em **Vermelho Ferrari** `#FF2800`

---

## ARQUIVOS MESTRES

| Arquivo | Descrição | Uso |
|---|---|---|
| `logo.svg` | Logo principal (fundo escuro) | Digital, apresentações |
| `logo-dark.svg` | = logo.svg | Fundo escuro |
| `logo-light.svg` | Logo fundo branco | Documentos, impressão |
| `logo-white.svg` | Logo sem fundo, texto branco | Fundos escuros, vídeo |
| `logo-preto.svg` | Monocromática preta | Impressão 1 cor |
| `logo-institucional.svg` | Monocromática grafite | Uso formal |
| `logo-grafite.svg` | Logo fundo grafite | Materiais premium |
| `icon.svg` | Símbolo K (fundo escuro) | App, favicon |
| `icon-dark.svg` | = icon.svg | |
| `icon-light.svg` | Símbolo K (fundo branco) | |
| `icon-transparent.svg` | Símbolo K sem fundo | Sobreposições |
| `favicon.svg` | Favicon | Browser |
| `Logo-recraft.svg` | **Arquivo mestre original** | Edição / referência |
| `k-symbol-recraft.svg` | Símbolo K isolado | Edição do ícone |

### PNGs Gerados

| Arquivo | Tamanho | Uso |
|---|---|---|
| `logo-horizontal.png` | 1434×414 | Alta resolução |
| `logo-dark.png` | 717×207 | Digital padrão |
| `logo-light.png` | 717×207 | Fundo claro |
| `logo-branco.png` | 717×207 | Fundo escuro |
| `logo-preto.png` | 717×207 | Impressão |
| `icon.png` | 512×512 | App stores |
| `icon-2000.png` | 2000×2000 | Social media HD |
| `icon-rounded.png` | 512×512 | App com cantos arredondados |
| `avatar-instagram.png` | 320×320 | Perfil Instagram |
| `avatar-whatsapp.png` | 192×192 | Perfil WhatsApp |
| `favicon-48.png` | 48×48 | Favicon browser |

---

## TAMANHOS MÍNIMOS

| Aplicação | Mínimo |
|---|---|
| Logo digital | 120 px |
| Símbolo digital | 32 px |
| Favicon | 16 px |
| Logo impressão | 25 mm |
| Símbolo impressão | 8 mm |

---

## REDES SOCIAIS

- **Avatar:** Símbolo isolado (`icon.svg`)
- **Margem interna:** 12%
- **Nunca:** usar logo completa em avatar

---

## REGRAS PROIBIDAS

- ❌ Não distorcer proporções
- ❌ Não rotacionar
- ❌ Não alterar cores da paleta
- ❌ Não aplicar sombras exageradas
- ❌ Não usar gradiente fora da paleta oficial
- ❌ Não usar sobre fundos com baixo contraste

---

## REGENERAR ASSETS

Para regenerar todos os arquivos a partir dos SVGs mestres:

```bash
cd d:\_Projetos\_WEB\koldex-site\koldex
python build_from_logo.py
```

---

*Koldex — IA e Automações que Escalam Resultados*
