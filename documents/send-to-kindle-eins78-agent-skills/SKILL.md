---
name: send-to-kindle
description: >-
  Use when getting a document onto an Amazon Kindle — which delivery routes
  still work, what format to produce, and why a delivery can silently fail.
  Kindle-only; nothing here applies to Kobo, reMarkable or other e-readers.
  Triggers: send to Kindle, put this on my Kindle, read on Kindle, Kindle
  email address, sendtokindle, personal documents, sideload EPUB, Kindle
  didn't receive it, kindle.com address, Kindle highlights, My Clippings.
globs: []
compatibility: claude-code, cursor
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/agent-skills
  version: "0.1.0"
---

# send-to-kindle

Delivering a document to a Kindle. Covers what to produce, how it gets there,
and the two failure modes that give no error message.

Producing the file is the `pandoc` skill's job —
`scripts/md2kindle-epub.sh` turns markdown into a suitable EPUB. This skill
starts at "the file exists".

**Everything below is service behaviour, and it moves.** Between 2022 and 2026
Amazon stopped accepting MOBI, started accepting EPUB, killed USB download of
purchased books, and retired Word's Send-to-Kindle button. Statuses here are
**as of 2026-08**; re-verify before relying on a dated claim.

## Produce EPUB, not PDF

| | |
|---|---|
| **EPUB** | Reflowable — text re-wraps to the reader's font size and margins. Kindles do not render EPUB natively; Send-to-Kindle converts it server-side into the device's own format (KFX/AZW3) on delivery, which is what buys reflow, resizable type, and a native TOC. Free, no local tooling. |
| **PDF** | Fixed-layout. A PDF page is a fixed canvas — on a 6" screen it either shrinks to illegible or needs constant pan/zoom. Right for print, wrong for reading. An A5 print booklet is roughly 60% wider than a Paperwhite's visible area. |
| **MOBI / AZW** | Not accepted as *input* since August 2022. Don't reach for an old MOBI recipe. |
| **AZW3 (locally converted)** | Only needed for the USB path — see below. |

## Delivery routes (status as of 2026-08)

| Route | Status | Notes |
|---|---|---|
| **Send-to-Kindle email** (`…@kindle.com`) | Works | The default. Wireless, works over a phone hotspot. See the three facts below |
| **Web upload** (sendtokindle.com, drag-and-drop) | Works | Manual, but no sender allowlist to trip over |
| **Kindle mobile app → "Import file"** | Works | Only useful if the reader reads on the phone |
| **USB sideload into `documents/`** | Works | A raw `.epub` copied over USB is **not indexed** by the Kindle library — convert to AZW3 locally first (e.g. Calibre). Email delivery gets that conversion for free. Unaffected by the 2025 removal of USB *download* for purchased Kindle Store books, which is a different thing |
| **Send to Kindle desktop app** | Being retired | Kindle for PC and the Windows desktop app shut down 2026-06-30. Email and web upload do not depend on it |
| **Send to Kindle from Microsoft Word** | Retired 2026-02-09 | The button is gone; web upload is unaffected |
| **Wireless delivery to older hardware** | Cut off for pre-2013 devices | The May-2026 cutoff hit Paperwhite 1 and older only. 2018-era hardware and newer keep full wireless delivery |

## Sending by email — three facts

1. **Send the file as an email attachment** to the reader's Send-to-Kindle
   address. Nothing else in the message matters.
2. **Addresses are per device, not per account.** An account with several
   registered Kindles has a separate ingress address for each, so delivery is
   granular. Amazon-facing *device names* are user-set and can be misleading —
   pick the target by a stable identifier (the address itself, or the device
   serial), never by display name.
3. **The sender address must be pre-approved** on the account's Approved
   Personal Document E-mail List. Mail from an unapproved sender is **dropped
   silently — no bounce, no error, no delivery.** This is the single most
   likely cause of "I sent it and nothing arrived".

The allowlist is separate from the ingress address; both live under
*Manage Your Content and Devices → Preferences → Personal Document Settings*.

## Confirming delivery — sending is not delivering

**Ingress validation is asynchronous.** Amazon accepts the SMTP transaction,
then validates the document afterwards and reports failure by email. Everything
observable at send time therefore proves only that the mail *left*, not that it
*arrived*:

| What you checked | What it actually proves |
|---|---|
| The mail client reported "sent" | The message was queued |
| The outbox drained to 0 | The SMTP handoff to your provider succeeded |
| The subject is at the top of the sent mailbox | Same as above — your provider took it |
| **No bounce after a few minutes** | **Amazon accepted it.** The only real signal |

Scripted senders make this worse: an AppleScript `send` returns as soon as the
message is *queued*, so a script that checks immediately after will always
report success. Nothing about a queued message predicts what Amazon does with
it two minutes later.

**So: wait, then check for a bounce.** Observed bounce latency is ~30–60
seconds. Waiting ~2–3 minutes and finding no bounce naming your filename is the
verification. Anything faster is checking the wrong thing.

### `E999 — Send to Kindle Internal Error`

