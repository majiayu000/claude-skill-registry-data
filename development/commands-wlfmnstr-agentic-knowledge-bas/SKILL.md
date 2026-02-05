---
description: Create a new skill, command, or agent to enhance capabilities
argument-hint: "[type] [name]"
---

# Skill Generator

You are creating a new skill, command, or agent for the Claude Code agentic system.

## Your Task

Guide the user through creating a new enhancement for the agent system. Ask clarifying questions, then generate the appropriate file(s) based on the type selected.

## Step 1: Determine Type

If not specified in the command arguments, ask the user which type to create:

1. **Skill** - Reusable knowledge and patterns (TypeScript patterns, React best practices, etc.)
2. **Command** - Workflow automation (like /spec, /review, /integrate)
3. **Agent** - Specialized subagent with specific domain expertise

**Ask:** "What type would you like to create? (skill/command/agent)"

## Step 2: Gather Information

### For Skills

Ask the user:
- **Name:** What should the skill be called? (kebab-case, e.g., "react-hooks")
- **Description:** Brief description of what knowledge this skill provides
- **Content:** What patterns, best practices, or knowledge should be included?

**Skill Structure:**
```
.claude/skills/[name]/
  SKILL.md
```

**SKILL.md Template:**
```markdown
---
name: "[name]"
description: "[description]. Use when [trigger conditions]."
---

# [Title]

[Comprehensive knowledge content, patterns, code examples, best practices]

## [Section 1]

[Content...]

## [Section 2]

[Content...]

## Best Practices

[Key guidelines and patterns...]

## Common Pitfalls

[What to avoid...]

## Quick Reference

[Cheat sheet or quick lookup...]
```

### For Commands

Ask the user:
- **Name:** What should the command be called? (kebab-case, e.g., "create-component")
- **Argument Hint:** What arguments does it take? (e.g., "[component-name]")
- **Description:** Brief description of what the command does
- **Process:** What steps should the command execute?

**Command Structure:**
```
.claude/commands/[name].md
```

**Command Template:**
```markdown
---
description: [Brief description of what this command does]
argument-hint: "[argument-pattern]"
---

# [Command Title]

You are [role or task description].

## Your Task

[Clear description of what this command should accomplish]

## Process

[Step-by-step instructions for executing the command]

### Step 1: [Name]

[Instructions...]

### Step 2: [Name]

[Instructions...]

## Output Format

[What the command should produce or return]

## Example Usage

```
User: /[command-name] [args]
You: [Example response]
```

## Remember

- [Key principle 1]
- [Key principle 2]
- [Key principle 3]

[Additional detailed instructions as needed]
```

### For Agents

Ask the user:
- **Name:** What should the agent be called? (kebab-case, e.g., "testing-specialist")
- **Description:** Brief description of the agent's domain and purpose
- **Tools:** What tools should the agent have access to? (usually "*" for all tools)
- **Model:** Which model to use? (usually "claude-sonnet-4-5")
- **Domain:** What is the agent's area of expertise?
- **Responsibilities:** What specific tasks should this agent handle?

**Agent Structure:**
```
.claude/agents/[name].md
```

**Agent Template:**
```markdown
---
name: [name]
description: [Brief description of domain expertise]
tools: "*"
model: claude-sonnet-4-5
---

# [Agent Title]

You are the **[Role]** for the agentic knowledge base project. Your role is to [high-level purpose].

## Your Domain

- **[Area 1]:** [Description]
- **[Area 2]:** [Description]
- **[Area 3]:** [Description]

## Decision-Making Authority

You have authority to:
- ✅ [Responsibility 1]
- ✅ [Responsibility 2]
- ✅ [Responsibility 3]

You should defer to:
- **[Other Agent]:** [When to defer]
- **User:** [When to ask for approval]

## Working Approach

### [Primary Process Name]

When [doing primary task]:

1. **[Step 1]:** [Instructions]
2. **[Step 2]:** [Instructions]
3. **[Step 3]:** [Instructions]

## Key Principles

- **[Principle 1]:** [Explanation]
- **[Principle 2]:** [Explanation]
- **[Principle 3]:** [Explanation]

## Context Awareness

Always reference:
- **CLAUDE.md:** [What to check]
- **[relevant-skill]:** [What patterns to use]

## Integration with Other Agents

- **Collaborate with [Agent]:** [How and when]
- **Hand off to [Agent]:** [When to hand off]
- **Request [Agent]:** [When to request]

## Example Workflows

### [Workflow 1 Name]

```
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

## Your Success Criteria

- ✅ [Success metric 1]
- ✅ [Success metric 2]
- ✅ [Success metric 3]

---

*[Closing motivational statement about the agent's role]*
```

## Step 3: Create the File(s)

Once you have all the information:

1. **Create the directory** (if needed for skills):
   - For skills: `.claude/skills/[name]/`

2. **Create the file** with appropriate template:
   - Skills: `.claude/skills/[name]/SKILL.md`
   - Commands: `.claude/commands/[name].md`
   - Agents: `.claude/agents/[name].md`

3. **Fill in the template** with the user's information

4. **Customize the content** based on the specific use case

## Step 4: Verify and Confirm

After creating the file(s):

1. Show the user what was created
2. Provide the file path(s)
3. Explain how to use the new enhancement:
   - **Skills:** Auto-invoked when relevant or manually with Skill tool
   - **Commands:** Invoke with `/[name] [args]`
   - **Agents:** Invoke with Task tool specifying the agent type
4. Ask if any modifications are needed

## Tips for Quality

### For Skills
- Include comprehensive examples and code snippets
- Organize by topics with clear headings
- Add "Quick Reference" section for common patterns
- Include "Best Practices" and "Common Pitfalls"
- Make it self-contained and reference-able

### For Commands
- Be specific about the process steps
- Include examples of expected input/output
- Define clear success criteria
- Reference relevant agents or skills
- Keep scope focused on one workflow

### For Agents
- Define clear domain boundaries
- Specify decision-making authority
- Explain when to defer to other agents
- Include example workflows
- Define success criteria

## Example Session

```
User: /create-skill
You: What type would you like to create? (skill/command/agent)

User: skill
You: Great! Let's create a new skill. What should it be called?

User: css-patterns
You: What's a brief description of what this skill provides?

User: Modern CSS patterns including Grid, Flexbox, and custom properties
You: What specific knowledge should be included? Any particular patterns or techniques you want to document?

User: CSS Grid layouts, Flexbox patterns, CSS custom properties, and responsive design patterns
You: Perfect! I'll create a comprehensive skill for CSS patterns. Creating .claude/skills/css-patterns/SKILL.md...

[Creates the file with comprehensive content]

You: ✅ Created CSS patterns skill at .claude/skills/css-patterns/SKILL.md

This skill will be auto-invoked when working with CSS, or you can manually invoke it with the Skill tool.

Would you like me to add or modify anything?
```

## Remember

- Ask clarifying questions - don't guess
- Use the templates as a starting point, then customize
- Make skills comprehensive with examples
- Keep commands focused on workflows
- Define clear agent boundaries
- Always show the user what was created
- Provide usage instructions

Start by determining what type the user wants to create!
