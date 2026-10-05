---
name: factory-release
description: Cut a new release — bump package.json + VERSION in lockstep, commit, tag with a per-version breakdown since the last published baseline, push, publish a GitHub Release, and publish to npm. Five approval gates; the user edits release notes in their preferred editor.
argument-hint: patch | minor | major (optional — asks if omitted)
---

You're cutting a new release. The user owns the final word at every gate and edits the release notes directly in their preferred editor.

A release is one atomic fact — package.json version, the `VERSION` file, the git tag, the GitHub Release, and the npm publish all name the same thing. This command's job is to advance them together. Letting any one of them move without the others is the drift this command exists to prevent.

**Invocation input:** `patch`, `minor`, or `major`. If empty, ask through the host's user-interaction capability or directly in chat.

## What to do

1. **Pre-flight.** Run in parallel:
   - `git status --porcelain` — must be clean. If dirty, list the files and ask whether to abort or stash.
   - `git rev-parse --abbrev-ref HEAD` — confirm we're on the default branch (typically `main`). If not, warn and ask before proceeding.
   - Establish the **current version** from up to three sources, and detect drift between them:
     - `package.json` `version` (if a `package.json` exists) — the source npm publishes from.
     - `VERSION` file at repo root (if present).
     - Latest git tag: `git describe --tags --abbrev=0` (strip leading `v`).

     If these disagree, **surface all of them explicitly** and treat the highest (by semver) as the current base. Drift is exactly what this command exists to close — name it, don't silently pick one. If none exist, treat current as `0.0.0`.

2. **Compute the new version** from the reconciled base:
   - `patch`: `X.Y.Z → X.Y.(Z+1)`
   - `minor`: `X.Y.Z → X.(Y+1).0`
   - `major`: `X.Y.Z → (X+1).0.0`

3. **Check for tag collision.** `git rev-parse v<new-version> 2>/dev/null` — if it resolves, fail with a clear message and stop. Don't overwrite an existing tag.

