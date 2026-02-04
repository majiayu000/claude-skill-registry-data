---
name: craft-coder-help
description: |
  Help and documentation for Craft-Coder plugin.
  Use when: user asks about available skills, commands, or how to use this plugin.
  Triggers: "help", "what can you do", "craft help", "как пользоваться".
---

# Craft-Coder: Pair Programming with a Senior Dev

Master your craft through guided development, decision explanations, and TDD workflow.

## Philosophy

**vibe-coder:** "Describe what you want" → [magic] → "Done!"

**craft-coder:** "Let's design together" → [dialogue] → "Here's why"

We explain WHAT we're doing and WHY.

## Commands

| Command | Description |
|---------|-------------|
| `/craft {project}` | Guided project creation with explanations |
| `/craft {project} --learn` | Learning mode (detailed explanations) |
| `/craft {project} --fast` | Fast mode (minimal dialogue) |
| `/why` | Explain the last decision |
| `/why stack` | Why this technology stack? |
| `/why architecture` | Why this project structure? |

## Quick Start

### Start a new project
```
/craft notes-app
```
5-step guided process:
1. Requirements gathering
2. Architecture design (with rationale)
3. Stack selection (with tradeoffs)
4. Project initialization
5. First feature implementation

### Understand decisions
```
/why
```
Explains the most recent architectural decision.

```
/why stack
```
Shows why we chose this technology stack, what alternatives were considered, and trade-offs accepted.

## Skills by Category

### Backend
| Skill | Description |
|-------|-------------|
| `backend-core` | API design, authentication, security, databases |
| `backend-python` | FastAPI, Django, SQLAlchemy, async patterns |
| `backend-nodejs` | Express, NestJS, Prisma, TypeScript backend |
| `backend-rust` | Axum, Actix, SQLx, performance-critical services |

### Frontend
| Skill | Description |
|-------|-------------|
| `frontend-react` | React 18+, hooks, state management, performance |
| `frontend-design` | Distinctive UI avoiding "AI slop" aesthetics |
| `theme-factory` | Color palettes, typography, design systems |

### Quality & Testing
| Skill | Description |
|-------|-------------|
| `code-review` | PR review workflow, technical feedback |
| `testing-core` | Unit, integration, e2e testing strategies |
| `test-driven-development` | TDD cycle: red → green → refactor |
| `testing-anti-patterns` | Common testing mistakes to avoid |

### Debugging
| Skill | Description |
|-------|-------------|
| `systematic-debugging` | Methodical bug investigation |
| `root-cause-tracing` | Find the actual source of issues |
| `defense-in-depth` | Prevent bugs from reaching production |

### Documentation
| Skill | Description |
|-------|-------------|
| `decision-logger` | Log architectural decisions (ADR format) |

## Modes

### Learning Mode (`--learn`)
- Detailed explanations for every decision
- "Why?" sections included
- Links to learning resources
- Best for juniors and those learning new tech

### Fast Mode (`--fast`)
- Skip explanations
- Use sensible defaults
- Minimal questions
- Best for experienced devs who want speed

### Balanced Mode (default)
- Key decisions explained briefly
- `/why` available for details
- Good speed/understanding balance
- Best for most developers

## Decision Records

All architectural decisions are logged to `docs/DECISIONS.md` in ADR format.

Example:
```markdown
## ADR-001: Use Rust + Axum

**Context:** Need fast API with single binary deployment

**Decision:** Rust with Axum framework

**Why:** Meets <50ms requirement, compiles to single binary

**Alternatives:** Go (less type safety), Node (not single binary)
```

## vs vibe-coder

| Aspect | vibe-coder | craft-coder |
|--------|------------|-------------|
| Decisions | Automatic | Explained |
| Errors | Auto-fix | Dialogue + options |
| Learning | Hidden | Built-in |
| Control | Minimal | Full |
| Speed | Maximum | Balanced |
| Audience | Makers | Developers |

Choose **craft-coder** when you want to:
- Understand architectural decisions
- Learn best practices
- Have control over technology choices
- Document decisions for your team

Choose **vibe-coder** when you want:
- Fastest path to MVP
- No technical decisions
- Just describe and ship
