---
name: quality-debt
description: Inventory AICP's technical debt across code (TODO/FIXME/XXX markers), wiki (deferred backlog tasks), and architecture (known workarounds + structural-vs-operational gaps), then prioritize what to pay down. Distinct from quality-coverage (testing gaps) and quality-lint (style gaps); this skill is the "what we know we owe but haven't fixed" inventory. Loads when the operator says "tech debt", "what's deferred", "debt inventory", "known shortcuts".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# quality-debt

Inventories AICP's known but unaddressed gaps — code TODO markers, wiki
deferred tasks, structural-only adoptions awaiting operational depth, and
documented workarounds. Different from `quality-coverage` (gaps you DIDN'T
know about until measurement) — this is gaps you DOCUMENTED at decision time
but deferred fixing. The skill turns the scattered debt signals into one
prioritized inventory the operator can actually act on.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "tech debt", "what's deferred", "debt inventory", "known shortcuts", "what do we owe", "structural vs operational gaps"
- **Periodic cycle**: monthly/quarterly debt review (debt grows silently between reviews)
- **Pre-release gate**: before a milestone ships, audit the debt that was deferred FROM the milestone (was the deferral correct? still warranted?)
- **Post-incident retrospective**: when a bug ships, check if the debt inventory had warned about that area
- **Onboarding new contributor**: hand them the debt inventory so they know where the workarounds and shortcuts live
- **Capacity planning**: when the operator asks "what should the next sprint focus on?", debt is a candidate

Do NOT load when:

- A specific bug needs fixing now (load `feature-implement` or `systematic-debugging` for the fix)
- The concern is testing gaps surfaced by measurement (load `quality-coverage`)
- The concern is style/lint gaps (load `quality-lint`)
- You want a full multi-dimension audit (load `quality-audit` — debt is one of its sub-audits)

## Operations

This skill has 4 named operations. Execute in order.

### Operation 1: Inventory debt across all sources

**Trigger**: skill loaded; operator wants the inventory.

**Process**:

1. **Code markers** — scan the codebase for explicit debt signals:

   ```bash
   grep -rn "TODO\|FIXME\|XXX\|HACK\|XXX-LATER" aicp/ tools/ tests/ 2>/dev/null | grep -v ".pyc"
   ```

   Capture: file, line, marker type, comment text. Classify by marker meaning:
   - **TODO**: planned future work (medium urgency)
   - **FIXME**: known broken behavior (HIGH urgency — possible bug)
   - **XXX**: warning about edge case (HIGH urgency)
   - **HACK**: deliberate workaround (medium urgency, but never delete without understanding)

2. **Backlog deferrals** — read `wiki/backlog/tasks/` for tasks tagged `deferred`, with `status: blocked`, or with notes containing "DEFERRED" / "deferred until":

   ```bash
   grep -lE "status: (blocked|deferred)|DEFERRED" wiki/backlog/tasks/*.md 2>/dev/null
   ```

   For each, capture: task ID, deferred reason, target unblock date/milestone (if any).

3. **Structural-vs-operational gaps** — read `wiki/decisions/` and `wiki/log/` for items marked "structural only" or "stub". Per Structural Compliance Is Not Operational Compliance, AICP currently has structural Tier 4/4 but operational only Tier 2+. Inventory which Tier-3+ requirements are stubs:

   ```bash
   grep -rln "structural stub\|STRUCTURAL only\|operational implementation pending\|TODO:.*operational" tools/ wiki/ 2>/dev/null
   ```

4. **Documented workarounds** — search wiki + memory for "workaround", "temporary", "until <X>", "known limitation":

   ```bash
   grep -rln -i "workaround\|temporary\|known limitation" wiki/ docs/ 2>/dev/null
   ```

5. Write the inventory to `wiki/decisions/00_inbox/debt-audit-<date>.md` (type=reference). Group by source (code markers / backlog deferrals / structural stubs / workarounds).

**Quality bar (Operation 1 done when)**:

- [ ] All four sources scanned with explicit commands captured
- [ ] Each item recorded with: file/path, marker type or category, brief description, age (days since first introduced if discoverable via git blame)
- [ ] Inventory written to dated audit page

