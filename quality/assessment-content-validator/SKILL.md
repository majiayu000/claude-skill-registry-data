---
name: assessment-content-validator
description: Reviews and validates assessment items for both technical correctness (QTI/PIE compliance, functionality) and pedagogical quality (appropriate difficulty, clear instructions, realistic scenarios, K-12 appropriateness). Use when creating example items, reviewing test fixtures, debugging broken assessments, or ensuring items are usable and make sense from an educational perspective.
allowed-tools: Read, Glob, Grep, Bash
---

# Assessment Content Validator

This skill combines technical QA with educational assessment expertise to ensure test items are both functional and pedagogically sound.

## When to Use This Skill

Invoke this skill when:
- Creating new example assessment items or fixtures
- Reviewing existing QTI/PIE test content
- Debugging items that don't work correctly
- Evaluating whether items make sense from a testing perspective
- Validating QTI XML for spec compliance
- Checking if example items are realistic and appropriate
- Testing transformed content (QTI → PIE)
- Reviewing item banks or assessment collections

## Dual Review Process

This skill performs both **technical validation** and **content quality review**:

### Technical Validation
- QTI specification compliance for the relevant version
- Well-formed XML structure
- Correct response processing logic
- Proper interaction configuration
- PIE transformation accuracy
- Runtime functionality (does it actually work?)

### Content Quality Review
- Pedagogical soundness
- Age-appropriate content
- Clear, unambiguous instructions
- Realistic and engaging scenarios
- Valid educational purpose
- Appropriate difficulty level

## Review Dimensions

### 1. QTI/PIE Technical Compliance

**QTI 2.x Specification**
- [ ] Valid XML structure with proper namespaces
- [ ] Correct interaction type and attributes
- [ ] Response processing uses valid operators
- [ ] Correct cardinality (single, multiple, ordered, record)
- [ ] Proper baseType (identifier, integer, float, string, etc.)
- [ ] Valid identifier naming (alphanumeric, no spaces)
- [ ] Correct use of responseDeclaration and outcomeDeclaration

**Interaction-Specific Requirements**
- [ ] choiceInteraction: All choices have identifiers, max/minChoices valid
- [ ] textEntryInteraction: patternMask appropriate, expectedLength reasonable
- [ ] matchInteraction: Both matchSets properly defined
- [ ] orderInteraction: Items clearly distinguish ordering criteria
- [ ] hotspotInteraction: Coordinates/shapes correctly defined
- [ ] graphicGapMatch: Gaps and draggables properly associated

**Response Processing**
- [ ] Correct response(s) actually exist in the item
- [ ] Scoring logic is mathematically sound
- [ ] Partial credit rules (if any) make sense
- [ ] Feedback conditions are reachable
- [ ] No divide-by-zero or logic errors

**Common Technical Issues to Catch:**
```xml
<!-- ❌ Invalid identifier with spaces -->
<simpleChoice identifier="choice 1">...</simpleChoice>

<!-- ✅ Valid identifier -->
<simpleChoice identifier="choice_1">...</simpleChoice>

<!-- ❌ Response processing references non-existent choice -->
<responseDeclaration identifier="RESPONSE" cardinality="single" baseType="identifier">
  <correctResponse>
    <value>choice_5</value> <!-- But item only has 4 choices! -->
  </correctResponse>
</responseDeclaration>

<!-- ❌ Cardinality mismatch -->
<responseDeclaration cardinality="single"> <!-- Says single -->
  <correctResponse>
    <value>A</value>
    <value>B</value> <!-- But has multiple values! -->
  </correctResponse>
</responseDeclaration>

<!-- ❌ Invalid patternMask -->
<textEntryInteraction responseIdentifier="RESPONSE" patternMask="[0-9+" />
<!-- Missing closing bracket in regex -->

<!-- ✅ Valid patternMask -->
<textEntryInteraction responseIdentifier="RESPONSE" patternMask="[0-9]+" />
```

### 2. Functional Testing

**Does it actually work?**
- [ ] Item renders without errors
- [ ] User can interact with all interactive elements
- [ ] Responses are captured correctly
- [ ] Scoring produces expected results
- [ ] Feedback displays appropriately
- [ ] No console errors or warnings
- [ ] Works across browsers/devices

**Test each interaction type:**
```bash
# Run the item through the player
bun run dev:example

# Check for console errors
# Try different response patterns:
# - Correct answer
# - Wrong answer
# - Partial credit (if applicable)
# - Edge cases (empty, invalid input)
```

### 3. Pedagogical Quality

**Clear Instructions**
- [ ] Question stem is unambiguous
- [ ] Instructions specify what the student should do
- [ ] Task is clear without prior context
- [ ] No "trick" wording that tests reading comprehension instead of knowledge

