---

name: expert-correct

description: "Part of the Expert Standard Dev Tools package. Use when an existing artifact — a spec, an architecture, or a plan — must be corrected against a review finding set. This is re-derivation of the affected sections from their sources, not authoring and not patching. Runs at a review gate, after a NEEDS_FIXES verdict, on an artifact that already exists and whose untouched sections are correct by the prior round's review. Do not use it to write a new artifact; that is expert-spec, expert-architecture, or expert-plan."

---

# Expert Correct — re-derive an artifact's affected sections against a finding set

You are correcting an artifact that already exists. You did not write it, and you are not
rewriting it. Correction is a distinct discipline from authoring, and this skill is the whole of
that discipline.

Neighbouring behaviours are **forbidden**, and each has been measured failing:

- **Patching is forbidden.** Editing the sentence a finding points at, at the fix site, without
  returning to that passage's sources, leaves the finding's *class* unswept everywhere else in the
  artifact. The APS Fusion architecture cycle spent rounds 1–11 failing this way, and three
  fix-site regressions still occurred at rounds 15, 16 and 19 — each one from verifying only the
  half of the record that supported the edit.
- **Re-authoring the artifact from the task is equally forbidden.** It discards every section no
  finding touched and regenerates a fresh defect surface, so each round's reviewer meets a new
  document rather than a narrowing one. The measured instance is eleven `Write` calls and zero
  `Edit` calls across six correction dispatches.

**The edit's size is whatever re-derivation produces.** A re-derived section may be one sentence or
forty. Size is not the discipline, and optimising for a small edit selects for patching.

---

## The discipline, per finding, in order

1. **Identify the section the finding lands in, and that section's sources.** The requirement, the
   named standard, the upstream artifact, the read of code or documentation the section was derived
   from. If you cannot name the section's sources, you cannot correct it — see the halt path.

2. **Re-derive the section from those sources.** Go back to what the section was built from and
   build it again correctly. **Do not edit the sentence the finding points at.** The finding names
   a symptom; the sources are what the section owes its content to.

3. **Sweep the finding's class across the whole artifact.** The finding is one instance. Every
   other passage of the same class is corrected in the same pass. This is the load-bearing half of
   the discipline: re-derivation with an incomplete sweep is not a milder failure than patching —
   the named instances close and the class resurfaces somewhere new the following round, which is
   the shape that fired the APS Fusion tripwire six times.

4. **Re-read what the re-derivation made stale.** Every passage that referenced the rewritten
   section, whether or not your edit touched it.

5. **Verify the whole record, not the half that supports the edit.** Where the finding asserts a
   relation, every term of that relation must be bounded somewhere in the artifact. Where a worked
   example and a normative reference disagree, the normative reference is the contract.

---

## When the class cannot be closed

A class that lives in a **hand-maintained derived surface** — a cross-reference table, an
enumeration, a count restated in several sections, with no generator — cannot be closed by sweeping
harder. Each correction edits the surface and re-arms it, so correcting ten instances one round at
a time is unbounded work. Closing such a class means converting the surface from maintained to
derived, which is an **authoring decision you are not authorised to make**.

Escalate it. Do not silently absorb it, and do not report the class closed when you have only
corrected its instances.

---

## The halt path

**A finding whose named standard you cannot verify is reported back, never guessed at.** Return
`status: 'halted'` with the reason in `halt.detail`. This is the escape hatch for a finding you
cannot act on; using it is correct behaviour, not failure. Guessing at a standard you could not
reach, or silently skipping the finding, burns the gate's remaining rounds on an artifact that is
not improving.

---

## Your structured return contract

Your final message is consumed as structured data. Report, in addition to `status` and
`artifact_path`:

**`sections_rederived`** — one entry per section you re-derived, each carrying:

- **`location`** — where the re-derived section is, in the grammar the reviewer's findings use:
  `path:start-end` (a line range) or `path#section` (a section identifier). Nothing else parses.
- **`source`** — what you re-derived it from: the requirement, standard, upstream artifact, or the
  read that supplied its content.
- **`finding_addressed`** — the finding this entry answers.
- **`class_sweep`** — the record of step 3, with these required fields:
  - **`searched`** — what the sweep looked for.
  - **`pattern`** — the executable search the sweep ran: a regex, in Grep syntax. This is the
    sweep itself, handed over — not a description of it.
  - **`scope`** — the file or glob `pattern` ran over (normally the artifact path).
  - **`found`** — **every** location the search returned, corrected or not.
  - **`sites_changed`** — the `found` locations you actually edited for this class (a subset of
    `found`).
  - **`open_sites`** (when applicable) — every `found` entry outside `sites_changed`, each with
    its `location` and a `designation`: either the escalation under "When the class cannot be
    closed" above, or an explicitly-open item. A found site neither changed nor designated is a
    class site left silently open, and fails the gate.

**Emitting all of these is not optional.** `location` and `class_sweep` are what the orchestrator
uses to detect a correction that regressed at its own fix site, and a class that was found and left
open. The sweep is not taken on trust: the orchestrator re-executes `pattern` over `scope` — through
an agent that did not perform the correction — **in the same round**, and executing it must
reproduce `found`. A sweep whose re-execution returns sites you did not report, or whose `found`
entries were neither changed nor designated, fails the gate that dispatched you, attributably,
instead of surfacing as the next round's "new" findings. Run the sweep after your edits and report
its current locations exactly.
