---
name: kelly-email
description: Busabase AirApp-first email inbox-zero operator for reviewing unread mail, drafting replies, approving archive/mark-read/send actions, and executing only explicitly approved mailbox changes across configured accounts. Use when the user invokes $kelly-email, asks to process unread email, configure an email account, generate or review an approval batch, execute approved email decisions, or reach inbox zero.
metadata:
  category: comms
  tags:
    - risk:gated-write
    - surface:busabase
    - surface:imap
    - surface:smtp
  busabase:
    # Opt in as an installable template. Explicit, never inferred from the
    # directory's shape: publishing one means accepting that installers run
    # this app's code and feed this file to their agent.
    template: true
    folderSlug: kelly-email
    # Each key names a Base under content/. The validator checks they exist, so
    # a manual can never describe a table the package does not ship.
    resources:
      - reviews
      - contacts
      - settings
    risk: gated-write
---

# Kelly Email

## Product Contract

Kelly Email is a Busabase Cloud App-in-Skill. Its canonical product surface is the AirApp in Busabase, not a separate local-data product and not a chat-only review mode. The same Hono source supports an explicitly requested local preview with OAuth connection bootstrap.

The system has two deliberately separate sides:

- The AirApp is the human review desk. It reads settings and review rows, shows sanitized account context, and writes reviewable ChangeRequests for human decisions.
- The trusted skill process scans IMAP, drafts replies, applies explicitly approved IMAP/SMTP actions, and writes execution outcomes.

The AirApp must never scan mailboxes, send mail, archive, mark read, delete, label, approve a ChangeRequest, or merge a ChangeRequest. An AirApp decision only proposes a Busabase change. The trusted process remains the sole owner of mailbox side effects.

Default behavior is AirApp-first. Unless the user explicitly asks only for explanation or configuration help, update the Busabase batch and give the user the clickable AirApp URL. Start localhost only when local preview/debugging is explicitly requested; it uses the same Busabase resources and never offers another data provider.

## Busabase Resources

All durable state belongs to the declared resources under the Kelly Email Folder:

- `kelly-email-reviews-v3`: structured email review rows, drafts, decisions, and execution outcomes.
- `kelly-email-contacts-v3`: structured derived contacts.
- `kelly-email-settings-v3`: non-secret account configuration, Vault reference names, agent lock, and scan state.
- `kelly-email-files-v3`: email HTML and attachment artifacts.
- `busabase:vault/kelly-email`: IMAP/SMTP secret values.

The last resolved Space and resource IDs live in `app/resource-map.json` and `app/app/js/config.js`. Treat them as scoped hints for that Space, not global identity. A local OAuth preview selects its Space before any resource access; deployed AirApp uses its ambient Space. On `NOT_FOUND`, discover the declared root slug with ownership metadata and lazily provision within the selected Space.

The app lazily materializes its declared Folder, Bases, and Drive when they are absent. It must verify ownership metadata (`appId`, `resourceKey`, `schemaVersion`) before adopting an existing same-slug node. A mismatch is a conflict, never permission to overwrite or move somebody else's resource.

Configuration is the `kelly-email-config` record in Email Settings. Its `payload` field follows `config.example.json`. Store only non-secret settings and Vault reference names in the record. Never store secret values, OAuth tokens, API keys, cookies, or passwords in a Base, Drive, source file, chat, screenshot, log, or execution report.

Busabase authentication is ambient inside the deployed AirApp, which must not show OAuth, API-key, Base URL, provider, hosting, or Space controls. Standalone loopback preview uses browser OAuth without exposing tokens; after OAuth it auto-selects a single/open-source Space or requires a native selector when several Spaces are accessible. It performs no app-resource read or initialization before selection. Agent-side Busabase tooling uses the user's existing credentials and explicit target Space. Mailbox credentials are resolved from authorized Vault references only.

## Runtime Contract

The canonical app project is `app/` and follows the Busabase AirApp runtime contract:

- Hono server with vanilla HTML, CSS, and JavaScript.
- `app/package.json` has exact `start: node server.js`.
- Exact-pinned latest supported `busabase-sdk`.
- No React, Vite, bundler, build step, local JSON provider, local handoff files, or alternate local product mode.
- Browser assets live under `app/app/` and use relative asset URLs.
- Persistent config and state flow through `busabase-sdk`; filesystem reads are only for packaged static assets.

