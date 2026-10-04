---
name: security-audit
description: Adversarial, authorized red-team / penetration-testing loop for a PHP backend you own — fans out one security-auditor subagent per OWASP/vuln family in parallel, each attacking the RUNNING service (black-box HTTP/GraphQL probing) AND inspecting source (SAST/taint, dependency, secret, config), verifies every candidate by reproducing it against the running service (no false positives), maps it to CWE + OWASP id + CVSS-ish severity, then drives root-cause, suppression-free fixes through php-implementer with a regression test per fix and re-dispatches only still-open families until a clean pass. Use when red-teaming, security-auditing, penetration-testing, vuln-hunting, or threat-modeling an authorized PHP backend, or when /sdlc-review triages the security lens. Defensive/authorized use only — probe ONLY the profile-resolved local service. Skip dynamic probing with a note when `capabilities.dynamic_security_testing` is false or `make.start` is null (static/SAST lanes still run).
---

# Security Audit Skill

## Profile keys consumed

- `make.security`
- `capabilities.dynamic_security_testing`
- `capabilities.publish_pr_comments`
- `make.start`
- `make.ci`
- `make.psalm`
- `make.post_review_findings`
- `architecture.source_root`
- `architecture.bounded_contexts`
- `framework.api_platform`
- `framework.graphql`
- `persistence.mapper`
- `persistence.engine`

Read these from `.claude/php-sdlc.yml` at runtime (no per-repo rendering; run
`/sdlc-setup` if the profile is missing). All paths and contexts resolve from
the profile — never from source-project literals. A `null` `make.*` value
means that lane is unconfigured: substitute the bundled static lane
(`make.security: null`) or degrade with a note (`make.start: null`), never
improvise a raw host command.

## Gating

**Authorized/defensive use only.** This skill exercises offensive technique
for a defensive purpose: a repo owner auditing their own service. The four
boundary rules are a hard contract, restated here and in
[`../../agents/security-auditor.md`](../../agents/security-auditor.md) verbatim,
and enforced at the Allowed-actions / Constraints level (a forbidden action,
not advisory prose):

1. **In-scope target only (verified, not assumed)** — probe ONLY the
   profile-resolved local service (the base URL of the `make.start`-booted
   service). The boundary is a checkable invariant, not just whatever URL was
   passed: BEFORE any dynamic probe, verify the target host resolves to
   loopback (`127.0.0.0/8`, `::1`), an RFC1918/private range (`10.0.0.0/8`,
   `172.16.0.0/12`, `192.168.0.0/16`, `fc00::/7`), or a known
   container/compose network name. If it does not, **refuse** — skip dynamic
   probing with a note and record a boundary-violation; never probe a
   public, remote, or third-party host even if one is supplied in the
   dispatch.
2. **No exfiltration** — never copy data, secrets, or credentials out of the
   disposable container instance.
3. **Mutate via the API only** — change state only through the service's own
   API; no out-of-band datastore writes.
4. **Container-only, no destructive non-API operations** — run through
   `make` / `docker compose exec php`, never host binaries; use the minimal
   payload needed to prove a vuln on a disposable instance.

**Degrade gates** (each completes the stage SUCCESS-WITH-REPORT — never a loop
or hard-fail, NFR-3):

- `make.security: null` ⇒ run the bundled static lane directly through the
  container (`make.psalm` with taint analysis, Semgrep, `composer audit`,
  secret-scan); add no dynamic dependency.
- `capabilities.dynamic_security_testing: false` OR `make.start: null` ⇒
  dynamic probing is skipped with a note; static/SAST/dep/secret/config lanes
  still run.
- `framework.graphql: false` ⇒ the GraphQL family is recorded N/A-with-reason
  and not dispatched.
- LLM Top 10 family ⇒ PROBE only when target LLM usage is detected (composer
  deps, `clean-architecture-llm` artifacts in `architecture.source_root`, or
  an explicit profile signal); otherwise recorded N/A-with-reason. See the
  triage rules in [`reference/owasp-catalog.md`](reference/owasp-catalog.md).

