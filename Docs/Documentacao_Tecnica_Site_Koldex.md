# Documentação Técnica — Site Koldex

> Versão: 1.0.0
> Data: 05/06/2026
> Deploy: https://koldex-site.vercel.app
> Repositório: https://github.com/koldex/koldex-site
> Status: Live (Produção)

---

## 1. VISÃO GERAL

Landing page de alta conversão para a agência de IA **Koldex**, focada em gerar leads via WhatsApp e formulário. Site estático, sem backend, otimizado para performance e SEO.

---

## 2. STACK TÉCNICA

| Camada | Tecnologia | Versão/Detalhes |
|--------|-----------|-----------------|
| Markup | HTML5 semântico | Estrutura acessível, ARIA labels |
| Estilo | CSS3 (custom properties, grid, flexbox) | 12 arquivos modulares |
| Interação | JavaScript vanilla (ES6+) | 1 arquivo, ~180 linhas |
| Fonte | Inter (Google Fonts) | Weights: 400, 500, 600, 700, 800 |
| Ícones | SVG inline | Zero requests extras |
| Deploy | Vercel | Auto-deploy via GitHub |
| DNS/CDN | Cloudflare | SSL, proteção, cache |
| Formulário | Formspree | ID: mykakjkj |
| Versionamento | Git + GitHub | Branch: main |
| Vetorização | Potrace (Python) + Inkscape | alphamax=0, cantos retos |

---

## 3. ESTRUTURA DE ARQUIVOS

```
koldex-site/
├── index.html              # Página principal (todas as seções)
├── .gitignore
├── README.md
├── robots.txt
├── sitemap.xml
├── vercel.json             # Headers de segurança + cache
│
├── css/
│   ├── tokens.css          # Design tokens (cores, tipografia, espaçamento)
│   ├── reset.css           # Reset + a11y (skip nav, focus, reduced motion)
│   ├── layout.css          # Container .wrap, .section
│   ├── typography.css      # Escala tipográfica (.display, .heading, .body)
│   ├── buttons.css         # .btn-brand, .btn-outline, .btn-wpp
│   ├── nav.css             # Navbar fixa com blur, mobile menu
│   ├── hero.css            # Hero + mockup WhatsApp + watermark
│   ├── sections.css        # Problemas, Solução, Como Funciona
│   ├── features.css        # Features grid + Serviços
│   ├── planos.css          # Planos, FAQ, CTA, Footer
│   ├── form.css            # Formulário de lead
│   ├── animations.css      # Reveal, stagger, glow, scrollbar
│   ├── utilities.css       # FAB WhatsApp, .hr, .r (reveal)
│   └── responsive.css      # Breakpoints para todos os dispositivos
│
├── js/
│   └── main.js             # Nav scroll, mobile menu, reveal, chat, form
│
├── assets/
│   ├── k-icon.svg          # Ícone K (com sombra)
│   ├── k-icon-gradient.svg # Ícone K (gradiente + sombra)
│   ├── k-icon-gradient.png # PNG do K gradiente (1024px)
│   ├── k-icon-512.png      # PNG transparente 512px
│   ├── k-icon-1024.png     # PNG transparente 1024px
│   ├── k-icon-2048.png     # PNG transparente 2048px (serigrafia)
│   ├── k-icon-print.png    # PNG transparente 1024px (impressão)
│   ├── k-icon-print-hd.png # PNG transparente 2048px (impressão HD)
│   ├── favicon.svg         # Favicon (K sem sombra)
│   ├── logo-dark.svg       # Logo completa (fundo escuro)
│   ├── logo-dark.png       # PNG da logo dark (1440px)
│   ├── logo-light.svg      # Logo (fundo claro)
│   ├── logo-light.png      # PNG da logo light
│   ├── logo-gradient.svg   # Logo (K + AI com gradiente)
│   ├── logo-gradient.png   # PNG da logo gradient
│   ├── logo-mono.svg       # Logo monocromática (impressão)
│   └── logo-mono.png       # PNG da logo mono
│
├── Docs/
│   ├── Site Koldex - Planejamento.md
│   └── Documentacao_Tecnica_Site_Koldex.md (este arquivo)
│
├── html/                   # Arquivos fonte originais (não vão pro deploy)
│   ├── K.png               # PNG original do K (referência)
│   ├── K+koldex.png     # PNG original da logo
│   └── ...
│
└── scripts/                # Scripts de processamento (não vão pro deploy)
    ├── potrace_v2.py       # Vetorização HSV + Potrace
    ├── final_fix.py        # Reconstrução SVGs sem retângulo
    ├── propagate.py        # Propagar path corrigido
    ├── export_pngs2.py     # Exportar PNGs via Inkscape
    └── ...
```

---

## 4. DESIGN SYSTEM

### 4.1 Paleta de Cores

