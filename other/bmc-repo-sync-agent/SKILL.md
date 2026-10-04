---
name: bmc-repo-sync-agent
description: >
  Mantiene actualizados dos repositorios: bmc-dashboard-2.0 (desarrollo y
  funcionamiento del dashboard) y bmc-development-team (equipo y artefactos).
  Tras cada corrida del equipo, evalúa qué debe actualizarse y sincroniza.
  Use when syncing repos after team run, updating bmc-dashboard-2.0, or
  maintaining bmc-development-team.
---

# BMC Repo Sync Agent

**Before working:** Read `docs/team/knowledge/RepoSync.md` if it exists.

Mantiene actualizados dos repositorios externos tras cada corrida del equipo BMC. Evalúa qué artefactos cambiaron y sincroniza con cada repo según su destino.

---

## Repos bajo mantenimiento

| Repo | Contenido | Qué se actualiza |
|------|-----------|------------------|
| **bmc-dashboard-2.0** | Desarrollo y funcionamiento del dashboard | Código dashboard (app.js, styles, index.html), rutas API (bmcDashboard.js), docs de dashboard, DASHBOARD-INTERFACE-MAP, planilla-inventory, config de Sheets, scripts de deploy |
| **bmc-development-team** | Equipo y artefactos | PROJECT-STATE, PROJECT-TEAM-FULL-COVERAGE, JUDGE-CRITERIA-POR-AGENTE, JUDGE-REPORT-HISTORICO, reportes Solution/Coding, handoffs, skills/agents actualizados |

---

## Cuándo usar

- Tras cada "Full team run" o "Run the BMC Dashboard team"
- Cuando el usuario dice: "sync repos", "actualizar bmc-dashboard-2.0", "mantener repos al día"
- Cuando hay cambios en dashboard o equipo que deben propagarse a los repos

---

## Protocolo (tras cada corrida)

1. **Evaluar** — Revisar qué artefactos cambiaron en esta corrida:
   - Dashboard: `docs/bmc-dashboard-modernization/`, `server/routes/bmcDashboard.js`, `docs/google-sheets-module/`, dashboard UI
   - Equipo: `docs/team/`, `.cursor/agents/`, `.cursor/skills/`, reportes

2. **bmc-dashboard-2.0** — Actualizar con:
   - Código del dashboard (frontend + backend)
   - Docs de mapa, planilla, API
   - Config y scripts relevantes

3. **bmc-development-team** — Actualizar con:
   - PROJECT-STATE, PROJECT-TEAM-FULL-COVERAGE
   - Criterios Judge, reportes históricos
   - Skills/agents actualizados
   - Reportes y handoffs

4. **Commit** — En cada repo: commit con mensaje descriptivo del run o cambio; push si aplica.

---

## Rutas y configuración

Las rutas de los repos se configuran en `PROJECT-STATE.md` (sección Estado por área) o en `.env`:

- `BMC_DASHBOARD_2_REPO` — path local o URL del repo bmc-dashboard-2.0
- `BMC_DEVELOPMENT_TEAM_REPO` — path local o URL del repo bmc-development-team

Si no están definidas, el agente reporta qué actualizaría y qué falta configurar. Ejemplo en PROJECT-STATE:

```markdown
### Repos (Repo Sync)
- bmc-dashboard-2.0: /path/to/bmc-dashboard-2.0
- bmc-development-team: /path/to/bmc-development-team
```

---

## Handoff

- **From:** Reporter, Orchestrator (al final del run)
- **To:** Repos (bmc-dashboard-2.0, bmc-development-team)
- **Artifacts:** Cambios en dashboard, equipo, reportes

---

## Referencias

- `docs/team/PROJECT-STATE.md` — estado actual, pendientes
- `docs/team/PROJECT-TEAM-FULL-COVERAGE.md` — equipo y propagación
- `docs/bmc-dashboard-modernization/` — artefactos del dashboard
