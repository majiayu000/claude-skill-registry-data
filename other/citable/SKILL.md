---
name: citable
tier: D
description: >
  Make authored content survive the two selection surfaces it now faces: human
  engagement and LLM retrieval for citation. These partially anti-correlate, and
  the tactics that raise reactions are in two measured cases the ones that
  suppress citation. Encodes effect sizes from published causal studies (Scrunch,
  12,000 ChatGPT observations via double machine learning; Semrush, 325,000
  prompts over 89,000 cited URLs) rather than folklore, and ships a linter that
  enforces the mechanical half. Use when: (1) about to publish a post, article,
  headline, bio, or profile field and wanting it cited by AI answer engines,
  (2) auditing existing content for the unicode/link-in-comments/thin-specificity
  failures, (3) deciding whether a piece should be a short post or a long-form
  article, (4) converting existing long-form work (specs, ADRs, docs) into
  publishable articles, (5) choosing between optimizing for reach and optimizing
  for citation. NOT FOR: website/page markup, meta tags, JSON-LD, llms.txt or
  Core Web Vitals (use seo-llmeo); recruiter-facing profile tuning for job search
  (use linkedin-profile-optimizer); running an engagement loop (use
  social-intelligence). Triggers on "will this get cited", "citable", "AI search
  visibility", "answer engine optimization", "audit this post", "should this be
  an article", "why is my content invisible to ChatGPT".
version: 1.0.0
category: publishing
tags:
  - content-optimization
  - ai-citation
  - answer-engine
  - publishing
  - linkedin
---

# citable

Your content is now selected by two different systems with two different
objectives, and most advice about "what performs" describes only the first.

**Surface one — engagement.** Humans scrolling, plus the feed model deciding what
to show them. Rewards hooks, rhythm, story, a CTA.

**Surface two — citation.** An LLM retriever deciding whether your text is worth
quoting in an answer to someone's question. Rewards specificity, named things,
and self-containment.

The measured result that reorganises everything else: **engagement does not
drive citation.** Holding content constant, a post with 100 reactions is cited at
essentially the same rate as one with 10,000, and accounts under 500 followers
are cited as often or more than large ones. Citation selects on content. Which
means a small account with real technical depth competes directly with a large
one, on the surface that increasingly decides what buyers believe.

## The effects

Every number below traces to a study, not to taste. Full provenance in
[`references/evidence.md`](references/evidence.md).

| Dimension | Citation | Reactions | Read |
|---|---|---|---|
| Technical detail | **+77%** | ~0 | The dominant factor, and free |
| Named entities (plain text) | +33% | +5% | Retriever reads text, not the mention graph |
| Topic specificity | +18% | +13% | The only true sweet spot |
| Link-in-comments | −31% | +11% | Transfers citability rather than destroying it |
| Unicode "bold" | **−58%** | +12% | A missing NFKD normalisation, not a style judgement |
| FAQ structure | 0 | −9% | Loses on both |
| Follow-for-more CTA, anecdote, step-by-step, line-break rhythm | 0 | +22 / +11 / +7 / +6% | The engagement playbook: harmless to citation, useless for it |

## First principles

**1. Decide which surface you are playing before you write a word.**
Both is possible but not automatic, and two dimensions force a real trade.
State the objective in one line, then let it pick the format.

**2. Specificity is the only free lunch.**
Technical detail buys the largest citation gain at zero engagement cost. There
is no reason to withhold it. The generic version of your sentence competes with
a hundred identical ones and gets summarised into a generic answer; the specific
version *is* the source.

**3. How-I beats how-to, now that instruction is free.**
A reader wanting steps asks a model and gets them personalised in seconds. Your
tutorial competes with infinite tailored instruction. What survives is the
first-person account: what you did, why, what happened, including the failures.
Generic frameworks get absorbed. A specific account becomes a citation. You
become the case study rather than the commodity.

**4. Long form feeds short form. Never the reverse.**
You cannot expand a 200-word post into an essay, because the thinking was never
done at that depth. So a place where you think a topic through end to end is a
prerequisite, not an output. If you already have specs, ADRs, design docs, or
incident writeups, you have already paid this cost.

