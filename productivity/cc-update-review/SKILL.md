---
name: cc-update-review
description: "Reviews PRs that modify the Feature Table in CLAUDE.md. Use when a PR adds CC version rows or modifies docs/CLAUDE-feature-table.md."
when_to_use: "Feature Table PR, CC version PR, CLAUDE.md feature table, cc-update-review"
user-invocable: false
allowed-tools: ["Read", "Grep", "Glob"]
---

# CC Update Review Guardrail

A quality guardrail that prevents "doc-only" additions to the Feature Table during Claude Code update integration.
Automatically classifies whether Feature Table additions are accompanied by implementation, and forces output of implementation proposals when lacking.

## Quick Reference

This skill is triggered in the following situations:

- When reviewing **CC update integration PRs**
- When a diff is detected with new rows added to the **Feature Table** (`CLAUDE.md` / `docs/CLAUDE-feature-table.md`)
- Internal invocation when `/harness-review` determines a PR is a CC integration PR

Situations where this skill is **not** triggered:

- Normal implementation work (`/work`)
- Changes only to files other than the Feature Table
- Setup and initialization work

## 3-Category Classification

Each item added to the Feature Table is classified into the following 3 categories.

### (A) Has Implementation

**Definition**: Implementation changes to hooks / scripts / agents / skills / core corresponding to the Feature Table addition are included in the same PR.

**Criteria**:
- Files related to the feature mentioned in the Feature Table row have been changed
- There is a diff in hooks.json, skill SKILL.md, agent .md, scripts/*.sh, or core/src/*.ts

**Examples**:

| Feature Table Addition | Corresponding Implementation Change | Classification |
|-----------------------|-------------------------------------|---------------|
| `PostCompact hook` | `hooks/post-compact-handler.sh` newly created | A |
| `MCP Elicitation support` | Elicitation event added to `hooks.json` + `elicitation-handler.sh` created | A |
| `Worker maxTurns limit` | maxTurns field added to `agents/worker.md` | A |

**Result**: OK. No additional action needed.

---

### (B) Doc-Only

**Definition**: Rows were added only to the Feature Table with no Harness-side implementation changes. Also does not qualify as CC auto-inherited (Category C).

**Criteria**:
- New rows exist in the Feature Table
- No related changes to hooks / scripts / agents / skills / core in the same PR
- The feature is one where Harness should provide its own added value (configuration, workflow integration, guardrails, etc.)

**Examples**:

| Feature Table Addition | Corresponding Implementation Change | Classification |
|-----------------------|-------------------------------------|---------------|
| `PreCompact hook` | None (Feature Table only) | B |
| `Agent Teams` | None (Feature Table only) | B |
| `Desktop Scheduled Tasks` | None (Feature Table only) | B |

**Result**: NG. Block the PR and require an implementation proposal. Output format described below.

---

### (C) CC Auto-Inherited

**Definition**: Items such as Claude Code core performance improvements, bug fixes, and internal optimizations that require no Harness-side changes.

**Criteria**:
- A CC core fix with no room for Harness to wrap or extend
- Performance improvements, memory leak fixes, UI improvements, etc.
- Internal changes that do not affect Harness workflows

**Examples**:

| Feature Table Addition | Reason | Classification |
|-----------------------|--------|---------------|
| `Streaming API memory leak fix` | CC internal memory leak fix. No Harness-side action needed | C |
| `Compaction image retention` | CC retains images during compaction. No Harness changes needed | C |
| `Parallel tool call fix` | CC internal parallel execution fix. Benefits are automatic | C |

**Result**: OK. However, "CC auto-inherited" must be explicitly noted in the Feature Table column.

## CC Update PR Checklist

Verify the following in order during PR review:

```
## CC Update Integration Checklist

### 1. Extract Feature Table Diff
- [ ] List added rows from the diff of `CLAUDE.md` or `docs/CLAUDE-feature-table.md`

### 2. Classify Each Item
- [ ] Determine A / B / C for each added row
- [ ] Confirm that Category B items are 0

### 3. Per-Category Verification
- [ ] (A) Has implementation: Are corresponding implementation files correctly linked?
- [ ] (B) Doc-only: Has an implementation proposal been provided? (Block PR if not 0)
- [ ] (C) CC auto-inherited: Is "CC auto-inherited" explicitly noted in the Feature Table?

### 4. CHANGELOG Verification
- [ ] Are Category A items documented in the CHANGELOG in "Before / After" format?
- [ ] Are Category C items documented in the CHANGELOG as CC auto-inherited?

### Classification Results

| # | Feature Table Item | Category | Corresponding File / Notes |
|---|-------------------|----------|---------------------------|
| 1 | (item name) | A / B / C | (file path or notes) |
| 2 | (item name) | A / B / C | (file path or notes) |
```

## Output Format When Category B Is Detected

When 1 or more Category B items are detected, output an implementation proposal in the following format.
**This output is mandatory and cannot be omitted.**

```
## Category B Detected: Implementation Proposals

### B-{number}. {Feature Table item name}

**Current state**: Listed in Feature Table only. No Harness-side implementation.

**Harness-specific added value**:
{Specific explanation of how Harness should leverage this feature}

**Implementation proposal**:

| Target File | Change Description |
|------------|-------------------|
| `{file path}` | {specific change description} |
| `{file path}` | {specific change description} |

**User experience improvement**:
- Before: {current user experience}
- After: {user experience after implementation}

**Implementation priority**: {High / Medium / Low}
**Estimated effort**: {Small / Medium / Large}
```

### Output Example

```
## Category B Detected: Implementation Proposals

### B-1. Desktop Scheduled Tasks

**Current state**: Listed in Feature Table only. No Harness-side implementation.

**Harness-specific added value**:
Integrate Scheduled Tasks with Harness workflows to automate periodic quality checks,
status syncing, and memory cleanup.

**Implementation proposal**:

| Target File | Change Description |
|------------|-------------------|
| `skills/harness-work/references/scheduled-tasks.md` | Scheduled task templates and guide |
| `scripts/setup-scheduled-tasks.sh` | Initial setup script |
| `hooks/hooks.json` | Cron trigger registration |

**User experience improvement**:
- Before: Users had to manually run periodic tasks
- After: Harness automatically runs periodic quality checks and notifies with results

**Implementation priority**: Medium
**Estimated effort**: Medium
```

## Recommended "Added Value" Column

It is recommended to add the following column to the Feature Table:

| Feature | Skill | Purpose | Added Value |
|---------|-------|---------|-------------|
| PostCompact hook | hooks | Context re-injection | A: Has implementation |
| Streaming leak fix | all | Memory leak fix | C: CC auto-inherited |

This column makes it possible to verify each item's classification at a glance and prevent Category B items from remaining.

## Related Skills

- `harness-review` - Code review (internally invokes this skill when a CC integration PR is detected)
- `harness-work` - Implementation work (when working based on Category B implementation proposals)
- `memory` - SSOT management (recording classification criteria decisions)
