---
name: test-audit
version: 1.0.0
description: Audita la suite de tests para hallar cobertura de bajo valor, acoplamiento a la implementacion y tests duplicados sin bajar la confianza real. Usar cuando la suite es lenta o sospechas de tests cosmeticos. No usar para borrar tests que fallan en la baseline (puede ser un bug de producto) ni para auditar codigo muerto (ver code-audit).
triggers: [/test-audit, test-audit, /tests-value]
author: agent
role: auditor
stage: review
cycle_phase: [F5-implementacion]
writes_memory: false
quality_gate: false
tags: [core, system, testing]
---

# test-audit

Skill para auditar la suite de tests del proyecto e identificar candidatos a
eliminacion/consolidacion sin perder cobertura real. Origen externo: patron
adaptado de `openclaw/openclaw` (`.agents/skills/test-audit/SKILL.md`, MIT) —
ver bloque Credits al final de este documento.

Optimiza para **confianza, no para numero de tests eliminados**. Un test que
falla en la baseline es un posible bug de producto, no un candidato a borrar.

## Por que existe

La suite canonica de este repo tiene medido `[snapshot 2026-09-24]` 336
ficheros bajo `tests/` y 6569 tests pasando (`--level all`, 875.56s). El coste
no es solo de wall-clock: cada test es superficie de mantenimiento que hay que
releer en cada refactor. No todos los tests protegen un contrato — algunos
solo repiten en el test lo que ya dice el codigo (self-comparison), duplican
un contrato ya cubierto en una frontera mas fuerte, o existen solo para
mantener vivo un seam de produccion que ningun caller real usa.

Esta skill NO asume que "menos tests" es la meta. Es una auditoria de VALOR:
cada test debe justificar su coste protegiendo un comportamiento observable,
una regresion creible o un contrato independiente.

## Relacion con skills hermanas (no duplicar, no fusionar)

Cada skill responde una pregunta distinta; fusionarlas mezclaria un flujo
read-only-por-defecto (auditoria) con uno prescriptivo-en-caliente (autoria),
y diluiria el trigger que cada una necesita. Esta skill REFERENCIA a las
demas, nunca las reimplementa:

- `skills/code-audit/SKILL.md`: dead code de PRODUCCION (vulture/deadcode/ruff
  + antiguedad git). Comparten el principio "triangular antes de borrar", pero
  `code-audit` NUNCA decide sobre tests — solo sobre codigo que los tests
  podrian dejar huerfano tras un test-audit.
- `skills/test-driven-development/SKILL.md`: gobierna la escritura de tests
  NUEVOS (Red-Green-Refactor) durante desarrollo activo. Esta skill audita
  tests YA EXISTENTES; su "authoring gate" (ver mas abajo) es el mismo tipo de
  filtro que TDD aplicaria al escribir, aplicado retroactivamente.
- `skills/systematic-debugging/SKILL.md`: si un test retenido falla en la
  baseline, se trata como bug real via esa skill, no se repara aqui a mano.
- `prompts/audit_agent_output.md` (CEM v0): gobierna el contrato de auditoria
  esceptica en general (evidencia antes que relato, etiquetas
  VERIFICADO/INFERIDO/NO VERIFICADO). Esta skill lo aplica al dominio de tests;
  no lo reproduce.
- `prompts/suite_optimization.md`: optimiza VELOCIDAD de una suite cuyo valor
  ya se asume correcto (reordena/paraleliza, nunca borra). Esta skill optimiza
  VALOR (que se ejecuta), no cuanto tarda en ejecutarse. Son complementarias y
  pueden correr en secuencia (primero valor, luego velocidad de lo que queda),
  pero no son la misma pasada ni deben fusionarse.

## When to activate

- Cuando se pide auditar/reducir la suite de tests o su tiempo de ejecucion.
- Antes de una campana de refactor grande, para saber que tests son contrato
  real y cuales son ruido que puede reescribirse sin miedo.
- Cuando `run_history.jsonl` muestra que la duracion de la suite crece sin que
  haya crecido la cobertura de contratos reales.
- Al escribir un test nuevo, para pasarlo por el authoring gate ANTES de
  commitearlo (modo autoria, ver `references/gate-checklist.md`).

## When NOT to activate

- Para optimizar la VELOCIDAD de una suite ya de alto valor (usa
  `prompts/suite_optimization.md` — es RECOLECTOR->JUEZ sobre timing, no sobre
  valor de contrato).
