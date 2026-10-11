---
name: suite-optimization
version: 1.0.0
description: Juez que lee la evidencia de run_history.jsonl y propone, o aplica, UN piloto de optimizacion de la suite del motor sin relajar asserts ni tocar barreras git reales (salvo una mejora de fixture demostrablemente segura), distinguiendo coste eliminable de coste re-atribuido. Usar cuando la suite canonica es lenta y hay una corrida completa en run_history.jsonl de la que derivar el objetivo. No usar para auditar la calidad de los tests (ver test-audit), para activar xdist ni para optimizar a ciegas desde la atribucion de pytest.
triggers: [/suite-optimization, suite-optimization, optimizar-suite]
author: agent
role: manager
stage: implement
writes_memory: false
quality_gate: false
tags: [core, system, tests, performance, codeonly]
source_prompt: prompts/suite_optimization.md
contract_id: cid-suite-optimization-v1
---

# suite-optimization

Skill para optimizar la suite de tests del motor **basandose en evidencia**, no
en intuicion ni en la atribucion enganosa de pytest. Lee la telemetria que
`run_pytest_safe` acumula (WOT-2026-021w: `run_history.jsonl`, alimentado por el
`--durations=25` de WOT-2026-021t), clasifica los lentos por CAUSA probable y
propone UN piloto con disciplina CEM.

NO reimplementa el metodo: el flujo completo (leer evidencia, clasificar por
causa, elegir piloto con las 2 condiciones duras, trampas verificadas, aplicar
con before/after + guard de no-relajacion) vive en `prompts/suite_optimization.md`.
**El prompt es la fuente de verdad; si algo diverge, prevalece el prompt.**

## Cuando usarla

- Hay evidencia acumulada en `run_history.jsonl` de corridas `--level all` y se
  quiere reducir el wall-clock de la suite SIN degradar cobertura ni barreras.
- Como insumo previo a decidir si vale la pena xdist-all (WOT-2026-020p).

## Cuando NO usarla

- Para activar xdist `--level all` (esa es la familia 020p, sesion dedicada).
- Para tocar el sandbox/hermeticidad de tests (familia 021k/020p): requiere su
  propia sesion con diseno.
- Para "ir mas rapido" relajando asserts o mockeando git plumbing real: eso NO es
  optimizacion, es romper barreras.

## Las DOS condiciones duras del piloto

Un candidato solo es piloto valido si cumple AMBAS (detalle en el prompt):

1. **NO toca zona prohibida:** ni sandbox/hermeticidad, ni git-plumbing de
   contrato real, ni relaja asserts, ni introduce mock-drift.
2. **El coste es ELIMINABLE, no solo RE-ATRIBUIDO.** Un cambio que solo MUEVE el
   coste a otro call-site es 0s de ahorro con riesgo neto positivo. Coste =
   trabajo hecho, no numero de call-sites.

## Trampas verificadas (no re-descubrir)

- **Atribucion de pytest:** el "teardown de ~5.8-7.58s" imputado a
  `test_deliverable_type_with_extra_spaces` es el teardown del fixture
  session-scoped `_project_temp_environment`, NO un test lento (aislado da
  0.03s). Re-derivar del run_history, nunca de esa atribucion.
- **"Duplicado" != "redundante" != "optimizable":** el doble
  `_rmtree_robust(SESSION_RUNTIME_ROOT)` (conftest teardown + `pytest_sessionfinish`)
  NO es optimizable -- quitar uno mueve el coste al otro (0s ahorro) y pierde el
  defense-in-depth (WOT-2026-013i). Antes de llamar "redundante" a algo
  duplicado, PROBAR que el trabajo desaparece, no que la llamada se mueve.

## Guard obligatorio al aplicar

Si se aplica un piloto: before/after real (tiempo del test AISLADO, no la
atribucion) + **mutation-guard de no-relajacion** (romper el codigo que el test
cubre debe seguir rompiendo el test; un test mas rapido que ya no falla ante su
bug es una regresion disfrazada) + suite `--level all` verde.

## Prompt canonico

Leer y aplicar `prompts/suite_optimization.md`. Hereda filosofia CEM de
`prompts/audit_agent_output.md` y consigna adversarial de
`prompts/manager_review.md`.

## Restriccion dura

- SOLO UN piloto por corrida (no un sweep).
- La evidencia manda sobre la intuicion y sobre la atribucion de pytest.
- Ante duda entre "eliminable" y "re-atribuido": es re-atribuido -> NO aplicar.
- La skill es puntero: no redeclara el metodo. Remite al prompt.
