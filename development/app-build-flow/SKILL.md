---
name: "app-build-flow"
description: "Use when scoping or building an app or product with Claude Code: cut the idea with the five-step framework, design it twice, build locally, test in three stages, add backend, audit security twice, then ship."
---

# App build flow

From the user's playbooks: the five-step app design framework and the mobile app flow (a creator's video, Expo + Supabase), plus "design it twice" (from a software design book). Figures in the source are the presenter's statements; check current Expo, Supabase, Apple and Google docs before relying on them.

## 1. Scope with the five steps
1. **Core function:** the one thing it does.
2. **Core loop:** action to reward in under about 30 seconds (sound, animation, haptics).
3. **Accessory features:** only what supports the loop.
4. **Surface-area check:** about 5 to 7 screens, fewer for simple apps. Cut the rest.
5. **Retention hook:** why the user comes back (daily check-in, a 3-day challenge, something that decays if ignored).

## 2. Design it twice
Before building, write a second design that is genuinely different (pretend the first is banned). Compare, then pick or combine, and keep an "alternatives considered" section. Keep interfaces small and push complexity inside.

## 3. Build
- Scaffold, then record the architecture in CLAUDE.md and start each task in a fresh session (see `task-tier-loop`).
- Build locally first with local storage, no database. Iterate in short rounds and add a developer test menu (skip onboarding, force states, clear data).
- Commit to GitHub after each working round.

## 4. Three-stage test, every time
Browser on the computer, then a phone mirror, then the real phone. Some things (push, haptics, status bar) only fail on the real device.

## 5. Backend and AI
- Supabase: enable row-level security, keep the URL and publishable key in config, secrets in .env or Supabase secrets, never in chat or in the app bundle.
- AI features go through a server function that calls the Claude API; the app never holds the API key. Test prompts on about 10 simulated examples first.
- Repeat the three-stage test after the backend is added.

## 6. Design pass after it works
Match a real reference, use `ui-design-guardrails`, have Claude open every screen and list inconsistencies, fix in a loop.

## 7. Security audit twice
In a fresh session audit for hard-coded secrets, missing server-side validation, open database policies, inconsistent auth, and expensive operations an attacker could repeat. Fix, clear, audit again, then repeat the three-stage test. For payments use `storefront-payment-check`.

## 8. Ship
App config and build (EAS for Expo), store accounts, a public privacy policy and support page, screenshots, a test login for reviewers, then submit. Approval is not guaranteed; read rejection notes and resubmit.