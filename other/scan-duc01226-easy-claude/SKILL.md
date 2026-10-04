---
name: scan
version: 1.0.0
description: '[Documentation] Use when a workflow step or the user asks for one project-reference doc to be regenerated. --target=<doc key> (project-structure, code-review-rules, domain-entities, docs-index). All docs: scan-all.'
---

## Quick Summary

**Goal:** Scan one selected built-in or explicitly generic custom reference doc and deliver a surgical, evidence-backed update that preserves action-changing rules, exceptions and verified discovery without report bulk.

**Summary:**

- **Purpose:** Run one selected, applicable manifest target; its entry owns the output doc, capability evidence, detection, agents, sections, exceptions, and enhancement requirements.
- **Ordered path:** Resolve optional config and selection → applicability → owner scan → candidate/retention review → enhance + final quality gate → baseline/no-op check and application → report.
- **Modes/gates:** Init/Sync and target-defined Force; `kind: orchestrator` uses its procedure; unknown key STOPs; unsupported capability is a reported skip, not a guessed fallback.
- **Evidence:** Use real `file:line` examples, incremental unique reports, surgical writes, all-path/name checks, target exceptions, and graph checks when the project supports them.

**Workflow:**

1. **Validate** — Resolve optional config; validate declared sections and derive missing facts from repository evidence.
2. **Resolve** — Parse `--target=<key>`, load its manifest entry, and confirm the output is selected or separately owned as an always-on input.
3. **Assess** — Check capability evidence before running target-specific Phase 0 detection.
4. **Scan** — Run only applicable declared work; capture authority and evidence in the temporary report.
5. **Write** — Build a candidate; verify its claims, semantic coverage and consumer contracts.
6. **Enhance + discovery gate** — Before applying a changed candidate: `/prompt-enhance`, then the AI-discovery gate (purpose + critical rules on top, reminders at the bottom when long, trigger-based pointers to existing docs, reachable from the docs index).
7. **Report** — Persist findings and return complete, unchanged, skipped, or blocked status with evidence.

**Key Rules:**

**MUST ATTENTION** resolve `--target` FIRST; the manifest entry owns all target-specific behavior, never memory.
**MUST ATTENTION** validate config and target applicability before scanning; a catalog entry is not proof the project uses that capability.
**MUST ATTENTION** detect framework/type only after applicability is established; derive scan terms and scopes from evidence, never hardcode.
**MUST ATTENTION** use actual project examples with `file:line` — NEVER fabricate.
**MUST ATTENTION** treat graph output as an optional, stale-able hint for code relationships (source callers remain the evidence); an absent graph is not a scan failure.

- Update affected sections; preserve meaningful guidance and parser contracts; disposition removed redundancy or outside-purpose material.
- Honor target-entry Content Rules/exceptions and Special slivers, including target-specific branches.

---

# Scan (parameterized reference-doc scanner)

## Phase 0.0: Resolve Target (BLOCKING — do this before anything else)

1. Parse `--target=<key>` from the invocation (e.g. `/scan --target=backend-patterns`). Built-in keys use their manifest entry. The reserved `generic-reference-doc` mode also requires `--filename="<relative-path>"`. If no target or an unknown key is supplied, STOP and list registered keys; never guess the intended target.
2. **Validate project config.** Resolve the configured config path through `.claude/hooks/lib/project-config-loader.cjs` (default `docs/project-config.json`). Absent config is supported: use the runtime capability resolver and repository evidence. Present config requires a non-empty `project.name`; omitted sections use neutral defaults/skips. Repair declared invalid sections through `project-init` / `project-config` before relying on them.
3. **Resolve output selection.** Read the effective `referenceDocs` selection through the project config/runtime resolver. An explicit array, including `[]`, is exact for task-specific docs. A built-in target may write only its manifest `doc` when that exact filename is selected. `generic-reference-doc` may write only the exact selected custom filename whose `scanTarget` is `generic`; a missing/`manual` target or unselected filename blocks the scan. Custom docs never inherit a built-in target by basename. The `lessons.md` and docs-index inputs are ensured by project-init separately from task-specific selection.
4. **Read `references/targets.md` (registry index: selection rules, path roots, key → file table), then the resolved target's own file `references/targets/<key>.md` — MANDATORY; the index carries no scan data and no other target file is needed.** `generic-reference-doc` uses the index's Dynamic Target section instead of a target file. The target file supplies:
   - `doc` — the reference doc path this scan owns
   - applicability and skip evidence
   - description, sub-agent roles, Phase 0 detection, Think scopes, sections, content rules, exceptions, special slivers, anti-rationalization, and enhancement requirements
