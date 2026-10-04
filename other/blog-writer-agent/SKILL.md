---
name: blog-writer-agent
description: "Daily-loop blog post factory inside a multi-channel content factory. Reads ideas from a SHARED ../raw-ideas/ library (immutable) and writes blog-specific outputs into ./blog-post/. Each run picks the oldest unconsumed idea (queue = ls raw-ideas/ minus this channel's TODO.md Done section), runs a 5-phase pipeline (Strategist → Content Writer → Title → Banner Prompt → SEO → Final Assembly), saves every handoff to a per-post folder, and updates TODO.md. The source idea NEVER moves — it stays in the shared library so other channels (LinkedIn, X, presentation) can also consume it. If no unconsumed ideas exist for the blog, the run exits quietly. Use when user says /blog-writer-agent, 'write a blog post', 'draft a blog about X', 'process my blog ideas', or when invoked via /loop. Always trigger this skill."
trigger: /blog-writer-agent
---

# /blog-writer-agent

A daily-loop Hashnode blog post factory. The user keeps dropping raw ideas into a folder; each invocation processes ONE new idea end-to-end and produces a publish-ready `.md` file — or no-ops if there are none.

---

## Project folder layout (canonical)

```
content-factory/                            ← project root
├── raw-ideas/                              ← SHARED, immutable, read-only from this skill
│   ├── 001-<slug>.md
│   └── 002-<slug>.md
├── blog.agent.md                           ← daily /loop prompt (calls this skill)
└── blog-post/                              ← Blog channel folder (this skill writes here)
    ├── README.md
    ├── CLAUDE.md
    ├── TODO.md                             ← Queue + In Progress + Done sections
    └── posts/                              ← one folder per generated post
        └── <slug>/
            ├── 01-content.md              ← Phase 1 output: full blog body
            ├── 02-title-options.md        ← Phase 2 output: 6-8 title options + recommendation
            ├── 03-banner-prompt.md        ← Phase 3 output: image generation prompt (for external tools)
            ├── 04-seo.md                  ← Phase 4 output: SEO title + description
            ├── blog-hero.svg              ← Image Designer output: SVG hero via /image-gen-agent
            └── final-post.md              ← Phase 5 output: complete Hashnode-ready .md
```

**`../raw-ideas/` is immutable.** Never move, rename, or delete files in it.

**Bootstrap on first run:** if `./blog-post/` doesn't exist, create `blog-post/posts/` and an empty `TODO.md` (template below). Then tell the user where to drop ideas and exit.

---

## Step 0 — Compute the queue and pick the idea

**Mode A — Loop / autonomous run** (no idea content passed in args, or invoked via `/loop`):

1. List files in `../raw-ideas/` (relative to `./blog-post/`). Accept `.md` and `.txt`.
2. Read `./blog-post/TODO.md`. Extract filenames listed in the **Done** section and the **In Progress** section.
3. Compute the blog queue:
   ```
   queue = (files in ../raw-ideas/) MINUS (Done filenames) MINUS (In Progress filenames)
   ```
4. Filter: drop any file whose frontmatter declares `channels: [...]` without `"blog"` in the list.
5. If queue is empty → print one line: `No new blog ideas. Skipping.`, write the run-log row with outcome `skipped` (see **Run log** below), and exit. Do not generate anything.
6. Otherwise pick the **oldest by filename sort** (lexical — `001-` runs before `002-`).
7. Read the chosen file. Its full content (minus frontmatter) is the **raw idea**.
8. Derive `<slug>` from the filename (strip extension AND any numeric prefix, kebab-case it).

**Mode B — Direct invocation with content in args** (user typed `/blog-writer-agent <idea text>`):

1. Treat the args as the raw idea.
2. Derive `<slug>` from the first 3-5 meaningful words.
3. Determine the next available numeric prefix in `../raw-ideas/` (e.g. if 001–005 exist, use 006).
4. Write the raw idea to `../raw-ideas/<NNN>-<slug>.md` so other channels can also consume it later. Then continue.

Create the per-post folder: `./blog-post/posts/<slug>/`.
Update `./blog-post/TODO.md`: move this idea's filename to **In Progress** with the date.

---

## Pipeline overview

