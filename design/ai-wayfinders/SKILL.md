---
name: ai-wayfinders
description: >-
  Use when designing AI product first-run or blank-slate UX — chat empty state,
  example prompts, capability discovery, templates, nudges, or follow-ups.
  Trigger on "users don't know what to ask", onboarding, suggestion chips, or
  discoverability.
---

# AI Wayfinders — discoverability UX

Wayfinders reduce blank-slate anxiety and teach **what the product can actually
do** without over-claiming.

Pattern catalog: [references/patterns.md](references/patterns.md).
Adapted from tommyjepsen/awesome-ux-skills `ai-wayfinders`.

## When to use

- Chat empty state, composer placeholders, suggestion chips, command palette,
  capability help, first voice session.
- Fixing "I didn't know it could X" or "it claimed Y and can't".
- **Not** for: visual craft (`ui-fix-observe-first`), HITL confirms
  (`ai-governors`), or privacy disclosure (`ai-trust-builders`).

## Constraints

1. **Wayfinders must track real capabilities and flags.** A chip that offers a
   blocked or missing feature is a product bug.
2. **Voice / spoken** — few short suggestions; no dense galleries.
3. **Cost honesty** — suggestions that imply spend should label cost class.
4. **No dark-pattern engagement** — no fake urgency; randomize only to reduce
   blank-slate pressure.

## Surface → pattern map

| Surface | Prefer | Avoid |
|---|---|---|
| Chat empty | Initial CTA + 3–5 suggestions + honest cannot-do | Endless gallery of unproven capabilities |
| Voice first start | Nudge for mic permission + mode explain | Auto-start without consent |
| Command palette | Templates for frequent tasks | Duplicating every nav link |
| Messaging channels | Rare contextual follow-ups | Prompt galleries in-chat |
| After a tool/run | Follow-ups tied to *this* result | Generic "ask me anything" |
| Capability / help copy | Show constraints | Inflated marketing bullets |

## Eight patterns (short)

1. **Initial CTA** — scaffolded composer, not a naked box.
2. **Example Gallery** — curated, actionable; dense UIs only.
3. **Suggestions** — 3–6 chips; prefer contextual over static.
4. **Templates** — madlibs for repeatable jobs.
5. **Nudges** — one tip at the moment of need.
6. **Follow-ups** — after a result, not during typing.
7. **Prompt Details** — show constraints so power users learn the system.
8. **Randomize** — optional shuffle of safe examples; never engagement bait.

## Capability-honesty checklist

- [ ] Mechanism exists on the live flag set (ON and OFF copy if flag-gated).
- [ ] Medium is correct (voice tip is spoken-safe).
- [ ] Cost class is acceptable as a default click (or labeled).
- [ ] Failure copy distinguishes dead capability vs gate miss when possible.

## Output format

1. **Blank-slate moment** — which surface.
2. **Patterns** — 1–3.
3. **Exact copy candidates** that pass the honesty checklist.
4. **Measure** — what observe-first or dogfood will verify.

## Cross-references

- `ui-fix-observe-first` — measure UI before declaring discoverability fixed
- `ai-trust-builders` — disclosure beside onboarding
- `ai-governors` — don't replace confirms with friendly chips
