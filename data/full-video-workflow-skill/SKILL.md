---
name: full-video-workflow-skill
description: Complete pre-production workflow that chains research, project creation, script generation, and presentation in one seamless flow. Use when starting a new video from competitor research all the way through to a ready-to-record script.
---

# Full Video Workflow Skill

## Overview

This skill chains the complete pre-production workflow into a single, guided experience:

1. **Research** — Analyze competitor videos
2. **Ideation** — Generate video ideas with virality scores
3. **Creation** — Set up project folder structure
4. **Script** — Write the full script with production notes
5. **Verification** — Fact integrity checkpoint
6. **Validation** — vidIQ keyword check
7. **Presentation** — Optional visual aid generation

**One command → Ready to record.**

---

## FACT INTEGRITY RULES (Inherited)

This skill combines multiple skills. All fact integrity rules from:
- `/video-research` (transcript extraction)
- `/video-presentation` (slide content)

**Apply throughout.** See global rules in CLAUDE.md.

---

## When to Use

Triggers:
- "full workflow"
- "complete pre-production"
- "research and create video"
- "analyze competitors and make a video"
- "start to finish video prep"
- User provides competitor URLs and wants full pre-production

---

## Workflow

### Step 1: Collect Competitor URLs

Ask user for 1-10 YouTube video URLs to analyze.

```
"Let's start your complete pre-production workflow!

Please provide 1-10 competitor video URLs I should analyze.
These will inform your video's angle, structure, and hooks."
```

### Step 2: Fetch Transcripts via Playwright MCP

For each video URL:
1. Navigate to video
2. Take snapshot for metadata (title, views, channel, length)
3. Click "Show transcript"
4. Extract transcript text
5. Close browser when done

**If extraction fails:** Fall back to Python script or ask for manual input.

### Step 3: Analyze Patterns

For each transcript, extract:
- **Hook Analysis:** What grabs attention in first 30 seconds?
- **Structure:** How is content organized?
- **Quotable Moments:** What statements stand alone as clips?
- **Engagement Patterns:** How do they maintain energy?
- **Gaps:** What's missing that you could add?

Present summary to user:
```
## Competitor Analysis Summary

### Video 1: [Title]
- Hook: [Description]
- Structure: [Pattern]
- Strength: [What they do well]
- Gap: [What's missing]

### Video 2: [Title]
...

### Patterns Across Videos:
- Common hooks: [List]
- Common structures: [List]
- Underserved angles: [List]
```

### Step 4: Generate Video Ideas

Create 3-5 video ideas with:

| Element | Content |
|---------|---------|
| Title Options | 3 alternatives (keyword, curiosity, contrarian) |
| Why It Will Perform | Search demand + differentiation |
| Hook Concept | Opening approach |
| Virality Score | 1-10 |
| Unique Angle | What YOU add that others don't |
| Main Points | Key sections to cover |

Present ideas and ask user to select one:
```
## Video Ideas

### Idea 1: [Title]
**Virality Score:** 8/10
**Why it works:** [Explanation]
**Hook:** [Concept]
**Unique angle:** [What makes it different]

### Idea 2: [Title]
...

Which idea would you like to develop? (1-5)
```

### Step 5: Create Project Folder

Once user selects an idea:

```bash
VIDEO_TITLE="[Sanitized Title]"
mkdir -p ~/YT/Ideas/"$VIDEO_TITLE"/{01_Script,02_Raw_Footage/{Screen_Recordings,Face_Cam},03_Audio/{Original,Processed},04_Assets/{B-Roll,Graphics,Music_SFX},05_Project_Files,06_Exports/{Long_Form,Shorts},07_Thumbnails}
```

### Step 6: VERIFICATION CHECKPOINT

Before generating script, present all extracted claims:

```
## 🔒 VERIFICATION CHECKPOINT

I extracted these factual claims from the competitor videos:

### ✅ VERIFIED (from transcripts with timestamps)
| Claim | Source | Timestamp |
|-------|--------|-----------|
| [claim] | [video title] | [MM:SS] |

### ⚠️ UNVERIFIED (mentioned but no citation)
| Claim | Source |
|-------|--------|
| [claim] | [video title] |

### ❌ WILL NOT USE (cannot verify)
| Claim | Reason |
|-------|--------|
| [claim] | [reason] |

**Should I proceed with only verified claims?**
**For unverified claims, should I attribute them as "According to [video]..."?**
```

