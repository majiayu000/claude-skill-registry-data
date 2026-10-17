---
name: humanize-writing
description: Rewrite or generate prose so it reads as natural human writing instead of obviously AI-generated text. Use when the user asks to humanize, de-AI, or un-robotify a text, and proactively whenever drafting substantive prose the user will publish or send (essays, blog posts, articles, emails, reports, marketing copy, bios).
license: MIT
---

# Humanize Writing

## The core idea: fix causes, not symptoms

Text reads as "AI-written" because of *underlying habits*, not because of any single banned word. The real problems are almost always one of these:

- **Vagueness** dressed up as substance (claims that could apply to any subject).
- **Padding** that inflates importance or adds analysis nothing in the source supports.
- **Mechanical uniformity** (every paragraph the same shape, every list the same format, the same three or four transition words).
- **Tonal drift** toward brochure or travel-guide enthusiasm.
- **Register leaks** where chatbot-to-user conversational habits bleed into the text.

So the goal is genuinely better writing, not find-and-replace. If you delete "delve" but leave the vague, padded sentence it sat in, you've only made the problem harder to see. Fix the sentence and the tell disappears on its own.

**Two hard rules while humanizing:**

1. **Preserve meaning and accuracy.** Never invent a specific fact, date, source, or bit of color to replace a vague claim — this is the rule most tempting to break, because a fabricated detail *feels* human. If a claim is empty, cut it or find a real specific from the source; don't manufacture one. This applies just as hard when *generating* prose in the user's voice: "specificity over generality" means using the specifics the user gave you, not inventing config values, incidents, or biographical details about their situation that they never stated. Keep genuinely necessary hedging ("approximately", "in most cases") — stripping accurate qualifiers to sound confident is a different failure.
2. **The tell is density, not the instance.** Every pattern below is a signal, not a ban. Natural writing uses em dashes, "however", even the occasional triple; what reads as machine-made is reflexive, repeated use. Over-correcting (zero em dashes ever, contorting a sentence to avoid "is") produces its *own* unnatural artifacts.

## Workflow

**When revising existing text:** Read it once for meaning. Identify which of the five causes above are present. Rewrite at the level of sentences and paragraphs, not words — recast the puffy sentence, vary the uniform structure, cut the unsupported analysis. **Then rebuild.** Heavy cutting leaves prose that is accurate but flat — uniform medium-length sentences marching in step, which is itself a machine signature. After the cuts, re-vary the rhythm and carry over the source's *real* concrete color (its specifics, its one vivid detail) so the result reads lively, not skeletal. Finish with the self-check pass at the bottom of this file.

**When generating fresh prose:** Write naturally, then run the self-check before delivering.

**Match the genre.** Encyclopedic, technical, marketing, and casual writing have different natural registers. "Humanized" marketing copy can be warm and punchy; humanized technical docs are plain and direct. Don't flatten everything to one voice.

## What good looks like

Aim *toward* these; the tells below are diagnostics for when you've missed:

- **Specificity over generality.** A concrete number, name, date, or example beats any amount of "significant" and "vibrant." Specifics are the most human thing you can write.
- **Varied rhythm.** Mix sentence lengths. Follow a long sentence with a short one. Uniform medium-length sentences are a machine signature.
- **Earn every clause.** If a phrase could be deleted without losing information, delete it.
- **Plain verbs and nouns.** Prefer the common word to the impressive one. Plain "is" is good.
- **Commit to claims.** Say the thing directly instead of hedging it behind a vague authority.
- **Let structure vary.** Not every section needs the same intro-body-significance arc. Not every list needs the same format or length.

---

## The tells, with fixes

Ordered roughly by importance — tonal and structural tells at the top matter far more than typographic ones at the bottom. When checking whether a specific word or phrase is a tell, or doing the density count in the self-check, read `references/word-lists.md` for the full inventories and plain-word swaps.

### 1. Significance-inflation and puffery (highest priority)

LLMs reflexively puff up importance, tying arbitrary details to grand themes ("stands as a testament to", "plays a pivotal role", "reflects a broader"). The single strongest tell.

- **Bad:** "Founded in 1989, the institute marked a pivotal moment in the evolution of regional statistics, reflecting a broader movement toward decentralization."
- **Good:** "The institute was founded in 1989 to produce statistics for the regional government."

Fix: state what happened. Cut the editorializing about what it "represents" or "symbolizes" unless a source actually makes that claim and it matters.

### 2. Superficial analysis via dangling participles

