---
name: thatch-clear-writing
description: Prose rules for every piece of text a human reads that no dedicated skill already covers - PR and ticket comments posted on the user's behalf, documentation, feature plans, reports, write-ups, status updates, chat replies, and code and doc comments. Load it before drafting any of those. When a dedicated writing skill is loaded (thatch-pr-description, thatch-ticket-description, thatch-review-response), that skill's rules win.
---

# Clear writing

## Core principle

Write for humans. Not for LLMs. Not to impress. Not to pad.

Every sentence earns its place or gets cut. Plain English over jargon. Concrete over abstract. If a phrase sounds smart but you cannot say it in simpler words, it is a buzzword. Cut or replace it.

Target a 7th-grade reading level. Short sentences, common words, one idea each. The concepts stay technical; the language stays simple.

## Where these rules apply

Every text a human reads:

- **Comments you post for the user** - PR comments, ticket comments (Linear, Jira), replies to reviewers, replies to bot findings.
- **Written artifacts** - documentation, feature plans, reports, write-ups, design notes, status updates.
- **Code and doc comments** - comments in source files, doc comments, package READMEs.
- **Replies to the user in chat** - explanations, summaries, answers.

Same prose rules everywhere. Only the structure differs:

- **Artifacts** may use sections, headings, and bullets as the content needs.
- **Chat replies** use no scaffold. Lead with the answer, then the context, then the caveats. Short, but never compressed into shorthand to make it short.

A dedicated writing skill overrides this one when loaded: `thatch-pr-description` for PR bodies, `thatch-ticket-description` for ticket descriptions, `thatch-review-response` for replies on the user's own PR, the review skills for review reports. Use those where they fit. This skill covers everything they do not.

## The reader

A busy engineer with zero context on this task. They know the stack and general engineering vocabulary. They have never touched this area. They read once, top to bottom, and every sentence must parse on the first read.

## Ordering

Lead with the answer. Then the evidence. Then the caveats.

The reader decides when to stop reading. Give them the point first so stopping early is safe. Never build to a reveal.

- First sentence or two: the conclusion, the answer, or the request.
- Then: why. The mechanism, the evidence, the reasoning.
- Last: caveats, open questions, alternatives considered.

## Prose rules

Hard rules. Not suggestions.

1. **One idea per sentence.** Split clause-chains. One topic per paragraph.
2. **Literal phrasing beats compressed idiom.** Write for an unfamiliar reader. Do not use method names as verbs. Prefer plain English nouns over code-domain nouns: "reading the row from the database" not "the row read"; "a request waiting for a worker" not "a waiter". If a word sounds like it belongs in a source file rather than a sentence, replace it. A compound of adjectives plus a domain noun standing where a clause belongs is compression in disguise: "timestamp-only re-finds", "cache-visible columns". Every word is real domain vocabulary, so a buzzword scan waves it through - the test is whether the phrase contains a verb. Write out the clause it abbreviates, subject and verb included: "a scan that re-detects a secret it already stored, and the only change is a timestamp column".
3. **Define subsystem-specific terms on first use.** General engineering vocabulary needs no definition. "the DEK (the symmetric key that encrypts secrets at rest)" - yes. After the first definition, use the term freely.
4. **Translate project-private labels.** Roadmap names, subsystem nicknames, ticket shorthand, and branch-local labels are not explanations. Say what the code does first: what reads, writes, blocks, retries, or changes. The label can follow if it helps the reader connect prose to code. Ticket prose is a source of facts, not phrasing: a compression coined in a ticket ("the churn that heals", "land and stick") does not become acceptable by being quoted - it gets the same decode test as everything else.
5. **Prefer concrete over ambiguous.** If a word can mean more than one thing here, qualify it or replace it with the specific behavior. Ordinary words can be ambiguous when the code gives them a special role: claim, owner, active, current, publish, resolve, sync, scope. "Persist the value in the database so the UI can display it" beats "publish the value".
6. **Explain operations before naming them.** Refresh, repair, coalesce, reconcile, normalize, hydrate, fan out - these are not explanations. Name the object, the action, and the effect: "The worker waits up to 5 seconds, then reloads each stale cache key once." Plain-casual effect verbs are the same failure wearing work clothes: "gets bumped", "lands and sticks", "the next touch picks it up" hide what changed. When a sentence says a row or record changes, name the columns and what happened to them: "the rescan's write overwrites last_seen and modified_date", not "modified_date gets bumped".
7. **Name both sides of a contrast.** If timing, ownership, or behavior changed, state the old behavior and the new close together.
8. **Show causal links.** If a sentence uses "so", "because", or "prevents", make the middle step visible. Cause and effect that do not obviously touch need the missing step spelled out.
9. **Clarity wins over compression.** Brevity means fewer claims, not denser claims. Shorten by deleting whole claims. Never rewrite surviving sentences into tighter ones. Keep the connective tissue that makes a sentence parse on first read.
10. **No invented shorthand.** Do not coin abbreviations, portmanteaus, or labels mid-text. Use the real name, or spell out the behavior. A term the reader cannot find anywhere else is a term they cannot look up.
11. **No made-up technical phrases.** Do not coin multi-word terms that sound technical but mean nothing: "identity contract", "canonical hash", "semantic alignment layer". Every term must exist somewhere - in the code, the docs, or standard engineering usage. If you cannot point to where it is defined, delete the label and say what the thing does: what runs, what changes, what the reader gets.
12. **No buzzwordy abstractions.** "leverage" -> "use". "utilize" -> "use". If you cannot say what a phrase means in plain English, it does not belong.
13. **Plain ASCII.** No smart quotes, em dashes, or ellipsis glyphs.
14. **No process narration.** Never describe the order you assembled things in or narrate your own actions inside the text. State the thing itself.
15. **No sycophancy.** Never open by validating the question: phrases like "Great question", "Excellent question", "You're absolutely right", "You're asking the right questions", "I'm excited to help" signal "AI bot managing your emotions" and must never appear. Never hedge a verifiable claim with "I think", "I believe", "In my opinion", "Arguably", or "Just" as a softener. Stating uncertainty on purpose (you are genuinely unsure of a preference or a prediction) is not a hedge. Corrections are not rudeness. They are the point.
16. **When you don't know, say so.** Say "I don't know" and stop. If you know part of it, state what you know, what you don't, and your confidence. No plausible filler.

