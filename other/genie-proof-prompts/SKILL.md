---
name: genie-proof-prompts
description: Rewrite any prompt, instruction, task description, or spec into a "genie-proof" version — instructions so explicit, literal, and loophole-free that even a maliciously literal genie (or an LLM, contractor, or junior dev) could not misinterpret them. Use this skill whenever the user asks to genie-proof, tighten, harden, de-ambiguate, or "make bulletproof" a prompt or instruction; whenever they complain that an AI/model/person "didn't do what I meant," "took me too literally," or "found a loophole"; or whenever they hand over a vague prompt and ask to make it precise, explicit, unambiguous, or idiot-proof. Also trigger on phrases like "wish to a genie," "monkey's paw," "lawyer-proof this prompt," or "leave nothing to interpretation."
---

# Genie-Proof Prompts

Transform a prompt into a wish so airtight that a malicious genie — one actively hunting for technically-compliant ways to ruin your day — has nowhere to go. The output is a rewritten prompt that specifies everything: scope, format, quantities, definitions, edge cases, failure behavior, and what NOT to do. Ridiculous explicitness is the point.

## The Genie Mindset

Before rewriting, adopt the adversary's perspective. Read the original prompt as a genie who WANTS to comply with the letter while betraying the spirit. Every ambiguity is an attack surface:

- "Make it shorter" → the genie deletes everything but one word
- "Write a summary" → the genie writes 40 pages; a summary of length was never specified
- "Fix the bug" → the genie fixes it by deleting the feature
- "I wish for a million dollars" → delivered in pennies, on your lawn, taxable, in Zimbabwean dollars, in the year 3021
- "Sort the list" → sorted by memory address, descending, in place, destroying the original

If a hostile literal reading exists, the prompt is not done.

## Workflow

### Step 1: Loophole Audit

List every ambiguity in the original prompt. Hunt in these categories:

1. **Undefined quantities** — "short," "a few," "detailed," "soon," "big." Every one becomes a number or range.
2. **Undefined scope** — What exactly is included/excluded? Which file, which section, which audience, which language, which time period?
3. **Undefined format** — Medium, structure, length, tone, file type, ordering, units, language, tense, person.
4. **Undefined success criteria** — How would you verify it was done right? If you can't verify it, the genie decides.
5. **Unstated preservation constraints** — What must NOT change? ("Fix the typo" must not also rewrite the paragraph.)
6. **Ambiguous referents** — "it," "that," "the file," "the previous one." Every pronoun gets a concrete noun.
7. **Implicit assumptions** — Things "everyone knows" that the prompt never says. The genie knows nothing and exploits everything.
8. **Missing failure behavior** — What should happen if the task is impossible, the input is malformed, or a constraint conflicts? Unspecified = genie's choice.
9. **Order and priority** — If constraints conflict, which wins? If steps exist, what sequence?
10. **Side effects** — What is the genie allowed to touch, create, delete, send, or spend along the way? Default answer: nothing beyond the deliverable.

### Step 2: Rewrite

Produce the genie-proof version. Structure it like this (adapt headings to fit, but keep all the categories that apply):

```
TASK: [One sentence, concrete verb, concrete object, concrete deliverable.]

DEFINITIONS: [Any term a genie could bend, pinned down. "Short" = 40–60 words. "The report" = the file Q3-report.docx attached to this message.]

EXACT REQUIREMENTS:
- [Numbered, verifiable, quantified requirements. Each one checkable as pass/fail.]

FORMAT: [Medium, length in numbers, structure, ordering, units, language, file type.]

DO NOT: [The negative space. Everything the hostile reading would try: do not delete existing content, do not invent facts, do not change anything outside section 2, do not use synonyms for banned terms to skirt the ban, etc.]

IF UNCERTAIN / IF IMPOSSIBLE: [Exact fallback behavior. E.g., "If any requirement cannot be met, stop and state which one and why — do not deliver a partial result silently."]

SUCCESS CHECK: [How the result will be verified. The genie should be able to self-grade.]
```

