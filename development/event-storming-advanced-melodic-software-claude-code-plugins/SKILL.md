---
name: event-storming-advanced
description: Deep dive Event Storming beyond big picture
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Event Storming Advanced Skill

## When to Use This Skill

Use this skill when:

- **Event Storming Advanced tasks** - Working on deep dive event storming beyond big picture
- **Planning or design** - Need guidance on Event Storming Advanced approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Conduct Event Storming sessions beyond big picture to process and design levels.

## MANDATORY: Documentation-First Approach

Before facilitating Event Storming:

1. **Invoke `docs-management` skill** for Event Storming patterns
2. **Verify methodology** via MCP servers (perplexity)
3. **Base guidance on Alberto Brandolini's methodology**

## Event Storming Levels

```text
Event Storming Progression:

LEVEL 1: BIG PICTURE
├── Purpose: Understand the whole domain
├── Participants: Everyone (business + tech)
├── Output: Domain overview, hotspots, bounded contexts
└── Duration: 2-4 hours

LEVEL 2: PROCESS LEVEL
├── Purpose: Detail specific business processes
├── Participants: Domain experts + analysts
├── Output: Detailed flows, policies, read models
└── Duration: 2-4 hours per process

LEVEL 3: DESIGN LEVEL
├── Purpose: Translate to software design
├── Participants: Developers + architects
├── Output: Aggregates, commands, event handlers
└── Duration: 2-4 hours per aggregate

LEVEL 4: SOFTWARE DESIGN
├── Purpose: Implementation details
├── Participants: Development team
├── Output: Code structure, APIs, schemas
└── Duration: Ongoing
```

## Sticky Note Colors

```text
Standard Event Storming Palette:

🟠 ORANGE: Domain Events
   - Things that happened
   - Past tense naming
   - Business-significant state changes

🟦 BLUE: Commands
   - User intentions
   - Imperative naming
   - May be rejected

🟨 YELLOW: Actors/Users
   - Who initiates commands
   - Personas or roles
   - External systems

🟪 PURPLE/PINK: Policies/Reactions
   - Business rules
   - "When X happens, we do Y"
   - Automated responses

🟩 GREEN: Read Models
   - Information needed
   - Views/screens
   - Query results

⬜ WHITE: External Systems
   - Third-party integrations
   - Legacy systems
   - APIs we don't control

🔴 RED/PINK: Hot Spots
   - Questions
   - Conflicts
   - Areas of uncertainty
```

## Big Picture Event Storming

### Purpose and Outcomes

```text
Big Picture Goals:
1. Create shared understanding
2. Discover bounded contexts
3. Identify hot spots and risks
4. Find key domain events
5. Align business and technical teams

What You Get:
- Timeline of domain events
- Bounded context candidates
- List of questions to answer
- Key actors and systems
- Critical business processes
```

### Facilitation Steps

```text
Big Picture Process:

STEP 1: CHAOTIC EXPLORATION (30 min)
- Everyone writes domain events
- No wrong answers
- Encourage wild ideas
- Cover the whole domain

STEP 2: TIMELINE ENFORCEMENT (30 min)
- Arrange events chronologically
- Left = earlier, right = later
- Find parallel flows
- Identify pivotal events

STEP 3: PIVOTAL EVENTS (20 min)
- Mark key moments (larger stickies)
- Business-critical transitions
- Points of no return
- Natural process boundaries

STEP 4: SWIMLANES (20 min)
- Group by actor or bounded context
- Identify handoffs
- Find integration points
- Note context boundaries

STEP 5: HOTSPOTS (20 min)
- Mark areas of confusion (red)
- Note missing information
- Flag conflicting views
- Capture open questions

STEP 6: BOUNDED CONTEXT SKETCH (20 min)
- Draw boundaries around related events
- Name the contexts
- Identify core vs supporting
- Note context relationships
```

## Process Level Event Storming

### Purpose and Depth

```text
Process Level Goals:
1. Detail one business process end-to-end
2. Identify all commands and events
3. Map policies and reactions
4. Define read models needed
5. Clarify business rules

Prerequisites:
- Big picture completed
- Process scope selected
- Domain experts available
- Questions from big picture
```

### Extended Notation

```text
Process Level Additions:

COMMANDS (Blue)
┌────────────────┐
│ CreateOrder    │
│ ─────────────  │
│ By: Customer   │
└────────────────┘

POLICIES (Purple) - aka Reactions
┌────────────────┐
│ ⚡ When order   │
│ placed, reserve│
│ inventory      │
└────────────────┘

READ MODELS (Green)
┌────────────────┐
│ 📖 Product     │
│ Catalog        │
│ (shows price,  │
│ availability)  │
└────────────────┘

AGGREGATE (Yellow border)
┏━━━━━━━━━━━━━━━━┓
┃ Order          ┃
┃ ┌────────────┐ ┃
┃ │ OrderPlaced│ ┃
┃ │ OrderPaid  │ ┃
┃ └────────────┘ ┃
┗━━━━━━━━━━━━━━━━┛
```

### Process Level Template

