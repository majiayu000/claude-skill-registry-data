---
name: systematic-debugging
description: Use to find the cause of a failure when it is unclear, after a fix did not hold, or for a flaky or production-only failure; it reports a diagnosis and changes no production code. To fix a reported bug end to end, run the bug-fix playbook instead; it calls this skill.
---

# Systematic Debugging

Find the cause of a failure and say how sure you are. The deliverable is a
diagnosis, not a fix: change no production code beyond temporary
instrumentation. Fixing belongs to the caller, usually the bug-fix playbook.

## Diagnose

1. Preserve the symptom, environment and relevant evidence. Reuse an existing
   failing test or command; otherwise build the smallest useful reproduction.
   Candidate methods include a focused test, CLI fixture, captured trace or
   isolated scratch harness. Minimize only enough to distinguish live causes.
   Confirm it shows the reported failure, not a nearby one. When a check
   fails unexpectedly, test the way it observes (the check, its fixture, the
   probe, the environment it reads) before concluding the system is wrong.
   If fixes were already tried, take their attempt log as evidence.
2. Form provisional hypotheses from code and evidence. Label them as hypotheses;
   choose a discriminating observation instead of generating a fixed count.
   A failure that appears only after a restart points first at persisted
   state: configuration files, caches, lock files, serialized state.
3. Probe the suspected boundary or variable, update the explanation, then repeat
   only while new evidence is produced. Tag every temporary probe with one
   unique prefix so cleanup is a single search. For cross-layer tracing or
   bisection, consult `references/localization.md`. Keep asking why at each
   link until the answer is a wrong decision in the code, not a consequence
   of an earlier one.
4. Before naming the place a symptom surfaced as the cause, decide whether
   the state that triggered it is legitimate. If the system may be in that
   state, the code that broke on it is the cause and handling the state there
   is the fix; if not, a guard there would hide the fault, so trace the state
   to what produced it.
5. Decide the status (below). A cause is confirmed by the reproduction or, when
   none is obtainable, by independent evidence such as traces.

For flakes or production-only failures, use `references/non-reproducible-bugs.md`;
for order-dependent tests, the bundled `scripts/find-polluter.sh` may help. If no
reproduction is available, continue safe source analysis or instrumentation.

A performance regression needs comparable timing evidence. A resource target
without a known regression belongs to performance-optimization; do not require a
failed bisect before switching when evidence already supports that distinction.

When hypotheses run out, get a critic review (review skill); pass artifacts (the
reproduction, its output, attempts), not conclusions.

## The diagnosis

One answer with one status:

- **Confirmed:** the cause, the evidence that confirms it (the reproduction
  command and its output, or the independent evidence) and the verification
  limit.
- **Provisional:** any cause not confirmed that is not an unresolved finding
  below, whether or not the failure reproduces. Give the reproduction if there
  is one, the safe source analysis, the remaining hypotheses and the evidence
  that would tell them apart (request it), and label any proposed fix unproven.
- **Unresolved:** an environmental or external cause, claimable only as
  `references/non-reproducible-bugs.md` describes, with the investigation
  attached. Offer no mitigation as the fix.

Every status also lists the reproducers kept and any temporary instrumentation
still in place.

## Cleanup

Before answering, remove the temporary instrumentation you added and keep
useful reproducers and user artifacts. When the caller says its own closeout
removes them, as the bug-fix playbook does, leave them and list them instead.
