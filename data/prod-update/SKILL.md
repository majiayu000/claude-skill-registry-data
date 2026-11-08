---
name: prod-update
description: Cut a production release of Token Circles — pre-flight checks (tests, guided-tour walk, migration dress rehearsal), then tag vX.Y.Z and push, then monitor the two prod deploys and verify the result live. Use whenever the user wants to release, ship, tag a version, or push to prod (e.g. "/prod-update", "release 5.9.1", "tag and deploy", "ship it").
---

# /prod-update — tag a release and watch it land

Prod deploys **only** from a `v*` tag. `push main` deploys to dev. Never deploy prod through
`workflow_dispatch`: a non-tag build stamps its version from `git describe --tags`, so it ships
as `5.9.0-3-gabc1234` instead of the release version. `docs/deploy-update-pipeline.md` records a
real incident from exactly that ("label says 5.6.0 but the 5.6.1 fix works").

## 1. Pre-flight

Run these before tagging. Everything here is cheap next to a bad prod deploy.

```sh
git checkout main && git pull --ff-only origin main
git status --porcelain            # must be empty
gh run list --branch main --limit 5   # the head commit must be green
```

- [ ] **Unit + worker tests green in CI** on the exact commit you are about to tag.
- [ ] **Guided tours walk clean.** Run the `tour-check` skill (`pnpm run test:tours`, and
      `MOBILE=1` too). Tours break silently when page layout changes, and nothing in CI
      catches it — this is the one manual gate that has to happen before a tag.
- [ ] **Changelogs updated.** Both of them, and to the rules in "Filling the changelogs"
      below — not to taste. Before tagging, check that `## [Unreleased]` actually accounts for
      every PR merged since the last tag:

      ```sh
      git log --oneline $(git describe --tags --abbrev=0)..HEAD
      ```

      An empty `## [Unreleased]` with ten commits behind it means ten PRs skipped their entry.
      Reconstructing them from commit messages afterwards is guesswork; do it anyway, but the
      fix is to stop it happening in the PR.

- [ ] **Version bumped** if the repo tracks it in `package.json` (the built app takes its
      version from the tag, so this is for tidiness, not correctness).
- [ ] **Migrations rehearsed**, if `worker/migrations/` gained files since the last release:

      ```sh
      git diff --name-only $(git describe --tags --abbrev=0)..HEAD -- worker/migrations/
      ```

      Rehearse against a copy of REAL prod, not a fresh build — a fresh build cannot tell you
      what 20k existing rows will do. Export prod, load it into a throwaway local D1, and run
      the same `migrations apply` the deploy runs. Verified working 2026-08-25 on 0025+0026:

      ```sh
      SP=$(mktemp -d)
      pnpm exec wrangler d1 export finance-manager --remote \
        --config worker/wrangler.jsonc --env prod --output "$SP/prod.sql"
      pnpm exec wrangler d1 execute finance-manager --local --persist-to "$SP/d1" \
        --config worker/wrangler.jsonc --env prod --file "$SP/prod.sql"
      pnpm exec wrangler d1 migrations apply finance-manager --local --persist-to "$SP/d1" \
        --config worker/wrangler.jsonc --env prod
      ```

      Four things that make this a real rehearsal rather than a ritual:

      - **`--persist-to` a throwaway dir.** Without it the dump lands in the repo's `.wrangler`
        state — real customer data inside your dev environment, and your local test data gone.
      - **`--env` is mandatory** on every one of these. The top-level d1 binding in
        `wrangler.jsonc` is `database_id: "local"` and shadows the real DB when it is omitted.
      - **The export carries `d1_migrations`**, which is the whole point: wrangler then applies
        exactly the migrations prod has not, in prod's order.
      - **Count rows before and after.** `ALTER TABLE ADD COLUMN` should not move them; assert
        it rather than assume it. Then run the routes' actual SQL against the migrated copy —
        migrating cleanly and the code still working are two different claims.

      Re-run `migrations apply` afterwards; it must say `No migrations to apply!`, which is what
      makes a re-deploy safe. Then **delete `$SP`** — it is a full copy of production.

      The deploy records a D1 Time Travel restore point before migrating, but a rehearsal is
      what stops you needing it.

## Filling the changelogs

Two files, two audiences. They are not the same document written twice.

- **`CHANGELOG.md` is a product surface, not a document.**
  `frontend/src/components/ChangelogModal.tsx` imports it with `?raw` and renders it in the
  app, so what you write here is literally what a user reads in "What's new".
- **`dev-changelog.md` is the record.** File paths, mechanisms, migrations, why the obvious
  fix was wrong — all of it goes here, and nothing is too detailed for it.

