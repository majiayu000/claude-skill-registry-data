---
name: secure-pa-http-trigger
description: >-
  Secure a Power Automate "When an HTTP request is received" flow: migrate from "Anyone"
  to "Any user in my tenant" with Entra bearer tokens and rewire callers (plugin, code
  app, MDA button, external). Use for MisMatchingOAuthClaims,
  DirectApiAuthorizationRequired, "secure my flow HTTP trigger".
---

# Secure Power Automate HTTP-Triggered Flows

Migrates a Power Automate `When an HTTP request is received` flow from `Anyone`
to authenticated `Any user in my tenant` and rewires the callers. Grounded in
the brief under `references/`; load only the sections you need.

## Why this matters

`Anyone` makes the flow URL anonymously callable by anyone who has it. The
modern `Any user in my tenant` setting forces every request to carry
`Authorization: Bearer <jwt>` whose `aud` is exactly
`https://service.flow.microsoft.com/` (Public cloud, **trailing slash
mandatory**; sovereign clouds differ — see §1 of
`references/01-protocol-and-claims.md`).

> **The trailing-slash trap (read §11 first).** Entra v2 strips the trailing
> slash from `https://service.flow.microsoft.com/` when you request `.default`,
> so `aud` has no slash and Power Automate rejects with `403
> MisMatchingOAuthClaims`. Fix: a **double slash** in the scope,
> `https://service.flow.microsoft.com//.default`. Every sample applies it.

Switching the setting **regenerates the URL** and **immediately invalidates
every legacy caller**. There is no in-place coexistence. So the migration is
always a clone-and-cut, with a Dataverse environment variable holding the URL
so callers swing in one flip.

## Intake — three questions

Ask only what is unclear; never re-ask what the user already gave you.

1. **What does the flow do?** — surfaces secure inputs/outputs and PII concerns.
2. **What is the caller context?** — pick exactly one:
   `dataverse-plugin`, `code-app`, `mda-button`, `external-service`. Multiple
   callers means do the workflow once per caller.
3. **What environment / cloud?** — Public / GCC / GCC High / China / DoD. Affects
   the audience value (table below). Default to Public if the user doesn't say.

## Workflow

Do these in order. Read each reference only when it applies.

1. **Always:** read `references/01-protocol-and-claims.md` (the protocol contract,
   same for every caller).
2. **Always:** read `references/02-entra-prerequisites.md`. App A is always
   needed; App B (SPA) only when the user insists on direct-fetch from MDA
   ribbon JS — rare, and not the default recommendation.
3. **One of, depending on caller:**
   - `dataverse-plugin` → `references/04-context-plugin.md`
   - `code-app` → `references/05-context-code-app.md`
   - `mda-button` → `references/06-context-mda-button.md`
   - `external-service` → `references/07-context-external.md`
4. **If the chosen path uses a custom connector** (mandatory for `code-app`,
   recommended for `mda-button`, optional otherwise): read
   `references/08-connector-wrapper.md`.
5. **Always:** read `references/03-migration-procedure.md`. The 12-step cutover
   doesn't change; quote the relevant steps with the user's flow name filled in.
6. **Skim:** `references/09-troubleshooting.md` so you can pre-empt the errors
   they're most likely to hit.
7. **Always:** read `references/11-known-bugs-and-workarounds.md` before
   emitting any code that requests a Flow service token (trailing-slash `aud`
   bug, 502 `NoResponse`, client_credentials failure on Self-Host Multitenant
   URLs, device-code prerequisites).
8. **Optional:** `references/10-recent-developments.md` for 2025-2026 platform
   changes and `[Inference]` flags.

## What to deliver — always all three

### 1. Recommendation paragraph

Two to four sentences. State target trigger setting, chosen pattern (e.g.
"Pattern A: Managed Identity direct call" or "Custom connector wrapper"), and
why it fits their context. If their stated path is suboptimal, say so and offer
the better alternative — but execute what they asked for unless they accept the
alternative.

### 2. Numbered migration steps

Concrete steps with the flow name, environment, and tenant filled in. Don't
emit raw `<tenant-id>` placeholders. If a value is missing, ask once in this
same response (don't trickle one question at a time).

### 3. The customised script(s)

Read the matching template from `assets/<context>/...`, fill in known values
(flow name, tenant ID, audience, scopes, redirect URIs), and output the
result inline. Anything still unknown stays as a clearly-named placeholder
like `${TENANT_ID}` with a note on where to get it.

Canonical templates per caller (plugin, code-app, mda-button, external-service), the custom-connector wrapper and the Entra provisioning scripts are listed in `references/12-assets-catalog.md`; `assets/plugin/` also holds `PluginAssembly.csproj.snippet`.

## Decision shortcuts

If everything else is on fire, use this table directly. Source: §2 of the brief.

| Caller context           | Use…                                                                              | Custom connector?        | Token type                                |
|--------------------------|-----------------------------------------------------------------------------------|--------------------------|-------------------------------------------|
| Dataverse C# plugin      | Pattern A: Managed Identity (FIC). Fallback: MSAL.NET cert. Or Pattern B: broker. | No                       | App-only                                   |
| PowerApps Code App       | Custom connector (mandatory after CSP enforcement 2026-01-30, MC1218747).         | **Yes**                  | Delegated, connector-managed               |
| Model-Driven app button  | Custom Page → connector. Fallback: `@azure/msal-browser` ribbon JS + `blank.html`.| Yes                      | Delegated, connector-managed               |
| External service         | Delegated authcode. Client credentials only with "Specific users + SPN allow-list". | Usually no               | Delegated for `Any user`; app-only for `Specific users + SPN` |

If the user pushes for client_credentials directly into `Any user in my tenant`,
flag it as `[Inference]`: community-confirmed but not Microsoft-documented
verbatim. Recommend either changing to `Specific users in my tenant` with the
SPN object ID allow-listed, or putting a broker API in front (Pattern B).

## Audience values per cloud

State this explicitly in every sample — silently defaulting to Public is the #1
cause of `MisMatchingOAuthClaims`. Source: §4.1 of the brief.

| Cloud      | Audience                                          |
|------------|---------------------------------------------------|
| Public     | `https://service.flow.microsoft.com/`             |
| GCC        | `https://gov.service.flow.microsoft.us/`          |
| GCC High   | `https://high.service.flow.microsoft.us/`         |
| China      | `https://service.powerautomate.cn/`               |
| DoD        | `https://service.flow.appsplatform.us/`           |

Trailing slash is mandatory.

The Flow Service first-party app id is
`7df0a125-d3be-4c96-aa54-591f83ff541c` — same in every cloud.

## What this skill does NOT do

- It does **not** push the secured URL anywhere: the user updates their
  Dataverse environment variable (recommend `pa_flowEndpoint`).
- It does **not** provision Entra apps (it generates the CLI / PS the user runs),
  smoke-test the flow (it produces the four-probe plan: anonymous, valid
  same-tenant, wrong-tenant, wrong-audience), or flip the trigger setting on a
  live flow (the user clones, cuts, and disables per `references/03-migration-procedure.md`).

## Authority and freshness

The brief was last verified **2026-05-05** against Microsoft Learn 2026-04-29.
Findings in `references/11-known-bugs-and-workarounds.md` were captured
**2026-05-08** on a real Self-Host Multitenant flow. For a sovereign cloud missing
from the table above, or a later platform shift (new Code Apps CSP defaults, a
deprecation date for `Anyone`, a new Managed Identity rollout), say so and direct
the user to verify against current Microsoft Learn before cutover.
