---
name: character-management
description: Maintain character consistency by cross-referencing canonical character files. Use when writing scenes with established characters, updating character information, or checking for contradictions. Prevents invented physical details, cars, homes, or backstory. Triggers include "character consistency", "check character", "update character file", "character canon", "character validation".
---

# Character Management

Ensure character consistency across scenes and episodes by maintaining canonical character files and validating usage.

## When to Use This Skill

Use this skill when you need to:
- Write a scene with established characters
- Update a character file with new canonical information
- Check if character usage contradicts established facts
- Verify character voices remain consistent

## Critical Rule: NO INVENTED DETAILS

**NEVER invent:**
- Physical traits (hair color, height, clothing style)
- Cars or vehicles ("drove away in her BMW" ❌)
- Homes or living spaces
- Habits or mannerisms not established
- Backstory elements
- Relationships not previously mentioned
- **Brand names or product specifics** ("Chanel handbag" ❌ when outline says "designer handbag")
- **Educational background** ("failed high school" ❌ or "honors student" ❌)
- **Knowledge or expertise** (don't assume what character knows based on social class)
- **Dialogue patterns** that contradict character background

## Critical Rule: CHARACTER KNOWLEDGE TIMELINE (FUNDAMENTAL)

**Characters can ONLY know what they've experienced or been told UP TO THIS MOMENT.**

This is not optional. This is fundamental to all fiction writing.

**What This Means:**
- Characters cannot reference events that haven't happened yet
- Characters cannot know details they haven't learned through experience or dialogue
- Characters cannot anticipate plot points or future scenes
- Characters cannot "save" information for later use unless they know why

**Common Violations:**
- ❌ Character mentions detail from future scene ("save that Britney impression for later")
- ❌ Character knows name/fact they weren't told (references person they haven't met)
- ❌ Character prepares for situation they have no reason to expect
- ❌ Character displays knowledge/skill not established in their background

**Validation Questions (Ask for EVERY detail a character mentions):**
1. **When did this character learn this information?**
   - Which scene? Which dialogue?
   - Or: Is it in their character file as established background?
2. **Why would this character know this right now?**
   - Direct experience?
   - Someone told them (when/where)?
   - Established expertise from character file?
3. **What is the SOURCE of this knowledge?**
   - If you cannot cite a source → character CANNOT know it

**Example Violations:**
```
❌ WRONG (Scene 7): Doogan tells Winston to "save that Britney impression for later"
   Why wrong: Doogan hasn't seen the impression yet. It happens in Scene 10.
   Source check: Where did Doogan learn about this impression? NO SOURCE.
   
❌ WRONG (Scene 3): Character mentions "the clinic investigation"
   Why wrong: Investigation hasn't started yet in story timeline.
   Source check: When did character learn about investigation? NO SOURCE.
   
❌ WRONG (Scene 5): Character says "I'll need this later for the tournament"
   Why wrong: Character knows future plot point they shouldn't anticipate.
   Source check: Why would character prepare for specific future event? NO REASON.

✅ RIGHT (Scene 7): Winston says "My wife loves her show"
   Why right: Winston can watch TV. His wife could be a fan. Plausible background knowledge.
   
✅ RIGHT (Scene 8): Character says "You mentioned the tournament earlier"
   Why right: References prior dialogue from Scene 6. SOURCE: Scene 6 conversation.
```

**Discipline Required:**
- Write characters IN THE MOMENT they're experiencing
- Characters live in "now" - they don't know what's coming next
- Reader knows more than characters (dramatic irony) - that's correct
- Characters knowing future events breaks the fourth wall

**If character needs information:**
- Show them learning it (dialogue, experience)
- OR establish it in character background file
- OR remove the reference entirely

## Critical Rule: THE SECRECY RULE (STORY-BREAKING IF VIOLATED)

**Targets NEVER know they're part of a paid rebound operation.**

This is a foundational business rule documented in:
- `elements/checklist.md` → "The Secrecy Rule" section
- `elements/notes.md` → "The Secrecy Rule" section
- `elements/characters/doogan-andrews.md` → "Relationships" → Secrecy Rule

