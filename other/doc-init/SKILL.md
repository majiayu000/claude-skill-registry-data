---
name: doc-init
description: Establish or refresh project documentation coverage and install the global documentation lifecycle preset. Use for missing documentation structure, stale domain coverage, or a missing/outdated global documentation contract.
---

# Documentation system init (doc-init)

This skill runs in two phases: **repair the global standard first, then initialize the project's docs**. Both phases can write files. For an explicitly read-only audit, inspect and report proposed repairs without running the injector or writing project artifacts; do not claim installation or initialization completed.

Apply the installed `Project Documentation Management` lifecycle contract. This skill owns initialization procedures; environment instructions own language, permissions and shared-document locations.

`<DOC_INIT_DIR>` = directory containing this `SKILL.md` (resolve dynamically; do not hard-code absolute paths).

**Literal detection keys:** a few strings written into a project's root `AGENTS.md` are parsed by the scripts in this skill (and protected by `doc-compact`): the section headings `## 领域地图（doc-init）` (domain map), `## 待补充知识库（doc-init backlog）` (pending knowledge bases), `## 文档导航` (documentation navigation), the `覆盖度复核基线` (coverage-review baseline) stamp, and that map table's two column titles. Reproduce them **verbatim**, including full-width parentheses, whatever language the project's docs are written in—translating them silently breaks the coverage gate and the lint checks. Everything else (domain names, anchors, content summaries, body text) follows the project's documentation language.

---

## Built-in scripts cheat sheet

Prefer built-in scripts for mechanical work; keep model context for business judgment:

| Script | Purpose |
|------|------|
| `scripts/project_inventory.py` | Scan language stack, build files, submodules, docs, configs, entry candidates; emits candidate facts only—does not decide business domains |
| `scripts/doc_coverage.py` | Coverage gate: code function entries vs map-anchor match + fingerprint baseline; exit codes `COMPLETE(0)/STALE(2)/NEEDS_INIT(3)` |
| `scripts/upsert_agents_nav.py` | Idempotent add/update of root `AGENTS.md` document-content summaries |
| `scripts/doc_nav_lint.py` | Check root `AGENTS.md`, `CLAUDE.md`, `docs/` nav consistency |
| `scripts/db_miner.py` | Database catalog and domain-level table/field evidence mining |
| `scripts/git_history_miner.py` | Light Git-history weak-signal mining (hotspots, historical names, Q&A clues) |
| `scripts/depth_scanner.py` | Deep knowledge extraction: state machines, concurrency, idempotency, events, entity fields, etc. |
| `scripts/test_insert_doc_governance.py` | Before changing or deploying the injector: upgrade, boundary preservation and idempotence regression checks |
| `scripts/insert_doc_governance.py` | Version detect + auto insert/upgrade of the "Project Documentation Management" section in global AI instruction files |
| `scripts/discover_global_instruction_files.py` | List unique real paths of user-level instruction files (follows symlinks); exit `3` if none exist |

Script output is evidence and guardrails—it does not replace model judgment on business boundaries, canonical terms, KB/Guide granularity, or what to persist.

---

## Phase 1: Validate and repair global AI instruction files

### Step 1 — Locate the real global AI instruction files

Do not hand-roll a path probe. Run:

```bash
python3 <DOC_INIT_DIR>/scripts/discover_global_instruction_files.py
```

The script follows symlinks, de-duplicates real paths, and prints one path per line. Candidates (only those that exist are printed): `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.codex/instructions.md`, `~/.config/opencode/AGENTS.md`, `~/.agents/AGENTS.md`, `~/.config/agentsync/AGENTS.md`.

| Exit code | Meaning | Next action |
|-----------|---------|-------------|
| `0` | One or more files found | Process that printed list |
| `3` | None of the candidates exist | Report and ask the user for paths, then continue |

**Forbidden:** passing the current project's `AGENTS.md` to `insert_doc_governance.py`—only paths printed by the discover script (or paths the user explicitly names as their global instruction file).

### Step 2 — Script validate and auto insert/upgrade

For each real file:

