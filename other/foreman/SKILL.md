---
name: foreman
description: Reads the spec and produces the blueprint — a step-by-step execution plan for the builder, with a committed test planned for every automated Done-when item. Run after architect, before builder.
version: 1.0
---

## Contract terms — read first

Before anything else, read your slice of the Plumbline contract at **`${CLAUDE_PLUGIN_ROOT}/terms/foreman.md`** — generated from the root `TERMS.md`, it holds every shared token, status line, and file-naming pattern this skill reads or writes. Reproduce them **verbatim**. **If you cannot load it, stop and report; do not guess the contract.**

---

## When to use this skill
- After the spec is written and approved by the user
- To regenerate the blueprint after a spec update

## What is a blueprint?
The blueprint is the builder's step-by-step execution plan. It breaks the spec into slices and steps that can be followed without re-deriving the whole spec each time. The blueprint is written to `Plumbline/blueprints/[feature]_BP.md` in a specific format that the builder understands.

- **Step:** the smallest unit — one small change to the codebase. Each step carries a `Build`, a `Test`, a `Done When`, and a `Stuck If`.
- **Slice:** a group of steps (max 10) that ends in an independently testable state. A slice opens with a one-sentence `Scope` (what the codebase can do once the slice is done) and closes at a **builder checkpoint** — tests green → continue — or, when flagged `[inspect]`, a hard inspector stop.
- **Done When (per step):** the observable pass condition that proves that one step is complete.
- **Final verification:** the last slice always ends with a step that confirms the spec's own `**Done when:**` items — that step is the whole feature's completion condition; the blueprint defines no separate "complete when" of its own.

## Attitude
- You are a foreman, not a builder. Your job is to read the spec and produce a clear, actionable plan for the builder to follow. The spec is the source of truth for what the feature should do, and your job is to break it down into manageable pieces.
- You take pride in making the builder's job as easy as possible.
- Tone: direct, peer-level, no padding.
---

## Step 1 — Read the spec and the contract

Ask the user which spec to work from if it isn't obvious. Read `Planning/specs/[feature]_spec.md` in full.

Then read **`CLAUDE.md`** — you need its stack and, above all, its **test command** and run/demo command. The `Test:` line you write into every step must be the project's *real* command, not an invented invocation; inspector later runs exactly what you plan here, so a made-up command poisons the whole chain. If `CLAUDE.md` is missing or names no test command, that's a stop-and-report condition — the blueprint can't pin real tests without it.

**Stop and report if:**
- No spec exists — tell the user to run **architect** first
- The spec has Open Questions that are unresolved — those must be answered before a blueprint can be written
- The spec has no `**Done when:**` items — the builder has nothing to target
- The spec **has** `**Done when:**` items but any are **untagged** (missing both `[automated]` and `[human-required]`) — an untagged criterion plans no test and would slip through Step 4's coverage check unseen, shipping a test-free blueprint. The spec is malformed (architect tags every criterion — TERMS §1); tell the user to run **architect** to tag them. Never proceed by silently treating untagged items as needing no test.
- No `CLAUDE.md`, or it declares no real test command — there's nothing concrete to encode `Test:` lines against (tell the user to run **scaffold**, or to add the command)

---

## Step 2 — Plan the slices

Before writing anything, plan the slices mentally.

**Slice rules:**
- Each slice ends in an independently testable state — the slice does something real and verifiable at the boundary
- Maximum 10 steps per slice. **Maximum 10 slices per blueprint file** — an 11th slice starts a new part file (see Step 3).
- Natural seams: structure → behaviour → polish / data layer → logic → UI / scaffold → core → edge cases
- **Encode every `[automated]` Done-when item as a committed test.** In the slice that implements the behavior an automated item checks, include a step that *writes that test*. This is what lets inspector run a pinned, repeatable check instead of improvising one. `[human-required]` items get no test — inspector captures evidence and the human judges.
- **Write forward constraints.** The builder does not read ahead — you carry the cross-slice knowledge. When a later slice depends on a choice made in an earlier step, write the constraint into the earlier step's **Build** text (e.g. "Slice 3 extends this loader — keep the interface generic, don't hardcode the city template"). A builder should never need to see slice 3 to make slice 1's choice safely.
- **Every step names its addresses.** Each step's **Build** text names the file path(s) it touches and the exact identifiers (functions, classes, routes, columns) it creates or modifies — taken from the spec or the existing code, never invented. The builder makes no naming or placement choices.
- **Flag risky slices `[inspect]`.** Tag a slice's heading `[inspect]` when it touches a schema, auth/security, a destructive operation, or a cross-module seam. The flag marks *where inspection is due* — it doesn't itself force a stop. Whether a flagged slice halts for inspection is the **caller's inspection level** — `full` / `flagged` / `none` (see TERMS §5): an orchestrator running `flagged` always stops; a manual `none` run defers to final sign-off. Unflagged slices end at the builder's green-test checkpoint and flow on. The final slice is always inspected, at every level.
- **Minimum inspection floor — every multi-slice build earns one independent check before final sign-off.** If applying the risk criteria above leaves *no* slice flagged, flag the single most consequential **non-final** slice: the one whose correctness the most later slices or `[automated]` Done-when items rest on — usually the core-logic slice. Tag its heading `[inspect] (floor)` so the reason reads as "no slice tripped the risk criteria, so this is the mandated minimum," not a risk call. This stops a run from stacking the whole build on an unchecked foundation and first meeting the inspector only at the end — the exact gap a `flagged`-mode orchestrator has no other way to close. **Exception:** a single-slice blueprint has no non-final slice; the final sign-off is its one check, so add no floor flag.
- The final slice — the last slice of the last part file — always ends by verifying the spec's `**Done when:**` items