A fact, then a comma, then a present participle faking analysis ("…, highlighting the region's growth", "…, ensuring its legacy").

- **Bad:** "The bridge opened in 1932, cementing the city's status as a regional hub and reflecting the era's ambition."
- **Good:** "The bridge opened in 1932."

Fix: if the participle clause adds a real, sourced point, make it its own sentence with a concrete claim. Otherwise delete it.

### 3. Vague attribution / weasel wording

Opinions pinned on a fuzzy authority that's never named ("experts argue", "observers have noted", "it is widely regarded").

Fix: name the specific person or source, or state the claim plainly as fact if it's uncontested, or cut it.

### 4. Negative parallelism ("not just X, but Y")

The contrast-for-drama construction ("this isn't just a tool — it's a complete rethinking", "not only … but also"). Stereotypical AI cadence.

Fix: make the positive claim directly. Cap at one per piece.

### 5. Rule of three — including structural triples

Reflexive grouping in threes. This covers vague adjective triples ("a fast, reliable, and scalable solution") *and* structural triples, which survive rewrites more often: "whether you're a freelancer, a small business owner, or a growing startup"; "another thing to patch, another thing to monitor, another thing to page you at 3am". Humans use triples sometimes; LLMs default to them.

Fix: vary your list lengths — two items, four, or one well-chosen one. Prefer a single concrete detail over three vague descriptors. When a structural triple appears in a source you're rewriting, don't just reword its three legs; change the count.

### 6. Overused "AI vocabulary"

*Delve, showcase, testament, tapestry, pivotal, robust, leverage, seamless, foster* and their kin, plus sentence-initial "Additionally,"/"Moreover," as default connectives. Fix: use the plain equivalent (*leverage* → *use*, *boasts* → *has*), and vary or drop transitions — not every sentence needs a connective. Full list with swaps in the reference file.

### 7. Copula avoidance and elegant variation

Two related over-corrections:

- **Avoiding plain "is/are":** "X serves as a", "X stands as" instead of "X is a". Use "is".
- **Elegant variation:** swapping in synonyms to avoid repeating a noun ("the film… the picture… the feature…"). Calling the same thing by its name twice is fine and clearer.

### 8. Formatting tells (lower priority, but easy wins)

- **Boldface spam:** bolding every key term. Use bold rarely; in running prose, usually none.
- **Inline-header bullet lists:** the "**Term**: description" format repeated for every item. Use prose, or vary the list shape.
- **Em dashes:** overused where a comma, colon, parenthesis, or full stop would do. Use sparingly. *(If the user has a stated preference against em dashes, follow it strictly.)*
- **Title Case Headings:** use sentence case unless house style says otherwise.
- **Curly quotes / special characters** pasted into plain-text contexts: match the surrounding document's convention.
- **Emoji as decoration or section markers:** drop unless the genre and user clearly call for them.

### 9. Register leaks (a dead giveaway — always remove)

Chatbot-to-user habits that have no business in finished text: conversational openers/closers (*Certainly!, I hope this helps, Let me know if…*), sycophancy (*Great question!*), knowledge-cutoff disclaimers (*as of my last update*), placeholder text (*[Company Name]*), and meta-commentary about the writing itself (*"In this section we will explore…"*). Full phrase lists in the reference file.

---

## Final self-check pass

Before delivering, scan the draft against this checklist:

1. Any sentence that puffs up importance or ties a detail to a "broader" theme? → cut or ground it.
2. Any participle tail clause (*highlighting…, reflecting…*) doing fake analysis? → cut or make it a real claim.
3. Any "not just X but Y" or other negative parallelism? → keep at most one in the whole piece.
4. Any rule-of-three lists, including structural triples? → vary the count or replace with a concrete.
5. Vocabulary density check — count the offender words (see reference file). More than a couple? → swap for plain words.
6. Every "is/are" dodge → restore plain copula. Every synonym swap to avoid repetition → revert if it hurts clarity.
7. Boldface, em dashes, Title Case, curly quotes, emoji → all at minimum / matched to house style.
8. Any conversational boilerplate, cutoff disclaimer, placeholder, or meta-commentary? → delete.
9. Rhythm check: are sentence lengths actually varied — at least one short punch, at least one long run? If everything landed at uniform medium length (common after heavy cutting), recast.
10. Read it aloud in your head. Does any sentence sound like a brochure or a chatbot being helpful? → recast it.
11. Did the edits change any of the author's actual facts or claims, or add color the source doesn't support? → they must not have.
