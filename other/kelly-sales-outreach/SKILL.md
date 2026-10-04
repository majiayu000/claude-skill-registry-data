---
name: kelly-sales-outreach
description: Run a Busabase-backed sales prospecting and first-touch outreach desk with a bundled Hono App-in-Skill deployable to AirApp. Use whenever the user invokes $kelly-sales-outreach or /kelly-sales-outreach, wants to enter a product or service and discover its ideal customers, asks to continuously find target accounts or public business contacts, needs evidence-based ICP scoring and personalized outreach drafts, or wants to review and send cold outreach safely. Four subcommands - setup, profile, research, send - plus the desk itself. Every first-touch message requires human approval; one company receives one initial email; guessed addresses, purchased lists, secret exposure, automated spam, and unreviewed external sends are forbidden.
metadata:
  category: sales-crm
  tags:
    - risk:gated-write
    - surface:busabase
    - surface:smtp
  busabase:
    template: true
    folderSlug: kelly-sales-outreach
    resources:
      - profile
      - companies
      - leads
    risk: gated-write

---

# Kelly Sales Outreach

Turn one product or service description into a repeatable customer-development
loop: infer the best initial ICP, find companies showing relevant business
signals, identify one public business contact, draft a message grounded in those
signals, and let the human approve every first touch.

## Subcommands

| Invocation | What to do |
| --- | --- |
| `/kelly-sales-outreach setup` | Create or adopt the Busabase Folder and three Bases, then verify them. |
| `/kelly-sales-outreach profile` | Read product/service material, store the offer, derive an explicit ICP hypothesis, and optionally build a factual one-page PDF. |
| `/kelly-sales-outreach research` | Discover and qualify target accounts and public business contacts, then draft one personalized first-touch email per company. |
| `/kelly-sales-outreach send` | Configure the seller's mailbox in Vault and send only the individually approved queue. |
| `/kelly-sales-outreach` | Open the desk and report the current bounded next step. |

Run `setup`, `profile`, `research`, then `send` the first time. Afterwards,
`research` repeats by period. Never repeat a first-touch email to a company that
is already `queued`, `sent`, or `opted-out`.

## Dependencies

Before changing the app:

1. Read `$kelly-app-skill-creator` for product behavior, responsive UI, and the canonical `content/kelly-sales-outreach-app/` artifact.
2. Read `$busabase` for target Space, ChangeRequests, review, merge, and Vault behavior.
3. Read `$busabase-app-creator` for runtime, SDK, security, validation, and AirApp deployment.
4. Read `references/sales-outreach-schema.md` before changing fields, statuses, or Vault keys.
5. Read `references/research-playbook.md` before running research.

If a dependency is unavailable, finish deterministic local artifact work but
stop before its Busabase or AirApp operation and name the missing dependency.
Never introduce a second backend.

## Product Boundary

- **The minimum input is the offer.** Onboarding requires only `offer-name` and
  `offer-summary`. Do not force the user to know their ICP before the research
  loop begins; propose it from the offer and evidence, then let them edit it.
- **One company, one initial thread.** Multiple public contacts are fallback
  candidates, not permission to blast several people at one company.
- **The human approves every first touch.** App approval changes `draft` to
  `queued`; it does not itself send. The trusted script is a separate explicit
  execution step.
- **Every company and contact carries provenance.** Require an exact public URL.
  Never generate likely address patterns or import purchased/scraped private
  lists. If no address is verifiable, keep the account blocked.
- **Honor opt-out immediately.** `opted-out` is terminal for outreach. The
  sender re-reads status immediately before sending and stops on opt-out,
  already-sent, or non-queued state.
- **Use truthful personalization.** Drafts may mention only stored offer claims
  and observed company signals. Do not invent urgency, customer logos, metrics,
  relationships, or research that did not happen.
- **Secrets stay trusted.** SMTP values live in Vault or runtime environment and
  never reach browser source, logs, screenshots, or chat.
- **Stay within lawful public access.** Do not bypass authentication, paywalls,
  robots controls, rate limits, or platform terms. Do not impersonate a person.

## `/kelly-sales-outreach setup`

```bash
node scripts/setup.mjs
node scripts/setup.mjs --apply
```

Confirm the Space first. Setup is idempotent and resolves resources from the
declared Folder; nobody copies Node IDs into config. Re-read after every
ChangeRequest and report a pending CR rather than claiming the workspace exists.

## `/kelly-sales-outreach profile`

Accept whatever the user has: website, deck, proposal, product notes, service
menu, or a short description. Extract facts and ask only for a missing fact that
materially changes targeting.

Store:

- offer name and plain-language summary;
- value proposition and verifiable proof points;
- target industries and regions;
- likely buyer roles;
- an explicit ideal-customer hypothesis covering size, stage, pain, trigger,
  exclusions, and why this offer wins now;
- public research channels;
- optional collateral filename and sender address.

Distinguish **facts** supplied by the user from **hypotheses** inferred by the
Agent. Put uncertainty into the ICP text instead of presenting it as known.
Never fabricate proof. When useful, generate a factual one-page asset:

```bash
node scripts/build_one_pager.mjs
node scripts/build_one_pager.mjs --apply
```

The dry run writes HTML. `--apply` renders `collateral/<offer>-one-pager.pdf`
and records the filename. The file is optional for sending.

## `/kelly-sales-outreach research`

Research in bounded rounds of 20-30 accounts. Use the offer profile to form a
testable ICP, then seek companies with observable signals rather than merely
matching industry keywords.

For every company record:

- canonical name, key, website, industry, region, and approximate size;
- exact company source URL;
- ICP score and a concrete match reason;
- observed pain/buying signals and capture date;
- evidence type: `first-party`, `public-directory`, or `market-signal`;
- one concise, plain-text first-touch subject/body grounded in that evidence.

For every contact record:

- company key, valid business email, optional public name, buyer role;
- exact public source URL and confidence;
- no guessed email patterns.

Use `references/research-playbook.md` for score calibration, sources,
personalization, and failure handling. Import is idempotent:

```bash
node scripts/import_leads.mjs findings.json
node scripts/import_leads.mjs findings.json --apply
```

Do not overwrite existing company rows. This preserves approvals, sends,
opt-outs, edits, and stable `#n` references.

## `/kelly-sales-outreach send`

Configure the user's own mailbox. Never ask for a mailbox password in chat;
use an app password/authorization code through `SMTP_PASS` or `--pass`.

```bash
SMTP_PASS=xxx node scripts/configure_smtp.mjs --host smtp.example.com --user seller@example.com --apply
node scripts/send_emails.mjs
node scripts/send_emails.mjs --test-to seller@example.com --apply
node scripts/send_emails.mjs --apply
```

The dry run prints sender, optional collateral readiness, SMTP readiness by key,
and exact recipients without printing secret values. `--test-to` sends one
approved message to an inbox the user controls and writes nothing to Busabase.

For each real send, re-read the account immediately before `sendMail`. Require:

- current status exactly `queued`;
- no `sent-at` and no `opted-out-at`;
- exact approved recipient, subject, and body;
- SMTP readiness;
- configured collateral exists, if a filename is present.

On success write `sent` and `sent-at`. On failure leave it queued and report the
company-specific error. Never silently retry in a way that can duplicate mail.

## Operating Loop

### Research

Run by explicit request or agreed period. Store capture date, source, coverage,
and uncertainty. Deduplicate by company key and company/email pair.

### Plan

Rank first-party evidence before directory evidence, then ICP score. The desk
gives stable `#n` references and lets the human edit recipient, subject, and
body. Missing evidence/contact/draft is blocked, not guessed.

### Action

Human approval queues one exact first touch. The trusted sender performs the
external side effect with duplicate prevention and records the result.

### Retrospective

When the user supplies replies, meetings, conversions, objections, or opt-outs,
compare outcomes with the stored ICP and signals. Propose changes to profile,
score weights, sources, and copy as reviewed updates. Do not silently rewrite
targeting rules from a single outcome. Automated follow-up sequences and inbox
reply ingestion are out of scope for v1.

## App Contract

- Keep the canonical Hono project in `<skill-root>/content/kelly-sales-outreach-app/`; use the same source
  locally and in AirApp.
- Store persistent profile, accounts, contacts, decisions, and execution state
  only in Busabase through `busabase-sdk`.
- Local OAuth appears only in an explicitly requested standalone preview;
  hosted AirApp uses its ambient Busabase session.
- Browser writes go through ChangeRequests and may auto-merge only in a
  standalone local runtime.
- Demo data is explicit, deterministic, non-persistent, and cannot send.
- Keep the desktop sidebar/list/detail shell, true mobile list/detail flow,
  hash routes, and responsive Help & Settings from the creator contract.

## Resources

| Resource | Purpose |
| --- | --- |
| `kelly-sales-outreach-profile` | One offer, ICP hypothesis, proof, research channels, optional collateral, sender address, onboarding version, and Vault reference names. |
| `kelly-sales-outreach-companies` | Target accounts with source evidence, pain signals, first-touch draft, review state, recipient, and send/opt-out timestamps. |
| `kelly-sales-outreach-leads` | Public business contacts with company key, name/role, source URL, and confidence. |
| Vault `SMTP_*` | Mail transport values readable only by trusted execution. |

## Screens

- `#/profile` — product, service, proof, ICP, channels, optional collateral,
  sender, and SMTP readiness.
- `#/all`, `#/to-send`, `#/sent` — account list/detail queue with evidence,
  contacts, editable draft, and exact approval action.
- `#/settings/<tab>` — commands, guide, resources, and connection.

## Stop Conditions

Stop rather than guess when the offer is missing; a company or contact lacks a
public source; an address is inferred; a company is already sent or opted out;
the draft contains unsupported claims; SMTP is unavailable; an explicit
collateral file is missing; the target Space is ambiguous; or the required
review/deployment dependency is unavailable.
