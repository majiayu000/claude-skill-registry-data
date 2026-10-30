---
name: marketing-trafego-pago-copy-anuncio
description: Escreve o texto/copy de um anúncio de tráfego pago (headline, descrição, CTA) para campanhas de geração de leads, em qualquer nicho de negócio. Habilidade acionada pela skill orquestradora marketing-trafego-pago. Use quando o pedido for especificamente sobre o texto do anúncio em si — não usar para definir segmentação/orçamento (isso é marketing-trafego-pago-estrutura-campanha) nem para produzir a imagem/vídeo do anúncio (isso é marketing-video-criativos).
---

# Habilidade: Copy do Anúncio (Tráfego Pago)

## Contexto obrigatório
Leia `/memoria/tom-de-voz.md` e `/marketing/contexto.md` (nicho do cliente). O anúncio fala com o **lead final** (quem vai comprar/contratar), não é o tom institucional da Creative — use o tom do cliente anunciante quando definido; na falta dele, seja direto e claro, sem jargão de marketing.

## Nunca invente
Preço, condições de pagamento, especificações do produto/serviço, prazo — pergunte ao CEO se esses dados não foram fornecidos e o anúncio depender deles.

## Procedimento
1. **Headline**: uma promessa clara e específica (não genérica) — destaque um diferencial real do produto/serviço/oferta, não frases vagas tipo "o melhor pra você".
2. **Descrição**: 2-3 linhas reforçando o diferencial + criando urgência/relevância real (lançamento, últimas unidades, condição especial) — só se for verdade, nunca inventar escassez.
3. **CTA**: direto e de baixo atrito — "Fale com um consultor", "Receba mais informações", "Agende uma visita" — evitar CTA vago como "saiba mais" quando o objetivo é geração de lead.
4. Gere **2-3 variações** de headline/descrição para possibilitar teste A/B, quando o pedido não pedir uma única versão fechada.
5. Se o formato for Meta Ads, considere formulário nativo de leads (perguntas objetivas: nome, telefone, interesse). Se for Google Ads (Search), alinhe a copy às palavras-chave usadas na estrutura da campanha.

## Entrega
Salvar em `/saidas/AAAA-MM-DD/marketing/copy-anuncio-<cliente>.md`, com as variações organizadas por headline/descrição/CTA.

## Regras
- Nunca publicar/ativar o anúncio sem aprovação explícita do CEO.
- Sem promessas que a Creative ou o cliente não podem garantir.

## Skills complementares
Para gerar mais variações de headline/descrição em escala, ou técnicas específicas de copy por plataforma, pode consultar a skill `ad-creative` (do ecossistema geral, não específica da Creative) como apoio — sem pular as regras acima.
