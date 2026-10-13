---
name: dev-upstream-report
description: "Report bugs and improvement ideas found in Takazudo's own upstream packages as GitHub issues on the upstream repo. The current project depends on packages built by the user under github.com/takazudo and github.com/zudolab (e.g. zudolab/zudo-doc, Takazudo/zudo-front-builder, the @takazudo/* npm scope). Use when: (1) User invokes /dev-upstream-report — with a description to report something now, or with no args to enable upstream-watch mode for the rest of the session, (2) During development a bug, limitation, or missing feature is traced to one of these upstream packages rather than the current project, (3) User says 'report upstream', 'upstream issue', 'file it on the package repo', or blames one of these packages for a problem."
argument-hint: "[what to report — leave empty to enable upstream-watch mode]"
---

# Dev Upstream Report

The user's projects depend on packages the user built themselves, hosted under
**github.com/takazudo** and **github.com/zudolab**. When development work
reveals that a bug or a missing capability lives in one of those packages —
not in the current project — the finding belongs on the upstream repo's issue
tracker; otherwise it is lost the moment this session ends. This skill files
that issue and keeps the local dev work moving.

## Invocation modes

**With arguments** (`/dev-upstream-report the formatter drops MDX comments`):
treat $ARGUMENTS as the finding. Identify the upstream package and repo, file
the issue now, report the URL.

**Without arguments**: enable **upstream-watch mode** for the rest of the
session. Confirm activation in one sentence, then continue whatever dev work
is in progress. From now on, whenever a problem traces to an upstream package
under these accounts, file an issue at the moment of discovery — don't batch
findings for the end of the session, and don't silently work around a problem
without recording it. The mode lasts only for the current session.

In both modes, file both **bugs** and **improvements**: awkward APIs, missing
options, confusing docs, and behavior the current project had to hack around
are all worth an issue — the user owns these packages and wants the feedback.

## Step 1: Confirm the problem is upstream

Before filing, verify the root cause is in the dependency, not in how the
current project uses it. Read the package's actual code under
`node_modules/<pkg>/` or its docs to confirm the behavior belongs to the
package. A misread API is not an upstream bug.

## Step 2: Resolve the package to its repo

1. Read `node_modules/<pkg>/package.json` → `repository` field (or run
   `npm view <pkg> repository.url`).
2. If that fails, look for the repo directly:
   `gh repo list takazudo --limit 100` / `gh repo list zudolab --limit 100`.
3. Only file on repos under these two accounts. If the culprit is a
   third-party package, tell the user instead of filing.

Also capture the **installed version** from the lockfile or
`node_modules/<pkg>/package.json` — the issue is meaningless without it.

## Step 3: Identify the source project and related issues

On invocation, identify the current working project (not the upstream package
repo or the repo storing this skill). In watch mode, repeat this check if the
working project changes. An upstream report should retain the source context
when the following ownership and visibility rules allow it:

```bash
gh repo view --json nameWithOwner,visibility -q '.nameWithOwner + " " + .visibility'
```

- Compare the source repo's owner case-insensitively with `takazudo` and
  `zudolab`. An exact match means **include source context**, regardless of
  whether visibility is `PUBLIC`, `PRIVATE`, or `INTERNAL`. The user authorizes
  naming and linking these repos and their related issues in upstream reports,
  including reports on public upstream repos; no extra confirmation is needed.
- For other owners, `PUBLIC` also means **include source context**.
- For other owners with `PRIVATE` or `INTERNAL` visibility, or when identity
  cannot be verified, **anonymize source context**. Do not infer ownership from
  the upstream package, npm scope, directory name, or logged-in GitHub user.

When including source context, name and link `<src-owner>/<src-repo>` in the
Context block. Include relevant source-project issue URLs from the current
session; if none are known, search the source repo for the finding:

```bash
gh issue list -R <src-owner>/<src-repo> --search "<keywords>" --state all --limit 20
```

Read candidate issues and link only those actually related to the finding,
with a short explanation of the connection. Use full URLs so cross-repo
references are unambiguous. If none are found or accessible, omit the related
issues line; never invent links or create source issues just for attribution.
Link a calling-code permalink
(`https://github.com/<src-owner>/<src-repo>/blob/<sha>/<path>#L<n>`) when it
helps explain the repro. Apply this context policy to duplicate-issue comments
and reopened issues as well as new reports.

## Step 4: Check for duplicates

```bash
gh issue list -R <owner>/<repo> --search "<keywords>" --state all --limit 20
```

If an existing issue already covers it, check its **state and closing reason**
before commenting. A comment on a closed issue is not an active report.

