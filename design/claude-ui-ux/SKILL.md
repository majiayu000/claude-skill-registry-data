---
name: claude-ui-ux
description: Design and build interfaces in the calm, warm, typography-led style popularised by Claude-style assistants — content-first layout, soft neutral palette with one amber accent, generous spacing, quiet motion — plus the UX patterns of agentic/chat products (streaming replies that never jump, collapsible tool steps, permission prompts, plan panels, graceful empty/loading/error states). USE WHEN the user asks for a "Claude-like", "Anthropic-style", "calm", "minimal but warm", "premium chat UI", "assistant UI", "agent UI", "make it feel like Claude", or wants a chat/copilot/agent surface designed or polished.
---

# Claude-style UI & UX

Goal: an interface that feels calm and trustworthy — the content is the hero, chrome recedes, motion explains rather than decorates, and every state (thinking, working, waiting on you, failed) is legible at a glance. This is a design *sensibility*, not a brand kit: adapt tokens to the host (VS Code theme variables, the product's palette) rather than hard-coding colours.

## 1. Read the room first
- Find the existing design tokens and component vocabulary (`grep_search` for `--`, `theme`, `tokens`, `tailwind.config`, the component library). Extend them; never add a second palette or spacing scale.
- Identify the surface: a full app, a side panel (narrow, 240–480 px), a dialog, a terminal. Narrow surfaces need container queries and icon-only collapses, not a scaled-down desktop layout.
- If a screenshot was attached, list the concrete problems before touching anything (crowding, competing accents, misaligned baselines, unclear state, truncation).

## 2. Visual language
**Palette — warm neutrals, one accent.**
- Background: a warm off-white (≈ `#F7F5F0`) or warm charcoal (≈ `#1F1E1B`) rather than pure white/black; surfaces one step lighter/darker; borders at ~10–14 % foreground alpha.
- Text: near-black warm grey (≈ `#2B2A27`) on light, warm light grey (≈ `#E8E4DC`) on dark; secondary text ~65 % of that.
- One accent, used sparingly for identity and "the model is working": an amber/terracotta family (≈ `#D97757` / `#F2A33A`). Primary buttons may use the host's accent (in VS Code: `--vscode-button-background`). Semantic colours only for meaning: success green, warning amber, error red — never as decoration.
- Contrast ≥ 4.5:1 for text, ≥ 3:1 for UI. Support light and dark through tokens from day one.

**Typography — a quiet hierarchy.**
- Body: a humanist sans at 13–15 px (UI) / 16–17 px (reading), line-height 1.5–1.6, max ~70 characters per line.
- Display/headings: optionally a soft serif (e.g. a Tiempos/Source Serif-like face) at 1.5–2× body with line-height 1.2 — the single most recognisable cue of this style. Never more than two families.
- Code: the editor's monospace at 0.92× body with tabular numbers for stats; inline code gets a subtle tinted background, not a border.

**Space, shape, depth.**
- 4/8 px spacing scale; tight inside a group (4–8), loose between groups (16–24), generous page margins (24–48 on wide surfaces).
- Radii: 6 / 8 / 12 px (controls / cards / sheets); pill radius for chips. Rounded but not bubbly.
- Depth from tint and 1 px borders, not shadows. Reserve a soft shadow for floating layers (popovers, lightbox).
- Icons: 16 px, 1.5 px stroke, outline style, inherit `currentColor`. Pair with text unless the meaning is universal.

**Motion — brief and explanatory.**
- 120–250 ms, ease-out; animate opacity/transform only (no layout properties). Fade-in new turns, slide-in panels, pulse only the one thing that is "live".
- Streaming text must not jiggle: stable caret element, no re-layout of finished blocks, no scroll-fighting (see §3).
- Honour `prefers-reduced-motion`: replace spinners with a static dimmed glyph plus text; keep opacity changes.

## 3. UX patterns for assistant / agent surfaces
- **Composer**: multi-line, auto-growing, `Enter` sends / `Shift+Enter` newline, chips for attached context, mode and model pickers as quiet popovers; placeholder adapts to width. Draft survives tab switches.
- **Turns**: user text in a light tinted block; assistant text as plain reading column with Markdown and highlighted code blocks that have *Copy* / *Insert* actions. No avatars needed — alignment and tint carry the roles.
- **Progress is a story, not a spinner**: show "Thinking…" with elapsed seconds, then grouped collapsible steps ("Exploring codebase · Reading prompts.ts" → "Explored codebase · 3 files, 2 searches"), edit cards with +/− diff stats, terminal cards with exit codes. Every running item has a verb and an object; never an anonymous spinner.
- **Stick-to-bottom scrolling**: auto-scroll only while the user is within ~160 px of the bottom and only for the visible session; a "Jump to latest" affordance when they've scrolled up.
- **Permission prompts**: one card per request with the exact command/path, three clear actions (Deny · Allow for session · Allow once) with single-key shortcuts; the oldest prompt answers keys; prompts from other tabs say which chat they belong to.
- **Plan / tasks panel**: a compact checklist with a progress meter; items tick off live; the current one carries the accent.
- **Changes bar**: files touched with Accept / Reject per file and for all; clicking opens the diff.
- **Empty state**: a warm greeting, one sentence of orientation, 3–4 concrete suggestion chips — and a clear, friendly notice (with a primary action) when something is missing (no model, no server).
- **Errors**: inline, specific, with the next step ("Ollama is not running — Start it"); never a bare red toast.
- **Tabs / parallel work**: running agents show an indicator and their current step; unread results get a dot; background work never moves the active transcript.
- **Keyboard & a11y**: everything reachable by keyboard; visible focus ring; roles for tabs/switches/menus; live regions for status; labels on icon-only buttons; keep heading order.

## 4. Implement
- Tokens first (CSS variables or theme), then primitives (button, chip, card, step row), then screens. Prefer the host's variables (VS Code `--vscode-*`) and layer the warm tint on top.
- Update DOM in place for live data (patch text/width/class); rebuild only on structural changes. Preserve scroll, focus and `<details>` open state across re-renders.
- Keep CSS co-located as the project does; delete styles you replace.

## 5. Verify (mandatory)
- Start/reuse the dev server or harness; `browser_inspect` the surface at a wide and a narrow width (`mobile: true` or a 320–460 px viewport). Fix console errors, overflow, tiny targets and contrast findings.
- Walk the states with `actions`: empty, streaming, tool steps running/finished, permission prompt, error, light and dark theme, reduced motion.
- `open_browser` to show the result; summarise before/after in terms of hierarchy, calm and clarity, and list what you verified.
