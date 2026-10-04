---
name: keel
description: >
  Measure whether a codebase's verification actually touches the world, or
  whether it is checking itself. Keel gathers the verification edges it can
  read in a target (GitHub Actions, CircleCI, GitLab CI, Travis, package
  scripts, Makefile, Rakefile, pyproject and a dozen tool configs) — and
  reports the surfaces it recognised but could not parse, so blindness never
  passes for absence. It classifies each edge as anchored, self-referential, or
  unknown by
  asking whether the actor being verified can write to the signal's producer,
  and reports a grounding ratio. Novel cases are judged by the agent and then
  crystallized into probes — small reviewable scripts — so repeat shapes get
  cheaper every run. Then routes each ungrounded check to an anchored signal
  that already exists in the same graph. Use when: (1) auditing whether
  AI-generated or agent-maintained work is genuinely verified, (2) assessing
  how AI-native a codebase actually is — measured by what fraction of its
  verification the agents cannot author, (3) reviewing a CI/CD pipeline for circular
  verification, (4) someone claims tests pass and you want to know what that
  claim rests on, (5) measuring verifier independence. Triggers on keel,
  grounding ratio, grounded, is this actually verified, who checks the checker,
  circular verification, self-referential verification, verifier independence.
license: MIT
metadata:
  version: "1.0.0"
  homepage: "https://github.com/broomva/skills/tree/main/skills/governance/keel"
primitive: null
category: governance
required: false
introduced_in: "0.38.0"
---

# Keel

A ship's keel is the reference line everything else is measured from. It is
also what keeps the ship from capsizing — an even keel is a stability
property, not a decoration.

Keel measures one thing:

> **A check is only a check if the signal it reads comes from somewhere the
> thing being checked cannot write to.**

Most verification in an agent-maintained codebase fails this. An LLM reviews
what an LLM wrote. A doc is validated against another doc. A status field says
"passed" because something set it to "passed". The pipeline is green and
nothing has been verified.

## Where the predicate comes from

Silver & Sutton (*Welcome to the Era of Experience*, 2025) argue that agents
must replace human-prejudged reward with **grounded** signals, "that arise from
the environment itself", because a human rater imposes "an impenetrable ceiling
on the agent's performance" and, ungrounded, an agent "will become an echo
chamber of existing human knowledge."

Grounded and independent are not the same property, and the paper only asks for
the first. Its own signal inventory — "cost, error rates … profit, sales …
visits, yields, stocks, likes … accuracy" — mixes producers the actor cannot
touch with producers it operates; and the success case it cites, **execution
feedback** ("the agent actually runs code and observes what happens"), is
maximally grounded *and* the canonical reward-hack surface, because the agent
writes the test.

Keel asks the second question — *and can the thing being measured write to it?*
That is the classification predicate below, and the reason `unknown` fails
closed: an abundance of grounded signals is not an abundance of independent
ones.

## The classification

Every verification edge gets exactly one class. The question is never "is this
a good check" — it is **who produces the signal, and can the actor write to
that producer?**

| Class | Means | Examples |
|---|---|---|
| `anchored` | The producer is outside the actor's write boundary | a test process exit code, a type checker, a payment that settled, a third-party API, a customer action, an independent prober |
| `self_referential` | The producer is inside it | an LLM judging output, a doc checked against a doc, a self-set status field, an agent asserting it completed |
| `unknown` | The fork point could not be established | anything you cannot trace |
| `not_a_check` | It asserts nothing about correctness | a dev server, a help target, a formatter that only rewrites, a step that cannot fail (`\|\| true`, `echo ok`) |

`unknown` **fails closed** — it counts against the ratio, exactly like
`self_referential`. Absence of evidence of dependence is not evidence of
independence. And `unknown` is never settable by the thing being measured:
if the target could choose its own class it would never choose `unknown`.

`not_a_check` is **excluded from the ratio** — a node that asserts nothing
would be a lie in either column. But it is the one **shoppable** class:
mis-filing a real check here shrinks the denominator and inflates the score.
So it carries the same burden of argument as any other verdict, the report
prints its count beside the ratio, and the audit samples it like everything
else. If you reach for it because a node is *hard*, the honest answer is
`unknown`.

Grounding ratio = `anchored / (anchored + self_referential + unknown)`.

## The loop

Run these in order. Stages 3 and 4 are optional — stage 2 alone produces a
complete, honest report.

## Run it

The scripts are plumbing — they locate, merge, validate, render and sandbox.
**Every judgment in the run is yours.** Paths are relative to the installed
skill; substitute wherever your harness put it.

