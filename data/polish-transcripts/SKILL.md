---
name: polish-transcripts
description: Polish raw interview transcripts into searchable, well-structured markdown with metadata, dynamic headers, and full fidelity to technical content. Designed for Ray Peat interview podcasts and similar shows where technical accuracy is paramount.
---

# Polish Transcripts Skill

Transform raw transcripts into discoverable, navigable documents where an LLM agent can find specific information without reading the entire transcript. This skill maintains 100% fidelity to technical and medical content while improving readability.

**Designed for automation:** Process 100+ transcripts consistently with built-in quality control and token-efficient chunking.

---

## Speaker Reference

**Standard Speakers (Ask Your Herb Doctor shows):**
- **Andrew Murray** - Host (often Speaker A or Speaker B)
- **Sarah Johanneson Murray** / **Sarah Murray** - Co-host (often Speaker D)
- **Dr. Raymond Peat** - Guest expert (often Speaker C or Speaker B)
- **Michael** - Engineer (when identified)
- **Caller** - Call-in guests (use "Caller" unless name is provided)

**Common Transcription Errors:**
- "Dr. Pete" → "Dr. Raymond Peat" or "Dr. Peat"
- "Pete" → "Peat"
- "fat fish in diet" → "fat-free diet" (context-dependent)
- "Kmud Garberville" → "KMUD Garberville"
- Speaker labels are often inconsistent—use context to identify

---

## Core Fidelity Principle: The Impartial Spectator

**The Impartial Spectator Test:**
When deciding what to clarify vs. what to preserve verbatim, ask: "Would an objective, neutral observer see this change as *necessary for comprehension* or as *interpretation*?"

- ✅ **Clarify:** "fat fish in diet" → "fat-free diet" (obvious transcription error)
- ✅ **Clarify:** Add missing punctuation that impedes reading
- ❌ **Don't interpret:** Awkward phrasing that's authentic to speaker
- ❌ **Don't interpret:** Unclear passages—flag with [unclear] instead

**Preserve the speaker's authentic voice.** The goal is to make the transcript *readable*, not to make it *formal* or *perfect*.

---

## Workflow: Five Sequential Stages

### STAGE 0: Initial Assessment & Planning (First Read)

**Purpose:** Understand the transcript structure before polishing.

1. **Read first 500 lines** of raw transcript to identify:
   - Speakers and their typical labels (Speaker A/B/C mapping)
   - Show date and context
   - Major topic boundaries (look for questions from hosts/callers)

2. **Skim entire transcript** (or read in 500-line chunks) to create a preliminary chapter outline:
   - Mark where topics substantially change
   - **Key trigger:** New questions from hosts or callers typically signal topic changes
   - Note: This is a judgment call—aim for 5-10 major sections per hour of content

3. **Output:** Mental or written map of major sections and their topics

---

### STAGE 1: Create Document Structure

**Purpose:** Build the skeleton before polishing content.

1. **Create new markdown file** named: `[filename]_polished.md` (replace `_raw` with `_polished`)

2. **Add YAML Front Matter at very top:**

```yaml
---
title: "[Descriptive Topic] - [Show Name] [Date]"
show_name: "[Exact show name]"
date: "YYYY-MM-DD"
speakers:
  - "[Full Name - VERIFIED from STEP 1]"
  - "[Full Name - VERIFIED from STEP 1]"
---
```

3. **Create preliminary Table of Contents** (without line numbers):

```markdown
## Table of Contents

[[#Chapter Header 1|Chapter Header 1]]
[[#Chapter Header 2|Chapter Header 2]]
[[#Chapter Header 3|Chapter Header 3]]
```

**Rules:**
- Use the chapter titles identified in Stage 0
- Do NOT add line numbers yet (these come in Stage 4)
- This TOC serves as a roadmap for polishing

---

### STAGE 2: Polish Content in Chunks

**Purpose:** Transform raw transcript into readable content while preserving fidelity.

**Token Management:**
- Process **300-500 lines of raw transcript at a time** (not 1,500-2,000)
- This prevents output token limits and maintains consistency
- Pause after each chunk for review

