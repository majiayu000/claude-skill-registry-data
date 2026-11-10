---
name: inbox
description: Organize the owner's Gmail through Proposals they sign off.
disable-model-invocation: true
---

Organize the owner's Gmail with them: read the mailbox, draft **Proposals**, and apply one only after the owner's **Sign-off**. Without Sign-off, a session only adds to the Proposal list. The terms are in [`GLOSSARY.md`](GLOSSARY.md).

The Gmail tools (`mcp__gmail__*`) exist only where the `gmail` server is registered; with none loaded, say so and stop.

## Data

The owner's data lives in the private `personal` repo's `inbox/` folder, beside `writing/`. This skill holds rules and steps only; every sender, label, keyword and person belongs in that folder or the session.

**`/inbox` runs in a [session workspace](../../../docs/agents/git-workflow.md#a-skills-session-workspace) named `inbox-<date>`**, since a primary checkout takes no edits, and lands the data when the session ends. The gmail gate and `record.sh` read that workspace's own `packages/personal/inbox/`.

- `always-inbox.md`: Gmail queries for mail that always stays in the Inbox.
- `proposals.md`: one entry per Proposal, in the format at its top.
- `changes.md`: append-only, one entry per applied change, in the format at its top. Never edit or remove an entry.

Write both through [`record.sh`](record.sh): `record.sh status <n|n-m> <status>` and `record.sh log <n> <tool and action> <changed> <reverse>`.

## Rules

- **Nothing changes in Gmail without Sign-off on one specific Proposal**, in a session the owner started and is present for. Never run unattended or on a schedule.
- **Sign-off is the owner's yes in the chat to that Proposal's id**, recorded as `signed-off` before its first Gmail call. A yes to a design, a step or a batch of Proposals at once signs off nothing. The repo's gmail gate then allows only a call one `signed-off` Proposal covers, and asks the owner for any other; a call that asks means the Proposal and the call disagree, so fix the Proposal or redraft it.
- **Trash, filters included, only under Sign-off.** Never mark mail as spam, send, reply or draft.
- **When unsure, leave mail in the Inbox.** Check every Proposal against the always-inbox list and name any overlap in it; a Proposal that would move always-inbox mail says so in its overlap field before Sign-off is asked.
- **The Inbox is all of `in:inbox`**, any category tab.
- **Existing topic labels stay** as the places mail is filed. The only new labels are `Reading/<source>`, `Waiting` and `Unsubscribe`.
- **A declined Proposal stays on the list, marked `declined`**, and is never raised again; a different query or action is a new Proposal.
- **One Sign-off covers one bulk Proposal, carried by one `batch_modify_gmail_message_labels` call.** Gmail caps that call at 1000 message ids, so a bulk pass over more is drafted as several Proposals of at most 1000 each.
- **Record before and after.** Write a Proposal to `proposals.md` when it is drafted, and log each Gmail call to `changes.md` before the next one.

## A Proposal

Every Proposal states, before Sign-off is asked:

- its **kind**: `filter`, `bulk` (label, archive or Trash), `label` (rename or delete) or `unsubscribe`;
- its exact **Gmail query**;
- its **action**: an `add` clause and a `remove` clause naming label ids, or a label created on apply by its name, as in `add Label_12; remove INBOX` (archive is `remove INBOX`; Trash is `add TRASH`), or a label's new name. The gmail gate allows only the labels these clauses name;
- its **match count** over existing mail, marked a lower bound when the search returned more than one page;
- a **sample** of a few matching messages (sender, subject, date), so a query that catches the wrong mail shows;
- its **always-inbox overlap**: the always-inbox entries it matches, or none.

## Tool facts (workspace-mcp 1.28.0)

- **A filter is created or deleted, never edited.** Changing one is a delete and a create, each logged, the delete's entry carrying the old filter's full criteria and action. `list_gmail_filters` shows what exists.
- **A filter acts on incoming mail only.** Existing mail it would have caught is a separate bulk Proposal (the backlog step).
- **The label tools take raw label ids** and nothing in them blocks `TRASH` or `SPAM`. The rules do: `TRASH` only under a signed-off Proposal, `SPAM` never. `list_gmail_labels` maps names to ids.
- **`search_gmail_messages` pages results with no total.** Count by paging with `page_token`; a count over only the first page is a lower bound and says so.
- **Removing or deleting a label never removes mail**; its messages keep their other labels, and mail with no labels stays in All Mail.

## Session steps

Each step reads the mailbox and drafts Proposals; apply only signed-off ones. Take the steps the owner asks for, in this order unless they choose another.

1. **Start.** Read `always-inbox.md` and every `pending` and `signed-off` entry in `proposals.md`, and report them before anything else. With an empty always-inbox list, ask the owner to name what belongs there first. Done when the owner has seen both.
2. **By-sender pass.** Group a time window of `in:inbox` by sender or mailing list, and propose one destination per sender as a filter: an existing topic label, `Reading/<source>`, archive, or Trash. Prefer a `list:` query over a `from:` query where the mail carries a list id. For a newsletter split by topic, keep the issues the owner follows in the Inbox under `Reading/<source>` and label the rest; the catch-all is labeled, not trashed, for its first month. Done when every sender in the window has a Proposal or is left in the Inbox.
3. **Backlog.** For each `applied` filter with no backlog Proposal, propose its query over existing mail as a bulk Proposal with the filter's action. Done when every applied filter has one.
4. **Unsubscribe sweep.** Propose putting one recent message per sender to unsubscribe from under `Unsubscribe`, as one bulk Proposal; the owner clicks each unsubscribe link. In a later session, a sender whose message lost the label is done: propose its backlog (archive or Trash) and a catch filter for mail it still sends. Done when every handled sender has both Proposals.
5. **Label cleanup.** Propose renames or deletes for labels Gmail misreads as nested, leftover labels and near-duplicates, each naming how many messages carry it. Done when the label list has been read through.
6. **Old-mail archive.** After filters and unsubscribing, take `in:inbox older_than:1y -is:starred`, leave out mail from people, and preview it grouped by sender and label with where each group ends up. Propose the archive as bulk Proposals. Done when the preview has been shown and each group has a Proposal or stays.
7. **Triage.** Sort what filters missed into Proposals, propose marking `Waiting` the threads where the owner sent the last message, and propose filters for repeats. Done when the Inbox holds only mail that needs the owner or has a Proposal.

## Applying a signed-off Proposal

1. Re-run its query; if the count moved by more than a few messages, show the new count and ask again.
2. Make the Gmail call it names, creating any new label it names first.
3. Log each call with `record.sh log` before the next, with what reverses it: the filter id and its full criteria and action, or the message ids and the labels added and removed, or the label's old and new name. A new label's entry reads `created label <name> (id <id>)`, which is how the gate learns its id.
4. Set it `applied` with `record.sh status`.
