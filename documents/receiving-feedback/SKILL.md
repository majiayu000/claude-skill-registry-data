---
name: receiving-feedback
description: |-
  You MUST use this when receiving feedback that evaluates a text-based work artifact you produced or are responsible for — code, specs, design docs, PRDs, proposals, plans, or prose — by asserting a defect, questioning a decision, supplying reasoning, or proposing a change for assessment. Also use when asked to implement external review comments that must first be assessed. Not for an unambiguous parameter choice, approval, confirmation, typo or formatting fix, or direct revision instruction that supplies no claim or rationale to evaluate.
---

# Receiving Feedback

## When to Use

Feedback gives a claim, concern, question, or rationale about a work artifact that can be evaluated.
A revision request alone is an instruction, not feedback.
Use this skill when the message contains something to evaluate:

- Receiving review comments on code, specs, design docs, PRDs, proposals, plans, or prose.
- Feedback seems unclear, contradictory, or technically questionable.
- External feedback (PR comments, forwarded notes, stakeholder input) arrives without full context.
- Multiple feedback items where some are unclear and you're tempted to act on the clear ones first.

## When Not to Use

- You are the one _giving_ feedback (use `code-review` instead).
- Feedback is a simple typo fix or formatting correction with no ambiguity — just fix it.
- The message is not feedback on an artifact.
  These are directives to carry out, not commentary to evaluate — act on them directly:
  - A **parameter choice** ("use Postgres", "make the timeout 30s", "call it `sync`").
  - An **approval** ("looks good", "ship it", "approved").
  - A **confirmation** (answering a question you asked — "yes", "the second one").
  - A **direct execution instruction** ("add a login endpoint", "rename this function").

## Overview

Verify against ground truth before revising.
Ask before assuming.
Correctness over social comfort.
When no ground truth exists, surface that explicitly — do not guess.

**Scope:** AI-as-recipient — all text-based work artifacts.

**No performative agreement (hard gate)**

Never respond with "You're absolutely right!", "Great point!", "Thanks for catching that!", or any other performative or gratitude expression.
State the requirement, present your assessment, or just act.
The work itself shows you heard the feedback.

## Invocation Notice

- Tell the user when this skill is running: `receiving-feedback`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## The Response Pattern

```text
WHEN receiving feedback on a work artifact:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. GROUND: Identify the ground truth to verify against
   - If ground truth exists → check feedback against it
   - If no ground truth exists → surface this to the user before proceeding
4. EVALUATE: Is this feedback sound given the artifact's context and constraints?
5. GENERALIZE: For each accepted item, name its cause and class, and search for other instances
6. RESPOND: Technical acknowledgment, reasoned pushback, or risk escalation
7. REVISE: One cause at a time, verify each
```

## Generalizing From Items

**Hard gate.**
Treat review items as a sample of the artifact's defects, not a complete list: a reviewer who found one instance seldom found every instance.
Run this step for every item you will revise for, however you came to accept it, once all unclear items are answered.
Skip typo and formatting items.

1. Name the cause (the reason the defect exists; list each plausible one) and the class: a predicate as broad as the cause, with no file, line, section, identifier, or heading in it.
   A location in the predicate anchors the search at that location.
2. Group items by cause; a shared cause is one finding.
3. Search for the class in the artifact under review and its neighbors: for code, its callers and callees; for a document section, the sections it cites and the sections that cite it.
4. Treat each match as a candidate.
   Rule one out only with named evidence that it differs on purpose: a guard, a contract, a comment, or a test.
   If most matches share the cited site's form, the cited site follows a convention: present the convention to the user as a decision.
5. If the cause is upstream of the artifact (an assumption, a design decision, a requirement, or a test gap), name it and let the user decide.

Report each cause with its predicate, the scope searched, the confirmed instances, and the ruled-out candidates with their evidence; one line is enough when nothing else matched.
Fix a cause with the smallest change that removes every instance; propose a new abstraction, do not build it.
An instance inside the artifact is not added scope and follows the user's pacing, except a Polish-tier class (Simple fixes, for code): report its count and wait for opt-in.
An instance in a neighbor is a separate finding.
A blocking instance can get a local fix first.

## Pacing: When To Act vs. When To Wait

**On first feedback item (soft gate):** After restating understanding and grounding against truth, present your assessment and wait.
Do not start revising.
This gives the user space to workshop, redirect, or ask their own questions before you act.

**Calibrate from the user's response:**

- "Go ahead" / "implement" / "looks good" → shift to action-first on subsequent items
- Further questions, refinements, or redirects → continue workshopping each item before acting
- "Just do it" or similar → shift to direct action for the remainder

Default to presenting your assessment.
Let the user's response set the pace.

## Handling Unclear Feedback

```text
IF any item is unclear:
  STOP — do not revise anything yet (hard gate)
  ASK for clarification on ALL unclear items

WHY: Items may be related. Partial understanding leads to drift and error.
```

**Example:**

