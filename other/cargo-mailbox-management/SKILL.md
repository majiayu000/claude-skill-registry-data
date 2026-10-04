---
name: cargo-mailbox-management
description: "Send mail from inboxes Cargo owns — provision mailboxes on a sending domain, run provider warm-up and the 5→40/day send ramp, deliver with the `sendEmail` action, and read back threads, replies, delivery events, and the workspace suppression list. Triggers: \"set up a sending mailbox\", \"provision inboxes for outbound\", \"warm up this mailbox\", \"how many sends do I have left today\", \"send this from Cargo\", \"did they reply\", \"who unsubscribed\", \"suppress this recipient\", \"take me off your list\", \"never email them again\", \"what do mailboxes cost\", \"my mailbox is stuck pending\". A mailbox is a recurring monthly credit charge, and every send is gated on basis, suppression, and relevance. Skip when: writing the copy or building the audience — use cargo-gtm; the mailbox belongs in git — use cargo-project."
version: "1.2.0"
compatibility: Requires @cargo-ai/cli (npm). Sign in or create an account with `cargo-ai login --email` (emailed code, no browser), `--oauth`, or an API token
homepage: https://github.com/getcargohq/cargo-skills
metadata:
  author: getcargo
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/cargo-skills
---

# Cargo CLI — Mailbox Management

**Mailboxes.** A mailbox is a real sending inbox the workspace **owns** — provisioned through
Cargo on a sending domain the workspace also owns, with SMTP and IMAP credentials Cargo holds
and uses to deliver outbound mail and to read the replies that come back. Two things follow,
and both are easy to get wrong: a mailbox is a **recurring monthly credit charge** rather than
a per-record one, and this domain does **not** send. It provisions the inbox, ramps it, and
reports on what it did; the send itself is the `sendEmail` action, under
[`cargo-orchestration`](../cargo-orchestration/SKILL.md).

```bash
cargo-ai mailboxManagement mailbox      …   # provision, warm-up, send allowance
cargo-ai mailboxManagement message      …   # outbound sends
cargo-ai mailboxManagement thread       …   # conversations, and the replies on them
cargo-ai mailboxManagement event        …   # sent / opened / clicked / replied / unsubscribed
cargo-ai mailboxManagement suppression  …   # workspace-wide do-not-send list
cargo-ai mailboxManagement pricing      …   # monthly credits per mailbox flavour
```

> **Version note.** Everything on this page is live in the pinned CLI (1.0.66), including
> `mailbox get-warmup-stats` and the `--daily-target` default of 40 — both of which were
> merged-but-unpublished when this skill was written. On an **older** CLI, `--daily-target`
> reads "provider default if omitted" and `get-warmup-stats` **silently prints the `mailbox`
> group help instead of erroring**, so a missing subcommand here looks like a usage mistake
> rather than a stale install. `cargo-ai mailboxManagement mailbox --help` lists what your CLI
> actually has; re-run the session refresh in [`../cargo/SKILL.md`](../cargo/SKILL.md) to catch up.

## Bootstrap

Already signed in (`cargo-ai whoami` returns a workspace)? Skip to the next section.

```bash
npm install -g @cargo-ai/cli            # no global install? prefix every command with `npx @cargo-ai/cli`
cargo-ai login --email you@company.com  # emailed code, no browser; creates the account on first use
                                        # alternatives: --oauth (browser) · --token <api-token> (CI)
cargo-ai whoami                         # confirm the active workspace before any write
```

Every command prints JSON to stdout; failures exit non-zero with `{"errorMessage": "..."}`.
Nothing in this domain is asynchronous — every command is a single HTTP call, so there is no
run to poll (the one thing that *looks* async, a freshly created mailbox sitting at `pending`,
is polled with `mailbox refresh-status`, not with `run get`). Mailboxes are guarded by
`mailboxManagement:read` / `mailboxManagement:write` permissions, which an admin and an editor
both hold and a viewer does not; if a create or update returns a permission error, the token is
read-only ([`../cargo-workspace-management/SKILL.md`](../cargo-workspace-management/SKILL.md)).
When the full skill bundle is installed, [`../cargo/references/prerequisites.md`](../cargo/references/prerequisites.md)
adds the CLI version pin, token scopes, and the admin-only surface.

