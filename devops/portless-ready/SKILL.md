---
name: portless-ready
description: Use when a stack has to go portless, makes a project compatible with the market portless tool (named HTTPS route, published backing ports switched off, frontend↔backend URLs aligned).
---

# portless-ready

**Setup / infra** block (not a pipeline step). Makes a Docker stack usable through **the market
portless tool**: one stable HTTPS URL per service, zero port collision, Windows browser → WSL
container. This is "the agent that fixes things so portless gets used every time".

## When
On demand, before testing a stack in the browser, or while migrating a project to portless.

## Steps
1. **Check portless is installed** (CA trusted in WSL *and* Windows). Otherwise: ask the dev to run
   the installation: it's a **system change** (CA in the Windows Root store), the agent doesn't do
   it.
2. **Identify the HTTP entry points** to expose (app, frontend, vite, mailpit) and their real port.
3. **Route**: `portless alias <project>-<role> <port>` → `https://<project>-<role>.localhost`
   (worktrees prefix the branch automatically).
4. **Compose hygiene** (proposed, **ratified by the dev**: it touches the real compose file): the
   *backing* services (db, redis, elasticsearch) **no longer publish on the host** (they talk to
   each other by name inside the docker network). If they have to stay reachable by an external tool
   (DBeaver), a **conscious** offset instead of the default value.
5. **Align the variables** frontend↔backend onto the `.localhost` names (`NUXT_BACKEND_URL`,
   `FRONT_END_URL`, etc.), no more manual resync on every port change.
6. **Verify**: Windows browser → `https://<project>-<role>.localhost` → WSL container.

## Output / checkpoint
Portless-ready stack: named HTTPS route(s), zero HTTP collision, variables aligned. No pipeline
checkpoint.

## Guardrails
- **portless = plumbing consumed**, not rewritten. What we own is *this wiring*.
- **The agent proposes, the human ratifies**: any change to the real `compose`/`.env` goes through
  the dev.
- **Only handles HTTP(S).** Non-HTTP ports (3306/6379/9200) are handled by **not publishing them**
  (intra-network) or a **conscious offset**: portless doesn't cover them.
- **On demand**, never an automatic hook. Installing portless = a human action (system change).
- **Microsoft SSO**: using the `https://<...>.localhost` URL as an Azure AD redirect URI is **to be
  verified** on the Azure side: don't assume it works.

## Origin
A market portless tool (the plumbing: 443 proxy + `*.localhost` + WSL/Windows CA + worktree names).
The wiring/the per-project fixing is ours. Realises the "portless agent" idea from the plan (see the
memory, `CHALLENGE.md`).
