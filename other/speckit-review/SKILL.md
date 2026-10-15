---
name: "speckit-review"
description: "Verified review of a feature's diff: spec-reviewer and code-reviewer run in parallel, then every finding is adversarially checked by independent agents before it reaches you. Uses the Workflow tool — invoking this skill is your opt-in to the multi-agent run."
argument-hint: "Optional diff range (default: merge-base..HEAD) or 'quick' for single-vote verification"
compatibility: "Requires the spec-reviewer and code-reviewer agents in .claude/agents and an active feature"
metadata:
  author: "blastradius"
  source: "project-local — verified review"
user-invocable: true
disable-model-invocation: false
---


## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). A range
overrides the default; `quick` drops the adversarial vote from three refuters
to one.

## Goal

`spec-reviewer` and `code-reviewer` each produce findings a reader then has to
trust. A reviewer that has read the code for ten minutes is confident in
exactly the way a wrong finding is confident. This command makes findings
**earn** their place: each one goes to independent agents whose only job is to
refute it, and only findings that survive reach the report.

The Workflow tool runs this deterministically — fan-out, verify, merge — so the
shape of the review does not depend on how the model feels about it today. The
user invoking this skill is the opt-in that tool requires; do not ask again.

## Steps

### 1. Scope inline

Before orchestrating, know the work-list:

```bash
git merge-base HEAD main
git diff --name-only <base>..HEAD
python3 .specify/scripts/python/check_prerequisites.py --json --paths-only
```

Record `RANGE`, `FEATURE_DIR`, and the changed-file list. A range with no
changes under `apps/`, `libs/` or `e2e/` has nothing to review — say so and
stop.

Do not invoke `speckit-tracker-sync qa` yet: QA follows the PR being marked
ready, which happens at the end of this skill if nothing blocks.

### 2. Run the workflow

Pass this script to the Workflow tool as `script`, with
`args: { range: RANGE, featureDir: FEATURE_DIR, votes: 3 | 1 }`. It is plain
JavaScript; adjust nothing but `args`.

If the Workflow tool is not available in this session (a cloud session may
not have it), run the same shape by hand: `spec-reviewer` and `code-reviewer`
in parallel through the Agent tool, then one refuting agent per CRITICAL or
HIGH finding, keeping only what survives; note `Workflow unavailable` in the
report.

```js
export const meta = {
  name: 'speckit-review',
  description: 'Spec and code review in parallel, every finding adversarially verified',
  phases: [
    { title: 'Review', detail: 'spec-reviewer and code-reviewer over the same range' },
    { title: 'Verify', detail: 'independent refuters per finding' },
  ],
}

const FINDINGS = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['APPROVE', 'BLOCK'] },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          severity: { type: 'string', enum: ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'] },
          where: { type: 'string' },
          finding: { type: 'string' },
          evidence: { type: 'string' },
          fix: { type: 'string' },
        },
        required: ['severity', 'where', 'finding', 'evidence'],
      },
    },
  },
  required: ['verdict', 'findings'],
}

const VERDICT = {
  type: 'object',
  properties: {
    refuted: { type: 'boolean' },
    reason: { type: 'string' },
  },
  required: ['refuted', 'reason'],
}

const REVIEWERS = [
  { key: 'spec', agentType: 'spec-reviewer',
    prompt: `Review the diff ${args.range} against ${args.featureDir}. Return your findings as structured output.` },
  { key: 'code', agentType: 'code-reviewer',
    prompt: `Review the diff ${args.range} for durability and bloat. Return your findings as structured output.` },
]

const refute = (f, lens, i) => agent(
  `A reviewer reported this finding against the diff ${args.range}:\n\n` +
  `  severity: ${f.severity}\n  where: ${f.where}\n  finding: ${f.finding}\n  evidence: ${f.evidence}\n\n` +
  `Your job is to REFUTE it through the ${lens} lens. Read the actual code at the cited location. ` +
  `Set refuted=true if the finding is wrong, already handled elsewhere, not reachable, or below the severity claimed. ` +
  `Default to refuted=true when uncertain. Give the one-line reason either way.`,
  { label: `verify:${f.where.split(':')[0]}#${i}`, phase: 'Verify', schema: VERDICT, effort: 'high' },
)

const LENSES = ['correctness', 'does-it-reproduce', 'severity-calibration']