## Context

This skill is the plugin's **adversarial security lens** — an adversarial,
multi-subagent red-team loop over an authorized PHP backend. It runs at two
entry points with one identical body:

- **Triaged inside Stage 4 `/sdlc-review`** — the review gate's applicability
  triage records an EXECUTE / NOT-APPLICABLE verdict for it like every other
  skill. It is the adversarial counterpart to the quality lens
  (`code-quality-reviewer`) and the spec lens (`fr-nfr-reviewer`).
- **Standalone** — invokable directly as `php-backend-sdlc:security-audit`
  against an authorized target.

There is **no dedicated security slash-command** — the command surface stays 8
(FR-2); the security lens runs inside `/sdlc-review` triage or standalone.
The skill **owns the loop** (triage → fan-out → find → verify → fix → regress
→ re-verify → loop); the `security-auditor` subagents are **find/verify only**;
all code edits route through the existing `php-implementer`. Its culture is
**no false positives** (a SAST candidate is never a finding until reproduced),
**root-cause only** (no suppression, baseline, or threshold edit), and
**container-only** execution.

This skill body PRESCRIBES the fan-out as text. It contains **no Task-tool
call** — skills never invoke agents. The orchestrator that loaded this skill
(the `/sdlc-review` agent or a standalone invocation that holds the `Task`
tool) executes the dispatch the steps describe.

## Task

Drive the target PHP backend to **zero new verified security findings**:

- Every OWASP/vuln family in
  [`reference/owasp-catalog.md`](reference/owasp-catalog.md) receives an
  explicit verdict — PROBE or N/A-with-reason. 100% triaged, no silent skips.
- Every PROBE family is driven to zero new verified findings through the
  bounded loop.
- Every reported finding carries a working reproduction, a CWE id, an OWASP id,
  and a severity band-with-rationale.
- Every fix is root-cause and secure-by-default, routed through
  `php-implementer`, and carries a failing-then-passing regression test.

## Steps

The canonical loop. Every **enumeration** (OWASP families, per-family probes,
remediations) lives in a `reference/` file — never inline here — so this
SKILL.md stays under ~500 lines (NFR-9).

### 5.1 Triage

Read [`reference/owasp-catalog.md`](reference/owasp-catalog.md) and record a
**per-family verdict table** (PROBE / N/A-with-reason) covering the entire
corpus. No silent skips (NFR-6). Exclude N/A families **before** fan-out to
control token cost (NFR-8):

- OWASP Mobile — N/A-for-backend (recorded reason).
- Memory-safety CWEs — N/A for managed PHP (recorded reason).
- LLM Top 10 — N/A unless LLM usage is detected (Gating rule above).
- GraphQL — N/A when `framework.graphql` is `false`.

The catalog file is the single source for the dispatchable family set and its
CWE/OWASP-id mappings; do not re-enumerate families here.

### 5.2 Fan-out (parallel red-team)

First, **boot the service** when dynamic testing is in scope: if
`capabilities.dynamic_security_testing` is true and `make.start` is non-null,
the orchestrator boots the service via the `make.start` target and captures its
in-scope base URL (loopback/private/container host per boundary rule 1). If the
capability is false or `make.start` is null, dynamic probing degrades to
skip-with-note and only the static lanes run — no base URL is passed.

**Capture and report the booted runtime env** (e.g. `APP_ENV`) alongside the
base URL. A fuzz/test/CI env (one that disables security middleware such as the
rate limiter, or enables debug/verbose errors and GraphQL introspection) will
**mask or inflate** env-sensitive families: rate / resource exhaustion
(API4:2023) can read falsely CLEAN, while error-disclosure (CWE-209) and
introspection can read falsely as findings. So: pass the env in every dispatch;
a family whose verdict depends on a control toggled by that env must
cross-check the prod/dev config source (raise-only thresholds, listener wiring)
before reporting CLEAN or promoting a finding, and state the env in its verdict.
Prefer booting a prod/dev-like profile for the dynamic pass when one exists.

