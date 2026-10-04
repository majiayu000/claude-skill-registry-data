---
name: git-guardrails-claude-code
description: "Infrastructure safety skill for blocking dangerous git commands in Claude-driven workflows. Use when the repo or user environment needs guardrails against destructive git operations. Not a delivery-pipeline step; it makes later work safer."
---

# Setup Git Guardrails

Sets up a PreToolUse hook that intercepts and blocks dangerous git commands before Claude executes them, and refuses `gh pr merge` when the pull request's review stamp is stale.

## Invocation Position

This is an infrastructure safety skill, not a feature-delivery step.

Use `/git-guardrails-claude-code` when the project or user wants stronger protection against destructive git operations in Claude-driven workflows.

Do not treat it as part of the normal feature pipeline. It is a repo or user setup action that makes later work safer.

## What Gets Blocked

- `git push --force` / `git push -f` / `git push --force-with-lease`
- `git push origin +main` (a leading `+` on a refspec is a force push)
- `git push --mirror` (force-updates every remote ref)
- `git reset --hard`
- `git clean -f` / `git clean -fd` / `git clean -df` / `git clean -d -f`
- `git branch -D` / `git branch --delete --force` / `git branch -f -d`
- `git checkout .` / `git restore .` / `git checkout -- .` / `git restore -- .`
- `git checkout ./` / `git checkout ./.` / `git checkout :/` / `git restore :/`

The guard reads the command as tokens and never evaluates it, so a destructive command assembled at run time — a flag or subcommand held in a variable, spliced with `${IFS}`, or produced by command substitution — is not visible to it. That is a limit of the design, not a missing entry; #334 records it alongside the destructive commands the lists do not yet cover.

## What Gets Blocked Conditionally

