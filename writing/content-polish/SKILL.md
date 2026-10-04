---
name: content-polish
version: 1.1.0
description: "End-to-end content polishing workflow that runs the humanizer and proofreader in the correct sequence with proper handoff between them. Language-branched: English content uses humanizer + proofreader; Vietnamese content uses humanizer-vi + grammar-checker-vi (with optional translationese-cleaner-vi pre-pass). Use whenever the user wants to take generated content (CVs, posts, articles, emails, cover letters) from draft to ready-to-publish in one step. Triggers: polish this, make this ready, humanize and proofread, clean this up, do the full pass, run the polish workflow. Runs three passes: (1) format-aware humanizer, (2) anti-fragmentation check, (3) format-aware proofreader/grammar check."
---

# Content Polish: End-to-End Workflow

This skill orchestrates the **humanizer** and **proofreader** skills in the correct order, with proper handoff between them, and adds a critical middle step that catches the most common failure mode: **over-fragmentation** (content reading like a list of short sentences instead of connected prose).

## Why This Skill Exists

Running humanizer then proofreader sequentially as separate skills produces sub-par results because:

1. The humanizer can over-correct: it strips em-dashes, kills -ing phrases, and mechanically "varies rhythm" which fragments connected ideas into staccato sentences.
2. The proofreader, applied to a CV, doesn't know that parallel structure across bullets is the format, not an error.
3. Neither skill knows the other ran. Format conventions get lost in handoff.
4. There's no anti-fragmentation pass between them so over-chopped content goes into the proofreader, which often fails to catch the issue (or worse, suggests further "clarity" fixes that fragment more).

This skill fixes all four problems.

---

## The Workflow

### Step 0 - Identify Document Type (DO THIS FIRST, ALOUD)

State the document type explicitly to the user before starting. This is the most important calibration decision and everything downstream depends on it.

Possible types:
- **CV / Resume** (bullets, parallel structure, action verbs)
- **Cover letter** (first-person warm-professional)
- **LinkedIn post** (mixed rhythm, opinion ok)
- **Blog post / Article** (full voice, varied rhythm)
- **Email** (recipient-calibrated)
- **Press release / Formal report** (third-person neutral)
- **Marketing copy** (fragments intentional)
- **Other** - ask the user

If unclear from context, ask once: *"Quick check: is this a CV bullet, LinkedIn post, blog, email, or something else? It changes the polishing rules."*

---

### Step 0.5 - Detect Language and Pick the Pipeline

Detect the content's primary language, then branch:

| Language | Step 1 (humanize) | Step 2 | Step 3 (check) |
|----------|-------------------|--------|----------------|
| **English** (or mixed, mostly EN) | `humanizer` | Anti-fragmentation | `proofreader` (post-humanizer mode) |
| **Vietnamese** (or mixed, mostly VN) | `humanizer-vi` | Anti-fragmentation | `grammar-checker-vi` |

**Vietnamese pre-pass:** if the VN draft shows translationese (English word order, nominalizations, "được"-heavy passives, business clichés translated literally — typical of translated or EN-prompted drafts), run `translationese-cleaner-vi` BEFORE Step 1. Skip if the draft reads as natively written Vietnamese.

Everything else in this workflow (Step 0 document typing, anti-fragmentation, output format, calibration card) applies to both pipelines. For Vietnamese, honor the register guidance in `humanizer-vi/references/registers.md` over the English soul/personality rules.

---

### Step 1 - Run the Humanizer (Format-Calibrated)

**English:** read and apply `~/.claude/skills/humanizer/SKILL.md`.
**Vietnamese:** read and apply `~/.claude/skills/humanizer-vi/SKILL.md` (follow its own workflow and preservation rules; the calibration instructions below still apply).

Load the document type as the calibration profile.

**Critical instructions for this step:**

- Pass the document type explicitly as the first thing the humanizer sees
- Do NOT apply blog-post rhythm rules to CVs
- Do NOT apply CV concision to blog posts
- Skip the "personality and soul" section for CVs, press releases, and formal reports
- Preserve all parallel structure in CV bullets
- Preserve metric numbers, dates, names, and product names exactly as written

**Output of this step:** Humanized draft (call it Version A).

---

### Step 2 - Anti-Fragmentation Pass (THE NEW MIDDLE STEP)

This is the step that fixes the most common failure of the previous workflow. Read Version A and check for these failure modes:

#### Failure Mode 1: Three-in-a-row short sentences
Count consecutive sentences under 12 words. If three or more appear in a row outside of marketing copy or intentional staccato, **merge** at least one pair using subordinate clauses, semicolons, or conjunctions.

Over-fragmented:
> *Led VPIM campaign. Budget was 12B VND. Team grew to 12 people. Top-3 ranking three years.*

Re-merged:
> *Led the 12B VND VPIM KOL/KOC campaign with a team of 12, contributing to a top-3 social media ranking three years running.*

#### Failure Mode 2: Bullets chopped into multiple sentences
A CV bullet should generally be **one sentence** (or one sentence plus an optional dependent clause). If the humanizer produced a bullet with multiple periods, recombine it.

#### Failure Mode 3: Lost connective tissue
The humanizer may have removed em-dashes or "which" / "while" / "because" phrases that carried logical relationships. If two adjacent sentences have a clear cause-and-effect or context-and-action relationship, restore the connection.

#### Failure Mode 4: Lost parallelism in CV sections
Read all bullets in a CV section together. They should share grammatical shape (all start with action verbs, all use the same tense, similar length). If the humanizer broke this, restore it.

