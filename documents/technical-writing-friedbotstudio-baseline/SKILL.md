---
name: technical-writing
owner: baseline
description: Write technical documentation that matches the measured profile of professionally-written docs. Carries the craft rules derived from 114k words of pre-2022 documentation (SQLite, PostgreSQL, Python, Django, Rust, Go, Pro Git, nginx), the per-Diátaxis-type numeric targets, and the copywriting register for page leads. Use when drafting or rewriting any documentation prose, or when a page is factually right but reads as machine-written.
---

Documentation that reads as machine-written is rarely wrong and rarely ugly. It fails on **range**. Every sentence lands near the same length, every paragraph opens with the same rhetorical move, every claim arrives at the same pitch of certainty. A reader cannot say which sentence is wrong, only that the whole thing feels extruded.

This skill is built from measurement rather than taste. A corpus of 28 documentation pages published before 2022 — 113,887 words of body prose from SQLite, PostgreSQL 12, Python 3.8, Django 3.2, the Rust book, Effective Go, Pro Git, nginx, Backbone, 12factor and Redis — was parsed and profiled on 24 axes. `references/corpus-profile.md` carries the full table. Every number below comes from it.

> **The finding that matters most.** The corpus writes *longer, more qualified, more conditional* prose than a de-slopped draft does. Across the shipped pages this skill was written to fix, not one sentence in 1,262 ran past 30 words; professional documentation runs 11.5% of its sentences past 30 words. Stripping complexity is what made those pages read as generated. Bans alone cannot fix that, because a ban can only remove.

---

## The gate

```
node .claude/skills/technical-writing/measure.mjs --type <reference|explanation|tutorial|howto> <file>
```

Accepts HTML, Markdown, or a rendered page. It returns a weighted deviation score against the corpus bands and names each axis that is out of range, worst first. **Threshold 4.5.** For scale: the corpus median is 0.14, the corpus 90th percentile is 4.93, and the site pages this skill was built to repair scored 5.83 to 30.2.

A page is not finished until this exits 0. The score is calibrated, not decorative — at 4.5 it passes 86% of the professional corpus and none of the pre-rewrite pages.

---

## Step 1 — Classify. Exactly one type.

The type decides the numeric targets, the heading grammar and the person. A page that mixes types fails on every axis at once, because it is averaging two profiles.

| Type | Reader is | Answers | Corpus signature |
|---|---|---|---|
| **Reference** | mid-task, looking something up | "what are the flags" | 36% passive, `you` rare (7.5/1k), longest sections (1,160 words) |
| **Explanation** | away from the keyboard | "why is it like this" | Longest sentences (19.2 words), most hedging (3.1/1k), most lists |
| **Tutorial** | learning, has not done it | "take me through it" | Most code (12.2 blocks/1k words), `you` heavy (19.3/1k), lowest grade (9.9) |
| **How-to** | working, has a goal | "how do I do X" | `you` heaviest (20.8/1k), most enumerated (11.7 items/1k), short sections (201 words) |

If the classification is genuinely ambiguous, the page is doing two jobs. Split it.

---

## Step 2 — Write with range

These four moves carry most of the distance between generated prose and professional prose. They are what the ban-list approach cannot supply.

### 2.1 Vary the opening move

**The strongest single signal.** Real documentation opens a paragraph with a bare assertion 64–70% of the time. The rest of the time it opens with a condition, a definition, a purpose, an aside or a contrast. The pages this skill replaces opened with an assertion **82–94%** of the time — every paragraph making the same move, one after another.

Corpus distribution of paragraph openings:

| Move | Opens with | Reference | Explanation | Tutorial | How-to |
|---|---|---|---|---|---|
| assertion | *The roster is derived from…* | 70% | 69% | 64% | 64% |
| condition | *If the branch is protected…* | 13% | 7% | 10% | 9% |
| definition | *A hook is a Node script that…* | 9% | 11% | 9% | 11% |
| aside | *By default, …* / *Note that…* | 3% | 1% | 3% | 3% |
| purpose | *To run a workflow, …* | 2% | 3% | 3% | 4% |
| contrast | *However, …* / *Although…* | 1% | 3% | 2% | — |
| address-reader | *You can override…* | 1% | 1% | 3% | 4% |

`if` is the second most common sentence-opening word in the entire corpus (8.4% of all sentences, behind `the` at 15.8%). Conditions are not decoration. A system has cases; prose that never opens on one is describing a system that apparently has none.

### 2.2 Let sentences run

| | Corpus | Pre-rewrite pages |
|---|---|---|
| Mean sentence | 17.6 words | 12.2 |
| 90th percentile | 30 words | 20.5 |
| Sentences ≥ 30 words | 11.5% | 0.3% |
| Sentences ≤ 10 words | 24.8% | 44.4% |
| Step between adjacent sentences | 9.4 words | 6.9 |

About one sentence in nine should run past 30 words. Those are the sentences carrying a condition plus its consequence plus the exception — the ones that would need three flat sentences and a "however" otherwise. Then follow one with a short sentence. The alternation is the point.

The last row is the one to watch. Professional prose moves about 9 words between neighbouring sentences; flat spacing reads as generated even when every individual sentence is defensible.

### 2.3 Restore the modal verbs

