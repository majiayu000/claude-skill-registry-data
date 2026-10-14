---
name: kairos-vocabulary
description: Name Kairos work only by its short code and by the words that Kairos gives. Use whenever work is named, numbered, grouped or reported — when the user or the agent says "task 1", "slice 2", "D3", "the third decision", "epic", "ticket", "story", "sub-task", "sprint", "phase 2", "batch 1", "mark it done", "in progress", "what should I call this" — and when writing a plan, a status note, a commit message or a summary about Kairos work.
---

# Kairos vocabulary

Kairos gives each item a name: its short code. Use that name. Do not make up a different one.

The server refuses an unknown field and an invalid transition. It cannot refuse a made-up name in an item, a commit or a reply. "Slice 2", "T1", "D3" or "the auth epic" looks clear in one message. After a compaction, nobody can find what it meant. `search` and `get_item` do not find it, and the board does not show it.

**The test:** can a reader find the definition of the name? A short code resolves with `get_item`. A numbered user story resolves to a line in its PRD. "Slice 2" resolves to nothing.

## The rules

### A work item's name is its short code

A short code has the form `PREFIX-L-NNNN`, for example `COLLIERY-T-0042`. The letter is the item type: `S` strategy, `I` initiative, `T` task, `D` document, `A` ADR. The prefix comes from the organization and the number from a sequence on the server.

- Take a short code only from a tool result. `create_item` gives a new one. `get_item`, `search`, `board_items` and the relationships in a result give existing ones.
- Do not predict a short code before `create_item` gives it. Do not continue a sequence. Two items that you create one after the other do not always get numbers that follow.
- Do not shorten a short code (`T-42`, `#42`, "the 0042 task"). Do not renumber one.
- If you do not know the short code of an item, find it with `search`. Do not describe the item in its place.
- A short code that you write into an item must come from a result in this session. A short code from memory is a guess. A short code that is already in an item: verify it with `get_item` before you use it again.

### Work that does not exist yet is a quoted title

A proposal, a decomposition draft and a grill session talk about work before it exists. Write each such item as its full title in quotes, marked "not yet created":

> Proposed (not yet created): "Rotate the refresh token", "Expire the sessions after a password change".

- Do not give it a temporary name: no "T1", no "task A", no "Slice 1". Do not use a short code that you plan to change later.
- A numbered list is correct inside one message, so that the user can answer "2: yes". The numbers are for that message only. Do not use them in a later message, an item or a commit.
- When `create_item` gives the short code, use the short code from then on.

### A decision is an ADR or prose

- A decision that is an ADR is its short code (`COLLIERY-A-0023`).
- A decision that is not an ADR is prose under a `## Decisions (<who>, <date>)` heading on the item that it belongs to. It has no number.
- A decision that is still open is named by what it decides ("the storage of the sessions").
- Do not write `D1`, `D2` or "the third decision".

`engineering/domain-modeling` says when a decision earns an ADR.

### A group is an initiative; an order is a `blocks` edge

- Work that belongs together is the children of one initiative (the `parent` edge). That is the group. Do not make up "workstream A", "batch 2" or "the migration epic".
- An order between tasks is a `blocks` edge from the first task to the second. Do not write "phase 1" or "batch 2". `/kairos:ralph-initiative` follows the `blocks` edges, so an order in text only is an order that nothing follows.
- A group that is real and lasts is an initiative. Propose one.
- "Vertical slice" is the shape of a cut. It is not a name. A slice becomes a task, and its name is the short code of that task.

### The state of an item is its column

- The state of an item is the column that `get_item` gives. Take the names of the columns from the board (`my_boards`, `get_item`), not from memory. Boards can have different columns.
- Say "Completed" (or the name of the done column of that board) only after `transition_item` succeeds. Do not say "done", "shipped" or "closed" for an item that is not in a done column.
- Say the column name, not "in progress", "WIP" or "on hold".

### The one place for numbers in an item

The numbered user stories of a PRD are correct: the PRD template numbers them. To cite one from a different item, add the short code of the PRD: "`COLLIERY-D-0031`, user story 4". Nothing else in an item gets a numbering scheme of its own. Cite an acceptance criterion as "`COLLIERY-T-0042`, the third criterion", not `AC-3`.

### Outside the conversation too

- Commits, pull requests, branch names: use the short code.
- Code comments: `TODO(COLLIERY-T-0042)` or no code at all.
- A summary to the user: the short code and the title.
- A todo list entry for Kairos work: put the short code in the text.

### Words from other trackers

The user can say "epic", "ticket", "sprint" or "sub-task". Translate the word to the Kairos word. Use the Kairos word in the reply, so that the user sees the mapping. Do not create an item of a type that does not exist. [ITEM-TYPES.md](ITEM-TYPES.md) gives the table from the user's words to the Kairos item types, and when to use each relationship.

For the words of procedural text, use the Technical Names in section 4 of [the STE reference](../../../references/simplified-technical-english.md).

## Repair a made-up name

When you find a made-up name (yours, from an earlier session, or the user's), repair it at once:

1. Find the item with `search`, with the words of the name and the parent or the board.
2. If an item matches, give the mapping in the reply, for example "'the auth epic' is `COLLIERY-I-0003`".
   Then fix the made-up name in each item that you can edit (`get_item`, then `edit_item`).
3. If no item matches, say that Kairos does not track the work. Offer to create the item. Do not guess a match.
4. If the user used the name, answer the question first, and use the short code in the answer. Do not lecture.
