---
name: marketing-social-media-design
description: Define o layout, formato e composição visual de uma postagem de rede social (feed, story, reels, carrossel) para um cliente da Creative Marketing — dimensões corretas por plataforma, hierarquia visual, onde entra texto/logo/CTA na peça. Habilidade acionada pela skill orquestradora marketing-social-media. Use quando o pedido for sobre como formatar/diagramar um post, dimensões corretas pra cada rede, ou montar o layout de um carrossel — não usar para produzir vídeo do zero ou criativos de campanha de tráfego pago (isso é marketing-video-criativos) nem para escrever a legenda (isso é marketing-social-media-legenda).
---

# Habilidade: Design / Formato de Postagem

## Contexto obrigatório
Leia `/identidade/visual.md` (identidade da própria Creative — usar quando a peça é institucional) e `/marketing/contexto.md`. Quando a peça é para um **cliente**, use a identidade visual daquele cliente; pergunte ao CEO se não estiver registrada.

## O que esta habilidade faz (e não faz)
Define **como a peça deve ser composta**: formato, dimensão, hierarquia visual, onde entram os elementos (imagem, texto, logo, CTA). Não é ela quem produz a arte/vídeo final do zero — quando a peça precisar ser criada visualmente do zero (foto, vídeo, ilustração), aciona `marketing-video-criativos`. Esta habilidade entra para adaptar/diagramar o que já existe (ou orientar como deve ser produzido) nos formatos certos de cada rede.

## Dimensões de referência por formato
- **Feed (Instagram/Facebook)**: quadrado 1080x1080 ou vertical 1080x1350
- **Stories**: 1080x1920 (vertical, 9:16)
- **Reels/vídeo vertical**: 1080x1920 (9:16)
- **Carrossel**: mesma dimensão do feed em todas as lâminas, com continuidade visual entre elas (elemento que atravessa os slides, numeração ou linha de leitura)
- **Post do Google Meu Negócio**: proporção 4:3 ou 1:1, priorizar leitura rápida (sem excesso de texto na imagem)

## Procedimento
1. Identifique a plataforma e o formato do post (vem da pauta, se existir).
2. Defina a hierarquia visual: o que deve chamar atenção primeiro (geralmente a imagem/vídeo do produto/serviço ou o gancho em texto), depois a informação de apoio, depois o CTA/logo.
3. Para carrossel, defina a sequência lógica das lâminas (gancho → desenvolvimento → CTA final).
4. Garanta contraste e legibilidade de qualquer texto sobreposto à imagem (considerar a identidade visual: fundo escuro + texto claro, no padrão da Creative, ou o padrão do cliente).
5. Indique onde entra o logo/marca (posição discreta, sem competir com a informação principal).

## Entrega
Descrição do layout/formato (ou wireframe textual) por peça, salva em `/saidas/AAAA-MM-DD/marketing/design-<cliente>.md`, pronta para orientar quem for montar a arte final (o próprio design, ou repassando pra `marketing-video-criativos` produzir).

## Regras
- Não inventar elementos visuais que dependem de assets que não existem (foto do produto/serviço, logo do cliente) — pedir se faltar.
- Sempre respeitar a identidade visual registrada, não criar um estilo novo por conta própria.

## Skills complementares
Para gerar a peça gráfica de fato a partir do layout definido, pode acionar `social-media-graphic` ou `graphic-design` — sem pular as regras acima.
