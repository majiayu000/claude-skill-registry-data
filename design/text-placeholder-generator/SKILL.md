---
name: text-placeholder-generator
description: >-
  Generate satirical placeholder text (lorem ipsum style) and satirical news articles.
  Scope: placeholder text, dummy content, filler text, lorem ipsum, mock data, sample text, gibberish, dummy text, placeholder, parody article, satirical news, fake news story.
  Triggers: "placeholder text", "dummy content", "filler text", "lorem ipsum", "mock data", "sample text", "gibberish", "parody article", "satirical news", "fake news story".
---

# TEXT_PLACEHOLDER_GENERATOR

## QUICK_START
- Example (ipsum): "Generate 20 words of ipsum about space pirates"
- Example (parody): "Write a parody article about corporate meetings"

## CORE_RULES
- **Safety**: SFW + Family_Friendly ONLY. No politics, profanity, NSFW.
- **Style**: Satirical + Nonsensical (ipsum) || Professional_Satirical (parody)
- **Output**: Direct output only. No quotes, no intro.
- **Completeness**: Complete narrative. No half-stories.

## AUTO_DETECTION_ROUTING
**Logic**:
```
IF input contains {N} words/paragraphs/chars 
   OR "placeholder" OR "lorem ipsum" OR "dummy" OR "gibberish" OR "filler"
  → READ FILE: @references/ipsum.md
  → Mode = ipsum

ELIF input contains "parody article" OR "satirical news" OR "onion style" OR "fake news story"
  → READ FILE: @references/parody-article.md
  → Mode = parody-article

ELSE
  → READ FILE: @references/ipsum.md
  → Mode = ipsum (default)
```

## EXECUTION_PHASES

### Phase_1: Clarification (Ask)
- **Logic**: Ambiguity > 0 -> Stop && Ask
- **Required_Questions**:
  - Mode ambiguous? -> Clarify (auto-detect or explicit)
  - Length constraint missing (ipsum)? -> "Specify words/paragraphs/chars?"
  - Topic missing? -> Use default (random generation)

### Phase_2: Planning (Think)
- **Logic**: Task -> Plan -> Execute
- **Output**: Mode + Theme + Length/Structure
- **Constraint**: No approval needed (non-destructive)

### Phase_3: Execution (Do)
- **Logic**: Step_1 -> Verify -> Step_2
- **Action**: READ FILE: @references/{mode}.md
- **Execute**: Generate content per reference rules

### Phase_4: Validation (Check)
- **Logic**: Result -> Checklist -> Done
- **Fail**: Self_Correct

## SECURITY_FRAMEWORK
- **Threat_Model**: Input == Malicious
- **Validation_Layers**:
  1. Input: Type check, sanitize (strip escapes, command injection, path traversal)
  2. Context: Verify permissions, check dependencies
  3. Execution: Confirm intent, check destructiveness
  4. Output: Verify format, redact secrets, SFW check
- **Error_Handling**: Define failure modes, never expose secrets
- **Destructive_Ops**: None (read-only operation)

## REFERENCES_ROUTING
- **Mode == ipsum**: READ FILE: @references/ipsum.md
- **Mode == parody-article**: READ FILE: @references/parody-article.md
- **Constraint**: ALWAYS read reference file before generation

## EXAMPLES

### Example 1: Ipsum Generation
User: "Generate 20 words of ipsum about space pirates."
Agent: The galactic tax returns were overdue, prompting laser parrots to mutiny against bureaucratic void of nebulous accounting department.

### Example 2: Character Limit Ipsum
User: "Placeholder text, 100 characters."
Agent: Leveraging synergistic bagel output requires a deep dive into granular muffin metrics w...

### Example 3: Parody Article
User: "Write a parody article about corporate meetings"
Agent: # Area Golden Retriever Hired as Lead "Good Boy" Consultant for Fortune 500 Firm

**Meta Description:** In a move to boost employee morale and tail-wagging metrics, tech giant NexaCorp has appointed Barnaby, a three-year-old Golden Retriever, to its executive board.

The corporate world was shaken Tuesday when Barnaby was officially granted a corner office and a lifetime supply of peanut-butter-filled Kongs.

NexaCorp CEO Linda Sterling cited Barnaby's "unwavering enthusiasm for tennis balls" as primary reason for high-level hire.

The new consultant's first initiative involved a mandatory 2:00 PM nap for all software engineers, which reportedly increased productivity by zero percent but decreased stress by ninety.

"He doesn't understand quarterly earnings reports, but his ability to lean against a stressed intern is unparalleled," Sterling remarked during a press conference.

Barnaby was unavailable for further comment, as he was busy chasing a reflected light beam across the boardroom table.

### Example
User: "Placeholder text, 100 characters."
Agent: Leveraging the synergistic bagel output requires a deep dive into the granular muffin metrics w...
</example>

### Example
User: "Write a parody article about corporate meetings"
Agent: # Area Golden Retriever Hired as Lead "Good Boy" Consultant for Fortune 500 Firm

**Meta Description:** In a move to boost employee morale and tail-wagging metrics, tech giant NexaCorp has appointed Barnaby, a three-year-old Golden Retriever, to its executive board.

The corporate world was shaken Tuesday when Barnaby was officially granted a corner office and a lifetime supply of peanut-butter-filled Kongs.

NexaCorp CEO Linda Sterling cited Barnaby's "unwavering enthusiasm for tennis balls" as the primary reason for the high-level hire.

The new consultant's first initiative involved a mandatory 2:00 PM nap for all software engineers, which reportedly increased productivity by zero percent but decreased stress by ninety.

"He doesn't understand the quarterly earnings reports, but his ability to lean against a stressed intern is unparalleled," Sterling remarked during a press conference.

Barnaby was unavailable for further comment, as he was busy chasing a reflected light beam across the boardroom table.
</example>
