---
name: load-project-cache-first
description: >
  Load ndestates-io project cache (docs/codebase/ + TODO + CONCERNS + .grok/.copilot memories) first before any deep exploration.
  Use at the start of almost every session to save tokens and provide accurate context quickly. Mandatory entry point for ongoing work.
argument-hint: "Optional: specific cache file or topic, e.g. 'CONCERNS', 'Filament panels', 'architecture', 'valuations'"
user-invocable: true
disable-model-invocation: false
---

# Load Local Codebase Cache First (Token-Efficient Session Start)

**This is the MASTER LOADER skill for the ndestates-io project.**

**MANDATORY FIRST STEP for most tasks on this project.**

Before performing any semantic_search, grep, or reading large numbers of source files, you **must** load the local knowledge cache.

**Read `.claude/project-manifest.yaml` first** — honor `token_policy.max_cache_files_default`, `grep_before_read`, and `no_source_until_confirmed`.

## Spine (always — does not count toward cap)

1. `docs/codebase/README.md` (index)
2. `docs/codebase/.codebase-scan.txt` (freshness)
3. Latest `TODO/*.md`
4. `.grok/memories/INDEX.md`

## Additional cache (cap: `max_cache_files_default`, default **2**)

Pick only what the task needs from `docs/codebase/`:
   - Architecture / overall understanding → `docs/codebase/ARCHITECTURE.md`
   - Tech stack and versions → `docs/codebase/STACK.md`
   - Directory layout and panels → `docs/codebase/STRUCTURE.md`
   - Rules, conventions, DDEV, DB safety → `docs/codebase/CONVENTIONS.md`
   - External integrations → `docs/codebase/INTEGRATIONS.md`
   - Testing rules and CI → `docs/codebase/TESTING.md`
   - Known risks and open items → `docs/codebase/CONCERNS.md` (recommended first pick)
5. At most **one** INDEX-selected memory file (counts toward cap if you already loaded 2 codebase docs).

**Grep-before-read (mandatory when `grep_before_read: true`)**:
- For any cache file >80 lines: `Grep` headings or keywords first; then `Read` with `offset`/`limit` for one section only.
- Do **not** read `chains/registry.yaml`, full skills, or app source until the user confirms direction — unless the task names an exact path.

**Rules for token efficiency**:
- Treat the cache files as your primary source of truth.
- Only read application source **after** cache load **and** user direction is clear (`no_source_until_confirmed`).
- If the cache appears stale, note this and ask the user before doing a full re-scan.
- When answering, cite the specific cache file(s) you used.

After loading the cache, confirm to the user with the list of loaded files.

Follow `.github/copilot-instructions.md` (DDEV, security, data safety) at all times.

See also the full prompt definition in `.grok/prompts/load-project-cache-first.md`.
