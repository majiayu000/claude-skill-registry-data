---
name: wrongodb-blogging
description: Plan and write WrongoDB devlog posts in this repo. Use when asked to plan, outline, draft, or revise posts under blog/, generate blog images, or follow the series structure for WrongoDB. This skill embeds the canonical planning and writing prompts and uses blog/generate_image.py for image generation.
---

# WrongoDB Blogging

## Overview
Create blog post plans and drafts for the WrongoDB series without re-reading or re-deriving the series structure. Use the canonical prompts embedded below and the image generator script in this repo.

## Workflow (plan -> write -> images)

### 1) Planning a post
- Read the "Planning prompt (canonical)" section below and follow it exactly.
- Before locking the topic, grab inspiration from recent work:
  - Scan git history beyond the last 20 commits and pinpoint the relevant change:
    - `git log --oneline --reverse --since="2025-12-01"` (widen/narrow dates as needed)
    - `git log --oneline -- src/blockfile.rs src/leaf_page.rs src/btree.rs docs/decisions.md` (file-focused)
    - `git log -S "BlockFile" -S "FULLFSYNC" -S "checkpoint" -S "slot" --oneline` (string-focused)
  - Cross-check `PLAN.md`, `docs/decisions.md`, `blog/SERIES.md`
  - Codex session logs for narrative hooks: `~/.codex/sessions` and `~/.codex/history.jsonl` (use `rg` for keywords like `blockfile`, `fs_usage`, `BTree`, `checkpoint`)
- Do not reread or re-discover prior posts; the prompt already encodes the structure and voice.
- Produce a plan with the required sections (Title + hook, scope, 7 beats, decisions, artifact, images, verification).
- If details are uncertain, tag as **TO VERIFY**.
- Outline clarity guidelines (apply when the user asks for simpler language or stronger pedagogy):
  - Reduce jargon and define any unavoidable terms in plain language.
  - Add a one-sentence definition for the core concept (e.g., “A B+tree is…”).
  - Deepen the “Why” beyond the immediate symptom (e.g., not just “page full,” but why the structure is a standard DB building block).
  - Keep each beat short and explanation-forward (one or two sentences max).
- Aha-moment mining (when planning or revising posts):
  - Scan `~/.codex/sessions` and `~/.codex/history.jsonl` for the exact questions/confusions you had (e.g., “what the hell is a slot,” “when do we compact?”).
  - Extract 2–4 of those questions and answer them in the post as short, teachable inserts.
- Image planning lessons:
  - Each image prompt must state the **story purpose** (e.g., “show the durability boundary” or “map trace lines to meaning”), not just the subject.
  - Prefer narrative structures (before/after, timelines, mappings) over generic box-and-arrow diagrams.
  - Specify labels and icons that reinforce the story (e.g., crash bolt, shield, timeline bands).
  - After generation, validate files are real images (`file blog/<post-dir>/images/*.png`); if invalid or dull, revise prompts and regenerate.
- Story/structure lessons:
  - After any significant change anywhere, re-check that the arc still flows.
  - Introduce new concepts inline before using jargon; keep definitions direct (no metaphors).
  - Use sections for readability; include explicit transitions or “lightbulb” moments where they help.
  - Diagrams must be narrated in the text and placed near the concept they illustrate.
  - Include a brief “how I ran the tool” line in the post when a tool is central; mention other options you did not use.
- Keep series continuity: add a short recap/link to the previous post when relevant; ensure numbering/order is updated.

### 2) Writing a post
- Read the "Writing prompt (canonical)" section below and follow it exactly.
- Use the plan as the single source of truth; do not add new slices.
- Keep the voice candid, playful, learning-first, “wrong on purpose.”
- Keep the body tight (5–10 minute read).
- Include the images specified in the plan.

### 3) Generating images
- For each image prompt, run:
  `python blog/generate_image.py "<prompt>" --post <post-dir> --out blog/<post-dir>/images/<NN-short-name>.png`
- Prefer sizes/aspects by intent:
  - Hero: `--aspect 16:9 --size 2K`
  - Diagrams: `--aspect 4:3 --size 1K` or `--aspect 1:1 --size 1K`
- Filenames must be prefixed with the order they appear in the post: `01-`, `02-`, `03-`, ...
- If an image prompt is unclear, revise the prompt text first (do not guess).

## QA checklist
- Keep **TO VERIFY** tags until verified against code or notes.
- Confirm the plan matches the thin-slice scope.
- Ensure images were generated with `blog/generate_image.py`, stored under `blog/<post-dir>/images/`, and filenames match the post markdown.

---

## Planning prompt (canonical)

# Blog Post Planning Prompt (WrongoDB series)

Use this prompt to plan a new post in the WrongoDB devlog series.

---

## Goal
Produce a tight, publish-ready plan for a single new post (5–10 minute read) that advances the series by **one thin slice**.

