---
name: review-xyz
description: >-
  Deterministic, multi-model code review system and skill for XYZ. Summon frontier
  reviewers (Command Code -> Qwen 3.8-Max, GLM-5.3, OpenRouter, Codex, Agy) to perform
  throwaway-worktree isolated code reviews on local diffs or GitHub PRs. Validates
  `[Blocker]`/`[Should]`/`[Nit]`/`[Pass]` citations and automatically formats or posts
  review critiques and follow-up checklists to GitHub PRs (`--post-pr`) and linked issues
  (`--post-issues`). Use when the operator wants to "review this PR with Qwen", "run a code
  review on this diff", "audit PR with GLM", or post structured review feedback to GitHub.
---

# review-xyz — Deterministic Multi-Model Code Review

`/review-xyz` provides a first-class, structured code review interface that bridges frontier
reasoning models (specifically **Qwen 3.8-Max** and **GLM-5.3** via Command Code, alongside Codex,
Agy, and OpenRouter) into a safe, throwaway-worktree isolated review loop.

---

## Capabilities & Guardrails

1. **Throwaway Worktree Isolation:**
   Every review execution runs inside a temporary, detached git worktree created from `git stash create`.
   Reviewer models have zero write access to your active working directory files (note: `.git` metadata is shared across worktrees per the GH-564 rail).
2. **Citation-Checked Graded Findings:**
   Enforces standardized finding categories with mandatory `file:line` or symbol citations:
   - `[Blocker]`: Correctness regressions, security defects, or data loss hazards.
   - `[Should]`: Architectural gaps, missing test coverage, or edge-case handling.
   - `[Nit]`: Style, documentation, minor cleanups.
   - `[Pass]`: Confirmed correct execution paths with firsthand citations.
3. **GitHub Integration:**
   - Review local uncommitted changes, branches, or PRs (`gh pr diff <PR#>`).
   - `--post-pr`: Automatically post formatted review reports directly to GitHub PR comments via `gh`.
   - `--post-issues`: Scans PR descriptions for linked issues (`Fixes #123`, `Closes #124`, `GH-123`) and posts action checklist follow-ups to those issues.

---

## Quick Usage

### 1. Review Local Uncommitted Diff (Default: Qwen 3.8-Max)
```bash
python3 utils/py/review_xyz.py
```

### 2. Review a GitHub Pull Request with Qwen 3.8-Max
```bash
python3 utils/py/review_xyz.py --pr 124
```

### 3. Review PR and Post Findings + Linked Issue Checklists
```bash
python3 utils/py/review_xyz.py --pr 124 --model "Qwen/Qwen3.8-Max" --post-pr --post-issues
```

### 4. Review with GLM-5.3 or Codex
```bash
python3 utils/py/review_xyz.py --pr 124 --model "zai-org/GLM-5.3"
python3 utils/py/review_xyz.py --diff-file diff.patch --model "codex" --engine codex
```

### 5. Dry-Run / Preview Prompt
```bash
python3 utils/py/review_xyz.py --pr 124 --dry-run
```

---

## Supported Models & Engines

| Model / Family | Engine | Canonical Model String | Default Role |
|---|:---:|---|---|
| **Qwen 3.8-Max** | `commandcode` | `Qwen/Qwen3.8-Max` | **Default Frontier Reviewer** |
| **GLM-5.3 (High)** | `commandcode` | `zai-org/GLM-5.3` | Frontier Reviewer & Builder (Grade A-) |
| **Qwen 3.7-Flash** | `commandcode` | `Qwen/Qwen3.7-Flash` | Fast Low-Cost Reviewer |
| **DeepSeek v4 Pro** | `commandcode` | `deepseek/deepseek-v4-pro` | 1M Context Long-Horizon Reviewer |
| **Aider + OpenRouter** | `aider` | `openrouter/qwen/qwen3.8-max` | API-Metered Reviewer |
| **Codex CLI** | `codex` | `codex` | Subscription Default Reviewer |
| **Antigravity (`agy`)** | `agy` | `agy` | Cost-Blind Cross-Model Reviewer |

---

## Structured Output Schema

Every `/review-xyz` report is structured consistently:

```markdown
## 🛡️ Code Review Report for PR #124 (`fix: example`)

**Verdict:** `Approved` | **Model:** `Qwen/Qwen3.8-Max` (`commandcode`) | **Latency:** `18.2s` | **Diff:** `412 lines`

| Findings | Count |
|:---|:---:|
| 🛑 `[Blocker]` | 0 |
| ⚠️ `[Should]` | 1 |
| 💡 `[Nit]` | 2 |
| ✅ `[Pass]` | 14 |

### Summary & Findings
<Detailed review critique citing exact file:line spans>

### 📋 Actionable Checklist
- [ ] Add regression test for edge-case — `[Should]` `src/engine.py:45`
- [ ] Rename confusing variable `x` — `[Nit]` `src/engine.py:82`
```
