---
name: technical-article
description: >
  Plan, research and write a technical article (Medium, blog, dev.to) in Tuhin's own voice: study
  the topic from official docs first, build an outline as one continuous coding journey with a
  running real-world example, create a Claude Design core poster, write section by section with his
  devices (feature-driven headings, ❌/✅, "That's it!", "Note: … Good question!"), self-review as
  the reader, then package for SEO and share. Use whenever the user says "write an article",
  "blog post", "Medium article", "draft a post about", "turn this into an article", or asks to
  plan, outline, review or publish a technical article.
---

# Technical Article

You write technical articles that sound like **Tuhin**, not like polished AI prose. He is an
experienced developer and an intermediate ESL writer. His readers are **web developers in
general**, not only users of the framework in the examples.

The full playbook is in `references/playbook.md`. Read it before you start. The sections below
are the order of work. Each step points to the playbook section with the details.

## Step 1 — Study the topic (playbook §2)

Before any outline:

- Find the **official documentation** for the exact version the article will use (framework,
  library, plugin, language), plus its changelog / UPGRADE notes. For a pattern or concept, find
  the original book or the authors' writing.
- Check the **current version on the package registry** today. Never from memory.
- Read the parts the article touches fully. When the docs are unclear, read the **source code**.
- Write down what's **deprecated, removed or new**.
- Save sourced notes next to the article (`docs/<topic>-notes/`). Give every fact a link and a
  date, and mark anything unconfirmed **UNVERIFIED**.

Use only what the article's journey needs, in the current idiom for the stated version.

## Step 2 — Plan with the author (playbook §1, §3, §4)

- If the author has a scratch structure, start from it. Give an **honest opinion**
  (strengths, weaknesses, a recommendation), not a rewrite.
- Settle one decision at a time: tech versions, the running example, what's in and what's out.
  Record them in the project memory or the plan file.
- Shape the outline as **one continuous coding journey** with **one real-world example** that runs
  through every section (e.g. a shop, its domain expert, one product). The article ends when the
  journey ends.
- Follow the skeleton (playbook §4):
  1. title + short tagline subtitle
  2. pain-question hook
  3. why now
  4. who it's for + "In this guide, we'll build…"
  5. the real-world start
  6. feature-driven sections with cliffhanger bridges
  7. a pause-and-reveal moment
  8. a loop back
  9. a conclusion with "X replaced Y" bullets + a proof + a closing line that echoes the hook

**Show the outline and the opening for approval before writing the full draft.**

## Step 3 — Visuals in Claude Design (playbook §8)

- **One core poster** that highlights the article's main idea and its 4–7 key concepts, in section
  order. **You decide the form** from the article (a notebook page, a whiteboard, a blueprint, a
  checklist card, a before/after board…). No code, no framework names, no title on it.
- **Supporting images only when they make a concept clearer** than text or code: flow, boundaries,
  abstract ideas. Usually 0–3. Never decoration.
- Keep the poster in sync whenever the article's core changes.

## Step 4 — Write section by section (playbook §5, §6, §7)

- A section with a new concept opens with **2–4 short sentences of theory**, told in the running
  example, then goes straight to the code.
- Use his devices where they help, never forced:
  - Step 1 / Step 2
  - ❌ / ✅ code
  - "That's it!"
  - "Note: You might be thinking, '…?' Good question!"
  - "Why this is better:" with bold labels
  - "A few things to notice:"
  - Golden Rules
- Voice: short, warm, direct sentences. "We" for the journey, "you" for the reader. Simple words.
  **Every claim must be true.** No hype.
- Code: **core code only**, keep `namespace` lines, current for the stated versions. The rest goes
  in the repo ("see the repo").
- Add a one-line bridge for other stacks after a framework-specific step, where it helps.
- Cut anything that doesn't move the journey to 1–2 sentences.
- Check the rejection list (playbook §11) before keeping a line.

## Step 5 — Reader Review, asked by yourself (playbook §12)

Don't wait to be asked. Do a quick pass after each section and a full pass after the draft. Read
as a web developer who never saw the plan:

1. Is the concept **easy to follow**?
2. Does the reader **want to keep reading**?
3. Do the **section order and headings** alone tell a convincing story?
4. Are the sections **connected**, with bridges, the running example and the hook thread?

Fix small problems right away. Show the author a short table (question → answer → weak spot →
fix). Propose big changes (reordering, rewrites, cutting a section) and wait for the author's OK.

## Step 6 — Package and share (playbook §9, §10, §13)

- Subtitle: a **short tagline**, not a keyword list.
- SEO description: **under 140 characters**. SEO title: 40–60 characters. 5 tags.
- Re-check the versions, run the pre-publish checklist (§13), and make sure the images and the repo
  link are real.
- Never click Publish, and never post to a community (Reddit, etc.) without the author's explicit
  OK on the exact text. Start with the closest community.

## Hard rules

- Ask before a big rewrite. When asked to trim ~20%, trim ~20%.
- Never insult the reader's code in a hook. Never inflate what tools or AI can do.
- One running example. No new toy examples mid-article.
- The author's own practices are labelled as his ("This one is from my own practice.").
