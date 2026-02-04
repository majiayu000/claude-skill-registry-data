---
name: continuity-checking
description: Validate cross-episode continuity by scanning scenes for invented details, contradictions, and timeline violations. Use after scene creation/editing to detect continuity errors. Triggers include "check continuity", "validate continuity", "continuity check", "continuity violations", "cross-check episodes".
---

# Continuity Checking

Validate scene content against all prior episodes and established canon to detect continuity violations, invented details, and timeline errors.

## When to Use This Skill

Use this skill when you need to:
- Validate a newly written scene for continuity errors
- Check edited scene for contradictions introduced during rewrite
- Audit an episode for consistency before compilation
- Verify no details were invented that contradict canon

## What This Skill Detects

### 0. The Secrecy Rule Violations (MOST CRITICAL - STORY-BREAKING)

**Doogan's business model requires targets never know they're part of a paid operation.**

**Documentation:**
- `elements/checklist.md` → "The Secrecy Rule" section
- `elements/notes.md` → "The Secrecy Rule" section
- `elements/characters/doogan-andrews.md` → "Relationships" → Secrecy Rule

**Violation Detection:**
Scan dialogue for any references to:
- ❌ Payment ("paid you," "paying you," "how much")
- ❌ Hiring ("hired you," "whatever you're hired for")
- ❌ Job/Work ("your job," "this is work for you")
- ❌ Service ("providing a service," "babysitting me")

**Acceptable Skepticism (NOT violations):**
- ✅ "You're too perfect"
- ✅ "This feels like a setup"
- ✅ "You're really good at this"
- ✅ Emotional doubt about authenticity

**Context:**
- Targets may doubt the connection is genuine
- Targets may be suspicious of timing or convenience
- But targets NEVER discover it's a paid transaction
- Discovery would end job immediately (story crisis event)

**Validation Process:**
1. Scan ALL dialogue in target scene
2. Flag ANY language suggesting payment/hiring/job
3. Check if character is a target (not client, not team member)
4. If target uses payment/job language → **CRITICAL VIOLATION**

### 1. Invented Details (Most Critical)

**Proper Nouns:**
- Store names not mentioned in prior scenes (e.g., "Ralphs" when only "grocery store" was used)
- Street names, business names, location names not established
- Pet names, nicknames not previously introduced
- Brand names for cars, clothing, products

**Physical Descriptions:**
- Car makes/models not in character files or prior scenes
- Home/apartment details not established
- Clothing brands, styles, or colors not mentioned
- Physical traits not in character files (eye color, height, build)

**Objects & Props:**
- Specific items appearing that weren't established
- Technology specs (phone models, laptop brands)
- Food/drink specifics not mentioned before

### 2. Character Knowledge Violations (CRITICAL - FUNDAMENTAL TO ALL FICTION)

**Core Principle: Characters can ONLY know what they've experienced or been told UP TO THIS MOMENT.**

This is not a style choice. This is fundamental to writing believable characters.

**Three types of knowledge violations:**

**Type 1: Factual Knowledge (Specific Details)**
- Character knowing information they haven't learned yet (**common violation**)
- Character using proper names/details they weren't told
- Character forgetting information they learned earlier
- POV character knowing off-screen events without being told

**Type 2: Contextual Knowledge (Situational Framework)**
- Character assumes situation is about X when they only know about Y
- Character asks questions that reveal contextual understanding they lack
- Character operates in wrong interpretive framework

**Type 3: Future Knowledge (MOST COMMON VIOLATION - NEW)**
- Character references events from future scenes
- Character anticipates plot points they have no reason to expect
- Character "sets up" callbacks they couldn't know about
- Character mentions details that haven't been revealed yet
- Character displays knowledge of future beats in the outline

**Example: Context vs Facts**
```
Facts: Doogan met Annabelle, they had dinner, she died
Context A (Martinez): Romantic date gone wrong
Context B (Reader): Professional rebound job gone wrong

Martinez operates in Context A because that's what he was told.
Martinez CANNOT ask questions from Context B without new information.
```

