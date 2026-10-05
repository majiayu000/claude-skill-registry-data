---
name: initializing-ledger
description: Use when starting a new product development project that needs traceable evidence and explicit decisions. Creates workspace structure from a project brief.
context: fork
agent: general-purpose
---

# Ledger Initialization

This skill creates a complete Context Ledger workspace from a project brief.

## Prerequisites

- User must provide a project brief (text description of what they're building)
- Optionally: custom path for ledger workspace (default: `./ledger/`)

## Workflow

Use TodoWrite to track these mandatory steps:

<required>
1. Parse the brief into structured components
2. Validate brief completeness (goals, constraints identifiable)
3. Create directory structure
4. Generate BRIEF.md
5. Generate PILLARS.md with default configuration
6. Confirm initialization complete
</required>

### Step 1: Parse the Brief

<good-example>
**Brief:** "Build a task management app for remote teams that integrates with Slack"
- Clear problem domain (task management)
- Specific target audience (remote teams)
- Key constraint (Slack integration)
- Can generate pillar questions immediately
</good-example>

<bad-example>
**Brief:** "Make an app"
- No problem domain specified
- No target audience
- No constraints or goals
- Cannot generate meaningful pillar questions
</bad-example>

Extract from the user's input:

| Component | Description | Required |
|-----------|-------------|----------|
| **Core idea** | What is being built (1-2 sentences) | Yes |
| **Target users** | Who will use this | Yes |
| **Key goals** | What success looks like | Yes |
| **Constraints** | What's explicitly out of scope | Recommended |
| **Context** | Any domain-specific information | Optional |

If the brief is too vague, use AskUserQuestion to clarify:

```
Question: "Your brief mentions [X] but I need more clarity on [Y]. Can you specify?"
Options:
- "[Interpretation A]"
- "[Interpretation B]"
- "Let me provide more detail"
```

### Step 2: Validate Brief Completeness

Check that the brief supports downstream work:

| Check | Pass Criteria |
|-------|---------------|
| Scope clarity | Can identify what's in/out |
| User clarity | Can describe target users |
| Goal measurability | At least one goal is falsifiable |
| Constraint presence | At least one constraint stated |

If validation fails, prompt for missing information before proceeding.

### Step 3: Create Directory Structure

Create the full ledger workspace. See [references/pillar-definitions.md](references/pillar-definitions.md) for pillar details.

```bash
mkdir -p ledger/{00-brief,01-pillars}
mkdir -p ledger/02-evidence/{market,users,tech,competitors,design,legal,ops,economics}
mkdir -p ledger/{03-synthesis,04-decisions,05-risks,06-prd,07-architecture,08-plan,09-brand,10-gtm-ops}
```

### Step 4: Generate BRIEF.md

Write the parsed brief to `00-brief/BRIEF.md` using the template in [references/brief-template.md](references/brief-template.md).

**Critical constraints:**
- Maximum 5 sentences for core description
- Goals must be specific and measurable where possible
- Constraints must be explicit exclusions, not vague limitations

### Step 5: Generate PILLARS.md

Create `01-pillars/PILLARS.md` with:

1. List of all 8 pillars (see [references/pillar-definitions.md](references/pillar-definitions.md))
2. Priority ranking based on brief analysis
3. Any pillar-specific scope notes

**Priority assignment logic:**
- If brief mentions market/pricing → Market pillar = high
- If brief mentions specific users → Users pillar = high
- If brief mentions technical constraints → Tech pillar = high
- If brief mentions competitors → Competitors pillar = high
- Default: all pillars medium priority

### Step 6: Confirm Initialization

Output summary:
- Workspace path
- Brief summary (2-3 sentences)
- Pillar priorities
- Next command to run (`/ledger-research`)

## User Interaction

Use the **AskUserQuestion tool** when:

### Brief is ambiguous
```
Question: "Your brief could be interpreted multiple ways. Which is closest?"
Options:
- "[Interpretation A focused on X]"
- "[Interpretation B focused on Y]"
- "Neither - let me clarify"
```

### Missing critical information
```
Question: "I couldn't identify [goals/constraints/users] from your brief. Can you specify?"
Options:
- "[Suggest likely answer based on context]"
- "[Alternative suggestion]"
- "Let me provide this information"
```

### Pillar prioritization unclear
```
Question: "Based on your brief, which areas are most critical to research first?"
Options:
- "Market + Users (demand validation focus)"
- "Tech + Competitors (feasibility focus)"
- "All equally important"
- "Let me specify priorities"
```

### Custom workspace path needed
```
Question: "Where should I create the ledger workspace?"
Options:
- "./ledger/ (current directory)" (Recommended)
- "~/projects/[project-name]/ledger/"
- "Let me specify a path"
```

## Output

After successful initialization:

```markdown
## Ledger Initialized

**Path:** ./ledger/
**Brief:** [2-3 sentence summary]

**Pillar Priorities:**
1. [High priority pillars]
2. [Medium priority pillars]
3. [Lower priority pillars]

**Next step:** Run `/ledger-research` to begin evidence collection.
```

## References

- [references/brief-template.md](references/brief-template.md) - BRIEF.md template
- [references/pillar-definitions.md](references/pillar-definitions.md) - Pillar definitions and scope
