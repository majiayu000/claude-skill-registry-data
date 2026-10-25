---
name: skill-recipes
description: >
  Self-installing markdown recipes for skills. Each skill can include an INSTALL.md
  that an agent reads and executes to set up dependencies, MCP servers, or config.
  Trigger: When installing a skill with INSTALL.md, or creating skills with setup requirements.
license: MIT
metadata:
  author: JNZader
  version: "1.0"
  tags: [skills, installation, automation, recipes]
  category: workflow
  source: garrytan/gbrain
---

## Purpose

Define a pattern where skills are self-installing: an INSTALL.md contains executable setup instructions that an agent follows to configure dependencies, MCP servers, or config.

---

## Recipe Format

```
own/skills/my-skill/
  SKILL.md         <- the skill itself
  INSTALL.md       <- optional setup recipe
```

### INSTALL.md Structure

```markdown
# Install: {skill-name}

## Prerequisites
- [ ] Node.js >= 20

## Steps
### 1. Install dependencies
\`\`\`bash
pnpm add -D playwright
\`\`\`

### 2. Verify
\`\`\`bash
npx playwright --version
\`\`\`

## Uninstall
\`\`\`bash
pnpm remove playwright
\`\`\`
```

---

## Agent Execution Protocol

1. **Read INSTALL.md** completely before executing
2. **Check Prerequisites** — verify each is met, stop if not
3. **Execute Steps** sequentially (Bash for commands, Write for files)
4. **Run Verify** step to confirm success
5. **Report** results

### Safety Rules

1. NEVER modify files outside project directory without confirmation
2. NEVER install global packages without confirmation
3. If a step fails, STOP — do not continue
4. Show commands to user BEFORE executing

---

## Critical Rules

1. INSTALL.md is OPTIONAL — skills work without it
2. Recipes MUST be idempotent — running twice must not break anything
3. Every recipe MUST have a Verify step
4. Recipes MUST NOT contain secrets or API keys
5. Agents MUST show what will execute before running