**Example: Future Knowledge Violations**
```
❌ VIOLATION (Scene 7): "Save that Britney impression for later"
   Analysis: Character references event from Scene 10
   Source check: When did character see/hear about Britney impression? NO SOURCE.
   Fix: Remove reference entirely. Let Scene 10 be spontaneous.
   
❌ VIOLATION (Scene 3): "This will be important for the investigation"
   Analysis: Character knows investigation will happen (future plot)
   Source check: Why would character anticipate investigation? NO REASON.
   Fix: Character acts in present moment without foreshadowing.
   
❌ VIOLATION (Scene 5): "I'll need this golf club setup for Thursday"
   Analysis: Character prepares for specific future scene
   Source check: Why would character know Thursday matters? OUTLINE ONLY.
   Fix: Character deals with present situation, not future plot beats.

✅ CORRECT (Scene 7): "My wife watches her show"
   Analysis: References plausible background knowledge
   Source check: Character could be fan of comedian. Plausible.
   
✅ CORRECT (Scene 8): "You mentioned the tournament starts tomorrow"
   Analysis: References prior dialogue from earlier scene
   Source check: Scene 6 conversation. Clear source.
```

**Information Source Tracking:**
- Every fact a character uses must have a SOURCE
- Every context a character operates in must have a BASIS
- Every reference must have a WHEN (which prior scene established this)

**Future Knowledge Detection Process:**
1. **Scan all dialogue and character thoughts**
2. **For each reference to a fact/event/detail, ask:**
   - When did this character learn this information?
   - Which scene showed them learning it?
   - OR: Is this in their character background file?
3. **If answer is "outline says it happens later" → FLAG AS VIOLATION**
4. **If answer is "it's for comedic setup" → STILL A VIOLATION**
5. **If answer is "reader needs to know" → READER ≠ CHARACTER**

**Common Sources of Future Knowledge Violations:**
- Writer knows outline, characters don't
- Writer wants to set up callback, but character wouldn't know to plant it
- Writer wants to foreshadow, but character lives in present moment
- Writer wants dramatic irony, but achieves it by breaking character knowledge

**Fix Strategy:**
- Remove future references entirely
- Let moments happen spontaneously when they arrive
- Trust the reader to connect dots WITHOUT character foreshadowing
- Keep characters in their present moment
- Sources: witnessed, told directly, overheard, deduced from evidence, read/researched
- **If no source exists in prior scenes, character CANNOT know this**

**Context Shift Requirements:**
- Character needs NEW INFORMATION to shift interpretive framework
- Evidence that contradicts current understanding
- Witness/suspect reveals different context
- Investigation uncovers different situation type

**Common Violation Patterns:**

**Pattern 1: Proper Name Without Source**
```
❌ Character uses proper name they never heard
   Example: Martinez says "Sebastian LeClere" when no one told him this name
   
❌ Character knows event details they weren't present for
   Example: Character references off-screen conversation they didn't witness
```

**Pattern 2: Context Without Basis (MOST COMMON - NEW)**
```
❌ Detective asks "Who hired you?" when suspect presented it as personal
   Why wrong: Assumes professional context without basis
   What detective knows: Romantic encounter story
   What detective should ask: "Why are you here?" or "What's your connection?"
   
❌ Character jumps to correct conclusion without information to support it
   Example: Assumes there's a client/job when only presented with date/relationship
   
❌ Character asks specific question that reveals knowledge of situation type
   Example: "Who hired you for this job?" requires knowing it's a job
```

**Validation Process (EXPANDED):**

**For EACH character statement/question in target scene:**

**Step 1: Fact Check**
1. Search ALL prior scenes for when they learned specific facts
2. If fact not found in prior scenes: **FLAG AS VIOLATION**
3. If found: note scene number and source type

**Step 2: Context Check (NEW - CRITICAL)**
1. What CONTEXT does character think they're operating in?
2. What was character TOLD about situation type?
3. Does this dialogue/action fit that context?
4. Has character received NEW INFO to shift context?
5. If not: **FLAG AS CONTEXT VIOLATION**

**Example Context Validation:**
```
Martinez Scene 1: Told it's a date (farmer's market meetup, dinner)
Martinez Scene 7: Still operating in "date" context
Martinez asks: "Who hired you for this job?" ❌ CONTEXT VIOLATION

Why violation:
- Martinez was told: romantic encounter
- Martinez context: date gone wrong
- Question assumes: professional job context
- No new information triggered context shift
- Martinez has NO BASIS for "job" assumption

Fix: Martinez asks from his actual context
- "What are you doing here?" ✅
- "Why are you investigating her workplace?" ✅
- "How did you know she worked here?" ✅
```

**Relationship Status:**
- Relationship dynamics contradicting prior scenes
- Nicknames used before they're established
- Ignoring established tensions or conflicts

### 3. Physical Continuity Errors

**Object Persistence:**
- Objects disappearing (coffee cup vanishes mid-scene)
- Objects appearing without introduction
- Physical state changes without explanation

