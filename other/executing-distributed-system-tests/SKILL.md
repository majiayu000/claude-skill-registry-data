---
name: executing-distributed-system-tests
description: Use when running a previously designed distributed-systems test plan against a real or simulated cluster — driving fault injection, workload, chaos scenarios, linearizability / consistency runs, durability, partition, crash-recovery, upgrade, performance/SLO runs, tenant isolation runs, boundary or authz runs, fairness / noisy-neighbor runs, or release validation. Also use when asked to "execute the plan", "reproduce a distributed bug", "run stability tests", "drive chaos", "validate a release end-to-end", "run the tenant isolation tests", or when a plan file exists at docs/testing-plans/ or any caller-specified location and needs to be run. Discovers and reuses the SUT's test toolbox rather than reinventing, captures nemesis landing evidence per scenario, runs the green-but-broken and weak-oracle audits before any PASS, and for boundary or fairness scenarios with §7.M.S arms runs each surface arm with its own verdict under a downgrade rule so the aggregate cannot fold an untested surface into a pass.
---

# Executing Distributed-System Tests

Pairs with `designing-distributed-system-tests`. That skill produces
a plan; this skill runs it. The two communicate only through
filesystem artifacts: the plan file in and a session directory
plus findings report out.

The most common failure mode this skill is built to avoid: a run
that produces a green checkmark without anyone having checked
that the workload, the fault, and the oracle each did their job.
The "green-but-broken" checks are not optional.

## Process

### 1. Load the plan

If a plan file path was supplied, read it. If the user described
a plan in conversation, extract the scenario list. If the plan
is missing oracles or per-scenario budget tiers (Smoke / Hardening
/ Release, per the plan template's §7 scenario fields), halt — hand
back to the design skill rather than improvise. Improvising an
oracle in the moment is how green-but-broken results get produced.

### 2. Discover the SUT toolbox

Search the repo before writing any new code. Look for:
- `tools/`, `scripts/`, `bin/` — drivers, workload generators,
  cluster bring-up scripts
- `tests/integration/`, `tests/stability/`, `tests/chaos/`
- `docs/runbooks/`, `docs/testing/`, `docs/stability-test-plan.md`
- Makefile / justfile / `cargo xtask` targets that look like
  cluster commands
- existing CI definitions that already wire fault-injection

Record what you found in the session log under "Toolbox
discovered". This is required before any scenario runs — it
prevents the skill from re-inventing tools that already exist.

### 2b. Probe environment capability and guide install if needed

Right after toolbox discovery, before running any scenario, check
that the host can actually run the toolbox you just catalogued.
If the plan has an "Environment requirements" section (the design
skill emits one), treat it as the spec; otherwise infer the list
from the selected techniques and the SUT toolbox.

**Ask the user first; do not silently probe.** Before running any
`which` / `--version` / `docker ps` checks, list the capabilities
the plan needs and ask the user: "what's available in your
environment, and what would you like me to skip?" Most operators
already know whether they have Docker, sudo for iptables, a Go
toolchain, etc. Asking up front saves a probe round, surfaces
substitution options the operator may know about (e.g. "I have
podman instead of Docker"), and respects their authority over
their own machine. After the user answers, verify with quick
probes and reconcile any gap between what they said and what's
actually present.

Probe categories:
- container runtime (docker / podman + compose)
- language toolchains at the version floors the plan declares
- backend services (Postgres, MinIO / S3-compatible, message brokers)
- fault-injection facilities (iptables, tc/netem, libfaketime,
  dm-flakey, Toxiproxy)
- kernel features (network namespaces for asymmetric partition,
  cgroups for IO throttling)
- observability stack referenced by the plan

For each capability, produce a row: requirement → present? → version
→ source. Record the full matrix in the session log; the findings
report cites it per scenario.

**For missing capabilities, do not silently mark INCONCLUSIVE.**
Two cases:

1. **Trivially installable** (a package the user can `apt-get install`
   / `brew install` in seconds): surface the install command to the
   user with a one-line explanation of what it enables, and offer to
   proceed once they've installed (or to install for them if you
   have permission and the change is low-blast-radius). Do not run
   `sudo` or system-level installs without explicit user approval.

2. **Non-trivial to install** (requires service setup, license,
   admin access, or careful configuration): explain what's missing,
   what scenarios depend on it, and what the user would gain by
   adding it. Then ask whether to (a) wait while they set it up,
   (b) proceed and mark dependent scenarios INCONCLUSIVE, or (c)
   substitute a degraded approximation (and document the
   substitution honestly in the findings).

Either way, INCONCLUSIVE is only the right verdict after the user
has been told what's missing and either declined to install it or
the install is genuinely out of reach. "Tried to run and silently
no-opped" remains forbidden.

### 3. Establish a session directory

Create:
```
{{session_root}}/{{plan_slug}}/{{UTC_timestamp}}/
├── logs/
├── metrics/
├── artifacts/
└── findings/
```
Default `session_root` is `./test-sessions/` in the SUT repo, or
`./test-sessions/` in the current working directory if the user
prefers not to write into the SUT repo. If the caller specified an
output root in the request (e.g. "produce a session directory and
findings report under `/path/X/`"), honor that path instead of the
default — do not silently relocate output. Place a copy of `assets/session-log-template.md` at
`session-log.md` inside this directory and fill in the header.

### 3b. Author mode (opt-in)

By default the execute skill runs scenarios against the SUT's
**existing** test infrastructure plus an ephemeral sibling-package
harness under `{{session_dir}}/artifacts/harness/`. Nothing is
written into the SUT repo.

When the operator explicitly asks for author mode (typically
"author the tests" or "fill the skeletons" in the prompt, or
`DIST_TEST_AUTHOR_MODE=1`), the skill **writes the scenario
skeletons into the SUT repo** at the `Target test file` paths
declared in the plan's §7. This is the only sanctioned exception
to the project-autonomy rule.

In author mode:

1. **Pre-flight diff scan.** For each scenario, check if its
   `Target test file` already exists. If yes, show the operator
   the existing file and ask whether to overwrite, skip, or
   regenerate as a sibling (`<path>.new.rs` etc.). Never silently
   overwrite operator-authored tests.
2. **Write the skeleton.** Drop the `Skeleton` from the plan to
   the `Target test file` path. Verify the `AUTO-GENERATED`
   header is present; refuse to write a skeleton missing the
   header. Run the SUT's formatter (`cargo fmt`, `gofmt`, `black`,
   …) on the new file.
3. **Fill the TODOs.** Expand the workload / faults / oracle
   TODO regions from the plan's prose. Use the SUT's existing
   test fixtures and patterns wherever possible — read at least
   one sibling test file in the same directory before writing,
   to match the codebase's idioms.
4. **Compile + run.** Build the SUT's test binary (e.g.
   `cargo test --no-run -p <crate>`) to catch compile errors
   before running. Then run the test, capture verdict + oracle
   execution evidence as usual.
