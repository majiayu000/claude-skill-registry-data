---
name: diagnose
description: Diagnose a specific agent, tooling, configuration, or workflow incident before any remedy. Use for /diagnose, why-did-this-happen questions, recurring process failures, broken hooks/skills/scripts, or diagnose-and-fix requests; not for ordinary code bugs, broad configuration audits, or repository-wide AI developer-experience reviews.
---

Use this workflow to establish why a specific incident occurred before changing the failing mechanism. Treat errors, confusion, and friction as *symptoms* of an underlying issue, not as direct fix targets. For a diagnosis-only request, the deliverable is the diagnosis. For a request that also asks for a fix, diagnose first, then implement the confirmed remedy.

Do not use this skill for ordinary code debugging, planned implementation work, broad agent-configuration inventories, or repository-wide developer-experience audits. When the request includes a fix, diagnose and perform the confirmed in-scope remedy in the same turn. Do not add external, destructive or hard-to-reverse actions without the required explicit authority; an audit/fix request does not silently grant it. Follow local approval policy and never add ask-style tool gates as an enforcement repair.

First establish the incident: exact expected versus observed behavior, time, runtime/session/account/project, versions and relevant changes. Distinguish the user's report, current observations and hypotheses. Preserve the original evidence before changing the failing mechanism. Investigate narrowly enough to explain this incident, not every configuration in the environment.

Your job is to:

1. **Check existing coverage.** Identify the hooks, skills, configs or scripts plausibly responsible for this incident. Separate configured, loaded/registered, triggered, successful and acted-on states. Reading a file establishes intended behavior, not that it ran in the failing session. Use time/session-matched execution evidence where available and mark missing evidence unknown. A missing log entry is not proof of nonexecution unless logging coverage is established.
2. **Identify the causal chain.** Trace observed inputs and effects, test competing explanations with safe discriminating checks, and distinguish the immediate cause from contributing conditions. Do not force uncertain, mixed or external causes into a single label. Separately assess prevention/detection gaps:

   - *Structural gap*: a required prevention/detection function is absent or its implementation is broken. Show the unmet requirement, causal relevance and appropriate boundary.
   - *Enforcement gap*: prose or a manual step covered the immediate failure, but the operation is repetitive, low-level, and deterministic enough to enforce. Name both the immediate rule violation and the mechanism that would prevent, constrain, or automatically detect that class of failure.
   - *Behavioral lapse*: an instruction or mechanism was demonstrably available, clear, sufficient and usable but was not followed, or its successful result was ignored. Use this only when evidence supports those prerequisites and no practical enforcement improvement is indicated. Stop adding prevention mechanisms for that lapse; this does not cancel separately requested, authorized recovery or correction after the diagnosis.

3. **Check the broader class** using relevant analogous paths, runtime modes or prior evidence. Do not call an incident recurrent from one observation or expand into an unrelated audit.
4. **Propose structural fixes for demonstrated structural or enforcement gaps.** Prefer repairing the responsible mechanism at its canonical source over stacking another wrapper or instruction. Explain the exact class covered, tradeoffs, false-positive/false-negative risks and how to verify enforcement. If only discipline was missing, name what was not followed; do not invent another mechanism. Ordinary external outages or expected guard denials may have no local implementation defect.
5. **Report, then stop or fix depending on the request.** Present the observed symptom, mechanisms checked, diagnosis category, evidence, broader pattern, and any structural remedy candidates. If no reliable structural fix is visible yet, say what remains to investigate. When the request was diagnosis-only, do not implement the remedy until the user asks; when the request included fixing, implement the confirmed remedy in the same turn (subject to the reversibility limits above).

While diagnosing, do not alter the failing mechanism or erase evidence just to make the symptom disappear. Do not repeatedly execute a harmful operation to obtain a reproduction. Use preserved evidence or isolated fixtures, with explicit uncertainty when they cannot establish the historical cause. Inspect diagnostic commands for writes, network/account effects or sensitive output before running them; use the routed service/secret-handling rules. Do not disable a guard, restart live applications, reset state or install dependencies as an implicit diagnostic step.

After a confirmed in-scope fix, test the exact reported behavior through the relevant runtime or a direct requirement-covering fixture, and check analogous affected paths. A source edit, successful hook unit test or changed metric does not alone prove live behavior. Distinguish causal evidence, fixture coverage and runtime verification; state material gaps rather than claiming resolution. Preserve unrelated work and commit logical owned fixes according to project policy. Diagnosis-only requests end with findings, not implementation.

## Diagnostic communication

When a diagnosis uses overloaded local tooling labels, define the concrete artifact in plain language before relying on the label: e.g. a Markdown skill file, plugin bundle, agent-skill helper, Emacs package, command wrapper, or hook script. Do this only when ambiguity could affect the explanation; do not define ordinary unambiguous terms.

## Before proposing any fix

For instruction/context-loading questions, inspect supported session diagnostics or the exact mechanism that creates the context. Bind evidence to the relevant agent/runtime, scope and invocation. Distinguish a file on disk, an available skill catalog entry, a body read during a task and proven injected context. A diagnostic rerun describes that rerun, not necessarily the original session. If the runtime does not expose the needed evidence, say what is unknown; do not claim access to hidden context or infer historical loading from configuration alone.

Run this check: *would an existing mechanism, firing as intended, have prevented this failure or surfaced it in time?* If no, determine whether prevention/detection was required and can reliably occur at a controllable boundary. Lack of universal prevention does not itself justify a new hook. If evidence is incomplete, keep the gap provisional.

If yes, ask: *is it enforced, or is it prose requiring a brittle deterministic operation to be performed by attention?* If a practical tool, hook, config or wrapper can enforce it at the actual execution boundary, identify an enforcement gap rather than stopping at discipline. Confirm the current rule was available before attributing a violation. Determinism in one test is not proof of coverage across alternate command forms, runtimes or asynchronous paths. Otherwise classify a behavioral lapse only with evidence that the rule was clear, sufficient, usable and not followed.

## What counts as a structural fix

A structural fix is a **mechanism** that prevents, constrains or automatically detects a defined failure class. Examples include a covered commit hook, an enforced configuration constraint, a deterministic resolver actually used by callers, or a CI check whose result gates completion. A Markdown skill or memory entry can supply useful guidance but does not force its own invocation or compliance. Claim automatic loading/enforcement only when a verified runtime path provides it; retain useful guidance when it serves a distinct purpose.

The following are NOT structural fixes and must NEVER be proposed as solutions:

- "I should do X in the future" — this is a resolution, not a mechanism. It depends on memory and discipline, which are exactly what failed.
- "I will be more careful about Y" — same problem. There is no enforcement.
- "I should scan/check/review Z before starting" — unless a verified execution mechanism forces or checks that scan, this remains an intention. Merely writing it to a skill, memory or configuration prose is not enforcement.

For a guard or resolver repair, check both the original legitimate case and the
relevant unsafe or wrong-scope negative control. Removing a protection is not a
successful false-positive fix. Test the actual enforcement boundary and report
any runtime/command forms that remain unverified.

If no reliable structural remedy is supported, say what evidence or controllable
boundary is missing. Do not prescribe a hook by default or fill the gap with
aspirational statements. A justified diagnosis may end without a new mechanism.
