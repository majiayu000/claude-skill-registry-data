---
name: designing-distributed-system-tests
description: >-
  Design claim-driven test plans for distributed or stateful systems with persistence, replication, consensus, retries, idempotency, async messaging, multi-tenancy, or partial failure. Supports change-scoped and project-wide plans, including existing-test inventories and gap analysis. Use for stability, release-validation, durability, partition, crash-recovery, upgrade, linearizability, deterministic-simulation, SQL semantics or compatibility, tenant isolation, authz, namespace boundaries, fairness, and noisy-neighbor testing. Investigate claimed guarantees and design scenarios to falsify them during normal operation and under relevant faults. Also use for "what should we test for this change", "are my tenants isolated", or "make a holistic test plan".
---

# Designing Distributed-System Tests

The default for testing distributed and stateful systems — write a few
integration tests and call it done — finds a small fraction of the bugs
that actually break these systems in production. This skill enforces an
opinionated workflow: scope the change, generate failure-mode hypotheses
that cover the categories the literature says matter most, pick
techniques from a curated catalog, and emit a structured plan file that
the executing-distributed-system-tests skill (or a human) can run.

## Plan modes

This skill produces two shapes of plan. Decide which one applies before
you start; the steps below branch on it.

- **Change-scoped** — the default. Use when the caller names a commit,
  PR, branch-diff, or feature. The plan covers what *this change* could
  regress, scoped by its blast radius.
- **Project-wide** — use when the caller asks for a "release-validation
  plan", "stability plan for the whole system", "test plan to enough
  coverage", "what should we be testing", or otherwise frames the
  request without a specific change. The plan covers what *the system*
  should be tested for, with an explicit inventory of existing tests
  and a gap analysis driving the new-scenario list.

If the framing is ambiguous, ask once before starting — the modes
diverge enough that retrofitting one into the other wastes work.

## Process

Follow these steps in order. Do not skip; the order matters because
later steps depend on artifacts the earlier steps produce.

### 1. Scope the system

Read the project's entry points: `README`, `AGENTS.md` or `CLAUDE.md`,
top-level `docs/`, any existing test-plan or runbook files. Note:
- Tenancy / isolation model
- Persistence model (what is durable, fsync contract)
- Replication / consensus protocol, quorum, leadership
- Ordering guarantee exposed to clients
- Network boundaries (which RPCs / streams)
- Retry / idempotency contract
- Observability (logs, metrics, traces) available to an oracle

Write this as a one-paragraph SUT model. If anything is ambiguous from
the repo, ask the user before proceeding — do not invent guarantees.

### 1b. Extract claims and guarantees

A good test plan exists to falsify what the product *claims*. Before
generating hypotheses, write down what the SUT promises its users.
This is the spine the rest of the plan hangs off — every hypothesis,
every scenario, every oracle should be traceable back to a claim it
either confirms or refutes.

Sources to mine:
- README "guarantees" / "what we offer" sections
- API docs / reference manuals
- ARCHITECTURE / DESIGN docs (claims about consistency, durability,
  replication, fault tolerance)
- Public blog posts, talks, marketing material (if any)
- The code itself: function names, doc-comments on public APIs,
  error types (`IdempotencyConflict`, `StaleRead`, etc.) imply
  guarantees the system claims to enforce
- Existing test names (a test called `linearizable_under_partition`
  implies a linearizability claim under partition)

Categorise each claim:
- **Safety** — "the system never returns a stale read", "no
  acknowledged write is ever lost", "linearizable per key"
- **Liveness** — "every accepted operation eventually commits",
  "leader election completes within N seconds of crash"
- **Durability** — "fsync'd writes survive crash", "replicated
  writes survive single-AZ loss"
- **Performance / SLO** — "p99 append latency ≤ X ms at Y ops/s
  per session"
- **Operational** — "rolling upgrade is non-disruptive",
  "configuration changes are atomic"
- **Idempotency / dedup** — "same idempotency key never produces
  two committed effects"
- **Isolation** — "tenant A's reads never observe tenant B's writes",
  "no read returns data from a transaction that has not yet
  committed"
- **Ordering** — "consumers always see messages in the order the
  producer sent them", "every reader sees a prefix of the global
  log order"
- **Membership** — "a node that fails its liveness probe is removed
  from the cluster membership view within N seconds", "every joined
  member appears in the membership table exactly once"
