---
name: outbox
description: "Show the user's draft emails and LinkedIn messages in chat and act on them: read one, copy it, edit it, make a Gmail draft, record that they sent it, or discard it. Use when the user says outbox, drafts, show my messages, what's waiting to send, I sent it, or copy that message. Never sends anything."
---

# Outbox (chat version)

The chat version of the Claude Outbox panel: same files, same rules. The user always sends messages themselves; you never send, reply, or forward. (A guard also blocks the usual email send tools, but it isn't a complete lock; the rule is yours to keep.)

## 1. Show the list

Read every `outbox/*.md` file except ones starting with `_` (examples). Read the header between the `---` lines (format in `knowledge/outbox-format.md`). Ignore `outbox/sent/` and `outbox/discarded/`.

Show three short numbered groups, oldest first:

- **Ready for you** (`status: draft` or blank): `1. Email to Jane Doe (Example Co), "Thank you, Operations Analyst interview", written Oct 6`. For LinkedIn add the type and length: `LinkedIn note to Alex Rivera, 182 of 200 characters`.
- **Waiting in Gmail** (`status: in-gmail-drafts`): "In your Gmail drafts. Tell me when you've sent it."
- **Needs fixing**: files with no readable header, an email with no subject or no `to:`, a placeholder (like `[Name]`, `{First name}`, `{{name}}`, `<Name>`, `___`, or `Your Name`), or a LinkedIn connection note over 200 characters. Say what's wrong and offer to fix it.

Nothing waiting? Say so in one line and suggest one next step (for example the `follow-up` skill).

Then ask what they'd like to do with one of them. Use the numbers from your list.

## 2. Actions

- **Read it:** show the full message in a plain text block, exactly as it will go out: for email, the subject line, then the body, then the signature from `profile/signature.txt`. If that file is missing or still has placeholders (like "Your Name" or a 555 number), leave the signature off, tell the user it isn't set up, and offer to make one from their confirmed profile details. Never use `profile/signature.example.txt` in a message. For LinkedIn, the body only, plus the character count.
- **Copy it:** show the same checked text as "Read it" in one plain text block they can copy: the body (plus the signature for email, if set up), never the `---` header. For email, show the subject on its own line above the block so they can paste it into the subject field. Tell them where to paste it (Gmail, or the LinkedIn message box). **Copying is not sending**; leave the status alone.
- **Edit it:** make the change, keep the header intact (to attach the job's checked resume or cover letter PDF, put its file name in `attach:`, comma-separated for two; blank otherwise), run voice-editor (and truth-checker if a fact changed), show the new version. If it's already waiting in Gmail, the Gmail copy still has the old text: tell the user to delete that Gmail draft, then offer to make a new one (and set the status back to `draft` until you do).
- **Make a Gmail draft** (only if a Gmail tool is available in this session; never a send tool): first check no placeholders (as above) in the body or signature, a subject, and a real `to:` address. Drafts made here in chat carry no attachments: if the message mentions an attached resume or file, tell the user which file to attach in Gmail before pressing Send (the `attach:` header names it; else the job folder's finished `<Name>-Resume-<Company>.pdf` or cover letter PDF, never a `-CHECK.pdf`). In Claude, the Outbox panel's **Create Gmail draft…** attaches it for them. Create the draft with to, cc, subject, and body plus signature; if `reply_to` is set and the tool supports threading, use it so the draft lands in the same conversation. Then set `status: in-gmail-drafts`, tell them it's in their Gmail drafts, and remind them to press Send there. If the tool fails or you can't tell whether it worked, say so and don't change the status; ask them to check their Gmail drafts before trying again, so they don't end up with two.
- **"I sent it"** (or "I sent number 2 yesterday"): re-read the file, set `status: sent` and add a `sent: YYYY-MM-DD` line to the header with the real date they sent it. Then:
  - Contacts (`contact:` names in `contacts/contacts.csv`): follow the playbook rule "When the user sends someone a message".
  - Job (`job:` folder in `jobs/tracker.csv`): for a follow-up, add 1 to `followups`; set the next step and `next_action_date` per the playbook's follow-up timing (the job row owns the date once they have applied).
  - Add one line to `history/activity.md`.
  - Move the file to `outbox/sent/`.
- **Discard it:** set `status: discarded` and move the file to `outbox/discarded/`. If it was waiting in Gmail, remind the user to delete the Gmail draft too (you can't delete it for them). It can be restored by moving it back and setting `status: draft`.
- **Gmail check:** if Gmail is connected, you can look in their Sent mail for each email that's waiting in Gmail or still a draft (they may have copied it in themselves) (same subject, sent to that `to:` address on or after `created:`, with a matching opening; one sent message can complete only one draft; if unsure, ask the user). If you find it, treat it as "I sent it" with the date it was sent.

## Rules

- Never send, reply, forward, or schedule email, and never post or message on LinkedIn. Never mark something sent unless the user says so or you saw it in their Sent mail. This chat version is always draft-only, whatever `outbox_mode` says. (`outbox_mode: send` only affects the Claude Outbox panel, which also asks the user once, in the panel, to confirm send mode before it sends anything, never sends attachments (a draft that mentions one becomes a Gmail draft, with the job folder's checked PDF attached), and keeps a draft blocked after a send it couldn't confirm until the user checks their Sent mail.) If a `[Outbox]` note or the file says a send's outcome was uncertain, don't mark it sent or suggest sending again: ask the user to look in their Gmail Sent folder first, then record what they find.
- After "I sent it" to someone at `replied`, `talked` or `referred` (a thank-you or update), only `last_contact` changes: no touches, no follow-up date.
- Re-read a file right before changing it (the other app may have touched it), change only the header line or text you mean to, and log tracker/contact changes in `history/activity.md`.
- Never change a file that is already `sent`.

## The Claude panel (Claude Code only; Codex: skip)

In Claude Code the same drafts show in the `/outbox` panel. What its main button does depends on `outbox_mode`:
- `draft-only` (default): **Create Gmail draft…** puts a formatted draft (with `profile/signature.txt`) in their Gmail, and they press Send there. If the message mentions an attachment, the panel first shows which checked PDF from the draft's job folder it will attach (named in `attach:`, else the one finished resume or cover letter PDF the text mentions), attaches it, or says plainly what to attach by hand. The draft then shows under **Waiting in Gmail** until the user presses **Mark sent…** (or `sync-inbox` finds it in Sent).
- `send`: **Send…** sends from their Gmail after a confirm step. The first time the panel sees `send`, it asks the user to confirm send mode inside the panel and keeps making Gmail drafts until they do; the confirmation counts only for this folder, and it asks again whenever a new dated "turned on send mode" note appears in preferences (so turning it off and back on means confirming again). It never sends attachments: such a draft goes through **Create Gmail draft…** instead. It keeps a send record outside this folder and refuses to send the same draft twice.
- Other buttons: **Copy**, **Ask Claude to edit**, **Discard**.

When the user acts there, the panel changes the draft's status, adds its own line to `history/activity.md`, and leaves an `[Outbox]` note. Update the tracker and contacts from the note (as in "I sent it" above, with the date it gives), and log only those changes.
