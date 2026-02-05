---
name: oblique
description: This skill should be used when the user asks to "/oblique", "oblique strategy", "give me an oblique strategy", "give me a creative prompt", or wants lateral thinking inspiration for their coding session.
allowed-tools:
  - Bash
  - AskUserQuestion
---

# Oblique Strategies

Inspired by Brian Eno and Peter Schmidt's Oblique Strategies deck - a set of cards offering creative prompts to break through creative blocks and introduce unexpected directions.

## Workflow

### Step 1: Get Random Strategies

Run the script to get 4 random strategies:

```bash
./scripts/pick-strategies.sh -n 4
```

### Step 2: Present Strategies to User

Use `AskUserQuestion` to present the 4 strategies as options. Each strategy becomes a selectable option.

**Format:**
- header: "Strategy"
- question: "Which oblique strategy would you like to apply to this session?"
- options: The 4 strategies from the script output
- multiSelect: false

### Step 3: Ask How to Apply

After the user selects a strategy, use another `AskUserQuestion` to ask how they'd like to apply it.

**Format:**
- header: "Application"
- question: "How would you like to apply '[selected strategy]'?"
- options:
  - "Apply to current task" - Focus this strategy on whatever I'm working on right now
  - "Use as session mindset" - Let this strategy color the entire session's approach
  - "Help me interpret it" - Explain what this strategy might mean in a coding context
- multiSelect: false

### Step 4: Acknowledge and Incorporate

Based on the user's choice:

- **Apply to current task**: Reframe the current work through the lens of the strategy. Offer specific suggestions for how the strategy might change the approach.

- **Use as session mindset**: Acknowledge the strategy and naturally reference it throughout the session when relevant. Let it influence suggestions and perspectives.

- **Help me interpret it**: Explain the strategy's origin and meaning, then offer interpretations for how it might apply to software development, debugging, architecture, or creative coding challenges.

## Example Interaction

```
User: /oblique

Claude: [Runs ./scripts/pick-strategies.sh -n 4]
        Output:
        - Honor thy error as a hidden intention
        - Emphasise the flaws
        - Do nothing for as long as possible
        - Use an old idea

Claude: [AskUserQuestion #1]
        "Which oblique strategy would you like to apply to this session?"
        Options presented to user...

User: Selects "Honor thy error as a hidden intention"

Claude: [AskUserQuestion #2]
        "How would you like to apply 'Honor thy error as a hidden intention'?"
        Options presented to user...

User: Selects "Apply to current task"

Claude: Interesting choice! "Honor thy error as a hidden intention" suggests that
        mistakes aren't accidents - they might be revealing something your
        conscious mind missed.

        For your current work, this could mean:
        - That bug you found might actually be a feature in disguise
        - The "wrong" approach might lead somewhere interesting
        - Instead of fixing, explore what the error is trying to tell you

        What are you working on? Let's see what hidden intentions might be lurking.
```

## Notes

- The script uses POSIX tools (`awk`, `sort`, `head`, `cut`) for cross-platform compatibility
- All 113 original Oblique Strategies are embedded in the script
- Each invocation is independent - no state is tracked between uses