Then dispatch **one `security-auditor` subagent per PROBE family, in
parallel** — the proven parallel-`php-implementer` idiom (no new
infrastructure). The orchestrator issues N `Task`-tool dispatches in one turn.
Each dispatch passes:

- the assigned OWASP family id and its
  [`reference/attack-playbooks.md`](reference/attack-playbooks.md) entry;
- the report contract (the finding-record schema in **Format** below);
- the current iteration number from this loop's `MAX_ITERATIONS=5` guard;
- the resolved base URL of the booted in-scope service (omitted when dynamic
  testing is degraded — the auditor then runs static lanes only);
- on re-dispatch, the prior ledger for that family.

Resolve the family set and its profile gates from
[`reference/owasp-catalog.md`](reference/owasp-catalog.md). N/A families from
5.1 are **never dispatched**.

### 5.3 Find → verify

Each subagent runs SAST/dep/secret/config analysis **and** adversarial dynamic
probing per its [`reference/attack-playbooks.md`](reference/attack-playbooks.md)
entry. A SAST/dep/secret/config result is a **candidate**, never a finding,
until **reproduced against the running service** — or, for static-only classes
such as a committed secret, deterministically demonstrated in-tree (FR-7,
NFR-6). A candidate with no working reproduction is recorded
**downgraded/dropped**, never reported.

### 5.4 Aggregate / dedupe / promote

The orchestrator collects the N subagent reports and:

- **Dedupes** findings by the tuple `(CWE id, sink location file:line,
  exploited endpoint)` — two families hitting the same sink collapse to one
  finding (NFR-8).
- **Promotes** only reproduced candidates to findings; a candidate without a
  working reproduction is recorded downgraded/dropped, never reported (FR-7) —
  the subagents already enforce this; the orchestrator is the second gate.
- **Orders** the promoted findings by severity band (Critical → Low) for the
  fix queue.

### 5.5 Fix → regression-test

Route each verified finding to **`php-implementer`** (never edited here, never
by the auditor) with the `{location, remediation, regression_test}` slice of
its finding record and the cited remediation from
[`reference/remediation-patterns.md`](reference/remediation-patterns.md). Each
fix is **root-cause and secure-by-default** and carries a **failing-then-passing
regression test** that reproduces the exploit and then proves it closed (FR-8,
NFR-7). No suppression, baseline, config relaxation, threshold reduction, or
`deptrac.yaml` edit — ever.

### 5.6 Re-verify → loop

Re-dispatch only **still-open families** (the re-dispatch set shrinks each
iteration, NFR-8). The affected family's `security-auditor` re-verifies that
its reproduction no longer succeeds (SA-6). The loop is bounded
`MAX_ITERATIONS=5`:

```text
iteration ← 1
loop:
  dispatch security-auditor for each still-open PROBE family (parallel)   # 5.2
  collect + dedupe + promote verified findings                            # 5.4
  if zero new verified findings: exit SUCCESS-WITH-REPORT                 # exit
  route each finding → php-implementer (root-cause fix + regression test) # 5.5
  affected-family re-verify                                               # SA-6
  iteration ← iteration + 1
  if iteration > 5  OR  php-implementer / Ralph breaker tripped:          # NFR-2
     emit canonical escalation block; STOP (never auto-reset the breaker)
final: run the make.ci target once; forbidden-suppression scan; emit report
```

Run the full `make.ci` target **once at loop close** (not per iteration — the
affected-family reproduction is the per-iteration correctness signal, the final
`make.ci` is the safety net, SA-6). Exit on the first iteration that yields
zero new verified findings. On `iteration > 5`, or on a tripped
`php-implementer` / Ralph circuit breaker, emit the canonical escalation block
and STOP — never auto-reset a breaker (NFR-2).

