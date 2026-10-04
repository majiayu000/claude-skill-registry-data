---
name: provider-access-scout
description: "Decision-ready scouting record for a user-connected provider access campaign. Use when an assigned Provider Access Launch task needs its easiest official route, minimum scopes, cost, account needs, approval path, implementation consumer, and easy-execute verdict established before submission. NOT for client Local Listings distribution."
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/provider-access-scout/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# Scout Provider Access

Scout five assigned campaigns by default. Finish each record independently so a submission agent can
continue without rereading the entire web or repeating portal discovery.

**Keep Local Listings separate.** Campaigns cover user-connected OAuth, API, API-key, remote MCP,
integration-marketplace, and partner access. Client Local Listings distribution (listing claims,
location publishers, data aggregators) is out of scope — it belongs to
`common-docs/systems/marketing/local-listings/PLAN.md`.

## Before research

1. Read `common-docs/systems/integrations/provider-access/FEATURE.md` when available.
2. Open the assigned task and set `status=active`, `Phase: scouting`, and yourself as owner using the
   normal Projects/Tasks product path.
3. Inventory existing implementation and assets before proposing access:
   - live MCP catalog and tool definitions;
   - first-party integration and external MCP connection records;
   - provider code, UI, and tests;
   - existing plugins and detailed provider plans;
   - CRM provider/interactions and Vault definition metadata.
4. If the campaign has no implemented or immediately testable user outcome, recommend “do not
   request yet.” Access for a hypothetical future enhancement is not launch progress.

## Research standard

Use current official developer docs, policy/terms pages, pricing, portal instructions, and help
center material. Verify facts that can change in the live portal when docs are incomplete. Record the
date and direct official URL for every approval, scope, cost, production, or review claim. Treat
third-party guides only as search leads.

Answer all of these:

1. What exact user outcome does AI Matrx already implement or can verify now?
2. Which access route is canonical: no-auth, official remote MCP, OAuth self-service, reviewed OAuth,
   API key, partner program, publisher enrollment, marketplace, or customer-specific activation?
3. What exact scopes/capabilities are required? Map each to the product action, code consumer,
   reviewer-visible UI, and verification operation.
4. Which offered scopes must not be requested now, and why?
5. Is developer/sandbox access distinct from production access?
6. Are fees, contracts, billing, legal-entity verification, business verification, compliance or
   regulated-data attestations, customer sponsorship, DNS, app publication, or quotas involved?
7. What account/role is required, and can the AI Matrx-owned `info@aimatrx.com` identity use Google
   SSO inside the separate Codex in-app Browser? If not, what exact password, mailbox verification,
   MFA, Vault metadata, recovery, and standing-authorized execution plan lets the agent complete the
   account without returning clerical work to Arman? Name an owner interruption only when the live
   flow introduces an explicitly excluded boundary.

Using Google SSO solely to authenticate an eligible non-Google provider is not work on a Google
campaign and remains standing-authorized even when Google-family campaigns have a dedicated owner.
8. Which redirects, domains, privacy/terms/support URLs, screenshots, videos, test credentials, or
   reviewer instructions are needed?
9. What confirmation/case ID will result, how long does the provider say review takes, where is
   status visible, and what is the escalation/support route?
10. How is access revoked and reconnected?

## Easiest-route rule

**Find the shortest official path before researching a custom developer application.** Check in
this order and stop when an implemented outcome is satisfied:

1. an existing verified AI Matrx connection;
2. an official hosted remote MCP with browser OAuth/dynamic registration;
3. an official no-auth or self-service API;
4. an official API key or self-service OAuth connection;
5. a provider-reviewed OAuth application or marketplace submission;
6. a partner, enterprise, customer-sponsored, or publisher program.

An official MCP may eliminate app registration, scope review, screenshots, and reviewer approval.
Do not climb the harder route merely because it exposes more capabilities. Record why the easier
route does or does not satisfy the implemented AI Matrx outcome.

## Scope rule

Choose the least privilege that completes the implemented outcome: read before write, resource-
specific before account-wide, and incremental consent at the moment of use. Separate unrelated scope
families or reviewer stories. If a scope cannot be tied to an implemented action, code consumer,
visible UI, and real verification, recommend that it not be requested.

## Connection ease and operation risk

Score two independent axes:

- `access_effort`: `existing` | `instant_mcp` | `self_service` | `provider_review` | `partner`
- `operation_risk`: `read_only` | `bounded_write` | `sensitive_write` | `regulated`

**Do not make connection difficulty inherit operation risk.** A database or payment MCP can be an
easy self-service connection even though destructive or financial tools require separate user
confirmation. Prove the connection with the safest useful operation—prefer a read-only, test,
sandbox, or project-scoped operation—and record stronger tool controls separately.

