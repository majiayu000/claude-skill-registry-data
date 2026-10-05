---
name: hooks-setup
description: Use when user says "install hooks", "setup hooks", "hooks setup", "configure
  hooks", "/hooks-setup". Installs and configures 1ai-skills auto-evolve hooks for
  Claude Code.
domain: meta
author: oyi77
license: Apache-2.0
subdomain: meta-skills
tags:
- hooks
- meta-learning
- self-improvement
- setup
- skill-evolution
version: 1.0.0
category: meta
---


# Hooks Setup — AI Agent Installation Guide

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Overview

Installs and configures 1ai-skills auto-evolve hooks. Tracks skill usage, captures feedback, auto-commits improvements, evolves underperforming skills.

## When to Use

**Trigger phrases:**
- "hooks setup"
- "User says "install hooks", "setup hooks", "hooks setup""
- "User says "configure hooks", "hook installation""
- "User types "/hooks-setup""


**Activate when:**
- User says "install hooks", "setup hooks", "hooks setup"
- User says "configure hooks", "hook installation"
- User types "/hooks-setup"
- Session-start detection reports hooks missing/outdated
- User asks "how do I enable auto-evolve?"

**Skip when:**
- Hooks already installed and up to date
- User explicitly says "skip hooks" or "no hooks"

## Agent Workflow
1. Receive input and validate format
2. Route to appropriate handler based on input type
3. Execute core operation with monitoring
4. Transform output to expected format
5. Return results or trigger follow-up actions


### Step 1: Check Status

```bash
node scripts/hooks-cli.js status
```

If all green (version match, 4/4 scripts, 4 entries), tell user hooks already set up. Skip to Step 5.

### Step 2: Install (non-interactive)

```bash
node scripts/install-hooks.js --yes
```

This copies hook scripts, merges settings.json, creates config, writes version stamp. Skips star/fork prompt.

### Step 3: Configure (ask user, write config)

Read current config:

```bash
cat ~/.1ai-skills/evolve-config.json
```

Ask user these questions (one at a time, use AskUserQuestion tool):

1. **Auto-push evolved skills?** (default: no)
   - If yes: "What repo? (e.g. user/repo)"

2. **Success threshold %** (default: 70)
   - Skills below this get auto-evolved

3. **Min invocations before evolving** (default: 5)

4. **Cooldown between evolve cycles** (default: 24 hours)

5. **Enable tracking?** (default: yes)

6. **Enable auto-evolution?** (default: yes)

Write answers to config:

```bash
# Edit ~/.1ai-skills/evolve-config.json with user choices
```

### Step 4: Star/Fork (ask user)

Ask: "Want to star & fork oyi77/1ai-skills on GitHub?"

If yes:
```bash
gh repo star oyi77/1ai-skills
gh repo fork oyi77/1ai-skills --clone=false
```

If no gh CLI: tell user to visit github.com/oyi77/1ai-skills

### Step 5: Verify

```bash
node scripts/hooks-cli.js status
```

Confirm all items green. Tell user hooks are active.

## Direct Commands (no TUI needed)

| Command | Purpose |
|---------|---------|
| `node scripts/install-hooks.js` | Install hooks (prompts star/fork) |
| `node scripts/install-hooks.js --yes` | Install hooks (no prompts) |
| `node scripts/hooks-cli.js status` | Text status report |
| `node scripts/hooks-cli.js uninstall` | Remove hooks cleanly |
| `node hooks/session-start-detect.js` | Health check (silent=healthy) |

## Config File

Location: `~/.1ai-skills/evolve-config.json`

```json
{
  "min_invocations": 5,
  "success_threshold": 70,
  "evolve_cooldown_hours": 24,
  "max_evolves_per_run": 3,
  "auto_push": false,
  "target_repo": "",
  "skill_dirs": ["~/.claude/skills"],
  "repo_dir": "",
  "commit_prefix": "evolve",
  "tracking_enabled": true,
  "evolve_enabled": true
}
```

Agent can read/write this file directly to configure.

## What Gets Installed

**Hook scripts** (to `~/.claude/hooks/`):
- `skill-tracker.js` — logs Skill tool invocations
- `skill-committer.js` — auto-commits skill file changes
- `skill-feedback-capture.js` — detects user feedback signals
- `skill-evolver.js` — identifies underperforming skills

**Settings** (merged into `~/.claude/settings.json`):
- PostToolUse hooks for Skill, Write|Edit tools
- UserPromptSubmit hook for feedback capture
- SessionEnd hook for evolution cycles

**Config** (`~/.1ai-skills/evolve-config.json`):
- Auto-detected agent skill dirs
- Thresholds, cooldown, push settings

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Skills do not need to evolve" | Static skills become outdated. Self-evolving skills improve continuously. |
| "Manual skill management is fine" | With 1000+ skills, manual management is impossible. Automate. |
| "Performance does not matter" | Skill performance directly impacts agent effectiveness. Track it. |