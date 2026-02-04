---
name: template-assistant
description: Generate intelligent content for PARA Obsidian vault templates. Use when asked to create new notes (project, area, resource, task, capture, daily, weekly-review, booking, checklist, itinerary, trip-research), populate template sections with AI-generated content, or understand what fields a template requires before creation.
---

# Template Assistant Skill

## Workflow

### 0. Gather Vault Context (NEW)

Before creating notes, understand what already exists:

```bash
# List existing areas
bun ${CLAUDE_PLUGIN_ROOT}/src/cli.ts list-areas --format json

# List existing projects (for task linking)
bun ${CLAUDE_PLUGIN_ROOT}/src/cli.ts list-projects --format json
```

**CRITICAL: Classification vs Invention**

When selecting areas/projects, you are CLASSIFYING content into existing categories, NOT inventing factual data:

- **Areas/Projects** = CLASSIFICATION (analytical task)
  - Analyze the content to determine which life domain or responsibility it belongs to
  - Areas are ongoing RESPONSIBILITIES or LIFE DOMAINS (Home, Work, Health, Finance, Learning, Family, etc.)
  - Projects are temporary initiatives with completion dates
  - **Example classifications:**
    - Garden shed construction → [[Home]] (ongoing home maintenance responsibility)
    - Fitness goals → [[Health]] (ongoing health management domain)
    - Work deadline → [[Work]] (professional responsibilities)

- **Factual Data** = INVENTION (requires user knowledge)
  - Dates, numbers, specific names must come from user
  - Use `null` when unknown, never guess

**Via MCP tools:**
- `para_list_areas` - Get existing areas
- `para_list_projects` - Get existing projects

**For slash commands:** Use `AskUserQuestion` to present existing areas/projects as options with descriptions of what domain they represent. Include "Other" for new classifications when content doesn't fit existing categories.

### 1. Discover Template Structure

```bash
bun ${CLAUDE_PLUGIN_ROOT}/src/cli.ts template-fields project --format json
```

Returns required args, auto-filled fields, and body sections.

### 2. Gather User Context

Ask focused questions matching the template type:

| Template | Key Questions |
|----------|---------------|
| project | What's the goal? How will you know it's done? Which life domain does this belong to (analyze: Home/Work/Health/Finance/Learning/Family)? ← CLASSIFY into existing areas |
| area | What's your responsibility? What standards matter? |
| resource | Why does this resonate? What's the key insight? Which life domain is this resource for? ← CLASSIFY based on content domain |
| task | What's the outcome? What's the priority? Which project is this supporting (analyze task context)? ← CLASSIFY into existing projects or standalone |

**Classification approach:**
- Analyze note content to determine life domain or project context
- Present existing areas/projects as classification options
- Only suggest new areas/projects when content clearly doesn't fit existing categories
- Remember: Classification = analytical judgment, not data invention

### 3. Generate Section Content

**Content-Heavy** (project, resource, weekly-review, daily): Generate paragraphs, bullet lists, `[[wikilinks]]`

**Metadata-Heavy** (task, booking, checklist, capture): Focus on frontmatter, minimal body content

**CRITICAL:** When generating wikilinks for frontmatter args, do NOT include quotes:
- ✅ Correct: `--arg "Area=[[Product]]"`
- ❌ Wrong: `--arg "Area=\"[[Product]]\""`

This ensures Dataview queries work correctly.

### 4. Create Note with Content

```bash
bun ${CLAUDE_PLUGIN_ROOT}/src/cli.ts create --template project \
  --title "Launch Dark Mode" \
  --arg "Area=[[Product]]" \
  --arg "Target completion date (YYYY-MM-DD)=2025-03-31" \
  --content '{"Why This Matters": "Dark mode reduces eye strain...", "Success Criteria": "- [ ] Theme toggle works\n- [ ] Persists across sessions"}'
```

### 5. Validate Result

```bash
bun ${CLAUDE_PLUGIN_ROOT}/src/cli.ts frontmatter validate "Launch Dark Mode.md" --format json
```

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Template not found | Run `bun ${CLAUDE_PLUGIN_ROOT}/src/cli.ts templates` to list available templates |
| Missing required arg | Run `bun ${CLAUDE_PLUGIN_ROOT}/src/cli.ts template-fields <template>` to discover requirements |
| Section not injected | Heading may not exist in template |
| Vault not git repo | Ensure PARA_VAULT is an initialized git repository |

---

## References

Load these as needed based on the task:

- **Template details**: `./references/template-catalog.md` — Full catalog of all 11 templates with required args and body sections
- **Generation patterns**: `./references/content-strategies.md` — Template-specific content generation strategies (goal clarification, success criteria, risk identification)
- **Examples**: `./references/examples.md` — Complete CLI examples for project, area, resource, task, capture

---

## Vault-Aware Workflows

### Automatic Mode (convert command)

The convert command uses **classification-based prompting** to intelligently populate area/project fields:

```bash
bun ${CLAUDE_PLUGIN_ROOT}/src/cli.ts convert note.md --template project
# Vault context: 5 areas, 12 projects, 20 tags
# LLM analyzes content and classifies into existing [[Health]] area
# Example: "fitness tracking" content → [[Health]] (not "Wellness" or "Fitness")
```

**How classification works:**
1. LLM receives existing areas/projects as classification options
2. Analyzes note content to determine life domain or project context
3. Selects best-matching existing category OR suggests new one if content doesn't fit
4. Areas represent ongoing RESPONSIBILITIES (Home, Work, Health) not temporary topics
5. Projects represent temporary INITIATIVES with completion dates

**Classification examples from prompt:**
- Garden shed → [[Home]] (ongoing home maintenance responsibility)
- Fitness goals → [[Health]] (ongoing health management domain)
- Work project → [[Work]] (professional responsibilities domain)

### Interactive Mode (slash commands)

For manual note creation via slash commands, use **classification-based questioning**:

1. **Fetch context** via MCP tools
2. **Analyze content** to determine likely domain
3. **Present options** with domain descriptions via AskUserQuestion
4. **Create note** with classification

**Example:**
```typescript
// 1. Fetch existing areas
const { areas } = await para_list_areas({ response_format: "json" });

// 2. Analyze content and ask user (with domain context)
const answer = await AskUserQuestion({
  question: "This content appears to be about fitness tracking. Which life domain should it belong to?",
  header: "Area",
  options: [
    { label: "Health", description: "Ongoing health & wellness management (recommended for fitness)" },
    { label: "Personal", description: "Personal development & self-improvement" },
    { label: "Home", description: "Home responsibilities & maintenance" }
  ],
  multiSelect: false
});

// 3. Create with classified area
await para_create({
  template: "project",
  title: "My Project",
  args: { "Area": `[[${answer}]]` }  // No quotes!
});
```

**Classification guidance:**
- Frame options with domain descriptions so user understands what each area represents
- Suggest most likely classification based on content analysis
- Only offer "Other" when content clearly doesn't fit any existing domain

### Tag Selection Pattern

Tags are **hard constrained** - must come from config. When working with tags, always validate against the allowed tag list defined in your vault configuration. Tags typically include categories like: project, area, resource, task, daily, journal, etc. NO new tags are allowed outside the configured set.
