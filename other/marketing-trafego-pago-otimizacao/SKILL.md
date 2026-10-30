---
name: marketing-trafego-pago-otimizacao
description: Analisa dados de performance de uma campanha de tráfego pago já rodando e sugere ajustes (orçamento, segmentação, criativo, pausar/escalar) para melhorar geração e qualidade dos leads. Habilidade acionada pela skill orquestradora marketing-trafego-pago. Use quando o pedido for sobre otimizar, ajustar, "a campanha não está performando", escalar orçamento, ou decidir se pausa um anúncio — não usar para montar campanha nova (isso é marketing-trafego-pago-estrutura-campanha) nem para gerar o relatório formal pro cliente (isso é marketing-trafego-pago-relatorio).
---

# Habilidade: Otimização de Campanha (Tráfego Pago)

## Contexto obrigatório
Leia `/marketing/contexto.md`. Lembre: o objetivo é volume e **qualidade** do lead (lead que realmente tem interesse/perfil), não só custo por lead mais baixo.

## O que pedir se não tiver
Dados de performance do período (impressões, cliques, CTR, custo por lead, número de leads, e se possível qualidade do lead reportada pelo comercial do cliente). Sem esses dados, não é possível recomendar ajuste com segurança — pergunte ao CEO antes de sugerir qualquer mudança.

## Procedimento
1. Analise as métricas fornecidas: CTR (relevância do anúncio), custo por lead (eficiência), volume de leads (escala), e taxa de qualificação se disponível (qualidade).
2. Diagnostique o problema mais provável:
   - CTR baixo → problema de criativo/copy, não de segmentação
   - CTR ok mas custo por lead alto → problema de segmentação ou de formulário/landing muito longo
   - Volume bom mas leads de baixa qualidade → segmentação ampla demais ou oferta genérica atraindo curiosos
3. Recomende UMA ação prioritária por vez (não uma lista genérica de "tente tudo") — ex: "pausar o conjunto X, testar novo criativo no conjunto Y" — e explique o porquê com base nos dados.
4. Se a recomendação exigir mudança de orçamento ou pausar/escalar campanha, isso precisa de aprovação do CEO antes de executar.

## Entrega
Diagnóstico + recomendação, salvo em `/saidas/AAAA-MM-DD/marketing/otimizacao-<cliente>.md`.

## Regras
- Nunca executar mudanças na campanha (pausar, mudar orçamento, mudar segmentação) sem aprovação explícita do CEO.
- Não recomendar mudança sem dado que a sustente — pedir o dado antes de responder.