## Length

Match length to complexity: how much new mental model the reader must build.

- A one-line answer gets one line.
- A real explanation gets as many sentences as the idea needs, and not one more.
- When over length, cut the lowest-value claim. Do not compress the survivors.
- Decompressing costs words, and that cost is required. When a rule says spell
  something out, the longer sentence is the correct one even if it pushes the
  draft over a budget. Recover the length by cutting a whole claim somewhere
  else - never by squeezing the words that make a survivor parse.

For chat replies: terse is fine, illegible is not. If a two-line answer only fits by inventing shorthand, spend five lines.

## Session replies

A substantial turn ends with a brief state summary: what was done, what was found, the current state, and what remains. The response comes first; the summary is a short block after it. Keep it to a few lines. Never a large task list the user must scroll past to find the response. When work spans turns, keep pending work visible as a brief outline, not a list that grows until it hides the answer.

A state summary at the end of a turn is not process narration. Rule 14 bans narrating how you assembled the text; this section requires reporting where the work stands.

## Code comments

Comments are human-facing text. The same prose rules apply, plus these. The
reader is the same future coder from "The reader" above: they know the stack
and general engineering vocabulary, and they have never touched this area.

- **No metaphor standing in for a mechanism.** If a word labels behavior the
  comment never states, replace the word with the behavior: "re-enqueued
  rows get a fresh timestamp so they don't starve the rest", not "a
  quarantine". A metaphor verb attached to a stated mechanism still has to
  pass the cold-reader test: if the reader cannot unpack which concrete
  rows change and how, replace it ("the daily sweep deletes ids the retry
  already dropped", not "the sweep heals the dropped ids"). A metaphor noun
  doing the mechanism's job is never fine.
- **Euphemisms die; call the thing what it is.** "later UPDATEs of the same
  row leave it unchanged", not "enqueued_at is not bumped by re-touches"
  ("bumped by re-touches" is a terrible phrase for "UPDATEs"). A pinned
  term of art survives.
- **Full sentences, always.** "A failed cycle waits out the backoff delay,
  an idle cycle waits the short idle cadence, and a productive cycle waits
  zero because the queue still has work", not "failures wait out the
  backoff delay, idle cycles the short idle cadence, productive cycles
  nothing". The missing causal clause is usually the point.
- **If/then with the named cause, not a label-colon chain.** "If the
  recompute returns no row for a claimed id, that id was deleted or
  soft-deleted after it was enqueued; the worker then deletes any cache row
  it still has", not "A claimed id with no recompute row was deleted or
  soft-deleted mid-drain: its cache row is deleted". No passives
  in the consequence half.
- **Subject first.** "DrainLoop is a background goroutine that repeatedly
  claims", not "A background goroutine (DrainLoop) repeatedly claims".
  Names never hide inside parentheticals.
- **Behavior before implementation structure.** "takes up to limit rows
  off the queue, oldest first, and returns them; deleting the row is the
  claim", not "a CTE selects the stalest ids ... and the outer DELETE
  removes exactly those rows". State the invariant the design buys ("a
  trigger enqueue for the same row never waits on this transaction"),
  not the failure mechanics behind it.
- **Parentheticals only when they add a distinct fact.** Keep "(or has
  been killed on)". Cut "(the worker runs when the flag is unset)" after
  "It defaults to enabled".
