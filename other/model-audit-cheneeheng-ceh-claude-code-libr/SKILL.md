---
name: model-audit
description: >-
  Audit the ceh-* plugins against Claude's per-model prompting guides and open the results as a
  draft PR. Trigger on "/model-audit", "audit the plugins for the new model". User-invoked only:
  every audit is a billed model call.
argument-hint: "[budget] | [--plugins plugins/standalone/ceh-a ...] [--model M --effort E] [--tune-model M --tune-effort E] [--apply]"
disable-model-invocation: true
user-invocable: true
compatibility: >-
  Needs python 3, git, gh (authenticated), and Claude Code v2.1.283+ for `/doctor prompt-audit`.
  The bundled `/claude-api` skill must stay enabled. Without them audit.py errors out.
license: Apache-2.0
---

# Model audit

Run the audit scripts and hand the results over as one draft PR, so the user reviews that PR and
nothing else. The scripts, their arguments, and their state files are in
`${CLAUDE_SKILL_DIR}/README.md`.

`$ARGUMENTS` passes to `audit.py` unchanged.

## Procedure

1. **Budget only.** When `$ARGUMENTS` is `budget`, run
   `python "${CLAUDE_SKILL_DIR}/scripts/context_budget.py"`, reply with its table and the three
   plugins that cost the most, and stop: no model call, no PR. The table shows what each
   plugin's descriptions and context-injecting hooks add to every session, prompt, and subagent.
2. **Detect.** Check the working tree is clean apart from untracked files, then run
   `python "${CLAUDE_SKILL_DIR}/scripts/detect.py" --write`. It prints JSON. If `stale` is empty
   and `--plugins` was not passed, report "nothing stale" and stop. Otherwise tell the user which
   plugins are stale and how many runs that makes: two per plugin with missing guides (`/doctor`
   plus the filter pass), plus one per pinned file with `"stale": true`.
3. **Audit.** Run `python "${CLAUDE_SKILL_DIR}/scripts/audit.py" $ARGUMENTS` in the background and
   wait for it to exit. Read only `audits/<date>/SUMMARY.md`. A non-zero exit means a plugin
   errored or failed validation: the summary says which. Carry on to the PR anyway, so the failure
   is reviewed with everything else.
4. **Commit.** Stage `${CLAUDE_SKILL_DIR}/assets/known-model-guides.json`, `audits/`, and
   `plugins/`. Commit with `chore(model-audit): audit reports for <date>` plus the attribution
   line. If the pre-commit hook reformats files and aborts, stage them again and commit again.
5. **Open the PR.** Chain with `&&`:
   `git push -u origin HEAD && gh pr create --draft --title "chore(model-audit): audit <date>" --body-file <body>`.
   `<body>` is a scratch copy of `SUMMARY.md` with the PR attribution line appended.
6. **Reply** in the shape under Output.

## Rules

- Do not read the per-plugin reports into this session. They are large, and the user reviews them
  in the PR.
- Do not bump versions or write the changelog. Which edits survive is the user's decision, and the
  summary's reviewer checklist covers both.

## Output

Reply with the PR URL, the summary table, any errors or validation failures, and these next steps,
trimmed to what the run needs: drop step 3 when nothing was tuned, steps 5 and 6 when no edit was
kept.

1. **Review the reports.** Read each `audits/<date>/<plugin>.md` and check that every kept change
   cites a guide that actually backs it. `<plugin>.doctor.md` is the raw `/doctor` output it
   started from.
2. **Keep or drop edits.** With `--apply`, revert the hunks under `plugins/` you reject. Without
   it, apply the ones you keep by hand before merging: `tuning.json` already records the guides as
   checked, so the next run will not propose them again.
3. **Accept or reject pinned tuning.** For each accepted file, set `tuned-for` to its `model` in
   the plugin's `tuning.json`. For a rejected one, revert the edit and leave `tuned-for` alone:
   `proposed-for` stops the same proposal from coming back.
4. **Mirror shared content.** If a kept edit touches a section listed in
   `docs/CROSS_REFERENCES.md`, apply it to every copy in the same PR.
5. **Bump versions.** Each plugin with a kept edit gets a PATCH bump in both its `plugin.json` and
   `.claude-plugin/marketplace.json`, and its `docs/PLUGIN_VERSIONS.md` row. A plugin whose only
   change is `tuning.json` gets none.
6. **Changelog.** Add the PR's entry under the date it was opened, per the root `CLAUDE.md`
   Versioning section, with a `### Plugin versions` table if anything was bumped.
7. **Handle failures.** For an errored plugin or a failed validation, fix the cause, then re-run
   `/model-audit --plugins <plugin-path>`. A report that looks weak can be re-run with
   `--model opus`.
8. **Verify and merge.** Run `python tools/validate-plugins/validate.py`, optionally
   `claude plugin eval` from a plugin root, tick the PR checklist, mark it ready, and merge with a
   merge commit per the root `CLAUDE.md` "Landing a branch".

## Stop conditions

- Working tree has tracked changes → stop and say so. Do not stash or discard them.
- `gh` is not authenticated or the push fails → report the failure and leave the commit in place.
