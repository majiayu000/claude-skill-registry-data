---
description: Record a workflow and auto-generate a reusable command from it
argument-hint: "[name for the playbook]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash(date:*)
---

Watch a manual workflow, then auto-generate a reusable command from it. You describe the steps, this command turns them into a repeatable, documented procedure.

## Steps

### Step 1: Name the playbook

Get the playbook name from the argument. If not provided, ask what this workflow does in one sentence and derive a kebab-case name.

### Step 2: Capture the workflow

Ask the user to describe their workflow step by step. For each step, capture:
- **What:** The action taken
- **Where:** What file, tool, or system is involved
- **Why:** The purpose of this step
- **Inputs:** What information is needed
- **Output:** What this step produces

Guide them through it: "What do you do first?" → "Then what?" → "What happens next?"

Continue until they say they're done.

### Step 3: Identify patterns

Analyse the captured workflow:
- **Which steps can be parallelised?** (independent reads, searches)
- **Which steps need user input?** (decisions, approvals)
- **Which steps are conditional?** (only if X, then Y)
- **What tools does each step need?** (Read, Write, Agent, Bash, WebSearch, etc.)
- **Are there any existing skills that match steps?** (check `.claude/skills/`)

### Step 4: Determine the argument

What variable input does this workflow need each time it runs?
- A project name? A file path? A topic? A client name?
- Define the argument-hint that makes sense

### Step 5: Generate the command

Write the command file to `.claude/commands/[playbook-name].md`:

```markdown
---
description: [one-line description derived from the workflow]
argument-hint: "[identified argument]"
allowed-tools:
  - [list of tools needed, derived from step analysis]
---

[Brief explanation of what this command does]

## Steps

### Step 1: [First action]
[Instructions derived from the captured workflow]

### Step 2: [Second action]
[Instructions]

[Continue for each step, with parallel steps marked]

### Step [N]: Output
[What the final output looks like]
```

### Step 6: Verify and refine

Show the generated command to the user:
- "Here's the command I generated. Does this capture your workflow correctly?"
- Make any adjustments they request
- Save the final version

### Step 7: Register the command

If a command-index.md exists, add the new command to it.

Output: "Your playbook is saved as `/[name]`. Run it any time to repeat this workflow."
