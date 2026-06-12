# Site Koldex — Planejamento de Desenvolvimento

> Versão: 1.0 | Criado: 05/06/2026
> Status: Em planejamento
> Deploy: Vercel (auto-deploy via GitHub)
> Domínio: koldex.com.br (Cloudflare DNS)

---

## 1. OBJETIVO

Landing page de alta conversão para a agência de IA **Koldex**, com foco em:

- Apresentar os serviços da agência
- Gerar leads qualificados via WhatsApp e formulário
- Posicionar a marca como premium e moderna
- Preparar estrutura para escalar (múltiplas páginas futuras)

---

## 2. PÚBLICO-ALVO

- Empresas pequenas e médias que perdem vendas por atendimento lento
- Donos de negócios que querem automatizar WhatsApp
- Profissionais liberais (clínicas, escritórios, lojas)
- Região primária: Nordeste (Campina Grande, Recife, João Pessoa)
- Perfil: decisor, 30-55 anos, busca resultados práticos

---

## 3. SERVIÇOS A APRESENTAR

| #   | Serviço                         | Status                   | Destaque   |
| --- | ------------------------------- | ------------------------ | ---------- |
| 1   | Agente de IA para WhatsApp      | Ativo (produto validado) | Principal  |
| 2   | Funis de vendas                 | Futuro                   | Secundário |
| 3   | Criação e manutenção de sites   | Futuro                   | Secundário |
| 4   | Busca de leads qualificados     | Futuro                   | Secundário |
| 5   | Manutenção de redes sociais     | Futuro                   | Secundário |
| 6   | Sistemas ERP/CRM personalizados | Futuro                   | Secundário |

---

## 4. STACK TÉCNICA

| Camada    | Tecnologia                              | Motivo                               |
| --------- | --------------------------------------- | ------------------------------------ |
| Markup    | HTML5 semântico                         | Performance, SEO, acessibilidade     |
| Estilo    | CSS3 (custom properties, grid, flexbox) | Zero dependência, performance máxima |
| Interação | JavaScript vanilla (ES6+)               | Animações, formulário, menu mobile   |
| Fonte     | Inter (Google Fonts)                    | Referência Stripe/Linear, já em uso  |
| Ícones    | SVG inline                              | Performance, customização            |
| Deploy    | Vercel                                  | Auto-deploy, CDN global, gratuito    |
| DNS/CDN   | Cloudflare                              | SSL, proteção, cache                 |
| Analytics | Google Analytics 4                      | Métricas de conversão                |
| Forms     | Formspree ou n8n webhook                | Captura sem backend                  |

### Preparação para escala futura

- Estrutura de arquivos modular (CSS separado por seção)
- Componentes reutilizáveis (buttons, cards)
- Design tokens via CSS custom properties
- Pronto para migração React/Next.js quando necessário

---

## 5. DESIGN SYSTEM

### 5.1 Paleta de Cores