- **Boundary** — access-boundary semantics: "tenant A's data is never
  reachable from tenant B on any surface", "a request scoped to
  namespace X never routes to namespace Y". Subsumes tenancy / authz
  / namespace / routing / multi-protocol; do not file those as
  separate categories. Triggers the §7.M.S surface-decomposition
  discipline (see step 3 and `references/boundary-and-isolation-testing.md`).
- **Fairness** — per-group performance and noisy-neighbor isolation:
  "no tenant can starve another for throughput", "one shard's load
  does not blow another shard's p99". Group can be tenant, shard,
  queue, partition, region, priority class, user, table, or workload
  class. Also triggers §7.M.S.

If the project does NOT explicitly document a claim that appears
in the code, write it as an *inferred* claim and mark it as such —
inferred claims are still testable, and surfacing them often
catches places where the docs lie or are silent about real
guarantees the implementation depends on.

Bind safety-critical claims to a version and configuration: artifact/build,
startup mode, session settings, durability mode, and client/protocol.
Preserve disagreements between manuals, CLI help, and observed defaults.
Plan effective-setting inspection and distinguishing behavioral probes;
an accepted setting, familiar alias, or "safe" label is not proof of a
consistency model. Keep unresolved contradictions in §1c.

When done, you should have a numbered claims list (C1, C2, …). The
hypothesis-generation step (step 3) will reference these by number,
the coverage matrix (template §5) tracks claim × hypothesis, and
scenarios (template §7) state which claim(s) each is trying to
falsify. If a hypothesis cannot
be tied back to a claim, either name the missing claim explicitly
or drop the hypothesis — untethered hypotheses produce ceremonial
scenarios.

**Missing claims are a first-class finding.** During hypothesis
generation (step 3) you will encounter behaviors the implementation
relies on that no claim covers — Unicode normalisation policy,
specific timeout windows, edge-case error semantics. List these
in the plan's "Missing claims discovered" section (template §1c).
Surfacing them is one of the highest-value outputs of the whole
exercise: it tells the maintainer where docs and implementation
have drifted apart.

### 2. Scope the change OR the project

**Change-scoped:** Identify the commit, PR, or feature under test.
List every file touched and the surfaces (RPCs, on-disk formats,
replication messages, public APIs) affected. Build a one-paragraph
blast-radius statement.

**Project-wide:** No specific change. Instead, enumerate the system's
externally observable surfaces (public APIs, on-disk formats, wire
protocols, replication/consensus, background jobs, operational
controls) and the invariants each must preserve. Declare what is
in-scope and what is explicitly out-of-scope (adapters, ancillary
tools, demo apps) — a project-wide plan that tries to cover
everything covers nothing well.

### 2b. Inventory existing tests (project-wide only)

Walk the SUT's test surface: unit tests, integration tests, fault-
injection / stability harnesses, smoke scripts, CI workflows, and
any test-plan / runbook docs. For each notable test or harness,
capture: what subsystem, what invariant it pins, and what failure
modes it would catch. This becomes the left-hand column of the
coverage matrix in step 4b.

Do not re-test what is already covered well. The point of the gap
analysis is to surface what is NOT covered.

### 3. Generate failure-mode hypotheses

For each claim from step 1b, ask: under what conditions could the
SUT fail to honor this claim? Each hypothesis must be tied to one
or more claims by number ("could falsify C3 and C7"). Tests exist
to refute claims, not to "check that things work" — a passing test
should mean "this claim survived this fault", and a failing test
should name the claim it falsified.

**Walk the pitfall catalog.** Before generating hypotheses from
intuition, open `references/common-distributed-systems-pitfalls.md`.
It lists 16 failure modes that recur across the Jepsen analyses
corpus, each with a hypothesis template ready to paste-adapt. For
every pitfall, decide if it applies to this SUT: y / n / maybe.
Every `y` and most `maybe`s become hypothesis rows. This shortcut
prevents the common failure mode of plans that only test what the
agent already thought of.

Generate hypotheses for each touched surface (change-scoped) or
in-scope surface (project-wide) across these categories:
correctness, durability, liveness, partial failure, idempotency /
replay, upgrade / rollback, configuration, performance / fairness.

If a category is genuinely not applicable, say so explicitly. The act
of writing "N/A because…" surfaces wrong assumptions more often than
it sounds like it would.