### Operation 2: Classify and prioritize

**Trigger**: Operation 1 inventory captured.

**Process**:

1. For each debt item, assign two attributes:
   - **Risk**: what happens if this debt is never paid? Low (cosmetic, internal-only) / medium (degrades dev velocity, complicates onboarding) / high (risk of bug, blocks Stage 3+ progress, blocks fleet integration).
   - **Cost to pay**: how much work to address? Low (<1 day) / medium (1-5 days) / high (>1 week).
2. Score: low cost + high risk = **HIGHEST priority** (pay now). Low cost + low risk = **LOW priority** (cleanup at convenience). High cost + low risk = **DEFER permanently** (or accept). High cost + high risk = **PLAN as epic** (too big for ad-hoc).
3. Identify "compound debt" — items that share a root cause. Example: 5 TODO markers all reference "router doesn't have stage-aware routing yet." Those are ONE debt (PreToolUse hooks — Step 9.5), not 5. Compound debt items get folded into the parent epic.
4. Identify "antiquated debt" — items older than 6 months that haven't been addressed AND aren't blocking anything. Candidate for deletion (the marker, not the code) — if it's been ignored for 6 months and nothing broke, the marker was wrong.

**Quality bar (Operation 2 done when)**:

- [ ] Every item has risk + cost attributes
- [ ] Items grouped by priority quadrant
- [ ] Compound debt identified and grouped
- [ ] Antiquated debt flagged for deletion review

### Operation 3: Author follow-up tasks for the priority items

**Trigger**: Operation 2 prioritization complete; operator approved which items to address.

**Process**:

1. Operator picks which HIGHEST priority items to address THIS pass. Don't try to address all — capacity is finite; debt grows faster than fixes if you over-commit.
2. For each chosen item, create a backlog task at `wiki/backlog/tasks/T<n>-<slug>.md` with:
   - Reference to the debt-audit page (`derived_from`)
   - Specific file/line references from Operation 1
   - Done When criteria (the debt marker is removed AND the underlying issue resolved, not just commented out)
   - Estimated effort from Operation 2's cost classification
3. For "PLAN as epic" items, create an epic at `wiki/backlog/epics/` instead of a task. Epic decomposes into modules + tasks via `pm-plan`.
4. For antiquated debt approved for marker deletion, create a single cleanup task: "Delete N antiquated debt markers" with the file:line list.
5. Update the debt audit page with the task IDs created (so future audits can verify the items were actioned).

**Quality bar (Operation 3 done when)**:

- [ ] Each chosen HIGHEST priority item has a backlog task
- [ ] Each "PLAN as epic" item has an epic + at least 1 child module
- [ ] Antiquated debt cleanup task created (if any)
- [ ] Audit page updated with task IDs

### Operation 4: Update the debt-audit page + contribute trends

**Trigger**: Operation 3 tasks landed.

**Process**:

1. Re-open the debt-audit page. Record:
   - Total items per source (code markers / deferrals / stubs / workarounds)
   - Distribution per priority quadrant
   - Items addressed (task IDs)
   - Items deferred (with reasoning)
   - Items deleted as antiquated (count)
   - Comparison with prior debt audit (if any) — trend up/stable/down
2. If a SYSTEMIC pattern emerged (e.g., "3 of 5 HIGHEST priority items are about stage-gate enforcement gaps"), contribute back as a lesson: `gateway contribute --type lesson --title "..."`.
3. Run `tools/lint.py wiki/decisions/00_inbox/debt-audit-<date>.md`.
4. Schedule next audit. Defaults: monthly for active development, quarterly for stable codebases. Increase frequency if trend shows growing debt.

**Quality bar (Operation 4 done when)**:

- [ ] Per-source counts in audit page
- [ ] Per-priority distribution
- [ ] Tasks/epics created and IDs captured
- [ ] Trend comparison vs prior audit (or "baseline established" if first)
- [ ] Lesson contributed if systemic
- [ ] Audit page lint passes

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Counting items, not understanding them (debt theater)