## Known series DNA (do NOT re-derive)
- Voice: candid, playful, learning-first
- Structure rhythm: hook → context → mental model → one key decision → concrete artifact → why it matters → what’s next.
- Teaching moves: rhetorical questions, crisp definitions, zoom from concept to bytes, explicit layer separation.
- Visual rhythm: 2–4 images per post
- Scope: one slice only, no roadmap dumps.

## Planning rules
- Plan the next post using the structure above
- Pick **one** core concept and **one** key decision to explain, if not provided by the user.
- Include **one** concrete artifact to anchor the explanation (code, struct, layout, file header, algorithm step, etc.).
- Prefer examples that can be verified against the repo if needed.
- If details are uncertain, mark as **TO VERIFY** (do not invent).

## Output format
Return a plan with the following sections, in order:

### 1) Title + Subtitle + One-line hook
- Proposed title
- A meaningful subtitle that sharpens the focus (not a generic label)
- A single-sentence hook that sounds like the existing voice

### 2) Thin-slice scope
- One sentence: “This post explains … and stops before …”

### 3) Outline (7 beats)
Use exactly these beats:
1. Hook
2. Context / Why this exists
3. Mental model (diagram candidate)
4. Key decision (trade-off + rationale)
5. Concrete artifact (code/struct/layout)
6. Why it matters (behavior + invariants)
7. What’s next (2–3 bullets)

### 4) Key decisions
- Decision: …
- Alternatives considered: … (2–3 options max)
- Trade-offs: …

### 5) Concrete artifact
- Name the artifact and where it lives (file path or conceptual object)
- Bullet list of the 2–4 elements you will show or explain

### 6) Images
- 2–4 image prompts (short, literal)
- Include the intended filename for each image with an ordered prefix (e.g., `01-...`, `02-...`)

### 7) Verification checklist
- 3–6 bullets of facts to verify against code/notes
- If anything is speculative, tag it **TO VERIFY**

---

## Style constraints for the plan
- Keep each section short; avoid narrative prose.
- Prefer plain language; avoid jargon unless defined.
- If the topic is concept-heavy, include a one-sentence definition in the plan.

## Example: acceptable brevity (mini)
- “Key decision: explicit allocation vs implicit append; trade-off: clarity vs convenience.”

---

## Writing prompt (canonical)

# Blog Post Writing Prompt (WrongoDB series)

Use this prompt to write a full post **from an existing outline** created with the planning prompt above.
**Do not reread or re-discover the existing posts.** The structure and voice are already known and summarized here.

---

## Inputs
You will be given a plan that follows the 7-beat outline and includes:
- Title + One-line hook
- Thin-slice scope
- Outline beats
- Key decisions
- Concrete artifact
- Images
- Verification checklist

## Goal
Produce a complete markdown post that follows the plan exactly, in the established voice and structure, and is ready to drop into `blog/NN-title.md`.

## Known series DNA (do NOT re-derive)
- Voice: candid, playful, learning-first, “wrong on purpose.”
- Structure rhythm: hook → context → mental model → one key decision → concrete artifact → why it matters → what’s next.
- Teaching moves: rhetorical questions, crisp definitions, zoom from concept to bytes, explicit layer separation.
- Visual rhythm: 2–4 images per post.
- Scope: one slice only, no roadmap dumps.

## Writing rules
- Follow the plan’s 7 beats in order.
- Do not add new topics or extra slices.
- Include 2–4 inline images as markdown: `![Alt](images/<NN-filename>.png)`.
- Image filenames must be prefixed in order of appearance: `01-`, `02-`, `03-`, ...
- Generate images by running `python blog/generate_image.py "<prompt>" --post <post-dir> --out blog/<post-dir>/images/<NN-short-name>.png`.
- If a fact is uncertain, mark it inline as **TO VERIFY** and keep going.
- Do not invent code details; only reference file paths or structs if the plan says they exist.
- Avoid markdown links unless the plan explicitly provides them.

## Output format
Return a single markdown document with:
1) `# Title`
2) `## Subtitle`
2) Optional hero image (if the plan calls for it)
3) Body sections in a natural flow (no numbered headings required)
4) “What’s next” as a bullet list

## Style constraints
- Tight paragraphs (3–6 lines each)
- Occasional rhetorical questions
- Definitions in short, punchy sentences
- Avoid marketing language

## Post template (skeleton)

# <Title>

## <Subtitle>

![<Hero Alt>](images/<hero_filename>.png)

<Hook paragraph>

<Context / why this exists>

<Mental model + image>

<Key decision + trade-off>

<Concrete artifact explanation>

<Why it matters>

## What’s next
- <bullet>
- <bullet>
- <bullet>

---

## After writing
- Ensure all **TO VERIFY** flags are still present (do not resolve them).
- Ensure all images mentioned in the plan are included.
- Ensure each image was generated with `blog/generate_image.py`, stored under `blog/<post-dir>/images/`, and matches the prompt.
- Ensure the post matches the thin-slice scope.
