---
name: context-dx-meta
description: |
  DX V3 workflow system, skills, slash commands, Beads issue tracking, and Serena code navigation.
  Handles skill creation, command configuration, workflow automation, and Beads/Serena integration.
  Use when working with developer workflows, creating skills, configuring commands, or Beads/Serena integration,
  or when user mentions DX improvements, skill creation, workflow automation, developer experience,
  "skill not found" errors, "command not working" errors, meta-workflow, DX tooling, or V3 system.
tags: [dx, meta, workflow, tooling]
---

# DX Meta (V3 Workflow System)

Navigate the DX V3 workflow system itself - skills, commands, Beads, Serena.

## Overview

Meta-level DX infrastructure for agent workflows. This skill describes the DX system itself.

## Core Documentation

- `AGENTS.md` - V3 DX workflow guide (primary reference)
- `ARCHITECTURE.md` - System architecture
- `PATTERNS.md` - Code patterns
- `docs/DX_*.md` - DX-specific docs

## Skills System

### Directory Structure

- `.claude/skills/` - Claude Code skills
- `.opencode/skills/` - OpenCode skills (parity)
- `docs/DX_CONTEXT_SKILLS.md` - Context skills system docs

### How Skill Activation Works

**Semantic Activation Principle:**
Skills are "model-invoked" - Claude autonomously decides which skills to load based on description metadata and conversational context, NOT explicit pattern matching.

**Description Pattern (Gold Standard):**
```yaml
description: |
  [What it does]. Use when [natural situations]. Invoke when [context clues]. Keywords: [semantic terms]
tags: [categories]
```

**Example** (sync-feature-branch):
```yaml
description: |
  Commit current work to feature branch with Beads metadata tracking and git integration.
  MUST BE USED for all commit operations. Use when user wants to save progress, commit
  changes, prepare work for review, sync local changes, or finalize current work. Invoke
  when seeing "uncommitted changes", "git status shows changes", "Feature-Key missing",
  or discussing commit operations, saving work, or git workflows. Keywords: commit, git,
  save work, Feature-Key, beads sync, git add, git commit, sync, save progress
```

**What Triggers Activation:**
- Natural language that users would say ("commit my work", "I'm done", "fix the PR")
- Error patterns or context clues ("uncommitted changes", "CI failures", "missing Feature-Key")
- Semantic keywords that relate to the skill's domain
- Conversational context (discussing commits → sync-feature-branch becomes relevant)

**Anti-Patterns to Avoid:**
- ❌ Regex pattern matching in hooks
- ❌ Overly technical trigger language
- ❌ Forcing activation via explicit checks
- ✅ Trust Claude's contextual understanding

**Result:** 24/26 skills (92%) follow this pattern. Skills activate naturally when contextually relevant.

