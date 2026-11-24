---
name: tilt-check
description: Independently re-investigate a finding that has already been marked a False Positive, by an AI triage agent, another analyst, or an automated tool, to check whether that verdict actually holds up. Treats the FP call and its justification as an unverified claim, not fact, and actively hunts for a reason the finding is still exploitable before agreeing to close it out. Trigger this whenever the user pastes a False Positive verdict, a suppression justification, a "not applicable" or "won't fix" ticket comment, asks to double-check, audit, sanity-check, or second-guess an AI triage result, or asks "are we sure this is actually a false positive?"
---

# Tilt Check

## Why this skill exists

An agent that triages security findings can be wrong in exactly the way a human analyst under deadline pressure is wrong: it finds one plausible reason a finding looks safe, stops looking, and writes it up convincingly. A confident, well-cited False Positive writeup is not the same thing as a correct one. The citations can be real and the conclusion can still be wrong, because the reviewer stopped one hop short of the path that actually matters.

This skill is the governor on that process. It does not re-run the original triage from scratch and does not trust the original triage's conclusion, evidence, or tone of confidence. It takes the FP verdict as a claim someone is asking you to sign off on, and its job is to try to break that claim before agreeing with it. If a genuinely thorough, skeptical, independent look still lands on False Positive, that agreement is worth something. If it doesn't, that's the entire point of running this.

This is the inverse of [`player-two-verdict`](../player-two-verdict): that skill takes a scanner's raw verdict and checks whether it's real. This skill takes a human's or an agent's "it's not real" verdict and checks whether *that's* real.

## When to use this