## Before any send — three checks

**This is a blocking gate, not advice.** Cargo owning the mailbox changes who presses send; it
changes nothing about whether the message should be sent. The canonical rules are
[`../cargo-gtm/references/acceptable-use.md`](../cargo-gtm/references/acceptable-use.md) §3 and
they apply here unchanged — run all three before the first `sendEmail`, not after:

- **Basis** — which permission covers this audience (customers, opted-in contacts, event
  attendees, or a documented legitimate-interest case for a B2B role)?
- **Suppression** — subtract the workspace suppression list from the audience *before* you
  enrich or send. `suppression list` is free and this domain is the source of truth for it.
- **Relevance** — can you name, per recipient, why this message is for them?

Any check that fails is a stop-and-ask. Two obligations are specific to Cargo-owned sending:

- **The ramp is a ceiling, not a target.** `get-send-allowance` reports what a mailbox may send
  today; it is not a quota to fill. Asking to raise it, to spread one campaign across a fleet of
  fresh mailboxes to clear the same volume, or to rotate identities so filters see less from
  each, is the evasion refusal in `acceptable-use.md` §2 — not a configuration question.
- **Unsubscribes are automatic and absolute.** Every send carries a signed `List-Unsubscribe`
  header; a recipient using it writes a workspace-wide `suppression` row, and the next send to
  that address is refused by the engine. There is no removal command, and that is the point —
  never route around a suppression to re-contact someone.

## The two numbers that govern a mailbox

They look similar and mean opposite things. Confusing them is the most common way to
mis-read a mailbox's health.

| | `mailbox get-send-allowance` | `mailbox get-warmup-stats` |
| --- | --- | --- |
| Measures | **Your** real outreach | The provider's **dummy** warm-up traffic |
| Window | Rolling 24 hours | Today, UTC |
| Returns | `dailyLimit`, `sentCount`, `remainingCount` | `sentCount`, `deliveredCount`, `spamCount`, `inboxRate`, `spamRate` |
| Answers | "How many more may I send?" | "Is this inbox landing in the inbox or in spam?" |

`dailyLimit` is not a setting — it is derived from how long warm-up has been running. The
arithmetic, the `warmupStatus` transitions, and how to size a fleet against it are in
**[`references/warmup-and-allowance.md`](references/warmup-and-allowance.md)**. Read it before
you promise anyone a send volume.

## Commands

All commands output JSON. Reads need `mailboxManagement:read`; everything that provisions,
updates, deletes, or suppresses needs `mailboxManagement:write`.

### Provision a mailbox

**First, the gap you will hit.** `mailbox create` requires `--domain-uuid`, and there is no
`cargo-ai` command that lists sending domains — the `domainManagement` API exists but has no
CLI surface yet. Get the UUID from the Cargo web app, or declare the domain in a CDK repo with
`defineDomain` and read it back from `cargo.state.json`. Say this to the user rather than
guessing a UUID.

Pricing a domain before buying it has the same gap, and one direct API call closes it:
`GET /v1/domainManagement/domains/search?name=<domain>` returns `available` and `priceCredits`
(where **`null` means not purchasable, not free**). The domain side of a fleet — that call,
sizing domains by blast radius rather than capacity, the apex redirect, DMARC, naming, and why
`dnsRecords` must stay undeclared — is
**[`references/sending-domains.md`](references/sending-domains.md)**.

```bash
cargo-ai mailboxManagement mailbox create \
  --domain-uuid <domain-uuid> \
  --type google \
  --username jane \
  --first-name Jane \
  --last-name Doe \
  --signature '<p>Jane Doe · Acme</p>' \
  --folder-uuid <folder-uuid>

cargo-ai mailboxManagement mailbox refresh-status <uuid>   # repeat until status is "active"
```