5. **Stage, do not commit.** The skill MUST NOT `git commit`
   the generated tests. Surface the diff to the operator and let
   them review + commit. Author mode produces candidate tests,
   not approved tests.
6. **Provenance.** Every auto-written file's header carries the
   plan path, the scenario id, and the sha of the plan at
   generation time. Reviewers can diff prose changes against
   test changes; if the plan's prose drifts from the test, the
   sha mismatch surfaces.

If a scenario has no `Target test file` or `Skeleton` in the
plan, author mode is impossible for it — surface that explicitly
to the operator and fall back to ephemeral-harness execution
for that scenario.

### 4. Run scenarios in plan order

**Checkpoint discipline for long-running scenarios.** Distributed
test runs routinely involve commands that stay silent for minutes
to hours: cold cargo builds, `docker compose up`, multi-node smoke
runs, sustained workload generators. Subagent harnesses and CI
runners commonly have watchdogs that kill a task after 5–10 minutes
of silence on its tool stream. To keep the watchdog fed and to
give the operator visible progress:

- Before starting any command expected to run longer than ~3 minutes,
  append a one-line "starting" entry to `session-log.md` (scenario id,
  command, expected duration). After it finishes, append the result
  line with elapsed time.
- For commands that take >5 minutes, prefer `Bash` with
  `run_in_background: true` plus periodic status pulls (`tail` the
  output file, `docker compose ps`, `curl` a health endpoint) every
  60–120 seconds rather than blocking on a single foreground call.
- Never let a single foreground command exceed the harness watchdog
  budget. If a build or run genuinely needs that long, split it
  (warm a cache first, then time the actual scenario).
- Each scenario writes its own per-scenario findings file as it
  goes, not only at the end. Partial findings beat a missing report
  when a scenario times out or the agent is killed mid-run.

For each scenario:

1. **Preconditions check.** Cluster up cleanly, observability
   live, baseline metric captured, fault plane responsive.
2. **Start workload** using the discovered driver.
3. **Inject fault** per the plan schedule.
4. **Capture evidence the fault landed.** The plan's §7.M
   `Nemesis + landing evidence` field declares which observable
   signal proves the fault landed (counter, RPC timeout pattern,
   log marker, partition-status metric). Capture *that* signal,
   not a generic one. If the signal is absent or ambiguous, the
   scenario verdict is `INCONCLUSIVE-fault-not-proven` (see
   `references/verdict-taxonomy.md`) — never PASS.

   For non-serious scenarios that did not declare §7.M (no gated
   claim category), capture a best-effort generic landing signal
   from the appropriate row of `references/fault-injection-howto.md`.
