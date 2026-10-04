---
name: project-architecture
description: "The master reference for how this project is structured — services, domains, database, and the rules for how services talk to each other. Consult this before creating any new service, folder, endpoint, or cross-service call. Any agent starting a new feature that might touch more than one service should read this first."
---

# Project Architecture — Master Reference

This project is a single monorepo containing independently deployed services sharing a shared database and running inside a single Railway project.

## The Eight Services

The repository has two main regions: `/store` (for the storefront and store backend) and `/studio` (for backend tools and ops services):

| Service | Folder | Language | Deploys to |
|---|---|---|---|
| Medusa backend | `store/backend` | Node.js (Medusa v2) | `mysite.com/api` |
| Storefront | `store/storefront` | Node.js (Next.js) | `mysite.com` |
| AI Gateway | `studio/ai-gateway` | Node.js (Express) | internal only |
| Dubbing | `studio/dubbing` | Python (FastAPI) | `studio.mysite.com/api/dub` |
| Bot Bridge | `studio/bot-bridge` | Node.js (Express) | internal only |
| Comment Bot | `studio/comment-bot` | Node.js (Express) | `studio.mysite.com/webhooks/comments` |
| TTS Service | `studio/tts-service` | Python (FastAPI) | internal only |
| Chatwoot | `studio/chatwoot` | Docker compose | `studio.mysite.com/chat` |

## The Two-Domain Split

- **`mysite.com`** — customer-facing storefront and API only. Must stay fast and polished.
- **`studio.mysite.com`** — operations side: Chatwoot inbox (`/chat`), comment webhook (`/webhooks/comments`), dubbing upload/processing (`/api/dub`). Only you and paying dubbing clients see this.

Internal services (`ai-gateway`, `bot-bridge`, `tts-service`) are fully private and accessible only via Railway private networking.

## The One Hard Rule: HTTP Only Between Services

Services NEVER import each other's code directly. They talk only over HTTP, using URLs from environment variables.

```javascript
// ❌ NEVER
import { dubVideo } from '../dubbing/pipeline'

// ✅ ALWAYS
const res = await fetch(process.env.DUBBING_URL + '/api/dub', {
  method: 'POST', body: JSON.stringify({ videoUrl })
})
```

Why: this is what makes it possible to move any single service to its own server/domain later by changing one env var, with zero code changes. Never hardcode `localhost:PORT` anywhere — always `process.env.<SERVICE>_URL`.

Standard service URL env vars:
```
STORE_URL=
STOREFRONT_URL=
DUBBING_URL=
AI_GATEWAY_URL=
TTS_SERVICE_URL=
CHATWOOT_URL=
```

## Shared Database (Supabase)

One Supabase project. Each service owns its own tables but all share the same Postgres instance.

| Table area | Owned by |
|---|---|
| `products`, `orders`, `customers` (Medusa's own schema) | Store (own Postgres instance) |
| `conversations`, `bot_logs` | Bot Bridge |
| `dubbing_jobs`, `dubbing_chunks` | Dubbing |
| `ai_requests` / `ai_usage_logs` (cost/usage log) | AI Gateway |
| `comment_log` | Comment Bot |
| `api_keys` | Dubbing (Clients auth) |
| `service_health` | Shared (ops) |

Row Level Security (RLS) is mandatory on every table — see the `security-engineering` skill for the exact policy pattern. Schema migrations live in `/architecture/migrations/` so any agent can see the full schema history.

## Per-Service Convention (non-negotiable)

Every service folder must contain:
- `README.md` — what it is, how to run it locally, which env vars it needs
- `.env.example` — every required var with a placeholder value (never real secrets)
- `.env` — real secrets, gitignored, never committed

If a new service is created and is missing either file, that is a bug — fix it immediately.

## AI Gateway Is the Only Door to AI Providers

No service calls Claude, Gemini, or MiniMax directly. All AI calls go through `AI_GATEWAY_URL`. See the `ai-gateway` skill for the contract. This is what lets you swap providers project-wide by editing one service.

## When Adding a New Feature

1. Does it belong in an existing service, or is it genuinely a new service? Default to existing unless it has its own deployment lifecycle.
2. Does it need AI? → call the AI Gateway, don't call providers directly.
3. Does it need new tables? → add a migration in `/architecture/migrations/`, add RLS policies, update the table-ownership list above.
4. Does it cross a service boundary? → HTTP + env var, never a direct import.
5. New service? → it needs its own README.md, .env.example, and an entry in the services table above and in the `deployment` skill.

## Future-Splitting Checklist

If any service ever needs to become its own product on its own domain:
- [ ] Confirm it has zero direct imports from other services (grep for relative imports crossing service folders)
- [ ] Confirm its `.env.example` is complete enough to deploy standalone
- [ ] Deploy it to the new location, update its `_URL` env var in the other services
- [ ] No other code changes should be required — if they are, that's a violation of the HTTP-only rule that should be fixed first
