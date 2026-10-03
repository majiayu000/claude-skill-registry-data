---
name: hyperframes-demo
description: >
  Optional: prepare an end-user demo video with the HyperFrames CLI when the user
  explicitly asks for a HyperFrames/video demo. Do not use by default.
---

# HyperFrames end-user demo (optional)

**Optional.** Use only when the user explicitly asks for a HyperFrames / video demo. Do not invent a HyperFrames deliverable for ordinary features.

Build a **short, shareable demo for the end user** — not an internal prototype. Output is a HyperFrames composition previewed and (after approval) rendered to video via the CLI.

For composition HTML, catalog, and render contracts, load `/hyperframes` then `/hyperframes-cli` (and `/hyperframes-core` before writing markup). This skill owns the **demo brief → deliverable** loop only.

## When to use

**Only when the user opts in** (names HyperFrames, `/hyperframes-demo`, or asks for a rendered video demo).

- Feature or product demo for customers / stakeholders
- Walkthrough of a shipped or prototyped flow
- Launch / changelog / “what’s new” clip

Skip by default for features, prototypes, reviews, and ordinary change requests. Also skip for throwaway UI/logic prototypes (`prototype`) or code-only reviews.

## Demo brief (ask once if missing)

Collect only what is missing — one short pass:

1. **Audience** — who watches (customer, stakeholder, support)?
2. **One message** — the single takeaway after 30–60s
3. **Source** — live URL, local app route, screenshots, or scripted beats
4. **Length** — default **30–60s** (cap ~90s unless they ask longer)
5. **Output** — path/name for the final `*.mp4` (default `demos/<slug>.mp4`)

Do not invent a stack. Prefer capturing a real UI over fake mockups when a URL or running app exists.

## Workflow

Run as `npx hyperframes ...` (Node 22+, FFmpeg). Prefer `--json` on agent calls.

```
Progress:
- [ ] 1. Brief locked (audience + one message + length)
- [ ] 2. Scaffold under demos/ (or agreed path)
- [ ] 3. Storyboard beats (3–7) written before polish
- [ ] 4. Composition authored (catalog first, hand-author only if miss)
- [ ] 5. lint / check pass
- [ ] 6. preview handed to user — wait for revise or approve
- [ ] 7. render --quality looks (then delivery after final OK)
- [ ] 8. Verify file + hand off path + one-line message for the end user
```

### 1. Scaffold

```bash
npx hyperframes doctor --json   # gate on .ok if env is unknown
npx hyperframes init demos/<slug> --non-interactive
```

Use `--example=<name>` only when a named example clearly matches. Put demos under `demos/` unless the project already has a video folder — then reuse that.

### 2. Beats first

Write 3–7 beats that sell the **one message**. Each beat: on-screen claim + what the viewer sees (UI moment or graphic). No filler.

### 3. Author with the CLI loop

1. Search before hand-rolling motion: `npx hyperframes catalog --query "<beat in English>"` then `npx hyperframes add <name>` when a fit exists.
2. Author composition HTML via `/hyperframes-core`. For timeline truth: `npx hyperframes timeline --json`.
3. Iterate: `npx hyperframes lint` while editing; final gate `npx hyperframes check` (includes lint — do not double-run).
4. Sub-compositions: midpoint `npx hyperframes snapshot --at <t1>,<t2>,...` when mounts matter.

### 4. Preview — never render early

```bash
npx hyperframes preview --background
```

Verify HTTP 200, give the user the Studio project URL, ask **revise or render**. Keep preview alive until they decide.

### 5. Render only after approval

| Stage | Command |
| ----- | ------- |
| Iterate | `npx hyperframes render --quality draft` |
| First real encode | `npx hyperframes render --quality looks --output demos/<slug>.mp4` |
| Final handoff | `npx hyperframes render --quality delivery --output demos/<slug>.mp4` |

Confirm the file exists and is non-empty; `ffprobe` duration should match root `data-duration`.

### 6. End-user handoff

Return:

1. Absolute or repo-relative path to the `*.mp4`
2. One sentence the end user should take away (the locked message)
3. Preview URL if still useful
4. Optional: `npx hyperframes feedback --rating <0-10> --comment "..."` after a successful run (unless they opted out)

## Rules

- Demo is for the **end user** — clear claim, readable type, no unfinished prototype chrome.
- One message; cut anything that does not serve it.
- Catalog before custom motion; English queries even if on-screen copy is not English.
- Never render just because `check` passed — wait for explicit approval.
- Prefer capturing real product UI when a URL/app exists (`hyperframes capture` / product-launch route via `/hyperframes` when that fits).
- Obey `git-branch-safety`: do not commit/push demo assets to production branches unless asked; ask which branch holds `demos/`.
- Do not duplicate HyperFrames API docs here — read `/hyperframes-cli` references before unfamiliar commands.

## Related

- Entry / routing: `/hyperframes`
- CLI loop: `/hyperframes-cli`
- Markup contract: `/hyperframes-core`
- Registry: `/hyperframes-registry`
- Throwaway code prototypes (not video): `prototype`
