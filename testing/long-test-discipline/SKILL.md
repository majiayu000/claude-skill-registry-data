---
name: long-test-discipline
description: "Runs long-running tests on a shared host: schedules them in the foreground with timeout wrappers, captures structured logs, enforces resource limits, handles flakes with deterministic reruns, and reports pass/fail with evidence. Use when a test takes minutes, needs a background worker, or fails intermittently."
license: MIT-compat
compatibility: "framework-agnostic; Linux host; pytest; shell; Ottili Biest host"
metadata: {}
allowed-tools: []
---

Standard: name/description/length rules — [agentskills.io standard](../references/agentskills-standard.md).
# Long Test Discipline Skill — Quick Reference (body <500 lines; full procedure in references/long-test-discipline-procedure.md)

## When to use this skill (trigger)
- A single test takes more than ~60 seconds to run (a smoke test that sleeps 5s does NOT fire; a minute-scale integration or load test does).
- You are asked to run something "in the background" on a shared host (this skill replaces `&`/`nohup` with a foreground wrapper).
- A test flakes: it passes alone but fails in a suite, or fails only on the second run.
- You need to prove resource usage (CPU, memory, wall time) for a test.
- A timeout killed your test and you need to know how far it got.
- A test spawns workers or forks and the host reports `fork: Resource temporarily unavailable`.

## Disambiguation
- Fires: a test takes more than ~60s, asked to run in the background on a shared host, a test flakes, proving resource usage, a timeout killed the test, a fork/worker resource error.
- Does NOT fire for: a 5-second smoke test, a one-off local run with no persistence, or CI wiring that is not a long test.

## When NOT to use this skill
- Unit tests that finish in under a minute.
- Tests that require a live human operator.
- Tests that depend on network access that is not available on the host.
- A test that passes in 2 seconds — the skill is for long/flaky tests; a fast unit test runs normally.
- A test that only ever runs in an interactive shell with a human watching — if it can run in CI, it can run in the foreground with a wrapper.
- "Just lower the timeout until it fits" — the skill says fix the hang or split the test; a shrinking timeout is a cover-up, not a fix.

## Decision table — execution strategy
| Situation | Strategy | Pitfall |
|-----------|----------|---------|
| Test takes 2-15 min | `timeout 900 /usr/local/bin/heavy <cmd> > <log> 2>&1; tail -40 <log>` | Running with `&` loses the log when the shell exits |
| Test flakes | Re-run deterministically: same seed, same order, same env | Re-running "as-is" may hide the real cause |
| Test needs a worker | Start the worker in the same foreground command chain; never `&` | A detached worker is killed when the command returns |
| Resource limit needed | Wrap with `ulimit -v` (memory) and `timeout` (wall clock) | `ulimit` is per-shell; set it in the same command that runs the test |
| Test must run in CI | Use the same wrapper script; CI has no interactive shell | Hardcoding `&` works locally but dies in CI |

## Decision table — flake handling
| Observation | Action | Threshold |
|-------------|--------|-----------|
| Passes alone, fails in suite | Re-run with `--randomly-seed` from the failing run | max 2 reruns |
| Fails on rerun with same seed | Real failure — stop, do not rerun again | — |
| Fails on rerun with different seed | Ordering dependency — record seed, fix test | — |
| Passes on rerun, no seed recorded | Not evidence — re-run with recorded seed | — |
| Timeout too short (partial log) | Raise timeout, do not claim pass | log must end with the JSON record |

## Numbered procedure (summary; full recipe in references/long-test-discipline-procedure.md)
1. **Classify the test** — unit (<1 min), integration (1-15 min), or end-to-end (>15 min). Pick the wrapper accordingly.
2. **Write the wrapper** — a small shell script that sets `ulimit`, `timeout`, redirects output to a log, and runs the test. Commit it to `scripts/`.
3. **Run in the foreground** — never use `&`, `nohup`, or `setsid`. Use `timeout` so the command always returns.
4. **Capture evidence** — the log file plus a one-line summary (exit code, wall time, peak RSS).
5. **Handle flakes** — if the test fails, re-run with `--randomly-seed` (if pytest-randomly) or a fixed order; record the seed.
6. **Enforce resource limits** — set `ulimit -v` (virtual memory) and `ulimit -u` (processes) before the test.
7. **Report** — pass/fail with the log path, the seed, and the resource numbers.

## Worked examples
Good (foreground wrapper, recorded seed, JSON record at end of log):
```bash
SEED=42
timeout 900 /usr/local/bin/heavy pytest tests/test_worker.py \
  --randomly-seed "$SEED" --lf > logs/test_worker.log 2>&1
tail -1 logs/test_worker.log
# {"name":"worker","status":"pass","elapsed_s":42,"seed":42,"rc":0,...}
```
Bad (background worker — killed when the shell exits, log never appears):
```bash
python -m worker > worker.log 2>&1 &   # AGENTS.md forbids this
pytest tests/test_integration.py        # worker is dead by now
```
Bad (flake "passed" with no seed — not evidence):
```bash
pytest tests/test_flaky.py            # green, but was it luck?
# re-run with a recorded seed or it does not count
```

## Pitfalls from research (real incidents)
- `&`-backgrounded processes are killed when the launching shell exits; the log never appears.
- A flaky test that passes on rerun hides a real ordering or resource problem.
- `ulimit` set in one command does not apply to a later command; it must wrap the test.
- A timeout that is too short leaves a half-written log that looks like a failure but is just a kill.
- Running the whole suite to "see if it still flakes" burns minutes and gives no evidence.

## Near-miss triggers (act before the incident)
- "Just run it in the background" — use `run_long_test.sh` in the foreground instead.
- "It passed once, it'll pass again" — re-run with a recorded seed.
- "The timeout is probably fine" — check the log ends with the JSON record, not a partial line.
- "Lower the ulimit to make it fit" — raise the limit or split the test; never weaken the test.

## Verification checklist (all must pass before you finish)
- [ ] The test runs in the foreground with a `timeout` wrapper.
- [ ] A log file is produced and contains the final summary line.
- [ ] Resource limits (`ulimit`) are set in the same command that runs the test.
- [ ] Flake reruns use a recorded seed and order.
- [ ] The wrapper script is committed to `scripts/` and is deterministic.

## References
- Full procedure, version table and worked examples: `references/long-test-discipline-procedure.md`.
- Eval prompts with expected behaviour and failure signs: `references/EVALS.md`.
- Primary sources with URLs and retrieval dates: `references/SOURCES.md`.

## Related skills
- [honest-status](../honest-status/SKILL.md) — a long test's outcome is a status item; mark it VERIFIED only after the log shows the JSON summary, not DONE on a half-written log.
- [shared-tree-git](../shared-tree-git/SKILL.md) — commit the wrapper script with explicit paths only.