**5. When a surface truncates, find out what it truncates on.**
Tokens for the retriever, pixels for the human eye, characters for the field
limit. These are three different budgets. Counting characters satisfies none of
them reliably. Check the actual constraint.

**6. Borrowed attention beats manufactured attention — until it degenerates into summary.**
Attaching your point to something people already watch (a company's decision, a
news event, a person, a consensus belief) works because you enter a room that is
already full. Each form has one test that stops it collapsing into a summary
with a name attached:

| Form | The test |
|---|---|
| A company's decision as your frame | Is the insight one only you would make? |
| A news event | Can you answer "so what" in one sentence? |
| A person's idea | Are you adding, or restating? |
| A contrarian claim | Does it make you slightly nervous to post? |

## Procedure

1. **Name the surface.** Citation, engagement, or explicitly both. One line.
2. **Pick the format from the objective.** Long-form articles are 50–66% of cited
   platform content at 500–2,000 words, and almost nobody publishes them; feed
   posts cluster at 50–299 words. If the goal is citation and the material is
   already written long, publishing it as an article is the highest-leverage move
   available.
3. **Mine, don't invent.** Pull the piece from work that already happened:
   transcripts, commits, incidents, specs. If you are inventing the content, you
   are writing surface-one filler.
4. **Write the body first, then find the hook inside it.** The best opening line
   is already in the draft. If nothing in the body is worth pulling to the top,
   the problem was never the opening.
5. **Run the linter.** `scripts/citable_check.py` handles everything mechanical.
6. **Answer what the linter cannot.** Is the technical detail real or performative?
   Does the specificity come from actual work? Would you have written this if no
   algorithm existed? A piece that passes every check and says nothing is the
   failure mode this skill cannot catch for you.

## The deterministic core

```bash
# a file, against a named surface budget
python3 scripts/citable_check.py draft.md --surface article

# stdin, asserting specific entities appear
cat post.txt | python3 scripts/citable_check.py --surface post --entities "Rust,Databricks,Linear"

# machine-readable
python3 scripts/citable_check.py draft.md --surface headline --json
```

Surfaces: `headline` (≤220 chars) · `services` (150–500 chars) · `post`
(50–299 words) · `article` (500–2,000 words) · `prose` (no length budget).

Exit `0` when no check FAILs, `1` on any FAIL, `2` on usage error — so it drops
into a pre-publish hook or CI.

It checks: math-alpha unicode, length against the surface budget, numeric
specificity density, named entities (supplied or auto-detected),
link-in-comments, FAQ shape, em-dash density as a machine-written tell, and a
full non-ASCII inventory.

It deliberately does **not** judge whether your content is any good.

## Boundaries

| Use instead | When |
|---|---|
| `seo-llmeo` | Page and site markup: meta tags, JSON-LD, `llms.txt`, Core Web Vitals |
| `linkedin-profile-optimizer` | Recruiter-facing profile tuning for a job search |
| `social-intelligence` | Running an engagement/outreach loop |
| `blog-post`, `content-creation` | Producing the draft in the first place |

`citable` starts once text exists and asks only whether it will survive retrieval.

## Anti-rationalization

| Excuse | Reality |
|---|---|
| "I need a bigger audience first." | Follower count has near-zero predictive power on citation. The audience was never the gate. |
| "Technical detail will hurt engagement." | Measured at ~0 effect on reactions. It costs you nothing and it is the largest citation gain available. |
| "Unicode bold looks more professional." | ChatGPT's retriever does not NFKD-normalise it, so those words are unqueryable. It is a tokenizer fact, not a taste question. |
| "The linter passed, so it's good." | The linter checks mechanics. It cannot tell whether you said anything. |
| "I'll write something citable this week." | If you are inventing content to be cited, you have it backwards. Mine what you already did. |

## Evidence and limits

Effect sizes come from two 2026 studies over a single platform, and the citation
rate for that platform already dipped once inside the measurement window. Treat
these as a dated snapshot with a decay rate, not a standing law. The durable part
is the *shape* of the finding — two surfaces, partially anti-correlated,
substance-selected rather than popularity-selected — which is unlikely to invert
even as the coefficients move.

Full sources, methodology, and what is `[HIGH]` versus `[MED]`:
[`references/evidence.md`](references/evidence.md).