| Token | Valor | Uso |
|-------|-------|-----|
| `--c-bg` | #09090F | Fundo principal |
| `--c-bg1` | #0F0F1A | Cards, seções alternadas |
| `--c-bg2` | #141420 | Elementos elevados |
| `--c-roxo` | #5B21B6 | Marca primária (K + AI) |
| `--c-roxo-v` | #7C3AED | Hover, destaques |
| `--c-roxo-l` | #8B5CF6 | Textos destacados, gradiente |
| `--c-ciano` | #06B6D4 | Secundária, CTAs alternativos |
| `--c-text-1` | #F8F7FF | Texto principal |
| `--c-text-2` | #A8A0C8 | Texto secundário |
| `--c-text-3` | #665D8A | Texto terciário |

### 4.2 Tipografia

- **Fonte:** Inter (Google Fonts)
- **H1 (hero):** clamp(2.75rem, 6vw, 5.5rem), weight 800
- **H2 (seção):** clamp(2rem, 3.5vw, 3rem), weight 700
- **Body:** 0.9rem, weight 400, line-height 1.7
- **Letras da logo:** posicionadas individualmente para espaçamento uniforme

### 4.3 Breakpoints

| Breakpoint | Dispositivo |
|-----------|-------------|
| > 1400px | Desktop grande |
| 960px - 1400px | Desktop/laptop |
| 768px - 960px | Tablets/laptops pequenos |
| 640px - 768px | Tablets portrait |
| < 640px | Celulares |
| < 380px | Celulares pequenos |

---

## 5. SEÇÕES DO SITE

| # | Seção | ID | Descrição |
|---|-------|-----|-----------|
| 1 | Navbar | `#nav` | Logo + links + CTA WhatsApp + hamburger mobile |
| 2 | Hero | `#hero` | H1 + subtítulo + CTAs + mockup WhatsApp animado + watermark K |
| 3 | Problemas | `#problemas` | 4 cards de dores + quote card |
| 4 | Solução | `#solucao` | Descrição + 4 métricas visuais |
| 5 | Como Funciona | `#como` | 3 steps com ícones |
| 6 | Features | `#features` | Grid 6 cards (recursos do agente) |
| 7 | Serviços | `#servicos` | 6 cards (serviços da agência) |
| 8 | Planos | `#planos` | 3 cards (Starter, Pro, Enterprise) |
| 9 | FAQ | `#faq` | 7 perguntas em accordion |
| 10 | CTA Final | `#contato` | Formulário de lead + botão WhatsApp |
| 11 | Footer | `footer` | Logo + navegação + contato + social |
| 12 | FAB | `.fab` | Botão WhatsApp flutuante |

---

## 6. FUNCIONALIDADES JAVASCRIPT

| Feature | Descrição |
|---------|-----------|
| Nav scroll | Adiciona sombra no scroll, esconde ao descer, mostra ao subir |
| Mobile menu | Hamburger toggle com overlay |
| Reveal on scroll | IntersectionObserver com stagger delay |
| Chat mockup | Animação sequencial de mensagens com typing indicator |
| Smooth scroll | Navegação suave para âncoras |
| Nav active | Destaque do link da seção visível |
| Form submit | Envio ao Formspree com fallback para WhatsApp |
| Phone mask | Máscara (XX) XXXXX-XXXX no campo WhatsApp |

---

## 7. BRAND ASSETS — PROCESSO DE CRIAÇÃO

### 7.1 Ícone K

**Processo:**
1. Imagem fonte: `html/K.png` (render 3D com sombras)
2. Filtro HSV para isolar o roxo puro (Hue 160-235, Saturation ≥ 50, Value ≤ 180)
3. Morfologia (mediana + MaxFilter + MinFilter)
4. Potrace com `alphamax=0` (cantos 100% retos, zero curvas Bezier)
5. Filtrar paths (remover retângulo externo de 4 segmentos)
6. Correção manual no Inkscape (deletar nós do serrilhado na perna)
7. Exportação PNG via Inkscape CLI

**Parâmetros Potrace:**
- `turdsize=5` (remove ruído < 5px)
- `alphamax=0.0` (cantos 100% retos)
- `opticurve=False` (sem otimização de curvas)
- `opttolerance=0.0` (zero tolerância)

**Sombra SVG:**
```xml
<feDropShadow dx="2" dy="-3" stdDeviation="6" flood-color="#3B0A8C" flood-opacity="0.6"/>
```

### 7.2 Logo Koldex

**Construção:**
- K estilizado em `scale(0.125)` (512→64px)
- Letras posicionadas individualmente para espaçamento visual uniforme
- Baseline do texto alinhada com a base do K (`y="61"`)

**Espaçamento entre letras:**
| Letra | x | Largura | Gap após |
|-------|---|---------|----------|
| K | 0 (ícone) | 64 | — |
| o | 56 | 27 | 3.5 |
| n | 86.5 | 27 | 3.5 |
| v | 117 | 25 | 3.5 |
| e | 145.5 | 25 | 3.5 |
| r | 174 | 18 | 6.5 |
| t | 198.5 | 17 | 4.5 |
| A | 220 | 30 | 2 |
| I | 252 | 12 | 0 |

