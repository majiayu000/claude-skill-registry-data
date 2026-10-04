---
name: onboard
description: >
  Interactive onboarding for The Agency inside Claude Code. Walks a new user through
  the full system: what it is, how it works, verifying installation, enabling slash
  commands, connecting MCP servers, creating a first project, and a guided first-run
  demo. Triggers on: "onboard", "set up the agency", "get started", "walk me through",
  "how does this work", "first time setup". Run after `agency init` or `./install.sh`.
aliases:
  - setup-agency
  - get-started
  - first-run
---

# /onboard — The Agency Onboarding

Interactive onboarding that runs INSIDE Claude Code. Introduces the system,
verifies the installation, enables skills as slash commands, connects MCP
servers and CLI tools, creates a first project, and runs a guided demo.

Prerequisite: `agency init` or `./install.sh` has already been run (skills and
agents are in `~/.claude/`). If not, tell the user to run it first.

---

## Phase 1 — Welcome & System Introduction

Print this introduction (adapt the tone — friendly, concise, no hype):

```
Welcome to The Agency.

This is Claude Code, fixed: memory that survives sessions, agents that
finish what they start, QA gates before "done", and token-lean routing.
Here's what it gives you:

  Agents    235+ specialists across 16 departments (Engineering, Design,
            Marketing, Content, Sales, Testing, Game Dev, and more).
            Each agent has a role, a model assignment, and a protocol.

  Skills    285+ slash commands you can invoke right here. /save-state,
            /recall, /pd-resume, /delegate, /swarm, /graphify, and more.

  Memory    Persistent project state that survives across sessions.
            /save-state at the end, /recall at the start. Your agents
            remember where they left off.

  PDs       Project Directors — autonomous agents that decompose work,
            spawn specialists, run QA gates, and report back. You
            supervise, they execute.

  Model     Opus for planning, Sonnet for execution, Haiku for bulk
  routing   work. Agents carry a model assignment.

Let's verify your setup and get you running.
```

---

## Phase 2 — Verify Installation

Check these paths exist. Report each as ✓ or ✗:

```bash
# Check these directories
ls -d ~/.claude/skills/ 2>/dev/null    # Skills installed?
ls -d ~/.claude/agents/ 2>/dev/null    # Agents installed?
ls -d ~/.claude/core/ 2>/dev/null      # Core docs installed?
ls -d ~/.claude/projects/ 2>/dev/null  # Projects dir exists?
ls -d ~/.claude/memory/ 2>/dev/null    # Memory dir exists?
```

Count skills and agents:
```bash
# Count skill directories (each has a SKILL.md)
find ~/.claude/skills -name 'SKILL.md' -maxdepth 2 | wc -l

# Count agent .md files
find ~/.claude/agents -name '*.md' | wc -l
```

Check if `agency` CLI is on PATH:
```bash
which agency 2>/dev/null || echo "NOT ON PATH"
```

If anything is missing, tell the user:
```
Some components are missing. Run this first:
  cd <repo-path> && ./install.sh
Or:
  cd <repo-path> && node cli/bin/agency.js init
Then re-run /onboard.
```

If everything checks out:
```
✓ Installation verified
  Skills: {n} installed
  Agents: {n} installed
  CLI: agency on PATH
```

---

## Phase 3 — Enable Slash Commands (Skills)

Explain how skills work:

```
Skills are slash commands. Type / in Claude Code and you'll see them.
The Agency installed {n} skills. Here are the essential ones:

  Session lifecycle:
    /save-state [slug]     Save everything before closing
    /recall [slug]         Load project briefing at session start
    /pd-resume [slug]      Resume a PD with full context

  Coordination:
    /swarm                 Status check across all projects
    /delegate              Hand off work to a specialist agent

  Content:
    /content-polish        Humanize + proofread in one pass
    /blog-pipeline         Research → write → polish blog post

  Quality:
    /qa                    Run QA gates on current work
    /review                Code review via subagent

  Planning:
    /autoplan              CEO + design + engineering review pipeline

Try one now — type /recall to see if any projects exist.
```

