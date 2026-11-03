---
name: dx-lifecycle-center
description: "Lifecycle Center for DX Inspector and Builder Central. Use this skill first for four jobs: (A) list the orgs connected to DX Inspector; (B) connect a new org (sandbox or scratch, production, OrgFarm) as a deploy target; (C) connect or check the Lifecycle Center org, also written LifecycleCenter org, lifecycle-center, ALMDevOpsCenterHub, DevOps Center hub, or Hub org; (D) deploy, validate, or quick-deploy components that already exist in the user's org to a connected org, and poll a simple-deploy requestId. TRIGGER on: show, list, or pick connected orgs or environments; connect, add, log in to, or repair an org; connect the Lifecycle Center org; deploy, validate, or push components to another org, URL, org id, alias, or environment name. Short asks like \"connect a new org\", \"which orgs can I deploy to\", or \"deploy to my sandbox\" match. These deploys move components from the connected source org to another org, not local project files."
metadata:
  version: "1.0"
  domains: ["Developer Experience"]
  minApiVersion: "67.0"
  cliTools:
    - tool: ["jq"]
      semver: ">=1.6"
    - tool: ["sf"]
      semver: ">=2.67.0"
---

# Lifecycle Center: Connect Orgs and Deploy Metadata

This skill manages which orgs a user can deploy to, and deploys to them. Everything runs from the **source org**: the org the user built in, where DX Inspector runs. All connections and environments are stored there.

## Operations

| Op | Name | What it does | Details |
|---|---|---|---|
| **A** | List orgs | Shows the orgs connected to DX Inspector (the deploy targets), or the current org's details. Also resolves a target the user names. | `references/list-orgs.md` |
| **B** | Connect an org | Connects a new sandbox or scratch, production, or OrgFarm org as a deploy target, or repairs a half-finished connection. The user signs in through a link. | `references/connect-org.md` |
| **C** | Lifecycle Center org | Connects, repairs, or checks the Lifecycle Center org (credential `ALMDevOpsCenterHub`). | `references/hub-org.md` |
| **D** | Deploy | Deploys, validates, or quick-deploys components from the source org to a connected target, then polls to the end. | `references/deploy.md` |

Connect (B) and deploy or quick deploy (D) change an org, so they wait for the user's confirmation first. Listing, status checks, validate runs, and polling do not change a target org.

## Key terms

| Term | Meaning |
|---|---|
| Source org | The org the user built in. Use the alias they name, else the default org from `sf org display --json`. Components must already exist in it. |
| DX Inspector environment | A `DevopsEnvironment` record in the source org with a Named Credential. The deploy targets are exactly these records. |
| Deploy target | An environment in state `selectable`. An `expired` or `unauthenticated` environment is not a target. |
| Lifecycle Center org | The Lifecycle Center hub. A separate connection that is never a deploy target. |

## Routing (deterministic)

Scripts, references, and assets are paths inside this skill's folder, `<skill_dir>`: the location given for this skill when it was listed or loaded, without the trailing `/SKILL.md`. Run every script as `bash <skill_dir>/scripts/<script>` from the current folder. Do not `cd` first (the current folder sets the default org for `sf`), and never guess another folder or search the filesystem for the skill. This skill owns every request below. Pick the operation by these rules **in order; the first match wins**. Do not hand these requests to another skill, and do not answer them from general knowledge.

| # | The request | Operation |
|---|---|---|
| 1 | Names the Lifecycle Center org, in any request, however it is spelled: "Lifecycle Center", "lifecyclecenter", "lifecycle-center", "lifecycle_center" (matching rules in `references/hub-org.md`) | **C** |
| 2 | Deploy, validate, quick deploy, or push components to an org, URL, org id, alias, or environment name; or gives a `requestId` or validation id | **D** |
| 3 | Show, list, or pick connected orgs or environments; "which orgs can I deploy to"; the current org's details | **A** |
| 4 | Connect, add, log in to, reconnect, or repair an org or its credential | **B** |
| 5 | Anything else about connected orgs or DX Inspector environments | **A** |

The Lifecycle Center org rule (1) has two exclusions: "Dev Hub" is never the Lifecycle Center org, and plural phrases such as "DevOps Center orgs", "DX Inspector orgs", "environments", or "orgs connected to DX Inspector" are not the Lifecycle Center org; route them by rules 2 to 5. Details: `references/hub-org.md`.

**Reading the wording.** Before applying the rules, normalize the request: lowercase it, treat hyphens, underscores, and extra spaces as single spaces, and ignore punctuation, one-letter typos in words of five or more letters, and filler such as "please", "can you", "I want to". (Rule 1 also uses the two forms described in `references/hub-org.md`.) Then match on any word in the groups below; the exact phrase does not matter.

| Operation | Action words (any form: "deploy", "deploying", "deployment") | Object words |
|---|---|---|
| **D** | deploy, deployment, validate, validation, check only, dry run, quick deploy, quickdeploy, push, send, ship, move, copy, release, add or install (when the object is a component) | components, metadata, classes, flows, objects, or a named org as the destination ("to", "into", "onto") |
| **B** | connect, connection, add, link, hook up, hookup, authorize, authenticate, log in, login, sign in, set up, setup, register, onboard, reconnect, repair, fix, refresh | org, environment, env, sandbox, scratch, production, prod, orgfarm, org farm |
| **A** | show, list, see, view, display, which, what, pick, choose, available | orgs, environments, envs, targets, connections, "where can I deploy" |

