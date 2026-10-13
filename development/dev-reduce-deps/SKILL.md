---
name: dev-reduce-deps
description: >-
  Audit a project's dependencies and remove the unnecessary ones — dead declarations, dead code
  holding a library alive, redundant/overlapping deps, and unmaintained deps needing a decision. Use
  when: (1) User says '/dev-reduce-deps', 'check our deps', 'confirm our deps', 'reduce
  dependencies', 'kill unnecessary deps', 'unused dependencies', 'dependency audit', 'slim the
  dependency graph', or 'can we replace this lib with our own code', (2) A lockfile has grown
  uncomfortably large, (3) Before a release or a supply-chain review, (4) A dependency is discovered
  to be deprecated, archived, or unmaintained. Covers Rust/Cargo and JS/npm/pnpm. Carries an
  accumulating cross-project verdict reference so a dep judged once is not re-litigated, a hard
  abandon rule that stops 'replace it with our own script' from turning into an unbounded rewrite,
  and an adversarial pass that attacks every removal verdict before it is acted on.
user-invocable: true
argument-hint: "[path (default: repo root)] [--rust | --js] [--plan]"
---

# dev-reduce-deps — find and remove unnecessary dependencies

Audit the dependency graph, remove what is provably unnecessary, and **write down what was kept and
why**. The register of deliberate keeps is as much the deliverable as the removals — without it, the
next audit re-derives every decision from scratch.

## The one principle that governs every verdict

The axis is **used vs unused**, not *free vs costly*.

- A dep **directly imported by first-party code stays a direct dependency** even when something else
  in the tree also pulls it. A transitive dep is not a supported import surface — relying on one is a
  latent break the day that intermediate package drops it.
- A **genuinely unused declaration is removed even when the package stays in the lockfile**. It still
  buys feature hygiene, clear ownership, and a smaller audit surface.

So a dep that is directly used and also transitively present is described as **"directly used; zero
package-count payoff from replacement"** — never "free", which invites a pointless removal.

**Always state which kind of win a removal got.** Never claim a package-count reduction the lockfile
does not show. Removing a redundant umbrella crate whose sub-crate is pulled anyway can be worth doing
and still change the lock file by exactly zero packages — say that plainly rather than implying a
graph win.

## Workflow

### Step 1 — Read the accumulated verdicts first

`references/verdicts.md` holds per-dependency findings from previous runs **across all projects**,
plus the general patterns that transfer between them. Read it before touching the current project so
work already done is not repeated.

Treat a recorded verdict as **evidence, not a rule**. The same dep in a different project has
different call sites, a different platform surface, and a different blast radius — a KEEP recorded
elsewhere may not hold here, and a REMOVE certainly does not authorize a blind removal. Re-check the
call sites in *this* project; the reference tells you what to look at and what bit someone last time.

### Step 2 — Inventory and run the detectors

Read the ecosystem guide for what applies:

- **Rust / Cargo** → [references/rust.md](references/rust.md)
- **JS / npm / pnpm** → [references/js.md](references/js.md)

Both cover: which detector to install and run, the false-positive classes that detector cannot see,
and the tree/feature commands that answer "who actually pulls this".

A monorepo usually has both — run each and keep the findings separate; the failure modes do not
overlap.

**Inventory the scripts, not only the manifests.** A tool a build shells out to — `pnpm dlx`, `npx`,
a bare binary in a CI step — is a dependency that no manifest declares, no lockfile pins, and no
detector reads. It is also the class most likely to sit on the deploy path. The ecosystem guide has
the sweep commands.

**Detectors are a starting point, never a verdict.** Every one of them reports declarations it cannot
see a use for, and each ecosystem has categories of dependency that are load-bearing while looking
completely unused. Those categories are the most expensive mistakes available here, which is why each
guide leads with them.

### Step 3 — Capture baseline oracles before editing anything

Claims of "nothing changed" are unverifiable after the fact. Capture first, on the untouched tree:

- **Package count** — the lockfile's package total. Take it *after* collapsing stale duplicate
  resolutions (JS: `pnpm dedupe`), or every later claim is measured against an inflated baseline. That
  collapse is usually a free win in its own right — no manifest edit, no behavior change.
- **Feature graph** — the feature-edge view (Rust: `cargo tree -e features`). Removing a dead *direct*
  declaration can still change which features a crate resolves with, and workspace feature unification
  hides it.
- **Build output fingerprints** — content hashes in emitted asset filenames, bundle sizes. These are
  what catch a "harmless" change that silently altered output.
- **Current CI state.** If a check is already red on the parent commit, its contract for this work is
  **no new failures**, not green. Never fix unrelated pre-existing debt to manufacture a clean
  baseline — report it instead.

