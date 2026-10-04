---
name: kelly-campaigns
description: Outbound email-marketing desk (Busabase App-in-Skill) for building segments, drafting campaigns, newsletters, and sequences, running pre-send deliverability and subject-line QA, and approving every send before it is scheduled. Structured around the SEND discipline — Setup, Engage, Nurture, Deliver — with an email-quality-auditor gate (EQS score + SHIP/FIX/BLOCK verdict). Use when the user invokes $kelly-campaigns or /kelly-campaigns, or mentions email marketing, campaigns, newsletters, drip/welcome/win-back sequences, broadcasts, segments, subject-line A/B tests, deliverability (SPF/DKIM/DMARC/spam score/inbox placement), or wants to review and approve marketing email before it is sent. This is OUTBOUND marketing to a subscriber list, distinct from kelly-email inbox triage (incoming mail). 出站邮件营销：策划分群、起草营销活动 / 新闻邮件 / 邮件序列，发送前做可送达性与主题行质检，人工审批后再排期发送。
metadata:
  category: marketing
  tags:
    - risk:gated-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-campaigns
    resources:
      - segments
      - sends
      - suppression
      - settings
    risk: gated-write

---

# Kelly Campaigns

## Overview

Kelly Campaigns is a Busabase Cloud App-in-Skill. Its canonical product
surface is the AirApp in Busabase, not a separate local-data product. The
same Hono source supports an explicitly requested local preview with OAuth
connection bootstrap. Use this skill as Kelly's outbound email-marketing
operator: it keeps a dashboard over audience segments, drafted **sends**
(campaign broadcasts, newsletter issues, and sequence steps), pre-send
deliverability and subject-line QA, and post-send performance. The skill
builds segments, drafts email copy, runs deliverability and quality checks,
and prepares sends; the human reviews, edits, and approves each send in the
app **before anything is scheduled or sent**.

This is **outbound marketing to a subscriber list**. It is distinct from
`kelly-email`, which triages an incoming inbox. Keep them separate:
`kelly-email` is about mail you received; `kelly-campaigns` is about mail you
send to many people.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, update Busabase directly and give the user the clickable AirApp
URL. Start localhost only when local preview/debugging is explicitly
requested; it uses the same Busabase resources and never offers another data
provider. Use chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar; in that mode present numbered sends (`Send #1`) and take verdicts in the conversation.

This skill is an implementation of the **App-in-Skill** pattern — a Codex/agent skill paired with a small companion UI for review and approval. See the spec paper: <https://mr-kelly.github.io/research/app-in-skill-specification-for-pairing-agent-skills-with-a-local-companion-ui.pdf>.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-campaigns-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and
product contracts, stop before the unavailable Busabase operation, and report
the exact missing dependency. Do not invent a second data backend.

## The SEND Discipline

Work is organized around four phases. Every send is tagged with the phase it belongs to, and the app groups by phase.

- **Setup** — the sending foundation: authentication and deliverability, audience segments, list growth, list hygiene.
- **Engage** — the creative: email copy, subject lines, HTML render / dark-mode, dynamic personalization.
- **Nurture** — the lifecycle: sequences (welcome, drip, win-back), newsletter cadence and monetization, preference/frequency management, reactivation.
- **Deliver** — getting it into the inbox: send experiments (A/B), inbox-placement monitoring, cold outbound, and the pre-send quality gate.

### Capability taxonomy (16 sub-skills)

| Phase | Sub-skills |
| --- | --- |
| **Setup** | `deliverability-qa` · `list-segment-builder` · `list-growth-designer` · `list-hygiene-monitor` |
| **Engage** | `email-creative-builder` · `subject-line-lab` · `email-render-builder` · `dynamic-content-personalizer` |
| **Nurture** | `email-sequence-designer` · `newsletter-monetization-planner` · `preference-frequency-manager` · `reactivation-specialist` |
| **Deliver** | `send-experiment-designer` · `inbox-placement-monitor` · `cold-outbound-sequencer` · **`email-quality-auditor` ⛩ (the quality gate)** |

### The quality gate — `email-quality-auditor` ⛩

Before any send can be scheduled, it passes the **SEND** framework, which produces an **EQS** (Email Quality Score, 0–100) and a **SHIP / FIX / BLOCK** verdict:

