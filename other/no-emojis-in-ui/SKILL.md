---
name: no-emojis-in-ui
description: "Emoji and Unicode-glyph removal for Lucide-only UI (Pattern Patrol P6). Use when running a P6 patrol, a UI edit meets an emoji or icon glyph in TSX, or asked to enforce Lucide-only icons."
---

# no-emojis-in-ui

Enforce one rule: user-visible UI uses Lucide icons, never emoji or Unicode
icon glyphs. Follow the Pattern Patrol constitution and keep each mutation
batch to 15 files or fewer.

## Detect

Run the registry detector over `.tsx` files:

```bash
rg -n -P '[\x{1F000}-\x{1FAFF}\x{2600}-\x{26FF}\x{2700}-\x{27BF}\x{2205}]' --glob '*.tsx'
```

Inspect every match in rendering context. Classify it as:

- **Finding:** JSX text, a rendered string, a chip/title/button label, seed or
  sample data rendered by the app, product-authored text copied/exported for
  the user, or an icon value that reaches the UI.
- **False positive:** non-rendered comment/documentation, console-only
  diagnostic text, a parser constant accepting glyphs as input, or an internal
  sentinel value that never reaches rendered or exported content.
- **Unresolved:** reachability or rendering cannot be proven. Report it; never
  silently clear it.

Rendered demos, admin tools, debug panels, and sample apps are UI findings.
User-authored or external content is not ours to rewrite; report the rendering
path only if the product itself injects the glyph.

## Route approval; never stop at the scan

Every verified finding takes exactly one route:

1. **Auto-approved:** it passes every gate below; fix it immediately.
2. **Manual approval:** the problem is certain and the repair is known, but an
   auto-approval gate fails; propose the exact repair to Arman.
3. **Unresolved:** certainty or a safe repair is missing; keep it open with the
   missing evidence.

An empty auto-approved set is not completion. Tier R forbids unapproved
mutation; it still requires a plain-English approval proposal for every
certain, safe, worthwhile repair.

## Auto-approval gates

Auto-approve only when all are true:

- The glyph is authored by us and visibly functions as UI iconography.
- One exact Lucide icon preserves its meaning, or an adjacent Lucide icon
  already communicates the same meaning and the glyph is redundant.
- Copy, handler behavior, state, semantic colors, DOM interaction, ARIA text,
  desktop/mobile layout, and light/dark behavior stay unchanged.
- The repair adds no wrapper/card/chrome, changes no chunk boundary, widens no
  type, adds no suppression, and touches no generated file.
- The result remains clear without relying on icon shape alone.

Anything ambiguous routes to manual approval. Never auto-approve edits to
user content, parser behavior, terminal protocols, branded art, complex ASCII
or Unicode diagrams, or copy whose meaning changes when the glyph disappears.

## Approved transformations

Choose the semantic Lucide icon already used by the component when available.
Otherwise import it directly from `lucide-react`.

| UI meaning | Normal repair |
|---|---|
| success / complete | `Check` or `CheckCircle2` |
| warning | `TriangleAlert` |
| private / locked | `Lock` |
| public | `Globe2` |
| keyword / key | `KeyRound` |
| document | `FileText` |
| removed / truncated | `Scissors` |
| new game | `Gamepad2` |
| reset / refresh | `RotateCcw` |
| celebration | `PartyPopper` |
| purely decorative glyph | delete it; preserve the text |

This is a semantic map, not a blind replacement table. Preserve icon size,
alignment, and `shrink-0` where wrapping text needs it. Mark decorative icons
`aria-hidden="true"`; an icon-only control keeps a real accessible label.
Delete a glyph instead of adding a second icon when a sibling Lucide icon
already conveys the same state. Never replace an emoji with a Lucide icon
banned by `matrx/no-banned-lucide-icons`; delete redundant decoration or route
the choice to manual approval.

## Verify and certify

For each batch:

1. Re-run the detector on every touched file and confirm only documented
   false positives remain.
2. Run `pnpm type-check`, `git diff --check`, and the relevant repo gates.
3. Inspect changed surfaces at desktop and mobile widths in light and dark
   themes. Exercise every changed control.
4. Spawn a second adversarial agent with: **"assume this broke something; find
   it."** It reruns the gates, audits false-positive classes, and returns
   `CERTIFIED` or `REJECTED`.
5. Fix or fully revert a rejected batch. Commit a certified batch by path and
   push to `main`; the release train ships it. Never run `./scripts/release.sh`
   unless Arman asked you to.

Update `.matrx/PATROL_SIGHTINGS.md` and
`.matrx/patrol-reports/no-emojis-in-ui.md` with the findings, fixes, approval
route, and certifier verdict.
