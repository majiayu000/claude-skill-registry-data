---
name: manifesto
description: Write or critique a company manifesto, mission page, founding essay, or "why we exist" document. Use when someone asks for a manifesto, a vision statement, a values page, an "about" or "mission" page with real conviction, a founding blog post, a charter, or a principles document. Also use to audit an existing one for hedging, empty values, and missing stakes. Grounded in a study of 36 tech manifestos from manifestos.tech (Tesla, SSI, Mozilla, Anduril, Obsidian, Linear, Anthropic, Physical Intelligence and others).
---

# Manifesto

A manifesto is not an about page with better adjectives. It is a document that
makes a claim about the world, states what follows from that claim, and names
what the writer is giving up in order to act on it. Everything in this skill
comes from reading the collection at
[manifestos.tech](https://www.manifestos.tech/) and taking apart what the good
ones actually do.

The single test: **could a competent, well-funded competitor publish the
opposite claim and mean it?** If not, you have written a description, not a
position. "We believe in quality software" fails. "Your files should outlive the
app that made them" passes, because a cloud-native company would genuinely
disagree.

## Reference files

Read the one you need. Do not read all four by default.

| File | Read it when |
|---|---|
| `reference/archetypes.md` | Choosing the shape. Seven forms, with spines and word counts. |
| `reference/voice.md` | Writing or rewriting sentences. Openings, closings, rhythm, banned words. |
| `reference/corpus.md` | You want a precedent to study, or the user asks "who does this well". |
| `reference/checklist.md` | Auditing a draft, yours or someone else's. |

## Workflow

### 1. Interview before you write

You cannot manufacture conviction. Do not start drafting from a company
description. Ask, and keep asking until you get answers that are specific enough
to be wrong:

1. **What do you believe that most serious people in your field do not?**
   Push until the answer is contestable. If they say "AI will be important",
   that is not a belief, it is a weather report.
2. **What broke, or what did you watch fail, that started this?** The best
   manifestos are downstream of a specific frustration. Get the scene.
3. **What is the bottleneck?** Not the market opportunity. The one thing that,
   if it moved, would move everything else.
4. **What are you giving up to do this?** Revenue, speed, optionality, a
   category, your own product's permanence. See "The cost" below.
5. **What does the world look like in ten years if you are right?** Concrete.
   What can a person do on a Tuesday that they cannot do now.
6. **Who is this for, and what do you want them to do?** Recruits, customers,
   investors, regulators, peers. The reader shapes the register.
7. **What are the real numbers?** Orders, dates, watts, milliseconds, headcount.
   One true number outperforms a paragraph of ambition.

If the user cannot answer 1 and 4, say so plainly and offer to write a good
about page instead. A manifesto without a contestable belief and a stated cost
reads as marketing, and readers can tell.

### 2. Find the one sentence

Before any structure, write the load-bearing sentence: the claim the whole
document is an argument for. It should survive being quoted alone with no
context. Test it three ways:

- **Invert it.** Does the inverse make sense as someone else's strategy?
- **Date it.** Could this have been written in 2015? If yes, it is a truism.
- **Cost it.** Does acting on it require sacrificing something obvious?

Show the user two or three candidate sentences and let them pick. This is the
highest-leverage decision in the document and it is theirs, not yours.

### 3. Choose the archetype

Read `reference/archetypes.md` and pick one deliberately. The most common
mistake is defaulting to the Principles Charter (numbered values) when the
material calls for the Named Problem or the Personal Testament. Match the shape
to what you actually have:

- One overwhelming conviction and nothing to explain → **Single Claim**
- A bottleneck you can name better than anyone → **Named Problem**
- A coalition or an institution that needs shared law → **Principles Charter**
- An idea bigger than your company → **Philosophy**
- A sequence where each step funds the next → **Staged Plan**
- A founder whose story is the argument → **Personal Testament**
- A technology whose time has arrived → **Historical Inevitability**

### 4. Draft to the spine

Nearly every manifesto in the corpus, regardless of archetype, moves through
these beats. Some compress several into one sentence. None skip more than two.

1. **World state.** What is true now. Present tense. No hedging.
2. **The gap.** What has not happened, and why the obvious explanations are
   wrong.
3. **The name.** Your term for the problem or the principle. This is the line
   people repeat.
4. **The belief.** Two to five things you hold that follow from the name.
5. **The build.** What you are actually making. Concrete enough to fail at.
6. **The cost.** What you gave up to make it that way.
7. **The world after.** What becomes possible. Specific, not utopian.
8. **The invitation.** One clear action.

### 5. Cut

First drafts run roughly 40 percent long. Cut in this order:

1. Every sentence that describes the company rather than the world.
2. Every adjective doing work a noun should do.
3. Every hedge: "aim to", "help to", "seek to", "strive to", "look to".
4. Every paragraph that would survive being moved to a different company's page.
5. The second example when the first one landed.

Then read it aloud. Manifestos are heard, not scanned. Anything you stumble over
is wrong.

### 6. Audit

Run `reference/checklist.md` against the draft before delivering. Report what
fails rather than quietly patching it, because some failures are the user's call
(for example, they may not be willing to state the cost yet).

## The cost

This is the move most people miss and it separates the real ones from the
imitations. Every manifesto in the corpus that still reads well years later
names a sacrifice:

- Safe Superintelligence structures itself so that commercial pressure cannot
  reach the work, which means no products in the meantime.
- Obsidian's philosophy concedes that Obsidian itself will become obsolete, and
  says the files matter more than the app.
- Tesla's 2006 plan opens by admitting the first car is expensive and only a few
  people can buy it, then explains why that is the plan and not a flaw.
- Mozilla commits publicly to principles that constrain what it is allowed to
  build.

A vision with no cost is a wish. Ask for the cost, and put it in the document
where a reader cannot miss it, usually right after the build.

## The enemy

Good manifestos name an adversary. Bad ones name a competitor. The corpus
consistently names a **condition** instead: institutional decay, bespoke
one-off projects, files trapped behind a login, coordination overhead, the gap
between what AI can do on a screen and what it cannot do with a shirt.

Naming a condition lets the reader place themselves on your side. Naming a
company makes the document expire when that company does, and reads as small.

If the user insists on naming a competitor, push back once, then do it their way
and tell them the tradeoff.

## Length

From the corpus, in words of body copy:

| Range | Use | Example |
|---|---|---|
| 150–350 | One conviction, maximum compression, brevity is the argument | SSI |
| 500–700 | A single idea developed properly. The default. | Obsidian, Linear, Hadrian |
| 1,000–1,300 | A company with several distinct commitments | Thinking Machines, Anthropic, Valar |
| 1,800–3,000 | A charter, or a vision plus its technical case | Mozilla, Physical Intelligence |
| 5,000+ | A personal testament with narrative | The Browser Company |

Default to 500–700 unless the material genuinely demands more. Length is not
seriousness. The shortest document in the collection is also one of the most
quoted.

## Formats

The same manifesto lands differently by surface. Decide which you are writing:

- **Web page.** Section headings carry the argument on their own. A reader who
  only reads headings should get the whole thing.
- **Founding blog post.** Dated, signed, first person, allowed to be provisional.
- **Charter.** Numbered clauses, stable grammar, written to be cited later.
- **Deck.** One beat per slide, the naming line gets its own slide.
- **Recruiting page.** Ends on the invitation and means it.

## If this is a Navon manifesto

Navon has house rules that sit on top of everything here:

- Plain human English. No AI cadence, no sentence fragments used for drama, no
  rhetorical pairs ("not X, but Y" repeated as a tic).
- No em dashes anywhere.
- Light on detail, heavy on what is actually true. Do not invent traction.
- White-label framing where partners are involved.

Read `.claude/skills/navon-design/SKILL.md` for surface and typography rules
before building the page or document, and `design-system/tokens.json` for the
token contract. For a printed version, use the `navon-brand-doc` skill.

## Do not

- Write a values list that no reasonable person would oppose.
- Use "passionate", "world-class", "cutting-edge", "revolutionize", "leverage",
  "synergy", "best-in-class", "empower" or "unlock" as load-bearing words.
- Refer to the company in the third person throughout. Use "we".
- Promise something you cannot start on this quarter.
- End with a contact form. End with an invitation.
- Ship a manifesto the founders have not read out loud.
