---
name: benchmark-checklist
description: Use only when the user explicitly invokes benchmark-checklist to vet a performance measurement (limiter, tuning, limits, errors, repeatability, relevance, and whether the work happened) before reporting or acting on it. Runs only the existing measurement of trusted code and installed, unprivileged profilers; asks before running unconfirmed code or making other changes.
license: MIT
disable-model-invocation: true
---

# Benchmark Checklist

Run only when the user explicitly invokes `benchmark-checklist`, such as
`$benchmark-checklist` in Codex or `/benchmark-checklist` in Claude Code. A
generic performance question or a reference from another skill, including
[explain-the-number](../explain-the-number/SKILL.md), does not activate this
workflow.

Use it when you produce a performance number: a change's before and after, a
regression claim, a tuning harness, or a library or configuration choice.
Answer each question with evidence from a run, not a guess about the code.

Pick the mode before you run:

- **Full** (default): every question below is required.
- **Ballpark**, only when the user asked for a quick ballpark: one run is
  enough, and questions 4 and 7 are required. Label the result a one-run
  estimate. Skip the other questions unless that run looks wrong. A choice
  between options is never a ballpark.

A check the mode requires and you did not run is a gap; see the verdict rule in
the Report section.

## Scope of execution

Before running, name the command and the revision of the code it runs.

When that code is the user's own or otherwise trusted, such as the user's
working tree or a reviewed branch, the invocation authorizes running the
existing measurement and profilers that are already installed and need no
elevated privileges, in the local workspace, as often as the questions below
ask. When you cannot confirm the code is trusted, such as an unreviewed
contributor branch or a downloaded script, get the user's specific
authorization for that run, or report it as not run.

Ask the user before:

- editing the measurement script, such as adding an error or work count;
- tuning a side's configuration, build, or data;
- installing a tool, using `sudo`, or changing dependencies;
- putting load on a shared, remote, or production system.

A step not run, including one the user did not authorize, is a gap under the
verdict rule in the Report section.

## Before you run anything

- Before any run, including a trial run, write down the decision the number
  feeds, the result that would change it, and the noise floor. Take the floor
  from earlier recorded runs; without them, write it as a stated estimate,
  which question 5's measured spread then checks. This is the first rule of
  explain-the-number, required here because an explicit run does not load
  that principle.
- Write down the claim you expect to make, in the words you would ship
  ("export is 30% faster at p50 on the 60k-row dataset"). The questions test
  that sentence.
- Read the measurement script. Note what it times, counts, and ignores.
- Check how busy the machine is (for example `uptime` and `nproc` on Linux, or
  the platform's equivalent). If it is busy, find out what is running. If you
  cannot stop it, interleave the sides so both see the same noise, and say so
  in the report.

## The questions

1. **Why not double?** Name the limiter. Profile in a run you do not report,
   because profilers and tracers slow the work down. Use CPU per process, a
   runtime profiler, I/O wait, and syscall counts (for example `top`,
   `pidstat`, `node --cpu-prof`, `py-spy`, `perf`, or `strace -c` on Linux;
   the platform's equivalent counts), then map the hot spot to source. Watch
   the load generator too: if it saturates first, you measured the load
   generator. If a change did not move the number, the limiter explains why,
   so find it before you call the change useless.
2. **Was it tuned?** Run every side the way production runs it: release
   builds, production flags and environment, batching and transaction
   settings, connection pools, caches as warm or cold as production sees them,
   and the same versions and data. If one side runs on defaults, you compared
   configurations, not implementations. A limiter that is a setting (a commit
   per row, a debug build, a missing index) means that side is untuned. Tune
   it, with the user's approval, and measure again before you pick a winner.
   If you cannot tune it, do not pick a winner from that run. When the user is
   choosing what to adopt, narrowing the claim to the code as it ships today
   does not fix this, because they adopt the option, not today's settings.
3. **Did it break limits?** Do the arithmetic. Compare bytes per second with
   disk and network bandwidth, operations per second times cost per operation
   with your cores, and the time saved with the time the changed piece took.
   Removing a piece that takes 10% of the run can make the run at most about
   11% faster. A result past a limit measured something other than the work,
   such as a cache, a no-op, or a bug.
4. **Did it error?** Count failures and non-success responses, and check that
   outputs are correct, not just present. Rejections are often fast, and
   timeouts and retries are slow. If the script does not count errors, ask
   before adding the count, or count them from its output.
5. **Does it reproduce?** Run each side at least 5 times, alternating (A, B,
   A, B, and so on) so warmup, lazy initialization, caches, and drift favor
   neither. Record the median and range, and compare the measured spread with
   the noise floor you wrote down; the verdict rule in the Report section says
   what each outcome means. When the call is close, use a rank-sum test or the
   harness's own statistics.
6. **Does it matter?** Next to any micro result, measure the end-to-end path a
   user waits on, with realistic data sizes and concurrency, and report the
   micro result as a share of the whole. A helper that takes 1% of a request
   can make the request at most 1% faster, however fast the helper gets.
7. **Did it even happen?** Confirm the work ran inside the timed region: the
   request reached the server, the rows were written, the bytes were read, and
   the code used the result. Lazy code (generators nobody iterates, promises
   nobody awaits, results the JIT can discard) and timeouts produce numbers for
   work that never happened.

## Report

- Lead with the verdict: faster, slower, no measurable difference, or
  inconclusive. In ballpark mode, label it a one-run estimate.
- Verdict rule: any check the mode requires that was not run makes the verdict
  inconclusive; name each gap. In full mode, the verdict is also inconclusive
  when the measured spread is larger than the written noise floor, when you
  claim a difference but cannot name the limiter, or when a side ran untuned.
  Otherwise, an effect within the run-to-run spread is no measurable
  difference.
- Give the number with its unit, the run count, the range, and the limiter.
  For example, "p50 41 ms -> 33 ms, median of 7 runs per side, range 32 to
  35 ms after, bound by JSON parsing on one core."
- Keep a report or PR description to one primary number. Keep the runs, range,
  and limiter evidence in the task's existing notes or ignored temporary
  storage; do not create, commit, or publish an artifact the user did not ask
  for.

## Source

Adapted from Lauren Tan's [pstack benchmark-checklist](https://github.com/cursor/plugins/blob/0b46ec399d55f2829e88822998f53b84944837d3/pstack/skills/benchmark-checklist/SKILL.md).
Local changes: explicit invocation; an execution scope that names the command
and revision, runs only the existing measurement of trusted code and installed,
unprivileged profilers, and asks before running unconfirmed code, script edits,
tuning, installs, `sudo`, or shared and remote load; full and ballpark modes
with one verdict rule; the decision and noise floor written before any run,
with an estimated floor checked against the measured spread; tools named as
examples with platform equivalents; evidence kept in existing notes rather than
new artifacts; and the upstream "Other perf material" section dropped, because
its Perf issue and Hillclimb playbooks have no local equivalent. The principle
stays a separate skill, [explain-the-number](../explain-the-number/SKILL.md).
See [LICENSE](LICENSE).
