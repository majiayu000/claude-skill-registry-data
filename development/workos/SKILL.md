---
name: workos
description: >-
  Use for WorkOS docs URLs, terms, dashboard fields (Sign-in endpoint, Redirect URI, `WORKOS_*`) and for implementing, debugging or migrating WorkOS: AuthKit, SSO, Directory Sync, RBAC, FGA, MFA, Vault, Audit Logs, Admin Portal, Pipes, Radar, `workos` CLI, Auth0/Clerk migration. Also @workos-inc/*.
---

# WorkOS Skill Router

## How to Use

**This file is a router, NOT the answer.** Before responding to the user:

1. Match the request to a reference file using Rule 0 and the rules below.
2. **You MUST Read the matched reference file with the Read tool before producing any answer, URL, or code.** If you have not Read a reference, you have not followed this skill.
3. Follow the instructions inside the reference (it will tell you which live docs to fetch with WebFetch and which gotchas to avoid).

**Exception**: Widget requests use the `workos-widgets` skill via the Skill tool, which has its own multi-framework orchestration.

## Guardrails (apply to every response)

The most common failure of past WorkOS agent interactions is plausibly-shaped fabrication of CLI commands and Dashboard paths.

- **Never invent `workos` CLI commands.** Verify the command tree first with `WORKOS_MODE=agent workos --help --json`. Do not assume a `create` subcommand exists because `list`/`get`/`delete` do. See `references/workos-management.md`.
- **Prefer `WORKOS_MODE=agent` when invoking the `workos` CLI from a coding-agent session.** Full rules, preflight and legacy flags: `references/workos-cli-agent-sessions.md`.
- **Never invent Dashboard click-paths.** Do not write "Dashboard > Organizations > X > Roles" or `dashboard.workos.com/some/path` unless verified against a docs page you just fetched. Cite the docs URL and describe the destination conceptually ("the Authorization page").
- **When the CLI does not support something, say so plainly** and give the docs URL. See the "Not in the CLI" section of `references/workos-management.md`.
- **Prefer docs URLs over prose.** When a reference tells you to cite a docs URL, cite it literally; do not paraphrase the slug.
- **Sandbox trust boundary.** If `workos doctor` reports `HOST_EXECUTION_UNTRUSTED` (or `hostExecution.ok` is `false`), the shell may be sandboxed: auth, config and keychain failures are not authoritative. Ask the user to re-run host-sensitive commands on their host shell. Preflight: `WORKOS_MODE=agent workos doctor --json --skip-ai`.
- **Destructive CLI commands in agent mode need the explicit flag** (`--yes` for `workos api` mutations, `--force` for `connection delete`, `directory delete`, `debug reset`), otherwise `confirmation_required`.

## Topic → Reference Map

All files are `references/<name>.md`. Terminology lookups ("what is X", "docs URL for X") go to Rule 0, not this map.

- **AuthKit install**: `workos-authkit-nextjs`, `-react`, `-react-router`, `-tanstack-start`, `-sveltekit`, `-vanilla-js`; architecture: `workos-authkit-base`. Verify tokens in a custom backend (Convex `auth.config.ts`, any JWKS verifier) or debug a login loop, CORS on `user_management/authenticate`, "No auth provider found", 403 after sign-in: `workos-authkit-jwt-custom-backend`. Widgets: `workos-widgets` skill.
- **Backend SDKs**: `workos-node`, `-python`, `-dotnet`, `-go`, `-ruby`, `-php`, `-php-laravel`, `-kotlin`, `-elixir`.
- **Features**: `workos-sso`, `-directory-sync`, `-rbac`, `-fga`, `-vault`, `-events` (webhooks), `-audit-logs`, `-admin-portal`, `-mfa`, `-email`, `-custom-domains`, `-integrations` (IdP setup), `-pipes` (Connected Apps), `-feature-flags`, `-radar`.
- **API only** (no feature topic): `workos-api-authkit`, `workos-api-organization`.
- **Migrations**: `workos-migrate-auth0`, `-aws-cognito`, `-better-auth`, `-clerk`, `-descope`, `-firebase`, `-stytch`, `-supabase-auth`, `-the-standalone-sso-api`, `-other-services`.
- **CLI**: `workos-management` (manage resources), `workos-cli-upgrade` (outdated CLI), `workos-cli-agent-sessions` (agent/sandbox sessions).
- **Terms**: `workos-terms`.

## Routing Rules (first match wins)

Full text, AuthKit framework/language detection order and edge cases: `references/workos-routing-details.md`. Read it when a request is ambiguous or spans several features.

0. **Terminology / docs URL lookup** ("what is X", "docs URL for X", dashboard field, `WORKOS_*`): Read `references/workos-terms.md`. If the term is missing, follow its "Still not here?" fallback and suggest a PR adding the row. Do NOT WebFetch `llms.txt` or guess `workos.com/docs/...` URLs first. Not for setup phrasing ("set up Vault"), which is Rule 3.
1. **Migration FROM a provider**: `workos-migrate-<provider>`, else `workos-migrate-other-services`.
2. **API reference request**: the feature topic file (it has an endpoint table); AuthKit or Organization APIs use `workos-api-<domain>`.
3. **Named feature** (SSO, MFA, Directory Sync, Audit Logs, Vault, RBAC, FGA, Admin Portal, Custom Domains, Events, Integrations, Email, Pipes, Feature Flags, Radar): `workos-<feature>`. Several features: most specific first. "FGA" or "fine-grained" goes to `workos-fga`, never `workos-rbac`. IdP group to role mapping (Entra, Okta, Google Workspace, SCIM): read `workos-rbac` AND `workos-directory-sync` (directory groups) or `workos-sso` (SSO-only groups). It is not a CLI operation; do not paraphrase dashboard paths.
4. **AuthKit install** (login, sign-up, sessions, "AuthKit" with no feature): detect framework or language in the priority order of `workos-routing-details`. Conflicting signals or unknown framework: ASK, never guess.
5. **IdP / third-party integration setup**: `workos-integrations`. "Google SSO" or "Okta SSO" goes to `workos-sso`.
6. **Managing resources / seeding / CLI**: `workos-management`. Outdated CLI (`unknown command`, old `workos --version`): `workos-cli-upgrade`; never guess the latest version, tell the user to run `npm view workos version`.
7. **Vague request** ("help with WorkOS"): WebFetch https://workos.com/docs/llms.txt, pick the matching section, WebFetch it, summarize and ASK what the user wants. Do NOT guess a feature.
8. **No match**: WebFetch llms.txt and search it. If nothing matches, say you could not find a WorkOS feature for the term and ask for clarification.
