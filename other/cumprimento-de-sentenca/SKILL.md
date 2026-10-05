---
name: cumprimento-de-sentenca
description: "Promove o cumprimento de sentenca (titulo executivo judicial) — disposicoes gerais (CPC 513), titulos judiciais (CPC 515), cumprimento DEFINITIVO de pagar quantia com intimacao em 15 dias e multa de 10% + honorarios de 10% se nao pago (CPC 523 §1, penhora/avaliacao §3), demonstrativo atualizado do debito (CPC 524), cumprimento PROVISORIO sob recurso sem efeito suspensivo (CPC 520-522), alimentos com prisao civil (CPC 528 §3) e Fazenda Publica (CPC 534-535). Use quando o operador disser cumprimento de sentenca, executar a sentenca, intimar para pagar em 15 dias, multa de 10% cumprimento, cobrar sentenca transitada."
---

# CUMPRIMENTO-DE-SENTENCA

> Camada 7 (cumprimento & execucao). Fase satisfativa do credor titular de titulo executivo JUDICIAL (sentenca/decisao). Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — arts. 513 (gerais), 515 (titulos judiciais), 520-522 (provisorio), 523 (definitivo: 15 dias; multa 10% + honorarios 10% §1; penhora/avaliacao §3), 524 (demonstrativo), 528-533 (alimentos), 534-535 (Fazenda) — **grep + ler a faixa**.
- `context/cpc-cc-alteracoes-recentes.md` + `context/jurisprudencia-civel.md` (so itens ✅).

## Objetivo
Deflagrar o cumprimento correto: titulo certo, demonstrativo impecavel, intimacao na forma certa e acrescimos legais no inadimplemento, ate a satisfacao do credito.

## Quando ativar
- Sentenca/acordao condenatorio transitado, ou recurso sem efeito suspensivo (provisorio); decisao homologatoria, sentenca arbitral, sentenca penal condenatoria ou outro titulo do art. 515.

## Metodologia
1. **Gestao processual SEMPRE (Camada 2):** `competencia-e-foro` (juizo do cumprimento) ; `gratuidade-e-impugnacao` ; `tempestividade-civel`.
2. **Titulo (CPC 515):** confirmar titulo JUDICIAL e o regime do art. 513. Nos incisos VI a IX, o devedor e citado para cumprir/liquidar em 15 dias (515 §1). So prosseguir liquido; se iliquido, liquidar antes (calculo via `calculosjudiciais-adv-os`).
3. **Pagar quantia — DEFINITIVO (CPC 523):** executado intimado a pagar em **15 dias** + custas. Nao pago: multa de **10%** + honorarios de **10%** (523 §1); parcial incide sobre o restante (§2); persiste, mandado de penhora e avaliacao desde logo (§3). Instruir com demonstrativo discriminado e atualizado (524): partes/CPF-CNPJ, indice de correcao, juros e taxas, termos inicial/final, capitalizacao e bens penhoraveis.
4. **PROVISORIO (CPC 520-522):** sentenca sob recurso sem efeito suspensivo; corre por iniciativa/responsabilidade do exequente (520 I); levantamento e atos de transferencia dependem de caucao (520 IV), dispensavel nas hipoteses do art. 521; multa/honorarios do 523 §1 devidos (520 §2); requerimento por peticao ao juizo (522).
5. **Alimentos (CPC 528-533):** intimacao pessoal para, em 3 dias, pagar/provar/justificar (528); nao pago e nao aceita a justificativa, protesto e **prisao civil de 1 a 3 meses** em regime fechado (528 §3-4); o debito que a autoriza = 3 prestacoes anteriores ao ajuizamento + vincendas (528 §7); alternativa pela expropriacao (528 §8).
6. **Fazenda Publica (CPC 534-535):** demonstrativo discriminado e atualizado (534); intimacao para impugnar em **30 dias** (535) — pagamento por precatorio/RPV, sem multa do 523.

## Entrega obrigatoria final
- Peticao de cumprimento ponta a ponta (qualificacao + titulo + demonstrativo atualizado + intimacao na forma certa + acrescimos do 523 §1 + penhora/avaliacao 523 §3, ou rito do 528/535) + checklist de documentos + indicacao do juizo.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria (Camada 2). Entrega pela `suprema-corte-civel` (R1-R4). Cross-link, nao duplicar: defesa do executado (titulo judicial) -> `impugnacao-ao-cumprimento`; execucao de titulo EXTRAJUDICIAL / expropriacao / cobranca -> `execucao-adv-os`; memoria de calculo / atualizacao -> `calculosjudiciais-adv-os`; consumidor (CDC), familia e sucessoes fora.