- `--type` — `google`, `shared`, or `private`. **`outlook` is accepted by the flag and always
  fails** with `transportNotSupported`: the Graph transport has not shipped, so an Outlook
  mailbox cannot deliver. Pick one of the other three.
- `--username` — the local part only (`jane` for `jane@acme.com`). Lowercased; letters, digits,
  dots, dashes and underscores, 1–64 characters, starting and ending alphanumeric.
- `--first-name` / `--last-name` — the From header the recipient sees. Use a real person's name
  under a real identity; a fabricated sender is a §2 refusal.
- `--signature` — HTML, stored on the mailbox (max 10,000 characters).
- `--folder-uuid` — a folder of kind `mailbox`, from [`cargo-workspace-management`](../cargo-workspace-management/SKILL.md).

`create` returns immediately with `status: "pending"` — the provider has not issued credentials
yet. It reaches `active` when `refresh-status` says so, or on its own within five minutes; a
send attempted before then fails with `credentialsMissing`.

```bash
cargo-ai mailboxManagement mailbox list                        # every mailbox
cargo-ai mailboxManagement mailbox list --statuses active      # comma-separated, no spaces
cargo-ai mailboxManagement mailbox list --domain-uuid <uuid>
cargo-ai mailboxManagement mailbox get <uuid>

cargo-ai mailboxManagement mailbox update --uuid <uuid> --first-name Janet
cargo-ai mailboxManagement mailbox update --uuid <uuid> --folder-uuid none   # "none" clears

cargo-ai mailboxManagement mailbox remove <uuid>               # deletes at the provider too
```

- `--statuses` — `pending`, `active`, `inactive`, comma-separated **with no spaces**. An
  `inactive` mailbox was disabled by the provider; `errorCode` says why (`401` auth, `402`
  spam) and it will not send until it is fixed.
- `none` is the sentinel for "clear it" on `--folder-uuid` and `--signature`. On `list`,
  `--folder-uuid none` means "mailboxes in no folder".
- `remove` is how monthly billing stops. There is no pause.

### Warm it up

A mailbox that never starts warm-up is pinned at **5 real sends a day, forever**. Warm-up is
what moves it, and it takes 45 days to finish.

```bash
cargo-ai mailboxManagement mailbox start-warmup <uuid> --daily-target 40
cargo-ai mailboxManagement mailbox get-warmup-stats <uuid>                    # next CLI release

cargo-ai mailboxManagement mailbox update-warmup --uuid <uuid> --status paused
cargo-ai mailboxManagement mailbox update-warmup --uuid <uuid> --daily-target 25
cargo-ai mailboxManagement mailbox stop-warmup <uuid>                         # resets the ramp
```

- `--daily-target` — warm-up messages per day at full ramp, 1–40 (default 40). This is the
  provider's dummy traffic, **not** your send allowance.
- `--status` on `update-warmup` accepts the whole enum, but only `active` and `paused` do
  anything: `pending` and `failed` are states the provider reaches on its own, and `disabled`
  is what `stop-warmup` is for.
- `stop-warmup` **resets the Cargo send ramp** as well as tearing down provider warm-up — the
  mailbox drops back to 5/day and starts the 45 days over. Pause instead unless you mean it.

### Check the allowance before you send

```bash
cargo-ai mailboxManagement mailbox get-send-allowance <uuid>
# → {"allowance":{"dailyLimit":12,"sentCount":4,"remainingCount":8}}
```

Read `remainingCount` before enrolling a batch. Sends past it do not queue for tomorrow — they
fail immediately with `dailyLimitReached`, one wasted run per row.

### Read what happened

```bash
cargo-ai mailboxManagement message list --mailbox-uuid <uuid> --statuses sent,replied --limit 50
cargo-ai mailboxManagement message get <uuid>

cargo-ai mailboxManagement thread list --mailbox-uuid <uuid> --search acme
cargo-ai mailboxManagement thread get <uuid>

cargo-ai mailboxManagement event list --kinds replied,unsubscribed --occurred-after 2026-08-01
```