```sh
# 1. locate the surfaces (mechanical, no model call)
bun <skill>/scripts/gather.ts <target> --json > nodes.json \
    --coverage coverage.json          # what it recognised but could not read

# 2. try the probe cache; everything it cannot decide comes back to you
bun <skill>/scripts/classify.ts nodes.json --json > classified.json
bun <skill>/scripts/classify.ts nodes.json --batches   # the same nodes, batched for judging

# 3. YOU judge every pending node over its `raw`, and write Verdict[] to verdicts.json

# 4. merge and validate — refuses on an unjudged node, a naked argument, a bad class
bun <skill>/scripts/assemble.ts nodes.json classified.json verdicts.json \
    --dir <target> --probes <skill>/probes -o report.json

# 5. the artifact
bun <skill>/scripts/render.ts report.json -o report.html

# optional
bun <skill>/scripts/route.ts report.json --dispatch      # then author RouteProposal[]
bun <skill>/scripts/route.ts report.json --proposals p.json -o bindings.json
bun <skill>/scripts/audit.ts report.json --sample 0.1    # the ε-audit; see §4
```

`assemble` is the step that keeps the arithmetic honest: it recomputes the
grounding ratio from the verdicts rather than trusting any block you hand it,
and it **refuses** rather than quietly computing a ratio over the nodes that
happen to have verdicts. A report silently computed over a subset is the exact
failure this tool exists to detect.

### 1. Gather (mechanical)

Find candidate verification edges. This step *locates surfaces*; it does not
judge them. Look at CI workflow definitions, package/task/make scripts, test
configuration, review and branch-protection requirements, deploy and promotion
conditions, and any wired integrations. Emit `Node[]` per `schemas/keel.ts`.

`gather` reads what it knows how to read. Pass `--coverage <file>` and it also
records the surfaces it **recognised and could not parse** — a `Jenkinsfile`, a
`.buildkite/`, a `build.gradle`. Carry that into the report: a ratio computed
over the residue of a repo whose real CI is Jenkins is not a measurement of that
repo, and non-coverage that goes unreported is Keel's own shoppable class.

Carry the **literal snippet** into `raw`. Downstream reasoning happens over the
real text, never over a summary you wrote — a summary is already a judgment.

### 2. Classify (agentic, cache-first)

For each node:

1. **Try the probe library.** Load probes from the shipped `probes/` directory
   and from `~/.config/keel/probes/`. Run `match(node)`; on a hit, run
   `assess(node)`. A non-null result is the verdict — record `decidedBy:
   'probe'` and move on. This costs no tokens.

   Probe code is executed by loading it, so **loading and running probes happen
   only inside a separate child process** with a kill-timer held by the parent:
   a synchronous `while(true)` cannot be preempted in JS, so an in-process time
   guard is fiction. A probe that throws, hangs, or exceeds the budget is skipped
   with a warning and its nodes fall through to your judgment — never fatal to
   the run.

   **That child is sandboxed on macOS only.** `sandbox-exec` exists nowhere
   else, so on Linux and Windows the child gets a stripped environment and the
   kill-timer and nothing more: a probe there can write files, reach the
   network, and spawn processes. Say so if you report on probe provenance, and
   see `SECURITY.md` for the enforced-vs-not table. A run that had to ignore
   part of its own configuration — a `KEEL_*` variable a dotenv in the target
   tried to set — records that in `warnings`; carry it into the report.
2. **On no match, or on abstention, judge it yourself.** Read `raw`. Ask the
   only question that matters:

   > What actually produces this signal, and can the actor being verified
   > write to it?

   Trace the causal path. A test command is anchored because the runtime
   decides the exit code and no amount of persuasion changes it. An LLM review
   step is self-referential because the same class of system that produced the
   work produces the assessment. A deploy check that reads a status field the
   deployer sets is self-referential no matter how many green checkmarks it
   renders.

   Fill `writeBoundary.argument` with the causal path, not a restatement of the
   class. "Self-referential because it is self-referential" is a failed verdict.
   If you cannot trace it, say `unknown` — that is a real answer and it is
   often the correct one.

See `references/grounding-classes.md` for worked cases, including the ones that
look anchored and are not.

### 3. Crystallize (optional)

When you judged a node the library could not, and the shape will recur, write a
probe to `~/.config/keel/probes/<id>.v<n>.ts` implementing the `Probe` interface.
Probes are versioned in the filename because `ProbeMeta.version` exists and two
versions cannot share one path: minting never overwrites, it writes the next
version, and the loader takes the highest version per id and warns about the
ones it shadowed. Set `KEEL_PROBE_DIR` to point the library somewhere else.

Rules:

- A probe **abstains** (`return null`) whenever it is unsure. It may never
  return `unknown`. Abstention costs a model call; a wrong confident probe
  costs correctness.
- Generalize the *shape*, never the specific repo. `match` keys on structure.
- One probe, one shape. A probe matching everything is a rule table wearing a
  costume, and it will rot.
- Probes are code so they can be read, diffed, tested, and rejected. Keep them
  small enough to review in under a minute.

