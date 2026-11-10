---
name: github-pr-review-request
description: Use only when the user explicitly requests `github-pr-review-request`, or when `github-pr-codex-review-cycle` or `github-pr-publish-and-ai-review-request` delegates review requests for an explicitly user-requested workflow. Request Codex, Copilot, or both on an existing PR.
---

# GitHub PR Review Request

Request AI review on an existing PR. This skill does not publish PRs, apply
feedback, wait for review completion, or request human reviewers.

Delegated calls follow
[Delegated Authorization](../delivery-common/SKILL.md#delegated-authorization);
the exact target is the PR and the selected providers.

## Inputs

- PR number or same-repository URL; otherwise use the current branch's PR.
- Provider: `codex`, `copilot`, or `both`. Accept equivalent natural-language
  instructions. A composing skill must supply the provider explicitly. If the
  user and calling workflow do not specify a provider, ask before posting any
  request; do not silently request both.
- Optional review focus, passed to the provider procedure where supported.

## Workflow

1. Resolve the current GitHub repository and target PR once. Use
   `gh pr view --json number,url,state` for the current branch, or supply the
   requested PR. If no PR can be resolved, ask for its number or URL. Reject
   cross-repository targets.
2. Read and follow only the selected provider procedures:
   - `codex`: [Codex request and acknowledgement](references/codex.md).
   - `copilot`: [Copilot request and verification](references/copilot.md).
   - `both`: Copilot first, then Codex, using the same resolved repository/PR.
3. For `both`, continue to the other provider if one request fails unless
   authentication or repository access is completely blocked. Do not retry a
   successful request to recover a failure for the other provider.
4. Return the repository/PR URL, selected providers, and separate outcomes.
   Include the Codex trigger comment URL and acknowledgement state when selected;
   include the Copilot requested-reviewer verification when selected. State
   failures and unattempted providers explicitly. A posted or acknowledged
   request is not a completed review.

## Guardrails

- Perform only the requested providers' review requests under applicable approval
  rules. Do not commit, push, merge, edit repository files, or apply feedback.
- Keep provider-specific commands and success checks in the linked procedures.
- Report partial success without hiding failures or automatically repeating writes.
