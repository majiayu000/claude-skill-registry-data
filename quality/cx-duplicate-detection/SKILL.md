---
name: cx-duplicate-detection
description: Use to find duplicate or repeated support conversations and produce a reviewable merge plan. Trigger for "find duplicate tickets", "customers contacting us twice about the same thing", deduplicating a helpdesk, cleaning up ticket volume, or measuring how much of your contact volume is the same issue submitted more than once.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Finding duplicate conversations

Duplicates inflate volume, split context across tickets so agents answer without
the full history, and make a customer feel unheard. They also distort every metric
you compute — two tickets for one problem doubles the contact rate and halves the
apparent first-contact resolution rate.

This produces a **reviewable merge plan**, not a change. Applying it is a separate
skill, deliberately.

## Why detection and merging are separate skills

Merging is irreversible on every major helpdesk. So the decision and the action
are split:

```
canonical export ──▶ cx-duplicate-detection ──▶ merge-plan.jsonl ──▶ <platform>-apply-merges
   (read-only)            (read-only)              (reviewable)          (writes, --apply)
```

Three things this buys you, and the reason every mutation in this catalog works
this way:

- **An agent can safely propose a bulk merge** without being able to perform one.
- **The plan is a diff a human can review** before anything happens, entry by entry.
- **The applier re-validates against live state**, so a plan that has gone stale
  cannot cause a wrong merge.

## What counts as a duplicate

Not "similar topic". A duplicate is **the same customer raising the same problem
more than once**, which happens for mundane reasons:

- The form was submitted twice, or an email retried.
- The customer got no reply and tried another channel.
- The customer replied to a closed ticket and the platform opened a new one.
- An integration created a ticket the customer had already raised by email.

The cross-channel case is the most valuable to catch and the one single-channel
tooling always misses.

**Related is not duplicate.** A customer with three separate genuine problems is
not a duplicate; merging them destroys the record of two of them. Detection here
is deliberately conservative for that reason.

## The safety boundary: identity

Candidates **must share a `customer_id`**. Cross-customer merges are never
proposed, because a wrong one discloses one person's conversation to another —
which is a data breach, not a data-quality problem.

Consequences you need to accept:

- **Conversations with no `customer_id` are excluded** by default. `--allow-null-customer`
  exists but weakens the boundary to text similarity alone; review every proposal
  individually if you use it.
- **Poor identity resolution means missed duplicates.** If the same person appears
  as two customer records, their duplicate conversations are invisible here. Fix
  identity first — see `cx-conversation-schema` for the resolution strategies.

That trade is deliberate: missing a duplicate costs a little efficiency, merging
two customers' conversations costs a lot more.

## Usage

```bash
node scripts/detect-duplicates.mjs ./out/zendesk --out ./plans
```

Input is a canonical export from any platform export skill in this catalog, so
this works identically against Zendesk, Intercom, Freshdesk, Gorgias, Front, and
the rest.

**Arguments**

- `--out <dir>` — where to write `merge-plan.jsonl`. Default `./plans`.
- `--window-hours <n>` — only pair conversations opened within this window of each
  other. Default 72.
- `--min-confidence <high|medium|low>` — what enters the plan. Default `medium`.
- `--allow-null-customer` — permit matching without an identity. Off by default.

**Message bodies are required.** A `--no-bodies` export has nothing to compare, and
the script reports how many conversations it had to skip for that reason.

## How matching works

Comparison is on the **first public customer message**, falling back to the subject
when bodies are missing. Text is normalised to strip the things that differ between
genuine duplicates — order numbers, dates, URLs, email addresses, and quoted email
history — then compared as a token set with Jaccard similarity.

Stripping digits matters: two submissions of the same complaint often differ only
in an order reference, and leaving numbers in suppresses the match.

| Tier | Rule |
| --- | --- |
| **high** | Similarity ≥ 0.80, **or** near-identical subject within 1 hour |
| **medium** | Similarity ≥ 0.55 |
| **low** | Similarity ≥ 0.35 |

The identical-subject-within-an-hour rule catches double submissions where the
bodies were retyped and differ in wording.

Clusters are formed by union-find, so three conversations about one problem become
a single merge rather than three pairs. Only links at or above `--min-confidence`
join a cluster — a weak link must not silently chain two strong clusters together.

**The target is the earliest conversation.** It holds the original context and is
the one the customer and any prior agent already referenced.

## Reading the plan

Each line proposes one merge:

```jsonc
{
  "target_id": "1",              // survives
  "source_ids": ["2", "3"],      // merged into the target
  "customer_id": "900",
  "confidence": "high",          // the weakest link in the cluster
  "channels": ["email", "chat"],
  "statuses": ["open", "open"],
  "preview": "i returned my order three weeks ago and the refund",
  "evidence": [
    { "source_id": "2", "similarity": 0.91, "hours_apart": 0.5, "direct": true }
  ]
}
```

Two fields deserve attention when reviewing:

- **`confidence` is the weakest link**, not the average. A cluster is only as
  trustworthy as its loosest pairing.
- **`direct: false`** means that conversation is linked to the target *through
  another conversation*, not to it directly. Chained similarity is weaker than it
  looks; review those individually.

## Present results to the user

1. **The gap between candidate pairs and clusters proposed**, and the confidence
   split. High-confidence clusters can be bulk-approved; medium should be sampled;
   low should be read.
2. **What was excluded and why** — no `customer_id`, no message text, deleted.
   If a large share was excluded for identity, say that duplicate detection is
   currently blind to most of the data and fixing identity comes first.
3. **Cross-channel clusters**, called out separately. These are usually genuine and
   are the strongest evidence that customers are not getting a reply in the first
   channel — which is an operational finding, not just a cleanup task.
4. **Duplicate rate as a metric**, not just a cleanup list: duplicates as a share
   of conversations tells you how much of your volume is self-inflicted. That number
   is often the most useful output.
5. **That this is a proposal.** Nothing has changed. Name the apply skill and the
   fact that merging is irreversible.
6. **Transitive clusters** flagged for individual review.

## Troubleshooting

**No duplicates found in an account that obviously has them** — check the excluded
counts. Missing `customer_id` or a `--no-bodies` export are the usual causes.

**Obvious duplicates rated only medium** — the customer rephrased. Lower
`--min-confidence` and review, or widen `--window-hours` if they contacted again
days later.

**Clusters that are too large** — similarity is chaining through a generic message
("any update?"). Raise `--min-confidence` to `high`, which requires direct strong
links.

**Different customers proposed for merge** — this cannot happen unless
`--allow-null-customer` is set. If you see it, that flag is on; turn it off.
