---
name: nonstop-agent
description: Creates long-running autonomous agents. Use when the user asks for "롱 러닝 에이전트 만들어줘", "자율 에이전트 생성", "autonomous agent", "long-running agent", "nonstop agent", or "24/7 agent". Collects requirements through AskUserQuestion and generates agent structure following Anthropic best practices.
---

# Nonstop Agent Generator

Creates autonomous agent harnesses based on Anthropic's long-running agent best practices.

---

## Execution Instructions (For Claude)

**When this skill is invoked, you MUST execute the steps below in order.**

---

## STEP 1: Requirements Collection (MUST use AskUserQuestion)

**Use the AskUserQuestion tool to ask the following questions sequentially.**

### 1.1 First Question Set (Ask at once)

```
AskUserQuestion call:
questions: [
  {
    question: "What is the current project state?",
    header: "Project State",
    options: [
      { label: "New Project", description: "Starting from scratch" },
      { label: "Existing Project", description: "Already has code (will analyze first)" },
      { label: "Partially Complete", description: "Some features already implemented" }
    ],
    multiSelect: false
  },
  {
    question: "What type of agent do you want to create?",
    header: "Agent Type",
    options: [
      { label: "Coding Agent", description: "Code generation, modification, refactoring" },
      { label: "Research Agent", description: "Information gathering and analysis" },
      { label: "Automation Agent", description: "Repetitive task automation" },
      { label: "Custom", description: "Define your own" }
    ],
    multiSelect: false
  },
  {
    question: "Which language will you use?",
    header: "Language",
    options: [
      { label: "Python", description: "Claude Agent SDK (Python)" },
      { label: "TypeScript", description: "Claude Agent SDK (TypeScript)" }
    ],
    multiSelect: false
  }
]
```

### 1.2 Second Question Set

```
AskUserQuestion call:
questions: [
  {
    question: "Select the tools the agent will use",
    header: "Tool Selection",
    options: [
      { label: "File System", description: "Read, Write, Edit, Glob, Grep" },
      { label: "Terminal", description: "Bash command execution" },
      { label: "Web Search", description: "WebSearch, WebFetch" },
      { label: "Browser Automation", description: "Playwright MCP" }
    ],
    multiSelect: true
  },
  {
    question: "Select the security level",
    header: "Security Level",
    options: [
      { label: "High (Recommended)", description: "Only allowed commands can run" },
      { label: "Medium", description: "Only dangerous commands blocked" },
      { label: "Low", description: "Most commands allowed (for local dev)" }
    ],
    multiSelect: false
  }
]
```

### 1.3 Third Question (Free Input)

```
AskUserQuestion call:
questions: [
  {
    question: "Describe the main functionality the agent should perform",
    header: "Target Features",
    options: [
      { label: "Enter manually", description: "Provide detailed feature description" }
    ],
    multiSelect: false
  }
]
```

---

## STEP 2: Existing Project Analysis (Conditionally Required)

### Important: MUST run if "Existing Project" or "Partially Complete" is selected

**Do NOT skip this step. You MUST run tests and understand current state.**

### 2.1 Project Structure Discovery

```bash
pwd
ls -la
cat README.md 2>/dev/null || echo "No README.md"
cat CLAUDE.md 2>/dev/null || echo "No CLAUDE.md"
```

### 2.2 Dependencies Check

```bash
# Python project
cat pyproject.toml 2>/dev/null || cat requirements.txt 2>/dev/null

# Node.js project
cat package.json 2>/dev/null | head -50
```

### 2.3 Run Tests (REQUIRED!)

```bash
# Python (uv - as per CLAUDE.md rules)
uv run pytest -v 2>&1 | head -100

# Node.js
npm test 2>&1 | head -100
```

**MUST record test results:**
- Total test count
- Passed test count
- **Failed test list** (these become first items in feature_list.json)

### 2.4 Build/Lint Check

```bash
# Python
uv run ruff check . 2>&1 | head -50
uv run mypy . 2>&1 | head -50

# Node.js
npm run build 2>&1 | head -50
npm run lint 2>&1 | head -50
```

### 2.5 Record Analysis Results

Create `claude-progress.txt` file:

```markdown
## Initial Project Analysis - [Today's Date]

### Project Overview
- Name: [Project Name]
- Type: [Web App/CLI/Library]
- Tech Stack: [Languages, Frameworks]

### Test Status
- Total Tests: X
- Passed: X
- Failed: X
- Coverage: X%

### Failed Tests (Priority Fix Targets)
1. test_xxx: [Failure Reason]
2. test_yyy: [Failure Reason]

### Build/Lint Status
- Build: PASS/FAIL
- Lint Errors: X
- Type Errors: X

### Discovered TODO/FIXME
[TODO list found in code]

### Next Steps
1. Fix failed tests
2. Resolve lint/type errors
3. Process TODO items
```

