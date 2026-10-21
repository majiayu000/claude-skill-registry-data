---
name: audit
description: Run a multi-category code audit on the cqs codebase. Spawns parallel agents per batch.
disable-model-invocation: true
argument-hint: "[batch-number|all]"
---

# Audit

Run the 16-category code audit.

## Implementation — the `audit` workflow (preferred)

The discovery + synthesis + disposition phases now run as one reusable workflow, `.claude/workflows/audit.js`:

```
Workflow({ name: 'audit', args: { churn: '<recently-changed areas to scrutinize>' } })
```

- **Discovery** — all 16 categories in ONE parallel stage (auditors return structured findings; no team, no 2-batch split — the concurrency cap schedules them).
- **Synthesize** — one agent dedups/clusters, triages P1–P4 (refining the deterministic difficulty×impact first-pass), assigns each row a disposition `route`, and WRITES `docs/audit-findings.md` + `docs/audit-triage.md`.
- **Disposition** — per row: `auto-fix` → generate a fix-spec + adversarially verify it against source; `issue` → draft a title+body; `tracked`/`inline`/`drop` → skip. Gen/verify/draft agents are **read-only** (`Explore`) so prepare-mode can't mutate the tree. `args.implement=true` additionally runs worktree-isolated implementers on verified fixes.

**The orchestrator (main loop) keeps the gated acts** — deliberately NOT in the workflow because they're irreversible / outward-facing / serialized to protected `main`:
- Review the triage — the cornerstone P1-vs-P2 + accept/reject/route-override call.
- `/land` the verified fixes (serialized, CI-gated).
- `gh issue create` the drafts, after dedup against open issues.

Route by **fix-nature, not tier**: a high-impact finding whose fix is a judgment call (architecture/API/perf-tradeoff) is `issue`, never `auto-fix`.

The team-based process below is the legacy reference — kept for the category scopes and the fix-prompt-review detail the workflow embodies. Teams are currently unavailable, so use the workflow.

## Arguments

- `$ARGUMENTS` — batch number (1-2) or `all` for full audit

**`all` means run BOTH batches** — all 16 categories. Run batch 1, then batch 2, then triage all findings together. Do NOT stop after batch 1.

## Batches

There are 16 categories split into 2 batches of 8. Each batch spawns 8 parallel agents (one per category). `all` runs both batches sequentially.

| Batch | Categories |
|-------|-----------|
| 1 | Code Quality, Documentation, API Design, Error Handling, Observability, Test Coverage (adversarial), Robustness, Scaling & Hardcoded Limits |
| 2 | Algorithm Correctness, Extensibility, Platform Behavior, Security, Data Safety, Performance, Resource Management, Test Coverage (happy path) |

## Process

### Setup

1. **Archive previous audit**: If `docs/audit-findings.md` or `docs/audit-triage.md` exist, rename both with the version suffix (e.g., `audit-findings-v0.9.1.md`, `audit-triage-v0.9.1.md`). Each audit starts with fresh files.

2. **Enable audit mode**: `cqs audit-mode on --expires 2h` — prevents stale notes from biasing review (no `-q` flag exists; the subcommand takes only `on`/`off` + `--expires`)

### Per-Batch

3. **Create team**: One team per batch (`audit-batch-N`)

