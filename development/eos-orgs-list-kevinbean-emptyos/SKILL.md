---
name: eos-orgs-list
description: List Real Orgs registered in `apps/public/standard/company/`. Use when the user asks "which orgs do I have", "list my companies", "show all teams", "what orgs are in the system", or wants to look up an org id before invoking `eos-orgs-member-add`. Read-only — never creates or modifies. NOT for creating an org (use eos-orgs-create) or adding a member (use eos-orgs-member-add).
---

# EmptyOS Orgs — List

Read-only listing of orgs from `apps/public/standard/company/`. Wraps `GET /orgs/api/orgs` with optional filters. Useful as a precursor to `eos-orgs-member-add` (which needs an org id) or just to confirm what the system already knows.

## When to Use

- "What orgs do I have?" / "List my companies" / "Show teams"
- Before `eos-orgs-member-add` — to find the target org's id
- To check whether an org already exists before invoking `eos-orgs-create`
- **Not** for inspecting one org's members — use the web UI at `/orgs/?org=<id>` for that (richer detail surface)

## Pre-flight

This skill reads through the daemon HTTP API, so the daemon must be reachable first:

- **Daemon up** — `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:9000/orgs/` should print `200`. If not, ask the user to run `restart.bat` — never start/restart the daemon yourself (`.claude/rules/daemon-handling.md`).
- **Auth (private mode)** — read `auth_token` from `emptyos.toml` `[network]` and send `Authorization: Bearer <token>` on every request (`.claude/rules/environment.md`).
- **Read-only** — this skill never creates or modifies; a failed call means the daemon or auth is off, not bad data.

## Filters

`GET /orgs/api/orgs` supports two query params:

- `reality=real` — filter to Real Orgs only (skip Persona Sims)
- `scope=member|private|public` — filter by visibility scope

Default: no filter, returns everything the user has access to.

## Process

### Step 1 — Read auth token

```bash
TOKEN=$(grep -E '^auth_token' D:/emptyos/emptyos.toml | head -1 | sed 's/.*= *"\(.*\)".*/\1/')
```

### Step 2 — Call the list endpoint

If the user's intent narrows the set (e.g. "list my real orgs"), apply the matching query param:

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://127.0.0.1:9000/orgs/api/orgs?reality=real"
```

If no narrowing context, omit the query string.

### Step 3 — Render compact

Print a table-style block. Columns: `id` · `name` · `kind` · `reality` · `members` (if response includes a member count; if not, omit). Sort by `name` ascending.

```
Real Orgs:
  acme-corp           Acme Corp          company    real
  build-club-sydney   Build Club Sydney  community  real
  phoenix-team        Phoenix team       team       real
```

If the list has >15 entries, render only the first 15 sorted by `updated` (most recent first) and footer with `(15 of 47 shown — narrow with reality=/scope=)`.

If the list is empty, say so and suggest `/eos-orgs-create`:

```
No orgs found. Create one with /eos-orgs-create.
```

### Step 4 — Stop

Do not chain into other skills. Do not propose follow-ups beyond what's already in the empty-state hint. Read-only means read-only.

## Anti-patterns

- **Don't** fetch each org's details one-by-one — the list endpoint already returns enough for a summary. Per-org GET is `eos-orgs-member-add`'s job.
- **Don't** include archived orgs unless the user asks. The list endpoint's default already filters them; don't override.
- **Don't** invent a `members` column if the response doesn't include member counts. Omit the column rather than render `?` or `0` everywhere.
