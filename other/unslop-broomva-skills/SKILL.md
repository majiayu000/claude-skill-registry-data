---
name: unslop
tier: D
category: design
version: 0.2.4
description: >-
  Remove the "vibecoded" / AI-slop look from an arbitrary frontend codebase at
  the ROOT, autonomously, and prove the result clears a crafted floor. Full-repo
  traversal (any framework) → root-cause attribution (the one file that declares
  each default: font, icons, color/radius/shadow tokens, gradient/glass, motion,
  copy voice) → fix once at the root, never at forty call sites → the substance
  tells no detector covers (legal routes, loading/empty/error states, placeholder
  and fake content, real product evidence) → render at 1280+390 → deterministic
  gate (scripts/unslop_gate.py, exit 0 = clear). Composes the impeccable
  detector (64 rules) and commands, Anthropic frontend-design for direction,
  broomva-design as the house example; reimplements none of them. USE WHEN: a
  site or app "looks vibecoded", "looks AI-generated", "looks like every other
  AI site", "feels generic/templated/slop", "make it feel premium / crafted /
  intentional", "de-slop / unslop this", "does this pass the vibecoded test",
  or before shipping any LLM-built UI. NOT FOR: designing a new surface from
  scratch (impeccable new-work / frontend-design), a11y/perf audits alone
  (impeccable audit), backend-only repos, or a one-line style tweak.
---

# unslop — remove the vibecoded look at the root, prove the crafted floor

Someone says *"this looks vibecoded"* or *"make it feel premium and crafted with care"*. `unslop` runs
one arc over the whole codebase and ends with a PR whose gate is green or whose remaining reds are
named and handed to a human — never a cosmetic pass over the pages someone happened to open.

## The one rule

> **Fix the class, not the example — and prove it on the rendered result.**
>
> A default (Inter, Lucide, purple-to-black, `rounded-2xl`, glass cards, em dashes) is declared in *one*
> place and consumed in forty. Edit the one place. Then screenshot at 1280 and 390 and run the gate;
> reasoning is not validation. Twenty-six of the thirty tells are surface and a prompt removes them;
> the four that are **absence of substance** (no real demo, no loading states, no TOS, no privacy
> policy) are removed only by the real product — the gate keeps them red until a human makes them true.

## Deterministic core (`scripts/`)

| Script | What it does | Exit |
|---|---|---|
| `scripts/unslop_survey.py <repo> [--detect] --json OUT --md OUT` | Full-repo inventory: framework + routes; **roots** (each default → declaring file + blast radius + the single fix); copy tells; **substance** (legal, async-state coverage, placeholders, testimonials, pricing scaffold, product evidence, motion, design docs); impeccable findings if `--detect` | 0 / 2 usage |
| `scripts/unslop_gate.py <repo> [--manifest M \| --detect] --evidence DIR [--waivers W] [--profile] [--strict]` | The crafted floor as PASS/WARN/FAIL per check (`direction.authored`, `detector.clean`, `fonts.deliberate`, `icons.single-system`, `tokens.*`, `copy.*`, `substance.*`, `motion.reduced-motion`, `evidence.render`); waivers need a reason ≥20 chars | 0 clear · 1 FAIL · 2 usage |

Stdlib Python, no edits to the target, any framework (Next app/pages, SvelteKit, Astro, Nuxt, Remix,
Vite+React, static HTML). The detector is *composed*: it is found in the installed `impeccable` skill
or via `npx impeccable detect`; when absent the survey says `unavailable` and the gate WARNs — it never
pretends classes A–C were checked. Override with `UNSLOP_DETECTOR="node /path/detect.mjs"`.

## The arc (`references/arc.md` — read it before running)

```
0 Snapshot → 1 Survey → 2 Direction (decide once, DESIGN.md) → 3 Root plan
→ 4 Fix at root → 5 Structure + copy → 6 Class D (states · legal · evidence · truth)
→ 7 Render + inspect at 1280/390 → 8 Gate → 9 PR + report
```

Never hand control back mid-arc. Never ask "what style do you want?" — infer the direction from the
product's own material and *state* it in DESIGN.md; if there is none, choose the quietest committed
world and say so. Never fabricate substance (policy text, testimonials, demos) to turn a red green.

