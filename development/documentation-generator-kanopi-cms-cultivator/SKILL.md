---
name: documentation-generator
description: Automatically generate documentation when user mentions needing API docs, README files, user guides, developer guides, or changelogs. Analyzes code and generates appropriate documentation based on context. Invoke when user mentions "document", "docs", "README", "API documentation", "guide", "changelog", or "how to document".
---

# Documentation Generator

Automatically generate documentation for code, APIs, and projects.

## When to Use This Skill

Activate this skill when the user:
- Says "I need to document this"
- Asks "how do I write docs for this API?"
- Mentions "README", "documentation", or "user guide"
- Shows code and asks "what docs should I write?"
- Says "need API documentation"
- Asks about changelog or release notes
- Mentions "developer guide" or "setup instructions"

## Workflow

### 1. Determine Documentation Type

**API Documentation** - For code interfaces:
- Functions, methods, classes
- Parameters and return types
- Examples and usage

**README** - For project overview:
- Installation instructions
- Quick start guide
- Features and requirements

**User Guide** - For end users:
- How to use features
- Screenshots and examples
- Troubleshooting

**Developer Guide** - For contributors:
- Architecture overview
- Setup and development
- Coding standards

**Changelog** - For releases:
- Version history
- What changed
- Migration guides

### 2. Analyze the Code/Project

**For API Docs**:
- Scan function signatures
- Identify parameters and return types
- Find existing comments
- Detect dependencies

**For README**:
- Check for package managers (composer.json, package.json)
- Identify framework (Drupal, WordPress, etc.)
- Find entry points and main features

**For Guides**:
- Understand user workflows
- Identify key features
- Note prerequisites

## Documentation Templates

Complete templates are available for reference:

- **[API Documentation Templates](templates/api-docs.md)** - PHPDoc/JSDoc for Drupal & WordPress
- **[README Template](templates/readme.md)** - Complete project README structure
- **[User Guide Template](templates/user-guide.md)** - End-user documentation
- **[Changelog Template](templates/changelog.md)** - Version history (Keep a Changelog format)

Use these templates as starting points, customizing for the specific project needs.

## Generation Strategy

### 1. Gather Information

Ask clarifying questions:
- "What documentation type do you need?"
- "Who is the audience? (developers, end users, admins?)"
- "What specific features should be documented?"

### 2. Analyze Code

For API docs:
- Read function signatures
- Extract existing comments
- Identify dependencies
- Find usage examples

### 3. Structure Document

Follow standard patterns:
- Overview/introduction
- Prerequisites
- Main content (organized logically)
- Examples
- Troubleshooting
- Resources

### 4. Add Examples

Include:
- Code examples
- Screenshots (placeholder references)
- Before/after comparisons
- Common use cases

## Integration with CMS Cultivator

This skill complements the `/docs-generate` slash command:

- **This Skill**: Automatically triggered during conversation
  - "How do I document this function?"
  - "Need docs for this API"
  - Quick single-function documentation

- **`/docs-generate` Command**: Explicit batch generation
  - Generate full project documentation
  - Create comprehensive README
  - Build complete user guides

## Quick Response Patterns

### For API Documentation

When user shows a class or function:

1. Identify the type (Drupal service, WordPress function, JS module)
2. Generate appropriate docblock format
3. Include:
   - Description of purpose
   - Parameter documentation
   - Return type documentation
   - Usage example in @code block
   - Related functions (@see tags)

### For README

When user asks for project documentation:

1. Scan project structure (composer.json, package.json)
2. Identify platform (Drupal/WordPress/standalone)
3. Generate sections in order:
   - Title and description
   - Features list
   - Requirements
   - Installation (Composer first)
   - Quick start example
   - Links to detailed docs

### For User Guides

When user needs end-user documentation:

1. Ask about target audience
2. Identify main workflows
3. Structure with:
   - Overview
   - Prerequisites checklist
   - Step-by-step instructions
   - Screenshots placeholders
   - Troubleshooting section
   - FAQs

### For Changelogs

When user needs version history:

1. Use Keep a Changelog format
2. Categories: Added, Changed, Deprecated, Removed, Fixed, Security
3. Include version numbers and dates
4. Link to GitHub comparisons

## Example Interactions

**Example 1: API documentation**
```
User: "I need to document this service class"
[Shows DataProcessor class]

Skill: "I'll generate API documentation for your DataProcessor service.
I see it has 3 public methods and uses dependency injection.
I'll create docblocks with:
- Class description with usage example
- Constructor documentation
- Method documentation with @param and @return
- @code examples for each method

[Generates documented code following Drupal standards]

This follows Drupal documentation standards. Each method includes
parameter types, return types, and usage examples."
```

**Example 2: README**
```
User: "Need a README for my custom module"

Skill: "I'll create a comprehensive README for your module.
Let me check the project structure...

I see:
- Drupal 10 module
- Composer-based
- Custom services and admin routes

I'll generate a README with:
- Installation via Composer
- Feature list
- Configuration steps
- API usage examples
- Links to extended docs

[Generates README.md]"
```

**Example 3: Changelog Entry**
```
User: "What should I add to CHANGELOG for this release?"

Skill: "Based on your recent commits, I'll generate a changelog entry
following Keep a Changelog format:

## [1.2.0] - 2025-01-15

### Added
- User profile export functionality (#234)
- Bulk operations support

### Changed
- Improved query performance (30% faster)

### Fixed
- Permission check on admin pages (#145)

Would you like me to add this to your CHANGELOG.md?"
```

## Best Practices

1. **Clear and Concise** - Write for your audience's level
2. **Examples** - Always include working code examples
3. **Up to Date** - Document current functionality, not planned features
4. **Structured** - Use consistent headings and format
5. **Searchable** - Include keywords users will search for
6. **Complete** - Cover common use cases and edge cases

## Platform-Specific Guidelines

### Drupal Documentation
- Use PHPDoc format with @param, @return, @throws
- Include @code examples in docblocks
- Document services with usage examples
- Reference related APIs with @see tags
- Follow Drupal API documentation standards

### WordPress Documentation
- Use PHPDoc with @since tags
- Document hooks and filters
- Include usage examples in docblocks
- Reference WordPress functions
- Follow WordPress inline documentation standards

### JavaScript Documentation
- Use JSDoc format
- Document parameters and return types
- Include examples
- Document React components with PropTypes
- Follow project-specific standards (ESDoc, TSDoc)

## Resources

- [Write the Docs](https://www.writethedocs.org/)
- [Drupal Documentation Standards](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards)
- [WordPress Inline Documentation Standards](https://developer.wordpress.org/coding-standards/inline-documentation-standards/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
