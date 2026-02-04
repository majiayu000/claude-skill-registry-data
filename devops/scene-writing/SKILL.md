---
name: scene-writing
description: Write fiction scenes following Stephen King principles and the McDonald opening rule. Use when drafting new scenes, editing existing prose, or writing chapters. Triggers include "write scene", "draft scene", "edit scene", "new chapter", "prose writing", "scene draft". Ensures POV discipline, character voice consistency, and craft quality.
---

# Scene Writing

Write fiction scenes following Fiction Kit voice, style, and craft principles (Stephen King methods + McDonald opening rule).

## When to Use This Skill

Use this skill when you need to:
- Draft a new scene from scratch
- Edit existing scene prose
- Rewrite a scene for pacing or voice
- Add a missing scene to an episode

## Pre-Writing Checklist (MANDATORY)

**BEFORE writing ANY prose, complete ALL these steps in order:**

### 1. Load ALL Elements Documents

**Character Files (CRITICAL - LOAD BOTH):**
- Read `elements/characters.md` for **character index** (supporting character details like Brad Levitt, Terry Tamborino, etc.)
- Read EVERY file in `elements/characters/` for **main characters** in this scene (Doogan, Eddie, Abby, etc.)
- **IMPORTANT:** Many supporting characters are ONLY documented in `elements/characters.md`, not in individual files
- Note: physical traits, voice patterns, mannerisms, relationships, anti-patterns
- Use ONLY canonical information—never invent details

**Story Structure Files:**
- `elements/plot.md` - Overall story arc and structure
- `elements/conflict.md` - Core conflicts and stakes
- `elements/theme.md` - Thematic elements
- `elements/setting.md` - Location details (do not invent setting details)
- `elements/outline.md` - Series outline
- `elements/outlines/episode-##.md` - THIS episode's outline
- `elements/notes.md` - Continuity notes and seeded clues

**Event Files (if applicable):**
- Check `elements/events/` for any past events referenced in scene
- Use ONLY canonical event details from these files

### 2. Load ALL Voice & Style Documents

- `voice/style.md` - McDonald-style prose rules, third-person close POV, **cinematic techniques**
- `voice/format.md` - Format structure (episodes, scenes, serial fiction rules)
- `elements/pov.md` - POV rules (third-person close, one per scene)
- `elements/tone.md` - Tone requirements (fast, witty, darkly funny)
- `elements/checklist.md` - Non-negotiable quality standards