- **Open:** add the new version/repro context there instead of opening a duplicate.
- **Closed as superseded:** follow the replacement issue. If it is open, comment
  there; if it is also closed and the problem still reproduces, reopen the
  issue that best describes the live bug and add the new evidence there.
- **Closed as fixed, not reproducible, or otherwise resolved:** verify the
  finding against the relevant released version. If it still reproduces,
  reopen that issue with the fresh evidence and explain why its prior closure
  no longer reflects the observed behavior. Open a new issue only when the
  new finding is materially different or reopening is unavailable.

After commenting or reopening, query the issue state again. Do not report a
still-closed issue as tracking an unresolved bug; leave an open upstream issue
for a confirmed, unresolved finding and include its URL in the final summary.

## Step 5: File the issue

```bash
gh issue create -R <owner>/<repo> --title "<concise summary>" --body "<body>"
```

`<owner>/<repo>` is the **upstream** repo throughout; the source repo from
Step 3 is written `<src-owner>/<src-repo>`.

- Apply a `bug` or `enhancement` label if the repo has one
  (`gh label list -R <owner>/<repo>`); skip labels that don't exist.
- If a screenshot or diagram is essential to the report, use
  `/gh-issue-with-imgs` instead of plain `gh issue create`.

Issue body shape:

```markdown
## Context

Found while developing
[<src-owner>/<src-repo>](https://github.com/<src-owner>/<src-repo>).
Installed version: `<pkg>@<version>`.
Related source issues: [<src-owner>/<src-repo>#<number>](<full issue URL>) — <connection to this finding>.
<!-- Omit the related source issues line when none were found. -->

## Expected

<what should happen>

## Actual

<what happens instead — include the error message verbatim if there is one>

## Repro

<minimal steps or snippet, reduced to the package's own API,
independent of the current project>

## Suggested fix (optional)

<only if the cause was actually located in the package source>
```

When Step 3 says to anonymize source context, use this Context block instead
— no source repo name, source issue links, or calling-code permalinks:

```markdown
## Context

Found while developing a private project. Installed version: `<pkg>@<version>`.
```

**Privacy**: upstream repos may be public while the current project may be
private or client work. Follow Step 3: verified `takazudo` / `zudolab` source
repos may be named and linked even when private; other private sources stay
anonymous. This permission covers source repo identity, related issue links,
and relevant code permalinks, not secrets or unrelated private content. Reduce
the repro to the package's API surface — no credentials, client names, private
service URLs, business logic, or pasted proprietary code.

### Fallback: when you can't file on the upstream repo

Filing on the upstream repo means opening an issue on a **different** repo than
the working directory. Restricted environments — notably Claude Code on the web
— may not have permission for that.

**On the web/remote container, `gh` does not exist at all** (see
[`web-mode.md`](../../web/web-mode.md) §1), so this step is never "run `gh
issue create -R <upstream>` and catch the auth error" — translate straight to
the GitHub MCP per [`github-ops.md`](../../web/github-ops.md): `gh issue
create` → `issue_write` (action: create). The upstream repo is normally
**out of the session's MCP scope**, so first add it via the platform's
`add_repo` tool (`mcp__Claude_Code_Remote__add_repo` in this container —
`github-ops.md`'s "Repo scope" note: "For cross-repo work, add the target repo
via the platform's `add_repo`"), then file with `issue_write` against it. Only
fall back to the working-repo placeholder below when `add_repo` itself is
denied or unavailable — don't skip straight to the placeholder just because
`gh` is missing.

On a terminal session, if `gh issue create -R <upstream>` fails with an
auth/permission error, file the issue on the **working repo** instead so the
finding still survives the session; never silently drop it.

When falling back:

- Check the working repo (not the upstream repo) for an existing placeholder
  first, so you don't file the same one twice.
- Title it `[upstream: <owner>/<repo>] <concise summary>` so it's easy to spot
  and move later.
- Open the body with a callout naming the real target, then the normal body
  shape above:

```markdown
> **Upstream report** — this is a bug/improvement report for the upstream
> package `<pkg>@<version>`, which lives at `<owner>/<repo>`. Filed here because
> this session can't open issues on that repo. To be refiled upstream in a
> separate session.
```

Tell the user it landed on the working repo as a placeholder and that they'll
move it upstream in another session — don't try to route around the permission
error by other means.

## Step 6: Keep dev moving

Filing the issue is a side quest — return to the main task immediately after.

- If the bug blocks progress, apply a local workaround and mark it with a
  one-line comment linking the issue: `// workaround for <issue URL>` (this
  is exactly the "context that lives outside the codebase" comment exception).
- Never patch files inside `node_modules/` as the fix.
- Include every filed or commented issue URL in the final summary of the
  turn, so the user can review them.