The temptation: report "47 TODO markers, 12 backlog deferrals, 5 stubs" and feel productive. But raw counts without classification are useless — 47 cosmetic TODOs are NOT equivalent to 5 high-risk operational stubs. Per Quality Standards anti-pattern: this is "documentation theater for the operator."

**Detection**: did you classify (risk + cost) for EACH item? Or did you report aggregate counts and call it done?

**The rule**: classification is the work, not counting. An audit page with raw counts but no per-item attributes failed Operation 2.

### Gotcha 2: Deleting markers without understanding (silent debt re-creation)

A `# HACK: temporary fix` comment is annoying. Tempting to delete the comment because "the code seems to work." But the HACK marker was put there for a reason — deleting it loses the warning. Future readers don't know it's a workaround; future bugs hit the unmarked workaround and aren't recognized as such.

**Detection**: did you delete a marker without confirming the underlying issue is fixed (not just that the code "works for now")?

**The rule**: never delete a marker unless the underlying issue is RESOLVED (and document the resolution in the same commit). If the code works but the workaround is still there, the marker stays.

### Gotcha 3: Inventorying everything as HIGH (priority inflation)

The temptation: every debt item feels important when you're looking at it. Marking everything HIGH defeats the purpose of prioritization.

**Detection**: more than 30% of items are marked HIGH risk.

**The rule**: HIGH risk means "real risk of bug, blocks roadmap, or affects external consumers." Most items are medium or low. If you have 47 items and 30 are HIGH, your filter is broken — recalibrate.

### Gotcha 4: Conflating debt with backlog (work-in-progress is not debt)

Tasks in `wiki/backlog/tasks/` with `status: in-progress` are WORK IN PROGRESS, not debt. Counting them as debt inflates the inventory and confuses the priority.

**Detection**: did Operation 1 step 2 filter on `status: blocked|deferred`? Or did it count ALL backlog items?

**The rule**: only `status: blocked` or `status: deferred` (or notes containing DEFERRED) count as debt. Active tasks are progress, not debt.

### Gotcha 5: Skipping the structural-vs-operational gap inventory

The temptation: code markers are concrete; structural-vs-operational gaps feel abstract. Skip them. NO — structural-only adoptions are AICP's biggest hidden debt right now (Tier 4/4 STRUCTURAL but Tier 2+ operational means: many tools have stubs, many adoption requirements are presence-only). Skipping this category misses the largest debt class.

**Detection**: did Operation 1 step 3 explicitly scan for "structural stub" / "STRUCTURAL only" / "operational implementation pending"?

**The rule**: structural-vs-operational gaps ARE debt, possibly the most consequential kind because they create FALSE CONFIDENCE (compliance checker says "Tier 4/4" while operational depth is shallower). Always inventory them.

## Reference exemplars

Per Extension Standards, reference exemplars are the second brain's `model-builder` and `wiki-agent` skills. For the OUTPUT artifact:

- **Debt audit page**: same shape as `coverage-audit-<date>.md` and `lint-audit-<date>.md` from sibling quality skills — reference page with classification table + recommendations.
- **Real systemic pattern example**: see [Skills audit 2026-04-17](../../../wiki/decisions/00_inbox/skills-audit-2026-04-17.md) — that audit identified 47% of skills as boilerplate; the systemic pattern was "scaffolding script generated all skills from one template without filling in skill-specific content." That's the kind of insight a debt audit should surface.

## Domain context

This skill operates in **backend-ai-platform-python** — see [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml). Read-only on code (creates wiki content + backlog tasks).

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| quality-coverage | unknown gaps surfaced by coverage measurement | Discovered debt; this skill inventories KNOWN debt |
| quality-lint | style/hygiene gaps | Different debt class — style isn't usually called "debt" but tracked separately |
| quality-audit | umbrella across all quality dimensions | Includes this skill as a sub-audit |
| pm-plan | epic/module/task decomposition | Large debt items become epics; this skill identifies them, pm-plan decomposes them |
| refactor-* skills | acting on debt that requires structural change | Debt audit identifies; refactor skills act |
| feature-iterate | improving a shipped feature | Different cycle — iterate adds value, debt-pay removes risk |
