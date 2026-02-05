---
name: adw-bootstrap
description: |
  Bootstrap AI Developer Workflows (ADWs) infrastructure in any codebase.
  Use when user wants to: "set up ADWs", "bootstrap agentic workflows",
  "add AI developer workflows", "enable programmatic agent execution",
  "initialize ADW infrastructure", or "set up programmatic Claude Code".

  This enables programmatic agent orchestration via subprocess/SDK,
  reusable workflow templates, multi-phase workflows, and structured
  observability for agent executions.
allowed-tools: [Read, Write, Glob, Grep, Bash, Edit, TodoWrite]
---

# AI Developer Workflows Bootstrap Skill

## Mission

Bootstrap **AI Developer Workflows (ADWs)** infrastructure that enables programmatic agent orchestration in any codebase. Transform a regular project into one where AI agents can be invoked programmatically to plan, implement, test, and deploy features.

## What ADWs Enable

After setup, developers can:
- **Execute prompts programmatically**: `./adws/adw_prompt.py "implement feature X"`
- **Use reusable templates**: `./adws/adw_slash_command.py /chore "task"`
- **Orchestrate multi-phase workflows**: Plan → Implement → Test → Deploy
- **Track agent behavior**: Structured outputs in `agents/{id}/` for debugging
- **Scale compute**: Run multiple agents in parallel for complex tasks

## Core Philosophy: Intelligence Over Templating

**You are NOT executing a rigid template substitution.**

You will:
1. Read working reference implementations
2. Understand the patterns they demonstrate
3. Analyze the target project's structure and conventions
4. Intelligently adapt the references to fit the target
5. Make contextual decisions based on project needs

**Use your reasoning.** Handle novel structures, mixed languages, and edge cases that no template could anticipate.

## Two-Layer Architecture

ADWs create a **two-layer architecture**:

1. **Agentic Layer** (`adws/`, `.claude/`, `specs/`) - Templates engineering patterns, teaches agents how to operate
2. **Application Layer** (`apps/`, `src/`, etc.) - The actual application code that agents operate on

The agentic layer wraps the application layer, providing a programmatic interface for AI-driven development.

## Progressive Enhancement Model

Setup happens in phases based on project needs:

- **Minimal** (Always): Core subprocess execution, basic prompts, essential commands
- **Enhanced** (Recommended for dev projects): SDK support, compound workflows, richer commands
- **Scaled** (Production/teams): State management, triggers, testing, worktree isolation

## IMPORTANT: Upgrade Detection

**BEFORE starting fresh setup, ALWAYS check if ADWs already exist in this project.**

### Detect Existing ADW Setup

Check for existence of:
```bash
# Primary indicator
adws/adw_modules/agent.py

# If exists, this is an ADW project - proceed to classification
```

If `adws/` directory exists, **DO NOT run fresh setup**. Instead, **classify and offer upgrade**.

### Classify Current Phase

Use file presence to determine current phase:

**Minimal Phase Indicators:**
- ✅ `adws/adw_modules/agent.py` (core module)
- ✅ `adws/adw_prompt.py` (basic CLI)
- ✅ `.claude/commands/chore.md` (basic templates)
- ✅ `.claude/commands/implement.md`
- ❌ No `adws/adw_modules/agent_sdk.py`
- ❌ No `adws/adw_modules/state.py`

**Enhanced Phase Indicators:**
- ✅ Everything from Minimal
- ✅ `adws/adw_modules/agent_sdk.py` (SDK support)
- ✅ `adws/adw_sdk_prompt.py` (SDK CLI)
- ✅ `adws/adw_slash_command.py` (command executor)
- ✅ `adws/adw_chore_implement.py` (compound workflows)
- ✅ `adws/adw_plan_tdd.py` (TDD planning for large tasks)
- ✅ `.claude/commands/feature.md` (richer templates)
- ✅ `.claude/commands/plan-tdd.md` (TDD task breakdown)
- ✅ `.claude/commands/prime.md`
- ❌ No `adws/adw_modules/state.py`
- ❌ No `adws/adw_modules/worktree_ops.py`