## Easy-execution verdict

Classify `easy_execute` only if every answer is yes:

- free and reversible, with no billing or contract;
- AI Matrx-owned account and approved publisher facts;
- no legal, compliance, regulated-data, customer, or identity attestation;
- no production DNS, customer-facing publication, customer data, or live-traffic mutation;
- no provider review, manually registered production app, or unpublished scope request;
- only the minimum documented connection for an implemented capability;
- private/development mode remains possible when offered;
- immediate verification and revocation are known.

An official remote MCP using browser OAuth may pass this gate even when it advertises high-impact
tools, provided connection is free/reversible and verification uses a safe read-only or test
operation. `easy_execute` authorizes connecting and performing that recorded proof; it never
authorizes arbitrary write/destructive tools.

If any answer is no or uncertain, set `easy_execute: false`, leave `Phase: ready_to_submit` only when
the recommendation is complete, and name the exact decision or prerequisite. “Free signup” alone
does not make a production publisher review easy.

Arman's 2026-08-29 standing authorization covers free, reversible, least-privilege account
creation, ordinary signup terms, development apps, keys, service accounts, DCR/OAuth/MCP grants,
Vault custody, secret rotation, service restart, and the recorded safe proof. Classify and hand the
campaign directly to `$provider-access-submit`; never ask Arman to reply yes again for those actions.
Paid commitments, negotiated contracts, regulated/compliance or legal-identity attestations,
customer data, production DNS/traffic, external communication, public publication, destructive
operations, and provider-enforced human ceremonies remain outside that authorization.

## Account-creation packet

**A scouted account path is executable, not a homepage.** When access requires an account,
organization, workspace, developer console, seller tenant, or business portfolio, append one
`ACCOUNT CREATION PACKET` to the live task before scouting is complete:

```text
Bundle: <stable shared account prerequisite; name every campaign it unlocks>
Exact signup page:
Exact login/developer-console page:
Recommended identity and authentication method:
Required account/workspace/business type:
Prerequisites and immutable fields:
Free sandbox/dev tenant vs paid/live tenant:
Human-only ceremony:
Agent-ready when:
Autonomous continuation:
Official sources (verified YYYY-MM-DD):
```

Use the deepest official URL that starts the actual enrollment; a provider homepage is insufficient
when a stable signup or developer-console URL exists. Deduplicate shared prerequisites: one Meta
developer account may unlock several Meta campaigns, while TikTok for Developers and TikTok for
Business remain separate bundles. State whether `info@aimatrx.com` with Google SSO works; when it
does not, name the exact approved identity class and Vault custody plan. Never invent a shared human
identity to satisfy a provider that requires a real person.

When account setup is assigned or scheduled, create exactly one execution action for each `Bundle`.
Use an owner-session action only when the bundle contains a named boundary outside the standing
authorization. Put the due date and click-through action on one primary campaign task; sibling
campaigns must reference that shared bundle without duplicating the due action. Separate bundles
remain separate actions even when they belong to the same provider. Reuse an existing account or
bundle task when canonical inventory proves it exists instead of creating a new signup action.

Do not ask Arman to create an account an agent can create under the standing authorization. Put a
provider-enforced identity, CAPTCHA, hardware key, legal document, payment decision, or immutable
business fact in `Human-only ceremony`; routine SSO, mailbox codes, password generation, MFA/Vault
work, and ordinary consent remain agent work. `Agent-ready when` must be an observable portal state
that lets the next agent continue without rediscovery.

## Required scouting record

Update the task case card and append a dated scouting section containing:

```text
Verdict: easy_execute | ready_for_owner | do_not_request_yet | no_auth_needed
Implemented outcome:
Access route:
Access effort: existing | instant_mcp | self_service | provider_review | partner
Operation risk: read_only | bounded_write | sensitive_write | regulated
Minimum scopes/capabilities:
Explicitly excluded:
Developer vs production:
Cost/contract:
Account/business/compliance requirements:
Required assets:
Submission URL:
Expected receipt/status surface:
Provider-stated review timing:
Revocation/reconnect:
Risks and open decisions:
Official sources (verified YYYY-MM-DD):
Exact next action:
Next check:
```

Resolve or link the provider `crm.party` when possible. Do not create a CRM interaction for merely
reading docs. At completion, leave the task `planned` when decision-ready, scheduled, or waiting on
a provider; use `active` only while an agent or human is working it right now. Never leave `active`
without an owner and exact current action.

## Example requests

- “Use `$provider-access-scout` on the next five P0 remote MCP campaigns.”
- “Use `$provider-access-scout` on Epic FHIR and distinguish sandbox from production.”
- “Use `$provider-access-scout` on Meta Ads and identify the smallest implemented permission set.”
