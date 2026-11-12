---
name: engine-api
description: >
  The LLM-facing contract for the deterministic claude-wiki-pages Bun engine —
  how ANY agent should call it. Documents each subcommand (verify, fix, heal,
  doctor, config, migrate, search, snapshot; plus planned index/link-suggest), its `--json` output shape, exit
  codes, and when to call it on a write-path. Trigger when an agent or user
  asks "how do I call the engine", "what does the engine return", "how do I
  verify/heal programmatically", or invokes /claude-wiki-pages:engine-api. This
  is reference material, not an action — it teaches the tool surface.
allowed-tools: Read Bash
---

# Engine API — the deterministic tool surface

The engine is a Bun CLI invoked through `scripts/engine.sh <command> [--target <vault>] [--json]`.
It is the source of truth for anything that must be exact (the wikilink graph,
frontmatter, MOC integrity). Agents call it and reason over its structured
output instead of eyeballing the vault. **Always pass `--json` for machine use.**

## Invocation

```sh
bash "${CLAUDE_PLUGIN_ROOT}/scripts/engine.sh" <command> --target <vault> --json
```

Global flags:

- `--target <vault>` — the vault root to operate on. Always supply this when a vault registry is
  configured; omitting it lets the engine resolve the vault independently, which may disagree with
  the hook's resolved path.