```bash
python3 <DOC_INIT_DIR>/scripts/insert_doc_governance.py "<real path>"
```

| Output prefix | Meaning | Next action |
|----------|------|----------|
| `[skip]` | Already latest | Go to Step 3 |
| `[added]` / `[done]` | First insert succeeded | Go to Step 3 |
| `[upgrade]` / `[done]` | Old version replaced | Clean scattered old rules, then Step 3 |

After an upgrade, migrate only duplicate clauses explicitly identified in the current task's reviewed migration inventory. Preserve unrelated global content; never delete paragraphs merely because they mention documentation. The injector replaces its own block only.

### Step 3 — Phase 1 report

State which files were processed, each script’s output, and which scattered old content was cleaned (if any).

---

## Phase 2: Initialize the current project’s documentation system

**Before Phase 2 starts, read** `references/knowledge-network-design.md` and use it to control doc granularity, naming, KB/Guide boundaries, and budget-limited behavior.

### Step 6 — Decide: init / continue / review

The sole completion anchor is the root `AGENTS.md` section `## 领域地图（doc-init）` (domain map; literal detection key):

1. **Map section present** → read it, enter Step 6.5 coverage review; **forbidden** to exit just because “already exists / all Generated / no backlog.”
2. **Map section absent** → whether or not `docs/` is non-empty, treat as **init incomplete**, enter Step 7/8; when building the map, reuse existing docs—do not rewrite.

If root already has `AGENTS.md`, you may run an auxiliary check (reference only):

```bash
python3 <DOC_INIT_DIR>/scripts/doc_nav_lint.py --root .
```

### Step 6.5 — Coverage review (mandatory when map exists)

Whether to finish is decided by `doc_coverage.py` exit codes—models must not self-claim “coverage is roughly fine”:

```bash
python3 <DOC_INIT_DIR>/scripts/project_inventory.py --root . --output .doc-init-project-inventory.json
python3 <DOC_INIT_DIR>/scripts/doc_coverage.py --root . --inventory .doc-init-project-inventory.json
```

| Exit code | Meaning | Action |
|--------|------|------|
| `3 NEEDS_INIT` | No real map section | Back to Step 6 judgment 2; full init |
| `0 COMPLETE` | Anchor coverage OK, no significant growth | Write the script-suggested baseline stamp back into the map section; tell the user “docs cover current code; use doc-update for incremental fills” and exit |
| `2 STALE` | Under-covered / new function areas / large code growth / no baseline stamp | **Not complete**; enter follow-up below |

**After STALE** (details in `references/scan-and-boundary-report.md` “Coverage review”):

1. Uncovered function areas → filter via product north star (Step 7a): real features join the map; dead code / implementation drift → pending discoveries.
2. Large code growth / no baseline stamp → drift spot-check on `Generated` domains; clear drift demotes to `Deep-write this session`; minor diffs → doc-update.
3. Return to Step 7a → Step 8/9 deep-write this batch; do not re-scan `Generated` domains confirmed still accurate.

Default thresholds: `--min-coverage 0.85`, `--max-uncovered-area-entries 3`, `--max-growth-pct 0.25`. When entry-sparse pure libraries/scaffolding are judged STALE, manually read the uncovered list to confirm—do not lower thresholds to bypass the gate.

### Step 7 — Product north star first + collaborative Intake

Read `references/human-intake.md`.

**Step 7a: Establish product north star first**—follow `human-intake.md` “Product north star first” (① project AGENTS.md product pointers → ② PRD/roadmap → ③ ask the user → ④ hard stop).

**After confirming truth, fix conflicting docs in-place:** if truth established at any stage conflicts with existing `docs/`, correct them in the same session—do not leave two contradictory conclusions. Adjudication, anti-thrashing, and propagation: `references/conflict-resolution.md`.

**Step 7b: Collaborative Intake.** Unless the user explicitly forbids questions, do light Intake (material entry points, business naming, runtime validation entry points, veteran experience). If questions are forbidden, skip and mark “Missing user experience input” in self-assessment.

