---
name: doc-auditor
description: Analyze a codebase to discover documentation gaps in README.md and docs/ directories, then generate or update missing documentation. Use when the user asks to (1) audit README/docs for missing coverage, (2) find undocumented features or modules, (3) fill documentation gaps, (4) update docs to match current code, (5) generate a doc-gap report, (6) "문서 누락 분석", "README/_docs_ 감사", "문서 보완", "docs gap audit", "undocumented features". Triggers on any request to compare codebase structure against existing documentation and produce a gap analysis or fill the gaps.
---

# Doc Auditor

Audit a codebase against its README.md and docs/ to find missing coverage, then generate or update documentation to close the gaps.

## Workflow

### Step 1 — Inventory the codebase

Run the analysis script to produce a machine-readable feature inventory:

```bash
python3 .agents/skills/doc-auditor/scripts/audit.py . --output .libragent/tmp/doc-audit.json
```

The script discovers:

- Frontend features (`src/features/*/`)
- Frontend lib modules (`src/lib/*/` and `*.ts`)
- Backend modules (`src-tauri/src/*/` and `*.rs`)
- Existing documentation (`README*`, `docs/**`)
- Benchmark directories (`*bench*`)

### Step 2 — Review the gap report

Read `.libragent/tmp/doc-audit.json` and review discovered gaps:

- **P0 gaps (Must fix)**: User-facing features/services with zero documentation (e.g., `scheduled-tasks`, `history`, `browser-sidecar`, `session-export`)
- **P1 gaps (Should fix)**: Features with internal/architecture specs but missing user guides (e.g., `knowledge`, `session-isolation`)
- **P2 gaps (Nice to have)**: Schema, validator, execution mode, or system protocol modules needing implementation docs (e.g., `db-schema-validator`, `execution-mode`)
- **P3 / Internal (Low impact)**: Internal utilities, shared helpers, test infrastructure (skipped or marked low priority)

### Step 3 — Prioritize and plan

Use this priority framework:

| Priority              | Criteria                                          | Example                                                               |
| --------------------- | ------------------------------------------------- | --------------------------------------------------------------------- |
| **P0 — Must fix**     | User-facing feature with zero docs                | `scheduled-tasks/`, `history/`, `browser_sidecar/`, `session_export/` |
| **P1 — Should fix**   | Documented internally/arch but missing user guide | `knowledge/`, `session_isolation/`                                    |
| **P2 — Nice to have** | System/spec modules needing architecture docs     | `db_schema_validator`, `execution_mode`                               |
| **P3 — Low impact**   | Internal helpers, test code, generated files      | `utils/`, `performance/`, `mime-utils`                                |

### Step 4 — Propose plan and obtain user approval

> [!IMPORTANT]
> **Git Protection Rule (`AGENTS.md`)**: `docs/`, `src/`, `src-tauri/`, and `README*.md` are git-protected directories.
> **DO NOT** modify or create files in these directories without explicit user confirmation.
>
> 1. Present the list of missing docs to create/update.
> 2. Propose draft file paths and outline content.
> 3. Ask the user for confirmation before writing protected files.

**Target locations for new docs:**

- User guides → `docs/user/guides/<feature>.md`
- Architecture & technical specs → `docs/architecture/<topic>.md`
- API reference → `docs/api/<module>.md`

**Target locations for index updates:**

- `docs/README.md` — add links to new guides/specs
- `docs/user/README.md` — add to the user docs index
- `README.md` — add feature descriptions and scenario references

### Step 5 — Validate and report

After writing docs, run lightweight validation on modified files:

```bash
# Verify formatting and markdown structure (DO NOT run heavy full pipelines like `pnpm refactor:validate` unless explicitly requested)
pnpm lint:format
```

Report results in a summary table:
| File | Status | Lines | Coverage Category |
|------|--------|-------|-------------------|
| `docs/user/guides/scheduled-tasks.md` | Created | 180 | P0 (New Guide) |
| `docs/architecture/db-schema-validator.md` | Created | 120 | P2 (Spec) |
| `docs/user/README.md` | Updated | 45 | Index Link |

## Guidelines

- **Respect Git Protection (`AGENTS.md`)**: Always get explicit user confirmation before writing to `docs/` or `README.md`.
- **KISS & Resource Protection (`GEMINI.md`)**: Keep documentation concise and action-oriented. Never execute heavy full pipelines like `pnpm refactor:validate` for markdown edits unless explicitly requested by the user.
- **Evidence-based**: Reference actual file paths, CLI flags, and module names.
- **Don't document the obvious**: Skip self-explanatory internal helpers (e.g., `date-utils.ts`, `mime-utils.ts`).
- **Update indexes**: Every new doc must be linked from `docs/README.md` and `docs/user/README.md`.