**Scaled Phase Indicators:**
- ✅ Everything from Enhanced
- ✅ `adws/adw_modules/state.py` (state management)
- ✅ `adws/adw_modules/git_ops.py` (git operations)
- ✅ `adws/adw_modules/worktree_ops.py` (worktree isolation)
- ✅ `adws/adw_modules/workflow_ops.py` (workflow composition)
- ✅ `adws/adw_modules/github.py` (GitHub integration)
- ✅ `adws/adw_sdlc_iso.py` (multi-phase workflows)
- ✅ `.claude/commands/classify_issue.md` (advanced templates)
- ✅ `.claude/commands/install_worktree.md`

### Report Current Phase to User

When existing ADW setup is detected:

```
🔍 Existing ADW setup detected!

Current Phase: <Minimal|Enhanced|Scaled>

Found infrastructure:
- Core modules: agent.py <and others...>
- CLI scripts: adw_prompt.py <and others...>
- Slash commands: <count> commands
- Workflows: <count> workflows

Available upgrades:
- <Next phase name>: <Brief description of what it adds>

Would you like to:
1. Upgrade to <next phase>
2. Keep current setup (no changes)
3. Add specific features
```

### Upgrade Execution Process

When user confirms upgrade:

#### Step 1: Safety Backup

Create timestamped backup:
```bash
mkdir -p .adw_backups
cp -r adws .adw_backups/adws_$(date +%Y%m%d_%H%M%S)
cp -r .claude .adw_backups/.claude_$(date +%Y%m%d_%H%M%S)
```

Inform user: "✅ Created backup in .adw_backups/"

#### Step 2: Read Reference Implementations

Based on target phase, read appropriate references:

