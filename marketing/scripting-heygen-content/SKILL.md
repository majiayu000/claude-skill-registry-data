---
name: scripting-heygen-content
version: "2.0.1"
description: >
  Generates HeyGen avatar scripts and production prompts for Abstrekkt
  and FlashFusion content. Three input modes: topic-first, bullet-first,
  or notes/research-first. Always outputs a paired script + production
  prompt block covering Look selection, Voice Director tags, B-roll
  suggestions, pacing notes, and credit estimate. Brand: Kyle Rosebrook
  / Abstrekkt. Voice: direct, first-person, earned authority, no hype.

  Activate when the user says: HeyGen script, write a script for HeyGen,
  generate an avatar script, script this for my avatar, video script,
  produce a HeyGen video, turn this into a HeyGen script, write a video
  for FlashFusion, Abstrekkt video, talking head script, brand video
  script, origin story video, explainer script, tutorial script for
  HeyGen, or any request to write a script for avatar delivery.
  Also activates on: topic → script, notes → video, bullets → video,
  research → script, write me a 90 second, write me a 60 second.
---

# HeyGen Script Generator

**TL;DR:** Takes a topic, bullets, or raw notes and outputs a production-ready avatar script in Kyle's voice plus a copy-paste HeyGen production block. Both deliverables ship together, every time. Neither ships alone.

---

## Decision Tree

```
Input received?
├── Topic/title only ──────────── → Mode A (Topic First)
├── Bullet list of points ────── → Mode B (Bullets First)
├── Research/notes/article ───── → Mode C (Notes First)
└── Nothing provided ─────────── → Ask: "What are you starting with: a topic,
                                    bullets, or notes/research?"

Duration specified?
├── Yes → use that length
└── No  → default 90s (185–215 words)

CTA destination specified?
├── Yes → pull from CTA Library → references/production-prompt.md
└── No  → default: "Find me at FlashFusion.co"
```

---

## Input Modes

### Mode A — Topic First
**Trigger:** User gives a title, concept, or one-line idea only.

1. Restate topic as a single sentence to confirm framing
2. Identify audience: domain expert, curious learner, or both
3. Default to "same script serves both" unless user specifies otherwise
4. Draft following voice rules → references/voice-rules.md
5. Output Script Block + Production Prompt Block

### Mode B — Bullets First
**Trigger:** User provides a bullet list of points to cover.

1. Scan bullets for: natural opening hook, one core insight, proof/story beat, soft close
2. Reorder if needed — note any reordering with a one-line reason
3. Compress redundant bullets without asking
4. Draft script — bullets become narrative, not a list read aloud
5. Output Script Block + Production Prompt Block

### Mode C — Notes / Research First
**Trigger:** User pastes research, newsletter draft, article, or raw notes.

1. Extract the single most useful insight from source material
2. Build script around that one insight — don't try to cover everything
3. Flag any claims that need verification before recording
4. Output Script Block + Production Prompt Block

---

## Script Length Guide

| Duration | Word count | Use case |
|---|---|---|
| 60s | 130–150 words | Social clip, teaser, quick tip |
| 90s | 185–215 words | Brand intro, concept explainer |
| 2 min | 250–280 words | Tutorial, case study, origin story |
| 3 min | 380–420 words | Deep explainer, product walkthrough |

Default: 90s. When in doubt, shorter.

---

## Voice Rules (Summary)

Full profile with banned phrase list and anchor sentences → `references/voice-rules.md`

**Core constraints (non-negotiable):**
- First person singular only — "I", "my", "me". Never "we" unless Kyle + client working together.
- Short declarative sentences. One idea per sentence.
- Earned authority: state what you did, not what you know.
- No hype phrases. No rhetorical question openers.
- No Loxihart/employer context. No co-founder framing. No ChaosClubCo.

**Tone calibration anchor:** "No hype. No gatekeeping. Just the work."

---

## Script Structure Arc

Full arc with sentence-count targets by duration → `references/script-structure.md`

```
[HOOK — 10–15%]         One statement that earns the next 60s. NOT a question.
[CREDIBILITY BRIDGE — 10–15%]  Why Kyle is speaking. Earned, not claimed.
[THE GAP — 20–25%]     The problem the audience hasn't named yet.
[THE WORK — 35–40%]    What Kyle actually does. Specific. Name the audience.
[SOFT CLOSE — 10–15%]  One sentence invitation. No hard CTA.
```

---

## Output Format

Always output in this exact order. No exceptions.

