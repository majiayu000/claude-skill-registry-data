---
name: registrar-decision
description: Registrar una decisión técnica en docs/DECISIONES.md (y si es grande, investigación en docs/investigacion/); las de producto van a QUESTIONS.md. No para diseñar features (design-feature).
allowed-tools: Read, Write, Edit, Grep, Glob
---

# registrar-decision

Añade una decisión a `docs/DECISIONES.md` (fuente única de decisiones técnicas y versiones). `$ARGUMENTS` (opcional): tema de la decisión.

## Cuándo usarla
- Se cambia o añade algo técnico: capas, módulos (`app/`, `motor/`), esquema Room, dependencias estructurales, formato de datos, motor de enrutado, mapas, TTS, CI.
- Una investigación previa (ROADMAP H0, §8 del prompt) concluye con una recomendación.
- `design-feature` o `architecture-review` detectan una decisión no registrada o contradictoria.

## Cuándo NO usarla
- **Decisiones de producto** (funcionalidad, interfaz, alcance) → no se deciden: van a `QUESTIONS.md` con contexto, opciones y recomendación, y se sigue con lo que no dependa.
- Preferencias del usuario sobre cómo trabajar → usa `recordar`.
- Diseñar una feature completa → usa `design-feature`. Revisar código → usa `architecture-review`.
- Cambios sin impacto (bugfix, refactor local) → no hace falta registro.

## Precondiciones
- Tema claro en `$ARGUMENTS`; si falta, pedirlo y parar.
- Haber leído `docs/DECISIONES.md` entero (las secciones fechadas posteriores mandan sobre las anteriores).
- `docs/DECISIONES.md` es reservado del agente principal; un subagente devuelve el texto propuesto.

## Pasos
1. Buscar duplicados o decisiones afectadas (`Grep` del tema en `docs/DECISIONES.md`, `docs/investigacion/`, `ROADMAP.md`).
2. Decisión pequeña: añadir una línea en la sección del tema: `- AAAA-MM-DD · tema · decisión · porqué`. Si sustituye a otra, indicarlo ("sustituye a § X") en vez de borrar la antigua.
3. Decisión grande (varias alternativas, licencias, impacto en hitos): crear `docs/investigacion/<tema-kebab>.md` desde `docs/_templates/INVESTIGACION.template.md` con Contexto, tabla de Alternativas (mínimo 2, con licencia y versión verificada), Recomendación y Consecuencias; en `docs/DECISIONES.md` añadir la línea resumen con enlace.
4. Lo no verificable se marca `VERIFICAR`; no inventar versiones ni APIs. Fuentes con URL y fecha.
5. Si la decisión afecta al producto (lo que ve o hace el usuario, coste, espacio, privacidad), además: entrada en `QUESTIONS.md` y marcar la decisión como `propuesta` hasta la respuesta.
6. Enlazar desde los docs afectados no reservados y desde el hito de `ROADMAP.md` que la usa (pedirlo al agente principal si es reservado).

## Validaciones / tests
- Cada enlace añadido apunta a un archivo existente: `node scripts/check-docs.mjs`.
- Ningún `<...>` de la plantilla sin rellenar.

## Definition of Done
- [ ] Línea en `docs/DECISIONES.md` con fecha, tema, decisión y porqué.
- [ ] Si es grande: `docs/investigacion/*.md` completo y enlazado.
- [ ] Impacto en producto → entrada en `QUESTIONS.md`.
- [ ] `node scripts/check-docs.mjs` sin errores nuevos.

## Docs a actualizar
- `docs/DECISIONES.md` · `docs/investigacion/` · `ROADMAP.md` · `QUESTIONS.md` si aplica · docs/ESTADO.md (skill `session-handoff`)