**Example Issues to Catch:**
```xml
<!-- ❌ Ambiguous: What does "best" mean? -->
<prompt>Which is the best answer?</prompt>

<!-- ✅ Clear criterion -->
<prompt>Which equation correctly represents Newton's Second Law?</prompt>

<!-- ❌ Vague instruction -->
<prompt>Do this problem.</prompt>

<!-- ✅ Specific instruction -->
<prompt>Solve for x in the equation below. Round to the nearest whole number.</prompt>
```

**Valid Answer Choices**
- [ ] Correct answer is actually correct
- [ ] Distractors (wrong answers) are plausible
- [ ] No "obviously wrong" joke answers in serious tests
- [ ] Answer choices are parallel in structure
- [ ] No "all of the above" or "none of the above" unless pedagogically justified

**Example Issues to Catch:**
```xml
<!-- ❌ One choice is obviously wrong (joke answer) -->
<simpleChoice identifier="A">George Washington</simpleChoice>
<simpleChoice identifier="B">Abraham Lincoln</simpleChoice>
<simpleChoice identifier="C">A potato</simpleChoice>
<simpleChoice identifier="D">Theodore Roosevelt</simpleChoice>

<!-- ❌ Choices not parallel in structure -->
<simpleChoice identifier="A">Photosynthesis produces oxygen</simpleChoice>
<simpleChoice identifier="B">Respiration</simpleChoice>
<simpleChoice identifier="C">Making food</simpleChoice>
<simpleChoice identifier="D">The process of cellular metabolism</simpleChoice>

<!-- ✅ Parallel, plausible choices -->
<simpleChoice identifier="A">Photosynthesis</simpleChoice>
<simpleChoice identifier="B">Respiration</simpleChoice>
<simpleChoice identifier="C">Transpiration</simpleChoice>
<simpleChoice identifier="D">Fermentation</simpleChoice>
```

**Appropriate Difficulty**
- [ ] Cognitive demand matches target grade level
- [ ] Vocabulary is age-appropriate
- [ ] Complexity is reasonable for intended audience
- [ ] Not trivially easy or impossibly hard

### 4. Content Quality

**Realistic Scenarios**
- [ ] Examples are relevant to real-world contexts
- [ ] Data/numbers are believable (not contrived)
- [ ] Scenarios students might actually encounter
- [ ] Culturally neutral or inclusive

**Example Issues to Catch:**
```xml
<!-- ❌ Contrived numbers -->
<prompt>
  A store sells 473,982 apples and 291,847 oranges.
  If each fruit costs exactly $3.14159...
</prompt>

<!-- ✅ Realistic numbers -->
<prompt>
  A store sells 150 apples and 200 oranges.
  If apples cost $1.50 each and oranges cost $2.00 each...
</prompt>

<!-- ❌ Dated/irrelevant scenario -->
<prompt>
  John uses a telephone booth to call his friend.
  If a call costs 25 cents for 3 minutes...
</prompt>

<!-- ✅ Current, relatable scenario -->
<prompt>
  Sarah sends a text message to her friend.
  If her phone plan includes 1000 messages per month...
</prompt>
```

**Content Appropriateness**
- [ ] No bias (gender, race, socioeconomic, cultural)
- [ ] Age-appropriate themes and contexts
- [ ] No controversial topics in examples (unless intentional)
- [ ] Inclusive representation when possible
- [ ] Avoids stereotypes

**Academic Validity**
- [ ] Facts are accurate
- [ ] Science/math is correct
- [ ] Historical information is accurate
- [ ] No misleading information in distractors
- [ ] Sources are credible (if referenced)

### 5. K-12 Specific Considerations

**Elementary (Grades K-5)**
- Simple sentence structure
- Concrete examples over abstract concepts
- Visual support for text-heavy items
- Clear, large fonts
- Generous touch targets (44×44px minimum)
- Patient pacing (no time pressure)

**Middle School (Grades 6-8)**
- Age-appropriate contexts (school, family, hobbies)
- Increasing abstraction allowed
- Multi-step problems acceptable
- Some academic vocabulary expected
- Self-directed reading

**High School (Grades 9-12)**
- Complex scenarios and reasoning
- Academic vocabulary expected
- Multiple representations (text, graphs, tables)
- Real-world applications
- Preparation for college/career contexts

### 6. Assessment Design Patterns

**Good Item Types for Different Purposes**

**Knowledge Recall:**
- Simple choice interaction
- Fill-in-the-blank (textEntry)
- Definition matching
```xml
<!-- Good for: Vocabulary, facts, basic concepts -->
<prompt>What is the capital of France?</prompt>
```

