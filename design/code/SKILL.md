---
name: code
description: Applies a Figma design to real code in a frontend repo — porting changed parts into existing code with minimal edits, or implementing screens and state variants that exist only in the design. Reads the repo's own naming, tokens, and state-management conventions first so it never overwrites them, checks both by numbers and by screenshot comparison, then opens a branch and a PR. Triggers - "/fig:code", "apply this design to the code", "implement this screen in the frontend", "시안 코드에 반영해줘", "피그마 바뀐 거 앱에 적용", "시안대로 코드 고쳐줘".
allowed-tools: AskUserQuestion, Bash, Read, Write, Edit, Glob, Grep, mcp__plugin_figma_figma__get_design_context, mcp__plugin_figma_figma__get_screenshot, mcp__plugin_figma_figma__get_metadata, mcp__plugin_figma_figma__get_variable_defs, mcp__plugin_figma_figma__download_assets, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__browser_batch, mcp__claude-in-chrome__read_console_messages
---

# fig:code — Figma design → frontend repo code

Moves what is drawn in the design into **the code of a running app**. The target is a frontend repo with a build system, and the deliverable is a branch and a PR in that repo.

**The premise — the design and the repo are each canonical for different things.**

| Canonical in the design | Canonical in the repo |
|---|---|
| Numbers, colours, spacing, copy, placement, state variants | File structure, naming conventions, state management, token reference paths |

Cross that line and something breaks. Tearing up the repo's conventions to match the design, and rounding the design's numbers off because the code prefers it, are the same failure. **When the call is unclear, do not apply it — ask.**

## When to invoke

- "apply the design change to the code", "make it match Figma", "implement this screen"
- Building a screen or a state variant that exists in the design and not in the code
- An explicit "/fig:code"

## When NOT to invoke

- A build-less single-HTML behavioural prototype → `/fig:proto`
- Just listing frames or reading structure → `/fig:read`
- Auditing the design's own structure, flow, and naming → `/fig:lint`
- Marking AS-IS/TO-BE changes on the design and writing them up → `/fig:diff`
- Applying into the canonical Figma page rather than into code → `/fig:sync`
- The reverse direction, a screen up into Figma → `/fig:draw`, which places it against this file's own canonical page and patterns before handing the assembly to `figma:figma-generate-design`

## Inputs

- `figma_url` (required): figma.com/design/:fileKey/...?node-id=... — the target frame. Ask if it is missing.
- `repo` (required): the target repo path. Defaults to the current working directory; ask explicitly if it is elsewhere.
- Mode (settled in step 1): **apply changes** or **implement new**. If both are in play at once, split them and go in order.

---

## Procedure

### 0. Load the prerequisite skill

