---
name: tempestividade-civel
description: "Calcula prazo processual civel (dias uteis CPC 219, marco inicial CPC 231, recesso/suspensao CPC 220-221, dobro por sujeito) e emite parecer de tempestividade. Aplica a regra NOVA de feriado local (Lei 14.939/2024 + STJ AREsp 2.638.376). Use ao verificar se contestacao, recurso, manifestacao ou peca esta no prazo; quando o operador disser calcular prazo, conferir tempestividade, ate quando posso protocolar, prazo em dobro, feriado local, recesso. Acionada pelo civel-master na gestao processual transversal de TODA peca."
---

# TEMPESTIVIDADE-CIVEL — Calculo de prazo + parecer

> Camada 2 — gestao processual transversal (o "nao esquecer nada"). Prazo errado = peca perdida.

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` — arts. 219 (dias uteis), 220-221 (suspensao/recesso), 224, 229-231 (marco inicial, dobro litisconsortes), 180/183/186 (dobro MP/Fazenda/Defensoria).
- `context/cpc-cc-alteracoes-recentes.md` — Lei 14.939/2024 (CPC 1.003 §6 — feriado local).
- `context/recursos-tutelas-civel.md` — tabela de prazos por recurso + preparo.

## Objetivo
Converter intimacao/publicacao em data fatal precisa, com justificativa legal de cada etapa, e emitir parecer de TEMPESTIVO / INTEMPESTIVO / SANAVEL. Sempre grep o artigo no anexo antes de citar.

## Quando ativar
- Operador pergunta a data fatal de um prazo ou se uma peca esta no prazo.
- Antes de qualquer recurso ou contestacao (gate transversal do `civel-master`).
- Gatilhos: "calcula o prazo", "ate quando protocolo", "isso esta tempestivo?", "prazo em dobro", "recesso", "feriado local", "intempestivo".

## Metodologia
1. **Coletar dados**: data e meio da intimacao (eletronica/pessoal/DJEN), tipo de ato (contestacao, ED, recurso geral), sujeito (parte privada / Fazenda / MP / Defensoria / litisconsortes), tribunal (para feriado local), processo eletronico (sim/nao).
2. **Marco inicial (CPC 231 — grep)**: definir o dia do comeco do prazo conforme o meio (intimacao eletronica, carta, oficial de justica, DJEN). A contagem **exclui o dia do comeco e inclui o do vencimento**; inicio no 1o dia util seguinte.
3. **Contar so dias uteis (CPC 219 — grep)**: prazos processuais em dias contam **somente dias uteis**. Pular sabados, domingos, feriados nacionais, feriados forenses do tribunal.
4. **Prazo-base por ato (anexo recursos-tutelas)**: regra geral **15 dias uteis** (CPC 1.003 §5); **ED 5 dias** (CPC 1.023, sem preparo); contestacao 15 dias (CPC 335).
5. **Dobro por sujeito (grep)**: **Fazenda 183** · **MP 180** · **Defensoria 186** · **litisconsortes com procuradores de escritorios distintos 229** — **NAO se aplica em autos eletronicos (CPC 229 §2)**. Dobro incide sobre o prazo-base (recurso geral vira 30; ED vira 10).
6. **Suspensao/recesso (grep)**: **CPC 220** suspende o prazo entre **20/12 e 20/01** (inclusive); **CPC 221** suspende por obstaculo da parte / forca maior. Descontar dias suspensos.
7. **Feriado local — regra NOVA**: se a tempestividade depender de feriado local, aplicar **Lei 14.939/2024 (CPC 1.003 §6)** + **STJ Corte Especial AREsp 2.638.376 (2025)** — a falta de comprovacao **NAO** e mais intempestividade automatica; o tribunal **manda corrigir o vicio** ou o desconsidera se a info ja consta dos autos eletronicos. Classificar como **SANAVEL**, nunca como perda automatica.
8. **Calcular a data fatal** somando os dias uteis a partir do marco inicial, com a regua D-7 / D-3 / D-1 / D-0. Mostrar o passo a passo (cada dia contado e por que foi pulado).

## Entrega obrigatoria final
- Data fatal com calculo passo a passo (dias uteis enumerados) + base legal de cada etapa.
- Parecer: **TEMPESTIVO / INTEMPESTIVO / SANAVEL** (com a tese de saneamento se feriado local).
- Regua de lembretes D-7/D-3/D-1/D-0 e alerta de risco.

## Guard
Nenhum dispositivo entra sem `validador-civel`. Jamais tratar feriado local nao comprovado como intempestividade automatica (Lei 14.939/2024). Na duvida sobre o marco inicial ou o dobro, classificar como risco e mandar conferir ao vivo. Tempestividade errada reprova em R4 na `suprema-corte-civel`.
