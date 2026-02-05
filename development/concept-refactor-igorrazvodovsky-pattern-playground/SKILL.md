---
name: concept-refactor
description: Refine concept designs using six transformational moves. This skill should be used when improving existing concepts, addressing design trade-offs, or deciding between split/merge, unify/specialise, tighten/loosen approaches. Handles queries like "should I split this concept", "how to make concepts more flexible", "improve this concept design", "add more automation to concepts", "make concepts more general".
---

# Concept Refactor

## Overview

Apply six transformational moves to refine concept designs, trading off between flexibility vs simplicity, generality vs specificity, and automation vs independent control. Use these moves to systematically improve concepts after initial design.

## When to Use This Skill

Use concept-refactor when:
- Concepts feel too rigid or too complex
- Users need more control or want more automation
- Design requires more generality or more specialization
- Multiple related concepts could be simplified
- Single concept is serving too many purposes

## The Six Moves: Three Dual Pairs

Each move transforms concepts to improve specific design qualities, often at the cost of others:

### A. Split ↔ Merge (Flexibility vs Simplicity)

**Split**: Break one concept into multiple independent concepts
- **Use when**: Users need separate control over sub-functions
- **Example**: Split Photocopy → Print + Scan
- **Gain**: Flexibility, independent variation
- **Cost**: More concepts to learn and coordinate

**Merge**: Combine multiple concepts into one
- **Use when**: Speed and ease matter more than customization
- **Example**: Merge Flashlight + Battery + Charger → EmergencyFlashlight
- **Gain**: Simplicity, tight integration
- **Cost**: Less flexibility, harder to vary independently

### B. Unify ↔ Specialise (Generality vs Specificity)

**Unify**: Replace specialized concepts with one general-purpose concept
- **Use when**: Variants share key actions and state
- **Example**: Combine MailingList + AdminGroup → List
- **Gain**: Generality, fewer concepts
- **Cost**: May lose optimization for specific use cases

**Specialise**: Split general concept into narrower, optimized concepts
- **Use when**: Different variants serve meaningfully different scenarios
- **Example**: Lightroom's Rating, Flag, ColorLabel (instead of generic Marker)
- **Gain**: Optimized for specific workflows
- **Cost**: More concepts, less transferability

### C. Tighten ↔ Loosen (Automation vs Independent Control)

**Tighten**: Increase synchronization between concepts
- **Use when**: Strong coupling prevents user errors
- **Example**: Airplane toilet light always on when locked
- **Gain**: Automation, error prevention
- **Cost**: Less flexibility in sequencing actions

**Loosen**: Reduce synchronization for independent operation
- **Use when**: Users need flexibility in sequencing actions
- **Example**: ProCamera lets focus point differ from exposure point
- **Gain**: User control, flexibility
- **Cost**: More decisions, potential for errors

## Move Selection Workflow

### Step 1: Understand Current Design Context

Before applying a move:

1. **Inventory existing concepts**
   - List each concept's name, purpose, and operational principle
   - Verify each meets criteria (user-facing, independent, complete, specific)

2. **Map relationships**
   - Use dependency diagram to see what requires what
   - Identify possible subsets of the app
   - Note where complexity, redundancy, or inflexibility exists

3. **Pinpoint the problem or opportunity**
   - Trying to simplify user experience?
   - Need to add flexibility?
   - Want more generality or specificity?
   - Need more automation or user control?

### Step 2: Choose the Appropriate Move

Match your design goal to the move's trade-off:

**Problem: Concepts feel inflexible or blocking variation**
→ Consider **Split** or **Loosen**

**Problem: Too many concepts, overwhelming users**
→ Consider **Merge** or **Unify**

**Problem: Concept too specific, not reusable**
→ Consider **Unify**

**Problem: Concept too general, inefficient for specific uses**
→ Consider **Specialise**

**Problem: Users make errors coordinating concepts**
→ Consider **Tighten**

**Problem: Automation causing friction or misfires**
→ Consider **Loosen**

### Step 3: Apply the Move

For each type of move:

#### Applying Split/Merge/Unify/Specialise

1. **Identify candidate concepts**
   - Use OPs and state to locate overlap or coupling
   - Look for "piggybacking" (unrelated functions in one concept)

2. **Refactor concepts**
   - Rewrite purpose and OP for each resulting concept
   - Ensure each has single, clear purpose

3. **Update state and actions**
   - Give each revised concept self-contained state
   - Align actions with new purpose
   - Make generic where possible (type parameters)

4. **Revise synchronizations**
   - Add/remove/modify syncs for new boundaries
   - Preserve each concept's independent behavior

#### Applying Tighten/Loosen

1. **Identify synchronization points**
   - Where do concepts currently coordinate?
   - Where could they coordinate?
   - What actions trigger actions in other concepts?