Amazon's **generic rejection**. The wording names no defect and reads as
transient, which is the trap: it is frequently a real, findable spec violation
in your file.

**Run `epubcheck` before theorising.** It settles in seconds what the error
message actively obscures.

Worked example, 2026-08-08 — one sender, one morning, all EPUBs from the same
generator. The file that bounced twice, 3.5 hours apart, was **the only one in
the batch missing `dc:title`**, a *required* element of the EPUB package
metadata. Every file that carried a `dc:title` was accepted. The generator had
made the title optional, so omitting one flag silently produced a spec-invalid
book.

Two things that make this hard to see without the validator:

- **Errors alone do not predict rejection.** Accepted files in the same batch
  failed `epubcheck` too — broken internal links, undefined fragment
  identifiers. Amazon tolerated all of it. What it would not tolerate was the
  missing *required* element. Triage by severity and by REQUIRED-ness, not by
  error count.
- **Surface plausibility misleads.** The twice-failing file was the smallest and
  structurally simplest of the batch (36 KB vs 60 KB) and passed `unzip -t`
  cleanly. Nothing about it looked wrong.

So on `E999`:

1. `epubcheck the-file.epub`
2. Fix any violation of a **required** element (`dc:title`, `dc:identifier`,
   `dc:language`) and rebuild.
3. Resend. Note that re-attaching the **byte-identical** file is the one thing
   observed never to work — it bounced again in 16 seconds — which makes sense
   once you know the defect travels with the file.
4. Only if a *validator-clean* build fails repeatedly should you treat it as
   genuinely transient on Amazon's side.

### The two silences are different

Both look like "nothing arrived", and they need opposite responses:

- **No bounce, no delivery** → an **allowlist** problem (see above). Amazon
  drops unapproved senders without a word.
- **A bounce** → the sender *is* approved; the message reached Amazon and was
  rejected downstream. Validate the file (above) rather than simply retrying.

A bounce is therefore mildly good news about your configuration. Once any
document from a given sender has arrived, "no bounce" reliably means delivered
for that sender.

## Size ceilings

| Route | Ceiling |
|---|---|
| Email attachment | **~50 MB** — widely-circulated community figure, not confirmed against an official Amazon page. Verify on the Personal Document Settings page if it matters |
| Web upload | ~200 MB, same caveat |

Text documents will not come near either. A document bundling archived source
captures plausibly could.

## Highlights only come back one way

Anything delivered via Send-to-Kindle is a **personal document**, not a Kindle
Store purchase, and Amazon's cloud highlight ecosystem is structurally closed
to it:

| Route | Covers personal documents? |
|---|---|
| `documents/My Clippings.txt` on the device | **Yes — the only route.** Plain text, trivially parseable, but retrieval requires physically connecting the device over USB. No wireless path exists for this file |
| `read.amazon.com/notebook` (web Notebook) | No — Kindle Store purchases only |
| Per-book "Export Notes and Highlights" | No — same scope, and manual anyway |
| Readwise | No — its docs explicitly exclude files sent via Send-to-Kindle |

So the USB cable is not a convenience fallback here; it is the only mechanism.
Plan around a manual step, or do not promise highlight round-tripping.

## Common Mistakes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Sent it, nothing arrived, no bounce | Sender not on the approved list | Add the exact sending address under Personal Document Settings |
| Sent it, nothing arrived, got `E999 - Send to Kindle Internal Error` | Amazon's generic rejection. Often a real spec violation the message doesn't name — observed cause: a missing `dc:title` | Run `epubcheck`. Fix any REQUIRED-element violation, rebuild, resend. Re-attaching the identical file never works |
| A script reported the send succeeded, but it never arrived | The script checked the outbox, which only proves SMTP handoff. Ingress validation happens later and reports by email | Wait ~2–3 min after sending, then check for a bounce naming the file. Absence of a bounce is the verification |
| Arrived on the wrong person's Kindle | Targeted by device display name | Target by ingress address or serial; names are user-set and often stale |
| Reader has to pan and zoom every page | A PDF was sent | Send EPUB and let Send-to-Kindle convert it |
| Copied an `.epub` over USB, it never appears in the library | Raw EPUB isn't indexed on-device | Convert to AZW3 locally, or use email delivery instead |
| Checkboxes render as blank gaps | Task-list HTML `<input>` elements were emitted | See the `pandoc` skill — build the EPUB with `task_lists` disabled |
| EPUB built fine, `epubcheck` shows errors, but it still delivers | Not all validation errors matter to Amazon — broken links and undefined fragment identifiers were tolerated | Triage by REQUIRED-ness, not error count. Fix required-element violations first; treat the rest as quality issues |
| Waiting for highlights to sync | Personal documents never reach the cloud | USB + `My Clippings.txt`, or nothing |

## What this skill deliberately does not do

- **It does not send anything.** No sender script, no AppleScript, no SMTP
  helper, and no configuration contract for one. The send step is the three
  facts above, performed by a human in a mail client.
- **It carries no addresses.** Ingress addresses, approved senders, device
  serials, and keychain account names are personal values that belong in the
  operator's own private workspace, never in a published skill.
