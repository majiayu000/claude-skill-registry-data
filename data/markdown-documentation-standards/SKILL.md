---
name: Markdown Documentation Standards
description: Professional markdown writing standards for documentation and content creation
version: 1.0.0
source: github.com/github/awesome-copilot/instructions/markdown.instructions.md
---

# Markdown Documentation Standards

## When to Use
This skill auto-activates when working on markdown files and provides comprehensive guidelines for creating professional, accessible, and well-structured documentation.

## Purpose
Enforce documentation and content creation standards for all markdown files in the project.

---

## Core Markdown Rules

### 1. Heading Hierarchy
- **Never use H1 (`#`)** - H1 is auto-generated from the document title
- **Use H2 (`##`) for main sections** - Primary organizational level
- **Use H3 (`###`) for subsections** - Secondary organizational level
- **Avoid H4 and beyond** - If needed, consider restructuring content
- **Maintain proper hierarchy** - Don't skip levels (e.g., H2 → H4)

**Example:**
```markdown
## Main Section (H2)

### Subsection (H3)

Content here...

### Another Subsection (H3)

More content...

## Another Main Section (H2)
```

### 2. Lists
- **Use `-` for bullet points** - Consistent bullet style
- **Use `1.` for numbered lists** - Auto-incrementing numbers
- **Indent nested lists with two spaces** - Visual hierarchy
- **Add blank line before and after lists** - Improved readability

**Example:**
```markdown
Main list:
- First item
- Second item
  - Nested item
  - Another nested item
- Third item

Numbered list:
1. First step
2. Second step
3. Third step
```

### 3. Code Blocks
- **Always use fenced code blocks** - Triple backticks
- **Always specify the language** - Enable syntax highlighting
- **Use inline code for short snippets** - Backticks for inline

**Example:**
```markdown
Use inline code like `const foo = 'bar'` for short snippets.

For code blocks:

\`\`\`typescript
function greet(name: string): string {
  return `Hello, ${name}!`;
}
\`\`\`
```

### 4. Links
- **Use descriptive anchor text** - Avoid "click here" or "link"
- **Validate all URLs** - Ensure links are not broken
- **Use proper markdown syntax** - `[text](URL)`
- **Include tooltips when helpful** - `[text](URL "tooltip")`

**Example:**
```markdown
✅ Good: Read the [TypeScript documentation](https://www.typescriptlang.org/docs/)
❌ Bad: Click [here](https://www.typescriptlang.org/docs/)

With tooltip: [TypeScript docs](https://www.typescriptlang.org/docs/ "Official TypeScript documentation")
```

### 5. Images
- **Always include alt text** - Accessibility requirement
- **Use descriptive alt text** - Explain what the image shows
- **Optimize image sizes** - Balance quality and file size
- **Use proper markdown syntax** - `![alt text](image URL)`

**Example:**
```markdown
![Screenshot of the user dashboard showing the navigation menu and activity feed](./images/dashboard-screenshot.png)
```

### 6. Tables
- **Use proper table syntax** - Pipe delimiters and headers
- **Align columns consistently** - Left, center, or right
- **Include header row** - First row with `---` separator
- **Keep tables simple** - Complex data may need different format

**Example:**
```markdown
| Feature | Status | Priority |
|---------|:------:|----------|
| Authentication | ✅ Complete | High |
| User Profile | 🚧 In Progress | Medium |
| Notifications | ⏳ Planned | Low |
```

### 7. Line Length
- **Limit lines to 400 characters maximum** - Hard limit for readability
- **Break paragraphs at 80 characters** - Soft break for better diffs
- **Don't break URLs or code** - Keep on single line
- **Use semantic line breaks** - Break at sentence or clause boundaries

**Example:**
```markdown
This is a long paragraph that should be broken at approximately 80 characters
per line. This makes it easier to read diffs and maintains good version control
practices. Each sentence or major clause can start on a new line.
```

### 8. Whitespace
- **Use blank lines between sections** - Visual separation
- **One blank line is sufficient** - Avoid excessive spacing
- **No trailing whitespace** - Clean up line endings
- **Consistent indentation** - Two spaces for nested content

**Example:**
```markdown
## Section One

Content for section one.

## Section Two

Content for section two.
```

### 9. Front Matter
Include YAML front matter at the beginning of documents for metadata:

**Required Fields:**
- `post_title` - Document heading
- `author1` - Primary author name
- `post_slug` - URL-friendly slug
- `microsoft_alias` - Author's identifier (adapt to your organization)
- `featured_image` - Featured image URL or path
- `categories` - Document categories (from controlled list)
- `tags` - Searchable tags
- `ai_note` - Indicator if AI was used in creation
- `summary` - Brief document synopsis (1-2 sentences)
- `post_date` - Publication date (YYYY-MM-DD)

**Example:**
```markdown
---
post_title: "Getting Started with TypeScript"
author1: "Jane Doe"
post_slug: "getting-started-typescript"
microsoft_alias: "jdoe"
featured_image: "./images/typescript-hero.png"
categories: ["Development", "TypeScript"]
tags: ["typescript", "tutorial", "beginners"]
ai_note: "AI-assisted writing"
summary: "A beginner-friendly guide to setting up and using TypeScript in your projects."
post_date: 2025-01-15
---

## Introduction

Content starts here...
```

---

## Best Practices

