---
name: ci-publish
description: Send main to the Chrome Web Store and Firefox Add-ons, by tagging it `store-<version>`.
disable-model-invocation: true
allowed-tools: Bash(git *), Bash(gh *), Bash(node scripts/version.ts *)
---

A `store-<version>` tag on `origin/main`'s last commit runs the Release
workflow in its store mode: the CI, then the version's GitHub release, the
store zip sent to the Chrome Web Store and the Firefox zip, with its
sources, to Firefox Add-ons. Each
store reviews it before it goes live. A version still in review on the
Chrome Web Store is cancelled, and the new one takes its place. Arguments:
`$ARGUMENTS`; refuse any.

Pass `gh` the `origin` repository (`--repo <owner>/<repo>`, from `git remote
get-url origin`): the checkout has more than one remote.

1. It runs on what GitHub has, not the local checkout: `git fetch origin
   --tags`, then compare `origin/main` with the local `main`. If local work
   isn't on `origin/main` yet, say so and stop: don't push for the user.
2. `v=$(node scripts/version.ts --ref origin/main)`: the version it gets.
3. Check the secrets: `gh secret list` must show `CWS_SERVICE_ACCOUNT`,
   `CWS_PUBLISHER_ID`, `AMO_JWT_ISSUER` and `AMO_JWT_SECRET`. If one is
   missing, name it and stop: that store's job would fail.
4. If `store-$v` exists on `origin` already, that commit was sent: say so
   and stop.
5. Tag and push: `git tag "store-$v" origin/main && git push origin
   "store-$v"`. Then find the run it made (`gh run list --workflow
   release.yml --event push --limit 1 --json databaseId,url,headBranch`,
   retrying briefly until its `headBranch` is the tag) and give its URL.
6. Follow the run to its end: `gh run watch <id> --exit-status` in the
   background (it takes several minutes, the end-to-end tests most of it),
   then give each job's outcome (`gh run view <id> --json jobs`). If the
   CI fails, nothing was sent: name the failing tests (`gh run view <id>
   --log-failed`) and what they say, then delete the tag (`git push origin
   :store-$v`, `git tag -d store-$v`): it would say this version was sent. If
   `release`, `store` or `amo` fails, give its error line: none holds the
   others up. If the release passed, give its URL (`gh release view
   "v$v" --json url`). If both stores passed, say each has the version in
   review and, from the `store` job's `Cancelled the review` line, which
   version it replaced, if any.
