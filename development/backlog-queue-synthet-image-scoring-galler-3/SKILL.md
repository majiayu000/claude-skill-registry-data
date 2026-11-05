---
name: backlog-queue
description: Cross-repo GitHub Project board is the canonical task queue. Use whenever picking work, claiming an issue, transitioning Stage, or filing/closing a backlog issue across image-scoring-gallery or image-scoring-pipeline.
---

# Backlog queue (compiled claim/stage)

> The canonical task queue is the GitHub Project board:
> **https://github.com/users/synthet/projects/1**
>
> It spans both repos: `synthet/image-scoring-gallery` (this repo) and `synthet/image-scoring-pipeline`.
> The repo `TODO.md` files are pointers only — **never** add tasks there.

## Compiled bootloader (claim / Stage)

Harness lives in the **sibling backend** repo. Do **not** hand-roll Stage IDs.

```powershell
# From gallery repo root (sibling layout):
python ../image-scoring-pipeline/scripts/agent_skills/backlog_stage.py claim <N> --repo gallery
python ../image-scoring-pipeline/scripts/agent_skills/backlog_stage.py set-stage <N> --repo gallery --stage in_progress
python ../image-scoring-pipeline/scripts/agent_skills/backlog_stage.py set-stage <N> --repo gallery --stage blocked --comment "Blocked: …"
python ../image-scoring-pipeline/scripts/agent_skills/backlog_stage.py set-stage <N> --repo gallery --stage review
```

Slash command `/task-claim <N>` uses the same harness with `--repo gallery` default in this repo.

| Owner | Responsibility |
|-------|----------------|
| **Code** | Assign, project item lookup, Stage transitions |
| **LLM** | Pick highest-priority Ready card; Blocked comment prose |
| **Human** | Promote Backlog→Ready; close dead issues |

## When to use

- User asks to pick the next task, start work, or "what's next".
- Filing a new backlog item; PR needs `Closes #N`.
- Blocked / Review / Done Stage transitions.
- Agent would start work without an issue — stop and file one first.

## The five-step contract

1. **Pick** from `Stage = Ready`, sort `priority:p0..p3` (LLM). Do not invent work if Ready is empty.
2. **Claim** via harness / `/task-claim`.
3. **In Progress** on first commit via `set-stage … --stage in_progress`.
4. **Blocked** → `set-stage … --stage blocked --comment "…"` (LLM writes comment).
5. **PR** must include `Closes #<N>`; move to `review` when opening.

## Filing a new task

1. Search both repos for duplicates.
2. Choose owning repo (or both + `cross-repo`).
3. Open issue with label taxonomy; add to Project; default Stage=Backlog.
4. Promote to Ready only with maintainer signoff.

## Label taxonomy

| Family | Values |
|--------|--------|
| `area:*` | `python`, `db`, `gradio`, `electron`, `docs` |
| `priority:*` | `p0`, `p1`, `p2`, `p3` |
| `type:*` | `bug`, `feature`, `refactor`, `test`, `chore`, `epic` |
| (special) | `cross-repo` |
| (status) | `obsolete` — stay open on Backlog |

## Don'ts

- Don't add tasks to `TODO.md`.
- Don't start work without claiming.
- Don't silently abandon Claimed/In Progress — Blocked + comment.
- Don't open a PR without `Closes #N`.

## Related

- Backend harness: [`backlog_stage.py`](https://github.com/synthet/image-scoring-pipeline/blob/main/scripts/agent_skills/backlog_stage.py)
- Contract: [`docs/project/00-backlog-workflow.md`](../../docs/project/00-backlog-workflow.md)
- Backend compilation notes: [SKILL_COMPILATION.md](https://github.com/synthet/image-scoring-pipeline/blob/main/.agent/SKILL_COMPILATION.md)
