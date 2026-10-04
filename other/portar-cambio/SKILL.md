---
name: portar-cambio
description: Porta el cambio de la rama actual a las variantes hermanas de esta plantilla (es/en × con-IA/sin-IA) — traduce el contenido, adapta o elimina la capa de IA según el destino y deja cada variante con una rama lista para PR. Úsalo cuando un cambio del template deba replicarse en las otras variantes (p. ej. "porta este cambio al template en inglés", "replica esto en las variantes").
---

<!-- Skill EXCLUSIVA DEL REPO-PLANTILLA: sirve para mantener la familia de variantes.
     /instanciar la elimina en los proyectos instanciados. -->

Replica el cambio de la rama actual en las variantes hermanas de la familia:

- 🇪🇸 con IA: `project-starter-template-es-ai` · 🇬🇧 con IA: `project-starter-template-en-ai`
- 🇪🇸 sin IA: `project-starter-template-es` · 🇬🇧 sin IA: `project-starter-template-en`

## Paso 1 — Delimitar el cambio

Toma el diff de la rama actual contra `main` (`git diff main...HEAD`) y clasifica cada
archivo: ¿documentación general, capa de IA (`.claude/`, `AGENTS.md`, `CLAUDE.md`,
`specs/`), o tooling neutro (`.github/`, scripts)?

## Paso 2 — Elegir destinos

Pregunta a qué variantes portar y dónde están sus copias locales (o clónalas). Reglas
por destino:

- **Mismo idioma, sin IA**: elimina del port todo lo que dependa de la capa de IA
  (skills, hooks de `.claude/`, menciones a agentes). Si existe un equivalente nativo
  (p. ej. `.githooks/`), adapta ahí.
- **Otro idioma**: traduce contenido y nombres siguiendo el mapa de renombres de
  `.github/scripts/check-parity.sh` (p. ej. `instanciar` ↔ `instantiate`,
  `portar-cambio` ↔ `port-change`, `actualizar-plantilla` ↔ `update-template`).
  Los placeholders también se traducen (`[NOMBRE_DEL_PROYECTO]` ↔ `[PROJECT_NAME]`):
  respeta el catálogo del TEMPLATE-USAGE de destino.

## Paso 3 — Aplicar en cada destino

En cada variante: crea una rama con el mismo nombre que la de origen, aplica el cambio
adaptado y ejecuta sus verificaciones (`.github/scripts/check-links.sh`,
`check-placeholders.sh`, tests si existen).

**Atribución**: en las variantes **con IA**, los commits llevan el trailer de coautoría
de `docs/conventions/ai-agents.md`; en las variantes **sin IA**, los commits NO llevan
ninguna atribución ni mención de IA (ni en el mensaje ni en el contenido portado).

## Paso 4 — Cierre

Resume por variante: rama creada, archivos portados, qué se adaptó u omitió y por qué.
Recuerda abrir los PRs (skill `/open-pr` en las variantes con IA).

Ejemplo: rama `feat/nuevo-hook` aquí → `/portar-cambio` → ramas `feat/nuevo-hook` en
las otras 3 variantes, traducidas y sin capa de IA donde no aplica.

NO hagas push ni abras PRs sin confirmación, NO portes a ciegas archivos de la capa de
IA a las variantes sin IA, y NO dejes las variantes a medias: si un destino falla,
repórtalo explícitamente.
