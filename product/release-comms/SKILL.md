---
model_tier: inherit
name: release-comms
description: "Turn a shipped changelog into a release narrative — value-not-feature framing, audience-segmented surfaces. Triggers on 'announce the release', 'write changelog post'."
status: active
tier: senior
domain: product
context_spine: [product, team]
recommended_for_user_types: [creator, gtm, founder]
workspaces:
  - gtm
packs:
  - gtm-marketing
trust:
  level: professional
install:
  removable: true
---

# release-comms

## When to use

- A release is shipping that contains user-facing change and the team is about to send a feature-list email.
- A changelog draft reads like a commit log — engineering-honest, but unparseable for the user.
- Multiple comms surfaces (in-app, email, social, docs) are about to be written by different people from the same release.

Do NOT use for incident comms (see `incident-commander`),
deprecation announcements that need legal sign-off, or pre-release
discovery — this skill assumes the change is **shipped**.

## Cognition cluster

- **Mental model 16 — Leading vs. lagging indicators.** A release
  note is the lagging artifact; the leading version is the in-app
  prompt that fired before the user found the change-log. See
  [`docs/contracts/mental-models.md`](../../../docs/contracts/mental-models.md) § 16.
- **Value-not-feature heuristic.** Every paragraph passes the *"so
  the user can ___"* completion. Failing rows go back for re-write.

## Procedure

### Step 0: Ground the release

1. Read the merged PR list / changelog block / release branch diff. The release is the **what**; comms is the **so what**. Conflate the two and you ship marketing.
2. Read the **product** and **team** slots of the [context-spine](../../../docs/contracts/context-spine.md) (if the consumer project has filled them) for bounded scope and release cadence — surface choice depends on cadence (weekly: in-app + log; quarterly: email + post; major: all four).
3. Identify the **single dominant change** the release ships. A release with three "headliners" reads as three half-announcements.

### Step 1: Audience-segment

1. Three audiences max: **active user**, **at-risk / lapsed user**, **prospect**. More segments fragment the message; fewer hides the routing.
2. Per audience, write one sentence: *"After this release, you can …"* completing with a user-side verb, not a product-side feature.
3. If two audiences end up with the same sentence, collapse them — segmentation that does not change the message is theatre.

### Step 2: Map surfaces to audiences

1. **Changelog** (always) — engineers + power users; truthful, dense, link-heavy. Source of truth — every other surface points back here.
2. **In-app prompt** — active users; ≤ 1 sentence + 1 CTA; fires for users whose past behaviour predicts they'll touch the new path.
3. **Email** — at-risk / lapsed; one headline value, one CTA, one paragraph of context. No feature lists.
4. **Social / blog** — prospect; the **why**, not the **what** — frame against the user job (cite [`customer-research`](../customer-research/SKILL.md) if a switch-event surfaced).

Cut surfaces aggressively. A weekly release does not need a blog post.

### Step 3: Draft each surface from the changelog

1. Open the changelog. Per surface, copy the dominant change line, then **rewrite the verb subject** from "we" to "you".
2. Strip qualifiers ("now", "even better", "lightning-fast"). They are noise, not signal.
3. Run the *"so the user can ___"* completion on every paragraph. Failing paragraphs are cut, not edited.

### Step 4: Truth-check

1. Every claim links back to a changelog row or a doc URL. Unsourced claim → cut.
2. No tense games — past for shipped, future for coming-soon (and only if the date is committed). "Roadmap" lives outside this skill.
3. Names match the product surface. If the in-app says "Reports" and the email says "Insights", the user fires the lookup tax.

### Step 5: Hand off

1. Produce the four artifacts (see `## Output`).
2. Hand to whoever owns the send. Do not embed scheduling or A/B test plans here — that is RevOps.

## Related Skills

**WHEN to use this**

- The change is **shipped** and needs to reach existing users.
- Multiple comms surfaces will be written by different people from the same source.
- The team is about to default to a feature-list email.

**WHEN NOT to use this**

- Production incident comms — route to [`incident-commander`](../incident-commander/SKILL.md).
- Pre-release discovery / validation — route to [`customer-research`](../customer-research/SKILL.md).
- Funnel-stage diagnostics post-release — route to [`funnel-analysis`](../funnel-analysis/SKILL.md).
- Ranking which release to comms next — route to [`rice-prioritization`](../rice-prioritization/SKILL.md).

## When the agent should load this

- "Write the release notes for sprint 47."
- "We're shipping the new export — how do we announce it?"
- "Draft the changelog email for last week's batch."
- "What's the in-app prompt copy for the redesign?"
- "Turn the merged PR list into something users can read."

## Output

1. **`release-narrative.md`** — single source of truth: dominant change, audiences (1–3), per-audience *"After this release, you can …"* sentence, links to source changelog rows.
2. **`changelog-entry.md`** — engineer-honest, dense, link-heavy block ready to paste into the project's changelog.
3. **`comms-pack.md`** — per-surface drafts (in-app prompt, email, optional social/blog), each ≤ the surface's hard cap, each pointing back to `changelog-entry.md`.
4. **`comms-checklist.md`** — pre-send checks: every claim sourced, names consistent across surfaces, audience match, "so the user can …" completion passing on every paragraph. Hand-off artifact for the senior PO ([`product-owner`](../../personas/product-owner.md); senior persona shipping in next plate).

## Gotcha

- The default failure mode is feature-list email — written to make engineering feel seen, not to help the user.
- Marketing puffery ("revolutionary", "delightful") fails the source check; cut on sight.
- Two surfaces using different names for the same thing is the highest-frequency support-ticket trigger after a release.
- Hidden coming-soon claims in past-tense paragraphs erode trust faster than missing the comms entirely.

## Do NOT

- Do NOT promote a coming-soon item alongside shipped items — the user cannot tell which is which and stops trusting the next note.
- Do NOT let a long-tail change steal the headline — the dominant change earns the headline, the long tail goes in the changelog.
- Do NOT ship surfaces without the truth-check pass; an unsourced claim survives in social longer than the release does.
- Do NOT paste more than a short excerpt from a linked source (commit message, PR body, issue thread) — `content-quoting-floor` caps verbatim quotes at 15 words, one per source; paraphrase the rest.

## Runnable example

Sprint 47 ships a one-click monthly export and three small bug fixes:

- Dominant change: one-click export. Bug fixes go in changelog only.
- Audiences: active user (will use it), at-risk (export friction was a churn trigger per [`customer-research`](../customer-research/SKILL.md) evidence-log).
- "After this release, you can pull a board-ready monthly report in one click." (active, at-risk — same sentence ⇒ collapse to one).
- Surfaces: changelog (full), in-app prompt to active users on next month-end, email to at-risk cohort with the same sentence and one CTA. No social.
- Truth-check: claim links to the export PR; "one click" is literal — verified against the shipped UI.

→ Final prose pass for audience-facing output: [`humanizer`](../humanizer/SKILL.md) — remove AI-writing tells before delivery.