**Process for Each Chunk:**

1. **Remove radio mechanics first:**
   - Station IDs, underwriter announcements, fundraising pitches
   - Call-in numbers (except first mention if contextually important)
   - Scheduling info: "You're invited to call in from 7:30 to 8:00"
   - Audio troubleshooting: "Can you hear me? Is that better?"

2. **Apply speaker labels:**
   - Replace [Speaker A/B/C] with actual names from Speaker Reference
   - Format: `**[Full Name]:** [Content]`
   - Don't repeat name if same speaker continues in next paragraph

3. **Insert headers when topic changes:**
   - **Primary trigger:** New question from host or caller
   - Secondary triggers: Explicit topic shifts, time breaks
   - Format:
     ```markdown
     ## [Specific, Clear Chapter Title]
     tags: [[tag1]] [[tag2]] [[tag3]] [[tag4]]

     **[Speaker]:** [Opening dialogue of this section]
     ```

4. **Add line breaks within speaker segments:**
   - Break up long monologues (3+ sentences) into shorter paragraphs
   - Preserve natural thought boundaries
   - Improves readability without changing content
   - Example:
     ```markdown
     **Dr. Raymond Peat:** The political action has been almost entirely based on a mathematical model from Imperial College in London. They predicted several million deaths if there wasn't a lockdown.

     This group, led by Neil Ferguson, published an article in Nature magazine pushing the same discredited model. They're neglecting that the influenza season drops off in spring and summer.
     ```

5. **Apply light-touch polishing** (see Content Polishing Standards below)

6. **End chunk with continuity marker:**
   - If pausing mid-section, include the next speaker's opening line
   - This ensures smooth pickup in the next chunk

---

### STAGE 3: Quality Control Review

**Purpose:** Verify fidelity and consistency before finalizing.

**Quality Control Checklist:**

- [ ] All speakers correctly identified (no Speaker A/B/C labels remaining)
- [ ] All medical/technical facts preserved exactly
- [ ] Headers align with major topic changes (typically new questions)
- [ ] Tags are relevant and consistent (3-5 per section)
- [ ] Line breaks improve readability without altering meaning
- [ ] No radio mechanics remain unless contextually important
- [ ] Speaker personality and voice preserved
- [ ] No interpretation or rephrasing of unclear passages
- [ ] Substantive caller interactions preserved
- [ ] Natural conversation flow maintained

**If issues found:** Return to Stage 2 and fix before proceeding.

---

### STAGE 4: Finalize Table of Contents

**Purpose:** Add line numbers to TOC after polishing is complete.

1. **Read the polished file** to get actual line numbers for each header

2. **Update TOC** with line numbers:

```markdown
## Table of Contents

Line 11 - [[#Introduction|Introduction]]
Line 27 - [[#Pandemic Policy and Mortality Data|Pandemic Policy and Mortality Data]]
Line 93 - [[#The Great Reset|The Great Reset]]
```

3. **Verify:** Click each link to ensure it jumps to the correct section

---

## Content Polishing Standards

### Core Principle
**100% FIDELITY to meaning + MAXIMUM READABILITY**

Apply the **Impartial Spectator Test** (see above) to every edit.

---

### What to ALWAYS Remove:

- **Pure radio mechanics:** Station IDs, frequency announcements, underwriter announcements
- **Scheduling/logistical info:** "You're invited to call in from 7:30 to 8:00 PM", "the number is 707-923-3911"
- **Repeated call-in invitations** (keep first mention if contextually relevant)
- **Audio troubleshooting:** "Can you hear me? Is that better?" unless it affects content
- **Generic filler:** Excessive "um, uh, you know, like" that impedes reading
- **Incomplete fragments:** "So I was going to— well actually—" that don't complete a thought
- **Redundant acknowledgments:** "Yeah, yeah, okay, yeah" when repeated without content

---

### What to ALWAYS Keep:

- **ALL medical/technical information** (100% fidelity to every fact, figure, mechanism, dosage, reference)
- **Speaker personality:** Casual phrasing, hesitations, authentic speech patterns ("I knew, I know")
- **Substantive asides:** References, anecdotes, explanatory details ("Guangdong virus of 1996", MLK quotes)
- **Relationship dynamics:** "As we discussed before", credibility signals, rapport building
- **Thinking process:** Even imperfect phrasing that shows how ideas develop
- **Call-in interactions:** Questions from callers, their backgrounds when relevant to discussion
- **Credibility markers:** Experience, track record ("I've followed this for 40 years")
- **Emotional tone:** Emphasis, frustration, humor, passion
- **Awkward/unusual phrasing:** Speaker's authentic voice ("the classical thing is", "very likely through science")
- **Substantive technical discussions:** Even if they wander or are exploratory

---

### Light Touch Edits Only:

- Fix obvious transcription errors ("Pete" → "Peat", "fat fish in diet" → "fat-free diet")
- Add missing punctuation that impedes reading (commas, periods—not speech punctuation)
- Fix clear misspeaks where context reveals intent
- Normalize speaker labels and format (not content)
- Clean up "um, uh" stuttering at phrase starts only (not mid-speech)
- Fix capitalization of proper nouns (KMUD, names, places)

---

### DO NOT:

- Rephrase in your own words
- Reinterpret garbled or confusing passages—preserve them and flag with [unclear] if needed
- Change vocabulary or technical terminology
- Over-formalize natural speech
- Remove personality markers or hesitations
- Remove substantive details (names, references, explanatory asides)
- Add content that wasn't in the original
- Condense substantive technical discussions

---

### Speaker Formatting:

```markdown
**[Full Name]:** [What they said]
```

**Rules:**
- Use actual names from Speaker Reference, not "[Speaker A]"
- Don't repeat name if same speaker continues in next paragraph
- Use "Caller" or "Caller (Name)" if caller name is provided
- Use "Michael (Engineer)" or "Engineer" for technical staff

**Line Breaks Within Speaker Segments:**
- Break long monologues (3+ sentences) into multiple paragraphs
- Use natural thought boundaries
- Improves scannability and readability
- Don't break mid-thought or mid-sentence

---

### Header & Tag Guidelines:

**When to Insert Headers:**
- **Primary trigger:** New question from host or caller
- **Secondary triggers:** Explicit topic announcements, return from break, major subject shift
- **Frequency guidance:** Typically 5-10 major sections per hour of content
- **Judgment call:** Use your understanding of the content to determine what constitutes a "substantial" topic change

**Tag Selection:**
- 3-5 tags per section
- Lowercase-hyphenated format: `[[covid-19]]`, `[[carbon-dioxide]]`
- Mix of specific and general: `[[thyroid-function]]` + `[[hormones]]`
- Technical terms: Use exact terminology from discussion
- Include both topic tags and concept tags

**Header Format:**
```markdown
## [Clear, Specific Chapter Title]
tags: [[tag1]] [[tag2]] [[tag3]] [[tag4]]

**[Speaker]:** [Opening dialogue]
```

---

## Examples

### Example 1: Opening Segment (Removing Radio Mechanics)

**BEFORE:**
```
[Speaker A]: 53 degrees outside 7pm Kmud Garberville, Kmue, Eureka K L A I Laytonville. Where the views and opinions expressed throughout the broadcast day are those of the speaker and not necessarily the station staff, underwriters or volunteers.
[Speaker B]: Sam Sa. Sam Sa.
[Speaker A]: And I believe I have the herb doctor here.
[Speaker C]: Hey, good evening.
[Speaker A]: Good evening. And we have Dr. Pete. Take it away.
[Speaker C]: Welcome to this month's ask your herb doctor. The see here, November 19th edition, 2021. My name is Andrew Murray.
```

**AFTER:**
```markdown
## Introduction
tags: [[intro]] [[welcome]] [[show-format]]

**Andrew Murray:** Welcome to this month's Ask Your Herb Doctor, the November 19th, 2021 edition. My name is Andrew Murray.
```

**What Removed:** Station ID, legal disclaimer, audio cues ("Sam Sa"), technical handoff
**What Kept:** Show introduction, date, host name

---

