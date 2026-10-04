---
name: slice-check
description: Audit tracker tickets or a plan's work items as dispatchable slices using cold-read probes.
disable-model-invocation: true
---

# Slice check

Audit a spec's tracker tickets or a plan document's named work items before dispatch. Each is a candidate **slice**. Use one independent cold-read probe per pending slice to rehearse its execution; combine its evidence with your whole-graph review. Plan work items need no tracker issues.

The deliverable is a verdict table with proposed remedies. Applying changes to tickets or the plan is a separate task requiring user authorization.

**Cold read** means fresh context containing one slice, its referenced requirements and applicable shared constraints, and access to the codebase. Supply the context its executor would receive, excluding the parent conversation, audit conclusions, and unrelated sibling assignments. For a plan, use scoped source excerpts with section references rather than the entire document; preserve their wording and record gaps instead of filling them with your own decisions.
**Context budget** is a planning heuristic for source material needed together, with room left to plan, edit, and verify. Default to **50k tokens** for that material unless the user supplies a budget. An estimate above it warrants investigation, not an automatic split.

## Verdicts

Assign evidence-backed verdicts:

| Verdict | Meaning | Evidence required |
| --- | --- | --- |
| `fits` | Context needs and active work are manageable in a fresh session | sufficient cold-start context, justified footprint, meaningful falsifiable criteria, independently verifiable contribution |
| `split` | Too much work or context for one session | footprint or work complexity explaining the limit, plus a viable split boundary |
| `merge` | Over-decomposed; name the sibling(s) to absorb it into | the sibling refs and the shared delivery or verification path |
| `horizontal` | No independently verifiable contribution after declared prerequisites are satisfied | the missing contribution and the later slice needed to demonstrate it |
| `criteria` | Acceptance criteria fail to distinguish success from failure | the missing or unfalsifiable criterion, or evidence that it passes at base without checking the intended change |
| `unclear` | Missing context or evidence prevents a supported verdict | the unresolved decision, unavailable material, or uncertain claim and what would resolve it |

A slice can carry multiple findings, such as `split` + `criteria`. Use `fits` only when all its evidence requirements are met and no unresolved finding remains.

Judge the contribution by the work: implementation delivers behaviour; prefactoring delivers a structural outcome with preserved behaviour; preparation, verification, and close-out deliver usable inputs or attributable evidence. These can be valid slices without application changes. Assess active work and context separately from cloud wait times and operator availability; record access and human prerequisites without treating waiting alone as a reason to split.

## Steps

### 1. Resolve the source and graph

Resolve the tracker spec or plan document from the argument or conversation. Enumerate slices with stable refs, state, work kind, and dependencies. Use tracker refs or document path plus work-item ID/heading, such as `plan.md#W4`. Treat items with no recorded completion state as pending and disclose that assumption. Read the source for the whole-graph review.

Record the code baseline SHA and the audit source version separately. A supplied draft may be newer than, or absent from, the baseline; preserve its snapshot or content hash and cite its sections as audit input. Inspect code and baseline repository references at the recorded SHA. Keep prerequisite assumptions distinct from observed baseline facts.

### 2. Dispatch cold probes

Use read-only subagents with conversation inheritance disabled. Choose available tools and scheduling to suit the environment; each slice needs a fresh reader, including when probes run sequentially. If isolated probes are unavailable, report the cold-read check as unverified.

Give each probe:

1. The slice ref and body, with source excerpts or bounded pointers supplying the cold-read context defined above. Record exactly which sections were supplied so omissions remain distinguishable from missing requirements.
2. The repo root, baseline SHA, and audit source version.
3. The context budget.
4. This checklist and report format:

```
You are rehearsing a fresh execution session for one slice. Grade it on the
supplied context and what you can establish from the codebase.

Read audit excerpts at their recorded source version. Inspect code and
baseline repository references at the supplied SHA.

1. FOOTPRINT: Estimate source context needed together, using relevant file
   sections where sufficient. Explain the estimate, uncertainty, and work
   complexity. If too large, identify a viable split boundary.
2. COLD START: Identify decisions or information still unresolved after
   reading the supplied context and repository. Record missing references
   and prerequisite assumptions separately from observed baseline facts.
3. CRITERIA: For each criterion, give a falsifying observation, the milestone
   at which it is due, and its baseline status: passes, fails, or unknown.
   Cite file locations or check results; distinguish an intentional regression
   guard from a criterion that passes without checking the intended change.
4. CONTRIBUTION: State the independently verifiable output appropriate to
   this slice's work kind after declared prerequisites are satisfied. Identify
   the output that unlocks downstream work and any later acceptance evidence.

Return a concise report containing:
- Assessment and unresolved concerns.
- Estimated tokens, estimation method, file sections, complexity, and any
  proposed split boundary.
- Missing cold-start context and prerequisite assumptions.
- Each criterion, its milestone, falsifying observation, baseline status,
  evidence, and any reason verification was unavailable.
- The delivery or verification path, downstream readiness, and later
  acceptance gates.
```

You assign final verdicts from probe evidence and the whole graph.

### 3. Review the graph

Check the source and incorporate probe findings as they arrive:

- Each dependency resolves to a slice or an explicit external prerequisite, including human access or approval where the source requires it.
- Check for cycles and identify which predecessor output unlocks each dependent slice. Distinguish implementation readiness from final acceptance. If a prerequisite's "done" condition waits for downstream verification, report the cycle or ambiguity and propose separate milestones without weakening acceptance criteria.
- Each slice adds an independently verifiable contribution once its declared prerequisites are satisfied. Depending on earlier work alone does not make a slice `horizontal`.
- Adjacent implementation items that only become usable together are `merge` candidates. Check whether shared files need one execution owner; do not merge distinct slices merely because they share a later integration gate.
- Prefactoring precedes the work it prepares and has a verifiable structural outcome with preserved behaviour.

### 4. Resolve consequential uncertainty

Verify uncertain or conflicting claims that could change a verdict against the recorded audit source or code baseline, as appropriate. For example, inspect the selected sections behind a borderline footprint or check a disputed criterion at baseline. Accept supported observations without a fixed recheck quota. Carry unresolved uncertainty into `unclear` with the evidence needed to resolve it.

### 5. Report

One table: slice ref, verdict(s), evidence, one-line remedy (`split along <seam>`, `merge into W2`, `separate implementation and acceptance milestones`). Below it, give the baseline SHA, audit source version, graph findings, status assumptions, and verification limits. Done when **every pending slice has a supported verdict or an explicit `unclear` finding naming what is needed**. End with the most consequential finding, or state that no dispatch-blocking finding remains.