4. **Spawn teammates**: One per category. Use `model: "fable"` for every auditor (per the 2026-06-11 model split: review/audit-finder lanes → fable) — the 2026-06-10 review/fix campaign showed Fable at or above opus quality on exactly this kind of judgment work (15/15 review findings confirmed, premise-drift catches, empirical hypothesis correction). Sonnet produces lower-quality judgments and haiku misses subtle findings. The per-category scope keeps each agent focused enough that frontier-model cost is reasonable.

   **Exception — the Security category auditor uses `model: "opus"`.** Fable's documented bug-finding gains explicitly exclude security-focused analysis (its cyber classifiers apply there), and benign-adjacent security work can occasionally trigger a classifier false positive — a mid-run refusal kills that category's coverage for the whole audit. Opus carries no refusal risk on this lane, has no documented capability deficit for it, and costs half. Same reasoning applies to `/boundary-probe`.

   **Nested-lead option for broad categories** (Code Quality, both Test Coverage categories, Performance, Data Safety): spawn the teammate as `subagent_type: "general-purpose"` (it needs the Agent tool) and have it (1) run the category's mandatory cqs commands itself, (2) fan out 3 read-only sub-scope agents in parallel (`subagent_type: "explorer"`, omit model so they inherit; HARD RULE in their prompts: no file writes — return candidate findings as their final message), (3) verify every candidate against the cited source + archived triages before appending, and report the candidate→appended funnel. Measured v1.42: 38 candidates → 31 appended (1 cross-category dup caught, 5 same-root-cause merges, 1 stale-triage reject); the two nested categories produced the largest verified hauls and the most P1s. Narrow/mined-out categories (Scaling found 1 finding in v1.42) stay single-agent — the lead overhead isn't worth it.

5. **Each teammate prompt must include**:
   - Their category scope (from table below)
   - Instruction to read archived triage files (e.g., `docs/audit-triage-v*.md`) — skip anything already triaged in prior audits
   - Instruction to read `docs/audit-findings.md` first — skip anything already reported by earlier batches in this audit
   - Instruction to append findings to `docs/audit-findings.md` **via bash heredoc append** (`cat >> docs/audit-findings.md <<'EOF' ... EOF`) — never Edit/Write on that file; 8 agents append concurrently and Edit fails with "file modified since read". This replaces the old per-category scratch-file + aggregation step: v1.42 ran 8 concurrent heredoc appenders with zero conflicts. (Initialize the findings file with a header before spawning so appends have a base.)
   - Format: `## [Category]\n\n#### [Finding title]\n- **Difficulty:** easy | medium | hard\n- **Location:** ...\n- **Description:** ...\n- **Suggested fix:** ...`
   - Use `subagent_type: "auditor"` when spawning — the auditor agent definition (`.claude/agents/auditor.md`) has cqs tools built in

6. **Shutdown team** after all agents complete

### After All Batches

7. **Triage**: Read `docs/audit-findings.md` in full, then classify:
   - P1: Easy + high impact → fix immediately
   - P2: Medium effort + high impact → fix in batch
   - P3: Easy + low impact → fix if time
   - P4: Hard or low impact → create issues for hard items; fix trivial ones inline (doc comments, one-liners, undocumented edge cases)
   - **Write triage to `docs/audit-triage.md`** — fresh file with P1-P4 tables (include Status column). This survives context compaction.
   - **Carry forward prior-triage open items**: read the most recent archived triage (`docs/audit-triage-v*.md`, honoring any verification section that supersedes its row statuses), reconcile against PRs merged since, spot-grep ambiguous items against main, and append the still-open entries as CF-P2/CF-P3 tables. The live `docs/audit-triage.md` must be the single source of truth for everything open — no hunting through archives.

8. **Generate fix prompts**: For each P1, P2, and P3 finding, spawn fable agents to (P4 trivials get prompts too; hard P4s get issue descriptions):
   - Read the actual source file at the stated line numbers
   - Write a self-contained fix prompt with: exact file path, current code verbatim, replacement code, one-line "why"
   - Group related findings (e.g., stale doc references) into a single prompt
   - Save to `docs/audit-fix-prompts.md`

9. **Review fix prompts**: Spawn a second fable agent to verify each prompt against the actual source:
   - Does the "current code" match what's really in the file? (catches line drift)
   - Does the fix compile? (check types, imports, API existence)
   - Are there any missing edge cases?
   - Report: "VERIFIED" or "NEEDS FIX — [specific issue]"
   - This step catches 20-40% of prompt errors (wrong field names, nonexistent APIs, moved code) — measured NEEDS-FIX rates: P1 42%, P2 41%, P3 16%

