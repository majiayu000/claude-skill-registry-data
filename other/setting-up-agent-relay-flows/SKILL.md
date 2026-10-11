---
name: setting-up-agent-relay-flows
description: Set up and activate an Agent Relay Flow end-to-end from a running agent session through the Cloud APIs, with no dashboard clicks - choose a catalog flow and repository, connect the GitHub (or other trigger) tools and any coding-agent credentials, activate the listener through the direct-source deploy API, and verify it is listening. Use when a human asks an agent to set up Flows, activate a recommended flow such as Software Garden on a repository, or finish Flows onboarding.
---

# Set Up Agent Relay Flows

Drive the setup through the documented Cloud APIs and the official CLI. Do not
use computer use, browser automation, or the dashboard UI. The human approves
sign-in, tool consent, and provider logins on their own approval pages; open
those links with the OS URL opener (or give them the link), then verify by
polling the API, never by inspecting the browser.

Paths below are relative to the Cloud API base, `https://agentrelay.com/cloud`,
including its `/cloud` prefix; the site is `https://agentrelay.com`. The flow
catalog is the one exception: it is a site API, served from the site origin
without `/cloud` (`https://agentrelay.com/api/v1/flows/catalog`). When a
guide names a different site and Cloud base (for example a local development
stack), use those exact origins throughout, including for the catalog, the
CLI's `--api-url` and the dashboard links, and never fall back to production.
Flows can be configured from any machine with HTTPS and Node.js 22+ for the CLI.

## Requires

A signed-in Cloud session: an access token and the `user.id` and
`currentWorkspace.id` from whoami. Get them with `signing-in-to-agent-relay-cloud`
first. Send `Authorization: Bearer <access_token>` only to the Cloud API
endpoints below. Never send it to the site's flow catalog or to a catalog
`source.rawUrl`; fetch those without credentials.

## API map

- Flow catalog (site origin, not under `/cloud`):
  `GET https://agentrelay.com/api/v1/flows/catalog` and `/<id>`.
- Tool consent links: `POST /api/v1/integrations/connect-link`; poll
  `GET /api/v1/workspaces/<workspaceId>/integrations/<provider>/status`.
- Coding-agent credentials: the official CLI's `cloud connect` (section 3);
  `GET /api/v1/cloud-agents` inspects existing connections.
- Activation: `POST /api/v1/flows/deploy` with the body in section 4.
- Custom-flow prompt generator (optional): `GET /api/v1/flows/prompt/generate`
  reports whether it is available.
- Verification: `GET /api/v1/flows/listeners/<agentId>`.

## 1. Prebuilt or custom?