2. **Adjust synchronizations**
   - **Tighten**: Add new syncs that couple concept actions
   - **Loosen**: Remove existing syncs to decouple

3. **Update documentation**
   - Make sync changes explicit in definitions
   - Document new workflows enabled/prevented

### Step 4: Evaluate the Transformation

After applying a move, validate the result:

1. **Re-check concept criteria**
   - Specific? Complete? Independent?
   - User-facing? Familiar? Reusable?

2. **Assess trade-offs explicitly**
   - What was gained (flexibility, simplicity, generality, etc.)?
   - What was lost?
   - Is net effect aligned with design goals?

3. **Check compositional synergy**
   - Does new arrangement enable functionality neither concept could achieve alone?

4. **Test with operational principles**
   - Run through OPs to ensure each concept still fulfills its purpose clearly
   - Can you write compelling "if...then" for each concept?

## Common Refactoring Scenarios

### Scenario 1: Monolithic Concept

**Symptom**: One concept doing too much, multiple purposes
**Example**: "Editor" that handles formatting, spell-check, version control, collaboration

**Solution**: **Split**
- Separate into Document, SpellCheck, Version, Comment concepts
- Each with single, clear purpose
- Coordinate through synchronization

### Scenario 2: Concept Proliferation

**Symptom**: Too many similar concepts, users confused
**Example**: Tag, Category, Label, Marker all doing similar things

**Solution**: **Unify**
- Combine into single Tag concept with generic implementation
- Reduces cognitive load
- May lose specific optimizations (acceptable trade-off)

### Scenario 3: Overly Generic Concept

**Symptom**: Concept tries to serve all use cases, none optimally
**Example**: Generic "Marker" trying to serve ratings, flags, color codes

**Solution**: **Specialise**
- Split into Rating (numeric scores), Flag (binary selection), ColorLabel (visual grouping)
- Each optimized for specific workflow
- Worth the added complexity if workflows are distinct

### Scenario 4: Error-Prone Coordination

**Symptom**: Users frequently make mistakes coordinating concepts
**Example**: Light and Lock controls separate, users forget to turn off light

**Solution**: **Tighten**
- Synchronize: when Lock engaged, Light automatically on
- Reduces errors through automation
- Acceptable loss of independent control

### Scenario 5: Restrictive Automation

**Symptom**: Tight coupling prevents legitimate use cases
**Example**: Camera forces focus and exposure to same point

**Solution**: **Loosen**
- Decouple Focus and Exposure concepts
- Enable advanced workflows (focus foreground, expose for background)
- Worth added complexity for power users

## Decision Framework

Use this framework to systematically choose moves:

### 1. Identify the Core Issue

**Flexibility Problems**:
- Concepts too coupled → **Split** or **Loosen**
- Need more control → **Split** or **Loosen**

**Simplicity Problems**:
- Too many concepts → **Merge** or **Unify**
- Users overwhelmed → **Merge** or **Unify**

**Generality Problems**:
- Too specific/inflexible → **Unify**
- Poor reusability → **Unify**

**Specificity Problems**:
- Too generic/inefficient → **Specialise**
- Missing workflow optimizations → **Specialise**

**Automation Problems**:
- Users making errors → **Tighten**
- Need better coordination → **Tighten**

**Control Problems**:
- Automation too restrictive → **Loosen**
- Need flexibility → **Loosen**

### 2. Consider Context

**When users are novices**:
- Prefer **Merge**, **Unify**, **Tighten** (simpler, more automated)

**When users are experts**:
- Prefer **Split**, **Specialise**, **Loosen** (more control, optimization)

**When workflows vary greatly**:
- Prefer **Split**, **Specialise**, **Loosen** (flexibility)

**When workflows are predictable**:
- Prefer **Merge**, **Unify**, **Tighten** (simplicity, automation)

### 3. Accept Trade-Offs

Every move has costs:
- **Split/Loosen**: Gain flexibility, lose simplicity
- **Merge/Tighten**: Gain simplicity, lose flexibility
- **Unify**: Gain generality, lose optimization
- **Specialise**: Gain optimization, lose generality

Be explicit about which property you're optimizing for.

## Integration with Design Workflow

Apply concept moves at specific points:

**During concept identification**:
- Use moves to shape initial concept set before implementation

**During problem-solving**:
- When encountering UX or functional flaws, try a move instead of only tweaking UI

**During iteration**:
- Periodically review concept inventory for refactoring opportunities

**During documentation**:
- Note where moves were applied, why, and what trade-off was made
- Helps future designers understand rationale

## Resources

### references/

- `concept-moves.md` - Complete detailed guide on all six transformational moves with examples and application patterns

Load this reference when:
- Need detailed examples of each move
- Want to understand trade-offs deeply
- Looking for specific patterns and anti-patterns
- Planning complex refactoring

**Note:** The moves reference is comprehensive (~2k words). Load when you need detailed guidance beyond the workflow above.
