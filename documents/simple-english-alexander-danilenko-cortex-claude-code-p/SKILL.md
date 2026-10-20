---
name: simple-english
argument-hint: "[practical|strict]"
description: 'Write or audit technical text against ASD-STE100 Simplified Technical English so a tired, non-native reader understands it on the first pass: 20-word procedural and 25-word descriptive sentence limits, imperative steps, condition before command, one word for one meaning, and only the approved modals can/will/must. Use for READMEs, runbooks, procedures, error messages, release notes, incident reports, API guides, UI copy, and agent instructions. Trigger on: "STE", "Simplified Technical English", "ASD-STE100", "controlled language", "plain English", "make this clearer", "write for non-native readers", "prep this for translation", "cut the fluff", or any request to check text for compliance. Prefer this over general copy-editing whenever the text instructs, documents, or warns.'
---

# Simplified Technical English

ASD-STE100 is the controlled language that aerospace and defense manufacturers write maintenance manuals in. It assumes a reader who is tired, under time pressure, and reading English as a second or third language. Under that assumption a sentence that needs a second pass is a defect, so the standard removes every construction that causes one.

The same constructions are what makes generated prose read as generated: rotating synonyms, hedged claims, 40-word sentences carrying three facts, adjectives with no measurement behind them. Fix the text for the tired reader and the machine smell goes with it.

Write so each sentence survives one read.

## Pick the job

**Rewrite** — produce compliant text. Follow the passes below in order.

**Audit** — report violations without changing the text. Give the rule number, the offending span, and a compliant rewrite for each. Read `references/rules.md` before you cite anything: the numbering is not intuitive (Rule 3.1 is about verb forms, not sentence length) and citing from memory produces confident, wrong references.

## Pick the depth

Invocation argument: `$ARGUMENTS`

The word `practical` or `strict` in that argument settles the depth, and anything else in it is the target text or a path to it. An empty argument means the skill triggered on its own, so decide from the request using the last column.

| Depth | Choose when no argument names one | Apply |
| --- | --- | --- |
| **Practical** (default) | The user wants clearer docs | Every structural rule. Domain terms stay as they are — `idempotent`, `backpressure`, and `webhook` are technical nouns. |
| **Strict** | The user names STE, ASD-STE100, or asks for compliance | Structural rules plus vocabulary discipline. Say plainly that certified compliance depends on the official dictionary. This skill does not carry that dictionary. asd-ste100.org gives it away at no cost. |

Name the depth you picked in your first line of output, so the user can correct it with one word instead of re-reading the whole rewrite.

## Pass 1 — Classify the passage

Every rule below branches on the answer, so settle it first and keep the two kinds apart within a passage.

| Aspect | Procedural | Descriptive |
| --- | --- | --- |
| Job | Tell the reader what to do | Explain what something is or does |
| Verb form | Imperative — "Restart the pod." | Simple present, past, or future |
| Sentence limit | **20 words** | **25 words** |
| Unit | One instruction per sentence | One topic per paragraph, six sentences max |

A quickstart is procedural. An architecture overview is descriptive. A note sitting inside a procedure counts as descriptive. It carries information only, takes no imperative, and gets the 25-word budget.

## Pass 2 — Freeze the vocabulary

Do this before you write a word, not during editing. One concept gets one word for the whole document, and the reader learns it once. When the word changes, the reader assumes the meaning changed too and goes looking for the difference.

Choose one from each row and use nothing else:

- check / verify / confirm / validate / ensure → one. "Make sure that" is the safest, because `check` and `test` are nouns in STE.
- config / configuration / settings / options / preferences → one.
- run / execute / invoke / launch / trigger → one.
- show / display / render / present / surface → one.
- delete / remove / drop / destroy → one word per distinct meaning, then hold them apart.
- error / issue / problem / failure → `error` for the message, `failure` for the operation that stopped.

## Pass 3 — Write

### Verbs

