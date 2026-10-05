---
name: capability-discovery
description: Discovers available agents, skills, quality commands (lint, test, typecheck), and tech stack in the project environment. Use when starting implementation, creating PRs, reviewing PRs, or addressing feedback to determine which agents to dispatch and which quality commands to run. Use before workflow execution to adapt gh-workflow commands to project-specific tooling.
allowed-tools: Bash, Read, Glob, Grep
context: fork
agent: Explore
---

# Capability Discovery

This skill discovers available capabilities (skills, agents, commands) in the user's environment to enable dynamic workflow adaptation.

## Purpose

Before executing workflows, discover what tools are available so commands can:
- Invoke specialized agents if available
- Use custom skills instead of defaults
- Apply project-specific quality commands
- Gracefully fall back when capabilities are missing

## Discovery Process

<!--
PARALLEL EXECUTION: Steps 1-5 are fully independent. Execute ALL five
simultaneously in a single message with parallel tool calls.
Step 6 is conditional — only execute if Steps 4-5 detected a tech stack
or quality commands (see Early Exit section).
-->

### Step 1: Scan for Custom Agents

Find agent files and extract their `description` from YAML frontmatter.

**1a.** Use **Glob** (two parallel calls) to find agent files:
- `Glob: pattern=".claude/agents/*.md"` — project-level agents
- `Glob: pattern="plugins/*/agents/*.md"` — plugin agents

**1b.** Use **Grep** on discovered files to extract descriptions:
- `Grep: pattern="^description:" path="{file}" output_mode="content"`

Parse each result:
- **Source**: `project` (from `.claude/agents/`) or plugin name (from `plugins/{name}/agents/`)
- **Agent name**: filename without `.md` extension
- **Description**: text after `description: ` on the matched line

If no files found by Glob, report "No custom agents found" and continue.

### Step 2: Scan for Custom Skills

Find skill files and extract their `description` from SKILL.md frontmatter.

**2a.** Use **Glob** (two parallel calls) to find skill files:
- `Glob: pattern=".claude/skills/*/SKILL.md"` — project-level skills
- `Glob: pattern="plugins/*/skills/*/SKILL.md"` — plugin skills

**2b.** Use **Grep** on discovered files to extract descriptions:
- `Grep: pattern="^description:" path="{file}" output_mode="content"`

Parse each result:
- **Source**: `project` (from `.claude/skills/`) or plugin name (from `plugins/{name}/skills/`)
- **Skill name**: parent directory of the SKILL.md file
- **Description**: text after `description: ` on the matched line

If no files found by Glob, report "No custom skills found" and continue.

### Step 3: Scan for Custom Commands

Find command files and extract their `description` from YAML frontmatter.

**3a.** Use **Glob** (two parallel calls) to find command files:
- `Glob: pattern=".claude/commands/*.md"` — project-level commands
- `Glob: pattern="plugins/*/commands/*.md"` — plugin commands

**3b.** Use **Grep** on discovered files to extract descriptions:
- `Grep: pattern="^description:" path="{file}" output_mode="content"`

Parse each result:
- **Source**: `project` (from `.claude/commands/`) or plugin name (from `plugins/{name}/commands/`)
- **Command name**: filename without `.md` extension
- **Description**: text after `description: ` on the matched line

If no files found by Glob, report "No custom commands found" and continue.

### Step 4: Parse CLAUDE.md for Quality Commands

Check both `.claude/CLAUDE.md` and root `CLAUDE.md` (prefer `.claude/CLAUDE.md`):

