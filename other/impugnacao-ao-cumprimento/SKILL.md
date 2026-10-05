---
name: impugnacao-ao-cumprimento
description: "Redige a impugnacao ao cumprimento de sentenca (CPC 525) — defesa do executado em titulo JUDICIAL, no prazo de 15 dias apos os 15 do art. 523 e independentemente de penhora, com as hipoteses do §1 (I-VII: nulidade de citacao, ilegitimidade, inexigibilidade, penhora/avaliacao, excesso de execucao, incompetencia, causa extintiva superveniente), dever de declarar o valor correto sob pena de rejeicao (§4-5) e efeito suspensivo so com garantia + grave dano (§6). Use quando o operador disser impugnar cumprimento, impugnacao ao cumprimento de sentenca, excesso de execucao, defender de cumprimento de sentenca, executado quer se defender de sentenca."
---

# IMPUGNACAO-AO-CUMPRIMENTO

> Camada 7 (cumprimento & execucao). Defesa do executado em titulo executivo JUDICIAL, no proprio processo. Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — art. 525 (prazo; hipoteses §1 I-VII; valor correto §4-5; efeito suspensivo §6; simples peticao §11; inexigibilidade por inconstitucionalidade §12) ; arts. 523-524 (cumprimento que a precede) — **grep + ler a faixa**.
- `context/cpc-cc-alteracoes-recentes.md` + `context/jurisprudencia-civel.md` (so itens ✅).

## Objetivo
Impugnacao admissivel: prazo certo, hipotese do §1 bem enquadrada, valor correto declarado no excesso (sob pena de rejeicao) e, se cabivel, efeito suspensivo fundamentado.

## Quando ativar
- Executado intimado/ciente do cumprimento de pagar quantia (titulo JUDICIAL) e quer se defender, havendo materia: inexigibilidade, ilegitimidade, excesso de calculo, penhora incorreta, incompetencia ou fato superveniente.

## Metodologia
1. **Gestao processual SEMPRE (Camada 2):** `tempestividade-civel` (prazo critico) ; `competencia-e-foro` (se arguir incompetencia) ; `gratuidade-e-impugnacao`.
2. **Prazo (CPC 525, caput):** transcorridos os 15 dias do art. 523 sem pagamento, inicia-se o prazo de **15 dias** para impugnar, **independentemente de penhora ou nova intimacao**, nos autos. Contagem em dias uteis (CPC 219).
3. **Hipotese (CPC 525 §1):** I — falta/nulidade da citacao se o processo correu a revelia; II — ilegitimidade; III — inexequibilidade do titulo ou inexigibilidade da obrigacao; IV — penhora incorreta ou avaliacao erronea; V — excesso de execucao ou cumulacao indevida; VI — incompetencia; VII — causa modificativa/extintiva (pagamento, novacao, compensacao, transacao, prescricao) **superveniente a sentenca**.
4. **Excesso de execucao (CPC 525 §4-5):** ao alega-lo, **declarar de imediato o valor correto** com demonstrativo atualizado. Sem isso: rejeicao liminar se for o unico fundamento; sem exame do excesso se houver outro (§5). Calculo via `calculosjudiciais-adv-os`.
5. **Inexigibilidade por inconstitucionalidade (CPC 525 §12):** inexigivel a obrigacao fundada em lei/ato declarado inconstitucional pelo STF, com decisao anterior ao transito (§14) — validar via `validador-civel`. Fato superveniente ao prazo ou vicio de penhora/avaliacao: simples peticao em 15 dias da ciencia (§11).
6. **Efeito suspensivo (CPC 525 §6):** a impugnacao **nao impede** os atos executivos; o juiz so o atribui a requerimento, **garantido o juizo** (penhora, caucao ou deposito) **e** se os fundamentos forem relevantes **e** houver risco de grave dano de dificil ou incerta reparacao.

## Entrega obrigatoria final
- Impugnacao ponta a ponta (tempestividade + hipotese(s) do §1 + valor correto e demonstrativo no excesso + efeito suspensivo fundamentado se cabivel + pedidos) + checklist de admissibilidade.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria (Camada 2). Entrega pela `suprema-corte-civel` (R1-R4). Cross-link, nao duplicar: qual via cabe -> `defesa-do-executado`; deflagracao do cumprimento -> `cumprimento-de-sentenca`; execucao de titulo EXTRAJUDICIAL / expropriacao -> `execucao-adv-os`; recalculo do debito -> `calculosjudiciais-adv-os`; consumidor (CDC), familia e sucessoes fora.