```
[Raw Idea from ../raw-ideas/<NNN>-<slug>.md]
    ↓
Phase 1 — Content Writer     → 01-content.md  (full blog body, narrative arc)
    ↓
Phase 2 — Title Generator    → 02-title-options.md  (6-8 options, recommendation)
    ↓
Phase 3 — Banner Prompt      → 03-banner-prompt.md  (text prompt for Midjourney/DALL·E/Ideogram)
    ↓
Phase 4 — SEO                → 04-seo.md  (seo_title + seo_description)
    ↓
Image Designer               → blog-hero.svg  (SVG hero via /image-gen-agent)
    ↓
Phase 5 — Final Assembly     → final-post.md  (complete Hashnode-ready .md, first title from Phase 2)
    ↓
DO NOT touch ../raw-ideas/   (immutable, shared with other channels)
Update ./blog-post/TODO.md: move filename from In Progress → Done with link to post folder
```

All phases run sequentially, end-to-end, without interactive pauses. The skill is fully autonomous.

---

## Phase 1 — Content Writer

**Job:** Transform the raw idea into a complete blog body using the narrative arc: **problem → reframe → solution → real example → call to action**

### Section order (every post follows this)

1. **Opening hook** — a relatable situation, a universal mistake, or a provocative statement. Reader nods immediately. Never start with "In this post I will..."
2. **The problem** — name the pain clearly. Make the reader feel the frustration they've had but couldn't articulate.
3. **The reframe** — one insight that flips the mental model. This is the "aha" moment.
4. **The solution** — what it is and how it works. Plain language first, then mechanics.
5. **Real walkthrough** — a concrete before/after or step-by-step scenario. Use Altaf's actual experiences. Never invent corporate-sounding examples. If internal details are present (company names, ticket IDs, internal service names, private file names), generalise them — keep the flow and lesson intact, strip the specifics.
6. **What makes it different** — 3-4 sharp points, each with a bolded lead-in sentence
7. **When to use it** — a short flat list of the best moments
8. **How to install / use it** — practical, no fluff. Include both the Claude Code install AND the universal install section for other IDEs when the post introduces an installable skill (see Install Block below).
9. **Call to action** — one clear thing to try right now
10. **Reader engagement** — ask 2-3 specific questions inviting comments; ask for a like if it was useful; mention the next part is coming
11. **Series connector** — one line tying to the larger series arc

### At the top of the content, always insert this placeholder block

```
<!-- 
BANNER IMAGE
============
Generate this image using Midjourney, DALL·E, Ideogram, or any image tool, then upload to Hashnode as the cover image.

PROMPT:
[filled in from Phase 3]

Midjourney: append --ar 16:9 --style raw --v 6
DALL·E / GPT-4o: add "digital illustration, flat design, no gradients"
Ideogram: add "flat vector illustration, editorial style, tech blog"

DO NOT include: code on screens, company logos, text or titles, photorealism
-->
```

The PROMPT field is left as `[filled in from Phase 3]` at this stage. Phase 5 final assembly inserts the real prompt.

Print `[HANDOFF: CONTENT WRITER]` AND save to `01-content.md`.

---

## Phase 2 — Title Generator

**Job:** Generate 6-8 title options across distinct angles. Present grouped by angle with a clear recommendation. The **first title option** from Phase 2 is used as the display title in `final-post.md`; the full option list stays in `02-title-options.md` for Altaf to override by editing `final-post.md` directly.

### Angles to cover

- **Provocative** — challenges their current habit ("You've Been Talking to AI Wrong")
- **Curiosity** — makes them want to know what's inside ("What If AI Asked the Questions Instead?")
- **Outcome** — leads with the result ("From Tickets to PR With Zero Rework")
- **Flip** — inverts the expected ("Stop Briefing AI. Let It Interview You.")

### What makes a good title for this series

- Short — ideally under 8 words
- Feels like something a developer would stop scrolling for
- Hints at a mental model shift, not just a topic
- Doesn't give everything away
- Works as a standalone thought even without reading the post

Print `[HANDOFF: TITLE GENERATOR]` AND save to `02-title-options.md` using this format:

```
## Title Options

### Provocative
- <option>
- <option>

### Curiosity
- <option>
- <option>

### Outcome
- <option>

### Flip
- <option>
- <option>

---

**Recommended:** <title>
**Why:** <one sentence — what angle it takes and why it fits this post's content>
```

---

## Phase 3 — Banner Prompt

**Job:** Write a text prompt Altaf can paste into Midjourney, DALL·E, or Ideogram. Do NOT generate images — only the prompt.

The prompt must describe the *feeling and concept* of the post — not the content. Think editorial magazine cover, not a screenshot or diagram.

