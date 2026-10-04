---
name: game-ui-designer
description: Use when designing or building a new in-game UI screen for a UEFN project (store, shop, missions/quests, teleporter, rewards, inventory, or similar menu/HUD panel) — applies a reusable "chunky cartoon game UI" style guide learned from real reference examples, and grows that reference library over time as new examples are provided.
status: draft
maturity: partial
---

# Game UI Designer

> **Reference images are private.** The public kit contains no example screenshots (they would be third-party material). Put your own in `references/examples/<archetype>/` and list them in `manifest.md`; the folder is git-ignored, so they stay on your computer.

Personal, user-level design skill (`~/.claude/skills/game-ui-designer/`) for building UEFN
in-game UI screens (menus, shops, HUDs — built with UMG/Verse widgets, not literal web pages)
in a consistent, polished "chunky cartoon game UI" style, learned from real examples the owner
has collected rather than invented from scratch.

## What this skill is for
- Generating a NEW UI screen (store, shop, missions/quests, teleporter, rewards, inventory, or
  a similar panel) for a UEFN project, in a style consistent with the owner's established taste.
- It does NOT cover gameplay logic, Verse device wiring, or backend data — only the visual and
  layout design of the screen. Hand off implementation details (device bindings, data source)
  to **coder** as usual; this skill only informs what the screen should look like and how its
  elements should be structured.

## Before designing any screen
1. Read `references/style-guide.md` in full — it's the distilled rule set (panel anatomy,
   section/tab structure, item-card recipe, currency display, progress/reward patterns,
   typography/color rules, and what NOT to copy directly from the source examples).
2. Check `references/examples/manifest.md` and open the 1-3 images whose archetype most closely
   matches what's being built (e.g. building a shop → look at `shop/*`, not `teleporter/*`).
   These are visual references only — reinterpret them with real UEFN widgets, never copy
   third-party art/icons/branding.
3. If the project already has its own UI screens built with this skill (check
   `Claude/docs/UI-STYLE-NOTES.md` if present — see "Per-project consistency" below), match
   THOSE first — a project's own established look wins over the generic reference set once one
   exists, so a game doesn't end up with inconsistent screens across sessions.

## Designing a screen
- Reuse the item-card recipe (icon/image → bold label → price/action pill) for any
  reward/purchase/mission item rather than inventing a new layout per screen.
- Reuse the panel anatomy (rounded modal, title banner, top-right close button, busy-but-low-
  contrast background) for every new panel so screens feel like the same game.
- Keep one currency = one icon + one color across the whole project — check other screens
  already built (or `Claude/docs/UI-STYLE-NOTES.md`) before introducing a new currency's visual.
- Flag anything that needs a custom-authored texture (ribbon banners, starburst badges,
  currency icons) as an asset dependency for the owner, rather than approximating it silently —
  see style-guide.md section 7.

## Per-project consistency (`Claude/docs/UI-STYLE-NOTES.md`)
The first time this skill is used inside a given UEFN project, create
`Claude/docs/UI-STYLE-NOTES.md` (if it doesn't exist) recording the concrete choices made for
THAT project: currency icon/color assignments, the exact palette used for section headers, font
choice, corner-radius values used. Every later screen built in that project reads this file
first and reuses those exact choices — this is what keeps a store screen and a missions screen
built in different sessions looking like the same game, instead of each session re-deriving its
own interpretation of the generic style guide.

## Self-learning / autoapprendimento (fully automatic, no per-task question)
This skill is meant to grow from real project work on its own, not stay frozen at today's example
set and not depend on being manually re-fed each time. Three mechanisms feed it, none of which
require asking the owner "should I save this" every time — that question was tried and explicitly
rejected as too manual; only genuinely owner-only decisions (there are none in this pipeline) get
a stop-and-ask:
1. **Per-task, automatic**: when `coder` finishes a UI screen, it stages any available screenshot
   into that project's `Claude/docs/ui-screenshots-pending/`. When `planner-docs` closes that task,
   it files the staged screenshot straight into `references/examples/<archetype>/` and logs it in
   `references/examples/manifest.md` — mechanical bookkeeping, done automatically at task close.
2. **Per-session catch-up**: every project's `CLAUDE.md` includes a "UI reference harvest" rule
   that checks `Claude/docs/ui-screenshots-pending/` on every session start (cheap, always safe)
   and files anything still sitting there that a previous task close didn't have an image for yet
   (owner dropped it in later, or an export happened after the fact).
3. **One-time backfill per existing project**: `project-bootstrap`'s Branch A (existing-project
   analysis) scans for screenshots of UI screens that already exist in a project analyzed for the
   first time under this skill, so pre-existing projects aren't stuck with an empty contribution
   just because they predate this skill.
