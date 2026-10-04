---
name: documentation-specialist
description: >
  Full-project documentation maker for orchestrator template or any forked app repo.
  Produces a GitHub Docs-style navigable site (docs/index.md + sections) plus agent cache.
  Uses .github/skills/chain/SKILL.md to compose load-cache, read-codebase, and readme-specialist. No secrets,
  trade secrets, or coding tips in output. Invoke .github/skills/documentation-specialist/SKILL.md or
  .github/skills/chain/SKILL.md documentation-full. Docs only — no source edits.
argument-hint: "Scope: full | refresh | architecture | onboarding | api — optional focus"
user-invocable: true
disable-model-invocation: false
---

# Documentation Specialist

**Purpose:** Produce a **complete, navigable documentation set** for this repo or any project — human-readable like [GitHub Docs](https://docs.github.com/) (hub → sections → step-by-step guides) **plus** agent cache in `docs/codebase/`.

**Docs only.** Do not edit application source, migrations, or tests unless the user explicitly expands scope.

**Blueprint:** [references/doc-site-blueprint.md](references/doc-site-blueprint.md)

## Content policy (non-negotiable)

| Allowed | Forbidden |
|---------|-----------|
| Step-by-step procedures, verify steps, Next steps links | Secrets (keys, tokens, passwords, real `.env` values) |
| Chain/skill/loop usage, manifest shapes, branch workflow | Trade secrets (undisclosed business logic, proprietary algorithms) |
| Architecture at appropriate abstraction | Coding tips, hacks, clever shortcuts, opinionated micro-optimizations |
| Config **field names and purpose** with placeholders (`YOUR_API_KEY`) | Production credentials, private URLs with auth |

When unsure → **omit** or use placeholder. Reference `CONVENTIONS.md` for standards, do not invent new "tips."

## Phase 0 — Manifest & scope (required)

1. Read `.github/project-manifest.yaml` (or `.claude/project-manifest.yaml`) — `stack`, `paths`, `token_policy`.
2. Read `docs/codebase/README.md`, `docs/index.md` (if present), `docs/codebase/.codebase-scan.txt`, latest `TODO/*.md`.
3. Classify repo:
   - **Template** (`stack.framework: generic`) — orchestrator prompts.github/skills/chain/SKILL.mds/loops/skills
   - **App fork** (laravel, django, etc.) — product guides, runtime, APIs, runbooks

4. Parse user scope (`$ARGUMENTS`):
   - `full` — full doc site + cache + optional codebase scan if stale
   - `refresh` — update from cache (no full scan)
   - `architecture` | `onboarding` | `api` | `integrations` — targeted section

## Phase 1 — Choose chain (opt-out allowed)

| User intent | Chain | Steps |
|-------------|-------|-------|
| Full docs / onboarding / stale cache | `.github/skills/chain/SKILL.md documentation-full` | load-cache → read-codebase → readme-specialist → documentation-specialist |
| Update docs from current cache | `.github/skills/chain/SKILL.md documentation-refresh` | load-cache → readme-specialist → documentation-specialist |
| Single section only | **No chain** — minimal cache load, then this skill | — |

Respect **no chain** / **skip chain** opt-out.

Emit when chaining: `Chain: <id> (<n> steps, tier <token_tier>)`

## Phase 2 — Chain handoffs (when chaining)

Pass ≤80 tokens between steps:

```json
{"doc_scope":"full","stack":"generic","cache_stale":false,"site_targets":["docs/index.md","docs/guides.github/skills/chain/SKILL.mds-and-skills.md"]}
```

| Step | Delivers |
|------|----------|
| `load-project-cache-first` | Cache cited; staleness flag |
| `read-codebase` | Updated `docs/codebase/*`, scan marker, repo memory |
| `readme-specialist` | Root `README.md` with link to `docs/index.md` |
| `documentation-specialist` (execute) | Full doc site + cache alignment + gap report |

## Phase 3 — Execute (two layers)

### Layer A — Human doc site (GitHub Docs style)

**Required for `full` scope.** Create or refresh:

```
docs/
  index.md                    # Navigable hub (sidebar-style lists)
  getting-started/
    index.md
    quickstart.md
    project-overview.md
  guides/
    index.md
    daily-workflow.md
    chains-and-skills.md
    documentation.md
  reference/
    index.md
    manifest.md
    chains.md
    skills.md
  operations/
    index.md
    testing.md
    delivery.md
```

**Every page must have:** Overview → Before you begin → numbered Steps → Verify → **Next steps** (2–3 links).

**Every section** must have `index.md` listing child pages with one-line descriptions.

See [references/doc-site-blueprint.md](references/doc-site-blueprint.md) for templates and app-repo extensions.

### Layer B — Agent cache (`docs/codebase/`)

Keep cache lean for AI sessions (may overlap summaries with Layer A but cache stays section-oriented):

| File | Contents |
|------|----------|
| `docs/codebase/README.md` | Cache index; link to `docs/index.md` for humans |
| `ARCHITECTURE.md` | Manifest → cache → chains/loops |
| `STRUCTURE.md` | Directory map |
| `CONVENTIONS.md` | Branch, sync, script-first, token rules |
| `TESTING.md` | Audit scripts, CI gates |
| `INTEGRATIONS.md` | GitHub, sync targets |
| `CONCERNS.md` | Numbered risks + mitigations (no secret detail) |
| `STACK.md` | Tooling (app repos) |

### App repos — add when applicable

`docs/guides/local-runtime.md`, `docs/reference/api.md`, `docs/operations/deploy.md`, existing `docs/guides/`, `docs/runbooks/`.

### Quality rules

- `[UPDATED YYYY-MM-DD]` on every touched file
- Relative links only; hub reachable in ≤2 clicks from any page
- Factual claims cite `path` from cache or read-codebase — no invented behavior
- `.github/skills/script-not-shell/SKILL.md` for multi-line shell (CONCERNS §6)
- After `.grok/` edits: remind `python3 scripts/sync_grok_to_github_claude.py`
- **Red-team pass:** scan draft for secrets, trade secrets, coding tips before marking complete

## Phase 4 — Gap report

```markdown
## Documentation complete: <scope>

- Chain used: <id or "none">
- Human site: docs/index.md + <N> pages across <sections>
- Cache updated: <list>
- Content policy: pass (no secrets/tips flagged)
- Gaps: <numbered or "none">
- Next: <1–3 actions>
```

Optional: `reports.github/skills/chain/SKILL.mds/YYYY-MM-DD-documentation-<scope>.md`

## Anti-patterns

- Flat markdown dump with no `docs/index.md` hub
- Pages without **Next steps**
- Embedding real credentials "for convenience"
- Coding tip sidebars ("pro tip: use reflection to…")
- Full codebase scan on `refresh` when cache is fresh
- Skipping `readme-specialist` on full runs
- Forcing a chain after user opted out

## Related

- Blueprint: [references/doc-site-blueprint.md](references/doc-site-blueprint.md)
- Chains: `documentation-full`, `documentation-refresh`
- README polish: `/readme-specialist`
- Cache rebuild: `.github/prompts/read-codebase.prompt.md`
- Composition: `.github/skills/chain/SKILL.md`