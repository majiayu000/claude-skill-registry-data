---
name: sync-template
description: Bring a project generated from Llamitai/wise up to a published SaaS Bootstrap template release. Use when asked to sync, update, or incorporate changes from the base template into an existing generated project. Use Copier for projects with valid answers metadata and a reviewed manual port for GitHub-template copies.
---

# Sync Template

Update one derived project from a **published** `Llamitai/saas-bootstrap-template`
release while preserving its product changes. The canonical `Llamitai/wise` repo
builds that mirror; its unreleased working tree is not an update source.

## Identify the target and base

1. Work from the target project's Git root. Read its `AGENTS.md` and any area
   instructions for files that may change. If invoked in the canonical repo,
   locate the derived project requested by the user first; do not run Copier
   against the canonical repo.
2. Check `git status --porcelain=v1 --untracked-files=all`. Require a clean tree
   before applying an update. Preserve local work; do not stash, reset, clean,
   force overwrite, or make a preparatory commit on the user's behalf.
3. If `.copier-answers.yml` exists, inspect `_src_path` and `_commit`. Continue
   with Copier only when they identify the published
   `Llamitai/saas-bootstrap-template` mirror and a recorded release. Never edit
   this file by hand or replace it with metadata from a new copy. Stop if the
   source is unknown or the recorded release cannot be resolved.
4. Without valid Copier metadata, use the manual route below. Do not run
   `copier recopy` or pretend that a GitHub-template copy supports 3-way updates.

## Copier route

1. Select the latest published stable tag unless the user specified a release.
   Do not use `HEAD`, an unreleased canonical commit, or a prerelease by
   default. Confirm that the target is newer than the recorded `_commit`;
   report "already current" if it is the same. Review release notes or the
   mirror diff to identify affected contracts and migrations. Inspect the
   destination release's `copier.yml` tasks and migrations before trusting it.
2. Run from the derived project's root:

   ```bash
   uvx --from 'copier>=9.6,<10' copier update --defaults --trust --vcs-ref "$template_tag"
   ```

   Set `template_tag` to the verified published tag. The checked `_src_path`
   determines what `--trust` executes. The template's current copy-only tasks
   leave `backend/.env` alone on update, and
   `_skip_if_exists` protects `backend/uv.lock`; verify both after the run.
   If the update command fails, inspect its partial changes and resolve them
   in place; never discard them automatically.
3. Review `git status`, `git diff`, and `git diff --check`. Search changed files
   for `<<<<<<<`, `=======`, `>>>>>>>` and `*.rej`; resolve every Copier conflict
   using the old project behavior, new template behavior, and product-specific
   requirements. Check that `.copier-answers.yml` now records the target tag.
   A successful Copier exit alone does not prove that every intended change
   survived the merge.
4. Regenerate `backend/uv.lock` with `uv lock --directory backend` when backend
   dependencies or package metadata changed. Regenerate other affected locks
   with their package managers. Review new migrations, environment examples,
   HTTP contracts, auth/tenancy boundaries, and deployment changes before
   treating the update as complete. Never overwrite real `.env` files or apply
   migrations to production as part of this skill.

## GitHub-template or clone route

Establish the exact canonical revision or release used to create the project
from its history or other reliable provenance. Compare that base with the
desired published release, then port the relevant changes file by file,
adapting neutral branding and preserving product-specific code. Treat the
result as an ordinary code change: review migrations and contracts, regenerate
affected locks, and check for conflicts and leftover neutral branding. If the
base cannot be established, ask for it before applying a guessed diff. This
route does not create or edit `.copier-answers.yml`.

## Verify and report

Run the target project's checks selected by its `AGENTS.md` and the actual
diff, including migration/API/browser checks when those contracts changed.
Inspect the final diff and working-tree status. Report the source and target
releases, changed files or capabilities, conflicts resolved, commands and
results, and any remaining manual work. Do not commit, push, open a PR,
release, or deploy unless the user requested that separately.
