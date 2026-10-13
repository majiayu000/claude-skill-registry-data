---
name: scope-check
description: "Analyze a feature or sprint for scope creep by comparing current scope against the original plan. Flags additions, quantifies bloat, and recommends cuts. Use when user says 'any scope creep', 'scope review', 'are we staying in scope'."
argument-hint: "[feature-name or sprint-N]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
model: haiku
---

## User Guide

- When to use: Analyze a feature or sprint for scope creep by comparing current scope against the original plan. Flags additions, quantifies bloat, and recommends cuts. Use when user says 'any scope creep', 'scope review', 'are we staying in scope'.
- Inputs: Command arguments: `/scope-check [feature-name or sprint-N]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: `memory_bank/t3_archive/reviews/review-index.md`.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

# Scope Check

Default behavior is read-only. It reports findings in conversation unless the
user explicitly approves saving the report.

Compares original planned scope against current state to detect, quantify, and triage
scope creep.

**Argument:** `$ARGUMENTS[0]` — feature name, sprint number, or milestone name.

---

## Phase 1: Find the Original Plan

Read the confirmed original feature baseline. For the CDD route below, use the actual governing CDD; if a different matching original design file is chosen, resolve and read that exact original file as the mandatory baseline. Choosing an alternate locator does not make the baseline optional. Missing or unresolved baseline still stops this comparison.

Locate the baseline scope document for the given argument:

- **Feature name** → read `design/cdd/[feature].md` or matching file in `design/`
- **Sprint number** (e.g., `sprint-3`) → read `production/sprints/sprint-03.md` or similar
- **Milestone** → read `production/milestones/[name].md`

If the document is not found, report the missing file and stop. Do not proceed without
a baseline to compare against.

---

## Phase 2: Read the Current State

Check what has actually been implemented or is in progress:

- Scan the codebase for files related to the feature/sprint
- Read git log for commits related to this work (`git log --oneline --since=[start-date]`)
- Check for TODO/FIXME comments that indicate unfinished scope additions
- Check active sprint plan if the feature is mid-sprint

---

## Phase 3: Compare Original vs Current Scope

Produce the comparison report:

```markdown
## Scope Check: [Feature/Sprint Name]
Generated: [Date]

### Original Scope
[List of items from the original plan]

### Current Scope
[List of items currently implemented or in progress]

### Scope Additions (not in original plan)
| Addition | Source | When | Justified? | Effort |
|----------|--------|------|------------|--------|
| [item] | [commit/person] | [date] | [Yes/No/Unclear] | [S/M/L] |

### Scope Removals (in original but dropped)
| Removed Item | Reason | Impact |
|-------------|--------|--------|
| [item] | [why removed] | [what's affected] |

### Bloat Score
- Original items: [N]
- Current items: [N]
- Items added: [N] (+[X]%)
- Items removed: [N]
- Net scope change: [+/-N] ([X]%)

### Risk Assessment
- **Schedule Risk**: [Low/Medium/High] — [explanation]
- **Quality Risk**: [Low/Medium/High] — [explanation]
- **Integration Risk**: [Low/Medium/High] — [explanation]

### Recommendations
1. **Cut**: [Items that should be removed to stay on schedule]
2. **Defer**: [Items that can move to a future sprint/version]
3. **Keep**: [Additions that are genuinely necessary]
4. **Flag**: [Items that need a decision from producer/creative-director]
```

---

## Phase 4: Verdict

Assign a canonical verdict based on net scope change:

| Net Change | Verdict | Meaning |
|-----------|---------|---------|
| ≤10% | **PASS** | On Track — within acceptable variance |
| 10–25% | **CONCERNS** | Minor Creep — manageable with targeted cuts |
| 25–50% | **FAIL** | Significant Creep — must cut or formally extend timeline |
| >50% | **FAIL** | Out of Control — stop, re-plan, escalate to producer |

Output the verdict prominently:

```
**Scope Verdict: [PASS / CONCERNS / FAIL]**
Net change: [+X%] — [On Track / Minor Creep / Significant Creep / Out of Control]
```

---

## Phase 5: Next Steps

After presenting the report, offer concrete follow-up:

- **PASS** → no action required. Suggest re-running before next milestone.
- **CONCERNS** → offer to identify the 2–3 additions with best cut ratio. Reference `/sprint-plan update` to formally re-scope.
- **FAIL** → recommend escalating to producer. Reference `/sprint-plan update` for re-planning or `/estimate` to re-baseline timeline.

Always end with:
> "Run `/scope-check [name]` again after cuts are made to verify the verdict improves."

---

## Phase 5b: Optional Scope Decision Evidence

After presenting the report, ask:

> "May I write this scope check to `production/scope/scope-check-[target]-[YYYY-MM-DD].md`?"

Write the report when its named effect is authorized. Update initialized
`memory_bank/t3_archive/reviews/review-index.md` only when its separate named
index effect is also authorized.

Update the Memory Bank index only when this run enters its separately named, authorized effect after saving the actual report. Initialized Memory Bank alone is insufficient; read-only and report-only scopes exclude indexing. If the intended effect or initialization is unresolved, retain Unknown. Before indexing, read the saved immutable report and exact input/evidence identities; a proposed output or INFO is insufficient. This effect does not initialize Memory Bank.

Review index row:

- Review Type: `scope-check`
- Source Artifact: `production/scope/scope-check-[target]-[YYYY-MM-DD].md`
- Verdict: `PASS`, `CONCERNS`, or `FAIL`
- Scope: feature, sprint, or milestone target

Use `Source Artifact` as the dedupe key. Do not create `memory_bank/` from
`/scope-check`; if it does not exist, keep the saved scope report and tell the
user to run `/constitute` to establish the memory_bank governance control
plane.

---

### Rules

- Scope creep is additions without corresponding cuts or timeline extensions
- Not all additions are bad — some are discovered requirements. But they must be acknowledged and accounted for
- **[Game]** When recommending cuts, prioritize preserving the core player experience over nice-to-haves. **[Product]** When recommending cuts, prioritize preserving the core user workflow and data integrity over nice-to-haves.
- Always quantify scope changes — "it feels bigger" is not actionable, "+35% items" is
