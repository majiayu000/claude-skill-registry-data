---
name: ci-review
description: Proposes and sets up an AI review step on a repo's CI that reviews every PR/MR and checks, from the proof the PR/MR carries (screenshots, videos, network captures, test report), that what was delivered and tested really works, so the team stops reviewing by hand. Use when the user says "AI review on CI", "agent review in the pipeline", "review every PR automatically", "claude -p in CI", "set up claude-code-action", or when working in a repo whose CI has no such step and no answer is recorded for it.
---

# AI review with proof on CI

The idea: every PR/MR carries its proof (what the test-evidence skill produces: screenshots, a short video, the requests behind it, a test report). An agent on the CI reads the diff, the code around it and the proof, checks the code itself rather than trusting the tests or the screenshots, challenges what doesn't hold, and posts its verdict on the PR/MR. People read the verdict instead of the whole diff.

Templates are in the `templates/` folder of this skill's base directory (`~/.claude/skills/ci-review/` when installed by install.sh; `$SK` below is that `templates/` folder). The review instructions live in one file, `review-prompt.md`, that any agent CLI can take, so the same step works with another agent (Codex and others) by swapping the command.

## 1. Propose it once per repo

Answers are kept in `~/.claude-sync/ai-review.md` when the sync engine is installed, otherwise `~/.claude/ai-review.md`: one line per repo, `<host>/<owner>/<repo> | yes / no / later | YYYY-MM-DD | note`.

When a repo we work on has no AI review step on its CI and no line in that file, propose it once, in a few lines: what it does, what it costs (one agent run per PR push), what the repo needs (a secret). Say what you'd pick for this repo and why. Record the answer, whatever it is, and don't ask again for that repo.

## 2. Pick the route with the user

Look at the CI first (`.github/workflows/`, `.gitlab-ci.yml`, `azure-pipelines.yml`), then recommend one:

| CI | Route | Auth |
|---|---|---|
| GitHub Actions | `anthropics/claude-code-action@v1` with the official code-review plugin (`$SK/templates/github-action.yml`) | `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_API_KEY` secret, or Bedrock / Vertex through OIDC (`use_bedrock` / `use_vertex`) |
| GitHub Actions, with our verdict, proof policy and optional auto-approval | the CLI headless (`$SK/templates/github-cli.yml` + `review-prompt.md`) | `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_API_KEY` secret; the job's `GITHUB_TOKEN` posts the review |
| GitLab CI | the CLI headless (`$SK/templates/gitlab-ci.yml` + `review-prompt.md`), see code.claude.com/docs/en/gitlab-ci-cd (beta) | `ANTHROPIC_API_KEY` and a project access token `GITLAB_REVIEW_TOKEN` (api scope) as masked CI/CD variables |
| Azure Pipelines, others | the same CLI steps; no official guide, so test it on a throwaway branch first | the same key, plus a token that can comment on PRs |

On GitHub, offer "@claude" in PR comments alongside the review (`$SK/templates/github-mention.yml`): people ask it to explain, re-check or push a fix to the PR branch. It needs the same secret and the Claude GitHub App installed on the repo (a repo admin, from github.com/apps/claude).

The quickest GitHub setup is `/install-github-app` in an interactive session (repo admin and the `gh` CLI needed): it installs the GitHub App, stores the key as a secret and opens a PR with the workflow. Offer it when the user is at their terminal.

**Which credential.** A team on a Claude plan (Pro, Max, Team, Enterprise) can run the review on a seat: the seat holder runs `claude setup-token` and the repo admin stores the printed token as `CLAUDE_CODE_OAUTH_TOKEN`. It lasts a year, uses that person's plan limits, and stops when they lose the seat, so say whose seat it is and when it expires (a reminder a month before helps). An Anthropic Console key (`ANTHROPIC_API_KEY`) bills per token instead and suits a shared, long-lived setup; it wins when both are set. `--bare` (faster, ignores the repo's hooks and MCP servers) reads only `ANTHROPIC_API_KEY`: with a seat token, the CLI template drops it and deletes `.claude/` and `.mcp.json` from the checkout instead, since the PR branch could otherwise run its own hooks.

Never write a key into a file, a commit or the chat: the user adds secrets themselves in the CI settings, and you tell them the exact names. Only a repo admin can; when the user isn't one, name who has to do it.

## 3. Set it up

1. Copy the template into the repo and adapt it: branch filters, the review prompt's language (the repo's PR language), the CLI's `--max-turns`.
2. Keep `review-prompt.md` next to the workflow (`.github/ai-review/` or `ci/ai-review/`) and tune it to the project: its proof policy, what counts as proof here, which paths need extra care.
   - **Proof policy**: `required` (default) when the team attaches proof to its PRs (test-evidence); `optional` when it ships fast without acceptance criteria or proof: the verdict then rests on the code and the tests, and "Can't tell" is kept for what the reviewer really cannot see.
   - **Automatic approval** (GitHub CLI template, `AUTO_APPROVE: "true"`): the job approves on "Works", requests changes on "Doesn't work", withdraws its earlier review when the verdict changes, keeps it when the verdict holds, and never merges. The review itself lives in one comment per PR that every run edits (with or without auto-approval), so a push doesn't stack a new comment; an issue tied to specific lines also gets a line comment there, which the next run edits, or marks resolved (and resolves its thread) once it's fixed; a new review, one line linking to that comment, appears only when the bot's state changes. A repo admin must tick Settings › Actions › General › "Allow GitHub Actions to create and approve pull requests"; until then GitHub refuses the approval and the comment says so, with a warning naming that setting. Ask the user before turning it on: an approval from the bot may be all a merge needs, so when a person must still approve, the admin sets main's protection to one more approval than the bot gives (2: the bot and a person). The template reads the prompt from the default branch, approves only PRs into it, pins the approval to the reviewed commit, and never approves a PR that changes `.github/`, `CLAUDE.md`, `CLAUDE.local.md`, `.claude/` or `.mcp.json`, so a PR can't rewrite the rules it is judged by.
3. Open it as a PR (ask first, as for any PR). Its own run is the first test: check that the verdict comment appears and reads well. Permissions and comment posting are the part most likely to need a fix; read the job log if no comment shows up.
4. Record "yes" in the answers file, with the PR link.

## 4. What the review must say

The verdict, first line: works / doesn't work / can't tell. "Works" needs the code to do what the PR claims, read in context, with nothing that should block it; under the `required` proof policy the proof must show it too. Then, short: what was checked, what the code does that the tests (and the proof) don't cover, tests that would still pass with the change reverted, production risks (data shape, renamed fields older clients use, triggers, cost) and the risky spots. Under `required`, a PR without proof gets "can't tell" and a list of what to capture, not a guess. The CLI templates ask for the verdict as structured output (`--json-schema`), so the pipeline reads it instead of parsing the comment.