5. **Stop / quiesce** and collect.
6. **Apply oracle** — read `references/oracle-patterns.md` for
   the right one if the plan didn't fully specify.
7. **Record the verdict** with the actual oracle execution evidence.
   The verdict is one of the ten states defined in
   `references/verdict-taxonomy.md`: PASS-smoke, PASS-hardening,
   FAIL-reproducible, FAIL-nondeterministic, INCONCLUSIVE-env,
   INCONCLUSIVE-oracle-too-weak, INCONCLUSIVE-fault-not-proven,
   PARTIAL-surface, PARTIAL-model, NOT-RUN. Apply the decision tree in
   that file to assign the verdict; do not free-form. Record the verdict
   together with the oracle execution evidence (op count consumed,
   anomalies found) and the §7.M nemesis landing signal — both are
   required for any PASS-hardening claim.

**Per-arm execution for boundary and fairness scenarios.** When the
plan's §7.M.S block declares scenario arms (e.g., `S5/api`,
`S5/sdk`, `S5/export`, `S5/admin`):

1. Run each arm as a separate scenario, in plan order. Log entries
   are tagged with the arm id, not the parent scenario id.
2. Apply the 10-state decision tree per arm — each arm earns its own
   verdict independently. Arms that the session never reaches earn
   `NOT-RUN` (the 10th state added by this iteration; see
   `references/verdict-taxonomy.md`).
3. After all arms are scored, compute the scenario-level aggregate
   verdict via the downgrade rule: any `NOT-RUN` or `PARTIAL-*` arm
   caps the scenario-level verdict at `PARTIAL-surface`, regardless
   of which arms passed.
4. Record both the per-arm verdicts and the aggregate in the
   findings report's Scenario results table and Surface coverage
   table.

**Budget-tier verdict gating.** PASS-* verdicts require the run to
have actually met the corresponding budget tier declared in the
plan, not just produced a clean oracle output:

- Run met only the smoke budget → at best `PASS-smoke`, never
  `PASS-hardening`.
- Run met the hardening budget → eligible for `PASS-hardening`.
- Run met the release budget → eligible for the release-tier
  verdict (currently expressed as `PASS-hardening` with a release
  annotation; a future iteration may introduce a dedicated state).

Record the budget tier actually met alongside the verdict in the
session log so the findings report can confirm the verdict is
defensible.

### 5. On failure: capture before moving on

Do not run the next scenario before recording:
- Reproducer (apply `references/test-case-reduction.md`).
- **Reduction classification** (SUT / harness / checker /
  environment, per the "Classify blame before filing" section of
  `references/test-case-reduction.md`). Required before filing.
  "Unknown — pending re-run on alternative harness/host" is
  acceptable as an interim value; a wrong guess is not.
- **TaxDC classification** (`references/finding-classification.md`,
  bug type — orthogonal to the reduction classification above).
- Evidence (log excerpts, op history files, metric snapshots).
- Hypothesised root cause and owning subsystem.
- Suggested next action.

### 6. Apply green-but-broken checks AND the weak-oracle audit

Before declaring any scenario PASS, run both checklists in
`references/green-but-broken-red-flags.md`:

1. The numbered "red-flag" checks (1–10) — guards against tests
   that never ran.
2. The "Weak oracles — do not trust these alone" section — guards
   against tests that ran but whose oracle could not distinguish
   PASS from FAIL.

Record the result of each check in the findings report's
green-but-broken section. A serious scenario (one with §7.M filled)
cannot be marked `PASS-hardening` if any weak-oracle check is
unchecked; downgrade to `PARTIAL-surface` or `PARTIAL-model` per
`references/verdict-taxonomy.md`.

### 7. Write the findings report

Copy `assets/findings-report-template.md` to
`{{session_dir}}/findings/report.md` (or to the caller's
specified location if they asked for one). Lead with the headline
result. Cover every plan hypothesis in the coverage section,
even the ones not exercised — those are gaps worth naming.

INCONCLUSIVE is a first-class verdict, not a soft failure.
Scenarios blocked by missing tooling, missing test-only plan
prerequisites (a flag the workload doesn't have, a span
attribute that hasn't been added, a proptest module that doesn't
exist yet), or environment limits get the INCONCLUSIVE label
with a single-line reason — never a silent PASS, never a
report-wide BLOCKED unless literally nothing ran.

A scenario can have multiple arms with different verdicts —
e.g. an in-process driver that PASSed and an external driver
that was INCONCLUSIVE. Record each arm on its own row in the
scenario table and split the finding accordingly.