`gh pr merge` is the one command here refused on a *condition* rather than on its shape. `/pre-merge` stamps the commit it reviewed into the PR body; `/closeout` Step 2 reads that stamp back before merging. The guard performs the same read at the merge itself, so a merge typed by hand or issued by an AFK loop cannot skip it (#327). It refuses only when the PR carries a stamp and that stamp names a commit other than the PR's current head — the reviewed diff is not the diff about to land.

### Refused when the review stamp is stale

- `gh pr merge`
- `gh pr merge # ship it`
- `gh pr merge 4821`
- `gh pr merge 4821 --squash --delete-branch`
- `gh pr merge 4821 -R owner/repo`
- `gh pr merge my-branch`
- `sudo gh pr merge 4821`
- `bash -c "gh pr merge 4821"`

The refusal prints both SHAs and the size of what landed after the review, then names its two exits: re-review with `/pre-merge`, which re-stamps at the new head, or re-run the merge with `ALLOW_STALE_STAMP_MERGE=1` in front of it to accept the diff as it stands. That variable is also honored as an exported environment variable, for a repo that wants the check advisory rather than blocking.

`-R` / `--repo` is read and forwarded to the lookup, so `gh pr merge 4821 -R owner/repo` is judged against PR 4821 *in that repo*. Dropping it made the first version of this check refuse on the wrong pull request.

### Allowed even when the stamp is stale

- `echo gh pr merge now`
- `grep -rn "gh pr merge" .`
- `git commit -m "gh pr merge is what closeout runs"`
- `gh pr merge --squash 4821`
- `gh pr merge --subject fix 4821`
- `gh pr merge --squash my-branch`
- `gh pr view 4821`
- `gh pr list`

Two different reasons, and both are deliberate.

The first three only *mention* the words. Unlike the git rules above, a `gh` token is inspected only where it is being invoked — first in its segment, or after an environment assignment or a wrapper (`sudo`, `env`, `xargs`, `bash -c`, `eval`, and the shell keywords) — and never inside a heredoc body. The asymmetry is the point: a `git push --force` written as search text is refused because a blocked grep costs one rephrase and a missed force push costs history, while the words `gh pr merge` appear in prose, in commit messages, and in every grep for them, and a missed merge is read a second time by `/closeout`.

The last five are commands the guard declines to judge, and the rule that decides is deliberately narrower than it could be. Two facts resolve which PR a merge would act on without this repo owning a copy of gh's option list: `gh pr merge` takes at most one positional argument, and a flag's value always follows its flag. So an operand appearing **before any flag** is the PR, and an operand appearing after one might be some flag's value — `gh pr merge --squash 4821` is therefore a miss, not a guess. An earlier draft guessed, on the reasoning that no gh flag takes a number; reading `gh pr merge --help` shows five that take a value, and the guess was resolving `gh pr merge --subject 4821` to PR 4821 while the merge itself would target the current branch's PR. Looking up the wrong pull request is worse than looking up none, because it reaches a confident verdict about a PR nobody asked about.

The check also fails open when `gh` or `jq` is absent, when the API call fails, when the PR carries no stamp, and when the stamp is malformed — every case where it cannot be certain. A gate that refuses wrongly is a gate that gets deleted, and `/closeout` Step 2 still performs this read on the path most merges take.

It inherits the design limit recorded above for the git rules, and for the same reason: the command is read as tokens and never evaluated, so a merge assembled at run time — `$CMD`, `gh${IFS}pr${IFS}merge`, a subcommand produced by command substitution — is invisible to it. #334 carries that limit for both halves.

## What Stays Allowed

- `git push origin feature/my-branch`
- `git reset --soft HEAD~1`
- `git clean -n`
- `git branch -d merged-branch`
- `git checkout main`
- `git checkout .github/workflows/ci.yml`
- `git restore .gitignore`
- `git restore --staged .` (unstages; never touches the working tree)
- `git checkout -p .` (prompts per hunk before discarding anything)
- `git commit -m "ordinary message"`

Both lists are executable, not decorative. `scripts/test-git-guardrails.sh` extracts every command in them and runs it through the real script, asserting exit 2 for the first list and exit 0 for the second. Adding a line to either list without making the script agree fails CI.

That test exists because this section was wrong for an unknown period: it claimed `git push -f` was blocked when the matcher only ever saw the `--force` long form (#227). A guard's own documentation is the thing a user reads when deciding whether to install it, so an unchecked claim here is worse than no claim.

### How matching works

The script parses the command into arguments rather than searching it for substrings, so it sees past the surface forms a substring search misses:

- **Flag order and bundling** — `-fd`, `-df`, and `-d -f` are the same command.
- **Long and short forms** — `-D`, `--delete --force`, and `-f -d` are all force-deletes of a branch.
- **The `--` separator** — `git checkout -- .` is `git checkout .`.
- **Leading global options** — `git -C /some/path push -f` is still a force push.
- **A path is not a pathspec of `.`** — `git checkout .github/workflows/ci.yml` merely *starts* with a dot and is left alone.

- **A pathspec is recognized by reduction, not by spelling** — `.`, `./`, `./.`, `:/`, and `:/.` all name the whole tree, so all are blocked without the script listing each one.

Matching stays deliberately conservative in two ways. A `git` token is inspected wherever it appears in a segment, so wrappers like `sudo git push -f` and `bash -c "git push -f"` are still caught. And `--force-with-lease` is blocked alongside `--force`: it is the safer force push, but it still rewrites published history.

### Known limitation — quoted text is matched too

Quote characters are stripped before the command is tokenized. That is what lets the guard see into `bash -c "git push -f"`, and the cost is that a dangerous command appearing as *quoted text* is also refused:

```bash
git commit -m "Block git push -f, which the matcher missed"   # refused
grep -r 'git push --force' docs/                              # refused
```

Both are harmless commands, and the block message will wrongly call them destructive. The two cases cannot be separated — honoring quotes would fix these and reopen the `bash -c` bypass — so the guard fails closed. Rephrase the message or search string. Commit messages are the surface this bites most often, which is why it is documented here rather than left to be rediscovered.

### Requirements

`jq` must be on `PATH`. If it is missing the hook cannot parse its input, so it refuses git commands rather than silently allowing them; non-git commands are unaffected.

`gh` is needed only for the review-currency refusal above, and only when a `gh pr merge` is being inspected. Without it — or without network, or without auth — that one check fails open and the git rules are unaffected.

When blocked, Claude sees a message telling it that it does not have authority to access these commands.

## Steps

### 1. Ask scope

Ask the user: install for **this project only** (`.claude/settings.json`) or **all projects** (`~/.claude/settings.json`)?

### 2. Copy the hook script

The bundled script is at: [scripts/block-dangerous-git.sh](scripts/block-dangerous-git.sh)

Copy it to the target location based on scope:

- **Project**: `.claude/hooks/block-dangerous-git.sh`
- **Global**: `~/.claude/hooks/block-dangerous-git.sh`

Make it executable with `chmod +x`.

### 3. Add hook to settings

Add to the appropriate settings file:

**Project** (`.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

**Global** (`~/.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

If the settings file already exists, merge the hook into existing `hooks.PreToolUse` array — don't overwrite other settings.

### 4. Ask about customization

Ask if the user wants to change what is blocked. Git rules live in the `case "$subcommand"` block in the middle of the copied script — one arm per git subcommand, each testing parsed flags and operands. Add a new arm for a subcommand that has none, or extend an existing arm's condition. The review-currency refusal is separate, in `check_gh_merge` below them, because it is conditional on repository state rather than on the command's shape.

There is no pattern array to edit. An earlier version of this script matched literal substrings; that is what let `git push -f` through (#227), and the rewrite replaced it with argument parsing.

If you change the rules, update the two lists above to match — `scripts/test-git-guardrails.sh` in the Skill Kit repo executes both lists against the script, so the documentation and the behavior fail CI together rather than drifting apart.

### 5. Verify

Run a quick test:

```bash
# Should be BLOCKED (exit 2):
echo '{"tool_input":{"command":"git push --force origin main"}}' | <path-to-script>
echo '{"tool_input":{"command":"git push -f origin main"}}' | <path-to-script>
echo '{"tool_input":{"command":"git checkout -- ."}}' | <path-to-script>

# Should be ALLOWED (exit 0):
echo '{"tool_input":{"command":"git push origin feature/my-branch"}}' | <path-to-script>
echo '{"tool_input":{"command":"git checkout .github/workflows/ci.yml"}}' | <path-to-script>
```

Each blocked command should exit with code 2 and print a BLOCKED message to stderr. Each allowed command should exit with code 0.

The short-form and `--` cases are here deliberately. An earlier version of this check tested only `git push --force`, so it passed while `git push -f` went unguarded — a self-check narrower than the claim above it cannot surface the gap it is meant to catch.

This block does not exercise the `gh pr merge` refusal, which needs a stamped pull request and a reachable API to have any verdict at all. `scripts/test-git-guardrails.sh` covers it against a stubbed `gh`, and both lists in "What Gets Blocked Conditionally" are executed there the same way the git lists are.

## Handoff

- **Expected input:** a project or user environment that needs stronger git safety controls
- **Produces:** installed guardrail hooks and safer Claude git behavior
- **Supports downstream:** all implementation and review work by reducing destructive-command risk
- **What comes next:** return to normal workflow with the guardrails in place
