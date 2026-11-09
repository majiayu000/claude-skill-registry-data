---
name: mejorar-ecosistema
description: >-
  Autocorrección CONSULTADA del ecosistema: cuando la IA detecta que algo está mal o se puede mejorar
  en la arquitectura, las reglas, una skill, un script o el Cerebro —por un hallazgo del Doctor, un
  pendiente que se repite, una verificación que siempre da SIN DATOS, una fricción de los workers, un
  postmortem—, lo registra como PROPUESTA en cerebro-digital/configuracion-ia/mejoras.md y se lo
  pregunta al humano, una propuesta por vez, con el qué, el porqué, el impacto y el cambio exacto.
  NUNCA aplica un cambio de arquitectura, skills o scripts por su cuenta: aplica sólo lo aprobado, por
  los canales normales (curator, sync-skills, tests), y lo deja asentado. Usar cuando se pida "¿qué
  mejorarías?", "revisá el ecosistema", "proponé mejoras", "/mejorar-ecosistema", y al cierre de
  cada Tarea o lote cuando quedaron señales acumuladas. Español (Argentina).
---

# Mejorar el ecosistema — autocorrección consultada

La IA que construye la aplicación también **ve** dónde el propio ecosistema falla: una convención que
todos los workers rompen igual, un script que siempre da `SIN DATOS`, una skill que pide un dato que
nadie tiene, una decisión del Cerebro que el código contradice. Esta skill convierte eso en
**propuestas con dueño** y las somete a decisión humana. **Propone, no aplica.**

> **Por qué consultada y no automática.** Un cambio en una skill o en un script cambia cómo trabajan
> todos los agentes a partir de ese momento; un cambio de arquitectura cambia el código que se va a
> escribir. Son decisiones de equipo. Que la IA las vea es el valor; que las aplique sola es el riesgo.

## De dónde salen las señales

| Señal | Dónde aparece | Qué suele indicar |
|---|---|---|
| Hallazgo del Doctor que se repite en dos corridas | `doctor/salida/historico` | Una regla que falta, o una que nadie puede cumplir |
| Un control del verificador que da `SIN DATOS` siempre | Comentarios de cierre de las Tareas | Falta una decisión (`DEC-003`, `C8`) o un script |
| La misma convención `C1…C8` en HALLAZGO en varias Tareas | Comentarios de cierre, Merge Requests | La regla está mal escrita, o la misión no la pasa bien |
| Un **pendiente a confirmar** que vuelve en tres tarjetas | `comentar-tarea`, `pendientes.md` | Un hueco del Cerebro que hay que cerrar de una vez |
| Preguntas de los workers que el orquestador contesta siempre igual | Misiones y respuestas | Falta en la misión o en el esqueleto |
| Un paso de una skill que el humano saltea o corrige siempre | La conversación | La skill pide de más o pide mal |
| Un postmortem de un lote o de una entrega | `borrador/lote-*/`, el cierre del lote | Lo que se aprendió y todavía no está escrito |
| **La tendencia de las últimas sesiones da PEOR** (más bloqueantes por veredicto, más SIN DATOS que frenan, más fricciones, más preguntas, más errores de script, más Tareas fallidas) | `bin/tendencia.py` al abrir cada sesión (hook `SessionStart`), sobre el archivo `sesiones.jsonl` de `configuracion-ia/` que escribe `bin/registrar-sesion.py` al cerrar (hook `SessionEnd`) | Algo que cambió en el Cerebro, en una skill o en una misión está costando más: se mira qué cambió entre las sesiones buenas y las malas |
| Un script que falla o cuenta mal | Las pruebas `bin/probar-*.py`, el autocontrol del Doctor | Un bug del ecosistema |
| **Una skill que nadie usa**, o dos con la misma pregunta | `bin/medir-uso-skills.py` (lee las transcripciones locales de Claude Code: invocaciones por el modelo y comandos `/nombre` de la persona, con fecha y costo de contexto) | Skill de más: candidata a poda o a fusión |
| Skills, MCP o plugins sin uso frente a su costo; `CLAUDE.md` duplicado o derivable del código; hooks lentos | `/doctor` de Claude Code (alias `/checkup`): informa y pide confirmación antes de tocar | Peso muerto en el contexto |
| Instrucciones viejas o que se contradicen entre `AGENTS.md`, reglas, skills y agentes | `/doctor prompt-audit` de Claude Code: propone ediciones, no cambia nada solo | Reglas que envejecieron |
| Qué pesa en cada sesión | `/context` (qué se cargó y cuánto cuesta) y `/usage` (qué skills, subagentes y MCP consumen el plan) | Dónde se va el contexto |
| Correcciones que la persona repite | La **auto memory** de Claude Code (`memory/` del proyecto, por máquina) | Una regla que falta en `AGENTS.md`, una convención, o un `AP-nnn` para `aplicacion/aprendizajes.md` |
| Una skill que se dispara cuando no debería, o no se dispara cuando sí | `bin/verificar-skills.py` (descripción dentro de la especificación) y el `skill-creator` de Anthropic con sus evals (un `evals.json` por skill, en su carpeta `evals`: casos antes/después) | Descripción mal calibrada: sobregiro |