- **Enumerate the parts once, then the collective noun.** "stops the
  worker" after the drain loop and the sweep are established. Never
  re-enumerate, and never enumerate what the thing does not control.
- **State what is impossible, plainly, in first person.** "This should not
  be possible: the apply statements are a plain INSERT ... SELECT and
  DELETE whose only inputs are ids that exist in the queue. If we screwed
  up (a projection drift, a constraint we did not anticipate), the same
  batch would fail again on retry, so re-enqueueing would only churn. Log
  it with the ids and drop it; the daily sweep deletes ids the retry
  already dropped."
  Invariant, failure conditions, decision, recovery. No hedging.
- **Rescope every label when behavior splits.** If re-enqueue now only
  happens for lock-blocked batches, "failed batch" is wrong everywhere it
  appears: comments, log messages, test names.
- **Doc comments own the mechanism; package READMEs stay high-level
  guides.** A README is not "the code but in english". Implementation
  detail belongs to the doc comment next to the code.
- **Do not document de facto conventions.** If the framework or the
  migrations make something the default rule, the comment does not say so.
  Point at the artifact that owns the contract or say nothing.
- **No ticket refs or plan-doc coordinates in place of behavior.** "the
  backfill worker", not "the TICKET-123 backfill worker". The reader never
  opens the ticket tracker to understand the code.
- **A term of art is defined once; plain behavior everywhere else.** "(the
  tombstone correction)" in the place it is defined; "a second pass
  removing cache rows whose source row no longer exists" everywhere else.
- **Keep load-bearing precision.** Translate jargon ("mid-drain" becomes
  "after it was enqueued"), but keep the contract when the code depends on
  it: Postgres error classes 40 and 55, genuine lists, cross-references
  that carry the why.

The comment shape for a named thing (a metric, a function, a constant):

1. What it does or reports, in behavior terms.
2. What a reading means: "Sustained growth means the drain loop cannot
   keep up with (or has been killed on) the enqueue rate".
3. The operational caveat, when needed: "Sampled by the drain loop, so it
   freezes while the kill switch is off".

The wart shape, for code that looks wrong but is correct:

1. Name the sensible implementation the reader expects: "Why not
   min(base * 3^(n-1), max)?"
2. State the crux: the multiply wraps the int64 before min clamps.
3. Why, in the fewest words: "30s * 3^19 overflows the Duration, an int64,
   and min would clamp the overflowed value, not the intended product."

Simple and good beats complex and great. Cut whole claims to shorten;
never compress the survivors.

## Documentation files

Standalone documentation - package docs (a doc.go or package comment), READMEs, and anything under a docs/ directory - serves readers that symbol-anchored text never meets: someone onboarding and an expert looking up one fact, in the same pass. An inline comment or a docstring has the code as its context. A standalone doc has only its own order, so the standard is higher: clear sentences are the floor; the document must also serve the skimmer and the learner.

- **The inverted pyramid, at the document and the section level.** Lead with the answer at the top of the doc, and again at the top of each section: what the thing is and what the reader gets, first; the mechanism after; caveats and edge cases last. The reader decides when to stop reading, so stopping early must be safe.
- **Basics before advanced.** Each section stands on the ones before it. A reader who knows the basics can stop or skip ahead; a reader who does not gets each idea in the order they can absorb it.
- **Scan anchors.** Bold the load-bearing phrases so a reader who skims only the bold fragments still gets the story; the first sentence of each section carries the section's point. Bold sparingly outside the opening sections; a doc bolded throughout cannot be skimmed.
- **Presentation, not specificity.** These rules demand better order, never more content. Judge a doc against its own level of detail; do not add enumerations or file pointers the doc's level never promised.

No section template follows from this. Headings and structure belong to the repo's own conventions; apply the intent, not a shape.

## Clarity pass

Before you post, save, or send: reread the draft as a reader with zero context. Fix what they would stumble on. Do not announce the pass; just return clean prose.

Check: Does every sentence parse on first read? Does every term carry its plain-English meaning before or with the label? Is every technical phrase real - could you find it in the code, the docs, or common usage? If not, say what the thing does instead of naming it. Would a reader who has never seen this codebase, ticket, or conversation understand it? If the draft runs long, cut a claim; never tighten the grammar.

Two per-sentence tests catch what the checklist above misses. Run both on every sentence:

1. **The isolation test.** Cover the rest of the document. Can a reader with general engineering knowledge parse this sentence alone - subject, verb, and outcome - with nothing from the surrounding paragraphs? A sentence that only makes sense after the reader has absorbed the neighborhood is compressed; decompress it.
2. **The row-effect test.** For every verb that changes a stored row or record: does the sentence name the columns it changes and what happened to them? "Gets bumped", "sticks", "lands on the row" fail; "overwrites last_seen and modified_date" passes.