Call `figma:figma-design-to-code` before calling `get_design_context` (that skill's own hard prerequisite). Skip it and the design read comes out wrong.

### 1. Interview — what counts as done

Fill these in before starting. Whatever cannot be filled in is asked, not guessed.

- **Scope** — which frames and screens, and how far the state variants go (default only, or lock, error, and empty too)
- **Mode** — applying changes, or implementing new
- **Definition of done** — in verifiable form. For example: "screen A's spacing and tokens match the design, screen B locks interaction in that state, typecheck passes"
- **Plan doc already updated** — if this changes screen structure or interaction rules (a new screen, a new state, a change to a locking or branching rule), check that the decision is already reflected in the plan doc. If it is not, the code is running ahead of the document — apply it anyway, but **say so in the step-6 report.** Presentational changes like numbers, colours, and copy do not count.

For several screens, share the order before starting.

### 2. Learn the repo's conventions (mandatory before writing — never skipped)

**Before touching a single line of code**, read how the target repo is written.

1. `CLAUDE.md`, `AGENTS.md`, `README` at the repo root — the architecture and the things not to do
2. **Open one or two sibling components in full** — class naming, where state comes from (a global store or local), which helper handles conditional disabling
3. Where style tokens are defined — CSS variables, a theme file, or a design token package
4. The verification commands — the typecheck, lint, build, and dev script names in `package.json`

Follow exactly what turns up here. Even where a better approach suggests itself, do not change it in this pass — only what was asked for.

### 3. Read the design accurately (read-only, no confirmation needed)

- Take structure, numbers, and tokens from `get_design_context` and the visual from `get_screenshot`, together. Either one alone goes wrong.
- Where token names are needed, `get_variable_defs`. If the design is bound to variables, **bind the code to the corresponding tokens. No hardcoded hex or px.**
- **Labels and copy verbatim from the design.** Even where better wording suggests itself, do not change it — copy was decided alongside the plan doc.
- Do not redraw images, icons, or illustrations in code; pull the originals with `download_assets`. Imitating them in code ends up inventing behaviour the design never had.
- **In change mode, build the comparison table here first** — design values beside current code values, so only the places that actually moved are picked out.

| Item | Design | Current code | Action |
|---|---|---|---|
| Card inner padding | 16 | 12 | change |
| Title size | 14 | 14 | keep |

This table is both the work list and the baseline for step 5's verification.

### 4. Apply — minimal edits

**Change mode**
- Touch only the rows marked "change" in the comparison table. Neighbouring elements, formatting, and comments stay as they are.
- Where one value is spread across several places, fix the single definition and let it propagate. Fixing every call site is a sign of stepping outside the conventions.

**New-implementation mode**
- Start from an adjacent sibling component as the skeleton. Never build a new pattern in an empty file.
- Handle state, locking, and errors through helpers the repo already has. Reimplementing the same decision makes two copies that then diverge.
- Keep state variants as conditional expressions rather than cloning them into separate components.

In both modes, do not add behaviour the design does not have — hover effects, animation, autosave.

### 5. Verify — all three are mandatory

Skip any one of them and the work is not applied.

**Do not cut this short for being in a hurry.** What gets cut under time pressure is the scope (split items off and push them back), never the verification. Substituting "a quick look" for the screenshot comparison in particular is a cut — this step is not finished until the design image and the real screen are side by side at the same zoom. Work shipped without verification stays wrong, and undoing it always costs more than the verification would have.

1. **Machine checks** — run the typecheck, lint, and build found in step 2. Only look at newly introduced warnings (kept apart from pre-existing ones).
2. **Real behaviour in a browser** — bring up the dev server and operate the screen. Confirm zero console errors. If state variants are in scope, actually produce those states.
3. **Comparison against the design (numbers and screenshot, both)**
   - Fill in the "action" column of the step-3 table against the actual result, row by row.
   - Put the design screenshot and the browser screenshot side by side at the same zoom and compare by eye. Numbers alone cannot catch omissions (a missing element, a wrong order); screenshots alone cannot catch small value differences.

Fix what is still off and verify again. **Whatever could not be fixed goes in the report rather than passing quietly.**

### 6. Preview → go → branch and PR (external writes)

Get the user's confirmation **without exception** before anything goes to the remote.

What the preview carries:
- Target repo and branch name
- A per-file summary of the changes (added, changed, deleted)
- The final comparison table (what was matched to what)
- The verification results (machine checks, browser, screenshot comparison)
- What could not be applied, and why

Close with "shall I proceed? (go / changes)". Only after a "go" is the branch cut, committed, pushed, and the PR opened. **Nothing that was not in the preview gets slipped in at execution time.**

The PR body carries the design link, the scope applied, how it was verified, and what is left.

---

## Constraints

- **Never adjust the design's numbers on your own.** Where they are awkward to express in code, put them in as they are, or say why and ask. Rounding and approximating break the premise that the design is canonical.
- **Never refactor the repo's conventions.** Even where a better structure is visible, in this pass just point it out.
- **Stop when the design and the code contradict each other.** Which one is current is something a person knows. Picking one as canonical on your own makes them diverge quietly.
- **Copy and labels stay verbatim.** Even what looks like a typo is reported rather than fixed — it may be a value agreed with the plan doc.
- If the design itself looks wrong (a missing state, overlapping elements), stop applying and hand it to `/fig:lint`.

## Notes

- Do not throw the comparison table away. In the PR body it tells a reviewer what changed and why without reading the diff.
- Project-specific constraints (a file's plan, font limits, the nature of a token library) do not belong in this document — check them in memory.
- For a large screen, split it into cards or regions and repeat steps 3–5. Change too much at once and it gets hard to narrow down where it went wrong.
