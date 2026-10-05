---
name: sg-student-event-radar
description: Discover, verify, score, deduplicate, and maintain a personalized queue of Singapore events for international students across any user-chosen industry or field. Use when a Singapore student wants recurring event discovery, industry networking opportunities, career or project events, a five-minute review queue, optional Notion synchronization, or recommendations constrained by classes, exams, budget, location, and career stage.
---

# SG Student Event Radar

Keep reusable rules public and every user's profile, choices, database identifiers, and reports under ignored paths.

## First use

1. Run `python3 scripts/init_local_state.py`.
2. Read [references/onboarding.md](references/onboarding.md).
3. If `local/config.json` has `onboarding_complete: false`, interview the user or run `python3 scripts/configure_profile.py` interactively.
4. Run `python3 scripts/validate_config.py`. Do not scan until it passes.
5. Offer Notion, but never require it. Local Markdown and JSON are the fallback.

## Every scan

1. Read [routine-prompt.md](routine-prompt.md) completely and follow it as authoritative.
2. Read private config and ledger state.
3. If Notion is connected, read user choices before discovery.
4. Generate source queries from the configured industries, fields, roles, companies, skills, goals, and exclusions. Do not silently substitute technology interests.
5. Deduplicate listing URLs before detail fetches.
6. Verify material facts, apply hard gates, score, and keep only qualified events.
7. Write at most the configured number of undecided events to the five-minute queue.
8. Preserve user choices and make external actions only after action-time confirmation.

## Non-negotiable rules

- Prefer direct organiser or registration evidence; label missing facts `needs_verification`.
- Distinguish `success_zero` from a failed source and report partial runs loudly.
- Never lower the score threshold to fill the queue.
- Never register, pay, message, invite, add calendar entries, or submit forms without confirmation.
- Never bypass login walls or collect personal attendee data.
- Never stage, commit, expose, or quote private runtime state.

Read detailed references only when relevant:

- [onboarding.md](references/onboarding.md) for first-run questions and profile generation.
- [source-strategy.md](references/source-strategy.md) for dynamic source discovery and evidence rules.
- [scoring-rubric.md](references/scoring-rubric.md) for gates, scoring, and student-stage examples.
- [notion-schema.md](references/notion-schema.md) only when Notion is requested or already connected.

Run `python3 scripts/check_public_release.py` before publishing.
