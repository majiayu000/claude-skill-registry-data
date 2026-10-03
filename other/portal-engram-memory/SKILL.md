---
name: portal-engram-memory
description: Use Engram (Gentleman-Programming/engram) as DEV-TIME persistent memory for Claude Code on the Portal Centralizado de Datos Financieros project. Local-only Go binary + SQLite + FTS5, cloud opt-in and disabled here. Use to persist team decisions, rubric absorptions, agreed degradations and fulfilled gates across coding sessions. Never store secrets, JWTs, credentials or production data. No integration with the runtime ADK agent.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal Engram Memory Skill (dev tooling)

Adaptación del skill homónimo de AgroSat. Engram es una herramienta de **productividad de desarrollo** que persiste memoria entre sesiones de Claude Code. **NO** forma parte del runtime del producto.

## Scope and Hard Boundary

| Capa | Almacén de memoria | Owner |
|------|--------------------|-------|
| Agente runtime (`/api/chat` SSE, ADK) | `SessionService` de ADK + PostgreSQL | `portal-adk-agent` |
| Retrieval del catálogo | pgvector + búsqueda híbrida | `portal-catalog-rag` |
| **Memoria dev-time del IDE** | **Engram (SQLite local, FTS5)** | **este skill** |

Engram **MUST NOT** conectarse a routers FastAPI, tools ADK ni ningún código de producción. Si surge necesidad de memoria de producto entre sesiones, va por Postgres+pgvector, nunca por Engram.

## Rules — NON-NEGOTIABLE

- **Instalación local únicamente.** Binario Go único (`engram.exe` en Windows). DB en `%USERPROFILE%\.engram\engram.db` (override `ENGRAM_DATA_DIR`), fuera del repo y git-ignored.
- **Cloud OFF.** No enrolar el proyecto en Engram Cloud (`engram cloud enroll`) sin acuerdo de los 3 integrantes. Sync entre laptops solo vía `engram sync` (chunks por git), tras revisión.
- **Scoping por proyecto.** Confirmar al inicio de sesión con `mem_current_project` que el contexto es el proyecto del portal (cwd `proyecto_ui`).
- **Nunca persistir**: valores de `.env.local` / Secret Manager, `JWT_SECRET_KEY`, `GEMINI_API_KEY`, tokens Bearer, contraseñas o hashes, prompts crudos de usuarios, emails reales de participantes de la investigación UX (las entrevistas son datos de campo, no memoria de dev).
- Registrar plugin vía marketplace de Claude Code (namespace `mcp__plugin_engram_engram__*`); no duplicar con entrada manual `mcpServers`.
- Operaciones destructivas (`mem_delete`, `mem_merge_projects`) fuera del allowlist: requieren aprobación explícita por llamada.

## Herramientas MCP que usamos

| Momento | Tool | Uso en este proyecto |
|---------|------|----------------------|
| Inicio de sesión | `mem_current_project`, `mem_context`, `mem_search` | Confirmar proyecto y recuperar decisiones previas relevantes a la tarea |
| Durante la sesión | `mem_save` | Guardar decisiones, gotchas y acuerdos EN CUANTO ocurren (no esperar a que lo pidan) |
| Cierre de sesión | `mem_session_summary` | Resumen obligatorio antes de dar la sesión por terminada |

## Qué persistir (y qué no)

### SAVE — conocimiento interno que decae lento

- **Decisiones de equipo** y su porqué: elección de nombre comercial, roles confirmados en kickoff, horario de sync acordado.
- **Absorción de rúbricas** (protocolo §25.2): fecha de publicación de la rúbrica A2–A5, tabla criterio→peso resultante, historias UX ajustadas y SP recalculados.
- **Degradaciones acordadas**: STRETCH congelados (orden E5→E4→E2), degradación del dashboard a 500K puntos, recortes acordados del CRUD de usuarios activados por el déficit −11 SP.
- **Gates cumplidos** (§20 del plan): qué gate de semanas 1–2 se cerró, con qué evidencia y fecha.
- Gotchas entre laptops ("dbmate falla si DATABASE_URL lleva sslmode en local", etc.).
- Punteros a docs canónicos ("rúbrica A1 en docs/general/semana_1/rubrica_tarea_1_UI.pdf").

### DO NOT SAVE — sensible / volátil / ya versionado

- Nada de `.env*`, Secret Manager, tokens ni credenciales.
- Datos de participantes de encuesta/entrevistas (citas con nombre real, contactos).
- Lo que ya está en código o git (la memoria guarda el **porqué**, no el **qué**).
- Estado semanal del sprint board (eso vive en el plan y el tracker, cambia cada semana).

## Patrón `mem_save`

```json
{
  "title": "Rubrica A2 absorbida: journey maps exigen blueprint de servicio",
  "type": "decision",
  "what": "A2 rubric published 27-jul; criterion 'service blueprint' (10%) mapped to the journey-maps story, SP raised 5 -> 6.",
  "why": "Protocol 25.2 T+1h step; delta covered by freezing E5 STRETCH (FinOps dashboards).",
  "where": "context/planeacion_proyecto.md section 11 + registro de cambios",
  "learned": "Canvas publishes rubrics without notification; check Mondays 9:00."
}
```

## Sync de equipo (manual, opt-in)

```bash
engram sync                    # exporta chunks a .engram/ local
# revisar y redactar antes de compartir; solo chunks bajo docs/engram/
git add docs/engram/ && git commit -m "chore(engram): sync shareable memories"
engram sync --import           # en otra laptop, tras pull
```

Solo se commitean chunks bajo `docs/engram/` tras revisión de un compañero (sin secretos, sin PII, sin datos de participantes). `.engram/` y `*.engram.db*` van en `.gitignore`.

## Verification Checklist

- [ ] `engram --version` funciona en cada laptop del equipo
- [ ] Plugin instalado vía marketplace (`claude mcp list` muestra `plugin:engram:engram`)
- [ ] `engram cloud status` = not enrolled para este proyecto
- [ ] `mem_current_project` devuelve el proyecto del portal desde Claude Code
- [ ] DB SQLite fuera del repo; `.gitignore` excluye estado local de Engram
- [ ] Ningún `mem_save` contiene `Bearer`, claves, emails de participantes ni rutas a credenciales
- [ ] Ningún código de `backend/`, `ml/` ni `frontend/` importa o invoca `engram`

## When NOT to Use This Skill

- Memoria conversacional del agente del producto → `portal-adk-agent` (SessionService).
- Retrieval del catálogo semántico → `portal-catalog-rag`.
- Documentar decisiones formales de arquitectura → ADR en `docs/` (Engram guarda el puntero, no reemplaza el documento).