**Location Consistency:**
- Layout details contradicting prior descriptions
- Weather/time-of-day mismatches
- Geographic impossibilities

**Character State:**
- Clothing changes without explanation
- Injuries/fatigue disappearing
- Mood shifts without cause

### 4. Canon Contradictions

**Element File Violations:**
- Plot details contradicting `elements/plot.md`
- Character arcs contradicting `elements/outline.md`
- Setting details contradicting `elements/setting.md`
- Character traits contradicting `elements/characters/<name>.md`

**Outline Violations:**
- Scene deviating from planned beats in episode outline
- Events out of sequence from outline
- Missing required story beats

## Validation Workflow

### Step 1: Load ALL Prior Content

**For Episode 1, Scene 2+:**
```
1. Read Scene 1, Scene 2, ... Scene N-1
2. Extract all proper nouns (names, places, brands)
3. Extract all physical descriptions
4. Note character knowledge at each point
```

**For Episode 2+:**
```
1. Read ALL scenes from ALL previous episodes
2. Read all scenes in THIS episode before target scene
3. Build comprehensive proper noun database
4. Build character knowledge timeline
5. Build physical description index
```

### Step 2: Load ALL Canon Files

```
1. Load elements/characters/<all-characters-in-scene>.md
2. Load elements/plot.md, conflict.md, setting.md
3. Load elements/outlines/episode-##.md
4. Load elements/notes.md (seeded clues, continuity notes)
```

### Step 3: Scan Target Scene

**For each sentence in scene:**
- Check proper nouns against prior content database
- Flag NEW proper nouns not in database
- Check character actions against knowledge timeline
- Check physical details against description index
- Check dialogue against character voice patterns

### Step 4: Generate Violation Report

Output format:
```markdown
## Continuity Validation Report: [Scene Name]

**Status:** [PASS / FAIL / WARNINGS]

### Invented Details (Critical)
- Line XX: "drove away in her BMW" — Car model not established in character file or prior scenes
- Line YY: "Ralphs grocery store" — Brand name not used in prior scenes (was generic "grocery store")

### Character Knowledge Violations
- Line XX: Character knows about event that happened off-screen without being told

### Physical Continuity Issues
- Line XX: Coffee cup from scene opening disappeared without mention

### Canon Contradictions
- Line XX: Character trait contradicts elements/characters/doogan-andrews.md

### Generic/Vague (Safe)
- Line XX: "drove away" — Generic, no invented detail (✅ SAFE)
- Line YY: "sat down" — No specific furniture detail (✅ SAFE)

### Recommendations
1. Remove or genericize lines [XX, YY]
2. Verify character file for missing information
3. Check prior scene [name] for established details
```

## Proper Noun Database Structure

Build as you scan prior content:

```json
{
  "store_names": ["Coffee Bean & Tea Leaf (Ep1Sc5)", "grocery store (generic, Ep1Sc8)"],
  "street_names": [],
  "car_models": ["Doogan's car (unspecified, Ep1Sc2)"],
  "pet_names": [],
  "locations": ["Eddie's office", "Eddie's kitchen"],
  "businesses": ["Palmer & Andrews (Ep1Sc1)"]
}
```

## Character Knowledge Timeline

Track what each character knows at each scene:

```json
{
  "doogan": {
    "episode_1_scene_5": ["met Paul at coffeehouse", "knows about Annabelle Anders case"],
    "episode_1_scene_9": ["knows Abby thinks he's too isolated"]
  }
}
```

## Validation Script

Run automated check:

```bash
python .github/skills/continuity-checking/scripts/validate_continuity.py content/episodes/episode-02-*/01-holding-cell-graffiti.md
```

**Script checks:**
- [ ] Scans all prior episodes/scenes
- [ ] Builds proper noun database
- [ ] Flags new proper nouns not in prior content
- [ ] Checks character files for invented traits
- [ ] Validates character knowledge timeline
- [ ] Reports line numbers for all violations

## Output: Pass/Fail Criteria

**PASS:**
- Zero invented proper nouns
- Zero character knowledge violations
- Zero physical continuity errors
- Zero canon contradictions

**WARNINGS:**
- New generic descriptions (acceptable if vague)
- New character mannerisms (check if consistent with voice)
- Implied details (review for safety)

**FAIL:**
- Invented brand names, car models, specific details
- Character knows info they shouldn't
- Contradicts character files or prior scenes
- Physical impossibilities

## Common Safe Patterns

