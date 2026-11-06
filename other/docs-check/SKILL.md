---
name: docs-check
description: Revisar docs/** y los .md de la raíz (links = enlaces/anclas rotos | consistency = datos vs DECISIONES.md, VERIFICAR); solo informa, no edita (docs-update).
argument-hint: "[links|consistency]"
allowed-tools: Read, Grep, Glob, Bash(node scripts/*)
---

# docs-check

Revisa la documentación según `$ARGUMENTS` (por defecto `links`). No modifica archivos: devuelve findings `SEVERIDAD | archivo:línea | problema | corrección propuesta`.

## Cuándo usarla
- Tras editar docs, mover archivos o antes de cerrar un hito.
- Para detectar versiones o datos que contradicen `docs/DECISIONES.md`.

## Cuándo NO usarla
- Reescribir o completar contenido → usa `docs-update`.
- Validar skills y agentes → `node scripts/check-claude-assets.mjs`.

## Precondiciones
- `$ARGUMENTS` es `links` o `consistency`; si falta, usar `links`; si es otro valor, parar y pedirlo.
- Ámbito: `docs/**`, `CLAUDE.md`, `ROADMAP.md`, `QUESTIONS.md` y `README.md` si existe.

## Pasos
### links
1. Ejecutar `node scripts/check-docs.mjs` y usar su salida como base.
2. Complemento: Glob de `docs/**/*.md` + los `.md` de la raíz; Grep de enlaces `\]\(([^)#]+)(#[^)]*)?\)` y de rutas en backticks (`docs/...`, `.claude/...`, `scripts/...`).
3. Para cada enlace relativo, resolver contra la carpeta del archivo y comprobar con Glob que el destino existe (ignorar `http(s)://` y `mailto:`).
4. Para cada ancla `#x`, comprobar que el destino tiene un encabezado con ese slug.
5. Informar: destino inexistente = ALTA; ancla rota = MEDIA; ruta en backticks inexistente = BAJA (puede ser un doc futuro; indicar el hito si consta).

### consistency
1. Extraer de `docs/DECISIONES.md` las versiones fijadas y decisiones cerradas; no copiarlas al informe, citar la sección.
2. Grep en `docs/**`, `CLAUDE.md` y `ROADMAP.md` de esas entidades (librerías, Kotlin, AGP, JDK, SDK mínimo/objetivo, fuentes de datos) y comparar valores.
3. Contrastar las dudas de `QUESTIONS.md` marcadas como respondidas con lo que dicen `ROADMAP.md` y `docs/DECISIONES.md`.
4. Informar discrepancias: contradice DECISIONES.md = ALTA; dato sin fuente = MEDIA.
5. Grep de `VERIFICAR` y `TODO` en `docs/**`: listar cada marca con archivo:línea y si tiene hito o registro en `docs/ESTADO.md`; sin dueño = MEDIA.
6. Comprobar que los `Actualizado:` de las cabeceras no son anteriores al último cambio (`git log -1 --format=%cs -- <archivo>`); desfase = BAJA.

## Validaciones / tests
- `links`: 0 destinos inexistentes en el ámbito.
- `consistency`: 0 discrepancias ALTA y todas las marcas `VERIFICAR` con dueño.
- Cada finding incluye archivo:línea reproducible con Grep.

## Definition of Done
- [ ] Ámbito completo revisado (todos los `.md` de `docs/**` y de la raíz).
- [ ] Informe en formato `SEVERIDAD | archivo:línea | problema | corrección propuesta`, ordenado.
- [ ] Ningún archivo modificado.
- [ ] Correcciones derivadas encargadas con `docs-update` (reservados: petición al agente principal).

## Docs a actualizar
- Ninguno (solo informa) · si se corrige algo, docs/ESTADO.md (skill `session-handoff`)