Ask the human first, unless their request already says: a **prebuilt** flow
from the Agent Relay catalogue (https://agentrelay.com/flows), or a **custom**
flow of their own? In an agent-driven signup, ask through that guide's
web-input protocol on the signup page, not in chat.

- Prebuilt: continue with section 2.
- Custom: follow **Custom flow: deploy journey** below. A custom flow is
  activated by the same `POST /api/v1/flows/deploy` API as a prebuilt one and
  as the deploy builder at https://agentrelay.com/cloud/flows/deploy; there is
  no separate custom API.

## 2. Choose the flow and repository

Ask the human for missing product choices: repository, desired
workflow/trigger, and approver. In an agent-driven signup, ask through that
guide's web-input protocol on the signup page, not in chat. Ask for the approver's
GitHub username in plain language (for example, "octocat" or "@octocat"),
not an internal provider-address format or their Google email. Normalize the
answer to github:@handle when constructing the deploy API request. Human-gate
replies are matched to that provider identity. Infer choices from the user's request and current
repository where clear.
Do not invent a repository or enable automation on an unrelated project.

GET https://agentrelay.com/api/v1/flows/catalog and select a matching entry from flows.
GET https://agentrelay.com/api/v1/flows/catalog/<id> for its full contract. Use the catalog's
kind before doing anything executable: only an entry with kind: flow (or a
legacy entry with kind omitted) is deployable through the direct-source API
below. An entry with kind: extension is discoverable metadata, not a standalone
listener. Do not download or deploy its source, even when it declares trigger
and input fields. Inspect baseFlowId and extension.activation instead. If the
extension is blocked, report the unmet dependencies and that it can only be
added to its base flow after a supported extension activation path is available;
never substitute a standalone flow deployment.

For a deployable flow, use the catalog's
supportedRepositoryHosts, defaultTrigger, inputs.required, inputs.defaults, and
inputs.allowedAgents. Name a model per harness in inputs.models when the house
default is wrong (for example {"claude": "claude-sonnet-4"}); omit it to fund
the house default for each declared agent. Download source.rawUrl, verify its bytes against
source.sha256, and use that source text unchanged for a recommended flow.
The source is TypeScript, not the source URL. Do not guess a template or hash.

## Custom flow: deploy journey

There is no journey API. A `journey_id` (for example in a
`next=/flows/deploy?journey_id=...` link) is only an analytics tag: pass it
through unchanged where you received it, and never call an endpoint with it or
wait on it. A custom flow is activated by the same `POST /api/v1/flows/deploy`
as a prebuilt one; only where the source comes from differs.

1. Author the flow with `writing-relayflows` (the Relayflows v2 engine,
   `@relayflows/surface` / `@relayflows/sdk`, CLI `flows`). Defer to that
   skill for the flow's shape and checks; Flows are always v2. Cloud's
   prompt generator is an optional shortcut: use it only when
   `GET /api/v1/flows/prompt/generate` returns `available: true`. If it
   reports unavailable, refuses your session (403 `session_required`), or
   fails, author with `writing-relayflows` instead; do not retry into it.
2. Choose its repository, trigger and approver as in section 2.
3. Continue with sections 3 to 5 unchanged. In section 4, `source` is the
   custom TypeScript text, `workflow` is its label, and `promptSpec` is sent
   only when the prompt generator produced one. `base` and `extensions` are
   optional and only for a flow that names them.

The human-only steps are the same for both paths: Google sign-in and device
approval, GitHub and trigger-app OAuth including the repository grants,
model-provider login when section 3 calls for one (not for an ordinary first
activation), and confirming the repository and trigger before activation. Do every other step yourself through the APIs.

## 3. Connect the required tools and coding agents

Use bearer-authenticated POST /api/v1/integrations/connect-link:

```json
{"provider":"github","workspaceId":"<currentWorkspace.id>"}
```

Open the returned connectUrl for the user to approve. Keep token/sessionToken
private. Connect only the repository and tools the chosen flow requires.
For GitHub the user must grant repository access. Repeat with the chosen trigger
provider if different. Reuse existing ready connections rather than relinking.
Check GET /api/v1/workspaces/<workspaceId>/integrations/<provider>/status
until oauth.connected is true (poll with backoff and a bounded timeout); a
returned connect link or a closed popup alone does not prove the connection.
For the GitHub-triggered Software Garden flow, activation separately checks
that the connected GitHub App covers the selected repository. Its trigger
does not require background data indexing, so do not block solely because
the broader status.ready is false from queued syncs.
If a different flow declares Relayfile data that requires synced records,
verify that readiness separately before activating it.

Do not connect a Claude or Codex subscription yet. The first three runs use
Cloud's own model key, so no provider login is needed to activate. If the chosen
flow declares more than one coding agent (the catalog's `inputs.defaults.agents`,
which becomes `inputs.agents` in the deploy body), included Cloud runs
can fund only one of them per run — connect your own subscription for at least
one declared agent before activating a multi-agent flow. After the included
runs, activation and launches will ask for your own subscription; only then use
the official Relay CLI with the private credential environment from
`signing-in-to-agent-relay-cloud` (its section 5) and a PTY:

This promotion depends on Cloud's internal house-key proxy and account
enrollment. If local activation returns flow_credentials_unavailable or
flow_model_not_connected before the three promotional runs, treat it as an
internal configuration or eligibility issue. Do not ask the user to connect
Claude/Codex, provide an API key, or choose an inactive draft as a workaround.
Report the blocker (in a signup, through its Progress API) and have an internal developer
verify the proxy, promotion flag, provider readiness, and enrollment. Never
copy a house key into the agent environment or expose it in this guide.

```sh
npx --yes agent-relay@13 cloud connect anthropic --api-url 'https://agentrelay.com/cloud'
```

Use anthropic for Claude or openai for Codex, according to the selected flow.
The command drives provider login; open its authorization URL for the user,
and keep the process alive until it confirms the credential is connected.
Google approval does not grant GitHub or model-provider access: those services
may require their own consent. Never fabricate credentials or claim consent
happened. GET /api/v1/cloud-agents lets you inspect the account's credential
state without reconnecting.

## 4. Activate through the same API as web onboarding

POST /api/v1/flows/deploy with Content-Type: application/json and the bearer
session. The token must be the device-flow session from
`signing-in-to-agent-relay-cloud` (scope `cli:auth`) or a token with
`flows:listeners:write`, and `workspaceId` must be that token's workspace. This is the direct-source listener API used by flows deploy, not the
browser onboarding handoff: source is TypeScript text, repository is singular,
and sources contains provider/settings objects. The catalog supplies the source
reference and defaults; it is not itself a deploy request. The current endpoint
does not accept a flowId/repositories-only catalog activation request or fetch
the source for you. For multiple repositories, submit one deployment per
repository with a distinct name and handoffId.

For the catalog's Software Garden entry (id `software-factory`), construct this body, substituting the
workspace, verified source, repository, GitHub approver and a new UUID:

```json
{
  "workspaceId": "<currentWorkspace.id>",
  "name": "Software Garden",
  "workflow": "software-factory",
  "source": "<verified TypeScript source text>",
  "handoffId": "<one UUID generated for this setup>",
  "inputs": {"approver": "github:@octocat", "agents": ["claude"]},
  "mode": "activate",
  "repository": {"owner": "acme", "name": "api"},
  "sources": [{"provider": "github", "settings": {"repository": "acme/api"}}]
}
```

For another deployable kind: flow catalog entry use its id as workflow, allowed agents, and
defaultTrigger for sources, then apply the user's trigger settings. Scope a
GitHub issue trigger with settings.repository set to the chosen owner/name;
for GitLab use settings.project. Cloud does not derive this filter from the
deployment repository. An empty filter can trigger on other repositories in
the workspace. Only use a different trigger scope when explicitly requested.
Give each repository its own trigger filter for multi-repository setup. Do not send
the example acme repository or octocat approver unchanged. The workflow field
is a label, not a source lookup; keep the verified source in the request.
For GitLab set repository.host to gitlab and use the namespace path
as owner. Reuse the handoffId on retry. Before retrying an ambiguous network
failure, GET /api/v1/flows/listeners and check whether the flow already exists;
do not create a new ID/name on every retry. Activation subscribes to matching
future events and can run work; confirm the intended repository and trigger
with the user if they have not specified them.

HTTP 201 must contain agentId and status: listening. A draft is not completion.
For a 409 workspace_mismatch, verify the active workspace; for connection
preflight failures, fix the indicated connection before retrying. If the user
wants to save incomplete work, use mode: draft explicitly and report that it
is inactive. Never mask activation failures by silently falling back to draft.

## 5. Verify

GET /api/v1/flows/listeners/<agentId>. Require listener.status: listening and
verify its repository and sources match the request. Open
https://agentrelay.com/cloud/dashboard/workflows/listeners/<agentId> for the user. Report the flow name,
workspace, repository, trigger, and verified listening state. This proves
activation; only an actual completed run proves execution. Do not create a
real issue or launch paid work merely to make the onboarding check turn green.
Delete temporary authentication files after the work is complete.

The desktop app is optional for Flows. If the user also wants local session
sharing, use `setting-up-agent-relay-desktop` and `setting-up-agent-relay-sessions`
with the same account (an agent-driven signup can follow
https://agentrelay.com/signup/agent/teams).