**For Minimal → Enhanced upgrade:**
- Read @reference/enhanced/adws/adw_modules/agent_sdk.py
- Read @reference/enhanced/adws/adw_sdk_prompt.py
- Read @reference/enhanced/adws/adw_slash_command.py
- Read @reference/enhanced/adws/adw_chore_implement.py
- Read @reference/enhanced/adws/adw_plan_tdd.py
- Read @reference/enhanced/commands/*.md (especially plan-tdd.md)

**For Enhanced → Scaled upgrade:**
- Read @reference/scaled/adw_modules/state.py
- Read @reference/scaled/adw_modules/git_ops.py
- Read @reference/scaled/adw_modules/worktree_ops.py
- Read @reference/scaled/adw_modules/workflow_ops.py
- Read @reference/scaled/adw_modules/github.py
- Read @reference/scaled/workflows/*.py
- Read @reference/scaled/commands/*.md

#### Step 3: Detect Customizations

Before adding files, check if target paths exist:
```python
# Pseudocode for detection logic
for file_to_add in new_files:
    if file_exists(file_to_add):
        # Compare with reference
        if file_is_customized(file_to_add):
            # Skip or ask user
            print(f"⚠️  {file_to_add} appears customized - preserving")
        else:
            # Can safely update
            print(f"📝 Updating {file_to_add}")
```

**Never overwrite:**
- Any file with modification timestamp significantly after installation
- Any file with content that differs from known reference versions
- Any file in a `custom_` directory
- When in doubt, preserve and create `<file>.new` instead

#### Step 4: Add New Capabilities

**For Enhanced upgrade**, add:
- `adws/adw_modules/agent_sdk.py` (if not exists)
- `adws/adw_sdk_prompt.py` (if not exists)
- `adws/adw_slash_command.py` (if not exists)
- `adws/adw_chore_implement.py` (if not exists)
- `adws/adw_plan_tdd.py` (if not exists)
- `.claude/commands/feature.md` (if not exists)
- `.claude/commands/plan-tdd.md` (if not exists)
- `.claude/commands/prime.md` (if not exists)
- `specs/plans/` directory (if not exists)

**For Scaled upgrade**, add:
- `adws/adw_modules/state.py` (if not exists)
- `adws/adw_modules/git_ops.py` (if not exists)
- `adws/adw_modules/worktree_ops.py` (if not exists)
- `adws/adw_modules/workflow_ops.py` (if not exists)
- `adws/adw_modules/github.py` (if not exists)
- `adws/adw_modules/data_types.py` (if not exists or needs extension)
- `adws/adw_modules/utils.py` (if not exists)
- `adws/adw_sdlc_iso.py` (if not exists)
- `adws/adw_plan_build_test_review_iso.py` (if not exists)
- `adws/adw_ship_iso.py` (if not exists)
- `.claude/commands/classify_issue.md` (if not exists)
- `.claude/commands/classify_adw.md` (if not exists)
- `.claude/commands/generate_branch_name.md` (if not exists)
- `.claude/commands/patch.md` (if not exists)
- `.claude/commands/install_worktree.md` (if not exists)
- `.claude/commands/cleanup_worktrees.md` (if not exists)
- `.claude/commands/test.md` (if not exists)
- `.claude/commands/review.md` (if not exists)
- `.claude/commands/document.md` (if not exists)
- `.claude/commands/pull_request.md` (if not exists)
- `.claude/commands/bug.md` (if not exists)
- `trees/` directory (create if not exists, add to .gitignore)

#### Step 5: Update Dependencies

**For Enhanced upgrade:**
- Check if scripts use uv inline deps (PEP 723)
- If agent_sdk.py is added, ensure claude-code-sdk is in dependencies

**For Scaled upgrade:**
- Ensure gh CLI is available (for GitHub operations)
- Create data_types.py with extended models if needed
- Add any missing utility functions

#### Step 6: Update Documentation

Add new sections to CLAUDE.md (if it exists):
- Document new capabilities added
- Show examples of new workflows
- Update command reference

Create/update README sections showing new usage patterns.

#### Step 7: Validate Upgrade

Run validation checks:
```bash
# Check all scripts are executable
# Verify imports resolve
# Test a simple prompt
./adws/adw_prompt.py "test upgrade" --model haiku
```

If validation passes: ✅
If validation fails: Show error and offer to rollback

#### Step 8: Report Upgrade Results

```
🎉 Upgrade to <phase> completed successfully!

Added:
- <count> new modules
- <count> new workflows
- <count> new slash commands

Your customizations were preserved:
- <list any files that were skipped>

Backup location: .adw_backups/<timestamp>

Try the new capabilities:
- <example 1>
- <example 2>
- <example 3>

To rollback: cp -r .adw_backups/<timestamp>/* ./
```

### Upgrade Special Cases

**Minimal → Scaled (skip Enhanced):**
If user wants to jump directly to Scaled, add both Enhanced and Scaled capabilities in one upgrade.

**Customized setups:**
If setup has significant customizations, offer to create new files with `.new` extension and let user merge manually.

**Failed upgrades:**
If any step fails, automatically rollback to backup and report error.

## Setup Process (Fresh Installation)

### PHASE 1: Analyze Target Project

Before creating anything, deeply understand the target project.

#### 1.1 Read Project Structure

Use Glob to explore:
```bash
# Find configuration files
**/{package.json,pyproject.toml,go.mod,Cargo.toml,pom.xml}