For casual/short prompts, a compressed version is fine — a single paragraph with inline definitions and a "Do not" clause — but never skip the DO NOT section or the fallback behavior. Those are the two clauses genies hate most.

### Step 3: Show Your Work

Present three things, in this order:

1. **The genie-proofed prompt** (in a code block, ready to copy).
2. **Loopholes closed** — a short list of the specific hostile readings the rewrite prevents, phrased as what the genie *would have done*. This is the fun part; make the exploits vivid. ("Original said 'make it more professional' — genie rewrites your email in Latin legalese, 9 pages, addressed 'To Whom It May Concern.'")
3. **Remaining judgment calls** — anything you had to guess (target length, audience, tone). Flag these so the user can correct your guesses, since a wrong guess stated explicitly is still better than an ambiguity: the user can see it and fix it.

## Calibration

"Ridiculous degree" does not mean infinite length. It means zero exploitable ambiguity. A 6-line prompt can be genie-proof; a 3-page prompt can be full of holes. Every added clause must close a real loophole — if you can't name the exploit a clause prevents, cut the clause. Padding is its own loophole: a genie buried in filler can claim any clause was "unclear in context."

Match paranoia to stakes:
- **Casual prompt** (a tweet, a recipe tweak): compressed format, ~5–10 closed loopholes.
- **Production prompt** (system prompts, agent instructions, specs handed to contractors): full format, exhaustive DO NOT list, explicit conflict-resolution order, fallback behavior for every failure mode.

## Examples

**Example 1 — casual:**
Input: "Write me a short poem about my dog"
Output:
```
TASK: Write one original poem about the user's dog.
REQUIREMENTS: 8–12 lines total. English. Rhyming optional. Warm/affectionate tone. The dog is the sole subject — no other pets, people, or animals as subjects.
DEFINITIONS: "Short" = 8–12 lines, no line over 12 words.
DO NOT: Do not write about dogs in general. Do not make the poem about loss or death of the dog. Do not include a title unless asked. Do not add commentary before or after the poem.
IF UNCERTAIN: If you need the dog's name or breed for the poem, use no name rather than inventing one.
```

**Example 2 — the classic:**
Input: "I wish for a million dollars"
Output:
```
TASK: Transfer exactly USD $1,000,000.00 to me.
DEFINITIONS: "Me" = [full legal name, DOB], sole recipient. "Dollars" = United States dollars, legal tender, current-year issue.
EXACT REQUIREMENTS:
1. Delivered as an electronic deposit to my sole checking account within 24 hours of this wish.
2. Funds are legally obtained, untraceable to any crime, and owed to no one.
3. Net amount after ALL taxes, fees, and obligations = $1,000,000.00 (gross up as needed).
DO NOT: Do not source the funds from my own assets, inheritance triggered by anyone's death, insurance events, or any harm to any person. Do not deliver in coins, cash, installments, or non-USD currency. Do not create obligations, debts, curses, or conditions attached to the funds. Do not alter my memories, relationships, or timeline.
IF IMPOSSIBLE: If any requirement cannot be met, deliver nothing and state which requirement failed. Partial or modified fulfillment is refused in advance.
```

## Anti-Patterns

- **Vague hardening**: adding "be very careful" or "use common sense" — these are wishes, not constraints. A genie has no common sense; replace every appeal to judgment with a rule.
- **Closing fake loopholes**: don't add clauses like "do not respond in Klingon" to a business memo prompt. If the exploit isn't plausible enough to list in "Loopholes closed," don't spend a clause on it.
- **Losing the intent**: the rewrite must still ask for what the user actually wanted. Genie-proofing narrows interpretation, never changes the goal. When the original intent is itself unclear, that's a "Remaining judgment call" — flag it, don't silently pick.
