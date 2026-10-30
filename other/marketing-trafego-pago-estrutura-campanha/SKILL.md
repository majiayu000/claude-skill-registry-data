---
name: marketing-trafego-pago-estrutura-campanha
description: Faz o diagnóstico inicial do cliente e estrutura uma campanha de tráfego pago (objetivo, orçamento, segmentação, plataforma) para geração de leads, em qualquer nicho de negócio. Habilidade acionada pela skill orquestradora marketing-trafego-pago. Use quando o pedido for sobre planejar/estruturar uma campanha nova, definir público-alvo, orçamento ou objetivo de uma campanha de ADS — não escreve o texto do anúncio (isso é marketing-trafego-pago-copy-anuncio) nem acompanha campanha já rodando (isso é marketing-trafego-pago-otimizacao).
---

# Habilidade: Estrutura de Campanha (Tráfego Pago)

## Contexto obrigatório
Leia `/memoria/negocio.md`, `/memoria/tom-de-voz.md` e `/marketing/contexto.md`. Lembre sempre: o papel da Creative é **gerar leads** — a conversão em venda é do cliente. A estrutura da campanha deve otimizar pra geração e qualificação de lead, não pra venda direta.

## O que perguntar ao CEO antes de estruturar (se não estiver registrado em `/marketing/contexto.md`)
- Qual o nicho do cliente e o que ele vende/oferece?
- Tipo de produto/serviço (ticket alto/baixo, recorrente/pontual, físico/digital)
- Região de atuação / raio de segmentação geográfica (se relevante ao negócio)
- Orçamento disponível (mensal ou por campanha)
- Plataforma preferida (Meta Ads, Google Ads, ou ambas) — se não souber, recomende com base no objetivo
- Já existe pixel/conversão configurada, ou é a primeira campanha?

## Procedimento
1. Defina o **objetivo** da campanha: geração de leads (formulário/WhatsApp), tráfego pro site, ou reconhecimento — o padrão é geração de leads, salvo indicação contrária.
2. Escolha a **plataforma**: Meta Ads (Facebook/Instagram) funciona bem pra segmentação de interesse/comportamento e formulário nativo de leads; Google Ads (Search) funciona bem pra captar quem já está buscando ativamente aquele produto/serviço/região. Recomende com base no objetivo e orçamento do cliente.
3. Defina a **segmentação**: localização (se o negócio depende de região), perfil demográfico (idade, renda estimada quando disponível), interesses/comportamento (para Meta) ou palavras-chave (para Google) — sempre alinhados ao nicho específico do cliente.
4. Defina a **estrutura de orçamento**: sugestão de divisão diária/mensal e teste inicial (ex: rodar 3-5 dias antes de otimizar).
5. Liste o que a campanha vai precisar dos outros funcionários: copy do anúncio (`marketing-trafego-pago-copy-anuncio`) e, se precisar de peça visual nova, sinalizar para `marketing-video-criativos`.

## Entrega
Documento de estrutura da campanha, salvo em `/saidas/AAAA-MM-DD/marketing/estrutura-campanha-<cliente>.md`, contendo: objetivo, plataforma, segmentação, orçamento sugerido, e o que falta pra campanha ficar pronta (copy, criativo).

## Regras
- Nunca criar/ativar a campanha de fato na plataforma sem aprovação explícita do CEO.
- Nunca comprometer orçamento sem confirmação do CEO.

## Skills complementares
Para detalhes específicos de configuração por plataforma (estrutura de conta, tipos de campanha, boas práticas), pode consultar `ads-meta` (Meta Ads) ou `ads-google` (Google Ads) como apoio técnico — sem pular as regras acima.