# Find source code locations
**/src/**
**/app/**
**/lib/**

# Find existing tooling
**/{Dockerfile,docker-compose.yml,.github,Makefile}
```

#### 1.2 Identify Key Characteristics

**Primary language(s)**:
- Python? (pyproject.toml, requirements.txt, setup.py)
- JavaScript/TypeScript? (package.json, tsconfig.json)
- Go? (go.mod, *.go files)
- Rust? (Cargo.toml, *.rs files)
- Polyglot? (multiple indicators)

**Application layer location**:
- Where does the actual application code live?
- `src/`, `app/`, `apps/`, `lib/`, `pkg/`, root?
- Monorepo with multiple packages?
- Single package structure?

**Package manager in use**:
- Python: uv, poetry, pip, pipenv?
- JavaScript: npm, yarn, pnpm, bun?
- Look at lock files and existing scripts

**Framework/runtime**:
- FastAPI, Flask, Django?
- Express, Next.js, Nest.js?
- Framework-specific patterns to follow?

**Existing development patterns**:
- How do they run the app currently?
- How do they run tests?
- What's their code style? (tabs vs spaces, line length, etc.)
- Any linters or formatters configured?

**Project maturity**:
- Mature project with existing conventions?
- Greenfield project needing structure?
- Legacy code needing modernization?

#### 1.3 Determine Setup Phase

Based on analysis, recommend:

**Minimal** if:
- Simple project or proof of concept
- User explicitly requests basic setup
- Just need adhoc prompt execution

**Enhanced** if:
- Active development project (most common case)
- Team collaboration
- Need workflow automation
- Python or TypeScript project

**Scaled** if:
- Production system
- Complex SDLC requirements
- Need CI/CD integration
- Large team or enterprise

**Ask the user** which phase to install if unclear.

### PHASE 2: Read Reference Implementations

Before creating anything, read and understand the reference code.

#### 2.1 Always Read (Minimal Phase)

**Read @reference/minimal/adws/adw_modules/agent.py**

This is the **core pattern**. Understand:
- How Claude Code CLI is invoked via subprocess
- How environment variables are filtered for security
- How JSONL streaming output is captured to files
- How output is parsed into structured JSON
- How retry logic handles transient failures
- How unique IDs track execution lineage
- How error messages are truncated to prevent flooding

**Key abstractions**:
- `AgentPromptRequest` - Configuration for prompt execution
- `AgentPromptResponse` - Results with success/failure/retry info
- `prompt_claude_code()` - Core execution function
- `prompt_claude_code_with_retry()` - Execution with automatic retry
- `RetryCode` enum - Different error types for retry decisions

**Read @reference/minimal/adws/adw_prompt.py**

This shows how to **wrap agent.py for CLI use**. Understand:
- uv inline dependency management (`# /// script`)
- Click CLI parameter handling
- Rich console output for user feedback
- Unique ID generation per execution
- Output directory structure (`agents/{adw_id}/{agent_name}/`)
- Multiple output formats (JSONL, JSON array, final object, summary)

**Read @reference/minimal/commands/chore.md**

This shows how to **structure slash command templates**. Understand:
- Variable substitution ($1, $2, $ARGUMENTS)
- Embedded codebase context
- Step-by-step instructions format
- Validation command patterns
- Output specifications

**Read @reference/minimal/commands/implement.md**

Simple implementation template showing minimal structure.

**Read @reference/minimal/env.sample**

Shows configuration for both usage modes:
- Mode A: Subscription (no API key needed)
- Mode B: API-based (requires ANTHROPIC_API_KEY)

#### 2.2 Read for Enhanced Phase

**Read @reference/enhanced/adws/adw_modules/agent_sdk.py**

This shows the **SDK-based approach**. Understand:
- Native async/await patterns
- Typed message objects (AssistantMessage, ResultMessage, etc.)
- SDK-specific error handling
- Interactive session support via ClaudeSDKClient
- Streaming with progress callbacks
- When to use SDK vs subprocess

**Read @reference/enhanced/adws/adw_slash_command.py**

Shows how to execute slash commands programmatically.

**Read @reference/enhanced/adws/adw_chore_implement.py**

Shows **compound workflow orchestration**:
- Multi-phase execution (planning + implementation)
- Output parsing between phases
- Comprehensive observability
- Workflow summary generation

**Read @reference/enhanced/adws/adw_plan_tdd.py**

Shows **TDD planning workflow** for breaking large tasks into agent-sized chunks:
- Subprocess execution with model selection (haiku/sonnet/opus)
- Breaks specifications into GitHub issue-sized tasks
- Agent-centric complexity metrics (context load, iterations, not human time)
- Dependency tracking and parallelization analysis
- Outputs to `specs/plans/plan-{id}.md`
- Smart Claude CLI detection (checks common install locations)

**Key Insight**: Complexity measures **context switching cost** and **iteration depth**:
- **Size S**: Read 1-2 files, modify 1-2, write 5-10 tests, 1-2 iterations
- **Size M**: Read 3-5 files, modify 2-4, write 10-20 tests, 2-4 iterations
- **Size L**: Read 6+ files, modify 3-5, write 20+ tests, 4-6+ iterations

**Read @reference/enhanced/commands/plan-tdd.md**

Template for breaking down large specifications with:
- Agent-centric task sizing philosophy
- TDD approach (Red-Green-Refactor) for each task
- Dependency graph and implementation phases
- Critical path analysis
- Parallelization opportunities

