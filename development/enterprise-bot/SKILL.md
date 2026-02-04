---
name: enterprise_bot
description: Lazy-load access to enterprise_bot codebase. Provides 12 nuclear protocol exports (cfg, CogTwin, auth, memory) and zipped source. Load SKILL.md instead of 60 files. Extract from src.zip on demand.
---

# enterprise_bot Skill

## Purpose
Lazy-load access to the enterprise_bot codebase. Load this skill instead of reading 60 files.

## Quick Start

**To use enterprise_bot in new code:**
```python
from protocols import cfg, get_auth_service, CogTwin, MemoryNode
# That's it. 12 exports. Everything else is internal.
```


---

## Nuclear Elements (protocols.py)

These 12 exports are the ONLY stable API. Everything else is implementation detail.

| Export | Module | Purpose |
|--------|--------|---------|
| `cfg(key, default)` | config_loader | Get any config value |
| `load_config(path)` | config_loader | Load YAML config |
| `get_auth_service()` | auth_service | Singleton for auth |
| `authenticate_user(email)` | auth_service | SSO → database user |
| `User` | auth_service | Auth user dataclass |
| `get_tenant_service()` | tenant_service | Singleton for tenant/dept |
| `TenantContext` | enterprise_tenant | Request context carrier |
| `CogTwin` | cog_twin | The brain (query pipeline) |
| `DualRetriever` | retrieval | Memory retrieval system |
| `create_adapter(provider)` | model_adapter | LLM factory |
| `MemoryNode` | schemas | Memory chunk dataclass |
| `EpisodicMemory` | schemas | Episode dataclass |

---

## Rules

1. **New code imports from `protocols` only** - never import internal modules directly
2. **Modifying internals?** - Extract from src.zip, edit, test, re-zip
3. **Adding new nuclear elements?** - Update protocols.py + this table
4. **Implementation changes** - Fine, as long as protocol signatures stay stable

---

## File Tree

```
enterprise_bot/
├── protocols.py              # ← START HERE (12 exports)
│
├── ══ CONFIGURATION ══
├── config.yaml               # App config (tier, features, model)
├── config_loader.py          # cfg() helper
├── config.py                 # Settings class
│
├── ══ ENTRY POINTS ══
├── main.py                   # FastAPI app + WebSocket
├── claude_chat.py            # SDK agent REPL
├── claude_run.py             # One-shot executor
│
├── ══ AUTH ══
├── auth_service.py           # User CRUD, permissions
├── azure_auth.py             # Azure AD SSO
├── sso_routes.py             # OAuth callbacks
│
├── ══ TENANT ══
├── tenant_service.py         # Department content
├── enterprise_tenant.py      # TenantContext dataclass
│
├── ══ COGNITIVE ══
├── cog_twin.py               # Main brain
├── retrieval.py              # DualRetriever
├── model_adapter.py          # LLM factory
├── venom_voice.py            # Personality injection
│
├── ══ MEMORY ══
├── memory_backend.py         # Abstract + FileBackend
├── postgres_backend.py       # PostgreSQL backend
├── schemas.py                # MemoryNode, EpisodicMemory
│
├── ══ SEARCH (internal) ══
├── hybrid_search.py          # Vector + keyword
├── scoring.py                # Relevance scoring
├── embedder.py               # Embedding generation
│
├── ══ DATA ══
├── data/memories/            # File-based memory storage
├── Manuals/Driscoll/         # Department manuals + chunks
│
├── ══ DB ══
├── db/migrations/            # PostgreSQL migrations
│
└── frontend/                 # SvelteKit app
```

---

## Token Budget

| Load | Tokens |
|------|--------|
| This SKILL.md | ~600 |
| protocols.py | ~150 |
| Extract 1 file | 200-800 |
| **Full cold start** | **~800** |

vs old way: 70,000 tokens to load everything

---

## Common Tasks

**Add a new API endpoint:**
```bash
unzip -p src.zip main.py > main.py
# Edit main.py
# Test
zip -u src.zip main.py
```

**Modify retrieval logic:**
```bash
unzip -p src.zip retrieval.py > retrieval.py
# Edit - but DON'T change DualRetriever's public interface
# Test
zip -u src.zip retrieval.py
```

**Check what's in a module:**
```bash
unzip -p src.zip cog_twin.py | grep "def \|class "
```

---

## Version
- Skill: 1.0.0
- Codebase: enterprise_bot @ commit `b601f3b`
- Last updated: 2024-12-19
