---
name: call-audit
description: >
  Audit acquisitions specialist call recordings or transcripts for a real
  estate wholesaling company. All training materials, scripts, SOPs, and
  checklists are embedded in this skill's knowledge base — no additional
  uploads needed. Use this skill whenever someone uploads a call transcript
  or audio file and asks to audit, review, score, grade, or coach on it.
  Triggers include: "audit this call", "review this transcript", "score
  my acquisitions guy", "fill out the checklist", "coaching notes", "call
  review", "how did he do", "what did he miss", or any time a call
  transcript is provided with a request to evaluate performance. Always
  use this skill even for casual phrasings like "can you look at this call"
  or "what could he have done better". Produces a completed checklist .docx
  and a coaching summary .docx ready for SharePoint upload.
---

# Call Audit Skill — Results Driven REI

## Knowledge Base Location
All training materials are embedded in `/references/`:
- `training-kb.md` — ICP, CHAMP, UMBC, Motivation Categories, Rebuttal Sheet, Lead Status SOP, Red Flag Indicators, ACQ Day prioritization, Ghost Text, closing checklists
- `process-call-checklist.md` — Detailed evaluation criteria and scoring for process-type calls
- `offer-call-checklist.md` — Detailed evaluation criteria and scoring for offer/renegotiation calls

**Read both the relevant checklist file AND training-kb.md before scoring any call.**

---

## Step 1: Receive & Prepare Inputs

The user will provide:
1. **A call transcript** — as text in the chat, or as an uploaded .docx/.txt file
2. **A prompt** to audit, review, or score the call

If the transcript is in a .docx file, extract it:
```bash
pandoc --track-changes=all transcript.docx -t plain
```

If the user provides an audio file (.mp3/.wav): Claude cannot process audio directly.
Tell the user: *"I can't process audio files directly — please paste the transcript as text or upload it as a .docx or .txt file."*

---

## Step 2: Read the Knowledge Base

Before scoring, read the relevant reference files:
```
/home/claude/call-audit-skill/references/training-kb.md
/home/claude/call-audit-skill/references/process-call-checklist.md   (if process-type call)
/home/claude/call-audit-skill/references/offer-call-checklist.md     (if offer/renegotiation)
```

---

## Step 3: Detect Call Type

Determine which type of call this is by reading the transcript content. The user may specify, or you infer from context:

| Call Type | Detection Signals | Checklist to Use |
|---|---|---|
| **Cold Call** | First contact, seller doesn't know the company, no prior relationship established | Process Call Checklist |
| **Follow-Up Call** | References a prior conversation, checking back in, seller is in "Interested Add to FU" or "Discovery" status | Process Call Checklist |
| **Process Call** | Structured info-gathering call, working through CHAMP/UMBC, gathering motivation + property condition + roadblocks | Process Call Checklist |
| **Offer Call** | Price is being presented in this call, includes offer delivery and acceptance/objection handling | Offer Call Checklist |
| **Manager Follow-Up** | Manager is calling to re-engage a stalled lead, references a previous offer or conversation | Process Call Checklist |
| **Renegotiation** | Price reduction being discussed after a prior accepted offer; includes justification and re-close | Offer Call Checklist |

**If unclear**, ask the user: *"Is this a process call (gathering info/building rapport) or an offer call (presenting price)?"*

State the detected call type at the top of your audit output.

---

## Step 4: Audit the Call

Go through the transcript systematically against the appropriate checklist. For each checklist item:

1. **Status**: ✓ Done / ~ Partial / ✗ Missed
2. **What happened**: Brief note on what the specialist actually said (with a direct quote where possible)
3. **What was good or what was missing**: Measured against the training materials
4. **Score**: 0–10 per section

### Scoring Scale
| Score | Meaning |
|---|---|
| 9–10 | Executed well, consistent with training |
| 7–8 | Mostly done, minor gaps |
| 5–6 | Attempted but significant gaps |
| 3–4 | Largely missed or poorly executed |
| 0–2 | Not attempted or actively harmful |