10. **Execute fixes**: P1 first, then P2. Dispatch `opus` implementer agents for the fixes (implementation lane); keep verification/review agents on fable. Mark each item in triage as fixed.

11. **Disable audit mode**: `cqs audit-mode off`

## Category Scopes

| Category | Covers (merged from) |
|----------|---------------------|
| Code Quality | Dead code, duplication, complexity, coupling, cohesion, module boundaries, **convenience wrappers that hardcode defaults** |
| Documentation | Accuracy, completeness, staleness of docs and comments |
| API Design | Consistency, ergonomics, naming, type design |
| Error Handling | Result chains, context, recovery, swallowed errors |
| Observability | Logging coverage, tracing, debuggability |
| Test Coverage (adversarial) | Edge-case/sad-path gaps: malformed input, NaN/Inf embeddings, concurrent access, empty queries, huge inputs, error paths not tested |
| Test Coverage (happy path) | Missing tests for high-caller public functions, untested modules, integration test gaps, meaningful assertion quality |
| Scaling & Hardcoded Limits | Constants that should scale with model config, corpus size, or hardware. Magic numbers without rationale. |
| Robustness | unwrap/expect, edge cases (empty/huge/unicode/malformed), panic paths |
| Algorithm Correctness | Off-by-one, boundary conditions, logic errors |
| Extensibility | Adding features without surgery, hardcoded values |
| Platform Behavior | OS differences, path handling, WSL quirks |
| Security | Injection, path traversal, file permissions, secrets, access control |
| Data Safety | Corruption, validation, migrations, races, deadlocks, thread safety |
| Performance | O(n²), unnecessary iterations, batching, caching, I/O patterns |
| Resource Management | Memory usage, startup time, idle cost, OOM protection, leaks |

## Mandatory First Steps per Category

Run these cqs commands **before** manual exploration — they surface the highest-value data in a single call.

**Batch 1:**
- **Code Quality**: Run `cqs dead --json` + `cqs health --json` first. Also grep for convenience wrappers that hardcode defaults (e.g., `fn foo()` that calls `foo_with_dim(HARDCODED)`) — these mask incorrect wiring when the default changes.
- **Documentation**: Run `cqs health --json` for staleness counts.
- **API Design**: No mandatory command.
- **Error Handling**: No mandatory command — grep-driven.
- **Observability**: No mandatory command — grep for `tracing::` patterns.
- **Test Coverage (adversarial)**: Run `cqs health --json` first (includes untested hotspots). Check for **adversarial test gaps**: functions that accept user input, external data, or embeddings should have tests for malformed/adversarial inputs (empty, NaN, truncated, wrong-type, concurrent).
- **Robustness**: No mandatory command — grep for `.unwrap()`, `.expect(`, `panic!`.
- **Scaling & Hardcoded Limits**: No mandatory command — grep-driven (const definitions, `.clamp(` sites, capacity/Duration literals, dim literals).

**Batch 2:**
- **Algorithm Correctness**: Use `cqs explain <fn> --json` on algorithmic functions.
- **Extensibility**: Run `cqs health --json` for hotspot overview.
- **Platform Behavior**: No mandatory command.
- **Security**: No mandatory command.
- **Data Safety**: No mandatory command.
- **Performance**: Run `cqs health --json` first (identifies hotspots).
- **Resource Management**: No mandatory command.
- **Test Coverage (happy path)**: Run `cqs health --json` first (includes untested hotspots).

## Rules

- Collect ALL findings before fixing ANY
- One batch at a time (context limits)
- Clean up teams between batches
- Stop at diminishing returns during discovery
- Once triaged, complete the tier — don't suggest stopping mid-priority
- Cross-check findings against open GitHub issues — note overlaps as "existing #NNN"
- **Mark items in `docs/audit-triage.md` as fixed when done** — update the Status column (e.g., `✅ PR #N` or `✅ fixed`). This is the source of truth for what's been addressed.
