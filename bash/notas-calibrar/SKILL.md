---
name: notas-calibrar
description: Calibrar umbrales del motor de notas (TablaGrados, DetectorCurvas, UmbralesRasantes) sobre trazas reales de Mallorca y revisar los goldens; no cambia frases (test-write) ni voz (H4).
argument-hint: "[traza.gpx]"
allowed-tools: Read, Grep, Glob, Edit, Bash(./gradlew :motor:test*), Bash(git diff*), Bash(git status*), Bash(node scripts/gen-claude-index.mjs*), Bash(rm motor/src/test/resources/notas/*.txt)
disable-model-invocation: true
---

# notas-calibrar

Ajusta los parámetros del motor de notas en `motor/src/main/kotlin/app/trombito/rallycopilot/motor/notas/` y mide el efecto sobre trazas reales. Traza: `$0` (si falta, elegir de `docs/rutas/*.gpx`).

## Cuándo usarla
- Las notas salen con grados, horquillas, «y» o avisos que no cuadran con la carretera real (p. ej. demasiadas horquillas o curvas de grado 6 mal clasificadas).
- Hay que mover un umbral (`TablaGrados.mu`, `umbralesKmh`, `radioHorquillaM`; `DetectorCurvas.radioEntradaM`/`radioSalidaM`; `UmbralesRasantes`) y comprobar su efecto.
- Llega una calibración de velocidad de Joan (perfil global o por tramo, según ROADMAP H3/H6).

## Cuándo NO usarla
- Cambiar el texto de las frases (`FrasesNota`) → usa `test-write` (tipo `motor`).
- Voz, TTS o clips de audio → H4, no esta skill.
- Solo reproducir una traza en el emulador → usa `gps-replay`.
- Decidir si una nota «suena bien» al copiloto sin datos → va a `QUESTIONS.md`, no se fija aquí.

## Precondiciones
- Leer `docs/ESTADO.md` y el hito H3 de `ROADMAP.md`.
- Traza en `docs/rutas/` (GPX con `trkpt`). Si no existe, ver Paso 1.
- Estado limpio en `motor/` antes de empezar (`git status`); el cambio se hace en un solo parámetro cada vez.

## Pasos
1. Traza: si `$0` existe en `docs/rutas/`, usarla. Si no, mirar `docs/rutas/README.md`. Para crear una traza nueva: `python -I scripts/traza-desde-vias.py <vias-mallorca.tsv.gz> <ref> <lat,lon ini> <lat,lon fin> docs/rutas/<nombre>.gpx` (el `.tsv.gz` se baja de la última release de `rally-copilot-data` con `gh release download`), y añadir su fila y atribución OSM a `docs/rutas/README.md`.
2. Leer la salida base: `./gradlew :motor:test --tests "*RealTest*"` y anotar nº de notas, reparto por grado, encadenadas, grado 6 y modificadores (líneas `println` de `GeneradorNotasRealTest`, en `motor/build/test-results/test/*.xml`).
3. Cambiar **un** parámetro en `motor/src/main/kotlin/.../notas/` con `Edit` (valor por defecto del constructor). Anotar valor anterior y nuevo.
4. Regenerar goldens a propósito: borrar el golden afectado (`ma-2141.txt`, `ma-2141-hoja.txt`, `ma-10-hoja.txt` en `motor/src/test/resources/notas/`) y ejecutar `./gradlew :motor:test --tests "*RealTest*"`. El test escribe el archivo y falla una vez: es lo esperado.
5. Comparar: `git diff -- motor/src/test/resources/notas/` y repetir el paso 2. Revisar nº de notas por grado, modificadores, «y» y avisos. Cada cambio debe poder explicarse con un tramo concreto (km o índice de la traza).
6. Si el cambio mejora un caso y empeora otro, no cerrar: volver al paso 3 o dejarlo como duda en `QUESTIONS.md`.
7. Revisión: pedir `copiloto-reviewer` (modelo `opus`, vía `delegate-task`) con el diff de goldens y los números de los pasos 2 y 5. Sin modificar archivos; findings citando nota o km.
8. Registrar con `registrar-decision` (tema «Calibración de notas (H3)»): valor anterior, nuevo, traza y porqué. Si un subagente lo ejecuta, devuelve la línea propuesta; `docs/DECISIONES.md` la escribe el agente principal.

## Validaciones / tests
- `./gradlew :motor:test --tests "*RealTest*"` en verde tras regenerar goldens (segunda pasada).
- `./gradlew :motor:test` completo sin fallos nuevos.
- `node scripts/check-claude-assets.mjs && node scripts/gen-claude-index.mjs --check`

## Definition of Done
- [ ] Un parámetro cambiado, con valor anterior y nuevo anotados.
- [ ] Goldens regenerados y revisados con `git diff`, con nº de notas por grado antes y después.
- [ ] Revisión de `copiloto-reviewer` sin BLOCKER pendiente.
- [ ] Decisión registrada (`registrar-decision`) o marcada como duda en `QUESTIONS.md`.
- [ ] `./gradlew :motor:test` en verde.

## Docs a actualizar
- `docs/DECISIONES.md` § Motor de notas (H3) (vía `registrar-decision`, agente principal) · `docs/rutas/README.md` si se añade traza · `docs/ESTADO.md` (skill `session-handoff`)
