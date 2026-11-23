---
name: charles-learn-anything
description: "Teach any topic as a short interactive lesson that opens in Chrome: one idea per screen, each hung on a real-life example, the key terms and an outline first, a predict-first question where people usually guess wrong, small demos to play with that change on the word the narrator says, stand-out facts, dot jots under every step, an acronym or phrase when there's a set to remember, quick checks with instant feedback, and a natural voice that reads along with each word highlighted at the speed you pick. Use when someone says teach me, help me understand, learn anything, walk me through, explain X step by step, make me a lesson on X, or I want to actually get X, and wants to understand a concept fast and properly rather than read a long answer."
---

# Goal

In 4 to 6 minutes of narration, the learner understands one topic well enough to explain it and get the quiz right. The lesson is a page on their computer that opens in Chrome. Building it takes about 10 minutes of your time: the kit already does the page, the player and the voice, so you only write the lesson and at most a few small demos.

Lessons live in `~/Learn/<topic-slug>/`: `lesson.json`, optionally `widgets.js` (the demos) and `assets/` (images). `examples/anti-aliasing/` is a complete lesson to copy from.

# Steps

## 1. Pin down one topic and its promise

Write the lesson's promise in one sentence: "Why slanted lines look jagged on screens, and how computers smooth them." If the request is a whole field ("teach me machine learning"), take the first 6-minute layer, say that's what this lesson covers, and offer the next layer at the end.

Why: a lesson that tries to cover a field teaches none of it. One layer learned properly sticks and makes the next one easy.

## 2. Outline 4 to 7 steps, concrete first

- One idea per step, and the step's title is the idea as a statement ("One check per pixel makes a staircase"), never a label ("Sampling").
- Order them: what they can already see or know, then how it works, then the fix or the variations, then where they'll meet it.
- Narration is at most 900 words in total (6 minutes at 1x) and at most 150 words per step (about a minute).

Why: engagement with lesson videos falls off past 6 minutes, and short segments the learner moves through beat one long stream (segmenting, d 0.67). Titles that state the idea work as a summary on their own.

## 3. Pick 2 to 4 key terms

Put the terms the lesson can't do without in `terms`, each defined in one plain sentence. The intro screen shows them with the outline before step 1.

Why: learning the names of the parts first frees attention for how they work (pre-training, d 0.78), and an outline up front tells them where it's going (signaling, d 0.70).

## 4. Choose each step's visual

```
What is this step's idea?
├── How something changes as you vary one thing (size, speed, amount) → a demo with one control
├── A process that unfolds over time → an animation, changed by cues in the narration
├── A before and after, or two ways compared → one picture with a toggle, or two side by side
├── The parts of a thing and how they connect → a diagram with the labels on the parts themselves
└── A definition, a list or some history → no visual (the step is text only)
```

- At most 2 controls per demo, and its starting state already shows the point before anyone touches it. Why: most readers never touch a control, so the demo has to teach as a picture first, and open-ended exploration fails beginners.
- At most 3 demos per lesson. Reuse one demo across steps with `widgetOptions` (the anti-aliasing example uses one demo for four steps). Why: demos are the slowest part to build and the likeliest to break.
- Put `[[name]]` in the narration right before the word where the picture should change, and make the demo's `cue(name)` do that change. Why: changing the picture on the word that describes it is the strongest effect in the research (temporal contiguity, d 1.31).
- Labels go on the parts, never in a legend (spatial contiguity, d 0.82).
- Never add decorative images, stock photos, mascots or music. Why: they cost attention and teach nothing (coherence, d 0.86).

`references/widgets.md` has the demo helpers and how to draw.

## 5. Hang every step on a real-life example

Pick each step's example before you write its narration:

```
What will the learner recognise?
├── Something they use or see every week (their phone, a game, an app, a TV) → use that
├── Something well known they've seen or heard (a film, a product, a song, a landmark) → use that
└── Nothing real shows it → a made-up case with real numbers
```

- Name it specifically ("a 1080p TV", "the wheels in old westerns"), never "a screen" or "a film", and put it right before or right after the idea it shows.
- Real numbers wherever there are any.

Why: an idea tied to something the learner already knows has somewhere to attach, and the example is what they remember first and rebuild the idea from ("the wagon wheels"). Illustrative examples help people learn abstract concepts, and an abstract statement on its own is the first thing forgotten.

## 6. Write the narration like a great teacher talking

The `say` text is both read aloud and shown with each word lit as it's spoken.

- The step's point is its first sentence.
- Bold a technical word the first time it's used (`**coverage**`), at most 3 a step, and define it in the same sentence. The 2 to 4 the whole lesson depends on also go in `terms`, which shows their definitions when someone taps them. Never point at anything the learner hasn't seen. Why: bold marks what's new, and when everything is bold nothing is.
- At most one analogy in the lesson, two only if two ideas are genuinely abstract. Map it, say where it breaks, then go back to the real thing.
- Write for the ear: no symbols ("→", "≥", "e.g.", "vs."), no code, no parentheses doing real work, and every abbreviation spelled out the first time, unless the full name explains nothing (for ISO, say what it does instead). Leave out names the voice will likely mispronounce. Why: whatever only works on the page sounds broken when the voice reads it.
- "You", short sentences, no "simply", "just" or "obviously".

