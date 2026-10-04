---
name: article-writing
description: Write articles, guides, blog posts, tutorials, newsletter issues, and other long-form content in a distinctive voice derived from supplied examples or brand guidance. Use when the user wants polished written content longer than a paragraph and voice consistency, structure, and credibility matter. Do NOT use for short social posts or threads (content-engine), for deriving the voice profile itself (brand-voice), or for search-brief work (seo).
origin: ECC
---

# Article Writing

Write long-form content that sounds like a real person or brand, not generic AI output.

## When to use

- drafting blog posts, essays, launch posts, guides, tutorials, or newsletter issues
- turning notes, transcripts, or research into polished articles
- matching an existing founder, operator, or brand voice from examples
- tightening structure, pacing, and evidence in already-written long-form copy

**When NOT to use:**

- the deliverable is a tweet, thread, or LinkedIn post — that is `content-engine`
- the job is to derive a reusable voice profile rather than write — that is `brand-voice`
- the required facts do not exist yet. Long-form without sourced material produces invented
  biography and invented metrics, which is the worst failure this skill has (see Failure modes)

## Inputs

Required before drafting — **absent input = stop and ask, never invent**:

1. **Audience and purpose** — who reads it, what they should be able to do afterwards.
2. **Source material for every factual claim** — notes, transcripts, docs, research, or a live
   probe. For SkyyRose content: product facts come only from
   `wordpress-theme/skyyrose-flagship/data/skyyrose-catalog.csv`, collection language only from
   `docs/brand/collection-stories.md`, founder voice only from `docs/brand/corey-questions.md`.
   Never a biographical or metric claim from memory.
3. **Voice reference** — a `VOICE PROFILE` from `brand-voice`, or 3+ real samples (published
   articles, newsletters, X/LinkedIn posts, docs, memos, a style guide). If none exist, default
   to a direct operator voice: concrete, practical, low on hype — and say that is what you used.

## Procedure

1. Confirm audience, purpose, sources, and voice reference.
2. Extract from the voice samples: sentence length and rhythm · formal vs conversational vs
   sharp · favored devices (parentheses, lists, fragments, questions) · tolerance for humor,
   opinion, contrarian framing · formatting habits (headers, bullets, code blocks, pull quotes).
3. Build a skeletal outline with **one purpose per section**.
4. Draft each section starting with the concrete thing — example, output, anecdote, number,
   described screenshot, or code block. Explain *after* the example, never before.
5. Expand only where the next sentence earns its place. Prefer short direct sentences.
6. Attach a source marker to every number and every factual claim as you write it
   (`(Source: …)`), so check 3 below can be run mechanically rather than by re-reading.
7. Apply the structure pattern for the format:
   - **Technical guide** — open with what the reader gets; a code or terminal example in every
     major section; end with concrete takeaways, not a soft summary.
   - **Essay / opinion** — start with tension, contradiction, or a sharp observation; one
     argument thread per section; examples that earn the opinion.
   - **Newsletter** — strong first screen; insight mixed with updates, not diary filler; clear
     section labels and easy skim structure.
8. Run the Verification checks on the draft file before delivering.

# Verification

Write the draft to a real file so the checks have a target. `grep` exiting 2 means the file path
is wrong — a **dead gate, not a pass** (bug-230). Exit 1 is clean; exit 2 is broken.

1. **Banned-pattern scan** — the tropes that make copy read as AI output:

```bash
grep -nEi 'rapidly evolving|game.chang|cutting.edge|revolutionary|moreover,|furthermore,|excited to share|in today.s .* landscape' article.md
```

   **PASS:** exit 1, zero matches. Any hit gets deleted and rewritten, not softened. `[repro]`

2. **Heading structure** — one purpose per section starts with one H1:

```bash
grep -c '^# ' article.md
```

   **PASS:** prints `1`. Two H1s means two articles; zero means no stated subject. `[repro]`

3. **Every number carries a source** — the check that stops invented metrics:

```bash
grep -nE '[0-9]+(\.[0-9]+)?%|\$[0-9]' article.md | grep -v 'Source:'
```

   **PASS:** exit 1, no lines returned. A number with no `(Source: …)` is either sourced now or
   deleted. `operator-supplied; unverified` is an acceptable source label; silence is not. `[repro]`

Prove check 3 can fail before trusting it (rule 3): drop one unsourced figure into the draft,
confirm the grep returns it, restore. Observed doing exactly this in the worked example.

**A SKIP is not a PASS:** if voice fidelity cannot be checked mechanically (it cannot — no
command grades tone), say so explicitly and name who closes it. The strongest available check is
mechanical: banned-pattern scan (check 1) plus a side-by-side read of one drafted paragraph
against a named source sample. The human requester closes the tone verdict, not the drafter.

## Worked example

Real run, 2026-07-28. Draft written to the session scratchpad as `article.md`, subject: the
one-run drop model, with the brand line from `docs/brand/collection-stories.md` `[repo]`.

```bash
$ grep -c '^# ' article.md
1
$ grep -nEi 'rapidly evolving|game.chang|cutting.edge|revolutionary|moreover,|furthermore,' article.md; echo "exit=$?"
exit=1
$ grep -nE '[0-9]+(\.[0-9]+)?%|\$[0-9]' article.md | grep -v 'Source:'; echo "exit=$?"
exit=1
```

The unsourced-number gate was proven red first, on a sibling file in the same run:

```bash
$ grep -nE '[0-9]+(\.[0-9]+)?%|\$[0-9]' research-brief.md | grep -v 'Source:'
3:- Average luxury-streetwear AOV is $240
```

After appending `(Source: operator-supplied; unverified)` to that line, the same command exits 1.
Both states observed this session `[repro]`. Passing the sourcing gate is what the article's
`30% unit-cost premium (Source: operator-supplied)` line exists to satisfy.

Dead-gate demonstration from the same run: `grep -nEi 'anything' no-such-file.md` printed
`no such file or directory` and exited **2** — zero matches, but not a pass `[repro]`.

## Failure modes

| Failure | What it looks like | Rule |
|---|---|---|
| Invented biography or metrics | "grew 4x in 18 months" with no source | Never invent biographical facts, company metrics, or customer evidence. Check 3 catches numbers; claims still need a human read |
| Hallucinated product/brand fact | wrong SKU, price, or collection story | bug-096 shape. Catalog CSV and `docs/brand/collection-stories.md` are the SOT; plausible ≠ sourced |
| Collection canon mixed | "bloodline" language outside Love Hurts | Each collection has its own canon; never substitute one collection's voice for another |
| Exit 2 read as clean | grep on a wrong path reported as "no banned patterns" | bug-230 fail-open. Exit 1 = clean, exit 2 = broken gate |
| Voice check silently skipped | delivered as "matches the voice" with no comparison | A SKIP is not a PASS. Name the sample compared against, or state the tone verdict is open and owned by the requester |
| Explanation before evidence | section opens with abstraction, example arrives late | Lead with the concrete thing; explain after |
| Filler transitions and hype | "Moreover", "game-changer", "cutting-edge" | Check 1 catches these mechanically — rewrite, do not soften |