- **S — Sender & auth**: SPF, DKIM, DMARC pass; correct from-identity.
- **E — Engagement risk**: segment quality, expected open/complaint behavior, re-permission for cold/lapsed lists.
- **N — Not spammy**: spam score, trigger words, link/image balance, working unsubscribe + physical address.
- **D — Deliverability**: inbox readiness against policy floors, IP/domain warm-up, render and dark-mode.

Verdicts: **SHIP** (ready to schedule), **FIX** (deliverable but revise first), **BLOCK** (hard stop — e.g. failing DKIM or a spam score above policy). The gate never sends; a human still approves. A send whose deliverability risk is `high` (SPF/DKIM/DMARC failing, spam score ≥ 5, or inbox readiness below 0.6 — see `deliverabilityInfo()` in `content/kelly-campaigns-app/app/js/campaigns-model.js`) is refused scheduling even if it carries an `approved` status.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Campaigns overview"></td>
    <td width="50%"><img src="assets/screenshots/campaigns.webp" alt="Kelly Campaigns queue"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Send calendar plus list health — subscribers, bounce, churn, and complaint rates.</td>
    <td><strong>Campaigns</strong><br>Draft and approval queue across campaigns, newsletters, and sequence steps.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/deliverability.webp" alt="Kelly Campaigns deliverability QA"></td>
    <td width="50%"><img src="assets/screenshots/performance.webp" alt="Kelly Campaigns performance"></td>
  </tr>
  <tr>
    <td><strong>Deliverability</strong><br>Pre-send QA — SPF/DKIM/DMARC, spam score, and the EQS SHIP/FIX/BLOCK gate.</td>
    <td><strong>Performance</strong><br>Open, click, and unsubscribe rates by campaign.</td>
  </tr>
</table>

## Boundary

- The skill may build segments, draft sends, run deliverability/quality checks, and write it all to Busabase.
- The AirApp reads and writes Busabase records only. It must never send email, call an ESP, mutate a subscriber list, or perform any other external side effect.
- Sending is always approval-required (outbound + volume). Real scheduling/sending is performed by the configured ESP by the skill, only after the user approves the specific send in the app or in chat. `scripts/execute_decisions.mjs` only marks an approved send `done` in Busabase and reports the handoff operation the ESP still needs to perform; it performs no sending itself.
- Treat subscriber data as sensitive. Never commit real subscriber lists, ESP credentials, or Busabase credentials.

## Busabase Resources

Four Bases under one application Folder (`kelly-campaigns`), declared in
`content/kelly-campaigns-app/app/js/config.js` and the generated template sidecars under `content/`:

- `segments`: audience segments — id, name, description, audience size.
- `sends`: the review queue — campaign/newsletter/sequence-step/cold-outbound sends: type, phase, subject/preview/body, segment + audience size, deliverability, subject A/B variants, the `quality-gate` (EQS + SHIP/FIX/BLOCK), workflow `status`, and the human verdict fields `decision-note` / `decided-at`.
- `suppression`: the consent/suppression list — recipients or whole segments removed by unsubscribe, hard bounce, or complaint.
- `settings`: one row per `kind` — `kelly-campaigns-profile` (operator/brand/ESP/from-identities/sending-policy/style-tone/list-health) and `kelly-campaigns-lock`.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/campaigns-schema.md` for
exact field shapes. Metrics, the pre-send deliverability-risk derivation, and
the consent/suppression pre-send check are computed client-side from the
`sends`/`suppression` Bases on every read — they are never stored. The EQS
score and SHIP/FIX/BLOCK verdict are authored per send by the
`email-quality-auditor` gate and stored on the record.

## First Run And Onboarding

On invocation, check the `kelly-campaigns-profile` settings row for
readiness. If it is absent, guide setup before doing real marketing work.

Ask for non-secret setup details only: operator profile (name, role, company, timezone), brand (name, homepage, unsubscribe URL), ESP provider name, from-identities (from-name/from-email/reply-to and when to use each), segments, sending policy (approval-required, daily/hourly caps, min inbox readiness, max spam score), risk keywords, and style/tone. Never ask the user to paste secret values into chat. Busabase authentication is ambient inside the deployed AirApp; ESP credentials belong to the trusted handoff process's own environment, never Busabase.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-campaigns-app dev` only when local preview/debugging is explicitly
requested.