Why: a conversational style with "you" helps people learn (personalization, d 1.00), and the voice reads exactly what's written.

## 7. Make it stick

**Stand-out facts.** Put 1 to 3 in the lesson. A stand-out fact is true, specific and non-obvious, the kind that makes someone say "wait, really?" ("CDs sample sound 44,100 times a second, just over twice the highest pitch you can hear"), and it explains or extends the step's idea. Never trivia for its own sake.

- Give each one its own paragraph starting with `> `, at most 40 words. The page shows it as a callout, and the voice reads it like any other paragraph.
- Only facts you've checked against a source you trust: official documentation, a paper, or an established publication that says where its number came from. If you can't confirm one, leave it out; if sources disagree on a number, leave the number out; and never round a number to make it more striking. Check every other number in the narration the same way.

Why: surprise and curiosity make people remember, and a line set apart from the rest is remembered better than the same line mid-paragraph. They're also the facts people repeat to friends, so a wrong one spreads.

**Dot jots.** Give every step `jots`: 2 to 4 bullets of at most 8 words each, the step's points as the learner would write them in their notes. The page lists them under the narration and the voice doesn't read them, so numbers and symbols are fine, in the narration's names and notation. Write them fresh; never copy a sentence from the narration.

Why: a short list to glance back at is how people review and find their place again, and 2 to 4 items is what working memory holds at once. Copied sentences only make them read the same thing twice.

**Memory aids.**

```
Does the lesson have a fixed set of 3 or more things to remember (stages, types, causes, rules)?
├── No → no memory aid
└── Yes → Do the items' names or key words start with letters that spell a word or a pattern?
    ├── Yes → an acronym of those letters
    └── No → one short phrase that links them in order ("edges, image, time" for MSAA, FXAA and TAA)
```

- When the lesson has more than one set, pick the one they're most likely to mix up or forget the order of.
- Say it in the narration as a `> ` callout, and put it in that step's jots.
- At most 2 per lesson. Never an acronym that needs explaining itself, or a letter that stands for a stretched word.

Why: a memory aid helps people recall a set and its order, but only a fixed set, and a forced one is one more thing to learn.

## 8. Add questions where they do work

- `predict` on 1 or 2 steps, the ones where people usually guess wrong. It's asked before the step, whose text and picture stay blurred until they answer. Make sure `terms`, the intro and the steps before it don't give the answer away. Why: a question asked before the answer improves memory for exactly that point (g 0.54), mostly through the surprise of being wrong, so it's wasted on easy points.
- `check` on 2 to 4 steps: one question about that step, shown when the narration ends. Why: answering from memory with the explanation right after it is one of the most reliable ways to learn (g 0.50).
- `quiz`: 3 questions across the whole lesson, and `recap`: 3 to 5 one-sentence takeaways.
- Every question has 2 to 4 choices with one clearly right, wrong choices that are the real misconceptions and use only what the lesson has taught by then, and a `why` of one or two sentences that explains the right answer.

## 9. Build, open and check it

```bash
python3 <this skill's folder>/kit/build.py ~/Learn/<topic-slug> --open
```

- The voice: Kokoro on fal.ai when `FAL_KEY` is in the environment or a `.env` (in the lesson folder, the folder you run from, or your home folder). It sounds natural and costs about $0.02 per 1,000 characters, so about $0.12 for a 900-word lesson, and every sentence is cached, so a rebuild only pays for what changed. Without a key, the page reads with the browser's own voice for free, which sounds more robotic. Never pay for a voice the user didn't ask for.
- Fix every error the build prints. It checks steps, questions and demo names.
- Then open every step once with the audio muted and confirm the demo draws, its controls work, each cue lands on its word and the predict step unblurs after an answer. Why: a broken demo in step 2 ends the lesson.

# Deliver

The page open in Chrome, and in the chat: where it is (`~/Learn/<topic-slug>/build/index.html`), how long it is ("6 steps, about 4 minutes at 1x"), what the voice cost, and the shortcuts (Space plays and pauses, the arrow keys move between steps, [ and ] change the speed). Never paste the lesson into the chat.

# lesson.json

```json
{
  "title": "Anti-aliasing",
  "subtitle": "The promise from step 1, in one sentence.",
  "terms": [{ "term": "pixel", "def": "One plain sentence." }],
  "steps": [
    {
      "id": "staircase",
      "title": "The idea, as a statement",
      "predict": { "q": "…", "choices": ["…", "…", "…"], "answer": 0, "why": "…" },
      "say": "Paragraphs, separated by a blank line. **Terms** in bold. [[cue]]A cue fires on the next word.\n\n> A stand-out fact or a memory aid: its own paragraph, starting with > .",
      "jots": ["Two to four notes", "At most 8 words each"],
      "widget": "pixels",
      "widgetOptions": { "any": "settings this step's demo reads" },
      "image": "assets/diagram.png",
      "caption": "One line under the picture.",
      "check": { "q": "…", "choices": ["…", "…"], "answer": 1, "why": "…" }
    }
  ],
  "recap": ["…"],
  "quiz": [{ "q": "…", "choices": ["…", "…", "…"], "answer": 2, "why": "…" }]
}
```

Only `title`, `steps`, and each step's `title` and `say` are required. Use `widget` or `image`, not both.