A request with a **D** action word and a destination, or that names a component and a destination whatever the verb ("add AccountService to my QA sandbox"), is **D**, even when it also contains a **B** word. A **B** action word whose object is an org or environment makes the request **B**, even when words like "connected" or "linked" also appear ("reconnect my sandbox, it shows not connected"). A request with only **B** words is **B**. A request with only **A** words, or a question about what is connected, is **A**. A bare `requestId` or "status of my deploy" is **D**. If no group matches, use the vague-prompt table below.

A request that mixes jobs (for example "connect my sandbox and deploy AccountService to it") takes the lowest-numbered match, here **D**, which runs **B** itself when the target is not connected.

**Vague prompts.** If the message is only "deploy", "push my changes", "connect an org", or similar, do not guess and do not call any API. Ask exactly one question that fixes the first missing input:

| Intent | Ask, in this order |
|---|---|
| Deploy | 1. Which components? (`references/deploy.md`, Step 1) 2. Which target org? |
| Connect | 1. "Is it a sandbox or scratch org, a production org, or an OrgFarm org?" 2. What short name (letters only) should the environment have? |
| Not clear which | "Do you want to connect an org or deploy components?" |

A bare "deploy" with no DX Inspector context is a question, not a deploy.

## Rules that always apply

- Targets come from the DX Inspector environments in the source org, never from `sf org list` or local aliases.
- Never deploy to a target that is not `selectable`, never to the source org, and never to the Lifecycle Center org.
- The Lifecycle Center org never appears in a list and is not mentioned while listing. It is discussed only when the user asks about it.
- Confirm before every call that changes an org: connect (`connect-org.md`, Step 1) and deploy (`deploy.md`, Step 4). `validate` is the only mode that needs no confirmation.
- When a connect started from a deploy and finishes, tell the user the org is connected and that you are continuing the deploy, then ask for the deploy confirmation. Connecting never deploys by itself.
- A sandbox and a scratch org are the same type (`SANDBOX`). Treat their URLs alike.
- Make one attempt per API call. Never retry in a loop, resubmit after a timeout, or invent an id, credential name, or status.
- Never ask for, print, or pass an access token. Never show row ids or credential names.
- Never say a browser was opened. Give the login link and wait for the user to reply **done**.
- Pass `render_widget` only a `CARD_JSON` line that `scripts/widget.sh` printed, exactly as printed. Never write, invent, or edit a card.
- Do not guess a missing input. Ask one question for the first missing input.
- Ask the user to confirm an org type that the URL host does not decide. Never infer it from an environment name.

## What the user sees

| After | Reply with |
|---|---|
| **A** list | Only the table and the closing sentence (`list-orgs.md`, section 4). No raw JSON, no extra offers. |
| **A** not enabled | The one-sentence message in `list-orgs.md`, section 2. Nothing else. |
| **B** connect | The sign-in layout with a button-style link (`connect-org.md`, Step 2), then after **done** the connected layout: environment name, org host, type, and status (`connect-org.md`, Step 5). |
| **C** | The exact sentences in `hub-org.md`. When connecting, the same sign-in and connected layouts as B, in hub form, or the sign-in and connected cards when the `render_widget` tool is available (`connect-org.md`, Steps 2 and 5). |
| **D** | A plain-language report: what was deployed, from where, to where, and the outcome (`deploy.md`, Step 7). No raw JSON. If the deploy is still running after about 2 minutes: the `requestId`, a note that it is in progress, and a request to send the id back to get the status (`deploy.md`, Step 6). |

## If something fails

| Failure | Where to look |
|---|---|
| The list or target lookup fails | `references/list-orgs.md`, section 2 |
| A connect step fails | `references/troubleshooting.md` |
| A deploy or validate fails | `references/error-handling.md` |
| The target login is stale | Reconnect that environment (`references/connect-org.md`, repair path), then ask before retrying |

## References

- `references/list-orgs.md`: Operation A. The resolver script, match statuses, the list table, and the not-enabled handling.
- `references/connect-org.md`: Operation B. Modes, Steps 0 to 5, and rules for connecting an org.
- `references/hub-org.md`: Operation C. The Lifecycle Center org: hub names, replies, and rules.
- `references/deploy.md`: Operation D. Steps 1 to 7 for deploy, validate, quick deploy, and polling.
- `references/request-body.md`: deploy, validate, and quick-deploy request bodies and test levels.
- `references/connect-api.md`: Environment API and `setupNamedCredential` request and response shapes, status checks.
- `references/troubleshooting.md`: connect error codes and recovery.
- `references/error-handling.md`: deploy error codes.
- `examples/workflows.md`: worked prompts for each operation.
- `scripts/resolve-environment.sh`: read-only list and identifier resolver.
- `scripts/poll-deploy-status.sh`: read-only status poller. Reads the Simple Deploy endpoint and `DevopsRequestInfo`, and reports component errors on failure.
- `scripts/widget.sh`: Operation C, Steps 2 and 5, only when the `render_widget` tool is available. Fills a card from `assets/widgets/` with `scripts/fill-widget.jq`, checks it with `scripts/card-policy.jq`, and prints `CARD_JSON <json>` or `CARD_UNAVAILABLE <reason>`. Makes no API call.
- `assets/widgets/<name>/`: the HXL chat cards (`connect-sign-in`, `connect-connected`), each a tile tree `<name>.json` and the `schema.json` of its values.
