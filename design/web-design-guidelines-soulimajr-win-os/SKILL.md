---
name: web-design-guidelines
description: Auditoria de qualidade de UX, acessibilidade (WCAG) e padrões de performance para sites e landing pages. Inspirada na suíte de heurísticas da Vercel Labs (vercel-labs/web-design-guidelines). Use para revisar páginas web antes do deploy, corrigindo áreas de toque, contraste de cores, tempo de carregamento e usabilidade mobile.
---

# Habilidade: Auditoria de Web Design & UX Guidelines

## Checklist de 6 Pilares de Qualidade

### 1. Acessibilidade & Contraste (WCAG 2.1 AA)
- Texto normal: relação mínima de contraste de 4.5:1 com o fundo.
- Textos grandes (títulos > 24px): relação mínima de 3:1.
- Elementos interativos com foco visível (`focus-visible`).

### 2. Ergonomia Mobile
- Área de clique/toque mínima para botões e links: 48x48px (ou espaçamento compensatório).
- Tamanho de fonte base no mobile não menor que 16px para evitar zoom automático em inputs no iOS.
- Margens laterais mínimas de 16px a 24px nas bordas da tela.

### 3. Hierarquia Visual & Escaneabilidade
- Apenas um título `<h1>` por página.
- Sequência lógica de títulos (`<h2>`, `<h3>`).
- Parágrafos curtos (máximo de 3 a 4 linhas por bloco de texto).

### 4. Performance & Core Web Vitals
- Imagens otimizadas em formato WebP/AVIF com dimensões explícitas para evitar CLS (Cumulative Layout Shift).
- Fontes pré-carregadas ou otimizadas via Next/Font.
- Páginas com carregamento estático e cache CDN ativado.

### 5. Formulários & Checkout
- Labels claros acima dos campos.
- Mensagens de erro em tempo real.
- Botão de envio desabilitado durante o carregamento para evitar cliques duplos.

## Procedimento de Auditoria
1. Varrer o código da página alvo.
2. Identificar violações de heurística (contraste, toque, espaçamento).
3. Aplicar as correções diretamente no código ou documentar no relatório.

## Entrega
Relatório de conformidade ou correções aplicadas salvo em `/saidas/AAAA-MM-DD/marketing/auditoria-web-<pagina>.md`.
