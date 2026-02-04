---
name: make-note
description: Create well-structured notes in Obsidian with intelligent tag suggestions. Use when the user asks to create a note, make a note, or save content to Obsidian. Scans existing vault for common tags and presents suggestions before creating the note in the Resources folder.
license: MIT
metadata:
  version: 1.2
---

# Make Note

Create or edit notes in Obsidian's Resources folder with intelligent tag management based on
existing vault patterns.

## Workflow

### Step 1: Analyze Tag Patterns

Before creating any note, scan the vault to understand existing tag patterns:

1. Use the MCP Server `mcp-obsidian` and invoke the tool `obsidian_get_tags`
   to get a list of all available tags
2. Identify the most commonly used tags and their hierarchies
3. Note tag categories (e.g., work-related, technical, personal)

The MCP tool `obsidian_get_tags` returns a JSON with tag frequencies. Focus on tags that appear
more than 3 times to identify genuine patterns rather than one-off tags.

This is an example of the JSON return:

```json
{
  "tags": {
    "#tag1": 24,
    "#tag2/subtagx": 37,
    "#tag3": 104,
    "#tag4": 62
  }
}
```

### Step 2: Suggest Relevant Tags

Based on the note content and existing tag patterns:

1. Analyze the note topic and content
2. Match it against common tags from the vault
3. Propose 3-5 relevant tags that fit the content
4. Present tags to the user as a numbered list for easy selection by number.
5. Allow the user to confirm, modify, or add tags

**Tag suggestion format:**

- Present hierarchical tags using slash notation (e.g., `ai/code-agent`, `dpg/strategy`)
- Group related tags together (e.g., all work tags, all technical tags)
- Include mix of general and specific tags where appropriate

### Step 3: Confirm Tags with User

Present suggested tags to the user for confirmation:

"I suggest these tags for your note:

1. [tag1]
2. [tag2]
3. [tag3]

Would you like to use these tags, modify them, or add additional tags?"

Wait for user confirmation before proceeding.

### Step 4: Create the Note

Once tags are confirmed:

1. Create or edit the note in the Resources folder using the MCP Server `mcp-obsidian` tool
   `obsidian_append_content`
2. Proper front matter MUST be included and MUST follow the following format:
   - `tags:` field formatted as list
   - `created:` field with current date in format `DD-MM-YYYY HH:MM`
3. Add the note title as H1 heading with wiki-link format: `# [[Title]]`
4. Include the main content below the heading
5. Preserve any sections, formatting, or structure from the original content
6. Add at the bottom of the note:
   - `## References` section with relevant external links (if any)
   - `## Related Notes` section with wiki-links to other notes in the vault (if any). DO NOT add dead links!

**MANDATORY Frontmatter format:**

```yaml
---
tags:
- tag1
- tag2
- tag3
created: DD-MM-YYYY HH:MM
---
```

**Bottom sections format:**

```markdown
## References

- [Link title](URL)
- [Another link](URL)

## Related Notes

- [[Related Note 1]]
- [[Related Note 2]]
```

Only include these sections if there are relevant links or related notes to add. If no references
or related notes exist, omit those sections entirely.

### Step 5: Confirm Creation

After creating the note, inform the user:

- Confirm the note was created in Resources folder
- List the filepath
- Confirm the tags that were applied

## Tag Guidelines

### Tag Format Standards

Follow these conventions observed in the vault:

1. **Hierarchical tags**: Use forward slash for hierarchy (e.g., `cloud/aws`, `ai/agentic`,
   `music/modular`)
2. **Array format**: Tags in frontmatter use list notation
3. **Lowercase**: All tags should be lowercase
4. **Hyphens for multi-word tags**: Use hyphens for multi-word tags (e.g., `platform-engineering`,
   `code-agent`)

### Common Tag Categories

Based on vault analysis, common tag patterns include:

**Work/DPG Related:**

- `secdevops`, `dpg/strategy`, `dpg/development-enablement`, `platform-engineering`

**Technical:**

- `cloud/aws`, `ai/code-agent`, `ai/agentic`, `coding/sdd`

**Personal/Hobbies:**

- `music/modular`, `learning`, `productivity`

**Context Tags:**

- Work context: Usually includes dpg-related or professional tags
- Home context: Usually includes personal/hobby tags

### Tag Selection Strategy

1. **Prioritize existing tags**: Prefer tags already in use (3+ occurrences)
2. **Match content specificity**: Use specific hierarchical tags when content is specific (e.g.,
   `ai/code-agent` vs just `ai`)
3. **Mix breadth and depth**: Include both general category tags and specific subtags
4. **Limit to 3-5 tags**: Avoid over-tagging; focus on most relevant categories
