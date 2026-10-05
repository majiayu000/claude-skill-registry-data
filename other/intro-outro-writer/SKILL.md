---
name: intro-outro-writer
description: "Writes episode-specific intro and outro scripts matched to a podcast's tone, format, and brand — including the episode hook, show context, and closing with CTA — ready to record."
status: stable
category: podcast
subcategory: scripting
version: 1.0
eval_score: 4.4
tags: [podcast, scripting, intro, outro, branding, host-voice]
---
# Intro Outro Writer

## What This Skill Does
Writes episode-specific intro and outro scripts matched to a podcast's tone, format, and brand — including the episode hook, show context, and closing with CTA — ready to record.

## When To Use This Skill
- You are recording a new episode and need the intro and outro scripted before you hit record
- Your current intro feels dated or generic and you want a rewrite that reflects how the show has evolved
- You produce multiple shows and need consistent intro/outro formats without starting from scratch each time
- You want to test a new intro style (e.g., opening with the guest's most arresting line versus a host-led setup)

## What You Need To Provide
**Required:** Show name; episode topic or title; host name(s); tone of the show (casual, serious, irreverent, warm, authoritative)
**Optional:** Guest name and one-line context; the most compelling or surprising moment from the episode (a quote, a finding, a scene); target intro length (30 seconds, 45 seconds, 60 seconds at typical speaking pace); whether a music bed plays under the intro; whether the outro should include specific CTAs (subscribe, leave a review, follow on social, Patreon); any standard language that appears in every episode's intro or outro

## How the Assistant Approaches This
1. Identifies the strongest opening hook from the episode — ideally a specific quote, moment, or question that makes a cold listener need to know what happens next
2. Writes the intro in three parts: hook (5–10 seconds), episode context (10–15 seconds), host welcome and show ID (5–10 seconds) — calibrated to the requested length
3. Writes the outro in two parts: brief episode callback (2–3 sentences referencing what was just heard), then CTA sequence
4. Calibrates every word to spoken-aloud delivery — contractions, natural rhythm, and no written-English constructions that sound awkward when spoken
5. Optionally provides two intro variants: one opening with the hook-quote, one opening with a host-narrated setup — so the host can choose
6. After the scripts, provides a "Next Step" note: read both versions aloud before recording to choose the right variant, confirm the hook quote is approved for use, and whether show-notes-generator should be run alongside to complete the episode's publish assets

## Output Format
Two clearly labeled script blocks: INTRO and OUTRO. Each is marked with approximate spoken duration at 150 words per minute. Delivery notes in parentheses where tone or pacing matters. Written to be read directly into a microphone. Total: 200–350 words for both scripts combined. Output ends with a "Next Step" note: read both intro variants aloud before recording, confirm any quoted material is approved, and run show-notes-generator to create the matching episode publish assets.

## Quality Criteria
- [ ] The intro hook is specific to this episode — not a generic "today we're talking about X" opener
- [ ] The intro includes the show name within the first 30 seconds
- [ ] The outro does not repeat the intro's exact wording
- [ ] CTAs in the outro are specific and in the correct order (listen/share before subscribe; subscribe before Patreon)
- [ ] Both scripts read naturally at normal speech pace — test by reading aloud, not silently
- [ ] Guest name and context are included in the intro (if a guest episode)
- [ ] Output includes at least one concrete next action the user can take immediately (read aloud and choose a variant, confirm quoted material, or run show-notes-generator)

## Example

### Input
Show name: The Work It podcast
Episode topic: Why your company's performance review system is making everyone worse at their jobs
Guest: An organizational psychologist who studies workplace feedback systems
Host: Jamie
Tone: Smart, slightly sardonic, accessible
Most compelling moment: Guest said "Performance reviews measure how good you are at being reviewed, not how good you are at your job"
Target intro length: 45 seconds
CTAs: Subscribe + leave a review

### Output

---

**INTRO** *(~45 seconds spoken at 150wpm)*

*(Open on quote — optional music bed fades under)*

"Performance reviews measure how good you are at being reviewed — not how good you are at your job."

That's not a disgruntled employee talking. That's an organizational psychologist who has spent fifteen years studying what actually happens to people and organizations when they go through the annual review cycle.

*(Warm, direct)*

I'm Jamie, and this is The Work It podcast — where we dig into the systems that shape how we work, and why so many of them were designed without us in mind. Today: the performance review. Why it exists, who it actually serves, and what the research says about whether it does any of what it's supposed to do. Let's get into it.

*(~85 words / ~45 seconds at 150wpm)*

---

**OUTRO** *(~30 seconds spoken at 150wpm)*

*(Slightly warmer pace than the intro)*

If this conversation made you think about your own review cycle differently — or if it confirmed something you already suspected — I hope it was useful. The guest's research is in the show notes, along with a couple of the papers we referenced.

*(Direct)*

If you got something from this episode, the best thing you can do is subscribe — it helps more people find the show. And if you have a minute to leave a review, that means a lot. We'll be back next week.

*(~85 words / ~30 seconds at 150wpm)*

---

**Alternate INTRO — host-led setup** *(~45 seconds)*

*(Host narration, no opening quote)*

Every year, millions of workers sit in a meeting where their performance for the last twelve months is evaluated by one person, using a number or a letter grade, in a process that typically takes about 45 minutes. And then everyone goes back to work.

I'm Jamie, this is The Work It podcast, and today we're asking whether performance reviews actually work — and what happens when an organizational psychologist looks at the data. The answer is uncomfortable if you're the one who runs them. Let's go.

*(~80 words / ~45 seconds)*

---

## Known Limitations
- Script timing is estimated at 150 words per minute — actual delivery pace varies by host; read the script aloud and time it before recording to verify length
- Opening with a guest quote requires that quote to be identified before the intro is recorded; if the episode hasn't been edited yet, record a generic intro and re-record with the quote after edit lock
- These scripts do not include music direction or sound design cues — coordinate with your audio producer or editor for music bed timing
- CTA ordering follows standard podcast convention; adjust if your monetization structure is different (e.g., Patreon-first audiences may expect the membership mention earlier)

## Related Skills
- [call-to-action-generator](../../../youtube/scripting/call-to-action-generator/SKILL.md)
- [solo-episode-script](../solo-episode-script/SKILL.md)
- [show-notes-generator](../../post-production/show-notes-generator/SKILL.md)