**Boundary and fairness claims trigger §7.M.S.** When you encounter a
claim about tenant isolation, authz, namespace, routing,
multi-protocol access, compatibility across API surfaces, or
per-group fairness (noisy-neighbor, queue-group, per-region), tag it
with the `boundary` or `fairness` category in §1b. Both categories
trigger the surface-decomposition discipline in §7.M.S of every
scenario that falsifies them — see
`references/boundary-and-isolation-testing.md` for the boundary
claim matrix template and surface catalogs.

In project-wide mode the list is typically larger (the system has
more surfaces than any single change). Group hypotheses by subsystem
so the gap-analysis table stays readable.

### 4. Select techniques

Include meaningful no-fault correctness coverage before layering on faults:
minimal supported deployment with one client, then concurrency where relevant.
Reuse existing tests when they have a suitable oracle. For SQL semantics or
compatibility claims, read `references/sql-semantic-testing.md` to select
sequential differential and transaction-local checks. Fault injection does
not substitute for validating basic state transitions.

Open `references/catalog-index.md` and find the techniques that match
your hypotheses. For each technique you pick, open its reference file
and write down in the plan: which hypotheses it addresses, what it
would catch that other techniques would miss, the typical cost.

For scenarios that will be serious (any claim in `{safety, durability,
idempotency, isolation, ordering, membership}`), also open the
executing skill's `references/oracle-patterns.md` and use the
"Checker picker" table at the top to pick the checker(s) matching
your model and claim category. The checker choice is part of the
plan, not a runtime decision.

A change usually warrants 2–4 techniques in combination. One technique
is suspicious — re-check whether you've collapsed multiple distinct
hypotheses into one. A project-wide plan typically reaches further
across the catalog (5–7 techniques) because the surface is larger.

### 4b. Map coverage and identify gaps (project-wide only)

Build a table indexed by claim, not just by hypothesis. Each row:
the claim (C-number), the hypothesis that would falsify it, the
existing test(s) (from step 2b) that exercise it, the verdict
(covered / partial / not covered), and the gap kind (no test /
shallow test / oracle too weak / no fault-injection variant).
Sort by claim severity × gap so the highest-leverage gaps end up
at the top.

This table is the heart of the project-wide plan. It tells the
maintainer where the product's claims are unverified. Without it
the plan is just a wishlist.

**For very large systems (50+ claims, 100+ hypotheses), split the
matrix.** A per-claim summary table (one row per claim with rolled-
up verdict) gives the maintainer the at-a-glance view; a per-
hypothesis detail table keeps the granular gap-kind information.
Without the split, a single matrix where load-bearing claims appear
in many rows becomes unreadable.

### 4c. Declare environment requirements

For each technique you picked, list the runtime dependencies the
executing skill will need on the test box: container runtime
(docker / podman + compose), language toolchains (Rust, Go, Node,
Python at specific minima), database / object-store backends
(Postgres N+, MinIO / S3-compatible), fault-injection facilities
(iptables, tc/netem, libfaketime, dm-flakey, Toxiproxy), kernel
features (network namespaces for asymmetric partitions, cgroups
for IO throttling), observability tooling (Prometheus, OTLP
collector), and any project-specific binaries.

Put this in the plan's "Environment requirements" section as a
checklist with version floors where they matter. The executing
skill consults this list at its environment-capability probe step
and uses it to either guide the operator through install or mark
dependent scenarios INCONCLUSIVE.

### 5. Design scenarios

For each technique, write concrete scenarios. Each scenario must
specify: workload (what generator, rate, distribution, duration);
faults (schedule of what is injected when); oracle (the property
checked and how); observability required; and the three budget
tiers (Smoke / Hardening / Release — see the field list below).

Resist "logs look fine" as an oracle. The oracle must be a
machine-checkable property or a metric SLO with a defined threshold.

In project-wide mode, prioritise scenarios that fill the highest-
leverage gaps from step 4b, and tag each scenario with both the
hypothesis-rows it closes AND the claim(s) it tries to falsify.
Long-tail "nice to have" scenarios go into template §9 (open
questions / followups), not the actionable scenario list in
template §7 — the plan should be actionable, not aspirational.

Every scenario name should encode the claim it targets:
`linearizable_per_session_under_partition`,
`durability_survives_fsync_loss`, `idempotent_replay_across_restart`.
A test named after its claim is harder to weaken; a test named
after its setup ("3-node cluster with chaos") tells you nothing
about what it actually verifies.

