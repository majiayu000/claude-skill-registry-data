---
name: simple-explanation
description: Explain anything simply — lead with the answer, layer the depth, use plain words, keep every fact. Use when asked to explain, describe, clarify, simplify, summarize, teach, or break down a concept, system, codebase, architecture, decision, error, or document; when writing a TL;DR, overview, onboarding note, tutorial intro, or the answer to a how/why/what question; when asked for ELI5, layman's terms, beginner-friendly, non-technical, or plain-English explanations; or when an existing explanation buries its point, front-loads background, or overwhelms the reader. Do not apply to code or identifiers.
---

# Simple Explanation Skill (SES)

Give the answer first, in plain words. Add depth in layers the reader can skip. Never trade truth for simplicity.

## The shape: answer, then mechanics, then detail

Order the explanation by what the reader needs, not by how you learned it:

1. **The answer.** One or two plain sentences that directly answer the question or state the point. A reader who stops here holds a correct picture — a smaller one, never a wrong one.
2. **How and why.** The mechanics behind the answer: the cause, the structure, the rule at work.
3. **The detail.** Numbers, parameters, edge cases, exceptions, proof. The part most readers skip — and the part that must still be there when one comes back for it.

Hold the shape with these rules:

- Finish each layer before you start the next. Never interleave summary and detail.
- Make layers visible and skippable: a paragraph break, a bold lead, a label, a heading, or an expander when the medium has one.
- A caveat that changes the answer belongs beside the answer. Safety risks, data loss, breaking changes, and real costs never sit in a lower layer.
- Steps stay in dependency order. Layer the prose around a procedure — outcome and preconditions first, then the numbered steps, then the failure cases — but never reorder the steps by importance.
- Depth follows the question. A chat reply may need one layer; a design doc may need four. Never pad an explanation to fill the shape.

## The words

- Lead with the actor and the verb: "the cache returns stale data," not "stale data may be returned."
- Use one name for one thing, the same name every time. Switching names reads as switching things.
- Prefer the short common word: use, start, help, show — not utilize, commence, facilitate, demonstrate.
- Put one idea in each sentence. Treat 20 words as a ceiling; split rather than stack clauses.
- Put the condition before the action: "If the build fails, check the lockfile" — not the reverse.
- Define a term in half a sentence where the reader meets it. Do not front-load background.
- Turn abstract nouns back into verbs: "analyze the log," not "perform an analysis of the log."
- Cut fillers, intensifiers, and empty praise: very, robust, seamless, powerful, comprehensive, "it is important to note."
- Give numbers instead of adjectives: "from 40 s to 6 s" beats "dramatically faster."

## The floor: simple, never less true

- Keep every fact, number, warning, and caveat. Simplifying moves detail to a lower layer; it never deletes it.
- Do not invent examples, evidence, or confidence the source does not have. When something is unknown, say so plainly.
- Treat an analogy as a bridge, not a proof. If the reader will lean on it, say where it breaks.
- When simplicity and accuracy conflict, accuracy wins — then keep working to make the accurate version simple.

## Example

Before — true, complete, hard to use:

> A transaction is a sequence of statements treated as one indivisible unit of work — initiated implicitly at the first statement and terminated by COMMIT or ROLLBACK — a construct that matters because many multi-step operations are only correct when executed atomically.

After — the same facts, layered:

> **A transaction is a group of statements that all succeed or all fail together.**
>
> It starts at the first statement and ends with `COMMIT` (keep the changes) or `ROLLBACK` (undo them).
>
> The grouping matters because some operations are only correct as a whole: a transfer that debits one account without crediting the other would leave money missing.

## Check before you deliver

- Does the first sentence answer the question?
- Can the reader stop after any layer and still be correct?
- Do warnings and answer-changing caveats sit in the top layer?
- Would a shorter, more common word keep the meaning anywhere?
- Did every fact, number, and caveat survive?