Verify skills are actually loadable by checking a sample:
```bash
test -f ~/.claude/skills/save-state/SKILL.md && echo "save-state OK"
test -f ~/.claude/skills/recall/SKILL.md && echo "recall OK"
test -f ~/.claude/skills/delegate/SKILL.md && echo "delegate OK"
```

---

## Phase 4 — Connect CLI Tools

Check which CLI tools are available and guide setup for any that are missing:

### 4a. Agency CLI
```bash
agency help 2>/dev/null
```
If not found: guide them through `./install.sh` or `node cli/bin/agency.js init`.

### 4b. Git (required)
```bash
git --version
```

### 4c. Optional tools (check and inform, don't block)
```bash
# Graphify — knowledge graph generation
which graphify 2>/dev/null && echo "graphify OK" || echo "graphify not installed (optional — for /graphify skill)"

# gws — Google Workspace CLI
which gws 2>/dev/null && echo "gws OK" || echo "gws not installed (optional — for Gmail/Drive/Calendar)"

# agent-browser — headless browser automation
which agent-browser 2>/dev/null && echo "agent-browser OK" || echo "agent-browser not installed (optional — for /browse skill)"
```

Report a summary:
```
CLI tools:
  ✓ agency          Project management CLI
  ✓ git             Version control
  ○ graphify        Knowledge graphs (optional)
  ○ gws             Google Workspace (optional)
  ○ agent-browser   Browser automation (optional)

Optional tools can be installed later. The core system works without them.
```

---

## Phase 5 — Check MCP Server Connections

Check if key MCP servers are accessible. This is informational — don't fail if
they're not connected, just tell the user what they enable.

List what MCP servers the user might want:

```
MCP servers extend what Claude Code can do. You connect them in
Claude Code settings. Here's what's useful with The Agency:

  Already connected (detected in this session):
    {list any MCP servers visible in the current tool list}

  Recommended:
    Playwright     Browser automation for /browse and QA testing
    Pinecone       Long-term memory and semantic search
    Firebase       Deploy and manage Firebase projects
    Supabase       Database and auth

  Optional:
    Gmail/Calendar/Drive    via Google Workspace MCP
    Slack                   Team notifications
    Canva                   Design generation
    Zapier                  8000+ app automations

You can add these anytime in Claude Code settings → MCP Servers.
```

---

## Phase 6 — Create First Project

If no projects exist yet (check `agency status` or `ls ~/.claude/projects/`),
guide through creating one:

```
Let's create your first project.

What are you building? Give me a name and a one-line description.
Example: "my-saas-app" — "Task manager with React and Supabase"
```

Wait for user input. Then run:
```bash
agency new <slug> "<description>"
```

If projects already exist, show them and ask if they want another:
```
You already have projects:
  {list from agency status}

Want to create another, or start working with an existing one?
```

---

## Phase 7 — Guided First Run

Walk through the core workflow with their project:

```
Your project "{slug}" is ready. Here's the daily workflow:

  START OF SESSION
    /recall {slug}
    → Loads where you left off. First time it'll be empty.

  DURING SESSION
    Tell the PD what to build. It decomposes, delegates, and reports.
    Example: "Build the auth system with email + Google OAuth"

  END OF SESSION
    /save-state {slug}
    → Saves everything. Tomorrow /recall picks up exactly here.

  UPDATING THE AGENCY
    agency upgrade
    → Pulls latest skills and agents from GitHub.

  IF THINGS BREAK
    bash rescue.sh
    → Fixes any git/CLI state.

Want to try /recall {slug} now to start your first session?
```

---

## Phase 8 — Summary & Next Steps

```
Onboarding complete. Here's your cheat sheet:

  /recall {slug}          Start a session
  /save-state {slug}      End a session
  /pd-resume {slug}       Resume with full PD context
  /swarm                  Check all projects at once
  /delegate               Hand off to a specialist
  agency upgrade          Get latest updates
  agency status           See all projects

  Docs:
    docs/ARCHITECTURE.md  How the system is structured
    docs/SKILLS.md        Full skill reference
    docs/SETUP.md         Setup troubleshooting

Welcome to The Agency.
```
