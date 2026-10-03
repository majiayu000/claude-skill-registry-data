---
name: adaptive-code-orchestrator
description: >
  Adaptively choose single-agent work, parallel reconnaissance, dependency
  waves, or independent review for reliable repository changes. Use for
  uncertain, cross-cutting, multi-file, long-running, or high-risk coding work
  where agent coordination may improve evidence or speed, or when the user
  asks how much agent coordination to use. When explicitly invoked for a small
  localized edit, stay single-agent and keep the workflow minimal.
---

# Adaptive Code Orchestrator

Make the smallest correct change with proof proportional to risk. Breadth is
for independent evidence; depth is for stateful execution and falsification.
Agent count is a cost, not a success metric.

## Authority and chain of command

The lead agent exclusively owns contract tracking, the global plan, shared
state, integration, and the completion claim. It enforces user-granted scope
and authority; it does not own or expand permissions. Workers receive bounded
questions or DAG nodes. They do not broaden scope, rewrite the objective,
merge their own work, or certify completion.

Prefer a one-level star for ordinary coding work:

```text
user -> lead -> optional scouts or isolated implementers -> lead
                                                       -> optional risk verifier
```

Add another delegation level only for a genuinely self-contained subtree that
cannot be managed directly. Do not create hierarchy merely to relay status.
Give every level the same evidence standards and authority boundaries, not the
same evidence payload.

Workers are read-only by default. Parallel writers require disjoint ownership
and isolated worktrees or equivalent sandboxes. Never allow concurrent writers
to mutate the same working tree.

## Start with the task contract

Use the full contract before delegation or when the work crosses a subsystem,
changes a shared or public invariant, lacks a direct acceptance check, or
touches persistence, money, authorization, security, concurrency, migrations,
deployment, external systems, or irreversible state. For a localized reversible
edit with a direct check, use a one- to three-line contract and remain SOLO.

```text
OUTCOME: user-visible result
ACCEPTANCE: observable evidence that proves it
NON-GOALS: nearby behavior that must not change
AUTHORITY: allowed reads, writes, external actions, and approvals
BASELINE: current behavior and repository state
UNKNOWNS: facts that could change the implementation
RISK: blast radius, reversibility, and costly failure modes
RECON: SOLO | SCOUT | FAN-OUT
EXECUTION: SOLO | DAG-WAVES | SEQUENTIAL
REVIEW: SELF-CHECK | INDEPENDENT | ADVERSARIAL
SWITCH TRIGGER: evidence that would expand or contract the topology
STOP: success, partial, or needs-input condition
```

Keep an obligation ledger separate from a progress ledger. The obligation
ledger holds the stable contract and invariants. The progress ledger holds
claims, evidence, disproved hypotheses, edits, tests, and open gaps. Keep both
in working context unless the user explicitly requests or authorizes a durable
artifact. A worker may update evidence, never the contract.

If an unknown is an irreducible user or product choice—such as the target,
desired behavior, compatibility contract, rail set, or risk tolerance—stop
before editing and ask one concise question. Do not infer the choice or delegate
workers to manufacture it.

## Choose the smallest useful topology

Choose reconnaissance, execution, and review independently. Use **SOLO**
reconnaissance when the change is localized, sequential, reversible, well
specified, and has a direct verification command. This is the default.

Use **SCOUT** for one bounded uncertainty where an independent read-only pass
would materially change the plan or review it.

Use **FAN-OUT** only when at least two independent uncertainty classes exist,
such as competing root causes, separate product surfaces, more evidence than
one context can inspect reliably, or orthogonal security, performance, and API
contract questions. Start with the smallest wave that covers those classes,
normally two to four sealed scouts. Diversity must come from different
hypotheses, evidence channels, tools, or surfaces—not cosmetic role names.

Use **DAG-WAVES** execution when implementation nodes have explicit
dependencies and unblocked nodes can be edited in isolation. The lead
integrates in dependency order and verifies after each wave.

Use **SEQUENTIAL** execution when work shares files or runtime state, has a
narrow critical path, or affects money, authorization, migrations, deployment,
security boundaries, or irreversible state. Use one writer and deterministic
verification.

Use **INDEPENDENT** review for changes spanning product surfaces or public
contracts and for any persistence, money, authorization, security, concurrency,
migration, deployment, external-system, or irreversible-state change. Use
**ADVERSARIAL** review only when a high-risk finding remains ambiguous: one
critic may challenge unsupported review claims; do not convene a voting
council.