**Generic is safe:**
- "drove away" ✅ (not "drove away in her BMW")
- "sat down" ✅ (not "slumped into leather armchair")
- "grocery store" ✅ (not "Ralphs" or "Whole Foods")
- "coffee shop" ✅ (if not referring to established one)

**Specific is risky:**
- Car makes/models (unless in character file)
- Store brand names (unless already used)
- Clothing brands (unless established)
- Physical measurements (height, weight)

## Integration with Implement Prompt

**This skill runs AFTER scene-writing skill:**

1. Orchestrator invokes scene-writing skill → scene draft created
2. Orchestrator invokes continuity-checking skill → validation report
3. If violations found → orchestrator fixes and re-validates
4. If clean → mark task complete in tasks.md

## Example Violation Catches

### Example 1: Invented Car Model
**Scene text:**
> She climbed into her BMW and drove off.

**Violation:**
```
Line 45: "her BMW" — Car model not established in elements/characters/abby-palmer.md or prior scenes.
Recommendation: Change to "her car" or "drove off"
```

### Example 2: Invented Store Name
**Scene text:**
> They met at the Starbucks on Wilshire.

**Violation:**
```
Line 12: "Starbucks on Wilshire" — Brand and street name not established in prior content.
Prior reference (Ep1Sc5): "coffeehouse" (generic), "Coffee Bean & Tea Leaf"
Recommendation: Use "Coffee Bean & Tea Leaf" if same location, or generic "coffee shop" if different
```

### Example 3: Character Knowledge Violation - Context (MOST CRITICAL)
**Scene text (Episode 2, Scene 7):**
> Martinez pulled out a notepad. "Who hired you for this job?"

**Violation:**
```
Line 49: Martinez asks "Who hired you for this job?" — CONTEXT VIOLATION (most severe type)

TYPE: Contextual Knowledge Violation
SEVERITY: Critical - reveals character operating in wrong interpretive framework

Timeline trace (What Martinez knows):
  Scene 1: Doogan says he met Annabelle at farmer's market (romantic)
  Scene 1: Doogan says they had dinner date at her place (romantic)
  Scene 1: Doogan found her dead next morning (date gone wrong)
  Scene 1: NO MENTION of business, job, client, professional work
  Scene 2: Lawyer arrived, Doogan released (no new info)
  Scene 3-6: Martinez not present
  Scene 7: Martinez encounters Eddie at clinic

What Martinez's CONTEXT is (what he thinks situation is about):
  - Romantic encounter / dating situation
  - Possible drugging (Doogan blacked out)
  - Murder investigation of date gone wrong
  - Now victim's friend is snooping at victim's workplace

What Martinez DOESN'T KNOW:
  - That there's a "job" or professional context
  - That someone "hired" Doogan
  - That Doogan is a "rebound specialist"
  - That this was professional work, not personal

Why this is a CONTEXT violation:
  - Martinez's question assumes professional/job context
  - Martinez was told romantic/personal context
  - NO NEW INFORMATION shifted his understanding
  - Question reveals knowledge Martinez cannot have

Recommendation: Martinez asks from his ACTUAL context:
✅ "What are you doing here?"
✅ "Why are you at her workplace?"
✅ "How did you know she worked here?"
✅ "You and your friend involved in this somehow?"

SOURCE REQUIRED: For Martinez to ask about "job/client":
  1. Doogan would need to mention his business in Scene 1, OR
  2. Martinez would need to investigate Doogan's business off-screen AND reader sees this, OR
  3. Someone would need to tell Martinez about the job, OR
  4. Evidence would need to contradict romantic story
```

**Critical Rule:** Every character operates within an interpretive framework based on what they were TOLD. Characters cannot jump to correct conclusions without information basis.

### Example 3: Knowledge Violation
**Scene text:**
> "I heard about your interrogation with Martinez," Eddie said.

**Violation:**
```
Line 8: Eddie knows about interrogation — No scene shows Eddie learning this information.
Prior scenes: Doogan was interrogated alone; no phone call/meeting with Eddie shown.
Recommendation: Add line showing Doogan told Eddie, or genericize: "How did it go with the cops?"
```

### Example 4: Safe Generic (No Violation)
**Scene text:**
> He sat down and took a sip of coffee.

**Status:**
```
✅ SAFE — No specific furniture detail ("sat down" generic), no coffee brand invented.
```

## Next Step

After running continuity check, use **editor** prompt for minimal fixes, or return to **scene-writing** skill if major rewrite needed.
