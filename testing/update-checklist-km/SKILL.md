---
name: hermes-update-checklist
description: >-
  Prepare Hermes for a safe update on this machine using the branch-first local
  customization workflow. Use whenever upstream updates might affect carried local
  behavior, local branches, machine-local helpers, or profile/runtime state.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

# Hermes Update Checklist

This machine no longer treats top-level replay patches as the normal preservation lane for repo code.

## Branch-first rule

Durable repo customizations must be committed on `local/studio-customizations` before update.

Do not call the setup update-safe if important repo work exists only in:
- a dirty worktree
- `git stash`
- a top-level patch file
- an archived patch export
- a backup branch with no active merge path

## Branch roles

- `main` -> clean upstream-tracking branch
- `local/studio-customizations` -> canonical local customization branch
- `backup/pre-*` -> safety snapshots only

## Pre-update flow

Before any large upstream merge on this repo, enable local merge safety aids once:
```bash
git config rerere.enabled true
git config merge.conflictStyle zdiff3
```
`rerere` reuses previously-correct conflict resolutions; `zdiff3` shows the common ancestor in conflicts so local behavior is less likely to be accidentally dropped.

1. Switch to the canonical branch:
```bash
cd ~/.hermes/hermes-agent
git switch local/studio-customizations
```

2. Audit branch state:
```bash
git status --short --branch
git branch -vv
git stash list --date=local
```

3. Classify any current work:
- durable repo work -> commit it now on `local/studio-customizations`
- intentionally temporary work -> stash it deliberately or discard it
- machine-local helper state -> inspect separately under `~/.hermes/patches/`

4. Inspect the narrow replay layer separately:
```bash
find ~/.hermes/patches -maxdepth 1 -type f | sort
```
Keep only legitimate machine-local helpers or explicitly justified emergency stopgaps there.

5. Optional safety snapshot before risky updates:
```bash
git branch backup/pre-update-$(date +%Y%m%d-%H%M%S)
```

6. Update upstream `main` cleanly:
```bash
git fetch origin
git switch main
git reset --hard origin/main
```

7. Move the customization branch forward deliberately:
```bash
git switch local/studio-customizations
git merge main
```

Use merge conflict resolution, not patch archaeology, as the normal integration path.

8. If a stash contains durable repo work, stop and promote that work into `local/studio-customizations` instead of treating stash as canonical.

## Post-update verification

Run all of these before declaring success:
```bash
git status --short --branch
git log --oneline --decorate -5
```

Then verify the actual local behavior you care about still exists from branch history.
Examples on this machine have included:
- Telegram context badge / compact-progress behavior
- gateway `/tts` or `/newthread` support
- local memory/provider behavior
- local TTS/provider wiring

Run focused tests and syntax checks for the touched features, not just a generic smoke test. For Telegram gateway merges, the minimum sentinel is:
```bash
python -m py_compile gateway/platforms/telegram.py gateway/stream_consumer.py gateway/run.py
python -m pytest tests/gateway/test_telegram_context_badge_connect.py tests/gateway/test_stream_consumer.py -q
```
Also verify runtime symbols survived the merge when user-visible affordances depend on local code: `TelegramAdapter.attach_context_badge`, `ctx:`/`compact:` callbacks, `GatewayStreamConsumer.final_message_id`, and post-stream context-badge scheduling in `gateway/run.py`.

## Patch layer policy

`~/.hermes/patches/` is now for:
- machine-local files outside the repo
- archived recovery material
- explicit emergency bridges during migration

It is not the normal answer for preserving repo code.

If a repo feature is still only recoverable from a top-level patch, the migration is not done yet.

## Archive/stash policy

- `git stash` is temporary scratch space only
- archived patch exports are cold-storage reference only
- do not auto-replay archived exports after update
- if old archived work still matters, promote it into `local/studio-customizations`

## Practical go/no-go gate

You are ready to update only when you can state, with evidence:
- which branch is canonical for local repo changes
- that durable repo work is committed there
- that `main` can be refreshed cleanly from `origin/main`
- that remaining patch artifacts are justified machine-local leftovers, not hidden repo truth
- that post-update verification ran and matched the expected behavior
