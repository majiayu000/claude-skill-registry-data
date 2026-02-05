---
name: sc-implement
description: Feature implementation with intelligent persona activation, task orchestration, and MCP integration. Use when implementing features, APIs, components, services, or coordinating multi-agent development. Triggers on requests for code implementation, feature development, or complex task orchestration.
---

# Implementation Skill

Comprehensive feature implementation with coordinated expertise and systematic development.

## Quick Start

```bash
# Basic implementation
/sc:implement [feature-description] --type component|api|service|feature

# With framework
/sc:implement dashboard widget --framework react|vue|express

# Complex orchestration
/sc:implement [task] --orchestrate --strategy systematic|agile|enterprise
```

## Behavioral Flow

1. **Analyze** - Examine requirements, detect technology context
2. **Plan** - Choose approach, activate relevant personas
3. **Generate** - Create implementation with framework best practices
4. **Validate** - Apply security and quality validation
5. **Integrate** - Update docs, provide testing recommendations

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--type` | string | feature | component, api, service, feature |
| `--framework` | string | auto | react, vue, express, etc. |
| `--safe` | bool | false | Enable safety constraints |
| `--with-tests` | bool | false | Generate tests alongside code |
| `--fast-codex` | bool | false | Streamlined path, skip multi-persona |
| `--orchestrate` | bool | false | Enable hierarchical task breakdown |
| `--strategy` | string | systematic | systematic, agile, enterprise, parallel, adaptive |
| `--delegate` | bool | false | Enable intelligent delegation |

## Personas Activated

- **architect** - System design, architectural decisions
- **frontend** - UI/component implementation
- **backend** - API/service implementation
- **security** - Security validation, auth concerns
- **qa-specialist** - Testing, quality assurance
- **devops** - Infrastructure, deployment
- **project-manager** - Task coordination (with --orchestrate)

## MCP Integration

- **PAL MCP** - Consensus for architectural/security decisions
- **Rube MCP** - External automation (ticketing, CI hooks)

## Guardrails

- Start in analysis mode; produce scoped plan before touching files
- Only mark complete when referencing concrete repo changes (filenames + diff hunks)
- Return plan + next actions if tooling unavailable
- Prefer minimal viable change; skip speculative scaffolding
- Escalate to security persona before modifying auth/secrets/permissions

## Evidence Requirements

This skill requires evidence. You MUST:
- Show actual file diffs or code changes
- Reference test results or lint output
- Never claim code exists without proof

## Examples

### React Component
```
/sc:implement user profile component --type component --framework react
```

### API with Tests
```
/sc:implement user auth API --type api --safe --with-tests
```

### Complex Orchestration
```
/sc:implement "enterprise auth system" --orchestrate --strategy systematic --delegate
```

## Loop Mode & Learning

When using `--loop`, this skill integrates with the skill persistence layer for cross-session learning:

### How Learning Works

1. **Feedback Recording** - Each iteration's quality scores and improvements are persisted
2. **Skill Extraction** - Successful patterns are extracted when quality threshold is met
3. **Skill Retrieval** - Relevant learned skills are injected into subsequent tasks
4. **Effectiveness Tracking** - Applied skills are tracked for success rate

### Loop Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--loop` | int | 3 | Enable iterative improvement (max 5) |
| `--learn` | bool | true | Enable learning from this session |
| `--auto-promote` | bool | false | Auto-promote high-quality skills |

### Example with Learning

```bash
# Iterative implementation with learning
/sc:implement auth flow --loop 3 --learn

# View learned skills
python scripts/skill_learn.py '{"command": "stats"}'

# Retrieve relevant skills
python scripts/skill_learn.py '{"command": "retrieve", "task": "auth"}'
```

### Learned Skills Location

Promoted skills are stored in:
```
.claude/skills/learned/
├── SKILL.md                    # Index
├── learned-backend-auth/       # Example promoted skill
│   ├── SKILL.md
│   └── metadata.json
```

## Resources

- [PERSONAS.md](PERSONAS.md) - Available persona definitions
- [scripts/select_agent.py](scripts/select_agent.py) - Agent selection logic
- [scripts/evidence_gate.py](scripts/evidence_gate.py) - Evidence validation
- [scripts/skill_learn.py](scripts/skill_learn.py) - Skill learning management