- The user pastes a completed triage writeup, suppression justification, or ticket comment that concludes False Positive / Not Applicable / Won't Fix, and wants it double-checked.
- The user asks to audit, sanity-check, second-guess, or challenge an AI-generated or human-generated false positive call.
- A batch of findings was just triaged (by this plugin's own triage skill or anything else) and the user wants an independent pass before anything gets suppressed for real.

If the user instead pastes a raw, untriaged scanner finding with no verdict attached, that's the other skill's job, not this one. This skill needs an existing FP claim to challenge; it doesn't do first-pass triage.

## Step 0: Prerequisite check

This skill's entire value depends on reaching its own conclusion, not on confirming one that's already sitting in the conversation. If the original FP verdict was produced earlier in this same session (for example by [`player-two-verdict`](../player-two-verdict) running right before this), or if the user has been discussing the finding with you before pasting the verdict, your own read of it is already anchored to that reasoning. Running the "independent" audit in that same context isn't independent, it's the same judgment re-reading its own homework and agreeing with itself. Step 1 below exists to guarantee real isolation, not just a claimed one.

Confirm an `Agent`-style tool is available that can spawn a fresh subagent with a fresh `subagent_type` (e.g. `general-purpose`), explicitly not a `fork` type or any option documented as inheriting the caller's context, since a fork's entire premise is shared memory with this conversation, which defeats the isolation this skill depends on.

If your environment genuinely has no way to spawn an isolated subagent, don't silently do the audit yourself in the shared context and present it as independent. Say plainly that this conversation already contains prior context on the finding and a truly independent check isn't possible here, and recommend the user open a fresh session and paste the FP verdict there instead.

## Step 1: Isolate the review

Do not perform Steps 2-6 yourself in this conversation. Delegate the entire audit to the fresh subagent confirmed available in Step 0, one that starts with no memory of this conversation, not a fork or continuation of it. Give that subagent nothing but:

- The raw pasted material exactly as the user provided it: the original finding, the FP verdict, and its justification.
- The repo location/access it needs to investigate.
- The full instructions in Steps 2-6 below.

Do not pass along your own read of the finding, anything said earlier in this session about it, or any hint of what verdict a prior review (yours or anyone else's) reached. The subagent's conclusion has to come from the raw material and the repo alone, or the isolation is theater.

Wait for the subagent to finish, then relay its finished output back to the user as-is. Don't edit its verdict, soften it, add commentary on top of it, or skip the delegation because the case looks obvious from where you're sitting, that instinct is exactly the failure mode this skill exists to catch.

## Step 2: Parse the input

Extract, from what's pasted:

- The original finding: tool, rule ID, CWE/CVE, file/line or package/version, severity as reported.
- The verdict being challenged: confirm it's actually claiming False Positive (or an equivalent like Not Applicable, Won't Fix, Suppressed, Accepted Risk with a "not exploitable" rationale). If it's a True Positive verdict, say so and stop, there's nothing adversarial to do here, the skill exists to pressure-test dismissals, not confirmations.
- The stated justification: every piece of evidence the original reviewer used, file:line citations, described control (sanitizer, auth middleware, config override, rotation, whatever), and the reasoning connecting that evidence to "not exploitable."

If the justification is missing evidence entirely (just "FP, not exploitable" with no reasoning), that's already a signal, note it explicitly in the output as a governance gap rather than trying to reconstruct a justification nobody gave you.

If a cited file or line doesn't resolve in the repo, don't assume it's a typo and move on, that's exactly the kind of gap this skill exists to catch. Flag it and keep investigating from what does resolve.

## Step 3: Handle multiple findings

Same batching logic as the sibling skill. Same root cause (same suppression reasoning applied across several instances): audit the reasoning once, list every file:line instance under the result. Unrelated findings: cap at 3-4 per run to avoid cross-contaminating evidence between independent audits in the same context window. If there are more, say so and either take the first 4 or ask the user to split it, based on how they framed the request.

After a multi-finding run, close with a note recommending `/compact` before the next audit.

## Step 4: Investigate, adversarially

Work silently. No narration of intermediate steps, no "let me check the citation now." The user gets the finished governance verdict, not a transcript.

The stance here is different from a neutral re-investigation: you are not trying to independently arrive at a verdict, you are trying to find the specific reason the FP verdict is wrong. If you can't find one after genuinely trying, the verdict survives. If you stop looking the moment the first citation checks out, you've just rubber-stamped the same mistake the original reviewer might have made. Treat the absence of a counter-argument as the bar to clear, not the presence of a plausible-sounding one.

### 4a. Audit every citation

Open every file:line, config value, or lockfile entry the original justification points to. Confirm it actually says what's claimed, not approximately, exactly. A citation that's off by a few lines, references a different function with a similar name, or describes stale behavior (the code has since changed) invalidates the reasoning built on it even if the general idea was right.

### 4b. Find the load-bearing claim and attack it directly

Every FP justification rests on one or two claims doing all the work: "input is sanitized here," "this path is unreachable," "not attacker controlled," "already rotated," "config is overridden in prod." Identify that claim. It's the single point of failure in the argument. Spend your investigation budget there, not re-confirming details that were never in question.

- **Sanitization claims**: confirm the sanitizer is the right one for this sink (HTML-escaping doesn't stop SQL injection), confirm it actually executes on this code path and not just somewhere in the file, and check for bypasses, encoding tricks, type confusion, case sensitivity, null bytes, list vs. allowlist gaps.
- **Unreachability claims**: search for every caller of the flagged function or route, not just the one the original reviewer traced. A second, less obvious entry point that reaches the same sink overturns the verdict even if the first path really is dead.
- **"Not attacker controlled" claims**: check whether the "trusted" source is actually attacker-influenced indirectly, through a config file a user can edit, an upstream service that itself accepts untrusted input, a header the original reviewer assumed was server-set.
- **Compensating control claims** (middleware, auth, framework auto-escaping): confirm the control actually sits on this exact path for every route/method that reaches the sink, not just the one example checked. A middleware applied to some routes and not others is a common source of a wrong FP.
- **Rotation / already-fixed claims** (secrets, patched versions): confirm with a timestamp or commit, not a description. "The team said it was rotated" is not evidence, a rotation log entry or a new credential replacing the old one in config is.
- **SCA "not called" claims**: go one layer deeper than the original reviewer did. If they checked the direct import, check whether a transitive dependency or a dynamic call (reflection, string-based dispatch, plugin loading) reaches the vulnerable function anyway.
- **IaC "overridden" claims**: confirm the override actually applies to the deployed environment in question, not a different environment or an unused module variant.

### 4c. Steelman the true positive

Before writing the verdict, explicitly try to construct the strongest realistic case that this finding is exploitable, given everything you now know. If that case is weak, thin, or requires stacking multiple unlikely assumptions, that's real signal the FP verdict is solid, say so. If it's not weak, that's the overturn.

## Step 5: Determine the governor's confidence

Same five-level scale as the sibling skill, applied to how solid your own conclusion about the FP verdict is, not the original reviewer's confidence.

- **Very High**: every citation checked out, the load-bearing claim was independently confirmed (or independently broken), no gap in the evidence either way.
- **High**: strong evidence, one minor unconfirmed detail that wouldn't flip the outcome.
- **Medium**: the core claim holds or breaks on solid evidence, but at least one real unconfirmed link remains, e.g. can't verify a runtime config or fully rule out an alternate call path.
- **Low**: evidence is thin or mixed. Give a reasoned lean, not a confirmed answer.
- **Very Low**: evidence is largely absent, e.g. the original justification cited nothing checkable. Don't default to upholding the FP just because you found nothing to contradict it, silence isn't confirmation.

## Step 6: Write the output

### Governance philosophy: default to skepticism, not to agreement

The three possible outcomes are not symmetric. Overturning an FP costs someone a few extra minutes of review. Upholding a wrong FP lets a real vulnerability ship as "handled." When the evidence is genuinely insufficient to confirm the original verdict, that is not a reason to let it stand, it's a reason to escalate. Never write "insufficient evidence to overturn, so FP stands." Insufficient evidence means the suppression isn't earned yet.

### Voice

Same register as the sibling skill: a senior AppSec engineer reviewing a colleague's, or an AI's, sign-off before it goes final. Direct, plain, no lecture.

- No em dashes.
- No preamble, no filler, no flattery. Start at the verdict line.
- No closing summary. End at Action.
- Active voice throughout.
- Every claim in the audit is backed by a file:line citation you personally verified, and the function or symbol name where one exists, or explicitly marked unverifiable.
- Keep the sections doing different jobs. "Summary" is the plain-language headline, no citations, no code, written for someone who may only read that one line. "Citation audit" and "Independent evidence" state only what's factually at each location, no interpretation. "Justification" is where the reasoning happens, and every bullet in it has to point back at a specific line above it, not introduce a new unsupported claim.
- No hedge words unless confidence is genuinely Low or Very Low.
- Say plainly when the original justification was solid. This isn't about finding fault for its own sake, a correctly upheld FP is a good outcome and should read as one, not as a grudging concession.
- Say just as plainly when it wasn't. Don't soften an overturn to spare the original reviewer, human or AI, that defeats the purpose.

### Format

Use this template exactly. Omit optional lines when they don't apply, don't leave placeholder text. "Summary" always comes first, right after the verdict line, and is the one field written for a reader with no security background: no jargon, no code, no citations. Everything below it is for the reader who wants to verify the call themselves.

```
🟢 UPHELD | Confidence: [level]
[or 🔴 OVERTURNED | Confidence: [level]]
[or 🟡 INSUFFICIENT EVIDENCE, treat as unresolved | Confidence: [level]]

Summary: [2-3 plain-language sentences. What the original verdict
claimed and, in plain terms, whether this audit agrees and why. No
jargon, no citations, no code. A reader who stops here should still
understand the call.]

Original verdict: [what was claimed, e.g. "False Positive, input is sanitized"]

Load-bearing claim: [the one claim the FP verdict actually depends on]

Citation audit:
- `path/file.ext:line` (cited as: [what the original justification claimed it shows]): HOLDS UP / DOES NOT HOLD UP: [what's actually there]
- `path/file.ext:line` (cited as: [...]): HOLDS UP / DOES NOT HOLD UP: [...]
[one bullet per citation the original justification relied on]

Independent evidence:
- `path/file.ext:line`, `functionOrSymbolName()`: [what this audit found on its own, factual, no interpretation]
- `path/file.ext:line`: [...]
[2-5 bullets, results of chasing alternate call paths, bypasses, stale claims, or anything the original review didn't check]

Justification:
- [reasoning bullet, cites specific lines from Citation audit and/or Independent evidence above by file:line]
- [reasoning bullet, cites evidence above]
[2-4 bullets. This is where "does the load-bearing claim survive" gets answered, no new facts, only bullets that connect the evidence to the verdict]

Gap in original review: [what the original reviewer missed or didn't check, omit only if the original review was genuinely thorough]

Action: [Upheld: suppress as originally justified, no further work. Overturned: reclassify as True Positive, route for a fix, cite the reachable path that proves it. Insufficient evidence: name the specific thing that would resolve this, and who/what can check it, don't suppress until it's answered.]
```

For batched same-reasoning findings, use one block, list every file:line instance as its own bullet under "Independent evidence" instead of a single citation.

If the run covered multiple findings, add one line after the last verdict block:

```
Ran /compact before the next audit to keep this session's context clean.
```
