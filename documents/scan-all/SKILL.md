---
name: scan-all
version: 1.0.0
description: '[Documentation] Use when refreshing every selected, evidence-applicable reference-doc scan target at once. One doc: scan; first-time setup: docs-manager --mode=init.'
---

## Quick Summary

**Goal:** Discover and refresh selected, evidence-applicable built-in targets and explicitly generic custom reference docs without assuming every project has every capability.

**Workflow:**

1. **Validate** — Support absent config; validate present config and use the runtime evidence-based resolver.
2. **Resolve** — Read always-on inputs separately and resolve the effective task-specific `referenceDocs` selection.
3. **Filter** — Resolve exact built-in targets, selected generic custom docs, and manually owned docs; verify capability evidence for each scan.
4. **Scan** — Run eligible targets in parallel only when their output write sets are disjoint.
5. **Verify** — Check every result and skip; clear stale status only after all required owners are current; run the AI-discovery gate across the refreshed set.
6. **Summarize** — Report refreshed, unchanged, skipped, blocked, and manual docs with evidence.

**Key Rules:**

- The registered targets are an option catalog, not a required scan list.
- `referenceDocs` absent resolves to no task-specific docs for a minimal project, adding only refs supported by config/repository evidence. An explicit array, including `[]`, is exact.
- `lessons.md` and the docs index are project-init-owned always-on context inputs; they are outside task-specific selection.
- Each built-in scanner writes only its manifest `doc`. A custom doc defaults to manual ownership; only `scanTarget: "generic"` opts it into an evidence-based generic scan. Never infer a built-in target from a basename.
- The generic scanner writes only the exact selected filename and uses its configured `purpose` and optional `sections`. Generic docs receive conservative non-disposable repository-wide impact routing; manual docs are not auto-scanned, freshness-tracked, or impact-routed.
- Optional capabilities that are not evidenced are skipped with the checked config/source evidence.
- Scans update reference documentation only. Graph work or any broader setup is conditional on project capability and a separate owner.

## When to Use

- Staleness gate blocks prompts ("BLOCKED: Reference docs are stale")
- First time initializing reference documentation for a content-bearing project
- Periodic refresh when codebase has changed significantly
- User runs `/scan-all` manually

## When to Skip

- Empty/greenfield project without evidenced capabilities; project-init handles its always-on context and no capability scans run.
- No selected applicable docs are stale and project-init-owned always-on inputs are current.

## Execution

### 1. Validate and resolve config

Resolve the configured project-config file through `.claude/hooks/lib/project-config-loader.cjs` (default `docs/project-config.json`). Absent config uses portable defaults and repository evidence. Present config requires a valid schema and non-empty `project.name`; repair invalid declared sections before relying on them. Optional capability sections may be omitted. A declared incomplete or unsupported section blocks the run.

Use `.claude/hooks/lib/session-init-helpers.cjs` to resolve the effective `referenceDocs` selection; do not copy the full registry into this skill:

- When `referenceDocs` is absent, the resolver supplies only the portable baseline and capability references supported by config/repository evidence. A minimal project with no evidenced capability resolves to no task-specific references.
- When `referenceDocs` is an explicit array, including `[]`, the array is the exact task-specific selection.
- The always-on `lessons.md` and docs-index inputs are owned by project initialization and remain outside this selection. Confirm those inputs through their owner; do not append them to task-specific work.

### 2. Map selected docs to targets

Read `.claude/skills/scan/references/targets.md`. Resolve each selected filename exactly. Built-in filenames use only their framework-owned manifest target; a custom filename with `scanTarget: "generic"` uses `/scan --target=generic-reference-doc --filename="<filename>"`; a custom filename with no target or `scanTarget: "manual"` remains under curated project ownership. Resolve the containing root from `docsRoots.projectReference.path` (default `docs/project-reference/`; `docsRoots.projectReference.path` in `docs/project-config.json` overrides it).

- Custom `referenceDocs` entries require `filename` and `purpose`, with optional `sections`, `templatePath`, and `scanTarget`. Config validation rejects unknown targets and unsafe paths; runtime path resolution also rejects physical symlink escapes.
- Registered targets are optional capabilities. [BLOCKING] Before launching a built-in target, read the head of its own file `.claude/skills/scan/references/targets/<key>.md` (its `applies when` and `skip when` lines) and apply that evidence; the registry index alone does not carry the gate. Config can select a scan or guide source search, but source examples and patterns must still be verified.
- If a selected built-in target's capability is absent, report `SKIPPED` with the config/source paths checked. Do not create a placeholder or claim the doc is refreshed. Generic scans use only their configured purpose and selected output; manual docs are not scan candidates.
- Do not launch `ui-system` alongside its child targets. `scan-all` selects individual docs from the effective list; an explicitly routed UI orchestration can fan out only to applicable children.
- Build a coverage ledger with one disposition per exact selected output: eligible, manual, skipped or blocked. Reconcile the union of assignments against that set, including nested/boundary paths; `[]` creates no task-specific scans. Deduplicate identical targets. Targets with different owned output docs may run in parallel; shared output owners run once.

