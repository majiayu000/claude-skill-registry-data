---
name: dogfood
description: "Fix-through loop: invoke a new thing, fix until it works."
triggers:
  - /dogfood
  - dogfood <target>
  - run dogfood
  - smoke test and fix
  - self-dogfood
argument-hint: "<target> [--narrow|--broad|--shakedown]"
allowed-tools: ["Read","Write","Edit","Bash","Grep","Glob","Agent","Skill","AskUserQuestion","TaskCreate","TaskUpdate","TaskGet","TaskList"]
---

# /dogfood — Smoke-Driven Fix-Through Super-Skill

Invoke a newly-built thing and exercise it until it works or gets replanned. Binary outcome:
converge or switch gears — no third path. "Log to backlog and keep going" is file-and-defer
wearing a dogfood costume.

Distinct from siblings: `/bug-blitz` works a known backlog; `/bug-sweep` searches the repo for
bugs; `/dogfood` invokes a new thing and exercises it until it converges or replans.

**Announce at start:** "Running `/dogfood <target>` — smoke-driven fix-through loop. Binary
outcome: converge or switch gears."

## Invoke When

A new skill/command/script/pipeline needs real-use validation, an install/setup process is new
or changed, a prior shakedown deferred bugs, or the PM authorizes a pass. Not for well-exercised
production code (`/bug-blitz`), latent-bug search (`/bug-sweep`), or static pre-flight
(`coordinator:validate`).

**Self-dogfood-first.** When the target lives in repo X, dogfood it there first — cross-repo
dogfood is a deliberate follow-up, never a substitute. Invoking against a target outside the
current repo surfaces this and requires PM acknowledgment before proceeding.

## Tier

PM declares at invocation (default `--narrow`): `--narrow` — single smoke surface, tight budget,
mid-loop check only if the surface explodes. `--broad` — multi-surface happy path, larger budget,
check-in at budget halfway. `--shakedown` — comprehensive coverage matrix (needs Gate 4), largest
budget, check-ins at halfway and PM pause. Shakedown composes inward — a broad dogfood per tool
plus a coverage overlay, not a separate activity.

## Gates — Precondition, Before Entering the Loop

1. **Idempotent re-run.** The target must be safely re-invocable; fix idempotency first if a
   second run diverges for non-bug reasons. Empirical judgment about the target — in-cone.
2. **Machine-parseable progress.** Tagged stdout, exit codes, or a status file the EM can diff
   pass-to-pass. Write a capture-and-classify wrapper first if the target doesn't already emit
   one.
3. **Framing audit.** Runs first, every invocation, including autonomous — never skipped. When
   the session carries inherited scope language ("verification only," "no scope expansion"),
   surface it and force a confirm: *"This phrase invites file-and-defer. Confirm dogfood
   fix-through posture, not verification-only."* Fix-through is the default; PM overrides only
   with explicit reasoning. Origin: the session/handoff text; the EM reads it, no engine field exists.
4. **Coverage matrix** (`--shakedown` only). PM declares the matrix at invocation; persisted to
   `tasks/dogfood-<target>-<date>/coverage-matrix.md`. Without one, shakedown degrades to
   `--broad` and the EM surfaces that before entering the loop.

Whichever gate's precondition fails, satisfy it as the session's first deliverable, then enter
the loop below.

## Loop

Invoke target → observe every channel (exit code, stderr, status-file claim vs. downstream
behavior, "complete" vs. phase-N failure) → classify each observation (below) → act → write
`pass-<N>-modes.json` → re-invoke → check convergence / switch-gears / PM-stop.

Multiple passes are the normal shape — a fix uncovers the next layer; single-pass "find all bugs"
is forbidden. A cross-channel contradiction (success exit + warning stderr) is a structural bug —
fix the inconsistent signal, not the channel that told the truth.

### Classify Every Observation — Mandatory, Logged to the Flight Recorder

- **In-cone, fix-now (default).** Mechanical fixes — validator gaps, missing fallbacks,
  false-success exits, off-by-ones, idempotency gaps, the skill/script/pipeline body itself,
  production code, hooks/`bin/` helpers, doctrine the target depends on. Default question: "is
  there a real reason this isn't fix-now," not "do I have permission."
