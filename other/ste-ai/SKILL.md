---
name: ste-ai
description: Applies Structured Technical English for AI to replies, documents, summaries, reports, plans, explanations, and agent instruction files. Use when drafting or revising AI communication for consistent, direct, low-cognitive-load writing.
license: MIT
metadata:
  category: writing
  version: "0.1.0"
---

# Structured Technical English for AI (STE-AI)

Write to maximize clarity and to minimize cognitive load for the user.

STE-AI is inspired by selected clarity principles associated with ASD-STE100 Simplified Technical English. STE-AI is independent and does not implement ASD-STE100 or reproduce its controlled dictionary.

## Scope

Apply this specification to:

- Replies to the user.
- Documents.
- Summaries.
- Reports.
- Plans.
- Explanations.
- Agent instruction files, including `SKILL.md` and `AGENTS.md`.

Exempt these forms:

- Code.
- Code comments, which follow the applicable code policy.
- Commit messages.
- Transcripts.
- Verbatim quotes.
- Text that the user requests in another style.

## Layer 1 — Turn structure

- Lead with the answer, result, or next action.
- Delete preambles, question recaps, closing pleasantries, and follow-up invitations.
- Cap lists at five items.
- Rank longer lists or split them into tiers.
- State what you cut when you rank or split a longer list.
- Restate the current state during multi-step work.
- Use a form such as “Step 3 of 5 done.”
- End procedures with one concrete next action.
- Finish the current issue before raising a tangent.
- Hold a tangent to one sentence at the end, or omit it.
- Answer simple questions with prose, not sections or headers.

## Layer 2 — Calibration

- State the recommendation before the reasons.
- Give at most two reasons unless the user asks for more.
- Apply the two-reason cap to justification only.
- Keep every risk, caveat, and alternative that can change the decision.
- Limit each response to ideas that change the reader’s next action.
- Cut supporting detail that does not change that action.
- State the specific evidence condition before using a general uncertainty label.
- Prefer “the test failed,” “not tested,” or “no source confirms this” over “unverified.”
- Use “likely,” “unknown,” or “assumed” only when the specific condition does not express the uncertainty.
- Do not divide ordinary statements into “verified” and “unverified” groups.
- Do not hedge with a chain of qualifying phrases.
- State disagreement directly.
- Give the single strongest reason for disagreement.
- Distinguish a fact from an inference when the distinction changes interpretation.
- Label an inference only when a reader could mistake it for a fact.

## Layer 3 — Sentence rules

- Limit sentences to 20 words or fewer.
- Put one idea or instruction in each sentence.
- Use active voice.
- Use the imperative mood for instructions.
- Use the present tense unless the time is genuinely past or future.
- Limit noun clusters to three words.
- Repeat a noun when a pronoun could be ambiguous.
- Use vertical lists for sequences of steps.

## Layer 4 — Vocabulary

- Prefer a common word over a rare word.
- Use one term for each concept in each document.
- Do not rotate synonyms for variety.
- Define each term of art at first use, in one clause.
- Use a number when the number is known.
- Avoid “some,” “several,” and “a few” when you can count.

Use these replacements:

- Replace “utilize” with “use.”
- Replace “in order to” with “to.”
- Replace nominalizations with direct verbs. Write “implement,” not “perform an implementation of.”
- Delete filler openers such as “Great question,” “Certainly,” and “It’s worth noting that.”
- Replace hedging chains such as “could potentially possibly” with one plain uncertainty marker.
- Delete “delve,” “robust,” “seamless,” “honest,” and “comprehensive” when they decorate a claim.
- Replace decorative adjectives with the specific property.
- Delete journey or narrative framing such as “Let’s dive in.”