- **Message vs thread vs event.** A *message* is one outbound send. A *thread* is a
  conversation — its `lastEmail` and `lastEvent` are what you sort a reply queue on. An *event*
  is something that happened to a message (`sent`, `opened`, `clicked`, `replied`, `bounced`,
  `unsubscribed`). Inbound replies are events, not message rows; only outbound mail is a message.
- `--statuses` on `message list` / `thread list` is the **list** status — `pending`, `error`,
  or an event kind. `success` is not in that set: a delivered message reads as `sent` or later.
- `--kinds`, `--statuses`, `--reasons` are all comma-separated with no spaces.
- **`bounced` never fires yet.** Nothing parses delivery-status notifications, so bounces do not
  produce events and do not auto-suppress. Do not build a deliverability report that treats an
  empty bounce count as a clean list.
- `message`, `thread`, and `event` lists default to `--limit 50` (max 200) and return a `count`.
  `mailbox list` and `suppression list` have **no** default limit (max 1000), and `mailbox list`
  returns **no** `count` — see [`references/response-shapes.md`](references/response-shapes.md).

### Suppression

Workspace-wide, not per mailbox: a recipient opting out is opting out of the sender, not of one
address the sender happens to own.

```bash
cargo-ai mailboxManagement suppression list --reasons unsubscribed,manual
cargo-ai mailboxManagement suppression create --email opted-out@acme.com
```