**Step 7c: Cross-project tech-standard reference check.** Read the real global AI instruction files (located in Step 1) for a declared location of “cross-project tech standard docs” (a public standards directory organized by language/stack; location and directory name vary by user—do not assume a fixed path; if undeclared, skip this step and do not invent paths). When declared:

1. Under the declared location, find matching standard docs for this project’s primary language/stack.
2. If found and project-root `AGENTS.md` does not yet reference them → add a reference near the top (after product intro, before body sections), matching the usage style already used at the declared location (e.g. `Shared engineering standards: [Go standards](<relative path>/go.md)`), adjusting relative paths to this project’s directory depth.
3. If the project spans multiple stacks (e.g. backend + mobile) → one link per matched standard doc, separated by `·` on the same line.

### Step 8 — Scan the project and output the full domain map + knowledge-boundary report

Read `references/scan-and-boundary-report.md`.

**Deliverable order: product north-star summary → complete domain map → per-domain detailed reports.**

**Before building the map, inventory existing docs:** cross-check `docs/` and existing root `AGENTS.md` nav; domains already covered mark “Generated (reuse existing)”—do not rewrite; update only when content is clearly stale or conflicts with current code/product truth.

**Hard constraints on domain partitioning** (see `references/knowledge-network-design.md` “Business domain ≠ code module”):

- Domain = business concept, not submodule/directory name
- One KB covers that business domain’s entries across modules (config/execution/entity/API)
- When one module holds multiple independent business objects, split into separate KBs

**Scripts (in order):**

```bash
# At Step 8 start, run in parallel
python3 <DOC_INIT_DIR>/scripts/project_inventory.py --root . --output .doc-init-project-inventory.json
python3 <DOC_INIT_DIR>/scripts/git_history_miner.py --root . --output .doc-init-git-history.json

# After inventory completes
python3 <DOC_INIT_DIR>/scripts/depth_scanner.py --root . --inventory .doc-init-project-inventory.json --output .doc-init-depth-scan.json
```

Read `references/depth-patterns.md` and turn depth_scanner mechanical signals into per-domain knowledge candidates (see that file’s signal→KB section mapping). Discard false positives—do not copy mechanically.

If the environment supports parallelism and the user has not restricted it, candidate-domain code-entry exploration may run concurrently; assign each worker boundaries by business domain (not by module).

After identifying the language stack, read matching docs under `references/hidden-semantics/` as needed (language list in `references/scan-and-boundary-report.md` “Language stacks and hidden semantics”).

Read `references/multi-source-evidence.md` and, with inventory `evidence_sources`, do light multi-source discovery; deep digs center on candidate business domains—not a full deep dig in this step.

### Step 8.5 — Database evidence mining (optional enrichment)

If the project has DB config, or candidate domains clearly depend on DB facts (status, money, balances, sharding, flows, dicts, etc.), read `references/database-mining/workflow.md` and use `scripts/db_miner.py` for a light catalog.

This stage only: table list, field list, PK/indexes and comments—no full-DB count/distinct/profile/sample-table. Afterward you may call `db_miner.py summarize-catalog` for a directory-level summary (local JSON only; no DB connection).

If connection is missing or the user forbids it, mark “Missing real data semantics” in the knowledge-boundary report and self-assessment.

### Step 8.7 — Confirm domain boundaries and priorities

Show the complete map once: covered domains, this batch with reasons, and backlog with entry anchors. Ask only about unresolved boundaries or priorities that materially change the work; use existing product decisions and user answers first. Do not ask permission to scan, repeatedly confirm each KB, or re-ask an accepted choice.

Apply requested adjustments and continue. If optional feedback is unavailable, proceed with stated assumptions; unresolved product-definition requirements still follow Step 7a's gate.

### Step 9 — Targeted Q&A and doc generation

Read precise Q&A rules in `references/human-intake.md`; read `references/document-templates.md`.

**Timing constraints (strict order):**

