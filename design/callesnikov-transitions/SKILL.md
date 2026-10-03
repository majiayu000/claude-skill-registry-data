---
name: callesnikov-transitions
description: Lightweight frontend motion reference inspired by transitions.dev. Use when Codex needs to pick or describe tasteful UI transitions for web apps, prototypes, dashboards, landing pages, component states, modals, dropdowns, panels, page changes, badges, number updates, success/error feedback, avatar stacks, or when the user asks for animation ideas without requiring full implementation code.
---

# Callesnikov Transitions Variations

Use this as a motion idea map, not a heavy animation library. The source inspiration is `https://transitions.dev/`, a compact catalog of essential product UI transitions.

## Vibe

Keep motion practical: tiny, legible, fast, and tied to user intent. Prefer one good transition over decorative chaos. Always respect `prefers-reduced-motion`.

## Quick Picker

| UI moment | Transition idea | Feel |
|---|---|---|
| Card expands/collapses | Card resize | Smooth layout confidence |
| Number changes | Number pop-in | Digit flip, blur, slight stagger |
| Badge appears | Notification badge | Diagonal slide plus spring pop |
| Label/text changes | Text states swap | Soft blur swap in place |
| Dropdown opens | Menu dropdown | Origin-aware open/close |
| Modal opens | Modal open/close | Scale, fade, anchored calm |
| Panel appears | Panel reveal | Slide/reveal from a region |
| Page/detail changes | Page side-by-side | Forward/back spatial movement |
| Icon changes | Icon swap | Scale, fade, blur |
| Task completes | Success check | Draw/rotate/bob, restrained celebration |
| Avatar/chip stack hover | Avatar group hover | Distance-falloff lift |
| Invalid input | Error state shake | Short shake, then settle |

## How To Interpret User Requests

- "Сделай живее", "добавь прикольный transition" -> pick the closest UI moment from the table.
- "Без кринжа", "дорого", "аккуратно" -> shorter duration, softer easing, less travel, no bounce except success/badge/avatar.
- "Вау", "чуть сочнее" -> add blur, tiny overshoot, stagger, or SVG path draw.
- "Формы/ошибка/валидация" -> error state shake.
- "Успешно/готово/оплачено" -> success check, maybe icon swap first.
- "Меню/поповер/дропдаун" -> menu dropdown, transform-origin from trigger.
- "Модалка" -> modal scale/fade, background stays calm.
- "Карточка меняет размер" -> card resize; do not fake it with a full page transition.
- "Страница туда-сюда" -> page side-by-side.
- "Покажи варианты" -> return 3-5 matching ideas, not code.

## Adaptation Rules

For React/Vue/Svelte/HTML/CSS, adapt the idea to the local stack instead of forcing a specific snippet.

- Use CSS variables for duration, distance, blur, scale, and easing.
- Keep state explicit: `data-state`, `data-open`, `.is-entering`, `.is-leaving`, `.is-error`, `.is-success`.
- Avoid `transition: all`; animate named properties only.
- Prefer transform/opacity/filter over layout-heavy properties, except intentional card resize.
- Keep durations mostly `120-400ms`; success/avatar can go a bit longer.
- Add `@media (prefers-reduced-motion: reduce)` with minimal/no motion.
- Do not add Framer Motion/GSAP/etc. unless the project already uses it or the user asks.
- Match existing design system naming and file structure.

## Format Variations

- **Production frontend:** propose exact component/state hooks and compact CSS.
- **Prototype/mockup:** describe the motion in plain language and timing.
- **Design spec:** write transition name, trigger, duration, easing, properties, reduced-motion behavior.
- **Presentation/site polish:** use motion sparingly: hero entry, card hover, panel reveal, success state.
- **Game-like UI:** allow more bounce/stagger, but keep controls readable.

## Tiny Motion Recipe

When asked to add a transition:

1. Identify the UI moment.
2. Pick one transition idea.
3. State why it fits in one sentence.
4. If editing code, add only the needed CSS/state hooks.
5. Verify text and controls do not jump, overlap, or become unreadable.

## Source Catalog

Transitions.dev currently highlights these twelve ideas: card resize, number pop-in, notification badge, text states swap, menu dropdown, modal open/close, panel reveal, page side-by-side, icon swap, success check, avatar group hover, and error state shake.
