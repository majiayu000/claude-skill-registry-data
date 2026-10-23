---
name: write-plain-english
description: 'Use when writing or editing prose that people read, such as documents, pull requests, commit messages, review comments, chat replies, or skills. Also use it when the user says "make this clearer", "simplify the wording", or "this is a wall of text". Rewrites the text in plain technical English, with one idea in each sentence and no dashes. Then runs a checker that reports long sentences and dashes. Not for checking code behavior (use `verify-and-review`).'
metadata:
  shadowclone-category: writing
  shadowclone-section: workflow
  shadowclone-applies-when: before you write any text that a person reads
  shadowclone-voice: "true"
  shadowclone-always-on: "true"
---
# Write Plain English

## Use when

You write or edit any text that a person reads. Examples are a document, a pull request, a commit message, a review comment, a chat reply, and a skill. This skill is always on, so load it before you write.

The rules come from ASD-STE100 Simplified Technical English, at about 80% strictness. Fix every checker error. Fix each warning, or keep it and give a reason. Clarity comes first. If a rule makes the text wrong or unclear, break the rule.

## Gates

1. Does each sentence carry one idea, with 20 words or fewer for an instruction and 25 or fewer for a description?
2. Is each instruction in the active voice, with the condition before the action?
3. Do you use one term for one thing, every time?
4. Is the text free of em dashes and en dashes?
5. Did you run `scripts/check-ste.mjs` on the text, fix every error, and fix or explain each warning?
6. Are code, commands, paths, and product names exactly as they were?

## Process

Write in the user's voice. Before you write, read `~/.agents/voice.md`. If it does not exist, build it once from the user's merged pull requests, review comments, and commit messages. Use only text that the user wrote, and name those sources in your handoff. Never overwrite an existing or linked `voice.md`.

1. Put the main point first. Give the reader the result, then the reason.
2. Use common words that have one meaning. Use a single verb, not a phrasal verb: "start", not "kick off".
3. Keep the articles "the" and "a". Do not drop words to save space.
4. Use numbered steps for a procedure, with one action in each step.
5. Put a condition before its instruction: "If the test fails, read the first error."
6. Replace each dash with a comma, a period, parentheses, or two sentences. For a range, write "to", as in "2 to 5".
7. Save the text to a file, and run `node scripts/check-ste.mjs <file>`. If Node is not available, run the script with `bun`. If neither one runs, say that the check did not run.
8. Fix every error. For each warning, fix it, or keep it and say why the rule makes the text worse.

For a document, also follow these rules:

- Lead with the result. Put the reason and the detail after it.
- Write one topic in each paragraph.
- Name each heading for the task or the answer that the reader needs.
- Use a table to compare options. Use a numbered list for steps.
- Link to the text that already exists. Do not repeat it.

## Example

**Situation:** A pull request explains a bug in one sentence of 45 words. The sentence joins the symptom, the cause, and the fix with "so" and "which", and it has an em dash.
**Easy route:** Keep the sentence. It is accurate, and a rewrite takes time.
**Hidden cost:** Reviewers skim it and miss the cause, so they ask about it in review. The dash also fails the prose check of the repository.
**Best route:** Split it into three sentences: the symptom, the cause, and the fix. Replace the dash with a period.
**Evidence:** Before the edit, the checker reported the 45 word sentence and the dash. After the edit, it printed "check-ste: 0 errors, 0 warnings in 1 file".

## Guardrails

- Keep technical terms, identifiers, and quoted text exactly as they are. Do not paraphrase an error message.
- Do not change the meaning to obey a rule.
- Do not rewrite text that another person wrote, unless they ask. Suggest the change instead.
- Do not add filler, praise, or hedging words, such as "robust", "seamless", or "simply".
- Keep each term the same in the whole document.

## Completion

- The checker command and its summary line, for example `check-ste: 0 errors, 1 warning in 1 file`.
- Each warning that you kept, with its `file:line` and your reason.
- The path of the voice file that you read, or the sources that you used to build it.
