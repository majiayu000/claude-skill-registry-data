---
name: multi-agent-ai-projects
description: Guidelines for multi-agent AI and learning projects with lesson-based structures. Activate when working with AI learning projects, experimental directories like .spec/, lessons/ directories, STATUS.md progress tracking, or structured learning curricula with multiple modules or lessons.
---

# Multi-Agent AI Projects

Guidelines for working with multi-agent AI learning projects and experimental codebases.

## Project Structure Recognition

### Common Patterns
- `.spec/` directory - Learning specifications and experimental code
- `lessons/` or similar learning directories
- `STATUS.md` - Progress tracking for learning journey
- Per-lesson or per-module structure
- Self-contained lesson directories

## Workflow Patterns

### Before Starting Work
1. **Check for `STATUS.md`** - Understand current progress and next steps
2. **Identify lesson structure** - Each lesson may be self-contained
3. **Check for lesson-specific dependencies** - Each module might have its own requirements
4. **Look for `.env` files per lesson** - API keys typically organized by lesson

### Execution Patterns
- Use `uv run python` for execution (most AI projects use modern Python tooling)
- Each lesson may have its own virtual environment or shared venv
- Check lesson README for specific setup instructions

### API Keys and Secrets
- API keys typically in per-lesson `.env` files
- Each lesson might require different API credentials
- Always check `.env.example` or `.env.template` in lesson directories
- Never commit `.env` files

## Progress Tracking

### STATUS.md Pattern
- Update after completing lessons
- Note blockers and next steps
- Document learnings and insights
- Track which lessons are complete

### Session Management
- Always check STATUS.md before starting
- Update STATUS.md before ending sessions
- Note any experimental findings

## Common Project Types

### Learning Spike Projects
- Focus on exploration and experimentation
- Code may not be production-quality
- Documentation of learnings is important
- Test different approaches

### Multi-Agent Frameworks
- Agent coordination patterns
- Tool usage and integration
- Message passing between agents
- State management across agents

## Quick Reference

**Always check:**
- ✅ STATUS.md for current progress
- ✅ Lesson-specific README files
- ✅ Per-lesson .env files
- ✅ .spec/ or lessons/ directory structure

**Execution:**
- Use `uv run python` for modern projects
- Check for per-lesson dependencies
- Respect lesson isolation if present

**Documentation:**
- Update STATUS.md with progress
- Document experimental findings
- Note what worked and what didn't

---

**Note:** These projects are often learning-focused - prioritize understanding and documentation over production perfection.
