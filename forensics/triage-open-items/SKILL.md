---
name: triage-open-items
description: Works through the open-items list with you, matching each item against your backlog, and files, keeps or drops it with your approval. Use when open items have piled up, when finish-branch or handle-feedback offers triage, or to resume a paused triage.
---

# Triage Open Items

Later work found mid-flow is only useful if it reaches the backlog once, in the right place, or is dropped on purpose. Triage takes the open-items list, checks each item against what the backlog already holds, and lets your partner decide each one.

Ask your partner one question at a time, in plain text; do not use the AskUserQuestion tool, because some clients show only the tool's question and drop the text around it. Put what your partner needs to answer in the same message: the problem and why it matters, then the options, recommended first, each with a short bold label in words (never numbers or letters) and a one-line reason. End with a line naming those labels in the same order, such as `Reply with **new PR**, **straight to main**, or **drop it**.`, and make the question the last thing in the message, after any tool use. Your partner may answer with an option, their own alternative, a question or an aside. Keep messages short: lead with the decision, then only the detail needed to answer it. Before a stretch of work that takes more than a moment, such as dispatching a reviewer, writing a spec or plan, or fixing findings, say in one line what you are about to do; after your partner answers, say what comes next before starting it.

When you find something worth doing later that this work does not include, add it as an item to `.dietpowers/trackers/open-items.md`, following `## Open items` in `${CLAUDE_PLUGIN_ROOT}/shared/trackers.md`, and say so in one line.

Triage commits nothing. When the backlog is a notes file, leave your edit to it on disk and say so.

The file's format and outcomes are in `## Open items`, and replies and resuming in `## Replies` and `## Resuming`, all in `${CLAUDE_PLUGIN_ROOT}/shared/trackers.md`.

0. If your partner asked to resume, follow `## Resuming` in `${CLAUDE_PLUGIN_ROOT}/shared/trackers.md`, then carry on from the step it leads to.
1. Read `.dietpowers/trackers/open-items.md`. If it is missing or has no `open` or `kept` items, say so and stop.
2. Find where the backlog lives, from the project instructions or your memory. If neither names it, ask once, for example GitHub issues, another tracker or a notes file, and offer to save the answer to memory. Read the backlog's open items: `gh issue list --state open` for GitHub issues; otherwise what your partner points to. If it cannot be read, say why; triage still runs, offering only **keep** and **drop**.
3. Study the list. Group related items, and merge items that describe the same thing into one, keeping all their evidence and the lowest number. Write the items back to the file in group order, so a resumed triage can follow it, and show the groups and merges in one message; this needs no question.
4. Clear the Recommendation, Question and Decision of every item. Then compare each item with the backlog for duplicates and close matches, and write its Recommendation: the outcome with a one-line reason, and for **file new** or **add to #N**, the draft title and body, or the comment.
5. Ask about one item at a time, in file order, recording each Question in the item before asking it. Offer the outcomes, recommended first, ending `Reply with <outcomes in bold>, or **pause**.` Your partner may edit the draft in the reply.
6. Carry out each answer before the next question: `gh issue create` or `gh issue comment` for GitHub issues, or appending to a notes file. Record the Decision only once the outcome has succeeded, then remove the item from the file, except a kept item, which stays with status `kept`. If filing or commenting fails, leave the item `open`, record the error under Recommendation, clear its Question and Decision so it does not look paused, and say so.
7. Report: what was filed, with links; what was added to, kept and dropped.

If the `dietpowers:finish-branch` skill invoked you and your partner replies `pause`, also say to resume the triage first and then run `/dietpowers:finish-branch` again to integrate.

Terminal state: if the `dietpowers:finish-branch` skill invoked you, return to it; otherwise stop.

Depth: ${CLAUDE_PLUGIN_ROOT}/shared/trackers.md