**Each scenario is an executable spec.** Beyond the prose
fields (Workload, Faults, Oracle, Observability, and the three
budget tiers), emit two more:

- **Target test file** — the relative SUT path where this test
  will live if/when it becomes a permanent regression. Follow
  the SUT's test conventions: for Rust crates `crates/<crate>/tests/auto/<S_id>_<slug>.rs`,
  for Go modules `<module>/<pkg>_test.go`, for Python pytest
  `tests/auto/test_<slug>.py`. The `auto/` subdirectory makes
  generated tests easy to find and review separately from
  hand-authored ones.
- **Skeleton** — a language-specific code block with imports,
  the test function signature, and TODO regions for the
  workload / faults / oracle bodies. The skeleton MUST include
  an `AUTO-GENERATED` header comment with the plan path and
  scenario id so a reviewer can trace any committed test back
  to its spec.

The skeleton is what the executing skill (in author mode) writes
to the target path and then fills the TODOs from. The plan +
the generated test are traceable back to each other; if the
plan's prose changes, the test should be regenerated.

**Fill §7.M for serious scenarios.** If any claim in this scenario's
`Falsifies if it FAILs` row belongs to `{safety, durability,
idempotency, isolation, ordering, membership}`, the scenario is
*serious* and must fill the §7.M sub-block in the plan template.
A scenario that decomposes into §7.M.S arms (boundary / fairness) is
also serious: each arm is always serious and carries its own §7.M
block, regardless of claim category — the executing skill scores
every arm through the §7.M checker node of the verdict decision tree.
The §7.M sub-block:

- **Model under test** — pick from the picker in
  `references/history-discipline.md`.
- **Operation history** — which of the default 11 fields the recorder
  captures; the recording mechanism (in-process / external / server-
  side / combined).
- **Checker** — name from the executing skill's
  `references/oracle-patterns.md` "Checker picker" table at the top
  of that file. Or, if no checker, write the justification.
- **Nemesis + landing evidence** — nemesis from the executing skill's
  `references/fault-injection-howto.md`, plus the observable signal
  that proves the fault landed. For an intentionally no-fault scenario,
  write `none — intentional no-fault correctness campaign`; retain the
  model, history, checker, and budget requirements.
- **Ambiguous outcomes** — how the recorder treats timeouts, unknowns,
  retries, duplicates.
- **Reduction plan** — minimisation recipe + the SUT/harness/checker/
  env classification step from the executing skill's
  `references/test-case-reduction.md`.

For non-serious scenarios (perf-SLO, liveness, operational), write
`§7.M: not applicable (no gated claim category falsified)` and move
on. Do not invent a model just to fill the field.

