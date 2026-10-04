---
name: open-issue
description: Redacta y crea un issue de GitHub rellenando la plantilla adecuada de .github/ISSUE_TEMPLATE/ según el tipo (bug, funcionalidad o tarea). Úsalo cuando la persona pida abrir/crear un issue, reportar un bug o registrar una tarea/petición (p. ej. "abre un issue por este bug", "crea un issue para la nueva funcionalidad", "registra esta tarea"). No cierra ni comenta issues existentes.
argument-hint: "[título o descripción breve]"
---

Crea un issue bien formado usando la plantilla del repositorio.

1. Mira las plantillas disponibles en `.github/ISSUE_TEMPLATE/` y elige la que corresponda
   al tipo de issue:
   - `bug_report.md` — un fallo o comportamiento incorrecto.
   - `feature_request.md` — una nueva funcionalidad o mejora.
   - `task.md` — una tarea de trabajo interna (chore, refactor, tooling).
     Si el tipo es ambiguo por lo que dice `$ARGUMENTS`, pregunta antes de elegir.
2. Lee la plantilla elegida para conocer sus secciones requeridas y su encabezado
   (`title:`, `labels:`, `assignees:`). Respeta ese frontmatter.
3. Rellena cada sección con la información de `$ARGUMENTS` y del contexto de la
   conversación:
   - Un título claro y en imperativo o descriptivo (no genérico como "bug").
   - Pasos de reproducción / comportamiento esperado vs. actual para bugs.
   - Motivación y criterios de aceptación para funcionalidades y tareas.
   - Deja como indicación (no inventes) cualquier dato que no tengas: versiones, entorno,
     capturas.
4. Crea el issue con la CLI `gh` respetando la plantilla, p. ej.
   `gh issue create --title "…" --body "…" --label "…"` (o `--template <archivo>` si se
   prefiere el flujo interactivo). Si no hay remoto configurado, muestra el issue relleno
   para que la persona lo pegue en GitHub.
5. Informa la URL del issue creado (o el cuerpo redactado).

Ejemplo: `/open-issue el login falla con Google en Safari` →
`.github/ISSUE_TEMPLATE/bug_report.md` relleno y publicado.

NO inventes datos que no tengas (versiones, logs, entorno) — déjalos como indicaciones,
NO crees un issue duplicado si ya existe uno igual (búscalo primero con `gh issue list`),
y NO cierres, edites ni comentes issues existentes.