### 5.7 Publish (gated)

When `capabilities.publish_pr_comments` is `true`, project this loop's promoted
finding records (§5.4) — deduped on the same `(cwe, location, endpoint)` tuple,
each `auto_fixed: true` with its `regression_test` when routed through §5.5 — to
the canonical ledger JSON (schema in the poster header) at
`${SDLC_LEDGER_DIR:-.sdlc/review-ledgers}/security.json`, then publish ONE
consolidated, idempotent PR comment via the target mapped by
`make.post_review_findings`; when that key is `null`, the plugin substitutes
`"${CLAUDE_PLUGIN_ROOT}/scripts/post-review-findings.sh"`:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/post-review-findings.sh" security \
  --file "${SDLC_LEDGER_DIR:-.sdlc/review-ledgers}/security.json" --pr "$PR"
```

The poster is idempotent (hidden `<!-- sdlc-review:security -->` marker — it
updates its prior comment, never spams), authorized (writes only to the resolved
repo's own PR), and DEGRADES (NFR-3): `capabilities.publish_pr_comments`
false/absent, `gh` absent, no PR, an empty ledger, a mismatched base repo, or a
`gh` write failure all skip-with-note and exit 0 — publishing NEVER fails this
loop. When the flag is false/absent, skip this step with a note.

## Constraints

**NEVER**:

- Probe any host or URL outside the profile-resolved local service, exfiltrate
  data, mutate state outside the service's own API, or run a destructive
  non-API operation (the four boundary rules in **Gating**).
- Run host binaries — execution is container-only (`make` /
  `docker compose exec php`).
- Report a finding without a working reproduction (FR-7), or fabricate a
  finding for an N/A family (NFR-6).
- Edit code from this skill or from a `security-auditor` subagent — fixes route
  through `php-implementer` only (SA-3).
- Add a suppression/ignore annotation, baseline, config relaxation, threshold
  reduction, or `deptrac.yaml` edit to make a finding disappear — thresholds
  are raise-only; fix the code (NFR-7).
- Loop or hard-fail on an absent capability — degrade with a note (NFR-3).
- Loop past `MAX_ITERATIONS=5` or auto-reset a tripped breaker (NFR-2).
- Use source-project literals — every path/context resolves from the profile
  (NFR-4).
- Issue a Task-tool call from this skill body — it is text the orchestrator
  follows.

**ALWAYS**:

- Record an explicit verdict (PROBE / N/A-with-reason) for every family in
  [`reference/owasp-catalog.md`](reference/owasp-catalog.md) — 100% triaged.
- Promote only reproduced candidates to findings; record non-reproducible
  candidates as downgraded/dropped.
- Map every finding to a CWE id + OWASP id + severity band-with-rationale and
  cite its remediation from
  [`reference/remediation-patterns.md`](reference/remediation-patterns.md).
- Route every fix through `php-implementer` with a failing-then-passing
  regression test.
- Re-dispatch only still-open families; run `make.ci` once at loop close; scan
  the diff for forbidden suppressions (the
  [`../code-review/SKILL.md`](../code-review/SKILL.md) Step 6 scan) before
  declaring success.
- Run the §5.7 Publish step gated on `capabilities.publish_pr_comments`; it
  degrades with a note (NFR-3) and never fails this loop.

## Format

**Finding-record schema** — the single hand-off shape, emitted by each
`security-auditor` and consumed by the orchestrator → `php-implementer`:

```text
FINDING <family-id>-<n>
  cwe: CWE-<id>                           # mapped from reference/owasp-catalog.md
  owasp: <A0X:2021 | APIx:2023 | LLMxx>   # edition-labelled id
  severity: Critical|High|Medium|Low      # band + one-line rationale (CVSS vector optional)
  location: <architecture.source_root>/<path>:<line>   # the sink, profile-resolved (no literals)
  endpoint: <METHOD> <path>               # the exploited surface
  reproduction:
    1. <exact container/curl command>     # copy-pasteable against a freshly
    2. <exact command>                    #   booted disposable instance
  expected: <secure behavior>   observed: <vulnerable behavior>
  remediation: <vetted library/primitive + cited OWASP cheat sheet>   # from remediation-patterns.md
  regression_test: <test path the fix must add>        # failing-before / passing-after
