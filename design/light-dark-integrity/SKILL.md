---
name: light-dark-integrity
description: "Light/dark theme violation repair for Pattern Patrol P4. Use when you find raw bg-white/text-black classes or a state invisible in one theme, or when running a P4 patrol."
---

# Light/Dark Integrity

Apply this skill only after reading the Pattern Patrol system, the P4 registry
row, the repo `CLAUDE.md`, the `pattern-patrol` skill, and
`ui-dense/data-dense-rules.md` section 1. Those safety rules remain binding.

## Detect

Run the deterministic detector from the repository root:

```bash
node .claude/skills/light-dark-integrity/scripts/detect-light-dark.mjs
```

Pass explicit `.tsx` paths to scan a structural-novelty scope. Use `--json`
for a machine-readable report and `--strict` to fail on pending or invalid
exceptions. A candidate is not automatically a defect, compliant, or exempt.

The detector reports every source line containing `bg-white` or `text-black`,
whether a `dark:` token exists on that line, and a possible exception hint.
Review the whole component and every place a shared component renders. Never
clear a candidate from a file-level `dark:` token elsewhere in the file.

## Classify each candidate

Choose exactly one surface class:

1. **Theme surface** — page, panel, card, row, menu, popover, dialog, input, or
   control whose appearance must follow the active theme. Raw white/black is a
   defect unless an explicit paired design is necessary.
2. **Proposed fixed/on-color exception** — chrome over a photo, video,
   gradient, canvas, crop handle, camera, code block, or other surface whose
   local contrast may be independent of the app theme. Propose it to Arman;
   never preserve or clear it on agent judgment alone.
3. **Non-app output** — print rules, HTML/iframe matte, exported image/PDF,
   email, or an authored visual specimen. If the raw palette is deliberate,
   propose it to Arman unless the source is truly non-rendered test/comment
   text.
4. **Explicit theme selection** — the opposite theme is selected through a
   theme prop, conditional class, variable, or multiline construction. Verify
   both branches. A real two-theme branch is compliant, not an exception.

If the class is unclear, the finding is Tier R. Report it; do not mutate.

## Mechanical repair table

For a verified theme surface, use the narrowest semantic token:

| Meaning | Required class |
|---|---|
| Page/application background | `bg-background` |
| Card or bounded content surface | `bg-card` |
| Subdued section or row | `bg-muted` |
| Floating menu/popover | `bg-popover` |
| Primary text | `text-foreground` |
| Secondary text | `text-muted-foreground` |
| Normal boundary | `border-border` |
| Neutral hover/focus fill | `hover:bg-accent` / `focus-visible:bg-accent` |

Keep a raw palette plus a `dark:` pair only when no semantic token expresses
an intentional two-theme design and both exact colors are already established
by the surrounding component. Do not invent a new pair during a patrol.

For a shared primitive used on both theme surfaces and fixed/on-color
surfaces, add an explicit, narrowly named surface variant. The default must use
semantic theme tokens; the fixed/on-color call site opts into its established
overlay classes. Do not force either side's styling onto the other.

Do not change layout, interaction, wording, component boundaries, imports, or
chunking. Do not create a new global token during a patrol. If the repair needs
design judgment or a new token, downgrade it to Tier R.

## Required false-positive review

Before counting or fixing, review all candidates against:

- `print:` rules and printed/exported documents;
- iframe, HTML preview, page-preview, and white-paper mattes;
- media, camera, crop, canvas, image, video, and gradient overlays;
- fixed visual specimens, games, loaders, and immersive authored designs;
- explicit theme props/conditionals and multiline `dark:` pairing;
- comments, fixtures, samples, and non-rendered strings;
- deliberately chosen contrast where the semantic foreground would fail.

Record the reason for every excluded class in the patrol report. Never add a
suppression or detector allowlist merely to make the output smaller.

## Human-owned exception approval

**Agents propose; Arman approves.** A plausible fixed palette is still an open
finding until Arman explicitly approves that exact surface. No certifier,
maintainer, prior styling, or “intentional” code comment substitutes for his
decision.

Every proposal must include:

- exact file, line, raw token(s), and visual state;
- a stable production URL plus precise click/state instructions;
- what would change if semantic tokens replaced it;
- an `Approve` or `Reject` decision request.

If no stable URL or reproducible artifact exists, the item cannot be approved.
Keep it open and create a Tier-C review-harness task. End any run containing
proposals with this unmistakable envelope:

```text
EXCEPTION APPROVAL REQUIRED
<complete numbered proposal list>
ARMAN, WE NEED YOU: approve or reject every listed P4 exception.
```

Only after approval, add one entry to `exceptions.json` with `approvedBy` set
to `Arman`, the approval date/reference, review URL, exact token list, file,
line, and reason. Add a source comment within two lines of that exact line:

```text
patrol-exception:P4-EX-###
```

The detector validates ledger ↔ source agreement and exact line/token identity.
It reports approved exceptions separately forever; it never silently removes
them from totals. An unapproved comment, missing comment, moved token, stale
pair, or one-to-many annotation is an invalid exception and a loud finding.
Rejection means fix it; never record the rejection as an exemption.

## Tier-M batch and certification

Keep each batch at 15 files or fewer. Run `pnpm type-check` and relevant gates.
Then spawn a second adversarial agent with the exact brief:

> assume this broke something; find it.

The certifier reruns the detector and gates, inspects every changed surface in
light and dark at desktop and mobile viewports, reviews the exception classes,
and returns only `CERTIFIED` or `REJECTED` with evidence. Fix or fully revert a
rejected batch. Nothing ships mostly.