### Overall Score
Weighted average across all sections. Weight **Motivation** and **Roadblocks** (process calls) or **Recap Motivation** and **Objection Handling** (offer calls) most heavily — these are the core of each call type.

---

## Step 5: Produce Two Output Documents

Use the docx skill to produce both files. See `/mnt/skills/public/docx/SKILL.md` for full reference.

Install if needed:
```bash
npm list -g docx 2>/dev/null | grep docx || npm install -g docx
```

### Output 1: Completed Checklist (.docx)

Mirror the format of the official checklist as closely as possible:

**Process Call Checklist format:**
```
☑/☐  STEP                    FEEDBACK
      Intro                   [note]
      Set Expectations
  ☑   a. Time                 [note]
  ☑   b. Agenda               [note]
  ...
      Section Score: X/10
```

**Offer Call Checklist format:**
```
☑/☐  STEP                         FEEDBACK
      Setting Expectations
  ☑   a. Time                      [note]
  ...
      ACCEPTED / NOT ACCEPTED
  ☑   a. Go for No                 [note]
  ...
      Section Score: X/10
      Overall Score: X/10
```

Include at top:
- Specialist name (if known from transcript)
- Call type
- Date (if known)
- Overall score: X/10

Filename: `[SpecialistName]_[CallType]_[Date]_Checklist.docx`
Fallback: `CallAudit_[ProcessOrOffer]_Checklist.docx`

---

### Output 2: Coaching Summary (.docx)

```
CALL AUDIT — COACHING SUMMARY
═══════════════════════════════════════
Specialist:  [Name or Unknown]
Call Type:   [Process / Offer / etc.]
Date:        [if known]
Overall Score: X/10

───────────────────────────────────────
WHAT WENT WELL
───────────────────────────────────────
[2–4 specific strengths with direct call quotes]

───────────────────────────────────────
TOP OPPORTUNITIES FOR IMPROVEMENT
───────────────────────────────────────
[Ranked 3–5 most impactful gaps. For each:]

  Issue:              [what was missed or done poorly]
  Moment in the call: "[brief quote or description of where it happened]"
  Training says:      [cite the specific script/SOP/framework]
  Try this instead:   [exact language or technique to use]

───────────────────────────────────────
SECTION SCORES
───────────────────────────────────────
[Section]: X/10 — [one-sentence summary]
...
OVERALL: X/10

───────────────────────────────────────
UMBC QUICK CHECK
───────────────────────────────────────
U — Urgency:     [Yes / No / Solution / Not Established]
M — Motivation:  [Distressed / Not Distressed / Not Determined]
B — Ballpark:    [Works / Doesn't Work / Not Asked]
C — Condition:   [Livable / Not Livable / Not Asked]

CHAMP Score: [X/8] — [Lead tier: A-List / B&B / C / Dead End]

───────────────────────────────────────
COACHING NOTES
───────────────────────────────────────
[Any patterns, observations, or longer-form feedback]
```

Filename: `[SpecialistName]_[CallType]_[Date]_CoachingSummary.docx`

---

## Step 6: Batch Audits

If multiple transcripts are provided:
- Audit each independently following Steps 1–5
- After all individual audits, add a **Batch Summary** section (or separate file) showing:
  - Each call's overall score
  - Recurring patterns across calls
  - Top 3 coaching priorities for the week based on the full batch

---

## Coaching Principles

- **Be specific, not generic.** Every coaching note must reference something that actually happened in THIS call. No generic sales advice.
- **Cite the training.** Always connect a miss to the specific script, SOP, or framework (e.g., "Per the Rebuttal Sheet, you should ask this 3 times in 3 different ways…").
- **Quote the call.** Short direct quotes make coaching land harder than paraphrases.
- **Frame positively.** This is coaching, not a performance review. Misses = opportunities, not failures.
- **Be direct.** Don't soften findings to the point of being useless. The goal is to win more contracts.

---

## Dependencies
- `pandoc` — for reading .docx transcripts
- `docx` npm package — for producing output .docx files (`npm install -g docx`)
- See `/mnt/skills/public/docx/SKILL.md` for full docx creation reference