### Example 2: Technical Content (Preserving Fidelity)

**BEFORE:**
```
[Speaker B]: A couple of the abstracts you're referring to I think mentioned that on a high fish oil diet, the Metastasis was about 1,000 times worse than on a low fat diet. Just a huge difference from supplementing fish oil versus not having fat. And we can make all of the unsaturated and saturated fats that we need from carbohydrates.
```

**AFTER:**
```markdown
**Dr. Raymond Peat:** A couple of the abstracts you're referring to mentioned that on a high fish oil diet, metastasis was about 1,000 times worse than on a low fat diet. Just a huge difference from supplementing fish oil versus not having fat. We can make all of the unsaturated and saturated fats that we need from carbohydrates.
```

**What Changed:** Speaker label (Speaker B → Dr. Raymond Peat), fixed capitalization ("Metastasis" → "metastasis"), removed filler ("I think")
**What Stayed:** Every fact, exact numbers (1,000 times), Ray's casual style ("just a huge difference")

---

### Example 3: Line Breaks Within Speaker Segments

**BEFORE:**
```
[Speaker C]: The political action has been almost entirely based on a mathematical model of an infection produced by a group at the Imperial College in London and delivered to the government March 16 and set them into motion on this lockdown because they predicted several million deaths if they didn't lock down. And this group, Neil Ferguson and his group at the Imperial College, published an article more recently in Nature magazine pushing the same absolutely discredited mathematical model nonsense, saying that, see, several million people didn't die and you locked down, therefore the lockdown prevented millions of deaths, neglecting that the influenza season drops off in the spring and summer.
```

**AFTER:**
```markdown
**Dr. Raymond Peat:** The political action has been almost entirely based on a mathematical model from a group at Imperial College in London, delivered to the government on March 16. They predicted several million deaths if there wasn't a lockdown.

This group, led by Neil Ferguson, published an article in Nature magazine pushing the same discredited model. They're saying that because several million people didn't die after lockdown, the lockdown prevented millions of deaths. They're neglecting that the influenza season drops off in spring and summer.
```

**What Changed:** Added line break for readability, light punctuation fixes
**What Stayed:** All facts, technical details, Ray's critical tone ("discredited model nonsense" → "discredited model")

---

### Example 4: Call-In Segment (Condensing Logistics, Keeping Content)

**BEFORE:**
```
[Speaker A]: And we have a couple callers.
[Speaker C]: Okay, we're good, let's hold that there. Caller, you're on the air. Where are you from and what's your question?
[Speaker A]: It was a local person who was a very bad connection. But they wanted to know what you thought of flax oil and avocados.
```

**AFTER:**
```markdown
**Andrew Murray:** We have a caller. Where are you from and what's your question?

**Michael (Engineer):** It was a local person with a bad connection, but they wanted to know what you thought of flax oil and avocados.
```

**What Removed:** Technical coordination ("Okay, we're good, let's hold that there")
**What Kept:** Call-in interaction, engineer relay, the actual question

---

## Processing Strategy for 100+ Transcripts

**For Consistent Automation:**

1. **Use the same workflow for every transcript** (Stages 0-4)
2. **Process in small chunks** (300-500 lines raw → ~200-350 lines polished)
3. **Run QC checklist** (Stage 3) before finalizing each transcript
4. **Track common patterns** across transcripts to refine the skill
5. **Maintain a running glossary** of speaker names, common errors, and technical terms

**Token Management:**
- Smaller chunks prevent output limit issues
- Allows for mid-process review and adjustment
- Maintains consistency across long transcripts

**Quality Assurance:**
- Every transcript goes through the same QC checklist
- No transcript is finalized without Stage 3 review
- Consistency builds over time as patterns are recognized

---

## Iteration & Improvement

This skill improves through use. As you process transcripts:
- Note recurring transcription errors and add them to the reference
- Refine header placement based on what makes transcripts most navigable
- Adjust tag vocabulary for consistency across the corpus
- Update examples based on edge cases encountered

The goal: A polished corpus where any transcript can be searched, navigated, and understood without reading the full text, while preserving 100% fidelity to the original content.
