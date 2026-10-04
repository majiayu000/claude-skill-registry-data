---
name: "review"
description: "Three-axis review of a diff: Standards (does it follow this repo's documented conventions and avoid known smells), Spec (does it do what was actually asked, and nothing more), and Adversarial (what breaks that nobody thought to look for). Runs the axes as parallel sub-agents, then rules on every finding as lead. Use for /review, 'review this branch', 'tear this apart', 'stress test this code', or 'find blind spots'."
disable-model-invocation: true
---

# Review

Three axes over one diff, run as parallel sub-agents so they cannot pollute
each other's context, then one lead judgment over everything they return.

The axes are orthogonal on purpose. A change can pass any one and fail another:

- Follows every convention, implements the wrong thing. **Standards pass, Spec fail.**
- Does exactly what the ticket asked, breaks the project's conventions. **Spec pass, Standards fail.**
- Correct and conventional, falls over on an input nobody considered. **Both pass, Adversarial fail.**

Reporting them separately is what stops one axis masking another.

**Not the built-in `/code-review`.** That one is fast, focused on correctness
bugs, and can post to a PR. Reach for it on routine changes. Reach for this
when the change is contested, architectural, or about to land somewhere
expensive to undo.

The deliverable is a verdict. **Do not auto-apply changes.**

## 1. Pin the scope

Whatever fixed point the user gave: a SHA, branch, tag, `main`, `HEAD~5`. If
they gave none, use the merge-base against the default branch and say so.

```bash
git diff <fixed-point>...HEAD          # three-dot: compares against merge-base
git log <fixed-point>..HEAD --oneline
```

Confirm the ref resolves (`git rev-parse`) and the diff is non-empty **before**
spawning anything. A bad ref should fail here, not three times in parallel.

For a diff whose blast radius is unclear, `search_graph` and `trace_path` from
`codebase-memory` find the call sites the diff affects, so the Standards axis
can see past the changed lines. Fall back to `grep` when the graph has no
entry for this repo.

## 2. State the intent

One clear paragraph: what is this change trying to accomplish? Derive it from
the user's message, the commit messages, the PR description, the code itself.

Reviewers challenge whether the work **achieves** the intent, not whether the
intent is right. If you cannot state it, ask before proceeding: an unstated
intent produces three reviews of three different imagined changes.

## 3. Gather the axis inputs

- **Standards sources.** Anything in-repo documenting how code should be written: `CLAUDE.md`, `CONTEXT.md`, `CODING_STANDARDS.md`, `CONTRIBUTING.md`, ADRs touching the area. Plus [SMELLS.md](SMELLS.md), which applies even when the repo documents nothing.
- **Spec source**, in this order: issue references in the commits (`#123`, `Closes #45`), a path the user passed, a spec under `docs/`, `specs/`, or `.scratch/` matching the branch. If nothing is found, ask. If the user says there is no spec, the Spec axis reports "no spec available" and is skipped.

## 4. Spawn the three axes in parallel

One message, three `Agent` calls, `run_in_background: true`. Each gets the diff
command, the commit list, and only its own inputs.

| Axis | Model | Brief |
|---|---|---|
| Standards | `sonnet` | "Report, per file or hunk: (a) every place the diff violates a documented standard, citing the standard file and the rule; (b) any baseline smell, named, with the hunk quoted. Distinguish hard violations from judgement calls: documented-standard breaches can be hard, baseline smells never are, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Under 400 words." Paste SMELLS.md in full; the sub-agent has no other access to it. |
| Spec | `sonnet` | "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff nobody asked for (scope creep); (c) requirements that look implemented but look wrong. Quote the spec line for each finding. Under 400 words." |
| Adversarial | `opus` and `fable`, one each | Fill [reviewer-prompt.md](reviewer-prompt.md) with the intent, the diff, [rubric.md](rubric.md), and [code-quality-review.md](code-quality-review.md). |

**On the adversarial axis.** Its signal comes from model diversity, not from
assigned personas, so run it on at least two different models. Be honest about
the ceiling: every model available here is a Claude model, so this is weaker
than a genuine cross-vendor panel. Two models agreeing is good evidence, not
proof. One model alone is a single opinion with extra steps.

## 5. Synthesize

1. Parse all findings.
2. **Consensus first.** Anything two or more reviewers raised independently is the highest signal in the run.
3. **Lone findings** still get read, weighted lower.
4. **Deduplicate.** Different reviewers describe the same issue differently. Merge them, noting who raised it.
5. **Note disagreements.** One reviewer flagging what another explicitly cleared is itself useful context.

## 6. Rule on it as lead

You are a pragmatic senior engineer, not a neutral aggregator. Read
[lead-judgment.md](lead-judgment.md) for the full framework.

The reviewers each saw a slice. You have the goal, the constraints, the
timeline, and which tradeoffs were already settled. Use that aggressively.
Every finding lands in exactly one bucket:

- **Act on.** Real, affects correctness, security, or maintainability given the actual goals. Would block a real PR.
- **Consider.** Legitimate, but you are not sure it outweighs the cost right now. Worth the user's attention.
- **Noted.** Valid but not actionable. Context-dependent, premature, or low-impact at this stage.
- **Dismissed.** Wrong, nitpicky, or missing context. Say briefly why.

## Output

```
### Intent
> the paragraph from step 2

### Axes
- Standards: N findings
- Spec: N findings (or "no spec available")
- Adversarial (<model>, <model>): N findings

### Act on
### Consider
### Noted
### Dismissed
```

Each finding names which axis and which model raised it, and carries a one-line
rationale for its bucket. Report Standards and Spec counts separately and never
rank one against the other; that reranking is exactly what the separation
exists to prevent.

Close with an **Agreement map**: where the reviewers converged, where they
split, and what that pattern says about confidence.