1. **Q&A before dispatch:** Complete one concentrated Q&A round for all domains in this deep-write batch (unless the user forbids questions). Focus on what code cannot show but affects correct implementation (business peaks, failure patterns, approval flows, historical conventions).
2. **Work planning:** Read `references/sub-agent-prompt-template.md`; for each deep-write domain assemble a structured work brief (domain definition + entry inventory + depth_scanner signals + canonical terms + Q&A results + quality gates). A vague “deep-write domain X” brief is insufficient.
3. **Dispatch work** (if supported and main batch ≥ 2 domains): weakly coupled domains may run in parallel; if domain A depends on domain B’s shared mechanism, serialize.
4. **Aggregation** (the coordinator completes after assigned work returns):
   - Shared-mechanism extraction check: same mechanism described in ≥ 2 KBs → decide whether to extract a `*_GUIDE.md`
   - Cross-reference alignment: each KB §8 references cross-domain relations
   - Canonical-term consistency: same concept uses the same canonical term across KBs
   - Ops cheat-sheet merge: multi-host module projects enumerate ports one by one

**Root file boundary:** workers must not modify root `AGENTS.md`; the coordinator hands the complete, bounded set of root-file edits to the `agents-md-edit` skill once after the domain map, navigation summaries, backlog, and operational notes are ready. Do not create one handoff per navigation entry. The coordinator integrates and verifies the result. If `agents-md-edit` is unavailable, report the missing capability and leave the root file unmodified.

**Generate docs** (per domain in this deep-write main batch):

- `docs/<DOMAIN>_KNOWLEDGE_BASE.md` (DOMAIN must be a business concept name—not a module name)
- `docs/<TOPIC>_GUIDE.md` (only extract shared horizontal mechanisms; threshold in `knowledge-network-design.md`)
- Project-root `AGENTS.md` (route deliberate edits through the dedicated `agents-md-edit` skill; use it once for the bounded root-file update, then let the coordinator integrate and verify the result. If unavailable, report the missing capability rather than editing the file directly.)
- Project-root `CLAUDE.md` (single line `@AGENTS.md` only)

**Deep-write standards and quality gates:** `references/document-templates.md` “Deep-write standards”; after each KB, immediately self-check against quality gates and backfill if unmet.

**Prepare root `AGENTS.md` navigation summaries** (collect them while generating docs; apply them in the single `agents-md-edit` handoff after the complete root update is ready):

```bash
python3 <DOC_INIT_DIR>/scripts/upsert_agents_nav.py --root . --path docs/<DOMAIN>_KNOWLEDGE_BASE.md --summary "<concise summary of the document content>"
```

The `AGENTS.md` document navigation has one shared instruction to read documents whose described content is relevant to the current task. The helper preserves an existing equivalent instruction and adds the default only when none is present. Entries are concise descriptions of actual document content, not trigger lists or duplicated policy. `--when-to-read` remains a backward-compatible alias for `--summary`; both have the same content-summary meaning. The designated `agents-md-edit` writer runs the helper; it does not infer or rewrite document facts. It recognizes `## 文档导航`, `## 规则索引`, `## Document index`, and `## Documentation index` without creating a competing section.

**Prepare backlog registration** (after the main batch, include all pending domains in the single `agents-md-edit` handoff—never silently drop):

```bash
python3 <DOC_INIT_DIR>/scripts/upsert_agents_nav.py \
  --root . --backlog \
  --name "<domain> KB" \
  --anchor "<entry dir>" \
  --summary "<content covered by the planned document>"
```

**Persist the domain map** (**mandatory**, even when this session fully covered everything):

Write the complete domain map into root `AGENTS.md` `## 领域地图（doc-init）`. This section **only serves the `doc_coverage.py` coverage gate**—do not duplicate paths and content summaries already in doc navigation.

Format: baseline stamp + two-column table (domain | entry anchors); **forbidden** process-metadata columns like “Status” or “Notes”—“Generated / Deep-write this session / To be filled” has no value for later work models; doc paths are already registered in doc nav.

The heading, the baseline-stamp comment, and the two column titles are literal detection keys (see “Literal detection keys” above): copy them exactly as shown. Domain names and anchors are free text in the project’s doc language.

