---
name: pitfall-verification
description: |
  After any PRD, spec, plan, or code change: verify artifact-specific pitfalls
  don't apply before declaring done. For ship-worthy changes, auto-chains Codex
  + a third model house + adversarial synthesis.
---

# Pitfall verification

Use this skill after finishing any PRD, spec, plan, or code artifact — before declaring the work done. It is NOT a generic review. It is a targeted check that *typical pitfalls for this type of artifact, in this domain, do not apply here*.

Invoke with: `/superpowers-gstack:pitfall-verification`

## This skill is a multi-model orchestrator

For anything beyond a trivial change, one model is not enough — there is always more to find, and a single training distribution has fixed blind spots. So this skill does **not** stop at Claude's own pitfall pass. For **substantive / ship-worthy** changes it runs, as ONE automatic flow:

1. **Self-pitfall** (Claude, lens 1) — the rounds below, max 2.
2. **Codex** (lens 2) — on a code diff, gstack's `/review` (which runs Codex adversarially); on a spec or plan, `/codex challenge`.
3. **Third model house** (lens 3) — `/superpowers-gstack:third-lens-review` on the patched artifact.
4. **Adversarial synthesis** — combine all findings, finding-is-real-until-refuted.

**Stages 2–4 run automatically. Do NOT stop after the self-pitfall rounds to ask the user whether to run Codex or the third lens — run them.** The whole point is that there is nothing extra to remember: invoking pitfall-verification on substantive work *is* the multi-model review. The only thing that skips stages 2–4 is the **trivial** tier (see "Tier gate" below) — a typo or doc fix gets the free self-pitfall pass and nothing else.

## Stage 0 — name the target, compute the tier floor

Two things must be settled before any lens runs, and neither may be decided by
feel:

**1. What is under review.** This skill used to inherit whatever happened to be in
context. In a long session that is a real drift risk — you review the last phase,
the model reviews the whole file, and nobody notices. Name the target explicitly,
in the same spelling `third-lens-review.py` uses, so Stage 0 and Stage 3 read one
artifact by construction rather than by hope.

**2. Which tier it is.** The tier decides whether the expensive lenses run at all.
Left to prose it was self-assessment by the model that had just written the code —
the one place where the incentive to pick the cheapest outcome is strongest. The
machine now computes a **floor**; you may escalate above it, never below.

Locate the script self-relatively (this skill usually runs in the USER's project,
where `scripts/` does not exist — derive it from this skill's base directory, shown
when the skill loads):

```bash
CLASSIFY="<this skill's base directory>/../../scripts/classify-change.py"

python3 "$CLASSIFY" --diff --diff-base main --explain   # a branch
python3 "$CLASSIFY" --files "src/**/*.swift" --explain  # named files
python3 "$CLASSIFY" --explain                           # auto: dirty tree, else merge-base
```

It prints the resolved target, the floor tier, and the signals that produced it.
**Copy its `verdict_header` line into your verdict** — that is what makes the
target and the tier auditable after the fact instead of a claim.

- **Escalate freely.** The floor sees paths, added lines and size. It cannot see a
  subtle protocol change or a data-loss path in ordinary-looking code. When you
  judge the change higher than the floor, say so and run the higher tier.
- **Never go below it.** Before running a tier lower than the header says, confirm
  with `python3 "$CLASSIFY" --assert-tier <your tier>`; it exits 1 on a downgrade
  and names the signals you would be skipping.
- **Missing or failing script → treat the change as ship-worthy at minimum**, and
  say in the verdict that the floor was not computed. The gate fails toward more
  verification, never less.
- The script contains its own signal patterns as literals, so a change touching
  *it* matches its own security/migration signals. That is a floor doing its job
  loudly, not a bug; `--explain` shows exactly which literal fired.

## When to invoke

Automatically after completing:

- A PRD, spec, or design document
- An implementation plan
- A code change (feature, refactor, bug fix)
- Output from `writing-specs`, `writing-plans`, `executing-plans`, `verification-before-completion`, or any GStack planning/review skill

Run **twice max**. Two rounds catch almost everything; a third round has sharply diminishing returns.

## Sequence

1. **Self-check first** (~30 seconds): placeholders, scope drift, internal consistency, ambiguity. This is the standard sanity pass. Fix anything obvious.
2. **Pitfall verification** (this skill): targeted check for the pitfalls below, adapted to the artifact type and domain.

