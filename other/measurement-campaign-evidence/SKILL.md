---
name: measurement-campaign-evidence
description: >-
  Benchmark the shipped candidate across sizes or topologies against a numeric acceptance threshold.
  When cold start, p95 latency, footprint or a ratio decides pass/fail, pin the payload, measure
  serially and reject mixed report sets or shortcuts in the comparator. Not for
  package-release-verification.
metadata:
  revision: "4"
  areas: "software-development,work-management"
  targets: "runtime-agnostic"
  summary: "bind the candidate, measure serially, keep one report set, never let a comparator fake a latency"
  summary_zh: "测量活动：先钉候选身份、串行跑、一致报告集，不让基线伪造延迟对比"
  kind: "entry"
---

# Measurement campaign evidence

A campaign is the evidence phase of a goal whose completion condition is *measured*: sizes ×
topologies, a packaged artifact, a browser/runtime profile, a comparator tree, overload controls. The
repeatable failure is not a missing number — it is a number belonging to a slightly different artifact
than the one the record claims. For the surrounding delivery loop and its gate verification rules see `gdd`.

## When to use

- A goal says "measure A against B at N sizes" or "accept only if p95 < X".
- A prior campaign exists but its reports came from a dirty tree, a mixed artifact, or a pre-change
  instrument.
- A delegate hands back a campaign with a summary table.

## 1. Bind the candidate before measuring

- Measure the **shipped artifact**, not the checkout, whenever the goal claims the package works: build
the tarball, install it into a scratch prefix, and drive the instrument with the package's own entry
file (`<prefix>/node_modules/<scope>/<name>/bin/<cli>.mjs`). A `node_modules/.bin/<cli>` symlink hides
the package manifest from an identity hasher, so the report records no installed-package or tarball
hash and cannot prove which bytes ran.
- Pass the tarball to the instrument when it validates one (flag or env var); it compares the tarball
payload with the installed tree and refuses a mismatch.
- After the campaign, verify **every** report carries the same payload/tree hash. One divergent report
means two artifacts were measured and no aggregate from that set is valid.

## 2. An interrupted run poisons the candidate

An instrument that hashes the installed package fails later runs with `payload does not match installed
package` when a killed build left its scratch directory inside the package (`<pkg>/.<tool>-build-*` and
siblings). Successful runs clean up; kills do not.

1. Reinstall the prefix from the tarball and delete stray scratch dirs.
2. Re-run the cheapest workload and confirm the payload hash equals the earlier reports before spending
   minutes on the large ones.
3. Keep long campaigns away from anything that restarts your supervisor — a gateway/service restart
   mid-build is what creates the poisoned state, and the campaign restarts from that workload.

## 3. Require a comparable measurement

Never synthesize latency from a structurally different path or weaken the corpus so the comparator
passes. Report no delta unless the numbers can be put on the same clock. If the comparator cannot
run the standard instrument or timer origins differ, read
[comparator measurement](references/comparator-measurement.md) before reporting the result.

## 4. Report the target metric alone, and the cost beside it

- Quote the metric the goal defines, in its own definition (for example dispatch to validated result,
excluding rendering).
- Then report what a maintainer must rule on — render cost, largest-list cost, transfer — as their own
columns, even at ten times the target. A passing headline that hides the material UX number is a P1 in
the evidence record.
- State the emulation channel that actually ran: a bundled Chromium is not "Chrome", and Chrome is not
"Edge". Note which target the throttle applies to (page vs worker) and that loopback is not a network.
- Keep the raw per-workload reports plus their digests; the aggregate table is derived, the reports are
  the evidence.

## 5. Accepting someone else's campaign

- Re-run at least one workload and one overload control yourself on a committed tree; a summary table
  is a claim.
- Check how the reported run got its result. A campaign whose gate is a clean tree or a stable candidate
  identity can be run through a defeated gate — `git update-index --assume-unchanged` (`git ls-files -v`
  shows a lowercase flag), `--no-verify`, a stub on `PATH`. That is disqualifying, not thorough: the
  numbers belong to a tree state you cannot reconstruct. Commit, re-run, then quote.
- A control that fails for an *instrument* reason (a child runner changed where it writes its
  machine-readable output) is a real defect to fix in the instrument, and the whole affected control set
  has to be re-run afterwards — not waived.

## 6. Execute serially and size the host

A 10,000-item workload builds for minutes and peaks near 1 GB. Two of those beside a test suite on an
8 GB host is an OOM the kernel resolves by killing whichever job it dislikes. One workload at a time,
no suite in parallel, and record peak RSS per workload so the next campaign can budget the host.

## Output shape

1. Candidate identity line: version, tarball digest, payload/tree hash, instrument source hash.
2. One row per workload: target metric, its inner cost, the drawing/transfer cost, failures.
3. Controls: each bound, the observed overshoot, the bounded failure, the retry.
4. A limits section: emulation not hardware, throttled target, loopback, which memory instruments are
   unavailable, and which comparator could not be measured.
5. What the maintainer must decide, as a short numbered list — never a conclusion the evidence does not
   own.

## Pitfalls

- Aggregating reports without checking that all of them share one candidate hash.
- Driving the instrument with the `.bin` symlink and losing the package identity the goal requires.
- Treating an instrument refusal on a comparator as a setup bug and "fixing" it by weakening the fixture.
- Letting a failing large or hub-heavy case disappear into an average; the goal usually forbids it.
- Reporting a south-of-target headline while the drawing cost tripled, so the maintainer accepts a UX
  trade-off they never saw.
- Running the campaign beside a full test suite on a host sized for one.
