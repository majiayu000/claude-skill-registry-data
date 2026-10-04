---
name: pr-description
description: Write or edit a GitHub pull request title and description in the concise, plain convention Charlie prefers. Use whenever creating, opening, or updating a PR body or title (gh pr create, gh pr edit), or when asked to write, fix, or shorten a PR description.
---

# PR descriptions

This is the convention Charlie prefers for his PR bodies and titles. It is his personal style, not a company standard. Apply it whenever you write or edit a PR, before you run `gh pr create` or `gh pr edit`.

## Shape

- Lead with one or two sentences that say what was broken and why. Give the problem and its cause, not just what you changed.
- Then add up to three bullets, and only if the change has distinct parts. Often you need none or one. Do not pad to three.
- Write each bullet as a plain full sentence. A bullet can start with the name of the file, test, or component it covers.
- For a trivial change, one line is enough.
- Note what you deliberately did not change when that helps the reader, e.g. "Existing saved filters still work as before."
- Describe only the main change. Do not mention incidental or unrelated fixes that happen to ride along in the diff, like a small build fix.
- Do not add an issue close line like `Closes #123.` at the end.
- Each bullet states its one main outcome in one or two sentences. Secondary behaviors that the diff shows on its own, like skip handling or a side effect on another feature, do not get sentences.
- Never enumerate field or file names the reviewer will see in the diff. Say what the change amounts to instead, e.g. "the classes now match the provider response", not the list of fields.
- Do not mention where test fixtures came from or how the change was tested. That is verification narration even when it sounds like a feature.
- A related sub-fix inside the same change does not get its own closing mention. The body sells the change, the diff holds the inventory.

Keep the whole body concise and easy to read. The body must not be longer than the diff it covers.

## Plain writing

Write the body the way a person writes. Run the `plain-writing` skill for the full rules. The ones that matter most in PRs:

- No dashes of any kind, including em dashes and number ranges. Use the word "to" for a range.
- No semicolon joining two clauses, and no colon used to set up a point. Use a colon only to introduce a list.
- Simple everyday words, complete sentences, no jargon.
- Name the data and its source directly. Replace `canonical` with the specific meaning, such as `the complete response from the service`.
- Do not invent a hyphenated phrase to sound compact.

## Never put in a PR body

- A verification or testing recap, or gate and command output.
- Code review or Codex narration.
- An implementation play by play.
- A What, Why, Scope, How to test template, or section headers on a small diff.
- A wall of text.

That belongs in the conversation or the commits, not the PR.

## Title

Use the `commit-style` skill for the pull request title.

This skill owns only the title and body text. The current request and repository delivery rules decide whether to create the pull request, whether it is ready or draft, and whether review is needed first.