Do not skip step 1 — self-check and pitfall verification are different lenses.

## Pitfall lists per artifact type

These are **starting points, not exhaustive checklists**. Always ask: *what typically goes wrong with this kind of artifact, in this specific domain?* Infer additional pitfalls from the actual code/spec under review.

### PRD

- Unclear user story or missing success metric
- Hidden stakeholder assumptions (who signs off? who blocks?)
- Unspecified non-functional requirements (perf, privacy, accessibility, i18n)
- Conflicting requirements across sections
- Missing failure modes (what if X is unavailable? what if load spikes?)
- Over-specification of solution vs under-specification of problem

### Spec / plan

- Ambiguous contracts — input/output types, error shapes, null semantics
- Uspecified edge cases (empty, max-size, concurrent, partial failure)
- Missing error states / recovery paths
- Hidden assumptions about call order, transactions, idempotency
- Signature drift: spec references functions/fields that do not exist in the code
- Assumed external API behavior that has not been verified

### Code

- **Security**: prompt injection, input sanitation, credential leakage, SSRF, path traversal, auth bypass
- **Idempotency**: side effects on retry, hidden state, ordering dependencies
- **Integration contracts**: field names, types, and signatures that actually match the code they call into (cross-check — do not assume)
- **Edge cases**: empty input, oversized input, Unicode, currencies, time zones, DST, negative numbers, leap years
- **LLM output**: markdown-wrapped JSON, unexpected JSON structure, hallucinated fields, schema drift
- **Concurrency**: race conditions, deadlocks, shared mutable state
- **Resource lifecycle**: leaked handles, unclosed connections, memory growth under load

## How to run the check

For each pitfall on the relevant list:

1. **State the pitfall** — one sentence.
2. **Locate the risk surface** — which function, field, section, or claim could be affected?
3. **Verify**, do not assume. Read the actual code/spec. Cross-check field names against the implementation. Test the edge case mentally with real values.
4. **Report**: *Not applicable* (with reason) / *Applicable and handled* (point to where) / *Applicable and not handled* (propose fix).

If a pitfall is not applicable to this domain, say so explicitly — do not silently skip it. Stating "N/A because this code never touches dates" is itself a verification signal.

## Domain inference — the step that decides the round's quality

The lists above are *generic-LLM-common*: any competent model produces roughly that
list unprompted, which is exactly why they find roughly what any model would have
found anyway. **The findings that justify this skill come from the domain-specific
pitfalls you infer before the round starts.** Treat this section as mandatory work,
not a warm-up.

### Step 1 — name the domain from evidence, not vibes

Cheap, concrete sources, in order of signal:

1. **The target's own paths.** `auth/`, `migrations/`, `audio/`, `Views/` each name
   a failure family before you read a line.
2. **`git log --oneline -30 -- <the target's paths>`.** What has broken *here*
   before is the highest-yield prior available, and it is two seconds away.
3. **`fix:` entries in CHANGELOG / incident notes touching these files.** A team's
   past bugs repeat far more than the generic list does.
4. **The names of the tests that already exist.** A test suite is a list of bugs
   somebody already paid for.
5. **The error handling the code already has.** What a function defends against
   tells you what bit its author — and what a *new* code path forgot to defend.

Name the domain in one line, with the evidence. "LLM pipeline over user-supplied
documents; last three `fix:` commits here were all JSON-parse failures" is a domain
inference. "This is a web app" is not.

### Step 2 — take the family's pitfalls

| Domain | What actually bites here |
|---|---|
| **Auth / session** | token lifetime vs session lifetime, revocation that never propagates, refresh races, privileges cached across a role change, non-timing-safe compare, session fixation |
| **Money / payments** | float arithmetic on currency, rounding direction and order vs tax, idempotency keys absent on retry, partial refunds, mixed currencies, replayed webhooks |
| **Data pipeline / ETL** | partial batch failure leaving half-written state, at-least-once delivery producing duplicates, schema drift at the source, timezone-naive timestamps, backfill and incremental paths disagreeing |
| **LLM pipeline** | markdown-fenced JSON, hallucinated or missing fields, prompt injection arriving through *retrieved* content, truncation mid-structure at the token budget, tests that assume determinism, cost per call at production volume |
| **Real-time / audio / DSP** | allocation or locking on the render thread, priority inversion, buffer overrun silently dropped, sample-accurate requirements confused with perceptual tolerance, late events applied to a stale state |
| **UI state** | state drift from the source of truth, cache stale after an external change, optimistic update with no rollback, double-submit, task outliving the view that owns it |
| **Shell / infra scripting** | an unset variable expanding to empty *inside a destructive command*, unquoted paths and refs, exit status swallowed by a pipe, `set -e` not covering subshells or command substitution, a re-run that is not idempotent |
| **Native mobile / desktop** | permission denied mid-flow, background/foreground transitions, work on the main thread, verifying against an installed copy instead of the built bundle, on-disk state that never migrates across versions |