When changing the product, update the canonical `app/` source first and submit an AirApp ChangeRequest in Busabase. Do not approve or merge that AirApp CR unless the user explicitly identifies and authorizes it. Return a clickable Inbox review URL.

## UI Contract

Preserve the established approval-desk layout and visual quality:

- Desktop uses a stable sidebar, dense list, and detail pane.
- Mobile uses one-column navigation with explicit list/detail transitions and no horizontal overflow.
- The top of the sidebar explains what needs human attention; primary filters are `All`, `Needs Review`, `Approved`, `Done`, and `Blocked`.
- Categories are badges on messages, not primary navigation.
- `Help & Settings` contains Guide, Files, Accounts, Profile, Style, Knowledge, Config, and appearance controls.
- Onboarding is a full-screen readiness gate showing declared resources, Settings configuration, and Vault reference readiness. It never asks users to copy IDs or create nodes manually.
- Show original email text. If operator and sender languages differ, add translation as a separate helper instead of replacing the original.
- Use a stable `Review #n` per current batch so chat edits such as “改 2” resolve unambiguously.
- Keep human input lightweight: one review note, plus an editable draft only when a draft exists or a send decision is being reviewed.
- Poll state automatically, but do not redraw while the user is editing a non-search input.

Screenshots in `assets/screenshots/` define the expected product character. Refresh them when a material UI change is merged.

## Operating Rules

- Require explicit approval before reading or processing a live email batch. Invoking the skill alone is not approval.
- Declare accounts, folders/labels, unread-only scope, time window or query, review quota, intended actions, cleanup policy, identity rules, and stop condition.
- Require separate explicit approval before every send or mailbox-changing action unless the user granted a precise standing approval for low-risk cleanup within the batch.
- Treat every message as sensitive. Quote only what is necessary and never expose unrelated thread contents.
- Track account, mailbox group, original recipient, sender, thread/message identifiers, received time, category, risk, status, and next action.
- Separate physical mailboxes from outbound identities. Select `reply_as` from original recipient, thread history, brand/product, customer domain, and customer language. Ask when ambiguous.
- Deduplicate aliases that reach the same physical mailbox using Message-ID/thread headers and `mailbox_group_id`.
- Never assume a universal Archive folder. Resolve archive targets from each mailbox's category/risk routing. If no target is configured, block and ask.
- Use configured knowledge before making product, pricing, billing, legal, security, roadmap, or policy claims. Ask when evidence is missing.
- For Chinese operators, use Chinese for operator-facing notes and UI recommendations; preserve customer text and reply in the customer's language when clear.

## Batch Approval Gate

Before reading live mail, propose:

```text
Batch plan:
- Accounts:
- Scope: unread support threads
- Folders / query / time window:
- Review quota:
- Auto-cleanup policy:
- Actions: triage / draft / prepare send-ready / execute approved
- Stop condition: one batch / account done / user stops
- Identity rules:

Please approve before I process this batch.
```

Allowed before approval: explain workflow, inspect declared Busabase readiness, prepare a configuration ChangeRequest, propose a batch, and ask non-secret clarifying questions.

Not allowed before approval: search/read/summarize/classify live mail, open attachments, draft from live mail, send, mark, archive, delete, label, unsubscribe, or move messages.

After triage, the AirApp is the approval surface. For each proposed action show the review reference, account, subject, reply identity, action, customer-visible draft or mailbox mutation, and risk. “Approve all” applies only to the exact latest visible proposal set.

## Onboarding

Before a scan, verify:

1. Declared Folder, Reviews Base, Contacts Base, Settings Base, and Drive exist and match ownership metadata.
2. Email Settings contains a `kelly-email-config` record with at least one mailbox.
3. Every IMAP/SMTP endpoint names a Vault reference.
4. The trusted runtime can resolve all referenced Vault secrets.

If resources are absent, use lazy provisioning. Do not ask the user to hand-create nodes or paste IDs.

If account configuration is absent, collect only non-secret details: mailbox address, aliases, IMAP/SMTP host/port/security/username, folders, mailbox group, outbound identities, display names, routing rules, profile, brands, URLs, style, and knowledge sources. Create a reviewable record CR in Email Settings based on `config.example.json`.

