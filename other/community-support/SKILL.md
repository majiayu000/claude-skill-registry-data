---
name: community-support
description: Run support and community well — intake/SLAs, help docs, triage loops, release comms, moderation.
version: 1
triggers: community, support, help desk, triage, moderation, release notes for users
category: Everyday life
blurb: Run support and community well — clear intake, honest answers and feedback that feeds the product.
archetype: knowledge
example: Set up a support process for my small product.
---

# Community & Support

Support is where the product meets reality. Make it easy to ask, fast to triage, honest to answer — and feed everything back into the build loop.

## When to use
- Standing up or running support channels (issues, email, chat, community).
- Preparing release communications or handling incident comms.
- Community guidelines, moderation, contributor care.

## Method
1. **Intake & SLAs**: defined channels + response-time targets by severity (outage > broken > question); every message lands somewhere tracked — no support DMs vanishing into history.
2. **Help that deflects**: FAQ/help docs for the top recurring questions, updated from actual tickets; fixes link a doc where possible (`technical-writing`).
3. **Triage loop**: classify (bug / feature / usage / noise); bugs need reproductions → issue tracker with evidence; features → backlog; every thread ends with a resolution or a tracked item.
4. **Response craft**: acknowledge → set expectation → deliver → confirm; own mistakes plainly; never argue publicly; never promise unshipped dates or features.
5. **Release & incident comms**: changelog highlights for users (`release-management`); incident updates with honest status ("investigating" ≠ fake precision); follow-up after resolution.
6. **Community norms**: code of conduct; consistent, documented moderation; celebrate contributors; keep spaces spam-free without turning hostile.
7. **Measure lightly**: first response time, resolution time, recurring themes, quiet satisfaction signals; monthly review; themes feed product (`product-analytics`).

## Quality gates
- [ ] Channels + SLAs documented; intake is tracked.
- [ ] Top-10 themes have help docs or backlog entries.
- [ ] Incident comms templates ready (with honesty rules).
- [ ] Community guidelines + moderation process exist where a community runs.

## Red lines
- Never promise what isn't shipped; never leak reporter privacy in public threads; no unanswered "obvious" issues — triage, then prioritize deliberately.

## Related
`technical-writing` · `product-analytics` · `observability-ops` (incident comms).