### Every banner prompt must include

- The atmosphere and mood (dark, minimal, editorial, tech)
- The core visual metaphor that captures the post's idea
- Wide banner format, 16:9 ratio
- Explicit instruction: no text, no logos, no code, no photorealism
- Style modifiers for each tool: Midjourney (`--ar 16:9 --style raw --v 6`), DALL·E ("digital illustration, flat design, no gradients"), Ideogram ("flat vector illustration, editorial style, tech blog")

Print `[HANDOFF: BANNER PROMPT]` AND save to `03-banner-prompt.md` using this format:

```
## Banner Image Prompt

**Core metaphor:** <one sentence describing the visual concept>

**Prompt (universal base):**
<the prompt text>

**Tool modifiers:**
- Midjourney: append `--ar 16:9 --style raw --v 6`
- DALL·E / GPT-4o: add "digital illustration, flat design, no gradients"
- Ideogram: add "flat vector illustration, editorial style, tech blog"

**Do NOT include:** code on screens, company logos, text or titles, photorealism
```

---

## Phase 4 — SEO

**Job:** Write SEO fields for the post. Think from the perspective of a reader landing from search — they don't know about this skill or series. They are searching things like "how to get better results from AI", "best practices for prompting", "why AI output is wrong half the time".

The SEO fields must use language the target reader already has in their head. Speak to the pain (wasted time, bad AI output, refactoring) and the gain (accurate results, less rework, faster shipping).

Print `[HANDOFF: SEO]` AND save to `04-seo.md` using this format:

```
seo_title: <search-optimised title using words readers actually search — under 60 chars>
seo_description: <1-2 sentences: name the pain, hint at the solution — under 160 chars>
```

---

## Image Designer (runs after Phase 4, before Phase 5)

**Job:** Generate one SVG hero image for the blog post by invoking the `/image-gen-agent` skill. The image is used as the Hashnode cover image or as a visual anchor for the post.

**Prepare the brief and invoke `/image-gen-agent`:**

```
[IMAGE BRIEF]
Channel: blog
Variations: 1
Dimensions: 1600×900
Style hint: reason
Content-type: editorial
Final post: <paste full 01-content.md text>
Stats:
  - <extract any concrete numbers or contrast pairs from the post; if none, use qualitative contrast pairs>
Tagline: <recommended title from Phase 2>
Author: Altaf Shaikh
Handle: @teachmebro
Domain: AI Engineering
Output path: ./blog-post/posts/<slug>/blog-hero
```

**Style reasoning rules for blog (agent applies in order, first match wins):**

| Post type | Best style |
|---|---|
| Tutorial / how-to / step-by-step | `warm-illustrated` |
| Claude Code feature / CLI concept / developer tool | `dark-terminal-cream` |
| Mental model shift / contrarian claim / single bold insight | `bold-editorial-type` |
| Architecture breakdown / comparison / technical deep-dive | `diagram-explainer` |
| Opinion / short insight / "less is more" | `minimal-sketch` |
| Concept-driven / atmospheric / big statement | `editorial-bold` |
| Fallback (no clear match) | `editorial-bold` |

Pass `Style hint: reason` so the image agent applies this reasoning itself after reading the post.

The image-gen-agent saves `blog-hero.svg` to the post folder. Do NOT write SVG inline in the conversation.

Print `[HANDOFF: IMAGE DESIGNER]` with the style chosen and output path.

**After `/image-gen-agent` completes, immediately proceed to Phase 5 — never stop after image generation.**

---

## Phase 5 — Final Assembly

**Job:** Assemble the complete Hashnode-ready `.md` file and write it to `final-post.md`.

1. Take the recommended title from Phase 2 as the display title.
2. Insert the banner prompt from Phase 3 into the `<!-- BANNER IMAGE -->` placeholder in the content from Phase 1.
3. Include the SEO fields from Phase 4 in the frontmatter.

Template:

