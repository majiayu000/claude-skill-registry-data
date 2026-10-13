---
name: adversarial-audit
description: Audit one Ergopti driver adversarially with reproducible evidence, without implementing fixes. Use for robustness audits, latent-bug searches, "fais un audit AHK", or "fais un audit Hammerspoon"; use perf-profiling for performance-only audits.
---

# Adversarial audit

Adopt an adversarial stance: the goal is not to confirm the code works, it is to
find the input, state or timing that breaks it.

Read only the matching scope reference, plus the report contract before writing
the deliverable:

- AutoHotkey: [references/ahk.md](references/ahk.md)
- Hammerspoon: [references/hammerspoon.md](references/hammerspoon.md)
- Output: [references/report-contract.md](references/report-contract.md)

This skill audits and reports. Do not edit production or test code unless the
user separately asks to implement the findings.

## The five guarantees

Audit against these, and state which one each finding violates:

- **G1 — Robustness.** No unhandled exception, crash or keyboard lock-up in _any_
  state: normal, suspended, paused, mid-layout-switch, mid-config-reload,
  updater-poll, cold start, first boot.
- **G2 — No missing output.** No silent no-op: every user action produces its
  effect or a loud failure.
- **G3 — No races.** Every async boundary (timer, hook, InputHook, HTTP, watcher)
  is safe against reentrancy and out-of-order completion.
- **G4 — No lag.** No perceptible latency on any hot path.
- **G5 — Truthful preview.** A tooltip or preview predicts the exact behavior
  the owning engine would produce in the same state.

## Method

1. **Map the entry points** — every hotkey, hook, timer, watcher, menu action,
   external trigger.
2. **Audit module by module**, then **flow by flow** end-to-end. Module-local
   review misses the interaction bugs, which are the expensive ones.
3. **Question every async boundary.** What happens if it fires twice? Out of
   order? While suspended? Before init? After teardown?
4. **Loop until dry.** Keep sweeping until two consecutive passes surface nothing
   new. A fixed finding count means you stopped early, not that the code is clean.

Bug classes worth a dedicated sweep: unguarded map/table access, state read
before init, load-time vs runtime registration, missing suspend guards, swallowed
exceptions, non-reentrant handlers, sync I/O on a hot path. The scope references
add platform-specific failure modes and current refutations.

## Proof discipline — every finding must carry

1. **A concrete repro sequence** — the exact steps and state.
2. **The root cause**, not the symptom.
3. **Why it is silent today** — what swallows the error or hides the no-op.
4. **Severity + confidence**, stated separately.
5. **A regression test encoding the root cause** (see `ship-fix`, `meta-test`).

A finding without a repro path is a hypothesis. Label it as one.

## The evidence rule — read this twice

**Re-derive every artifact you cite, from the artifact itself, before citing it.**

The cautionary tale here is a **refutation that was wrong**, which is worse than
the finding it killed. The second 2026-07-20 audit declared the first audit's
performance section fabricated — "zero `Slow` lines exist in any log". A third
pass re-derived the disputed figures independently and got them _exactly_:
`Tooltip.ResolvePos` max 2560.3 ms, `OnChar` max 701.3 ms, 8 958 `Slow` lines
across 10 days. The debunker had searched `<ConfigDir>/ahk/logs/` — a directory
that never existed — instead of `<ConfigDir>/autohotkey/logs/`
(`_AhkSubDir := "autohotkey\"`), and `<ConfigDir>` is itself redirected by
`%APPDATA%\Ergopti\paths.toml`. A real 2.5-second stall on the typing path was
dismissed as unmeasured and stayed open an extra cycle.

Consequences to internalise:

- **Hold refutations to the same standard as findings.** "This evidence does not
  exist" is a positive claim about the world and needs proof of where you looked.
  Absence of evidence at the wrong path is not evidence of absence.
- **Resolve the logs path before concluding anything about logs.** Read
  `LogsDirPath` in `paths.toml` first (empty means the OS default below).
- **Never present a sub-agent's or tool's output as measured evidence** without
  opening the artifact yourself. Aggregating an unverified claim launders it.
- **Cheapest possible check first**, run at the _correct_ path:
  `awk 'index($0,"Slow")>0{c++} END{print c+0}' <log>`.
- **Be fair when you suspect fabrication.** Prefer "I could not locate the artifact
  at X, Y, Z — where should I look?" over "this was invented".
- **Label the provenance of every claim.** "Derived from reading the code" is a
  perfectly respectable basis for a finding. Dressing it up as a measurement is
  not. G4 in particular is unmeasured on this driver unless you have a log line
  to quote.
- Where logs live: `%LOCALAPPDATA%\ergopti_plus\logs\` on Windows,
  `~/Library/Logs/ergopti_plus/` on macOS, unless `LogsDirPath` in
  `%APPDATA%\Ergopti\paths.toml` (macOS: the launcher-managed paths.toml) moves
  them; logs written before 2026-09 are in the old `<ConfigDir>/autohotkey/logs/`
  and `<ConfigDir>/hammerspoon/logs/`. There is a dedicated errors-only sink and
  14-day retention. Getting this path wrong is precisely what produced the false
  refutation above. Files found elsewhere (e.g. `D:\tmp`) may be **test harness
  output** rather than driver output — check before attributing them.
- Caveat when dating events: the log **filename carries the date the driver
  started, not the date of the entries** (the path is resolved once at init), so a
  file named `..._07-11.log` can hold entries from the 14th. Read the line's own
  timestamp; never date an event from the filename.

## Deliverable

Follow `references/report-contract.md`: write a human report and validated
`findings.json` under a dated `docs/audits/<scope>/` directory. Include an
executive summary, confirmed findings by severity, performance evidence with
provenance, memory watch-list status, rejected hypotheses, and a coverage
register. Be explicit about gaps — silence reads as "covered".

## Constraint

Never propose weakening or deleting a test to make a change pass.
