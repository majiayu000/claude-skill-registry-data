---
name: gw-update
description: Bring a project's copy of Galivelop-workflow up to the workflow repo's current version, showing the template changes before applying what the user confirms. Use after the workflow publishes a new version (run by hand with /gw-update).
disable-model-invocation: true
license: MIT
compatibility: Claude Code or any Agent Skills agent; git and python3 3.8+; the Galivelop-workflow repo cloned or added to the session
metadata:
  version: "0.4.3"
  source: "Galivelop workshop"
---

# gw-update

If `.claude/gw/gw-update.md` exists in the project, read it first: it holds what is specific to the project.

Updates what the workflow owns (scripts, skills, git hooks, settings entries, CI) and reports changes in what the
project fills in (log, `REVIEW.md`, `GLOSSARY.md`, notes). The mechanical part is `aplicar.py`; this skill adds the
judgement: what changed, what the user wants, what to merge by hand. Reply in the project's `language`.

## 1. Compare versions

`<workflow>` is the clone of `Galivelop-workflow` (a sibling `../Galivelop-workflow`, or attached to the session;
else ask the user). Read it, never edit it. Fetch it first: `git -C <workflow> pull --ff-only`.

- Project version: `version` in `.claude/gw.json`.
- Copied headers: `# galivelop-workflow vX.Y.Z` in `.claude/gw/scripts/*` and `.githooks/*`.
- Workflow version: `version` in `<workflow>/.claude-plugin/plugin.json`, and its entries in `CHANGELOG.md`.

Done when you can say "project at X, workflow at Y". Equal and no `.gw-nuevo` pending: say so and stop. Project
newer than the workflow: stop and tell the user to update the workflow clone.

## 2. Dry run

```bash
git -C <project> status --short            # a clean tree makes the update easy to review and undo
python3 <workflow>/scripts/aplicar.py <project> --dry-run
```

It lists what it would create, update or propose, files the workflow no longer has, and template updates, plus the
user's personal notes (`~/.claude/gw/notas/`, see `docs/en/config.md`) it would create (`personal note`) or that differ
from the project's copy. Summarise it for the user with the CHANGELOG entries between X and Y (`### ES` or `### EN` per the user's language).

## 3. Show the template diff for filled files

Log, `REVIEW.md`, `GLOSSARY.md` and the `.claude/gw/*.md` notes are never overwritten, because the project filled
them in. Show what the **template** changed, not what differs from the project's file:

```bash
old="$(mktemp -d)"                                                              # a throwaway folder
git -C <workflow> show v<X>:templates/<language>/<file> > "$old/<file>"      # the template at the old version
git diff --no-index "$old/<file>" <workflow>/templates/<language>/<file>     # old template vs new template
```

If there is no tag `v<X>`, take the commit where `plugin.json` said X: `git -C <workflow> log -S'"version": "<X>"'
--oneline -- .claude-plugin/plugin.json`. Placeholders (`{{key}}`) stay unrendered on both sides, so the diff
shows only the template's own change. Offer each hunk to the user; apply the ones accepted to the project's file by
hand.

## 4. Apply what the user confirms

1. Workflow-owned files with no local edits update in place:
   `python3 <workflow>/scripts/aplicar.py <project> --update`. Use `--update` only after the user confirms, because
   it also replaces local edits in workflow-owned files. Auto mode may ask permission to edit `.claude/settings.json`
   and `.githooks/`; tell the user first.
2. A `<file>.gw-nuevo` is a proposal: merge it by hand with the user, then delete it. `AGENTS.md` and `CLAUDE.md`
   merge block by block, keeping the project's rules and the `galivelop-workflow` marker line.
3. Files the workflow no longer has are reported, never deleted: ask before `git rm`.
4. Personal notes: the missing ones are created by the run above. For each `personal note … differs` line, show the
   user `diff <source> <target>` (the project's copy is never overwritten and gets no `.gw-nuevo`) and merge by hand
   only what they accept. Nothing personal ever goes into the workflow repo; `--sin-notas-personales` skips them.
5. Set `version` in `.claude/gw.json` to Y once the proposals are reviewed.

## 5. Check and commit

1. `python3 <project>/.claude/gw/scripts/doctor.py` until no `FAIL`; `python3 <workflow>/scripts/aplicar.py --check
   <project>` exits 0 when nothing is left to merge.
2. Commit with the message `aplicar.py` suggested and a real `Next:` line (`Siguiente:` in Spanish projects), update
   the log in the same commit, and `git push`; the pre-push runs the check.

Done when doctor is green, no `*.gw-nuevo` is left and `version` equals Y.
