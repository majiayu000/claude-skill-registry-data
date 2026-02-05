---
name: meta-skill
description: Creates new skills for unfamiliar technologies. Use when needing to create a skill, add support for unknown frameworks, or extend capabilities for new tech. Researches documentation and delegates to skill-creator for scaffolding.
allowed-tools: Write, Read, Glob, Grep, WebFetch, WebSearch, Edit, Bash(*)
---

# Meta-Skill

Expert agent architect that creates new skills for any technology.

## Autonomy Level: Full

- Create skills immediately when threshold reached (2+ uses of unfamiliar tech)
- Notify after creation, don't ask before
- Research documentation autonomously
- Delegate to `skill-creator` for scaffolding

## When to Activate

- New technology encountered 2+ times without existing skill
- User explicitly requests skill creation
- Learning agent proposes new skill
- Repeated documentation lookups for same technology

## Skill Creation Process

### Step 1: Research Technology

```
WebSearch: "[technology] official documentation"
WebSearch: "[technology] best practices 2025"
WebSearch: "[technology] common patterns"
```

Gather:
- Official docs URLs
- API patterns
- Best practices
- Common pitfalls

### Step 2: Analyze Requirements

Determine:
- Primary use cases
- Required tools
- File patterns that trigger it
- Common workflows
- Error patterns

### Step 3: Initialize with skill-creator

Run the scaffolding script:
```bash
python .claude/skills/skill-creator/scripts/init_skill.py <name> --path .claude/skills
```

### Step 4: Populate Skill Content

Edit the generated `SKILL.md` with:

**Frontmatter:**
- `name`: kebab-case (e.g., `stripe-integration`)
- `description`: What it does + trigger keywords (max 1024 chars)
- `allowed-tools`: Minimal required set

**Body:**
- Documentation URLs discovered in research
- Workflows based on best practices
- Common patterns with examples
- Error handling guidance
- Delegation rules

### Step 5: Add Resources

Based on research, add:
- `scripts/` - Automation for repetitive tasks
- `references/` - Detailed docs, schemas, patterns
- `assets/` - Templates, boilerplate

### Step 6: Validate and Notify

```bash
python .claude/skills/skill-creator/scripts/quick_validate.py .claude/skills/<name>
```

Then notify: "Created skill: [name] for [technology]"

## Example

**Trigger**: Claude encounters Stripe integration twice

**Research**:
```
WebSearch: "Stripe API documentation"
→ https://stripe.com/docs/api

WebSearch: "Stripe webhooks best practices"
→ https://stripe.com/docs/webhooks/best-practices
```

**Initialize**:
```bash
python .claude/skills/skill-creator/scripts/init_skill.py stripe-integration --path .claude/skills
```

**Result**: `.claude/skills/stripe-integration/SKILL.md`

```yaml
---
name: stripe-integration
description: Handles Stripe payments, webhooks, and subscriptions. Use for stripe, payment, checkout, subscription, webhook integration.
allowed-tools: WebFetch, Read, Write, Edit, Bash(npm:*), Bash(curl:*)
---
```

## Quality Checklist

- [ ] Description under 1024 chars with trigger keywords
- [ ] Official documentation URLs included
- [ ] Minimal tool permissions
- [ ] Error handling guidance
- [ ] Delegation rules specified
- [ ] Validated with quick_validate.py

## Delegation

| Condition | Delegate To |
|-----------|-------------|
| Need skill scaffolding | `skill-creator` |
| Frontend/UI work | `frontend-design` |
| LSP setup needed | `lsp-setup` |
