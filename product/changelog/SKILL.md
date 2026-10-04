---
name: changelog
description: Actualiza CHANGELOG.md en el formato Keep a Changelog, añadiendo los cambios actuales bajo la sección Unreleased. Úsalo cuando la persona pida actualizar el changelog, añadir una entrada al changelog o registrar lo que cambió para las notas de la versión (p. ej. "añade esto al changelog", "actualiza el CHANGELOG con estos commits").
---

Añade los cambios actuales a `CHANGELOG.md`.

1. Lee `CHANGELOG.md` para coincidir con su estilo existente y confirma que sigue Keep a Changelog (https://keepachangelog.com). Asegúrate de que exista una sección `## [Unreleased]` al inicio; créala si falta.
2. Determina qué cambió desde la última versión: revisa los commits recientes (`git log <last-tag>..HEAD --oneline`) y/o el diff del working tree.
3. Resume los cambios en las categorías estándar bajo Unreleased, creando solo las subsecciones que apliquen:
   - `Added` — nuevas funcionalidades.
   - `Changed` — cambios en el comportamiento existente.
   - `Deprecated` — funcionalidades que pronto se eliminarán.
   - `Removed` — funcionalidades eliminadas.
   - `Fixed` — correcciones de errores.
   - `Security` — correcciones de vulnerabilidades.
4. Escribe las entradas como viñetas concisas y orientadas a la persona usuaria (qué cambió y por qué importa), no mensajes de commit en crudo. Vincula issues/PRs si el archivo lo hace.
5. Si el cambio implementa una spec, marca también el ítem que su `proposal.md` declara en el campo _Ítem de roadmap_ dentro de `docs/product/roadmap.md` — CHANGELOG y roadmap viajan en el mismo PR (`docs/conventions/workflow.md`, reglas 5 y 6).
6. Informa las líneas que añadiste.

Ejemplo: bajo `### Fixed` → `- Prevent crash when saving an empty form (#142).`

NO publiques una versión con número (no muevas Unreleased a una versión con fecha) a menos que la persona lo pida explícitamente. NO incrementes números de versión por tu cuenta.
