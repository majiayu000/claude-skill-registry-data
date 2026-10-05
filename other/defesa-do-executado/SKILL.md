---
name: defesa-do-executado
description: "Orienta a ESCOLHA da via de defesa do executado conforme o titulo — embargos a execucao de titulo EXTRAJUDICIAL (CPC 914, independem de penhora/deposito/caucao; 915 prazo de 15 dias; 917 materias, inclusive excesso de execucao §2-4; 919 regra sem efeito suspensivo, atribuivel pelo juiz se garantia + requisitos de tutela §1); impugnacao para titulo JUDICIAL (CPC 525 — cross-link); e excecao/objecao de pre-executividade para materia de ordem publica conhecivel de oficio, sem garantia. Use quando o operador disser defesa do executado, fui executado, como me defender da execucao, embargos a execucao, pre-executividade, qual defesa cabe na execucao."
---

# DEFESA-DO-EXECUTADO

> Camada 7 (cumprimento & execucao). Triagem das vias de defesa: o caminho muda conforme o titulo seja JUDICIAL ou EXTRAJUDICIAL. Cross-check OBRIGATORIO com gestao processual (Camada 2).

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — arts. 914 (embargos independem de penhora/deposito/caucao), 915 (prazo 15 dias), 917 (materias + excesso §2-4), 918 (rejeicao liminar), 919 (sem efeito suspensivo; atribuivel §1) ; art. 525 (impugnacao do titulo judicial — cross-link) — **grep + ler a faixa**.
- `context/jurisprudencia-civel.md` (so ✅ — pre-executividade: confirmar a sumula antes do numero) + `context/cpc-cc-alteracoes-recentes.md`.

## Objetivo
Acertar a via ANTES de redigir: titulo judicial -> impugnacao; extrajudicial -> embargos; ordem publica -> pre-executividade. Errar a via custa o prazo e a defesa.

## Quando ativar
- Cliente foi executado e precisa decidir qual instrumento de defesa cabe (duvida entre embargos, impugnacao ou pre-executividade).

## Metodologia
1. **Gestao processual SEMPRE (Camada 2):** `tempestividade-civel` (qual prazo corre) ; `competencia-e-foro` (se houver vicio de competencia).
2. **Natureza do titulo (decisivo):** titulo executivo JUDICIAL (sentenca, decisao homologatoria, sentenca arbitral etc.) -> defesa e a **impugnacao** -> `impugnacao-ao-cumprimento` (CPC 525). Titulo EXTRAJUDICIAL -> defesa sao os **embargos a execucao**.
3. **Embargos — titulo extrajudicial (CPC 914-919):** independem de penhora, deposito ou caucao (914); prazo de **15 dias** (915); materias do art. 917 — inexequibilidade/inexigibilidade (I), penhora/avaliacao (II), excesso ou cumulacao indevida (III), retencao por benfeitorias na entrega de coisa (IV), incompetencia (V) e **qualquer materia deduzivel como defesa no conhecimento (VI)**. No excesso, declarar o valor correto e o demonstrativo sob pena de rejeicao (917 §3-4).
4. **Efeito suspensivo dos embargos (CPC 919):** regra e que **nao tem** (caput); o juiz o atribui a requerimento quando presentes os requisitos da tutela provisoria **e** garantida a execucao por penhora, deposito ou caucao (§1).
5. **Pre-executividade (excecao/objecao):** via excepcional, por simples peticao nos autos, para **materia de ordem publica conhecivel de oficio** (condicoes da acao, pressupostos processuais, nulidade do titulo, prescricao aferivel de plano), **sem garantia** e sem dilacao probatoria. NAO citar numero de sumula sem confirmar em `context/jurisprudencia-civel.md` via `validador-civel`; na duvida, descrever sem numero. Cabivel combinar a pre-executividade (urgente, sem garantia) com embargos/impugnacao dentro do prazo.

## Entrega obrigatoria final
- Diagnostico da via correta (com fundamento) + minuta da peca escolhida (embargos OU pre-executividade), ou roteamento para `impugnacao-ao-cumprimento` se o titulo for judicial + checklist de prazo e garantia.

## Guard
Nenhum dispositivo/jurisprudencia sem `validador-civel`. Gestao processual transversal obrigatoria (Camada 2). Entrega pela `suprema-corte-civel` (R1-R4). Cross-link, nao duplicar: defesa em titulo JUDICIAL -> `impugnacao-ao-cumprimento`; deflagracao do cumprimento -> `cumprimento-de-sentenca`; execucao de titulo EXTRAJUDICIAL pesada / expropriacao -> `execucao-adv-os`; recalculo do debito -> `calculosjudiciais-adv-os`; consumidor (CDC), familia e sucessoes fora.
