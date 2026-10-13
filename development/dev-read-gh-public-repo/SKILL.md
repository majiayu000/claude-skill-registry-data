---
name: dev-read-gh-public-repo
description: "Read files from a PUBLIC GitHub repo that the Claude Code web/remote environment reports as out-of-scope for its GitHub MCP tools. Use when (1) running in the web/remote container (claude.ai/code, NOT a local Mac/terminal session), AND (2) a `mcp__github__*` call fails with \"Access denied: repository ... is not configured for this session\", AND (3) the repo is public. Triggers: \"can't see that repo\", \"access denied repository not configured\", \"read a public repo that's not in scope\", \"clone a public repo to read it\"."
---

# Read a public GitHub repo that's out of MCP scope

## The problem

In the Claude Code **web/remote** environment, the GitHub MCP tools (`mcp__github__*`)
are locked to an allow-list of repos chosen when the session was created. Reading any
other repo — even a public one — fails like this:

```
Access denied: repository "owner/name" is not configured for this session.
Allowed repositories: <only-the-scoped-ones>
```

## The fix — try in this order

### 1. Add the repo to session scope (primary path)

Call the platform's `add_repo` tool (`mcp__Claude_Code_Remote__add_repo` in this
container) with the owner/repo — this is the supported way to widen scope
mid-session (see [`github-ops.md`](../../web/github-ops.md), "Repo scope": "For
cross-repo work, add the target repo via the platform's `add_repo`"). On success it
returns a clone command; run it, then call `register_repo_root` so the harness picks
up the new repo. After that, the normal `mcp__github__*` tools / Read / Grep work
against it like any in-scope repo — full read access (issues, PRs, file contents),
not just a one-off file dump.

If `add_repo` is unavailable in this session, or the call is denied
(authorization/policy error, GitHub App not installed for the repo), fall through
to step 2.

### 2. Codeload tarball fetch (fallback)

Fetch a tarball over plain HTTPS instead of using `git` — the same bootstrap
pattern `dev-setup-webenv` uses to pull `claude-resources` into a web session:

```bash
cd /tmp && curl -fsSL "https://github.com/<owner>/<repo>/archive/refs/heads/<branch>.tar.gz" -o repo.tar.gz \
  && mkdir -p <repo> && tar -xzf repo.tar.gz -C <repo> --strip-components=1
# now Read / Grep files under /tmp/<repo>
```

Try the actual default branch first (commonly `main`, then `master` if that 404s).

### 3. Plain `git clone` — verify before relying on it

```bash
cd /tmp && git clone --depth 1 https://github.com/<owner>/<repo>.git
```

Whether this works depends on how this session's git proxy is scoped, and that has
been observed to vary: some container configurations reject `git clone`/`git
ls-remote` of an out-of-scope repo with a 403 (the assumption documented in
`dev-setup-webenv`), while a plain `git clone` of a public, out-of-scope repo has
also been observed to succeed outright in-container. Don't assume either outcome —
check first with `git ls-remote --exit-code https://github.com/<owner>/<repo> HEAD`
(expect a commit hash, not an error) before depending on it. Steps 1–2 above don't
depend on this uncertain behavior, so prefer them.

## Gotchas

- **HTTPS only — SSH fails.** There is no `ssh` binary in the container, so

  `git clone git@github.com:owner/repo.git` dies with `ssh: not found`. Always use
  the `https://github.com/...` URL (or the codeload tarball URL).

- **No auth needed for public repos** over HTTPS — the fetch just works, assuming

  the environment's outbound network policy allows `github.com` /
  `codeload.github.com`.

- **Clone/extract outside the working repo** (`/tmp`, or any path that isn't the

  user's project) so the checkout stays ephemeral and never gets committed by
  accident.

- `--depth 1` (or the tarball, which has no history at all) keeps it fast; only

  fetch full history if you actually need it.

## Limits — don't misapply

- **Reading only.** This is for research: reading a doc/spec, copying a pattern. It

  grants no write access and is not a substitute for proper repo scope.

- **Public repos only.** Private repos still require adding the repo to the session

  scope via `add_repo` (or real auth) — a plain HTTPS clone/tarball fetch will 404
  or prompt for credentials and fail.

- **Web/remote env only.** On a normal local session, just use `gh` or an existing

  checkout instead — don't reach for this.
