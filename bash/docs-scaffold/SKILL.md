---
name: docs-scaffold
description: Scaffold and maintain documentation as a single source of truth (SSOT)
  for humans and AI agents, in embedded (docs inside the code repo, Kiro specs) or
  standalone (separate docs repo) layouts. Detects gaps, stale sections, broken links
  and edited history with a warn-only CLI; preserves wrong or changed specs in .deprecated/;
  keeps an append-only, hash-chained session journal in the git-ignored ignore/ folder
  so agents can resume and audit their last steps.
argument-hint: <init | check | new | verify | deprecate | session> [args]
---

<!-- Generated from skills/docs-scaffold.md by tools/generate_integrations.py. Edit the source file, not this one. -->

# Docs Scaffold

Creates and maintains a documentation tree that humans and agents can read fast and trust: one home per fact, explicit gaps instead of silent ones, staleness detected from code changes, and history that is preserved instead of overwritten.

## Tooling

All operations go through the CLI shipped with this skill at `scripts/docs_scaffold.py`, next to this file (canonical source: `skills/docs-scaffold/scripts/docs_scaffold.py`). It needs Python 3.8+ and git, and nothing else. Run it from the project root:

```bash
python3 <skill-dir>/scripts/docs_scaffold.py <command> [args]
```

Every check is warn-only: `check` prints findings and exits 0. Exit code 2 means a usage or configuration error.

## Initialization (always ask first)

Before running `init`, explain both scaffold types to the user and ask which one to use. Never choose for them.

| | `embedded` | `standalone` |
|---|---|---|
| Layout | Docs inside the code repo (or monorepo) | Docs in their own repo; code in other repos |
| Use when | You own the code; AI-assisted and Kiro spec-driven work | Documenting systems you study or maintain but cannot write to; several code repos |
| `sources` | `src/billing/**` | `app:src/billing/**`, each repo declared in `manifest.json` `repos` with a `path_env` |
| Change specs | `.kiro/specs/<feature>/` | `<docs>/70-work/changes/<id>/` |
| Sync guarantee | Docs and code change in the same pull request, plus stale checks | Stale checks against local clones; missing clones report `unverifiable` |

Suggested question:

> This project has no docs scaffold yet. Where should the docs live?
> 1. **Embedded**: inside this repo, updated in the same pull request as the code. Best when you own the code.
> 2. **Standalone**: a separate docs repo that points at one or more code repos.
> Docs root will be `docs/` unless your conventions name another folder (use `.` for a docs repo whose root is the tree). Change it?

Then run `init --type <embedded|standalone> [--root <dir>] [--changes-dir <dir>] [--ignore-dir ignore]`. Existing files are never overwritten; report the ones `init` kept.

## Layout

```text
<docs root>/
├── README.md  INDEX.md (generated)  glossary.md
├── 10-context/        overview, requirements (REQ-n), nfr (NFR-n), constraints
├── 20-architecture/   system, data model, interfaces, cross-cutting
├── 30-units/<unit>/   README (section), design, tests (+ detail, interfaces, ops by unit kind)
├── 40-verification/   strategy, environments
├── 50-operations/     deploy, configuration, runbooks/
├── 60-decisions/      NNNN-<slug>.md, locked once approved
├── 70-work/           STATUS.md, investigations/, reviews/, releases/, test-runs/ (changes/ in standalone)
├── 80-guides/         onboarding, how-tos, examples
├── 90-meta/           conventions.md, manifest.json, locks.json
├── _generated/        machine-owned (traceability.md, code indexes)
└── .deprecated/       preserved wrong or superseded specs, read-only
<ignore dir>/          git-ignored, temporary only: README.md, sessions/, health.md
```

## Rules

1. One fact, one home. Link to it; never copy it.
2. Docs and specs are tracked by version control. The ignore dir holds only temporary, local material (session journals, health reports). Never put specs there.
3. `10-context/` to `50-operations/` describe the system as it is now. `60-decisions/` and `70-work/` are history.
4. Every live document has frontmatter: `id`, `type`, `status` (`draft`, `approved`, `todo`, `n/a` with `na_reason`, `closed`), `owner`, one-line `summary`, and `traces: [REQ-n]` where it satisfies requirements.
5. A section is a folder of 2 to 10 related documents whose `README.md` has `type: section`, `sources` (code globs) and `verified` (commit and date). Verification is per section, not per document.
6. Never hand-edit `INDEX.md`, `_generated/`, `.deprecated/README.md` or `90-meta/locks.json`; run `index`.
7. Never edit or delete closed work records, approved decisions, deprecated files or journal entries. Record corrections in a new document.
8. Do not modify a project's existing source folders to fit the scaffold; describe them through `sources` instead.

