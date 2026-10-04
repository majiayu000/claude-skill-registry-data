---
name: insolvia-branch-protection
description: >-
  How to add or remove a required status check on `main` yourself, instead of
  asking a human to click through repo settings. Use this whenever a task means
  changing the `protect-main` ruleset — "make the Marketing site check
  required", "add a PR check to the ruleset", "gate merges on the API service
  job" — or diagnosing a PR stuck on "Expected — waiting for status to be
  reported". Trigger it the moment you rename a job `name:` or a matrix leg in
  any `*-pr.yml`, because the ruleset matches checks by exact name and a rename
  silently orphans the gate. Read it BEFORE hand-rolling
  `gh api --method PUT .../rulesets/<id>`: that call REPLACES the arrays you
  send, so a partial payload deletes every other rule on `main`. There is no
  `gh ruleset edit` — don't go looking for one.
---

# Changing `main`'s required checks (Insolvia)

**This does not need a human.** Don't ask the user to open repo settings.

```bash
scripts/update-ruleset.sh show
scripts/update-ruleset.sh add "Marketing site"
scripts/update-ruleset.sh remove "Marketing site"
```

It shows a before/after diff and asks before writing. Rollback:
`gh api /repos/insolvia-ai/insolvia/rulesets/<id>/history`.

## Getting the check name right

The name is the job's `name:` in the workflow, matched **character for
character** — matrix legs get a `(leg)` suffix. The list of valid names and
which workflow reports each lives in
[`docs/reference/architecture.md`](../../../docs/reference/architecture.md) § "Required status
checks".

A typo doesn't error. GitHub accepts a required check nobody reports, and every
PR then parks on *"Expected — waiting for status to be reported"* forever.
Copy the name from the workflow file; don't type it from memory.

## Why the script exists rather than a `gh api` one-liner

- **`PUT /repos/{owner}/{repo}/rulesets/{id}` replaces the arrays it receives.**
  It takes `name`, `target`, `enforcement`, `bypass_actors`, `conditions`,
  `rules` — all optional — and whatever array you send wholly replaces its live
  counterpart. Send `rules` containing just your new check and `deletion`,
  `non_fast_forward` and `required_linear_history` are gone from `main`. The
  REST docs don't mention this. Hence read-modify-write, always.
- **A live `GET` is not a valid `PUT` body** — it also returns `id`, `node_id`,
  `source`, `created_at`, `_links`, `current_user_can_bypass`. Project to the
  six fields above.
- **Ids rot.** The script resolves by name. `protect-main` was recreated at some
  point, which is why `18947945` shows up in older notes and 404s today.

## Gotchas

- **`gh ruleset` is read-only** — `check`, `list`, `view`, nothing else (gh
  2.96). Mutations go through `gh api`.
- **`bypass_actors` is only returned to a caller with write access.** Without
  admin it reads as empty, and writing that back would silently drop every
  bypass. Check `gh auth status` first.
- **`enforcement: evaluate`** reports what *would* have been blocked without
  blocking — a way to land a new required check without stopping merges on day
  one. `disabled` turns the ruleset off entirely.
- **This isn't a deploy.** `insolvia-deploy`'s "deploys run in CI, never from
  your CLI" rule doesn't apply — this runs from your machine against the GitHub
  API, as a repo admin.
