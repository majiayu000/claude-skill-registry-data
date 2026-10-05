---
name: git-identity-guard
description: Install a $PATH-level git wrapper that hard-blocks any commit or push whose author/committer identity doesn't match one configured name/email, everywhere on the machine, with no override. Use when commits keep landing under the wrong email (breaking CLA bots, GitHub's "Verified" badge, or account-linked contribution credit), when a project's own docs say "always commit as X" but agents keep overriding it anyway, or when setting up a fresh machine/session for an external-contribution campaign.
---

# Git Identity Guard

Installs a `git` shim ahead of the real binary in `$PATH` that inspects every
`commit`, `commit-tree`, and `push` invocation and refuses to let one through
under the wrong author/committer identity - regardless of what tries to set
one.

## The problem this solves

A documented rule ("always commit as `you <you@example.com>`") is not
self-enforcing. On a real campaign, this showed up as:

- The correct identity was already the git **global default**.
- Every commit still explicitly overrode it with `-c user.email=...`, using
  a *different* email available in context for an unrelated reason (a
  subscription/session address, not the account's own email) - because
  nothing stopped that override from winning.
- The result: dozens of PRs across several upstream repos landed
  unverifiable - GitHub had no account to link the commit to at all (not
  merely "unverified"), so CLA-assistant bots rejected them and the commits
  showed no avatar/username in GitHub's UI. This went unnoticed for a long
  stretch because nothing failed *loudly* - the commits succeeded, the pushes
  succeeded, only a downstream bot comment surfaced it, per PR, much later.

A rule stated once in a project's `CLAUDE.md`/`AGENTS.md` gets re-read (or
not) by every fresh agent context. An explicit command-line override always
wins over a global default, so restating the correct default doesn't help
once something is actively overriding it.

## Why a `$PATH` shim, not a Claude Code `PreToolUse` hook

This pack's other guardrails (`git-guardrails-claude-code`,
`docker-volume-guardrails`, `docker-db-guardrails`) are Claude Code
`PreToolUse` hooks - they intercept a tool call *before Claude's own Bash
tool runs it*. That pattern is a good fit for those because the thing being
protected against is Claude Code's own action.

Identity enforcement has a wider blast radius: the same OSS-contribution
campaign that motivated this skill also runs work through `codex exec`
subprocesses and dispatched subagents, none of which go through this
session's own `PreToolUse` hook chain - a hook registered in
`~/.claude/settings.json` only ever sees tool calls from *this* Claude Code
session. A `PreToolUse` hook here would still leave every other process on
the machine free to commit under the wrong identity.

A `$PATH` shim is transparent to *anything* that shells out to `git` -
this session, a subagent, a `codex exec` subprocess, a plain terminal, a cron
job. It also composes safely with a repo's own hooks (husky, lint-staged,
pre-commit framework): those live in `.git/hooks/` and run as part of the
*real* git binary's own execution, which this shim calls via `exec` after
its own check passes - it never touches `core.hooksPath` or a repo's hook
files, so nothing about a project's existing tooling changes.

## What Gets Blocked

- `git commit` (any form) where the effective `user.name`/`user.email` -
  from an explicit `-c user.name=...`/`-c user.email=...`, a
  `--author="Name <email>"` override, a `GIT_AUTHOR_*`/`GIT_COMMITTER_*`
  environment variable, or a plain `git config` default - doesn't match the
  configured identity. Author and committer are resolved independently, so a
  correct `GIT_COMMITTER_EMAIL` can't launder a wrong configured author.
- `git commit-tree` under a `GIT_AUTHOR_*`/`GIT_COMMITTER_*` environment
  override that doesn't match (this is the one commit-creation path that
  bypasses git's own hook system entirely, so a hook-based approach alone
  cannot catch it - see "Known limitations" for why the shim's push-time
  check is the actual backstop for this case).
- `git push` of any commit - however it was created (`commit`,
  `commit-tree`, `rebase`, `cherry-pick`, an inherited bad commit from
  upstream history) - if its author or committer identity doesn't match.
  The check reads the invocation's actual refspecs, so it covers pushing a
  branch other than the checked-out one, a raw SHA, a tag, a detached HEAD,
  and `--all`/`--tags`, not just `HEAD`. Commits the *destination* remote
  already has are excluded; commits already on a *different* remote are
  still checked.
- Any invocation whose argument layout this wrapper cannot parse, if a gated
  subcommand appears in it - the parse fails closed rather than open.

Every other subcommand, and a repo's own commit-time hooks, are untouched.

## Steps

### 1. Decide the identity

Almost always: whatever `git config --global user.name`/`user.email`
already is. Confirm with the user if there's any doubt - this is the one
identity every commit on the machine will be forced to use.

### 2. Run the installer

```bash
bash scripts/install.sh                       # uses the existing global git config
# or, explicitly:
bash scripts/install.sh "Your Name" "you@example.com"
# or, to a specific directory (must precede the real git in $PATH):
bash scripts/install.sh "Your Name" "you@example.com" ~/.local/bin
```

