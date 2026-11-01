---
name: delivery-discipline
version: "1.0.0"
user-invocable: true
description: "Optional code-delivery discipline: decide whether this run needs commit + PR/MR, then commit/push via git-commit and create or update the PR/MR. Use after verification (and OpenSpec archive when the host requires it) and before feature-branch-closeout. Do NOT use for protected-branch merge (merge-discipline) or release→main shipping (git-release-finish). Triggers — 「提交并开PR」「提交并开MR」「代码交付」「开PR」「开MR」「delivery-discipline」 / deliver code, commit and open PR, open merge request."
dependencies:
  - git-commit
---

# Delivery Discipline

> Shared skill — single source of truth for **optional** post-verify code delivery: **need-delivery gate → commit/push → open or update PR/MR**. Hosts declare it in `dependencies` and abort if missing — no silent fallback.
>
> **Layering**: `git-commit` (commit/push) → **this skill** (delivery orchestration) → `feature-branch-closeout` (menu) → `merge-discipline` (merge gates). Do not fold merge or release shipping into this skill.

## Prerequisite skill check

On load, verify `git-commit` is available; if missing, abort with install hint (`npx skills add FuDesign2008/open-skills -g --skill git-commit --yes`). No silent degrade.

## Placeholder contracts

| Placeholder | Meaning | Who supplies |
|-------------|---------|--------------|
| `{pr-body-extra}` | Host-specific PR/MR body sections (Jira link, OpenSpec path, scenario tables, etc.) | Referencing host, at the call site |
| `{commit-context}` | Optional commit fields (`type`, `scope`, `subject`, `jira_id`) | Host or inferred from branch/diff |

## When this applies

After verification is green (or pendings are explicitly listed) — and after OpenSpec archive when the host requires archive before delivery — when the run may need commits and/or a PR/MR.

**Not this skill:** merge into a protected branch; release-tag / release→main flows; commit-only with no PR intent (call `git-commit` directly).

## 1. Need-delivery gate

Skip the rest of this skill (no commit, no PR) when **any** of the following holds:

| Signal | Meaning |
|--------|---------|
| Clean delivery surface | No uncommitted changes **and** no commits ahead of the intended PR base (or no feature branch work to publish) |
| User declined | User said this run should not deliver / no PR / analysis-only |
| Host marked non-delivery | Host path is analysis-only or equivalent with no code (or artifact) changes to publish |

When skipping: state the reason in one line and return to the host (typically `feature-branch-closeout` or retrospective). Do **not** open an empty PR.

When delivery **is** needed (dirty tree, ahead commits, or user/host requested PR): continue.

## 2. Commit / push

1. If there are uncommitted changes: load `git-commit` with `execute=true` (unless the user asked for manual commit commands only). Pass `{commit-context}` when the host has Jira IDs or a fixed message format.
2. If the tree is clean but the branch is ahead of the remote: push as part of `git-commit`'s auto flow, or push explicitly if commit was skipped.
3. If already committed and already pushed: continue to §3 without re-committing.

**Idempotency**: never create an empty commit; never re-commit the same tip “for ceremony.”

## 3. Open or update PR/MR

1. Detect the remote host (`gh` / `glab` / equivalent — agent picks native CLI).
2. If an open PR/MR already exists for this head branch: update title/body when the host supplies new `{pr-body-extra}`; ensure the branch is pushed.
3. If none exists: create one against the default / protected base branch.
4. **Minimum body** (always): summary of intent, changed-file overview, verification status (Executed / Pending per `completion-evidence-discipline` honesty when the host has verification notes).
5. Append `{pr-body-extra}` exactly as the host provided (do not drop Jira/OpenSpec fields).

Stop after presenting the PR/MR URL. **Do not merge.**

## 4. Return to host

Hand back: branch name, tip SHA, PR/MR URL (or “skipped — &lt;reason&gt;”). Hosts then load `feature-branch-closeout` for merge / keep / continue (and PR-only if delivery was skipped earlier and the user later chooses open PR — closeout option 1 re-enters this skill).

## Host integration

- **solve-workflow / opsx-solve-workflow**: after verify (and archive for opsx), load this skill, then `feature-branch-closeout`, then retrospective.
- **jira-fix-workflow** stage 9 / **opsx-jira-fix-workflow** post-archive delivery: thin-reference this skill; pass Jira/OpenSpec fields via `{pr-body-extra}` and `{commit-context}`.
- **feature-branch-closeout** option “Open / update PR”: load this skill (idempotent).
- Prefer not copying commit-message or PR-body prose into hosts beyond the field map.

## Forbidden

- Merging the PR/MR from this skill
- Embedding `merge-discipline` Parts A–D
- Requiring a PR on every host run (gate in §1 is mandatory)
- Silent no-op when the user explicitly asked to open a PR and the tree has deliverables
