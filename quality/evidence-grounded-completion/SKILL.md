---
name: evidence-grounded-completion
description: Verifies completion claims with evidence before declaring done. Use before stating "done", "complete", "fixed", "shipped", "ready", or any synonym. Use when wrapping up a unit of work and about to summarize to the user. Use when about to acknowledge a user-reported issue with "good catch". Use also before asserting a factual property of an artefact you have not read (a state assertion in research, assessment, planning, or review), not only at completion. Also use before ending a turn on a stated intention ("continuing with X", "next I will do X"), which is a claim about your own next action.
derives_from: ../../governance/evidence-grounded-completion.md
---

# Evidence-Grounded Completion

## Overview

A completion claim is a state assertion a reader will rely on. This skill runs the six-step verification protocol from the canonical rule [`governance/evidence-grounded-completion.md`](../../governance/evidence-grounded-completion.md) before any completion claim is emitted.

The rule is the source of truth for normative content (framework alignment, exception handling, rationale). This skill is the workflow wrapper: when to invoke the protocol and how to execute it step by step.

## When to Use

- Before stating "done", "complete", "completed", "finished", "fixed", "shipped", "ready", "resolved", "addressed", "handled", "all set", "good to go", "validated", "verified" (in the conclusory sense), "confirmed", "looks good", or "LGTM".
- Before saying "good catch" in response to a user-reported issue (the phrase implies "I understand the scope and have it under control", which is itself a state assertion).
- Before wrapping up a unit of work with a summary message that a reviewer or downstream operator will rely on.
- Before ending a turn on a sentence about your own next action ("continuing with X", "next I will do X"): it is a commitment, true only if you take that action before yielding, so if you are yielding, report the state instead.
- After a gate, lint, audit, or test suite reports green and you are about to claim the underlying work is complete (passing gates prove what gates check, not the whole claim).
- Before asserting a factual property of an artefact you have not read: that a file, template, schema, configuration, or document contains, lacks, or requires something, in any phase including research, assessment, planning, or review. Read the artefact first, or label the statement an unverified hypothesis. See the canonical rule's section "Beyond completion: claims about artefact state".

## Process

The six-step verification protocol from the canonical rule, executed in order:

1. **Enumerate every file in scope**. List, by path, every file touched or referenced by the claim you are about to make. Unrelated files do not count; relevant files do, even if you did not touch them.
2. **Re-read each file in full**. Not just the section you edited. Not just the lines around the diff. For very long files where a full re-read is impractical, state explicitly which sections you read and which you did not.
3. **Quote specific lines that support each claim**. Paraphrases do not count. Cite by `path:line-number`. If the claim depends on a passing audit, the supporting evidence is the audit output and exit code, not "I ran it and it looked fine".
4. **Search for contradictions**. For each claim, run a search across the affected files for phrases that would falsify the claim if present. Report the search command and the result. A search that returns nothing is evidence. A search that was not performed is not.
5. **Distinguish mechanical from semantic verification**. A passing gate proves what that gate checks. It does not prove claims the gate does not check (internal consistency, prose accuracy, currency of citations). State the gate-coverage boundary explicitly: "All N gates pass; this proves [list]; it does not by itself prove [list of unchecked claims]; I have separately verified [list] by re-reading [files] and quoting [lines]".
6. **State unverified items explicitly**. Name the unverified part. Do not imply verification you did not perform.

If the contradiction search returns a positive result, the claim is not yet supported. Fix the contradiction. Re-run the search. Then re-claim.

## Red Flags

- Declaring victory in the same message that carries the failing tool result.
- Treating user silence as confirmation.
- Relying on prior runs ("it passed last time and the change is small") to substitute for verification on the current state.
- Saying "good catch" before enumerating the scope of what was caught.
- Hedging with "should" or "appears to" while still making a state assertion.
- Stating a claim and immediately performing the search that would have falsified it (the search is part of the claim, not a coda).
- Conflating "I edited the file" with "the file is correct".
- Skipping the protocol to make progress faster.

## Verification

The protocol is complete when:

- Every file in scope has been re-read (or the unread sections are named explicitly).
- Each completion claim is grounded in a quoted line.
- The contradiction search has been run and the search command and result reported.
- The gate-coverage boundary is stated explicitly (which claims are gate-verified vs which required a separate re-read).
- Unverified items are listed by name.

If any of these is missing, the protocol is incomplete and the completion vocabulary is not yet permitted.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "All the gates pass, so it must be done." | Gates prove what they check. Claims the gates do not check require separate verification. |
| "I just edited it; of course it is correct." | The edit happened. Correctness is a separate proposition. |
| "The user did not push back, so it must be right." | Silence is not verification. The user may not have noticed. |
| "The protocol is slow; let me skip it just this once." | Skipping is the failure mode the protocol exists to prevent. |

## See Also

- Canonical rule [`governance/evidence-grounded-completion.md`](../../governance/evidence-grounded-completion.md): framework alignment (NIST SSDF N/A; CSA CCM GRC-04 / GRC-05 / LOG-02 / LOG-04 / LOG-10; ISO 27001 Annex A.5.4 / A.5.36 / A.8.15; OWASP ASVS V15.1 / V16.2 / V16.4), exception-handling protocol for genuinely impractical re-reads, and the discussion of why an AI coding assistant is the dominant target of this discipline.
- Related skill [`clarify-before-acting`](../clarify-before-acting/SKILL.md): handles ambiguity before action. This skill handles verification after action.
- Related skill [`gate-discipline-diagnose`](../gate-discipline-diagnose/SKILL.md): handles gate failures. When a gate fails, fix the artefact and then run this skill to verify the fix actually closed the underlying issue.
- Related skill [`validation-sweep`](../validation-sweep/SKILL.md): applies this skill's per-claim verification protocol at project-wide scope. After any issue identified and corrected, the sweep confirms no sibling issue remains.
- Related skill [`citation-quote-verification`](../citation-quote-verification/SKILL.md): specializes this skill's protocol to citation-bearing content (quote-to-source correspondence).
- Related skill [`fresh-reader-validation`](../fresh-reader-validation/SKILL.md): complements step 2 (re-read each file in full) with an outside reader for new or substantively-revised documents.
- Related skill [`skill-authoring-discipline`](../skill-authoring-discipline/SKILL.md): applies this skill's verification discipline to authoring new pack skills (trigger-accuracy validation, structural-template compliance).
