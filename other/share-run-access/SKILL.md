---
name: share-run-access
description: >
  Grant named people the access they need to review or work on an ACE run, on every surface it
  links: ace-web, labs dashboards, the Connect opportunity, HQ apps, the OCS chatbot. Editor by
  default; approval-gated per invite.
disable-model-invocation: false
---

# Share run access — one primitive for "let the thread review this run"

> ## ⛔ Granting access is WORK TO DO NOW, not work to schedule
>
> When a human asks you to give named people access, the deliverable is **those people having
> access** — not a plan, not a ticket, not a skill describing how it would be done.
>
> - **A missing atom changes the MECHANISM, never WHETHER it happens this turn.** If there's no
>   atom for a surface, do it by hand *now* (UI, authenticated HTTP, a one-off script). Filing the
>   atom issue is something you do *in addition to* granting access, never instead of it.
> - **Do not decide the human's ask was unnecessary.** Default scope is every gated surface the
>   run-summary links. "They probably don't need the app builder" is not your call; narrowing is
>   the human's, made explicitly.
> - **You may not report success while any requested surface is ungranted**, and no outbound
>   message may say "access is set up" unless every surface is granted *and read back*. Say
>   plainly which ones are NOT DONE and who owns the next step.
>
> Origin (dimagi-internal/ace#915): asked to grant a thread access, ACE filed two atom issues at
> 16:36, merged a skill documenting them as "manual until the atom lands" at 16:47, and emailed
> "Access is set up" at 18:34 — having performed neither manual step. The reviewer hit 404s and had
> to write back. Three lines in this very skill authorized that: "atom pending → report the manual
> step", "most reviewers don't need the raw app-builder", and a report contract where
> `blocked: <precondition>` was an acceptable terminal state.

As more people use ACE and ace-web, sharing access must be a repeatable step, not a bespoke
scramble each time (Jon, 2026-07-23: access "should go to all individuals on a thread about a
project we are working on"). This skill is that primitive: given an opp/run and a set of emails,
it grants each person what they need to review the run, surface by surface, and reports exactly
what was granted vs. what's blocked on a precondition.

## Access is for CO-CREATION, not review (Jonathan, 2026-08-14)

This skill used to frame every grant as *review* access: share the docs so a partner can read
them and maybe comment. That is the wrong model. **ACE opportunities are co-created with
partners.** When Spark, or Sophie, or any partner engages with a run's outputs, they should be
able to **edit** the artifacts — feedback in this model arrives as *revisions*, not only as
comments.

So on ACE-authored Drive documents the default grant for a named partner collaborator is
**editor (`writer`)**, and the primitive is:

| Atom | Grant | Use when |
|---|---|---|
| `drive_share_with_person` | `type: user` — `writer` (default) / `commenter` / `reader` | **You know who the collaborators are.** The co-creation primitive. `writer` lets them edit; the grant is scoped to that person. |
| `drive_set_anyone_with_link` | `type: anyone` — `reader` (default) / `commenter` / `writer` | Nobody named: a public run-summary asset, a PNG a Slides deck must fetch (`reader`), or a doc handed round a thread for reactions (`commenter`). |

⚠ **`drive_set_anyone_with_link` at `writer` is a blunt instrument** — anyone the URL is
forwarded to can edit *or delete* the document. It works on this Shared Drive (verified
2026-08-14; Drive returned `{"id":"anyoneWithLink","type":"anyone","role":"writer"}`), but when
you can name the people, name them.

⚠ **Neither atom emails anyone.** `drive_share_with_person` sets Drive's
`sendNotificationEmail: false` unless you explicitly opt in — ACE's outbound email is gated
through `bin/ace-email` and a Drive-sent share notice would route around that gate. Sending the
link is a separate, approval-gated step you do through the normal email path.

Downstream implication, flagged not solved: `skills/feedback-ledger` models feedback as
**comments** (`channel: gdoc-comments`). Direct edits are a channel it does not capture — see
that skill's "Revisions are a channel this ledger does not yet capture" note and
dimagi-internal/ace#1335.

## The access model (why each surface is different)

The run-summary page itself is **public** ("the URL is the secret"). Its ACE-authored
deliverables are **not**.

> **Correction (2026-08-14).** This section used to claim every ACE-authored deliverable
> "is anyone-with-link — set at creation by the producer skills and enforced by
> `run-summary-qa`". None of that was true. `grep -rl drive_set_anyone_with_link skills/`
> hits only `training-deck-render`, `app-screenshot-capture`, `common-screenshot-capture`,
> `partnership-deck-build`, the summary gate and this skill — and all of those share **PNG
> images** so Slides' image-import service can fetch them, never a Doc or the deck itself.
> No producer skill shares a document. And `run-summary-qa` (now superseded by
> `run-surface-audit`) enforced nothing: its checker
> bucketed a private-doc 401 as AUTH-GATED and passed the run. Live proof on
> `spark-facilitator/20260813-2126` — the first run shown to an external partner: all 8
> reviewer-facing artifacts carried 24 permissions each and **zero** `type: anyone`, and the
> link checker still reported `12 links · 0 BROKEN`.

**What actually shares them, today, is this skill + `run-surface-audit`.** The auditor now
classes an unshared `docs.google.com`/`drive.google.com` deliverable as
**`PRIVATE-DELIVERABLE`** and exits non-zero (so it can no longer certify a run whose docs
open for nobody), and step 2 below is the step that fixes them — by calling
`drive_set_anyone_with_link` per file. Producer-side sharing at creation is still an open
gap (jjackson/ace#902); until it lands, treat every run's docs as private until you have
shared them and re-checked. Beyond the docs, what needs a grant is the **platform-gated**
links, each a separate membership system:

| Surface | Summary link(s) | Auth | Grant mechanism |
|---|---|---|---|
| **ace-web workbench** | `/ace/w/<workspace>/opps/<opp>/runs/<run>` (the "how we got there" view) | Connect/CCHQ OAuth + ace-web's login gate + `WorkspaceMembership` | Allowlisted domains (`dimagi.com`, `dimagi-ai.com`, `dimagi-associate.com`) **auto-join** on first sign-in (no grant). Any other address signs in only through an invite or an existing membership — see the login-gate box below. |
| **labs dashboards** | `/labs/workflow/<id>/run/?...` | labs (CCHQ OAuth) + the synthetic opportunity's `allowed_domains` | **Dimagi-only.** Phase 7 dashboards sit on labs-only synthetic opportunities that `demo-data-setup` creates with `allowed_domains: ['@dimagi.com', '@dimagi-associate.com', '@dimagi-ai.com']`; labs' `is_accessible_to` rejects any other email domain, and seeing the opp in the picker also needs the `view_synthetic_opps` toggle. Internal staff need no grant. An external reviewer who signs in successfully still opens **no** dashboard here — see step 4. |
| **Connect opportunity** | `connect.dimagi.com/a/<org>/opportunity/<id>/` | Connect org membership | `connect_add_org_member` into the org that **HOLDS** the opportunity (`run_state` → `connect.products.connect.holding_org_slug`; legacy runs: `organization_slug`). Connect's `org_opportunity_access` gives the holding org's members access to its opportunity; on a PM→NM run that is the NM org, not the PM org (live 2026-09-26, `playbook/integrations/connect-api.md § PM→NM org-URL matrix`). |
| **CommCare HQ apps** | `commcarehq.org/a/<domain>/apps/view/<id>/` | HQ web-user on the domain | `commcare_invite_web_user` (ships since ace#905; defaults to the **`App Editor`** role — load-bearing, see below; reconciles an existing member's role rather than skipping). |
| **OCS chatbot admin** | `openchatstudio.com/a/<team>/chatbots/<id>/` | OCS team membership | `ocs_add_team_member` ("Chatbot Admin" group). **Internal (Dimagi) only.** OCS has NO per-chatbot permissions: every group is team-wide, and Chatbot Admin (the only group that opens a chatbot's config page) grants view + edit + delete on **every chatbot on ACE's team**; Chat Viewer (transcripts only) still reads every bot's transcripts. **External reviewers get no OCS account** (Jon, 2026-09-28) — they chat through the public link, which needs no login and exposes nothing else: `products.ocs_chatbot.public_url`. |

**The account precondition threads through all of them:** every gated surface authenticates via
CommCareHQ/Connect OAuth, so a person can only reach ANY of them once they have a Connect/CommCare
account and have signed in once. `@dimagi.com` staff generally do; an **external collaborator**
(e.g. `@dimagi-associate.com`) must create one first. This skill never provisions accounts — it
grants membership and tells the person the one sign-in they must do themselves.

> ⛔ **ace-web admits an outside address by invite, and a workspace invite grants the WHOLE
> workspace.** ace-web's login gate (`apps/auth/login_gate.py` `admission_rule` in the ace-web
> repo) checks four rules in order: `open` (the domain list is empty) → `domain`
> (`ACE_ALLOWED_EMAIL_DOMAINS`, currently `dimagi.com,dimagi-ai.com,dimagi-associate.com`, set in
> ace-web's `deploy/aws/ace-web.cfn.yaml`) → `invite` (a pending, unexpired, unrevoked
> `WorkspaceInvite`) → `membership` (an existing `WorkspaceMembership`). So an invite to an
> outside address does work: they sign in through it, and after they accept it the membership
> keeps them in. Removing their last membership is how they are cut off. What that invite opens is
> every run in the workspace, not one. **For an external reviewer, never invite them into
> `dimagi-team`.** That would show them every opp's runs. The path for an external reviewer is
> `clone-to-new-workspace` → `validate-release-readiness` → `release`, which copies the run into a
> workspace of its own and invites them there. (History: before the invite rule, 2026-07-23, an
> external reviewer was told to accept a pending invite that could not be redeemed —
> dimagi-internal/ace#913. ace#2525 corrected the domain list and the admission rules.)

## Inputs

Pipeline-only: grants access to ONE run's products, so the run is the object (`run_state.yaml` resolves its org, domain, team and opportunity). Every row below is an explicit argument. To give someone access to a live program's objects outside a run, grant them through `partner-on-connect-program` § Changing a live program.

| Input | Required | Notes |
|---|---|---|
| `opp` (slug) + `run_id` | yes | Resolves `run_state.yaml` for the org/domain/team/opp identifiers below. |
| `emails[]` | yes | The people to grant. Default source: the current project thread's full To+Cc (verify from the structured read, never a raw dump). |
| `workspace` | no | ace-web workspace slug. Default `dimagi-team`. |
| `surfaces` | no | Subset to grant. Default: all gated surfaces the run has products for. |

## Process

1. **Resolve the run's identifiers** from `run_state.yaml` (`resolve_opp_path` → read the run's
   `run_state.yaml`): the Connect org that HOLDS the opportunity — `connect.products.connect.holding_org_slug`,
   else legacy `organization_slug` (`runConnectOrgs()` in `lib/connect-orgs.ts` is the rule; the run's
   RECORDED org is authoritative; if both keys are absent read the `/a/<org>/` segment of
   `.opportunity.url`, and only if that is absent too fall back to the configured PM org `connect_orgs.pm_org` from
   `bash bin/ace-doctor --preflight --no-live` — never a typed slug), `.opportunity.url`,
   the `commcare` `domain` (HQ), the `ocs_chatbot.team_slug` (OCS), the labs `opp_id`, and the
   `ace_web_summary_url`. Confirm the summary is clean first — run `run-surface-audit` if you
   haven't; never share a run with an unresolved **broken** or **misleading** finding.

2. **Share the deliverable docs — assume they are private.** Nothing sets anyone-with-link on
   them at creation (see the correction above), so this is a real step, not a verification.
   Two grants, and you normally do both:

   - **Per named collaborator → `drive_share_with_person({fileId, email})`, which defaults to
     `role: 'writer'`.** This is the co-creation grant: the partner can edit the artifact, and
     their feedback can arrive as a revision. Do this for everyone on the thread you were asked
     to grant. Narrow to `commenter` only when the human says the doc is read-and-react
     (a frozen deliverable, a signed work order), and say so in the report.
   - **Link-level floor → `drive_set_anyone_with_link`.** Run `run-surface-audit`
     (`scripts/audit-run-surface.ts <opp> <run>`): every `docs.google.com`/Slides/Drive
     deliverable must report `OK 200`, and each one that comes back **`PRIVATE-DELIVERABLE`**
     must be fixed before proceeding (anyone else on the thread hits "You need access"
     otherwise). Use `role: 'commenter'` as the floor for a document — a `reader` physically
     cannot comment, so the `gdoc-comments` channel `feedback-ledger` assumes is dead. `reader`
     stays right for PNGs a Slides deck fetches. `writer` here is available and works, but
     prefer the named grant above: link-writer means anyone the URL reaches can edit or delete.

   Neither call emails anybody — see the co-creation section. Telling people they have access is
   step 5/6, through the gated email path.

3. **Classify each email once** (per-person isolation — one person, one decision, like inbox-triage):
   - `@dimagi.com` / `@dimagi-ai.com` / `@dimagi-associate.com` → **internal**: ace-web auto-joins on
     sign-in (no invite needed) and labs' synthetic allowlist admits them; Connect/HQ/OCS grants apply
     normally.
   - **OCS is internal-only.** An external collaborator is NEVER invited to the OCS team — every OCS
     group is team-wide, so any invite exposes (and, as Chatbot Admin, lets them edit or delete)
     every chatbot on ACE's team. Give them the public chat link
     (`products.ocs_chatbot.public_url`) instead and report OCS as `public link (no account)`.
   - anything else → **external collaborator**: **not into `dimagi-team` on ace-web** (login-gate box
     above — an invite would admit them to every run in the workspace; route them to
     `clone-to-new-workspace` → `release`); for Connect, a deliberate external add —
     `add-org-member`'s @dimagi.com guard is intentional, so external Connect adds go through THIS
     skill's explicit external path (below), not that skill.

4. **Grant per surface** (idempotent — re-running skips people already granted):

   - **ace-web workbench.** Internal → nothing to grant; tell them to open the workbench URL and sign
     in (they auto-join). **External → STOP: report `NOT DONE — dimagi-team spans every run; release a
     clone instead — owner: operator (clone-to-new-workspace → release)`.** Do not send the invite below into `dimagi-team`. It would
     work (login-gate box above), and that is the problem: it opens every opp's runs. The invite
     endpoint here is for internal addresses that somehow missed auto-join:
     ```bash
     curl -sS -X POST -H "Authorization: Bearer $ACE_WEB_PAT_TOKEN" \
       -H "Content-Type: application/json" \
       "${ACE_WEB_BASE_URL:-https://labs.connect.dimagi.com/ace}/api/workspaces/<workspace>/members/invite" \
       -d '{"email":"<email>","role":"editor"}'
     ```
     Owner-gated: `ACE_WEB_PAT_TOKEN` must belong to a workspace **owner**. ACE is now a first-class
     ace-web principal — `ace@dimagi-ai.com` is an **owner** of `dimagi-team` and mints its OWN bot PAT
     (ace-web#670: the `0005_promote_ace_owner` migration + the `mint_personal_token` command), so ACE
     invites under its own identity, never on behalf of a human. (Bring-up after an ace-web deploy:
     `python manage.py mint_personal_token --email ace@dimagi-ai.com --label ace-bot`, set as
     `ACE_WEB_PAT_TOKEN` — a local-only `.env` key, not held in the vault.) The invitee then signs in once and accepts the pending
     invite. Read back `GET /api/workspaces/<workspace>/members` to confirm (pending until they accept).

   - **Connect opportunity.** **Read first, read-only:** `connect_list_org_members({ organization_slug: <holding org from step 1> })`
     — the member + pending-invite tables, GETs only (ace#2986). Someone already in `members`
     (or in `pending_invites`) needs no call; report them from that read. Only a person absent
     from both gets the grant, after the step 5 approval:
     `connect_add_org_member({ organization_slug: <holding org from step 1>, email, role: "viewer" })`.
     **Never use `connect_add_org_member` as a check** — for an absent person it creates an invite
     and Connect emails them. Any later "is X still a viewer?" verification is `connect_list_org_members`.
     The holding org, not the program org: a viewer there gets VIEW on exactly the org's own
     opportunities, where a PM-org viewer would see every program the PM org runs. **Blast radius:**
     with `nm_org` configured, EVERY run's build/QA opportunity is held by the same NM org
     (`lib/connect-orgs.ts` `phase4Orgs()`), so a viewer there sees every ACE run's opportunities,
     not one. That is fine for staff and an over-grant for an external reviewer; say so in the
     step 5 plan. **Connect SSO order for a first-time external user:** they must **sign in to
     Connect with "Log in with CommCare HQ" FIRST, then open the invite link while signed in.**
     Accepting the invite while logged out creates a *password* account for that email, after
     which Connect's `_reject_if_email_already_registered` blocks their first CommCare HQ sign-in
     (commcare-connect `users/adapters.py`). Put that order in the message that tells them. (Upstream
     `org_opportunity_access` grants the holding org ADMIN on the opp, capped by the member's own
     role — so a `viewer` member reads it.) Not yet exercised with a real reviewer on a PM→NM run;
     the claim rests on that upstream source.
     Precondition Connect enforces (not bypassable): ACE must be an **admin** of the org — on 403 →
     ask a current org admin to add `ace@dimagi-ai.com` as admin. No Connect account is needed
     first: Connect records a **pending invite** and the invitee signs up from its link (ace#2503).
     Statuses `invited-pending` (the normal outcome — pending until they accept) / `already-invited`
     / `invited` / `already-member` are all grants; `role` is the read-back, and `role_unchanged`
     means the requested role did not land. A `ConnectValidationError` (email in neither the member
     nor the pending table after the POST) is a **NOT DONE** — never relay it as "sign in to Connect
     first". **External emails:** allowed here (this is the deliberate external path
     `add-org-member` points to).

   - **labs dashboards.** Internal → no separate grant: labs authenticates via the same CCHQ OAuth,
     and an internal domain is on the synthetic opp's `allowed_domains`. Include the dashboard URLs
     and "sign in with your CommCare account" in the report. **External → report `NOT DONE —
     synthetic opp is Dimagi-only — owner: operator`.** Signing in will not get them in: `is_accessible_to` rejects
     their domain. Adding their domain with `synthetic_set_allowed_domains` (it REPLACES the list)
     opens that opp to everyone at that domain, not only this person, so it is a human decision.
     The partner path (`clone-to-new-workspace` → `release`) sets a partner workspace's own labs
     scope instead.

   - **CommCare HQ apps.** Call `commcare_invite_web_user({domain, email})` (ships since ace#905).
     **Blast radius:** an HQ role is a role on the whole DOMAIN. `App Editor` on ACE's shared domain
     gives view **and edit** on every run's apps there, not just this run's. That is fine for
     Dimagi staff and an over-grant for an external reviewer. Name it in the step 5 plan, and for a
     partner prefer the release path, which rebuilds the apps in the partner's own HQ space.
     **Do NOT pass `role: "Read Only"`.** The default is `App Editor` and that is load-bearing: HQ's
     stock Read Only preset grants `view_reports` + `download_reports` and **not** `view_apps`, so a
     Read Only member gets a bare 403 on every app link this skill shares — while the *releases* page
     still renders, which is exactly what makes the access look like it mostly works. Of the stock
     presets only `App Editor` and `Admin` carry `view_apps`; `App Editor` is the narrower. (Found by
     a real reviewer, not a judge — Sophie Feintuch, 2026-07-23.)

     The atom handles every state itself with read-back proof: fresh invite, pending-invite
     idempotent skip, already-a-member (nothing to change), and — the one that matters — **role reconciliation for
     a member sitting on the wrong role**, which membership-shaped checks report as success. Statuses
     `invited` / `invite-pending` / `already-member` / `role-reconciled` are all grants; a throw is a
     **NOT DONE** with the read-back evidence. Do not defer to "an HQ admin will do it" unless ACE
     genuinely lacks admin on the domain — and if so, that's a **NOT DONE** with a named owner.

   - **OCS chatbot admin — internal people only** (see the classification step: externals get the
     public link, never an OCS account). Call `ocs_add_team_member({email})` (ships since ace#906; default group
     "Chatbot Admin" is load-bearing — it carries `experiments.view_experiment`, the permission the
     linked chatbot page needs; a member on any other group 403s there). The atom handles all three
     states itself with fresh-read proof: fresh invite, pending-invite idempotent skip (or
     `replace_invite: true` when the pending groups are wrong), and additive group reconciliation
     for an already-accepted member. Statuses `invited` / `invite-pending` / `already-member` /
     `groups-reconciled` are all grants; a throw is a **NOT DONE** with the read-back evidence.
     It is an internal-tool surface, which is a reason to ask the human whether to include it
     *before* they ask — never a reason to silently drop it from a grant they requested.

5. **Approval gate (procedural).** Sending invites is outbound. Present the full per-person /
   per-surface plan and get the human's yes before firing any invite or `connect_add_org_member`.
   Read-backs (including `connect_list_org_members`) and doc-sharing (own artifacts) run freely.

6. **Report — binary per surface, no soft states.** Per person: domain class, then per surface
   exactly one of:
   - `granted` — **with the read-back that proves it** (a membership list showing them, not the
     invite call's response code)
   - `auto-join (sign in)` — nothing to grant; they land on first sign-in
   - `n/a` — the run has no product on that surface
   - **`NOT DONE — <reason> — owner: <who>`** — anything else. There is no `blocked:` status: an
     ungranted surface is outstanding work, not a state to file.

   **If any surface is NOT DONE, the skill's verdict is NOT DONE.** Say so first, before the
   granted list, and carry that into any outbound message — "access is set up" is false while one
   remains. End with the exact links to hand each person + the one sign-in action they must do.

## Guardrails

- **Idempotent + isolated.** Re-runnable; process one person at a time; a read-back is the success
  signal (invite endpoints can redirect identically on success/failure).
- **Never tell anyone their access is set up until you have read it back.** "You'll see a pending
  invite — accept it" is a claim about system state; verify it (`GET .../members`, and for a
  pending invite note there is **no** list endpoint, so you can only assert what you just created
  and got a token back for). An unverified access claim sends the person hunting for something that
  isn't there and costs a full round-trip. This is the `agent-turn-review` done-claim rule applied
  to grants. (Origin: 2026-07-23, dimagi-internal/ace#913.)
- **Never provision accounts.** Grant membership only; the person does their own first sign-in.
- **External domains are deliberate, not default.** An external add is an explicit choice surfaced
  in the approval step, never silent — Connect/ace-web both treat non-Dimagi domains specially.
- **Least privilege.** A reviewer gets exactly what reviewing needs: ace-web `editor` (confirming,
  changing and commenting on decisions needs editor; `viewer` is read-only since ace-web adopted
  canopy's owner/admin/editor/viewer ACL, 2026-10-08), Connect `viewer`, HQ `App Editor`. Never
  owner/admin unless asked.

## Related skills
- `feedback-ledger` — captures the reviewer's feedback and renders where each item went. It models
  **comments**; edits made under a `writer` grant are a channel it does not yet capture (ace#1335).
- `run-surface-audit` — gate the whole external review surface (links, payload contract,
  confidentiality, published-document rendering, and the rendered page) before you share access.
  `run-surface-audit-eval` is its judged half.
- `add-org-member` — the internal-only (@dimagi.com) Connect-org add; this skill is the superset
  that also covers ace-web + external collaborators + the other surfaces.
- `inbox-triage` — the per-sender isolation discipline this skill borrows for per-person grants.