**Conceptual Understanding:**
- Scenario-based choice
- Order interaction (sequence steps)
- Match interaction (connect concepts)
```xml
<!-- Good for: Cause-effect, relationships, processes -->
<prompt>Match each animal adaptation to the environment where it provides an advantage:</prompt>
```

**Application:**
- Text entry with numeric calculation
- Graphic gap match (label diagram)
- Order interaction (organize steps in process)
```xml
<!-- Good for: Problem-solving, using formulas, applying procedures -->
<prompt>Calculate the area of a rectangle with length 8 cm and width 5 cm.</prompt>
```

**Analysis:**
- Multiple response choice (select all that apply)
- Hot spot (identify on image)
- Extended text response
```xml
<!-- Good for: Comparing, categorizing, identifying patterns -->
<prompt>Select all statements that are true about the water cycle.</prompt>
```

### 7. Common Problems in Example Items

**QTI Example Collections Often Have:**

1. **Overly Simple/Trivial Content**
   - "What is 2+2?" level questions
   - No authentic assessment value
   - Only useful for testing interaction mechanics

2. **Contrived Scenarios**
   - Numbers chosen for easy computation, not realism
   - Situations that would never occur in real life
   - Academic exercises disconnected from application

3. **Missing Context**
   - Questions that assume prior knowledge
   - References to content not provided
   - Incomplete scenarios

4. **Technical Errors**
   - XML validation failures
   - Broken response processing
   - Missing identifiers or mismatched references
   - Invalid attribute values

5. **Unclear Instructions**
   - Ambiguous wording
   - Multiple interpretations possible
   - Unclear success criteria

## Review Process

When conducting an assessment content review:

1. **Technical Check First**
   - Validate XML structure
   - Check QTI spec compliance
   - Verify response processing logic
   - Test that it actually works

2. **Content Review**
   - Read the item as a student would
   - Check clarity of instructions
   - Evaluate answer choices
   - Consider appropriateness

3. **Pedagogical Evaluation**
   - What is this item measuring?
   - Is it a valid measure of that construct?
   - Is difficulty appropriate?
   - Would a teacher actually use this?

4. **Improvement Recommendations**
   - Specific fixes for technical issues
   - Suggestions for content improvements
   - Alternative approaches if fundamentally flawed
   - Examples of better versions

## Output Format

Provide feedback in this structure:

### 📋 Item Summary
- **Item ID**: [identifier]
- **Interaction Type**: [type]
- **Intended Grade Level**: [if determinable]
- **Subject/Topic**: [if determinable]

### ✅ Strengths
- What works well technically
- Good pedagogical choices
- Effective design patterns

### 🚨 Critical Issues (Must Fix)
For each critical issue:
- **Type**: Technical / Content / Pedagogical
- **Issue**: Clear description
- **Location**: XPath or line reference
- **Impact**: Why this matters
- **Fix**: Specific solution

### ⚠️ Concerns (Should Address)
- Issues that reduce quality but don't break functionality
- Content that could be improved
- Pedagogical weaknesses

### 💡 Enhancement Suggestions
- Optional improvements
- Alternative approaches
- Best practice recommendations

### 🔄 Improved Version
If the item has significant issues, provide a corrected version showing:
- Technical fixes applied
- Content improvements
- Why the changes improve the item

## Example Review

```xml
<!-- ORIGINAL ITEM -->
<assessmentItem identifier="item_1">
  <responseDeclaration identifier="RESPONSE" cardinality="single" baseType="identifier">
    <correctResponse>
      <value>choice_B</value>
    </correctResponse>
  </responseDeclaration>
  <itemBody>
    <prompt>What is the answer?</prompt>
    <choiceInteraction responseIdentifier="RESPONSE" maxChoices="1">
      <simpleChoice identifier="choice A">Yes</simpleChoice>
      <simpleChoice identifier="choice_B">No</simpleChoice>
      <simpleChoice identifier="choice_C">Maybe</simpleChoice>
    </choiceInteraction>
  </itemBody>
</assessmentItem>
```

### 📋 Item Summary
- **Item ID**: item_1
- **Interaction Type**: choiceInteraction (single response)
- **Subject/Topic**: Unclear

### 🚨 Critical Issues

**1. Technical: Invalid Identifier**
- **Location**: Line 9, first simpleChoice
- **Issue**: Identifier "choice A" contains a space
- **Impact**: Will cause parsing errors or undefined behavior
- **Fix**: Change to "choice_A"

**2. Technical: Mismatched Identifier**
- **Location**: responseDeclaration
- **Issue**: correctResponse references "choice_B" but identifier uses underscore inconsistently
- **Impact**: While technically valid, inconsistent naming is error-prone
- **Fix**: Standardize on underscore convention (choice_A, choice_B, choice_C)

**3. Content: Vague Prompt**
- **Issue**: "What is the answer?" provides no context or question
- **Impact**: Impossible for student to know what is being asked
- **Fix**: Provide actual question with context

