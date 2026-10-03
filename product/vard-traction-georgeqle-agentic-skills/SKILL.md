---
name: vard-traction
description: Check post-launch traction for a shipped VARD app and recommend iterate, graduate, or archive
type: ops
version: v0.1
context_intake: artifact_only
---

# VARD Traction

Invoke as `/vard-traction`.

Post-launch traction check for shipped VARD experiments. Reads the ship log and current signals, compares them against the VARD graduation thresholds, and recommends exactly one of: iterate, graduate to Business AFPS, or archive. This is the semi-automatic graduation gate — the skill recommends, you confirm before anything happens.

## Process

1. **Resolve target:** Use `$ARGUMENTS` to name the shipped concept. If omitted, use the most recent `launched` entry in `research/vard-ship-log.md`.
2. **Confirm timing:** Traction is meaningful after 1-2 weeks live. If the ship date is more recent, note the signal is early and mark the recommendation provisional.
3. **Gather signals:** Collect the available distribution and engagement signals for the app:
   - Users / unique visitors
   - Shares and social engagement (is the viral mechanic working?)
   - Core-action completion (the one thing the app does)
   - Revenue or revenue-intent signals
   - Inbound interest (enterprise inquiries, feature requests, press)
   Use the analytics wired at ship time. Where a signal is unavailable, mark it `unknown` rather than guessing.
4. **Compare to graduation thresholds:** Evaluate against the VARD graduation triggers:
   - Enterprise inquiry or clear revenue potential → strong graduate signal (Business AFPS)
   - User base large enough to justify deep customer discovery → graduate signal
   - Sustained engagement or sharing growth → iterate-and-grow signal
   - Flat or no traction after 1-2 weeks → archive signal
5. **Recommend (semi-auto gate):** Produce exactly one recommendation with its rationale and the signals that drove it:
   - **Graduate** → install the Business AFPS entry pack with `npx skillpacks install business-research`, then enter at `/idea-scope-brief` for raw/new product framing or `/customer-discovery` when the shipped app already has a clear concept and traction evidence. Link the VARD scan, align, ship-log, and traction-log entries as evidence.
   - **Iterate** → keep it in VARD; run another build and distribution cycle.
   - **Archive** → record the outcome and move on to the next experiment.
   State explicitly that the user confirms before any graduation, archive, or further action happens.
6. **Log the check:** Append a traction entry under the concept in `research/vard-ship-log.md`:
   - Date of check, weeks since launch
   - Each signal and its value (or `unknown`)
   - Threshold comparison result
   - Recommendation and rationale
   - Status: `iterating`, `graduating`, or `archived`

## Output

End with:

```md
**Traction:** <concept name> — <one-line signal summary>
**Recommendation:** iterate | graduate to Business AFPS | archive
**Next work:** <the confirming action for the recommendation>
**Recommended next command:** npx skillpacks install business-research, then /idea-scope-brief or /customer-discovery (graduate) | /vard-scan (next experiment) | none (archived)
```

## Constraints

- Do not run paid API calls or external account actions to gather signals.
- Do not graduate, archive, or delete anything automatically — recommend and let the user confirm.
- Mark unavailable signals as `unknown`; do not fabricate metrics.
- If no ship-log entry exists for the target, report that and stop.
- Create `research/vard-ship-log.md` with a header only if it is missing and a shipped app clearly exists.

## Cross-Pack Routing

A graduation to Business AFPS requires the `business-research` pack. If it is not installed, include `npx skillpacks install business-research` as the prerequisite. Use `/idea-scope-brief` when the opportunity still needs raw or new product framing; use `/customer-discovery` when the shipped app has a clear concept and traction evidence ready for deliberate customer research.

## Default Shipping Contract

Follow the shared shipping contract convention.
