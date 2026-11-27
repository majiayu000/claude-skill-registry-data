---
name: kio-backend-cloud
description: "Kio Backend, Database, Cloud & AI/ML hub. Use for server-side work: REST/GraphQL/tRPC API design, auth (OAuth2, JWT, sessions, RBAC, anti-IDOR), payments and idempotent webhooks (Stripe, PayPal, VNPay, MoMo, PayOS/VietQR, SePay), file uploads, queues and email; PostgreSQL schema, Supabase RLS, EXPLAIN/index tuning, zero-downtime migrations, Redis caching and locks; Docker, GitHub Actions CI/CD, Terraform IaC, deployments; RAG pipelines, pgvector hybrid search, re-ranking, RAG evaluation, QLoRA fine-tuning; building MCP servers (Python, TypeScript); scaffolding new projects (Next.js, FastAPI, WordPress FSE Docker)."
license: MIT
metadata:
  author: Kio System / Toan Pham
  version: 3.0.0
---

# ⚙️ Kio Backend, Database, Cloud & AI/ML (`kio-backend-cloud`)

The router for Kio's server-side work. Knowledge lives in `references/`; this file only points the way and holds the mandatory standards.

## ⚙️ How to work

1. **Read the project context first:** stack, ORM, where it runs (Vercel, VPS, AWS…), the project's `CLAUDE.md`/`AGENTS.md`. Do not switch the user's stack.
2. **Open the area overview** ("Start" column), then the deep-dive references it points to.
3. **Payments, auth, RLS, migrations:** follow the reference checklist exactly and write a test for every failure case it lists. These are never "temporary".
4. **Production changes** (migrations, infrastructure, secrets, DNS) need user approval and a rollback plan.
5. **MANDATORY reads (open the file before you write code, not from memory):** payment or webhook code → `references/payments-webhooks.md`; RLS, per-user data → `references/postgres-supabase-rls.md`; migrations or DDL on live tables → `references/migrations-and-caching.md`; MCP server → `references/mcp-server-builder.md`; RAG or vector search → `references/production-rag-pipelines.md`. In the answer, name the reference you followed.

## 🧭 Routing table

| Area | Start | Deep dives |
|---|---|---|
| API, auth, uploads, email, queues | `references/api-and-payments.md` | — |
| Payments & webhooks | `references/payments-webhooks.md` | Tested reference code: `scripts/payment_signatures.py`, `scripts/payment_apply.py` |
| PostgreSQL | `references/database.md` | `postgres-supabase-rls.md` (RLS, multi-tenant), `indexing-and-optimization.md` (EXPLAIN, indexes), `migrations-and-caching.md` (safe DDL, Redis) |
| DevOps & infrastructure | `references/devops.md` | `docker-containers.md`, `github-actions-cicd.md`, `terraform-iac.md` |
| AI/ML & RAG | `references/ai-ml.md` | `production-rag-pipelines.md`, `vector-db-and-eval.md`, `huggingface-fine-tuning.md` |
| MCP servers | `references/mcp-server-builder.md` | `mcp/best-practices.md`, `mcp/python-server.md`, `mcp/typescript-server.md`, `mcp/evaluation.md` |
| New project scaffolding | `references/project-scaffolding.md` | — |

All deep-dive paths are inside `references/`.

## 🔀 Selection rules for overlaps

| Need | Start at | Switch when |
|---|---|---|
| "Integrate payments" | `payments-webhooks.md` | General API/auth rules around the payment flow → `api-and-payments.md` |
| Slow query | `indexing-and-optimization.md` | Missing cache or lock contention → `migrations-and-caching.md` |
| Per-user data security | `postgres-supabase-rls.md` | API without Supabase → Anti-IDOR section of `api-and-payments.md` |
| Schema change | `migrations-and-caching.md` | Adding an index → §5 of `indexing-and-optimization.md` |
| Semantic search | `production-rag-pipelines.md` | Index/metric choice, quality measurement → `vector-db-and-eval.md` |
| "Should we fine-tune?" | §3 of `huggingface-fine-tuning.md` | Usually RAG instead → `production-rag-pipelines.md` |
| Deploy | `devops.md` | Image → `docker-containers.md`; pipeline → `github-actions-cicd.md`; infra → `terraform-iac.md` |

## 🧩 Workflows

| Job | Order |
|---|---|
| New SaaS | `project-scaffolding.md` → `database.md` + `postgres-supabase-rls.md` → `api-and-payments.md` → `payments-webhooks.md` → `docker-containers.md` → `github-actions-cicd.md` |
| Add a Vietnamese payment gateway | `payments-webhooks.md` (VNPay/MoMo/PayOS/SePay) → `payment_events` table → tests from §4 → `github-actions-cicd.md` |
| Docs Q&A chatbot | `production-rag-pipelines.md` → `vector-db-and-eval.md` (eval set first) → `api-and-payments.md` (rate limits, auth) |
| Expose an internal API to AI | `mcp/best-practices.md` → `mcp/python-server.md` or `mcp/typescript-server.md` → `mcp/evaluation.md` |
| Go to production | `terraform-iac.md` → `docker-containers.md` → `github-actions-cicd.md` → `migrations-and-caching.md` (backward-compatible migrations) |

UI belongs to `kio-frontend-craft`; security review, test cases and Playwright to `kio-qa-security`.

## 🛡️ Mandatory standards

1. **No secret exposure.** Never hardcode credentials, JWT secrets or API keys; read them from environment variables or a secret manager. Commit `.env.example`, never `.env`.
2. **Idempotent payment webhooks.** Verify signatures on the raw body with a constant-time compare, match the amount, and record `(provider, event_id)` under a unique key in the same transaction as the order update.
3. **Server-side authorisation.** Every by-ID query checks ownership (anti-IDOR) or is covered by RLS; never trust client-sent prices, roles or statuses.
4. **Database performance.** Large tables have indexes matching their filters and sorts, verified with `EXPLAIN (ANALYZE, BUFFERS)`; keyset pagination instead of large `OFFSET`s.
5. **Zero-downtime migrations.** `lock_timeout`, `CREATE INDEX CONCURRENTLY`, `NOT VALID` → `VALIDATE` constraints, expand/contract for renames and type changes.
6. **Lean architecture (< 700 lines/file).** Layers `Routes/Controllers` → `Services` → `Repositories/Models`; no file over 700 lines.
7. **Safe errors.** Consistent JSON errors without stack traces or SQL; logs carry a request ID and never card data or secrets.
8. **Language:** answer in the language of the user's request (an English prompt gets an English answer), even when skill documents are written in another language.

## 📦 What's included

- `references/` — the documents in the table above (`mcp/` for MCP servers).
- `scripts/payment_signatures.py` — reference signature checks for Stripe, VNPay, MoMo, PayOS.
- `scripts/payment_apply.py` — applies a webhook exactly once: checks the amount before using the idempotency key, locks the order row, checks the update row count; the same SQL runs on PostgreSQL and SQLite. Tests: `python3 -m pytest scripts/tests` (set `KIO_TEST_PG_DSN` to also run against a real PostgreSQL).
- `THIRD_PARTY_NOTICES.md` — credits and licenses for the open-source sources Kio uses; keep it when redistributing.
