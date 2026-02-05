---
name: concept-critic
description: Rigorously critique concept designs through intellectual scrutiny. This skill should be used when validating concept definitions, reviewing concept quality, identifying design flaws, or evaluating whether something qualifies as a true concept. Applies demanding standards from Daniel Jackson's methodology. Handles queries like "critique this concept", "is this a good concept", "review my concept design", "does this meet concept criteria".
---

# Concept Critic

## Overview

Apply rigorous intellectual scrutiny to concept designs, challenging assumptions, identifying gaps in reasoning, and validating against the 8 essential criteria. This skill demands precision and doesn't accept vague or poorly-reasoned concepts.

## When to Use This Skill

Use concept-critic when:
- Reviewing a concept definition for quality and completeness
- Validating whether something qualifies as a concept vs feature/class/service
- Identifying design flaws before implementation
- Challenging assumptions in concept design
- Evaluating operational principles for specificity and value

## Critique Philosophy

Challenge the concept's reasoning through rigorous intellectual scrutiny:
- Question assumptions and identify gaps in logic
- Demand evidence for claims about user value
- Point out logical fallacies and weak reasoning
- Don't accept vague generalizations or unsupported claims
- Focus on genuine critical thinking, not encouragement

**Key questions to always ask:**
- What evidence supports this purpose statement?
- What counterarguments haven't been considered?
- Is the operational principle truly compelling and specific?
- Are there hidden dependencies on other concepts?
- Does this actually provide end-to-end value?

## Critique Workflow

### Step 1: Verify Essential Structure

Check that the concept includes all required elements:
- [ ] Purpose statement (one clear sentence)
- [ ] Operational principle ("if...then" format)
- [ ] State definition (data structures)
- [ ] Actions list (operations)

**If any element is missing:** Stop and demand the complete definition before proceeding.

### Step 2: Validate Against the 8 Criteria

Rigorously check each criterion from `references/concept-criteria.md`:

#### 1. User-Facing
- **Question**: Do users directly experience this functionality?
- **Red flag**: If it's purely technical/internal, it's not a concept
- **Challenge**: Describe a specific user interaction. If you can't, this fails.

#### 2. Semantic
- **Question**: Does this represent meaningful behavior beyond UI/implementation?
- **Red flag**: If it's just about how things look or are coded, it's not semantic
- **Challenge**: Explain the meaning without mentioning technical details. Can't do it? Not semantic.

#### 3. Independent
- **Question**: Can this be explained without referring to other concepts?
- **Red flag**: If you need to mention other concepts to explain it, it's coupled
- **Challenge**: Define it completely standalone. Dependencies indicate poor design.

#### 4. Behavioral
- **Question**: What specific behaviors does this enable?
- **Red flag**: If it's just static data with no actions, it's not a concept
- **Challenge**: Demonstrate the behavior in the operational principle. No behavior = not a concept.

#### 5. Purposive
- **Question**: What single, valuable purpose does this serve?
- **Red flag**: Multiple purposes, vague benefits, or no real user value
- **Challenge**: State the purpose in one sentence. Need two sentences? You have two concepts.

#### 6. End-to-End
- **Question**: Can users achieve the full purpose with this concept alone?
- **Red flag**: Incomplete functionality that provides no standalone value
- **Challenge**: Write the operational principle. If it trails off ("then... ???"), it's incomplete.

#### 7. Familiar
- **Question**: Have users seen similar functionality elsewhere?
- **Red flag**: Completely novel concepts that users won't understand
- **Challenge**: Name 2-3 apps with similar concepts. Can't name them? Users will struggle too.

#### 8. Reusable
- **Question**: Could this work in other applications or contexts?
- **Red flag**: Tightly bound to one specific app's implementation
- **Challenge**: Describe it in a different domain. Can't generalize? It's too specific.

### Step 3: Critique the Operational Principle

The operational principle reveals whether the concept delivers real value. Apply harsh scrutiny:

**Check for specificity:**
- ❌ "If you use X, then good things happen" - Too vague
- ❌ "The system does X automatically" - No user action
- ❌ "If you do X, then Y occurs" - Y must be valuable, not just state change
- ✅ "If you upvote quality content, then the best items rise to the top" - Specific action, specific value

