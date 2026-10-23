---
name: code-review
description: 'Reviews local changes or GitHub PRs and saves actionable findings. Use when reviewing a PR, requesting a full local review, or creating a review-fix artifact.'
argument-hint: '[--quick] [--approve | --request-changes] [--parallel | --team] [--no-worktree] [--keep-draft] [--keep-worktree] [--yes] [--save] [pr-number | pr-url | blank for local review]'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Skill
  - Agent
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
  - SendMessage
  - Bash(git:*)
  - Bash(gh:*)
  - Bash(ls:*)
  - Bash(cat:*)
  - Bash(test:*)
  - Bash(find:*)
  - Bash(npm:*)
  - Bash(pnpm:*)
  - Bash(yarn:*)
  - Bash(bun:*)
  - Bash(npx:*)
  - Bash(cargo:*)
  - Bash(go:*)
  - Bash(pytest:*)
  - Bash(python:*)
  - Bash(python3:*)
  - Bash(make:*)
  - 'mcp__github__*'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/*.sh:*)'
---

# Code Review

Review local changes or a GitHub PR; save machine-parseable findings for
`/ycc:review-fix`. Input: `$ARGUMENTS`. Use `/ycc:quick-review` for inline-first
local review. PR review mode adapted from PRPs-agentic-eng by Wirasm.

## Parse flags and select mode

Extract flags before interpreting the remaining text as the selector:

| Flag                | Effect                                                       |
| ------------------- | ------------------------------------------------------------ |
| `--approve`         | Override PR decision to APPROVE; still report findings       |
| `--request-changes` | Override PR decision to REQUEST CHANGES                      |
| `--parallel`        | 3 standalone `ycc:code-reviewer` reviewers                   |
| `--team`            | Same roster, Claude Code agent team                          |
| `--worktree`        | Legacy no-op; PR worktree isolation is default               |
| `--no-worktree`     | PR: skip worktree, artifact commit/push and cleanup          |
| `--keep-draft`      | PR: skip draft-to-ready promotion; draft decision is COMMENT |
| `--keep-worktree`   | PR: keep worktree after successful publish                   |
| `--quick`           | Alias for `/ycc:quick-review` after validation               |

Strip these from `$ARGUMENTS` and set `QUICK_MODE=true|false`, `PARALLEL_MODE=true|false`, `AGENT_TEAM_MODE=true|false`, `NO_WORKTREE_MODE=true|false`, `KEEP_DRAFT=true|false`, and `KEEP_WORKTREE=true|false`. Compute `WORKTREE_MODE=true` unless `--no-worktree` is present (default-on in PR mode; ignored for local mode as before). The remaining text is the mode selector (PR number/URL or blank for local).

Gates (abort on invalid combinations):

- Both `--parallel` and `--team`:
  `--parallel and --team are mutually exclusive. Pick one.`
- `--team` in Cursor/Codex bundles:
  `--team is not supported in bundle invocations; use --parallel instead.`
- `--team` without `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`:
  `--team requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1. Use --parallel instead, or set CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 in your Claude Code settings if you intentionally want agent-team dispatch.`
- `--quick` with PR number/URL:
  `--quick only reviews uncommitted local changes; remove the PR argument or drop --quick.`
- `--quick` with `--approve`/`--request-changes`:
  `--approve / --request-changes have no meaning in quick mode (no GitHub review is posted). Drop the flag or use PR mode.`
- Quick mode accepts `--no-worktree`, `--keep-draft`, `--keep-worktree` as
  no-ops; print `<flag> has no effect in quick mode.`

Mode selection: `--quick` first; PR number/URL (or branch selector) means PR;
blank means local. Local/quick mode MUST NOT post to GitHub, promote drafts,
commit/push artifacts, or remove worktrees.

**Questions:** none. A PR argument is the explicit `confirm-publish` selection: PR mode posts the review, promotes a draft unless `--keep-draft`, and commits and pushes the artifact, interactive or headless. Local and `--quick` modes never publish. See `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.

### Quick delegation

Print:
`--quick delegated to /ycc:quick-review. Run /ycc:quick-review directly for full option surface (--yes, --save, --severity).`

Invoke `Skill: ycc:quick-review`, forwarding its accepted flags (`--parallel`
or `--team`, `--yes`, `--save`, `--write-and-apply`, `--severity <level>`).
Drop code-review-owned flags (`--quick`, decision and worktree flags).
After delegation exit; quick-review owns artifact lifecycle.

## REVIEW path (both modes)

Read changed files in full. Apply mode-specific checklist and severity rubric:

`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/review-checklist.md`

Flag only gaps that affect correctness or the stated requirements. Checklist
items are investigation prompts, not automatic style findings.

The shape of this phase depends on `PARALLEL_MODE` and `AGENT_TEAM_MODE`:

| Flags             | Path                                        |
| ----------------- | ------------------------------------------- |
| Neither set       | **Path A** — single-pass review (default)   |
| `PARALLEL_MODE`   | **Path B** — 3 parallel sub-agent reviewers |
| `AGENT_TEAM_MODE` | **Path C** — 3-reviewer agent team          |

Read only on the selected fan-out path:

- `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/review-dispatch.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/standalone-dispatch.md`
  (`--parallel` only; dispatch contract; reviewers are read-only and the caller persists scratch copies)
- `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/agent-team-dispatch.md`
  (`--team` only; team creation, tasks up front, shutdown, deletion)

Reviewers use checklist roster, pre-ID findings format and merge procedure,
plus the prompt contract in review-dispatch.md. PR prompts include head revision and Phase 2 context. Assign IDs only
after merging; record partial-review gaps, never fabricate failed-role findings.

## Local Review Mode

Uncommitted changes cannot be branch-isolated. Set `WORKTREE_ACTIVE=false`.
If explicit `--worktree`, print:
`Note: --worktree has no effect in local mode; uncommitted changes are not branch-isolated.`

1. **GATHER** — `git diff --name-only HEAD`. Empty: `Nothing to review.`; stop.
2. **REVIEW** — Read changed files, project rules and relevant requirements;
   follow REVIEW path above (Local / Quick checklist).
3. **REPORT** — Read canonical artifact schema before writing:
   `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/review-artifact-format.md`.
   Generate one timestamp per invocation, reused for any fan-out run-id and
   `docs/prps/reviews/local-{YYYYMMDD-HHMMSS}-review.md`. Write even when no
   findings. Apply the schema's Finding ID rules — IDs ordered by severity
   (CRITICAL first), then by file path — plus initial Status and required
   fields.
   Omit Worktree Setup. Include validation table; mark unrun checks Skipped.
   After successful write remove this invocation's parallel scratch directory.

Print artifact path, severity counts, and `/ycc:review-fix <path>` (optionally
`--parallel`) as next steps. Block commit if CRITICAL/HIGH issues exist; never
approve security vulnerabilities.

## PR Review Mode

GitHub-only. Before any `gh pr` call, detect provider on `origin` using
`forge_detect_provider origin`; read
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/forge-detection.md`.
Non-GitHub provider: state limitation, offer local mode; do not call `gh pr`.
Prefer available `mcp__github__*` for fetch/view/review; otherwise use `gh`.
If neither is available, warn and fall back to local-only review without publish.

Read `${CLAUDE_PLUGIN_ROOT}/skills/code-review/references/pr-procedure.md`
only after selecting PR mode; it contains setup commands, validation examples,
posting procedure and edge cases. Read canonical schema for REPORT:
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/review-artifact-format.md`.
For release-base checks in CONTEXT, also read
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/pr-base-and-backport.md#checking-an-existing-pr`.

Phase checklist (execute in order):

- [ ] **SETUP (0½)** — Unless `--no-worktree`, resolve PR head and create/reuse
      parent feature worktree via `setup-worktree.sh`; abort checkout failures.
      All subsequent reads, validation and artifact commands run in that worktree.
- [ ] **FETCH (1)** — Resolve selector, fetch metadata and diff; stop if absent.
- [ ] **CONTEXT (2)** — Rules, PRP artifacts, PR intent, changed files and
      release-base compatibility. Skip release-base check if no release state.
- [ ] **REVIEW (3)** — Full files at PR head (worktree or GitHub API),
      PR checklist; optional fan-out follows REVIEW path above.
- [ ] **VALIDATE (4)** — Run applicable project checks sequentially; record each
      Pass/Fail/Skipped. Review fan-out never parallelizes validation.
- [ ] **DECIDE (5)** — Zero CRITICAL/HIGH and validation pass: APPROVE (comments
      for MEDIUM/LOW); HIGH or failed validation: REQUEST CHANGES; CRITICAL: BLOCK.
      Draft retained with `--keep-draft`: COMMENT. Explicit decision flags override
      recommendation, not findings. Docs/config-only changes get lighter review.
- [ ] **REPORT (6)** — Unless `--keep-draft`, promote draft before reporting.
      Write `docs/prps/reviews/pr-<N>-review.md` under active checkout using shared
      schema. With active worktree, commit only artifact and push before publish.
      Gitignored artifact: skip commit, preserve worktree. Clean scratch only after
      successful artifact write and applicable commit/push.
- [ ] **PUBLISH (7)** — Post review and inline comments per PR procedure.
      BLOCK maps to request-changes. Cleanup only after successful review post,
      only clean worktree, and only without `--keep-worktree`. Keep branch.
- [ ] **OUTPUT (8)** — PR title, decision, counts, validation, artifact path,
      GitHub URL and contextual next steps.

## Safety gates

- PR argument explicitly selects GitHub publishing; local/quick never do.
- Do not remove dirty worktrees or destroy source changes. Failed publish or
  failed commit/push leaves worktree available for recovery.
- PR worktree is snapshot of head at SETUP. New head commits require re-review.
- Large PRs (>50 files): warn; prioritize source, tests, then config/docs.
