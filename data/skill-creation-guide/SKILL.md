---
name: skill-creation-guide
description: Complete comprehensive guide for creating, managing, and optimizing Claude Code Skills. Reference documentation covering structure, API usage, examples, best practices, and troubleshooting.
version: 1.0.0
---

# Claude Code Skills Creation Guide

Complete reference documentation for creating, managing, and optimizing Claude Code Skills.

## What are Claude Code Skills?

Skills are modular capabilities that extend Claude's functionality through organized folders containing instructions, scripts, and resources. They allow you to teach Claude your specific workflows, patterns, and domain expertise in a repeatable, efficient way.

**Key Benefits:**
- Autonomous activation based on context
- Token-efficient with progressive disclosure
- Reusable across projects
- Shareable with teams
- Version controllable

## Documentation Structure

This guide is modularized for easy reference:

### **getting-started.md**
First steps for creating your first skill
- Installation and setup
- Using skill-creator for interactive creation
- Manual skill creation
- Testing your first skill

### **structure.md**
Technical specifications and file organization
- Directory structure patterns
- SKILL.md format and YAML frontmatter
- REFERENCE.md for supplemental content
- Resources and scripts organization
- Progressive disclosure architecture

### **api-usage.md**
Programmatic access and team integration
- Messages API integration
- /v1/skills endpoint usage
- Team sharing strategies
- Version management
- Enterprise deployment

### **examples.md**
Real-world use cases and implementations
- Official Anthropic skills repository examples
- Document processing (PDF, Excel, Word, PowerPoint)
- Brand guidelines enforcement
- Workflow automation
- Community examples

### **best-practices.md**
Performance optimization and efficiency
- Token usage optimization
- Description writing guidelines
- Context management
- When to split content into multiple files
- Security considerations

### **troubleshooting.md**
Common issues and solutions
- Installation problems
- Skill not activating
- Testing and debugging
- Performance issues
- Reloading skills

## Quick Reference

**Installation Locations:**
- Personal Skills: `~/.claude/skills/` (all projects)
- Project Skills: `.claude/skills/` (team shared)

**Activation:**
- Automatic based on description match
- No manual invocation required
- Up to 8 skills per request (API)

**Reload Skills:**
```bash
/reload-skills
```

**Official Resources:**
- GitHub: https://github.com/anthropics/skills
- Docs: https://docs.claude.com/en/docs/claude-code/skills
- API: https://docs.claude.com/en/api/skills-guide

## Minimum Requirements

A skill requires only:
1. A directory with your skill name
2. A `SKILL.md` file with YAML frontmatter:

```markdown
---
name: your-skill-name
description: What it does and when to use it
---

# Your Skill Name

[Your instructions here]
```

## Next Steps

1. **New to Skills?** Start with `getting-started.md`
2. **Creating Custom Skills?** Review `structure.md`
3. **Team Deployment?** Check `api-usage.md`
4. **Need Examples?** Browse `examples.md`
5. **Optimizing Performance?** Read `best-practices.md`
6. **Troubleshooting?** See `troubleshooting.md`

---

*Last Updated: 2025-10-21*
*Based on official Anthropic documentation and community best practices*
