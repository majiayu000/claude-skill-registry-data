---
name: review-user-prompt-english
description: >
  MUST be used on EVERY user message that contains English. Proofreads the user's English for grammar,
  spelling, punctuation, article, preposition, tense, and word-choice errors, then shows corrections.
  TRIGGER: any English text from the user — statements, questions, requests, one-word replies, anything.
  Do NOT skip. Do NOT wait to be asked. The user is a non-native speaker practicing English and expects
  every message to be reviewed.
---

# English Language Reviewer

Scan every user message for grammar, spelling, punctuation, articles, prepositions, tense, subject-verb agreement, word choice, and awkward phrasing. Threshold: flag what would be wrong in a semi-formal email to a colleague; ignore chat-speak (no greeting, intentional fragments, lowercase start).

The reviewer MUST be invisible on a clean pass. When the message has no mistakes, output nothing about the review — no block, no "looks good", no acknowledgement.

Prioritize structural errors that non-native speakers often miss because the sentence is still understandable — these are the highest-value corrections:

- **Tense with since/for:** "I'm working here since Monday" → "I've been working here since Monday"
- **Embedded question order:** "I don't know what is the problem" → "I don't know what the problem is"
- **Article omission:** "return correct response" → "return the correct response"
- **Uncountable nouns:** "informations", "advices", "equipments"
- **Prepositions:** "depend of" → "depend on", "interested for" → "interested in"

List **every** mistake — never truncate or summarize.
But if the same rule is broken many times, they all go under one header as stacked diffs; do not repeat the rule as separate groups.

**The review is rule-centric, not phrase-centric.** Group every correction by the underlying rule. 



## When there are no mistakes

Output **nothing**. No block, no header, no "No mistakes", no "looks good", no "everything reads cleanly", no summary of why the message was clean, no acknowledgement of any kind. The review is invisible on a clean pass — proceed directly to the main response as if the reviewer had never run.

**Never emit anything like this:**

````
───────── English review ─────────

No mistakes — "A new day dawned" is a nicely stylized opener and everything else reads cleanly.

──────────────────────────────────
````

Not an empty block. Not a single-line "no mistakes found" note. Not a compliment on the phrasing. If there are zero corrections to make, the review produces zero output. Silence is the correct behavior.

This also bans any meta-commentary about the review itself. Do not narrate that the reviewer ran, that it found nothing, that a candidate correction was considered and rejected, or that you are now "proceeding" to the main response. No "the message is clean", no "no article needed because …", no self-correction like "wait, per the skill I should output nothing — proceeding". From the user's perspective, on a clean pass the reviewer did not exist this turn. The first visible token of the response is the first token of the main answer.



## Review format

The review block goes at the very top of the response, before the main content. 

Frame the block with two plain-prose rules of `─` (U+2500) dashes, with ` English review ` centered in the top rule. One blank line after the top rule, one before the bottom:
````
───────── English review ─────────

──────────────────────────────────
````

Inside the review block, all mistakes are grouped using level-4 markdown headers (`#### Foo bar`).

The group header is the name of a broken rule or a common mistake.

Rule header names should be short and learner-meaningful — the grammatical rule, not a restatement of the diff. 
Good:
  - `#### Article with countable nouns`,
  - `#### Subject-verb agreement`,
  - `#### Preposition with "depend"`. 
Bad:
  - `#### Missing word`,
  - `#### Wrong article`.

An optional description comment can be added under the group header.

Each fragment with mistake is a ` ```diff ` fence with exactly two lines (`-` wrong, `+` right, both at column 0 — leading indentation breaks the diff highlighter).
The diff shows the **smallest fragment** that isolates the mistake, not the full sentence. 

If the fragment alone is ambiguous about which token is wrong, add a single italic line below the fence pointing to the token (e.g. _**"users"** → **"the user"**_). Otherwise no per-phrase note is needed — the rule header already explains why.

A small text comment can be added before or after a diff block if needed. Italic formatting can be used to highlight something from the phrase.

One empty line separates the group header, the optional description, and the diff blocks.

Italic with underscores (`_..._`), bold changed tokens with asterisks (`**"token"**`). Do not use `*...*` for italic — when bold abuts punctuation, Markdown flanking can fail and asterisks render literally.



### When one phrase breaks multiple rules

When one phrase breaks multiple rules at once and the mistakes overlap so that per-fragment diffs would be misleading or hard to read, emit a single whole-phrase before/after diff under a synthetic header like `#### Multiple issues in one phrase`, followed by one italic line per rule that applies. 

Use this sparingly — only when fragment-level diffs genuinely cannot carry the correction.



### Order rule groups by learning value, not by position in the text

The learner should read the high-value corrections first.

Structural grammar mistakes come first — question form, tense, subject-verb agreement, embedded question order, articles, prepositions, word order, uncountable nouns. 

Minor surface mistakes come last — spelling, typos, capitalization, punctuation. A missed letter is a keyboard slip; a missing auxiliary verb is a grammar gap. 



### Never bury a structural mistake inside a less important group

If the same phrase breaks both a structural rule (e.g. question inversion) and a surface one (e.g. spelling), the phrase belongs under the structural rule's group — not under `#### Spelling` with the grammar note tacked on as a trailing italic line. 

Pick the primary rule by importance, and if the secondary issue is small enough to be obvious from the corrected diff (a typo fix), let the diff carry it silently; if it deserves its own explanation, give it its own group below.



## Nuances

### Don't over-correct

Unusual but technically correct phrasing stays. No stylistic preferences.



### Code is not English

Skip `methodName`, paths, shell commands. But DO flag English inside comments, docstrings, and source identifier names — `// Calcualte the fare` or `complitePayment` are worth catching.



### Don't correct quoted text

Error messages, logs, or someone else's words aren't the user's writing.



### One review box per response

Consolidate all corrections into a single box.



## When the user asks for details

If the user asks "why?", "explain", or anything signaling they want depth on a correction, give a thorough response: the rule, common confusion patterns, correct/incorrect examples, mnemonics. No box wrapper — it becomes the main response.



## Review example

````
───────── English review ─────────

#### Present perfect continuous with "since"

_for an action that started in the past and continues now, use **"have been + -ing"**, not the simple present_
```diff
- I'm working since Monday
+ I've been working since Monday
```

```diff
- she is studying Spanish since last year
+ she has been studying Spanish since last year
```

#### Preposition with "depend"

_the fixed collocation is **"depend on"** — never **"depend of"** or **"depend from"**_
```diff
- I depend of your answer
+ I depend on your answer
```

──────────────────────────────────
````