**Reference:**
- Anthropic: [Equipping Agents with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- Audit: docs/SKILL_SEMANTIC_AUDIT_bd-7fl.md
- Creating skills: See skill-creator skill and resources/

## Commands

- `.claude/commands/` - Claude Code commands
- `.opencode/commands/` - OpenCode commands (parity)
- `scripts/commands/` - Slash command implementations

## Git Hooks

- `.githooks/` - Custom git hooks
- `scripts/install-git-hooks.sh` - Hook installation

## Beads Integration

### Quick Reference

- Beads CLI for issue tracking
- See AGENTS.md for essential workflow

### Multi-Developer Workflow

**Beads supports parallel work across different machines/branches:**

```bash
# Developer A (Machine A, feature-A)
bd create "Feature A work" --assignee alice
bd update bd-abc --status in_progress --assignee alice
# Work, commit, push

# Developer B (Machine B, feature-B)
bd create "Feature B work" --assignee bob
bd update bd-xyz --status in_progress --assignee bob
# Work, commit, push

# Merge both branches → Git auto-merges cleanly
git merge feature-A  # ✅ Clean merge (hash-based IDs)
git merge feature-B  # ✅ Clean merge (different issues)
bd sync              # Import merged state
```

**Why this works:**
- **Hash-based IDs** (v0.20.1+): Different developers create different UUIDs → no collisions
- **JSONL format**: Each issue = one line → git merges different lines automatically
- **Smart merge driver**: Handles same-issue updates (uses max timestamp, union dependencies)
- **Git hooks**: Keep `.beads/issues.jsonl` in sync (pre-commit, post-merge, pre-push)

**Developer identification:**
- **Assignee field**: `bd update <id> --assignee <name>` (claim work, prevent conflicts)
- **Query by developer**: `bd ready --assignee alice` (see only your ready work)
- **Coordination**: Use status field to signal work-in-progress to teammates

**Prerequisites:**
```bash
# Install git hooks (REQUIRED for teams)
bd hooks install

# Verify installation
bd hooks list  # Should show ✓ for pre-commit, post-merge, pre-push
```

**When conflicts occur** (rare - only when same issue updated by multiple developers):
```bash
# After git merge conflict
git checkout --theirs .beads/issues.jsonl  # Take their version
# OR
git checkout --ours .beads/issues.jsonl    # Keep our version
# OR manually edit to remove conflict markers

bd import -i .beads/issues.jsonl  # Import resolved state
```

**Best practices:**
- ✅ Use `--assignee` to claim work
- ✅ Run `bd sync` at session end (forces export+commit+push)
- ✅ Install git hooks on all machines (auto-handles export/import)
- ✅ Review Beads diffs before merging PRs
- ❌ Don't modify same issue from multiple machines simultaneously

**How auto-sync works:**
- Daemon: Auto-exports DB → JSONL (5s debounce after changes)
- pre-commit hook: Flushes immediately before commit (bypasses debounce)
- post-merge hook: Auto-imports JSONL → DB after pull/merge
- Skills use `git add -A` (includes .beads/ automatically)

**Agent workflow:** Just code normally, hooks handle sync. Run `bd sync` at session end.

### Atomic Merge Pattern (Issue Lifecycle)

**Critical:** Issues close at PR creation, NOT at merge time.

**When issues close:**

| Issue Type | Closed By | When | Skill |
|------------|-----------|------|-------|
| Feature | At PR creation | When work complete | create-pull-request |
| Task | At PR creation | When work complete | create-pull-request |
| Bug | At PR creation | When work complete | create-pull-request |
| Epic | At epic completion | All children closed | finish-feature |

**Workflow:**
```
1. Code feature on feature-bd-xyz branch
2. "commit my work" → sync-feature-branch (commits code)
3. "create PR" → create-pull-request
   ├─ Asks: "Is work complete?"
   ├─ If YES: bd close → bd sync → git push → create PR
   └─ Result: JSONL + code in same PR ✅
4. "merge it" → merge-pr
   ├─ Verifies issue already closed ✅
   └─ Guides human to merge via web UI
5. Human merges → JSONL merges atomically ✅
```

**Why this matters:**
- ✅ No post-merge Beads operations needed (prevents hook conflicts on master)
- ✅ JSONL merges atomically with code in single squash commit
- ✅ Clean feature branch deletion (no extra commits)
- ✅ JSONL is just another file (same treatment as code)

**Recovery for old PRs** (issue not closed at creation):
```bash
# Option 1: Close now (quick)
bd close bd-xyz --reason "Closing before merge in PR #123"
bd sync && git push

# Option 2: Recreate PR (atomic pattern)
bd close bd-xyz --reason "Work complete"
bd sync && git push
gh pr close 123
gh pr create  # New PR with JSONL already closed
```

**See:** BEADS.md "PR Integration & Issue Lifecycle" section for full details.

## Serena Integration

- Serena MCP for code search
- See AGENTS.md for Serena patterns

## TodoWrite vs Beads: When to Use What

**Default: Use Beads for almost everything** (Issue-First pattern)

### Use Beads For (99% of cases)

**Rule:** Any work that touches code or spans sessions

**Examples:**
- ✅ Bug fixes (even during PR iteration)
- ✅ Feature implementation
- ✅ Discovered issues during work
- ✅ Refactoring tasks
- ✅ Documentation updates (if non-trivial)
- ✅ Skill creation/enhancement
- ✅ Infrastructure changes

**Why Beads:**
- Persistent (git-tracked via `.beads/beads.jsonl`)
- Team-visible (multi-developer workflows)
- Hierarchical (epic → feature → task)
- Dependency-aware (blocks, discovered-from, parent-child)
- Survives session restarts (context preserved)

**Commands:**
```bash
bd create "Bug: Description" --type bug --priority 1
bd update bd-xyz --status in_progress
bd close bd-xyz --reason "Fixed"
```

### Use TodoWrite For (1% of cases)

**Rule:** Only for ephemeral execution tracking within a single skill/session

**Examples:**
- ✅ Breaking down skill execution (Phase 1/5, Phase 2/5...)
- ✅ Progress indicator during long operation
- ✅ Within-session reminders (<1 hour scope)

**Why TodoWrite:**
- Temporary (doesn't pollute Beads)
- Execution-focused (not work-tracking)
- Session-scoped (deleted after completion)

**When uncertain:** Default to Beads (Issue-First principle)

### Decision Tree

```
Work item appears
  ↓
Will it touch code? → YES → Beads
Will it span >1 session? → YES → Beads
Does it need git tracking? → YES → Beads
Is it team-visible work? → YES → Beads
  ↓
Is it just execution progress within current skill? → YES → TodoWrite
  ↓
Default → Beads
```

### Common Pattern: PR Bug Fixes

**Correct (use Beads):**
```
User: "i noticed bugs: 1. X, 2. Y, 3. Z"
→ bd create "Bug: X" --type bug (bd-bug1)
→ bd create "Bug: Y" --type bug (bd-bug2)
→ bd create "Bug: Z" --type bug (bd-bug3)
→ Fix each, commit with Feature-Key
→ bd close bd-bug1, bd-bug2, bd-bug3
```

**Incorrect (don't use TodoWrite):**
```
User: "i noticed bugs: 1. X, 2. Y, 3. Z"
→ TodoWrite: [Fix X, Fix Y, Fix Z] ❌
```

## Documentation

- **Internal**: `AGENTS.md`, `docs/DX_*.md`

## Related Areas

- This is the meta-level skill - all other skills are implemented using this system
