---
name: skill-proposer
description: >
  Use when the user asks to turn wiki patterns into a concrete SKILL.md change,
  propose one atomic skill patch, or record Accept/Reject in the skill-impact
  ledger. Triggers on "propose a skill fix", "patch this skill from the wiki",
  "skill-proposer", or "gate a skill change".
---

# Skill Proposer

Read the **host-global** skill-evolution wiki and propose **one** atomic skill
change. Works on Windows, macOS, and Linux. Meta workflow only — do not inject
wiki files into a normal task agent.

## Prerequisites

- Prefer the bundled **Wiki Maintainer** assistant (history + workspace for wiki CLI).
- On scheduled/autonomous wakes: **Propose** only — never Accept a skill patch
  without an explicit interactive user Accept (see wiki-maintainer
  `references/autonomous-loop.md`).
- Shell/Python to run **wiki-maintainer**’s CLI (shared wiki IO).
- Wiki root: `Path.home() / ".libragent" / "wiki"` (Linux/macOS `~/.libragent/wiki`, Windows `%USERPROFILE%\.libragent\wiki`).
- Resolve **wiki-maintainer** Base Directory as `<wiki-maintainer-dir>` (system skill install of `wiki-maintainer`).
- Editable target skill under a **runtime** skill root (user / assistant / workspace). Read [proposal-checklist.md](references/proposal-checklist.md).

```bash
python "<wiki-maintainer-dir>/scripts/wiki_cli.py" init
python "<wiki-maintainer-dir>/scripts/wiki_cli.py" path
```

## Not this skill

| Need | Use |
| --- | --- |
| Mine sessions → patterns | **wiki-maintainer** |
| Knowledge graph facts | **knowledge-distiller** |
| Brand-new skill with no wiki | Manual authoring / skill-creator guidance |

## Workflow

### 1. Read prior art

```bash
python "<wiki-maintainer-dir>/scripts/wiki_cli.py" cat index.md
python "<wiki-maintainer-dir>/scripts/wiki_cli.py" list-patterns
python "<wiki-maintainer-dir>/scripts/wiki_cli.py" cat patterns/<id>.md
python "<wiki-maintainer-dir>/scripts/wiki_cli.py" cat skill-impact.md
```

Skip proposals that already **Reject**ed the same change without new evidence. One pattern id per proposal.

### 2. Choose the owning skill

1. Map pattern direction to one skill name.
2. Edit a writable runtime skill root. If only a read-only system copy exists, propose overlay text for user/assistant skills — do not invent fake paths.

### 3. Draft one atomic change

1. Change one skill’s `SKILL.md` (or one reference file) only.
2. Keep frontmatter `name` + trigger-bearing `description`.
3. One-sentence **user-facing mechanism**.
4. Forbidden: evaluation answers, grader hints, checkout-only paths, machine-locked absolute paths in guidance (home-relative wiki paths via `wiki_cli path` are OK).

### 4. Validate

1. Check relative `references/` links inside the edited skill.
2. Self-check [proposal-checklist.md](references/proposal-checklist.md).
3. Prefer a short user-like smoke of the same failure class.

### 5. Ledger

```bash
python "<wiki-maintainer-dir>/scripts/wiki_cli.py" append-impact \
  --skill "<name>" \
  --summary "<what changed>" \
  --mechanism "<user-facing mechanism>" \
  --validation "<what you ran or Pending>" \
  --decision Pending|Accept|Reject \
  --notes "<optional>"
```

On **Reject**, restore the skill content. **Never** delete wiki pattern or ledger rows.

### 6. Hand-off

Summarize: pattern id, skill, mechanism, decision, remaining Pending work.

## Safety

- One proposal at a time; new evidence before retrying Reject.
- Wiki is global per OS user account; skills stay in skill roots.
