---
name: recursos-excepcionais
description: "Redige recurso especial (CPC 1.029 + CF 105 III) e recurso extraordinario (CF 102 III), com prequestionamento obrigatorio, repercussao geral no RE (1.035), regime de repetitivos (1.036-1.041) e a regra NOVA de feriado local (Lei 14.939/2024 + STJ AREsp 2.638.376 — nao e mais intempestividade automatica). Use quando o operador disser REsp, recurso especial, RE, recurso extraordinario, repercussao geral, repetitivo, prequestionamento, levar pro STJ/STF."
---

# RECURSOS-EXCEPCIONAIS — REsp / RE / Repercussao Geral / Repetitivos

> Camada 6 (recursos). Via estreita: so questao de direito, prequestionada. Sem prequestionamento, nao conhece.

## Anexos obrigatorios (context/)
- `context/recursos-tutelas-civel.md` (§2.5 REsp/RE/RG/repetitivos + §0 preparo).
- `context/cpc-13105-15.md` (arts. 1.029-1.041 + 1.030; **grep + faixa**). CF 102 III (RE) / 105 III (REsp).
- `context/cpc-cc-alteracoes-recentes.md` (Lei 14.939/2024 — feriado local, CPC 1.003 §6).
- `context/jurisprudencia-civel.md` (feriado local AREsp 2.638.376 ✅; Sumula 98/STJ ✅ — prequestionamento via ED).

## Objetivo
Levar a questao de direito ao STJ/STF com cabimento, prequestionamento e (no RE) repercussao geral demonstrados, tempestivo e preparado.

## Quando ativar
- Causa decidida em ultima/unica instancia que contrarie **lei federal/tratado ou divirja** (REsp) ou contrarie a **CF** (RE).
- Gatilhos: "REsp", "recurso especial", "RE", "recurso extraordinario", "repercussao geral", "repetitivo", "prequestionar", "STJ/STF".

## Metodologia
1. **Cabimento:** **REsp** (CF 105 III + CPC 1.029) — contrariedade a lei federal/tratado, validade de ato local contestado, ou divergencia jurisprudencial. **RE** (CF 102 III) — contrariedade a CF, (in)constitucionalidade de tratado/lei, validade de lei/ato local em face da CF. Interpor em **peticoes distintas** (1.029).
2. **Prequestionamento:** a materia tem de ter sido **decidida** no acordao. Se omisso, opor **ED** antes (Sumula 98/STJ ✅ — ED prequestionador nao e protelatorio; 1.025 — prequestionamento ficto). Sem prequestionamento -> nao conhecimento. Cross-link `embargos-de-declaracao`.
3. **Divergencia (REsp — 1.029 §1):** provar o dissidio por **cotejo analitico** (acordao paradigma + similitude fatica).
4. **Repercussao geral (RE — 1.035):** o STF nao conhece RE sem RG; demonstra-la em preliminar formal e fundamentada (§3: ha RG se contraria sumula/jurisprudencia dominante do STF ou reconhece inconstitucionalidade de tratado/lei).
5. **Tempestividade:** **15 dias uteis** (1.003 §5), dobro por sujeito. **Feriado local — regra NOVA:** Lei 14.939/2024 (CPC 1.003 §6) + **STJ Corte Especial AREsp 2.638.376/2025 ✅** — falta de comprovacao **NAO** e mais intempestividade automatica; o tribunal **manda corrigir**. Classificar como **SANAVEL**. Cruzar com `tempestividade-civel`.
6. **Preparo:** sim, sob pena de desercao (regras gerais). Calcular com `valor-da-causa`.
7. **Repetitivos (1.036-1.041):** verificar se a questao esta **afetada** (suspensao nacional — 1.037 II) ou ja tem **tese fixada** (1.040). Se desfavoravel, tentar **distinguishing** (1.037 §9); se favoravel, invocar a tese.
8. **Admissibilidade na origem (1.030):** o presidente/vice pode negar seguimento, sobrestar, devolver para retratacao ou admitir. Da decisao do inciso V cabe **agravo do 1.042**; dos incisos I e III cabe **agravo interno (1.021)** — encaminhar a `agravo-em-recurso-excepcional` ou `agravo-interno`.
9. Redigir: enderecamento ao **presidente/vice do tribunal de origem** + cabimento + prequestionamento + (RE) repercussao geral + razoes.

## Entrega obrigatoria final
- REsp e/ou RE redigidos (peticoes distintas) com cabimento, prequestionamento demonstrado e (no RE) preliminar de repercussao geral.
- Parecer de tempestividade (com a tese de saneamento de feriado local, se o caso) + preparo + nota sobre afetacao/tese de repetitivo aplicavel.

## Guard
Toda tese/sumula/tema so via `validador-civel` (feriado local e Sumula 98 ✅ ja conferidos). Sem prequestionamento, avisar do risco de nao conhecimento e indicar ED previo. Jamais tratar feriado local nao comprovado como intempestividade automatica. Entrega final pela `suprema-corte-civel`.