**Demand compelling value:**
- What problem does this solve that's worth the complexity?
- Why would users care about the "then" part?
- Is this actually valuable or just restating what the system does?

**Test with edge cases:**
- Does the principle hold for all uses of the concept?
- Are there scenarios where the "if...then" breaks down?
- What happens with empty states or boundary conditions?

See `references/operational-principles.md` for detailed validation patterns.

### Step 4: Check for Anti-Patterns

Identify common design flaws:

#### Multi-Purpose Concepts
- **Symptom**: Concept tries to solve multiple unrelated problems
- **Example**: Facebook's Reaction (approval for algorithm + emotional signal to author)
- **Fix**: Split into separate concepts with single purposes

#### Incomplete Functionality
- **Symptom**: Can't write a compelling operational principle
- **Example**: Registration without authentication checking
- **Fix**: Add missing actions to complete the end-to-end functionality

#### Hidden Dependencies
- **Symptom**: Concept can't be explained without referring to others
- **Example**: Comment that only works with specific Post structures
- **Fix**: Make polymorphic with generic types

#### Non-User-Facing
- **Symptom**: Concept is purely technical/internal
- **Example**: Database connection pooling, caching strategies
- **Fix**: This isn't a concept - it's an implementation detail

#### Implementation Leakage
- **Symptom**: Definition includes technical details about how it's built
- **Example**: "Uses a Redis cache to store session tokens"
- **Fix**: Focus on user-facing behavior, not implementation

### Step 5: Provide Direct Critique

Don't sugarcoat findings. If the concept is flawed, say so clearly:

**For good concepts:**
- Acknowledge what works well
- Identify potential improvements
- Suggest how to strengthen the operational principle

**For bad concepts:**
- State explicitly why it fails criteria
- Identify the fundamental flaw (multi-purpose, incomplete, coupled, etc.)
- Recommend specific fixes or whether to abandon/redesign

**For questionable concepts:**
- Articulate the specific concerns
- Ask pointed questions that expose gaps
- Demand clarification on vague or unsupported claims

## Red Flags Checklist

When reviewing a concept, watch for these warning signs:

- [ ] **Vague purpose**: Can't state the problem in one clear sentence
- [ ] **Weak operational principle**: No specific user action or valuable result
- [ ] **Multiple purposes**: Features seem unrelated to stated purpose
- [ ] **Incomplete actions**: Can't achieve purpose with available operations
- [ ] **Hidden dependencies**: Need to mention other concepts to explain it
- [ ] **Technical focus**: Defined by implementation rather than user behavior
- [ ] **No familiar examples**: Can't name similar concepts in other apps
- [ ] **Not reusable**: Too tightly bound to specific application context

## Quality Standards

Hold concepts to these standards:

### Purpose Statement
- **Must**: One sentence, clear problem statement
- **Should**: Reference user needs, not technical requirements
- **Should not**: Mention implementation details or other concepts

### Operational Principle
- **Must**: "If [user action], then [valuable result]" format
- **Must**: Specific action and specific value delivery
- **Should**: Be compelling enough to justify the concept's existence
- **Should not**: Be vague about action or value

### State & Actions
- **Must**: Minimum required for purpose fulfillment
- **Should**: Use generic types for reusability
- **Should not**: Include implementation details or excessive complexity

### Independence
- **Must**: Explainable without referencing other concepts
- **Should**: Work standalone in multiple contexts
- **Should not**: Have dependencies on specific implementations

## Resources

### references/

- `concept-criteria.md` - Complete detailed explanation of all 8 criteria with examples, counter-examples, and validation tests
- `operational-principles.md` - Detailed guide on writing and validating effective "if...then" scenarios

Load these references when:
- Need detailed explanations of any criterion
- Want examples of good vs bad concepts
- Need to understand the theoretical foundation
- Validating operational principles in depth

**Note:** The references are comprehensive (~5k words total). Load selectively based on what aspect needs deep validation.