const results = await pipeline(
  REVIEWERS,
  (r) => agent(r.prompt, { label: `review:${r.key}`, phase: 'Review', schema: FINDINGS, agentType: r.agentType }),
  (review, r) => review === null ? null : parallel(
    review.findings.map((f, i) => () =>
      parallel(LENSES.slice(0, args.votes).map((lens) => () => refute(f, lens, i)))
        .then((votes) => {
          const cast = votes.filter(Boolean)
          const refutations = cast.filter((v) => v.refuted).length
          const survives = cast.length > 0 && refutations * 2 < cast.length
          return { ...f, reviewer: r.key, votes: cast.length, refutations, survives,
                   reasons: cast.map((v) => v.reason) }
        }),
    ),
  ).then((verified) => ({ reviewer: r.key, verdict: review.verdict, findings: verified.filter(Boolean) })),
)

const reviews = results.filter(Boolean)
const confirmed = reviews.flatMap((r) => r.findings.filter((f) => f.survives))
const dropped = reviews.flatMap((r) => r.findings.filter((f) => !f.survives))
log(`${confirmed.length} finding(s) survived verification, ${dropped.length} refuted`)
return { reviews: reviews.map((r) => ({ reviewer: r.reviewer, verdict: r.verdict })), confirmed, dropped }
```

A reviewer that returns `null` (skipped or died) is reported as **not run**,
never as APPROVE.

### 3. Report

```
## Verified Review: <feature> (<range>)

spec-reviewer: APPROVE|BLOCK|not run · code-reviewer: APPROVE|BLOCK|not run
votes per finding: <n>

Confirmed (<n>):
| Severity | Where | Finding | Fix | Refuters |
|----------|-------|---------|-----|----------|

Refuted (<n>) — one line each: where — the reason the refuters gave
```

A finding survives when fewer than half its refuters refuted it. Report every
refuted finding in one line so the user can disagree with the refuters; the
workflow's `journal.jsonl` has the full reasons if they do.

Then act as `/speckit-auto` phase 14 does: fix every **confirmed** CRITICAL and
HIGH, re-run this skill once, and treat survivors as a Hard Stop. Refuted
findings are not fixed.

### 4. Hand-off

Run standalone (not from `/speckit-auto`, which hands off after its own phase
17): when no confirmed CRITICAL/HIGH is left and `typecheck`, `lint` and the
tests are green, fill in the PR body from `.github/pull_request_template.md`
and mark the PR ready exactly as `/speckit-auto`'s hand-off steps 1–3 do
(records committed, `pr-body-check.ts`, `gh pr edit --body-file`, `gh pr ready`,
`speckit-tracker-sync qa` and its line pushed; ready is QA). `lifecycle.mjs
ready` may refuse a level 2 or 3 feature whose owed artifacts are missing
(`level.mjs check --ready`): run the phases it names, then run it again. Then run the QA step
and merge exactly as `/speckit-auto`'s "The tail" steps 1–6 do: green CI, `/speckit-pr-test <n>`
(story → QA) until `agent-review` is success on the head commit, then merge.
MEDIUM/LOW findings with a small or medium fix are fixed on the branch before
ready, pre-existing or adjacent ones included; only a large fix (the size test
in AGENTS.md, "Technical debt a review defers") is routed to defer, goes to
`specs/<feature>/deferred.md` and is filed as a tracker issue
(`speckit-tracker-sync debt`). With a blocker left, do none of this.

## Done When

- [ ] Both reviewers ran, or the one that did not is reported as not run
- [ ] Every finding went to the configured number of refuters; none reached the report unverified
- [ ] Confirmed and refuted findings both listed, with the refuters' reasons available
- [ ] Confirmed CRITICAL/HIGH fixed and re-reviewed once, or reported as a Hard Stop
- [ ] Standalone and clean: PR ready, story Implementing → QA, merged only on `agent-review` success

## Agent Execution Rules: review deltas

The constitution's Agent Execution Rules apply in full. Specific to this command:

- Never edit the script's logic to make a review pass; change `args` only.
- A refuter's "default to refuted when uncertain" is deliberate: the cost of a
  wrong fix is higher than the cost of a missed nit. Say in the report when
  that default plainly threw away something real, and let the user decide.
- No internal identifiers in anything written to source as a result of this
  review (Constitution II), apart from a whole-line `// @traces
  <feature>-FR-<n>` comment in a test file.

## The repair loop has a cap

Every fix-and-re-verify lap is counted:

```bash
node .claude/scripts/run-state.mjs repair
```

It exits 1 at the tenth lap (`SPECKIT_MAX_REPAIR_ITERATIONS`) and leaves
`.specify/run-state.json` at `status: blocked`, `blocking_condition:
repair-loop-exceeded`. Borrowed from BMAD's autonomous build, whose blocking
conditions include "review repair loop exceeded 5 iterations".

When it fires, stop and report. A cycle that has not converged in ten laps is
not one lap from converging: either a finding is wrong, or the requirement is,
and both are decisions rather than another edit.
