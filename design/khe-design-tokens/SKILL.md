---
name: khe-design-tokens
description: "Finds a project's design contract (a `.design` file or DESIGN.md), resolves which one wins, and threads its tokens through the UI as CSS variables, a Tailwind theme or component props. Also writes design-system docs an agent can follow and checks the contract for drift. Use when a repo has a `.design` or DESIGN.md, or someone says \"use our tokens\", \"make it on-brand\", \"stop hardcoding colors\", \"the agent keeps inventing variants\" or \"document our design system\". To design the scales themselves, review the result or finish a screen that still feels unfinished, use `khe-ui`."
license: MIT
metadata:
  author: Harshit Khemani
  version: "1.0.0"
---

# Design tokens

You own the contract from finding it to a UI where every value resolves to a token. An agent that invents a color beside an existing token has failed the job.

A construction skill. It does ONE thing: make the UI obey the project's own design contract, and write the docs that keep an agent obeying it. It does not design a palette, a contrast pair or a type scale, review a screen for craft, or finish a screen whose tokens are right and which still feels flat (all three are `khe-ui`).

## The one idea

**Every value in the UI resolves to a name in the project's own contract, on the role that name was given, and anything the contract lacks is reported, never guessed.**

Five ways it fails:

- **Guessed.** A raw hex, a 6px radius, Inter: a value typed because it looked close. A guess looks exactly like a decision.
- **Invented.** A name the contract does not hold: `var(--radius-xl)`, `variant="outline"`, a documented variant no code has.
- **Misbound.** The token resolves and it is the wrong one: the accent on a card because its hex matched the mockup. No script catches this.
- **Forked.** Two sources of truth: a `.design` and a DESIGN.md with no stated order, a `:root` that drifted from the contract, a second styling system, a hand-built twin of a catalogued component.
- **Silent.** A contract edited without a yes, a literal left with no reason, a system invented where there was no contract, or the contract's silence taken as permission to default.

The fix: find the one contract, read its intent before its tokens, map each value to a token by the role it plays, land the tokens in the system the project already uses, and report every gap, drift and leftover literal in writing.

## Initial response

When this skill is invoked with no request, reply only with:

> I'm ready to find your design contract and thread its tokens through the UI. Usage: `/khe-design-tokens [target]`

Then wait. Give nothing else until the user asks.

## How hard to press

Bind it the way the contract's author would review it: with the contract open beside every file. The gold examples in `examples/` are the bar. If your file holds a literal, a second naming scheme or an unexplained candidate line where the closest gold holds none, that is the first fix. Then picture the single line the author would screenshot and send back: the accent on a surface that is not the primary action, a `6px` beside a scale of 4 / 8 / 16, a `--brand-2` nobody defined. If you can picture that screenshot, you have found the next fix. A gate pass is where this judgment starts, never where it ends.

## Workflow

Most of the quality is decided before any file changes: which contract, what it intends, and where each token lands. Under `khe-auto` the same loop runs with this skill's gate.

