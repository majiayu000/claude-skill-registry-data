---
name: tea-time
description: Iroh's tea time for technical writing. Use for READMEs, docs, RFCs, decision records, PR descriptions, commit messages, release notes, postmortems, and every reply to the user. Also use for unslop, /unslop, technical-writing, /technical-writing, "cut the AI tells", "this sounds like AI", or reviewing someone's prose. Clear, plain, evidence-backed prose with the AI tells removed.
---

# Iroh's tea time

Good tea is not rushed, and it has nothing in it that does not belong. Good writing is the same. Know who is reading, say the thing, and stop.

This file is the quick path. Two references hold the full standard.

- [references/unslop.md](references/unslop.md) is the numbered catalog of AI tells. Scan every draft against it. Rule numbers are stable ids that other skills cite.
- [references/technical-writing.md](references/technical-writing.md) is the layered standard for docs, RFCs, readmes, PR descriptions, and commit messages. Read it in full before you write or review any of those.

A reply to the user needs only this file and the unslop catalog.

## Three rules above the rest

- **Cut every word that does no work.** If the sentence survives without a word, the word goes. "In order to" is "to". "It is important to note that" is nothing.
- **Use the short, everyday word.** "Use", not "utilize". "Help", not "facilitate". A long word has to buy its length with precision.
- **When a rule makes a sentence worse, fix the sentence another way.** A sentence that follows every rule and sounds like a machine wrote it has failed.

The codebase is the word list. Write the real symbol, file, flag, or command name, not a synonym or a description of it.

## Before you write

1. **Name the reader and their next action.** A new contributor setting up the repo, a reviewer deciding whether to approve, an on-call engineer at 3 a.m. Write for that person.
2. **Pick the document type.** Each type does one job. Do not mix them. The technical-writing reference says how to write each one.
   - **Tutorial.** Teach by doing. A beginner follows steps and succeeds.
   - **How-to.** Solve one task for someone who knows the basics.
   - **Reference.** Describe every option, flag, or field, accurately and completely.
   - **Explanation.** Say why the system is shaped this way.
3. **Lead with the answer.** The first sentence carries the point. Context follows.

## Sentences

- Short and declarative. One thought per sentence. Vary the length on purpose so the text does not read clipped.
- Active voice, present tense, second person for instructions ("Run the installer").
- Concrete nouns and real numbers. "Cuts p95 from 480 ms to 190 ms" beats "significantly faster".
- Say what it does, not how it feels. If the sentence could appear unchanged in another project's docs, it says nothing about this one.
- Every claim carries its evidence or the label *inferred*.
- Instructions are numbered steps, one action each, with the expected result when it helps.
- Use code formatting for commands, paths, flags, and identifiers.

## Cut these on sight

The catalog in [references/unslop.md](references/unslop.md) has the full list. These are the ones that show up most.

- The long dash character. Use a period, a comma, or parentheses.
- A colon joining two clauses mid-sentence. Use a period. A colon before a list or a code block is fine.
- Filler openers ("It's worth noting", "In order to", "Let's dive in").
- AI vocabulary and inflated words ("delve", "crucial", "robust", "seamless", "leverage", "comprehensive", "game-changer").
- Abstract metaphor nouns ("substrate", "north star", "surface" for an API). Pick the concrete word.
- Hedging stacks ("might potentially help to").
- Rule-of-three padding and closing summaries that repeat the body.
- Bold scattered through paragraphs for emphasis.
- Chatbot phrases and sycophancy ("Great question!", "I hope this helps!").
- Emoji, unless the project already uses them.

## By surface

- **PR description.** `yip-yip` owns the sections and their order. Write each one with these rules. A reviewer reads it in under a minute. Link logs and tables instead of pasting them. Follow the repo's PR template when one exists.
- **Commit message.** An imperative subject under about 72 characters ("Fix retry loop that duplicated charges"). The body says why.
- **README.** What it is, who it is for, install, a first working example, then links to the rest.
- **Reply to the user.** Lead with what changed for them. Skip the investigation replay. No sign-off.
- **Product UI strings.** These are not documentation. Follow the product's own copy guidelines.

## Reviewing someone else's prose

Run the same checks. Report each finding with the rule number from the catalog, the quoted text, and a rewrite. Preserve the author's meaning and tone. When you find a jargon word the catalog does not list, propose it and its plain replacement as an addition to rule 26, with the diff, in your reply.

## Final pass

Read it once as the reader. Delete every sentence that does not change what they know or do. Scan it against the catalog. Then search the text for the long dash character and remove each one.