#### Failure Mode 5: Over-stripped specifics
If the humanizer replaced a specific number, name, or date with vague language to "remove AI vocabulary," restore the specific. "Significant budget" should go back to "12B VND budget."

#### Vietnamese calibration (VN pipeline only)

The rules above are English-calibrated. For Vietnamese, adjust:

- **Threshold:** count tiếng (syllables), not words — flag three consecutive sentences under **~15–18 tiếng** (a 12-tiếng VN sentence carries the content of ~6–8 EN words, so the EN threshold under-fires).
- **Merge tools:** use VN connectors — *mà, nên, vì… nên, còn, trong khi, khiến* — plus relative clauses. Semicolons are rare in VN prose; don't introduce them.
- **Skip Failure Mode 3's em-dash restoration** — that's an EN-humanizer artifact. `humanizer-vi` is conservative and rarely over-chops, so this pass is a safety net for VN, not load-bearing. Failure Modes 1, 2, 4, 5 apply unchanged.

**Output of this step:** Version B (Version A with fragmentation fixed).

---

### Step 3 - Run the Proofreader (Format-Calibrated, Post-Humanizer Mode)

**Vietnamese pipeline:** read and apply `~/.claude/skills/grammar-checker-vi/SKILL.md` instead — it covers spelling, tone marks, punctuation, spacing, and sentence structure at depth. Still check for the post-humanizer over-correction failures listed below (lost specifics, broken parallelism), then produce Version C the same way.

**English pipeline:** read and apply the proofreader skill instructions from `~/.claude/skills/proofreader/SKILL.md` with two flags set:

1. **Document type:** Same as Step 0
2. **Post-humanizer mode:** ON (the proofreader has a specific section for this - it does additional checks for over-correction, lost specificity, broken parallelism)

The proofreader will produce:
- Issues found (grouped, with reasons)
- Overall assessment
- Optional clean rewrite if 3+ issues

Apply the proofreader's clean rewrite (if produced) to get **Version C**. If the proofreader only flags 1-2 minor fixes, apply them inline to Version B to get Version C.

**Output of this step:** Version C - the polished final.

---

### Step 4 - Final Read-Aloud Sanity Check

Before delivering to the user, mentally read Version C aloud and ask:

1. Does it sound like a real person wrote this for this format?
2. Does any sentence feel like Morse code (dot dot dot)?
3. Does any paragraph still have AI vocabulary tells (testament, leverage, robust, vibrant, pivotal, landscape, key)?
4. For a CV: are all bullets parallel and metric-rich?
5. For a blog: does it have a real voice?
6. For an email: would the recipient actually expect this register?

If anything feels off, fix it. Then deliver.

---

## Output Format

Present the result to the user like this:

```
**Document type detected:** [CV bullet / LinkedIn post / blog post / etc.]

**Polishing notes:**
- [1-3 bullet points on what was changed and why]
- [E.g., "Re-merged 4 fragmented bullets into single sentences for CV parallelism"]
- [E.g., "Restored '12B VND' specific where humanizer had genericized it"]
- [E.g., "Fixed 2 typos and one comma splice"]

**Final version:**

[Version C - the polished, ready-to-use content]
```

Skip lengthy issue lists in the final output. The user wants the polished version, not a report of every step. If they ask "what changed?", expand then.

---

## When NOT to Use This Skill

- **User wants ONLY humanizing** (no proofread): use humanizer directly
- **User wants ONLY proofreading** (no humanizing): use proofreader directly
- **User wants to see all issues for learning purposes**: use proofreader directly with full output
- **Single sentence or chat message**: this workflow is overkill - a quick proofread is fine
- **Code, technical specs, structured data**: this skill is for prose content

---

## Calibration Reminder Card

| Format | Sentence length | Voice | Parallelism | Soul/personality |
|--------|----------------|-------|-------------|------------------|
| CV bullet | Mixed (12-35 words) | Action verb led, no "I" | Required | Skip |
| Cover letter | Medium (18-30 words) | First person, warm | Loose | Light |
| LinkedIn post | Varied | First person, opinionated | None | Yes |
| Blog post | Varied (5-50 words) | Full voice | None | Yes |
| Email | Recipient-matched | Direct | None | Match recipient |
| Press release | Medium-long (20-35) | Third person neutral | Loose | Skip |
| Marketing copy | Whatever sells | Brand voice | Sometimes | Brand-dependent |

**Universal rule:** Never produce three short sentences (under 12 words each) in a row outside marketing copy. This is the over-fragmentation tell that the previous workflow kept producing.

---

## Reference

This skill orchestrates:
- English: `~/.claude/skills/humanizer/SKILL.md` (v3.0+) + `~/.claude/skills/proofreader/SKILL.md` (v2.0+)
- Vietnamese: `~/.claude/skills/humanizer-vi/SKILL.md` + `~/.claude/skills/grammar-checker-vi/SKILL.md`, optional `~/.claude/skills/translationese-cleaner-vi/SKILL.md` pre-pass

When polishing Vietnamese content: also load matching files from `skills/vietnamese-language/` via its SKILL.md routing table — covers platform-specific register, formal document conventions, Gen Z slang shelf-life, advertising regulatory constraints, and more.

Both skills must be at version 3.0+ and 2.0+ respectively for this orchestrator to work as designed. Older versions don't have the format calibration system or post-humanizer mode this workflow depends on.
