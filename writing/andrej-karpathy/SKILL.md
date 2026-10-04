---
name: karpathy-article-writing
description: Write technical blog posts in the voice of Andrej Karpathy — first-person, build-from-scratch, mixing deep technical substance with conversational warmth, dry humor, vivid analogies, and intellectually honest hedging. Use when the user asks for a post "in Karpathy's style," a "Karpathy-flavored" writeup, or wants to turn an experiment/reproduction/tutorial into something that reads like karpathy.github.io.
---

# Writing in Karpathy's Style

This skill distills the voice found across four reference posts:

- *A from-scratch tour of the Bitcoin protocol in Python* (2021) — a dense technical tutorial
- *Short story on AI* ("Forward Pass", 2021) — speculative fiction from a model's POV
- *Biohacking Lite* (2020) — a year-long self-experiment written up
- *Deep Neural Nets: 33 years ago and 33 years from now* (2022) — a paper reproduction + retrospective

The voice is the same across all four despite the wildly different genres. That voice is what this skill captures.

---

## The five-word north star

> **Curious. Built it. Write it up.**

Karpathy doesn't opine; he *makes* things and then reports back on what he found. If the piece isn't grounded in something the author actually did — implemented, reproduced, measured, lived through — the voice falls apart. Before writing, make sure there's a concrete artifact (code, data, a lived experiment, a reproduction) at the center.

---

## Voice rules

### First person, always
- "I" for the author's actions, opinions, hedges: *I set out to reproduce…*, *I suspect…*, *I was a bit sketched out about…*
- "We" for collaborative walkthroughs where the reader is coming along: *we are going to…*, *we now have…*
- Avoid passive constructions. *The weights were initialized* → *I initialized the weights* (or *we initialize the weights*).

### Conversational, but never dumbed down
- Use domain jargon without defensive scaffolding. UTXO, ECDSA, MACs, glycogen, oxidative phosphorylation — drop them in, gloss only if they're genuinely load-bearing for the next sentence.
- The reader is assumed smart and curious. Trust them.
- No "let me explain X in simple terms" framing. Just explain it.

### Intellectual honesty via hedges
Karpathy hedges *constantly*, and it reads as honesty rather than weakness because the hedges are about things genuinely uncertain:
- *I suspect…*
- *most likely…*
- *I believe the…*
- *probably…*
- *as far as I can tell…*
- *¯\\_(ツ)_/¯*

Use a hedge when you're interpreting, speculating, or reading between the lines. Don't hedge on things you actually verified.

### Self-deprecation, dry and confident
The humor is never anxious. It's the humor of someone who's comfortable with what they know *and* what they don't:
- *hah never thought I'd say that*
- *a bit too much of the mad scientist crazy out*
- *yolo*
- *Uh, hello???*
- *it's highly amusing to think that…*

Never self-deprecate about competence in a way that undermines credibility. The joke is usually about scope, taste, or life choices — not about whether the technical work holds up.

### Enthusiasm shows through precision
Don't write *"this is really cool!"*. Write the specific number that makes it cool:
- *approximately 3,000X faster*
- *100,000,000X more pixel data*
- *reduced errors from 82 to 32 test mistakes — roughly 60% error reduction*
- *lost 35 pounds over the year*

Exact quantitative comparisons do the emotional work. Adjectives are cheap; multipliers are earned.

---

## Structural moves

### Opening
Pick one of these. Never bury the lede.

1. **Historical/significance hook.** *"The 1989 paper by Yann LeCun et al. is, as far as I know, the earliest real-world application of a neural network trained end-to-end with backpropagation."*
2. **Personal framing / first-person setup.** *"Throughout my life I never paid too much attention to what I eat…"*
3. **Build-from-scratch declaration.** *"In this post we are going to implement a Bitcoin transaction from scratch in pure Python, with no external dependencies."*
4. **Philosophical epigraph.** Karpathy loves *"What I cannot create, I do not understand"* — Feynman. A single quote at the top is on-brand if it genuinely frames the piece.

Keep the opening to one short paragraph. Don't stack multiple hooks.

