---
name: accessibility
description: >-
  Accessibility for this prototype: WCAG 2.2 AA checklist tailored to the app, senior mode spec, screen-reader
  patterns for routes, chat and confirmations, keyboard, reduced motion, contrast, and how to test (axe in
  Playwright, VoiceOver/TalkBack scripts, 200% zoom). Use when building or reviewing any UI, or for "a11y",
  "WCAG", "screen reader", "seniors", "large text", "keyboard".
---

# Accessibility

Accessibility is a judging angle ("more accessible" than the reference), not polish. The floor is WCAG 2.2 AA.
Owners: the `ui-engineer` agent builds it, and the `accessibility-auditor` agent checks it. Related: the
`plain-polish` skill (cognitive accessibility), the `design-system` skill (tokens), and the
`web-vitals-a11y-audit` skill for Lighthouse runs.

## Checklist (every screen)

| Area            | Requirement                                                                                                                              |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Structure       | one `<h1>` per screen, logical headings, landmarks (`header`, `nav`, `main`)                                                             |
| Names           | every control has an accessible name; icon-only buttons have `aria-label`                                                                |
| Targets         | ≥ 48×48 px (56 in senior mode), ≥ 8 px apart (WCAG 2.5.8 is the minimum, we go higher)                                                   |
| Contrast        | text ≥ 4.5:1, large text and UI parts ≥ 3:1, in every theme                                                                              |
| Colour          | never the only signal: urgency = colour + icon + text ("za 3 dni")                                                                       |
| Text size       | usable at 200% zoom and with OS large text; no truncation of key info; reflow at 320 CSS px                                              |
| Focus           | visible focus everywhere (`--focus`, 2 px+), not obscured by sticky bars (2.4.11)                                                        |
| Keyboard        | all actions reachable; no traps; Esc closes sheets; focus returns to the trigger                                                         |
| Motion          | `prefers-reduced-motion` turns off non-essential animation; nothing flashes                                                              |
| Forms           | visible labels, hints and errors linked with `aria-describedby`, no placeholder-only labels; accessible authentication is N/A (no login) |
| Time            | no timeouts in matters; if a confirmation expires, say so and offer to extend                                                            |
| Language        | `<html lang="pl">`; foreign-language snippets marked `lang`                                                                              |
| Help            | consistent "Pomoc" location on every screen (3.2.6)                                                                                      |
| Redundant entry | never ask twice for data we already have (3.3.7), which is also our once-only story                                                      |

## Screen-reader patterns

- **Route changes:** move focus to the new screen's `<h1>` (tabindex -1) and update `document.title`.
- **Assistant chat:** messages in a `role="log"` container with `aria-live="polite"`; announce "Asystent
  pisze…" once, not per token; new rich cards are announced by their heading. The input keeps focus after
  sending.
- **Confirm before action:** `ConfirmCard` is a region with a heading that states the action; the primary
  button text repeats it ("Zastrzeż dowód"), never just "OK".
- **Result:** success or failure in a `role="status"` region, and focus moves to the result heading.
- **Documents:** read as a definition list (`<dl>`), and the watermark is announced once as part of the
  heading ("mDowód, prototyp").
- **Reminders:** the tile's accessible name includes what, when and urgency.

## Senior mode (a first-class mode, offered on first run)

- Base text ≥ 20 px, targets ≥ 56 px, line height ≥ 1.6.
- A simplified home: the three most likely actions plus "Porozmawiaj z asystentem"; nothing else above the
  fold.
- Fewer choices per screen (≤ 3 primary), no gestures-only actions, no hidden menus.
- Explicit "Wstecz" buttons in addition to system back.
- Optional read-aloud of each screen (speechSynthesis, pl-PL) with a stop button.
- Confirmations restate the consequence in one sentence.

## Help from a relative (feature idea; product decision)

Shared access ("pełnomocnictwo" in plain words: "Pozwól córce pomagać Ci w sprawach"): invite a trusted
person, choose what they can see or do, see a log of what they did, revoke anytime. This is strong for the
"more accessible" angle and the privacy angle. Specify it with the `service-journeys` skill before building.

## Testing

1. **Automated:** `@axe-core/playwright` on every screen in every E2E flow (phone viewports, light, dark and
   senior). Zero violations is the bar; any exception is documented in the test with a reason.
2. **Keyboard-only pass:** Tab through each flow; note order, traps, and invisible focus.
3. **Zoom:** 200% browser zoom plus a 320 px wide viewport, with no horizontal scroll and nothing cut off.
4. **VoiceOver (iOS Safari) script:** open the link, swipe through home, open a reminder, complete one matter,
   and confirm. Record what was announced. Same with **TalkBack** (Android Chrome).
5. **Reduced motion:** emulate in DevTools / Playwright (`reducedMotion: 'reduce'`).
6. Report as: issue · WCAG criterion · screen · steps · severity · suggested fix. The `accessibility-auditor`
   agent owns the format.

Never claim screen-reader support from axe alone. Say which manual pass was actually run.