Do not fan out merely because slots are available. If one root cause gates all
work, drill it first. If coordination, context duplication, merge risk, and
verification cost exceed the value of independent evidence or latency saved,
stay concise.

## Breadth-depth oscillation

The phases are conditional, not a required ritual. SOLO runs seed depth and
the depth drill. SCOUT adds one bounded read-only check. FAN-OUT uses a breadth
wave and convergence. DAG-WAVES applies only to isolated execution nodes.

### 1. Seed depth

The lead first discovers enough repository structure to partition honestly:
canonical sources, current behavior, relevant definitions and calls, tests,
shared invariants, and the first unproved edge. Do not delegate an unbounded
"understand the repo" task.

### 2. Breathe out

Only when SCOUT or FAN-OUT reconnaissance was selected, dispatch one scout or
an independent wave respectively. Give each a sealed packet with one
decision-changing question, exact scope, constraints, evidence priority,
falsifier, and return schema. Workers form initial findings before seeing peer
conclusions. They return compact evidence deltas, not transcripts.

### 3. Breathe in

The lead merges findings into the progress ledger, deduplicates by claim and
artifact, preserves minority findings, and reconciles contradictions. Evidence
outranks consensus in this order:

```text
reproduced runtime or executed checks
> compiler, type, static, and structural evidence
> exact source inspection
> canonical documentation
> agent judgment
```

Agreement alone never authorizes an edit. Resolve a disagreement with the
cheapest discriminating test, trace, or canonical source check.

### 4. Drill depth

Choose the smallest falsifiable implementation path. Reproduce or capture the
baseline, trace the affected call/data chain, make the minimal edit, and run a
focused check. Explore multiple repair candidates only when selection can be
grounded in executable or structural evidence.

### 5. Reopen breadth only on new information

Use one SCOUT when a failed gate creates one bounded decision-changing unknown.
Breathe out into FAN-OUT only when it creates at least two independent unknowns.
Otherwise remain in depth. Remove a role when its evidence channel is
exhausted.

For fan-out, DAG execution, review packets, ledgers, and merge gates, read
[references/orchestration-protocol.md](references/orchestration-protocol.md).

## Verification gate

Before editing, establish the acceptance obligations, baseline, relevant
callers and user surfaces, canonical implementation source, and verification
commands. After editing:

1. Inspect the exact diff and account for every changed line.
2. Run the focused reproduction or acceptance check.
3. Run type, compile, lint, integration, or regression checks proportional to
   the blast radius.
4. Discover the canonical caller or surface entity independently of the target
   qualifier, cover native representation variants, and reconcile every
   observed instance that shares the changed invariant. If exhaustive coverage
   cannot be established, report PARTIAL with the exact boundary.
5. When the change meets the INDEPENDENT or ADVERSARIAL review criteria above,
   give the reviewer the contract, diff, and raw evidence without the
   implementer's verdict.
6. Re-run the decisive checks after integration.

A reviewer supplies hypotheses, not authority. Worker self-reports and passing
tests alone do not prove intent fit or coverage.

## Stop and report honestly

Stop breadth when every independent uncertainty class has evidence, another
worker would duplicate an existing channel, or the last wave added no
decision-changing candidate or falsifier. Do not start a second wave unless the
first reveals a named new frontier.

Stop a depth branch when it is disproved, dominated by a better verified path,
or repeated work produces no new discriminating evidence. Reformulate rather
than adding agents to a stale hypothesis.

Report:

- **VERIFIED** only when every acceptance obligation maps to observed evidence
  and no material unexplained diff or cross-surface gap remains.
- **PARTIAL** when useful work exists but access, environment, test coverage,
  authority, or another named gap prevents the requested strength of claim.
- **REJECTED** for a hypothesis killed by a specific counterexample.
- **NEEDS INPUT** when required progress needs user authority or unavailable
  external state.

Finish with the selected mode, changes, decisive proof, residual risks, and why
more agents would or would not add a distinct evidence channel.

## Scientific basis

When the user asks why this protocol works, requests a research refresh, or
wants to tune the topology, read [references/evidence.md](references/evidence.md).
Treat it as a dated evidence snapshot and browse current primary sources before
claiming it is the latest research.
