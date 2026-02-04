---
name: strategic-plays
description: Identify strategic options and gameplay patterns from Wardley Maps
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Strategic Plays Skill

Identify strategic options and gameplay patterns from Wardley Maps for competitive advantage.

## When to Use This Skill

Use this skill when:

- **Strategic Plays tasks** - Working on identify strategic options and gameplay patterns from wardley maps
- **Planning or design** - Need guidance on Strategic Plays approaches
- **Best practices** - Want to follow established patterns and standards

## MANDATORY: Documentation-First Approach

Before identifying strategic plays:

1. **Invoke `docs-management` skill** for strategic patterns
2. **Verify Wardley gameplay** via MCP servers (perplexity)
3. **Base guidance on Simon Wardley's gameplays catalog**

## Strategic Play Categories

```text
Wardley's Gameplay Categories:

USER PERCEPTION PLAYS
├── Education
├── Lobbying
├── Marketing
└── Fear, Uncertainty, Doubt (FUD)

ACCELERATOR PLAYS
├── Open Approaches
├── Exploiting Network Effects
├── Standards Game
└── Industrialization

DEACCELERATOR PLAYS
├── Creating Artificial Constraints
├── Exploiting IPR
├── Slowing Evolution
└── Raising Barriers

MARKET PLAYS
├── Two-Factor Markets
├── Ecosystem Model
├── Tower and Moat
└── Channel Conflict

DEFENSIVE PLAYS
├── Signal Distortion
├── Threat Acquisition
├── Embracing Competition
└── Fragmentation

ATTACKING PLAYS
├── ILC (Innovate-Leverage-Commoditize)
├── Fool's Mate
├── Pig in a Poke
└── Misdirection

ECOSYSTEM PLAYS
├── Co-option
├── Sensing Engines
├── Center of Gravity
└── Land and Expand
```

## Key Strategic Plays

### ILC (Innovate-Leverage-Commoditize)

```text
ILC Pattern:

1. INNOVATE (Genesis)
   - Create new capability
   - Build expertise
   - Accept high failure rate
   - Focus on learning

2. LEVERAGE (Custom → Product)
   - Take successful innovations
   - Build repeatable solutions
   - Capture market share
   - Establish position

3. COMMODITIZE (Product → Utility)
   - Industrialize at scale
   - Drive costs down
   - Enable new innovations
   - Create ecosystem lock-in

Example: AWS
- Innovate: Internal cloud infrastructure
- Leverage: EC2, S3 products
- Commoditize: Utility computing model
```

### Open Approaches

```text
Open Source/Open Standards Strategy:

WHEN TO USE:
- Component is in Product/Commodity stage
- Competitor has dominant position
- Need to accelerate commoditization
- Want to shift competition elsewhere

MECHANISMS:
- Release IP to commoditize competitor advantage
- Build ecosystem around open standard
- Shift competition to higher-order systems
- Reduce costs through community contribution

RISKS:
- Loss of direct control
- Competitor adoption/contribution
- Community governance challenges
- Forking potential

EXAMPLES:
- Google releasing Kubernetes (commoditized orchestration)
- Facebook releasing React (commoditized UI frameworks)
- Microsoft embracing Linux (shifted competition)
```

### Two-Factor Markets

```text
Two-Factor Market Pattern:

STRUCTURE:
┌─────────────────┐
│  Platform/Hub   │
├─────────────────┤
│ Side A: Users   │◄──────────┐
│ (often free)    │           │
├─────────────────┤    Value  │
│ Side B: Payers  │───────────┘
│ (monetized)     │
└─────────────────┘

CHARACTERISTICS:
- One side subsidized
- Network effects between sides
- Winner-take-most dynamics
- High barriers once established

EXAMPLES:
- Google: Users (free) + Advertisers (pay)
- LinkedIn: Basic users + Recruiters/Premium
- Android: Users + App developers + Advertisers

EXECUTION:
1. Identify which side to subsidize
2. Build critical mass on free side
3. Monetize other side
4. Defend with network effects
```

### Ecosystem Plays

```text
Ecosystem Strategy:

COMPONENTS:
┌─────────────────────────────────────┐
│           YOUR PLATFORM            │
├─────────────┬─────────────┬────────┤
│  Partners   │  Developers │ Users  │
├─────────────┴─────────────┴────────┤
│         Complementors              │
└─────────────────────────────────────┘

BUILDING ECOSYSTEM:
1. Identify anchor components (your moat)
2. Enable complementors (APIs, SDKs)
3. Attract partners (mutual value)
4. Foster developer community
5. Create switching costs through integration

ECOSYSTEM DEFENSE:
- Continuously innovate anchor
- Maintain platform control
- Manage partner relationships
- Invest in developer experience
- Monitor for disintermediation
```

### Tower and Moat

