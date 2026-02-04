---
name: opencode-agent-generator
description: Creates OpenCode agents in project folders for opencode serve operations. Use when you need to autonomously create specialized OpenCode agents that will be used by OpenCode serve, not by Claude directly.
---

# OpenCode Agent Generator

Creates OpenCode agents in project folders (`.opencode/agent/`) for use with opencode serve operations. These agents will be used by OpenCode serve, not by Claude directly.

**CRITICAL UNIVERSAL WARNING**: All agent examples in this skill (code-analyzer, documentation-writer, security-auditor, test-engineer, etc.) are EXAMPLES ONLY. They exist purely to demonstrate the communication protocol format. Real swarms will have completely different agent types, purposes, and domains. This skill works with ANY agent configuration, not just the examples shown.

## Instructions

**IMPORTANT: Create agents BEFORE launching opencode serve. Agents are only loaded when the server starts.**

1. Determine agent requirements from the context:
   - Agent name (kebab-case, based on purpose)
   - Purpose/description (from task context)
   - Agent type (use PRIMARY for direct interaction, subagent cannot be directly used)
   - Tools needed (based on purpose)
   - Communication requirements (for swarm coordination)

2. Create the agent file at `.opencode/agent/{name}.md` (project-local)

3. Generate appropriate YAML frontmatter:
   ```yaml
   ---
   description: {purpose}
   mode: {agent_type}
   tools:
     read: true
     grep: true
     # Add other tools based on purpose
   permissions:
     edit: ask
     write: ask
     bash:
       "git*": allow
       "*": ask
   ---
   ```

4. Write a focused system prompt based on the agent's purpose

5. **CRITICAL FOR SWARM**: Add communication protocol section to agent prompt

6. Validate the YAML syntax and file structure

## Examples

### Specialist Agent with Communication Protocol

**⚠️ EXAMPLE ONLY - The following demonstrates the communication protocol format. The specific agent type (Code Analyzer) is just an example. ANY agent type can use this pattern.**

```bash
# EXAMPLE: Create a [SPECIALIST_TYPE] agent with swarm communication
cat > .opencode/agent/[agent_name].md << 'EOF'
---
description: [Brief description of agent's specialty]
mode: primary
tools:
  read: true
  grep: true
  bash: true
permissions:
  edit: ask
  write: ask
  bash:
    "git*": allow
    "*": ask
---

You are a [SPECIALIST_TITLE] specializing in [domain of expertise].

## Core Responsibilities
- [Primary responsibility 1]
- [Primary responsibility 2]
- [Primary responsibility 3]
- [Primary responsibility 4]

## Swarm Communication Protocol

**CRITICAL**: When you need to communicate with other agents, you MUST follow this format:

1. **Introduction**: Always start with your identity and folder
2. **Purpose**: Clearly state why you're contacting them
3. **Request**: Specify exactly what you need
4. **Expected Response**: Describe the format you need

### Communication Template:
```
I am the [Agent_Title] agent from the '[folder_name]' folder. I am contacting you because I need [specific reason].

I need you to [specific request with details]. Please respond with [expected format/timing].
```

### Example Communications:
- **To [Other Agent Type]**: "I am the [Agent_Title] agent from '[folder_name]'. I need you to [specific task]. Please provide [expected output]."

## Coordination with Orchestrator
- Report progress regularly to orchestrator
- Request task clarification when needed
- Announce completion of tasks
- Escalate blocking issues

Remember: You are a specialist. Focus on your domain expertise and communicate clearly when collaboration is needed.
EOF
```

**UNIVERSAL TRUTH**: This pattern works for ANY agent type:
- `marketing-strategist/` - Marketing campaign planning
- `legal-advisor/` - Legal compliance and review
- `product-manager/` - Product strategy and roadmap
- `sales-analyst/` - Sales data and forecasting
- `teacher/` - Educational content and tutoring
- `chef/` - Recipe development and cooking techniques
- `fitness-trainer/` - Workout planning and nutrition

The examples are limitless - this skill is truly universal.

### Additional Example Patterns

**⚠️ MORE EXAMPLES - These show the pattern works for different domains:**

**Example 1: Creative Specialist**
```bash
# [ANY-CREATIVE-TYPE] agent pattern
cat > .opencode/agent/[agent_name].md << 'EOF'
---
description: [Creative specialty description]
mode: primary
tools:
  read: true
  write: true
  edit: true
permissions:
  edit: allow
  write: allow
  bash: false
---

You are a [Creative Specialist] creating [type of creative work].

## Communication Template:
```
I am the [Agent_Title] agent from the '[folder_name]' folder. I am contacting you because I need [specific reason].

I need you to [specific request]. Please respond with [expected format].
```
EOF
```

**Example 2: Technical Specialist**
```bash
# [ANY-TECHNICAL-TYPE] agent pattern
cat > .opencode/agent/[agent_name].md << 'EOF'
---
description: [Technical specialty description]
mode: primary
tools:
  read: true
  grep: true
  bash: true
permissions:
  edit: ask
  write: ask
  bash:
    "git*": allow
    "*": ask
---

You are a [Technical Specialist] specializing in [technical domain].

## Communication Template:
```
I am the [Agent_Title] agent from the '[folder_name]' folder. I am contacting you because I need [specific reason].

I need you to [specific request]. Please respond with [expected format].
```
EOF
```

**INFINITE POSSIBILITIES**: The pattern works for literally ANY domain:
- `artist/` - Visual art creation and critique
- `musician/` - Music composition and performance
- `writer/` - Creative writing and editing
- `scientist/` - Research and experimentation
- `teacher/` - Education and tutoring
- `therapist/` - Counseling and mental health
- `business-consultant/` - Business strategy and advice
- `personal-trainer/` - Fitness and health coaching

**THESE ARE NOT LIMITATIONS** - They are illustrations of the universal pattern.

## Agent Type Guidelines

- Use **subagent** for specialized tasks (code review, security, testing)
- Use **primary** for coordination and project management tasks

## Permission Guidelines

- **Security/analysis**: deny write/edit, restrictive bash
- **Implementation**: allow write/edit, permissive bash for dev tools
- **General**: ask for write/edit, allow git commands