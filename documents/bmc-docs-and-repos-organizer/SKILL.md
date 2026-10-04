---
name: bmc-docs-and-repos-organizer
description: >
  Organiza carpetas y documentación en Calculadora-BMC, detecta huecos o docs
  obsoletos, mantiene índices en docs/ y READMEs, y guía flujos GitHub (ramas,
  PR, etiquetas). Use when the user asks to organize documentation, fix doc
  structure, update READMEs, doc index, repo hygiene, or GitHub workflow for docs.
---

# BMC Docs & Repos Organizer

**Before working:** Read `docs/team/knowledge/DocsOrganizer.md` if it exists. Reference: [`reference.md`](./reference.md).

Mantiene el workspace **legible para humanos y agentes**: rutas predecibles, hubs enlazados, READMEs mínimos útiles y documentación alineada al código y a `AGENTS.md`.

---

## Objetivos

1. **Clasificar** — Cada tipo de conocimiento tiene un “hogar” (team vs google-sheets-module vs bmc-dashboard-modernization vs procedimientos).
2. **Indexar** — Los hubs (`README.md` en `docs/`, `docs/team/`, submódulos) enlazan a los documentos hijos; evitar islas sin enlace ascendente.
3. **Detectar gaps** — Rutas citadas que no existen, duplicados canónico vs copia vieja, docs que contradicen `AGENTS.md` o el inventario de planillas.
4. **GitHub** — Ramas por tema (`docs/...`, `chore/docs-index`), PRs pequeños, descripciones que enlazan a issues o a `PROJECT-STATE` cuando aplica.

---

## Mapa mental del repo (Calculadora-BMC)

| Área | Ruta típica | Qué documenta |
|------|-------------|----------------|
| Equipo / runs | `docs/team/` | Estado, prompts, judge, panelsim, orientación |
| Planillas / Sheets | `docs/google-sheets-module/` | Mapeos, inventario, sync accesos |
| Dashboard UI | `docs/bmc-dashboard-modernization/` | Interface map, propuestas |
| API / operación | `AGENTS.md`, `docs/api/`, `docs/procedimientos/` | Comandos, deploy, checklists |
| Cursor | `.cursor/agents/`, `.cursor/skills/` | Definición de agentes y skills |

---

## Protocolo de corrida (orden sugerido)

### 1. Inventario rápido

- Listar cambios recientes relevantes (git o lo que indique el usuario).
- Identificar **nuevos archivos** en `docs/` o scripts sin mención en ningún README/hub.

### 2. Detección de problemas

- **Enlaces rotos** — Referencias `docs/...` o rutas relativas inexistentes.
- **Doble canónico** — Dos documentos que declaran la misma verdad (elegir uno canónico; el otro: redirección breve o enlace prominente).
- **Obsolescencia** — Términos o comandos que ya no existen en `package.json` / `AGENTS.md`.
- **Secretos** — Nunca documentar tokens; recordar `.env.example` como lugar de nombres de variables, no valores.

### 3. Acciones correctivas (mínimo necesario)

- Añadir o actualizar **README** en la carpeta afectada (3–15 líneas: propósito, enlaces abajo).
- Actualizar **un hub** (p. ej. `docs/team/README.md` o el README del submódulo) con una línea y enlace.
- Si el cambio es grande: proponer **un PR solo de docs** con título claro (`docs: index …`).

### 4. README: checklist por archivo

- **Qué es** esta carpeta.
- **Enlaces** a los 1–3 documentos más importantes.
- **Dueño o convención** (opcional): “canónico vs histórico”.
- No duplicar `AGENTS.md` entero; enlazarlo.

### 5. GitHub (cuando toque código + docs)

- Rama descriptiva; PR con descripción en oraciones completas; si el repo usa plantillas de PR, respetarlas.
- Si hay CI: cambios solo en Markdown suelen no requerir build; si se tocó `src/`, recordar `npm run lint` / gates según `AGENTS.md`.

---

## Integración con “Full team run” (plan 0→9)

- Tras pasos con muchos artefactos (**5 Reporter**, **5f Audit**, **7 Repo Sync**, **8 PROJECT-STATE**), este skill puede ejecutarse como **paso opcional** para:
  - enlazar nuevos reportes desde un índice en `docs/team/reports/` o README de team;
  - asegurar que `MATPROMT` / `PROMPT-FOR-EQUIPO-COMPLETO` referencien rutas reales.

No sustituye el **paso 8** (Orchestrator sigue siendo quien actualiza `PROJECT-STATE` con la política del repo).

---

## Handoff

- **To Repo Sync** — Si existen paths `BMC_DASHBOARD_2_REPO` / `BMC_DEVELOPMENT_TEAM_REPO`, listar qué docs deben copiarse o alinearse en el repo hermano.
- **To Orchestrator** — Lista corta de “pendientes documentales” para `PROJECT-STATE` (sin editar hasta confirmación del usuario si la política lo exige).
- **To Mapping / Contract** — Si el gap es de verdad de negocio (columnas, API), no inventar: escalar con ruta al documento canónico.

---

## Referencias

- `AGENTS.md`
- `docs/team/PROJECT-TEAM-FULL-COVERAGE.md`
- `docs/team/INVOQUE-FULL-TEAM.md`
- `.cursor/agents/bmc-dashboard-team-orchestrator.md`
- `.cursor/agents/bmc-repo-sync-agent.md`