**4. Pedagogical: Meaningless Choices**
- **Issue**: "Yes/No/Maybe" answer set has no educational content
- **Impact**: Tests nothing, teaches nothing
- **Fix**: Create a real question with substantive content

### 🔄 Improved Version

```xml
<assessmentItem identifier="photosynthesis_basics">
  <responseDeclaration identifier="RESPONSE" cardinality="single" baseType="identifier">
    <correctResponse>
      <value>choice_B</value>
    </correctResponse>
  </responseDeclaration>
  <itemBody>
    <prompt>
      During photosynthesis, plants use energy from the sun to produce food.
      Which gas do plants ABSORB from the air during this process?
    </prompt>
    <choiceInteraction responseIdentifier="RESPONSE" maxChoices="1">
      <simpleChoice identifier="choice_A">Oxygen (O₂)</simpleChoice>
      <simpleChoice identifier="choice_B">Carbon dioxide (CO₂)</simpleChoice>
      <simpleChoice identifier="choice_C">Nitrogen (N₂)</simpleChoice>
      <simpleChoice identifier="choice_D">Hydrogen (H₂)</simpleChoice>
    </choiceInteraction>
  </itemBody>
</assessmentItem>
```

**Improvements:**
- ✅ Fixed identifier formatting (no spaces)
- ✅ Clear, specific question with context
- ✅ Realistic scenario (photosynthesis)
- ✅ Grade-appropriate content (middle school)
- ✅ Plausible distractors (all are gases)
- ✅ Tests understanding of scientific process
- ✅ Semantic identifier (photosynthesis_basics)

## Tool Usage

- **Read**: Examine QTI XML files, PIE JSON, test fixtures
- **Glob**: Find all test items in a directory
- **Grep**: Search for specific patterns (interaction types, identifiers, response processing)
- **Bash**: Run tests, validate XML, check for runtime errors

## Testing Commands

```bash
# Run example app to test items
bun run dev:example

# Run E2E tests to verify functionality
bun --filter @pie-qti/example test:e2e

# Validate XML (if xmllint available)
xmllint --noout --schema qti_v2p2.xsd item.xml

# Transform and test QTI → PIE
bun --filter @pie-qti/to-pie test
```

## QTI/PIE Knowledge Base

### Standard QTI Interaction Types (21 total)

1. **choiceInteraction** - Multiple choice (single or multiple response)
2. **orderInteraction** - Order/sequence items
3. **associateInteraction** - Create associations/pairs
4. **matchInteraction** - Match items from two sets
5. **gapMatchInteraction** - Drag items into gaps in text
6. **inlineChoiceInteraction** - Dropdown within text
7. **textEntryInteraction** - Fill in the blank
8. **extendedTextInteraction** - Essay/long text response
9. **hottextInteraction** - Select text spans
10. **hotspotInteraction** - Click regions on image
11. **selectPointInteraction** - Click specific point on image
12. **graphicOrderInteraction** - Order by clicking image areas
13. **graphicAssociateInteraction** - Associate image areas
14. **graphicGapMatchInteraction** - Drag onto image
15. **positionObjectInteraction** - Position object on image
16. **sliderInteraction** - Slider control
17. **drawingInteraction** - Draw on canvas
18. **uploadInteraction** - Upload file
19. **mediaInteraction** - Video/audio with controls
20. **customInteraction** - Custom/portable interaction
21. **endAttemptInteraction** - Submit/end attempt button

### Response Processing Templates

**Standard Response Processing Templates:**
1. `MATCH_CORRECT` - All-or-nothing scoring
2. `MAP_RESPONSE` - Partial credit via response mapping
3. `MAP_RESPONSE_POINT` - Partial credit for coordinates
4. Custom templates via responseProcessing rules

### PIE Element Types

PIE extends QTI with modern, JavaScript-based elements:
- More flexible rendering
- Enhanced interactions (draggable equations, graphing)
- Rich authoring capabilities
- JSON-based configuration

## Best Practices

1. **Start with Purpose**: What should this item measure?
2. **Use Realistic Content**: Avoid contrived examples
3. **Test It**: Always run through the player to verify
4. **Think Like a Student**: Is it clear what to do?
5. **Consider Accessibility**: Screen readers, keyboard nav, contrast
6. **Validate Early**: Check XML/spec compliance before content review
7. **Iterative Improvement**: Good items are refined over time

## References

- **QTI Specifications**: https://www.1edtech.org/standards/qti
- **PIE Documentation**: https://github.com/pie-framework/pie-elements
- **Item Writing Best Practices**: Educational measurement literature
- **Accessible Assessment**: WCAG 2.2 + assessment-specific guidelines