5. **Check applicability before scanning.** Verify the capability from relevant config plus repository evidence. Config may select or point to search locations, but does not prove that a code pattern exists. If evidence shows the capability is absent, report `SKIPPED` with the config fields and paths checked and write nothing. If evidence conflicts materially, stop and surface the conflict.
6. **Orchestrator branch:** if the entry is `kind: orchestrator`, follow its applicability-aware procedure and include only eligible children. Do not run the shared single-doc engine for the orchestrator.

> Everything below is the SHARED engine (standard single-doc scanner targets). Wherever it says "the target entry," read the loaded manifest entry — do not assume values from another target. **Orchestrator-kind targets do not use this engine** — they run their entry's Orchestration Procedure instead.

## Phase 0: Classify & Assess

After config, output selection, and applicability pass, run only the checks relevant to this target:

1. Read the target's `doc`.
   - Detect mode: **Init** (placeholder — headings only / sentinel present) or **Sync** (populated). Some targets add a **Force** mode (user says "rebuild"/"reset" → treat as Init even if the doc exists) — honor it if the target entry defines it.
   - Save the exact baseline (or record absence) in the unique temporary report directory. Classify full owner scan, impact-scoped verification or editorial rewrite under `scan-and-update-reference-doc`; existing sections are not evidence that their owners were checked.
2. Run the target entry's **Phase 0 detection** table(s) only for the evidenced capability. For a generic custom doc, derive evidence and search scope from its configured purpose and sections, then verify against repository sources without assuming a stack, architecture, or test convention. Derive patterns from source, manifests, test config, or documentation; a framework name in config is a search hint to verify, not permission to invent usage.
3. Load only relevant configured paths and profiles, and validate every declared section the scan consumes. Omitted optional properties mean neutral defaults or a skipped branch; a declared malformed property blocks the scan.
4. For code-oriented targets, trace relevant files with the project graph only when `.code-graph/graph.db` and the graph tool are available.

**Evidence gate:** If applicability or framework detection cannot be established, report what was checked and what remains unknown. Skip absent capabilities; ask only when unresolved evidence materially changes the doc and cannot be settled from config or source. Never substitute a guessed manifest fallback.

## Phase 1: Plan Scan Strategy

From the evidenced framework/type, derive concrete patterns to search (naming, lifecycle, data access, configuration, and test organization). Treat architecture patterns such as repositories, CQRS, events, or domain entities as options to evaluate against observed boundaries, not mandatory structures.

Read the shared `ai-discovery-doc-quality` content-value contract before drafting. Record authoritative owners and exemplar preconditions; distinguish intended practice from legacy frequency. Bound exploration by selected owner scope and relevant consumers, use live registries, and record unknowns rather than exhaustive inventories. Create work items only for applicable branches. When delegation is authorized, assign disjoint source scopes and reconcile their union, including boundary files, before dispatch; the main agent owns output writes.

## Phase 2: Execute Scan (Parallel Sub-Agents)

Launch only the general-purpose sub-agents defined for applicable branches in the target entry. Give each sub-agent its **Think scope** + scan-target bullets verbatim from the entry. Each sub-agent MUST:

- Write findings incrementally after each file/section — NEVER batch at end
- Cite `file:line` for every pattern example
- Confidence: >80% document with authority/preconditions; 60-80% label unresolved observations, never required practice; <60% omit or report a material unknown

Each worker writes a **unique shard** under `tmp/reports/scan-{target}-{YYMMDD}-{HHMM}/`; workers never append to the same report. After the barrier, the main agent reads and validates every shard and is the **sole writer** of `tmp/reports/scan-{target}-{YYMMDD}-{HHMM}-report.md`.

> Honor every **conditional / ordered** sub-agent from the entry (for example, cross-service work only when service boundaries exist, or a BDD agent only when BDD artifacts are present). Honor any **CRITICAL security flag** the entry defines. Never create extra architecture or test components to fill a section.

## Phase 3: Analyze & Generate

Read the full report. Apply the fresh-eyes protocol:

**Round 1 (main agent):** Build section drafts from report findings, using the target entry's **Target Sections** + **Content Rules / exceptions**.

