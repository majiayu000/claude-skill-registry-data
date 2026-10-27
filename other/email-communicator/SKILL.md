---
name: email-communicator
description: >
  Internal ACE turn step — Send/receive email as ace@ via gog; sends go only through bin/ace-
  email.
user-invocable: false
disable-model-invocation: false
---

# Email Communicator

Send and receive email through the ACE Gmail account using the GOG CLI. This is a utility skill —
other skills delegate to it whenever they need to send or read email rather than reimplementing
Gmail access themselves.

**The send path is a rail, and approval is procedural.** Raw `gog gmail send`/`reply` under the ACE
identity is hard-blocked by a deny rail in `config/gating.json`, enforced by canopy's session gating hook
(`agent-core/gating_guard.py --session`; canopy#849) — `bin/ace-email` is the only way email leaves ACE, which also guarantees the
comms-log threadId capture. The rail never prompts; *whether* a send is appropriate is governed by
the calling context's procedure (a run's pause-point mode, a turn's review posture) — see
`docs/superpowers/specs/2026-07-01-agent-operating-model-adoption.md § Gating`.

**`bin/ace-email` and `bin/ace-mark-read` are thin shims over the shared canopy email engine**
(`canopy email send|mark-read|preflight`, canopy ≥ 0.2.255; identity from this repo's
`config/agent.json`) — fixes propagate fleet-wide, same as hal's shims (ace#826). Requires the
canopy CLI on PATH (`/canopy:setup`); the shims exit with the remediation when it's missing.

### Configuration (preamble)

The identity has ONE source of truth — `config/agent.json` (`email` = `ace@dimagi-ai.com`,
`gog_client` = `canopy`); `bin/ace-email` and the canopy engine read it from there. There are NO
`ACE_GMAIL_ACCOUNT` / `ACE_GMAIL_CLIENT` env vars any more: they were RETIRED with ace#1147 /
#1338 (ACE's Canopy vault carries no such keys), and a
`$ACE_GMAIL_ACCOUNT` in a shell command expands to EMPTY — so the account flag followed by that
var silently ran as `-a ` and failed. Write the literals.

The GOG CLI must be installed (`brew install steipete/tap/gogcli`) and the configured account must
be authenticated. **Preferred:** connect via the canopy-web "Connect Google mailbox" button —
self-service, no terminal. **Terminal alternative:** `gog login ace@dimagi-ai.com --client canopy
--services gmail,calendar,drive,docs,slides,sheets,forms` — pass the FULL scope list every time; a
narrower `--services` list (e.g. just `gmail`) **replaces** the grant and drops the other scopes
(calendar/drive/docs/slides/sheets/forms), it does not add to them.

**The gog client is SHARED across the fleet; the mailbox is what's per-agent.** Every agent
(ace/eva/hal/ada) authorizes its own address under one of the two interchangeable fleet OAuth
clients (`canopy`, `canopy-web`) — identity bleed
means acting as another agent's *mailbox*, and that is governed by `--account`, never by the
client. `config/agent.json`'s `gog_client` is the declared preference the email engine
(`canopy email`, `bin/ace-email`) reconciles. The two fleet clients (`canopy`, `canopy-web`) are one app — never type a client name; `canopy email client` picks the one this machine holds a token under. A raw gog call passes
`--client "$(canopy email client --repo .)"`. Do **not** set it to `ace`: no `credentials-ace.json` is
provisioned, so every read/send fails and the printed remedy (`gog login --client ace`) is an
interactive browser OAuth that a headless turn cannot run (jjackson/ace#1147).

## Process

1. **Resolve configuration.** The mailbox comes from `config/agent.json` (`email`); the gog
   client from `canopy email client --repo .` — never from the environment. Abort with a clear error if gog itself is
   missing.

2. **Determine the operation.** The calling skill specifies one of: **send**, **reply**, **search**,
   or **read**.

3. **For send operations:**
   - Write the body to a temp file (single-line paragraphs separated by blank lines; bullet lines
     one per line — `bin/ace-email` builds a reflowing HTML body + plain-text alternative; put the
     sign-off on its own paragraph, blank-line-separated).
   - Use: `bin/ace-email --to <recipient(s), comma-separated> [--cc <address>] --subject <subject> --body-file <path>`
   - Approval is procedural, per the calling context: in a turn or review-mode run, present the
     composed email (to/cc/subject/body) and get the human's yes before invoking; in auto-mode runs,
     the phase's pause-point governance applies. Use `--dry-run` to preview the rendered bodies.
   - **Run-page check (ace#2378):** a body that links `docs.google.com` / `drive.google.com` and no
     `labs.connect.dimagi.com/ace/` page exits 3 before canopy is called, dry-run included. Lead with
     the run's `ace_web_summary_url`; when the recipient is not a reviewer of the run —
     a thread with no run (sales/BD), or a partner-facing deliverable whose subject IS the
     Drive pack (Phase 9 `llo-onboarding`, ace#2380) — pass `--no-run-page "<why>"`, which
     is stripped before canopy and echoed to stderr.
   - Capture `message_id` and `thread_id` from the JSON result.

4. **For reply operations:**
   - Read the original thread first (step 6) to get the thread context and the thread id.
   - **Prefer `--reply-all`:** `bin/ace-email --reply-all --thread-id <thread_id> --subject "Re: <original>" --body-file <path>`
     — with `--thread-id` the engine derives To + Cc from the thread's **LATEST non-self** message's
     structured headers, so cc'd people are never silently dropped (§1b rule 3, now tool-backed).
     Explicit `--cc` merges in. Only pass `--to` yourself when deliberately narrowing the recipient
     set — and say so in the approval step.
   - **Never `--reply-all --reply-to-message-id <thread id>`** (ace#2391). A Gmail thread id IS the
     id of the thread's FIRST message, so that pair takes the engine's *message* mode and replies to
     the thread head: on a thread ACE opened it addresses `To: ace@dimagi-ai.com` and demotes the
     counterpart to Cc; on any long thread it targets whoever started it. *Enforced:*
     `test/skills/reply-all-thread-id.test.ts`.
   - Replies maintain the Gmail thread via the thread id.

5. **For search operations:**
   - Use: `bin/ace-env gog gmail search "<query>" -a ace@dimagi-ai.com --client "$(canopy email client --repo .)" --json`
     (The two fleet clients (`canopy`, `canopy-web`) are one app — never type a client name; `canopy email client` picks the one this machine holds a token under.
     The `bin/ace-env` prefix carries gog's file-keyring password, which a runner-spawned session cannot otherwise see — ace#2844.)
   - Common queries: `from:<address>`, `to:<address>`, `subject:<text>`, `in:inbox`, `is:unread`,
     `newer_than:1d` — combined with spaces.
   - Returns thread list with IDs, dates, senders, subjects.

6. **For read operations** (use the shared canopy engine, not raw `gog` — canopy ≥ 0.2.346):
   - Use: `bin/ace-env canopy email read <threadId> --repo .`
   - Returns normalized JSON: per message the headers + decoded `body_text` (quoted reply tail
     trimmed) + each attachment's `attachment_id`, PLUS a thread-level `reply_all` recipient set
     (`{to, cc, reply_to_message_id}`). Pass a **THREAD id** — gog reads threads and 404s on a
     bare message id (the multi-message-thread trap).
   - **Recipient safety is now the engine's job.** Take the reply-all set from `reply_all` (To/Cc)
     and pass it to `bin/ace-email --to <set>`, choosing reply-all vs. direct on purpose. A raw
     `gog gmail read` text dump hid `Cc:` and silently dropped cc'd recipients; the canopy reader
     is structured, so that can't happen. Download any attachment with `canopy email
     fetch-attachment <messageId> <attachmentId> --repo . --out <dir>` (see inbox-triage's File
     action). Per canopy `docs/agent-operating-model.md § 1b` reply-quality rule 5 (jjackson/ace#828).

7. **Log the operation — the routing contract.** For every send/reply, the calling skill MUST record
   `thread_id` + `message_id` + recipients + date in the run's comms-log
   (`ACE/<opp>/runs/<run-id>/<N>-<phase>/<skill>_comms-log.md`; a send that belongs to no phase logs
   at the run root instead — `release-run_comms-log.md`, ace#2780; `run-closeout_comms-log.md`,
   ace#2823). **Never log a send under the run's `comms-log/` subfolder** — that holds
   `observations.md` and `dry-run-*.md`, and routing does not search it. This is not optional bookkeeping:
   `inbox-triage` routes inbound replies to their opp/run by matching `thread_id` against comms-logs.
   A send without a logged `thread_id` produces an unroutable reply.

8. **Mark-read** (turn housekeeping, not part of normal skill sends): `bin/ace-mark-read <threadId> …`
   removes the UNREAD label after a turn fully handles a thread.

9. **Forward** — when asked to *forward* a message (a receipt, an invoice, someone's mail),
   forward it: `bin/ace-email forward <thread-id> --to <addr> [--note-file note.txt] [--dry-run]`.
   It sends the original headers, body and attachments (real filenames) under `Fwd:`; the review
   receipt is keyed to the note file. Do not compose a new message summarising the mail and
   re-attach with `--attach-from-thread` — that is not a forward (2026-10-05).

## MCP Tools Used

None — this skill uses the GOG CLI and the guarded `bin/ace-email` wrapper via shell commands, not
MCP tools.

## Mode Behavior
- **Auto:** Execute email operations directly (the phase's pause-point governance decides whether the
  send-bearing step runs at all), return results to the calling skill.
- **Review:** For send/reply, present the composed email in-conversation for human approval before
  invoking `bin/ace-email`. Search/read execute immediately.

## Dry-Run Behavior

When `--dry-run` is active:
- **Send/reply:** `bin/ace-email … --dry-run` prints the rendered plain + HTML bodies without sending
  (and without the approval gate). Also write the composed email to `comms-log/dry-run-<step>.md` per
  the skills README contract. Return a synthetic message ID for logging.
- **Search/read:** Execute normally (read-only operations are safe in dry-run).

## Terminology

**The platform is `Connect`, never `CommCare Connect`** — in every word this skill
puts in front of a human. The full rule, including the carve-outs for CommCare the
mobile app, CommCare HQ and code-level identifiers, is
[`skills/_terminology.md`](../_terminology.md). Read it before writing prose; it is
binding on this skill's output.
