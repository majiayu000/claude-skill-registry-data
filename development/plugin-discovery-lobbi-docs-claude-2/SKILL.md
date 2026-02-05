---
name: Plugin Discovery
description: Use when the user wants to find, search, or browse Claude Code plugins for specific functionality or use cases
version: 1.0.0
---

# Plugin Discovery

Help users find the right Claude Code plugins for their needs.

## When to Use This Skill

Activate this skill when the user:
- Asks about available plugins
- Wants to find plugins for specific functionality (e.g., "find a plugin for code formatting")
- Asks what plugins can help with a task
- Wants recommendations for plugins
- Asks about plugin categories or popular plugins

## Discovery Process

### 1. Understand the Need

Ask clarifying questions to understand:
- What problem are they trying to solve?
- What language or framework are they working with?
- Do they prefer official or community plugins?
- Any specific requirements (permissions, integrations)?

### 2. Search the Registry

Use the browse command to search:
```
/plugin-marketplace:browse <search terms>
```

### 3. Present Options

When presenting plugins, include:
- **Name** and publisher (@scope/plugin-name)
- **Description** of functionality
- **Category** (formatting, testing, AI, productivity, etc.)
- **Popularity** (downloads, ratings if available)
- **Verification status** (official, verified, community)

### 4. Provide Recommendations

Based on the user's needs, recommend:
- Best match for their use case
- Popular alternatives
- Any official Anthropic plugins that fit

## Plugin Categories

| Category | Description | Examples |
|----------|-------------|----------|
| `code-generation` | Generate code snippets and boilerplate | Templates, scaffolding |
| `code-analysis` | Analyze and review code | Linting, security scanning |
| `testing` | Testing utilities and frameworks | Test runners, mocking |
| `formatting` | Code formatting and style | Prettier, ESLint integration |
| `documentation` | Documentation generation | JSDoc, README generators |
| `git` | Git workflow enhancements | Commit messages, PR helpers |
| `ai-enhancement` | Enhance AI capabilities | Custom prompts, context |
| `productivity` | Developer productivity | Snippets, shortcuts |
| `integration` | External service integration | APIs, databases |

## Example Interactions

### User: "I need a plugin for formatting my TypeScript code"

**Response:**
I found several plugins for TypeScript formatting:

1. **@claude/code-formatter** (Official)
   - Supports TypeScript, JavaScript, and 50+ languages
   - Integrates with Prettier and ESLint
   - ⭐ Most popular formatting plugin

2. **@community/ts-prettier** (Verified)
   - Focused on TypeScript with Prettier
   - Fast and lightweight

Would you like me to show more details or install one of these?

### User: "What plugins are available for testing?"

**Response:**
Here are the top testing plugins:

1. **@claude/test-runner** - Run tests directly in Claude Code
2. **@community/jest-helper** - Jest integration with coverage
3. **@community/vitest-plugin** - Vitest support

Which testing framework are you using? I can provide more specific recommendations.

## Registry Data Format

Plugins in the registry include:
```json
{
  "name": "@scope/plugin-name",
  "description": "What the plugin does",
  "version": "1.0.0",
  "category": "category-name",
  "author": "Publisher Name",
  "verified": true,
  "downloads": 15000,
  "rating": 4.8,
  "keywords": ["tag1", "tag2"]
}
```

## Best Practices

1. **Start broad, then narrow** - Ask about general needs before specific features
2. **Prefer verified plugins** - Recommend verified/official plugins first
3. **Consider compatibility** - Check if plugins work with user's setup
4. **Explain trade-offs** - Different plugins have different strengths
5. **Offer to install** - After recommendation, offer to install the chosen plugin
