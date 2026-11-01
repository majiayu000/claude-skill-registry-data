---
name: git-worktree-discipline
version: "1.1.0"
user-invocable: false
description: "Pre-write (docs or code) git/native worktree isolation with worktree-gate (always|never|ask; unset≡ask): detect reuse (incl. submodule guard), recommend suitability, create (native then ignored .worktrees/), setup+baseline, or decline/lean with 留痕; cleanup via feature-branch-closeout. Triggers — 「git worktree」「工作区隔离」「隔离工作区」「执行前隔离」「worktree 门控」 / git worktree discipline. Do NOT use as Superpowers using-git-worktrees alias or for closeout destroy."
---

# Git Worktree Discipline

> Internal shared skill. Optional **create/detect** isolation before the first non-trivial write (docs or code). Hosts declare it in `dependencies` and abort if missing.
>
> **Name note:** intentionally **not** named `using-git-worktrees`. Use `git-worktree-discipline` only. Operational create/detect/setup details live in `reference.md` (inspired by common worktree practice; no external skill dependency).

## When to run

Before the first non-trivial persistent write (docs or code) in the host run. Skip the create offer only when already isolated for this change, or gate/`never`, or lean/hotfix in-place 留痕 this session.

## Loop

1. **Detect** — already in a linked worktree for this change? Reuse (do not nest). Distinguish **submodule** from worktree before concluding isolation. Commands: `reference.md`.
2. **Resolve preference** — `worktree-gate` in `AGENTS.md` / `CLAUDE.md`: `always` | `never` | `ask`. Unset ≡ `ask`.
3. **Recommend (ask / always)** — suitability from project state (sibling `../` scripts, full product pack, dirty primary tree). Good for code + unit tests; poor for pack without path rebinding.
4. **Act by gate**
   - `never` → skip create; `【工作区隔离跳过】escape=worktree-gate-never；reason=…`
   - `always` → create when possible (no ask)
   - `ask` → after recommendation, ask: create / decline / lean; do not silently create
5. **Create** — prefer the agent’s **native** workspace/worktree capability when available (avoids harness-invisible phantom git worktrees); else git fallback under ignored project-local dir (`.worktrees/` preferred). Verify ignore with `git check-ignore`. Path priority and failure fallback: `reference.md`.
6. **Setup + baseline** — in the new workspace, run project-appropriate install/build and a baseline test/typecheck when the project has one; if baseline fails, report and ask whether to proceed or investigate. Skip install/baseline only when no project markers apply.
7. **Lean/hotfix / decline** — `【工作区隔离跳过】escape=lean-hotfix|user-decline；reason=…`

Do **not** replace design approval. Do **not** silently destroy isolation mid-run. Do **not** imply one-click full product pack inside a worktree.

## Cleanup ownership

**Destroy/remove** after verify/archive → `feature-branch-closeout` optional cleanup. This skill may note the remove command symmetric to create.

## Integration guide

- Hosts: one line before the first artifact/code write — load this skill (worktree gate + optional isolation).
- Compose with `feature-branch-closeout` for cleanup only.
- Prefer `user-invocable: false`.
- Full detect/create/setup checklist: `reference.md`.
