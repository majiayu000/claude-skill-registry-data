---
name: e2e-test-configuration
description: Run Crossplane E2E tests (`up test run --e2e`) for a control-plane project, locally on kind (`--local`) or on an Upbound Space (Upbound Cloud). Use when asked to run or re-run, execute or debug E2E tests or an E2ETest, to check a configuration against a real cloud, or when an E2E run hangs, times out or fails. Covers preconditions (build, composition tests, credentials), choosing and stating the target, a run whose log keeps its exit code and duration, stuck detection from the test's timeoutSeconds, failure analysis, cleanup checks and an evidence-based report. Load it before any `up test run --e2e`, a re-run included, instead of running it raw. Not for writing or changing an E2ETest (fields, defaultConditions, credentials) - use author-tests.
license: Apache-2.0
references:
  - references/local.md
  - references/space.md
  - references/troubleshooting.md
  - references/report-templates.md
---

# E2E Test Runner for Crossplane Configurations

Run a project's `E2ETest`s with `up test run --e2e` and report what the run did, from its own output. Each
test gets a fresh control plane, creates real cloud resources, and is torn down afterwards, pass or fail.

## Before you start

Load `control-plane-project-charter` first, or read its `SKILL.md` beside this skill's directory; this skill
does not load it. Every "ask" below follows its §1 (unattended: never ask; act on the brief and state the
assumption, or stop and report), and its §4 binds every summary.

- Writing or changing an `E2ETest` (fields, `defaultConditions`, credentials per target) is `author-tests`'
  job: read its `e2e.md` reference. This skill runs them.
- Your scope is running and reporting. Fixes are the caller's.

If the project's own gate (README, Makefile, CI) runs E2E, use it and report its command, exit code and
output (charter §2, §4). Everything below still applies to reading its output.

## Phase 1: Choose the target and the tests

A local kind control plane and an Upbound Space are equally valid targets; this skill has no default. Use
the one your caller, the brief or the project's own gate names, then **read that target's reference before
you run anything**:

| Target | Target flags | Read first | Test credentials |
|---|---|---|---|
| Local kind control plane | `--local` | [local.md](references/local.md) | static Secret (`source: Secret`) |
| Upbound Space / Upbound Cloud | `--control-plane-group=<group> --kubeconfig <file>` | [space.md](references/space.md) | web identity (`source: Upbound`) or static Secret |

- **Nothing names a target:** interactive, ask; unattended, stop and report that the target is unspecified.
  Do not pick one.
- **A test that can only pass on one target decides.** A ProviderConfig with `source: Upbound` works only on
  a Space. Report the mismatch rather than running it elsewhere.
- **Always pass the target flags.** Without them the current context silently decides where the run lands
  (`control-plane-project-charter/references/charter/targets.md`).
