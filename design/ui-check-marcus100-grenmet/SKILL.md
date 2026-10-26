---
name: ui-check
description: "Implements or refines a UI component against a design reference (Claude Design canvas, screenshot or written description): maps intent onto the --gm-* token contract, lists discrepancies, applies token-legal changes and iterates on screenshots. Use when the user shares a design or screenshot to match, or asks to make a component look like a reference."
allowed-tools: Bash(pnpm dev:*), Bash(pnpm design-system:*), Bash(pnpm ui:screenshots *), Read, Edit, Glob, Grep
---

## UI Check

Figma is not linked to this repo. The design reference is a Claude Design canvas,
a screenshot the user supplies, or a written description. Never ask for a Figma
frame URL or reach for a Figma MCP tool.

**Step 1 — Gather info**
Ask the user for:
- The design reference (Claude Design canvas, a pasted/attached screenshot, or a description)
- The component file path (or "new component" if creating from scratch)
- Target viewport(s): mobile (375px), desktop (1280px), or both

Do not proceed until you have all three. If the user has no reference yet, establish intent from the existing design lane and the user's description; use an available design skill if useful.

**Step 2 — Establish the design intent**
From the reference, write down the intended colors, typography (size, weight,
line-height, family), spacing, border-radius, layout direction, and component
hierarchy.

Map every value onto the token contract before comparing: a color must resolve to
a `--gm-*` token, a Tailwind alias, or a shadcn semantic. If an intended value has
no token, say so explicitly — that is a token request needing user approval, not
something to hardcode.

**Step 3 — Audit the current implementation**
Read the component file. Compare it against the intended values. List every
discrepancy:
- Typography (weight, size, line-height, family)
- Spacing (padding, margin, gap)
- Color (background, text, border)
- Border radius
- Layout / alignment
- Missing or extra elements

Present this list to the user. Do not edit files yet.

**Step 4 — Propose changes**
For an implementation request, apply changes within the authorized scope. For a review-only request, show proposed changes without editing; existing authorization counts.
Flag separately any change that would need a new or altered `--gm-*` token.

**Step 5 — Apply and render**
After approval, apply the changes and run `pnpm design-system:check` to confirm
the token contract still holds. Then render the result yourself:

```bash
pnpm ui:screenshots --app <app> --path <route>
```

It needs the app's dev server, which runs on the host, never inside the
devcontainer. If it exits 2, nothing is listening: ask the user to start the
command it prints (see `docs/ports.md`), then rerun. Read every PNG it lists.
Fix each `FLAG` line (horizontal overflow, console errors, failed requests) before
any visual review; those are defects, not taste. Aborted `_rsc` prefetches are
navigation noise, not defects. Dark captures force the `dark` class, so ignore
them for light-only apps (`docs`). To check a deployed build instead, pass
`--url https://<app>.staging.barrels.gd`.

**Step 6 — Independent review**
Do not approve your own render. Start a fresh-context subagent and give it only:
the reference (or the intent from Step 2), the screenshot paths, and
`.claude/skills/design-critique/SKILL.md` to follow. Ask for the three most
important problems, each with the screenshot file, what is visibly wrong, the
smallest token-legal fix, and what must not change. It must judge the PNGs, not
your description of them.

**Step 7 — Repair loop**
Fix one finding at a time with the smallest change, rerun `pnpm ui:screenshots`
for the affected route only, and re-read the new PNGs. Stop when the reviewer
reports nothing that blocks the reference. Allow at most two repair rounds per
finding; if one survives two rounds, stop, show the user the before and after
screenshots, and ask for direction. Never relax the reference or the token
contract to make a review pass.

**Step 8 — Hand off**
Show the user the final screenshots (phone and desktop, light and dark), list
what changed, and name anything left for their judgement.
