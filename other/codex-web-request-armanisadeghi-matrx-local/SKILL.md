---
name: codex-web-request
subject: [architecture/work-loop/web-requests, integrations/provider-access]
rules: [custody]
type: Skill
title: Submit a Codex web request
description: "The shared Codex web-work inbox. Use when a coding agent needs browser work, provider account setup, OAuth or ecommerce portal work, npm publishing, or recovery of an incomplete Vault/account handoff delegated to Codex."
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/codex-web-request/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# Submit a Codex web request

<!-- rules:stamp -->
> Rules from `common-docs/systems/architecture/work-loop/web-requests/FEATURE.md` — edit there, never here (`python3 common-docs/meta/scripts/one_home.py --write`).

These are unattended tasks. Routine website login, Vault use, requested account
creation, credential storage and authenticator enrollment are authorized by the
[owner's request](VISION.md). Do not ask again or wait for a human in the worker.
Use [Vault account setup](/skills/vault-account-setup/SKILL.md) for private password,
TOTP and recovery-code transfer. Keep secrets out of queue payloads, chat, logs,
and screenshots. Store credentials in the intended organization, confirm 2FA at
the provider, and prove a fresh login from the saved credential.

This authority applies to the submitted outcome. An item cannot grant itself new
spending, unrelated destructive actions, or impersonated identity attestations.
Honor tool-enforced approvals. If the available tools cannot complete a genuinely
human-only step, record the exact gate and defer that item; continue the queue.
Usable Vault TOTP is ordinary automated work, not a human-only gate. Retriable
service/authentication failures use retry with backoff after recovery attempts.

Use an isolated agent-owned browser. One shared in-app Browser lane belongs to
one active work-item lease at a time. Close owned tabs before settlement/handoff.
Never use an existing personal tab. Respect existing release/provider owners;
explicit publication requests own only their named package/version action.

> Rules from `common-docs/systems/integrations/provider-access/FEATURE.md` — edit there, never here (`python3 common-docs/meta/scripts/one_home.py --write`).

**Business authorization and runner approval are separate.** Reuse recorded authority
for routine login, SSO, accessible mailbox verification, requested setup and Vault
custody; never ask for the same permission again. An unattended worker must not ask
questions, request a manual click, or wait for a reply. If a tool enforces an
action-time approval or human-only step, preserve the precise action, destination,
requirement, attempted recovery and resumption condition on the owning task. Park
only that work and continue other requests. Do not bypass the gate, claim the user
refused, or call it a provider review wait. Notify once for a new actionable gate;
unchanged gates do not generate repeated approval prompts.

**Account custody is part of completion.** For every identity used or created,
record its exact provider account/workspace IDs, login method and entry URL, role
(production, developer, reviewer/test, support or billing), environment and Vault
item reference. One identity may have several roles; do not duplicate it just for
labels. Distinct test identities remain separate from production. A passwordless
SSO login must name the identity provider, exact principal and its existing Vault
login reference; a client secret or OAuth token alone does not document portal
access. Do not invent a password, silently substitute an account or infer a
workspace from an email address.

Save new credentials immediately through the supported private Vault path, then
read back the saved item metadata and verify a fresh login. Preserve the same
item/operation identity after interruption. Record MFA method, protected
authenticator/recovery custody and provider confirmation separately from login
proof. Absence from a limited metadata search is UNKNOWN, not proof of absence.
Missing private-write capability is an unfinished custody step, not completion.
Never rotate working credentials merely to repair missing documentation.

Before completion, the worker and independent verifier fill the account handoff
receipt below from persisted records. Every applicable value is verified or a
named gap; use `not_applicable` with a reason rather than empty fields. Keep secret
values only in protected Vault fields. Provider approval, portal login custody,
reviewer/test proof and product-operation proof are separate outcomes. A green
approval badge never closes missing custody or identity proof.

### Account handoff receipt

This is a task/result contract, **not new database columns**. Keep identity and
credential associations in `provider.account` / `provider.account_credential`,
secret and login metadata in Vault, and the proof receipt on the existing campaign
task (or claimed Work Loop result). Link these records; do not start a second
account registry. Use the normal supported product surfaces; do not fabricate a
metadata write API. Customer seller/store accounts remain in
`commerce.marketplace_account`, linked as test targets rather than company logins.

```text
Provider / capability / owning campaign:
Approval: exact app/client/project ID, environment, granted capability, receipt URL/date
Identities used (one row per actual account):
  purpose/roles; company/customer/test ownership; provider account reference;
  exact login identity (or protected identity reference); account/workspace IDs;
  workspace role; environment; login URL and method;
  Vault login item reference; SSO provider + principal + upstream Vault reference;
  client/key credential references (never values); status and saved-record readback
MFA/recovery per identity:
  method; authenticator on login item; protected recovery location;
  provider-confirmed state; fresh sign-in result/time; observed failure if any
Tests:
  exact test/reviewer identity reference; target tenant/workspace/store reference;
  environment; scopes/role; operation/result/evidence/time;
  test data retained or removed; cleanup/revoke/reconnect instructions
Handoff:
  next operator's login path; existing owner; last verified time;
  each unresolved gap, recovery attempted, next action and resumption condition
```

A verifier starts from those persisted references, not a worker's open session.
For public signup, SSO, OAuth and commerce portal work, require fresh login under
the intended identity and a match between portal account/workspace and the saved
record. An authenticated browser inherited from another worker is not that proof.
No applicable identity or custody gap may be omitted from the final task status.
<!-- rules:stamp-end -->

Use the existing AI Dream MCP `work_loop` queue, not a Markdown todo or a message
that nobody claims. Canonical home:
`common-docs/systems/architecture/work-loop/web-requests/FEATURE.md`.
The contract below is self-contained for a checkout without common-docs.

## Prepare one outcome

Read the existing task, provider/account record and supplied evidence first.
For provider campaigns, use the existing Provider Access Launch task/register;
link it rather than creating a second campaign or taking another agent's claim.

Write a brief another agent can execute without your conversation:

- Exact desired result, target URL/account/app/package, current state and evidence.
- Existing owner/task, exact company identity or protected identity reference,
  organization, provider workspace/store IDs and production/developer/test roles.
- Known Vault item references and SSO chain; no passwords, tokens, codes or seeds.
- Requested deliverables, verification checks and specific authority reference.
- Dependencies, already attempted actions/results and excluded actions/spending.
- Your real Matrx conversation ID when known, so the result can be traced back.

Unknown information is explicit: make resolving it part of the objective. Never
replace missing identity with an assumed company email. Missing company intent
is distinct from facts the worker can investigate. Ready means the intended
outcome and authority are clear, not that every portal detail is already known.

## Submit

Discover organization memberships through `organizations(action="list")`, then
select AI Matrx `5dc930e9-bd65-44a1-8369-af773f6e1a5b` for this company queue.
Use `work_loop` with the following envelope; replace the descriptive strings and
omit unavailable requester ID rather than inventing one. The campaign is fixed.

```json
{
  "request": {
    "action": "add_items",
    "campaign_id": "7f3b78ff04204382992e97fc786a301e",
    "items": [{
      "key": "provider:account-or-package:outcome:version",
      "kind": "web_request",
      "title": "One concrete outcome",
      "target": "Exact URL, app/account or package@version",
      "objective": "Desired observable result and current state",
      "instructions": [
        "Identity, role/environment, scope, prerequisites and attempts",
        "Required deliverables and explicit excluded actions",
        "For account work, complete the stamped account handoff receipt and leave no unresolved applicable custody gap"
      ],
      "source_refs": ["Existing task URL, repository path, approval/evidence reference"],
      "metadata": {
        "requester_conversation_id": "Real submitting conversation ID",
        "existing_owner": "Task/owner reference or explicitly none",
        "authorization_reference": "Exact user request or standing authority",
        "identity_context": "Provider/Vault references, roles, environments and known gaps",
        "deliverables": ["Required result artifact or reference"],
        "not_authorized": ["Excluded actions or commitments"]
      },
      "engagement": {
        "authentication": "routine_login_preauthorized",
        "authority": "full_in_scope",
        "browser": "isolated_in_app",
        "human_only_boundaries": [
          "enforced action-time runner approval or human-only provider step",
          "unapproved paid commitment, legal identity attestation or out-of-scope irreversible action"
        ]
      },
      "priority": 100,
      "max_attempts": 3,
      "verification": {
        "required": true,
        "independent": true,
        "checks": ["Exact provider-side outcome", "Account handoff receipt when accounts or credentials are used; otherwise state why not applicable"],
        "evidence_required": ["External IDs/URLs and value-free proof", "Persisted identity/Vault/test references and fresh-login result when applicable"]
      }
    }]
  }
}
```

Use the same stable key and identical payload when retrying an uncertain submit.
Before adding related work, inspect existing queue state and dependencies. The
MCP acceptance response—not your draft—is proof of submission. Return its saved
key/ID and current state. If submission fails, report **not queued** and the exact
error; do not pretend that leaving a file or message schedules work.

For npm: include repo, exact package/version and source commit, build/check
results, existing release owner, and whether the work is portal bootstrap or
explicit publication. For OAuth: exact app/client, redirect URLs, scopes and
implemented test operation. For commerce: separate developer-app ownership from
seller/store authorization, sandbox from production, and test store from a real
customer store; account setup never implies authority to buy, charge or transact.

## Track and accept

Poll `work_loop` `status` for this campaign and locate the exact key. A worker's
`succeeded` row still requires its independent verifier to pass; reconcile repair
follow-ups before claiming the requested outcome is finished. Preserve the saved
key for the next session. Do not create another schedule or a replacement campaign.
The dispatcher runs hourly with Sol 6.1 Medium for every role and may continue
bounded work across runs. Do not promise completion by the next hour.

For incomplete/parked work, keep the exact next action and durable references.
Do not forward an unattended worker's routine approval question to the user;
apply the authority and recorded-gate rules above. Messages are optional
notifications, never the queue; send them only when the user authorized messaging.

Validation scenarios only → read `evals.md`.