- Como sustituto de `code-audit` para decidir sobre codigo de produccion muerto.
- Para borrar tests sin pasar por `references/candidate-evidence.md` completo:
  un candidato sin evidencia registrada NO esta listo para editar.
- Si no hay autorizacion explicita para tocar tests existentes: esta skill por
  defecto es READ-ONLY (audita y propone), igual que `repo-compare`. Solo edita
  si el Manager/usuario aprueba el batch propuesto.

## Dos modos: campaign vs focal

Igual que `openclaw/openclaw` distingue modo autoria de modo campana, esta
skill soporta dos escalas de auditoria (decision de diseno 2026-09-24):

- **Modo FOCAL** (default, bajo riesgo): audita los tests tocados por un diff
  concreto, un directorio pequeno, o un lote explicito de candidatos que ya se
  sospechan (p.ej. los del `top_slowest` de `run_history.jsonl`). Es la
  entrada natural cuando el disparador es "este test tarda mucho" o "este
  fichero se acaba de tocar".
- **Modo CAMPAIGN** (alto volumen, deliberado): barre UN subsistema completo
  (todos los ficheros de test que posee un area) en lanes paralelos de
  discovery, igual que openclaw separa core/packages, plugins, UI/tooling y un
  barrido de patron transversal. Para este repo, los lanes naturales medidos
  son:
  - `tests/unit/` (210 ficheros `[snapshot 2026-09-24]`) — logica de
    scripts/bus aislada.
  - `tests/` raiz (110 ficheros) — gates/guards de pre-commit y pre-push
    (`test_prepush_*`, `test_check_*`).
  - `tests/integration/` + `tests/evals/` (7 ficheros) — contratos end-to-end
    y evals de seguridad (`test_eval_guard_paths.py` etc.) — LEER CON CUIDADO:
    aqui vive mas contrato de seguridad real por test que en `tests/unit/`.
  - `tests/sandbox/` + `tests/debug/` (8 ficheros) — segun
    `.claude/rules/00-startup.md`, son scripts de un solo uso; su bar de valor
    es distinto (pueden no perseguir un contrato productivo en absoluto).
  Un campaign NUNCA se hace en una sola PR: cada lane cierra su propio batch
  coherente (ver `references/edit-shape.md`), se valida, y solo entonces se
  continua con el siguiente lane.

## Workflow (7 pasos)

### Paso 1: Preflight — evidencia real, no intuicion

- Ejecutar `python scripts/run_pytest_safe.py --status` para confirmar que no
  hay lock activo y ver el `last-run.json` mas reciente.
- Leer `.agent/runtime/pytest-safe/run_history.jsonl` (motor) para:
  - la duracion real de la ultima corrida `level=all` + `args_mode=default_discovery`
    completa (NO una corrida filtrada — ver `WOT-2026-044o` en AGENTS.md);
  - el campo `top_slowest` de esa corrida como lista de candidatos objetivos
    para modo FOCAL (un test lento no es automaticamente de bajo valor, pero
    es donde el ROI de auditar primero es mayor).
- Si el objetivo es un subsistema (modo CAMPAIGN), listar sus ficheros:
  `find tests/<lane> -name "*.py" | wc -l` y anclar el denominador ANTES de
  auditar (mismo principio que `check_distribution_agnostic.py`: un censo que
  no publica su denominador no cuenta).

### Paso 2: Validar input y modo