Domains combine. A SwiftUI app that calls a model is *both* LLM pipeline and UI
state, and the interesting pitfalls usually live at the seam.

### Step 3 — write the inferred pitfalls down before running

List **3–5 domain-inferred pitfalls** ahead of the round, each marked `[domain]`,
alongside the `[generic]` ones you take from the lists above. A round that produces
zero `[domain]` pitfalls has not been run properly — say so in the verdict rather
than passing it off as clean.

### The bar for a finding (worked example)

This is a real one, from this plugin's own 2.44.0 review — domain: shell/infra
scripting, inferred from a plan whose phases were all bash:

```
[domain] Unset variable expanding to empty inside a destructive command.
Risk surface: plan Phase 5, the fallback branch of the app-quit step.
Verified: Phase 2 defines EXECUTABLE_NAME; Phase 5 reads $EXEC. The name never
matches, so the fallback becomes `pkill -f "/Contents/MacOS/"` — an empty pattern
against every process path. Measured against a live process list: it matches
loginwindow, authd and CodeSigningHelper, not merely user apps. Followed literally,
this phase logs the user out.
NOT HANDLED → make every interpolated value fail closed before it can be empty:
`"${EXECUTABLE_NAME:?}"`, and reconcile the two phases on one variable name.
```

That is the bar: the pitfall named, the exact risk surface, a verification that was
actually *performed* (not assumed), the concrete consequence, and a fix that closes
the class rather than the instance. A finding that could have been written without
opening the file is not a finding.

## Output format

End the round with a compact verdict:

```
Pitfall verification (round N/2):
Target: <spec> · Tier floor: <tier> (signals: ...) · computed by scripts/classify-change.py
Tier used: <floor, or higher + why escalated>
Domain: <one line, with the evidence it came from>
- [domain] <pitfall> → N/A | handled at file:line | NOT HANDLED — proposed fix
- [generic] <pitfall> → ...

Verdict: CLEAN | ISSUES FOUND (see above)
```

The first two lines are the classifier's `verdict_header` and your tier decision.
Both are copied, not composed — a target and a tier nobody can check afterwards are
the two things this skill used to leave to trust.

If round 1 surfaces issues, fix them, then run round 2 on the patched artifact. If round 2 is clean, declare done. If round 2 still finds issues, surface them to the user — do not silently run round 3.

**Re-run Stage 0 after the fixes.** The floor was computed from the artifact as it
stood BEFORE the self-pitfall round, and fixes add code. A fix that introduces a
`subprocess.` call, an `ALTER TABLE`, or a concurrency primitive raises the real tier
of the change — but the floor is a snapshot, so the lens that new code most needs
never runs on it. Re-run `classify-change.py` on the patched artifact and take the
higher of the two floors. Escalation is always allowed; the snapshot is not a ceiling.

## Tier gate — which lenses run automatically

The tier comes from Stage 0's computed floor, plus any escalation you can justify.
Run the rest of the chain **automatically** for that tier. Do not ask the user which
lenses to run — the tier decides, and the tier is now computed.

| Tier | What the floor keys on | Lenses (all automatic) |
|------|-----------|------------------------|
| **Trivial** | docs, typo, comment-only, test-only-coverage, WIP checkpoint | Self-pitfall only — stop here |
| **Ship-worthy** | bumps a version file, produces a CHANGELOG entry, `feat`/`fix`/`refactor` affecting runtime, or changes public contracts | Self-pitfall → **Codex** (via gstack `/review`) → synthesis |
| **+ High-stakes** | a ship-worthy change that *also* touches **architecture / real-time / security / public contracts / migration logic** | …→ **third model house** → synthesis |

In practice most substantive work is at least ship-worthy, so Codex runs by default through `/review`. The third house adds itself on the high-stakes subset. Both fire **without a confirmation prompt**; cost is reported after each call, not gated before it.

