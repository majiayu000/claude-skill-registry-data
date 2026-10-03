---
name: project-surface-auditor
description: Audit this repo's project ownership before changing README, AGENTS.md, skills, data, reports, scripts, or status docs. Use when the user asks what projects exist, says the repo invented projects, wants cleanup, wants deleted/obsolete surfaces found, or needs a tracked inventory of real, hidden, duplicate, obsolete, placeholder, and generated file series.
---

# Project Surface Auditor

Use this skill before answering "what projects are here" or before changing
workspace project lists. Do not trust old lane tables by themselves. Classify
the actual file series first.

## Source Of Truth Order

1. User's current correction in the conversation.
2. `data/project-surface-inventory.json`, if present.
3. Current filesystem and `git status --short`.
4. Current `skills/*/SKILL.md` surfaces.
5. README, AGENTS.md, decisions, and status docs.

If these disagree, report the disagreement. Do not silently normalize stale docs.

## Audit Commands

Run these from the repo root:

```bash
git status --short
git ls-files | sort
git ls-files --others --exclude-standard | sort
find skills data docs reports scripts -maxdepth 4 -type f | sort
npm run validate
```

Use `rg` for targeted checks:

```bash
rg -n "foundation|untitled-project|address-disaster|metro-manila-source-atlas|agent-workflow|workflow catalog|agentic-repos|Active Lanes|Project Lanes" README.md AGENTS.md docs reports data scripts skills
```

## Classification Rules

Classify every major file series:

- `active_current`: a real current project with a skill and owned data/scripts.
- `active_hidden_needs_promotion`: real work on disk that lacks a proper skill,
  README entry, or project contract.
- `predecessor_or_duplicate`: older version or maintainer copy of a current
  project; not counted as a separate current project unless the user confirms.
- `obsolete_deleted_candidate`: stale tracked project surface the user says is
  deleted or no longer wanted.
- `placeholder_delete_candidate`: placeholder scaffolding not tied to a real
  repeated job.
- `generated_run_artifact`: batch outputs, prompts, logs, or generated indexes.
- `shared_or_legacy`: old source material that may be useful but is not a
  project.

Never call something a project just because it has a `skills/` folder. A
project needs a repeated job, an input contract, an output artifact, and a
current user-backed reason to exist.

## Output

Write or update:

- `data/project-surface-inventory.json` for machine-readable ownership.
- `docs/status/YYYY-MM-DD-project-surface-audit.md` for human-readable findings.

The audit report must include:

1. intended current projects and confidence;
2. hidden project surfaces;
3. stale or made-up project surfaces;
4. duplicate/predecessor surfaces;
5. generated artifacts that should not become projects;
6. cleanup batches, without deleting files unless explicitly approved.

## Cleanup Guard

Do not delete tracked files in the audit pass. Produce a cleanup plan first.

Before deleting or moving any surface, require one explicit user confirmation of
the cleanup batch. Keep batch names concrete, such as:

- remove deleted disaster-risk assessor;
- remove placeholder untitled project;
- promote agent workflow project maker;
- archive V1 building-code predecessor;
- rewrite README and AGENTS project index.