4. **Establish the baseline and enumerate the version spans.** The breakdown starts from the last *published* point, not merely the last tag — so versions that were tagged but never shipped still get a changelog entry.
   - **Baseline:**
     - If this is an npm package (`package.json` with a `name`, not `private`): `npm view <name> version` → the last version on npm. The baseline ref is its tag `v<published>` if that tag exists; if the tag is missing, fall back to `git describe --tags --abbrev=0` and note the mismatch.
     - Otherwise: baseline = previous tag `git describe --tags --abbrev=0`. If no tags exist at all, baseline = the initial commit.
   - **Enumerate every version boundary from the baseline to HEAD.** List tags with `git tag --list 'v*' --sort=v:refname`, keep those strictly greater than the baseline, and append the new version (`v<new-version>`, spanning the last existing tag → HEAD). This yields an ordered list of spans: `(baseline → v_a), (v_a → v_b), …, (v_last → HEAD as v<new-version>)`. In the normal no-drift case the baseline IS the last tag, so there's exactly one span and the per-version breakdown collapses to a single block automatically.
   - **For each span, gather deterministically (straight from git, no interpretation):**
     - Commits: `git log <from>..<to> --pretty=format:"%h %s"`, grouped by Conventional Commits type (`feat`, `fix`, `refactor`, `chore`, `docs`, `test`; anything non-conforming → `**other:**` with a flag for the user to rewrite).
     - Diffstat: `git diff --shortstat <from>..<to>` → "N files changed, +X / −Y".
     - Surface map: `git diff --name-status <from>..<to>`, group changed paths by top-level directory and mark added (`+`), modified (`~`), deleted (`−`), renamed (`→`). For this kit, `skills/`, `agents/`, `commands/`, and `bin/` ARE the public API surface (see the README's Versioning section), so this line is the at-a-glance "what moved in the surface."
   - Identify the dominant theme across the whole span (largest user-facing group, `feat` > `fix` > `refactor` > `chore`) for the top-level Outcome line.
   - Extract any Linear IDs (`<TEAM>-<NUM>`) across all spans for the Refs line.

5. **Write the draft to a file the user can actually edit.** Use the host's filesystem-write capability to create `/tmp/factory-kit-release-notes-v<new-version>.md`. Auto-fill everything you can; leave clear `REFINE` markers where judgment is needed. Order version blocks newest-first — this release at the top, older catch-up versions beneath. Shape:

   ```markdown
   **Outcome:** v<new-version> — <one-line summary of the dominant change across the span — REFINE>

   **Why:** <best guess from the dominant type — REFINE THIS>

   <!-- Catch-up line: include ONLY when unpublished versions exist between the baseline and the previous tag -->
   **Catch-up:** npm last shipped v<baseline>; this release also folds in v<a>…v<last> that were tagged but never published. Per-version breakdown below.

   ## Changes by version

   ### v<new-version> — this release
   _<N files changed, +X / −Y>_

   **feat:**
   - <subjects>

   **fix:**
   - <subjects>

   <omit any empty group>

   **Surface:** Skills ~factory-api.md +factory-x.md · Commands ~release.md · Bin +factory-kit-check.js
   <!-- omit the Surface line for a span if nothing under skills/ agents/ commands/ bin/ changed -->

   ### v<last-existing-tag>
   _<diffstat>_

   **feat:**
   - …

   **Surface:** …

   <!-- …one block per span, down to v<baseline+1>… -->

   **Refs:** <aggregated Linear IDs across all spans — omit line if none>
   ```

6. **Open it in the user's editor.** Use the host's safe application-launch capability with `$EDITOR` when available. If the host cannot launch applications, tell the user the path and ask them to open it manually.

7. **Gate 1 — wait for the user.** Print:
   > Draft is ready at `/tmp/factory-kit-release-notes-v<new-version>.md`. Edit anything you want — `Why`, `Outcome`, the bullets, all of it. Save the file and reply `done` (or `cancel` to abort).

   Wait for the user's reply. On `cancel`, delete the temp file and stop.

8. **Read back what they saved.** Use the host's filesystem-read capability on the temp file. Print a brief diff summary (or just the final content if the diff would be longer than the file). Extract the **Outcome** line's summary fragment (the text after `— `) to use as the commit subject. Ask one final confirmation:
   > Final notes shown above. Confirm to write the version bump + commit + tag, or reply with another round of edits and I'll wait again.

9. **Gate 2 — write.** On confirmation, bump every version source that exists, in lockstep:
   - **package.json** (if it exists and `private` is not `true`): `npm version <new-version> --no-git-tag-version --allow-same-version`. This rewrites `package.json` (and `package-lock.json` if present) without making its own commit or tag — this command owns the commit. If the repo has no `package.json`, skip this and note it.
   - **VERSION** file (only if it existed before): write the new version to it.
   - `git add` everything that changed: `package.json`, `package-lock.json`, `VERSION` (whichever apply).
   - `git commit -m "release: v<new-version> — <outcome-summary>"` — the summary comes from the **Outcome** line in the notes. Keep the full header ≤ 72 chars (truncate the summary if needed; full text is in the tag annotation).
   - `git tag -a v<new-version> -F /tmp/factory-kit-release-notes-v<new-version>.md` — pass the file directly so multi-line formatting (the full per-version breakdown) is preserved in the annotation.

10. **Gate 3 — push?** Show local state (`git log -1 --oneline`, `git tag --list 'v*' | tail -3`) and ask explicitly whether to push. Don't pre-authorize. On yes:
    - `git push origin HEAD`
    - `git push origin v<new-version>`

11. **Gate 4 — publish GitHub Release?** Only runs if Gate 3 was approved (no tag on origin means nothing to release against). Pre-checks:
    - `git remote get-url origin | grep -q github.com` — if origin isn't GitHub, **skip this gate entirely** (don't ask).
    - `command -v gh` — if `gh` isn't on PATH, print the manual one-liner and the Releases URL, then skip. Don't fail the run.

    Otherwise ask explicitly:
    > Publish a GitHub Release for v<new-version>? Notes come from the tag annotation. (y/n)

    On yes, run:
    ```
    gh release create v<new-version> \
      --title "v<new-version> — <outcome-summary>" \
      --notes-file <(git tag -l v<new-version> --format='%(contents)')
    ```
    `<outcome-summary>` is the same fragment used for the commit subject (step 8). The annotation carries the full per-version breakdown, so the Release page shows the catch-up changelog. Print the returned Release URL.

    Rationale: tag and GitHub Release should be 1:1. Tags are the source of truth for "what shipped"; the Release page is the discoverable changelog and the feed that Renovate/Dependabot watch. Skipping it for patches creates "did this ship?" gaps on the Releases page.

