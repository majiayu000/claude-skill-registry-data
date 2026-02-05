---
name: concept-designer
description: Design software concepts using Daniel Jackson's methodology. This skill should be used when analyzing existing applications to identify concepts, designing new concepts for features or systems, defining concept structure (purpose, operational principles, state, actions), or composing multiple concepts together. Handles queries like "design a concept for X", "what concepts does this app have", "help me model this feature as a concept".
---

# Concept Designer

## Overview

Apply Daniel Jackson's concept design methodology to analyze software, identify reusable concepts, and design new concepts with clear purpose, operational principles, state, and actions. Based on "The Essence of Software" - https://essenceofsoftware.com/

## What is a Concept?

A **concept** is a reusable unit of functionality that can be understood independently:
- **Purpose**: What problem it solves (one clear sentence)
- **Operational Principle (OP)**: "If [user action], then [valuable result]"
- **State**: What data it maintains
- **Actions**: What operations it provides

**Example - Upvote concept:**
- Purpose: Let users collectively rank content by quality
- Principle: If you upvote good content and downvote bad content, then popular items will rise to the top
- State: Items, votes per item, user voting history
- Actions: upvote(), downvote(), getScore()

## Workflow Decision Tree

**Choose the appropriate workflow based on the user's request:**

1. **"What concepts does [app] have?"** → Use Analysis Workflow
2. **"Design a concept for [feature]"** → Use Design Workflow
3. **"How do these concepts work together?"** → Use Composition Workflow
4. **"Is this concept definition good?"** → Refer to concept-critic skill
5. **"How can I improve this concept?"** → Refer to concept-refactor skill

## Analysis Workflow

When analyzing existing software to identify concepts:

### Step 1: Inventory User-Facing Functionality
- List all features users directly interact with
- Focus on semantic functionality, not UI elements
- Group related actions that might belong together

### Step 2: Identify Candidate Concepts
For each functional group, ask:
- Does this solve a specific problem users have?
- Can users understand this without knowing other features?
- Does this appear in other applications?
- Does it have associated behavior (not just data)?

### Step 3: Define Each Concept
Use the template from `references/concept-templates.md`:
```
concept ConceptName [GenericTypes]
  purpose: [one sentence describing what problem this solves]
  principle:
    [if user does X, then system provides Y value]
  state:
    [key data structures and relationships]
  actions:
    [main operations users can perform]
```

### Step 4: Validate Against Criteria
Check each concept against the 8 criteria in `references/concept-criteria.md`:
- User-facing, Semantic, Independent, Behavioral, Purposive, End-to-end, Familiar, Reusable

### Step 5: Map Relationships
- Identify how concepts share data types (generic parameters)
- Note where concepts need synchronization
- See `references/concept-composition.md` for details

## Design Workflow

When designing new concepts for features or systems:

### Step 1: Define the Problem
- What user need are you addressing?
- What real-world pattern does this match?
- Have you seen similar functionality elsewhere?

### Step 2: Write the Purpose
One clear sentence answering: "What problem does this solve?"

**Good examples:**
- "Let users collectively rank content by quality" (Upvote)
- "Enable categorization and discovery of content" (Tag)
- "Let users see content from preferred users" (Follow)

**Bad examples:**
- "Manage user interactions" (too vague)
- "Store data and process requests" (implementation detail)

### Step 3: Write the Operational Principle
Template: "If [specific user action], then [valuable system response]"

**Good examples:**
- "If you tag content with keywords, then you can find related items by searching those tags"
- "If you follow someone, then their new content appears in your feed"

**Bad examples:**
- "If you use the system, good things happen" (not specific)
- "The system automatically does X" (missing user action)

See `references/operational-principles.md` for detailed guidance on writing compelling OPs.

### Step 4: Model State and Actions
- **State**: Minimum data structures needed to fulfill the purpose
- **Actions**: Essential operations only (avoid implementation details)
- Make concepts generic where possible (use type parameters)

### Step 5: Validate the Design
Use the checklist from `references/concept-templates.md`:
- [ ] Can users understand this concept independently?
- [ ] Does it solve one clear problem?
- [ ] Is the operational principle compelling and specific?
- [ ] Does it align with real-world patterns?
- [ ] Is it reusable across contexts?

## Composition Workflow

When working with multiple concepts that need to interact:

### Step 1: Keep Concepts Independent
Each concept should be understandable without referring to others. Use generic types for shared data.

**Example:**
```
concept Comment [Item]  // polymorphic over any Item type
concept Upvote [Item]   // works with posts, comments, anything
```

### Step 2: Define Synchronizations
Synchronizations coordinate concepts without creating dependencies.

**Example:** "When user creates a Post, automatically create an associated Upvote counter"

See `references/concept-composition.md` for detailed patterns.

### Step 3: Avoid Tight Coupling
- Don't make concepts depend on specific implementations of other concepts
- Use synchronization points, not direct dependencies
- Preserve each concept's ability to work alone

## Common Concept Patterns

Reference these common concepts when designing:

**Authentication & Access:**
- Account, Session, Password, Role

**Content & Social:**
- Post, Comment, Upvote, Follow, Tag

**Organization:**
- Folder, Search, Bookmark, Filter

**Communication:**
- Message, Notification, Mention

See `references/concept-templates.md` for complete definitions.

## Key Principles

1. **Software = Concepts**: Any app is a collection of interacting concepts
2. **Reuse Familiar Concepts**: Users learn faster when concepts match mental models
3. **One Purpose Per Concept**: If serving multiple purposes, consider splitting
4. **Focus on Behavior**: Concepts are about what users can do, not technical implementation
5. **Independence Enables Reusability**: Keep concepts self-contained for maximum flexibility

## Resources

### references/

This skill includes detailed reference documentation that Claude can load as needed:

- `concept-templates.md` - Complete templates, examples, checklists, anti-patterns
- `concept-criteria.md` - The 8 criteria for validating concepts (user-facing, semantic, independent, behavioral, purposive, end-to-end, familiar, reusable)
- `operational-principles.md` - Detailed guide on writing effective "if...then" scenarios
- `concept-composition.md` - How concepts work together through synchronization
- `concept-state-modeling.md` - Formal state machine modeling (for advanced use)

Load these references when:
- Need detailed validation criteria
- Writing operational principles
- Modeling complex state
- Composing multiple concepts

**Note:** These files are detailed (10k+ words total). Load selectively based on the specific task to manage context efficiently.
