---
name: skill-generator
description: Meta-skill for creating, refining, and managing Agent Skills. Use when needing to create new skills, improve existing skills, analyze skill performance, or teach the agent new capabilities. Enables self-improvement and knowledge capture.
metadata:
  author: coachone
  version: "1.0"
compatibility: Works with any VS Code Insiders with chat.useAgentSkills enabled
---

# 🧬 Skill Generator - Self-Evolving Capabilities

This skill enables the agent to create, refine, and manage new skills autonomously, capturing learned patterns and domain expertise into reusable capabilities.

## When to Create a New Skill

Create a skill when you observe:
- **Repeated context** provided across multiple conversations
- **Domain-specific knowledge** that Claude doesn't have by default
- **Multi-step workflows** that benefit from consistent execution
- **Project-specific conventions** that should be encoded
- **Debugging patterns** discovered during problem resolution

## Skill Creation Workflow

### Step 1: Identify the Need

Ask yourself:
- Is this knowledge reusable across sessions?
- Would encoding this save significant tokens in future conversations?
- Does this represent procedural knowledge Claude lacks?

### Step 2: Design the Skill Structure

```
skill-name/
├── SKILL.md              # Required: Main instructions (<500 lines)
├── scripts/              # Optional: Executable code
│   └── helper.ts
├── references/           # Optional: Detailed documentation
│   └── REFERENCE.md
└── assets/               # Optional: Templates, data
    └── template.md
```

### Step 3: Write the SKILL.md

**Template:**
```markdown
---
name: [lowercase-hyphen-name]
description: [What it does AND when to use it. Max 1024 chars. Be specific with keywords.]
metadata:
  author: [author]
  version: "1.0"
---

# [Skill Title]

## Quick Reference
[Table or list of most common operations]

## Core Functionality
[Main instructions, organized by task]

## Examples
[Concrete input/output examples]

## Guidelines
[Rules and constraints]
```

### Step 4: Validate the Skill

Checklist before saving:
- [ ] Name is lowercase with hyphens only
- [ ] Description includes WHAT and WHEN
- [ ] SKILL.md body < 500 lines
- [ ] No time-sensitive information
- [ ] Consistent terminology
- [ ] Clear examples provided
- [ ] File references are one level deep

## Skill Categories for This Project

### Debug Skills (`.github/skills/debug-*`)
For capturing debugging patterns:
- `debug-nextjs` - Next.js specific debugging
- `debug-prisma` - Database debugging
- `debug-react-query` - State management debugging

### Feature Skills (`.github/skills/feature-*`)
For feature development patterns:
- `feature-api-routes` - API route conventions
- `feature-components` - Component patterns

### Process Skills (`.github/skills/process-*`)
For workflow automation:
- `process-deploy` - Deployment procedures
- `process-migration` - Database migrations

## Auto-Generation from Debug Sessions

When a debug session reveals new patterns, create a skill:

```markdown
## Pattern Discovered: [Name]

**Problem Type**: [category]
**Root Cause**: [description]
**Solution Pattern**: [reusable fix]
**Prevention Strategy**: [how to avoid]

→ Suggest: Create skill `debug-[category]` capturing this pattern
```

## Skill Evolution

### Improving Existing Skills

When a skill proves insufficient:
1. Identify the gap
2. Propose enhancement
3. Add to appropriate section (or new reference file)
4. Update version in metadata

### Deprecating Skills

When a skill becomes obsolete:
1. Add deprecation notice at top of SKILL.md
2. Point to replacement skill
3. Remove after migration period

## Example: Creating a Debug Skill

After discovering a recurring Next.js hydration issue pattern:

```markdown
---
name: debug-hydration
description: Diagnose and fix React hydration mismatches in Next.js. Use when seeing hydration errors, content flickering, or server/client mismatches.
metadata:
  author: coachone
  version: "1.0"
---

# Hydration Debugging

## Quick Diagnosis

1. Check browser console for specific hydration error
2. Identify the component mentioned in error
3. Compare server-rendered HTML with client-rendered output

## Common Causes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Date/time mismatch | Server/client timezone | Use `suppressHydrationWarning` or standardize timezone |
| Random IDs | useId() not used | Replace Math.random() with React.useId() |
| Browser APIs | window/document access | Check typeof window !== 'undefined' |
| Extension interference | Browser extensions | Test in incognito mode |

## Fix Patterns

### Pattern 1: Deferred Client Rendering
\`\`\`tsx
const [mounted, setMounted] = useState(false);
useEffect(() => setMounted(true), []);
if (!mounted) return <Skeleton />;
return <DynamicContent />;
\`\`\`

### Pattern 2: Suppress Warning (use sparingly)
\`\`\`tsx
<time suppressHydrationWarning>{new Date().toLocaleString()}</time>
\`\`\`
```

## Skill Discovery Tips

Skills are activated when their description matches user intent. Write descriptions that:
- Use specific keywords users might mention
- Cover synonyms and alternative phrasings
- Describe both the capability AND the trigger context

**Good**: "Debug and fix React hydration errors, content mismatches between server and client rendering, SSR issues"
**Bad**: "Helps with React problems"

## File Locations

Skills for this project should be created in:
```
.github/skills/[skill-name]/
├── SKILL.md
└── [optional resources]
```
