---
name: make-it-look-expensive
description: Every screen, flow and feature your agent builds meets the bar of a mature consumer app, with no lost features, no dead ends and instant feedback on every action. Use before designing, building or reviewing any UI, or when you say "make it look great", "polish this", "no shoddy work", "product bar" or "review this screen".
---

# Product bar

Apply all eleven points to every screen, flow or feature you design, build or review.

0. **Never lose functionality.** A change keeps everything the app already does, settings included. If something
   would be lost, tell the user first, with the option that keeps it.
1. **No shoddy work.** Build what a mature consumer app ships: every control, state and action a person expects.
   Never the literal minimum. A half-built feature is a regression.
2. **Finesse is the whole experience.** UI, UX, ease of use, product loops, smart defaults.
3. **Loops.** After any result or failure, the next action is right there. No dead ends.
4. **Smart defaults.** Decide from what the app already knows. Offer no noise.
5. **Consumer-first.** Ask once, where the choice arises, with a recommendation. A blocked state says why in one
   line and gives the next step.
6. **Less is more.** Cut needless words. Use icon buttons (with a label for screen readers and a tooltip) where
   the glyph is clear. On desktop, use columns and grids instead of long stacked lists.
7. **One design doc.** Find the project's design source of truth: a design philosophy, design system, brand guide
   or style guide (look in the repo root, `docs/`, `design/`, a sibling `brand` repo, or where the agent
   instructions point). If it has per-platform profiles (desktop, mobile), those own each platform's details.
   No other copy is a source. If there is none, ask the user whether to start one, and until then follow the
   existing screens.
8. **Every page is a route.** Back and Forward return exactly where you were, scroll position and open panels
   included.
9. **Every platform the product ships on.** Check the list (for example Android, iOS, macOS, Windows, Linux, web)
   and name any platform the change misses.
10. **Every action answers at once: pressed, then working, then done.** Any tap, click, key or gesture shows
    feedback on the touched control within about 100 ms. A slow result shows a working state on that control (a
    choice shows as chosen at once), then a done state. Never a silent gap, then a jump. Review every screen and
    test for it.

When the change touches UI components, also load `match-the-design`. To review many screens with the user,
use `show-me`.
