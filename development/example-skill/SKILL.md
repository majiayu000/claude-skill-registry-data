---
name: example-skill
description: Demonstrates proper skill structure and frontmatter format for marketplace skills
version: 1.0.0
author: Skills Marketplace Team
category: examples
tags:
  - template
  - documentation
  - best-practices
license: MIT
---

# Example Skill

This skill demonstrates the proper structure and documentation format for Skills Marketplace submissions.

## Purpose

Use this skill as a **template** when creating your own skills. It shows:

- ✅ Proper YAML frontmatter format
- ✅ Required and optional fields
- ✅ Clear documentation structure
- ✅ Usage examples
- ✅ Best practices

## Features

- **Complete frontmatter** - Shows all recommended fields
- **Clear documentation** - Well-organized sections
- **Usage examples** - Demonstrates how to use the skill
- **Best practices** - Follows marketplace guidelines

## Installation

```bash
# Add the marketplace
/plugin marketplace add token-eater/skills-marketplace

# Install this example skill
/plugin install example-skill
```

## Usage

This is an example skill for demonstration purposes. In a real skill, this section would explain:

1. **How to use the skill** - Step-by-step instructions
2. **Commands** - Specific commands or workflows
3. **Configuration** - Any setup required
4. **Tips** - Helpful usage tips

### Example Usage

```bash
# Example command (this is a template - replace with real usage)
/skill example-skill --help
```

## Structure

This skill follows the standard marketplace structure:

```
skills/example-skill/
├── SKILL.md           # This file (required)
├── scripts/           # Optional: Helper scripts
├── references/        # Optional: Reference documentation
└── assets/            # Optional: Images, templates, etc.
```

## Frontmatter Fields

### Required Fields

```yaml
name: example-skill              # Unique identifier (kebab-case)
description: Brief description   # 1-2 sentence summary
version: 1.0.0                  # Semantic version (X.Y.Z)
author: Author Name             # Your name or organization
category: examples              # Primary category
tags:                           # 2-5 searchable keywords
  - template
  - documentation
```

### Optional Fields

```yaml
license: MIT                    # License type
repository: https://github...   # Source code URL
homepage: https://example.com   # Documentation URL
dependencies:                   # Required tools/packages
  - tool-name
```

## Categories

Choose the most appropriate category for your skill:

- `productivity` - Task management, workflows, automation
- `development` - Git, testing, code quality, deployment
- `data` - Data processing, visualization, reporting
- `documentation` - Markdown, diagrams, API docs
- `devops` - CI/CD, containers, infrastructure
- `ai-ml` - AI/ML integration, training, evaluation
- `security` - Security scanning, verification, compliance
- `web` - Web scraping, APIs, frontend tools
- `knowledge` - Research, memory, note-taking
- `examples` - Templates and learning resources

## Best Practices

### Documentation

- ✅ Write clear, concise descriptions
- ✅ Include usage examples
- ✅ Document all dependencies
- ✅ Provide troubleshooting tips

### Structure

- ✅ Keep skills focused (single purpose)
- ✅ Use semantic versioning
- ✅ Organize files logically
- ✅ Include only necessary files

### Security

- ⚠️ Never hardcode API keys or secrets
- ⚠️ Never commit credentials
- ✅ Document how to configure secrets
- ✅ Use `.gitignore` for sensitive files

## Contributing

To create your own skill based on this example:

1. **Copy the structure**:
   ```bash
   cp -r skills/example-skill skills/your-skill-name
   ```

2. **Update SKILL.md**:
   - Change frontmatter fields (name, description, etc.)
   - Write your skill documentation
   - Add usage examples

3. **Test locally**:
   ```bash
   /plugin marketplace add ./skills-marketplace
   /plugin install your-skill-name
   ```

4. **Submit**: See [Contributing Guide](../../docs/contributing.md)

## Resources

- 📖 [Creating Skills Guide](../../docs/creating-skills.md)
- 🤝 [Contributing Guide](../../docs/contributing.md)
- 📥 [Installation Guide](../../docs/installation.md)
- 🏗️ [Architecture Guide](../../docs/architecture.md)

## License

MIT License - Free to use, modify, and distribute.

## Support

- 💬 [GitHub Discussions](https://github.com/token-eater/skills-marketplace/discussions)
- 🐛 [Report Issues](https://github.com/token-eater/skills-marketplace/issues)

---

**Ready to create your own skill?** Use this as a template and see the [Creating Skills Guide](../../docs/creating-skills.md) for detailed instructions.
