---
name: marketing-canvas-designer
description: Geração de peças gráficas vetoriais, layouts e banners programáticos em SVG e HTML/Canvas de alta precisão. Use quando for necessário criar arte vetorial nítida, infográficos escaláveis, badges, selos ou banners com tipografia e logos perfeitamente renderizados sem perda de qualidade.
---

# Habilidade: Designer Vetorial SVG & Canvas

## Contexto obrigatório
Leia `/identidade/visual.md` e `identidade-win-os/DECISAO-LOGO.md`.

## Capacidades Técnicas
- **SVG Puro:** Criação de gráficos vetoriais escaláveis, gradientes lineares e radiais, efeitos de brilho metálico (`#c9a24b` e ouro), máscaras e ícones geométricos.
- **HTML + Tailwind / Canvas:** Renderização de layouts estáticos em alta resolução para exportação de criativos.
- **Tipografia Vetorizada:** Textos nítidos em qualquer resolução, sem artefatos de compressão de imagem.

## Procedimento
1. **Definição de Dimensões:**
   - Stories: `viewBox="0 0 1080 1920"`
   - Feed/Post: `viewBox="0 0 1080 1080"` ou `viewBox="0 0 1080 1350"`
   - Banners: `viewBox="0 0 1200 630"`
2. **Camadas de Composição:**
   - Camada 1: Background com gradiente escuro (`#0b0c0e` para `#121316`) e malha sutil.
   - Camada 2: Elementos gráficos, iluminação dourada e linhas conectoras.
   - Camada 3: Conteúdo de texto, títulos com contraste WCAG AA+ e badges.
   - Camada 4: Assinatura visual (logo/escudo do Win OS e CTA).
3. **Validação de Código:**
   - Garantir tags fechadas, IDs únicos para filtros/gradientes e código limpo.

## Entrega
Arquivo `.svg` ou `.html` pronto para renderização ou exportação salvo em `/saidas/AAAA-MM-DD/marketing/arte-<nome>.svg`.
