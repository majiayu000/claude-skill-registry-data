---
description: Design high-converting popups and modals
---

# Popup CRO

Design effective popups and modals for "$ARGUMENTS". Create non-intrusive, high-converting overlays for lead capture, upgrades, and engagement.

## Prerequisites

Read `.metapowers/marketing/$ARGUMENTS/00-strategy.md`. If this file does not exist, tell the user:

> Phase 0 (Strategy) has not been completed for "$ARGUMENTS". Run `/marketing:customer-research $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/marketing/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context:**
   - Read `.metapowers/marketing/$ARGUMENTS/00-strategy.md` for audience and messaging
   - Read `.metapowers/marketing/$ARGUMENTS/02-act.md` and `.metapowers/marketing/$ARGUMENTS/04-engage.md` if they exist

2. **Define popup purpose:**
   - Lead capture (email signup, lead magnet delivery)
   - Exit intent (save abandoning visitors)
   - Upgrade prompt (free-to-paid conversion)
   - Announcement (new feature, promotion)
   - Feedback collection (survey, NPS)

3. **Design popup experience:**
   - Trigger: time-based, scroll-based, exit-intent, click-triggered, page-count
   - Frequency: how often does a user see it?
   - Targeting: which pages, which segments, new vs. returning
   - Mobile experience: slide-up vs. full-screen vs. banner
   - Dismiss behavior: easy close, remember preference

4. **Create popup content:**
   - Headline (benefit-focused, under 10 words)
   - Body copy (1-2 sentences max)
   - CTA (specific action, not "Submit")
   - Visual direction
   - A/B test variants

5. **Write the artifact** — append to `.metapowers/marketing/$ARGUMENTS/04-engage.md` under a `## Popup CRO` section:
   - **Popup Strategy** — purpose, trigger, targeting
   - **Content** — headline, body, CTA per popup
   - **UX Rules** — frequency, dismissal, mobile behavior
   - **A/B Test Plan** — what to test first
   - **Anti-Annoyance Checklist** — ensuring popups help, not hurt

## Output

Popup strategy written to `.metapowers/marketing/$ARGUMENTS/04-engage.md`. Present popup designs with copy for review.