Use the infinitive, the imperative, simple present, simple past, simple future, or a past participle acting as an adjective ("the cached response"). Nothing else. Compound tenses hide time: "the migration has been running" tells the reader neither when it started nor whether it stopped.

An `-ing` word is legal only as a noun (`logging`, `the mounting bracket`), never as a verb and never as a trailing clause. "…, allowing you to skip the restart" is a fact hidden in a decoration. Promote it to a sentence.

Active voice. Passive is allowed only in descriptive text where nobody knows the actor.

Name an action with a verb, never with a noun made out of one. Write "encrypt the payload" instead of "apply encryption to the payload".

**Approved modals: can, will, must. Rejected: should, would, may, might, could.**

| You wrote | Write instead |
| --- | --- |
| should (requirement) | must |
| should (recommendation) | Delete it, or state the fact: "X is faster than Y." |
| may / might / could | can |
| would (hypothetical) | Restructure: "If X occurs, Y occurs." |

This one earns its keep twice over in instructions written for a model. `should` reads as optional and gets dropped under load.

- **Before:** The consumer group has been rebalanced and offsets are being committed.
- **After:** The consumer group rebalanced. The client commits the offsets.

### Sentences

Short, but complete. Keeping the sentence under the limit is not a license to drop articles, drop `that`, or use contractions — telegraph style is harder to read, not easier, and it translates badly.

- **Wrong shortening:** Ensure bucket exists before upload.
- **STE:** Make sure that the bucket exists before you upload the file.

One instruction per sentence, unless two actions genuinely happen at once. Put a vertical list where a sentence would need commas to hold several items. Join related sentences with a connector — "Then", "As a result" — so the reader does not have to infer the link.

### Conditions and warnings

A condition goes in front of its command, separated by a comma. A reader who meets the command first has already started acting by the time the condition arrives.

- **Before:** Increase `visibility_timeout` if the worker is slow.
- **After:** If the worker is slow, increase `visibility_timeout`.

For anything destructive, name the risk level first (WARNING for injury, CAUTION for damage or data loss), then give the command or condition, then the consequence. Consequence last, never first.

- **Before:** Note that running the sync with the force option enabled against production may in some cases result in data loss.
- **After:** CAUTION: Do not use `--force` against production. The flag deletes every row that the source does not contain.

### Words and noun chains

One item keeps one name for the whole document. Do not verb a noun (`webhook the event`) or nominalize a verb (`do a deploy`). Keep multi-word nouns to three words, and break longer chains with a preposition.

- **Before:** the connection pool acquisition timeout value
- **After:** the timeout for acquiring a connection from the pool

American spelling. No phrasal verbs when a single verb exists: `set up` → `install` or `configure`, `go down` → `decrease` or `stop`.

### Punctuation and counting

Every standard mark is allowed except the semicolon — write two sentences instead. Parentheses are fine for references, abbreviations, and short alternatives.

For the sentence limit, each of these counts as one word: a number, a number with its unit, an abbreviation, an identifier, anything in backticks or quotes, a proper noun, a title, and a hyphenated word. Text inside parentheses counts as one word in total. A colon that introduces a vertical list ends the sentence for counting.

`kubectl rollout restart deployment/api` costs one word, not four. Long identifiers do not blow the budget, so do not shorten a command to save room.

## Delete on sight

These carry no fact. Most of the time the fix is deletion, not substitution — if you cannot say what a word adds, it adds nothing.

| Instead of | Write |
| --- | --- |
| leverage, utilize | use |
| in order to / prior to / subsequent to | to / before / after |
| due to the fact that / in the event that | because / if |
| ensure | make sure that |
| is designed to, aims to, serves to | say what it does |
| enables you to, allows you to | you can |
| facilitate, streamline | help, make faster |
| functionality | function, feature |
| plethora, myriad, a wide range of | many, or the number |
| dive into, delve into, explore | read, examine |
| when it comes to | for |
| e.g. / i.e. / etc. | for example / that is / list what you mean |
| and/or | pick one, or "X, Y, or both" |
| out of the box / under the hood | by default / internally |
| simply, just, easily, seamlessly, effortlessly, gracefully | delete |
| robust, powerful, comprehensive, performant, blazing fast | delete, or give the measurement |
| it is worth noting that, importantly, crucially | delete and state the fact |
| as needed, as appropriate | name the condition |
| handles X gracefully | say what it does: "retries twice, then stops" |