**CRITICAL: voice/style.md now includes:**
- Em-dash cold opens (mid-sentence scene openings)
- Action beats as exposition (show don't tell character details)
- Background activity as cinematic atmosphere (Sorkin/West Wing techniques)
- Trust the reader (no hand-holding)
- Accidental meetings (characters encounter naturally, not by arrangement)

### 3. Load ALL Prior Content for Continuity

**CRITICAL: This step prevents continuity errors.**

**For Episode 1, Scene 1:**
- No prior content to check
- Proceed with elements and voice files only

**For Episode 1, Scene 2+:**
- Read ALL previous scenes in THIS episode (Scene 1, Scene 2, ... Scene N-1)
- Note established details: names, places, objects, physical descriptions
- Note character knowledge state: what they know/don't know at this point
- Note secrets that must stay secret

**For Episode 2+, Scene 1:**
- Read ALL scenes from ALL previous episodes
- Note all established facts that cannot be contradicted
- Note character arcs and relationship changes
- Note running gags, callbacks, recurring elements

**For Episode 2+, Scene 2+:**
- Read ALL previous episodes (all scenes)
- Read ALL previous scenes in THIS episode
- Create comprehensive continuity notes

### 4. Create Continuity Notes

**Document these before writing:**
- **Established Facts:** What details have been set in stone? (store names, car models, pet names, addresses, jobs, etc.)
- **Character Knowledge (CRITICAL):** What does POV character know at THIS point in timeline?
  - Build knowledge timeline from Scene 1 forward
  - Document WHEN each piece of information was learned (which scene, which dialogue)
  - Document WHAT character has experienced up to this moment
  - Document WHO character has met and WHAT they know about them
  - **Characters can ONLY reference information they've learned by this scene**
  - **Characters CANNOT know future events, plot points, or details from later scenes**
- **Secrets:** What must stay hidden from certain characters?
- **Physical Descriptions:** What have we established about appearance, clothing, vehicles, homes?
- **Relationship Status:** Where do character relationships stand right now?
- **Emotional State:** What just happened to POV character? What's their mood?
- **Timeline Markers (CRITICAL):** When does this scene take place relative to prior scenes?
  - Track time-of-day mentions (morning, afternoon, evening, night, 3 AM, 9 AM, etc.)
  - Track day progression ("tomorrow," "next day," "same day," "that evening")
  - Track elapsed time references ("six hours later," "the next morning," "two days ago")
  - Calculate actual timeline from Scene 1 forward to THIS scene
  - Document timeline in continuity notes to prevent contradictions

### 4a. Build Character Knowledge Timeline (NEW - MANDATORY)

**For EVERY character in this scene, document:**

**What They Know:**
- Facts learned in prior scenes (list scene numbers)
- People they've met (when/where)
- Events they've experienced or been told about
- Skills/knowledge from character background file

**What They DON'T Know:**
- Events that happen in FUTURE scenes
- Details from other characters' POV scenes they weren't present for
- Information no one has told them yet
- Plot points the READER knows but character hasn't learned

**Source Every Reference:**
Before writing ANY character dialogue/thought that references information:
1. Ask: "When did this character learn this?"
2. Cite: "Scene X, Character Y told them" OR "Character file background"
3. If NO SOURCE exists → character CANNOT reference it

**Example Knowledge Timeline:**
```
Scene 7 - Winston's Knowledge:
✅ Knows: Brenda is a comedian (Doogan told him)
✅ Knows: They're at golf course for tournament (observable)
✅ Knows: Mara is a golfer (introduced to her)
❌ Does NOT know: Brenda does Britney impression (hasn't seen it, no one mentioned it)
❌ Does NOT know: Fourth hole incident will happen (future event)
❌ Does NOT know: Doogan's rebound business (no one told him)

Scene 7 - Doogan's Knowledge:
✅ Knows: Winston is experienced golfer (Eddie's contact info)
✅ Knows: Brenda is comedian (character background)
✅ Knows: Mara needs help with sponsors (Jake told him Scene 1)
❌ Does NOT know: Brenda does Britney impression (hasn't seen her perform)
❌ Does NOT know: Fourth hole incident will happen (future event)
❌ Does NOT know: Candy will be on fourth hole (hasn't happened)
```

### 5. Extract Referenced Facts (MANDATORY - NEW)

**CRITICAL: Prevent factual contradictions when referencing prior events.**

See: `.github/skills/scene-writing/references/fact-verification.md` for full protocol.

**Before writing Scene N:**

1. **Identify what will be referenced:**
   - Review outline beats for this scene
   - List any prior conversations characters will mention
   - Note any amounts, times, or details from earlier scenes
   - Identify any "you said" or "we discussed" moments

2. **Create Fact Reference Table:**

```markdown
**FACT REFERENCE TABLE**

Reference #1: [Description]
- Will appear as: [planned dialogue or narrative]
- Source: Scene X, lines Y-Z
- Established detail: [exact quote or specific fact]
- Constraint: [what this scene MUST NOT contradict]
```

**Example:**
```markdown
Reference #1: Jake comments on auction bid
- Will appear as: Jake's reaction to $3,000 bid
- Source: Scene 1, lines 85-86
- Established detail: Jake said "Whatever it takes. Three or four thousand should do it."
- Constraint: Jake CANNOT say it was more than expected. $3,000 is low end of range.
```

3. **Keep table visible during writing**
4. **Before writing any reference phrase, verify against table**

**See checklist:** `.github/skills/scene-writing/checklists/fact-verification-checklist.md`

### 6. Verify Scene Context & Timeline

**Before writing, answer:**
- What happened immediately before this scene?
- **WHEN does this scene take place?** (time of day, which day in the story)
- **How much time has elapsed since the previous scene?**
- **How much time has elapsed since key events in earlier scenes?** (arrests, meetings scheduled, deadlines mentioned)
- Who is present in this scene?

### 5a. SCENE SETUP VERIFICATION (MANDATORY - BLOCKING REQUIREMENT)

**DO NOT WRITE PROSE until you complete this verification.**

**Purpose:** Prevent writing scenes with wrong character locations, wrong communication methods (phone call vs in-person), or missing critical logistics.

**Required Output (before ANY prose writing):**

```
=== SCENE SETUP VERIFICATION ===
Scene: Episode X, Scene Y — [Scene Title]
Source: elements/outlines/episode-XX.md, Section ##

**QUOTE FROM OUTLINE (exact text):**
"[Paste the relevant section from the episode outline that describes WHO/WHERE/WHAT]"

**WHO is physically present in this scene:**
- [Character Name] — [their location/position: "at dining table with laptop", "standing in kitchen", etc.]
- [Character Name] — [their location/position]
- [List ALL characters who are in the room/location]
- [Note if anyone is on phone/video call but NOT physically present]

**WHERE are they (specific location):**
- [Physical location from outline: "Eddie's house", "Doogan's condo", "country club", etc.]
- [Room/area if specified: "living room", "dining table", "kitchen", etc.]

**WHAT is the situation (1-2 sentence setup):**
- [Brief description of what's happening at scene start]

**KEY LOGISTICS (critical details from outline):**
- [Any specific setup like "Baxter at laptop working", "phone call with X", "just arrived from Y", etc.]
- [Communication method: in-person conversation, phone call, video call, earpiece communication]
- [Props/objects mentioned: laptop, coffee, documents, etc.]
- [Character states: exhausted, dressed for wedding, just woke up, etc.]

**VERIFICATION CHECKLIST:**
- [ ] All characters from outline are listed
- [ ] No characters added who aren't in outline
- [ ] Physical location matches outline
- [ ] Communication method clear (in-person vs phone vs video vs earpiece)
- [ ] Critical logistics noted (who has what object, who's sitting/standing where)
- [ ] Character states/appearances noted if specified
- [ ] If outline says "Baxter is in the room", he is NOT on a phone call
- [ ] If outline says "phone call", characters are NOT in same room

**VALIDATION:** [PASS/FAIL]

[If FAIL, STOP - do not write until setup is clear]
===
```

**This step is BLOCKING. Do not proceed to writing if:**
- Outline is ambiguous about who's in the room
- Communication method unclear
- Critical logistics missing

**If verification fails, ASK USER for clarification before writing.**
- What is the POV character's emotional state?
- What information does POV character know at this point?
- What details were established in prior scenes that must be preserved?
- Are there any anti-patterns to avoid? (Check character files for Fashion Anti-Patterns, Motor-Mouth Rules, etc.)

**Timeline Verification Examples:**
```
Scene 2: "Eddie was woken at 3 AM" → Scene 2 walkout: "Hank sweating at 9 AM"
= 6 hours elapsed between call and walkout

Scene 3: "job starts tomorrow morning at nine"
Scene 5: Restaurant meeting same day as Scene 3
= Scene 5 happens BEFORE the job, on day BEFORE the job

Doogan's internal reference: "six hours out from holding cell"
✗ WRONG if holding cell was at 1-3 AM and current scene is evening (12-18 hours)
✓ CORRECT: "less than twenty-four hours out from interrogation"
```

### 6. Verify Beat Mechanisms (NEW - CRITICAL)

**For EACH outline beat in episode-##.md, verify the MECHANISM:**

**The "HOW?" and "WHY?" Questions:**
- Beat says "Character X arrives" → HOW do they know to come? WHY are they there?
- Beat says "Character knows Y" → HOW did they learn it? WHEN? FROM WHOM?
- Beat says "Object appears" → WHERE did it come from? WHO brought it?
- Beat says "Character does Z" → WHY do they do it? What's their motivation?

**Check These Sources:**
1. **notes.md** - Look for established procedures, mechanisms, information flow
2. **Prior scenes** - Was the mechanism established earlier?
3. **Character files** - Does character background explain this knowledge/action?
4. **Common sense** - Is there an obvious implied mechanism (e.g., "lawyer knows case details" = standard briefing)?

**If Mechanism is Unclear:**
- ❌ DO NOT INVENT a mechanism
- ✅ FLAG IT in your context log as "UNVERIFIED BEAT"
- ✅ Ask user for clarification before proceeding
- ✅ Check if mechanism should be shown on-screen vs. implied

**Example Verification:**
```
Outline Beat: "Eddie is there, Hank is there"
❓ HOW does Eddie know to come?
✅ VERIFIED: notes.md says "one phone call" → Doogan called Eddie
✅ MECHANISM: Police procedure allows one call, Doogan used it

Outline Beat: "Hank mentions money too many times"
❓ WHY does Hank bring up money?
✅ VERIFIED: Character type = "parking meter with law degree"
✅ MECHANISM: Hank's personality (transactional, business-focused)

Outline Beat: "Eddie knows about Annabelle investigation"
❓ HOW does Eddie know investigation details?
✅ VERIFIED: Episode 1, Scene 8 - Doogan called Eddie from store
✅ MECHANISM: Phone call established information flow
```

**Document Verified Mechanisms:**
Add to your continuity notes:
- "Eddie knows Doogan was arrested → Doogan called him (one phone call, police procedure)"
- "Hank knows case basics → Eddie briefed him when calling at 3 AM (implied off-screen)"

### 7. Load ENTIRE Episode Outline & Create Scene Map (MANDATORY - CRITICAL)

**BEFORE writing ANY scene, you MUST:**

1. **Read the COMPLETE episode outline** from `elements/outlines/episode-##.md`
2. **Create a SCENE MAP** of the entire episode
3. **Identify THIS scene's "Button" (ending point)** - this is WHERE YOU MUST STOP
4. **Identify the NEXT scene's opening** - this is what you CANNOT write

**Why This Is Non-Negotiable:**
- **Prevents scene spillover** - Most common violation
- Ensures you know what comes BEFORE and AFTER this scene
- Enforces precise scene boundaries (stop at the Button)
- Episode structure dictates pacing - don't break it

**CRITICAL RULE: STOP AT THE BUTTON**

Every scene in the outline has a "Button:" marker. This is the EXACT point where you MUST stop writing. Do not continue past it. Do not write "what happens next." That's the next scene's job.

**Example Violation:**
```
Scene 10 Outline Button: "They have the golden ticket; Jillian is still stuck inside"

❌ WRONG: Write them running back, arriving at country club, seeing Jillian there first
✅ RIGHT: End outside speakeasy with ticket, Jillian still inside, start running back

Scene 12 is "Finish Line" - that's where arrival happens. Don't steal it.
```

**SCENE MAP FORMAT:**

```
EPISODE 2 SCENE MAP:
Scene 1: Holding Cell Graffiti (Doogan POV - interrogation)
  Button: "You've got a lawyer"
  
Scene 2: The Walkout (Doogan POV - lawyer arrives)
  Button: Eddie says "Abby's making pancakes"
  
Scene 3: Eddie's Kitchen (Doogan POV - team briefing)
  Button: Doogan goes home to sleep
  
Scene 4: Doogan's Condo (Doogan POV - shower, sleep, reset)
  Button: Doogan leaves for country club
  
Scene 5: Restaurant Meeting (Doogan POV - client meeting)
  Button: Doogan goes home
  
Scene 6: Country Club Kickoff (Doogan POV - hunt begins)
  Button: "They head for Rose Shop—Jillian tailing"
  
Scene 7: Strip Mall Clinic (Eddie POV - Martinez confrontation)
  Button: Eddie waits for Martinez to leave
  
Scene 8: The Flower Shop (Doogan POV - roses clue)
  Button: "They head for bookstore—Jillian following"
  
Scene 9: Eddie's House (Eddie/Abby/Baxter POV - plan infiltration)
  Button: "Baxter in IT uniform"
  
Scene 10: Bookstore to Speakeasy (Doogan POV - accelerated hunt)
  Button: [to be determined]
```

**CRITICAL VERIFICATION (for Scene 8 example):**

```
WRITING SCENE 8: The Flower Shop

PRIOR SCENE (Scene 7):
- Eddie at clinic
- Martinez confrontation
- Different timeline/POV

THIS SCENE'S BEATS (Scene 8 outline):
- Arrive at Rose Shop
- Jillian follows and eavesdrops
- Cheryl orders red roses (wrong)
- Baxter reads sonnet, identifies "red and white"
- Doogan orders red and white roses
- Clerk gives envelope
- Next clue is Pride and Prejudice
- Baxter finds bookstore
- Cheryl decides to "crush" not just win

THIS SCENE'S BUTTON:
"They head for the bookstore—Jillian and her boyfriend still tailing"

NEXT SCENE (Scene 9):
- Eddie's House
- Different timeline/POV
- Baxter/Abby planning

SCENE AFTER THAT (Scene 10):
- Bookstore to Speakeasy
- THIS is where bookstore happens

BOUNDARY ENFORCEMENT:
❌ DO NOT write: Arriving at bookstore
❌ DO NOT write: Inside bookstore
❌ DO NOT write: Finding Pride and Prejudice clue
❌ DO NOT write: Next clue reveal
✅ STOP AT: Heading toward bookstore
```

**MANDATORY PRE-WRITING CHECKLIST:**

Before writing Scene N:
- [ ] Read ENTIRE episode outline (all scenes)
- [ ] Created scene map with all Buttons identified
- [ ] Identified Scene N-1 (what came before)
- [ ] Identified Scene N's beats and Button
- [ ] Identified Scene N+1 (what comes after)
- [ ] Identified Scene N+2 (to catch multi-scene threads)
- [ ] Verified NO overlap with Scene N+1 or N+2
- [ ] Documented where to STOP writing

**If You Cannot Create Complete Scene Map:**
- ❌ DO NOT proceed with writing
- ✅ FLAG: "Incomplete episode outline - cannot verify boundaries"
- ✅ Ask user for complete episode structure

### 8. Compare Outline to Scene (ANTI-FABRICATION CHECK + BOUNDARY ENFORCEMENT)

**AFTER creating scene map, do line-by-line comparison:**

**Read the episode outline beat list for THIS scene:**
- List every action mentioned in the outline
- List every piece of dialogue mentioned
- List every object/prop mentioned
- List every character interaction specified
- **IDENTIFY WHERE THIS SCENE ENDS** (the "Button" in the outline)

**CRITICAL: SCENE BOUNDARY RULE**
> **Each scene must END at its designated outline "Button." NEVER spill into the next scene's beats.**

**Why This Matters:**
- Episode outlines define clear scene boundaries
- Each scene has a designated purpose, beats, and ending
- Spillover into next scene creates duplication and ruins pacing
- Next scene's opening is carefully crafted—don't steal it

**Scene Boundary Verification:**
1. **Read THIS scene's outline beats** (Scene N)
2. **Read NEXT scene's outline beats** (Scene N+1)
3. **Identify the dividing line**:
   - Where does Scene N's "Button" end?
   - Where does Scene N+1's opening begin?
4. **STOP writing at Scene N's button**—even if it feels like the story should continue

**Example (Episode 2):**
```
Scene 6 Outline:
- Terry introduces Doogan to Cheryl
- Rules announced (scavenger hunt, literature theme)
- First clue given: Shakespeare sonnet
- Baxter identifies "roses"
- Button: "They head for Rose Shop—Jillian tailing"

Scene 7 Outline:
- [Different timeline: Eddie at clinic]

Scene 8 Outline:
- Doogan and Cheryl at Rose Shop
- Roses clue solved
- Next clue received

❌ WRONG (Scene 6 spillover):
Scene 6 includes: heading to Rose Shop → arriving → entering → solving clue → leaving
RESULT: Scene 8 duplicates Rose Shop visit

✅ CORRECT (Scene 6 boundary respected):
Scene 6 includes: rules → clue → Baxter identifies location → Button: heading toward Rose Shop
Scene 8 includes: FULL Rose Shop visit (arrival → entry → solve → exit)
```

**Enforcement Checklist:**
- [ ] Identified where THIS scene's Button ends (per outline)
- [ ] Verified NEXT scene's opening (per outline)
- [ ] Stopped writing at Button—did not continue into next scene
- [ ] If tempted to continue, STOP and flag as "Scene Boundary Risk"

**Create "Outline Implementation Map":**
```
Outline Beat: "Terry introduces Doogan to Cheryl"
Implementation: Terry calls Doogan over, names him, Cheryl responds
Verification: ✅ Matches outline exactly

Outline Beat: "First prize is a designer handbag"
Implementation: Terry announces "vintage Birkin handbag"
Verification: ❌ FABRICATION - outline says "designer handbag" (generic), not specific brand
FIX NEEDED: Use generic "designer handbag" OR verify with user which brand
```

**CRITICAL ANTI-FABRICATION RULES:**

**DO NOT add actions not in outline:**
- ❌ Outline: "Baxter feeds location" → ❌ WRONG: Add phone call charade
- ✅ Outline: "Baxter feeds location" → ✅ RIGHT: Baxter speaks in earpiece, Doogan relays info

**DO NOT add dialogue beats not in outline:**
- ❌ Outline: Silent beat → ❌ WRONG: Add witty banter
- ✅ Outline: Silent beat → ✅ RIGHT: Action/movement only

**DO NOT upgrade generic terms to specific brands:**
- ❌ Outline: "designer handbag" → ❌ WRONG: "Chanel handbag"
- ✅ Outline: "designer handbag" → ✅ RIGHT: "designer handbag" (or ask user for specific brand)

**DO NOT attribute knowledge to characters they shouldn't have:**
- ❌ Outline: "Baxter identifies Sonnet 130" → ❌ WRONG: Doogan recognizes it first
- ✅ Outline: "Baxter identifies Sonnet 130" → ✅ RIGHT: Baxter provides info, Doogan relays

**DO NOT invent character traits from social class assumptions:**
- ❌ ❌ WRONG: "Wealthy character → must know literature" OR "Wealthy character → failed school"
- ✅ ✅ RIGHT: Check character file for actual education/knowledge

**IMPLEMENT EXACTLY WHAT'S WRITTEN:**
- Outline says character "taps ear" → They tap their ear (not make phone call)
- Outline says "Baxter feeds location" → Baxter speaks in earpiece (already established device)
- Outline says "designer handbag" → Use that exact phrase (or ask which brand)
- Outline says beat is character's knowledge → That character provides it (not POV character)

**If outline beat seems incomplete or unclear:**
- ❌ DO NOT improvise to "make it work"
- ✅ FLAG IT and ask user for clarification
- ✅ Implement literally what IS written, skip what ISN'T

### 8. Flag Missing Details (NEW - CRITICAL)

**If ANY detail needed for the scene is NOT in element files, STOP writing.**

**Create a "❓ MISSING DETAILS - USER INPUT NEEDED" section:**

**Examples of details to flag:**
- Character physical descriptions not in files
- Character backgrounds/history not documented
- Relationship histories not established
- Object descriptions (car models, clothing brands, possessions)
- Location specifics (if setting.md doesn't cover it)
- Character motivations not explained in files
- Technical details (procedures, mechanisms, how things work)

**Format for asking:**
```
## ❓ MISSING DETAILS - USER INPUT NEEDED

Before proceeding with Scene X, I need clarification:

### 1. [Detail Category]
**Outline says:** [what outline mentions]
**Currently missing:** [what's not in files]
**Question:** [specific question for user]
**Options (if applicable):** [logical possibilities based on context]

### 2. [Next detail]
...

**Please provide answers, and I'll proceed with accurate details.**
```

**DO NOT:**
- ❌ Invent details to fill gaps
- ❌ Guess at character backgrounds
- ❌ Make up object descriptions
- ❌ Assume relationship histories
- ❌ Proceed with scene until user provides details

**DO:**
- ✅ Stop immediately when detail is missing
- ✅ List ALL missing details before asking
- ✅ Provide context from outline/prior scenes
- ✅ Offer logical options when possible
- ✅ Wait for user response
- ✅ Document user's answers in appropriate element file after scene is complete

## McDonald Opening Rule (NON-NEGOTIABLE)

See `references/mcdonald-rule.md` for full explanation.

**NEVER open with:**
- ❌ Weather descriptions
- ❌ Atmospheric scene-setting
- ❌ Introspection before dialogue
- ❌ Character arriving at location

**ALWAYS open with:**
- ✅ Dialogue mid-progress
- ✅ Action already in motion
- ✅ Eavesdropper test: reader overhears conversation in progress

**Test:** Could an eavesdropper understand what's happening without needing narrator exposition first?

### Quick Examples

**❌ BAD:**
```
Rain drummed against the windows of Eddie's kitchen. Doogan felt exhausted after the interrogation.
```

**✅ GOOD:**
```
"—so Hank costs money, obviously, guy's a lawyer even if he's a bottom-tier one—"
```

## Stephen King Principles

See `references/king-principles.md` for full details. Key rules:

1. **Discovery-Driven** - Character action drives plot (not convenience)
2. **Sensory Detail** - One specific sensory detail per scene beat
3. **Emotional Truth** - Character behavior must be honest
4. **Cut 10-20%** - First draft is too long; remove adverbs, strengthen verbs

## POV Discipline (CRITICAL)

**This project uses third-person close, one POV per scene.**

- Reader knows ONLY what POV character knows
- No head-hopping (switching POV mid-scene)
- No omniscient narrator intrusions
- Off-screen events delivered indirectly (briefing, document, report)

**Fletch Rule:** Reader learns when protagonist learns.

## Continuity Violation Prevention (CRITICAL)

**Common continuity errors to avoid:**

### The Secrecy Rule (NON-NEGOTIABLE - STORY-BREAKING IF VIOLATED)

**Doogan's business only works if targets never know they're part of a paid operation.**

See `elements/checklist.md` → "The Secrecy Rule" and `elements/notes.md` → "The Secrecy Rule" for complete guidance.

**Critical Points:**
- Targets believe Doogan's interest is genuine
- Cover stories explain Doogan's presence (family friend, coincidence, mutual connection)
- Targets may become skeptical about authenticity, but NEVER discover it's a paid service
- NO character references "hiring," "paying," "job," "babysit," or "service" in relation to Doogan

**Example violations to NEVER write:**
- ❌ "My parents paid you to babysit me"
- ❌ "Is this your job?"
- ❌ "How much are they paying you?"

**Acceptable skepticism:**
- ✅ "You're too perfect. This feels like a setup."
- ✅ "My parents set me up with someone exactly like you. That's suspicious."
- ✅ "You're really good at this. Too good."

**If target discovers the truth, it's a story-breaking crisis event (has NOT happened in Episodes 1-2).**

### Invented Details
- ❌ Adding store brand names not mentioned (e.g., "Ralphs" when prior scene said "grocery store")
- ❌ Specifying car makes/models not in character files
- ❌ Describing homes/apartments with details not established
- ❌ Inventing clothing brands, styles, or colors
- ❌ Adding physical traits not in character files (eye color, height, build)

### Knowledge Violations
- ❌ Character knowing information they haven't learned yet
- ❌ Character forgetting information they learned earlier
- ❌ POV character knowing things that happened off-screen without being told

### Self-Contradictory Fabrications (CRITICAL - NEW)

**The "cash under the table + tax forms" error class:**

These are invented details that directly contradict the mechanism that makes another detail possible.

**Examples of self-contradictory fabrications:**
- ❌ "Paid cash under the table" + "Baxter found tax records" (tax records mean it WAS reported, not under the table)
- ❌ "Completely off the grid" + "Found through social media" (can't be both)
- ❌ "Never left fingerprints" + "Matched fingerprints to scene" (contradictory)
- ❌ "No paper trail" + "Traced through business filings" (filings ARE paper trail)
- ❌ "Anonymous transaction" + "Credit card receipt" (credit cards aren't anonymous)

**Prevention Protocol:**

**BEFORE writing any "how we found X" explanation:**
1. **Read the prior scenes** that established HOW it was found
2. **Identify the mechanism** explicitly stated (tax forms, social media, witness statement, etc.)
3. **Do not add contradictory color** that undermines the mechanism
4. **Verify logic chain:** If A enabled us to find B, then A must be possible/true

**Example from actual error:**
```
❌ WRONG:
"She worked there cash under the table, no official records except the tax forms Baxter pulled"

PROBLEM: "Cash under the table" means NO official reporting
BUT: "tax forms" means it WAS officially reported
THESE CONTRADICT EACH OTHER

✅ CORRECT (honors the mechanism):
"She worked there eight months, filed a 1099 which is how Baxter found the place"

OR (if truly under the table):
"She worked there eight months under the table, but Baxter traced her through [different mechanism]"

BUT NOT BOTH "under the table" AND "tax forms" - pick ONE and stick with it.
```

**Mechanism Verification Checklist:**

Before writing ANY "how we know this" or "how we found this" line:
- [ ] **Read outline:** What does it say about how this was discovered?
- [ ] **Read prior scenes:** Was the mechanism already established?
- [ ] **Check notes.md:** Are there procedures or research methods documented?
- [ ] **Logic check:** Does my explanation contradict the mechanism?
- [ ] **Simplify:** Can I just state the mechanism without adding "color" that contradicts it?

**If you're unsure about the mechanism:**
- ✅ Use the EXACT wording from outline/prior scene
- ✅ Keep it simple: "Baxter found her through tax records" (don't elaborate)
- ✅ Flag for user review if mechanism seems unclear

**RED FLAGS that indicate potential self-contradiction:**
- Writing "but" or "except" in same sentence as contradictory detail
- Adding "color" details about how something was done without checking if that contradicts the discovery method
- Assuming details about financial arrangements (cash/check/wire/reported/unreported) without checking canon
- Embellishing with specific methods when outline only says "found" or "traced"

### Relationship Errors
- ❌ Changing established relationship dynamics without cause
- ❌ Characters using nicknames not yet established
- ❌ Ignoring established tensions or conflicts

### Physical Continuity
- ❌ Objects appearing/disappearing (if character arrived with coffee cup, it stays unless mentioned)
- ❌ Time inconsistencies (scene 2 can't be morning if scene 1 ended at night)
- ❌ Location errors (if they're in Eddie's kitchen, stay consistent with established layout)

**Rule:** When in doubt, stay VAGUE. "She drove away" not "She drove away in her BMW." Generic is safe.

### Environment as Character Exposition (CRITICAL)

**Use visible objects in a character's environment to convey background, accomplishments, lifestyle, and health status. NEVER have characters talk about their own résumé.**

**The Rule:**
POV character observes objects → Infers information → Reader learns through observation

**Examples:**

❌ **WRONG: Career Exposition in Dialogue**
```
"I've been doing this seventeen years."
"Now I manage north of two hundred million."
"Started on the floor of the exchange."
```

✅ **RIGHT: Environment Shows Background**
```
"Ironman triathlon finish shot, sail boat, golf tournament trophy, shots of the man with his trophy family."
— POV character (Eddie) observes photos on credenza
— Reader infers: healthy, active, affluent, accomplished
— Zero dialogue about career/accomplishments
```

**What to Show Through Environment:**
- **Health:** Sports trophies, race medals, athletic photos, gym equipment
- **Wealth:** Office quality, artwork, furniture, neighborhood, vehicle
- **Background:** Diplomas, certificates, family photos, memorabilia
- **Personality:** Desk organization, book selection, décor style, personal items

**POV Character's Role:**
- Notices specific objects ("Ironman finish photo")
- Makes wry observations ("Outdoor sports?")
- Infers without asking directly
- Lets reader draw conclusions

**FORBIDDEN:**
- ❌ Characters stating years of experience
- ❌ Characters listing credentials or degrees
- ❌ Characters announcing income/assets managed
- ❌ Characters describing their own accomplishments
- ❌ POV asking "how long have you been doing this?"
- ❌ POV asking "do you exercise much?"

**Why This Matters:**
- Respects reader intelligence (show, don't tell)
- Keeps dialogue focused on scene's actual purpose
- Creates natural characterization through observation
- Prevents exposition dump interruptions
- Maintains third-person close POV discipline

**Scene-Writing Application:**
When POV character enters a space, describe 2-4 specific visible objects that reveal character background. Let POV character notice them, possibly comment wryly, then move on to scene's actual purpose.

### Character Worldview Over Biography (CRITICAL)

**One-scene characters must be PEOPLE with worldviews and ethics, not résumés with dialogue. Reveal character through philosophy/values, NEVER through career stats.**

**The Rule:**
Character's ETHICS and WORLDVIEW define them → Creates dramatic content → Biography emerges as byproduct

**Examples:**

❌ **WRONG: Career Biography**
```
"Seventeen years in finance."
"Manage portfolios north of two hundred million."
"Clients across three states."
```
PROBLEM: This is a résumé, not a person. Creates no dramatic tension. Just data delivery.

✅ **RIGHT: Character Philosophy/Worldview**
```
"There are two types of investors. Predators and prey. Predators see the shift coming before anyone else. They don't wait for consensus. They move."
```
REVEALS: Ethics (social-Darwinist), personality (aggressive), worldview (competitive), potential conflict with Eddie's values

**What Worldview Reveals:**
- **Ethics:** How they view right/wrong, rules, other people
- **Values:** What they prioritize (money, status, fairness, loyalty)
- **Personality:** Aggressive, cautious, cynical, optimistic
- **Potential Conflict:** Where they might clash with protagonist

**How POV Character Responds:**
- Reacts to the PHILOSOPHY, not the information
- Makes wry observation ("Outdoor sports?")
- Engages with the worldview or deflects
- Learns information as BYPRODUCT of interaction

**Scene Structure:**
1. Character states philosophy/worldview
2. POV character responds to WHO this person is
3. Information emerges naturally through interaction
4. Scene has dramatic content (clash of values, personality friction)

**FORBIDDEN:**
- ❌ Characters stating years in profession
- ❌ Characters listing credentials
- ❌ Characters announcing revenue/clients/accomplishments
- ❌ POV asking "how long have you been doing this?"
- ❌ POV asking about career history
- ❌ Treating one-scene characters as information sources only

**Why This Matters:**
- Creates actual dramatic content (personality, ethics, potential conflict)
- Respects that even one-scene characters are PEOPLE
- Makes scenes ABOUT something beyond data delivery
- Generates natural dialogue instead of interview format
- Reveals information as byproduct, not purpose

**Scene-Writing Application:**
When introducing any speaking character (even one-scene), establish their worldview/philosophy within first 3-5 lines. Let POV character respond to WHO they are. Information about their role/background emerges through interaction, not interrogation.

### Name Every Speaking Character (CRITICAL)

**Every character who speaks must have a name. NEVER use generic labels like "the broker," "the nurse," "the clerk." Naming creates presence and respect.**

**The Rule:**
If character speaks → Character has name → Use it consistently

**Examples:**

❌ **WRONG: Generic Label**
```
"The broker leaned back."
"The finance guy nodded."
"He gestured to the chart."
```
PROBLEM: Reduces person to function. Creates distance. Feels like NPC in video game.

✅ **RIGHT: Named Character**
```
"Phil Blakely leaned back."
"Blakely nodded."
"He gestured to the chart."
```
REVEALS: This is a PERSON who exists in this world. Has identity beyond role.

**Naming Conventions:**
- **First Introduction:** Full name ("Phil Blakely")
- **Subsequent References:** Last name ("Blakely") or pronoun ("he")
- **Dialogue Tags:** Use name in first tag, then pronouns if clear

**How to Generate Names:**
1. Check if character file exists in `elements/characters/`
2. If not, check notes.md for any mentioned names
3. If creating new one-scene character, choose name that:
   - Fits setting/genre (professional environment → professional name)
   - Isn't similar to existing character names
   - Feels real (not placeholder like "Bob Smith")
   - Has appropriate ethnicity/cultural background for setting

**FORBIDDEN:**
- ❌ "the broker," "the finance guy," "the man"
- ❌ "the nurse," "the receptionist," "the clerk"
- ❌ "the waiter," "the driver," "the trainer"
- ❌ Using profession as label for speaking characters
- ❌ Leaving character unnamed because they're "minor"

**Exception:**
Non-speaking background characters CAN remain unnamed ("a waiter refilled water glasses"). But if they speak, they need a name.

**Why This Matters:**
- Shows respect for every character as a person
- Creates sense of populated, real world
- Prevents "NPC" feeling in scenes
- Makes dialogue tags clearer and more natural
- Establishes that even one-scene characters matter

**Scene-Writing Application:**
Before writing ANY scene with new speaking character, determine their name. Add to notes.md after scene complete if they might appear again. For true one-scene characters, name is sufficient—no need to create full character file unless they become recurring.

### Every Scene Must Be ABOUT Something (CRITICAL)

**Scenes are dramatic encounters between people, NOT information-delivery mechanisms. The scene must be ABOUT character interaction, worldview clash, or emotional stakes—information emerges as byproduct.**

**The Rule:**
Scene's PURPOSE ≠ Delivering information
Scene's PURPOSE = Dramatic content (clash, tension, personality, decision)
Information = Byproduct of dramatic interaction

**Examples:**

❌ **WRONG: Scene as Data Delivery**
```
Purpose: "Eddie needs to learn if broker is healthy"
Structure: Eddie asks health questions → Broker answers → Eddie gets information → Scene ends
Result: Interview format. No dramatic content. Feels mechanical.
```

✅ **RIGHT: Scene as Dramatic Encounter**
```
Purpose: "Eddie encounters predatory finance-bro philosophy and responds to WHO this person is"
Structure: Blakely states worldview (predators/prey) → Eddie responds with wry observation → Eddie infers health from environment → Scene is ABOUT the personality clash
Byproduct: Eddie learns broker is healthy (through photos, trophies)
Result: Actual dramatic content. Character-driven. Information emerges naturally.
```

**What Makes Scene "ABOUT Something":**
- **Personality Clash:** POV character encounters different worldview/ethics
- **Values Conflict:** Characters have competing priorities
- **Emotional Stakes:** Decision, revelation, or realization with weight
- **Character Choice:** Someone makes decision that reveals who they are
- **Power Dynamic:** Status, control, or influence shifts between characters

**Scene Structure (Proper):**
1. **Opening:** Drop into existing interaction (McDonald rule)
2. **Dramatic Content:** Character philosophies, ethics, personalities interact
3. **POV Response:** Protagonist reacts to WHO the other person is
4. **Information Byproduct:** Necessary plot info emerges through interaction
5. **Button:** Scene ends on turn or decision, propels to next scene

**FORBIDDEN:**
- ❌ Scene exists ONLY to deliver plot information
- ❌ POV character asks direct questions to extract data
- ❌ Other character answers in exposition mode
- ❌ Dialogue feels like interrogation or interview
- ❌ No actual dramatic content (personality, conflict, decision)
- ❌ Scene could be replaced with "Eddie researched the broker and learned he was healthy"

**The "Could This Be a Paragraph?" Test:**
If scene could be replaced with single paragraph of summary without losing anything important, scene ISN'T about something—it's just data delivery. Fix it.

**Why This Matters:**
- Respects reader expectation (scenes are for drama, not just info)
- Creates actual story content (characters, conflict, stakes)
- Makes protagonist ACTIVE (responding to people, not extracting data)
- Generates organic dialogue (interaction, not interrogation)
- Information lands better when it's byproduct of drama

**Scene-Writing Application:**
BEFORE writing scene, ask: "What is this scene ABOUT (dramatically)?" If answer is only "character learns X information," stop and redesign. Find the dramatic content: whose worldview appears? What personality does POV encounter? What's the actual human interaction? Then let information emerge as byproduct.

### POV Character Responds to WHO, Not Information Need (CRITICAL)

**POV character responds to the OTHER CHARACTER'S personality, energy, and philosophy—NOT to the plot's need for information. This creates realistic interaction instead of mechanical interrogation.**

**The Rule:**
POV reacts to WHO the person is → Makes observations about personality → Information learned indirectly
NOT: POV thinks "I need to know X" → Asks question to get X → Gets X

**Examples:**

❌ **WRONG: Responding to Information Need**
```
Eddie thought: I need to know if he's healthy.
Eddie asked: "Do you exercise much?"
Eddie thought: I need to know about time off.
Eddie asked: "Ever take time off? For health stuff?"
```
PROBLEM: Eddie is a robot extracting data. No human personality. Interview format.

✅ **RIGHT: Responding to WHO Character Is**
```
Blakely stated philosophy: "Predators and prey. Predators move first."
Eddie observed environment: Ironman photos, trophies, sailboat shots
Eddie responded to personality: "Outdoor sports?" (wry, observing the aggressive-achiever type)
Result: Eddie learned health status by responding to WHO Blakely is (trophy-collecting predator)
```

**What POV Character Notices:**
- **Personality:** Aggressive? Cautious? Arrogant? Nervous?
- **Energy:** High-energy motor-mouth? Measured and controlled? Scattered?
- **Ethics:** Ruthless? Principled? Cynical? Idealistic?
- **Environment:** What objects reveal about them?
- **Contradictions:** Do words match environment? Actions match philosophy?

**How POV Character Responds:**
- Makes wry observation
- Comments on personality ("You sound like Terry")
- Deflects or engages philosophy
- Notices objects and infers
- Reacts emotionally to WHO they're encountering

**Scene Interaction Flow:**
1. Other character reveals personality/worldview
2. POV character NOTICES who they're dealing with
3. POV responds to personality (not extracting information)
4. Information emerges as natural byproduct
5. Scene is about the PEOPLE, not the data

**FORBIDDEN:**
- ❌ POV thinking "I need to learn X" then asking for X
- ❌ POV asking direct questions to extract plot information
- ❌ POV in interrogation mode (question → answer → question)
- ❌ POV ignoring personality to focus on data extraction
- ❌ Dialogue structured as: Need info → Ask for info → Receive info → Move to next info need

**Character-Specific Applications:**

**Eddie Palmer (motor-mouth investigator):**
- Responds to personality with rapid observations
- Makes connections between what he sees and who they remind him of
- Infers rather than asks directly
- Example: "Outdoor sports?" (observing photos) not "Do you exercise?"

**Doogan Andrews (measured observer):**
- Notices personality, responds minimally
- Lets others talk, observes contradictions
- Asks follow-up questions about PHILOSOPHY, not facts
- Example: "That how you see yourself?" (engaging worldview) not "What's your background?"

**Abby Palmer (sharp analyst):**
- Cuts through bullshit, responds to what's REALLY being said
- Notices gaps between words and actions
- Challenges philosophy if it's suspect
- Example: "So you're a predator who preys on people's fear?" not "How do you make money?"

**Why This Matters:**
- Creates realistic human interaction (people respond to personality, not plot)
- Keeps POV character feeling like actual person, not robot
- Makes dialogue natural (conversation, not interview)
- Information emerges organically (byproduct of interaction)
- Respects reader intelligence (show character responding like human would)

**Scene-Writing Application:**
BEFORE POV character speaks, ask: "What personality trait is POV responding to HERE?" Not "What information does POV need?" If you can't answer the personality question, redesign the beat. POV should always respond to WHO the other person is showing themselves to be.

## Character Voice Patterns

**Doogan Andrews:**
- Measured drawl
- Short responses
- Dry humor
- Observant, not chatty

**Eddie Palmer:**
- Motor-mouth avalanche
- Mid-sentence starts with em-dashes
- Tangents that circle back
- Nervous energy

**Abby Palmer:**
- Elevated vocabulary
- Sharp, pragmatic
- No yoga pants / messy home clichés
- Confident, competent

**Martinez:**
- Deadpan delivery
- Dry wit
- Principled, married high school sweetheart
- Doesn't understand Doogan's world

## Dialogue Formatting

**Max 3 untagged lines** in 2-person dialogue:

```markdown
"First line," Doogan said.
"Response."
"Follow-up."
"Final response," Eddie said.
```

After 3 lines, re-tag speaker.

## Scene Structure

1. **Opening** (McDonald rule compliance)
2. **Escalation** (tension increases or discovery occurs)
3. **Turn** (something shifts—information, emotion, decision)
4. **Button** (scene ending that propels to next scene)

## Scene Ending Discipline (CRITICAL - HARD STOP RULE)

**STOP WRITING AT THE BUTTON. DO NOT CONTINUE.**

### The Problem: Scene Epilogue Bloat

**Common violation:** After the scene's purpose is complete (decision made, information revealed, action taken), writers continue with:
- ❌ Reflective epilogues (character thinking about what just happened)
- ❌ Rehashing conversations that already occurred
- ❌ "One more thing" beats that belong in next scene
- ❌ Extended goodbyes or transitions
- ❌ Internal monologue wrapping up themes
- ❌ Characters discussing what they just decided
- ❌ Walking to next location (that's next scene's opening)

### The Rule: Button = Hard Stop

**Once the scene's functional purpose is complete, END THE SCENE.**

**Scene purpose examples:**
- Decision made → END (don't show them discussing the decision again)
- Information revealed → END (don't show them processing it at length)
- Agreement reached → END (don't show them confirming it repeatedly)
- Action taken → END (don't show aftermath unless that's this scene's purpose)

### Real Example from Episode 3, Scene 1

**Original ending (312 lines):** Scene continued for ~186 lines after the decision was made, including:
- Multiple "are you sure?" exchanges
- Jake's additional warnings about Mara
- Cart ride with Eddie monologuing
- Doogan's internal reflections about hoping "this stayed simple"
- Extended goodbye sequences

**Corrected ending (126 lines):** Scene ends immediately after logistics established:
```markdown
"Making my point for me. The humility. You can't fake that, Jake."

They reached Eddie's ball. He pulled a club, studied the distance.

Doogan walked to his own ball, crouched, read the lie. Good position. Clean shot to the green. "Then I'll see you Monday night."

---
```

**What was cut:** 186 lines of epilogue material that didn't advance the scene's purpose.

### Scene Ending Checklist

**Before writing past the button, ask:**

1. **Has the scene's purpose been fulfilled?**
   - ✅ Decision made? → STOP
   - ✅ Information delivered? → STOP
   - ✅ Agreement reached? → STOP
   - ✅ Stakes established? → STOP

2. **Am I writing beats that belong in the next scene?**
   - ❌ Character traveling to next location? → Next scene's opening
   - ❌ Character processing information alone? → Next scene (if needed at all)
   - ❌ "One more thing" revelations? → Next scene or cut entirely

3. **Am I rehashing what already happened?**
   - ❌ Characters discussing the decision they just made? → REDUNDANT
   - ❌ Character thinking about what was just said? → REDUNDANT
   - ❌ Confirming agreements already confirmed? → REDUNDANT

4. **Would cutting the next 50 lines hurt the scene's purpose?**
   - ✅ If NO → CUT THEM
   - ❌ If YES → Those lines probably belong in earlier in the scene

### Hard Stop Signals

**When you see these patterns forming, STOP IMMEDIATELY:**

- Character enters vehicle to travel → STOP (next scene opens at destination)
- Character alone with thoughts about what happened → STOP (reader was there, they know)
- "One more thing" after agreement reached → STOP (save for next scene or cut)
- Characters saying goodbye → STOP (goodbye is the button)
- "Let me think about this" / reflection → STOP (next scene shows the result)

### Button Types & How to End

**Agreement/Decision Button:**
```
"Then I'll see you Monday night."
---
[STOP - don't show them leaving, don't show drive home, don't show processing]
```

**Information Reveal Button:**
```
"She worked at the clinic. Same one we're investigating."
---
[STOP - don't show team discussing implications, that's next scene]
```

**Action Taken Button:**
```
He started the car and pulled into traffic.
---
[STOP - don't show the drive, next scene opens at destination]
```

**Cliffhanger Button:**
```
The phone rang. Martinez.
---
[STOP - next scene is the phone conversation]
```

### Word Count Guideline

**Target scene length:** 800-1,200 words for most scenes

**Warning signs you've written too long:**
- Scene exceeds 1,500 words → Check for epilogue bloat
- Scene exceeds 2,000 words → Almost certainly has 500+ words of unnecessary ending
- Multiple "farewell" beats → Cut to first goodbye
- Character reflection paragraphs at end → Cut entirely

### Enforcement

**This is a HARD RULE. If you write past the button:**
- ❌ Scene is too long
- ❌ Pacing suffers
- ❌ Next scene's opening is stolen
- ❌ Reader gets bored

**When in doubt:** End the scene 100 words earlier than feels natural. The reader's imagination will fill the gap.

### Confrontation Scenes: Cut Them Short (CRITICAL - NEW)

**Problem:** Writers tend to over-explain confrontations, dragging out tension with repetitive dialogue exchanges.

**The McDonald Principle:** One sharp line carries more weight than five lines of interrogation.

**Real Example from Episode 3, Scene 2:**

**❌ WRONG (over-explained, 30+ lines):**
```markdown
Nancy's gaze flicked to the filing cabinet, then back to Abby. "This room is clearly marked 'Staff Only.'"

"I know, I just—"

"The bathroom is down the hall. In the opposite direction." Nancy stepped fully into the room, blocking the doorway. "You were in Exam 4. That's three doors past the bathroom. You'd have to walk past it to get here."

Abby forced an apologetic expression. "I'm sorry. I wasn't paying attention."

"You seem to have trouble following basic directions." Nancy's tone could cut glass. "First you're wandering the hallways when you should be waiting for the doctor. Now you're in restricted areas. Is there a reason you're so... curious about our clinic layout?"

"I'm not—I was just looking for—"

"The bathroom. Right." Nancy's eyes narrowed. "What's in your purse?"

Abby's hand moved instinctively to her purse, protective. "Excuse me?"

"You heard me. What's in your purse?"

"That's none of your business."

"Actually, when patients start snooping through staff areas, it becomes my business." Nancy took a step closer. "I could call security. Have them check. Or you could show me yourself."

Abby met her eyes. Nancy wasn't bluffing. But she also had no actual authority to search a patient's belongings without cause. It was a power play.

"I'd like to return to my exam room now."

"Not until you explain why you're back here."

"I got lost."

"Twice."

They stood there, locked in silent confrontation. Nancy's perfectly manicured nails—French tips, flawless—tapped against her clipboard. Expensive nails. Expensive scrubs. Everything about this woman screamed money that a nurse's salary shouldn't afford.

Finally, Abby broke the standoff. "I'll wait for the doctor in the lobby. I don't feel comfortable continuing this appointment."

She moved toward the door. Nancy didn't step aside immediately. For a moment, Abby thought she'd actually block her. Then Nancy shifted, just enough.

Abby walked past, feeling Nancy's eyes boring into her back. She returned to Exam 4, grabbed her jacket, left the room. Walked down the hallway toward the lobby, Nancy trailing ten feet behind like a prison guard.
```

**✅ CORRECT (trust the reader, cut short, 8 lines):**
```markdown
Nancy's gaze flicked to the filing cabinet, then back to Abby. "This room is clearly marked 'Staff Only.'"

"I know, I just—"

"The bathroom is down the hall. In the opposite direction." Nancy stepped fully into the room, blocking the doorway. "You were in Exam 4. That's three doors past the bathroom. You'd have to walk past it to get here."

Abby forced an apologetic expression. "I'm sorry. I wasn't paying attention."

"The bathroom. Right." Nancy's eyes narrowed.

Abby slipped back into the exam room, closed the door but just shy of latching. She waited for a beat or two before cracking the door to confirm Nancy was no longer in the hallway.
```

**What Was Cut:** 22+ lines of:
- Repetitive accusations ("You're snooping," "You're curious")
- Purse search threat (over-explaining Nancy's hostility)
- Power struggle choreography (blocking, confronting, trailing)
- Multiple "I'm leaving" beats
- Detailed physical descriptions mid-confrontation

**What Carries the Scene:**
- "Right." — One word. Nancy doesn't believe her. Reader gets it.
- Reader already knows: Nancy caught Abby in restricted area, both know it's suspicious
- Trust the reader to understand the tension without spelling it out

### Confrontation Cutting Rules

**STOP writing when:**
1. **Suspicion is established** - Don't belabor it with multiple accusations
2. **Power dynamic is clear** - Don't choreograph every blocking move
3. **Character makes decision** - Don't show them explaining/justifying it repeatedly

**Cut these patterns:**
- ❌ "You're lying" / "No I'm not" / "Yes you are" exchanges
- ❌ Repeated threats that escalate ("I could do X" / "Or I could do Y")
- ❌ Character explaining their lie multiple times
- ❌ Detailed physical description of opponent mid-confrontation
- ❌ Internal monologue about whether opponent is bluffing
- ❌ Multiple "I'm leaving" attempts with blocking/yielding choreography

**Keep only:**
- ✅ Initial accusation/suspicion
- ✅ One deflection/excuse
- ✅ One sharp line that shows disbelief ("Right.")
- ✅ Exit (immediate, no extended negotiation)

### Trust Single Lines

**One dismissive word carries more weight than ten lines of interrogation:**

- "Right." — Establishes Nancy doesn't believe Abby
- "Sure." — Skepticism without explanation
- "Interesting." — Implies suspicion without stating it
- "I see." — Communicates doubt clearly

**The reader is smart.** They were present for the scene. They know:
- Why the character is lying
- Why the antagonist is suspicious
- What the stakes are
- What both parties are protecting

**Don't explain it again through extended confrontation dialogue.**

### Before/After Comparison

**BEFORE (typical AI over-writing):**
- 30-50 lines of confrontation
- Multiple back-and-forth exchanges
- Detailed power struggle choreography
- Reader bored by line 15

**AFTER (McDonald-style cut):**
- 8-12 lines maximum
- One accusation, one deflection, one sharp dismissal
- Exit immediately
- Reader engaged, tension preserved

**Length Guideline:** If your confrontation scene exceeds 15 lines of dialogue, cut it in half.

**When in doubt:** End confrontation after the first suspicious "Right." or "I see." Everything after that is over-explanation.

## Output Format

Output scene content as markdown:

```markdown
## Scene [Number] — [Title]

[Scene content here]

---
```

## Scene Opening Techniques (CRITICAL - UPDATED)

### The Em-Dash Cold Open (Preferred)

**Start mid-sentence with dialogue or action already in progress:**

```markdown
## Scene 3 — Welcome Gala

"—come on, John. If you'll go to fifteen, I'll see if I can get an hour driving the ball return cart..."
```

**Why this works:**
- Drops reader directly into active scene
- No setup, no explanation
- Reader catches up through context
- Creates immediate energy and momentum

**When to use:**
- Scenes with active dialogue/events (auctions, meetings, arguments)
- High-energy openings
- When scene picks up mid-conversation or mid-action

### Action Beat Opens (Alternative)

**Start with character mid-action:**

```markdown
Doogan crossed the parking lot toward Eddie's truck.

"You bring coffee?"
```

**When to use:**
- Quieter scenes
- Physical movement openings
- When establishing location is important

### What NEVER to Open With

❌ Weather descriptions
❌ Time of day setup ("The morning sun...")
❌ Atmospheric descriptions ("The kitchen smelled of...")
❌ Character introspection
❌ Summaries of what's happening ("The MC had the room eating out...")
❌ "Establishing shot" prose

### Trust the Reader

**Don't explain who's speaking—show through action:**

❌ WRONG: "The MC, a well-known comedian, had the room eating out of his hand"
✅ RIGHT: "—forty-five thousand for a weekend..." [dialogue establishes MC through what they do]

**Character identification through action beats:**
- First mention: Use action beat that reveals context
- "A man in a tailored tuxedo nodded while holding up his paddle" (reader learns he's John through MC calling him)
- Don't frontload "John, the tech CEO wearing..." 
- Let context reveal identity naturally

### The Sorkin Pace

**Use background activity as cinematic atmosphere:**
- Auction running while characters talk
- MC's voice weaving through foreground conversation
- Environmental layers without stopping action
- Keep dialogue moving, let background breathe

**Example structure:**
1. Open with background event (MC at auction)
2. Quick anchor of POV character (Doogan stood in back)
3. Background continues (MC makes jokes, crowd reacts)
4. Foreground action begins (Doogan moves, interacts)
5. Background weaves through (MC voice continues between beats)

**Balance:**
- McDonald efficiency (brief, tight)
- Sorkin atmosphere (layered environment)
- Trust reader to track multiple threads simultaneously

## Validation Checklist

After writing, verify:

- [ ] **Pre-Writing Completed:** ALL elements, voice, and prior content files loaded
- [ ] **Continuity Preserved:** NO invented details (checked against prior scenes and element files)
- [ ] **Established Facts Honored:** Store names, car models, pet names, physical traits all match prior content
- [ ] **Self-Contradiction Check (CRITICAL):** No fabricated details that contradict established mechanisms
- [ ] **Opening Technique:** Em-dash cold open or action beat (NOT weather/introspection/summary)
- [ ] **Trust Reader:** No hand-holding, context reveals details organically
- [ ] **Action Beats as Exposition:** Character details shown through action, not description
- [ ] McDonald opening (no weather/introspection first)
- [ ] POV maintained throughout (no head-hopping)
- [ ] Character voices accurate (reviewed character files)
- [ ] Sensory details present (specific, not generic)
- [ ] Emotional truth (behavior feels honest)
- [ ] Scene opens/closes doors (discovery momentum)
- [ ] **Stopped at Button:** Did not spill into next scene's beats
- [ ] Scene break marker `---` at end
- [ ] **Environment as Exposition (CRITICAL):** Background shown through visible objects, NOT dialogue about career/accomplishments
- [ ] **Character Worldview (CRITICAL):** One-scene characters reveal philosophy/ethics, NOT résumé details
- [ ] **Named Characters (CRITICAL):** Every speaking character has name, not generic label
- [ ] **Scene ABOUT Something (CRITICAL):** Scene has dramatic content (personality clash, values conflict), information is byproduct
- [ ] **POV Responds to WHO (CRITICAL):** POV character responds to personality/philosophy, NOT extracting information through interrogation

## Post-Writing Self-Contradiction Audit (NEW - MANDATORY)

**BEFORE finalizing scene, run this line-by-line audit:**

### Audit Process:

**1. Scan for "mechanism" statements** (lines about how something was discovered/done):
   - Lines containing: "found through," "traced via," "discovered by," "researched," "identified"
   - Lines about money: "paid," "cash," "check," "wire," "under the table," "officially"
   - Lines about records: "tax forms," "official records," "filing," "paper trail"

**2. For EACH mechanism statement, verify:**
   - **Does this match prior scenes?** Check exact wording in prior content
   - **Does this match outline?** Check episode outline for how this was established
   - **Is there internal contradiction?** Look for "but" or "except" connecting contradictory details
   - **Does the mechanism enable the result?** (e.g., "found via tax records" requires tax records exist)

**3. Red Flag Patterns to Fix:**

```
❌ PATTERN: "[Contradictory descriptor] + [contradicting fact]"
Examples:
- "off the books + found via records"
- "cash under table + tax forms"
- "no paper trail + business filing"
- "anonymous + credit card"
- "completely hidden + social media post"

✅ FIX: Remove contradictory descriptor, keep mechanism only
- "found via records" (drop "off the books")
- "filed tax forms" (drop "cash under table")
- "business filing" (drop "no paper trail")
- "credit card" (drop "anonymous")
- "social media post" (drop "completely hidden")
```

**4. Fabricated Color Check:**

Ask for each detail: **"Did I add this for color, or is it canonical?"**

If you added detail for color/atmosphere, check:
- [ ] Does it contradict any mechanism?
- [ ] Does it contradict prior scenes?
- [ ] Could I just remove it without losing meaning?

**When in doubt: CUT THE COLOR. Keep only mechanism.**

### Example Audit:

**Original line (WRONG):**
> "She worked at this clinic for eight months, cash under the table, no official records except the tax forms Baxter pulled"

**Audit Questions:**
- Q: How did Baxter find her? A: Tax forms
- Q: Were tax forms filed? A: Yes (prior scene: "She filed a 1099")
- Q: Can "cash under table, no records" AND "tax forms filed" both be true? A: NO ❌

**Fixed line:**
> "She worked at this clinic for eight months, filed a 1099 which is how Baxter found the place"

**Audit Result:** ✅ PASS - No contradiction, mechanism preserved

### Continuity Cross-Check

**Before finalizing, answer these questions:**

1. Did I invent ANY detail not in element files or prior scenes? (If yes, remove or make vague)
2. Does this contradict anything established in prior episodes/scenes? (If yes, fix it)
3. Do all character voices match their established patterns? (Check character files)
4. Does POV character know only what they should know at this point? (Check timeline)
5. Are all physical details (clothing, vehicles, locations) consistent with prior scenes?

**If you cannot verify a detail exists in canon, make it GENERIC or REMOVE IT.**

## Next Step

After drafting, use **draft-validation** skill to check against full checklist.