1. **Find the contract, nearest first.** Walk up from the edited file for a `.design` or `<name>.design` (match the extension in any case) and resolve `extends`, child over parent. Then look for `DESIGN.md` at the root, in `docs/`, `design/` and `.design/`. If both exist, the `.design` is the contract and DESIGN.md is rationale. In a video project the order is `frame.md`, then `design.md`, then `DESIGN.md`. No contract: say so, scan the code for the system it already uses (global CSS, the Tailwind config, `components.json`, design notes), and offer to bootstrap one from the closest gold in `examples/`. **Exit:** you can name one contract file and its version, or you have said in writing that there is none.
2. **Read it before generating anything.** A `.design` requires `schema: design.v1`, `name`, `version` and `agent.instructions`, in YAML or JSON. Read [gotchas](references/gotchas.md) and [pov](references/pov.md), then [using-design-file](references/using-design-file.md) or [using-design-md](references/using-design-md.md). For a `.design`: `agent.instructions`, `intent`, `constraints`, `policy` and `decisions`, `tokens`, `voice`, `components`, in that order. For a DESIGN.md: the front matter binds, the body picks between tokens, and its Do's and Don'ts are hard constraints. **Exit:** you can state from the file what the accent is reserved for and what happens when a token is missing.
3. **Plan the map.** Read how the project styles things (utility classes, CSS modules, CSS-in-JS, its motion library). Run `node scripts/token-check.mjs <folder>` on the source as it stands: that is the baseline. Write the token map: each token and where it lands, each existing literal and the token its role calls for, each gap. Report drift between the contract and the real CSS before fixing any of it, as `added`, `removed` or `modified` with a `regression` flag. For a docs job, the plan is the inventory in [design-system-docs](references/design-system-docs.md): tokens, component unions, two or three real call sites each. **Exit:** every literal in scope has a token or a named gap, and the drift report is written.
4. **Start from the closest gold.** Pick it from the Examples table and open it beside your target. Take its structure: one mirror file, names that are the token's path, components that hold no value of their own. **Exit:** you can say which gold you started from and the one thing you kept.
5. **Build.** The mirror first (CSS variables, the Tailwind theme, or design-system props), then the components. Bind by role. If `integrations.shadcn.enabled` is set, write `css_vars` into the declared CSS file. If the project imports `@ui-sdk/core/web.css`, add the `--ui-*` block from [using-design-file](references/using-design-file.md), UI SDK. A missing token follows `policy.if_missing` (`ask`, `nearest` or `invent_with_note`) under a `.design`, and becomes a proposal comment under a DESIGN.md. Apply `voice` to UI copy with the same force as tokens. **Exit:** no value was typed that is not in the map.
6. **Rehearse with the gate.** `node scripts/token-check.mjs <folder> --gate`, on the folder and never on one file, until it ends `token-check passed`. Fix the largest fault first: contract lines (`contract-invalid:`, `two-contracts:`), then names nothing defines, then literals, then candidates. Every line it prints is a value that will drift. `inconclusive` is never a pass. **Exit:** the last line reads `token-check passed`, and every candidate line has a one-line answer.
7. **Walk [verify](references/verify.md) from evidence.** Answer each question from the gate's output, the diff, or the contract open beside the file. Render once per color scheme the contract defines. Check three bindings at random for role. **Exit:** every answer is yes, or the no is written down.
8. **Fresh-eye review.** Hand a reviewer the evidence, the gold and [review](references/review.md); never your plan, reasons or handover. **Exit:** a ranked list you have answered, or "nothing" with what was opened.
9. **Hand over.** Write `TOKENS.md` beside the contract from the template in [verify](references/verify.md): the gate's last line pasted, the token map, the drift, each literal left in place with its reason, what was not checked. **Exit:** the file exists and its Not checked line is filled in.

## Faults that come back every round

- **A value bound by looks.** 6px because it "looked like" the button; bind by role ([using-design-file](references/using-design-file.md), Reference).
- **A literal that survived.** Grep for hex and `px` and name the missing token behind every survivor ([using-design-md](references/using-design-md.md), Check).
- **Stale `css_vars` trusted in `:root`.** Tokens outrank them; refresh the CSS after token edits ([using-design-file](references/using-design-file.md), shadcn).
- **Two contracts drifting.** The `.design` wins and DESIGN.md is rationale; say so in the file and offer to converge ([using-design-file](references/using-design-file.md), `.design` vs `DESIGN.md`).
- **A sound or a default added where the contract is silent on purpose.** An absent `tokens.sound` means silent ([using-design-file](references/using-design-file.md), Sound, video, and companions).
- **The contract treated as the whole job.** It pins colors and radii and says nothing about a flashing spinner; silence is not permission to default ([using-design-file](references/using-design-file.md), Gotcha).
- **An unknown DESIGN.md field flagged as an error.** The spec is `version: alpha`; pass the field through ([using-design-md](references/using-design-md.md), Gotcha).
- **Docs written from memory.** A documented variant that does not exist is worse than an undocumented one that does ([design-system-docs](references/design-system-docs.md), section 1).
- **An open variant list or a hedge in the docs.** Close the set and give the number ([design-system-docs](references/design-system-docs.md), sections 3 and 4).
- **The same fault as last time.** Read [gotchas](references/gotchas.md) first; append to it when a new one lands.

## Hard rules

1. **The contract outranks this skill.** The order is the user's prompt, the nearest contract, this skill, model defaults. If the contract sets a base duration of 400ms, use 400ms. When you disagree, raise it once in prose, then comply.
2. **`.design` beats DESIGN.md.** When both exist, the `.design` is the contract and DESIGN.md is rationale. Offer to converge them, because two sources drift apart.
3. **Bind by role, never by a value that looks close.** No raw hex, spacing or radius where a token exists. A value that matches is not proof the role matches.
4. **Never edit a contract silently.** A DESIGN.md change is a proposal with human approval. A `.design` edit is made in place with `version` bumped, and any path in `locked` needs a yes first. Drift is reported before it is fixed.
5. **No contract: say so and offer to bootstrap.** Scan the code for the system it already uses. Never invent one without saying so.
6. **Write docs from an inventory of the code.** Every name in the docs traces to a file and a line, because a name from memory teaches an agent a variant that does not exist.
7. **Write in the project's own system.** Express every fix in the styling system the project already uses and reuse its tokens. A correct value written in a second system is a defect, because the next person now maintains two.

Aliases: `contract`, `apply-design-md`. **Posture: build.**

## Examples

Open the closest one before you build (step 4). Each file's top comment says what it is the gold for.

