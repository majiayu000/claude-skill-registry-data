---
name: repurpose-post
description: >-
  Load this skill when adapting a finished blog post into a Twitter/X thread, LinkedIn post, TL;DR,
  or newsletter blurb. Trigger on "make a thread from this", "turn this into a LinkedIn post",
  "write a TL;DR". Not for an unfinished draft (use ceh-blog:edit-post).
argument-hint: "[post file or URL] [thread | linkedin | tldr | newsletter]"
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Repurpose post

Adapt a finished blog post into the requested channel formats. Every output must stand alone: the
reader shouldn't need the original post to get the value. Done means each requested format is
produced, labelled, and ends on the post's open thread or a plain link to it.

## Procedure

### 1. Identify the format(s)

If the user specifies format(s), proceed immediately. Otherwise ask once:

> _"Which format(s) would you like? I can produce:_
>
> _1. **Twitter/X thread** — opening tweet + numbered thread (up to ~12 tweets) + link close_
> _2. **LinkedIn post** — 150–300 words in the post's own voice, ends on its open thread_
> _3. **TL;DR** — 2–3 sentences: what happened or the claim, what was found, what's still open_
> _4. **Newsletter blurb** — 3–5 sentences teasing the post, ends with `[Read more →]`_
>
> _Any combination."_

With no human to answer (a headless run), produce all four, since each is cheap and dropping one
is easier for the author than asking again later.

### 2. Read the post

Identify: **the thesis** (the single central claim); **the key takeaway**; **the audience**; **the tone**; **length** (enough content to thread, or short-form?).

**Series awareness**: if the post is an episode in a series, the adaptation is the reader's entry point into the whole serial, so use that. The thread's closing link or the newsletter blurb can point at the series ("part 3 of the [X] build — start at part 1: [link]"), and the post's open thread (what's unresolved, what comes next) is natural enticement material: it promises a next episode without manufacturing a cliffhanger. Don't spoil an earlier episode's payoff in the adaptation.

**No clear thesis**: flag before repurposing, because a fuzzy post produces fuzzy content. Offer to sharpen first (suggest `/ceh-blog:edit-post`) or proceed as-is, and wait for the answer.

**Too short to thread** (under ~400 words or only 2–3 distinct points): flag it and recommend LinkedIn or TL;DR instead. If they insist, produce the best thread possible and note where it feels thin.

### 3. Produce the output(s)

Produce every requested format, each labelled with a `##` heading, in order: Thread → LinkedIn → TL;DR → Newsletter blurb.

**Format 1: Twitter/X thread**

```
[Opening tweet]     — the post's opening moment or thought, standalone
[Tweet 2]           — the setup
[Tweets 3–N]        — one beat per tweet, numbered ("2/")
[Closing tweet]     — the open thread, then the link
```

- **Opening tweet**: must work standalone — no "A thread on…" filler. Open where the post opens: inside a moment or a thought, in the author's words. Not a teaser line engineered to stop the scroll.
- **Numbered tweets** ("2/" style from tweet 2): each must make sense on its own — rewrite anything that only makes sense via the previous tweet. No same-sentence-split continuations. Full sentences in the post's register, not staccato one-liners.
- **Length**: ≤ 280 characters each — count carefully on long ones.
- **Count**: as many as the post's beats support, usually 5–12, with no filler. If the post only supports 4 good tweets, make 4.
- **Closing tweet**: the post's open thread in a sentence, then `[link]`. No follow invite, no reply-bait question, not "That's it!"
- **Hashtags**: 0–1 total, only if genuinely relevant.

**Format 2: LinkedIn post**

```
[Lead]              — the post's opening moment or thought
[Body]              — the story or argument, compressed (2–4 short paragraphs)
[Close]             — the open thread, then [link]
```

- **150–300 words** — one idea developed properly, readable in full.
- **Lead inside the moment, not with backstory or a pitch** — the first two lines show above "see more", so they carry the post's opening, not "I've been thinking about X lately" and not a lesson stated upfront.
- **Match the original post's tone**: technical stays technical, personal stays personal, so the writer's voice survives the adaptation.
- **Connected paragraphs**: 2–4 sentences each, blank line between. No one-line-per-paragraph broetry.
- **0–2 hashtags**, only genuinely descriptive ones. In doubt: zero.
- **End on the open thread** — what's unresolved or what comes next, then `[link]`. No engagement question.

**Format 3: TL;DR**

```
[Sentence 1]    — the thesis / core argument
[Sentence 2]    — the key insight or supporting evidence
[Sentence 3]    — the open thread (what's still unresolved or next)
```

- **2–3 sentences**, no more. A fourth means one of the three is doing too much.
- **Must stand alone** for someone who never saw the post.
- **Active voice, first person** where the post is first person: "I found X causes Y", not "Y is caused by X".
- **No jargon** unless the audience uses it daily.
- **Capture the substance, not a summary of it**: state what happened or the actual claim, not "This post is about…". No advice to the reader.

**Format 4: Newsletter blurb**

```
[Tension or hook]       — a question, problem, or tension the post resolves
[Brief context]         — enough setup to care
[Payoff hint]           — gesture at the insight without giving it away
[Link placeholder]      — [Read more →]
```

- **3–5 sentences** — enough to create intrigue, not enough to replace the click.
- **Tension, not summary**: pose the question the post answers or name the problem it solves. The reader should finish wanting the answer.
- **Don't give away the key insight**: if the thesis is "X is the wrong approach", raise the problem X solves and don't reveal that X is wrong. That's the click.
- **End with `[Read more →]`.**

## Rules

**Voice.** The adaptation carries the post's personal voice onto the platform. It does not switch
to platform-native influencer style. If the target repo's `CLAUDE.md` defines a blog voice, it
overrides the format rules above.

- **Banned tells apply here too:** punchy standalone one-liner paragraphs; aphoristic closers; imperative lessons aimed at the reader ("Don't design your own. Surface theirs."); "If you're building X, then Y" prescriptions; bold pseudo-headers as section labels; tidy meta-takeaway sign-offs; CTA endings ("follow for more", "what do you think?").
- **Never invent** a scene, feeling, number, or claim the post doesn't contain. The adaptation compresses the post, it doesn't add to it. Reuse the post's own sentences where they fit.
- **Endings:** each format ends on the post's open thread or a plain link to it, never a lesson and never an engagement prompt. A bare `[link]` is a link, not a CTA.
- **Highly technical post**: keep the technical language, don't dumb it down.
- **Personal or emotional post**: preserve the honest voice, don't make it corporate.
- **Post is on disk**: read it from the file, and don't overwrite the post.

## Output

Single format: output directly with a format label. Multiple: `##` heading per format in the order above.

Save each format to its own file, `<slug>-<format>.md` (`thread`, `linkedin`, `tldr`, `newsletter`): next to the post when it is on disk, otherwise in `.agents_workspace/blog/` with the slug from the post's title in kebab case. A re-run overwrites the format files, never the post. Say where they were saved.

After delivering, ask: _"Anything you'd like adjusted — tone, length, a specific tweet, the LinkedIn opener?"_ Also offer **one proactive observation**, something you'd refine even if they're satisfied. Common candidates: opening tweet reads as summary rather than a moment; LinkedIn opener starts with backstory; a banned tell crept in during compression; blurb gives away too much.

## Stop conditions

- No clear thesis → flag it, offer to sharpen first or proceed as-is, and wait.
- Too short to thread → flag it and recommend LinkedIn or TL;DR instead.
