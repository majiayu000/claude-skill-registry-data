---
name: gemini-partner
description: >
  Invoke Gemini CLI as a partner AI developer for tasks benefiting from its
  1M token context window or a second opinion. Use when analyzing large
  codebases, generating documentation, getting alternative perspectives,
  researching topics with web search, or creating UI wireframes/components.
  Gemini has read/write/edit/shell/web search capabilities like Claude.
---

# Gemini Partner

Invoke the Gemini CLI as a collaborative AI partner for development tasks. Gemini runs in headless mode with full filesystem access to the current project.

## When to Use Gemini

Use Gemini CLI when you need:

1. **Large Context Analysis** - Gemini has 1M token context (vs ~200k for Claude)
   - Analyzing entire codebases at once
   - Bulk documentation generation
   - Large refactoring analysis

2. **Second Opinion** - Alternative AI perspective
   - Architecture decisions
   - Code review
   - Debugging complex issues
   - Evaluating approaches

3. **Web Research** - Gemini has built-in web search
   - Researching libraries/frameworks
   - Finding implementation examples
   - Checking latest documentation

4. **UI Generation** - Design wireframes and components
   - HTML/CSS wireframes
   - React/Vue/Svelte components
   - Full page layouts

## Headless Invocation Pattern

**Basic syntax (Gemini 3 Pro):**
```powershell
gemini -y -o json -m gemini-3-pro-preview "<prompt>"
```

**Flags:**
- `-m gemini-3-pro-preview`: **ALWAYS use Gemini 3 Pro** (latest and most capable model)
- `-y` or `--yolo`: Auto-approve all file operations
- `-o json`: Return structured JSON output

**Important:**
- Always specify `-m gemini-3-pro-preview` to use the latest model
- Run from the project working directory so Gemini has filesystem context

## JSON Output Format

Gemini returns structured JSON with:
```json
{
  "response": "The AI's text response",
  "stats": {
    "models": { /* token usage */ },
    "tools": { /* tool call stats */ },
    "files": { "totalLinesAdded": 0, "totalLinesRemoved": 0 }
  }
}
```

## Invocation Examples

### 1. Codebase Analysis (Large Context)

```powershell
gemini -y -o json -m gemini-3-pro-preview "Analyze this entire codebase and provide:
1. Architecture overview
2. Key patterns used
3. Potential improvements
4. Security considerations

Focus on the src/ directory structure and how components interact."
```

### 2. Second Opinion on Approach

```powershell
gemini -y -o json -m gemini-3-pro-preview "I'm implementing [feature]. My current approach is [description].

Review my approach and provide:
1. Strengths of this approach
2. Potential issues or concerns
3. Alternative approaches to consider
4. Your recommendation"
```

### 3. Web Research

```powershell
gemini -y -o json -m gemini-3-pro-preview "Research the latest best practices for [topic] in 2025.

Include:
1. Current recommendations
2. Common pitfalls to avoid
3. Relevant libraries/tools
4. Code examples if applicable

Cite your sources."
```

### 4. Generate UI Component

```powershell
gemini -y -o json -m gemini-3-pro-preview "Create a React TypeScript component for [description].

Requirements:
- Use Tailwind CSS for styling
- Include TypeScript types
- Make it accessible (ARIA labels, keyboard nav)
- Add JSDoc comments

Save to: src/components/[ComponentName].tsx"
```

### 5. Documentation Generation

```powershell
gemini -y -o json -m gemini-3-pro-preview "Generate comprehensive documentation for this codebase.

Create:
1. README.md with project overview
2. API documentation for public functions
3. Architecture diagram description
4. Getting started guide

Save documentation to the docs/ directory."
```

### 6. Code Review

```powershell
gemini -y -o json -m gemini-3-pro-preview "Review the recent changes in this codebase for:
1. Code quality issues
2. Potential bugs
3. Security vulnerabilities
4. Performance concerns
5. Suggestions for improvement

Be specific with file paths and line numbers."
```

## Prompt Engineering Tips

1. **Be specific about output location** - Tell Gemini where to save files
2. **Request structured responses** - Ask for numbered lists, sections
3. **Provide context** - Mention relevant files or patterns to consider
4. **Set constraints** - Specify technologies, patterns, or limits
5. **Ask for reasoning** - Request explanations for recommendations

## Gemini's Built-in Tools

Gemini CLI has these capabilities (auto-approved with `-y`):

| Tool | Description |
|------|-------------|
| `read_file` | Read file contents |
| `write_file` | Create/overwrite files |
| `edit_file` | Modify existing files |
| `shell` | Execute shell commands |
| `web_search` | Google Search grounding |
| `web_fetch` | Fetch web content |

## Error Handling

- Non-zero exit code indicates failure
- Check `stats.tools.totalFail` for tool errors
- Stderr may contain MCP warnings (usually ignorable)

## Collaboration Pattern

When working with Gemini as a partner:

1. **Claude initiates** - Formulate the request and invoke Gemini
2. **Gemini executes** - Performs analysis/generation with 1M context
3. **Claude reviews** - Evaluate Gemini's output and integrate
4. **Iterate if needed** - Refine with follow-up prompts

## See Also

- [prompts.md](prompts.md) - Curated prompt templates
- [examples.md](examples.md) - Real-world usage examples
- Docs/Gemini_CLI/ - Full Gemini CLI documentation
