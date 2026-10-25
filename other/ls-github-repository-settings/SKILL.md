---
name: ls-github-repository-settings
description: "Use when asked to enhance this GitHub repository or for requests such as audit registered GitHub controls, prepare this repository for public release, or apply repository best practices. Routes broad requests to LocalSetup's GitHub repository enhancement workflow."
metadata:
  version: "1.1"
---

# GitHub repository enhancement

Use [the GitHub repository enhancement workflow](../../workflows/ls-wf-github-repository-settings-audit/SKILL.md)
for the seven-group audit, plan, apply, and verify procedure. Its fixed
registry defines exact coverage for registered controls, not every possible
GitHub setting. The workflow owns fixed target identity, exact plan
authorization, capability and permission reporting, policy-scoped signature
and release proof, safe reconciliation, and the limited social-preview
handoff. Do not replace its typed CLI operations with ad hoc `gh api` requests
or browser automation.

Remote writes are currently enabled only on `github.com`; other GitHub hosts
support reads and audit, with requested drift reported incomplete while the
Enterprise Server API-version matrix remains unverified.

Repository alert counts are not read by default during audit, plan, or verify.
Add `--include-security-alerts` to those modes to request aggregate counts for
Dependabot, code scanning, and secret scanning. The option applies to the
current command only, does not expose alert details or establish health, and
is rejected for apply; a saved plan does not authorize a later alert read.

Release proof is optional and limited to identities explicitly selected by
policy. Use repeatable verify-only `--trusted-public-key FILE` arguments for
signature trust keys. If the policy has no verification requirements, release
readiness is `not_assessed`; settings apply completion does not establish
release readiness. Saved plans use schema v4 with schema-v2 policies;
regenerate old schema-v2 or schema-v3 saved plans from their reviewed policy.

Each planned operation displays its canonical interface descriptor in JSON
and Markdown, including transport, fixed command or method/endpoint template,
target binding, required flags, and any API selection reason. Use native
`gh repo edit` when its exact flags express the complete operation. LocalSetup
checks bounded command help for all required flags and fails closed if the
command or a flag is missing; it does not switch transports after a failure.
Ruleset mutations use the documented REST interface through `gh api` because
`gh ruleset` exposes listing, checking, and viewing, not writes. A matching
fresh social-preview Boolean can satisfy its selected presence/absence setting
when any selected local asset is still valid and bound; exact remote pixels
remain unverified.

Policy schema v2 supports `repository.web_commit_signoff_required: true|false`
for the `collaboration.web_commit_signoff` control. The official [`gh repo edit`
options](https://cli.github.com/manual/gh_repo_edit) do not document an exact
native flag, so the typed operation uses `PATCH /repos/{owner}/{repo}` through
`gh api` with `web_commit_signoff_required` in the request body and records
the REST-selection reason. See GitHub's [Update a repository
API](https://docs.github.com/en/rest/repos/repos#update-a-repository).

The workflow composes the existing GitHub publishing, LocalSetup safety,
documentation, testing, framework, Git, version, and release owners. Load and
follow those owners through its `required_skills` manifest when this workflow
is selected. Tracked content and releases remain on their normal local
validation and signed Git paths.