```markdown
# Process Level: [Process Name]

## Scope
[What this process covers, start and end points]

## Actors
- [Actor 1]: [Role description]
- [Actor 2]: [Role description]

## Process Flow

```text
[ASCII flow diagram]
```

## Commands

| Command | Actor | Event Produced | Preconditions |
|---------|-------|----------------|---------------|
| [Name] | [Who] | [Event] | [What must be true] |

## Events

| Event | Command/Policy | Downstream Effects |
|-------|----------------|-------------------|
| [Name] | [Trigger] | [What happens next] |

## Policies

| Policy | Trigger Event | Action | Produces |
|--------|---------------|--------|----------|
| [Name] | [When this] | [Do this] | [Events/Effects] |

## Read Models

| Read Model | Purpose | Populated By |
|------------|---------|--------------|
| [Name] | [What query] | [Events] |

## External Systems

| System | Integration Point | Direction |
|--------|-------------------|-----------|
| [Name] | [Where] | Inbound/Outbound |

## Hot Spots & Questions

- [ ] [Question needing resolution]
- [ ] [Uncertainty to investigate]

```text

```

## Design Level Event Storming

### Purpose and Artifacts

```text
Design Level Goals:
1. Define aggregate boundaries
2. Identify command handlers
3. Design event structure
4. Specify validation rules
5. Plan event sourcing strategy

Outputs:
- Aggregate definitions
- Command/event schemas
- Invariant specifications
- Consistency boundaries
```

### Aggregate Identification

```text
Aggregate Design Questions:

BOUNDARY IDENTIFICATION:
- What must be consistent together?
- What can be eventually consistent?
- What is the transaction boundary?

NAMING:
- What noun represents this cluster?
- Is it a domain concept?
- Does business recognize it?

INVARIANTS:
- What rules must always hold?
- What combinations are invalid?
- What constraints protect integrity?

LIFECYCLE:
- How is it created?
- How does it change?
- When is it complete/archived?
```

### Design Level Notation

```text
Aggregate Card:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ AGGREGATE: Order          ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Commands:                 ┃
┃ • PlaceOrder              ┃
┃ • AddItem                 ┃
┃ • RemoveItem              ┃
┃ • SubmitPayment           ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Events:                   ┃
┃ • OrderCreated            ┃
┃ • ItemAdded               ┃
┃ • ItemRemoved             ┃
┃ • OrderPaid               ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Invariants:               ┃
┃ • Total > 0               ┃
┃ • Items not empty         ┃
┃ • Status valid transition ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

## Bounded Context Discovery

### Context Mapping from Events

```text
Finding Bounded Contexts:

LINGUISTIC BOUNDARIES:
- Where does terminology change?
- Where are there synonyms/homonyms?
- Where do meanings differ?

OWNERSHIP BOUNDARIES:
- Who owns which events?
- Where do teams hand off?
- Which group decides?

LIFECYCLE BOUNDARIES:
- Different rates of change?
- Different deployment needs?
- Different data governance?

TECHNICAL BOUNDARIES:
- Different tech stacks?
- Different scalability needs?
- Different consistency needs?
```

### Context Relationship Patterns

```text
Context Relationships:

PARTNERSHIP
[Context A] ◄──► [Context B]
Tight collaboration, shared goals

CUSTOMER-SUPPLIER
[Customer] ◄── [Supplier]
Supplier serves customer needs

CONFORMIST
[Conformist] ──► [Upstream]
Downstream conforms to upstream

ANTI-CORRUPTION LAYER (ACL)
[Context] ──[ACL]──► [Legacy]
Translation layer protects domain

OPEN HOST SERVICE (OHS)
[Provider] ──[OHS]──► [Many Consumers]
Published API for integration

SHARED KERNEL
[Context A] ◄──[Shared]──► [Context B]
Small shared code/model (use sparingly)
```

## Workshop Facilitation

### Room Setup

```text
Physical Requirements:
- Long wall (8+ meters ideal)
- Plenty of sticky notes (all colors)
- Markers for everyone
- Tape or sticky wall
- Timer visible to all
- Refreshments available

Virtual Alternatives:
- Miro / Mural / FigJam
- Unlimited canvas
- Sticky note templates
- Timer integration
- Breakout rooms for parallel work
```

### Facilitation Tips

```text
Effective Facilitation:

DO:
✓ Keep energy high
✓ Enforce timeline direction
✓ Encourage questions
✓ Capture hot spots immediately
✓ Rotate facilitation if long session
✓ Take breaks every 90 minutes
✓ Photograph results frequently

DON'T:
✗ Let one person dominate
✗ Jump to solutions
✗ Ignore quiet participants
✗ Skip hot spot discussion
✗ Allow technology discussion too early
✗ Forget to capture decisions
```

## Workflow

When conducting Event Storming:

1. **Prepare**: Room, materials, participants, scope
2. **Big Picture**: Domain-wide event exploration
3. **Identify Hotspots**: Mark uncertainties and conflicts
4. **Find Boundaries**: Sketch bounded contexts
5. **Select Focus**: Choose process for deep dive
6. **Process Level**: Detail commands, policies, read models
7. **Design Level**: Define aggregates and invariants
8. **Document**: Capture results in structured format
9. **Iterate**: Refine based on implementation feedback

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