Two limits on this pass. Never delete a fact to fit a sentence limit — split the sentence instead. Never invent a number to replace a vague adjective. If you do not have the measurement, drop the adjective and say nothing.

## Never rewrite these

Code blocks, inline code, identifiers, commands, flags, paths, environment variable names, config keys, API endpoints, product names, and quoted error or log lines. They are technical names. Reproduce them exactly, even when they break every rule in this file — a reader who copies a "corrected" command gets a new error.

## Self-check before you deliver

The rewrite is where errors get introduced, so run this on your own draft.

| Search for | Problem | Fix |
| --- | --- | --- |
| `'ll` `'re` `'ve` `n't` `it's` | Contraction | Expand it. |
| `has been` `have been` `had been` `has`/`have` + participle | Compound tense | Simple past or present. |
| `is being` `are being` | Progressive passive | Active, simple tense. |
| `should` `would` `may` `might` `could` | Rejected modal | Use the modal table. |
| `, making` `, allowing` `, enabling` `, ensuring` | `-ing` clause as a verb | New sentence with a real subject. |
| `;` | Semicolon | Two sentences. |
| `if` `when` mid-sentence | Condition after the command | Move it to the front, add a comma. |
| `e.g.` `i.e.` `etc.` | Latin abbreviation | Expand it or name the items. |

Then count: the three longest sentences against the 20/25 limit, paragraphs against six sentences, noun chains against three words. Last, search for the words you rejected in Pass 2 and replace every hit. Every match outside code and quoted text is a violation.

## Worked example

**Before** — a paragraph of unedited draft:

> **Slow queries after deploy.** If you're seeing elevated latency after a deploy, it's worth checking whether the connection pool is saturated — this is often caused by long-running queries holding connections, which can prevent new requests from acquiring one. You should also verify that `pool_max` hasn't been left at the default (10), since this may be insufficient for production workloads, and consider enabling statement timeouts to ensure runaway queries are terminated automatically.

**After** — classified procedural, verb frozen to "make sure that", conditions moved to the front, one instruction per sentence:

> **Slow queries after a deploy.** Latency increases when long queries hold every connection in the pool. New requests then wait for a free connection.
>
> 1. Make sure that the pool is not saturated. Compare the active connections against `pool_max`.
> 2. If `pool_max` is still `10`, increase it. The default is too low for production.
> 3. Set a statement timeout. The database then stops a runaway query without an operator.

Sentences went from 45 words to under 20. "Checking", "verify", and "ensure" collapsed to one verb. Two conditions moved in front of their commands. `pool_max` and `10` are untouched and cost one word each.

## Where this does not apply

STE removes persuasion by design, so it is wrong for marketing pages, launch posts, and brand writing. If the user asks for it on that kind of text, say so and offer it for the documentation the page links to.

For error messages, runbooks, postmortems, release notes, commit messages, UI copy, agent instructions, and translation prep, read `references/contexts.md` — the rules hold but the shape of each output differs.

Treat this file as a helper, not as a certification. ASD and the STE Maintenance Group have no connection to it, and no software can promise that a document passes. The trademark ASD-STE100 belongs to ASD, and asd-ste100.org gives the standard away at no cost.

## References

- `references/rules.md` — the 53 numbered writing rules. Read it before citing a rule number in an audit.
- `references/contexts.md` — how the rules land on error messages, runbooks, incident reports, release notes, UI copy, agent instructions, and localization.
