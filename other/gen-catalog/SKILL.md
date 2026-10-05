---
name: gen-catalog
description: "Generate skill catalog — auto-discovers skills, builds README tables, JSON, or HTML output. Triggers: generate skill catalog, update skills documentation, list all skills"
version: "2.0.0"
category: docs
platforms:
  - CLAUDE_CODE
---

You are a catalog generation agent. Do NOT ask the user questions.

============================================================
PHASE 1: DISCOVER ALL SKILLS
============================================================

1. Determine the skills directory:
   - If the user specifies a directory, use that.
   - Otherwise default to `~/.claude/skills/`.

2. Glob for all `*/SKILL.md` and `*/skill.md` files under the skills directory.
   Also check `~/.claude/commands/*.md` for global commands (slash commands
   that exist outside the skills directory).

3. For each file found, parse the YAML frontmatter (between `---` delimiters):
   - `name` (required)
   - `description` (required)
   - Any other frontmatter fields are preserved but not required.

4. Auto-detect categories by scanning each skill's instructions content.
   Do NOT use a fixed category list. Instead:
   - Extract keywords and themes from the instructions.
   - Group skills by their primary purpose. Common groupings include
     (but are not limited to): research/discovery, spec/design, build,
     testing, quality/review, documentation, operations, security,
     infrastructure, combo/chain, deployment, analysis, etc.
   - If a skill clearly chains other skills (e.g., "Follow the instructions
     defined in the `/X` skill" or "Chains /X -> /Y"), classify it as a
     combo/chain skill and record the chain sequence.
   - Use short lowercase labels for categories (e.g., "research", "build",
     "testing", "docs", "ops", "combo").
   - Generate human-readable display names from category labels
     (e.g., "research" -> "Research & Discovery", "build" -> "Build & Implement").

5. Generate a markdown link for each skill pointing to its SKILL.md file
   relative to the skills directory root (e.g., `[/name](./name/SKILL.md)`).

============================================================
PHASE 2: DETERMINE OUTPUT FORMAT
============================================================

Check if the user requested a specific output format. Supported formats:

- **readme** (default): Markdown table injected into README.md
- **json**: JSON array of skill objects written to `skills-catalog.json`
- **html**: Standalone HTML page written to `skills-catalog.html`

If no format is specified, use "readme".

### README format (default)

Read the existing README.md in the skills directory.

Preserve everything ABOVE `<!-- AUTO-GENERATED-SKILLS-TABLE-START -->`.
Preserve everything BELOW `<!-- AUTO-GENERATED-SKILLS-TABLE-END -->`.

If these markers do not exist yet, add them after the first heading and
intro paragraph.

Between the markers, generate:

### Skills by Category

For each detected category (sorted alphabetically, with combo/chains last):

#### [Category Display Name]

| Skill | Description |
|-------|-------------|
| [`/name`](./name/SKILL.md) | description |

For combo/chain skills, add a "Chain" column:

| Skill | Chain | Description |
|-------|-------|-------------|
| [`/name`](./name/SKILL.md) | `/a` -> `/b` -> `/c` | description |

Also include global commands from `~/.claude/commands/` with a note:
> Global commands (available in any project):

| Command | Description |
|---------|-------------|
| `/name` | description |

### JSON format

Write a JSON file with this structure:
```json
{
  "generated": "ISO-8601 timestamp",
  "skills_directory": "/path/to/skills",
  "categories": {
    "category-label": {
      "display_name": "Category Display Name",
      "skills": [
        {
          "name": "skill-name",
          "description": "...",
          "path": "relative/path/to/SKILL.md",
          "chain": ["/a", "/b"] // only for combo skills
        }
      ]
    }
  },
  "global_commands": [
    { "name": "command-name", "description": "..." }
  ]
}
```

### HTML format

Generate a standalone HTML page with:
- Clean CSS styling (no external dependencies)
- Skills grouped by category in collapsible sections
- A search/filter input for skill names and descriptions
- Links to each skill's SKILL.md file

============================================================
PHASE 3: UPDATE skills-list (README format only)
============================================================

If outputting README format and `skills-list/SKILL.md` exists in the
skills directory, update its embedded skills table:

- Keep the YAML frontmatter intact.
- Replace ONLY the skills table content.
- Keep any manually-written sections after the table (pipeline diagrams,
  parallelization rules, development patterns).

The generated table format:

| Skill | Description |
|---|---|
| **name** | description |

Group by category with category headers.

============================================================
PHASE 4: VERIFY
============================================================

1. Count total skills discovered.
2. Count skills in generated output.
3. Counts must match. If not, flag the discrepancy.
4. Check for orphan directories (dirs under the skills directory with no SKILL.md).
5. Check for skills referenced in combo chains that don't exist.

Report:
## Catalog Generated
- Skills discovered: N
- Output format: [readme|json|html]
- Output updated: N skills
- Orphan directories: [list or "none"]
- Missing chain targets: [list or "none"]

============================================================
PHASE 5: COMMIT (optional)
============================================================

If changes were made, stage the updated files.
Commit: "docs: auto-generate skills catalog (N skills)"

Do NOT include Co-Authored-By lines.
Push after committing.


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing documentation, validate completeness:

1. Verify all required sections are present and non-empty.
2. Verify internal cross-references and links resolve correctly.
3. Verify no placeholder text remains ("{TODO}", "[TBD]", "...", "etc.").
4. Verify code examples are syntactically valid.

IF VALIDATION FAILS:
- Identify which sections are incomplete or contain placeholders
- Re-generate only the deficient sections
- Repeat up to 2 iterations


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /gen-catalog — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