- Si viene un path/diff concreto -> modo FOCAL sobre ese subconjunto.
- Si viene "audita `tests/unit/`" o similar -> modo CAMPAIGN sobre ese lane.
- Si no hay ninguno explicito -> usa el `top_slowest` del preflight (Paso 1)
  como arranque de modo FOCAL, declarandolo explicitamente ("sin scope dado,
  arranco FOCAL sobre los N tests mas lentos de la ultima corrida completa").
  NO te detengas a pedir permiso para esto — es el default seguro (FOCAL, bajo
  riesgo) y queda declarado en el reporte, no ejecutado en silencio.
- Si te piden "audita toda la suite" sin mas detalle -> CAMPAIGN, lane por
  lane, nunca de una vez.

### Paso 3: Authoring gate check (retroactivo)

Para cada test candidato, aplicar las 4 preguntas de
`references/gate-checklist.md` como si el test se fuera a escribir hoy.
**Cuidado con la polaridad: las preguntas 1-3 exigen respuesta CONCRETA
(no un si/no), y la pregunta 4 es una trampa invertida — "si" a la 4 es MALO
(necesita un seam artificial).** Un test PASA el gate cuando 1-3 tienen
respuesta concreta Y la 4 responde "no". Un test que NO pasa el gate (falta
respuesta en 1-3, o la 4 responde "si") es candidato a la Fase 4; uno que si
pasa, se descarta como candidato salvo que ademas matchee un
`references/junk-patterns.md`.

### Paso 4: Cotejar contra junk patterns

Aplicar el checklist completo de `references/junk-patterns.md`. Un match no es
veredicto automatico: pasa a la Fase 5 (value bar) antes de proponerse.

### Paso 5: Value bar + retention bar

Aplicar `references/value-bar.md`. **Regla dura de este repo (2026-09-24,
decision de usuario): no hay jerarquia de dominio predefinida** — un gate de
seguridad no vale automaticamente mas que un test de schema de CLI. Cada
candidato se juzga por evidencia propia: que contrato protege, que regresion
creible detecta, si existe un owner mas fuerte que ya lo cubre. Antes de
juzgar, leer el test completo, su owner de produccion, callers, callees,
hermanos y AGENTS.md/CLAUDE.md relevantes (mismo principio que M4 de este
repo: "prompt/contrato citado => leelo entero", aplicado a "test citado =>
leelo entero + su produccion").

### Paso 6: Mutation-verify obligatorio antes de proponer eliminacion

**Barrera dura, no opcional.** Este repo YA exige mutation-verify para
cualquier guard/test nuevo (AGENTS.md, seccion CEM v0: "Barrera verificada").
Aplicado a un test EXISTENTE que se propone eliminar, la carga de la prueba se
invierte: hay que demostrar que su desaparicion NO pierde deteccion real.

- Herramienta ya existente en este repo (`scripts/mutation_cycle.py`):
  protege el ciclo mutar->probar->restaurar con snapshot byte a byte. **El
  ORDEN es contra-intuitivo y hay que respetarlo al pie de la letra —
  verificado leyendo `main()` completo y su propio test de referencia
  (`tests/unit/test_mutation_cycle.py::test_fix_survives_destructive_revert`):**
  el snapshot se toma DENTRO de `main()`, al arrancar el proceso, es decir
  **DESPUES de invocar el CLI, no antes**. Si mutas el fichero a mano ANTES de
  lanzar `mutation_cycle.py`, el snapshot fotografia el ESTADO YA MUTADO, y el
  `finally` "restaura" ese mutante — el defecto queda vivo en produccion tras
  el ciclo, exactamente al reves de lo que la barrera deberia garantizar.
  **NUNCA mutes a mano antes de invocar el CLI.**
  - Secuencia CORRECTA: la mutacion se aplica DENTRO del `command` (tras el
    segundo `--`), en el mismo proceso donde corre el test — igual que hace el
    test de referencia del propio script: el snapshot se toma con el fichero
    LIMPIO, y es el comando ejecutado dentro de `run_cycle` el que escribe la
    mutacion antes de correr la comprobacion.
  - Forma practica para un mutante de texto simple (`python -c` inline que
    aplica el parche, corre pytest, y propaga su rc):
    ```bash
    python scripts/mutation_cycle.py -- <rutas de produccion a proteger> -- python -c "
    import pathlib, subprocess, sys
    p = pathlib.Path('<ruta mutada>')
    original = p.read_text(encoding='utf-8')
    p.write_text(original.replace('<fragmento original>', '<fragmento mutado>'), encoding='utf-8')
    rc = subprocess.run([sys.executable, 'scripts/run_pytest_safe.py', '--level', 'all', '--', '<nodeids del candidato y de su posible sustituto>']).returncode
    sys.exit(rc)
    "
    ```
  - **`--level all` es obligatorio dentro de ese comando, NUNCA `--level
    unit`.** Verificado en `scripts/run_pytest_safe.py::normalize_pytest_args`:
    `--level unit` antepone SIEMPRE `-m "not integration"` cuando los args no
    traen ya un `-m` explicito, y ese filtro se aplica incluso sobre nodeids
    explicitos por linea de comandos. Si el candidato o su sustituto viven en
    `tests/integration/`/`tests/evals/` (markers `integration`/`eval`/`slow`
    de `pytest.ini`), quedan DESELECCIONADOS en silencio — pytest reporta "N
    deselected", no un error — y el mutation-verify se interpreta como
    "RETENER" (el candidato "no fallo") cuando en realidad NUNCA SE EJECUTO.
    `--level all` no añade ningun filtro de marker. Antes de interpretar el
    resultado, confirma en el output de pytest que el conteo `collected`
    incluye los nodeids que pediste (no solo "N deselected").
  - Interpreta el resultado: si el candidato falla con la mutacion presente,
    detecta la mutacion; si no falla, no la detecta.
  - Tras el ciclo, verifica SIEMPRE que el fichero de produccion quedo
    restaurado a su version original (`git diff --stat <ruta>` debe salir
    vacio) — es la comprobacion barata de que la secuencia se siguio bien y de
    que no quedo un mutante vivo en el arbol.
- **Repite el ciclo por CADA caso/aserción distinta que el candidato ejercita,
  no solo una mutacion "representativa".** Dos tests pueden detectar la misma
  mutacion gruesa (borrar la validacion entera) y solo uno detectar un caso
  limite (off-by-one, string vacio, unicode); verificar solo la mutacion
  gruesa sobreestima la redundancia del candidato.
- Por cada caso, hay TRES veredictos posibles (no dos):
  - **RETENER** ese caso: el candidato es el UNICO que lo detecta. Es un
    false-positive del junk-pattern-match — promuevelo con nota en
    `references/candidate-evidence.md`.
  - **ELIMINAR** ese caso: el owner-boundary sustituto tambien lo detecta.
  - **NINGUNO DETECTA** ese caso: ni el candidato ni el sustituto fallan con
    esa mutacion. Esto NO es evidencia de que el candidato sea eliminable —
    es evidencia de que ESE CASO no tiene cobertura real en ningun lado. Abre
    un hallazgo de cobertura FALTANTE aparte (fuera del batch de limpieza) si
    el caso importa; no declares el candidato eliminable por un caso donde
    tampoco hay sustituto.
- El veredicto FINAL del candidato es ELIMINAR solo si TODOS sus casos salen
  ELIMINAR. Un solo caso en RETENER o NINGUNO DETECTA bloquea el ELIMINAR
  global (ver `references/candidate-evidence.md` para el formato exacto).
- Registrar el resultado exacto (mutado: fail esperado / sin mutar: pass) DE
  CADA CASO como parte de la evidencia del candidato — sin este recibo, el
  candidato NO esta listo para editar (mismo principio que CEM: "un exit 0 no
  basta, hace falta el artefacto").

### Paso 7: Output y batch

- Reportar con la plantilla de `references/candidate-evidence.md` — un bloque
  por candidato, TODOS los campos rellenos o el candidato no esta listo.
- Agrupar candidatos en UN batch coherente por owner boundary (ver
  `references/edit-shape.md`); nunca mezclar limpiezas de lanes distintos en
  el mismo batch.
- Persistir el reporte en `.agent/runtime/audit/test_audit/<lane-o-scope>-<YYYY-MM-DD>.md`
  (gitignored, mismo patron que `.agent/runtime/compare/` de `repo-compare`).
- **No editar tests/produccion en la misma pasada que genera el reporte**,
  salvo que el usuario ya haya aprobado modo ejecucion para ese batch
  especifico (ver Constraints).

## Constraints

- **Skill hibrida, no pura**: a diferencia de `repo-compare` (nunca escribe
  codigo), esta skill SI puede terminar editando tests/produccion — pero solo
  en la Fase de edicion, tras el batch aprobado. El descubrimiento (Pasos 1-7)
  es SIEMPRE read-only por defecto **respecto al arbol persistente**: la
  mutacion TEMPORAL del Paso 6 (mutation-verify) es la unica excepcion
  declarada, y no cuenta como "editar produccion" en el sentido que esta regla
  prohibe, porque `mutation_cycle.py` la restaura SIEMPRE antes de que el Paso
  6 termine (ver verificacion `git diff --stat` al final de ese paso). Si esa
  restauracion fallase (exit 126 del helper), el arbol SI quedaria sucio —
  DETENTE y repara antes de continuar el descubrimiento; no es un estado
  aceptable para reportar un candidato.
- **Nunca editar tests mientras la suite corre en el mismo checkout** (mismo
  riesgo de carrera que documenta openclaw para Vitest; aqui aplica a
  `run_pytest_safe.py` — comprobar `--status` antes de tocar ficheros).
- **No mezclar limpieza con refactor de produccion no relacionado**: si una
  eliminacion de test destapa un seam de produccion muerto, eliminarlo es
  DESEABLE (LOC de produccion negativa) pero se reporta como parte del mismo
  batch, con su propio diff separado en el numstat final.
- **Nunca aumentar el conteo de tests para "quedar bien"**: no se escriben
  tests de reemplazo que repiten la misma implementacion para compensar una
  eliminacion. Si hace falta cobertura nueva real, se abre como hallazgo
  aparte (Contract Formation), no como parte del mismo batch de limpieza.
- **Gate de evidencia = el mismo umbral que el resto del repo** (AGENTS.md,
  CEM v0): sin SHA/diff/exit-code/nodeid citado, el hallazgo se descarta o
  degrada, nunca se promociona a memoria ni a backlog.
- **Un test retenido que falla en la baseline es un bug de producto**: se
  reproduce y se repara en el owner, nunca se borra para "limpiar la suite".
- **Validacion final obligatoria** antes de cerrar cualquier batch:
  `python scripts/run_pytest_safe.py --level all` en verde,
  `ruff check .` en verde, y `python .agent/agent_controller.py --validate --json`
  en `0/0` si el batch toco `.agent/collaboration/`.

## References

- `references/gate-checklist.md` — Las 4 preguntas + junk patterns aplicados
  a un test NUEVO (uso preventivo, antes de commitear).
- `references/junk-patterns.md` — Checklist compartido entre autoria y
  auditoria.
- `references/value-bar.md` — Barra de valor + retention bar (que SI se
  conserva aunque parezca ruido).
- `references/candidate-evidence.md` — Campos obligatorios por candidato antes
  de editar.
- `references/edit-shape.md` — Como agrupar el batch de edicion y que validar.
- `PROMPT_TEMPLATE.md` — Prompt completo agnostico de backend, listo para
  pasarle al Builder.

## Troubleshooting

**P: ¿Que pasa si `run_history.jsonl` no tiene ninguna corrida `level=all` +
`default_discovery` completa reciente?**
R: El disparador de "test lento" queda NO VERIFICABLE para modo FOCAL por
timing; se puede seguir en modo FOCAL por sospecha manual (test citado por el
usuario) o iniciar CAMPAIGN igualmente, ya que CAMPAIGN no depende del timing.

**P: ¿Que pasa si un candidato usa un mock que hace imposible saber si prueba
algo real?**
R: Es exactamente el junk pattern "mocks that implement the asserted behavior"
— léase `references/junk-patterns.md`. Mutation-verify (Paso 6) lo confirma:
si mutar el owner real no hace fallar el test, el mock esta ocultando la falta
de cobertura.

**P: ¿Se puede automatizar el conteo de candidatos con vulture/deadcode como
en `code-audit`?**
R: No directamente — esas herramientas detectan codigo de PRODUCCION no
referenciado, no valor de un test. Un test puede tener 100% de "uso" (se
ejecuta, pasa) y seguir siendo basura porque no protege nada. El filtro aqui
es semantico (junk patterns + value bar), no de referencia estatica.

---

## Credits — origen externo

| WOT | Source | Pattern | License | Adapted vs Ported |
|----|--------|---------|---------|-------------------|
| WOT-XXXX-XXX (TBD) | [openclaw/openclaw@main](https://github.com/openclaw/openclaw/blob/main/.agents/skills/test-audit/SKILL.md) | Authoring gate + junk patterns + value/retention bar + candidate evidence + edit shape para auditoria de tests | MIT (verificar LICENSE del repo source antes de citar en `CREDITS.md`) | Adapted — estructura y checklist tomados del original; comandos, lanes de campaign, mutation-verify y umbrales de evidencia reescritos para el contrato CEM v0 y las herramientas propias de este repo (`mutation_cycle.py`, `run_pytest_safe.py`, `run_history.jsonl`). |

Cuando se adopte esta skill formalmente (abrir el ticket que la incorpora),
pegar la fila anterior (con el WOT-id real y la licencia verificada) en
`CREDITS.md` de la raiz del repo, siguiendo el contrato de
`AGENTS.md` seccion "Atribuciones externas (CREDITS.md)".

---

**Version:** 1.0.0
**Autor:** agent (adaptado de openclaw/openclaw, MIT)
**Ultima actualizacion:** 2026-09-24