| Need | Example | What to learn |
|---|---|---|
| A `.design` threaded through CSS and components | `examples/design-file` | One mirror file named by token path; components that hold no value of their own; the accent only on the primary action |
| A DESIGN.md threaded through CSS and components | `examples/design-md` | The front matter binds and the body picks: radii nested by role, the defined `button-primary` used instead of a second one |
| A project that styles with Tailwind | `examples/tailwind-theme` | Tokens land in the theme and the component stays in utilities; no bracketed value, no second styling system |
| A design-system doc page | `examples/system-docs` | The four-part order, a closed variant set with its default, a correct and an incorrect example, every name traced to a line |
| A finished handover | `examples/design-file/TOKENS.md` | The gate's last line pasted, the token map, the literals that stayed with their reasons, what was not checked |

`teaching/` holds fourteen bad/good pairs, indexed in [teaching](references/teaching.md). Use one to diagnose a fault; the bad halves are never starting points.

## Find the reference

Open a reference only when the job needs it. Never load the whole folder.

| Job or symptom | Open |
|---|---|
| A `.design` or `<name>.DESIGN` file exists; which contract wins; a drift check; shadcn `css_vars`; the `--ui-*` variables of Vercel's UI SDK; sound or video tokens | [using-design-file](references/using-design-file.md) |
| Only a DESIGN.md exists; linting it; proposing a missing token | [using-design-md](references/using-design-md.md) |
| Writing or repairing design-system docs; an agent keeps hardcoding colors, inventing variants or picking the wrong component | [design-system-docs](references/design-system-docs.md) |
| The last pass; what a gate line means; a symptom and its fix; the `TOKENS.md` template | [verify](references/verify.md) |
| Briefing a reviewer who has not seen your plan | [review](references/review.md) |
| "Mine looks like this bug": the bad/good pair for it | [teaching](references/teaching.md) |

## Never ship

Check the work against this table before finishing.

| Never | Instead |
|---|---|
| `border-radius: 6px` when the scale defines 4 / 8 / 16 | The scale token, such as `var(--rounded-lg)` |
| `font: 14px/1.5 Inter` when the file defines Public Sans 16/1.6 | The typography token |
| A raw hex where a token exists | A token reference; every surviving literal reported with its reason |
| A missing token filled with a literal | A proposal comment for DESIGN.md; `policy.if_missing` for a `.design` |
| A silent rewrite of DESIGN.md | A proposal in a review or PR comment, applied after approval |
| `proposed_changes` or a changelog inside the `.design` | The file edited in place with `version` bumped; git is the audit trail |
| Stale `css_vars` literals trusted in `:root` | The CSS refreshed after token edits; tokens outrank them |
| A sound added when the contract has no `tokens.sound` | Silence; an absent group means silent |
| An unknown DESIGN.md field flagged as an error | The field passed through unchanged |
| Docs written from memory | An inventory of tokens, component unions and two or three real call sites |
| "Use small text sparingly" in the docs | "Body 16px, captions 14px, never below 12px" |
| An open variant list | "Variants: `primary`, `secondary`, `danger`. Nothing else exists." |
| A gate line cleared by hiding the value | The value bound, or the line answered in `TOKENS.md` with its file and line |
| "No literals left" said from memory | The gate's last line, pasted |

## Output

`TOKENS.md` beside the contract, and the same in the reply: the contract and its version, the token map (token, where it lands), the drift report, the edits, the gate's last line, every literal left in place with its reason, and what was not checked.

## Tone

Deferential to the contract and strict about literals. Say "there is no contract here" when there is none, and say "the contract sets 400ms; I would pick under 300ms; using 400ms" when the two disagree. Report every literal left in place with its reason.

## Yours to edit

Read both before producing anything. They outrank the defaults in this skill, and a project's `.design` contract or DESIGN.md outranks them.

- [gotchas](references/gotchas.md): lived failures, one line each. Append one when something goes wrong.
- [pov](references/pov.md): your taste calls.

## Pairs with

- `khe-ui`: the contract is silent on a scale, a contrast pair, dark mode or motion, and that gap needs its rules; and after tokens are threaded, when the screen still feels unfinished.
- `khe-auto`: runs this skill first whenever a project has a contract, then the skill that picks colors, sizes or curves.
- `khe-sound`: only when the contract has a `tokens.sound` group; its values outrank that skill's defaults.

Names without the `khe-` prefix are other people's skills, not part of this one: `stageshow` is Benji Taylor's ([benjitaylor/skills](https://github.com/benjitaylor/skills)); `animate`, `emil-design-eng` and the rest are Emil Kowalski's ([emilkowalski/skills](https://github.com/emilkowalski/skills)); `ui-sdk` is Vercel's ([vercel-labs/ui](https://github.com/vercel-labs/ui)). Install them from their own repos.

Harshit Khemani. MIT.
