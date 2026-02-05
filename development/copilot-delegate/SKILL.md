---
name: copilot-delegate
description: Delegate GitHub operations and research tasks to Copilot CLI to preserve Claude Code session limits. Automatically activates when detecting GitHub keywords (issue, PR, repo, commit) or research needs (compare, research, lookup, best practices). Offloads heavy operations to Copilot subprocess and returns compressed results only.
---

# Copilot Delegate

Preserve Claude Code session limits by delegating GitHub operations and research tasks to GitHub Copilot CLI.

## Purpose

This skill enables intelligent task delegation to preserve Claude Code's limited session capacity:

- **Pro plan:** 10-40 prompts per 5 hours
- **Max 5x:** 50-200 prompts per 5 hours
- **Max 20x:** 200-800 prompts per 5 hours

By delegating GitHub operations and research to Copilot CLI (which runs in a subprocess), you preserve your main Claude Code session for critical thinking, architecture decisions, and implementation.

## When to Use This Skill

### Automatic Activation Triggers

The skill activates when Claude detects these keywords in user prompts:

**GitHub Operations:**
- "create issue"
- "list issues"
- "create PR" / "pull request"
- "merge PR"
- "check status"
- "repo stats"
- "commit history"
- "branch operations"

**Research Tasks:**
- "research"
- "compare"
- "best practices"
- "which library"
- "lookup documentation"
- "what's the best"
- "evaluate"

### Manual Activation

Use when you need to:
- Perform bulk GitHub operations
- Research libraries/tools/technologies
- Analyze documentation
- Compare multiple options
- Preserve session capacity for later

## Core Workflows

### 1. GitHub Issue Management

**Create a single issue:**

```bash
./scripts/github_operation.sh create-issue \
  "Fix authentication bug" \
  "Users cannot login with OAuth. Error at auth.ts:42" \
  "bug,priority-high"
```

**List issues:**

```bash
./scripts/github_operation.sh list-issues . open 20
```

**Query repo:**

```bash
./scripts/github_operation.sh query \
  "Show last 10 commits with authors and dates"
```

### 2. Pull Request Operations

**Create PR:**

```bash
./scripts/github_operation.sh create-pr \
  "Add OAuth authentication" \
  "Implements Auth0 integration. Fixes #123" \
  main \
  feature/oauth
```

### 3. Research Tasks

**Compare libraries:**

```bash
./scripts/research_task.sh compare \
  "zustand,jotai,recoil" \
  "bundle-size,DX,performance"
```

**Research best practices:**

```bash
./scripts/research_task.sh best-practices \
  "React performance optimization" \
  2025
```

**Look up documentation:**

```bash
./scripts/research_task.sh documentation \
  "Next.js App Router" \
  "server components"
```

**Research a specific library:**

```bash
./scripts/research_task.sh library \
  "zustand" \
  "React state management"
```

### 4. General Delegation

For any task not covered by specialized scripts:

```bash
./scripts/delegate_copilot.sh "Your task description here"
```

Or with a task file:

```bash
./scripts/delegate_copilot.sh --task-file tasks/custom-task.json
```

## Session Preservation Strategy

### Decision Matrix

| Task Type | Consume (Prompts) | Delegate? | Reason |
|-----------|-------------------|-----------|---------|
| **Create GitHub issue** | 1-3 | ✅ Yes | Saves 1-3 prompts, simple operation |
| **Research library** | 5-10 | ✅ Yes | Saves 5-10 prompts, Copilot has web access |
| **Compare 3 options** | 10-15 | ✅ Yes | Saves 10-15 prompts, research-heavy |
| **List issues** | 1-2 | ✅ Yes | Saves 1-2 prompts, bulk data retrieval |
| **Quick code fix** | 1 | ❌ No | Overhead not worth it, context-dependent |
| **Architecture decision** | 2-5 | ❌ No | Requires conversation context, critical thinking |
| **Debug with stack trace** | 3-7 | ❌ No | Context-dependent, needs repo understanding |

### Example Savings

**Scenario: Research and implement state management**

Without delegation:
1. Research zustand: 5 prompts
2. Research jotai: 5 prompts
3. Research recoil: 5 prompts
4. Compare findings: 3 prompts
5. Best practices: 5 prompts
6. Implement: 10 prompts
7. Test: 5 prompts

**Total: 38 prompts** (Pro plan maxed out in one task!)

With delegation:
1. Delegate research (all libraries): 0 prompts (subprocess)
2. Delegate comparison: 0 prompts (subprocess)
3. Delegate best practices: 0 prompts (subprocess)
4. Review findings: 1 prompt
5. Implement: 10 prompts
6. Delegate testing: 0 prompts (subprocess)
7. Review test results: 1 prompt

**Total: 12 prompts** (68% savings!)

## How It Works

### Architecture

```
User: "Create a GitHub issue for bug X"
    ↓
Claude detects: GitHub operation keyword
    ↓
Skill activates: copilot-delegate
    ↓
Claude executes: ./scripts/github_operation.sh create-issue "..." "..." "..."
    ↓
Script launches: Copilot CLI in subprocess
    ↓
Copilot executes: gh CLI commands
    ↓
Copilot returns: JSON result
    ↓
Script saves: copilot-results/github_issue_<timestamp>.json
    ↓
Claude reviews: Compressed JSON result (~500 tokens)
    ↓
Claude responds: "Issue created: #<number> <url>"

Session impact: 1 Claude prompt vs. 3-5 without delegation
```

### Output Format

All delegation scripts return results in:

**Main result file:**
```json
{
  "issue_number": 123,
  "issue_url": "https://github.com/user/repo/issues/123",
  "title": "Fix authentication bug",
  "status": "created"
}
```

