---
name: dotnet-techne-code-review
description: "Use when reviewing PRs/diffs/branches/documents for .NET quality, correctness, performance, security, data access, messaging, and observability. Includes adversarial critical-thinking mode for skeptical/cynical review requests. Keywords: code review, review PR, review diff, critical review, cynical review, adversarial review, production readiness, low GC, AOT, security review."
disable-model-invocation: false
user-invocable: true
license: MIT
compatibility: Requires git and bash (Linux/macOS) or PowerShell (Windows). Works with any AI agent that supports the Agent Skills specification and has file read and command execution tools.
metadata:
  author: Metalnib
  version: "1.6.0"
  trigger_keywords:
    - code review
    - review pr
    - review diff
    - critical review
    - cynical review
    - adversarial review
    - production readiness
    - low gc
    - aot
    - security review
---
# End-to-end .NET Code Review

Lean entrypoint for high-signal .NET review. Detailed commands/checklists/output requirements are split into reference files for progressive disclosure.

On Claude Code with this plugin installed, prefer `/dotnet-episteme-skills:dotnet-review` for parallel multi-agent review (4 domain specialists + a generalist + adversarial maintainer verification). This file remains the complete single-context procedure for all other tools.

## Requirements
This skill requires:
- **Git** for diff and commit analysis
- **Bash/Zsh** (Linux/macOS) or **PowerShell 5.1+** (Windows)
- **Agent tools** with file read capability and shell command execution

Optional but recommended:
- `rg` (ripgrep) for faster dependency searches on Linux/macOS
- `dotnet` CLI for build verification

## When to use this skill
Use this skill when the user asks for:
- PR / branch / diff / commit-range review
- "code review this implementation"
- "critical review of ..."
- "cynical review of ..."
- adversarial / devil's-advocate review
- production-readiness review (performance, AOT/trimming, security, observability, DB, messaging)

## Reference files (read on demand)
- `references/scripts-and-context.md`
  - Read first when gathering change context and choosing script commands.
- `references/domain-checklists.md`
  - Read after context is loaded; focus on only the relevant sections for changed components.
- `references/output-contract.md`
  - Read before writing the final review output.
- `references/maintainer-playbook.md`
  - Read during the falsification pass (Step 3) to pressure-test findings before output.

## Review modes

### Standard mode (default)
- Balanced review focused on correctness, maintainability, and risk.

### Cynical mode (adversarial)
Use when request language is explicitly skeptical: "critical review", "cynical review", "tear this apart", "assume this is broken", "devil's advocate".

Mandates:
- Assume defects exist until disproven.
- Prefer failure-mode discovery over style nits.
- Generate **at least 5 issue hypotheses** before finalizing.
- Validate each hypothesis with evidence; remove weak/speculative findings.

## Core workflow

### Step -1: Receive content
- Load content from provided input or current context.
- If content is empty (no diff/branch/files/document), ask for clarification and stop.
- Identify content type: diff, branch, uncommitted changes, commit range, or document/spec.

### Step 0: Gather context
- Read `references/scripts-and-context.md`.
- Run the baseline context commands.
- Read changed files with your file-read tool.

### Step 1: Select review mode
- Use **Cynical** mode for explicitly skeptical requests.
- Otherwise use **Standard** mode.

### Step 2: Establish component context
- Identify component type(s): API, worker, repository, domain, messaging, etc.
- Identify critical paths: request path, message path, DB path.
- Identify invariants: idempotency, correlation, ordering, transaction boundaries.

### Step 3: Adversarial hypothesis pass
- Generate candidate defects (at least 5 in cynical mode).
- For each hypothesis, collect direct evidence (`file:line`, snippet, or command output).
- Try to falsify each hypothesis (tests, guards, explicit design intent, invariants).
- Apply `references/maintainer-playbook.md` to each surviving finding (maintainer persona, five checks, evidence-backed verdicts).
- Keep only confirmed/high-signal findings.

### Step 4: Domain checklist pass
- Read `references/domain-checklists.md`.
- Apply only relevant sections based on changed files and architecture.
- If scope is unclear, run all sections but prioritize correctness/security/data-loss risks first.

### Step 5: Produce findings
- Read `references/output-contract.md`.
- Format output exactly as specified there.
