---
name: lesson-runner
description: Run Python code in lesson context with proper uv and venv handling for agent-spike project. Activate when user wants to run tests, demos, or CLI commands for lessons in lessons/ directories. Project-specific for agent-spike multi-agent learning.
---

# Lesson Runner Skill

Standard patterns for running lesson code in the agent-spike multi-agent learning project.

## When to Use

This skill activates when:
- User wants to run test/demo scripts in lessons
- User wants to execute lesson CLI commands
- User is working in lessons/ directories
- User asks "how to run this lesson"

## Running Lesson Code

### Standard Execution Patterns

**Navigate to lesson directory first:**
```bash
cd lessons/lesson-XXX
```

**Run test scripts:**
```bash
uv run python test_router.py
uv run python test_coordinator.py
uv run python test_*.py
```

**Run demo scripts:**
```bash
uv run python demo.py "https://example.com"
uv run python demo.py "https://youtube.com/watch?v=..."
```

**Run module CLI (if lesson has one):**
```bash
# Interactive mode
uv run python -m youtube_agent.cli interactive
uv run python -m webpage_agent.cli interactive

# Analyze mode
uv run python -m youtube_agent.cli analyze "URL"
uv run python -m <name>_agent.cli analyze "URL"
```

### Running from Project Root

You can also run from project root (uv finds the lesson automatically):
```bash
# From root directory
uv run python lessons/lesson-003/demo.py "URL"
uv run python lessons/lesson-001/test_agent.py
```

## Why uv run Works

**Cross-directory execution:**
1. `uv` searches upward for `pyproject.toml` (finds project root)
2. Looks for `.venv` at project root
3. Also checks for lesson-specific `.venv` if in lesson directory
4. Runs command with correct Python interpreter and dependencies

**Benefits:**
- No manual venv activation
- No manual path management
- Works from any directory
- Cross-platform (Windows/Linux/Mac)

## Virtual Environment Structure (FYI)

This project has a hybrid .venv structure:
- **Root .venv**: Contains all dependencies (created by `uv sync --all-groups`)
- **Lesson-001 .venv**: Legacy from initial setup (still works)
- **Lessons 002, 003**: Use shared root .venv

**You don't need to manage this** - `uv run python` handles it automatically.

## Common Commands

```bash
# Install lesson dependencies
uv sync --group lesson-001
uv sync --group lesson-002
uv sync --group lesson-003
uv sync --all-groups              # Install all lessons (recommended)

# Check what's installed
uv pip list

# Run specific lesson
cd lessons/lesson-001
uv run python -m youtube_agent.cli analyze "https://youtube.com/watch?v=..."

cd lessons/lesson-002
uv run python -m webpage_agent.cli analyze "https://github.com/..."

cd lessons/lesson-003
uv run python test_coordinator.py
```

## Troubleshooting

**If you get "module not found" errors:**
1. Check dependencies installed: `uv sync --group lesson-XXX`
2. Verify you're using `uv run python` (not `python` directly)
3. Check that you're in the right lesson directory

**If you get ".env not found" warnings:**
1. Copy `.env` from another lesson: `cp ../lesson-001/.env .`
2. Or create new `.env` with API keys (see lesson README)

**If tests fail:**
1. Check STATUS.md for known issues
2. Verify API keys in `.env`
3. Check that lesson is marked as complete in STATUS.md

## Quick Reference

**Most common pattern:**
```bash
cd lessons/lesson-XXX
uv run python <script>.py
```

**Always use:**
- ✅ `uv run python` (handles venv automatically)
- ✅ `-m` flag for module execution (e.g., `-m youtube_agent.cli`)
- ✅ Navigate to lesson directory first (clearer context)

**Never use:**
- ❌ Manual .venv paths (`.venv/Scripts/python.exe`)
- ❌ System `python` command directly
- ❌ Relative venv paths (`../../../.venv/`)

---

**Note:** See python-workflow skill for general Python/uv best practices. This skill is specific to running agent-spike lesson code.