**Write both entries in the PR that makes the change**, under `## [Unreleased]`. The
`chore(release)` commit does one thing to these files: insert the `## [X.Y.Z] — date` heading
directly beneath `## [Unreleased]`, turning whatever accumulated there into that release. It
is not where entries get written.

### CHANGELOG.md — what earns a line

Only what a user would notice and care about: a new feature, something visibly broken now
working, anything touching their money, their data, or their ability to sign in.

**One or two sentences. Lead with the outcome.** No mechanism, no archaeology, no account of
what was wrong under the hood — that is what `dev-changelog.md` is for. A bullet that runs to
four lines is a dev-changelog entry that got lost.

Leave out entirely:

- Visual and layout polish — spacing, alignment, a control that was the wrong colour, text
  that wrapped badly, a dialog whose buttons were reordered.
- Refactors, dead-code removal, dependency bumps, test and CI work.
- Anything a user could not have noticed, or would not think about twice.

Related fixes go in **one** bullet, not five. A patch release is usually three to six lines;
if yours is thirty, most of them do not belong there.

Two mechanical constraints from `parseChangelog()` in `ChangelogModal.tsx`:

- **Top-level `- ` bullets only.** An indented sub-bullet matches no rule and is dropped
  silently — it renders on GitHub and vanishes in the app. Nest in `dev-changelog.md`, never
  here.
- **`## [Unreleased]` is filtered out of the modal**, so entries staged there are invisible in
  the app until the release commit inserts the version heading. That is the intended flow, not
  a reason to write the version heading early.

Length is the thing that goes wrong. Compare — same fix, both real:

> **Too long.** A backup is always the whole account. The full backup exported whichever
> profiles happened to be selected, but restoring one replaces _every_ profile on the account
> — so a backup taken while looking at two of your three profiles quietly deleted the third
> when you restored it. The backup file now always covers everything a restore would replace.
> Per-resource CSV exports are unchanged: those follow your selection, and nothing restores
> from them.

> **Right.** **Backups now cover the whole account.** Restoring replaces every profile, so a
> backup taken while viewing only some of them could delete the rest.

### dev-changelog.md — what goes in

Everything, **including what you kept out of `CHANGELOG.md`**. A UI fix too small for the
user changelog still gets its developer entry; that is where it lives instead, not nowhere.
Name the files, state the mechanism, and record what a future reader would otherwise have to
rediscover.

## 2. Tag and push

```sh
git tag -a v5.9.1 -m "v5.9.1

<short summary of what is in it>"
git push origin refs/tags/v5.9.1
```

Annotated (`-a`), never lightweight. The tag push is what triggers prod.

## 3. Monitor

```sh
gh run list --limit 6            # two runs appear on headBranch v5.9.1
gh run watch <worker-run-id> --exit-status
gh run watch <frontend-run-id> --exit-status
```

**Deploy API Worker** must show these steps in this order:

1. `Typecheck`
2. `Record the D1 restore point before migrations (prod)`: a D1 Time Travel bookmark
3. `Show the restore point in the job summary`: the bookmark a rollback needs
4. `Apply D1 migrations (prod)` — every migration must report ✅
5. `Deploy worker (prod)`

If the restore point was not recorded before the migration step, stop and investigate before
doing anything else.

## 4. Verify live

```sh
curl -s https://tokencircles.com/version.json          # {"version":"5.9.1","gitSha":"<sha>"}
curl -s https://api.tokencircles.com/api/health        # {"ok":true,"env":"production"}
```

The `version` must equal the tag without its `v`, and `gitSha` must be the commit you tagged.
Anything of the shape `5.9.0-3-g…` means a non-tag build reached prod — see the warning at the
top.

## Rollback

The worker and the frontend deploy independently, so roll back whichever broke:

- **Data**: restore prod to the bookmark in the deploy run's job summary, from before its
  migrations:

  ```sh
  pnpm exec wrangler d1 time-travel restore finance-manager --config worker/wrangler.jsonc \
    --env prod --bookmark=<bookmark>
  ```

  It overwrites the database in place. Time Travel reaches back 30 days on Workers Paid (7 on
  Free). Never put a dump of the database in a workflow artifact: the repository is public, and
  any signed-in GitHub account can download its artifacts.

- **Code**: tag the previous good commit as a new patch version and let the pipeline run
  forward. Re-pointing an existing tag is worse — it makes the version stamp lie about which
  code is live.

## Notes

- Tag pushes are not test-gated in `ci.yml` (no `tags: ['v*']` trigger). The pre-flight list
  above is the gate; do not skip it on the assumption CI will catch something.
- Force-pushing an existing tag does **not** reliably re-trigger the deploy workflows. If a tag
  has to move, expect to trigger the deploy another way, and re-check `version.json`.
- A GitHub Release is optional and separate from the tag. The tag alone deploys.