The installer first checks that `<install-dir>` really precedes the real git
in `$PATH`, and aborts without writing anything if it doesn't. Only then does
it write `~/.config/git-identity-guard/config`, copy
[scripts/git-identity-guard.sh](scripts/git-identity-guard.sh) to
`<install-dir>/git`, `chmod +x` it, and overwrite the global
`user.name`/`user.email` to match (belt-and-suspenders for tools that read
config directly - it announces this before doing it).

If it aborts, add the printed `export PATH=...` line to the shell rc file,
open a new shell, and re-run.

### 3. Verify

Test both directions before trusting this in a new environment:

```bash
cd "$(mktemp -d)" && git init -q
echo x > x.txt && git add x.txt

# Should be BLOCKED (exit 1) - wrong email explicitly forced:
git -c user.name="Your Name" -c user.email="wrong@example.com" commit -m "should fail"

# Should SUCCEED (exit 0) - correct identity:
git -c user.name="Your Name" -c user.email="you@example.com" commit -m "should pass"

# Should be BLOCKED (exit 1) - --author override:
git commit -m "should fail" --author="Someone Else <wrong@example.com>"

# Should be BLOCKED (exit 1) - the config variable is not a kill switch:
GIT_IDENTITY_GUARD_CONFIG=/dev/null \
  git -c user.email="wrong@example.com" commit -m "should fail"

# Should be BLOCKED (exit 1) - commit-tree bypass with a bad env override:
echo y > y.txt && git add y.txt
TREE=$(git write-tree); PARENT=$(git rev-parse HEAD)
GIT_AUTHOR_NAME="Your Name" GIT_AUTHOR_EMAIL="wrong@example.com" \
GIT_COMMITTER_NAME="Your Name" GIT_COMMITTER_EMAIL="wrong@example.com" \
  git commit-tree "$TREE" -p "$PARENT" -m "should fail too"
```

Then confirm a repo's own hooks still fire (coexistence, not replacement):

```bash
mkdir -p .git/hooks
printf '#!/bin/bash\necho REPO HOOK FIRED\n' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
echo z > z.txt && git add z.txt
git -c user.name="Your Name" -c user.email="you@example.com" commit -m "hook coexistence check"
# Expected output includes both "REPO HOOK FIRED" and a successful commit.
```

## Known limitations

- `check_identity` (the commit-time gate) reads `GIT_AUTHOR_*`/
  `GIT_COMMITTER_*` env vars and `-c`/`git config` overrides, which covers
  every realistic way a commit gets created *through this wrapper*. It
  cannot see a commit created by a process that bypassed the wrapper
  entirely (e.g. a differently-pathed `git` binary invoked by full path, or
  a language binding that calls libgit2 directly instead of shelling out).
  It also can't statically resolve an identity a commit *inherits* rather
  than states - `git commit --amend` without `--reset-author`, `commit -C
  <commit>`, `rebase`, `cherry-pick`. The `push`-time check is the backstop
  for all of those: it inspects the real author/committer metadata of every
  commit that the invocation would actually send and that the destination
  remote doesn't already have, regardless of how the commit was created, and
  blocks the push if any of them don't match. A commit that reaches a remote
  through a path this wrapper never sees at all (a real git invoked by
  absolute path, a libgit2 binding) is outside its reach entirely.
- Commits the destination remote already has are not re-checked, so history
  inherited from an upstream (authored by other people, as it should be)
  doesn't block a push. The flip side: a bad commit that somehow already
  exists on that same remote won't be flagged on a later push.
- Requires `<install-dir>` to precede the real git's directory in `$PATH`.
  `install.sh` verifies this *before* writing anything and aborts without
  side effects if the wrapper wouldn't be active, but it can't force a
  running shell to pick up a `$PATH` change - a new shell is needed.
- Other copies of this wrapper on `$PATH` are recognized by a marker string
  in the file header. A file is only treated as a copy if it starts with a
  `#!` shebang *and* carries the marker in its first 40 lines, so the real
  (binary) git and unrelated scripts that merely mention the variable name
  are not mistaken for one.
- There is no override flag, and `GIT_IDENTITY_GUARD_CONFIG` is not one: if
  it is set but doesn't name a readable regular config file, every gated
  subcommand is refused rather than let through. (When the variable is unset
  and no config exists at the default path, the wrapper does pass everything
  through - that is the genuine pre-install state, not a bypass.) If this
  blocks a commit under a genuinely different, correct identity (e.g.
  co-maintaining someone else's fork under their name), the fix is to run
  `scripts/install.sh` again with the new identity, not to bypass the check
  for one commit.
- The push-time check has one built-in exception: a commit whose committer
  is exactly `GitHub <noreply@github.com>` (created by GitHub itself - a
  web-UI squash-merge, an "Update branch" click, a bot-authored commit) is
  only checked on its author *email*, not its author/committer *name*.
  Found live while retroactively rewriting a batch of already-open PR
  branches: several contained legitimate GitHub-generated commits (another
  maintainer's merge, a CI bot's auto-format commit) whose author display
  name naturally isn't the configured `REQUIRED_NAME` string. Forcing those
  to match would misattribute a real action GitHub took on someone else's
  behalf - the email is the actual signal CLA bots and account-linking use,
  so that's what's still enforced.