**What This Means for Dialogue:**
- NO character ever references "hiring," "paying," "job," "babysit," "service"
- Targets may doubt authenticity ("you're too good to be true") but never discover payment
- Cover stories explain Doogan's presence (family friend, coincidence, mutual connection)
- Targets' skepticism comes from emotional walls, not knowledge of transaction

**Example Violations (NEVER WRITE):**
- ❌ "My parents paid you"
- ❌ "Whatever they're paying you"
- ❌ "Is this your job?"
- ❌ "You're babysitting me"

**Acceptable Skepticism:**
- ✅ "You're too perfect"
- ✅ "This feels like a setup"
- ✅ "My parents set me up with someone exactly right—that's suspicious"

**If violated, the job ends immediately and becomes a story crisis (has NOT happened in Episodes 1-2).**

**ANTI-FABRICATION: Social Class Assumptions**

**DO NOT invent character traits based on wealth/class:**
- ❌ "Wealthy family → character must be educated/cultured"
- ❌ "Wealthy family → character must have failed school (rebellious)"
- ❌ "Working class → character must lack education"
- ✅ CHECK character file for ACTUAL education/knowledge/background

**Example Violations:**
```
❌ WRONG: Cheryl (wealthy background) says "I failed high school English"
   Why wrong: Character file shows wealthy family (private schools), no indication of failure
   
❌ WRONG: Doogan instantly recognizes "Sonnet 130"
   Why wrong: Outline says "Baxter identifies" - knowledge belongs to Baxter, not Doogan
   
❌ WRONG: "vintage Chanel handbag"
   Why wrong: Outline says "designer handbag" (generic) - specific brand is fabrication

✅ RIGHT: Cheryl says "I never paid attention in poetry"
   Why right: Admits lack of knowledge without inventing failure/character background
```

**IF information is missing:**
- Stay vague ("drove away" ✅ not "drove away in her BMW" ❌)
- Use generic descriptions ("sat down" ✅ not "slumped into leather chair" ❌)
- **Use outline's exact wording** ("designer handbag" ✅ not "Chanel handbag" ❌)
- **Attribute knowledge correctly** (Baxter knows → Baxter provides, not Doogan)
- Flag for author to decide and add to character file

## Character File Structure

All character canonical data lives in TWO locations:

### 1. Character Index: `elements/characters.md`
**Contains supporting/minor character details:**
- Characters who don't have individual files (Brad Levitt, Terry Tamborino, Jillian, etc.)
- Brief descriptions sufficient for scene usage
- Relationships to main characters
- Role in specific episodes

**CRITICAL:** Many characters are ONLY documented here. Always check this file FIRST before assuming a character needs an individual file.

**Portrait File Protocol:**
- Character entries include portrait references: `<!-- Portrait: characters/name.jpg -->`
- If portrait file exists, DO NOT request visual details (height, build, hair color, clothing style, facial features)
- Portrait provides complete visual reference
- Only request non-visual character details: mannerisms, speech patterns, internal motivations, behavioral quirks, voice patterns
- When writing scenes: describe actions and behavior, not physical appearance already shown in portrait

### 2. Individual Character Files: `elements/characters/<name>.md`
**For main recurring characters only (Doogan, Eddie, Abby, Martinez, etc.):**

