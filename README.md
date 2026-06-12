# Koldex — Site Institucional

Landing page de alta conversão para a agência de IA **Koldex**.

## Stack

- HTML5 semântico
- CSS3 (custom properties, grid, flexbox)
- JavaScript vanilla (ES6+)
- Inter (Google Fonts)
- SVG inline para ícones

## Deploy

Deploy automático via **Vercel** conectado ao GitHub.

- Domínio: `koldex.com.br`
- DNS/CDN: Cloudflare

## Estrutura

```
├── index.html          # Página principal
├── css/
│   ├── tokens.css      # Design tokens
│   ├── reset.css       # Reset + a11y
│   ├── layout.css      # Container, grid
│   ├── typography.css  # Escala tipográfica
│   ├── buttons.css     # Componentes de botão
│   ├── nav.css         # Navbar
│   ├── hero.css        # Hero section
│   ├── sections.css    # Problemas, Solução, Como Funciona
│   ├── features.css    # Features + Serviços
│   ├── planos.css      # Planos, FAQ, CTA, Footer
│   ├── animations.css  # Animações e polish
│   └── utilities.css   # FAB, reveal, dividers
├── js/
│   └── main.js         # Interações
├── assets/
│   ├── k-icon.svg      # Ícone K (cor sólida)
│   ├── k-icon-gradient.svg
│   ├── favicon.svg
│   ├── logo-traced.svg # Logo completa vetorizada
│   └── logo.svg
├── vercel.json         # Config de deploy
├── robots.txt
└── sitemap.xml
```

## Performance Targets

- Lighthouse Performance: > 95
- Accessibility: > 95
- Best Practices: > 95
- SEO: > 95