- `--other-vaults <colon-separated-paths>` — the registered vault roots other than the active one,
  used by the `firewall` command to enforce the `cross-vault` deny rule. Derive this value from
  `registry_other_vaults` in `scripts/resolve-vault.sh` rather than hard-coding paths. See
  [Multi-vault operating rules](../maintain-contract/SKILL.md#multi-vault-operating-rules) for the
  full confinement contract (ADR-0009 + ADR-0016).
- `--json` — emit structured JSON output. Always pass this for machine use.

If Bun is missing, the bridge prints a warning and exits 0 — degrade to the bash
verifiers (`verify-ingest.sh`) rather than failing.

## Commands

### `verify` — read-only integrity check

Ports `verify-ingest.sh` CHECK 0–3. Returns a report; **exit 1 when any error**, else 0.

```json
{
  "command": "verify",
  "vault": "docs/vault",
  "findings": [
    {
      "severity": "error|warn|info",
      "check": "schema|index-duplicates|sources-format|moc|orphan-sources|topic-folder|legacy-index-filename",
      "message": "…",
      "file": "…"
    }
  ],
  "errors": 0,
  "warnings": 0,
  "clean": true
}
```

At schema_version 3 the per-folder index is a **folder note** (`wiki/<topic>/<topic>.md`,
`type: index`). A legacy `_index.md` is still accepted, but verify emits a
WARN-severity `legacy-index-filename` finding for it — message: run
`engine.sh migrate --write`. The WARN never flips `clean` to false on its own.

Call it: before trusting the vault, and after every write-path as the closing gate.

### `fix` — deterministic safe repairs (idempotent)

Repairs only what has one correct value: index duplicates, missing folder notes
(created at the canonical name `<folder>/<folder>.md`), folder-note children
drift. It never renames an existing legacy `_index.md` — that is `migrate`'s
job (`rename-index`). Never touches body prose, schema_version, or sources
semantics. Running twice changes nothing. Exit 0.

```json
{
  "command": "fix",
  "vault": "…",
  "changes": [{ "file": "…", "action": "dedupe-index|create-index|sync-children" }],
  "changed": 2
}
```

### `heal` — git-checkpointed self-heal (the write-path closer)

Checkpoints the vault in git, then loops `verify → fix → re-verify` until clean
or no progress, and commits the result. **Exit 0 when clean, 1 when errors
remain.** Rollback is `git revert <healCommit>`.

```json
{ "command": "heal", "vault": "…", "errorsBefore": 2, "errorsAfter": 0,
  "iterations": 1, "clean": true, "checkpoint": "<sha>", "healCommit": "<sha>",
  "changes": [ … ], "unresolved": [] }
```

### `doctor` — environment + vault health (D01–D10)

Returns `{ results: [{ id, title, status, message, hint }], worst }` with status
`pass|warn|fail|fixed|skip`. `--fix` repairs D04/D05/D08; `--strict` exits 3 on
any warn/fail. See `/claude-wiki-pages:doctor`.

### `config` — effective configuration

`config` (show), `config validate` (exit 1 on schema violations), `config path`.
Merges defaults ← user (`~/.config/claude-wiki-pages/config.json`) ← project
(`.claude/claude-wiki-pages.json`) ← `CLAUDE_WIKI_PAGES_*` env overrides.

### `migrate` — upgrade schema_version in place (v1 → v2 → v3)

Dry-run by default; `--write` applies under a git checkpoint. Additive and
idempotent (bumps `schema_version`, writes new templates, generates the source
manifest). The v2 → v3 step adds the **`rename-index`** action: each legacy
`_index.md` is renamed to its folder-note name (`<folder>/<folder>.md`) and
the wikilinks that pointed at it are rewritten; a name conflict (a
`<folder>.md` already exists) is reported and skipped, never overwritten.
This rename clears the `legacy-index-filename` WARN that `verify` emits.
Rollback is `git revert <commit>` (printed on completion).

```json
{
  "command": "migrate",
  "vault": "…",
  "from": 2,
  "to": 3,
  "applied": true,
  "changes": [{ "file": "…", "action": "bump-schema|add-template|generate-manifest|rename-index" }],
  "checkpoint": "<sha>",
  "message": "Migrated schema_version 2 → 3 …"
}
```

### `search` — deterministic keyword retrieval

`search "<query>"` ranks `wiki/` pages (title/alias > tag > body, ties by title)
and returns `[[wikilink]]`-ready hits. Reproducible — same query, same ranking.
A candidate set, not a cited answer (use `query` for that).

```json
{
  "command": "search",
  "vault": "…",
  "query": "graph rag",
  "hits": [
    {
      "title": "Graph RAG",
      "wikilink": "[[Graph RAG]]",
      "file": "…",
      "type": "concept",
      "score": 18,
      "snippet": "…"
    }
  ]
}
```

### `backlog` — outstanding-maintenance probe

`backlog` reports pending raw sources (no `_sources/` summary, or manifest
`pending`) and overdue lint. The deterministic input to the heartbeat and the
maintenance agent.

```json
{
  "command": "backlog",
  "vault": "…",
  "pendingRaw": ["raw/x.md"],
  "lastIngest": "2026-05-20",
  "lastLint": "2026-05-21",
  "daysSinceLint": 9,
  "needsCatchup": true
}
```

### `propose` — human-in-the-loop draft review

Drafts live under `_proposed/` (outside `wiki/`, so unvalidated until promoted).
`propose review` lists them with a readiness check; `propose approve --file <p>`
promotes a draft into `wiki/` (status→active, drops `proposed_by`, git
checkpoint); `propose reject --file <p>` deletes it under a checkpoint.

```json
{
  "command": "propose",
  "sub": "approve",
  "vault": "…",
  "promoted": ["wiki/topics/x.md"],
  "checkpoint": "<sha>",
  "message": "promoted … Next: curator heal + polish. Rollback: git revert <sha>"
}
```

### `snapshot` — git-bound an LLM write phase

`snapshot pre` checkpoints the vault before a write phase; `snapshot post`
commits whatever the phase wrote. Use it around any write phase that happens
OUTSIDE the engine (ingest, curator judgment fixes, polish) — engine verbs
checkpoint themselves. Prefer the wrapper
`bash "${CLAUDE_PLUGIN_ROOT}/scripts/snapshot.sh" <pre|post> --target <vault> [--label <msg>]`,
which falls back to inline git when Bun is absent. Honors `gitCheckpoint.mode`
(`off` → no-op) and is pathspec-scoped to the vault. **Always exits 0 — it
reports, it never gates.**

```json
{
  "command": "snapshot",
  "sub": "post",
  "vault": "…",
  "mode": "commit",
  "sha": "<sha>",
  "skipped": false,
  "reason": null,
  "message": "snapshot post: committed <sha> (ingest …; rollback: git revert <sha>)"
}
```

A clean vault on `post` returns `skipped: true, reason: "clean"` — expected
after an idempotent pass, not an error.

### `capabilities` — agent-facing verb-surface manifest (ADR-0015)

`capabilities --json` returns the engine's own dispatch table as a machine-readable
manifest. Agents call this to discover which verbs are safe to invoke without parsing
prose or guessing. The output is deterministic (same call, same result, every run).

```json
{
  "command": "capabilities",
  "vault": "",
  "findings": [],
  "errors": 0,
  "warnings": 0,
  "clean": true,
  "manifest": {
    "verbs": [
      { "name": "verify", "status": "implemented" },
      { "name": "fix", "status": "implemented" },
      { "name": "heal", "status": "implemented" },
      { "name": "doctor", "status": "implemented" },
      { "name": "config", "status": "implemented" },
      { "name": "migrate", "status": "implemented" },
      { "name": "search", "status": "implemented" },
      { "name": "firewall", "status": "implemented" },
      { "name": "backlog", "status": "implemented" },
      { "name": "propose", "status": "implemented" },
      { "name": "capabilities", "status": "implemented" },
      { "name": "ontology", "status": "implemented" },
      { "name": "route", "status": "implemented" },
      { "name": "snapshot", "status": "implemented" },
      { "name": "index", "status": "planned" },
      { "name": "link-suggest", "status": "planned" }
    ]
  }
}
```

Exit 0 (clean). The `manifest.verbs` array is the authoritative list — every
`status: "implemented"` verb has a live dispatch branch; every `status: "planned"`
verb returns `{status:"not-implemented"}` until it ships. **Why-not-RAG:** exact
enumeration of the engine's own in-code dispatch table — same input, same output,
no corpus, no embeddings.

**Note:** `capabilities` is an agent-facing term (ADR-0015 Glossary note). It is
defined here (agent-facing skill) and must not appear in user-facing onboarding.

### Planned (return `{status:"not-implemented"}` until shipped)

`index` (deterministic page/entity index), `link-suggest <page>` (exact auto-link
candidates).

## Graceful degradation for planned verbs

When a planned verb is unavailable (returns `{status:"not-implemented"}`), fall
back deterministically. Do not block the calling agent or return an error to the
user — substitute the approved fallback listed below, then continue.

| Planned verb   | Returns when called today    | Approved deterministic fallback                                                                                                                                                                                                          |
| -------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `index`        | `{status:"not-implemented"}` | Read `wiki/index.md` directly (the hand-maintained top-level catalog). Use `Glob` to enumerate `wiki/**/*.md` when a full page list is needed; never synthesize an index in memory.                                                      |
| `link-suggest` | `{status:"not-implemented"}` | Use `grep`/`Glob` over `wiki/` to find typed wikilinks whose `[[title]]` matches the target term. Exact-string match only — no fuzzy or similarity search.                                                                               |

(The former planned `checkpoint` verb shipped as `snapshot`; its degradation
path lives inside `scripts/snapshot.sh` itself — the wrapper falls back to
inline git when Bun is absent, so callers never need a manual fallback.)

Confirm which verbs are currently implemented before calling a planned one:
`bash scripts/engine.sh capabilities --json` returns `.manifest.verbs[]` with
`status:"implemented"` or `status:"planned"`. Check this once per session rather
than hardcoding assumptions about the shipped set.

## Ontology-aware write guard

> **Gating note.** This section describes guidance that activates once P3.3
> (the `ontology` verb, `src/commands/ontology/`) ships and `ontology --json`
> is available. Until then, the `entity_type` allow-list is documented in
> `skills/init/template/CLAUDE.md` (the `ontology-profile-v1` section, enum table)
> and must be read from there directly. Do not write `entity_type` values without
> consulting the allow-list from one of these two sources.

`entity_type` is the **only vault-extensible field** in the schema. Every other
enum (`type`, `source_type`, `synthesis_type`, `project_status`, `source_format`,
`status`) is closed-core and not owner-extensible — writing a value outside the
core set for those fields is an error.

For `entity_type`, the legal set is the core values **plus** any per-vault
extensions the vault owner has declared. Once P3.3 ships, an agent resolves the
live allow-list at write time by calling:

```sh
bash scripts/engine.sh ontology --json --target <vault>
```

and reading `.enums.entity_type[]` from the output. That array is the composed
set (core ∪ `entity_type_extensions` from the vault's own `CLAUDE.md`), computed
at read time by the engine. Do not cache it across vaults or across sessions.

**Write-guard rule.** Before writing a page with an `entity_type` value, verify
the value appears in `.enums.entity_type[]`. If the value is absent, stop and
surface an error — do not write the page. If `ontology --json` is unavailable
(P3.3 not yet shipped), read the core list from
`skills/init/template/CLAUDE.md` `ontology-profile-v1` enum table and apply the
same membership check there.

**No other `*_extensions` field composes.** Only `entity_type_extensions` is
recognized. Any other `*_extensions` key in a vault's `CLAUDE.md` is ignored by
the engine (D15; `docs/plan/0005-software-3-0-deferred.md` decision N7). Do not
write, propagate, or reason over unrecognized extension keys.

## The rule for callers

Ground, then judge, then verify: let the engine compute facts (candidates,
findings) — never hallucinate them — make only the judgment calls yourself, and
end every write-path with `verify` (or `heal`). See `/claude-wiki-pages:maintain-contract`.

## Specification anchor

Contracts: [`docs/architecture.md`](../../docs/architecture.md) (engine layer & command contracts).