**Round 2 (only after Round 1 finds and fixes issues; fresh sub-agent, zero memory of Round 1):** Sub-agent re-reads report + draft doc independently and checks (apply the target entry's Round-2 verification specifics):

- Does every code example match an actual existing file (Glob verify)?
- Do class/token/variable names in examples match actual declarations (Grep verify)?
- Do consumer-required sections retain valid syntax/data? Unsupported sections are omitted or explicitly dispositioned, not filled to satisfy a heading.
- Does each section improve an action or discovery decision? Check exceptions, rationale and exemplar fit; put audit/coverage evidence in the report unless needed for action or required by the local owner.

**Round 3 only if Round 2 finds issues.** Max 3 rounds → escalate to user if unresolved. (Clean Round 1 ends the scan; fresh-eyes is mandatory only after issues are found and fixed.)

> **Authoring branch (init mode):** if the target entry defines one (e.g. `design-system` authors the canonical doc + token `.scss`), follow it exactly — including any **sentinel removal** (e.g. "First: REMOVE `PLACEHOLDER_MARKER_SCSS`") and regen-marker prepend.

## Phase 4: Write & Verify

1. **[BLOCKING] No-op scans write NOTHING — not even the stamp.** Finish enhancement and semantic review on the full candidate before application; choose freshness metadata according to the classified operation, then compare it against the doc on disk with the shared guard, which ignores volatile stamps and whitespace:

   ```bash
   node .claude/hooks/lib/doc-stamp-guard.cjs --check <target doc> --candidate <candidate file> --baseline <baseline file>
   ```

   - **Exit 4 (CONFLICT)** → preserve candidate/live baseline, reconcile newer guidance and repeat semantic/discovery checks before retrying. Single main writer applies immediately after the check; it is optimistic detection, not locking.
   - **Exit 0 (CHANGED)** → write the fully reviewed candidate with truthful operation metadata.
   - **Exit 3 (NO-OP)** → do **NOT** write the file, do **NOT** touch the stamp. Only after a full owner scan, record verification in the local ledger; impact/editorial work preserves full-scan staleness:

     ```bash
     node .claude/hooks/lib/doc-stamp-guard.cjs --record-verified <doc filename>
     ```

     Then report `unchanged (no write)`. — why: a date-only rewrite is an unmergeable line at the top of a file many branches touch, so two branches that each merely RE-RAN this scan conflict over a date neither of them decided. The churn carries no information and costs a manual merge.

2. Apply only affected guidance; preserve manual annotations and meaningful local rules. Remove redundant/outside-purpose sections with semantic dispositions, preserving parser-owned structures. Never use a pointer that cannot deliver the rule when needed.
3. Verify (Glob check): **ALL** code example file paths exist — not just a sample of 5.
4. Verify (Grep check): class/token/variable names in examples match actual declarations.
5. Verify any target-mandated section is real, not hypothetical (Anti-Patterns / Coverage gaps / M1-M2 leaks / ports-from-config / etc.).
6. For code-oriented claims, validate call-chain or dependency claims with the available project graph; when no supported graph exists, trace relevant source callers directly.
7. **Convention classes (main agent only, never a worker):** when the valid project config declares convention classes, follow their configured additive merge procedure. Omitted optional convention configuration is a skip; do not create classes from guessed stack facts. Workers keep writing only their unique shard; the main agent stays the sole writer.
8. Report: sections updated / unchanged / coverage gaps / violations found / convention classes added-refreshed-kept.

> **Output-rule overrides:** apply the target entry's "Content Rules / exceptions" — owner-required index rows/counts/anchors remain intact; contractual thresholds/versions remain actionable. Detailed statistics and coverage reports stay in temporary evidence unless they govern action or a consumer requires them.

<!-- SCAN:prompt-enhance-final-step -->

## Final Step: Enhance Scanned Doc (MANDATORY — before Phase 4 application)

**MUST ATTENTION** for a changed candidate, run `/prompt-enhance` with the target output identity and its ownership contract before application when required by the manifest. Use its agent-guide branch; compare final semantic dispositions against the baseline so enhancement cannot restore removed bulk. A skipped or unchanged target is not rewritten or enhanced.

**TaskCreate (last task when a doc changed):** `Enhance candidate and review semantic retention before applying <target doc>`

**Then run the AI-discovery gate (`SYNC:ai-discovery-doc-quality`) on the enhanced doc:** first screen states purpose, when to read it and its critical rules · a long or rule-bearing doc ends with closing reminders · every pointer to another doc is `read <path> when <situation>` with an existing target · the doc is reachable from the docs index (a missing route is reported for the `docs-index` target, not patched here). Fix a failure inside this doc before reporting; the gate includes the shared content-value/retention review and never widens rewrite authority.

<!-- /SCAN:prompt-enhance-final-step -->

---

> **[IMPORTANT]** Use small tracked tasks for multi-phase or delegated scans. Do not ask whether to skip a clear one-target scan.

**Prerequisites:** **MUST ATTENTION READ** before executing:

<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `ai-discovery-doc-quality` — Agent-guide content value, authority, retention and verified discovery; writing a doc that an agent reads → .claude/skills/shared/protocols/ai-discovery-doc-quality.md
- `output-quality-principles` — Useful, readable guidance without lost conditions; writing generated docs or reports → .claude/skills/shared/protocols/output-quality-principles.md
- `scan-and-update-reference-doc` — Baseline-safe updates with semantic retention and truthful freshness; scanning or updating a reference doc → .claude/skills/shared/protocols/scan-and-update-reference-doc.md

<!-- PROTOCOL-GUIDES:END -->

<!-- SYNC:scan-and-update-reference-doc:reminder -->

**IMPORTANT MUST ATTENTION** read/save baseline, classify full/impact/editorial operation, preserve semantic dispositions and manual guidance, reject/reconcile changed live bytes before application. No-op writes nothing; only full owner scans advance full-scan freshness.

<!-- /SYNC:scan-and-update-reference-doc:reminder -->

<!-- SYNC:output-quality-principles:reminder -->

**IMPORTANT MUST ATTENTION** lead with useful guidance and readable priorities; preserve action-changing conditions/numbers and required structures. Remove report bulk from guides, use verified discovery, and judge semantic value rather than word or warning counts.

<!-- /SYNC:output-quality-principles:reminder -->

<!-- SYNC:ai-discovery-doc-quality:reminder -->

**MUST ATTENTION** AI-read guides: purpose/read-when and priorities first; retain action-changing rules, exceptions and rationale; verify triggered discovery and parser contracts. Use the content-value and semantic-disposition gate after enhancement; keep evidence in temporary reports and fix generated output at its source.

<!-- /SYNC:ai-discovery-doc-quality:reminder -->


## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Scan one manifest-selected reference-doc target and deliver a surgical, evidence-backed update that preserves action-changing rules, exceptions and verified discovery without report bulk.

**IMPORTANT MUST ATTENTION** verify every emitted path, example, coverage claim, and generated projection against the real repository before reporting success.

**IMPORTANT MUST ATTENTION** resolve `--target` and load its manifest entry FIRST — never scan from memory of "what a backend/frontend/design scan does"

**IMPORTANT MUST ATTENTION — Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **Scan & Update Doc:** read/save baseline, classify operation, preserve semantic coverage, reconcile conflicts, skip no-op writes.
- **Output Quality:** retain decision value, readable conditions, useful examples and actionable numbers; detailed evidence stays in reports.
- **AI-Discovery Doc Quality:** purpose + critical rules on top, reminders at the bottom when long, trigger-based pointers to existing docs, reachable from the docs index.
- **Parallel Sub-Agent Dispatch:** Tag tasks PAR/SEQ, group PAR into disjoint-write-set waves, spawn each wave in ONE message, barrier before advancing.

**IMPORTANT MUST ATTENTION Final Step:** enhance only a doc the scan actually changed, then pass the AI-discovery gate on it; a no-op or evidence-backed skip requires no write or enhancement
**IMPORTANT MUST ATTENTION** break work into small `TaskCreate` tasks BEFORE starting — one task per sub-agent, one per phase
**IMPORTANT MUST ATTENTION** verify applicability before framework/type detection — all grep terms derive from evidence, never hardcoded
**IMPORTANT MUST ATTENTION** cite `file:line` for every pattern (confidence >80% to document; <60% omit)
**IMPORTANT MUST ATTENTION** a project graph is an optional hint for code relationships; source callers remain the evidence, and an absent graph is neither a limitation nor a finding
**IMPORTANT MUST ATTENTION** sub-agents write findings incrementally after each file — NEVER batch at end (context loss)
**IMPORTANT MUST ATTENTION** read existing doc FIRST, save baseline, diff evidence, preserve meaningful guidance and disposition removals
**IMPORTANT MUST ATTENTION** clean Round 1 ends the scan; after Round 1 finds and fixes issues, Round 2 fresh-eyes review is mandatory; Round 3 runs only if Round 2 finds issues (max 3 rounds)
**IMPORTANT MUST ATTENTION** honor the target entry's Content-Rule exceptions, Special slivers, and Anti-Rationalization rows — they encode why this target differs from the others

**Anti-Rationalization (shared — the target entry adds its own rows):**

| Evasion                                           | Rebuttal                                                                            |
| ------------------------------------------------- | ----------------------------------------------------------------------------------- |
| "I know what a `<target>` scan does, skip the manifest entry" | The entry holds the BLOCKING gates, sub-agent count, and exceptions — scanning from memory drops them |
| "Framework/type already known, skip Phase 0 detection" | Phase 0 is BLOCKING — derive grep terms from evidence, not assumption               |
| "Doc has content, skip re-read"                   | Show section list extracted from doc as proof of re-read                            |
| "Examples look right"                             | Glob-verify ALL file paths + Grep-verify ALL names — looking right ≠ verified       |
| "Round 2 review not needed after fixing a small scan" | Size does not waive the issue-triggered gate: corrected Round 1 requires a fresh sub-agent; a clean Round 1 ends the scan. |

**[TASK-PLANNING]** Before acting, analyze task scope and break into small todo tasks and sub-tasks using TaskCreate.
