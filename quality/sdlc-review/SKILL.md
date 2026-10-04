---
name: sdlc-review
description: Invoked explicitly by /review. Reviews a diff, file or use case against the project's production standards and against the specification it was meant to implement, then writes the findings to state so the development loop can route them. Reports only — never applies changes.
argument-hint: "[path | FEAT-ID | staged]"
disable-model-invocation: true
---

# /review — quality review

## Protocol (shared — do not restate here)
Framework assets — `.agent/framework.yaml`, `.agent/steps/`, `.agent/rules/`,
`.agent/gates/`, `.agent/templates/`, `.agent/modules/` — resolve **project-first**: use
the repository's copy when it exists, otherwise `${CLAUDE_PLUGIN_ROOT}/.agent/…`. That is
how one repo can override a single template or rule without forking the framework.
`.agent/project-context.yaml` and `.agent/state/` are **always project-local** — never
read or write them under the plugin root.
1. If `.agent/state/context-cache.md` exists and its `framework_version` matches
   `.agent/framework.yaml`, Read ONLY that file. Otherwise Read
   `.agent/steps/context-loader.md` and execute it, then write the digest back to the cache.
2. Read `.agent/steps/gate.md` and execute it with the phase inputs below.
3. On completion, format output per `.agent/steps/report-footer.md`.
Never copy the contents of those files into this skill.

**Phase inputs** — phase `review`, gate `G6`, template
`{{paths.templates_dir}}/review-report.md`, output
`{{paths.review_dir}}/{FEAT-ID}/RV-{nnn}-{phase}.md` + rows in `{{paths.findings}}`.
Read-only: skip gate Step 4 (CHECKPOINT).

---

## Step 1 — Input check

Gate Step 2.7 has already run `.agent/steps/input-check.md` against
`input_contracts.review`. A review needs two things: a change, and the specification the
change claims to satisfy.

- `NOT_READY` with no specification — say so and **stop**. A review with no spec collapses
  into a style opinion, which is the least valuable thing a reviewer can produce and the
  easiest to argue with.
- `PARTIAL` — no recorded test run. Proceed, and say in the report that test results were
  not available rather than implying the change is untested.
- `READY` — proceed.

## Step 2 — Resolve the target

`staged` → the staged diff. A path → that file or directory. A FEAT-ID → the diff of its
branch against the default branch, scoped to the feature's `scope.entrypoints` and the
components in its techdoc. No argument → the working diff.

Also gather the artifacts the change claims to satisfy: the `.feature` scenarios, the SRS
requirements, the techdoc component map, the test catalog, and `quality.json`.

## Step 3 — Delegate to `quality-guardian`

Hand the target, the specification artifacts and the slim context to the
`quality-guardian` agent. It has `Read, Grep, Glob, Bash` and deliberately **no Write or
Edit** — the review contract promises not to auto-apply changes, and an agent holding a
pen does not keep that promise.

For a large change, fan out by area per `.agent/steps/spawn-agent.md` and merge.

## Step 4 — Review against the spec first

The order matters. Check whether the change does what the scenario says **before**
checking how it is written. Style findings on code that should not exist are wasted
work, and they crowd out the finding that mattered.

Then the standards: architecture layering, SOLID, DRY at the Rule of Three, KISS, YAGNI,
naming, types, docstrings, error handling, test quality, documentation currency.

Run the project's own tools — `lint`, `format_check`, `typecheck`, `test`, `coverage` —
and quote their real output. Do not report a style opinion the configured linter does not
hold; the linter configuration is the project's decision, not the reviewer's to
relitigate.

## Step 5 — AI review (when `ai_class != none`)

- Prompt **version bumped**, not edited in place
- Input guardrails before the provider call; output parsed and validated, never trusted
- Context-engineering rubric: clarity (would two agents read this identically),
  completeness (can it act without asking), relevance (does every sentence change
  behaviour), consistency (can all rules hold at once)
- System prompt token count against the budget in `ai_conventions.budgets`
- Cost per call and p95 latency against the prompt spec
- **Eval delta versus baseline** — the number that decides whether quality moved

## Step 6 — Write findings to state

Every finding becomes a row in `{{paths.findings}}`:

```
id	feat_id	opened	severity	category	found_in	route_to	ref	title	status	closed
```

`id = RF-{FEAT-ID}-{nnn}`. `route_to` comes from `framework.yaml → loop_routes`.

**A finding without a route is invisible to the loop.** The router acts on `route_to`; a
finding that only exists in the report is a finding nobody will act on.

Severity discipline:

- **blocker** / **major** — block G6 and drive a loop-back. Each must name a concrete
  failure: inputs, state, and the wrong result.
- **minor** / **nit** — never block, never loop. Carried as tech debt.

Inflating severity to force attention destroys the signal the router depends on, and it
is the reason review backlogs stop being read.

## Step 7 — Write the report

Use the template. It keeps the established format — Summary verdict `ship | revise |
block`, Findings with severity, category, location, problem and a concrete fix diff,
Documentation Impact, Suggested Next Actions — and adds `## Traceability`,
`## Prompt & cost review` and `## Findings written to state`.

## Step 8 — Evaluate G6 and record

Run `.agent/gates/G6-review.yaml`: verdict `ship`, zero open blocker or major,
documentation impact resolved, trace green or waived.

On `pass`: set `phase: done`, move the feature file to `.agent/state/archive/`, remove it
from `current.yaml → features`, and suggest the PR.

On `revise`/`block`: leave the feature open. The next `/sdlc` reads the findings and
routes to the earliest `route_to` among them.

---

## Boundaries

- **Never apply changes.** Propose diffs. This is the contract, and it is what lets the
  review be honest about things the reviewer would rather not have to fix.
- Do not rewrite working code that already meets the standards for taste.
- Do not invent requirements. If a standard does not apply here, say so explicitly.
- Escalate rather than decide: architecture changes, new dependencies, breaking API
  changes, and any AI ADR trigger go to the user with a recommendation.
- If a check could not be run, report it as `unknown`. Never report `pass` for something
  you did not verify — a review that overstates its coverage is worse than no review,
  because it stops anyone else from looking.