The §7d confidence statement should lean on the chain ("checker X
consumed history Y under nemesis Z with landing evidence E") for
every serious scenario. A serious scenario whose §7.M is partially
filled cannot contribute to a hardening claim.

**Fill §7.M.S for boundary and fairness scenarios.** If any claim in
this scenario's `Falsifies if it FAILs` row belongs to
`{boundary, fairness}`, the scenario is *surface-decomposition
mandatory* and must fill the §7.M.S sub-block in the plan template:

- **Surfaces** — drawn from the catalog in
  `references/boundary-and-isolation-testing.md`, or SUT-specific
  surfaces the catalog does not cover. Minimum three per boundary
  claim or written justification for fewer.
- **Operations** — per surface, which operations the scenario
  exercises.
- **Adversarial inputs** — confusable identifiers from the catalog
  in `boundary-and-isolation-testing.md`.
- **Positive controls** — what legitimate access must still succeed.
- **Negative controls** — what illegitimate access must be denied
  AND not observable in metrics / logs / side channels.
- **Delayed / async paths** — background jobs, retries, GC,
  compaction, CDC, exports.
- **Observability paths** — metrics, traces, audit logs that could
  themselves leak across the boundary.
- **Scenario arms** — per-arm IDs (`S<n>/api`, `S<n>/sdk`, etc.).
  Apply the split-into-arms rule: if the scenario spans more than 3
  surfaces, more than 3 claim categories, or requires more than 1
  independent oracle, split into arms with independent verdicts.

For non-boundary scenarios, write `§7.M.S: not applicable (no
boundary or fairness claim falsified)` and skip the fields. Do not
invent surfaces just to fill the field.

The §7.M.S sub-block is a *sibling* to §7.M (model / history /
checker), not a replacement. A scenario falsifying both a
consistency claim and a boundary claim fills both blocks.

**Every scenario declares three budget tiers.** Replace the legacy
single `Exit criteria` field with explicit Smoke / Hardening /
Release budgets per scenario:

- **Smoke budget** — minimum config + duration + faults + seeds
  required for `PASS-smoke`.
- **Hardening budget** — stronger on relevant coverage dimensions
  (cases, duration, operations, seeds, configurations); justify fixed
  dimensions such as one node or zero injected faults. Required for
  `PASS-hardening`; no-fault hardening supports only no-fault claims.
- **Release budget** — long / repeated / statistical gate, OR an
  explicit `not provided — <reason>. Revisit when: <condition>.`
  declaration. Empty / "TBD" / "see §6b" are explicitly disallowed.

The execute skill uses the budget tier actually met as a verdict
precondition; the findings report surfaces every "not provided"
release budget in a dedicated Release-budget disclosures section.

### 5b. Argue coverage adequacy

A test plan that lists scenarios without arguing they are *enough*
is not a test plan — it's a wishlist. Before writing the plan file,
build the argument for adequacy. Cover three things:

**1. Architectural summary.** A one-page (≤ 30 lines) summary of the
system's actual architecture: the major components, how data flows
between them, where state is durable, where consensus runs, where
trust boundaries live. This is not the catalog (catalog is reference
material) — this is the system as it actually exists, written so a
reviewer who has never seen the codebase can follow the test plan.
The architectural summary makes it possible for the reviewer to
spot a missing test ("you have nothing exercising the
storage→index handoff") that a flat scenario list would hide.

**2. Coverage adequacy argument.** For each claim, demonstrate that
the chosen scenarios — *taken together* — would falsify the claim
if it were violated. The form is: "claim Cn could be violated under
threats T1, T2, …; scenarios Sa, Sb, Sc exercise those threats
under conditions X, Y, Z; therefore if Cn is wrong, at least one
of Sa/Sb/Sc would catch it." A reviewer should be able to read
this and either accept the argument or point at a specific gap
("scenario Sa doesn't actually inject T2 — it only injects T1").

**3. Residual uncertainty.** Honestly list what the plan does NOT
falsify and why that is acceptable. "Claim Cn is not exercised
under multi-AZ failure because the harness cannot inject AZ-level
faults today; we accept this risk because production deploys are
single-AZ for now." This section is what turns a plan from "tests"
into "an argument for shipping."

These three sections together are the "confidence" the reader
needs. Without them, the plan answers "what would we test" but
not "is testing this enough to ship."

For boundary or fairness claims (any claim whose §7.M.S decomposes
into multiple arms, or whose oracle covers multiple groups), the
§7d statement must include a per-aspect
confidence table after the leading paragraph. The paragraph alone
hides which arms are well-tested vs. which are deferred; the table
makes it visible. A single conservative paragraph that says
"confidence is moderate" without naming which aspects are moderate
and which are low is the specific failure mode the table prevents.

### 6. Write the plan file

Copy `assets/plan-template.md` to the plan destination and fill it in.
Default destination is `docs/testing-plans/<short-slug>.md` in the SUT
repo; the user may override (e.g. when they don't want the agent
writing into their repo, fall back to whatever path they specify, or
to `./testing-plans/<short-slug>.md` in the current working directory
if no path was given).

If the parent directory does not exist, create it before writing. Many
repos won't have a `docs/testing-plans/` directory the first time this
skill runs; `mkdir -p` it without ceremony.

The plan slug is the only handoff to the executing skill. Pick a
descriptive slug — `durable-idempotent-append-replay`, not
`plan-1`.

### 7. Self-check

Read the plan back. Every hypothesis has at least one scenario.
Every scenario has an oracle that is not "logs look fine". Every
chosen technique cites its reference file. If anything fails the
check, fix it in the plan; do not move on with known gaps.

**The adequacy test.** Imagine a reviewer who has never seen the
codebase reading the plan cover to cover. Then they're asked: "if
all of these scenarios pass, would you be comfortable shipping
this code?" If the plan does not contain enough material for them
to answer yes/no with confidence — specifically: the architectural
summary, the coverage-adequacy argument per claim, the residual
uncertainty list — the plan is not done. A list of scenarios is
not a confidence argument.

**Anti-pattern checks (run before declaring the plan done).**

1. **Surface decomposition implied by name but missing in arms.** If
   a scenario name contains "across all surfaces" or names multiple
   surfaces but only one `Target test file` is declared — split into
   arms.
2. **Boundary claim without negative controls.** If a claim is in
   `{boundary}` but §7.M.S `Negative controls` is empty — required
   negative controls missing. (Tenancy / authz / namespace / routing
   claims are subsumed under `boundary`; they do not appear as
   separate categories.)
3. **Fairness claim without per-group formula.** If a claim is in
   `{fairness}` but the oracle is not a per-group formula from the
   executing skill's `references/oracle-patterns.md` §14 — fairness
   criterion missing.
4. **Vague oracle.** A scenario whose `Oracle` field reads as "no
   leaks," "no unauthorised access," or similar prose without a
   model / state comparison or formula — sharpen with a concrete
   checker pattern.
5. **Confidence statement missing untested-surface disclosure.** If
   §7d does not name the untested surfaces for any boundary claim
   whose §7.M.S arms include `NOT-RUN` or `PARTIAL-surface` — the
   §7d surface-coverage disclosure rule requires that naming.
6. **Release budget without disclosure.** If any scenario's
   `Release budget` field is empty, equals "TBD", "see §6b", or any
   value not matching either a concrete budget specification OR the
   `not provided — <reason>. Revisit when: <condition>.` template
   — absence must be an explicit disclosure, not a silent gap.
7. **Scenario name promises decomposition that §7.M.S does not
   deliver.** If a scenario name contains "routing", "tenant isolation",
   "blast radius", "multi-tenant", "cell", "region", "shard",
   "namespace", "availability zone", "replica set", "placement
   pool", "failure domain", or similar architectural-boundary
   keyword, AND the scenario's §7.M.S `Surfaces` field is empty or
   names only one surface — the plan is incomplete. Either fill
   §7.M.S with the surface decomposition the boundary keyword
   implies, or rename the scenario so its name does not promise a
   decomposition the plan does not deliver. The expert framing:
   tests tend to validate that the boundary mechanism *exists*,
   not that it *actually contains failure*; this check forces the
   plan author to confront which one their scenario tests.

## Early exit

If the change genuinely does not warrant a distributed test plan —
for example, a docs-only change, a typo fix, a refactor with no
behavior change covered by existing unit tests — say so explicitly
and recommend the appropriate lighter-weight testing. Do not produce
a ceremonial plan for changes that don't need one.

## What this skill does not do

- It does not execute the plan. That's the
  `executing-distributed-system-tests` skill.
- It does not author Jepsen tests, TLA+ specs, or fuzz harnesses.
  It tells the engineer which to reach for; building them stays the
  engineer's job.
- It does not replace project-specific stability plans. It produces
  change-scoped plans that complement them.

## Reference files

- `references/catalog-index.md` — start here; selector page
- `references/jepsen-and-elle.md`
- `references/sql-semantic-testing.md` — SQL differential campaigns,
  transaction-local models, and semantic coverage; read for SQL engine
  or compatibility changes
- `references/deterministic-simulation.md`
- `references/chaos-and-fault-injection.md`
- `references/fuzzing.md`
- `references/formal-methods-tla.md`
- `references/property-and-metamorphic.md`
- `references/performance-and-benchmarking.md`
- `references/crash-recovery-and-upgrade.md`
- `references/common-distributed-systems-pitfalls.md` — 16 pitfalls
  with hypothesis templates (walk this during step 3)
- `references/history-discipline.md` — operation-history schema and
  ambiguous-outcome handling (required reading when any scenario
  will be serious)
- `references/boundary-and-isolation-testing.md` — surface catalogs,
  boundary claim matrix, confusable-identifier catalog,
  negative-control anti-patterns (required reading when any scenario
  falsifies a `boundary` or `fairness` claim)

Each reference file follows the same shape: when to reach for it,
what it detects well, what it misses, concrete tools, papers,
cost / wall-clock signal, plan checklist. The discipline references
(`common-distributed-systems-pitfalls.md`, `history-discipline.md`)
instead follow an enumeration + anti-pattern shape — they are walked
exhaustively rather than picked from.

## Asset

- `assets/plan-template.md` — the structure to fill in.