**Read @reference/enhanced/commands/feature.md**

More comprehensive planning template with:
- User stories
- Problem/solution statements
- Multi-phase implementation plans
- Acceptance criteria

**Read @reference/enhanced/commands/prime.md**

Context loading pattern for priming Claude with project knowledge.

### PHASE 3: Create Minimal Infrastructure

Now create the ADW infrastructure, adapted to the target project.

#### 3.1 Create Directory Structure

```bash
mkdir -p adws/adw_modules
mkdir -p .claude/commands
mkdir -p specs
mkdir -p agents  # For output observability
```

If the project already has any of these, note and work with existing structure.

#### 3.2 Create adws/adw_modules/agent.py

**Do NOT just copy the reference.** Adapt it:

**Understand the core patterns** from the reference, then create a version that:
- Uses paths appropriate to this project's structure
- Matches this project's code style (if established)
- Includes inline documentation explaining patterns
- Has the project root detection logic that makes sense

**Key adaptations**:
- If project uses specific directory structure, adjust `project_root` calculation
- If project has special environment needs, adapt `get_safe_subprocess_env()`
- Keep all the core patterns: subprocess execution, JSONL parsing, retry logic
- Add comments explaining "why" for future maintainers

**Essential components to preserve**:
- `AgentPromptRequest` and `AgentPromptResponse` data models
- `prompt_claude_code()` core function
- `prompt_claude_code_with_retry()` with retry logic
- JSONL to JSON conversion
- Error handling and truncation
- Environment variable filtering

#### 3.3 Create adws/adw_prompt.py

Adapt the reference to this project:

**Dependencies**:
- If project uses uv, use uv script headers (PEP 723)
- If project uses poetry, adapt for `poetry run`
- If project uses npm, this might be a TypeScript version

**Paths**:
- Adjust output paths to make sense for this project
- Adjust working directory defaults
- Adjust imports to find agent.py

**Style**:
- Match the project's Python style if established
- Use their preferred CLI framework if they have one
- Follow their naming conventions

**Make it executable**:
```bash
chmod +x adws/adw_prompt.py
```

#### 3.4 Create .claude/commands/chore.md

Adapt the reference template:

**Codebase Structure section**:
- Replace with ACTUAL structure of this project
- List where their app code actually lives
- Reference their actual README, docs, etc.

**Plan Format**:
- Keep the core structure (metadata, description, tasks, validation)
- Adapt validation commands to this project's tooling

**Validation Commands**:
- Use their actual test commands
- Use their actual linting commands
- Use their package manager

