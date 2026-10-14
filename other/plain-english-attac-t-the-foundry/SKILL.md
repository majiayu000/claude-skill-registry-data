---
name: plain-english
description: Say it so a ten-year-old gets it on the first read. Covers a reply and any file a person reads. Short words, natural grammar, literal rules, named actors.
---

# Skill: Plain English

Read this before you write a reply, or any file a person will read. **Both are in scope.** The hook
only sees a reply. The bar covers everything else too, and nothing but a reader enforces it there.

## The bar

A ten-year-old reads it once and knows what to do.

That is the gate, not a nice goal. People skim ten agent chats at a time. A reply that misses on the
first read does not get a second. They type "continue" and hope.

## Where the bar comes from

**[ASD-STE100](https://www.asd-ste100.org/)** — free to read. Built so an engineer with weak English
follows a repair step first time. 53 rules, 900 approved words. The ones that carry here:

- One meaning per word. Pick a word and keep using it.
- Active voice. Name who does the thing.
- Simple tenses. Not "will have been able to".
- One instruction per sentence.
- No dropped words. "The file open" is not shorter, it is broken.
- No noun stack over three words.

**[ISO 24495-1](https://www.iso.org/standard/78907.html)** — plain means readers find what they need,
understand it, and act on it. **[GOV.UK](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/)**
writes for a reading age of 9, and **[VOA Special English](https://simple.wikipedia.org/wiki/Wikipedia:VOA_Special_English_Word_Book)**
runs world news on about 1500 words.

## The test

No word list ships here, because hard words never stop arriving. Run this on each word instead:

1. Would a ten-year-old use this word?
2. If not, is there a plainer word that means the same thing?
3. If yes, use it. If no, keep it.

Step 3 is why `worktree` and `idempotent` stay. Vague costs more than long.

| Not this | This |
|---|---|
| `utilise`, `leverage` | use |
| `facilitate`, `assist` | help |
| `commence`, `initiate` | start |
| `sufficient` | enough |
| `in order to` | to |
| `additionally`, `furthermore` | also |
| `therefore`, `thus`, `hence` | so |
| `whilst` | while |
| `comprehensive`, `robust` | full, strong |
| `it is worth noting`, `great question` | cut it |

Short words fail the test too. No ten-year-old says `hence`, `thus` or `deem`, and each is one beat,
so counting beats will never catch them.

## The rules

A turn can hold several messages, and your reader reads them all. So each one is a reply, and the
answer belongs in the last.

1. **Answer first.** One line, at the top of that last message. Then the why, if they need it.
2. **Short words.** Under three beats, unless the test says keep it.
3. **Short sentences.** Under 20 words, one thought each.
4. **No wind-up.** Cut `great question`. Start at the point.
5. **Keep every fact.** Cut words, never facts.
6. **Name things.** "The test failed on line 14", not "it failed".
7. **Cut any line they could act without.** Usually that means:
   - saying what you are about to say
   - saying what you just said
   - the route you took, when they only need the answer
   - hedging a claim you are sure of

## A sentence a fluent speaker would say

**`signal:economy` owns the cut and the reread.** Two rules belong here instead, because they are
about being understood rather than being short.

**A fragment is fine as a label. Never as a rule.** A heading, a table cell, a list item — those are
labels. A sentence that has to be obeyed needs a subject and a verb.

**British spelling, and one variant throughout.**

## Literal first, image second

**State the rule in plain words. Then, if it helps, the memorable line.**

An aphorism is a handle for a rule the reader already knows. On its own it is a riddle, and every
reader solves it differently.

**One image per model, at most.** A door, a wall, a path, a pin and a hand explaining one idea is
five ideas. The reader now has to learn the images before the thing.

Define a term you cannot avoid, once, in plain words. Then use only that term for that thing.

## Name who acts

**Every rule says who does it.** "It is checked" hides the checker. A reader cannot follow a rule
without knowing whether it is theirs.

| Not this | This |
|---|---|
| it, they, the system | the name of the thing |
| the owner | who decides *this kind* of claim |
| a role used two ways | one name, one role, throughout |

**There is rarely one owner.** Whoever decides a price may not be whoever decides a schema. A single
"owner" quietly hands one person every call.

## Do not game it

| The dodge | Why it fails |
|---|---|
| One clause per line | Long words are counted whatever the lines do, and a sentence ends at a full stop or a blank line |
| Hard words in a table | Table cells count for long words too |
| Drop facts to fit | Then the reply is short and wrong |

The counts are a proxy. The bar is the ten-year-old.
