---
name: commitment-ledger
description: Build a ledger of what we promised versus what they promised, and what is still outstanding, across the last few engagements with an account or contact. Uses conversation_intelligence as the primary source. Identify the account or contact by ZoomInfo ID (preferred) or name (triggers a lookup), or point it at specific calls. Use when someone asks "what did we commit to", "what are they supposed to send us", "what's still outstanding with this account", or wants an accountability check before a follow-up. Covers the last few engagements only, not full history.
---

# Commitment Ledger

A two-sided accounting of promises across recent conversations: ours, theirs, and what is still open.

## Prerequisites

`conversation_intelligence` requires at least one connected email or meeting source and consumes AI credits. `browse_engagements` (used to scope or pick engagements) requires an active integration and is free. If no conversation data exists, say so rather than presenting an empty ledger as "no commitments".

## Input

Provided via `$ARGUMENTS`:

- **Scope** (required) — an account (company ID or name/domain), a contact (contact ID or name + company), or specific calls to review.
- **Emphasis** (optional) — e.g. "just what they owe us", "anything tied to the contract". Shapes the output.

## Workflow

1. **Resolve scope.** Use a ZoomInfo ID directly, or resolve a name via `search_companies` / `search_contacts`. If the user wants specific calls and none are named, present a `browse_engagements` shortlist to pick from before spending credits.
2. **Extract commitments.** Run `conversation_intelligence` scoped to the account, contact, or chosen engagement. Ask it to list commitments by side (what we said we would do; what they said they would do), with status and the source meeting. Keep CI scoped to one ID per call; it sees only the last few engagements and cannot count or topic-search, so frame this as a recent-commitments ledger, not an exhaustive audit.
3. **Reconcile.** Mark each commitment open, done, or unclear based on later conversations. Flag anything overdue or contradicted. Attribute every line to a source meeting; do not list a commitment the conversation does not support.

## Output Format

### Commitment Ledger — [Account / Contact]

*Covers the last few engagements (through [date]). Not a full-history audit.*

**We owe them**
| Commitment | Made on | Status |
|------------|---------|--------|

**They owe us**
| Commitment | Made on | Status |
|------------|---------|--------|

**Outstanding / overdue** — a short list of what most needs chasing, with who owns it.

### When there is no data

If no conversation data is available for the scope, report that the ledger cannot be built from conversations and point the user to their ZoomInfo admin to confirm integration coverage.
