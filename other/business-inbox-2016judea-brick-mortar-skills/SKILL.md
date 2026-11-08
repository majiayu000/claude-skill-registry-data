---
name: business-inbox
description: Take a business inbox (Zoho Mail via its MCP; the pattern fits any mailbox) to zero the right way — read every message, work out what each one changes, write that into the repo or ledger that owns the thread, queue the next chase, then file the message. Use when you say "go through my business emails", "check the business inbox", "any replies", "did the county answer", "clear the inbox", or when a campaign needs to know whether anyone wrote back. Includes how to get attachment bytes the Zoho MCP can't download (Mail.app's local IMAP cache).
---

# The business inbox

A business mailbox that mostly receives **replies to things you sent** is not a personal
inbox: every message belongs to a campaign that already has a ledger somewhere.

**The inbox is not the record. The ledger is.** A reply read and left in the inbox is a
reply that never happened: the campaign doc still says "SENT", the next session re-chases an
office that already answered, and the fact dies with the session. So the unit of work is
*read it -> write what it changed into the ledger -> queue the next move -> file the
message*. Filing is the last step and the proof the first three happened. Zero inbox means
zero unrecorded facts, not zero unread mail.

## Constants

Look these up once with `ZohoMail_getMailAccounts` and `ZohoMail_getAllFolders`, then keep
them in your project notes: `accountId`, and folder ids for Inbox, Archive, Spam, Sent, and
one topic folder per *kind* of thread (e.g. "Records requests", "Bids", "Discovery"). Folder
ids are stable; re-read them only if a move 404s.

## The loop

1. **`ZohoMail_listEmails`** on the Inbox, `limit: 100`, fields
   `subject,messageId,folderId,fromAddress,toAddress,receivedTime,status,summary,hasAttachment,sender`.
   Also glance at Spam — an official's reply can land there, and a missed response costs
   weeks.
2. **`ZohoMail_getMessageContent`** with `includeBlockContent: true` on every message. Read
   the whole thing, quoted history included: the quoted block is usually the only place the
   question being answered is written down.
3. **`ZohoMail_getMessageAttachmentInfo`** whenever `hasAttachment` is `1`. Record filenames
   and sizes in the ledger even if you can't fetch them yet (see below).
4. **Find the ledger and write the change into it.** Not a summary of the email — what it
   *changes*: a status that moves, a fact that lands, a premise that dies.
5. **Queue the next move** in a file your future sessions read (e.g. `pending.json`).
   Rewrite the existing item rather than appending a second one, so a chase never fires on a
   question already answered. The entry must stand alone — a future session gets no
   transcript.
6. **File it** with `ZohoMail_moveMessages`, then re-list the Inbox and confirm it is empty.
   Never delete: these may be the only copy of what an official said.

## Routing

Make a table like this in your project, one row per kind of thread:

| Thread | Folder | Ledger |
|---|---|---|
| A government office answering a records request | Records requests | the request tracker row for that jurisdiction |
| An RFP, bid, addendum, purchasing agent | Bids | the doc for that solicitation |
| Someone answering a discovery question you asked | Discovery | that project's outreach README — verbatim quote, then what it changes |
| Vendor receipts, platform notices | Notifications | none |

Nothing fits? Archive it and say so. Don't invent a folder for one message.

## Rules

- **Never send a reply unprompted.** Put any needed reply in front of the owner as a draft,
  in the session and in a file. They press send.
- **A personal mailbox is not a bulk sender.** Zoho blocks outgoing mail for an account that
  sends in bursts (dozens in an hour), and while blocked nothing goes out, replies included.
  Cap it (e.g. 10/hour, 25/day, 90s apart — the `zoho-send-cap` hook enforces this) and send
  batches through a bulk provider instead. A block notice tends to land in Spam from
  `noreply@zoho.com`.
- **Quote verbatim in the ledger, paraphrase only in the report.** "This work is typically
  performed by Operations or Engineering" is a sentence about who the customer is; "they
  routed it internally" is not.
- **A partial answer is not a closed request.** Log which numbered items came back and which
  are still out, by number. Marking a half-answered request FULFILLED quietly abandons the
  items it existed for.
- **A forward is not a lead.** "I've passed this to the appropriate staff" closes nothing.
  Record it; don't queue a chase on it; don't count it as a reply.
- **Read what the replies say about your next email.** If five replies all describe an
  unstructured process and none gives the number you asked for, the finding is about the
  *question*: stop asking it by email and derive it another way.

## Attachments — read them off the Mac, not the API

**The Zoho MCP cannot download an attachment**: it exposes `getMessageAttachmentInfo` (name,
size, id) and no download endpoint, and as a hosted connector it leaves no local token for a
curl fallback.

**If the account is also in Mail.app over IMAP, Mail has already downloaded it:**

```
~/Library/Mail/V10/<account-uuid>/<Folder>.mbox/**/Attachments/<n>/<n>/<filename>
find ~/Library/Mail/V10/ -iname "*.xlsx" -newer /tmp/marker
```

Find your account's UUID by looking for the folder names you created. The mbox tree mirrors
the server's folders almost immediately, so file first, then look. Copy the file into the
repo that owns the thread and **verify the byte size against what
`getMessageAttachmentInfo` reported** — that match proves it's this message's attachment and
not a same-named file from another thread. Then open it before describing it: a sheet you
assumed was an index can turn out to be a price list.

For xlsx, load twice with openpyxl — `data_only=True` for values, and again without it for
`number_format` and font colour, because both carry meaning a values-only read throws away.

## Reporting back

Lead with what changed, one line per thread, then the actions taken. End with what is now
waiting on the owner: usually a draft to approve or an attachment to look at.
