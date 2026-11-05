---
name: empty-vs-error
description: Use whenever code READS something (query, fetch, groupBy, aggregate, probe) and RENDERS or SCORES the result — a panel, a stat tile, a health verdict, a score, a report section. A failed read must never render as a confident zero. Also use when auditing a wave for this shape, or when fixing one instance of it.
triggers: read, query, fetch, groupby, aggregate, probe, render, score, panel, stat tile, health verdict, report section, confident zero, failed read
---

# Empty vs Error vs Unmeasured

**Three states, never two.** A read has three outcomes and they are not
interchangeable:

| State | Means | Must render as |
|---|---|---|
| `ERROR` | the read failed | "couldn't load — state unknown, not empty" |
| `UNMEASURED` | the read never ran, or the writer has never written | "not measured yet" + what would unlock it |
| measured zero | the read succeeded and the answer is genuinely 0 | a real zero, with its denominator |

Collapsing the first two into the third is the single highest-frequency
defect shape in this repo.

## The base rate

- **10 instances on ONE page** — the `/brain` nine-tab audit (PR #2090,
  2026-09-02). Dominant of the five shapes found; 41 defects total.
- **It survived the fix, twice.** #2090 split "read FAILED" from "empty"
  and stopped there, leaving an **empty** contradiction ledger scoring a
  hardcoded **7 of 100** — prod has never recorded a contradiction in any
  category, so that branch fired on every render (PR #2091).
- **The identical shape sat in a second file the same wave.**
  `resolutionRate = 1` on an empty table was fixed in
  `lib/brain/learning-velocity.ts` and missed in the contradiction path.
  Two agents, one session.
- **Three more in one day** (2026-07-30), all "a read with no writer":
  `apiRequestLog` filtered to `/api/ai/chat` (chat never passes through
  the request logger), `ai_generations` where `status='failed'` (writers
  emit `complete`/`error`), `error_logs` where `level='fatal'` (writers
  emit `error`/`warn`). Each rendered a fabricated all-clear.

Every one of these passed typecheck, lint, and a green suite.

## Copy these — they already do it right

Do not invent a state model. Three verified reference implementations:

1. **`apps/statenour/components/brain/judgment-quality-panel.tsx:34`** —
   the minimal form. `isLoading` skeleton, then:
   ```tsx
   if (spcQ.isError || calQ.isError) {
     return <section …>Judgment-quality readings couldn&apos;t load —
       state unknown, not empty.</section>;
   }
   ```
2. **`apps/statenour/components/brain/contradiction-resolution-panel.tsx:300`**
   — the full three-state form. `EmptyState` takes a `provenance` prop:
   ```tsx
   provenance={contraQuery.isError ? "ERROR" : "UNMEASURED"}
   ```
   The vocabulary is three literal strings — `"ERROR"`, `"UNMEASURED"`,
   and `provenance="ZERO"` (line 311) for a measured zero, which renders
   in its own branch (line 306) with an `unlock` string saying what would
   make the number move. Its line 64 carries the
   incident comment — the code used to end `?? (isError ? [] : null)`, so
   a failed query fell into the empty branch and rendered a green
   "Clean ledger".
3. **`apps/statenour/lib/observability/fleet-truth.ts`** — the server-side
   vocabulary: `fresh / stale / never_produced / unknown`, with
   "**a failed probe or fetch is UNKNOWN, never healthy**" (line 13) and
   `ok` defined as *every* capability fresh — "unknown counts as NOT ok"
   (line 190). Every `catch` pushes `state: "unknown"`, never a default.

## Detection — scope to the DIFF, never the repo

**Match the TYPE ANNOTATION, or you miss a third of them.** The house
form is often `.catch((): never[] => [])`, and a pattern that requires
`()` immediately before `=>` silently skips every one. Measured on
`6ade5771b` across `apps/statenour/{lib,app}`:

| Pattern | Files |
|---|---|
| dangerous fallbacks — `=> []` / `=> 0`, **any annotation** | **147** |
| the same, matched **untyped-only** (the naive regex) | 98 |
| `=> null` — usually honest, null is a legitimate "unknown" | 130 |

The 49-file gap between the first two rows is the cost of a detector that
does not allow an annotation. **This exact miss shipped in the first
version of this skill and was caught in review** — the counts it quoted
came from a stricter regex than the one it told you to run.

Those totals are also why a repo-wide grep is not a gate: at 147 files
this is a house idiom, not a defect list. Scope to your own change, or to
one surface you are auditing:

```bash
# your diff only
git diff origin/main | grep -nE '\?\? *0|\?\? *\[\]|\.catch\(\([^)]*\)( *: *[^=]+?)? *=> *(\[\]|0)|useState\(\{[^}]*: *0'

# one surface, when auditing a page
git grep -nE '\.catch\(\([^)]*\)( *: *[^=]+?)? *=> *(\[\]|0)' -- apps/statenour/components/brain

# a read with no writer: prove the discriminator has a producer
git grep -n "status: *'failed'"   # 0 hits today — writers emit complete/error
```

Positive-control any change to these patterns against all four forms
before trusting them — `() => []`, `(): never[] => []`, `() => 0`,
`(): number => 0` must all match, and `() => null` must not.

Three specific traps behind these:

- **A `.catch(() => [])` INSIDE a service** makes the caller's `isError`
  permanently `false`. The component cannot render honestly because the
  failure never reaches it. Fix at the service, not the panel.
- **A narrower tRPC output annotation than the function it wraps silently
  deletes fields** — no error anywhere.
- **A hardcoded floor in a scorer** (`+7`, `rate = 1`, `?? 100`) is this
  bug wearing a number. An empty population has no rate.

## Fixing one is not fixing the class

The four rules that cost five PRs to learn:

1. **Cross-check the SHAPE across every file in the wave**, not just the
   file it was reported in. Grep the fix's signature repo-wide before
   claiming the class closed.
2. **Audit the FIX as hostilely as the code it replaced.** Twice the new
   defect was in code written minutes earlier *while criticising that
   exact defect class*.
3. **A partial fix that ships a test cements itself.** #2091's own test
   read `expect(view.score).toBe(7)` under the comment "A measured empty
   ledger DOES still earn the 7". Second bug-encoding test of the wave —
   `calibration.test.ts` had already pinned `resolved === 0` as correct
   and would have blocked the real fix. **When a test resists a correct
   fix, read the test as a finding.**
4. **After deleting or renaming a field, grep for consumers AND for UI
   branches that can now never fire** — one fix created a dead alarm
   (`truncated` hardcoded `false` behind a live UI branch).

## Verify the fix actually fires

A silenced alarm and a fixed alarm produce the same green suite. The test
must prove the honest branch RENDERS: mutate the fix out and watch it go
red (`vi.clearAllMocks()` does **not** drain a `mockResolvedValueOnce`
queue — a red you did not diagnose is not a passing canary). Assert
behaviour, not source text; `not.toContain("catch")` false-fails on a
reformat.

## When NOT to use

Pure functions with no IO, and reads whose only consumer is another
internal computation that already propagates failure. This is about the
boundary where a read becomes a rendered or scored claim.

Related: `statenour-verify` (the corollary for report/diagnostic
sections, and the "prove the source receives rows" table) ·
`base-rate-check` (a zero also needs its denominator).