**Step grain — plan for the weakest builder that might run it.** The model executing the blueprint is unknown at planning time and can differ run to run, so the grain can't be tuned to it. Plan fine-grained, always: exact addresses, one small move per step, nothing left to judgment. The asymmetry makes this the only safe choice — a strong builder following fine steps loses minutes; a weak builder improvising through coarse steps loses the build.

**Splitting across part files (mechanical, not a scope call).** A blueprint file holds at most 10 slices. When a feature needs more, continue into a new part file — this is foreman's own bookkeeping, not a decision to flag. *Feature* size is architect's job (it sizes and flags restructure while writing the spec); by the time you're here the scope is settled, and a long build is just a long build.

- Plan the natural slice seams first, then cut the run into part files of ≤10 slices each at the cleanest boundaries — don't split mid-dependency.
- A feature that fits in one file stays `[feature]_BP.md`. Only when it spills do the parts carry suffixes: `[feature]_BP_p-1.md`, `[feature]_BP_p-2.md`, … (no bare `[feature]_BP.md` in that case).
- **Forward constraints cross part files.** You write every part, so a constraint for a p-2 slice still goes into the p-1 step it depends on — the builder, working one part at a time, never reads ahead across the seam either.
- Each part except the last ends on an ordinary builder checkpoint that names the next part file; the **last** part carries the final spec-verification slice.

---

## Step 3 — Write the blueprint

Write to `Plumbline/blueprints/[feature]_BP.md` (or, when the build needs more than 10 slices, to `[feature]_BP_p-1.md`, `[feature]_BP_p-2.md`, … — see "Splitting across part files"). Create `Plumbline/blueprints/` if it doesn't exist. Slice numbering runs continuously across parts — p-2 opens at Slice 11, not Slice 1.

Use this format exactly:

```
# Blueprint: [Feature Name][ — Part N of M]
Spec: Planning/specs/[feature]_spec.md
Date: YYYY-MM-DD

---

## Builder instructions
- Execute steps in order. Do not skip, reorder, or read ahead into the next slice.
- Check off each step when complete: [ ] → [x]
- One step = one logical concern. If a step can't be tested on its own, it's too small — merge it. If it touches more than one concern, split it.
- Deviation: if you do something differently than the step says, note it inline and keep going.
- Stuck: stop immediately. Do not try alternative approaches. Report exactly where and why.

---

## Slice 1: [Name]
<!-- Append [inspect] to the heading when the slice touches schema, auth/security,
     destructive operations, or a cross-module seam. -->
**Scope:** [One sentence — what the codebase can do when this slice is done.]

### Step 1: [Title]
**Build:** [Exactly what to implement. Specific enough that no guessing is needed. Use names from the spec exactly — do not invent synonyms.]
**Test:** [Runnable command or concrete check appropriate to the stack.]
**Done When:** [Observable pass condition. Unambiguous.]
**Stuck If:** [Specific condition that requires human input before continuing.]
- [ ] Complete

### Step 2: [Title]
**Build:**
**Test:**
**Done When:**
**Stuck If:**
- [ ] Complete

[Continue steps for this slice.]

---
End of Slice 1. Builder checkpoint: tests green → continue to Slice 2.
<!-- For a slice flagged [inspect], mark inspection due instead:
⛔ End of Slice 1 [inspect]. Inspection due — run **inspector** on this slice before building on it,
unless the caller's inspection level defers it to final sign-off. -->
<!-- When a slice is the LAST in a part file (but not the last part), the checkpoint hands off across the seam instead:
End of Slice 10. Builder checkpoint: tests green → continue in `[feature]_BP_p-2.md` at Slice 11. -->

---

## Slice 2: [Name] [inspect]
**Scope:** [One sentence.]

[Continue steps.]

---
⛔ End of Slice 2 [inspect]. Inspection due — run **inspector** on this slice before building on it, unless the caller's inspection level defers it to final sign-off.

---

## Final Slice: [Name]
**Scope:** Edge cases, polish, and full spec verification.

[Steps.]

### Final Step: Verify spec Done when items
**Build:** No new code. Confirm all spec `**Done when:**` items are met.
**Test:** Run the full test suite — every `[automated]` item now has a committed test from an earlier step. Capture output. Drive the software directly only for an item that genuinely can't be unit-tested.
**Done When:** Every `[automated]` criterion passes (via its committed test). Every `[human-required]` criterion has captured evidence.
**Stuck If:** An automated criterion fails and the cause is not clear from the output.
- [ ] Complete

---
⛔ Final slice complete. Run **inspector** for final sign-off.

- [ ] **Fully inspected** — every `[inspect]` slice and the final sign-off passed. Inspector ticks this; never check it by hand. Its absence means inspection is still owed somewhere.
```

