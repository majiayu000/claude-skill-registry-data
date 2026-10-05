---
name: plain-prose
description: Holds this repo's writing rules for plain, human prose and the LLM-voice tells to cut. Load it before writing any human-facing text — docs, code comments, benchmark write-ups, site copy, or chat replies.
---

# plain-prose — write plain, human prose; keep the proof out of the shop window

The stock LLM writing voice reads as generic and machine-made, and on a project whose whole pitch is
"no LLM, deterministic, grounded or an honest miss," that voice undercuts trust in the claims. This
skill is the standing style guide. It has two jobs: make prose read as if a person wrote it, and keep
the supporting evidence out of the way so reader-facing surfaces stay short enough that someone
actually reads them.

**Scope: everything written for a human reader** — the homepage, the README, the design docs,
the benchmark write-ups, the other skill docs, code comments, and the assistant's own chat responses.
Plain, direct sentences carry more authority than decorated ones, and they match the voice tmct's
docs already use: honest, terse, lowercase-y, no marketing.

The base rules in section 1 are the Plain English Campaign's, who have promoted plain English and
fought gobbledygook since 1979 (plainenglish.co.uk). Section 2 adds the LLM-voice tells to cut on top
of them.

> **Use it whenever you draft or edit human-facing text** in this repo: `README.md`,
> `public/index.html` (the homepage at tmct.polycode.co.uk, also the landing surface), the `PLAN_*.md` design
> docs, the `BENCHMARK_INFERENCE_<version>.md` / `BENCHMARK_AGENT_<version>.md` /
> `BENCHMARK_CONVERSATION_<version>.md` write-ups, the other skill docs, any other `*.md`, code comments,
> and chat.

---

## 1. Plain English base rules

The foundation. Apply these before worrying about anything else.

- **Short sentences. Average 15–20 words.** Mix short and longer, but if a sentence runs past ~25
  words, split it. One long clause-stacked sentence is the most common wordiness fault in these docs.
- **One idea per sentence** (plus perhaps one closely related point). If you are joining two ideas
  with a dash or a semicolon, they usually want to be two sentences.
- **Active voice, not passive.** "The parser resolves it," not "it is resolved by the parser." Passive
  hides who does what and adds words.
- **Everyday words.** Use the simplest word that fits. Cut jargon a first-time reader can't parse, or
  define it in three words the first time.
- **Write to the reader as "you"; call ourselves "we".** "You run it from the repo root," not "the
  tool is run by the user from the repo root."
- **Cut nominalisations** (an abstract noun hiding a verb). "We discussed it," not "we had a
  discussion about it." "It fails," not "it results in a failure."
- **Use lists** when you have three or more parallel points. A bullet list scans; a comma-spliced
  sentence does not.
- **Cut every word that earns nothing.** Delete redundant openers ("It is important to note that",
  "In order to"), doubled words ("each and every"), and filler adverbs.