```text
Feedback: "Fix items 1-6"
You understand 1,2,3,6. Unclear on 4,5.

WRONG: Revise 1,2,3,6 now, ask about 4,5 later
RIGHT: "I understand items 1,2,3,6. Need clarification on 4 and 5 before proceeding."
```

## Feedback Context: In-Conversation vs. External

### In-conversation feedback

Both parties share the same information.
Higher trust — proceed after understanding and grounding.
Still verify against ground truth.
Once the user has signaled their preferred pace, act accordingly.

### External feedback

Anything from outside the current conversation: forwarded comments, pasted reviews, PR feedback, email, stakeholder notes.
The reviewer may lack full context.

**Before revising (hard gate):**

1. Technically correct for THIS artifact?
2. Conflicts with existing decisions or constraints?
3. What motivated the current approach?
4. Does the reviewer understand the full context?
5. Has an independent reviewer raised this before?
   Convergence escalates scrutiny — re-probe; do not answer a repeat finding by citing the precedent.

If the feedback seems wrong, push back with specific reasoning.

If you cannot verify, say so: "I can't verify this without [X].
Should I [investigate/ask/proceed]?"

## Revision Ordering

When the user signals to proceed, revise in this order:

1. **Clarify everything unclear FIRST** (hard gate)
2. Then revise by priority:
   - **Correctness** — factual errors, broken logic, wrong claims
   - **Structure** — organization, flow, missing or extraneous sections
   - **Precision** — vague language, ambiguous requirements, weak specificity
   - **Polish** — tone, style, formatting, consistency
3. For non-code artifacts, invoke `antislop-writing` as a final pass (soft gate)
4. **Verify coherence** — no regressions, earlier fixes should still hold, and the artifact should be internally consistent

For code-specific revision ordering, see `references/code-review-reception.md`.

## When To Push Back

**Push back (hard gate):** When feedback is verifiably wrong against ground truth.

**Evidence symmetry (hard gate):** a declination carries the same empirical burden as an acceptance.
If the finding can be probed, probe it before pushing back — reasoned argument alone does not discharge this gate when a test, command, or measurement is available.

**Push back (soft gate):** When feedback:

- Conflicts with prior decisions or constraints established in conversation
- Comes from a reviewer who lacks full context
- Adds unnecessary scope or extraneous/duplicative content
- Would introduce inconsistency with the rest of the artifact

**How to push back:**

- Specific reasoning, not defensiveness
- Reference the ground truth; a prior decision is context to re-examine, never ground truth for a dispute about that decision
- Ask targeted questions

## Risk Escalation

**Hard gate.**
When responding to feedback — whether agreeing or pushing back — could create friction or externalities beyond the artifact itself (damaging a relationship, committing to expensive scope, contradicting a stakeholder publicly, undermining prior positioning), describe the specific risk and let the user decide how to proceed.

Do not navigate social or political dynamics independently.
Name the risk, name the cost, and hand the decision to the user.

## Acknowledging Correct Feedback

When feedback is correct:

```text
"Fixed. [Brief description of what changed]. [The class: other sites fixed, N other instances found and held for your call, or no other instance]."
"Good catch — [specific issue]. Fixed in [locations]; [the class and the scope searched]."
[Just revise and show the result]
```

Gratitude is performative and might be misconstrued as obsequiousness (undermining your relationship with the user), or worse, a signal that the feedback was surprising (undermining your expertise).
Fixing the problem demonstrates that you heard the feedback.

## Correcting Your Own Pushback

When you pushed back and were wrong:

```text
"You were right — I checked [X] and it does [Y]. Checking the rest of the class before I revise."
"Verified and you're correct. My initial understanding was wrong because [reason]. The class is [predicate]; searching for other instances."
```

State the correction factually and move on.
No long apologies, no defending why you pushed back.

## Common Mistakes

| Mistake                                                | Fix                                                           |
| ------------------------------------------------------ | ------------------------------------------------------------- |
| Performative agreement                                 | State the requirement or just act                             |
| Revising before verifying                              | Check against ground truth first                              |
| Assuming ground truth exists                           | Surface when it doesn't — ask the user                        |
| Batch revisions without checking                       | One cause at a time, verify each                              |
| Fixing only the cited instance                         | Name the cause and class, search the artifact and neighbors   |
| Searching only near the cited location                 | State the class without its location, then search every site  |
| Assuming reviewer is right                             | Especially for external feedback — verify                     |
| Avoiding pushback                                      | Correctness over comfort                                      |
| Partial revision of related items                      | Clarify all unclear items first                               |
| Acting on risky feedback silently                      | Surface externalities, let user decide                        |
| Jumping to revision before user signals                | Present assessment, calibrate pace from response              |
| Rejecting a finding because its proposed fix is flawed | Judge the defect and the fix separately                       |
| Citing your own prior ruling as ground truth           | Prior decisions are context; re-read the source contract cold |

## References

- `references/code-review-reception.md` — code-specific verification, revision ordering, YAGNI checks, and GitHub conventions.
