---
name: pr-review
description: Request and manage pull request reviews using pr-agent (local CLI) with optional Claude second-pass. Use when needing to review a PR, check review comments, address feedback, or iterate on fixes. Triggers on "review pr", "request review", "check review comments", "review this", or "re-review".
---

# PR Review

Primary reviewer: `pr-agent` (Qodo Merge), installed locally via pipx.
Optional Claude second-pass for code PRs: `pr-review-toolkit:review-pr` (model-invocable). `code-review:code-review` is user-invocable only, so Claude cannot call it; the user can type `/code-review` themselves.

## Environment

pr-agent is configured entirely through **environment variables** — there is no user-global config file for the CLI (see [Notes](#notes)). Put this block in your shell rc (`~/.zshrc`) once, substituting your provider's endpoint, key var, and model:

```sh
export OPENAI__KEY="$YOUR_PROVIDER_KEY"
export OPENAI__API_BASE="https://your-endpoint/v1"   # your real endpoint URL — no angle brackets
export CONFIG__MODEL="<provider/model>"            # e.g. openai/<model-name>
export CONFIG__FALLBACK_MODELS='["<provider/fallback-model>"]'
export CONFIG__CUSTOM_MODEL_MAX_TOKENS=<tokens>    # required if model isn't in pr-agent's built-in list
export GITHUB__USER_TOKEN="$GITHUB_TOKEN"
```

- `SECTION__KEY` double-underscore is dynaconf's env convention (pr-agent sets `envvar_prefix=False`, so no prefix). These vars are read **only** by pr-agent — they don't collide with other tools' `OPENAI_API_KEY`/`OPENAI_API_BASE`. `OPENAI__*` here means the OpenAI-compatible interface, not the OpenAI service specifically — it works with any provider that exposes an OpenAI-compatible endpoint.
- `CONFIG__MODEL` overrides the default (`gpt-*`); prefix with the provider (`openai/`, `anthropic/`, …) to route a custom model to your `OPENAI__API_BASE`.
- Setting `OPENAI__API_BASE` pins all openai-provider calls to your endpoint, so a stray real `OPENAI_API_KEY` in the environment can never reach `api.openai.com` via pr-agent — no `unset` needed.

Project-level config lives in `.pr_agent.toml` (if present).

## Commands

All commands write to the PR under the user's GitHub identity. Confirm before running `review`, `improve`, or `describe` (which rewrites the PR title and body) on a PR the user didn't author.

In an interactive terminal the env block is already loaded, so just call `pr-agent`. Non-interactive callers (e.g. an agent's shell tool) that don't load your rc should load the env block first, for example by prepending `source ~/.zshrc;` to the command.

```sh
# Review — posts a top-level review comment (correctness, security, completeness)
pr-agent --pr_url <pr-url> review

# Improve — posts inline code suggestions
pr-agent --pr_url <pr-url> improve

# Describe — rewrites the PR title and description
pr-agent --pr_url <pr-url> describe

# Ask — ask a specific question about the PR
pr-agent --pr_url <pr-url> ask "<question>"
```

## Workflow

1. **Identify the PR**: `gh pr view <number>` to confirm scope, then grab the URL.
2. **Request pr-agent review**:
   ```sh
   pr-agent --pr_url <pr-url> review
   ```
   For inline suggestions, also run `improve`. The [Environment](#environment) vars must be loaded (see the non-interactive note under [Commands](#commands)).
3. **Optional Claude second-pass** (code PRs): invoke `pr-review-toolkit:review-pr`. Useful for a second-model perspective — pr-agent uses a different model by default, so Claude catches different patterns.
4. **Read the posted feedback** with the commands under [Checking Review Status](#checking-review-status).
5. **Address feedback** — fix code, commit, push.
6. **Reply to each thread** explaining what was fixed:
   ```sh
   gh api repos/OWNER/REPO/pulls/<PR_NUMBER>/comments/<COMMENT_ID>/replies \
     -X POST -f body="Fixed in <commit-sha>"
   ```
7. **Re-review** — repeat from step 2. Stop when a round produces no new actionable comments after the previous round's fixes landed. Keep going while rounds surface real findings.

### Round count guidance

- **1 round**: enough only when the first review finds nothing actionable.
- **2-3 rounds**: typical. A fix can introduce a new edge case the reviewer catches on re-pass, so the round after the last fix must come back clean.
- **4+ rounds**: expected for security issues, logic bugs, or when an earlier skip was later reversed.

### Deciding What to Address

- **Address immediately**: Security issues, bugs, missing error handling, secret leaks
- **Create issue for later**: Style preferences, nice-to-have refactors, doc suggestions
- **Skip with explanation**: Comments that don't apply to the project's context — reply on the thread so the rationale is on record. Be prepared for the reviewer to re-flag if the skip was wrong.

## Checking Review Status

```sh
# List open PRs
gh pr list

# View PR details + diff
gh pr view <number>
gh pr diff <number>

# Check existing reviews
gh pr view <number> --json reviews --jq '.reviews[] | {author: .author.login, state, submittedAt}'

# Check inline review comments
gh api repos/OWNER/REPO/pulls/<number>/comments \
  --jq '.[] | {id, path, line, user: .user.login, body}'
```

## Notes

- pr-agent is a **local CLI only** — there is no GitHub Action workflow firing on push.
- Install via `pipx install pr-agent`. **Do not edit the bundled `.secrets.toml` inside the pipx venv** — `pipx upgrade`/`reinstall` rebuilds the venv and wipes it. Configure via the env vars above instead (they live outside the venv and survive upgrades).
- **There is no user-global config file for the CLI** (no `~/.pr_agent.toml`). The org-level `pr-agent-settings` repo in the docs applies only to the hosted GitHub App. Environment variables are the only global mechanism.
- Project-specific guidance for pr-agent goes in the project's `.pr_agent.toml` (for example `extra_instructions`).
