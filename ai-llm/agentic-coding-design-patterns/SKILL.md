---
name: agentic-coding-design-patterns
description: AI SDLC patterns catalog for working effectively with AI coding agents
triggers:
  - how do I work better with AI coding agents
  - show me agentic coding patterns
  - what are best practices for AI-assisted development
  - how to structure tasks for AI agents
  - agentic coding design patterns
  - AI SDLC patterns and anti-patterns
  - improve my workflow with coding agents
  - patterns for working with AI assistants
---

# Agentic Coding Design Patterns

> Skill by [ara.so](https://ara.so) — Design Skills collection.

A comprehensive catalog of patterns and anti-patterns for working effectively with AI coding agents, inspired by the "Gang of Four" design patterns. This project documents proven approaches for task setting, context management, verification, and project organization when collaborating with AI.

## What This Project Does

The Agentic Coding Design Patterns catalog provides:

- **Structured patterns** for AI-assisted development workflows
- **Anti-patterns** to avoid common pitfalls
- **Multi-language support** (English, Russian, Spanish)
- **PDF/EPUB export** for offline reading
- **Pattern categories**: task setting, context management, verification, project organization

Built with [HonKit](https://github.com/honkit/honkit) as a multi-language book with print capabilities.

## Installation

```bash
# Clone the repository
git clone https://github.com/mokevnin/agentic-coding-design-patterns.git
cd agentic-coding-design-patterns

# Install dependencies
npm install
```

## Key Commands

### Development & Preview

```bash
# Start local development server with live reload
npm start

# Build static site to ./dist
npm run build

# Generate PDF for a specific locale (requires Calibre/ebook-convert)
npm run pdf:ru
npm run pdf:en
npm run pdf:es
```

### Project Structure

```
book/                 # Book root (HonKit)
  book.json           # HonKit configuration
  LANGS.md            # Language list for multilingual support
  <locale>/           # Language-specific content (ru, en, es)
    SUMMARY.md        # Table of contents (groups = headings, patterns = links)
    README.md         # Locale landing page
    <slug>.md         # Individual pattern chapters (flat structure)
  assets/<slug>/      # Shared diagrams and code samples
templates/<locale>/   # Localized pattern and anti-pattern templates
```

## Configuration

### HonKit Configuration (`book/book.json`)

```json
{
  "title": "Agentic Coding Design Patterns",
  "language": "en",
  "plugins": [
    "theme-default",
    "-sharing",
    "sitemap",
    "multilingual"
  ],
  "pluginsConfig": {
    "sitemap": {
      "hostname": "https://mokevnin.github.io/agentic-coding-design-patterns/"
    }
  }
}
```

### Language Configuration (`book/LANGS.md`)

```markdown
* [Русский](ru/)
* [English](en/)
* [Español](es/)
```

## Pattern Structure

### Creating a New Pattern

Each pattern follows a consistent markdown structure:

```markdown
# Pattern Name

## Context
Description of when this pattern applies

## Problem
The challenge this pattern addresses

## Solution
How to implement the pattern

## Example
Concrete code or workflow examples

## Consequences
Benefits and trade-offs

## Related Patterns
Links to similar or complementary patterns
```

### Pattern Template Usage

```bash
# Use locale-specific templates
templates/en/pattern.md        # English pattern template
templates/en/anti-pattern.md   # English anti-pattern template
templates/ru/pattern.md        # Russian pattern template
```

### Adding a Pattern to Table of Contents

Edit `book/<locale>/SUMMARY.md`:

```markdown
# Summary

* [Introduction](README.md)

## Task Setting Patterns
* [Clear Scope Definition](clear-scope-definition.md)
* [Incremental Task Breakdown](incremental-task-breakdown.md)

## Context Management Patterns
* [Context Window Optimization](context-window-optimization.md)

## Anti-Patterns
* [Over-Prompting](over-prompting.md)
```

## Working with Translations

The canonical locale is **Russian (`ru`)** — patterns are first written in Russian, then translated to English and Spanish.

### Translation Workflow

1. Create pattern in `book/ru/<slug>.md`
2. Add entry to `book/ru/SUMMARY.md`
3. Translate to `book/en/<slug>.md` (same slug)
4. Translate to `book/es/<slug>.md` (same slug)
5. Update `SUMMARY.md` for each locale
6. Share assets in `book/assets/<slug>/`

### Referencing Shared Assets

```markdown
<!-- In any locale, reference shared assets -->
![Diagram](../assets/pattern-name/diagram.png)

```python
# Reference shared code samples
# See: ../assets/pattern-name/example.py
```

## Common Patterns for AI Agent Collaboration

### 1. Task Setting Patterns

**Clear Scope Definition**: Define explicit boundaries, success criteria, and constraints before starting work.

```markdown
Example task:
- Objective: Implement user authentication
- Scope: Email/password only, no OAuth
- Constraints: Use existing DB schema, <100 LOC
- Success: Tests pass, PR approved
```

**Incremental Task Breakdown**: Split large tasks into verifiable increments.

```markdown
Phase 1: Database migration
Phase 2: Backend API endpoints
Phase 3: Frontend integration
Phase 4: Tests and documentation
```

### 2. Context Management Patterns

**Context Window Optimization**: Provide relevant context without overwhelming the agent.

```bash
# Good: Targeted context
git diff main..feature -- src/auth/

# Avoid: Dumping entire codebase
cat **/*.py | pbcopy
```

**Selective File Inclusion**: Include only files relevant to the current task.

```markdown
Focus files:
- src/auth/login.py (modify)
- tests/test_auth.py (add tests)
- docs/api.md (update)
```

### 3. Verification Patterns

**Incremental Validation**: Verify each step before proceeding.

```bash
# After each change
npm test
npm run lint
git diff --check
```

**Explicit Acceptance Criteria**: Define testable success conditions.

```markdown
Acceptance criteria:
- [ ] All tests pass
- [ ] No linting errors
- [ ] API response time < 200ms
- [ ] Documentation updated
```

### 4. Project Organization Patterns

**Flat Pattern Structure**: Keep patterns as flat files for easy GitHub browsing.

```
book/en/
  pattern-one.md
  pattern-two.md
  anti-pattern-one.md
```

**Localized Templates**: Provide consistent structure across languages.

```bash
cp templates/en/pattern.md book/en/new-pattern.md
# Edit book/en/new-pattern.md
# Add to book/en/SUMMARY.md
```

## Anti-Patterns to Avoid

### Over-Prompting
Providing excessive detail that confuses rather than clarifies.

### Context Dumping
Sharing entire codebases without filtering for relevance.

### Vague Requirements
Asking for features without clear success criteria or constraints.

### Skipping Verification
Moving to the next task without validating the current output.

## Troubleshooting

### HonKit Build Fails

```bash
# Clear cache and rebuild
rm -rf _book dist
npm run build
```

### PDF Generation Issues

```bash
# Ensure Calibre is installed
# macOS
brew install --cask calibre

# Ubuntu/Debian
sudo apt-get install calibre

# Then generate PDF
npm run pdf:en
```

### Missing Translations

If a pattern exists in `ru/` but not `en/`:

```bash
# Check SUMMARY.md for missing entries
diff book/ru/SUMMARY.md book/en/SUMMARY.md

# Copy and translate
cp book/ru/pattern.md book/en/pattern.md
# Edit book/en/pattern.md for translation
```

### Live Reload Not Working

```bash
# Kill existing HonKit process
pkill -f honkit

# Restart
npm start
```

## Contributing Patterns

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:

- Pattern naming conventions (slug format)
- Required sections for patterns
- Translation workflow
- Asset organization
- Pull request process

## Resources

- **Online Documentation**: https://mokevnin.github.io/agentic-coding-design-patterns/
- **Repository**: https://github.com/mokevnin/agentic-coding-design-patterns
- **License**: Text/diagrams under CC BY-SA 4.0, code samples under CC0

## Example: Adding a New Pattern

```bash
# 1. Create pattern in canonical locale (Russian)
cp templates/ru/pattern.md book/ru/efficient-prompting.md

# 2. Edit the pattern
vim book/ru/efficient-prompting.md

# 3. Add to Russian table of contents
vim book/ru/SUMMARY.md
# Add: * [Efficient Prompting](efficient-prompting.md)

# 4. Translate to English
cp templates/en/pattern.md book/en/efficient-prompting.md
vim book/en/efficient-prompting.md

# 5. Update English TOC
vim book/en/SUMMARY.md

# 6. Preview changes
npm start

# 7. Build and verify
npm run build
```

This catalog helps AI coding agents understand and apply proven patterns for effective human-AI collaboration in software development.