12. **Gate 5 — publish to npm?** Only runs if Gate 3 (push) was approved — publishing a version that isn't on origin recreates the drift this command exists to prevent. Pre-checks (skip the gate, don't fail the run, when one isn't satisfied):
    - `package.json` exists, has a `name`, and `private` is not `true` — if not, this isn't a publishable npm package; **skip entirely** (don't ask).
    - `npm whoami` — if it errors (not logged in), print: `Not logged in to npm. Run` `npm login` `, then` `npm publish` `from <repo-dir> to ship v<new-version>.` and skip.
    - `npm view <name>@<new-version> version` — if it returns the version, it's already on npm; print that and skip.
    - Show exactly what will ship: run `npm publish --dry-run` and surface the tarball file list and the version line.

    Otherwise ask explicitly:
    > Publish v<new-version> to npm? Tarball shown above. (y/n)

    On yes:
    - Run `npm publish`. The package's `publishConfig.access` governs scope visibility, and any `prepublishOnly` script builds artifacts first — don't add flags it doesn't need.
    - If npm reports a one-time password is required (2FA), ask the user for their OTP code and re-run `npm publish --otp=<code>`. Never ask them to disable 2FA.
    - On success, print the published version and the URL: `https://www.npmjs.com/package/<name>/v/<new-version>`.

    Rationale: npm is the distribution surface. If the git tag advances but npm doesn't, the package your users `npx` is older than the tag claims — the exact gap this command now closes.

13. **Clean up and confirm.** Delete `/tmp/factory-kit-release-notes-v<new-version>.md`. Print:
    > Released v<new-version>. package.json + VERSION bumped, tag pushed *(if approved)*, GitHub Release published *(if approved)*, npm publish done *(if approved/applicable)*. Run `git show v<new-version>` to verify the annotation.

## Style

Follow `factory-voice.md`. Five explicit gates — notes (edited by the user), write (version bump + commit + tag), push, GitHub Release, npm publish — none batched, none skipped silently. Gates 4 and 5 auto-skip when the environment can't satisfy them (origin isn't GitHub, `gh`/`npm` missing, not logged in, no `package.json`, already published); they never ask a question the environment can't answer, and they never fail the whole run for a missing optional step — they print the manual fallback and move on.

The version bump in Gate 2 always moves package.json and VERSION together; that lockstep is the anti-drift guarantee. The notes are a **per-version breakdown from the last published baseline** — every tagged-but-unpublished version gets its own block (commits, diffstat, surface map), so a catch-up publish documents each step instead of collapsing it into one jump; with no drift it's a single block. All of it is deterministic from git — the auto-grouped commit list and diffstat/surface map ARE the changelog; don't editorialize them. Architect judgment goes on the Outcome and Why lines, which the user will rewrite in their editor. If a commit was pushed with `--no-verify` and doesn't fit the conventional format, surface it under `**other:**` so the user can decide how to characterize it.

## Related

- `factory-commits.md` — the Conventional Commits format this command parses
- `factory-voice.md` — the shape used for release notes