### Middle
- **Short paragraphs.** Often 2–4 sentences. Sometimes one.
- **Topic sentences up front**, frequently bolded or posed as a question: *"**So how much does our body weigh?**"*, *"**What changed and what didn't.**"*
- **Numbered/bulleted lists** for mechanisms, steps, or observations. Don't use them for everything — they punctuate the prose, they don't replace it.
- **Embed results inline.** Code output, training curves, measurements — drop them into the narrative as they come up, not in a separate "Results" section at the end.
- **Parenthetical asides.** Liberal. They add color without blocking flow: *(hah never thought I'd say that)*, *(btw if the visual format of this article…)*, *(I suspect)*.
- **Em-dashes and ellipses for rhythm.** *"Training took 3 days on a SUN-4/260 — today it takes 90 seconds on my MacBook Air."*

### Closing
- **Extrapolate.** If you looked backward, now look forward. *"Projecting forward to 2055…"* The future-looking paragraph is a Karpathy signature.
- **Or end with casual irreverence.** *"Okay great. I'll now go eat some cookies, because yolo."* This works when the piece was personal/experimental.
- **Or: list pointers for further exploration.** Books, papers, repos, exercises left to the reader.

Don't write a dutiful "Conclusion" heading that recaps what you just said. Recapping is for the reader, not for you.

---

## Signature techniques

### Analogies from adjacent domains
Karpathy reaches across fields for analogies. Computer memory hierarchies to explain biological energy stores. "Slow-motion combustion" for cellular respiration. "Fancy bit mixers" for hash functions. "A molecular spring" for ATP.

**Rule:** when introducing a mechanism, find the closest physical-world analogy and use it *once*. Then return to the technical vocabulary. Don't belabor the metaphor.

### The time-travel conceit
Two of the four reference posts center on this: going back to old work (LeCun 1989, early Bitcoin) and asking *what would I do differently now?* or *what has actually changed?* It's a powerful organizing device because it naturally produces the two things Karpathy does best: concrete quantitative comparisons, and speculation about the future.

If the piece is about an old paper, technique, or artifact — frame it this way.

### Build it, then explain it
The code or experiment is the primary artifact. Prose exists to contextualize it. A typical flow:

1. One paragraph of motivation / why this matters.
2. A conceptual sketch of the thing (1–3 paragraphs).
3. **Implementation**, often step-by-step, with code blocks interleaved with short explanations.
4. **Results**, measured and compared, ideally with surprising numbers.
5. **Reflections** — what was harder than expected, what was easier, what's next.
6. **Looking forward or outward** — implications, open questions, links.

### Mixed register
A single paragraph can contain: a research citation, a line of Python, a shrug emoticon, an exact multiplier, and an em-dash aside. This is not a bug — it's the texture. Don't sanitize into uniform academic prose. Don't sanitize into uniform casual prose either. The *mix* is the voice.

### Fiction is fair game
*Forward Pass* is speculative fiction written from a model's first-person perspective. If the topic lends itself to a vignette, a short story, or a thought experiment, Karpathy will write one. Don't feel bound to the expository format — just keep the voice (curious, technically precise, dryly funny, first-person).

---

## Anti-patterns (don't do these)

- **Don't write marketing copy.** No *"unlock the power of…"*, *"in today's rapidly evolving landscape…"*, *"dive deep into…"*. Karpathy would never.
- **Don't over-explain.** If the reader needs to google a term, that's fine. The post isn't a textbook.
- **Don't hide behind the passive voice** to sound authoritative. The voice *is* the "I."
- **Don't use corporate hedges** (*"it could be argued that,"* *"one might consider"*). The hedges should be genuinely epistemic (*I suspect*, *most likely*), not rhetorical armor.
- **Don't pad with transitional throat-clearing** (*"Now that we've covered X, let's turn to Y"*). Just turn to Y.
- **Don't fake the artifact.** If there's no real code, reproduction, or lived experiment behind the post, the voice won't work. Insist on the artifact first.
- **No emoji in the prose** unless it's the *¯\\_(ツ)_/¯* shrug or a similarly load-bearing unicode joke. No 🚀, ✨, 🎉.
- **Don't end with "Thanks for reading!"** or a call to subscribe. Just stop when you're done.

---

## A before/after example

**Generic tech-blog voice:**
> In this article, we will explore how modern optimization techniques can be applied to improve the performance of classic neural network architectures. Through a series of carefully designed experiments, we demonstrate that significant gains are possible even with minimal architectural changes. Our findings have important implications for the field.

**Karpathy voice:**
> So I set out to reproduce LeCun et al. 1989 in PyTorch and see what would happen if I showed up from the future with 33 years of tricks. Swapping MSE for cross-entropy, SGD for AdamW, and adding a single pixel of data augmentation knocked test errors from 82 down to 32 — about 60% — without touching the architecture. The inference cost is identical. Training time went from 3 days to 12 (on the same tiny net), which, hah, is the opposite of what you'd hope for, but the network is so small that the GPU is mostly sitting idle anyway.

Notice: first-person. Specific numbers. A concessional aside (*hah, opposite of what you'd hope*). Casual mechanics (*showed up from the future*). No marketing cadence.

---

## Quick checklist before publishing

Run through these. If more than one or two are failing, the piece isn't there yet.

- [ ] Is there a real artifact (code, reproduction, experiment, lived event) at the center?
- [ ] Does the opening get to the hook in one short paragraph?
- [ ] Am I in first person throughout, with "we" only when walking through a build?
- [ ] Are there at least two exact quantitative comparisons (Xx, percentages, before/after numbers)?
- [ ] Is there at least one cross-domain analogy, used once and then dropped?
- [ ] Did I hedge honestly (*I suspect*, *most likely*) where I'm actually uncertain?
- [ ] At least one dry, self-aware aside — parenthetical or em-dashed?
- [ ] Does the closing either extrapolate forward, end with casual irreverence, or offer pointers — *not* recap?
- [ ] No marketing verbs, no passive-voice throat-clearing, no emoji padding?
- [ ] Would a reader finish it feeling that the author *made the thing* rather than *described the thing*?

---

## Ready-to-use skeleton

```
> "What I cannot create, I do not understand." — Feynman   [optional]

[One short paragraph: why this artifact, why now. Personal stake or historical hook.]

[One or two paragraphs of conceptual setup. Introduce the key analogy.]

**[Bolded section header posed as a question or a declarative fragment]**

[Prose interleaved with code / math / data. Short paragraphs. Parenthetical
asides OK. Embed results inline as they come up.]

**[Next section]**

[More prose + artifact. Exact quantitative comparison lands somewhere here.]

**Reflections**

[What was surprising. What was harder or easier than expected. Hedges here
are fine and expected.]

**[Looking forward / looking outward]**

[Extrapolate. What does this pattern suggest for N years from now? Or:
casual irreverent sign-off. Or: pointers to further reading / code repo /
exercises left to the reader. Pick one — don't do all three.]
```

Use this as scaffolding, not as a template to fill in mechanically. The voice only works when the author is genuinely present in the prose.
