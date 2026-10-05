---
name: suprema-corte-civel
description: "Gate de qualidade final do plugin civel. Aplica 4 validacoes (R1 fatos/competencia/foro, R2 fundamentacao legal vigente, R3 jurisprudencia real verificada, R4 forma/pedidos/tempestividade/valor da causa/gratuidade) antes de qualquer entrega. Use SEMPRE antes de entregar peca, recurso, manifestacao ou parecer; acionada pelo civel-master ao fechar qualquer ato. Tambem quando o operador disser revisao final, valida antes de entregar, /revisao-final."
---

# SUPREMA-CORTE-CIVEL — Gate R1-R4

> Tier 0. Auditoria final obrigatoria. Nenhuma entrega sai sem passar por aqui.

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md`, `context/cc-10406-02.md`, `context/cpc-cc-alteracoes-recentes.md`, `context/jurisprudencia-civel.md`, `context/recursos-tutelas-civel.md`, `context/metodologia-civel.md`.

## As 4 validacoes
**R1 — Fatos, competencia e foro.** Os fatos batem com o caso (`memoria-de-caso-civel`)? A fase processual esta certa? **Competencia/foro corretos** (CPC 42-66 + Lei 14.879/2024 — foro de eleicao exige pertinencia)? Valor da causa adequado (CPC 291-293)?

**R2 — Fundamentacao legal vigente.** Cada dispositivo existe e esta vigente (cruzar com `context/cpc-13105-15.md` / `cc-10406-02.md`)? Atencao as reformas (`cpc-cc-alteracoes-recentes.md`): art. 63 (foro), 1.003 §6 (feriado local); **nao** citar o PL 4/2025 como lei.

**R3 — Jurisprudencia real.** Todo acordao/sumula/tema/enunciado passou pelo `validador-civel` e consta de `context/jurisprudencia-civel.md` como ✅? Nenhuma citacao 🟡 sem conferir; nenhuma ❌; nada inventado.

**R4 — Forma, pedidos e gestao processual.** A peca tem enderecamento ao orgao certo, partes, pedidos claros (com tutela se cabivel), valor da causa? **Tempestividade** conferida (dias uteis; 15 dias / ED 5 / dobro por art.: Fazenda 183 / MP 180 / Defensoria 186 / litisconsortes 229; feriado local Lei 14.939/2024)? **Gratuidade** requerida/impugnada quando cabivel? **Preliminares** (337) verificadas? Para recurso: cabimento + preparo + admissibilidade.

## Metodologia
1. Rodar R1 -> R2 -> R3 -> R4 em ordem.
2. Marcar cada item OK / CORRIGIR.
3. Se CORRIGIR, devolver a skill de origem; nao entregar.
4. So liberar quando R1-R4 = OK.

## Entrega obrigatoria final
- Veredito (LIBERADO / CORRIGIR) + lista do que foi checado + correcoes.

## Guard
Na duvida em R3, default e remover/checar. Tempestividade ou competencia/foro errados = reprova em R1/R4. Nao "passar pano".
