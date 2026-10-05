---
name: autonomous-fix-review
description: Run autonomous multi-model code review on a finding. Invokes claude/codex/gemini via reviewd, evaluates consensus, and auto-commits or escalates to human.
user-invocable: true
argument-hint: <finding-file-or-description>
context: fork
---

# Autonomous Fix-Review Pipeline

Give it a finding, walk away, come back to a committed fix that passed multi-model review.

## Usage

```
/autonomous-fix-review "Fix the null pointer in src/main.py:42"
/autonomous-fix-review docs/research/trail/findings/finding-001.yaml
```

## 7-Phase Pipeline

| Phase | Action | Tool |
|-------|--------|------|
| 1. Research | Gather context (docs, code) | /find-docs, /context7-mcp |
| 2. Implement | Dispatch coder in worktree with TDD | subagent-driven-development |
| 3. Review | Invoke claude + codex + gemini | reviewd.invoke_cli() |
| 4. Consensus | Evaluate 75% threshold | mde.consensus.evaluate_consensus() |
| 5. Decision | Apply autonomy mode | ConsensusGate.apply_autonomy() |
| 6. Quality gate | Run lint + test + validate | uv run mde-py quality |
| 7. Commit | Commit on feature branch or escalate | git commit |

## Autonomy Modes

- **supervised**: Human approves everything except unanimous approval
- **semi-autonomous** (default): Auto-retry on warnings, escalate on disagreement
- **autonomous**: Proceed on any non-abort consensus

## Decision Matrix

| Consensus | Supervised | Semi-Autonomous | Autonomous |
|-----------|-----------|-----------------|------------|
| >= 90% approve, no criticals | PROCEED | PROCEED | PROCEED |
| >= 75% approve, no criticals | ESCALATE | RETRY | PROCEED |
| Any critical findings | ESCALATE | ESCALATE | ESCALATE |
| < 75% approve | ESCALATE | ESCALATE | ESCALATE |
| All reject | ABORT | ABORT | ABORT |

## Workflow

```bash
# Step 1: Parse the finding
finding=$(echo "$ARGUMENTS")

# Step 2: Research context
# Invoke /find-docs and /context7-mcp for the affected code area

# Step 3: Implement fix (if not already done)
# Dispatch coder subagent in worktree with TDD

# Step 4-5: Run multi-model review + consensus
uv run mde-py review "$finding" --autonomy semi-autonomous

# Step 6: Quality gate (auto-runs unless --skip-quality)
uv run mde-py quality

# Step 7: Based on decision output:
# PROCEED → commit on feature branch
# ESCALATE → present findings to human for decision
# RETRY → re-implement and re-review (up to max_retries)
# ABORT → stop, finding may be invalid
```

## Constraints

- Zero API keys — all LLM calls via subscription CLIs (claude, codex, gemini)
- Worktree isolation for implementation phase
- Human interview ONLY on consensus disagreement (ESCALATE)
- Quality gate (6/6) required before commit