- Reasons are `unsubscribed` (the recipient's own choice, via `List-Unsubscribe`), `bounced`,
  `complained`, and `manual`. `suppression create` always records `manual`.
- It is idempotent — suppressing an already-suppressed address returns the existing row.
- Addresses are normalised (`trim().toLowerCase()`) on both write and check, so casing and
  stray whitespace cannot slip a suppressed recipient back into a send.
- There is no `suppression remove`. That is deliberate.

### Pricing

```bash
cargo-ai mailboxManagement pricing get
# → {"monthlyCredits":{"google":125,"outlook":160,"shared":100,"private":100}}
```

Read this **live** before quoting a fleet cost — the figures above are what the workspace
returned at the time of writing, not a constant.

## Sending: the `sendEmail` action

Delivery is deliberately not in this CLI domain. It is a native orchestration action so that
sends inherit orchestration's pacing, retry, and credit machinery:

```bash
cargo-ai orchestration action execute \
  --action '{"kind":"native","actionSlug":"sendEmail"}' \
  --data '{"mailboxUuid":"<mailbox-uuid>","to":"jane@acme.com","subject":"...","bodyHtml":"<p>…</p>"}' \
  --wait-until-finished
```

- **0.1 credits per send**, fixed. The action carries no `config`; the inputs go in `--data`, like every
  other action ([`../cargo-orchestration/SKILL.md`](../cargo-orchestration/SKILL.md)).
- Optional `bodyText` (generated from the HTML when omitted), `inReplyTo`, and `references`.
- **To keep a reply threaded, send the whole chain.** `references` is every `Message-ID` in the
  thread so far, oldest first — not just the parent. Mail clients break the thread otherwise.
- The action is rate-limited **per mailbox** to that mailbox's own daily limit, spread across
  the day. A burst of 100 on a mailbox with 40 left fails the 41st immediately rather than
  parking it for a day.
- **A refused send is a node error, not a thrown exception.** `recipientSuppressed`,
  `mailboxNotActive`, and `transportNotSupported` need a human and do not retry;
  `dailyLimitReached`, `credentialsMissing`, and `deliveryFailed` retry on their own.
- **There is no dry run from the CLI.** The engine has one, but no `action execute` flag reaches
  it — the send is live the moment you run the command. Send to yourself first.

Threading, the full refusal table, and what Cargo injects into every message (unsubscribe
header, open pixel, click redirect) are in **[`references/sending.md`](references/sending.md)**.

### Reading events back from a workflow: `listEmailEvents`

`mailboxManagement event list` is the CLI read, but inside a workflow the delivery events on a
thread come from a **native action** (CLI ≥ 1.0.86), so a play can branch on whether someone
replied:

```bash
cargo-ai orchestration action execute \
  --action '{"kind":"native","actionSlug":"listEmailEvents"}' \
  --data '{"threadUuid":"<thread-uuid>","kinds":["replied","clicked"],"limit":50}' \
  --wait-until-finished
```

- `threadUuid` is required; `kinds` is optional (omit for every event on the thread) and `limit`
  defaults to **50**, capped at **200**, newest first.
- Event kinds are `sent`, `opened`, `clicked`, `replied`, `bounced`, `unsubscribed`. Note the wire
  value is **`opened`** even though the UI labels it "Viewed".
- Each event returns `uuid`, `mailboxUuid`, `messageUuid`, `threadUuid`, `kind`, `occurredAt`,
  `actorEmail`, plus nullable `url` (on `clicked`), `inboundRfcMessageId`, and `snippet`.
- **`bounced` still has no producer** — nothing parses delivery-status notifications yet, so
  filtering on it returns nothing and proves nothing. Never report an empty bounce count as a
  clean list.

## Cost discipline

This domain bills differently from the rest of the pack, and the difference is the thing to say
out loud before provisioning anything.

- **A mailbox is a monthly, recurring charge** — 100–160 credits *per mailbox, per month*, for
  as long as it exists. Five mailboxes is 500–625 credits every month, not once. `mailbox
  remove` is the only way to stop it; there is no pause. Quote the fleet size and the monthly
  credit estimate from a live `pricing get`, and get an explicit yes, before the first `create`.
- **Sends are 0.1 each**, so volume is cheap and the fleet is not. Do the arithmetic in that
  order.
- **A play or scheduled tool that calls `sendEmail` re-bills on every run** — and re-contacts
  the same people on every run, which is the §6 cadence gate in `acceptable-use.md` as much as a
  spend gate. Check `get-send-allowance` before enrolling a batch: rows past the allowance burn
  a run each and deliver nothing.
- The full spend rules — sampling before a full enrollment, the approval message, the receipt —
  are [`../cargo-gtm/references/cost-discipline.md`](../cargo-gtm/references/cost-discipline.md).

## Declarative alternative: `defineMailbox` (CDK)

For the inbox itself, **prefer CDK** — the `mailbox create` help says so, and the reason is that
a mailbox is long-lived infrastructure with a monthly cost, which is exactly what belongs in
git and in a plan you can review. `defineMailbox` (with `defineDomain` for the sending domain)
covers it; `adopt: true` binds a mailbox bought in the web app instead of provisioning a second
one. See [`../cargo-project/SKILL.md`](../cargo-project/SKILL.md) and "Declarative vs imperative" in
[`../cargo/SKILL.md`](../cargo/SKILL.md).

Use this skill's imperative commands for one-off provisioning, and for everything CDK does not
model at all: warm-up, allowance, messages, threads, events, and suppressions.

## When the CLI surprises you

If a documented flag or response shape doesn't match what you observe, re-refresh the CLI and
skills; if it still doesn't add up, file a report — it's read by the team. The missing
`domainManagement` surface is a live example: `mailbox create` needs a `--domain-uuid` that no
command can produce.

```bash
cargo-ai workspaceManagement report create \
  --title "<one-line summary>" \
  --description "<exact command(s), errorMessage verbatim, expected vs actual, UUIDs>"
```

## Presenting results

Follow [`../cargo/references/interaction.md`](../cargo/references/interaction.md): lead with the
outcome ("mailbox active, 8 of today's 12 sends left, 2 replies since Monday"), summarize a
fleet or a reply queue as a compact table, and never dump raw `mailbox get` or `event list` JSON
into the conversation. When you report a fleet, report its **monthly** cost, not a one-off one.
