---
name: marketing-video-criativos-adaptacao-trafego
description: Adapta uma peça de vídeo/imagem já pronta (orgânica) para os formatos e requisitos técnicos de campanhas de tráfego pago (Meta Ads, Google Ads). Habilidade acionada pela skill orquestradora marketing-video-criativos, geralmente pedida em conjunto com marketing-trafego-pago. Use quando o pedido for sobre transformar uma peça orgânica em criativo de anúncio — não usar para criar a peça do zero (isso é marketing-video-criativos-video/imagem) nem para o texto do anúncio (isso é marketing-trafego-pago-copy-anuncio).
---

# Habilidade: Adaptação de Criativo pra Tráfego Pago

## Contexto obrigatório
Leia `/marketing/contexto.md` e a estrutura de campanha (`marketing-trafego-pago-estrutura-campanha`, se existir) pra saber plataforma e formato exigido.

## Procedimento
1. Identifique a plataforma de destino e os formatos exigidos (ex: Meta Ads aceita feed 1:1/4:5, stories 9:16; Google Display tem tamanhos IAB específicos).
2. Adapte o enquadramento da peça original sem cortar informação essencial (produto, texto, CTA) — recompor quando o corte simples perder informação.
3. Garanta que o texto embutido na peça (se houver) respeite os limites de proporção de texto por imagem de cada plataforma, quando aplicável.
4. Gere as variações de tamanho necessárias pra cobrir os posicionamentos da campanha.
5. Confirme com `marketing-trafego-pago-copy-anuncio` se a peça precisa refletir alguma variação específica de oferta/CTA por versão.

## Entrega
Peças adaptadas por formato/plataforma, salvas/referenciadas em `/saidas/AAAA-MM-DD/marketing/adaptacao-trafego-<cliente>.md`.

## Regras
- Não ativar a peça em campanha real sem aprovação explícita do CEO.
- Não inventar informação que não estava na peça original ou no briefing.

## Skills complementares
Pode consultar `ad-creative-design` (tamanhos IAB, hierarquia de CTA em banners) como apoio técnico — sem pular as regras acima.