Required app views (hash routes):

- `#/overview`: send desk. Human-attention counts, upcoming sends for the next weeks, list health (subscriber count, bounce/complaint/churn rates, avg open/click), and a SEND-phase breakdown.
- `#/campaigns` and `#/campaigns/<send_id>`: the review queue over drafted sends in workflow states `needs_review`, `changes_requested`, `approved`, `done`, `blocked`. Each item shows a stable row ref (`Send #1`), type + phase + quality-gate verdict badges, the segment and audience size, deliverability risk, subject + preview text, an editable body draft, an A/B subject picker when variants exist, a `Review note` textarea, and Approve / Request changes / Block buttons that write the verdict directly onto the send record.
- `#/deliverability`: pre-send QA table — SPF/DKIM/DMARC pass flags, spam score, inbox readiness, and the SEND verdict per send, plus the read-only suppression list, so weak auth or spammy copy is caught before scheduling.
- `#/performance`: open/click/unsub/bounce by sent campaign.
- `#/settings`: sanitized config summary — operator, brand, ESP + secret readiness, from-identities, segments, sending policy, and onboarding state. Never expose secret values.

Keep the sidebar workflow filters (All / Needs Review / Approved / Done / Blocked) as the primary nav, plus the views above.

Demo mode:

- `?demo=1` (or `?demo=overview`) opens a deterministic mock program ("Northwind Coffee") for documentation and screenshots.
- `?demo=overview`, `?demo=campaigns`, `?demo=deliverability`, `?demo=performance`, and `?demo=detail` select named mock scenes; `detail` deep-links to a send detail.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.
- Demo mode never reads or writes Busabase.

UI language: support English and Chinese chrome with `Auto` default. Keep subject lines, body copy, segment names, and drafts in their original language.

## Review Workflow

Read `references/campaigns-schema.md` before editing the app or its domain logic.

A human verdict (`approve` / `request_changes` / `block` / `revise`) writes
the new `status` plus `decision-note` / `decided-at` (and, for `approve`, the
edited `body` / chosen `chosen-variant`) directly onto the send record
through `busabase-sdk`. From a standalone local preview the write merges
immediately (trusted operator); from the deployed AirApp it creates a
pending ChangeRequest for the trusted process to merge.

## Normal Workflow

1. Detect mode. Default to App UI.
2. When Kelly asks for a campaign, newsletter, or sequence: build/refresh the relevant segment, draft the send(s) into Busabase's `sends` Base with `status: "needs_review"`, the correct `type` and SEND `phase`, a clear `reason`, risk badges, a `deliverability` object, subject variants when A/B is intended, and run the `email-quality-auditor` gate to attach `quality-gate` (EQS + verdict). Metrics, deliverability risk, and the consent/suppression check recompute automatically on every read.
3. Give Kelly the AirApp URL (or local preview URL) to review the queue, deliverability, and quality gates.
4. For a send moved to `changes_requested`, re-draft it per the review comment, re-run the gate, and write it back to `needs_review`.
5. On "schedule approved sends": run `node scripts/execute_decisions.mjs --apply` to re-read approved sends from Busabase, re-check the quality gate/deliverability risk/suppression list, and mark each `done`. Then perform the actual scheduling/sending through the configured ESP with the approved, possibly user-edited body and chosen variant, one send at a time.
6. Never schedule a send without an explicit `approve` decision, never schedule one whose gate is `BLOCK` or whose deliverability risk is `high`, and never re-schedule sends already recorded as scheduled/sent.

## Safety Defaults

- Treat every outbound send as approval-required (outbound + volume). Money offers, compliance-sensitive copy, cold outbound, and high send volume raise the bar further.
- A `BLOCK` verdict or `high` deliverability risk is a hard stop; fix authentication or copy before the send is eligible.
- Store only the minimum content needed for review; keep raw subscriber lists and PII out of Busabase (segments carry names + sizes, not rows).
- Redact the ESP API key and any credential-like strings from logs, reports, and UI state; expose only boolean readiness for configured env vars.
- Keep stable ids (`send_id`, `segment_id`) and `ref` numbers so repeated updates and executions are idempotent.
