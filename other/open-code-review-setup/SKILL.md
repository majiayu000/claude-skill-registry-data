---
name: open-code-review-setup
description: Set up Alibaba Open Code Review (OCR) on a repository that lacks it, or audit and update an existing setup. Use when creating a new repository, onboarding an existing repo to automated AI code review, configuring `.opencodereview/rule.json` or the OCR GitHub Actions workflows, or when OCR reviews are not running on PRs.
---

# Open Code Review Setup

Lifecycle operation: detect → install → configure → verify. For PR metadata, agent labels, and the token-spend semantics of `rule.json`, use `ai-agent-pr-metadata` — this skill only installs and validates the plumbing.

## 1. Detect

```sh
ls .opencodereview/ .github/workflows/ 2>/dev/null | grep -i -E 'ocr|open-code-review'
gh variable list --repo <owner>/<repo> | grep OCR_
gh secret list  --repo <owner>/<repo> | grep OCR_LLM_AUTH_TOKEN
```

- All present → audit only: confirm the action is pinned to a SHA, the maintainer gate matches the repo owner, and the model var is still wanted. Do not clobber local customizations.
- Anything missing → install/configure the missing pieces below.

## 2. Install

Branch per git workflow (`feature/issue-N-open-code-review`, PR to the default integration branch — never commit to `main`/`staging` directly).

1. Copy `templates/open-code-review.yml` and `templates/ocr-manual-review.yml` into `.github/workflows/`.
2. Set the maintainer gate in both files (`github.event.pull_request.user.login == '<maintainer>'` / `github.event.comment.user.login == '<maintainer>'`) to the account that opens PRs (the bot account whose token creates PRs, if agents open them).
3. Copy `templates/rule.json` to `.opencodereview/rule.json` and adapt `exclude` to the stack:
   - JS/TS: `node_modules/**`, `dist/**`, `pnpm-lock.yaml`, `package-lock.json`
   - PHP/Laravel: `vendor/**`, `storage/**`, decide explicitly on `tests/**` (built-in excludes do not cover `*Test.php`)
   - Static/binary assets (images, fonts, brand files): exclude their directories
   - Keep `**/*.md`, `**/*.json`, `**/*.lock` unless docs/schema review is wanted
4. Pin `alibaba/open-code-review` to the current release SHA (never a floating tag).

## 3. Configure

Repo variables (non-secret):

```sh
gh variable set OCR_LLM_URL              --repo <owner>/<repo> --body "https://openrouter.ai/api/v1"
gh variable set OCR_LLM_MODEL_FREE       --repo <owner>/<repo> --body "nvidia/nemotron-3-super-120b-a12b:free"
gh variable set OCR_LLM_MODEL_FALLBACK   --repo <owner>/<repo> --body "<paid-model-id>"
gh variable set OCR_USE_ANTHROPIC        --repo <owner>/<repo> --body "false"
```

- Default free model: `nvidia/nemotron-3-super-120b-a12b:free` (OpenRouter free tier, 262k ctx). Override per repo only when asked; verify any model ID against `https://openrouter.ai/api/v1/models` first.
- Fallback model: use a known-working paid model already proven for this deployment context if one exists, otherwise a cheap general-purpose paid model — verify against `https://openrouter.ai/api/v1/models` first, same as the free model. The preflight probes `OCR_LLM_MODEL_FREE` first and falls back to `OCR_LLM_MODEL_FALLBACK` on any non-2xx response (quota exhaustion, outage, etc.).
- Secret: `OCR_LLM_AUTH_TOKEN` = OpenRouter key. Pipe it from the local secrets store straight into `gh secret set` — never print, log, or commit the value:

```sh
grep -m1 '^OPENROUTER_API_KEY=' <env-file> | cut -d= -f2- | tr -d '\r' | gh secret set OCR_LLM_AUTH_TOKEN --repo <owner>/<repo>
```

- No key available, or preflight returns 401 → stop and use `hitl-blocker`; do not retry automation.

## 4. Verify

1. Open the setup PR. The `pull_request` trigger runs the workflow from the PR head, so the PR reviews itself — watch `gh run list`.
2. Preflight must pass (HTTP 2xx). 401 = bad key (→ step 3 HITL); other codes = check `OCR_LLM_URL`/model ID.
3. Confirm the review comment lands on the PR and ends with the `Review metadata` footer per `ai-agent-pr-metadata`.
4. Compare `tool_calls`/`input_tokens` in the workflow log's `=== OCR result ===` block after tuning `rule.json` to confirm spend dropped.
5. `ocr rules check --rule .opencodereview/rule.json <path>` verifies a path matches before relying on it (no LLM call).
6. Confirm both probe branches are exercised at least once: the free-model probe should succeed under normal conditions; to test the fallback branch deliberately, temporarily set `OCR_LLM_MODEL_FREE` to an invalid model ID via `gh variable set` in a throwaway test, confirm the workflow logs "Free model unavailable ... falling back to paid model", then revert the variable to its real value.
7. The preflight probe only proves the model is reachable (1-token reply) — it does not prove a real review will finish within `llm_timeout`. A free-tier model can pass the probe and still time out mid-review on a large diff, and since fallback only triggers on a failed probe (not a failed review), a slow-but-reachable free model gets no fallback. `llm_timeout: '300'` is the template default and a starting point, not a guarantee — raise it further per repo if reviews are timing out on large diffs.

## Guardrails

- Never print, commit, or comment secret values; public artifacts must use `Credential details: [redacted]`.
- The manual `/ocr-review` workflow must stay gated to the maintainer — an open comment trigger lets anyone spend LLM budget.
- Never check out or execute PR-supplied code in OCR workflows; the action diffs content remotely.
- Existing `rule.json` exclusions are deliberate cost controls — treat removals as spend increases, not cleanups.