### Required Sections
- **Name & Role**
- **Physical Description** (age, appearance, distinctive features)
- **Voice Patterns** (speech style, vocabulary, cadence)
- **Mannerisms** (habits, body language, tics)
- **Relationships** (to other characters)
- **Background** (only what's established in canon)
- **Motivation** (current arc goals)

## Character Consistency Workflow

### Before Writing Any Scene

1. **Load All Present Characters (BOTH SOURCES)**
   - **FIRST:** Read `elements/characters.md` for ALL characters in scene (many characters ONLY exist here)
   - **Check for portrait files:** If `<!-- Portrait: characters/name.jpg -->` exists, skip requesting visual details
   - **SECOND:** Read individual files from `elements/characters/<name>.md` for main recurring characters
   - Note current emotional state from previous scenes
   - Check relationships to other present characters
   - **Timeline Check:** Verify character knowledge at THIS point in story timeline

2. **Voice Verification**
   - Review speech patterns for each character
   - Check vocabulary level and cadence
   - Verify dialogue tags match voice

3. **Visual Consistency**
   - Check physical descriptions match established canon
   - Verify mannerisms appear consistently
   - Check clothing/appearance only if previously established

4. **Relationship Dynamics**
   - Verify how characters interact matches established relationships
   - Check emotional temperature between characters
   - Note any relationship changes that occurred in previous scenes

5. **Timeline-Aware Knowledge Verification (CRITICAL)**
   - What does each character KNOW at this point in the timeline?
   - When did they learn this information? (which scene, which day?)
   - **Information source required:** If character knows something, WHERE did they learn it?
   - Track time references from prior scenes:
     - Explicit time markers ("3 AM," "9 AM," "tomorrow morning")
     - Day progression ("next day," "that evening," "same day")
     - Elapsed time references ("six hours later," "less than 24 hours")
   - Cross-check character internal thoughts about elapsed time against actual timeline
   - Flag timeline contradictions BEFORE writing
   - Note any relationship changes that occurred in previous scenes

## Character Knowledge Tracking (CRITICAL)

**THE FUNDAMENTAL RULE:**
> **Just because the AI can see all story details does NOT mean characters can.**

**BEFORE writing any character action or dialogue, ask:**
1. **"Does this character KNOW this information?"**
2. **"WHERE and WHEN did they learn it?"**
3. **"What was the exact source?"** (overheard, told directly, deduced, witnessed, investigated)
4. **"What CONTEXT does this character have?"** (What do they think this situation is about?)

### Knowledge vs Context (NEW - CRITICAL)

**Knowledge:** Specific facts a character has learned
**Context:** The framework a character uses to interpret those facts

**Example: Martinez in Episode 2**
- **Knowledge:** Doogan met Annabelle at farmer's market, they had dinner, she died
- **Context:** Martinez thinks this is a DATE/ROMANTIC ENCOUNTER, not a job
- **What Martinez DOESN'T know:** Doogan's business, that someone hired him, that this was work

**Therefore:**
- ❌ WRONG: Martinez asks "Who hired you?" (assumes knowledge of job context)
- ✅ RIGHT: Martinez asks "What were you doing here?" (investigates suspicious behavior)

### Character Knowledge Violations

**Type 1: Using proper names/facts they haven't learned:**
- Character using proper names they haven't heard yet
- Character knowing events that happened off-screen
- Character remembering details from scenes they weren't present for

**Type 2: Having context they don't have (MOST COMMON ERROR):**
- Character assumes situation is about X when they only know about Y
- Detective assumes there's a "job" when suspect presented it as personal
- Character asks specific questions that reveal contextual knowledge they lack

**Example Violations (from Episode 2, Scene 7):**

**Violation 1: Proper Name**
```
❌ WRONG: Martinez asks "When did Sebastian LeClere hire you?"
   Why wrong: Martinez never heard this name
   Fix: Martinez asks "Who hired you?" AFTER learning there's a job context
   
✅ BETTER: Martinez asks "Why are you here?"
   Why right: Open question, no assumed knowledge
```

**Violation 2: Context (MORE FUNDAMENTAL)**
```
❌ WRONG: Martinez asks "Who hired you for this job?"
   Why wrong: Martinez doesn't know there IS a job
   What Martinez knows: Doogan met Annabelle romantically (farmer's market, dinner, date)
   What Martinez THINKS: This is a romantic encounter / possible drugging / murder
   Martinez has NO BASIS to think this is professional work
   
✅ RIGHT: Martinez asks "What are you doing at her workplace?"
   Why right: Based on what Martinez actually knows (Eddie snooping, Annabelle worked here)
```

### Tracking Character Knowledge & Context

**For each character, track TWO things:**

**1. Knowledge Timeline (Facts):**
- Scene 1: Character learned X from source Y
- Scene 2: Character learned Z from source A
- Scene 5: Character still doesn't know about B

**2. Context Framework (Interpretation):**
- What does character THINK this situation is about?
- What assumptions are they making?
- What questions would they naturally ask given their context?

**Example: Martinez Context Timeline**
```
Scene 1 (Interrogation):
  Knowledge: Doogan met Annabelle at farmer's market, dinner date, she died
  Context: Martinez thinks this is ROMANTIC/DATING situation gone wrong
  Assumptions: Doogan picked up woman, maybe drugged her, she died
  
Scene 7 (Clinic encounter):
  Knowledge: Eddie (Doogan's friend) is at Annabelle's workplace
  Context: Still thinks this was romantic - now friend is snooping
  Assumptions: Either helping investigate OR involved in crime
  Martinez still has NO REASON to think there's a job/client
```

### Special Case: Detective Characters (EXPANDED)

**Detectives learn through:**
- Interrogation (what suspects/witnesses SAY)
- Investigation (what they DISCOVER through police work)
- Evidence (what physical/digital evidence SHOWS)

**CRITICAL: Context matters more than facts**
- If suspect presents situation as personal, detective interprets it that way
- Detective needs REASON to shift context (evidence, contradiction, new information)
- **NEVER have detective magically know situation is different from what they were told**

**Example:**
```
Doogan tells Martinez: "I met her at farmer's market, we had dinner"
Martinez's context: This is a romantic encounter
Martinez's questions: About the date, the relationship, his movements

For Martinez to know it's a JOB:
1. Doogan would need to mention his business
2. Evidence would need to contradict romantic story
3. Witness would need to reveal professional context
4. Martinez would need to investigate Doogan's business and connect it

UNTIL THEN: Martinez operates in "romantic encounter" context
```

### Validation Checklist (USE FOR EVERY SCENE)

**Before writing character dialogue/action:**
- [ ] What FACTS does this character know? (List them)
- [ ] What CONTEXT does this character have? (What do they think this is about?)
- [ ] What SOURCE gave them this knowledge? (Scene number + method)
- [ ] Does this dialogue/action fit their knowledge AND context?
- [ ] Am I making character assume knowledge they don't have?
- [ ] Am I making character jump to conclusions without basis?

**Red flags:**
- Character asks specific question that assumes knowledge they lack
- Character uses proper name they never heard
- Character shifts context without new information triggering it
- Character "conveniently" knows what reader knows

## Updating Character Files

**When adding to character files:**

1. **Source Verification**
   - Information must come from published scenes
   - Author explicitly established it
   - Not inferred or invented

2. **Update Process**
   - Add to appropriate section in character file
   - Include scene reference where established
   - Format consistently with existing entries

3. **Change Log**
   - Note date of update
   - Reference scene/episode where detail was added

## Character Introduction Pattern

**First appearance of character:**
- Use name + role: "Eddie Palmer, his business partner"
- Give 1-2 distinctive physical details (if relevant to POV)
- Establish voice immediately through dialogue
- Show relationship to POV character

**Subsequent appearances:**
- Use first name only (unless context requires full)
- Reference distinctive trait only if relevant to moment
- Voice carries identity more than description

## Validation

Use `scripts/validate_consistency.py` to check character usage:

```bash
python .github/skills/character-management/scripts/validate_consistency.py content/episodes/episode-01-*/01-scene.md
```

Checks:
- [ ] All characters in scene have files in `elements/characters/`
- [ ] No physical details contradict character files
- [ ] Voice patterns match established speech
- [ ] Relationships match established canon
- [ ] No invented details (cars, homes, habits)

## Example Character File

```markdown
# Doogan Andrews

**Role:** Protagonist, Rebound Specialist

**Physical Description:**
- Age: Late 30s
- [Details per author's establishment only]

**Voice Patterns:**
- Measured drawl
- Short, economical responses
- Dry humor
- Rarely volunteers information

**Mannerisms:**
- Observes before speaking
- Physical stillness (doesn't fidget)
- Eye contact without intimidation

**Relationships:**
- Eddie Palmer: Business partner, best friend since college
- Abby Palmer: Eddie's wife, friend, occasional moral compass
- Paul Martinez: Detective, professional respect, occasional friction

**Motivation (Episodes 1-2):**
- Clear his name in Annabelle Anders murder investigation
- Complete client jobs to pay mounting legal fees
- Protect Eddie/Abby from investigation fallout

**Established in Episodes:**
- Episode 1: Voice, business model, arrest circumstances
- Episode 2: Interrogation style, work ethic, relationship with police
```

## Next Step

After updating character files, use **continuity-checking** skill to verify no contradictions exist across episodes.