The floor's own reading of that table: instruction surface (`skills/`, `CLAUDE.md`,
`.claude/`) is runtime behaviour and never counts as docs; a version-file or
CHANGELOG change alone is ship-worthy; `auth|session|token|crypto` paths, migrations
and `.sql`, `openapi`/`.proto`/`.graphql`/`Package.swift`, and `audio|realtime|
websocket|scheduler|queue` paths are high-stakes, as are ≥8 changed files or ≥400
added lines (the mechanical proxy for "architecture").

## Stages 2–4 — external lenses + synthesis (automatic per tier)

Run on the **patched** artifact, in order — each later lens reads a cleaner surface.

### Stage 2 — Codex (ship-worthy and above)

**gstack owns the Codex pass.** For a code diff, invoke gstack's `/review`: its adversarial step runs Codex on the diff with the model gstack currently defaults to, and it is the one place Codex should run on a given patched state. For a spec or plan (no diff), invoke `/codex challenge` on the artifact. Codex catches cross-file drift, concurrency contracts, and concrete run bugs that self-review systematically misses. Fix what it finds. Run it automatically — do not ask first.

**Verify that lens 2 really was Codex.** gstack's `/review` echoes a `CODEX_MODE:` line and, when it is anything but `ready` (Codex disabled in config, not installed, not authenticated, broken, or running under Codex), silently substitutes a Claude subagent — the same model family. Read that line (or the persisted `source:` field of its adversarial-review entry). If Codex did not run, the ship-worthy tier is **not** satisfied: record `lens 2 absent (CODEX_MODE=<value>)` in the Stage 4 verdict, escalate the third house as the outside read even below high-stakes, and never present the substitute's findings as Codex's.

**One Codex pass per patched state.** If `/review` has already run on this exact patched artifact earlier in the flow (an orchestrator such as `/superpowers-gstack:autoimplement` runs it at every phase boundary), do **not** run it again — fold its Codex findings into the Stage 4 synthesis. Never call `/codex review` directly on a diff; that is a second pass on the same state.

### Stage 3 — third model house (high-stakes only)

Invoke `/superpowers-gstack:third-lens-review` on the patched artifact. A different model house (different training distribution → different blind spots) finds architecture-level mistakes ("you never wired it together"), degraded-state bugs, and challenged assumptions the two Western houses both took for granted. It picks the model by artifact type (`--role architecture`/`correctness`/`countersynthesis`; the third house runs on non-Western infra, so keep sensitive artifacts — auth/keys/health/finance — to the self + Codex lenses) and runs its own adversarial synthesis of the third-house output. Run it automatically for the high-stakes tier — do not ask first.

### Stage 4 — combined adversarial synthesis (mandatory whenever stage 2 or 3 ran)

Do not dump raw findings. Fold Codex + third-house results into one verdict, **adversarially**: an external finding is REAL until you explicitly refute it with a reason (this counters LLM-judge agreement bias — failure-detection drops to ~50% when a judge is conciliatory, worse when it is partly judging its own earlier work). Log each dropped finding with *why*. Treat cross-model disagreement as the signal, not noise — every disagreement ends in an explicit, reasoned decision. Cross-model agreement = high-confidence green, no action.

```
Multi-lens verdict (tier: <trivial|ship-worthy|high-stakes>):
- Target: <spec> · Tier floor: <tier> (signals: ...) · Tier used: <tier> [escalated because …]
- Lenses run: self-pitfall [+ Codex] [+ <third-house model id>]
- CONFIRMED (fix now): [P1/P2] <finding> — <file:line> → <fix> (survived refutation because …)
- DISAGREEMENT → DECISION: <finding> → <explicit reasoned call>
- DROPPED (with reason): <finding> → <over-strict | handled at file:line | wrong>
- Cost: $<sum from lens footers>
- Verdict: CLEAN | FIX-THEN-RECHECK | SURFACE-TO-USER
```

## Why two rounds

One round catches the obvious pitfalls. Round 2, run on the patched artifact, catches pitfalls that the fixes from round 1 introduced or exposed. Beyond that, returns drop fast and reviewer fatigue introduces noise.

## What this skill is NOT

- Not a security audit (narrower, adversarial, deeper)
- Not a code review of style or readability
- Not a test suite (does not execute code)
- Not a replacement for `verification-before-completion` (which checks *claims vs reality* for already-finished work — pitfall verification is upstream of that)

Use it as the *last check before handing off* — after implementation, before the user sees "done".
