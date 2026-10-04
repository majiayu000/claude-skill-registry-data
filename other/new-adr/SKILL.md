---
name: new-adr
description: Genera un nuevo Registro de Decisión de Arquitectura (ADR) copiando la plantilla de ADR en el siguiente archivo numerado y registrándolo en el índice de decisiones. Úsalo cuando la persona quiera registrar una decisión de arquitectura, crear/añadir un ADR o documentar una elección técnica (p. ej. "escribe un ADR para cambiar la base de datos", "añade un registro de decisión").
argument-hint: "[título breve]"
---

Crea un nuevo ADR para la decisión cuyo título está en `$ARGUMENTS`.

1. Lee `docs/decisions/README.md` para conocer el esquema de numeración, la convención de nombres de archivo y cómo se mantiene el índice. Sigue ese documento si difiere de los pasos siguientes.
2. Encuentra el `NNNN-*.md` existente con el número más alto en `docs/decisions/` y calcula el siguiente número con relleno de ceros (p. ej. `0007`).
3. Copia `docs/decisions/0000-template.md` a `docs/decisions/<NNNN>-<kebab-title>.md`, donde `<kebab-title>` es el `$ARGUMENTS` convertido a slug (minúsculas, separado por guiones).
4. En el nuevo archivo, completa:
   - Título (la forma legible de `$ARGUMENTS`)
   - Estado: `Proposed`
   - Fecha: la fecha de hoy (`YYYY-MM-DD`)
   - Deja Context / Decision / Consequences como indicaciones guiadas para que la persona autora las complete.
5. Añade un enlace al nuevo ADR en el índice dentro de `docs/decisions/README.md`, en orden numérico.
6. Informa la ruta del archivo creado y recuerda a la persona autora completar Context, Decision y Consequences.

Ejemplo: `/new-adr usar renderizado del lado del servidor` → `docs/decisions/0007-use-server-side-rendering.md`.

NO marques el ADR como `Accepted` por tu cuenta, NO edites ni reemplaces ADRs existentes, y NO inventes contenido para secciones que debe decidir la persona autora.