No se buscan señales "por las dudas" en cada turno: se recogen al **cerrar** una Tarea, un lote, una
corrida del Doctor o cuando el humano lo pide.

## Poda de skills: el criterio (lo que pasó en el proyecto de origen)

El proyecto de origen terminó con skills de más: cada una pedía cosas, se pisaban, y el código se sobregiraba.
Una skill es **candidata a sacar o fusionar** cuando se da **una** de estas, con la evidencia del script al lado:

| Señal | Evidencia | Qué se propone |
|---|---|---|
| **Cero usos** en 60 días (ni el modelo ni la persona) y su pregunta la cubre otra skill | `medir-uso-skills.py` + la tabla «una pregunta por skill» de `COMO-USAR-ESTE-TEMPLATE.md` | Sacarla (y bajar el conteo en los cuatro documentos) |
| **Dos skills con la misma pregunta** o con texto compartido | Lectura de las dos descripciones; `verificar-skills.py` | Fusionar, como pasó con las de orquestación (M-002) |
| **Se dispara en pedidos que no son suyos** (sobregiro) o pide pasos que el humano saltea siempre | La conversación; `/doctor prompt-audit` | Acortar la descripción o mover lo de más a `references/` |
| **Pesa mucho y se usa poco** | `medir-uso-skills.py` (tokens) y la sonda «Tamaño» del Doctor | Partirla o moverla a `references/` con carga bajo demanda |

Nada se saca solo: la propuesta va a `mejoras.md` con la fila de evidencia y la decide una persona. Cero usos
puede querer decir «todavía no llegó esa etapa», y eso lo sabe la persona, no el script.

## La tendencia, cada sesión (sin hacer nada)

Al cerrar una sesión de Claude Code, el hook `SessionEnd` corre `bin/registrar-sesion.py`: deja **una línea de conteos** en el
archivo `sesiones.jsonl` de `configuracion-ia/` (skills usadas, veredictos con sus bloqueantes y SIN DATOS, fricciones
reportadas por los agentes, Tareas terminadas y fallidas, preguntas que frenaron, errores de script, duración). Nunca
texto, nunca datos de personas. Al abrir la siguiente, el hook `SessionStart` muestra la frase de `bin/tendencia.py`:

```
[tendencia] Ultimas 5 sesion(es): MEJOR que las 5 anteriores. Mejora: bloqueantes por veredicto 0,4 -> 0,0; fricciones por sesion 6,0 -> 2,0.
```

**Cuando dice PEOR**, esta skill mira qué cambió entre las sesiones buenas y las malas (qué skills se usaron, qué
veredictos, qué fricciones) y propone **un** ajuste, como siempre: la persona decide, nada se aplica solo. Lo único que
se escribe sin preguntar es la línea de métricas. Los hooks viajan en el `settings.json` de la carpeta `.claude/` (sin secretos) y
`bin/instalar.py` avisa si faltan. Detalle completo: `python bin/tendencia.py` (sin `--breve`).

## El ritual mensual (quince minutos)

```
python -B bin/medir-uso-skills.py --dias 60 --proyecto <ruta del núcleo>   # qué se usó, qué no, qué pesa
bash doctor/bin/doctor.sh --comparar                                         # cómo venimos
python -B bin/verificar-skills.py                                            # la especificación
/doctor                     (en Claude Code: skills, MCP y plugins sin uso frente a su costo; CLAUDE.md derivable)
/doctor prompt-audit        (en Claude Code: instrucciones viejas o contradictorias, con ediciones propuestas)
```

