---
name: aid-prototype
description: >
  Build a throwaway, low-fidelity model to test whether a direction actually works, before
  anyone commits to building it properly. Use this skill when a decision hinges on something
  you can only learn by trying it. The model is isolated and disposable -- it lives in the
  work folder or an opt-in worktree and never touches production -- and it is deliberately
  rough, so it gets a light verification rather than a polish grade. It resolves nothing: it
  reports whether the direction holds and what was learned, and you decide. For a kept
  design meant to inform the build rather than a throwaway, use `/aid-design` instead; the
  real build is a separate `/aid-create` step.
allowed-tools: Read Glob Grep Bash Shell Terminal Write Edit Agent
argument-hint: "<direction> -- the direction/hypothesis to validate (optionally: fidelity paper|low-fi|runnable-spike)"
---

# Prototype (validate a direction, throwaway)

`/aid-prototype` builds a **throwaway** model **now** to de-risk a direction, captures the
validation signal, presents it, and hands the real build off. It **resolves nothing** and
its output is **not** production. For a design you intend to **keep and build**, use
`/aid-design`. Deeper per-slot guidance: `.aid/runtime/templates/shortcut-scaffolding/prototype.md`.

- **Not a numbered pipeline phase**; does not route to `/aid-execute`.

State machine: **INTAKE -> BUILD -> VERIFY (light) -> PRESENT [user decides] -> HANDOFF? ->
DONE**. Print the `[State: NAME] -- {purpose}` entry line on each state.

---

## State: INTAKE

1. **Require a direction.** Empty argument -> ask one bootstrapping question ("What
   direction do you want to validate, and what would tell you it works?") and wait.
2. **Capture (thin):** direction/hypothesis; fidelity (`paper` | `low-fi` | `runnable
   spike`, default `low-fi`); the success signal that would validate it; the scope
   boundary (what it does NOT attempt -- keeps it throwaway).
3. **Pick the path:** **Fast** -- a clear direction + success signal -> build now.
   **Guided** -- vague ("prototype something for onboarding") -> scope direction / success
   signal / fidelity first.
4. **Classify complexity (model + effort):** simple -> `aid-architect` at **sonnet /
   medium**; complex (a runnable spike, a rich flow) -> **opus / high**.
5. **Consult the Work Initiation Gate, then allocate the work folder + STATE.** First run
   the gate (`.aid/runtime/templates/work-initiation-gate.md`):
   `bash .aid/runtime/scripts/works/enumerate-works.sh` (main tree + every git worktree).
   Empty -> allocate, no prompt. Works exist -> ask new-vs-continuation; on **continuation**
   route to the chosen work's resume door and STOP (allocate nothing); on **new work**:
   create and enter the worktree per the gate's `§ 3a` step 2
   (`worktree-lifecycle.sh create <work-id> <name>`, STOP on a non-zero exit or empty path,
   else enter the resolved path), **then** allocate (`pipeline.path: lite`, `initiator:
   aid-prototype`, `lifecycle: Running`, `active_skill: aid-prototype`; `phase` not
   driven). For a **runnable spike**, associate an opt-in git worktree so the throwaway
   code is isolated.

**Advance:** BUILD.

---

## State: BUILD

Dispatch **`aid-architect`** (clean context, tiered) to build the low-fidelity model of
the direction and capture the validation signal. A "runnable spike" is **throwaway code
written by this same `aid-architect` dispatch** -- deliberately NOT `aid-developer` (whose
job is production code), keeping the throwaway/non-production boundary crisp. All artifacts
stay in the work folder / opt-in worktree and **never touch production modules**. It writes
a validation assessment (see [Deliverable](#deliverable)) into the work folder.

**Advance:** VERIFY.

---

## State: VERIFY  (LIGHT -- do not polish-grade a rough model)

A prototype is *deliberately* low-fidelity, so this is a single light clean-context check
(not the full adversarial loop the other collapses run): dispatch **`aid-reviewer`** once to
confirm (a) the **"success signal observed" claim is honest and grounded** in what was
actually built, and (b) the **throwaway scope was respected** -- no production code snuck in,
nothing was committed to real modules. If the check fails, return to BUILD once to correct;
do not loop on polish.

**Advance:** PRESENT.

---

## State: PRESENT  (hard stop -- the user decides)

Set `lifecycle: Paused-Awaiting-Input`. Present the throwaway model + the validation
assessment: **Direction · What was built (fidelity) · Success signal — observed or not ·
What we learned · viable? (a conclusion, not a resolution).** Assert no resolution.

**Advance:** HANDOFF (optional) then DONE.

---

## State: HANDOFF  (optional; printed suggestions only)

Printed suggestions the user may act on: build the validated thing for real
(`/aid-create*`, or `/aid-design` first if a kept design is wanted), or test it with users
(`/aid-experiment` / `/aid-test`). Never auto-invoked; never a resolution.

**Advance:** DONE.

---

## State: DONE

Set `lifecycle: Completed`, `updated` now, append a `## Lifecycle History` row. Keep the
throwaway artifacts + assessment in the work folder as the audit record; nothing is promoted
to production.

---

## Deliverable

A validation assessment in the work folder: *Direction · What was built (fidelity) ·
Success signal (observed / not) · What we learned · Viable? (conclusion, not resolution)*,
alongside the throwaway model/spike artifacts.

---

## Constraints

- **Throwaway + isolated** -- artifacts never touch production; a runnable spike is written
  by `aid-architect` (not `aid-developer`), in the work folder / opt-in worktree.
- **Resolves nothing** -- presents a viability conclusion; the user decides.
- **LIGHT verify** -- honesty + throwaway-scope check on the assessment, not a polish-grade.
- **Verification is always a sub-agent dispatch** (`aid-reviewer`), never inline.
- **Kept design is `/aid-design`, not this.**
- **Tracking:** write STATE `lifecycle` at every transition.