### Step 4 — Triage into three buckets

Order the work **certain → judgment-heavy**, so value lands even if the tail stalls.

| Bucket | What qualifies | Handling |
|---|---|---|
| **REMOVE** | Zero call sites anywhere, verified by hand — not just by a detector. Includes a dep whose only consumer is dead code. | Delete the declaration and its now-orphaned rationale comment. Behavior cannot change. |
| **KEEP** | Directly used; or cheap, maintained and correct; or a replacement trips an abandon trigger. | Record the reason at the declaration and in the register. A documented keep is a completed result. |
| **DECIDE** | Deprecated, archived, or unmaintained, but load-bearing. | Produce a written evaluation. **"Stay, with a named blocker" is a valid outcome** — do not force a migration to satisfy the framing. |

**Look for dead code, not just dead declarations.** The most valuable removal in a real audit was an
unwired `#[allow(dead_code)]` struct whose deletion took four packages out of the lock file. A library
kept alive by code nothing calls is invisible to every detector, because the code *does* import it.

### Step 4.5 — Attack every REMOVE verdict before acting on it

REMOVE is the only verdict that can break the build, and the failure modes that survive to this point
are precisely the ones a careful read already missed — that is *why* they survived. So do not re-read
your own reasoning; attack it from a different angle.

Three lenses, each asking a different question:

| Lens | The question it asks |
|---|---|
| **Hidden consumption** | What consumes this that an import grep cannot see? A plugin **named as a string** inside a bundler config, a component file the detector cannot parse, a binary whose package has a different name, config files, a CLI binary in a `scripts` entry, plugin auto-resolution, a computed `import()`, a barrel re-export, **another branch**, a sibling workspace package, a subprocess spawned from non-JS code. |
| **Behavioral fidelity** | For a replacement rather than a delete: which real input breaks it? Escaping, Unicode/CJK, locale and timezone, error contracts callers depend on, stream/async semantics, numeric precision. |
| **Value vs churn** | What does this actually free? Zero packages and no lifecycle script means the removal buys nothing and leaves code to maintain forever. |

**Default to KEEP when a lens is inconclusive.** A wrong REMOVE costs a broken build; a wrong KEEP
costs one line in a manifest. The asymmetry is not close.

In an autonomous or multi-agent run make this a real step, not a re-read — spawn one skeptic per lens
whose instruction is to *refute*, not to confirm, and demote the verdict when a majority refutes. In a
53-verdict audit this caught four removals that each looked well-evidenced:

- A diagramming library with **zero usage on the working branch** and three live call sites on a
  long-lived drafting branch (hidden consumption — branch scope).
- An ML background-remover with zero imports that was an **optional peer consumed through a wrapper**,
  on the default code path (hidden consumption).
- An S3 client whose proposed lighter replacement rested on a **signing claim that was false for S3**
  (behavioral fidelity).
- A frontmatter parser whose 15-consumer rewrite would have freed **zero packages**, because the
  framework that renders the docs depends on it anyway (value vs churn).

Every one would have shipped as a confident, well-cited removal.

### Step 5 — Replacing a dep with first-party code: the abandon rule

**First, check who else retains it — this gate kills most replacement ideas for free.** If anything
else in the tree depends on the package, hand-rolling your call sites frees *zero* packages and
removes *zero* supply-chain surface, while leaving you owning the code forever. Ask before writing a
line:

```bash
pnpm why <dep>            # any consumer besides your own manifest?  (Rust: cargo tree -i -p <crate>)
```

A first-party package of your own is the easiest one to miss, and it retains the dep just as hard as a
third-party one. In one audit `chalk` and `glob` were retained by the org's own lint package — which
runs on every CI gate — so rewriting 153 call sites would have freed nothing; `uuid` was retained by a
charting library that was itself a KEEP; and a frontmatter parser was retained by the docs framework.
Three separate "obvious utility replacements", all worth exactly zero.

A retained dep can still be worth removing from *your* manifest when the declaration is genuinely
unused (feature hygiene, clear ownership) — but say plainly that the package count does not move, and
never spend a rewrite on it.

"This is just a utility, we can write it ourselves" is where dependency audits go wrong. Rewriting an
external tool's behavior has no natural finish line: every round finds a genuinely new divergence, so
the reviewer is right every time and the work never converges. A real run of this failure produced a
fix sequence that *grew* — +366, then +953, then +1986 lines — before anyone stopped it.

So a replacement attempt ends immediately when **any** of these fires:

1. It exceeds **40 lines of formatted non-test production code**, counted across every file it
   touches. Compressed one-liners do not evade this.