**Metadata file (*.meta):**
```json
{
  "status": "success",
  "duration_seconds": 12.7,
  "timestamp": "2025-10-27T20:15:00Z",
  "tokens_estimate": 450,
  "characters": 1800,
  "cli": "copilot"
}
```

## Task Templates

Pre-built templates available in `assets/task-templates/`:

### github-issue.json
Template for creating GitHub issues with customizable title, body, and labels.

### github-pr.json
Template for creating pull requests with title, body, base, and head branches.

### research.json
Template for research and comparison tasks with configurable options and criteria.

**Usage:**

```bash
# Copy template
cp assets/task-templates/github-issue.json tasks/my-issue.json

# Customize
vim tasks/my-issue.json

# Execute
./scripts/delegate_copilot.sh --task-file tasks/my-issue.json
```

## Performance Characteristics

### Speed

- **Copilot execution:** 12.7s average
- **Script overhead:** 2-3s
- **Total:** ~15s per delegation
- **Faster than:** Sequential Claude prompts (30-60s)

### Cost

- **Copilot:** Subscription model (~1 Premium request per query)
- **Claude Code:** Token-based (~$0.12 per equivalent query)
- **Net savings:** Preserve Claude Code sessions (limited resource)

### Quality

- **GitHub operations:** ⭐⭐⭐⭐⭐ (Native gh CLI integration)
- **Research tasks:** ⭐⭐⭐⭐ (Web access, current data)
- **Code analysis:** ⭐⭐⭐ (Practical, concise)

Use Claude Code for deep analysis and architecture; use Copilot for data retrieval and bulk operations.

## Best Practices

### 1. Batch Similar Operations

**Bad:**
```bash
./scripts/github_operation.sh create-issue "Bug 1" "..."
./scripts/github_operation.sh create-issue "Bug 2" "..."
./scripts/github_operation.sh create-issue "Bug 3" "..."
```

**Good:**
```bash
# Create single task file with batch operation
./scripts/delegate_copilot.sh --task-file tasks/batch-issues.json
```

### 2. Review Results Before Acting

Always review Copilot's output before using it in implementation:

```bash
# Delegate research
./scripts/research_task.sh compare "optionA,optionB,optionC"

# Claude reviews result
cat copilot-results/research_compare_*.json

# Claude makes decision based on findings
# Claude implements chosen solution
```

### 3. Use Specific Prompts

**Bad:**
```bash
./scripts/research_task.sh general "What about React state?"
```

**Good:**
```bash
./scripts/research_task.sh compare \
  "zustand,jotai,recoil" \
  "bundle-size,TypeScript-support,ecosystem,DX"
```

### 4. Monitor Session Usage

Check remaining capacity regularly:

```
/status
```

If approaching limit, delegate more aggressively.

### 5. Preserve Context for Critical Tasks

Delegate routine tasks early to save sessions for:
- Architecture decisions
- Security reviews
- Complex debugging
- Code reviews requiring full context

## Troubleshooting

### "Command not found: copilot"

**Solution:** Install GitHub Copilot CLI:

```bash
# Install
npm install -g @githubnext/github-copilot-cli

# Verify
copilot --version
```

### "Authentication required"

**Solution:** Login to GitHub Copilot:

```bash
copilot login
```

### "Timeout after 60s"

**Solution:** Increase timeout:

```bash
# Temporary (this execution only)
export COPILOT_TIMEOUT=120

# Permanent (add to shell rc)
echo 'export COPILOT_TIMEOUT=120' >> ~/.zshrc
```

### "Invalid JSON output"

**Issue:** Copilot returned markdown-wrapped JSON or plain text.

**Solution:** Our scripts handle this automatically. If using Copilot directly:

```bash
copilot -p "..." --allow-all-tools | \
  sed 's/```json//g; s/```//g' | \
  jq '.'
```

### "No result file generated"

**Solution:** Check logs:

```bash
ls -la copilot-results/*.meta
cat copilot-results/<latest>.meta
```

Check for errors in metadata file.

## References

For deeper information, see:

- **`references/session-preservation.md`** - Detailed session management strategies
- **`references/copilot-capabilities.md`** - What Copilot excels at and limitations

Load references when you need specific guidance on when/how to delegate.

## Quick Reference

```bash
# GitHub Operations
./scripts/github_operation.sh create-issue "title" "body" "labels"
./scripts/github_operation.sh list-issues [repo] [state] [limit]
./scripts/github_operation.sh create-pr "title" "body" [base] [head]
./scripts/github_operation.sh query "query description"

# Research Tasks
./scripts/research_task.sh library "name" [use-case]
./scripts/research_task.sh compare "opt1,opt2,opt3" [criteria]
./scripts/research_task.sh best-practices "topic" [year]
./scripts/research_task.sh documentation "tool" [feature]
./scripts/research_task.sh general "question"

# General Delegation
./scripts/delegate_copilot.sh "task description"
./scripts/delegate_copilot.sh --task-file tasks/task.json

# Results
cat copilot-results/<latest>.json       # View result
cat copilot-results/<latest>.meta       # View metadata
ls -lt copilot-results/                 # List all results
```

## Summary

**Use this skill to:**
- ✅ Preserve Claude Code sessions (50-80% savings)
- ✅ Offload GitHub operations to native gh CLI integration
- ✅ Delegate research to Copilot (has web access)
- ✅ Get faster results (12.7s vs. 30-60s)
- ✅ Maintain context in main Claude session

**Don't use for:**
- ❌ Critical architecture decisions
- ❌ Security audits requiring deep analysis
- ❌ Context-dependent debugging
- ❌ Tasks requiring iterative refinement

**Result:** Focus Claude Code on high-value thinking, delegate routine operations to Copilot.
