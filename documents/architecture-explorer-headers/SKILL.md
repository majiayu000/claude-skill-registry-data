---
name: architecture-explorer-headers
description: Backfill `<!-- EXPLORER_HEADER ... -->` blocks into existing `docs/NN-*.md` and `docs/components/**/*.md` files that are missing one. The header (5–10 lines after the H1) surfaces key concepts, technologies, components, scope, and related ADRs, which `explorer-cli.ts manifest` lists and downstream skills use to choose which files to read. Invoke when a doc lacks a header, when bulk-backfilling a legacy project, or whenever the explorer is misclassifying files.
triggers:
  - regenerate explorer headers
  - regenerate explorer header
  - add explorer headers
  - add explorer header
  - backfill explorer headers
  - backfill explorer header
  - explorer headers
  - update explorer headers
  - sync explorer headers
---

# Architecture Explorer Headers — Backfill Skill

## When This Skill Is Invoked

Manually activated when users want to add or refresh `<!-- EXPLORER_HEADER -->` blocks across architecture docs. This is a maintenance workflow, not part of the normal authoring loop. Use it:

- On a project whose docs are missing headers.
- When `explorer-cli.ts manifest` lists a clearly relevant file with no concepts, technologies or components — usually a missing or stale header.
- After a major refactor that renamed components or added technologies, where existing headers have drifted.

NOT activated for:
- Routine architecture authoring (use `architecture-docs`).
- **Component file creation or update** — `architecture-component-guardian` is the first-class writer of EXPLORER_HEADER blocks for `docs/components/**/*.md` (L1 descriptors and L2 containers) at create/update/migrate time. This backfill skill must NOT be used to fill gaps left by the guardian; reach for it only on legacy `docs/NN-*.md` files or to repair drift caused by external edits.
- ADR creation (use `architecture-definition-record`).

`ARCHITECTURE.md` at the project root is **never touched by this skill** — it is a navigation index and the explorer reads it in full.

---

## Documentation Language

Resolve the project's documentation language **before writing anything**, using the protocol in
`skills/architecture-docs/references/LANGUAGE_POLICY.md` §3:

```bash
rg -m1 '<!-- DOC_LANGUAGE:' ARCHITECTURE.md || rg -m1 '<!-- LANGUAGE:' ARCHITECTURE.md
```

`DOC_LANGUAGE` → use it. Legacy `LANGUAGE` → use it and rewrite the marker as `DOC_LANGUAGE`.
Neither → infer from headings (§5.5), ask the user to confirm **once**, stamp `DOC_LANGUAGE` into
`ARCHITECTURE.md`, and never infer again. Messages this skill displays to the user stay English
in every case; only authored file content follows `doc_language`.

**In this skill**: the `EXPLORER_HEADER` field **keys** (`key_concepts`, `technologies`, `components`, `component_self`, `component_type`, `scope`, `related_adrs`) are machine identifiers and stay English — `utils/header-detector.ts` matches them literally. Backfilled **values** follow the language of the document they describe: `key_concepts` and `scope` are prose and localize; `technologies` (product names), `component_self` / `components` (canonical slugs), `component_type` (fixed vocabulary) and `related_adrs` (ids) are verbatim in every language.

Structural headings this skill writes carry their English anchor comment in both languages
(`## Heading <!-- SECTION: English Name -->`). The full do-not-localize registry — codes, status
enum values, table column headers, filenames, marker names, `EXPLORER_HEADER` field keys — is
`LANGUAGE_POLICY.md` §4.

---

## Activation Forms

- `/skill architecture-explorer-headers` — interactive: scan, present plan, ask before writing.
- `/regenerate-explorer-headers` — slash-command alias.
- `/regenerate-explorer-headers --force` — overwrite existing headers (default behaviour skips files that already have one).
- `/regenerate-explorer-headers --dry-run` — list what would change, write nothing.
- `/regenerate-explorer-headers <path-glob>` — restrict to a subset (e.g. `docs/components/payment-service/**`).

---

## Workflow

### Phase 0 — Resolve Plugin and Project Roots

1. **Resolve `plugin_dir`**: `plugin_dir=$(bun ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts)` — the install registry's answer (project scope, else user scope, else the copy the script runs from), never a Glob over `~/.claude/plugins/cache/`; show its stderr warning when a newer version is on the machine.
2. **Confirm `project_root`**: the current working directory. Verify `ARCHITECTURE.md` exists at the root — if not, abort with `ARCHITECTURE.md not found at project root. This skill operates on architecture documentation.`

### Phase 1 — Inventory

```bash
bun [plugin_dir]/skills/architecture-explorer-headers/utils/header-cli.ts list <project_root>
```

The CLI emits a JSON array, one entry per candidate file:

```json
[
  { "path": "docs/01-system-overview.md", "has_header": false, "h1": "System Overview", "byte_size": 14820 },
  { "path": "docs/08-scalability-and-performance.md", "has_header": true, "h1": "Scalability & Performance", "byte_size": 18234 },
  { "path": "docs/components/payment-service.md", "has_header": false, "h1": "Payment Service", "byte_size": 9120 }
]
```

Parse it. Bucket files into:

- **needs_header** — `has_header === false` and the path is in scope (matches the `<path-glob>` argument if provided).
- **already_has_header** — `has_header === true`. With `--force`, treat these as needs_header too. Without `--force`, skip.
- **skipped** — outside scope, or `ARCHITECTURE.md` (excluded by the CLI).

If the inventory is empty, report `No docs need explorer headers.` and exit.

### Phase 2 — Present Plan

Show the user a one-screen plan:

```
Architecture Explorer Headers — Backfill Plan

Project: <project_root>
Scope:   <path-glob or "all docs">
Mode:    <add-missing | --force | --dry-run>

Files to update (N):
  - docs/01-system-overview.md     (no header)
  - docs/03-architecture-layers.md (no header)
  - docs/components/payment-service.md (no header)
  ...

Files skipped (M):
  - docs/08-scalability-and-performance.md (already has header — pass --force to overwrite)
  - ARCHITECTURE.md (project root index — exempt by design)

Proceed? (yes / no / edit-scope)
```

Wait for confirmation. On `--dry-run` skip the prompt and end after this report.

### Phase 3 — Generate and Insert Headers

For each file in `needs_header`:

**Step 3.1 — Read the full file.** You need the body to extract accurate metadata; do NOT cap reads here. (This skill is the inverse of the explorer — you are *creating* the metadata the explorer will later sample.)

**Step 3.2 — Extract metadata.** Build the EXPLORER_HEADER content from the file's actual content:

- `key_concepts` — 5–15 domain terms that recur in the doc. Pull from H2/H3 headings, bold terms, table headers, and frequently-occurring capitalized phrases. Avoid generic words ("system", "approach", "data"); favor specific ones ("SLO", "MTTR", "idempotency", "circuit breaker"). Downstream skills (compliance, analysis, dev-handoff) filter the explorer's manifest by these terms when deciding which files to read — concrete, domain-specific vocabulary surfaces relevant docs; generic vocabulary surfaces nothing.
- `technologies` — concrete tools/products named in the doc (Prometheus, AWS, PostgreSQL 16, Spring Boot 3.3, etc.). Skip generic terms ("database", "API"). Preserve version numbers.
- `components` — kebab-case component names referenced in the doc. Match `docs/components/<NN>-<slug>.md` filenames. For component files themselves, use `component_self: <slug>` instead.
- `scope` — one short sentence (≤120 chars) describing what the doc covers and what it does NOT. Read the doc's intro paragraph to source this.
- `related_adrs` — ADR identifiers (`ADR-NNN`) referenced in the doc body or footer.
- `component_self` (component files only) — the component's kebab-case slug, derived from filename.
- `component_type` (component files only) — extract from `**Type:**` field in the file. If absent, omit the field.
- `internal_name` (component files only) — the exact value of the `**Internal Name:**` metadata row (the repository / workload / product identifier when it differs from the canonical name, e.g. `shp-spa-order-history`). If the row is absent, omit the field; never derive it from the filename or invent one.

**Step 3.3 — Compose the 30-second summary blockquote.** One paragraph (≤300 chars) that complements the machine-readable header. Read for a reader who has 30 seconds to decide whether to read the full doc.

**Step 3.4 — Insert via Edit.**

Find the H1 line (`^# `) in the file. The insertion goes immediately after the H1 and the blank line that should follow it.

```markdown
# <existing H1>

<!-- EXPLORER_HEADER
key_concepts: <comma-separated>
technologies: <comma-separated>
components: <comma-separated>     # OR `component_self:` + `component_type:` for component files
scope: <one sentence>
related_adrs: <ADR-NNN, ADR-NNN>
-->

> <30-second summary paragraph>

<existing body>
```

Use the Edit tool (not Write) so you preserve the rest of the file byte-for-byte.

**Step 3.5 — Validate.**

```bash
bun [plugin_dir]/skills/architecture-explorer-headers/utils/explorer-cli.ts check <project_root> --file <abs_path>
```

Exit code 0 = the header parses, uses only the closed key set the parser reads, sits right after the H1, carries every required field, and its `component_self`, `components` and `related_adrs` point at files that exist. Exit code 1 = one of those is broken; revert the Edit, log the finding, continue with the next file. (`header-cli.ts validate` still exists for a single file in isolation; the gate is `check`, which sees the whole project.)

### Phase 4 — Report

Print a summary table:

```
Architecture Explorer Headers — Backfill Complete

Updated:   N files
Skipped:   M files (already had headers; pass --force to overwrite)
Failed:    K files (malformed header — Edit reverted)

Updated files:
  ✅ docs/01-system-overview.md
  ✅ docs/03-architecture-layers.md
  ✅ docs/components/payment-service.md
  ...

Failed files:
  ❌ docs/components/legacy-thing.md — header validation: missing 'scope' field
```

Suggest a follow-up: `Want me to /schedule an agent to re-run this monthly? Stale headers degrade explorer accuracy over time.`

---

## Anti-Patterns

1. **Don't generate headers from imagination.** Every field MUST come from the file's actual content. If a technology isn't named in the doc, don't list it. The explorer's classification is only as accurate as the header's truthfulness.
2. **Don't touch `ARCHITECTURE.md`.** It's a navigation index, exempt by design. The CLI's `list` subcommand excludes it.
3. **Don't run with `--force` on a freshly-tuned project.** Operators may have hand-curated headers; `--force` wipes that work. Default mode (skip-existing) is safe.
4. **Don't skip the validation step.** A malformed header (missing field, broken comment fence) is worse than no header — it actively misleads the parser. Always run `header-cli.ts validate` and revert on failure.
5. **Don't widen the scope past `docs/` and `docs/components/`.** Headers are not for ADRs (ADRs have their own structure that the explorer reads natively) or for `archive/v*/` snapshots (those are immutable).

---

## Permissions

This skill needs the same `Read`, `Edit`, and `Bash([plugin_dir]/skills/architecture-explorer-headers/utils/header-cli.ts list/validate)` permissions as `architecture-docs`. The pre-configured `.claude/settings.json.example` already covers them.

---

**Skill Version**: 1.2.0
**Specialization**: Backfill EXPLORER_HEADER blocks into legacy architecture docs