```

`php-implementer` receives `{location, remediation, regression_test}` and
produces the root-cause fix + the failing-then-passing test; the affected-family
`security-auditor` re-verifies the reproduction no longer succeeds. Severity is
a **band-with-rationale**; a full CVSS v3.1/v4.0 vector is an optional field,
never mandated.

**Run report shape** — emitted at loop close:

```text
SECURITY-AUDIT RUN REPORT
  per-family verdict table: <family> → PROBE | N/A (<reason>)
  per-iteration finding counts: iter 1: <n> … iter k: <n>
  iterations used: k / MAX_ITERATIONS=5
  promoted findings: <count by severity band>
  dropped candidates: <count> (non-reproducible)
  make.ci: <PASS|FAIL>   forbidden-suppression scan: <CLEAN|VIOLATION>
  status: SUCCESS-WITH-REPORT | ESCALATED
```

**Canonical escalation block** (on `MAX_ITERATIONS=5` breach or breaker trip,
parent §2 format):

```text
=== SDLC ESCALATION ===
stage: security-audit
iteration: <n>/5
exit_condition: zero new verified findings (all dispatched families CLEAN)
status: NOT MET
blocking_finding: FINDING <family-id>-<n> (<cwe> / <owasp> / <severity>)
iteration_log: <one line per iteration: open families + candidates/reproduced/re-verified counts>
recommended_action: <next step for the owner, e.g. route FINDING <id> to php-implementer>
=== END ===
```

## Verification

- [ ] Every family in
      [`reference/owasp-catalog.md`](reference/owasp-catalog.md) received a
      recorded verdict (PROBE / N/A-with-reason) — 100% triaged, no silent
      skip.
- [ ] N/A families (Mobile, memory-safety CWEs, LLM-when-not-detected,
      GraphQL-when-`framework.graphql`-false) were excluded before fan-out with
      a recorded reason.
- [ ] Every reported finding carries reproduction steps + CWE id + OWASP id +
      severity band-with-rationale + a cited remediation.
- [ ] Every non-reproducible candidate was recorded downgraded/dropped, not
      reported.
- [ ] Every fix is root-cause, routed through `php-implementer`, and carries a
      failing-then-passing regression test.
- [ ] Only still-open families were re-dispatched each iteration (shrinking
      set).
- [ ] The loop exited on a zero-new-verified-findings iteration, or escalated
      at `iteration > 5` / breaker trip with the canonical escalation block —
      no breaker auto-reset.
- [ ] The `make.ci` target exits `0` at loop close and the
      forbidden-suppression scan (from
      [`../code-review/SKILL.md`](../code-review/SKILL.md) Step 6) reports zero
      suppressions introduced.
- [ ] No action targeted an out-of-profile host or performed a destructive
      non-API operation (the four boundary rules held throughout).

## Related Skills

- [`../code-review/SKILL.md`](../code-review/SKILL.md) — the forbidden-suppression
  scan and per-comment evidence ledger this loop reuses.
- [`../testing-workflow/SKILL.md`](../testing-workflow/SKILL.md) — where each
  failing-then-passing regression test lives.
- [`../ci-workflow/SKILL.md`](../ci-workflow/SKILL.md) — the `make.ci` gate run
  once at loop close.
- [`../bmad-fr-nfr-review-gate/SKILL.md`](../bmad-fr-nfr-review-gate/SKILL.md) —
  the sibling spec-driven review gate lens.
