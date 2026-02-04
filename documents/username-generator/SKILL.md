---
name: username-generator
description: >-
  Generate clever, witty, and original usernames based on user input keywords or theme.
  Scope: Outputs markdown bullet list of 20 usernames (unless specified), each ≤ 20 characters, using only alphanumeric characters and either hyphens or underscores.
  Triggers: "username", "username generator", "generate username", "create username", "creative usernames", "witty usernames".
allowed-tools: []
---

# Username Generator

## COMPONENTS
- **Dependencies**: None (LLM-generated)
- **Context**: User-provided keywords/themes

## INSTRUCTIONS

### Phase 1: Clarification
**Logic**: Ambiguity > 0 -> Stop && Ask.

Input Requirements:
- Keywords OR theme [Required]
- Quantity [Optional: Default=20]
- Format preference [Optional: hyphen OR underscore]

**IF** Missing keywords/theme OR Ambiguous intent:
- List: [What theme/keywords?, How many usernames (default 20)?]

Wait(User_Input).

### Phase 2: Planning
**Logic**: Theme -> Plan -> Approval.

**IF** Theme == Inappropriate/Hateful/Explicit:
- Output: "I'm sorry, but I can't generate usernames based on that theme."
- Stop.

Else:
- Parse keywords/theme
- Apply constraints:
  - Length: ≤ 20 chars/username
  - Charset: [A-Za-z0-9] + (hyphen OR underscore, not both)
  - Quantity: User_Specified OR 20
  - Tone: Clever, witty, playful
  - Safety: No profanity, sexual refs, hate speech, brand names, culturally insensitive jokes
  - Originality: Unique, not common/overused
- Generate puns/humor IF topic provided

### Phase 3: Execution
**Logic**: Step_1 -> Verify -> Step_2.

1. Extract keywords from user input.
2. Generate username list meeting ALL constraints.
3. Apply validation: Each username ≤ 20 chars, alphanumeric + ONE separator type.
4. Format: Markdown bullet list (• item).

### Phase 4: Validation
**Logic**: Result -> Checklist -> Done.

**Final_Checklist**:
- [ ] Exact requested quantity (default 20)?
- [ ] Each username ≤ 20 chars?
- [ ] Alphanumeric + ONE separator (hyphen OR underscore, not both)?
- [ ] Original, relevant, witty, safe for all audiences?
- [ ] Puns included IF topic provided?

**IF** Fail(Any):
- Self_Correct: Regenerate failing entries.

## EXAMPLES

### Example 1: Space Theme
User: "space"
Agent:
• AstroNutz
• OrbitWit
• CosmicComic
• LunarLaughs
• NovaKnowsBest
• ZeroGravityGig
• SaturnSmiles
• StarryWit
• MilkyPun
• RocketRoller
• SpaceySense
• OrbitOrbit
• MoonMirth
• LightSpeedy
• SkyPunLimit
• CosmicCrafter
• InterPunetic
• GalacticGig
• VoidVoyager
• AstroGiggle

### Example 2: Cats with Underscores
User: "cats, with underscores, 10 usernames"
Agent:
• Purr_Fect
• Meow_Wits
• Cat_Comic
• Kitty_Jokes
• Feline_Fun
• Paw_Puns
• Whisker_Wit
• Meow_Mirth
• Claw_Humor
• Purr_Funny

### Example 3: Inappropriate Theme
User: "inappropriate theme"
Agent:
I'm sorry, but I can't generate usernames based on that theme.

### Example 4: Incorrect Output
❌ INCORRECT:
• DarkHole69
• SpaceMaster3000
• Cool-Guy
• Hot_Babe

**FAIL REASONS**:
- DarkHole69: Sexualized number, not witty, inappropriate
- SpaceMaster3000: Generic/overused, not original
- Cool-Guy, Hot_Babe: Boring, Hot_Babe inappropriate

## VALIDATION PROTOCOL

**Security & Safety**:
- **Input_Sanitize**: Strip profanity, hate speech, sexual content
- **Output_Validate**: Verify format, length, charset constraints
- **Safety_Check**: Ensure all usernames inclusive, neutral, universally appropriate

**Failure Modes**:
- Theme = Explicit/Hateful -> Refuse with standard message
- Constraints_Violated -> Regenerate until pass
- Low_Creativity -> Increase pun/wordplay density

## ANCHORING

**Ref**:
- Clever == Original + Witty + Playful
- Safe == No profanity, hate speech, sexual refs, brand names, culturally insensitive content
- Separator == Hyphen (-) OR Underscore (_), mutually exclusive per output list