### Documentation Structure
1. **Start with a clear introduction** - What is this document about?
2. **Use consistent heading hierarchy** - Maintain logical structure
3. **Include a table of contents for long docs** - Easy navigation
4. **Add examples liberally** - Show, don't just tell
5. **End with references or next steps** - Guide the reader forward

### Writing Style
- **Use active voice** - "Run the command" not "The command should be run"
- **Be concise and clear** - Remove unnecessary words
- **Use consistent terminology** - Don't alternate between synonyms
- **Write for your audience** - Adjust technical level appropriately
- **Proofread before committing** - Check spelling and grammar

### Accessibility
- **Provide alt text for images** - Screen reader support
- **Use semantic HTML when needed** - Proper heading levels
- **Don't rely solely on color** - Use text indicators too
- **Keep tables simple** - Complex tables are hard to navigate
- **Test with screen readers** - When possible

### Version Control
- **Use semantic line breaks** - One sentence per line
- **Keep commits focused** - One logical change per commit
- **Write clear commit messages** - Explain what changed and why
- **Review diffs before committing** - Catch formatting issues

---

## Common Mistakes to Avoid

❌ **Don't:**
- Skip heading levels (H2 → H4)
- Use H1 in document body
- Write "click here" as link text
- Omit alt text from images
- Create overly long lines
- Use excessive blank lines
- Mix bullet styles in same list
- Forget language specifiers in code blocks

✅ **Do:**
- Maintain proper heading hierarchy
- Use H2 as top level in body
- Write descriptive link text
- Include meaningful alt text
- Break lines at sensible points
- Use consistent spacing
- Stick to one bullet style
- Always specify code language

---

## Validation Checklist

Before committing markdown files, verify:

- [ ] No H1 headings in document body
- [ ] Proper heading hierarchy (no skipped levels)
- [ ] All code blocks have language specifiers
- [ ] All links use descriptive anchor text
- [ ] All images have alt text
- [ ] Lines are under 400 characters
- [ ] Consistent blank line spacing
- [ ] Front matter is complete (if required)
- [ ] Tables are properly formatted
- [ ] No trailing whitespace
- [ ] Proper list indentation
- [ ] Spell check completed

---

## Examples

### Complete Document Example

```markdown
---
post_title: "API Authentication Guide"
author1: "John Smith"
post_slug: "api-authentication-guide"
microsoft_alias: "jsmith"
featured_image: "./images/api-auth.png"
categories: ["API", "Security"]
tags: ["authentication", "api", "security", "jwt"]
ai_note: "Human-written"
summary: "Comprehensive guide to implementing authentication in REST APIs."
post_date: 2025-01-15
---

## Introduction

This guide covers authentication strategies for REST APIs, focusing on
JWT-based authentication and best practices for secure implementation.

## Authentication Methods

### Token-Based Authentication

Token-based authentication uses cryptographic tokens to verify user identity:

- **Stateless** - No server-side session storage required
- **Scalable** - Works well with distributed systems
- **Flexible** - Can include custom claims and metadata

### Implementation Example

Here's a basic JWT authentication flow:

\`\`\`typescript
import jwt from 'jsonwebtoken';

interface TokenPayload {
  userId: string;
  email: string;
  role: string;
}

function generateToken(payload: TokenPayload): string {
  return jwt.sign(payload, process.env.JWT_SECRET!, {
    expiresIn: '24h'
  });
}

function verifyToken(token: string): TokenPayload {
  return jwt.verify(token, process.env.JWT_SECRET!) as TokenPayload;
}
\`\`\`

## Security Best Practices

Follow these guidelines to ensure secure authentication:

1. **Use HTTPS only** - Never send tokens over unencrypted connections
2. **Set appropriate expiration** - Balance security and user experience
3. **Rotate secrets regularly** - Change signing keys periodically
4. **Validate all inputs** - Prevent injection attacks

## Comparison Table

| Method | Security | Complexity | Scalability |
|--------|:--------:|:----------:|:-----------:|
| JWT | High | Medium | Excellent |
| Session | Medium | Low | Good |
| OAuth 2.0 | Very High | High | Excellent |

## Next Steps

To implement authentication in your project:

- Review the [JWT documentation](https://jwt.io/introduction)
- Set up environment variables for secrets
- Implement token refresh mechanism
- Add rate limiting to authentication endpoints

For more information, see the [Security Best Practices Guide](./security-guide.md).
```

---

## Tool Integration

### Recommended Linters
- **markdownlint** - Comprehensive markdown linting
- **remark** - Markdown processor with plugins
- **vale** - Prose linting for style consistency

### Editor Extensions
- **Markdown All in One** (VS Code) - Formatting and shortcuts
- **Markdown Preview Enhanced** - Live preview with advanced features
- **Grammarly** - Grammar and spell checking

### CI/CD Integration
Add markdown linting to your CI pipeline:

```yaml
# .github/workflows/lint-docs.yml
name: Lint Documentation

on: [pull_request]

jobs:
  lint-markdown:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Lint markdown files
        uses: avto-dev/markdown-lint@v1
        with:
          args: '**/*.md'
```

---

## References

- [CommonMark Specification](https://commonmark.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Write the Docs](https://www.writethedocs.org/)

---

## Maintenance Notes

**Version History:**
- v1.0.0 (2025-01-15) - Initial skill creation from awesome-copilot instructions
- Converted from: `github.com/github/awesome-copilot/instructions/markdown.instructions.md`

**Review Schedule:** Quarterly review recommended to incorporate new best practices

**Feedback:** Submit improvements via project issue tracker