If secrets are absent, name the exact Vault keys to add. Never ask the user to paste the values into chat.

Do not scan mail until onboarding is ready.

## Inbox-Zero Workflow

1. Verify onboarding and propose the bounded batch plan.
2. Wait for explicit approval.
3. Write the Busabase agent lock and clear it in `finally`.
4. Run `scripts/generate_review_batch.ts` for the approved scope. Use `--mailbox <mailbox-id>` to limit secret checks and reads to one physical mailbox, and `--recipient <email>` when the support identity shares a mailbox with aliases; the recipient filter is applied by IMAP before message bodies are downloaded. It writes Reviews/Contacts/Settings/Drive through the provider.
5. Treat its rule classification as a conservative prefilter, not final judgment.
6. Perform an Agent Semantic Classification Pass using the message, thread context, taxonomy, account rules, and user preferences.
7. Correct keyword false positives and write `classification_method: agent_review` with concise evidence and confidence.
8. Give every Needs Review item a brief: background, why it needs review, and a recommended next step.
9. Return the clickable AirApp URL and wait for the user to review.
10. When asked to execute, run `scripts/execute_ui_decisions.ts`. Read only materialized, explicitly approved decisions; use `--dry-run` when unsure.
11. Apply only approved IMAP/SMTP actions and write an execution report to Reviews.
12. Summarize executed, blocked, failed, and remaining work.

The scan script is a trusted producer and may auto-merge its own review/contact/lock/scan-state records. AirApp writes are always review-first. A decision that is still in an unmerged CR is not approval and must not be executed.

## Classification And Quota

Default goal: all unread support-related threads in approved accounts. Every thread ends as one of:

- `reply_needed`
- `escalate`
- `waiting_on_customer`
- `waiting_on_user`
- `no_reply_cleanup`
- `not_support`

Default scan stops when Needs Review reaches 5 or no in-scope unread mail remains. Low-risk notifications may continue within an explicitly approved cleanup policy and do not consume the review quota.

Always surface real customer intent, money, refunds, billing disputes, access problems, complaints, sales/partnership, privacy/security, unresolved technical alerts, attachments, course/homework/feedback, and unclear messages from real people.

Do not infer high risk from isolated keywords or tracking parameters. Judge sender, subject, visible intent, thread context, and requested action together.

After cleanup, report total, counts by category, and a compact list with account, UID/message identifier, sender/domain, short subject, and reason. Scan audit state belongs in the `kelly-email-scan-state` Settings record, never a local cache.

## Decision Semantics

Supported decisions are defined in `references/batch-schema.md`, including archive, mark read, draft reply, send reply, keep unread, no action, needs review, and revise.

- `draft_reply` is an approved agent task, not a mailbox mutation. After drafting, return the item to Needs Review for wording approval.
- `archive` and `mark_read` may execute after the corresponding materialized AirApp approval unless `risk_policy.block_by_default` explicitly requires another override.
- `send_reply` always requires an explicit materialized send decision and a non-empty approved draft. Broad cleanup approval never authorizes sending.
- Preserve `In-Reply-To` and `References` headers. Include only a short relevant quote unless the user requests a clean reply.
- When archiving after send, use the configured category/risk folder and mark read; never hardcode Archive.

## Reply Quality

Write customer replies for minimal editing:

- Lead with the answer or useful conclusion.
- Use short paragraphs and only useful bullets.
- Do not repeat the request unless clarity requires it.
- Include only relevant links, caveats, contacts, and next steps.
- Keep routine support to 60-120 words, sales/customer replies to 100-180, and complex technical replies to 180-300 with a short summary first.
- For angry customers or escalation, acknowledge briefly and state the next step without over-explaining.
- Do not promise refunds, discounts, custom work, roadmap dates, legal/compliance outcomes, or security conclusions without evidence and approval.

For coupon or broken merge-tag replies, include the verified code and CTA URL. If either is unavailable, ask before sending.

## References

- Read `references/inbox-accounts.md` for account routing, aliases, labels, and per-account rules.
- Read `references/support-taxonomy.md` for classification, priority, and reusable support notes.
- Read `references/batch-schema.md` before changing review fields, workflow states, or decision semantics.
- Use `config.example.json` as the Settings Base payload template, never as a configured mailbox and never as a place for secret values.