Lo que salga se convierte en propuestas, **de a una**, y se decide. Las dos herramientas de Claude Code informan
primero y piden confirmación antes de tocar: encajan en esta regla sin cambiarla.

## El registro: `cerebro-digital/configuracion-ia/mejoras.md`

Una fila por propuesta, siempre, antes de preguntar:

| # | Fecha | Señal (fuente) | Qué cambiar (archivo) | Por qué | Impacto | Estado |
|---|---|---|---|---|---|---|

Estados: `propuesta` → `aceptada` / `rechazada` / `pospuesta` → `aplicada` (con el commit o la entrada de `log.md`).
Una propuesta rechazada **queda escrita** con el motivo: así no se vuelve a proponer lo mismo.

## Cómo se propone (una por vez)

Cada propuesta es **una Consulta Interactiva de Decisión** ([[cerebro-orquestador]] §«Paso B»), con la
herramienta nativa de preguntas del entorno si existe, nunca como tabla en la respuesta. El enunciado
lleva, en criollo:

1. **Qué está mal o qué se podría mejorar**, con la señal y su fuente (`archivo:línea`, `#ID`, corrida del Doctor).
2. **Qué cambio concreto** se propone: el archivo y el texto o el diff exacto (si es un script, el cambio y la prueba que lo cubre; si es una skill, el párrafo; si es arquitectura, la `DEC-nnn` nueva o modificada).
3. **Qué impacta**: a quién le cambia el trabajo (workers, verificador, funcionales), qué se vuelve a verificar, si rompe algo existente.
4. **Qué pasa si no se hace.**

Opciones fijas: **Aplicar** · **Rechazar** (con motivo) · **Editar y aplicar** · **Posponer**. El silencio no es un sí.

**Tipos de cambio y qué piden además:**

| Tipo | Canal de aplicación | Pide además |
|---|---|---|
| Cerebro (ficha, decisión, pendiente) | `cerebro-curator`, con `log.md` | Si cambia una `RN`/`DEC`, el footer de trazabilidad |
| Regla de `AGENTS.md` | Edición directa + entrada en `log.md` | Que `bin/probar-reglas.*` siga en OK si toca lo que mide |
| Skill | Edición en la fuente + `bin/sync-skills.*` | Si cambia el conteo o el nombre, actualizar `AGENTS.md`, `README.md`, `INSTALACION.md` e `index.md` (el hook lo exige) |
| Script de `bin/` o del Doctor | Edición + su `probar-*.py` en OK | Un script sin prueba no se cambia |
| Arquitectura (`DEC-002`, `C1…C8`, esqueleto) | `DEC-nnn` nueva o modificada, validada | Decir qué código existente queda fuera de la regla nueva y cómo se trae |

## Cómo se aplica (sólo lo aprobado)

1. Se aplica **exactamente** lo mostrado; si al aplicarlo aparece algo distinto, se vuelve a preguntar.
2. Se corre lo que verifica ese cambio (el `probar-*.py`, el Doctor en la sonda que corresponda, el hook).
3. Se actualiza la fila del registro a `aplicada`, con el commit o la entrada de `log.md`.
4. Si el cambio es una skill o un script, se avisa en el resumen de cierre: **cambia cómo trabajan los agentes desde ahora.**

## Barreras

- **Nunca se aplica una propuesta sin su "sí" explícito**, ni por lote, ni porque "es obvia", ni porque ya se aprobó una parecida.
- **Nunca se cambia una skill o un script sin la prueba que lo cubra en OK.**
- **Una propuesta no se repite** si ya fue rechazada con motivo; se cita la fila.
- **No se proponen cambios al negocio por esta vía**: una regla de negocio nueva o cambiada sigue el flujo de curaduría (Vigilancia Semántica), no el de mejoras.
- **Lo que es de la aplicación y no del ecosistema tampoco va acá**: un bug y su causa, una trampa del stack, una deuda aceptada son `AP-nnn` o `DT-nnn` en `<modulo>/aplicacion/`. Acá entra sólo lo que cambia cómo trabajan los agentes: reglas, skills, scripts, arquitectura.
- **Se propone de a una.** Diez propuestas juntas son una lista que nadie lee; una por vez es una decisión.
- Todo en español (Argentina).