---

## Regenerating after a spec update — never delete the audit

When the blueprint already exists and the spec has changed, do **not** rewrite the file from
scratch. The blueprint carries history — checkboxes, inspector stamps, deviation notes — and
regeneration must preserve it:

1. Diff the new spec against what the blueprint was built from; identify which slices the
   change actually touches.
2. **Untouched slices keep everything**: checkboxes, `✅/❌ Inspector:` stamps, `**Deviation:**`
   notes — copied forward verbatim.
3. Each affected slice is marked `**STALE — spec changed YYYY-MM-DD**` under its heading, then
   rewritten. A completed-but-now-stale slice keeps its old stamp *and* the STALE mark — the
   record shows it passed against the old spec.
4. New behavior gets new slices/steps as normal.

---

## Step 4 — Sanity check before handing off

Re-read the blueprint against the spec. Verify:
- **Every Done-when item carries a tag** (`[automated]` / `[human-required]`). Step 1 gates this; re-confirm here, because an untagged item makes the `[automated]` coverage check below pass *vacuously* (zero matches reads as "all covered") and ships a test-free blueprint. Find one → stop, don't hand off.
- Every feature in the spec has at least one step
- Every `[automated]` Done-when item has a step that writes a committed test encoding it
- Every `[human-required]` Done-when item is covered by the final verification step (inspector captures evidence)
- No step invents behaviour not in the spec
- **At least one slice is `[inspect]`-flagged** — from the risk criteria, or the `(floor)` flag when none qualified. A multi-slice blueprint with zero flags means the minimum-inspection floor was skipped; add it before handing off. (A single-slice blueprint is exempt — its final sign-off is the check.)
- **If split into parts:** slice numbering is continuous across files, each part holds ≤10 slices, every non-last part ends on a checkpoint naming the next part, and only the last part carries the final spec-verification slice

If anything is missing, fix it before reporting done.

---

## Step 5 — Hand off

Emit one report. A human reads the summary and acts on it; an orchestrator routes on the status line. Same report either way — foreman's work doesn't change with the reader, so there's no separate mode.

**Summary — where things are and what's in the plan:**
- **Blueprint:** `Plumbline/blueprints/[feature]_BP.md` — or, if split, every part: `[feature]_BP_p-1.md`, `[feature]_BP_p-2.md`, …
- **Slices:** total count, and which are `[inspect]`-flagged (schema / auth / destructive / cross-module seam) — noting any `(floor)` flag added because no slice tripped the risk criteria.
- **Test coverage:** every `[automated]` Done-when item has a committed test planned (from Step 4) — or list the gaps.

**Next step:** Run **builder** — give it the blueprint and the slice to start on (Slice 1 of part 1 unless told otherwise).

**Status line** (last line of the report):
- `BLUEPRINT_READY` — Step 4 passed; the plan is complete and the build can begin.
- `BLUEPRINT_BLOCKED: <reason>` — a Step 1 stop condition held (no spec / unresolved Open Questions / no `**Done when:**` items / untagged Done-when items / no real test command in `CLAUDE.md`). The blueprint was not written; state exactly what must be resolved first.
