---
name: opus-delegate
description: Delegate substantial implementation, debugging, or independent review from Codex to Claude Opus when it can reduce the calling model's token use while preserving solution quality. Use when handing off bounded implementation, hard debugging, or adversarial review of a diff, and for the `opus-guidelines` alias, which profiles the current repository for delegation and writes that profile into AGENTS.md. Do not use for trivial tasks or work a cheaper local subagent handles.
metadata:
  version: "0.1.0"
  short-description: Hand bounded work to Claude Opus
---

# Opus delegation

The aim is to save the calling agent's tokens while retaining its strengths in
reasoning, architecture, and judgment. Use Opus for substantial, bounded
implementation or independent analysis; keep the caller responsible for task
decomposition, integration, critical review, and final validation.

Judge savings across the whole task, including briefing, duplicated context,
review, and rework. Delegate when those costs are likely lower than the caller
doing the work directly. Each delegation also carries a fixed floor of roughly
18k prompt tokens for Opus's own session setup, regardless of how small the
task is, so trivial handoffs lose on cost even when they succeed. Give focused context and request concise evidence
instead of raw logs; do not duplicate the delegated implementation in the
calling session. Token savings must not reduce correctness, necessary
verification, or completion of the user's request.

Invoke:

    <skill-dir>/scripts/opus_worker.sh

for implementation, and

    <skill-dir>/scripts/opus_consultant.sh

for consulting/debugging. `<skill-dir>` is this skill's own directory —
`${CODEX_HOME:-~/.codex}/skills/opus-delegate` for a normal install, or the
plugin's `skills/opus-delegate` when installed as a plugin. Pass the target
repository with `--cwd` rather than relying on the current shell directory,
and provide the complete task through stdin. This keeps delegation portable
when the caller is working in another repository.

Use a compact brief containing:

- objective and relevant repository/context;
- target repository path and files or symbols in scope;
- ownership boundaries (what Opus may edit and what it must leave alone);
- constraints and acceptance criteria; and
- verification commands and the evidence to report.

Do not make Opus rediscover context the caller already has, but include enough
context for it to work independently.

## Aliases

Codex registers no slash commands, so these are plain phrases the user types.
Route them here:

- **`opus-guidelines`** (also `/opus-guidelines`, "set up this repo for
  delegation") — follow `references/repo-profile-recipe.md`. It profiles the
  current repository and writes a delegation section into `AGENTS.md`, so
  later sessions know this repo's verification commands and which paths are
  off-limits.

Codex loads `AGENTS.md` automatically but does **not** resolve `@file`
imports. Repo-specific delegation notes must be inlined into `AGENTS.md`;
pointing at a separate file leaves them unread.

## When to use Opus

Prefer Opus for substantial implementation it can carry through reliably, or
when independent reasoning would materially improve confidence. Use a cheaper
subagent for routine bounded work, and keep small tasks local when delegation
overhead would exceed the benefit.

Other situations where you might find Opus useful:
- difficult debugging where the root cause is unclear;
- adversarial review of a proposed implementation;
- situations where your own diagnosis is uncertain;
- bugs for which an earlier attempted fix failed;
- research-oriented or algorithmically difficult implementation questions that you had trouble understanding.

Do not use Opus for:
- simple file discovery;
- grep/search operations;
- routine tests;
- straightforward mechanical changes;
- tasks already adequately handled by a cheaper subagent.

## Delegation protocol

When you need its opinion on something, treat Opus as an independent expert, not an authority.

Give it sufficient context to solve the task, but do not bias it with your
preferred answer when independent judgement is desirable.

For implementation work, ask Opus to return:
1. status (complete, partial, or blocked);
2. concise summary of changes and relevant files/symbols;
3. verification commands actually run and their results;
4. remaining work, blockers, and uncertainties.

For consultation or debugging, ask Opus to return:
1. conclusion and independently derived reasoning/evidence;
2. relevant files and symbols;
3. recommended action;
4. uncertainties, competing explanations, and how to distinguish them.

For debugging, ask Opus to independently derive the root cause and attempt
to falsify plausible competing hypotheses.

For review, provide the proposed implementation or current diff and ask
Opus to actively search for correctness problems, regressions and missing
edge cases. Require each finding to include severity, file and line or symbol
location, concrete evidence, and a recommended fix; require an explicit
statement when no findings were found.

After receiving the result:
- inspect its evidence yourself;
- reconcile it with your own findings and other agents;
- do not blindly implement its recommendation;
- retain responsibility for the final decision and verification.

Treat a nonzero exit, timeout, interruption, or `partial`/`blocked` report as
incomplete work. Inspect the working tree and diff, preserve useful partial
changes, and either resume with a brief that states what remains or finish the
task locally. Do not report completion unless the acceptance criteria and
verification have been satisfied.

Before delegation, inspect the target working tree and preserve unrelated user
changes. In a shared checkout, give Opus explicit file ownership and do not
have the caller or another agent edit those files concurrently. Use an isolated
Git worktree for concurrent, risky, or broad changes when practical; integrate the
result only after reviewing its diff and verifying it in the target repository.
A new worktree does not include uncommitted changes: explicitly transfer any
changes needed for the task without overwriting unrelated work.

## Instructions to use the claude command

Both wrappers read the prompt from stdin and default to `xhigh` effort and JSON
output. Pass the target repository explicitly with `--cwd`; the wrapper runs
Opus from that directory. For example:

    SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/opus-delegate"
    printf '%s\n' "$TASK" | "$SKILL_DIR/scripts/opus_worker.sh" medium \
      --cwd /path/to/repository --timeout 300 \
      --allow-tool 'Bash(npm test *)'

Supported options are `low`, `medium`, `high`, `xhigh`, or `max` effort;
`--cwd DIR`; `--timeout SECONDS`; `--resume SESSION_ID`;
`--output-format text|json|stream-json`; `--session-file FILE`; and repeated
`--allow-tool TOOL`.
Use `--resume` with the returned session identifier when continuing an
interrupted or partial delegation. Keep the target repository in `--cwd`, and
keep the skill path absolute even when the current shell directory differs.

`--allow-tool` adds task-specific preapprovals; it does not define the entire
available tool set or bypass permission rules. Worker mode preapproves only
`Read`, `Edit`, `Write`, and read-only `git diff`/`status`/`log`, so pass the
verification commands the task needs with `--allow-tool`.

Patterns match the literal command string, not the tool behind it:
`'Bash(pytest *)'` does not match `python -m pytest`, which is what a worker
often reaches for. Allow every invocation form the task might use, or state
the exact command to run in the brief. Both modes deny
requests that would require a permission prompt. Workers must report denied
verification commands as blockers, never as passing checks. Consultant mode
uses plan permissions; use worker mode when the task requires edits.

The wrappers require Bash and Claude Code, plus a UUID source (`/proc`,
`uuidgen`, or `python3`) and GNU `timeout` when `--timeout` is used. No timeout
is imposed unless specified.

If a delegation fails with a connection or API error, the caller's sandbox is
probably blocking network access rather than the task being at fault: Codex's
`workspace-write` sandbox denies network unless `sandbox_workspace_write.network_access`
is `true` in `~/.codex/config.toml`. Report that as a blocker and say what the
user must change; do not retry it repeatedly or fall back to doing the work
locally without saying so.
They announce a session ID and log path on stderr before launching Claude.
Each run gets a separate log under `${XDG_STATE_HOME:-$HOME/.local/state}/opus-delegate`,
containing the session ID, emitted stdout/stderr, and exit status. Use
`--session-file FILE` to append to a chosen log; relative paths resolve against
the caller's directory. Logs contain task output; remove them when no longer needed.

Claude output and diagnostics are combined on stdout and in the log; the log
also contains wrapper metadata and is not a standalone JSON document. For
partial progress during long runs, choose `--output-format stream-json`.
On timeout, the wrapper sends TERM then escalates to KILL after five seconds;
exit 124 normally indicates timeout (forced termination can return 137).
A saved ID permits `--resume` only if Claude persisted the session before the
interruption. Inspect partial edits before resuming, and do not retry unchanged
permission or environment failures repeatedly.
