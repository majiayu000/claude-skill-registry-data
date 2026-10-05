---
name: simplify-report
description: Explain supplied technical reports and already-produced tool output in clear everyday language while preserving the real outcome, severity, uncertainty, and actionable evidence. Use when the user asks what CI results, test summaries, audits, security findings, command output, status checks, or verification reports mean, including requests to simplify, decode, translate, summarize, or explain like they are five. Do not use for general prose editing, live diagnosis, or rerunning the underlying check.
---

# Simplify Report

Explain supplied technical output so the user can quickly understand what happened, why it matters, and what to do first. Preserve the report's actual conclusion.

## Workflow

1. Read only the supplied report or output. Do not rerun tools, checks, or commands unless the user separately asks. If no report or result is available, ask the user to provide it and stop.
2. Identify the overall outcome, meaningful successes, failures or warnings, uncertainty, and the best supported first action. Do not infer an overall pass from successful subchecks.
3. Check whether the evidence is incomplete, truncated, stale, or internally contradictory. State any limitation that changes what can safely be concluded.
4. Separate reported facts from interpretation. Do not present a likely explanation as confirmed or invent a remedy the evidence does not support.
5. Translate jargon into ordinary language. Preserve counts, severity, verdicts, and names the user needs to understand or act; omit internal identifiers that do not help.
6. Draft the answer using the format below, then verify that it matches the report. Correct any softened failure, hidden uncertainty, unsupported claim, or misleading overall status before responding.

## Default output

Follow a format the user explicitly requests. Otherwise:

1. Start with **Bottom line.** State the overall result and its practical meaning.
2. Include every relevant question below. Omit a question only when its answer would add no useful information.
   - **What worked?** Explain the most meaningful successful parts without implying that they made the overall result pass.
   - **What needs attention?** Explain the failure, warning, uncertainty, or unexpected result and why it matters.
   - **What should I do?** Give the best first action supported by the report. When materially different choices exist, name the decision and briefly explain the options instead of choosing for the user.
3. Use as many sentences as needed to make the explanation genuinely easy to understand. Prefer short sentences that explain one idea at a time, and stop when the user has enough context to understand the result and next step. Never omit a necessary explanation just to make the answer shorter.
4. Keep the full answer inside the bottom line and selected questions. Do not add an opener, closing sentence, raw evidence dump, report path, taxonomy, or offer to explain more unless the user asks.

## Writing rules

- Use calm, respectful, everyday language. "Explain like I'm five" means assuming no technical background, using simpler words, and explaining unfamiliar ideas without baby talk.
- Break complicated ideas into small steps. Use a familiar comparison only when it makes the meaning clearer.
- Lead with practical meaning, not the report format or the analysis process.
- Preserve severity. Never turn failed, blocked, incomplete, unsafe, or uncertain into passed or okay.
- Preserve mixed outcomes explicitly. State both a successful component and a failed overall result when both are true.
- Preserve uncertainty. If the evidence cannot establish something, say so plainly.
- Keep actionable evidence such as a count, severity, filename, command, or product term when it changes understanding or next steps.
- Distinguish a product failure from a check, tool, or environment failure.
- Do not assign blame or infer who caused a change.
- Do not invent remediation. If the report supports no safe next action, say what information or decision is needed first.
- For medical, legal, financial, privacy, or security findings, simplify the language without softening risks or removing necessary cautions.

## Example

Input meaning: tests passed, two task files stayed in scope, one unrelated file changed, and the overall scope check failed.

Output:

**Bottom line.** The work passed its tests, but the overall scope check failed because an unrelated configuration file also changed.

**What worked?** The tests passed, and the two task files stayed in the agreed area.

**What needs attention?** `config/prod.json` changed outside that area. That extra change is why the overall check failed.

**What should I do?** Review the config change and decide whether to remove it or explicitly include it in the task.