Minted probes live in `~/.config/keel/probes/` so a skill update never destroys
them. Contribute one back by copying it into the skill's `probes/` directory in
[broomva/skills](https://github.com/broomva/skills) and opening a PR — that is
how the library compounds across everyone who runs Keel.

### 4. Audit (optional, and the honest part)

Probes drift. A generalization that over-matches will mis-classify silently
forever, and the failure is invisible precisely because it is cheap.

So: sample a fixed fraction of probe-decided nodes — start at ~10% — and
re-decide them agentically **with the cached verdict hidden from you.** Record
the comparison in `verdict.audit`. On disagreement, narrow the probe's `match`
or retire it.

`audit.ts` is a stepper, for the same reason `corpus.ts` is: it cannot re-decide
anything, because deciding is yours.

```sh
bun <skill>/scripts/audit.ts report.json --sample 0.1 --seed 1 -o pending.json
# it prints the sampled nodes WITHOUT their cached class, probe, confidence or
# argument — you judge them cold, and write Verdict[] to redecided.json
bun <skill>/scripts/audit.ts record pending.json redecided.json --report report.json
```

The blindness is the whole mechanism. If you can see the cached verdict while
re-judging, the audit measures your agreement with yourself and nothing else.

The probe library's agreement rate is Keel's own counter-metric. Report it
**with its denominator** — "1.00 over 10 compared nodes" — because a rate over
three nodes and a rate over three hundred are different claims. A system that
measures groundedness while refusing to measure its own is telling you
something.

`record` reports disagreement and names the probe. It does not retire anything:
retiring a probe is a judgment about the world, and that stays with a human.

## Output

Write `Report` (see `schemas/keel.ts`) as JSON, then render a self-contained
HTML report alongside it. The HTML carries the grounding ratio, the node graph
with each class, the write-boundary argument for every verdict, and — across
runs — the crystallization curve of cost per node as the probe library grows.

**The ratio never travels alone.** Print the absolute anchored count and the
gathered-surface coverage (nodes by kind) beside it, always. A 1.0 over one
edge and a 0.7 over fifty are different claims, and a bare ratio rewards
*deleting* checks — the pair is the guard. A target with zero gathered nodes
gets an explicit "nothing gathered" state, never a ratio.

Report `unknown` prominently. It is the most honest number Keel produces.

## Modes

Keel is one skill with modes, not a family of skills.

| Mode | Reads | Emits |
|---|---|---|
| `keel measure` | a target | `Report` — the four stages above |
| `keel route` | a `Report` | `Binding[]` — a route from each ungrounded check to an anchored signal already in the graph |
| `keel audit` | a `Report` | the probe library's agreement rate, with its denominator |
| `keel construct` | `Binding[]` | counter-metric pairings, arbitration, audit loops — **not yet built** |
| `keel apply` | `Binding[]` | a diff or PR — gated, **never completed by an agent** |

### The routing rule

**Independence cannot be manufactured, but it can be routed.** A route may only
point at a node that is present in the same report *and* already classified
`anchored`. Validate that in code — a proposal that fails the check becomes
`null` with a reason. "No route found" is a first-class answer and is correct
whenever the fix needs a policy decision rather than a rewiring.

Route mode runs in three steps: `--dispatch` emits the judgment payload, the
agent authors `RouteProposal[]` from it, and `--proposals` validates those into
bindings. A proposal may carry an **`effort`**, and the only legal values are:

| `effort` | means |
|---|---|
| `config` | a value in a file that already exists — a flag, a limit, a `needs:` edge, an existing job's `if:` |
| `wiring` | new plumbing between things that already exist — a step that reads an artifact another step already produces |
| `process` | a change to how people or systems behave — a required check, a branch-protection rule, a third party's involvement |

`--dispatch` carries that same list, with the same distinctions, in
`effortValues` — so a proposal can be authored from the payload alone. Effort
**ranks** cheapest-first and never scores; there is deliberately no numeric
weight, because a cost is one step from an objective over the ratio. An
unrecognised value is warned about and dropped, never coerced to a default —
and since a dropped effort is no effort, that route sorts behind every route
that stated one. Omitting `effort` is legal and silent, and lands in the same
tier: "we did not say" is not cheap, it is unmeasured. Only an `effort` the
proposal itself declares counts — one inherited from the prototype chain is not
something the agent authored, so it is ignored.

Routing never moves the ratio. A proposal is not a change. The number moves
only when a human applies one and Keel re-measures **from the target** — the
world stays in the loop, so a route's claim never asserts its own outcome.

### The edge that must stay open

The router receives **verdicts** — what is ungrounded and why. It must never
receive the **ratio as an objective**. The moment the score becomes something
to optimize, it becomes a selection signal, and the router hill-climbs into the
scorer's blind spot: the number keeps rising while it stops meaning anything.

*Inform freely, optimize never.*

This is not enforced by putting the router in a separate skill — a package
boundary asserts nothing, and would itself be a `not_a_check`. It is enforced
by a test: fabricate an adversarial bindings file claiming everything is
routable, re-measure, and assert the verdicts and grounding come back
byte-identical.

## Scope

Keel measures the *shape* of verification, not its quality. A repo can be 100%
anchored and have terrible tests. Anchoring says the signal comes from outside;
it does not say the signal is sufficient. Do not let a high ratio be read as
"well tested", and say so in the report.