- **Out-of-cone, switch-gears.** The fix would reverse a load-bearing structural choice in the
  target — an architectural-shape read the EM makes each time. Loop ends on PM confirm.
- **Surface-and-skip.** Reserved for PM-product decisions, externalities (PRs, signing, network),
  or genuinely-not-this-loop scope — the rare exception. Structured entry `{category, evidence}`
  to `tasks/dogfood-<target>-<date>/surface-and-skip.md`, never `state/bug-backlog/`. Silent
  skips are forbidden.

Skip-ratio and consecutive-skip thresholds: wiki.
<!-- engine-gap: field=dogfood.skip_ratio producer=unknown memo=engine-gap-markers-name-a-memo-that-was-never-filed.md -->

### Per-Iteration Mode Artifact

After each pass, write `tasks/dogfood-<target>-<date>/pass-<N>-modes.json` — `{component,
error-class}` tuples, one per distinct failure mode. `backlog-grind-assemble brief dogfood` reads
the current file against the prior pass and returns the tuple count plus a stuck flag (same
tuples, unchanged) — the mechanical half of the switch-gears signal; acting on it stays an EM
proposal, PM confirm. Each pass also tees a log to `pass-<N>.log`.

### Commits — Tier-Dependent

`--narrow`: EM commits each fix directly via `backlog-grind-assemble apply dogfood`
(`commit-per-item`), smoke evidence in the body. `--broad`/`--shakedown`: fix agents are
edit-and-report only, never commit; the EM serializes at wave gates via `apply dogfood`
(`commit-per-wave`). `--expected-branch` applies only to `--narrow` executor dispatches that
commit. Fixes spanning files for one bug ship as one unit — never split a bug across parallel
per-file executors.

## Switch-Gears

A judgment call, informed by mechanical signals, never automatic: `backlog-grind-assemble brief
dogfood`'s tuple-count/stuck signal, three or more failures traceable to the same architectural
shape, a skip-ratio breach, or a fix that would reverse a load-bearing choice. EM proposes with
reasoning, PM confirms; the session output becomes the replan ask, not a converged thing.

## Loop Exit

All three must hold: primary goal met end-to-end on the latest pass; no new in-cone bugs surfaced
in the last iteration (out-of-cone skips don't count against this); PM signals stop, or EM
proposes converge and PM confirms.

**Not an exit path:** "budget exhausted, file remainder to backlog" — exhaustion is itself a
switch-gears signal. "Zero new bugs this pass" alone — flakes mask a single quiet pass; both
criteria above must hold, not just one.

**PM is loop terminator, not loop driver.** Once authorized, fix-through posture is hardcoded —
mid-loop "should I continue?" is anti-signal.

## Flight Recorder

`tasks/dogfood-<target>-<date>/`: `pass-<N>.log`, `pass-<N>-modes.json` (mandatory),
`surface-and-skip.md`, `coverage-matrix.md` (`--shakedown` only). Never route surface-and-skip
findings to `state/bug-backlog/` — that's a deliberate PM hand-off, not automatic spillover.

## Composition

`/bug-blitz` works the backlog; dogfood doesn't file remainder there — switch-gears output is a
replan, not a backlog dump. `/bug-sweep` is repo-driven; dogfood is invocation-driven.
`coordinator:validate` is static pre-flight, before the first pass and after the loop, not a
substitute. `/dogfood` exit emits a workstream-complete-shaped summary but doesn't invoke it — PM
may chain. Doctrine drift surfaced mid-loop files to `state/lessons/` for `/learn-lessons`,
out-of-loop by design.

## Final Summary — Report by Exception

Two lines always; everything else only when not clean.

```markdown
## Dogfood Session Complete

**Target:** <target> (tier: --narrow/--broad/--shakedown)
**Verdict:** <converged: thing works | switch-gears: replan ask | stopped: open observation was X>
```

Append only when true: `**Bugs fixed this session:**` (count + one-line characterization) when
≥1; `**Surface-and-skip:**` (count + one-line characterization) when ≥1. No `Outcome`, `Passes
run`, or standalone `Tier` line — redundant with `Verdict`/`Target`/the flight recorder. No commit
SHAs or per-item evidence pointers in the reply — those live in the commit body and
`surface-and-skip.md`.