Wait for user confirmation before proceeding.

### Step 7: Generate Script

Create script adapted to content type:

| Content Type | Structure |
|--------------|-----------|
| Tutorial | Problem → Solution → Demo → Variations |
| Comparison | Context → Option A → Option B → Verdict |
| Explainer | Hook → Core concept → Examples → Implications |
| News/Reaction | News → Why it matters → Hot take → What's next |

Script includes:
- `[FACE CAM]` and `[SCREEN RECORDING]` markers
- `[PAUSE]` and `[EMPHASIS]` for delivery
- 3-5 naturally quotable clip moments
- Production notes for B-roll and graphics
- Shorts potential section

Save to: `~/YT/Ideas/[Title]/01_Script/script.md`

### Step 8: Create Research Documentation

Create `research.md` with:
- All analyzed videos with timestamps
- Extracted claims with sources
- Verification status of each claim
- Differentiation strategy

Save to: `~/YT/Ideas/[Title]/01_Script/research.md`

### Step 9: Create todo.md

Create comprehensive progress tracker:

```markdown
# [Video Title] - Production Progress

**Created:** [Date]
**Current Phase:** Pre-Production (Script Ready)
**Last Updated:** [Date/Time]
**Source:** Full Workflow Skill

## Research & Planning
- [x] Competitor videos analyzed ([X] videos)
- [x] Video idea selected
- [x] Folder structure created
- [x] Verification checkpoint passed
- [ ] Topic validated in vidIQ
- [ ] Keywords incorporated

## Script
- [x] Script draft generated
- [ ] Hook alternatives tested
- [ ] vidIQ AI review incorporated
- [ ] Final polish complete

## Presentation (Optional)
- [ ] Presentation slides generated
- [ ] Saved to 04_Assets/Graphics/

## Recording
[Standard recording checklist]

## Post-Production
[Standard post-production checklist]

## Export & Publish
[Standard export checklist]

## Notes
- Research videos: [URLs]
- Unique angle: [Description]
- Virality score: [X]/10
- vidIQ keywords: [To be validated]
```

### Step 10: vidIQ Validation Prompt

```
Script is ready! Before recording, validate with vidIQ:

1. Go to vidIQ → Keywords Tool
2. Search: "[primary keyword]" and alternatives
3. Paste back: KEYWORD, SCORE, VOLUME, COMPETITION, RELATED

This ensures your video is discoverable.

(Say "skip vidiq" if you want to proceed without validation)
```

### Step 11: vidIQ AI Review Prompt

```
Script ready for vidIQ AI review:

1. vidIQ → AI Coach
2. Share title + script
3. Ask for retention, SEO, virality feedback
4. Paste full feedback here

I'll incorporate the recommendations into the script.

(Say "skip review" to proceed without)
```

### Step 12: Offer Presentation Generation

```
Would you like me to create an interactive presentation for screen recording?

This is helpful for:
- Tutorial walkthroughs
- Comparisons and verdicts
- Step-by-step explanations
- Data visualization

Options:
1. Yes - Create presentation now
2. No - I'll record without visual aids
3. Later - I'll invoke /video-presentation when ready
```

If yes, invoke `/video-presentation` skill with context pre-filled.

### Step 13: Offer Metadata Generation

After script and optional presentation:

```
Would you like me to generate YouTube metadata now?

This creates metadata.md with:
- Optimized title (with vidIQ validation)
- Full description with timestamps
- Tags (up to 500 characters)
- Hashtags
- Thumbnail brief
- Pre-upload checklist

Options:
1. Yes - Full metadata with vidIQ validation (~5 min)
2. Quick - Generate metadata without vidIQ (I'll validate later)
3. Later - I'll invoke this when ready to upload
```

#### If User Selects Full Metadata with vidIQ

Follow structured copy-paste workflow:

**Step 13a: Keyword Validation**
```
## vidIQ Keyword Check

Please validate your keywords:

1. Go to: https://app.vidiq.com → Keywords Tool
2. Search these terms:

   PRIMARY: "[primary keyword from script]"
   ALT 1: "[alternative 1]"
   ALT 2: "[alternative 2]"

3. For EACH keyword, paste back:

---
KEYWORD: [keyword]
SCORE: [0-100]
VOLUME: [e.g., 12K]
COMPETITION: [Low/Medium/High]
TREND: [Rising/Stable/Declining]
RELATED: [top 5 related, comma-separated]
---

(Type "skip" to proceed without keyword data)
```

**Step 13b: Title Optimization**
```
## Title Check

Test your title in vidIQ:

1. Go to vidIQ → AI Title Generator
2. Enter: "[current title from script]"
3. Paste back:

---
TITLE: [your title]
SCORE: [0-100]
SUGGESTIONS:
1. [alt 1]
2. [alt 2]
3. [alt 3]
---

(Type "skip" to keep current title)
```

**Step 13c: Tag Collection**
```
## Tag Suggestions

For best tags:

1. Use vidIQ extension on a top competitor video
2. Check their tags section
3. Paste the most relevant ones:

---
COMPETITOR TAGS: [comma-separated list]
---

Or type "generate" and I'll create tags from keywords.
```

**Step 13d: Generate metadata.md**

Create `~/YT/Ideas/[Title]/01_Script/metadata.md` with complete YouTube-ready metadata including:
- Title with character count and vidIQ score
- Description with timestamps extracted from script sections
- Tags optimized for 500 character limit
- Hashtags for description and Shorts
- Thumbnail brief based on competitor analysis
- Pre-upload checklist
- vidIQ data log

#### Graceful Fallback Handling

If user skips vidIQ steps or provides incomplete data:
- Use available data + best practices
- Mark in metadata.md: `**vidIQ Data:** Partial/Skipped`
- Add reminder: `**Recommendation:** Validate in vidIQ before upload`

```
No worries! I'll generate metadata with what we have.

You can always:
1. Validate keywords in vidIQ before upload
2. Use YouTube Studio's tag suggestions
3. Check competitor descriptions for ideas

Proceeding with best-effort metadata...
```

---

## Output Summary

At the end of the workflow, user has:

| Deliverable | Location |
|-------------|----------|
| Project folder | `~/YT/Ideas/[Title]/` |
| Full script | `01_Script/script.md` |
| Research notes | `01_Script/research.md` |
| YouTube metadata | `01_Script/metadata.md` (if generated) |
| Progress tracker | `todo.md` |
| Presentation (optional) | `04_Assets/Graphics/[topic]-presentation.html` |

**Pre-production complete. Ready to record.**

---

## Troubleshooting

### Transcript Extraction Fails
See troubleshooting in `/video-research` skill.

### User Wants to Skip Steps
Allow skipping:
- vidIQ validation ("skip vidiq")
- vidIQ AI review ("skip review")
- Presentation generation ("no thanks")

Do NOT allow skipping:
- Verification checkpoint (fact integrity required)

### User Changes Mind Mid-Workflow
If user wants different idea after starting:
- Ask: "Would you like to go back to idea selection?"
- If yes, return to Step 4 with same analysis
- Delete any created folders

---

## Example Interaction

```
User: "Full workflow with these videos: [URL1], [URL2], [URL3]"

Claude: "Starting complete pre-production workflow!

Analyzing 3 competitor videos..."

[Fetches transcripts, analyzes patterns]

"## Competitor Analysis Summary
...

## Video Ideas
1. [Idea with 8/10 virality]
2. [Idea with 7/10 virality]
3. [Idea with 9/10 virality]

Which would you like to develop?"

User: "3"

Claude: "Great choice! Creating project folder...

## 🔒 VERIFICATION CHECKPOINT
[Lists all claims with sources]

Should I proceed with verified claims only?"

User: "Yes"

Claude: [Generates script, creates files]

"✅ Pre-production complete!

**Created:**
- Project folder: ~/YT/Ideas/[Title]/
- Script: 01_Script/script.md (12 min, 6 sections)
- Research: 01_Script/research.md
- Progress: todo.md

**Next steps:**
1. Validate keywords in vidIQ
2. Get vidIQ AI review (optional)
3. Record!

Would you like me to create a presentation for screen recording?"
```
