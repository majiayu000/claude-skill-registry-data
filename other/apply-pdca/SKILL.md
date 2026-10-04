---
name: apply-pdca
description: Use when implementing a process improvement, resolving a recurring operational problem, or running a controlled experiment where you need to learn and standardize before scaling.
source: W. Edwards Deming, "Out of the Crisis" (1986); Walter Shewhart (originator, 1939); ISO 9001:2015 §10; Toyota Production System Kaizen practice
related: [apply-insight-synthesis, apply-fidelity-before-adaptation, apply-5s-methodology, apply-statistical-process-control]
tags: [continuous-improvement, operations, quality, process, lean, kaizen, problem-solving, experimentation]
verified: true
---

# Apply PDCA

Run a disciplined four-phase cycle — Plan, Do, Check, Act — to make improvements systematically, learn from each iteration, and lock in gains before scaling.

## Why This Is Best Practice

**Adopted by:** ISO 9001 (adopted by 1.1 million organizations in 170 countries as of 2022), Toyota Production System (Kaizen), Six Sigma (DMAIC is a direct extension), NHS (UK National Health Service quality improvement), U.S. Department of Defense, and standard curriculum in every accredited operations management program globally.
**Impact:** Toyota's application of PDCA-based Kaizen is directly credited with its position as the world's most efficient major automaker — Toyota's defect rate is consistently 50–70% lower than industry average (J.D. Power IQS longitudinal data). ISO 9001 meta-analyses show certified organizations achieve 15–30% reduction in defect rates and measurable customer satisfaction improvement within two years of adoption (Psomas & Antony, 2015, International Journal of Quality & Reliability Management).
**Why best:** Most improvement attempts skip the Check phase — they implement a change and assume it worked. PDCA enforces measurement of actual results against predicted results before locking in or scaling the change. This prevents three failure modes: improvements that don't actually work, improvements that work but create side-effects, and improvements that are scaled before they're understood.

Sources: W. Edwards Deming "Out of the Crisis" (1986); Shewhart "Statistical Method from the Viewpoint of Quality Control" (1939); ISO 9001:2015 §10.3; Psomas & Antony (2015) IJQRM

## Steps

1. **Plan — Define the problem** — Write the current state in measurable terms. "Customer support tickets take an average of 48 hours to resolve; target is 24 hours." Vague problem statements produce vague plans.
2. **Plan — Identify root cause** — Use Five Whys or fishbone analysis to find the systemic cause before designing the fix. Fixing symptoms produces the symptom again within weeks.
3. **Plan — Design the change** — Write the specific intervention: what will change, who owns it, what resources are needed, and what the predicted outcome is in measurable terms. The prediction is what the Check phase validates.
4. **Plan — Define success metrics** — Choose 1–3 measurable indicators that will tell you whether the change worked. Set a target and a timeline for measurement.
5. **Do — Run a small-scale pilot** — Implement the change in a limited scope: one team, one shift, one product line, or one week. Never scale an untested change organization-wide. Document everything that happens, including deviations from the plan.
6. **Check — Measure actual vs. predicted** — At the end of the pilot, compare actual results to the predicted outcome from step 3. Did the metric move? By how much? Were there unexpected side effects?
7. **Check — Identify what you learned** — If results match prediction: the change works. If not: determine whether the root cause was wrong, the intervention was wrong, or the measurement was wrong. Each answer leads to a different next cycle.
8. **Act — Standardize or abandon** — If the change worked: update the standard operating procedure, train all affected people, and remove the old way. If it didn't: return to Plan with updated understanding. Never leave a "pilot" running indefinitely without deciding to standardize or discontinue.

## Rules

- Never skip the Check phase to save time — an unchecked change is an assumption, not an improvement. If there's no time to check, the pilot scope is too large; reduce it.
- The prediction in Plan is mandatory — without a specific predicted outcome, Check has nothing to validate and learning collapses into "it seemed to help."
- Act means standardize or discard — a change that stays as a "pilot" or "temporary fix" permanently is a process that is neither controlled nor improvable.
- Each PDCA cycle must produce a documented learning that informs the next cycle — continuous improvement without recorded learning is just iteration, not progress.

## Common Mistakes

- **Running PDCA on symptoms instead of root causes** — implementing a fix that addresses the observable problem without identifying why it occurred. The symptom returns in a different form within weeks.
- **Scaling in the Do phase before the Check phase** — rolling out the change organization-wide immediately because it "obviously works." This embeds bad changes at scale and makes them very hard to undo.
- **Treating Act as "done"** — the Act phase that standardizes a change should immediately seed the next Plan phase. PDCA is a cycle; no cycle is the last one.
- **Using PDCA for one-time decisions** — PDCA is a process improvement tool, not a decision-making framework. For one-time irreversible decisions, use premortem or structured decision analysis instead.

## Examples

**Support ticket resolution:** Plan: current 48hr average, root cause is manual triage, predicted fix is automated routing, target 30hr average in 2 weeks. Do: pilot automated routing with one team for 2 weeks. Check: average drops to 31hr, one edge case category routes incorrectly. Act: fix routing rule for edge case, standardize automated routing for all teams, document the exception rule.

**Manufacturing defect:** Plan: 3% defect rate on Line 4, root cause is temperature variance in step 3, predicted fix is tighter thermostat tolerance, target <1% in one production run. Do: adjust one machine on Line 4 for one shift. Check: defects drop to 0.8%. Act: update maintenance spec for all machines, retrain operators, update quality checklist.

## When NOT to Use

- When the problem requires an immediate fix with no time for a pilot — stabilize first, then apply PDCA in the post-incident improvement phase.
- When the process runs too infrequently to generate measurable data in a reasonable timeframe — annual processes need adapted measurement strategies before PDCA can be applied meaningfully.
- When the change is a one-time strategic decision rather than a repeatable process — PDCA improves processes, not decisions; use a decision framework for irreversible strategic choices.
