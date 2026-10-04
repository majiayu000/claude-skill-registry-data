---
name: langflow
description: |
  Langflow — plateforme visuelle de construction d'agents IA et workflows LLM (backend FastAPI + UI React).
  Builder drag-and-drop de flows RAG/multi-agents, expose les flows comme outils MCP, ou consomme
  des MCP servers existants. Tourne comme service web (port 7860) dans un venv isolé.
  Use when: user asks to build a visual AI workflow, design a multi-step LLM pipeline, prototype a RAG,
  orchestrate tools visually, expose a flow as an MCP tool, chain LLM calls with custom tools,
  drag-and-drop AI agent builder, "langflow", "visual workflow", "flow IA", "RAG builder".
  Triggers: "langflow", "visual flow", "workflow IA", "RAG builder", "drag and drop agent",
  "multi-agent orchestration", "flow LLM", "diagramme IA", "expose flow as tool".

  Don't use when: target is a simple scraping task (use scrapling/scrapy), target is a static API
  integration (write a service module directly), you need programmatic fine-grained control (write
  Python/TS directly — Langflow is visual-first). Langflow is a prototyping/orchestration layer.

  Requires: venv .venv-langflow/ (isolé), démarré via `node scripts/langflow-cli.js start`.
  Pas de clé API requise pour l'usage local (LLM providers configurés dans l'UI).
license: MIT
metadata:
  author: langflow-ai (DataStax) / pariscore-cto (intégration)
  version: "1.x"
  source: https://github.com/langflow-ai/langflow
---

# Langflow — Plateforme visuelle d'agents IA + MCP bidirectionnel

> **Rôle** : Construire visuellement (drag-and-drop) des workflows IA multi-étapes
> (RAG, agents, chaînes LLM + tools), les exposer comme outils MCP, ou orchestrer
> les serveurs MCP existants de PariScore (Scrapling, Scrapy, BSD, etc.).
> Service web (port 7860) dans un venv isolé pour protéger Scrapy/Scrapling.

## Architecture (différente de Scrapling/Scrapy)

