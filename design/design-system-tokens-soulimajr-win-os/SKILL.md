---
name: design-system-tokens
description: Gestão e sincronização de Design Tokens entre Figma, código frontend (Tailwind/CSS) e materiais de marketing. Garante que cores, fontes, raios de borda, sombras e espaçamentos sejam 100% idênticos no site, nos posts do Instagram e nas propostas comerciais.
---

# Habilidade: Design System & Gestão de Tokens

## Tabela de Tokens Oficiais (Win OS & Creative)

### Cores (Color Tokens)
- `color-bg-base`: `#0b0c0e` (Obsidiana escura)
- `color-surface`: `#121316` (Cards e caixas)
- `color-surface-raised`: `#17181b` (Elementos elevados / barras de título)
- `color-accent-gold`: `#c9a24b` (Ouro metálico / Brass oficial)
- `color-accent-glow`: `rgba(201, 162, 75, 0.15)` (Halo de luz dourada)
- `color-text-primary`: `#edebe6` (Marfim / Off-white para títulos)
- `color-text-muted`: `#9a958a` (Cinza quente para apoio)
- `color-border`: `#232427` (Bordas sutis)
- `color-signal-green`: `#6e8b7a` (Indicadores de sucesso e receita)

### Tipografia (Typography Tokens)
- `font-family-display`: Fontes de autoridade, elegantes e geométricas para títulos.
- `font-family-body`: Sans-serif limpa e moderna para leitura corrida.
- `font-family-mono`: Monospace técnica com tracking espaçado (`[0.2em]`) para indicadores e tags de sistema (`/ manifesto.sys`).

### Espaçamentos & Raios (Spacing & Radii)
- `radius-sm`: `8px`
- `radius-md`: `16px`
- `radius-lg`: `24px`
- `radius-full`: `9999px` (Pílulas e botões de destaque)

## Procedimento de Aplicação
1. Para código Web: Exportar como variáveis CSS em `globals.css` ou `@theme` no Tailwind.
2. Para peças gráficas e prompts: Usar os códigos hexadecimais exatos para guiar o motor de imagem e designers.
3. Para propostas: Manter alinhamento rigoroso com a mesma paleta de cores.

## Entrega
Arquivo de tokens atualizado ou mapa de variáveis em `identidade/tokens.json` ou `/saidas/AAAA-MM-DD/marketing/tokens-<versao>.md`.