## Commands

| Command | Purpose |
|---|---|
| `check` | Warn-only report: structure, tracking, frontmatter, gaps, coverage, links, staleness, section size, locks, generated files, journal. Also writes `<ignore>/health.md`. |
| `index` | Regenerate `INDEX.md`, `_generated/traceability.md`, `.deprecated/README.md`; lock newly closed records. |
| `new unit <name> [--unit-kind K] [--group G]` | Unit folder with section README and required docs from `manifest.json` `unit_kinds`. |
| `new adr <slug>` | Next numbered decision record. |
| `new investigation\|review\|release <slug>` | Dated work record. |
| `new test-run <unit\|integration\|system>` | Dated test run with the next round number. |
| `new change <slug>` | Change spec folder (`requirements.md`, `design.md`, `tasks.md`) in the changes dir. |
| `verify <section-dir>...` | Stamp sections as verified at the current commit, after you have checked them against the code. |
| `deprecate <path> --reason R [--superseded-by ID\|none] [--keep]` | Preserve a spec in `.deprecated/YYYY-MM-DD-<slug>/`. |
| `session start\|log\|resync\|sync\|show` | Append-only session journal. |

## Session journal

The journal in `<ignore>/sessions/` is the agent's memory of what it did. Entries are appended, never edited or deleted, and each entry carries a hash of the previous one, so `check` detects edits, deletions and reordering across all session files.

1. At session start: `session start --goal "<task>"`. Read the printed previous entries and the `commits since last entry` and `stale sections` lines before doing anything else.
2. After every change to the codebase or docs: `session log --action "<what changed>" --result ok|fail|partial [--note "<why, errors, next>"]`. The CLI records HEAD and the changed files itself; describe intent and outcome, including failures.
3. If work happened outside the session (other tools, other people, a pull): `session resync`.
4. At milestones and before ending: update `70-work/STATUS.md` (Current focus, Next steps), then `session sync`. Sync records the journal position and health counts in STATUS.md, which detects a truncated journal later.
5. To find what went wrong: `session show -n 20`, then compare the failing entry's HEAD and changed files with `git log` and `git diff`.

## Deprecation

Deprecate a spec document (requirements, nfr, design, detail, interface, test, or a change spec) when it is wrong, mistaken, or about to change substantively.

- Substantive: changes behavior, scope, acceptance criteria, requirement IDs, interfaces, data definitions, values or design decisions. Deprecate.
- Minor: typography, spelling, formatting, whitespace, link repair. Do not deprecate; git history covers it.
- Unsure which one applies: ask the user before editing.

Before a substantive edit, run `deprecate <file> --reason "<why>" --keep` (copies the current version), then edit the live file. When a spec is replaced or withdrawn, create the replacement first, then `deprecate <path> --reason "<why>" --superseded-by <new-id>` (or `none`); the CLI moves the file, stamps `deprecated` frontmatter, locks it, and relinks or reports live links. Live documents must never link into `.deprecated/`.

## Spec-driven changes

1. Create the change (`new change <slug>`, or Kiro's own flow in `.kiro/specs/` when embedded) and work through requirements, design and tasks.
2. When implemented, merge the lasting facts into `10-context/` to `50-operations/` and the unit docs, add `traces`, then `verify` each affected section.
3. Deprecate any superseded spec as described above, run `index`, then `check`.

## Agent pointers (embedded)

Offer to add one line pointing to `<docs root>/README.md` in `AGENTS.md`, `CLAUDE.md` and a Kiro steering file. Ask before modifying any of these that already exist, and check whether they are generated from another source first; if so, change the source instead.

## Finishing a task

- [ ] Docs for every changed behavior updated, affected sections re-verified.
- [ ] Substantively changed or wrong specs deprecated, not deleted.
- [ ] `index` run; `check` reviewed and its findings reported to the user.
- [ ] Session journal logged and synced.
