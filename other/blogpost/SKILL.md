---
name: blogpost
description: "Emily's blog post pipeline: capture, draft, revise, finalize posts; maintain posts/INDEX.md; delegate research and images to sub-agents."
---

# Blog post workflow

Folder contract lives in AGENTS.md. Two rules override everything:
- NEVER edit or overwrite `initial-draft.md`.
- Log feedback to `feedback-log.md` (with the passage it refers to) BEFORE editing the draft.

Before drafting or revising, read `skills/blogpost/references/voice-style-guide.md` if it exists.

## Intake interview
Use this when Emily brings a new rough idea, voice memo, or rambly draft and the main point is not clear yet.

Goal: help Emily figure out what she is actually trying to say, both for herself and so the writing workflow has a clear target.

Ask one concise question at a time. Do not interrogate. Stop when the answer is clear enough to write:
- One-sentence main point
- Intended reader/audience
- Hook or tension
- What makes the idea interesting or different
- Desired reaction: what the reader should think, feel, or do
- Likely format: longform-substack, short-substack, or tiktok

Good first question after capture:
- "What's the one sentence takeaway you want someone to repeat after reading this?"

Write the current answer in `main-point.md`. If the main point changes during discussion, update `main-point.md` and record Emily's correction there.

Protect against scope creep: if new side ideas appear, capture them in `tasks.md` or create a sparked-by post, then return to the current piece.

## posts/INDEX.md
Master table, one row per post:

| slug | working title | type | status | started | last worked | next action | sparked by |
|---|---|---|---|---|---|---|---|
| creativity-walks | Why my ideas only come on walks | longform-substack | revising | 2026-07-02 | 2026-07-05 | awaiting Emily feedback on section 2 | — |

- type: longform-substack | short-substack | tiktok. Ask if unclear.
- status: idea | drafting | revising | researching | final | posted | parked.

Update ONLY on: (1) folder creation -> add row; (2) status change; (3) session end ("end session", "done for now") -> update `last worked` + `next action` for posts touched; (4) resuming a post -> correct stale row. NOT on every file edit.

"What's in flight?" -> read INDEX.md aloud: slug + status + next action. Skip posted/parked unless asked.

## Research delegation
When Emily flags something to research, or a claim needs verification, spawn a sub-agent (do not research in this session):

sessions_spawn with task:
"Read workspace/skills/blogpost/references/research-worker.md and follow it exactly. Post slug: <slug>. Research question: <one specific question>. Main point of post: <2 sentences from main-point.md>. Existing findings: <list titles already in research.md, or 'none'>."

One question per spawn; parallel spawns are fine. When a worker announces completion, read the new entries in `research.md` and give Emily a one-paragraph spoken summary. Do not block waiting; keep the conversation going.

## Clean-room draft delegation
Use this only when Emily wants an independent agent draft for comparison, not when the main agent is drafting directly from Emily's words.

sessions_spawn with task:
"Read workspace/skills/blogpost/references/draft-worker.md and follow it exactly. Post slug: <slug>. Main point: <summary from main-point.md>. Interview notes: <notes only; do not include Emily's own draft text>. Recommended format: <longform-substack | short-substack | tiktok>."

The draft worker must not see `initial-draft.md`; it writes only to `agent-draft.md`.

## Image delegation (Phase 5 only)
sessions_spawn with task:
"Read workspace/skills/blogpost/references/image-worker.md and follow it exactly. Post slug: <slug>. Final draft: posts/<slug>/final-draft.md. Title chosen: <title, or 'not chosen'>."

The image worker should report local image paths and, when possible, browser-openable GitHub preview/raw links without exposing credentials. The detailed image workflow, reusable image-direction prompt, and browser-link rules live in `references/image-worker.md`.

## Phase 1 - Capture (new idea or voice memo)
1. Create `posts/<slug>/`.
2. Save her words verbatim -> `initial-draft.md`.
3. Write your best current read of the main point -> `main-point.md`; mark uncertainty if unclear.
4. Add INDEX.md row (status: idea).
5. git add -A && git commit -m "capture <slug>".
6. Reply: your read of the main point + at most ONE intake question. STOP and wait.

## Phase 2 - Clarify / think it through
- Continue the intake interview when the argument is still fuzzy.
- Ask one question at a time until the main point, audience, hook/tension, and desired reaction are clear.
- Update `main-point.md` when Emily clarifies or corrects the idea.
- Research flags -> spawn per Research delegation (or add to tasks.md if she says later).
- Side idea -> new folder + initial-draft.md + INDEX.md row with `sparked by`, or add to `tasks.md` if it is not a post yet. Return to current post.

## Phase 3 - Draft
1. Read `main-point.md`, `initial-draft.md`, and `voice-style-guide.md` if it exists.
2. Write `working-draft.md` from her draft + conversation. Preserve her phrasing; she will rewrite most of it.
3. Status -> drafting. Commit.
4. Reply: word count + readback options (by section | straight through | changes only). STOP and wait.

## Phase 4 - Revise (loop)
1. Read back in her chosen unit. After each chunk, STOP for feedback.
2. Each piece of feedback -> `feedback-log.md`: passage reference, feedback, status (pending | applied | discussed-not-applied).
3. "Change X" -> apply. Question/reaction -> answer, log as discussed-not-applied, do NOT edit.
4. Before each substantial edit pass: git add -A && git commit -m "pre-edit <slug>".
5. Status -> revising.

## Phase 5 - Finalize (on explicit approval)
1. Write `final-draft.md`, fully formatted (headers, paragraph breaks, bullets), Substack-ready.
2. Generate 3-5 title/subtitle pairs -> `titles-and-images.md`. Spawn image worker per Image delegation.
3. Status -> final. Update INDEX.md. Commit and push.
4. Reply: file paths, open Emily tasks, spawned post slugs.