Documentation is about what is permitted, required, possible and default. The corpus uses `can`, `may`, `must`, `will`, `should` and `might` **20.3 times per 1000 words**. The pre-rewrite pages used them 7.9 times, and several pages used none at all.

Flat indicative prose overstates certainty. "The guard blocks the write" and "the guard **will** block the write **unless** the marker is fresh" describe different systems, and only one of them is true.

Hedging is not weakness either: explanation prose hedges (*generally*, *typically*, *usually*) 3.1 times per 1000 words. Reference hedges far less, 1.4.

### 2.4 Stop avoiding the passive

Reference prose in the corpus is **36% passive**. Explanation 23%, how-to 25%, tutorial 19%. The pre-rewrite pages ran 9.9%.

The passive is correct when the actor is irrelevant or obvious: *the value is returned*, *the file is created in the project root*, *the token is written before the guard runs*. Forcing an active verb there invents an agent and reads translated. Use the active voice when the actor matters, which in a tutorial is most of the time and in a reference is not.

---

## Step 3 — Headings

Corpus grammar, as a percentage of headings on the page:

| Type | noun phrase | gerund | imperative | question |
|---|---|---|---|---|
| Reference | 91% | 7% | 1% | 1% |
| Explanation | 90% | 5% | 3% | 1% |
| Tutorial | 61% | **35%** | 4% | — |
| How-to | 57% | **29%** | — | 11% |

**Gerund headings are correct in tutorials and how-tos.** Django ships "Writing your first Django app"; Python ships "Using the Logging Module". A blanket ban on `-ing` headings contradicts the corpus and should not be applied outside reference and explanation.

Mean heading length is **2.7 words** (reference 2.5, tutorial 3.9). The pre-rewrite pages averaged 5.1, because their headings were sentences making claims. A heading is a signpost for someone scanning, not an argument.

Sentence case throughout. Title case appears on 16% of corpus headings and is a house-style choice; pick one and hold it.

---

## Step 4 — Evidence density

Prose that describes machinery without showing it reads as generated regardless of style, because a model can produce plausible description without access to the thing being described.

| | Corpus | Pre-rewrite pages |
|---|---|---|
| Inline identifiers per paragraph | 1.44 | 0.58 |
| Code blocks per 1000 prose words | 6.6 (tutorial 12.2) | 2.1 |
| Enumerated items per 1000 words | 7.4 | 0.5 |
| Parentheticals per 1000 words | 7.6 | 1.9 |

Name the actual flag, field, path or function rather than describing it. Put options, cases and steps in a list or table instead of a sentence that lists them. Use parentheses for units, defaults and cross-references — the corpus does so constantly, and their near-total absence is a reliable tell.

**Every factual claim traces to code, config, or a cited doc.** If the source does not support it, cut the claim rather than softening it.

---

## Step 5 — What to suppress

The ban list still applies, with corpus-measured ceilings rather than zero. Natural rates are **not zero**, and driving them to zero is its own tell.

| Pattern | Corpus rate | Ceiling |
|---|---|---|
| "X, not Y" negation-definitions | 1.3 /1k | 2.8 |
| Inflated vocabulary (*delve, realm, pivotal, seamless*…) | 0.55 /1k | 1.5 |
| Discourse connectives (*moreover, furthermore*…) | 1.5 /1k | 5.0 |
| Rule-of-three triplets | 0.53 /1k | 1.6 |
| Em dashes | 0.92 /1k | 3.2 |

Note `however` opens 0.8% of corpus sentences and `but` another 0.8%. Deleting every transition is over-correction; the corpus uses them, just sparingly.

Still absolute, because the corpus rate really is near zero:

- No `TODO`, `FIXME`, placeholder text, or "coming soon".
- No two headings sharing a rhetorical shape. Read the headings alone as a list; if four are built `<claim>, not <foil>`, that is the page's voice and it is machine-made.
- No promotional register in reference or explanation body copy.
- No claim the source does not support.

---

## Step 6 — Page leads (the copywriting register)

A lead, hero line or meta description is the one place persuasion is legitimate, and the only place the `copywriting` register applies. Body copy under Diátaxis reference and explanation forbids it.

A lead earns its place by being **specific and verifiable**, not by being warm:

- Assert what becomes true for the reader, then name the mechanism. Never the mechanism alone.
- Use a concrete number, name or limit the reader can check. "26 guards, wired at 7 lifecycle events" beats "a comprehensive guard system".
- One sentence, or two. The corpus lead averages under 40 words.
- No superlatives the page cannot demonstrate below the fold.

Everything in Step 5 still binds here. Persuasive register is not permission to inflate.

---

## Step 7 — Checks a score cannot make

Run these by reading, after the gate passes.

- **Paragraph-reshuffle.** Swap two body paragraphs. If nothing breaks, the section is a list wearing prose — give it a through-line or make it a list.
- **Treadmill.** Per paragraph, ask what is new. If 40% could be cut with no loss, cut it.
- **Type leakage.** Instruction on a reference page, explanation inside a tutorial, a flag table in a tutorial — move it and link.
- **Headings alone.** Read them in order as a table of contents. They should name subjects, not assert claims.
- **Claim tracing.** Pick three factual sentences at random and find their source. If any cannot be traced, the page has invented something.

---

## Receipt

Close with the page type, the measure score before and after, and the axes that moved. A receipt that cannot honestly be written means the page is not done.
