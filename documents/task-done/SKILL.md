---
name: TASK-DONE
description: >
  Marca una feature de docs/features/ como terminada: actualiza sus checkboxes,
  la mueve a docs/done/, agrega/actualiza su fila en docs/logros.md y agrega
  una entrada en docs/changelog-interno.md (técnico) y docs/changelog.md
  (para compartir con el cliente/usuarios externos). Usar cuando el usuario dice
  "marcar feature como done", "actualizar estado de features", "cerrar feature",
  "feature terminado", o pide reflejar que un trabajo ya quedó completo en la
  documentación del proyecto.
---

# TASK-DONE

## Propósito

Cuando una feature de `docs/features/*.md` queda completa (o se retoma/ajusta
después de estar en `docs/done/`), este skill deja consistentes los 4 lugares
donde el proyecto trackea trabajo terminado:

1. El doc de la feature (checkboxes + estado)
2. `docs/logros.md` (tabla para el cliente, no técnico, con impacto/pago)
3. `docs/changelog-interno.md` (historial técnico, uso interno — NO compartir con el cliente)
4. `docs/changelog.md` (novedades en lenguaje simple, SÍ se puede compartir con el cliente/usuarios externos)

No commitear ni hacer push — solo dejar los archivos editados, como el resto
del flujo de este proyecto.

## Si `docs/` o alguno de estos archivos no existe

Crearlos. No asumir que ya existen ni preguntar — si falta la carpeta `docs/`,
crearla; si falta `docs/logros.md`, `docs/changelog-interno.md` o
`docs/changelog.md`, crearlos con un header mínimo (título + una línea de
propósito, igual que los existentes) antes de agregar la entrada nueva.

## Proceso

### 1. Doc de la feature (`docs/features/<nombre>.md` o `docs/done/<nombre>.md`)
- Marcar todos los ítems de `## Todo list` con `[x]`
- Actualizar `## Estado` con una línea corta: qué quedó activo, fecha (formato `YYYY-MM-DD`, usar la fecha actual del sistema)
- Si el archivo vive en `docs/features/`, moverlo a `docs/done/` con `git mv`
- Si ya vive en `docs/done/` (se está reactivando o cerrando un ajuste posterior), no moverlo de nuevo — solo actualizar `## Estado`

### 2. `docs/logros.md`
- Buscar si ya existe una fila para esta feature (por nombre)
  - Si existe: actualizar `Fecha fin` a la fecha de hoy
  - Si no existe: agregar una fila nueva al final de la tabla
- Redactar la columna **Descripción** en lenguaje simple, sin jerga técnica — el cliente no es técnico
- Elegir **Impacto** (Bajo/Medio/Alto) según complejidad real: cuántos archivos, si tocó backend/DB, si es una feature nueva vs. un ajuste
- **Pago**: dejar como está si la fila ya existía (no asumir que se cobró); si es fila nueva, usar `Todavía`

### 3. `docs/changelog-interno.md` (técnico, interno)
- Agregar una entrada nueva **al inicio** del archivo (después del header, antes de la entrada más reciente existente)
- Formato: `## YYYY-MM-DD — Título corto`
- Contenido técnico: qué se tocó, decisiones de diseño, gotchas encontrados (ej. bugs de contraste, APIs deprecadas, workarounds) — este archivo sí lleva detalle técnico

### 4. `docs/changelog.md` (externo, compartible)
- Agregar una entrada nueva **al inicio** del archivo (mismo formato `## YYYY-MM-DD — Título corto`)
- Redactar en lenguaje 100% no técnico, orientado a "qué puede hacer ahora el usuario" — nada de nombres de archivos, librerías, decisiones internas ni bugs
- Esta entrada normalmente es una versión resumida de la fila que se agregó en `docs/logros.md`

## Ejemplo de una pasada completa

Ver `docs/done/feat-share-routine.md` (Estado + Todo list), la fila "Compartir y
guardar rutinas" en `docs/logros.md`, la entrada `2026-07-11` en
`docs/changelog-interno.md`, y la entrada equivalente en `docs/changelog.md`
— esa secuencia es el resultado esperado de una corrida de este skill.

## Boundaries

- No inventar fechas de inicio para features viejas si no hay commit/dato real — buscar en `git log` primero
- No marcar `Pago` como `Pagado` sin que el usuario lo confirme explícitamente
- No borrar contenido existente en ninguno de los 4 archivos — solo agregar/actualizar
- Nunca poner detalle técnico (nombres de archivo, librerías, bugs internos) en `docs/changelog.md` — eso es exclusivo de `docs/changelog-interno.md`
- Si la feature tiene cambios de código pendientes de verificar (sin probar en navegador), decirlo en `## Estado` en vez de afirmar que está 100% validado