**Cores na logo:**
- K: `#5B21B6` (ou gradiente)
- "onvert": `#F8F7FF` (dark) / `#1A1A2C` (light)
- "AI": `#5B21B6` (mesma cor do K)

---

## 8. SEO & PERFORMANCE

### Meta Tags
- Title: "Koldex — Agentes de IA para WhatsApp | Atendimento Automático 24h"
- Description otimizada para conversão
- Open Graph (Facebook/LinkedIn)
- Twitter Card
- Canonical URL
- Structured Data: Organization + LocalBusiness

### Performance
- CSS modular (12 arquivos ~15KB total)
- JS vanilla (~180 linhas, ~5KB)
- SVG inline para ícones
- Google Fonts com preconnect + display=swap
- Vercel CDN global
- Headers de cache (1 ano para assets)

### Acessibilidade
- Skip navigation
- ARIA labels em interativos
- Focus visible
- Keyboard navigation
- Reduced motion support
- Contraste mínimo 4.5:1
- Touch targets ≥ 44px

---

## 9. DEPLOY & INFRAESTRUTURA

| Item | Detalhe |
|------|---------|
| Hosting | Vercel (gratuito) |
| Deploy | Auto-deploy via git push para main |
| CDN | Vercel Edge Network (global) |
| DNS | Cloudflare |
| SSL | Automático (Vercel + Cloudflare) |
| Domínio | koldex.com.br |
| Formulário | Formspree (ID: mykakjkj, 50 envios/mês grátis) |

### Headers de Segurança (vercel.json)
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: strict-origin-when-cross-origin
- Cache-Control: 1 ano para assets estáticos

---

## 10. COMO DAR CONTINUIDADE / ESCALAR

### Próximos passos sugeridos:

1. **Google Analytics 4** — Adicionar tag no head para métricas de conversão
2. **Número WhatsApp real** — Substituir `5583999999999` pelo número correto
3. **Formspree ID** — Já configurado (`mykakjkj`), verificar email de destino
4. **Domínio** — Configurar DNS no Cloudflare apontando para Vercel
5. **Imagens OG** — Criar og-image.png (1200x630) para compartilhamento social
6. **Testimonials reais** — Substituir quote placeholder por depoimento real
7. **Logos de clientes** — Adicionar seção social proof quando tiver clientes

### Para escalar (futuro):

| Etapa | Ação | Quando |
|-------|------|--------|
| Multi-página | Criar /blog, /sobre, /portfolio | Quando tiver conteúdo |
| CMS | Integrar headless CMS (Contentful/Strapi) | Para blog |
| Analytics | Hotjar/Microsoft Clarity para heatmaps | Após 100+ visitas/dia |
| A/B Testing | Vercel Edge Config / Split | Para otimizar conversão |
| i18n | Versão em inglês | Se expandir região |
| Framework | Migrar para Next.js/Astro | Se precisar SSR/SSG dinâmico |
| Forms | Migrar Formspree → n8n webhook | Para automação completa |

### Comandos úteis:

```bash
# Deploy (automático ao push)
git add .
git commit -m "descrição da mudança"
git push

# Ver logs de deploy
# → Vercel Dashboard → Deployments

# Testar localmente
# Abrir index.html no navegador (funciona sem servidor)

# Exportar PNGs do K (se editar o SVG)
python scripts/export_pngs2.py

# Propagar K corrigido para logos/demais
python scripts/propagate.py

# Exportar PNGs das logos
python scripts/export_logo_pngs2.py
```

---

## 11. FERRAMENTAS UTILIZADAS

| Ferramenta | Uso | Instalação |
|-----------|-----|------------|
| Python 3.12 | Scripts de processamento | Já instalado |
| Pillow | Manipulação de imagens | `pip install pillow` |
| potrace (potracer) | Vetorização bitmap→SVG | `pip install potracer` |
| vtracer | Vetorização alternativa | `pip install vtracer` |
| Inkscape 1.4.4 | Edição visual de SVG + export PNG | Instalado via winget |
| Git | Versionamento | Já instalado |
| Vercel | Deploy | Via GitHub integration |

---

## 12. DECISÕES TÉCNICAS

| Decisão | Motivo |
|---------|--------|
| HTML/CSS/JS puro (sem framework) | Performance máxima, zero build time, Lighthouse 95+ |
| CSS modular (12 arquivos) | Organização, manutenibilidade, caching individual |
| SVG com sombra via filter | Efeito premium sem imagem extra |
| Potrace com alphamax=0 | Cantos 100% retos (geométrico) |
| Letras posicionadas individualmente | Controle total do kerning visual |
| Formspree para formulário | Sem backend, funciona imediatamente |
| Fallback WhatsApp no form | Se Formspree falhar, lead não se perde |
| fill-rule: evenodd | Permite buracos no path do K (cortes internos) |

---

*Documento gerado em 05/06/2026. Atualizar a cada mudança significativa.*
