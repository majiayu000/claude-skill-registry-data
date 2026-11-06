---
name: recordar
description: Guardar en docs/MEMORIA.md lo que el usuario pide que se recuerde entre sesiones («a partir de ahora», «siempre», «nunca», correcciones generales); no para decisiones técnicas (registrar-decision).
argument-hint: "[lo que hay que recordar]"
allowed-tools: Read, Edit, Write, Grep, Bash(git add docs/MEMORIA.md), Bash(git commit *), Bash(git status*), Bash(git diff*)
---

# recordar

Mantiene `docs/MEMORIA.md`, la memoria del proyecto entre sesiones. CLAUDE.md la importa (`@docs/MEMORIA.md`), así que todo lo que contiene se carga en cada sesión. `$ARGUMENTS`: lo que hay que recordar (si falta, tomarlo del último mensaje del usuario).

## Cuándo usarla
- El usuario dice «a partir de ahora», «recuerda», «siempre», «nunca», «no vuelvas a…» o «prefiero…».
- El usuario corrige una forma de trabajar de manera general (no un error puntual), o confirma un enfoque no obvio que conviene repetir.
- `session-handoff` detecta una preferencia expresada en la sesión que aún no está guardada.

## Cuándo NO usarla
- Decisiones técnicas con alternativas → usa `registrar-decision` (`docs/DECISIONES.md`).
- Dudas de producto pendientes → `QUESTIONS.md`. Respuestas del usuario a esas dudas → se reflejan en `QUESTIONS.md` (respondida) y en `ROADMAP.md`/`DECISIONES.md`; aquí solo si establecen una regla general.
- Estado de la sesión o próxima acción → `session-handoff` (`docs/ESTADO.md`).
- Lo que ya dice el código, git o CLAUDE.md: no se duplica.

## Precondiciones
- Leer `docs/MEMORIA.md` entero antes de editar.
- Es archivo reservado del agente principal: un subagente devuelve el texto propuesto.

## Pasos
1. Reformular la petición como regla accionable y breve, en español, sin ambigüedad. Si la intención no está clara, preguntar antes de guardar.
2. Elegir sección: **Preferencias de trabajo** (proceso, git, delegación, comunicación) · **Producto** (criterios generales del producto que no son una duda concreta) · **Estilo/UI** · **Correcciones** (algo que se hizo mal y no debe repetirse).
3. Buscar duplicados o contradicciones (`Grep` de palabras clave en `docs/MEMORIA.md`):
   - Si ya existe igual: no añadir; como mucho actualizar la fecha.
   - Si contradice una entrada: **manda la más reciente**. Reescribir o borrar la antigua (no dejar dos reglas opuestas).
4. Escribir la línea: `- AAAA-MM-DD · ámbito · lo que pidió el usuario · porqué/cómo aplicarlo`. El porqué permite juzgar casos límite; si el usuario no lo dio, inferirlo con prudencia o dejar «—».
5. Si la regla vale también para los otros proyectos del usuario (Sous Chef, Trombito), guardarla además en la memoria personal de Claude Code (directorio de memoria del usuario, un archivo por hecho e índice en `MEMORY.md`), sin duplicar lo específico de Rally Copilot.
6. Si la regla cambia cómo se aplica algo ya escrito (CLAUDE.md, una skill), proponer ese cambio al agente principal; MEMORIA.md no sustituye a corregir la fuente.
7. Commit: `git add docs/MEMORIA.md` y `git commit -m "docs(memoria): <resumen de la regla>"` (sin coautoría; sin push).
8. Confirmar al usuario en una línea qué se ha guardado.

## Validaciones / tests
- `docs/MEMORIA.md` sigue con sus cuatro secciones y cada línea con el formato de 4 campos.
- Ninguna pareja de entradas contradictorias (`Grep` del tema).
- Sin secretos, datos personales sensibles ni valores de entorno.

## Definition of Done
- [ ] Regla guardada una sola vez, en la sección correcta, con fecha y porqué.
- [ ] Contradicciones resueltas a favor de la más reciente.
- [ ] Copia en la memoria personal si es transversal a los proyectos.
- [ ] Commit `docs(memoria): …` hecho; usuario informado.

## Docs a actualizar
- `docs/MEMORIA.md` · memoria personal de Claude Code si aplica · CLAUDE.md o la skill afectada (vía agente principal) si la regla los contradice