```markdown
---
title: <recommended title from Phase 2>
tags: <3-5 relevant tags>
seo_title: <from Phase 4>
seo_description: <from Phase 4>
---

<!-- 
BANNER IMAGE
============
SVG hero (generated): blog-hero.svg — upload this to Hashnode as the cover image.

To generate a higher-res version with an external tool, use the prompt below:

PROMPT:
<banner prompt from Phase 3>

Midjourney: append --ar 16:9 --style raw --v 6
DALL·E / GPT-4o: add "digital illustration, flat design, no gradients"
Ideogram: add "flat vector illustration, editorial style, tech blog"

DO NOT include: code on screens, company logos, text or titles, photorealism
-->

<full blog body from Phase 1, with the placeholder now filled>

---

## Post assets

| File | Use |
|------|-----|
| [blog-hero.svg](./blog-hero.svg) | Hashnode cover image (SVG, 1600×900) |
| [03-banner-prompt.md](./03-banner-prompt.md) | Prompt to regenerate with Midjourney / DALL·E / Ideogram |
| [02-title-options.md](./02-title-options.md) | All title options — edit frontmatter above to switch |
```

Print `[HANDOFF: FINAL ASSEMBLY]` AND save to `final-post.md`.

---

## Install Block (for any post introducing a skill)

Every post that introduces an installable skill must include TWO install sections.

### Section 1 — Claude Code

```markdown
## How to Install It

This is a Claude Code skill. Two steps — that's it.

**Step 1 — Create the folder**
mkdir -p ~/.claude/skills/<skill-name>

**Step 2 — Paste this into ~/.claude/skills/<skill-name>/SKILL.md**
[skill file content]

Done. No npm. No config changes. No restart. Claude Code picks up skills from ~/.claude/skills/ automatically.

For project-only scope, use .claude/skills/<skill-name>/SKILL.md inside the project folder instead.
```

### Section 2 — Universal install for any IDE

```markdown
## Using a Different AI Tool?

Paste this prompt into whatever agent you're running — Cursor, Gemini CLI, Windsurf, or Antigravity. It detects its own environment and installs the skill automatically.

[universal meta-prompt with all five tool mappings]
```

Universal meta-prompt target paths:

| Tool | Workspace | Global |
|---|---|---|
| Cursor | `.cursor/skills/<name>.md` | `~/.cursor/skills/<name>.md` |
| Claude Code | `.claude/skills/<name>.md` | `~/.claude/skills/<name>.md` |
| Antigravity | `.agent/skills/<name>.md` | `~/.gemini/antigravity/skills/<name>.md` |
| Gemini CLI | `.gemini/skills/<name>.md` | `~/.gemini/skills/<name>.md` |
| Windsurf | `.codeium/windsurf/skills/<name>.md` | `~/.codeium/windsurf/skills/<name>.md` |

---

## Step N — Finalize and update the queue

**This step is mandatory. Run it immediately after Phase 5, every time — never skip it.**

1. **DO NOT touch `../raw-ideas/`.** It's immutable and shared across channels.
2. **Update `./blog-post/TODO.md`:** remove the entry from "In Progress"; prepend a line to "Done" with the source filename, a link to the post folder, and the date.
3. **Print the final output block** in the conversation.

```
Channel: Blog
Processed: <NNN>-<slug>.md
Post folder: ./blog-post/posts/<slug>/
Final post: ./blog-post/posts/<slug>/final-post.md
Hero image (SVG): ./blog-post/posts/<slug>/blog-hero.svg
Queue remaining (Blog): <N> idea(s)
```

---

## `TODO.md` template

Create on first run if missing. Update on every run.

```markdown
# Blog — Queue & Status

This is the Blog channel's consumption ledger. Raw ideas live in `../raw-ideas/` (shared across all channels). Queue = files in `../raw-ideas/` MINUS the filenames listed under **Done** below.

## Queue (unprocessed for Blog)
- [ ] <NNN>-<slug>.md — <one-line preview>

## In Progress
- [ ] <NNN>-<slug>.md — started <YYYY-MM-DD>

## Done
- [x] <NNN>-<slug>.md → [posts/<slug>/final-post.md](./posts/<slug>/final-post.md) — <YYYY-MM-DD>
```

Regenerate the Queue section each run: list files in `../raw-ideas/`, subtract filenames already in Done and In Progress. Append to Done; never delete entries from Done unless the user explicitly asks to re-run an idea.

---

## Altaf's Voice Rules

Every sentence must pass these before it stays.

1. **Short sentences.** Long sentence? Break it.
2. **No filler openers.** Cut: "In today's world", "It's important to note", "As we can see", "Leveraging", "Delve into", "In conclusion"
3. **Say it once.** Don't repeat the same idea three ways to sound thorough.
4. **Humor only when it fits naturally.** If a joke lands organically, keep it. If it's forced, cut it.
5. **Peer, not teacher.** Write like a developer talking to another developer over coffee. Not lecturing.
6. **Every paragraph earns its place.** If it doesn't move the reader forward, cut it.
7. **No AI-isms.** No "certainly", "absolutely", "it's worth noting", "I'd be happy to".
8. **Real over invented.** If Altaf has a real story, use it. Sanitise internal details (company names, ticket IDs, private service names, file names) but keep the flow and lesson.