---

## STEP 3: Generate Agent Structure

### 3.1 Create Directory

```bash
mkdir -p agent/prompts
```

### 3.2 Copy and Substitute Templates

Copy files from this skill's `templates/python/` (or `templates/typescript/`) directory and substitute the following placeholders:

| Placeholder | Substitution |
|-------------|--------------|
| `{{AGENT_DESCRIPTION}}` | Target functionality description from STEP 1.3 |
| `{{MODEL}}` | `claude-opus-4-5-20251101` (default) |
| `{{SYSTEM_PROMPT}}` | System prompt appropriate for agent type |
| `{{BUILTIN_TOOLS}}` | Selected tool list (e.g., `"Read", "Write", "Edit", "Bash"`) |
| `{{MCP_TOOLS}}` | MCP tool list (Playwright if browser automation selected) |
| `{{MCP_SERVERS}}` | MCP server configuration |
| `{{EXTRA_COMMANDS}}` | Additional allowed bash commands |

### 3.3 Files to Generate

```
agent/
├── main.py                    # Entry point
├── agent.py                   # Session logic
├── client.py                  # Claude SDK client
├── progress.py                # Progress tracking
├── security.py                # Security hooks
├── prompts.py                 # Prompt loading
├── requirements.txt           # Dependencies
└── prompts/
    ├── app_spec.txt           # Application specification
    ├── initializer_prompt.md  # Initialization prompt
    ├── coding_prompt.md       # Coding prompt
    └── existing_project_prompt.md  # Existing project analysis
```

---

## STEP 4: feature_list.json Generation Strategy

### For Existing Projects (Priority Order)

```json
[
  // Priority 1: Failed tests (each as a feature)
  {
    "id": 1,
    "category": "bugfix",
    "description": "Fix failing test: test_user_authentication",
    "steps": [
      "Step 1: Read the failing test code",
      "Step 2: Understand what it's testing",
      "Step 3: Find and fix the bug",
      "Step 4: Run the test to verify"
    ],
    "passes": false
  },

  // Priority 2: Build/lint errors
  {
    "id": 2,
    "category": "bugfix",
    "description": "Fix type error in user_service.py line 45",
    "steps": [...],
    "passes": false
  },

  // Priority 3: TODO/FIXME items
  {
    "id": 3,
    "category": "enhancement",
    "description": "TODO: Implement password reset flow",
    "steps": [...],
    "passes": false
  },

  // Priority 4: New features
  {
    "id": 4,
    "category": "functional",
    "description": "User can modify their profile",
    "steps": [...],
    "passes": false
  }
]
```

### For New Projects

Generate feature list based on app_spec.txt

---

## STEP 5: Usage Instructions

After generation, provide the following instructions:

```markdown
## Agent Generation Complete!

### Authentication Setup (Required)
```bash
# Set Claude Code OAuth token
export CLAUDE_CODE_OAUTH_TOKEN="your-oauth-token"

# Or login via Claude Code CLI
claude login
```
> The SDK authenticates through the bundled CLI.

### Running the Agent

**New Project:**
```bash
cd agent/
uv add claude-agent-sdk
uv run python main.py --project-dir ../my_project
```

**Existing Project (Analyze First):**
```bash
cd agent/
uv add claude-agent-sdk
uv run python main.py --project-dir ../existing_project --analyze-first
```

**Resume Previous Session:**
```bash
cd agent/
uv run python main.py --project-dir ../my_project --resume
```

### Key Options
- `--project-dir`: Project directory path
- `--max-iterations`: Maximum iteration count (default: unlimited)
- `--analyze-first`: Existing project analysis mode
- `--resume`: Resume previous session (uses saved session_id)
- `--model`: Claude model (default: claude-opus-4-5-20251101)

### Generated Files
- `agent/main.py`: Main entry point
- `agent/prompts/`: Agent prompts
- `agent/security.py`: Allowed command list (modify as needed)

### Check Progress
```bash
cat feature_list.json | jq '[.[] | select(.passes == true)] | length'
cat claude-progress.txt
```
```

---

## Core Principles Summary

1. **2-Agent Pattern**: Initializer (first session) → Coding (subsequent sessions)
2. **Mandatory Existing Project Analysis**: Run tests → Identify failures → Generate feature_list
3. **State Persistence**: git + claude-progress.txt + feature_list.json
4. **Incremental Progress**: One feature at a time
5. **Immutable Rules**: NEVER modify description/steps in feature_list.json

---

## References

- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed Architecture
- [templates/python/](templates/python/) - Python Templates
- [Anthropic: Effective Harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Autonomous Coding Demo](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)