2. It needs a **second corrective round**. One implementation plus at most one fix.
3. It requires `unsafe`, FFI, OS-specific branches, polling loops, signal supervision, or Unicode
   tables. These are immediate keeps regardless of line count.

**On trigger:** restore the dep, delete the replacement, and record a **terminal KEEP** — a completed
outcome, not a failure. Note in the report that removal of that dep is settled, so a later review pass
does not simply re-propose it. Without that closing note an autonomous fix loop reopens the same
removal on its next round, which is exactly how the runaway above happened.

A cheap, zero-transitive, maintained, correct dependency is not worth hand-rolling. Reach for a
replacement only when the dep is genuinely heavy, genuinely abandoned, or genuinely one function.

### Step 6 — Verify

Scope the verification to what actually changed, then check the things a normal build misses:

- Build and test the affected packages, plus a full-workspace build.
- **Diff the feature graph against the Step 3 baseline.** Every delta must be an intended removal; an
  unintended feature change is a finding.
- **Compare build-output fingerprints.** Content hashes must not move.
- **Verify a migration by running it, not by reasoning about it.** When a verdict rests on "these
  tests would pass under the other runner" or "this replacement is equivalent", go execute it in a
  scratch copy and report the real numbers. The most trustworthy verdict in one audit read "6 files /
  47 tests pass in 3.92s (baseline 16.5s)" — measured, not predicted — and it was the only migration
  nobody had to re-litigate.
- Run the **conditionally-compiled targets** a default build skips — feature-gated tests, alternate
  feature combinations, other compile targets. Each ecosystem guide names these.

**Never edit a test assertion to make a removal pass.** If a hash moves or a line number shifts, that
*is* the finding. A gate made green by editing the assertion it was checking has been disabled, not
satisfied.

In any parallel or multi-agent run, give the **lockfile a single owner per wave** — workers edit
manifests only and never stage a lockfile; one integration step regenerates it and proves it with a
frozen install (`pnpm install --frozen-lockfile`, `cargo build --locked`).

The obvious hazard is a conflict on a huge generated file. The subtler one is worse and silent: two
branches each *legitimately* retain a shared transitive package because the other branch's removal has
not landed yet, and after both merge cleanly, **neither lockfile deleted the now-orphaned package**.
There is no conflict to alert you — the graph is just quietly wrong. A single regeneration on the
merged manifests is the only thing that catches it. Resolve any conflict by regenerating, never by
hand-merging hunks.

**Delete your own probes before reporting.** Verifying a migration by actually running it (below) is
right, but the scratch copies, alternate configs, and scratch test files it needs are not deliverables
— and a new test glob will happily pick them up. One audit left 14 untracked probe files behind after
reporting the tree clean. Check `git status --short` yourself rather than trusting the claim.

### Step 7 — Report, register, and record

Produce a report using verdict-style headings (the heading states the outcome, not the topic).
Cover, at minimum:

- **Removed** — each declaration, its evidence, and the *actual* lockfile delta it produced.
- **Considered and kept** — with specific reasons. This is the half that stops the next audit from
  redoing the work.
- **Explicit non-goals** — consolidations deliberately not attempted, and why.

For a project worth a standing record, write a **`DEPENDENCIES.md`** in the repo carrying those
sections plus duplicate-version notes and any deliberate duplication (e.g. a pin intentionally
repeated across two manifests). Consider a **regression guard** so dead declarations do not
re-accumulate — the detector wired into the existing local pre-push gate and CI job. Adding it to an
*existing* job is cheap; adding a new required check is a governance change and usually out of scope.

Then **record what was learned back into the skill**, so the next project starts ahead:

```bash
"$HOME/.claude/skills/dev-reduce-deps/scripts/record-verdict.sh" \
  --dep <name> --ecosystem <rust|js> --verdict <REMOVE|KEEP|DECIDE> \
  --project <repo-name> --reason "<one line — the evidence, not the conclusion>"
```

The script appends to `references/verdicts.md` with today's date and keeps the table format
consistent. Record the deps whose verdict took real work to reach; skip the trivial ones. If a run
surfaced a *pattern* rather than a per-dep fact, add it to that file's Patterns section by hand —
patterns transfer between projects far better than individual verdicts do.

## Escalating to a full plan

When the findings are large enough to need sequencing, parallel work, or review — many removals, a
deprecated dep needing its own evaluation, a regression guard, plus a register — hand off to
`/big-plan` rather than doing it inline. That gives each piece its own issue, dependency-ordered
waves, and a confirm pass at the end.

Pass along the abandon rule, the used-vs-unused framing, and the baseline-oracle requirement, since a
plan that omits them will produce sub-tasks that re-derive the wrong conclusions. Audits that turn up
only a handful of dead declarations do not need this — just fix them and report.
