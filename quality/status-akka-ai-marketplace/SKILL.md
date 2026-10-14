---
name: status
description: "Show a read-only rollup of the definition of done — every exit condition with its state, properties, and open reason — without running any auditor."
---

## User Input

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

`/akka:status` prints the current definition-of-done manifest: every exit
condition grouped by Definition-of-Done type, with its state (`open`, `green`,
or `red`), its properties (provenance, waiver, applicability), and any `open`
reason. The two locked process-integrity gates, `PROC-AUDITOR-COVERAGE` and
`PROC-ADEQUACY-REVIEWED`, appear among the conditions like any other.

The manifest reflects the project's own state — waived, struck, and signed-off
conditions appear as such — so it agrees with `/akka:conform`.

**Status never runs an auditor.** It does not build, test, lint, or probe. That
is the whole difference from `/akka:conform`: machine-checkable conditions stay
`open` here until conform evaluates them. Once conform has run, the two agree.

Because it changes nothing and costs nothing, status is the command to reach
for during an autonomous build — it shows progress without interrupting the
machine.

## Outline

1. **Render the manifest.** Call `akka_ec_status` for the project directory.
   This resolves the exit-condition library against the org governance floor
   and the project's own strikes, waivers, and sign-offs, then renders the
   manifest. It is read-only and runs no auditors.

2. **Get the counts.** Call `akka_ec_rollup` for the same directory. It returns
   the status counts by tier and by Definition-of-Done type as JSON. Use this
   as the headline so the user sees the shape of the build before the detail.

3. **Report plainly.** Lead with the rollup: how many conditions are settled,
   how many are waiting on the user, how many are blocked outside the project.
   Then surface the conditions that are `open` or `red`, each with its
   user-facing reason — the reason field is the action.

   State plainly that the auditors were not run, and that the machine-checkable
   conditions are therefore still `open` rather than failing. Do not present an
   unevaluated condition as a problem. Offer `/akka:conform` as the way to
   resolve them.

   Do not restate internal condition ids, check keys, or the words "auditor" /
   "coverage gate" / "adequacy review" in the summary. Offer *"say 'show
   details' for the full checklist"* and show the raw manifest only if asked.

## Key rules

- Read-only, always. Never run a build, a test, or a probe from this command,
  and never call `akka_ec_conform` or `akka_ec_summary` — both run the
  auditors, which is precisely what status must not do.
- Never characterize an unevaluated condition as passing or failing. It is
  `open` because nothing has looked at it yet, and saying otherwise is the one
  way this command can mislead.
- Do not change the project. No sign-offs, no strikes, no waivers, no mode
  changes as a side effect of showing status.

## Done When

- [ ] `akka_ec_status` was called and the manifest was resolved without running
      any auditor.
- [ ] `akka_ec_rollup` was called and its counts led the report.
- [ ] Conditions that are `open` or `red` were surfaced with their user-facing
      reasons (no internal ids, no machinery words).
- [ ] The report stated that the auditors did not run, and did not present
      unevaluated machine-checkable conditions as failures.
- [ ] Nothing in the project was modified.