---

## Series Continuity

Each post must stand alone — a new reader can start anywhere. But it must also feel like part of a progression when read in order.

The series arc: **Mindset → Skills → Tools → Building → Advanced Patterns**

Reference previous posts naturally in the series connector line. Never: "as I mentioned in Part 1". Just: "If you missed Part 1, start there — this builds on it."

---

## Hashnode Formatting

- `#` for title (H1) — one per post, matches frontmatter title
- `##` for major sections
- `---` between sections for breathing room
- **Bold** for key terms on first mention and bolded lead-ins in point lists
- ` `` ` for commands, skill names, file paths, technical strings
- Paragraphs max 3-4 lines in rendered view
- No nested bullet lists — flat only, or write in prose
- Skill install blocks use triple-backtick fenced code blocks

---

## Shared rules

- Never invent statistics, quotes, or claims not in the raw input
- If Altaf gave a real story or example, anchor the content to it — don't replace with a generic one
- Strip any company names, internal tool names, or private details — keep the lesson, drop the specifics
- No emojis unless Altaf explicitly asks
- No em dashes (—). Use a comma, a colon, a full stop, or rewrite as two sentences instead.
- No "In this post I will..." openings — ever
- Authenticity beats polish — a slightly rough real line beats a smooth generic one
- Every handoff is BOTH printed in the conversation AND written to the per-post folder — never one without the other
- Never write outside `./blog-post/` (except: Mode B may write a NEW file to `../raw-ideas/<NNN>-<slug>.md` to register a direct-args idea for other channels). No extra folders. No scratch files elsewhere.
- Never move, rename, or delete anything in `../raw-ideas/`. It's shared and immutable.
- Pads to hit a word count — never
- Adds generic tips at the end ("follow me on Twitter!") — never
- Uses stock metaphors (rocket ship, tip of the iceberg, low-hanging fruit) — never
- Writes a conclusion that just repeats what was already said — never
- Generates images — never (only image prompts in Phase 3)

---

## Loop integration (`/loop`)

This skill is wrapped by the loop prompt in `../blog.agent.md`:

```
/loop 1d <paste blog.agent.md prompt>
```

Each daily firing:
- Computes Blog queue = `../raw-ideas/` MINUS TODO.md Done + In Progress
- Processes ONE idea if queue non-empty
- No-ops silently if queue is empty
- Never re-processes a filename already in TODO.md Done section
- Respects `channels:` frontmatter — skips ideas that exclude "blog"

To process multiple ideas in one day, invoke the skill manually as many times as needed — each invocation drains one entry from the Blog queue. Other channels (LinkedIn, X) maintain independent queues against the same shared library.

---

## Run log (heartbeat) — write this on EVERY run

**The last action of every run, on every path, including early exits.** Full contract: `runs/README.md` at the repo root.

Append ONE row to `./runs/blog.md` (repo root, not the channel folder). Newest at the bottom:

```
| <YYYY-MM-DD> | <outcome> | <one short line, no trailing period> | <link to post folder or —> |
```

`<outcome>` is exactly one of `produced` · `skipped` · `blocked` · `error`.

| Path through the run | Outcome |
|---|---|
| Wrote a post and opened a PR | `produced` |
| Empty queue, or every remaining idea already has an open PR | `skipped` |
| A gate stopped the run on purpose | `blocked` |
| The run failed. Put the failure in `Detail` | `error` |

The blog channel has historically written long explanatory notes into `TODO.md` when a run found nothing to do. Keep doing that if it helps, but the run-log row is what `/factory-health` reads, so it is not optional.

**Committing the row:**

- **Wrote a post** → include `runs/blog.md` in the same content branch and commit.
- **Produced nothing** → commit this one file alone and push straight to the fork's `main`:

  ```bash
  git add runs/blog.md
  git commit -m "runs: blog <YYYY-MM-DD> <outcome>"
  git pull --rebase origin main && git push origin main
  ```

  The ONE exception to "never push to main directly." It must never carry any other file. If the push fails, say so and finish the run anyway.

This channel writes outside `./blog-post/` for exactly this one file and nothing else.