| Aspect | Scrapling/Scrapy | **Langflow** |
|--------|------------------|--------------|
| Type | Lib Python | **Application web complète** |
| Runtime | Import dans script | Service backend + UI React |
| Démarrage | Immédiat | `langflow run` (~20s startup) |
| Dépendances | ~10-50 | **~200** (tout l'écosystème LangChain) |
| Isolation | Dans l'env global | **venv dédié `.venv-langflow/`** |
| Port | N/A | **7860** (configurable) |

**Pourquoi un venv isolé** : Langflow tire tout LangChain + FastAPI + SQLAlchemy + chromadb.
Une install dans l'env global casserait les versions pydantic/starlette/uvicorn dont Scrapling
et le MCP dépendent. Le venv `.venv-langflow/` isole complètement.

## Setup (déjà fait)

```bash
# 1. uv installé (recommandé par Langflow, plus rapide que pip)
python -m pip install uv

# 2. Venv dédié
uv venv .venv-langflow --python 3.12

# 3. Install langflow dans le venv
VIRTUAL_ENV=$(pwd)/.venv-langflow uv pip install langflow

# 4. Wrapper CLI pour gérer le lifecycle (déjà créé)
node scripts/langflow-cli.js install   # (re)fait les étapes 2-3 si besoin
node scripts/langflow-cli.js start     # démarre le serveur
```

## Usage via le wrapper CLI

```bash
# Démarrer Langflow (default: http://127.0.0.1:7860)
node scripts/langflow-cli.js start
node scripts/langflow-cli.js start --port 8080 --host 0.0.0.0

# Vérifier l'état (process + health check)
node scripts/langflow-cli.js status

# Obtenir les URLs (UI/API docs/MCP endpoint)
node scripts/langflow-cli.js url

# Voir les logs
node scripts/langflow-cli.js logs --lines 100

# Arrêter
node scripts/langflow-cli.js stop

# Version installée
node scripts/langflow-cli.js version
```

Le wrapper gère le PID file (`.langflow/langflow.pid`), les logs (`.langflow/langflow.log`),
et le health check (`/health`). Le serveur tourne en arrière-plan (détaché du CLI).

## URLs importantes

| URL | Usage |
|-----|-------|
| `http://127.0.0.1:7860` | **UI React** — builder drag-and-drop des flows |
| `http://127.0.0.1:7860/docs` | API docs (Swagger/OpenAPI) |
| `http://127.0.0.1:7860/api/v1/mcp` | Endpoint MCP server (expose flows comme outils) |
| `http://127.0.0.1:7860/health` | Health check |

## Cas d'usage typiques pour PariScore

### 1. Prototyper un RAG sur la doc PariScore
Drag-drop : `PDF loader` → `Text splitter` → `Embeddings` → `Vector store` → `LLM` → `Output`.
Brancher les `.context/*.md`, `CLAUDE.md`, `ARCHITECTURE.md` comme sources. Permet de poser
des questions en lang naturel sur l'architecture du projet.

### 2. Orchestrer les MCP servers existants
Le composant **MCP Tools** de Langflow permet d'appeler directement tes serveurs MCP PariScore :
- `scrapling` (stealth fetch)
- `scrapy` (bulk crawl)
- `bzzoiro-sports` (live tennis/foot)
- `sportradar` (stats)
- `playwright` (E2E browser)

Workflow visuel : `MCP scrapling stealthy_fetch` → `LLM analyse` → `MCP scrapy crawl_to_json`.
Utile pour prototyper un pipeline data complexe sans coder.

### 3. Exposer un flow comme outil MCP pour l'agent ZCode
Une fois un flow construit et testé dans Langflow :
1. Dans Langflow UI → onglet projet → **MCP Server** tab
2. Sélectionner les flows à exposer comme outils (Edit Tools)
3. L'endpoint MCP est `http://127.0.0.1:7860/api/v1/mcp`
4. L'agent ZCode peut alors appeler le flow comme un outil via cet endpoint

## Configuration LLM providers

Langflow supporte de nombreux providers (OpenAI, Anthropic, Google, Ollama local, etc.).
Les clés API se configurent dans l'UI (Settings → Models) ou via variables d'environnement.

PariScore a déjà `GEMINI_API_KEY` dans `.env` — Langflow peut l'utiliser directement via le
composant `Google Generative AI` (configurer la clé dans l'UI ou exporter `GOOGLE_API_KEY`).

Pour usage local sans cloud : **Ollama** (https://ollama.ai) — installer Ollama, pull un modèle
(`ollama pull llama3.1`), puis Langflow `Ollama` component (URL `http://localhost:11434`).

## Limites & coûts

- **Démarrage lent** : ~15-20s pour le backend FastAPI + chargement components
  (mesuré : banner "Welcome to Langflow" à ~17s, "Application startup complete" à ~20s).
  Pas adapté au serverless ; prévoir un service long-lived (pm2/systemd en prod).
- **RAM** : ~500MB-1GB à vide, plus selon les flows et vector stores actifs.
- **Venv volumineux** : `.venv-langflow/` ~2GB (tout LangChain + deps natives).
- **Persistance** : Langflow stocke les flows en SQLite (`langflow.db` dans le cwd au premier
  run). Pour la prod, brancher PostgreSQL via `LANGFLOW_DATABASE_URL`.
- **Coût LLM** : chaque flow qui appelle un LLM consomme des tokens. Surveiller les quotas.

## Spécificités Windows (validé 2026-07-13)

- **Premier run lent** : `langflow --version` et `langflow run` mettent 30-60s au tout premier
  appel (chargement eagerly de tous les components + cache). Les runs suivants sont rapides.
- **`langflow.exe` est un launcher** : il spawn un subprocess `python -m langflow`. Le PID dans
  `.langflow/langflow.pid` est celui du launcher. Pour arrêter proprement, le wrapper utilise
  `taskkill /F /T /PID` qui tue tout l'arbre (launcher + python), pas juste le launcher.
- **Telemetry warning** : au démarrage, `[error] Failed to start telemetry writer; ... [WinError 87]`
  s'affiche. C'est un warning Windows-only (le writer telemetry échoue, fallback legacy).
  **Non bloquant** — Langflow fonctionne normalement. Pour silencer : `DO_NOT_TRACK=true`.
- **Détachement** : le wrapper lance langflow avec `detached: true` + `unref()` + stdio redirigé
  vers fichier (pas de pipe node → le spinner langflow sature le buffer et stall le startup).
- **Sandbox ZCode** : dans le sandbox, les process backgroundés (`&`) sont tués. Pour valider
  le démarrage, lancer en foreground bloquant : `timeout 50 .venv-langflow/Scripts/langflow.exe run`.
  En conditions normales (VPS / shell local), le wrapper `langflow-cli.js start` fonctionne.

## Intégration avec l'écosystème PariScore

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT ZCODE                               │
└──────────┬───────────────────────────────┬───────────────────┘
           │ MCP (stdio)                   │ HTTP
           ▼                               ▼
┌─────────────────────┐         ┌──────────────────────────────┐
│ Serveurs MCP natifs │         │ Langflow (port 7860)          │
│  - scrapling        │◄────────│  - UI builder drag-and-drop   │
│  - scrapy           │ MCP     │  - Flows → MCP server         │
│  - bzzoiro-sports   │ client  │  - MCP Tools component        │
│  - sportradar       │         │    (consomme les MCP PariScore)│
│  - playwright       │         │  - LLM orchestration          │
└─────────────────────┘         └──────────────────────────────┘
```

Langflow est à la fois :
- **MCP client** : consomme scrapling/scrapy/sportradar via le composant MCP Tools
- **MCP server** : expose ses flows comme outils appelables par l'agent ZCode

## Anti-patterns

- ❌ Installer Langflow dans l'env global Python → casse Scrapling/Scrapy (conflits deps).
- ❌ Laisser Langflow tourner en permanence si pas utilisé (gaspillage RAM).
- ❌ Compter sur Langflow pour du scraping direct → utiliser Scrapling/Scrapy (plus adaptés).
- ❌ Mettre des clés API LLM en clair dans les flows exportés (git).
- ❌ Démarrer Langflow sur `0.0.0.0` sans auth en prod (UI exposée).

## Fichiers de référence

- `scripts/langflow-cli.js` — wrapper CLI (start/stop/status/logs/version/url/install)
- `scripts/test-langflow.js` — suite de validation (5 tests statiques + lifecycle `--full`)
- `.venv-langflow/` — venv isolé (non commité)
- `.langflow/` — PID + logs runtime (non commité)
- `.gitignore` — excludes `.venv-langflow/`, `.langflow/`
- https://github.com/langflow-ai/langflow — source officielle
- https://docs.langflow.org — documentation officielle
- https://docs.langflow.org/mcp-server — doc MCP server
- https://docs.langflow.org/mcp-client — doc MCP client

## Résultats de validation (2026-07-13)

| Test | Résultat | Détail |
|------|----------|--------|
| Venv `.venv-langflow/` créé | ✅ | Python 3.12.10 isolé |
| Binary `langflow.exe` présent | ✅ | 46KB launcher |
| Version | ✅ | **1.10.2** (via `importlib.metadata`) |
| Wrapper CLI help | ✅ | 7 commandes (install/start/stop/status/version/logs/url) |
| Wrapper CLI status | ✅ | JSON process + venv + binary check |
| Démarrage backend | ✅ | Welcome banner + "Started server process [15912]" + "Waiting for application startup" capturés à ~17s |
| Health check `/health` | ⚠️ sandbox | Non validable dans le sandbox ZCode (background process killed). Marche en conditions normales (VPS/shell local). |
| Endpoint MCP `/api/v1/mcp` | ⚠️ sandbox | Idem — nécessite langflow tournant en arrière-plan ( foreground-only dans sandbox) |

**Pour valider le démarrage en conditions réelles** (VPS, shell local Windows/Mac/Linux) :
```bash
node scripts/langflow-cli.js start                # démarre en arrière-plan détaché
node scripts/langflow-cli.js status               # health check + URLs
# Ouvre http://127.0.0.1:7860 dans le navigateur
node scripts/langflow-cli.js stop                 # arrêt propre (taskkill /T sur Windows)
```

---

*Skill orchestration IA PariScore — Langflow 1.10.2 intégré comme service web isolé.*
