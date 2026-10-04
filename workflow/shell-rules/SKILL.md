---
name: shell-rules
description: Shared shell rules for portable, approval-friendly agent commands. Use when running git, GitHub CLI, builds, tests, cross-directory commands, or commands that write files.
user-invocable: false
---

## Command Shape

- Prefer one logical command per tool call. Separate unrelated inspection, mutation,
  and verification so failures and approvals remain attributable.
- Do not assume a directory change persists between tool calls. Use the client's
  `workdir`/working-directory parameter or the command's own directory option, such
  as `git -C <path> status`.
- Avoid `bash -c`, conditional shell programs, compound pipelines, and command
  substitutions when the agent can run a command, inspect its result, and branch in
  reasoning instead.
- Never start an interactive CLI flow from automation. Pass explicit titles, bodies,
  messages, and other required inputs.

## Background Commands

- Prefer the foreground. Background execution is for a command that must keep running
  while the agent does other work — a dev server, a desktop app, a file watcher. A
  slow-but-finite command (a build, a test suite, a formatter) belongs in the foreground
  with a raised timeout instead; backgrounding one only to skip the wait creates a shell
  nobody is accountable for.
- Stop every background shell you start. Before a workflow reports its result, review the
  shells it started and stop each one still running, using the client's own
  background-shell control (in Claude Code, the kill/stop tool that takes the shell id
  returned when the shell was started; in Codex, the recorded process). A command that
  looks finished is not proof its shell exited — check, then stop.
- A leaked shell is not free. Claude Code reports still-running background shells on the
  session's `Stop` event, and cenci-watch deliberately holds such a session at `running`
  rather than `done` (#698/#699) because it cannot tell an abandoned shell apart from work
  the session is genuinely waiting on. The hold clears on the session's next event, and an
  abandoned shell never produces one, so the session reads as still-working until it ends.
- A process meant to outlive the session is exempt, but only when it detaches for real —
  its own session/process group and its own log file, never the agent's shell. `cenci
  babysit` is the reference case: it detaches its own supervisor, so its launching shell
  exits normally and there is nothing to reap.

## Command Output Discipline

- A long-running build or test run's stdout+stderr belongs in a log file, not inline in the
  transcript: redirect it to an absolute path under `${TMPDIR:-/tmp}/cenci/<name>-<scope>.log`,
  reusing `## Body Files and Heredocs`'s `<scope>` uniqueness and `^[A-Za-z0-9._-]+$`
  validation rule so concurrent runs never collide on a shared fixed name.
- Locate a failure with the client's search tool rather than scanning full output by eye — in
  Claude Code, `Grep` over the log; in Codex, `rg`. Then read only the failing region with the
  client's read tool (Claude Code's `Read`, or the portable equivalent) instead of the whole
  file.
- Do not paste a full command run back into the conversation: never inline a whole suite run
  into the transcript. A full passing or failing run dumped verbatim wastes context on lines
  nobody needs and, on retry, repeats the cost every time.
- Precedence: a single `>… 2>&1` redirect into that log is one command and does not violate
  `## Command Shape`'s one-command-per-call rule — it is a plain redirection, not a pipeline or
  compound. `## Worktrees and Cross-Directory Writes`'s absolute-path requirement still binds:
  `guard-main-worktree.sh` refuses a relative redirect target, so the log path in the redirect
  must itself be absolute (`${TMPDIR:-/tmp}`/`$TMPDIR`/`$HOME`/`$PWD` are its supported
  expansions).

## Search and File Operations

Use the client's native read, search, glob, and patch tools when available. In Codex,
prefer `rg`/`rg --files` for repository search when no structured search tool is
available. In Claude Code, prefer `Read`, `Grep`, and `Glob`.

Do not add shell banners such as `echo "=== files ==="` to batched searches. They
make output noisier and can change approval matching.

Use the client's patch or edit tool for source changes. Shell-based generation is
appropriate only for mechanical output, formatter/codegen output, or tools whose
normal interface writes files.

## Body Files and Heredocs

Heredocs can require shell-created temporary files and may fail in restricted
sandboxes. Write long issue or pull-request content with the client's file tool, then
pass it through a CLI body-file option. Scope every such filename with a run-unique
suffix — `<scope>` below is a ticket id, PR number, or run id, whichever is already
in scope for the calling skill — so concurrent runs never collide on a shared fixed
name. Any scope key that isn't already format-constrained by its own source (a
numeric ticket/PR ID is inherently safe) must be validated against
`^[A-Za-z0-9._-]+$`, additionally rejecting `.`, `..`, or any value containing `..`,
before use — the same rule `implement`'s slug validation applies, since a scope key
can end up as a standalone path segment (e.g. a per-run subdirectory) where a
dot-only value could traverse:

```bash
gh issue edit <number> --body-file "${TMPDIR:-/tmp}/cenci/issue-body-<scope>.md"
```

Any write that also sets a title goes through `gh api ... --input` instead of
`gh issue edit --title`/`gh issue create --title` — neither has a `--title-file`
equivalent, so a title carried as a shell argument is always an interpolation risk.
Compose the JSON payload mechanically instead of hand-escaping it, in three steps:

1. The file tool writes the raw title and body as plain text to `<scope>`-suffixed
   files — never a hand-escaped JSON literal.
2. A standalone `jq -n --rawfile title <f> --rawfile body <f>` call builds the
   payload on one source line and redirects it to a payload file. General form:
   `jq -n --rawfile title <f> --rawfile body <f> '{title: ($title | rtrimstr("\n")), body: $body}' > <payload>.json`.
   Concretely:

   ```bash
   jq -n --rawfile title "${TMPDIR:-/tmp}/cenci/issue-title-<scope>.txt" --rawfile body "${TMPDIR:-/tmp}/cenci/issue-body-<scope>.md" '{title: ($title | rtrimstr("\n")), body: $body}' > "${TMPDIR:-/tmp}/cenci/issue-<scope>.json"
   ```

   `rtrimstr("\n")` strips the file tool's trailing newline from the title — an
   untrimmed title breaks the post-write title re-fetch comparison. `jq` cannot let
   `--rawfile` content influence the payload's *structure*, so a well-formed
   injection attempt in the title/body still can't add or change JSON keys.
3. A separate `gh api ... --input <payload>.json` call sends it:

   ```bash
   gh api repos/<owner>/<repo>/issues/<number> -X PATCH --input "${TMPDIR:-/tmp}/cenci/issue-<scope>.json"
   ```

As with the body file above, the raw title/body files and the payload file are all run-scoped by the existing `<scope>` rule above. The `jq` call and the `gh api` call are separate Bash calls (no pipe, no `&&`) — each is a single non-compound command whose result the agent inspects before proceeding.

```bash
gh pr create --title "<title>" --body-file "${TMPDIR:-/tmp}/cenci/pr-body-<scope>.md"
```

`gh pr create` has no `--input`/`--title-file` equivalent, so its title stays a
plain `--title` argument (out of scope for the `jq` pattern above).

Never print or interpolate authentication tokens into command output.

## Reading PR CI Status

Never derive a PR's CI status from check *conclusions*. `gh pr view --json
statusCheckRollup` leaves `conclusion` **empty** for a check that is still queued or
running, so a conclusion-only scan silently reads "still running" as "passed" — the whole
class of false-green PR reports (#900).

Read the buckets instead, as one standalone call:

```bash
gh pr checks <pr-number> --repo <owner>/<repo> --json bucket,name,state
```

`bucket` is the settled classification: `pass`, `fail`, `pending`, `skipping`, or
`cancel`. Classify strictly, matching what `cenci babysit` enforces before it will
automerge (`watch/internal/babysit/automerge.go`), so an agent's answer and the
supervisor's behavior can never disagree:

- **Green** only when at least one check exists *and* every check is in `pass`.
- Any check in `pending` → the answer is "still running", not green. Report those checks
  by name and say what is still outstanding; never round them up to a pass.
- `fail`, `cancel`, `skipping`, or an empty/unrecognized bucket → not green, each
  reported as itself rather than folded into "failing".
- **Zero checks** is *unknown*, never green — a PR whose workflows have not been created
  yet looks identical to a PR with no CI at all.

`gh pr checks` exits **8** while checks are pending and still writes valid JSON to stdout.
Treat a non-zero exit as a genuine command failure only when the JSON does not decode — an
exit code alone is neither a CI-failure signal nor a reason to report the read as broken.

State the same distinction in prose: "CI is green" means every check finished and passed.
While anything is pending, say so — "CI green except `<check>`, still running" — even when
every finished check passed.

## Shell Portability

Commands may run through zsh, bash, or another configured login shell. Prefer
portable command syntax and avoid bash-only arrays, `mapfile`/`readarray`,
`BASH_REMATCH`, and shell-specific array slicing. When complex shell logic is truly
needed, put it in a reviewed repository script with an explicit interpreter.

## Worktrees and Cross-Directory Writes

- Keep the main worktree read-only for implementation and direct edits to the feature
  worktree with an absolute path or the tool's working-directory option.
- Do not combine `cd <other-dir>` with a write, redirection, or unrelated command.
- The same absolute-path rule applies to Bash redirect (`>`, `>>`) and `tee` write
  targets specifically: `guard-main-worktree.sh` refuses every relative target the
  tokenizer extracts, because a preceding directory change, a subdirectory hook
  cwd, or a symlink can move where the write actually lands. Use an absolute
  feature-worktree, plan, design, or temp path so the guard can canonicalize it
  before deciding; unsupported zero-parse constructs retain the bounded residual
  documented in `docs/adapter-contract.md`.
- Never rescue an edit made in the wrong worktree with stash, checkout, or file
  copying. Reapply the intended edit to the correct absolute path, then restore only
  changes created by the current operation.

## Client-Specific Approval Notes

### Claude Code

Claude Code allow rules and its shell analyzer inspect every segment of compound
commands. A call containing both `cd` and a redirection/write can hard-prompt even
when each command is allow-listed. Use standalone calls or `git -C`.

### Codex

Codex evaluates shell segments independently at control operators and may require
approval for any unmatched segment. Supply `workdir` on each shell call rather than
relying on a previous `cd`, and request narrowly scoped escalation only after a
sandbox-related failure or when the operation inherently needs it.