**Example adaptation**:
```markdown
# Before (generic):
- `uv run python -m py_compile apps/*.py`

# After (adapted to Next.js project):
- `npm run type-check` - Verify TypeScript types
- `npm run lint` - Run ESLint
- `npm run build` - Ensure build succeeds
```

#### 3.5 Create .claude/commands/implement.md

Simple implementation template - minimal changes needed, maybe adapt the validation reporting to match their tooling.

#### 3.6 Create .env.sample

Adapt to show both usage modes:

```bash
# Mode A: Claude Max Subscription (default - recommended for interactive use)
# No configuration needed if you have Claude Max subscription
# Claude Code will authenticate through your subscription

# Mode B: API-Based Programmatic Execution (for automation, CI/CD, webhooks)
# Required for headless/automated workflows
# ANTHROPIC_API_KEY=sk-ant-...

# Optional: Claude Code Path (auto-detected if not set)
# CLAUDE_CODE_PATH=claude

# Optional: Maintain working directory
# CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=true
```

**Note**: The agent module includes smart Claude CLI detection via `find_claude_cli()`:
1. Checks `CLAUDE_CODE_PATH` environment variable
2. Runs `which claude` command
3. Checks common install locations (~/.claude/local/claude, /usr/local/bin/claude, etc.)
4. Falls back to "claude" (assumes in PATH)

#### 3.7 Update CLAUDE.md

If CLAUDE.md exists, add ADW section. If not, create it with:

**Essential Commands section**:
```markdown
## AI Developer Workflows (ADWs)

Execute Claude Code prompts programmatically:

```bash
# Direct prompt execution
./adws/adw_prompt.py "your prompt here"
./adws/adw_prompt.py "analyze this module" --model opus

# Run slash commands (after enhanced setup)
./adws/adw_slash_command.py /chore <id> "add feature X"
./adws/adw_slash_command.py /implement specs/chore-*.md
```
```

**Architecture section**:
Explain the two-layer model, observability in `agents/` directory, etc.

Use examples from THIS project structure.

### PHASE 4: Validate Minimal Setup

Before moving forward, validate everything works.

#### 4.1 Check Prerequisites

```bash
# Verify Claude Code installed
claude --version

# Check if it's available (should show help)
claude --help
```

If not installed, guide user to install:
- macOS/Linux: Installation instructions
- Windows: Installation instructions

#### 4.2 Test Prompt Execution

```bash
# Try a simple prompt
./adws/adw_prompt.py "What is 2 + 2?"
```

Expected:
- ✓ Script executes
- ✓ Creates output in `agents/{id}/oneoff/`
- ✓ Multiple output files created (JSONL, JSON, summary)
- ✓ Returns success

If subscription mode, should work with no API key.
If API mode, requires ANTHROPIC_API_KEY.

#### 4.3 Verify Output Structure

Check that `agents/{adw_id}/oneoff/` contains:
- `cc_raw_output.jsonl` - Raw streaming output
- `cc_raw_output.json` - Parsed JSON array
- `cc_final_object.json` - Final result object
- `custom_summary_output.json` - High-level summary

#### 4.4 Report to User

Show:
- ✅ What was created
- ✅ How to use it
- ✅ Test results
- ✅ Next steps (enhance if desired)

### PHASE 5: Create Enhanced Infrastructure (If Requested)

Only proceed if user wants enhanced setup or you recommended it.

#### 5.1 Add SDK Support (adws/adw_modules/agent_sdk.py)

Adapt the SDK reference:

**Dependencies**:
- Requires `claude-code-sdk` Python package
- Add to project dependencies or inline script deps

**Adaptation**:
- Keep all the SDK patterns (async/await, typed messages, error handling)
- Adjust imports if needed for project structure
- Match project style
- Add documentation explaining when to use SDK vs subprocess

**When to use SDK approach**:
- Interactive sessions (multi-turn conversations)
- Better type safety needed
- Async workflows
- Native Python integration

**When to use subprocess approach**:
- Simple one-shot prompts
- Shell script compatibility
- Lower dependencies
- Easier debugging

#### 5.2 Add Slash Command Executor (adws/adw_slash_command.py)

Adapt for this project:
- Adjust paths
- Match style
- Use their package manager
- Make executable

#### 5.3 Add Compound Workflow (adws/adw_chore_implement.py)

This orchestrates: planning (/chore) → implementation (/implement)

Adapt:
- Paths and imports
- Package manager
- Output formatting to match project conventions
- Error handling to project standards

#### 5.4 Add Enhanced Commands

**Create .claude/commands/feature.md**:
- Adapt codebase structure section to this project
- Adapt validation commands to their tooling
- Keep the comprehensive planning structure

**Create .claude/commands/prime.md**:
- Update to read THIS project's docs
- Point to their actual README, architecture docs, etc.

**Create .claude/commands/start.md** (if applicable):
- Update with commands to run THIS project's apps
- Their actual run commands, not generic ones

#### 5.5 Update Documentation

Add to CLAUDE.md:

**Enhanced Commands**:
```markdown
### Compound Workflows

# Plan and implement in one command
./adws/adw_chore_implement.py "add error handling to API"

# Feature development
./adws/adw_slash_command.py /feature <id> "user authentication"

# Prime Claude with context
./adws/adw_slash_command.py /prime
```

```markdown
### TDD Planning for Large Tasks

# Break down large spec into agent-sized tasks
./adws/adw_plan_tdd.py "Add user authentication with JWT and OAuth2"

# From a spec file
./adws/adw_plan_tdd.py specs/feature-auth.md --spec-file

# Use Opus for complex architecture planning
./adws/adw_plan_tdd.py "Build real-time collaboration system" --model opus

# Output: specs/plans/plan-{id}.md with:
# - 25 tasks broken down (agent-optimized sizing)
# - Dependency graph and phases
# - TDD guidance for each task
# - Agent-centric complexity metrics
```

**Architecture Deep Dive**:
- Explain subprocess vs SDK approaches
- Show workflow orchestration patterns
- Document output observability structure

#### 5.6 Validate Enhanced Setup

```bash
# Test slash command execution
./adws/adw_slash_command.py /prime

# Test compound workflow
./adws/adw_chore_implement.py "add a hello world endpoint"
```

Check outputs, verify everything works.

### PHASE 6: Create Scaled Infrastructure (If Requested)

Only for production/enterprise needs.

This adds:
- State management across workflow phases
- Git worktree isolation for safe operations
- Workflow orchestration helpers
- Trigger systems (webhooks, cron)
- Comprehensive testing infrastructure
- Database for agent execution history

**Note**: This is advanced. Most projects won't need it initially.

Guide through adding:
- `adws/adw_modules/state.py` - Workflow state tracking
- `adws/adw_modules/workflow_ops.py` - Orchestration helpers
- `adws/adw_triggers/` - Event-driven invocation
- `adws/adw_tests/` - Testing suite
- `trees/` - Git worktree isolation
- `.claude/hooks/` - Event handlers
- `.claude/settings.json` - Hook configuration

## Special Adaptations for Different Project Types

### Python Projects

**Package manager detection**:
- uv? Use `# /// script` headers with inline deps
- poetry? Use `poetry add` and `poetry run`
- pip? Use requirements.txt or pip install -e .

**Style matching**:
- Check for black, ruff, mypy configs
- Match their line length, quote style
- Follow their typing conventions

**Validation commands**:
- Their test runner (pytest, unittest, etc.)
- Their linter (ruff, flake8, pylint)
- Their type checker (mypy, pyright)

### TypeScript/JavaScript Projects

**Consider TypeScript version of ADWs**:
- Could create TypeScript equivalents
- Or keep Python scripts (they work on any project)

**Package manager**:
- npm, yarn, pnpm, or bun?
- Use their lock file type

**Validation commands**:
- `npm run test` or their test command
- `npm run type-check` or equivalent
- `npm run lint` or equivalent
- `npm run build` to ensure builds

### Monorepo Projects

**Structure awareness**:
- Multiple packages in `packages/` or `apps/`?
- Each package has own ADWs? Or shared at root?
- Recommend root-level ADWs that can target specific packages

**Adapt paths**:
- Commands need to specify which package
- Working directories may vary per operation

### Polyglot Projects

**Flexibility**:
- ADWs work on any code (they orchestrate Claude Code)
- But validation commands must cover all languages
- Documentation must explain multi-language structure

## Usage Mode Configuration

### Mode A: Claude Max Subscription (Recommended for Users)

**How it works**:
- User has Claude Max subscription
- Claude Code authenticates through subscription
- No API key needed
- ADWs invoke `claude -p "prompt"` and it just works

**Setup**:
- No `.env` file needed
- Scripts work out of the box
- Perfect for interactive development

**Limitations**:
- User must be logged in
- Not suitable for fully automated/headless workflows
- Can't run in CI/CD without additional setup

### Mode B: API-Based (For Automation)

**How it works**:
- User has ANTHROPIC_API_KEY
- Scripts set the API key in subprocess environment
- Claude Code uses API for programmatic execution
- Enables headless automation

**Setup**:
```bash
# Create .env file
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# Or set in environment
export ANTHROPIC_API_KEY=sk-ant-...
```

**Use cases**:
- CI/CD pipelines
- Webhook-triggered workflows
- Scheduled tasks (cron)
- Server-side automation

### Detection and Configuration

In `agent.py`, the environment handling already supports both:

```python
def get_safe_subprocess_env():
    env = {...}

    # Only add API key if it exists
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        env["ANTHROPIC_API_KEY"] = api_key

    # Claude Code will use subscription if no key provided
    return env
```

**Guide users**:
- Default to subscription mode (simpler)
- Document API mode for automation needs
- Show both in .env.sample with clear comments

## Best Practices to Embed

### 1. Environment Safety
- Filter environment variables before subprocess
- Only pass required vars
- Never leak secrets

### 2. Observability First
- Always create structured output directories
- Multiple output formats (JSONL, JSON, summary)
- Include metadata (adw_id, session_id, timestamps)

### 3. Error Handling
- Retry logic for transient failures
- Truncate error messages (prevent flooding)
- Clear error messages to users
- Distinguish retry-able from non-retry-able errors

### 4. Type Safety
- Use Pydantic models for data
- Use SDK types when available
- Document expected shapes

### 5. Documentation
- Inline code comments explain "why"
- CLAUDE.md with project-specific examples
- README in adws/ directory
- Reference upstream docs

### 6. Progressive Enhancement
- Start simple (minimal)
- Add features as needed (enhanced)
- Scale for production (scaled)
- Don't over-engineer initially

## Reporting to User

After setup, tell the user:

### ✅ What Was Created

```
AI Developer Workflows infrastructure is set up!

Created:
- adws/adw_modules/agent.py - Core subprocess execution engine
- adws/adw_prompt.py - CLI wrapper for adhoc prompts
- .claude/commands/ - Slash command templates (chore, implement)
- specs/ - Directory for implementation plans
- agents/ - Observability outputs directory
- .env.sample - Configuration template
- CLAUDE.md - Updated with ADW documentation
```

### 📚 How to Use

```bash
# Execute an adhoc prompt
./adws/adw_prompt.py "analyze the database schema"

# Create a plan for a chore
./adws/adw_slash_command.py /chore $(uuidgen | cut -c1-8) "add logging"

# Implement a plan
./adws/adw_slash_command.py /implement specs/chore-abc123-*.md

# Or do both in one command (enhanced setup)
./adws/adw_chore_implement.py "add error handling"
```

### 🔍 Observability

```
Agent outputs saved to:
agents/{adw_id}/{agent_name}/
  cc_raw_output.jsonl       - Raw streaming output
  cc_raw_output.json         - Parsed JSON array
  cc_final_object.json       - Final result object
  custom_summary_output.json - High-level summary
```

### 📖 Documentation

```
See CLAUDE.md for:
- Complete command reference
- Architecture explanation
- Examples for this project
- Extension patterns
```

### 🚀 Next Steps

```
1. Try a simple prompt:
   ./adws/adw_prompt.py "what does this project do?"

2. Create your first plan:
   ./adws/adw_slash_command.py /chore test "add a new feature"

3. Read CLAUDE.md for more examples

4. (Optional) Upgrade to enhanced setup for more features:
   - SDK support for better type safety
   - Compound workflows (plan + implement in one command)
   - Richer slash commands (feature planning, testing)
```

### ⚙️ Configuration (If Needed)

```
For API-based automation (CI/CD, webhooks):
1. Create .env file: cp .env.sample .env
2. Add your API key: ANTHROPIC_API_KEY=sk-ant-...

For interactive use with Claude Max subscription:
- No configuration needed! Just use the scripts.
```

## Troubleshooting

### Claude Code not found

```bash
# Check if installed
claude --version

# If not, guide to installation
```

### Permission denied

```bash
# Make scripts executable
chmod +x adws/*.py
```

### Import errors

```bash
# Check dependencies
# For uv scripts, they auto-install on first run
# For poetry projects, run: poetry install
```

### API key issues

```bash
# Verify key is set
echo $ANTHROPIC_API_KEY

# Or check .env file
cat .env
```

## Success Criteria

✅ Directory structure created correctly
✅ Reference code adapted to project context
✅ Scripts are executable
✅ Test prompt executes successfully
✅ Output directories created properly
✅ Documentation updated with project-specific examples
✅ User understands how to use the system
✅ User knows how to extend the system

## Remember

- **Use your intelligence** - Don't just copy/paste
- **Understand the project** - Every project is different
- **Adapt thoughtfully** - Make it fit their conventions
- **Document well** - Future maintainers will thank you
- **Test thoroughly** - Ensure everything works before finishing
- **Guide the user** - Show them how to use what you created

You're not installing a template. You're teaching a codebase how to work with programmatic agents.