```text
Tower and Moat Strategy:

THE TOWER (Genesis/Custom):
- High-value innovation
- Difficult to replicate
- Differentiating capability
- Your competitive advantage

THE MOAT (Product/Commodity):
- Surrounds and protects tower
- Creates switching costs
- Locks in customers
- Makes tower access dependent on moat

BUILDING:
1. Identify your tower (unique value)
2. Commoditize adjacent components
3. Integrate tower with commoditized moat
4. Make tower accessible only through moat

EXAMPLES:
- Apple: Design (tower) + iOS ecosystem (moat)
- Tesla: AI/Software (tower) + Charging network (moat)
```

## Play Selection Framework

### Situational Assessment

```text
Questions Before Selecting Plays:

POSITION ANALYSIS:
□ Where are your components on the map?
□ Where are competitor components?
□ What is evolving fastest?
□ Where do you have advantage?

CAPABILITY ASSESSMENT:
□ What can you execute well?
□ What resources do you have?
□ What is your risk tolerance?
□ What is your time horizon?

MARKET CONTEXT:
□ Is the market growing or consolidating?
□ Are there regulatory pressures?
□ What are customer pain points?
□ What substitutes are emerging?
```

### Play-Position Matrix

| Your Position | Market Position | Recommended Plays |
|---------------|-----------------|-------------------|
| Genesis leader | Early market | ILC, Ecosystem, Tower |
| Custom strength | Growing market | Leverage, Standards, Open |
| Product parity | Mature market | Two-Factor, Channel, Moat |
| Commodity laggard | Consolidated market | Open (disrupt), FUD, Acquisition |

### Play Compatibility

```text
Plays That Work Together:
- ILC + Ecosystem: Industrialize then build ecosystem
- Open + Two-Factor: Open commoditizes, platform monetizes
- Standards + Ecosystem: Standard attracts, ecosystem locks
- Tower + Moat: Innovation protected by commoditization

Plays That Conflict:
- Open + IPR exploitation (contradictory)
- Standards + Fragmentation (undermines standard)
- Two-Factor + Raising Barriers (limits one side)
```

## Gameplay Analysis Template

```markdown
# Strategic Play Analysis: [Context]

## Current Situation

### Map Position
[Where you are on the evolution axis]

### Competitive Position
| Competitor | Position | Trajectory | Threat Level |
|------------|----------|------------|--------------|
| [Name] | [Stage] | [Direction] | High/Med/Low |

## Play Options

### Option 1: [Play Name]
**Description:** [What the play involves]

**Prerequisites:**
- [Required capability/position]

**Execution Steps:**
1. [Step]
2. [Step]
3. [Step]

**Expected Outcomes:**
- Short-term: [Impact]
- Long-term: [Impact]

**Risks:**
- [Risk and mitigation]

**Resource Requirements:**
- [What's needed]

### Option 2: [Play Name]
[Same structure]

## Recommendation

**Selected Play:** [Which play and why]

**Success Criteria:**
- [Measurable outcome]
- [Measurable outcome]

**Review Points:**
- [When to reassess]
```

## Anti-Patterns

```text
Strategic Mistakes to Avoid:

1. PLAYING IN THE WRONG STAGE
   - Genesis plays in Commodity space (wasted innovation)
   - Commodity plays in Genesis space (premature optimization)

2. IGNORING INERTIA
   - Assuming market will adopt without resistance
   - Underestimating competitor response

3. SINGLE PLAY DEPENDENCE
   - Betting everything on one approach
   - No fallback if play fails

4. MISREADING EVOLUTION
   - Thinking you can stop evolution
   - Fighting inevitable commoditization

5. ECOSYSTEM HUBRIS
   - Assuming you'll be the center
   - Underestimating partner leverage

6. OPEN WASHING
   - Claiming open but maintaining control
   - Community will recognize and resist
```

## Doctrine Application to Plays

```text
Doctrine Principles Affecting Plays:

FOCUS: Pick plays that align with purpose
KNOW YOUR USERS: Ensure plays serve real needs
USE APPROPRIATE METHODS: Match play to component stage
THINK SMALL: Start with minimal viable plays
MANAGE INERTIA: Account for resistance in play design
USE COMMON LANGUAGE: Map is the common language for plays
CHALLENGE ASSUMPTIONS: Test play assumptions early
```

## Workflow

When identifying strategic plays:

1. **Map Current State**: Complete Wardley Map first
2. **Assess Position**: Where are you strong/weak?
3. **Identify Options**: What plays are available?
4. **Evaluate Fit**: Which plays match your situation?
5. **Check Compatibility**: Do selected plays work together?
6. **Plan Execution**: Detailed steps and timelines
7. **Define Success Criteria**: How will you measure?
8. **Plan Reassessment**: When to review and adjust?

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