```
SCRIPT
───────
[script text with Voice Director tags embedded inline]

PRODUCTION PROMPTS
──────────────────
[full production prompt block — format at references/production-prompt.md]

ASSUMPTIONS
────────────
[every non-user-specified decision: length, CTA, audience, framing]
```

---

## Worked Example

**Input (Mode A):** "Write a 60s script. Topic: why I left hospitality for AI."

```
SCRIPT
───────
Ten years in hotel management taught me how people work.
<break time="0.8s" />
I had no tech background. I taught myself AI from scratch, in my spare
time, while managing a team of forty.
<emphasis level="strong">The gap between what AI can do and what most
people think it can do — that's the work I do now.</emphasis>
I help teams cross that gap without needing a technical hire.
<break time="0.5s" />
Find me at FlashFusion.co.

PRODUCTION PROMPTS
──────────────────
LOOK SELECTION
Recommend: Smart-Casual
Reasoning: Personal origin story — credible enough to earn trust,
approachable enough to land.

VOICE DIRECTOR TAGS
<break time="0.8s" /> after hook. <emphasis> on "the work I do now."
<break time="0.5s" /> before close.

PACING NOTES
- Hook: Steady. Matter-of-fact. No performance.
- Bridge: Slightly slower — let "from scratch" land.
- Close: Warm, not salesy.

B-ROLL SUGGESTIONS
1. Hotel lobby or front desk (hospitality era)
2. Laptop open at a kitchen table (self-teaching era)
3. Claude or n8n workflow on screen

CREDIT ESTIMATE (HeyGen Creator Plan)
~2–3 credits for ~140 words at 1080p.

ASSUMPTIONS
- Duration: 60s (user specified)
- CTA: FlashFusion.co default (no destination specified)
- Audience: Both domain expert and curious learner
- Look: Smart-Casual (origin story register)
```

---

## Eval Scenarios

### Should Trigger
1. "Write me a 90-second HeyGen script about using AI for SOPs"
2. "Script this for my avatar: I want to explain what FlashFusion does"
3. "Turn these bullets into a HeyGen script: [bullet list]"
4. "I have a newsletter draft — turn it into a video for my channel"
5. "Write a 60-second origin story video"

### Should NOT Trigger
1. "Write a LinkedIn post about AI automation" — social copy, not avatar script
2. "Edit my YouTube video transcript" — editing, not scripting

---

## Self-Verification (Acceptance Criteria)

Run this checklist before outputting. Every box must clear.

- [ ] Word count hits target duration (±10%)
- [ ] First word of script is NOT a rhetorical question
- [ ] No "we" except Kyle + client context
- [ ] No banned phrases present (scan against references/voice-rules.md)
- [ ] Voice Director tags placed: `<break>` after hook, `<emphasis>` on key phrase, `<break>` before close
- [ ] B-roll has 3–5 items, all feasible to shoot or source
- [ ] Credit estimate is present and plausible
- [ ] ASSUMPTIONS section lists every non-user-specified decision made
- [ ] FAIL CONDITIONS block checked — none triggered
- [ ] Production Prompt Block is complete — no bracketed placeholders remaining

---

## FAIL CONDITIONS

Do not generate output if:
- No topic, bullets, or source material provided
- User asks to reference CCA-F before July 20, 2026
- User asks to include Loxihart, employer, or co-founder framing
- User asks to include ChaosClubCo branding (retired June 2026)
- Script would exceed 500 words without explicit user override

---

## CLAIMS

**[GENERATED]** Paired script + production block as a single atomic deliverable reduces platform friction — eliminates the context-switch to build HeyGen prompts separately after scripting.

**[GENERATED]** Defaulting to 90s reduces scope creep in first drafts; users can always request longer, but a 3-minute script requested off a 3-word topic is almost always wrong.

**[GENERATED]** "Mode C extracts one insight" is a creative constraint that produces focused video, but conflicts with how users think about their research — they often want 3–4 points covered. Must be managed by naming the constraint before generating.

## COUNTEREXAMPLE

A topic with no established Kyle connection (e.g., a client product demo) may not benefit from the credibility bridge beat — the arc may need to skip or compress it and expand THE WORK instead.

## CONTRADICTIONS

! "First person singular only" conflicts with content about collaborative client work where "we" is accurate. The current carve-out ("Kyle + client working together") is vague — a FAIL CONDITION should explicitly protect this path or define it more precisely.

! "Extract the single most useful insight" (Mode C) makes for focused video but creates friction when the user believes their research contains 3–4 equally valuable points. The skill does not currently instruct how to explain or negotiate this tradeoff with the user before generating.