```bash
# Determine CLAUDE.md path
CLAUDE_MD=""
[ -f ".claude/CLAUDE.md" ] && CLAUDE_MD=".claude/CLAUDE.md"
[ -z "$CLAUDE_MD" ] && [ -f "CLAUDE.md" ] && CLAUDE_MD="CLAUDE.md"

if [ -n "$CLAUDE_MD" ]; then
  echo "Found: $CLAUDE_MD"

  # Explicit quality command definitions (key: value format)
  grep -E "^(lint|test|check|format|typecheck|build):" "$CLAUDE_MD" 2>/dev/null

  # npm/pnpm/yarn/bun script references
  grep -E "(npm|pnpm|yarn|bun) (run )?(lint|test|check|format|build|typecheck)" "$CLAUDE_MD" 2>/dev/null

  # Python tool references
  grep -E "(ruff|pytest|poetry run|python -m pytest|mypy|pyright|black|isort|flake8|pylint)" "$CLAUDE_MD" 2>/dev/null

  # Go tool references
  grep -E "(go vet|go test|golangci-lint)" "$CLAUDE_MD" 2>/dev/null

  # Rust tool references
  grep -E "(cargo (clippy|test|fmt|check))" "$CLAUDE_MD" 2>/dev/null

  # Make targets
  grep -E "^(lint|test|check|format):" "$CLAUDE_MD" 2>/dev/null
  grep -E "make (lint|test|check|format)" "$CLAUDE_MD" 2>/dev/null
else
  echo "No CLAUDE.md found"
fi
```

### Step 5: Detect Tech Stack and Extract Config

```bash
# Detect stack and extract actionable config
[ -f "pyproject.toml" ] && echo "python" && grep -A5 '\[tool.ruff\]\|\[tool.pytest\]\|\[tool.mypy\]' pyproject.toml 2>/dev/null | head -20
[ -f "package.json" ] && echo "node" && python3 -c "import json; d=json.load(open('package.json')); [print(f'  script: {k} = {v}') for k,v in d.get('scripts',{}).items() if any(w in k for w in ['lint','test','check','build','dev','start','format','typecheck','e2e'])]" 2>/dev/null
[ -f "tsconfig.json" ] && echo "typescript"
[ -f "go.mod" ] && echo "go"
[ -f "Cargo.toml" ] && echo "rust"
[ -f "Gemfile" ] && echo "ruby"
[ -f "Makefile" ] && echo "makefile" && grep -E '^(lint|test|check|format|build|dev|serve):' Makefile 2>/dev/null
```

### Early Exit: Markdown-Only Projects

If Step 5 detected **no tech stack files** (none of pyproject.toml, package.json, tsconfig.json, go.mod, Cargo.toml, Gemfile, Makefile) and Step 4 found **no quality commands** in CLAUDE.md:

**Skip Step 6** and produce the output with:
- Quality Commands: "No code-related quality commands applicable"
- Tech Stack: "Markdown-only project (no code runtime detected)"
- Verification Capabilities: "N/A for markdown-only project"
- Recommended Workflow: Focus on agent/skill dispatch only, omit quality command recommendations

### Step 6: Discover Verification Capabilities

```bash
# Determine CLAUDE.md path
CLAUDE_MD=""
[ -f ".claude/CLAUDE.md" ] && CLAUDE_MD=".claude/CLAUDE.md"
[ -z "$CLAUDE_MD" ] && [ -f "CLAUDE.md" ] && CLAUDE_MD="CLAUDE.md"

# Check for runtime verification commands in CLAUDE.md
[ -n "$CLAUDE_MD" ] && grep -E "^(dev-server|verify|e2e|smoke|health):" "$CLAUDE_MD" 2>/dev/null

# Check for verification scripts
ls verify.sh scripts/verify* test-e2e.sh smoke-test.sh 2>/dev/null

# Check for E2E frameworks
ls playwright.config.* cypress.config.* 2>/dev/null
grep -l "playwright\|cypress\|selenium" package.json pyproject.toml 2>/dev/null

# Check for dev server in package.json scripts (proper JSON extraction)
python3 -c "import json; d=json.load(open('package.json')); [print(f'{k}: {v}') for k,v in d.get('scripts',{}).items() if k in ('dev','start','serve')]" 2>/dev/null
```

## Output Format

Report discovered capabilities in structured format. The calling command uses this output to decide which agents to dispatch, which quality commands to run, and how to adapt the workflow.

