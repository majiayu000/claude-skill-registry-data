---
name: hook-generator
description: "Write three opening hook options — one per style — for a YouTube video, podcast intro, or documentary opening."
status: stable
category: youtube
subcategory: pre-production
version: 1.0
eval_score: 4.78
tags: [youtube, pre-production, hooks, retention, podcast, documentary]
---
# Hook Generator

## What This Skill Does
Write three opening hook options — one per style — for a YouTube video, podcast intro, or documentary opening. Each hook is 1–3 sentences and ready to use as-is.

## When To Use This Skill
- You have a video, episode, or film topic and need to write the first 15–30 seconds
- You have a draft hook but want stronger alternatives before filming
- You want to test which angle creates the most tension or curiosity before committing to a shoot

## What You Need To Provide
**Required:**
- Topic or premise in one to three sentences — what the video/episode is actually about
- Format: YouTube (long-form or Shorts), podcast, or documentary

**Optional:**
- Tone: serious journalism · popular science · entertainment (defaults to entertainment if not specified)
- Target audience: who this is for in one phrase (e.g., "first-time founders", "true crime listeners")
- A specific fact, statistic, or scene from your content that could anchor the hook

## How the Assistant Approaches This
1. **Identifies the core tension.** Before writing, finds the single most compelling thing about the topic — the counterintuitive fact, the unexpected outcome, the stakes that make this worth watching. This becomes the raw material all three hooks draw from.

2. **Writes one hook per style**, each attacking the tension from a different angle:
   - **Provocative question** — opens a knowledge gap the viewer needs to close. Does not ask rhetorical questions that answer themselves. The question should make the audience feel a personal stake.
   - **Surprising statistic or fact** — leads with a specific, counterintuitive number or detail. The specificity is what creates credibility and curiosity. Avoids vague superlatives.
   - **Bold declarative claim** — makes a confident, slightly controversial statement that reframes how the viewer thinks about the subject. Earns its confidence; does not bluster.

3. **Adapts register to tone.** Serious journalism hooks are measured and authoritative — they earn credibility without sensationalism. Popular science hooks trade in wonder and accessibility. Entertainment hooks lead with personality, energy, or a visual provocation. If the input tone is ambiguous, the assistant matches the most common register for the format.

4. **Respects the format.** YouTube hooks prioritize visual provocation and pattern interrupts. Podcast hooks rely entirely on language and often work best when they are conversational and surprising. Documentary openings can sustain a slower build — a declarative statement of place or time followed by a pivot.

5. **Recommends the immediate next step.** After delivering the hooks, specifies which to film or record first, and which related skill to use next (seo-title-optimizer to align the title, thumbnail-concept-brief to translate the hook's visual energy, or full-script-writer to expand).

## Output Format

Three labeled hook options. Each hook: 1–3 sentences, no more. No preamble, no rating, no explanation — just the hooks. After the three options, one line of practical guidance on which style tends to work best for the given format and tone. Output ends with a one-line "Next Step" specifying the immediate action: which hook to lead with and which skill to run next.

```
**Option 1 — Provocative Question**
[Hook text]

**Option 2 — Surprising Statistic**
[Hook text]

**Option 3 – Bold Claim**
[Hook text]

---
*Guidance: [One sentence on which option best fits this format/tone and why.]*
```

## Quality Criteria
- [ ] Each hook opens a knowledge gap — the viewer genuinely needs to keep watching to close it
- [ ] The surprising statistic option uses a specific figure or detail, not a vague claim
- [ ] No hook uses the phrase "in this video" or announces what the content will cover
- [ ] Tone matches the specified register (journalism / popular science / entertainment)
- [ ] Each option is genuinely distinct — not a rephrasing of the others
- [ ] Output fits the format: YouTube punchiness, podcast conversational pull, or documentary deliberateness
- [ ] Guidance note is specific and actionable, not generic
- [ ] Output includes at least one concrete next action the user can take immediately (which hook to use and what to do next: film it, run seo-title-optimizer, or open full-script-writer)

## Example

### Input
**Topic:** A deep-dive YouTube video about why most personal finance advice is designed for a demographic that no longer exists — the single-income household with a stable job and a pension.

**Format:** YouTube long-form (20–25 minutes)

**Tone:** Serious journalism

**Audience:** People in their 30s and 40s who feel financially behind despite doing everything they were told to do

### Output

**Option 1 — Provocative Question**
What if the reason you feel financially behind isn't that you're doing something wrong — but that you're following advice written for a version of the economy that ended in 1989?

**Option 2 — Surprising Statistic**
The most-cited personal finance framework in the English-speaking world was designed in an era when 62% of households had a single income, a defined-benefit pension, and a job they expected to keep for 30 years. That era ended before most of you started working.

**Option 3 — Bold Claim**
Most personal finance advice isn't broken. It's just optimized for someone who doesn't exist anymore — and using it without understanding that assumption will cost you.

---
*Guidance: For serious journalism aimed at this audience, Option 2 works hardest: the specific statistic signals research and authority, which earns trust before making the larger argument. Option 1 is strongest if the tone edges toward editorial or opinion.*

## Known Limitations
- The skill cannot verify statistics. If you supply a specific figure in your input, it will use it. If you don't, the surprising statistic option may construct a plausible-sounding one that requires fact-checking before filming.
- For topics where the core tension is genuinely obscure or highly technical, the hooks may be accurate but abstract — provide one concrete detail from your research to give the assistant something specific to anchor to.
- Documentary hooks benefit significantly from knowing the opening scene or image. Without that, this skill generates language-only hooks that may need visual adaptation.

## Related Skills
- [seo-title-optimizer](../seo-title-optimizer/SKILL.md) — write the title after locking the hook angle
- [thumbnail-concept-brief](../thumbnail-concept-brief/SKILL.md) — translate the hook's visual energy into a thumbnail direction
- [full-script-writer](../../scripting/full-script-writer/SKILL.md) — write the complete script once hook and title are confirmed
- [intro-outro-writer](../../../podcast/scripting/intro-outro-writer/SKILL.md) — podcast-specific intro/outro writing