- **State the target in one line before the run** ("running e2e on local kind" or "running e2e on Space
  `<space>/<group>`"), and check it against the run's first progress line (Phase 4).

**Which tests:** the names you were given (`e2etest-network-lifecycle`, space-separated) or `all`. With none,
list `ls -1d tests/e2etest-*`; interactive, ask which to run; unattended, run the ones the brief names, or all
of them.

**Several tests** run one after another, never in parallel, one log each. A failed test does not stop the
next: each has its own control plane. Stop the rest only when the failure is shared — a precondition, the
target, or the package install (`Waiting for package to be ready`) would fail every test the same way — and
list what did not run.

## Phase 2: Preconditions

An `--e2e` run creates a control plane and real cloud resources, so everything cheap comes first. **A
precondition that fails ends the run**; it is not a warning you carry forward. Check in this order and stop
at the first failure:

1. **The project builds:** `up project build`.
2. **The composition tests pass:** `up test run "tests/test-*"`. That is `test-*` by default, not `tests/*`:
   `up test run` runs every matched dir's program, e2e ones too, even without `--e2e`, and fails at
   `✗ Parsing tests` when an e2e input is unset. If the project's own gate runs `up test run tests/*`,
   use it, with the e2e inputs (check 3) set for that run too, and say so in the report
   (`control-plane-project-charter/references/charter/container.md`).
3. **Credentials.** List what the test programs read, in any language, and check each:

   ```bash
   grep -rhoE 'UP_[A-Z0-9_]+' tests/e2etest-*/ | sort -u
   # then, for each:
   [ -n "${UP_AWS_CREDENTIALS:-}" ] || echo "MISSING: UP_AWS_CREDENTIALS"
   ```

   A variable built from others (author-tests' `e2e.md` reference) must be exported inside the Phase 4 run
   block, before `up test run`, since one exported in an earlier command is gone: check its inputs (`AWS_*`)
   here instead. KCL and Python programs see only `UP_`-prefixed variables and no `~/.aws`; Go and
   go-templating programs run locally and can read any name, so also check a Go program's `os.Getenv` calls
   and a go-templating test's `env`/`expandenv` calls. An unset variable the program
   does not fail on becomes an empty Secret. That surfaces only when the provider rejects it, after a
   control plane and real resources exist.
4. **The target's own preconditions:** [local.md](references/local.md) (Docker) or
   [space.md](references/space.md) (context, group, repository visibility). Local: run under the default
   umask (`022`), never `umask 077`; under `077` the package is never ready and the run ends in
   `context deadline exceeded` ([local.md](references/local.md#preconditions) has why and the symptom).

**If you cannot complete a precondition, stop and say so. Do not start the run.** That includes a check that
is blocked rather than failed: a permission prompt you cannot answer, a command the sandbox refuses, a
credential you cannot read. A run with a precondition known to be unmet carries no information and is not
free. Report which precondition you could not establish and what the user needs to do. Skip a check only if
the user explicitly asks you to.

## Phase 3: Size the run

Read the test's own settings first:

```bash
grep -rniE 'timeoutseconds|skipdelete' tests/e2etest-<n>/
```

- **No `timeoutSeconds` in that output: don't run.** It is a broken test, not a sizing question: the run would
  panic after setup and leak its control plane (author-tests' `e2e.md` reference). Report it as a failed
  precondition.
- **Worst case** ≈ build + `setupTimeoutSeconds` (default 600) + `timeoutSeconds` + `cleanupTimeoutSeconds`
  (default 600). Scaffolds write `timeoutSeconds` 300 (Go) or 4500 (YAML, KCL, Python, go-templating).
  Typical durations differ by target: see its reference.
- **`skipDelete: true`** leaves the control plane and the cloud resources running. Say so before you run.
- **Stuck threshold: `min(15 min, timeoutSeconds / 3)` with no new log output.** A fixed 15 minutes never
  fires on a 300 s test, which fails at 5 minutes. Crossing it starts an investigation (Phase 5); it is not a
  verdict.

## Phase 4: Run it

One idiom on both targets; only the target flags differ:

```bash
{ echo "START=$(date +%s)"
  up test run "tests/e2etest-<n>" --e2e <target flags>
  echo "EXIT=$?"
  echo "END=$(date +%s)"; } > /tmp/e2e-<n>.log 2>&1
```

- **The exit marker and the timestamps go into the log**, so the log alone is the record. An `echo` placed
  after the redirect goes to stdout, and a wait for it in the log never ends.
- `--function-logs` is rejected with `--e2e` and no `_output/e2e*` is ever written: this log is the only
  evidence. Without it you have nothing, and nothing is not a pass.
- **Foreground** when the worst case fits the longest timeout your harness allows for one command: the call
  returns the complete log in one result.
- **Otherwise in the background**, with your harness's own facility (charter §1; never detach it yourself with
  `nohup` or `&`). **Whatever runs it in the background must not have a shorter timeout than the run:** give
  it the worst case from Phase 3; a run cut off mid-install can leak its control plane (charter §1). Wait for
  the process to exit with bounded waits only:

  ```bash
  for _ in $(seq 1 30); do grep -q '^EXIT=' /tmp/e2e-<n>.log && break; sleep 20; done
  tail -5 /tmp/e2e-<n>.log
  ```

  Size each wait to fit one command's timeout, and repeat until `EXIT=` is in the log. Never an unbounded
  `until grep …`: if the marker never arrives, it waits until the harness kills it. If the process is gone
  (`pgrep -f '[u]p test run'` prints nothing) and there is no `EXIT=` line, the run was cut off: report what it
  reached, not an outcome. With no background facility, run in the foreground with the longest timeout you
  have, and treat a timeout the same way.
- **Never write a verdict from a poll.** A partial log is a progress view: resources routinely reach `Ready`
  after your last look. The run is over only when `EXIT=` is in the log.
- If you stop a run early (wrong target, stuck with a terminal cause), say it was **terminated** and why. A
  killed run has no outcome, and may have skipped teardown: clean up as
  `control-plane-project-charter/references/charter/targets.md` (Teardown and leftovers) says before you
  report.

**Then check the target the run used.** The first progress line names it:

```bash
grep -m1 -E 'Creating (local )?development control plane' /tmp/e2e-<n>.log
```

```text
Creating local development control plane...          <- local kind
Creating development control plane in Spaces         <- Space
```

If it contradicts the target you stated, **the result is void**, even with `EXIT=0`: report the mismatch, not
a pass. In the background, check as soon as the line appears and terminate on a mismatch. A pass on one target
is no evidence about the other.

## Phase 5: While it runs

Between bounded waits, read the log's tail to keep the user informed and spot a stuck run. Mention errors
briefly with a timestamp; analyse only when stuck.

**Most alarming strings during provisioning are transient**, and calling one fatal stops a run that was about
to pass: before you call an error terminal, read
[troubleshooting.md](references/troubleshooting.md#transient-or-terminal).

**Stuck** = no new log output for the threshold from Phase 3. First check the resource is not still `Creating`
(`crossplane beta trace`); slow cloud resources (NAT gateways, RDS) are normal. Otherwise investigate with the
brief in [troubleshooting.md](references/troubleshooting.md): hand it to a sub-agent to keep your context
small, or follow it yourself. The target's reference says how to reach the control plane while it exists.
Stop the run only if the investigation finds a terminal cause; otherwise let `timeoutSeconds` end it.
`up: error: context deadline exceeded` is not a diagnosis; report the underlying Configuration or Provider
condition instead.

## Phase 6: Report

**Every claim must trace to captured output.** Before writing a line, produce these three. If you cannot,
the report is **"UNVERIFIED — could not confirm"**, not a pass:

```bash
grep -E '^(START|EXIT|END)=' /tmp/e2e-<n>.log   # exit code, and the run's own start and end
tail -30 /tmp/e2e-<n>.log                       # the run's final output
```

1. the `EXIT=` line; a non-zero exit is a failure however the output reads;
2. the log's last 30 lines;
3. the duration, `END - START` from the log.

Then:

- **Quote the raw lines** the verdict rests on: the summary, the chainsaw step lines with their times
  (`--- PASS: chainsaw/apply (79.15s)`), the `Cleanup summary` line.
- **Durations come from the run's own timestamps:** `END - START`, or a step time printed in the log. Never
  derive a duration from file timestamps (a log's or any file's birth or modification time), and never
  estimate: an unrelated file's timestamp once turned a 6-minute run into "~95 min".
- **Readiness is what you read.** The assert step passing in the log is the evidence. A resource read must be
  taken while the control plane exists: both targets tear it down after every test. Quote a status value read
  during the run as "read-back, not asserted" (how, on kind: [local.md](references/local.md)).
- **A claim about the provider comes from the provider:** its own read (CLI or SDK, whichever is installed),
  taken before teardown (when: [local.md](references/local.md#reaching-the-cluster-while-it-runs)), and
  quoted. Reading back the XR or your manifest proves only that your input round-tripped. Without that
  read, say "not verified at the provider".
- **Cleanup:** the target's reference says what proves it.
- **Re-read your evidence before the verdict.** Grep what you are about to paste for `False`, `Creating`,
  `Failed`, `FAIL`. If any appears, explain it or correct the verdict.
- Never call anything "production-ready"; that is the caller's judgement.

Shape (templates in [report-templates.md](references/report-templates.md)):

- **Pass:** 5–10 lines: test, target, exit code, duration from the log, resources, cleanup evidence.
- **Stuck or failed:** 50–100 lines: test, phase, last output, analysis, proposed fixes.
- **Cannot verify:** say so, name the missing artifact, and stop. An unverified run reported as a pass is
  worse than a failure: it gets relayed onward as fact.

## Never

- Start a run with a precondition unmet, or with no target named.
- Write a verdict from a poll, or report an outcome for a run that was terminated or cut off.
- Derive a duration from file timestamps, or estimate one.
- Report readiness or provider state you did not read.
- Re-run a green e2e only to read a status value: read it during the run, or report "not read back".
- Run an e2e test program by hand with real credentials, or print or save its output: it carries the
  credential Secret. Check or diff it with a dummy `UP_*` value (author-tests' `e2e.md` reference).
- Local: connect to, apply to or delete a kind cluster or container this run did not create. Names
  such as `<project>-uptest-<test>` repeat across runs, and a cluster you find may hold live cloud
  resources; how to tell yours: [local.md](references/local.md#preconditions).
- Space: **never add `--public` on your own initiative: it permanently publishes the user's package.** Only
  the user chooses it; an orchestrating agent may relay the user's explicit choice in its brief, never make it.
- Space: **never create a group, space or control plane** as a side effect (charter §9).
- Space: pass a `--kubeconfig` path you did not write and check in this run.