**The findings report must close the adequacy loop.** The plan's
§7b ("Coverage adequacy argument") and §7d ("Confidence statement")
committed to specific claim→threat→scenario mappings and a
confidence verdict. The report must include:

- **Surface coverage** — for scenarios with §7.M.S arms in the plan,
  list planned vs executed surfaces per arm with verdict and
  downgrade reason. The aggregate row applies the downgrade rule:
  any `NOT-RUN` or `PARTIAL-*` arm caps the scenario at
  `PARTIAL-surface`. Render as "No boundary or fairness scenarios in
  this plan" if §7.M.S was never declared.
- **Release-budget disclosures** — lift every "Release budget: not
  provided — <reason>. Revisit when: <…>." declaration from the plan
  verbatim. Surfaces production-readiness gaps the run cannot close
  on its own. Render as "All scenarios declared a concrete release
  budget" if none of the plan's scenarios used the "not provided"
  template.
- **Adequacy assessment vs plan** — row per claim showing what
  the plan argued for vs what actually ran. INCONCLUSIVE scenarios
  shrink the adequacy of their claims; surface those gaps.
- **Confidence delta** — what should the reviewer believe MORE /
  LESS / UNCHANGED after this run, compared to the plan's §7d.

Without these sections, the report tells the reviewer what passed
but not whether to ship. A list of verdicts is not a confidence
verdict.

**Session-level verdict.** Set the headline session verdict by
the strongest evidence found, not by counting. Every per-scenario
verdict maps into one of five session values:
- Any FAIL with a reproducer → session is FAIL (lead with the
  finding, even if most scenarios were INCONCLUSIVE).
- No FAIL, at least one PASS-smoke/PASS-hardening with cited
  evidence → session is DONE if every other scenario also PASSed
  clean; DONE_WITH_CONCERNS if any scenario was INCONCLUSIVE-*,
  PARTIAL-surface, PARTIAL-model, or NOT-RUN. Treat PARTIAL-* and
  NOT-RUN as concerns, never as clean passes.
- No PASS and no FAIL, but at least one scenario produced signal
  (INCONCLUSIVE-* or PARTIAL-*) → session is INCONCLUSIVE.
- Nothing ran at all — every scenario NOT-RUN, or couldn't load
  the plan / reach the SUT → session is BLOCKED.

A high INCONCLUSIVE fraction is not by itself a problem if each
INCONCLUSIVE has an honest single-line reason; it just means the
plan needs an environment the operator didn't have.

**Writing the report file.** Some harnesses (subagent sandboxes
in various agent runtimes, restricted CI runners) block writing
arbitrary `.md` files under output directories. If your write is
refused, return the full report content as text and surface the
restriction explicitly so the caller can save it — do not skip
producing the artifact, and do not pretend it was written.

## Project autonomy

This skill does not modify SUT source files in default mode.
It may create scripts inside the session directory and may add
a single new file `docs/testing-plans/<slug>.md` only if the
user explicitly asks the design skill to write there. Everything
else lives under `{{session_root}}`.

**Author mode is the sanctioned exception.** When the operator
explicitly opts into author mode (see step 3b), the skill may
write to the `Target test file` paths declared in the plan's §7
— and ONLY those paths. Any write outside a declared target
path is forbidden, in any mode. Author mode does not git commit;
all generated tests are staged for operator review.

**Sibling-package harness is in bounds.** When in-process tests
need to call into the SUT's libraries (a Rust integration test
against a SUT crate, a Go test importing a SUT module, a Python
test importing a SUT package), create a standalone package under
`{{session_dir}}/artifacts/harness/` that depends on the SUT by
path. This is in bounds. What is NOT in bounds: adding files
under the SUT's own `tests/` directory or modifying the SUT's
manifest (`Cargo.toml`, `go.mod`, `package.json`, `pyproject.toml`,
`pom.xml`, etc.). The distinction matters because the latter
would land in the SUT's repo if committed.

## Reference files

- `references/oracle-patterns.md` — start here when an oracle
  needs picking
- `references/fault-injection-howto.md` — concrete mechanisms per
  fault type
- `references/test-case-reduction.md` — minimize a failing
  reproducer
- `references/finding-classification.md` — TaxDC-derived labels
- `references/green-but-broken-red-flags.md` — non-optional
  pre-PASS checklist
- `references/verdict-taxonomy.md` — the ten verdict states and the
  decision tree for assigning one at run end
- `references/boundary-and-isolation-testing.md` (lives in the
  design skill; named here for cross-reference) — surface catalogs
  and the downgrade rule the execute skill applies to per-arm
  verdicts for `{boundary, fairness}` scenarios

## Assets

- `assets/session-log-template.md`
- `assets/findings-report-template.md`
