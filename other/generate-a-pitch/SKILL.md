---
name: Generate a pitch
description: Develops a focused pitch (title plus 150-200 word paragraph) that defines the scope, thesis, word budget, target audience and suggested tags for a new article or newsletter. Use at the start of drafting any new post, after the idea is clear enough (use brainstorming first if it is vague).
---

# Generate a pitch

## Overview

A pitch is the critical step that makes the aim of a post clear and its scope manageable.
Your role is to refine and distil the human partner's energy into a single paragraph of not more than 150-200 words.

**The pitch is the spine of the article.** It gates both scope and length: every later change — including changes proposed by reviewers — is judged in-scope or out-of-scope against it. That only works if the pitch stays short enough to hold in one read, so this skill enforces a fixed shape and hard caps (Step 5).

## Success criteria

The pitch is ready when:

1. **It states a word budget the draft must fit.** Newsletters: 900–1,200 words. Blog posts: 1,600–2,000 words. Treat the upper number as a CAP, not a target. Anything above 2,000 needs the user's explicit sign-off recorded in pitch.md frontmatter (`budget_approved_by` + reason in discussion.md). A post that needs more than one budget increase is two posts. The budget is enforced mechanically: `lint-posts.js` warns at +10% and errors at +25%.
2. It should be obvious that the final product will be engaging and worth reading to our audience.
3. It should be possible to see what kinds of research are needed to produce a valuable article.
4. It is in narrative form: a title and a single paragraph of not more than 150-200 words.

Even if some criteria can't be fully met, as long as the human partner believes this is a good post to write, continue.

## The process

### Step 0: Track the phases

Create a todo list with the five workflow phases — PITCH, WRITE, REVIEW, POST, CHECK — and nothing else. Expand a phase into steps only when you reach it. Do not add steps the workflow does not name; a longer list is not a safer one.

### Step 1: An idea

The human partner has suggested an idea which is suitable for developing a pitch. If it is still too vague, use "skills/brainstorming" first.

**Record the user's opening message verbatim.** The message that started the post is the reference point for the "whose subject is this?" check (Step 3.6, question 4) — save it into pitch.md under `## Original framing (verbatim, never edited)` before anything else is written. Drift is cumulative and each pitch version looks reasonable next to the one before it; only the original message shows the true delta.

### Step 1.5: Voice contract

Read `/docs/Houfu_Voice_Guide.md` — the dosage preamble and Part 4 (Templates). Then pick, with the user if unclear:

- **Lane:** news-commentary or learning-in-public
- **Moves:** the 2–3 voice patterns THIS material genuinely supports (not all of them — a post that uses every pattern reads as parody)

Record both in pitch.md frontmatter (`voice:`). audit-tone checks the draft against this contract, not against the whole guide.

### Step 1.7: Ask for the User's Genuine Experience

Before drafting the pitch, ask ONE question:
"What's the specific personal experience, feeling, or moment that's driving this post? What happened — or what did you feel — that made you want to write this?"

Wait for the user's answer. This response is the source for the emotional core.

**Do NOT invent a vulnerability hook, and do NOT infer feelings the user hasn't stated.** The mined edit corpus (docs/voice-edit-corpus-2026-08.md, rule R3) shows every inferred emotion gets corrected or deleted — one inferred "I hesitated" was factually wrong and shipped to a Ghost draft. If the answer is vague, ask a follow-up. If part of the story is missing, mark it `[HOUFU: …]` rather than filling it in.

### Step 2: Develop the pitch

From the idea, generate a pitch. Imagine we are in an elevator with our readers: limited time to persuade them the post is worth their day. Present a draft title and pitch and ask: "Does it look alright?"

**Declare the primary audience.** Choosing reviewers is choosing who the post is for, and it happens here, not at review time. Pick from the three constituencies (wei-lin / sarah / marcus) per the CLAUDE.md routing table, check the audience-coverage picture (which constituency has waited longest — a neglected audience can tip a close call), and record `primary_audience` (plus optional secondary) in pitch.md frontmatter. `/feedback` reads this field.

### Step 3: Authenticity Check

Interrogate the personal angle to avoid expensive rewrites. For each claim in the pitch:
- Is this true to my experience? (Not aspirational or third-person)
- Can I cite a specific moment when I felt/learned this?
- Am I framing someone else's work as mine?
- Am I claiming expertise I don't have?

Red flags: "I learned that..." (did you?), "Others might think..." (distancing), "One should..." (who?).

### Step 3.5: Verify the Data

A pitch is a hypothesis, not a finding. Before locking it:

- If the pitch contains numbers or factual claims, **verify them against the actual data now** — run the query, check the repo, ask the user for the source. Two posts required full rewrites because pitch numbers were wrong ("444 articles" was actually 27; "600 hours" was actually ~150).
- For time-investment claims, **ask the user for their lived numbers**. Never derive time estimates from lines of code or other formulas.
- If verification must wait, mark the claim `[UNVERIFIED]` in pitch.md.
- **When a source is a chat log or session transcript, read the artifact it produced** (design doc, ADR, commit), not just the log — pitch v6 of legal-oss-maintainer cost a full draft because the reversibility principle lived in a design doc the log merely pointed at.

