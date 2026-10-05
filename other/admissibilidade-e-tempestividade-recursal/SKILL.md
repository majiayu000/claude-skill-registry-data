---
name: admissibilidade-e-tempestividade-recursal
description: "Faz o juizo de admissibilidade recursal completo antes de interpor: cabimento, tempestividade (dias uteis + dobro + feriado local da Lei 14.939/2024), preparo/desercao (CPC 1.007), regularidade formal, legitimidade/interesse e sucumbencia. Gate transversal de TODO recurso. Use quando o operador disser esse recurso e cabivel?, vai ser conhecido?, conferir admissibilidade, checar preparo, desercao, feriado local, interesse recursal, antes de protocolar o recurso."
---

# ADMISSIBILIDADE-E-TEMPESTIVIDADE-RECURSAL — Gate transversal dos recursos

> Camada 6 (recursos). Roda ANTES de qualquer recurso sair. Pressuposto faltando = recurso nao conhecido (perda total).

## Anexos obrigatorios (context/)
- `context/recursos-tutelas-civel.md` (§0 prazos/preparo/desercao + tabela-mestra de recursos + §5 checklist de prazo).
- `context/cpc-13105-15.md` (arts. 1.003, 1.007, 932-1.044; **grep + faixa**).
- `context/cpc-cc-alteracoes-recentes.md` (Lei 14.939/2024 — feriado local, CPC 1.003 §6).
- `context/jurisprudencia-civel.md` (feriado local AREsp 2.638.376 ✅).

## Objetivo
Emitir parecer de ADMISSIVEL / INADMISSIVEL / SANAVEL antes de interpor, conferindo cada pressuposto recursal (intrinseco e extrinseco).

## Quando ativar
- Antes de interpor **qualquer** recurso (gate transversal acionado pela skill do recurso).
- Gatilhos: "esse recurso e cabivel?", "vai ser conhecido?", "conferir admissibilidade", "checar preparo", "desercao", "interesse recursal", "antes de protocolar".

## Metodologia
1. **Cabimento (pressuposto intrinseco):** o recurso e o **adequado** para a decisao? (sentenca -> apelacao; interlocutoria -> agravo de instrumento/Tema 988; monocratica -> agravo interno; inadmissao de REsp/RE -> 1.042 ou agravo interno). Apontar a fungibilidade quando houver duvida objetiva.
2. **Legitimidade e interesse (intrinsecos):** parte/terceiro/MP (996); ha **sucumbencia** (interesse recursal — so recorre quem foi prejudicado pela decisao)? Sem sucumbencia, falta interesse.
3. **Tempestividade (extrinseco):** delegar o calculo a `tempestividade-civel` — **dias uteis (219)**, prazo-base por ato (15 / ED 5), **dobro** Fazenda(183)/MP(180)/Defensoria(186)/litisconsortes(229, nao em autos eletronicos), recesso (220). **Feriado local — regra NOVA:** Lei 14.939/2024 (CPC 1.003 §6) + **STJ AREsp 2.638.376/2025 ✅** — nao comprovacao **NAO** e intempestividade automatica; tribunal manda corrigir -> classificar **SANAVEL**.
4. **Preparo / desercao (1.007 — extrinseco):** preparo + porte comprovados **no ato**, sob pena de desercao. Insuficiencia -> 5 dias (§2); ausencia -> recolher em **dobro** (§4); isentos no §1 (MP, Fazenda, gratuidade); autos eletronicos dispensam o porte (§3). Conferir valor com `valor-da-causa`.
5. **Regularidade formal (extrinseco):** peticao com razoes, enderecamento ao orgao certo, procuracao/representacao, pecas obrigatorias (no AI, as do 1.017), prequestionamento (nos excepcionais).
6. **Inexistencia de fato impeditivo/extintivo:** renuncia, aceitacao tacita, desistencia (998), preclusao logica/consumativa.
7. **Sintese:** marcar cada pressuposto OK / CORRIGIR / FALTA, com a base legal, e emitir o veredito.

## Entrega obrigatoria final
- Checklist de pressupostos (cabimento · interesse/sucumbencia · tempestividade · preparo · regularidade formal · ausencia de fato impeditivo) com OK/CORRIGIR/FALTA + base legal.
- Veredito **ADMISSIVEL / INADMISSIVEL / SANAVEL** + o que sanar (e como) antes do protocolo.

## Guard
Tempestividade sai de `tempestividade-civel`; dispositivos/teses so via `validador-civel`. Feriado local nao comprovado = SANAVEL, nunca perda automatica. Pressuposto faltante sem aviso reprova em R4 na `suprema-corte-civel`.