All three file images the same way: copy into the closest-matching (or new) archetype folder
under `references/examples/`, append one row to `manifest.md`, source labeled as that project's
real work (never mixed up with the generic Roblox-sourced starting examples). Never overwrite or
delete an existing example as part of this pipeline.

4. **Direct source-code analysis (no image needed)**: when the project has real UI implementation
   files — UMG/Verse widget definitions (`.verse` files constructing `canvas_panel`, `stack_box`,
   `button`, `text_block`, `image`, and similar; or any exported layout/style data for those
   widgets), analyze them directly instead of waiting for a screenshot. This is the right path
   whenever the owner points at actual code rather than a picture.
   - Find candidate files: anything under the project's UI/widget code area whose name or content
     suggests a screen this skill cares about (store, shop, mission/quest, teleporter, reward,
     inventory, HUD) — grep for widget-construction calls and for the relevant class/device names.
   - Read each candidate file and extract concrete, verifiable facts only — never invent values
     not actually present in the code: which widget types are used and how they're nested (panel
     anatomy), literal colors/hex values assigned, corner-radius/border/padding values if set,
     font/text-style references, currency icon/asset references and where each is reused,
     layout structure (grid vs. list vs. stack), any constants/config driving prices or rewards.
   - Write one entry per screen analyzed into `references/examples/code-derived.md` (create if
     missing): file path, screen/archetype, and the extracted facts above in the same categories
     `style-guide.md` uses (panel anatomy / cards / currency / typography), so it's directly
     comparable to the image-derived rules. Append a row to `manifest.md` too, source labeled as
     "`<ProjectName>` (source code, `<file path>`)" so it's traceable back to the real file.
   - Feed the same per-project file, `Claude/docs/UI-STYLE-NOTES.md`, with the concrete values
     found (currency icon/color per currency, palette, corner-radius) exactly as the screenshot
     path does in `planner-docs` step 5 — code-derived facts are usually MORE reliable than
     eyeballing a screenshot, since they're literal values, not visual estimates.
   - This can run on demand, not just at bootstrap: if the owner says something like "analyze the
     UI already present in the project, they're real files not screenshots," locate and read the real
     widget/UI files right now and do the extraction above in the current session — don't wait
     for a scheduled hook, and don't ask for a screenshot when the owner already pointed at code.

Two things stay genuinely manual, by design:
- Adding an external inspiration image (not from the owner's own UEFN work) is something the
  owner shares directly in conversation when they want to — there's no "external inspiration"
  auto-harvest, since that would mean guessing what counts as inspiring off the internet.
- Every 5-10 new examples added (from any of the 3 automatic sources), re-read
  `references/style-guide.md` and check whether any rule is now contradicted by the accumulated
  real examples (e.g. the project consistently uses a different card shape than section 3
  describes) — if so, propose an update to style-guide.md reflecting what's actually being built,
  rather than letting the two drift apart silently. This review is worth flagging to the owner
  since it changes the shared rule set, unlike filing an individual example.

5. **Per-session code-drift check (breaks the chicken-and-egg case)**: mechanisms 1-3 above all
   assume a screen went through a tracked `coder` task. If the owner designs/edits UI screens by
   hand, directly, outside any task — the actual common case for someone hand-authoring UEFN
   widgets rather than asking `coder` to generate them from scratch — none of those fire. For that
   case, `CLAUDE.md`'s "UI reference harvest" rule hashes every real UI/widget file in the project
   on every session start and diffs against `Claude/docs/.ui-code-ingested.json`; anything new or
   changed since last session gets the same "Direct source-code analysis" treatment automatically,
   no task and no explicit request needed. This is the primary feeding path when the owner is the
   one drawing screens by hand rather than `coder` — mechanisms 1-3 stay relevant once `coder`
   starts generating screens FROM this skill's own accumulated style guide, at which point the
   loop closes: hand-made screens teach the skill, the skill then lets `coder` generate new screens
   consistent with them, and those get fed back too.

This skill's `status` stays `draft` until real (not backfilled-from-guesswork) examples exist from
at least 3 distinct UEFN projects — same promotion discipline as the kit's Genre Skills, so
"mature" means genuinely validated across real, shipped work, not just present in the folder.

## Source of the initial example set
The 9 starting examples under `references/examples/` are screenshots from published Roblox
experiences, given by the owner purely as aesthetic reference for the "chunky cartoon game UI"
genre (store/shop/missions/rewards patterns) — not UEFN screenshots, not this project's own
work, and not to be treated as authoritative once real project-specific examples accumulate.
