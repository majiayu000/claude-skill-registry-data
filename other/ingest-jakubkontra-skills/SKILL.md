---
name: ingest
description: Gap analysis of a requirement against the current codebase and project memory. Takes a feature request, GitHub issue, PDF/document, or pasted email, breaks it into discrete capability requirements, and verdicts each as SUPPORTED / PARTIAL / MISSING with file:line evidence and memory citations, estimates effort for gaps, and offers follow-ups (spec proposal, memory write, memory bootstrap). Use when the user says "ingest", "/ingest", "can we already do this", "do we support this", "gap analysis", "assess this ticket/requirement", or pastes a requirement, issue number, or email and asks what the system already supports.
user-invocable: true
---

# Ingest - Requirement Gap Analysis

You analyze an incoming requirement ("can our system do X?") against what the codebase and project memory actually contain, and deliver an evidence-backed verdict per capability.

**Core principle: every verdict needs evidence.** SUPPORTED without a file:line reference you actually read is a guess, not a verdict. Write the report in the language the user is speaking (identifiers and file paths stay as-is). Use plain hyphens "-", never em-dashes.

## Phase 0: Detect project affordances

Run one parallel batch of cheap read-only checks and keep the results as a capability table. Everything downstream branches on it; a missing affordance means degradation, never failure (Grep/Glob/Read and Explore subagents always exist).

| Signal | Check | Enables |
|---|---|---|
| ariadne CLI | `command -v ariadne` | memory persistence (`remember`/`index`), bootstrap (`init`) |
| ariadne-code MCP | `mcp__ariadne-code__*` tools respond this session | semantic code navigation |
| ariadne configured, MCP down | `ariadne.config.json` at repo root, but tools absent/failing | suggest the user start it: `ariadne mcp` |
| code graph cache | `.ariadne/code-map.md` (+ `symbol-index.json`) at repo root | offline module/symbol routing |
| team memory | `docs/brain/` with README | memory recall + team-layer writes |
| personal memory | `${CLAUDE_CONFIG_DIR:-~/.claude}/projects/<flattened-cwd>/memory/MEMORY.md` | memory recall |
| spec workflow | `openspec/` dir or `openspec` CLI | spec-proposal follow-up |
| git + gh | `git rev-parse` + `gh auth status` | issue-number input |

## Phase 1: Normalize input

| Input shape | Action |
|---|---|
| Plain text / pasted email | Use as-is; for email strip headers, `>` quote blocks, and signature |
| `#123` or issue URL | `gh issue view <n> --json title,body,comments`; without gh, ask the user to paste the body |
| File path (.md, .txt, ...) | Read the file |
| PDF path | Read with `pages` (max 20 pages per request; chunk larger PDFs) |

Output: normalized requirement text plus a one-line provenance note for the report header.

## Phase 2: Extract requirements

- Split the text into discrete, individually verifiable capability statements R1..Rn ("The system can X") - one capability per item, no compound requirements.
- Separate constraints (deadlines, budget, non-functional wishes) - they are listed in the report but not verdicted.
- If there are more than ~10 requirements or the text is ambiguous, show the extracted list to the user for confirmation before verifying.

## Phase 3: Memory recall (before touching code)

If memory layers exist: read the personal `MEMORY.md` index (read-only - it is auto-generated, never edit it) and Grep the `description:` frontmatter lines of the team memory notes. Attach matching notes to requirements. Memory often decides PARTIAL vs SUPPORTED (e.g. "disabled in production") and carries incident context the code cannot show. Schema details: [references/memory-and-bootstrap.md](references/memory-and-bootstrap.md).

## Phase 4: Codebase verification

Pick the highest available rung (full guide: [references/verification.md](references/verification.md)):

1. **ariadne-code MCP live** - `search_code`/`find_symbol` to locate, `outline_file` to confirm, `who_calls`/`find_dependents` to prove the capability is wired end-to-end (guard with `dead_code`), `impact_of` to feed the effort estimate.
2. **Configured but down** - tell the user: "ariadne-code MCP is configured but not running - start it with `ariadne mcp` and I can navigate faster." Meanwhile route via `.ariadne/code-map.md` + `symbol-index.json`, then Grep/Read for evidence.
3. **No ariadne** - LSP tool if available, otherwise Grep/Glob + Read (language-agnostic).
4. **More than 5 requirements, or unfamiliar repo** - fan out parallel Explore subagents, one per requirement cluster, each returning verdict + file:line evidence.

Verdicts:
- **SUPPORTED** - an end-to-end path exists (data model + business logic + exposure surface such as API/UI), with evidence at every layer, and memory does not contradict it.
- **PARTIAL** - some layers exist, or a neighboring capability needs extension/config; state exactly what is missing.
- **MISSING** - nothing found after an honest search; state where the capability would live.

Evidence is always `path/to/file.ts:142`, verified by Read - never a bare grep hit or index entry.

## Phase 5: Verdict report

Render the report from [references/report-template.md](references/report-template.md): header (source, date, available tooling), summary, requirements table with verdict/evidence/gap estimate, detail sections only for PARTIAL/MISSING, constraints, next steps. Effort scale: S (up to half a day), M (0.5-2 days), L (2+ days or cross-module), always naming the affected modules.

## Phase 6: Follow-ups (always offer, never auto-execute)

1. **Spec proposal** for MISSING/PARTIAL items - if the project uses OpenSpec, offer to invoke the spec-proposal workflow; otherwise offer to write the gap up as an issue or design note.
2. **Persist findings to memory** - `ariadne remember "<fact>"` per notable finding, then `ariadne index`; without ariadne, write a note file by hand following the schema in [references/memory-and-bootstrap.md](references/memory-and-bootstrap.md).
3. **Memory bootstrap** - if Phase 0 found no memory system, offer to initialize one: `ariadne init` when the CLI is present (interactive - surface the prompt to the user, never pipe "y"), otherwise the minimal manual structure from the same reference.

## Decision flowchart

- Input is a number/URL? -> gh available? yes: `gh issue view`; no: ask for the pasted body.
- ariadne-code MCP tools respond? -> yes: semantic navigation; no but `ariadne.config.json` exists: suggest starting it + use the `.ariadne/` cache; neither: Grep/LSP/Explore.
- More than 5 requirements? -> parallel Explore subagents.
- Any MISSING/PARTIAL? -> offer the spec-proposal follow-up.
- No memory system? -> offer bootstrap.

## Navigation

- [references/verification.md](references/verification.md) - codebase-navigation tool ladder, verdict criteria, Explore prompt template
- [references/report-template.md](references/report-template.md) - report structure and effort scale
- [references/memory-and-bootstrap.md](references/memory-and-bootstrap.md) - memory schema, persistence commands, bootstrap

## Red Flags - STOP

- About to run `ariadne ingest` - STOP. That is a different, pre-existing command (vault raw-document ingestion), not this skill. Persistence uses `ariadne remember` / `ariadne new` / `ariadne index`.
- About to edit `MEMORY.md` - STOP. It is auto-generated; only `ariadne index` writes it.
- About to write SUPPORTED without a file:line you have Read - STOP. Verify or downgrade the verdict.
- About to auto-create a spec change or memory note without the user choosing that follow-up - STOP. Offer first.
- Report drifting into a language the user is not speaking - STOP. Paths and identifiers stay untranslated.
