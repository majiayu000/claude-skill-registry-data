---
name: ship-readiness
description: Advisory pre-deploy/pre-handoff checklist (not a blocker). Use when preparing a project for deployment, release, or client handoff — deploy, ship, go live, release, hand off.
---

# Ship-readiness (advisory checklist — not a blocker)

This is a **practical checklist**, not an enforced gate. Report items as pass/fail with evidence — never assert without checking. Nothing here blocks a build; it just helps you not hand off something broken. **Production deploys should still have explicit user approval.**

## Universal
- Before declaring a run complete, run `node .claude/forge-bin/forge-verify.cjs <run_id>` and report its result; a mismatch means rework, not a pass.
- No test mode, mock backend, or fake/sample data left in.
- No localhost URLs, debug/test banners, or debug-only UI.
- Secrets in env; `.env.example` uses placeholders; no real secrets committed.
- Runtime artifacts swept for leaked secrets too, not just source: `node .claude/forge-bin/forge-secret-scrub.cjs [--json]` (advisory, reports location only) — covers `.claude/forge-runs/*/events.jsonl`, which the doctor's git-tracked leak scan cannot see because it is gitignored.
- No unfinished placeholder content/copy.
- Forms submit and validate; error handling present on all I/O.
- Mobile **and** desktop layout intact; primary CTA clear.
- *Optional:* for important code, run the `codex-reviewer` agent (Codex) and/or `security-reviewer` — advisory, not required.

## Website / landing page
Perf/SEO/a11y pass; meta/OG + canonical; favicon; 404 route; no broken links; responsive at ~360/768/1280; no Lorem/test copy; CTAs/links resolve.

## Full-stack app / auth
Auth enforced server-side on protected routes; input validation per endpoint; secrets out of the client bundle; DB migrations reversible; e2e green.

## API integration
Retries/backoff + timeout; idempotent writes; consistent error envelope; pagination; webhook signature verification; safe logging.

## Dashboard / data viz
Empty/loading/error states; correct aggregation (no silent NULL drops); timezone correctness; no PII leaked client-side.

## n8n
Webhook method correct; input schema validated; credentials set (not hardcoded); error branch exists; retry/backoff defined; test/prod flows separated; `validate_workflow` clean. (Validation is good practice before calling it production-ready.)

## Scraping / lead-gen
Public/official-API/permitted sources only; rate limits + robots respected; no login/paywall bypass; data storage lawful + minimal; outreach **drafted only** (no bulk send without explicit user confirmation).

## AI / RAG / chatbot
Clear fallback for empty/low-confidence retrieval; source-aware answers; no hallucinated business facts; logging + human-handoff defined.

## Prediction systems
No certainty claims; confidence/risk labels on outputs; data-source quality verified; backtest shown with sample size; **no automatic real-money betting**.

## Telegram bot
Token in env only; webhook vs long-poll chosen; command allowlist; rate-limit; admin-only commands gated; graceful failure message.

## Business automation
Dry-run vs live separated; no bulk-send without confirmation; audit log; rollback/dead-letter for failed calls.