Common substitutions (Plain English Campaign's A-to-Z, the ones that recur here):

| instead of | write |
| --- | --- |
| additional | extra |
| commence / initiate | start |
| ensure | make sure |
| in excess of | more than |
| prior to | before |
| subsequent to | after |
| terminate | end |
| utilise | use |
| in order to | to |
| approximately | about |
| demonstrate | show |
| sufficient | enough |
| require | need |
| regarding / with regard to | about |
| whilst | while |
| in the event that | if |

---

## 2. The LLM-voice tells to cut

On top of the Plain English rules, scan every draft for these machine-voice fingerprints and remove
them.

- **Em-dash sprinkling as fake sophistication.** Do not bolt clauses together with `—`. Use a period,
  a comma, or restructure. Reserve em-dashes for rare, deliberate use. (tmct's docs already lean hard
  on em-dashes; this is the most common tell to trim here.)
- **The "not X, it's Y" / "not X but Y" / "not only X but also Y" negation-contrast.** State what the
  thing is, not what it isn't. "One of 15 cells cleared the bar," not "it is not a broad win."
- **Announced-honesty preambles.** Drop "honest current state:", "to be clear," "reported honestly."
  Just report the thing. Labelling text as honest signals the opposite. (tmct's ethos is honesty; let
  the prose *be* honest rather than *say* it is.)
- **Colon reveals.** Avoid the dramatic setup-then-colon. Write a plain subject-verb sentence.
- **Anthropomorphizing tools and benchmarks.** A parser does not "want," a benchmark does not
  "struggle." Say what it did or measured. (The README's PARRY framing is a deliberate, earned
  exception; don't extend it to the metrics.)
- **Rule-of-three padding, hedging, and hype.** Cut "powerful", "transformative", "seamless",
  "robust", "in the ever-evolving landscape", "it's worth noting", "delve", and the reflexive
  three-item list where one item does the job.
- **Listicle bloat and promotional filler.** Don't inflate two real points into a bulleted five.
  Don't restate the headline three ways. One concrete claim beats three decorated ones.

Default to short declarative sentences a person would write. Say the thing once, plainly.

---

## 3. Proofs and evidence: keep the shop window short

Reader-facing surfaces (the homepage, the README) sell the idea. They are not the place to
prove it. Someone landing on the page wants to know what tmct does and how to try it, in that order,
before they hit any methodology. Bury the value under proof apparatus and they leave.

**On the homepage and README:**

- Lead with what it does and what the reader gets, in one or two short sentences. Benefit before
  evidence.
- Give the headline result in a sentence, with the one number that matters and its condition (which
  benchmark cycle, judge, task shape). Then stop.
- One small table at most, and only if it earns its place. Do not stack multi-row cross-cycle tables,
  per-run N-counts, caveat paragraphs, and method notes on a landing page.
- Prefer whitespace and short blocks over dense paragraphs. If a section is a wall of text, a reader
  skips the whole wall.
- State conditions in one clause, not three hedged paragraphs.
- Link out for the proof: "full method and scores in the cycle write-up (`BENCHMARK_INFERENCE_<version>.md`)."

**Keep the full detail in the `BENCHMARK_INFERENCE_<version>.md` write-ups** (and their siblings,
`BENCHMARK_AGENT_<version>.md` and `BENCHMARK_CONVERSATION_<version>.md` — each bench family folds its own
transcript/evidence section into the one report file, no separate companion files). That is the
home for the complete tables, the judge scores and spreads, the per-cell breakdowns, the
tuning-cycle contract, the caveats, and the raw transcripts. The `PLAN_*.md` docs hold the
design-level detail behind a feature. A reader who wants to verify follows the link and finds
everything; a reader who just wants to know what tmct does is not made to wade through the proof.

The rule in one line: **the claim lives in the window, the proof lives in the back room, and a link
connects them.**

---

## 4. Related principles (same spirit)

- **No delta-framing.** Describe the work on its own terms. Don't frame a design as a rebuttal to a
  single external citation or to seonix's old shape. If a benchmark refuted an idea, report the
  measurement, not a running quarrel with the source. Contrast framing reads as defensive.
- **Dependency pragmatism.** Never frame work around avoiding dependencies. State what a choice does
  positively.
- **"NOT" sections stay factual.** The README's "What tmct deliberately is NOT" section is fine
  because each bullet states a positive scope decision (it's a conversation layer, not an indexer).
  Keep those grounded; don't let them drift into a list of things competitors get wrong.

All three are the same instinct as this skill: say what the thing is, positively and plainly, without
scaffolding it against something else.

---

## 5. Workflow — edit before you ship

**Delegate the drafting of a large deliverable.** When a task calls for a long doc rewrite or a big
report, prefer handing the drafting itself to a background sub-agent under the coordinator model
(`CLAUDE.md`), then review and edit the result in the main session. This keeps the main chat free
for the operator, the same standing preference this repo applies to any other long-running work.

After drafting any human-facing text:

1. **Cut length first.** Split every sentence over ~25 words. Delete redundant openers and filler.
   Turn a three-plus-point sentence into a list. Run the substitution table over it.
2. **Cut the tells.** Search for `—`, "not just", "not only", "not X, it's Y", "honest"/"transparent"
   self-labels, "delve", "it's worth noting", and hype adjectives. Remove each one.
3. **Read it as a stranger.** If a clause sounds like a press release or a model's default voice,
   rewrite it as the sentence a person would say out loud.
4. **On a reader-facing surface, check the order.** Benefit first, then how to try it, then a short
   claim with a link to the relevant `BENCHMARK_*_<version>.md`. If methodology arrives before benefit, move
   it.
5. **Match the surrounding voice.** tmct's docs are terse and lowercase-leaning; a paragraph that
   suddenly turns formal and three-adjectived is a tell even if every word is fine.

This applies to the assistant's own chat responses too, not only the artefacts it produces.

---

## 6. One-paragraph TL;DR

Write plain, direct prose a person would recognise as human. Short sentences (15–20 words), one idea
each, active voice, everyday words, "you"/"we", no nominalisations, lists for parallel points. On top
of that, cut the LLM tells: em-dash sprinkling, "not X it's Y", announced-honesty, colon reveals,
anthropomorphized parsers or benchmarks, hype, rule-of-three padding, listicle bloat. On the homepage
(`public/index.html`) and README, lead with the benefit, state the headline claim in a sentence, and
link to the proof instead of reproducing it; the full tables, judge scores, contract, caveats, and
transcripts live in the `BENCHMARK_*_<version>.md` write-ups, and the
design detail in the `PLAN_*.md` docs. Base rules are the Plain English Campaign's
(plainenglish.co.uk). Match the honest, terse voice the repo already uses. Applies to docs, code
comments, site copy, and chat.