### Step 3.6: Interrogate the Pitch

**Interrogate the spine hardest.** A spine enforces; it does not check whether it is true. A wrong spine produces a draft that is internally perfect and about the wrong thing. Ask four questions and record the answers in pitch.md frontmatter (`interrogation:`):

1. **Test the diagnosis.** If the pitch is built on the user's own problem framing, probe it instead of accepting it: "Does [diagnosis] actually explain the tension? What would contradict it?"
2. **The differentiation question.** "This will always be 'another [X] post' — what makes ours different?" If there's no answer, the pitch isn't ready.
3. **The framing risk question.** "Could a named person, company, or community read this as an attack?" Decide now whether to anonymize or reframe — not after drafting.
4. **Whose subject is this?** Re-read the user's ORIGINAL framing message — the verbatim block at the top of pitch.md — and ask: is its subject still this pitch's subject, or has it become the evidence for something else? Check against that message, never against the previous pitch version. (legal-oss-maintainer drifted subject twice — v4 made the field report the subject and stewardship the conclusion, the reverse of the opening message; v6 made the tool the protagonist. Seven pitch versions, two full drafts.) If the subject has moved, say so explicitly and ask before proceeding.

A pitch amended mid-draft is not a sin, but it means this step failed — when it happens, note in discussion.md which of these questions would have caught it.

### Step 3.7: Seed Must-Link Posts and Timeline

- Identify 2-3 **must-link prior posts** this post builds on or contradicts (use `ghost_search`). List them in frontmatter `must_link`. Full curation still happens at final draft via `backlink_curating`.
- Ask whether there's a **target publish date or external deadline**. Record it — surprise schedule acceleration causes rushed metadata, images, and backlinks.

### Step 3.8: Triage before you block

Do not present an open question to the user until it fails all three tests:

(a) **Can I answer it from data I can reach?** Then answer it. Say what you found and note it is correctable at review.
(b) **Is the post better with the uncertainty stated than with the fact?** Then write the uncertainty into the draft. "I don't know whether X or Y" is usually better voice than a confident cause.
(c) **Is it needed before PUBLISHING rather than before DRAFTING?** (consent to name someone, quote approval, a scheduled date) Then it is a publish-gate. Draft around it — an unnamed contributor is a find-and-replace away from named.

Only **lived personal facts** — hours spent, how something felt, how a role came about — are genuinely un-guessable and genuinely block. Never invent those; mark them `[HOUFU: …]` and build prose that survives without them.

Cap: at most 3 open questions to the user at any pitch checkpoint. More means you have not triaged. (History: a session once listed seven pre-draft gates; on triage, none blocked drafting.)

### Step 4: Suggest Tags

After the pitch is approved, use the **tag-registry** skill: 3-4 tags from the canonical registry, at least 1 Core Topic tag, recorded in pitch.md frontmatter.

### Step 5: Scaffold the post

Create the folder (`posts/{post-short-title}/`) and save `pitch.md` in this exact shape. **pitch.md is a fixed-shape file with hard caps — it is the scope contract, so it must be short enough to hold in one read. Cap: 120 lines. Everything else — research, cut material, rejected alternatives, design extracts — lives in `research.md` or `discussion.md`.**

```markdown
---
word_budget: 1900          # prose words for the main file; cap = budget × 1.10
budget_tolerance: 10       # optional, percent
primary_audience: wei-lin  # wei-lin | sarah | marcus (+ optional secondary list)
thesis_keywords: []        # 2-4 terms the draft must actually be about (lint-checked)
protected_lines: []        # exact strings that survive every cut (lint-checked)
voice: {lane: learning-in-public, moves: []}   # 2-3 moves from the Voice Guide
interrogation: {diagnosis: "", differentiation: "", framing_risk: "", subject: ""}
must_link: []              # 2-3 prior post slugs
tags: []
target_date: ~
---

# Pitch: {post-short-title}

## Original framing (verbatim, never edited)

> [The user's opening message, quoted verbatim.]

**Title:** [one line — titles the user has settled are marked SETTLED and not re-proposed]
**Thesis:** [ONE sentence — the claim the post argues]
**Spine:** [ONE sentence that ships in the prose. Distinct from the thesis — the spine lands in the draft; the thesis is what the post argues]
**Emotional core (user's words):** [verbatim — never invented]

## Pitch

[One paragraph, 150–200 words. Hard cap 200 — lint-checked.]

## Beats

- [3–7 bullets, one line each, with a word allocation per beat summing to the budget]

## Out of scope

- [Named cuts. A reviewer suggestion that maps here is declined by default.]
```

**Superseded versions are deleted, not stacked.** When the pitch is amended, rewrite the file in place and record the diff and its reason in discussion.md. Git holds the audit trail; pitch.md holds one current contract. (The old convention of keeping v4/v5/v6 in the file produced an 8,078-word "contract" that could retroactively justify nearly any scope.)

Save the discussion using "skills/note-taking" under `discussion.md`, then ask the human partner whether to develop the outline.
