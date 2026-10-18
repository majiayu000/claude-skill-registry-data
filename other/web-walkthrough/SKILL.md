---
name: "Web: Walkthrough"
description: "The sign-off walkthrough: discover every open state, plan every route on every intended device, capture through asset-shot under the capture naming rule, gate the results and record what failed"
when_to_use: "After a design is signed off and built, once web-check's signoff mode is clear; also on its own to re-capture a product after a change, inside a wider task."
model: sonnet
effort: medium
metadata:
  glyph: ᛊ
  family: web
  goblin-spinner: opening every drawer|walking the routes|counting captures
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write", "Bash", "AskUserQuestion", "Skill", "ArtifactData"]
argument-hint: "[base URL or site directory] [devices: phone, desktop or widths] [scope document]"
---

# The sign-off walkthrough

Load `web-conventions` and `asset-conventions` first. Scripts: `~/.claude/library/scripts/web/open-states.ts` (Node, Playwright) and `walkthrough-plan.py`; capture runs through `asset-shot`.

## Step 1: Inputs

- **Routes**: slug to path, from the inventory (scope document §4 or the review's inventory table), else per `asset-conventions` detection. A route with a parameter takes the sample value the inventory names.
- **Devices**: from the scope document §2 or `$ARGUMENTS`. Names map to widths: phone 390, tablet 834, desktop 1440, unless the scope gives widths; a scope that gives only widths uses them as the prefix. One device means no prefix.
- **Base**: a served origin (start the dev server as `asset-shot` Step 1 does) or a directory of HTML.
- **Planned open states**: from the inventory's open-states column, as `[{route, specifier, javascript}]` in a scratch file.

Say all four back in one table before running anything.

## Step 2: Discover

```
cd ~/.claude/library/scripts/web && node --experimental-strip-types open-states.ts --base <base> --routes '<json>' --devices '<json>' --out <scratch>/states.json
```

Every `details`, `aria-expanded="false"`, `aria-haspopup` and hidden `aria-controls` target becomes a state with the JS that opens it. Each state also carries `toolbarMoved`: the controls of the toolbar the trigger sits in (or any toolbar above it) whose position changed when it opened. That is principle 4's test.

## Step 3: Plan

```
python3 ~/.claude/library/scripts/web/walkthrough-plan.py --base <base> --routes '<json>' --devices '<json>' --states <scratch>/states.json --planned <scratch>/planned.json --out docs/assets/walkthrough.yml --json
```

Show the YAML and the unplanned states (discovered, not in the inventory) and stop for approval, per `asset-conventions`. An unplanned state is a gap in the inventory: add it there or say why it is not a state worth capturing.

## Step 4: Capture

Invoke `asset-shot` with `docs/assets/walkthrough.yml no frame` (a walkthrough is evidence, not a README mockup; add framing only when Jason asks). Captures land in `docs/assets/walkthrough/` under the naming rule, apart from the README's `docs/assets/shots/`. Run the quality gate from `asset-conventions` on every PNG.

## Step 5: Record

1. `check.py coverage docs/assets/walkthrough --routes <slugs> --devices <names> --json`: a missing capture is a finding under principle 8.
2. Every state with a non-empty `toolbarMoved` is a finding under principle 4: `where` the route and the trigger's name, detail the controls that moved and by how much.
3. Every capture that failed the quality gate twice is an entry with `source: walkthrough`, severity `major`, the file name in `whereDetail`.

Write them to the store as `web-check` Step 4 does (live store or `observations.py add`), then re-export.

## Step 6: Report

One table: route, device, captures, open states, findings. Then the paths written and the `observations.py status` line. Findings reopen the branch; a clean status is the end of the walkthrough.