### 3. Run and verify

For each eligible built-in or generic target, invoke its exact scan command and accept only its evidence-backed result. Generic targets include their configured filename. A scan can finish as `UPDATED`, `UNCHANGED`, `SKIPPED`, or `BLOCKED`; preserve the target report and surface every non-complete status.

Reconcile every selected output against returned reports at the all-return barrier before dependent writes. Check final content-value/semantic-retention reviews after enhancement, baseline reconciliation and truthful operation stamps. Check the exact selected outputs and the always-on owner inputs. Clear `.claude/.scan-stale` only after the selected automatically scannable docs are current and project-init-owned inputs are confirmed; skipped or stale docs keep the result open. Manual docs do not enter the automated freshness gate. Use the owner helper only after this check:

```bash
node -e "require('./.claude/hooks/lib/session-init-helpers.cjs').refreshScanStaleFlag()"
```

Each changed scan output follows its target's enhancement rule. Verify that enhancement in the scan result; do not run a second hardcoded enhancement list or rewrite unchanged/skipped docs.

**AI-discovery gate across the set (`SYNC:ai-discovery-doc-quality`).** Per-doc quality belongs to each scan; this run checks what no single scan sees: the docs index and root context route to every refreshed or selected doc through a `read <path> when <situation>` trigger, no route points at a missing or not-applicable doc, and no selected doc is an orphan. A routing gap is fixed by the docs-index target scan, or — for the root context — a `referenceDocs` entry via `/project-config` followed by `/ai-context-refresh`, never by hand-editing generated output.

## Optional Graph Refresh

A graph is not a universal scan prerequisite. If the project config and repository show a supported code graph is part of this project, run its owning graph workflow when the graph is stale or the setup explicitly requests refresh. Otherwise report graph work as not applicable; never block documentation scans on an absent graph.

## Summary Output

Report each selected target with its status, output path, and evidence-backed reason. List always-on inputs checked, manual docs left to their owner, and any blocked stale gate. Do not claim all docs are refreshed when optional targets were skipped or unselected.

---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting.

<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `ai-discovery-doc-quality` — Agent-guide content value, authority, retention and verified discovery; writing a doc that an agent reads → .claude/skills/shared/protocols/ai-discovery-doc-quality.md
- `output-quality-principles` — Useful, readable guidance without lost conditions; writing generated docs or reports → .claude/skills/shared/protocols/output-quality-principles.md

<!-- PROTOCOL-GUIDES:END -->

<!-- SYNC:output-quality-principles:reminder -->

**IMPORTANT MUST ATTENTION** lead with useful guidance and readable priorities; preserve action-changing conditions/numbers and required structures. Remove report bulk from guides, use verified discovery, and judge semantic value rather than word or warning counts.

<!-- /SYNC:output-quality-principles:reminder -->

<!-- SYNC:ai-discovery-doc-quality:reminder -->

**MUST ATTENTION** AI-read guides: purpose/read-when and priorities first; retain action-changing rules, exceptions and rationale; verify triggered discovery and parser contracts. Use the content-value and semantic-disposition gate after enhancement; keep evidence in temporary reports and fix generated output at its source.

<!-- /SYNC:ai-discovery-doc-quality:reminder -->

## Closing Reminders

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries) — MUST ATTENTION honor each canonical body:**

- **Output Quality:** MUST ATTENTION retain actionable guidance, conditions and consumer-required structures; move investigation bulk to temporary reports.
- **AI-Discovery Doc Quality:** MUST ATTENTION the docs index and root context route every refreshed doc by trigger; no orphan, dead or not-applicable route.

**IMPORTANT MUST ATTENTION** break work into small todo tasks using `TaskCreate` BEFORE starting
**IMPORTANT MUST ATTENTION** search codebase for 3+ similar patterns before creating new code
**IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim (confidence >80% to act)
**IMPORTANT MUST ATTENTION** add a final review todo task to verify work quality

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using TaskCreate.
