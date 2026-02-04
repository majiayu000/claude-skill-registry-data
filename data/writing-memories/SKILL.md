---
name: writing-memories
description: Writes or updates memory files with proper YAML frontmatter in the agent's memories directory. Use when saving new project learnings or updating existing memory files.
---

<quick_start>
- Write to `./.{AGENT_NAME}/skills/memories/<name>/SKILL.md`.
- Create the directory if needed.
- Prepend the required header if missing.
</quick_start>

<configuration>
<file_format>
- Path: `./.{AGENT_NAME}/skills/memories/<name>/SKILL.md`
- The `<name>` is the memory name using hyphens (e.g., `project-overview`, `suggested-commands`)
- The file must be named `SKILL.md` (uppercase)
</file_format>

<header_rules>
- The header uses YAML frontmatter (between `---` delimiters)
- **Required fields:**
  - `name` - the memory name (must match the folder name)
  - `description` - brief description of what this memory contains and when to use it
- The `description` field must NOT contain colons (`:`) after the initial one
  - Good: `description: Brief summary of project structure`
  - Bad: `description: Project structure: components and layout`
- Keep the description on a single line
- Do NOT add extra fields like `type` or `mutable` - only `name` and `description` are required
</header_rules>
</configuration>

<templates>
<header>
Every `SKILL.md` file **must** have this exact header format:
```
---
name: <memory-name>
description: <brief description without colons>
---
```

Example:
```
---
name: project-overview
description: Skillrena repo purpose and structure
---
```
</header>
</templates>

<decision_points>
- Existing memory? Update if the info is the same topic; otherwise create a new file.
- Multiple small notes? Consolidate into one concise memory. If you see more than 10 memories it is a good idea to consolidate them into 5 memories.
</decision_points>

<quality_checklist>
- Concise and actionable
- No duplication with other memories
- Sources or file paths included when relevant
</quality_checklist>

<failure_modes>
- Missing description: add a short, specific summary.
- Wrong path: keep memories under `./.{AGENT_NAME}/skills/memories/`.
</failure_modes>
