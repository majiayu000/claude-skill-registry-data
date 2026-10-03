---
name: ord-traction
description: Check post-launch adoption for a published ORD package and recommend iterate, graduate, or archive
type: ops
version: v0.1
context_intake: artifact_only
---

# ORD Traction

Invoke as `$ord-traction`.

Post-launch adoption check for published ORD packages. Reads the ship log and current signals, compares them against the ORD graduation thresholds, and recommends exactly one of: iterate, graduate to Devtool AFPS, graduate to Business AFPS, or archive. This is the semi-automatic graduation gate — the skill recommends, you confirm before anything happens.

## Process

1. **Resolve target:** Use `$ARGUMENTS` to name the published package. If omitted, use the most recent `published` entry in `research/ord-ship-log.md`.
2. **Confirm timing:** Adoption is meaningful after 1-2 weeks live. If the publish date is more recent, note the signal is early and mark the recommendation provisional.
3. **Gather signals:** Collect the available adoption signals for the package:
   - npm weekly downloads
   - GitHub stars
   - Issues filed by non-authors (substantive)
   - Integration or feature requests
   - Mentions (dev Twitter, Reddit, HN, Discord)
   Use public package and repo data. Where a signal is unavailable, mark it `unknown` rather than guessing.
4. **Compare to graduation thresholds:** Evaluate against the ORD graduation triggers:
   - npm weekly downloads > 100 sustained → consider graduation
   - GitHub stars > 50 → consider graduation
   - More than 5 substantive non-author issues → strong signal
   - More than 3 integration requests → graduate to Devtool AFPS
   - Enterprise inquiry or revenue potential → cross-domain graduate to Business AFPS
   - Flat or no adoption after 1-2 weeks → archive signal
5. **Recommend (semi-auto gate):** Produce exactly one recommendation with its rationale and the signals that drove it:
   - **Graduate (Devtool AFPS)** → install the Devtool AFPS entry pack with `npx skillpacks install devtool`, then enter at `$devtool-workflow` by default or `$devtool-user-map` when the user wants the first concrete research step. Link the ORD scan, align, ship-log, and traction-log entries as evidence.
   - **Graduate (Business AFPS, cross-domain)** → rare; an OSS tool showing business or enterprise demand. Install `business-research` and enter at `$idea-scope-brief`.
   - **Iterate** → keep it in ORD; ship another version or distribution push.
   - **Archive** → record the outcome and move on to the next experiment.
   State explicitly that the user confirms before any graduation, archive, or further action happens.
6. **Log the check:** Append a traction entry under the package in `research/ord-ship-log.md`:
   - Date of check, weeks since publish
   - Each signal and its value (or `unknown`)
   - Threshold comparison result
   - Recommendation and rationale
   - Status: `iterating`, `graduating`, or `archived`

## Output

End with:

```md
**Traction:** <package name> — <one-line signal summary>
**Recommendation:** iterate | graduate to Devtool AFPS | graduate to Business AFPS | archive
**Next work:** <the confirming action for the recommendation>
**Recommended next command:** npx skillpacks install devtool, then $devtool-workflow or $devtool-user-map (graduate) | npx skillpacks install business-research, then $idea-scope-brief (cross-domain) | $ord-scan (next experiment) | none (archived)
```

## Constraints

- Do not run paid API calls or external account actions to gather signals.
- Do not graduate, archive, unpublish, or delete anything automatically — recommend and let the user confirm.
- Mark unavailable signals as `unknown`; do not fabricate metrics.
- If no ship-log entry exists for the target, report that and stop.
- Create `research/ord-ship-log.md` with a header only if it is missing and a published package clearly exists.

## Cross-Pack Routing

A graduation to Devtool AFPS requires the `devtool` pack. If it is not installed (check `.agents/project.json` `enabled_packs`), include `npx skillpacks install devtool` as the prerequisite in the recommendation. Use `$devtool-workflow` as the default orchestrator after install; offer `$devtool-user-map` as the direct first-step route when the user wants to begin concrete user research immediately.

## Default Shipping Contract

Follow the shared shipping contract convention.
