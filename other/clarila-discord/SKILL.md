---
name: clarila-discord
description: "Synchronize a workflow with its issue thread in the configured Clarila Discord server. Use for publication preflight, role-attributed updates, verifying receipts after a lost response, or explicit owner commands."
---

# Keep Discord and the workflow aligned

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Read the shared workflow, current issue, configured Clarila owner/server/destinations and existing canonical thread mapping. Resolve/reuse the Clarila-server workflow thread by canonical repository/issue. Keep the original report conversation as source evidence, not a default publishing destination.
2. Before every write, verify the target guild/forum matches the configured Clarila destination, or the specific alternate destination explicitly authorized by the user, and verify the publisher is the configured bot. An alternate destination alone does not authorize a personal-account fallback. Use an available authorized Discord connector or HTTP API operation for thread creation/reuse, summary updates, attributed messages and owned evidence. Follow the operations reference. Credentials remain in private configuration.
3. Publish useful findings, blockers, independent results and outcomes. For Codex specialist work, use the [role publication procedure](references/operations.md#publish-a-codex-specialist-finding) so the corresponding Discord bot posts the specialist's own words. Clarila owns the issue summary. Keep raw task logs, private account data and unchanged heartbeat noise out. Show actual branch/PR/session links and a checked time.
4. Retain the original write intent and verify returned identities. Reconcile uncertain sends and thread creation before retrying. Reuse the original starter and preserve its findings, holds, PR links and existing workflow state. Verify both the issue route and the owner's following membership when investigating a missing Issues sidebar entry.
5. Owner controls belong to the Clarila control service (`clarila-discord-listener serve`, which replaces only the Clarila bot's presence job). It hears the owner in #workbench (`/clarila` commands and the pinned mode panel) and in issue threads (`@Clarila start|continue|hold|release|auto|manual|auto-ship|stop|refresh`). It enrolls an issue into its own worktree, starts or continues one Codex context per issue, and shows Working only after the native turn is observed. See [modes](references/operations.md#modes-and-owner-controls). A skill run never starts other issues itself.
6. When PR cards are enabled, the PR bot owns the PR, review and merge cards in the same canonical issue thread. A newly validated PR revision gets a fresh review handoff. GitHub's confirmed merge gets its own receipt. The existing Go Gateway forwards authenticated button and modal events to Clarila's sole coordinator. Read [PR cards](references/pr-cards.md) before changing this path.

## Keep the opening card useful

Use a short problem description with GitHub, Mode, Status, Phase and Next step. Preserve a known blocked, paused, held, merged or review state when updating its format. An old minimal card needs a status check; an open assignment alone cannot establish that work has never started. Keep priority tags and existing source/PR links. Edit the verified bot-owned original and read back every authored change.

Card formatting and issue mirroring do not subscribe the owner to threads or change issue assignees. The listener manages sidebar following separately on verified threads after work admission or an owner action on the issue card. Retain the original intent, respect a later unfollow, and remove only a follow the listener added when cleaning up automatically. Display execution buttons only while the corresponding listener binding is fresh; ordinary GitHub links remain useful without it.

## Close the publication loop

Carry the specialist's original public finding together with its intended role, issue/thread association and stable event key. Check the route before the write, then retain and read back the matching author, message and destination. Reuse the original event on a confirmed replay. An uncertain attempt keeps its existing intent and next reconciliation action.

For synchronized work lasting beyond the activity lease, renew the same role/run association at meaningful checkpoints. Finish that association on completion, pause or handoff even if publication is blocked. Show working status only for work actually observed in the corresponding Codex context.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record. The installed background jobs mirror GitHub issues and report the activity recorded by the invoked Codex skills.

## Deliverable

Return confirmed thread/message receipts or pending/unknown synchronization with a concrete reconciliation action.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.

Read the [operation-specific reference](references/operations.md) when performing this responsibility.