| Token       | Valor                                              | Uso                           |
| ----------- | -------------------------------------------------- | ----------------------------- |
| --c-bg      | #09090F                                            | Fundo principal               |
| --c-bg1     | #0F0F1A                                            | Cards, seções alternadas      |
| --c-bg2     | #141420                                            | Elementos elevados            |
| --c-roxo    | #5B21B6                                            | Marca primária                |
| --c-roxo-v  | #7C3AED                                            | Hover, destaques              |
| --c-roxo-l  | #8B5CF6                                            | Textos destacados             |
| --c-ciano   | #06B6D4                                            | Secundária, CTAs alternativos |
| --c-ciano-l | #22D3EE                                            | Hover secundário              |
| --c-text-1  | #F8F7FF                                            | Texto principal               |
| --c-text-2  | #A8A0C8                                            | Texto secundário              |
| --c-text-3  | #665D8A                                            | Texto terciário               |
| --g-brand   | linear-gradient(135deg, #5B21B6, #7C3AED, #06B6D4) | Gradiente marca               |

### 5.2 Tipografia

| Elemento   | Size                     | Weight | Line-height |
| ---------- | ------------------------ | ------ | ----------- |
| H1 (hero)  | clamp(2.5rem, 5vw, 4rem) | 800    | 1.1         |
| H2 (seção) | clamp(2rem, 4vw, 3rem)   | 700    | 1.2         |
| H3 (card)  | 1.25rem                  | 600    | 1.3         |
| Body       | 1rem                     | 400    | 1.6         |
| Small      | 0.875rem                 | 400    | 1.5         |
| Caption    | 0.75rem                  | 500    | 1.4         |

### 5.3 Espaçamento

| Token           | Valor                  |
| --------------- | ---------------------- |
| --space-xs      | 0.5rem                 |
| --space-sm      | 1rem                   |
| --space-md      | 1.5rem                 |
| --space-lg      | 2.5rem                 |
| --space-xl      | 4rem                   |
| --space-2xl     | 7rem                   |
| --space-section | clamp(4rem, 8vw, 8rem) |

### 5.4 Componentes

- **Button Primary:** gradiente brand, sombra roxo, hover com lift
- **Button Secondary:** border roxo, fundo transparente
- **Card:** bg1, border sutil, hover com glow
- **Badge:** roxo/ciano com opacity baixa no fundo
- **Input:** bg2, border roxo no focus
- **WhatsApp Float:** fixo bottom-right, pulsando

---

## 6. ESTRUTURA DE SEÇÕES

### 6.1 Navbar

- Logo K + Koldex (SVG)
- Links: Serviços | Como funciona | Planos | Contato
- CTA: "Fale conosco" (WhatsApp)
- Hamburger mobile
- Transparente no topo, blur no scroll

### 6.2 Hero

- Badge: "Agentes de IA para WhatsApp"
- H1: "Seu atendimento trabalhando 24h. Sem folga."
- Subtitle: "Agentes de IA que atendem, qualificam e convertem seus clientes pelo WhatsApp — enquanto você foca no que importa."
- CTA 1: "Testar grátis por 7 dias" (WhatsApp)
- CTA 2: "Ver demonstração" (scroll para demo)
- Visual: mockup do WhatsApp com conversa do agente

### 6.3 Logos/Social Proof

- "Empresas que já confiam na Koldex"
- Logos em grayscale com hover colorido
- (futuro — quando tiver clientes)

### 6.4 Problemas

- H2: "Seu negócio perde vendas todos os dias"
- 3-4 cards com dores:
  - "Clientes esperam horas por uma resposta"
  - "Leads esfriando enquanto ninguém atende"
  - "Equipe sobrecarregada com perguntas repetitivas"
  - "Concorrentes mais rápidos fecham antes"

### 6.5 Solução

- H2: "A Koldex resolve isso em minutos"
- Descrição do agente de IA
- Métricas visuais:
  - "Resposta em < 3 segundos"
  - "Atendimento 24/7"
  - "0 leads perdidos"
  - "100% das mensagens respondidas"

### 6.6 Como Funciona

- H2: "3 passos para ativar seu agente"
- Step 1: "Nos conte sobre seu negócio" (ícone formulário)
- Step 2: "Configuramos o agente em 48h" (ícone engrenagem)
- Step 3: "Seu WhatsApp atende sozinho" (ícone check)

### 6.7 Features

- Grid de 6 cards:
  - Atendimento automático
  - Qualificação de leads
  - Transferência inteligente
  - Áudio e imagem
  - Histórico completo
  - Multi-idioma

### 6.8 Serviços Completos

- H2: "Tudo que sua empresa precisa para crescer"
- Cards dos 6 serviços (agente IA destacado, demais com "em breve")

### 6.9 Demo Visual

- Mockup iPhone com conversa WhatsApp
- Mostra o agente Conex respondendo
- Animação de digitação

### 6.10 Planos

- H2: "Planos que cabem no seu bolso"
- 3 cards: Starter | Pro | Enterprise
- Destaque no Pro (mais popular)
- CTA em cada card

### 6.11 FAQ

- Accordion com 6-8 perguntas frequentes

### 6.12 CTA Final

- H2: "Pronto para nunca mais perder uma venda?"
- Formulário (nome, WhatsApp, empresa)
- OU botão WhatsApp grande

### 6.13 Footer

- Logo
- Links rápidos
- Redes sociais
- CNPJ/dados legais
- "© 2026 Koldex"

---

## 7. PERFORMANCE

### Targets (Lighthouse)

- Performance: > 95
- Accessibility: > 95
- Best Practices: > 95
- SEO: > 95

### Estratégias

- CSS inline crítico no head
- Lazy load em imagens abaixo do fold
- Font preconnect + display=swap
- SVG inline para ícones (zero requests extras)
- Minificação antes do deploy
- Sem jQuery, sem bibliotecas pesadas

---

## 8. SEO

- Title: "Koldex — Agentes de IA para WhatsApp | Atendimento Automático 24h"
- Meta description otimizada
- Open Graph (Facebook/LinkedIn)
- Twitter Card
- Structured data (LocalBusiness + Organization)
- Sitemap.xml
- Robots.txt
- Canonical URLs

---

## 9. ACESSIBILIDADE (WCAG 2.1 AA)

- Contraste mínimo 4.5:1
- Skip navigation
- ARIA labels em todos os interativos
- Focus visible em todos os elementos
- Alt text em todas as imagens
- Keyboard navigation completa
- Reduced motion support

---

## 10. COPY (HEADLINES PRINCIPAIS)

| Seção         | Headline                                      |
| ------------- | --------------------------------------------- |
| Hero          | "Seu atendimento trabalhando 24h. Sem folga." |
| Problemas     | "Seu negócio perde vendas todos os dias"      |
| Solução       | "A Koldex resolve isso em minutos"         |
| Como funciona | "3 passos para ativar seu agente"             |
| Features      | "Tudo que um agente premium oferece"          |
| Serviços      | "Tudo que sua empresa precisa para crescer"   |
| Planos        | "Planos que cabem no seu bolso"               |
| CTA Final     | "Pronto para nunca mais perder uma venda?"    |

---

## 11. CRONOGRAMA DE DESENVOLVIMENTO

| Etapa | Entregas                                       | Status   |
| ----- | ---------------------------------------------- | -------- |
| 1     | Estrutura HTML + Design System + Navbar + Hero | Pendente |
| 2     | Seções: Problemas + Solução + Como funciona    | Pendente |
| 3     | Features + Serviços + Demo visual              | Pendente |
| 4     | Planos + FAQ + CTA Final + Footer              | Pendente |
| 5     | Animações + Mobile + Polish                    | Pendente |
| 6     | SEO + Performance + Deploy                     | Pendente |

---

## 12. REFERÊNCIAS VISUAIS

- stripe.com — gradientes, tipografia, espaço negativo
- linear.app — dark mode, animações sutis
- vercel.com — minimalismo, velocidade percebida
- notion.so — clareza, hierarquia
- apple.com — premium, produto como herói

---

*Próximo passo: desenvolvimento da Etapa 1 (estrutura + hero)*
