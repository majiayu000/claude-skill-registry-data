---
name: ui-pack
description: >-
  A design/frontend skill bundle — the single entry point for high-fidelity UI
  work. Loading ui-pack pulls in the whole UI toolchain at once: clone-website
  (extraction + builder dispatch), ui-ux-pro-max (design intelligence), and
  impeccable + emil-design-eng (polish & taste) — and points you at the
  agent-browser CLI for real-browser building and verification. Use it before any
  UI cloning, building, reviewing, or polishing so every helper skill is loaded
  consistently in one step instead of remembering each one. (Motion craft lives
  in the separate ui-animation skill — load that too when you need animation.)
user-invocable: true
---

# ui-pack — the UI/frontend skill bundle

`ui-pack` is a **wrapper**: it doesn't carry its own technique, it loads the set
of skills you want present for any serious UI work so you never have to remember
them one by one. Load this first, then do the work.

## What to load (do this now, in order)

Invoke the **Skill** tool for each of these — skip any that are already loaded:

1. **`clone-website`** — extraction (screenshots, `getComputedStyle`, asset
   download) and builder dispatch. The backbone for replicating any UI.
2. **`ui-ux-pro-max`** — design intelligence: layout systems, spacing/type
   scales, color, component patterns.
3. **`impeccable`** — pixel-level correctness and detail discipline.
4. **`emil-design-eng`** — design-engineering taste: the invisible details that
   make software feel great.

Then make sure the real-browser tool is available:

5. **`agent-browser`** — a CLI (not a skill), used to **drive and verify** the UI
   in a real Chromium. Check it's on PATH with `command -v agent-browser`; read
   its command guide with `agent-browser skills get core --full`. Install it with
   `npm i -g agent-browser` if missing. Real-browser verification is the
   non-negotiable — never sign off UI from source alone.

## Notes

- **Graceful degradation.** If one of the constituent skills isn't installed,
  load whatever is present and proceed — `agent-browser` on PATH is the only hard
  requirement for verification.
- **Motion is separate.** Animation/interaction craft lives in the
  **`ui-animation`** skill (transitions vs keyframes vs springs, easing,
  clip-path reveals, gestures, performance). Load `ui-animation` in addition to
  `ui-pack` whenever the work involves motion.
- **Installer.** All of the above are installed together by clone-team's
  `scripts/install-deps.sh` (idempotent — already-present pieces are skipped).