```markdown
## Discovered Capabilities

### Agents Available
| Agent | Source | Description |
|-------|--------|-------------|
| code-reviewer | gh-workflow | Code quality analysis |
| convention-checker | gh-workflow | Git convention validation |
| test-runner | gh-workflow | Quality command execution |
| implementation-planner | gh-workflow | Task breakdown from acceptance criteria |
| custom-agent | project | [extracted from frontmatter] |

### Skills Available
| Skill | Source | Description |
|-------|--------|-------------|
| repo-config | gh-workflow | Dynamic repo configuration |
| runtime-verification | gh-workflow | Runtime smoke/E2E testing |
| suggest-users | gh-workflow | Reviewer/assignee suggestion |
| custom-skill | project | [extracted from frontmatter] |

### Quality Commands
| Command | Purpose | Source |
|---------|---------|--------|
| `ruff check .` | Python linting | CLAUDE.md |
| `pytest` | Python tests | CLAUDE.md |
| `npm run lint` | JavaScript linting | package.json scripts |

### Tech Stack Detected
- Python (pyproject.toml found)
- TypeScript (tsconfig.json found)

### Verification Capabilities
| Capability | Command | Source |
|-----------|---------|--------|
| Dev server | `npm run dev` | package.json scripts.dev |
| E2E tests | `npx playwright test` | playwright.config.ts detected |
| Health check | `curl localhost:3000/health` | CLAUDE.md |

### Recommended Workflow
Based on capabilities:
1. Use `code-reviewer` agent for code analysis
2. Use `convention-checker` for Git validation
3. Run `ruff check .` then `pytest` for quality
4. Invoke `lint` skill if project-specific
```

## Usage in Commands

### In gh-start (Phase 3)

```markdown
Before implementation:
1. Invoke capability-discovery skill
2. Note available agents for later review phases
3. Note quality commands for Phase 6
4. Store tech stack for appropriate tooling
```

### In gh-pr (Phase 1 Step 1.2)

```markdown
Before PR creation:
1. Invoke capability-discovery skill
2. Extract LINT_CMD, TEST_CMD, TYPECHECK_CMD for Phase 3
3. Note available agents for review dispatch
```

### In gh-review (Phase 2)

```markdown
Before detailed review:
1. Check for review-specific agents (code-reviewer, convention-checker)
2. Check for quality skills (lint, test)
3. Plan review facets based on available capabilities
```

### In gh-address (Phase 2)

```markdown
Before addressing feedback:
1. Invoke capability-discovery skill
2. Extract quality commands for Phase 5 verification
3. Note available agents for Phase 6 code review
```

### In gh-resolve (Step 2.2)

```markdown
Before post-resolution verification:
1. Invoke capability-discovery skill
2. Extract LINT_CMD, TEST_CMD, TYPECHECK_CMD for Phase 5
3. If skill fails, fall back to tech-stack detection table
```

## Graceful Degradation

When capabilities are not found:

| Missing Capability | Fallback |
|-------------------|----------|
| No custom agents | Use built-in review checklist |
| No lint skill | Detect from tech stack |
| No CLAUDE.md commands | Use standard tools for detected stack |
| No tech stack detected | Ask user for commands |
| No package.json scripts | Fall back to grep-based detection |

## Integration Points

This skill is invoked by:
- `gh-start` — Phase 3 (before implementation)
- `gh-pr` — Phase 1 Step 1.2 (before PR creation)
- `gh-review` — Phase 2 (before code review)
- `gh-address` — Phase 2 (before addressing feedback)
- `gh-resolve` — Step 2c (quality command discovery for post-resolution verification)

Results inform:
- Which agents to delegate to (code-reviewer, convention-checker, test-runner, implementation-planner)
- Which quality commands to run (LINT_CMD, TEST_CMD, TYPECHECK_CMD)
- How to adapt workflow to project capabilities

**Caching note**: This skill runs in a forked context. The calling command must store the returned output (agent list, quality commands, tech stack) in its own context for use in later phases. Do not re-invoke this skill within the same command execution.

## Best Practices

1. **Prefer explicit** — CLAUDE.md commands take precedence over tech-stack inference
2. **Report clearly** — Show what was found and what wasn't so the caller can plan fallbacks
3. **Enable fallbacks** — Never block workflow due to missing capabilities
4. **Extract descriptions** — Agent/skill descriptions help the caller decide what to dispatch