```markdown
## 领域地图（doc-init）

<!-- 覆盖度复核基线：2026-06-21 · 源码指纹 扫描 1573 文件 / Go 412 · TS 88 / 11 子模块 · 基线提交 a1b2c3d -->

| 领域 | 入口锚点 |
|------|---------|
| Channel system | src/channels/ |
| Agent execution loop | src/agents/ |
| Plugin system | src/plugins/ |
```

Simplest way to get the stamp right: `doc_coverage.py` prints a ready-to-paste `suggested_stamp` for the current tree—copy that line instead of hand-writing it. Its values come from inventory (`scan.scanned_files`, each `languages[].file_count`, `submodules` count) plus `git rev-parse --short HEAD`. Domains registered in the map section must match domains covered by doc nav (the map section does not register backlog—backlog is managed via `upsert_agents_nav.py --backlog`).

**Conditional ops cheat sheet:** If depth_scanner `runnable_project.type` is not `library/cli/unknown`, generate an “Ops cheat sheet” section in root AGENTS.md (format in `document-templates.md`). Multi-host module projects must list every submodule with `spring-boot-maven-plugin`/`mainClass` and its port.

### Step 10 — Runtime validation and conditional Operations generation

Only when the project has local-run value, read `references/operations-validation.md`.

Route runtime-validation evidence by semantics: start commands / health / config / log paths → `OPERATIONS_GUIDE.md`; real business API behavior / state changes / error codes → corresponding domain KB; cross-domain shared mechanisms → `*_GUIDE.md`.

Generation conditions:

- At least one reusable runtime experience or start blocker → create or update `docs/OPERATIONS_GUIDE.md`
- Validation not executed but the project has a runtime surface → only a thin “runtime hypotheses and pending validation list”
- No local runtime surface → do not generate; put validation method in root `AGENTS.md`

### Step 11 — Self-assessment report

Report batch completion separately from project-wide coverage, backlog count and unverified evidence. Finishing the agreed batch does not mean the whole project is fully documented.

First run doc-nav consistency check:

```bash
python3 <DOC_INIT_DIR>/scripts/doc_nav_lint.py --root .
```

Include lint errors/warnings in self-assessment. Fix errors before reporting complete.

**Coverage ledger (must give numbers):**

- Domain-map total N = Generated (reuse) A + Deep-write this session M + Candidate dead code/drift D + backlog B
- Assert: A + M + D + B = N ✓ (if not, silent domain drop—must backfill backlog)
- Assert: root `AGENTS.md` `## 领域地图（doc-init）` is written and matches the ledger ✓
- Assert: map section has a “coverage-review baseline” stamp ✓

**If Step 6.5 ran**, also output the coverage-review ledger (G gaps + R stale needing refresh; only G + R == 0 may be judged truly complete).

Self-assessment must also cover (item by item—not one vague paragraph):

- Per-KB deep-write quality-gate pass/fail (§2/§3/§4/§6/§7 meet minima; if not, reason and remediation)
- depth_scanner signal utilization (how many signals out, how many written into KBs, how many discarded and why)
- Domain-language coverage (canonical terms unified? unresolved homonyms?)
- Git weak-signal coverage (available? hotspots and fix/revert clues only as pending candidates?)
- Database evidence coverage (connected? which domains catalogued? which key tables unanalyzed?)
- Multi-source evidence coverage (which sources available, which dug, which high-value missing)
- High-risk uncovered items (concepts undisambiguated, status flows unclear, mechanism effect conditions unclear, validation paths missing)
- Operations validation coverage (which steps executed; which remain low-confidence hypotheses)
- Follow-up persistence suggestions (what doc-update should fill; what suits doc-compact)

### Step 12 — Close or offer concrete remaining work

After verification, report completion of the agreed batch and any evidence-backed gaps. Offer further investigation only where real findings justify it; there is no minimum number of proposals and no repeat-until-stopped loop. User-selected independent directions may run in parallel; serialize dependencies and update the map, backlog and navigation after each accepted batch.