## Composition map (bstack-native names; generic behavior in parentheses)

| Step | Composes |
|---|---|
| Survey / gate | `scripts/unslop_survey.py`, `scripts/unslop_gate.py` (this skill) |
| Mechanical tells (classes A–C) | **impeccable** detector `detect --json <dir>` (64 rules) + its per-edit hook |
| Direction | **impeccable** `init` / `document` / `new-work`; Anthropic **frontend-design**; **broomva-design** DESIGN.md as the house example of stated decisions |
| Root fixes | **impeccable** `extract`, `typeset`, `colorize`, `layout`, `quieter`; `references/root-cause-playbook.md` |
| Structure + copy | **impeccable** `shape`, `distill`, `clarify`, `polish` |
| Class D | **impeccable** `harden`, `onboard` + a human for what must be true |
| Render evidence | Playwright / agent-browser screenshots (bstack **P11 Empirical**) |
| Audit | **impeccable** `audit` (a11y / perf / responsive) — never re-implemented |
| Ship | bstack **P4 Pipeline**, **P20 Cross-Review** for design-system-touching diffs |

## References

- `references/arc.md` — the nine steps, with what each composes and the anti-rationalizations.
- `references/crafted-floor.md` — the operational definition of "crafted" (typography · spacing · color ·
  motion · states · copy · a11y · perf · consistency · trust), every rule tagged [M] machine-checkable
  or [J] judgment, sourced (Kowalski, Freiberg, Linear, Comeau, Refactoring UI, Butterick, Rams, Apple,
  Material, GOV.UK, Vercel, Stripe, NN/g, Fogg, WCAG, web.dev), contradictions resolved explicitly.
- `references/tells.md` — the dated, regenerable list of current LLM defaults (the reel's 30 → class →
  machine check), Vercel's reject list, the no-ai-slop prose-pattern catalog (dated), and why a
  static ban-list decays.
- `references/root-cause-playbook.md` — per root kind: where the default lives, the one edit, the order.

## Anti-rationalization

| Excuse | Reality |
|---|---|
| "The pages I opened look fine now." | Traversal is the point. Run the survey; `roots[]` and `routes[]` are the scope, not your tabs. |
| "I replaced Inter in every component." | You fixed the example. Re-survey: the old face's site count must reach zero by *one* edit at the root. |
| "The impeccable detector is clean, done." | Classes A–C only. The gate's other half is substance + render evidence; a clean detector with lorem and no privacy route is still slop. |
| "I'll generate a privacy policy / testimonials to pass the gate." | That turns an absence-of-substance tell into a fake-content tell. Leave it red, hand it to a human, name it in the PR. |
| "The tell list says no Lucide, so I'll switch icon sets." | The list detects, it doesn't ban. Keep it and *state the decision* in DESIGN.md; the gate reads it. |
| "It renders fine, I can tell from the JSX." | Screenshots at 1280 and 390 or it did not happen (P11). |
| "Should I ask which direction they want?" | No. Infer from the product's material, state it in DESIGN.md, proceed. A stated quiet choice beats an unstated loud default. |

## Validation (skill self-test)

- `python3 -m pytest tests/` green (survey + gate, both polarities, waivers, strict, evidence, CLI, and one
  regression per P20 finding — every case a false positive or fail-open a reviewer hit on a real repo).
- Dogfood: `scripts/unslop_survey.py <a real repo> --detect` produces roots with a `root_file`; the
  detector status is `ok` when impeccable is installed and `unavailable` (never a silent pass) when not.
- `unslop_gate.py` on the crafted fixture exits 0 with evidence; on the sloppy fixture exits 1 naming
  `fonts.deliberate`, `substance.legal`, `substance.placeholders`, `motion.reduced-motion` among others.
- skillify gate: `skillify_check.py skills/design/unslop --run-tests` exits 0.

## Provenance

BRO-2184. Origin: `/checkit` on an Instagram reel ("30 reasons your site looks vibecoded", 2026-08-15,
34k likes) → `research/entities/pattern/vibecoded-tells.md` (the 26-surface / 4-substance finding) →
this skill. Research synthesis: `research/notes/2026-08-18-unslop-what-others-point-to-synthesis.md`.
