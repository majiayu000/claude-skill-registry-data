---
name: github-as-code
description: "GitHub repositories, labels, rulesets, organisation secrets and GitHub Apps written as OpenTofu with the github provider, instead of changed by hand with gh or the web UI. Use when writing or reviewing OpenTofu that manages one of those, or when asked to change one of those by hand."
---

# github-as-code

Repository, label, ruleset and organisation secret settings for GitHub as OpenTofu.

## When to use

- Writing or changing OpenTofu that manages a repository, a label, a ruleset, a secret or an app.
- Bringing a repository, a label set or a ruleset created by hand under management.
- Renaming a label a skill matches on.
- Asked to change a repository, organisation or label setting by hand: refuse, propose OpenTofu.

## Rules

### Authentication

- `provider "github"` authenticates with an `app_auth` block or a `token`, never a literal
  credential in the configuration.
- Prefer `app_auth`: `id`, `installation_id` in the configuration, `pem_file` from secret manager.
- A `token` comes from the secret manager the same way, never typed into a variable default.
- `owner` is required on every provider block when authenticating with `app_auth`.

### Apps

- One GitHub App per purpose, named `<org>-<purpose>`, with the rights that purpose needs and
  nothing more, installed only on the repositories that need it.
- Purposes, write unless marked read: `infrastructure` (this provider: administration, issues
  for labels, secrets, variables), `release` (release-me or release-please: contents, pull
  requests, issues), `review` (agents' review identity: pull requests, issues, checks read,
  contents read), `dependencies` (self hosted Renovate: contents, pull requests, issues,
  workflows, checks read), `backup` (contents read), `queue` (contents, pull requests:
  workflows that push or open pull requests so that checks still trigger).
- Created in the web UI. App id and installation id are organisation variables, the private key
  an organisation secret, both managed here and read from the secret manager.
- Review and author are never the same identity. Implementation commits carry the person,
  never an app, so the review app can approve them.

### Aliases

- One `provider "github"` block per organisation this module manages.
- The default organisation's block carries no `alias` and is declared first.
- Every other block carries `alias = "<organisation>"`, declared after it, and its resources set
  `provider = github.<alias>`.

### Repositories

- Repositories of one organisation are one map variable, keyed by repository name, fed to
  `github_repository` with `for_each`; each value carries what varies: `visibility`, the label
  groups it opts into. Fixed for every repository: `allow_merge_commit = true`,
  `allow_squash_merge = false`, `allow_rebase_merge = false`, `delete_branch_on_merge = true`.
- Branch protection and required checks are ruleset input, not `github_repository` attributes.
- `lifecycle { prevent_destroy = true }` on every repository: removing a map key fails first.

### Labels

- The label catalog is a local map of named groups, each group a map of label name to color and
  description: `base`, `ai`, `priority`, `release`, `dependencies`, `community`, `stack`. Names
  for `ai`, `dependencies` and `priority` come from `~/.claude/skills/README.md` and the schema.
- `base` holds config `types`, `needs triage` (config `labels.needsTriage`), `duplicate`,
  `question`, and the context labels `breaking-change`, `deprecated`, `research`, `upstream`.
- `release` holds release-me's pending/tagged/alpha/beta/rc and release-please's pending/tagged.
- `community` holds `good first issue` and `help wanted` for public repositories, `stack` exactly
  the keys of config `stacks`.
- `github_issue_labels` is authoritative per repository, built from its chosen groups; an unlisted
  label is deleted on apply, so the catalog is a superset of every label any skill matches on.
- A rename drops the label from every issue: add the new name as its own entry, update every
  skill that reads the old name, then remove the old entry in a later commit.

### Rulesets

- `github_repository_ruleset`, never the legacy `github_branch_protection` resources.
- `enforcement` is required: `active`, `evaluate` (logs only, organisation repositories), `disabled`.
- `target = "branch"`, `conditions.ref_name` required with both `include` and `exclude`:
  `~DEFAULT_BRANCH` or an explicit ref in `include`, `exclude = []` as the default.
- `bypass_actors` typed by `actor_type` (`RepositoryRole` for the admin role, `Integration` for
  an app) and timed by `bypass_mode`: `pull_request` for a merge gate, `always` only for admins.
- Split a ruleset when a bypass should cover only part of its rules.

### Secrets

- Organisation secrets are `github_actions_organization_secret` with `value` or `value_encrypted`
  in `sensitive()`. `plaintext_value`, `encrypted_value` and `selected_repository_ids` are
  deprecated.
- `visibility = "selected"` plus `github_actions_organization_secret_repositories` scopes a
  secret to the repositories that need it. `all` only when every repository needs it.

### Membership

- Membership stays outside this code: no `github_membership` or `github_team_membership`.

### Import

- A repository, a label set or a ruleset created by hand is imported, never deleted and recreated:
  write the resource block to match the hand made state, add an `import` block with `to` and
  `id`, plan until the plan shows no change, then apply.
- `id` formats: `github_repository` and `github_issue_labels` take the repository name,
  `github_repository_ruleset` takes `<repository>:<ruleset_id>`, read from the GitHub UI or API.
- The import block stays in the configuration, it is inert once the state holds the resource.

## Guardrails

- Never change a repository, organisation or label setting with `gh` or the web UI: use OpenTofu.
- Never `github_branch_protection` or `github_branch_protection_v3`: rulesets replace both.
- Never a secret value as a literal, and never printed with `tofu output` or `tofu state show`.
- Never delete and recreate a resource that already exists by hand: import it.
- Never a label removed from the catalog while a skill still matches on its old name.

## Config

- `types` (default `bug`, `feature`, `improvement`, `documentation`, `security`): `base` types.
- `labels.needsTriage` (default `needs triage`): `base`. `labels.dependencies` (default
  `dependencies`): `dependencies`. `labels.ready` through `labels.blocked` (defaults in
  `~/.claude/skills/README.md`): `ai`.
- `priority` (default urgent, high, medium, low with the `priority:` prefix): `priority` group.
- `stacks` (default none): the `stack` group's names.

## References

- `opentofu-conventions` for file layout, state and the general provider rules.
- `tofu-plan` for reading the plan before an apply.
