---
name: research-result-commit
description: Commit completed remote experiment results in the nested research_workspace repository. Use after pulling remote artifacts, ingesting metrics, updating research_workspace/EXPERIMENTS.csv or research_workspace/STATE.md, generating experiment analysis/next-step/search-evidence files, or whenever current ExpID research outputs should be consolidated into one linked research_workspace commit.
---

# Research Result Commit

## Overview

Use this workflow to turn a completed experiment result ingest into one auditable `research_workspace` commit. Keep `issues/`, `docs/`, source code, configs, scripts, and tests in the main repository; this skill only handles the nested `research_workspace` repository.

## Workflow

1. Identify the current `ExpID`.
   - Prefer the user-provided ExpID or the active mission/CSV context.
   - If absent, infer it from changed paths under `research_workspace/experiments/<ExpID>/`.
   - If multiple ExpIDs changed and the intended scope is unclear, stop and ask for the minimal clarification.

2. Inspect both repository boundaries.
   - In the main repository, note the associated branch and commit when the experiment depends on current main-repo code or workflow:
     `git branch --show-current` and `git rev-parse --short HEAD`.
   - Run `git -C research_workspace rev-parse --show-toplevel`. Its resolved path must be exactly `<PROJECT_ROOT>/research_workspace`, with its own Git metadata. A successful Git command alone does not establish independence: Git searches parent directories.
   - If it resolves to the code repository, do not stage or commit research files through this skill. Initialize a dedicated repository with `git init -b main research_workspace`, preserve the existing files, and confirm its top-level directory. If the code repository already tracks research data, preserve its history and complete that tracking migration before committing experiment results. A template checkout may distribute tracked examples; it is not an initialized project research repository.
   - In the verified research repository, run `git status --short` and `git diff --stat`.
   - Do not stage or commit `issues/`, `docs/`, source code, configs, scripts, or tests from this workflow.

3. Select only files belonging to the current experiment result.
   - Always consider `experiments/<ExpID>/`, `EXPERIMENTS.csv`, and `STATE.md`.
   - Include other `research_workspace` files only when they are clearly tied to the current ExpID, such as command records, search evidence, analysis drafts visualization notes, or next-step documents.
   - Exclude unrelated dirty files and unrelated experiments, even if they are already present in `research_workspace`.

4. Stage deliberately.
   - Use explicit `git add` paths, for example:

```bash
cd <PROJECT_ROOT>/research_workspace
git add experiments/<ExpID> EXPERIMENTS.csv STATE.md
git add <other-current-ExpID-research-files>
git diff --cached --stat
```

5. Commit once.
   - Use one commit for the pulled artifacts, records, analysis, search evidence, and state updates for this ExpID.
   - Use the project commit style. Template:

```text
📃 docs(exp): 记录 <ExpID> 远程结果与分析

Why:
- 固化本次远程训练/评估的日志、指标、分析和可恢复状态

Why this works:
- 当前 ExpID 的 artifacts/analysis/search evidence 保存结论证据
- EXPERIMENTS.csv 与 STATE.md 记录实验状态
- 关联主仓库: <branch> @ <commit>

Remaining:
- <下一步、已知限制或 validation_gap>
```

6. Report the result.
   - Return the `research_workspace` commit SHA.
   - Mention any excluded dirty files or `validation_gap`.
