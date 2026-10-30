---
name: comercial-jornada-cliente-qualificacao
description: Qualifica um lead que já chegou (via Marketing ou prospecção) antes de avançar pra proposta — perguntas de diagnóstico, critérios de fit, e roteiro de primeira conversa. Habilidade acionada pela skill orquestradora comercial-jornada-cliente. Use quando o pedido for sobre qualificar um lead, montar um quiz/formulário de diagnóstico, ou decidir se um lead tem fit — não usar para prospecção ativa (isso é comercial-jornada-cliente-prospeccao) nem para montar a proposta em si (isso é comercial-jornada-cliente-proposta).
---

# Habilidade: Qualificação de Lead

## Contexto obrigatório
Leia `/memoria/negocio.md`, `/memoria/tom-de-voz.md` e `/comercial/contexto.md`. Lembre: o Marketing entrega o lead, esta habilidade decide se/como ele avança no funil comercial.

## Procedimento
1. Defina os **critérios de fit**: o que torna um lead qualificado pra este negócio (orçamento mínimo, urgência, decisão própria, nicho compatível).
2. Estruture as **perguntas de diagnóstico** — objetivas, poucas, que já filtram fit sem parecer interrogatório (ex: seguir o padrão do exemplo em `/memoria/tom-de-voz.md`: "qual seria sua necessidade, você é X ou Y?").
3. Se o pedido for um **quiz/formulário de qualificação** (substituindo link direto de WhatsApp), estruture perguntas curtas com lógica de pontuação simples (qualificado / não qualificado / precisa de mais informação).
4. Defina o que acontece com cada resultado: lead qualificado → `comercial-jornada-cliente-proposta`; não qualificado → resposta educada de encerramento ou redirecionamento.

## Entrega
Roteiro/quiz de qualificação, salvo em `/saidas/AAAA-MM-DD/comercial/qualificacao-<contexto>.md`.

## Regras
- Nunca descartar um lead sem justificar o critério usado.
- Nunca prometer algo na qualificação que a proposta não vai poder cumprir.

## Skills complementares
Pode consultar `anthropic-skills:quizz-qualificacao` (quiz de diagnóstico que substitui link direto de WhatsApp) como apoio técnico — sem pular as regras acima.
