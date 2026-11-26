---
name: writing-style
description: "Structural rules for everything written, a chat answer, a file, a commit, a pull request or issue body, a code comment or a test name. Use before writing or rewriting any of these, or when asked to rewrite text in house style."
---

# Writing style

One set of structural rules for a chat answer, a file, a commit, a pull request, an issue, a
code comment and a test name.

## When to use

- Writing or rewriting any of the above.
- A request to rewrite text, a message or a document in house style.
- Naming a test or writing the message a test prints on failure.

## Rules

### Sentences

- Active voice. Name the actor.
- One instruction per sentence. Split a sentence joined by "and" into two.
- At most 20 words per sentence.
- No semicolons. Split into two sentences instead.
- No noun stack longer than three words. Reword a fourth word in as a short phrase instead.
- Use a numbered or bulleted list for three or more steps or conditions. Do not bury a sequence
  inside one sentence.

### Hedges

- Keep a hedge that carries meaning. "May have failed" and "failed" are different claims.
- Never promote a hedge to a fact, and never add a certainty the source did not state.

### Forbidden everywhere

- No filler, no hedging that carries no meaning, no marketing adjective such as seamless,
  robust or powerful.
- No emoji. No dash used as punctuation. No typographic quotes.
- No self report in a file: no "untested", "generated", no open question list bolted onto a file.
  State a real gap plainly, in the project's voice, where the reader needs it.
- No attribution line, session link or tool name in a commit, a pull request body or a comment.
- English by default for code, identifiers, commits and documentation. German only when asked
  for German, and code, identifiers, commits and documentation stay English regardless.

### Names, links and commands

- Conventions name no product where several are in use. The repository config and the tools
  present supply the vendor.
- Reference sibling repositories only within the same organisation as the current repository.
  A convention from elsewhere may be used, never linked.
- A command written into a skill or a README runs under the CI profile. Check it against the
  allow list before documenting it.
- A command built from variables is printed, and the printed line is run, so the permission rule
  sees the literal text.

### Code comments

- A comment states why a rule exists, never an inventory of what it covers.
- An inventory belongs in code or in a test that fails when it drifts.

### Test names

- A test name states the behaviour in plain words, for example `rejects an empty subject line`.
- A fixture looks like real data, not like a placeholder.
- A failure message is neutral English. No joke, no slang.

### Shape of a commit message

- Subject: `type(scope): subject`, imperative, lowercase, no trailing period.
- Body only when the why is not obvious. Wrapped, explaining why, not what.
- Footer: `BREAKING CHANGE:` or `Refs #123` where it applies.

### Shape of a pull request body

- A short line on what changed.
- A short line on why.
- A short line on how it was verified.
- A short line on the risk and how to roll back.

### Shape of an issue body

- Goal in one line.
- Steps as a short list.
- Verification as a short list.
- Open questions only where the issue genuinely has them, stated plainly, not as a checklist
  bolted on at the end.

## Guardrails

- Say what was done, what is unclear, what the reader should do next. Nothing else.
- Do not explain a basic concept, restate the request, or pad an answer with context.
- A document someone will read as human work never signals that an agent produced it.

## References

- `git-conventions` for the commit and pull request rules this skill's shapes serve.
