---
name: app-feature-craft
description: Use when implementing or improving a user-facing app workflow. Guides product-grade UX, frontend, backend/API behavior, AI/provider or long-running task states, tests, and end-to-end verification from rough requirements to a shippable feature.
license: MIT
---

# App Feature Craft

Use this skill to turn an app request into a feature users can actually rely on.
Default to shipping the smallest complete behavior, not a technical stub.

## Workflow

1. Ground in the product before designing.
   - Inspect routes, screens, state stores, API clients, backend handlers, data
     models, tests, packaging scripts, and existing copy.
   - Resolve discoverable facts from the repo before asking the user.
   - If visual behavior matters, inspect screenshots or run the app.

2. Define the user-facing outcome.
   - State what the user can do after the change.
   - Identify the audience, success criteria, in/out of scope, data safety
     constraints, and where the behavior must appear.
   - Separate optional convenience from behavior required for a complete feature.

3. Design the whole path.
   - Cover UI states: empty, loading, success, failure, stale data, first-run,
     and already-configured.
   - Keep controls near the user's task context. Avoid bolted-on panels,
     rigid form-heavy surfaces, or result views that disappear behind an
     ambiguous "back" action.
   - Prefer reading-first UI with focused edit affordances for dense knowledge
     or writing surfaces.
   - Cover data/API behavior: persistence, validation, compatibility,
     migration, idempotency, and failure modes.
   - Cover lifecycle behavior for desktop apps: startup, restart, sidecars,
     installer state, and local paths when relevant.
   - For long-running AI or provider work, design background progress,
     reopening/recovery, cancellation semantics, and honest stage labels before
     implementing the request.

4. Implement narrowly.
   - Follow existing local patterns instead of inventing a new framework.
   - Keep user data safe by default; never delete, overwrite, or migrate
     destructively unless the user explicitly asked for it.
   - Do not expose raw backend/browser errors in public UI.
   - Do not report a fake success for external integrations. Mocked tests prove
     code paths, not real provider availability.
   - Run only the user-selected AI/profile/configuration set. Do not silently
     add a default provider after the user made an explicit choice.
   - Keep separate provider profiles and locally saved keys isolated by owner;
     never let one profile's credential overwrite another profile's source.
   - Make AI-generated drafts, candidate imports, and writeback actions
     review-first unless the user explicitly requested automatic mutation.

5. Verify from the user's seat.
   - Run focused unit/API tests for changed behavior.
   - Run frontend tests for state, copy, and interactions.
   - Use browser or app screenshots for UI/visual changes.
   - For provider, installer, or filesystem features, run at least one real
     local smoke test when credentials and environment are available.
   - For background jobs, verify close/reopen, status reconnect, cancellation,
     completion, and failure states without resending the provider request.

6. Report the result.
   - Summarize user-visible changes, important files, tests run, and any
     residual risk.
   - Say clearly when a test was mocked, skipped, or only verified locally.

## Reference Use

Read `references/app-quality-principles.md` before implementing complex app
features, AI/provider integrations, long-running jobs, first-run experiences,
data-path behavior, or desktop lifecycle work.

Read `references/living-to-tell-casebook.md` when the task resembles one of
the captured cases: startup feedback, Not Found cleanup, AI provider transport,
data location safety, installation/version mismatch, async selection races, or
motif/excerpt deduplication, AI result recovery, profile key isolation, or
release asset verification.

## Ask Only When Needed

Ask the user only when the decision is product intent and cannot be discovered
from the codebase. Prefer one concrete tradeoff question over a broad design
question.
