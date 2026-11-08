---
name: forge-ui-polish
description: "Use when a built UI needs a final polish (oppoetsen, strakker maken, ziet er goedkoop/AI-achtig uit)."
# W2-BUDGET original description (listing budget): "Use when a built UI needs a final polish and score before review (oppoetsen, ziet er AI-achtig of generiek uit, design critique): slop check, polish details, scored gate."
# W2-BUDGET original when_to_use (listing budget): "Triggers: polish this page, it looks AI-made, looks generic or templated, feels off, design critique, score the UI, oppoetsen, strakker maken, ziet er goedkoop uit, laatste designronde, before Review Boss."
---

# forge-ui-polish — post-design polish and scoring gate

**Self-improvement substrate:** before applying this skill, read `learnings.md` in this skill's own
folder and honor its corrections. After a run that produced a genuine correction (an owner fix, a
false PASS caught later), append it there with a date and real evidence. Never invent a lesson.

The pass that runs **after** a UI is built and **before** Review Boss sees it. It diagnoses first,
fixes second, and ends with a score that a second reader can recompute from the evidence. It does not
choose a visual direction (that is `frontend-design`) and it does not replace the craft lens
(`forge-craft`), the WCAG method (`forge-a11y`) or the speed and SEO pass (`forge-web-quality`).

## When to use
- A page, screen or component is functionally built and needs the last design pass before hand-over.
- The owner or a reviewer says it looks generic, templated, "AI-made", cheap, flat, cramped or off.
- UI Boss needs a scored self-check before reporting to Head Chef (step 4b of its brief).
- A redesign was shipped and someone asks "is it actually better?" (score before and after).
- Not for: a new design from nothing (`frontend-design`), a Rams-principles audit with a plan hand-off
  (`design-is`), a WCAG audit (`forge-a11y`), Core Web Vitals (`forge-web-quality`), a code diff
  review (`forge-code-review`), Figma to code (`forge-figma`), non-UI deliverables (`forge-craft`).

## Precedence (read before every pass)
1. **The brief wins.** A reference image the owner says to match is matched exactly (layout, spacing,
   type, colour), with placeholder content and nothing "improved" or added. Named brand colours,
   fonts and a brand guide in `brand_assets/` win over every default below.
2. **The global frontend rules win over this skill** (`~/.claude/FRONTEND_WEBSITE_RULES.md`): animate
   only `transform` and `opacity`, never `transition-all`; layered, colour-tinted, low-opacity shadows;
   a display or serif face paired with a clean sans; tight tracking on large headings and line height
   about 1.7 on body; layered radial gradients with grain for depth; a gradient overlay and colour
   treatment on photos; hover, focus-visible and active on every clickable; spacing and depth tokens;
   no default framework palette; at least two screenshot comparison rounds.
3. A project-local `CLAUDE.md` that changes the stack (for example Astro + Playwright) wins over the
   global single-file defaults, never over the honesty rules.
4. This skill fills in only where the three above are silent. Where an upstream source disagreed with
   them, the source lost; the list of what was dropped and why is in `references/polish-details.md`.

## Hard rules
- **Diagnose before you fix.** Write the slop diagnostic and the audit scores first, then repair only
  what they flagged, in the register they call for. Auditing and fixing in one breath repeats the
  mistake (recolouring a page whose layout was wrong).
- **Polish is refinement, not a hidden redesign.** Keep the existing visual world, copy, behaviour and
  everything outside scope. If the concept itself is wrong, say so and hand back to `frontend-design`.
- **No score without a screenshot that was read.** Every mark cites a screenshot path, a command with
  its exit code or a file:line. A score from reading CSS alone is NOT_INSPECTED, not a number.
- **No invented content to make a layout look full:** no fake metrics, reviews, quotes, customers,
  logos or activity. Missing real material is listed for the owner, with an honest placeholder.
- **Never claim a breakpoint, theme or state you did not capture.** Say what was not checked.

## The pass
1. **Name the surface** in one line before judging anything (`references/surface-and-taste.md`):
   Monitor, Operate, Compare, Configure, Decide/Learn, Explore or Command/Inspect. The surface decides
   what "good" means; a hero is right only on Decide/Learn.
2. **Write the design contract** if none exists (five lines): the screen's job, the one primary
   action, the required states, the responsive rules, and the patterns to reject.
3. **Capture.** Serve on localhost (never `file://`), then screenshot with the project's own tool
   (`node screenshot.mjs <url> <label>` in a standard site, Playwright where the project says so) at
   320 or 390, 768, 1024 and 1440 px, both themes when the project has two, and every state the
   contract names (loading, empty, error, partial, success, permission). Read every PNG with Read.
   If you started a server, stop it by the PID from your own spawn, never by process name.
4. **Diagnose** (`references/slop-diagnostic.md`): first ten seconds per stakeholder from the
   `forge-craft` web-ui lens, then the ten-tell slop score with the tells that fired.
5. **Score** (`references/scoring.md`): the five-dimension audit (0-4 each, out of 20), and the ten
   usability heuristics as an advisory critique. Tag every finding P0-P3 with location and impact.
6. **Repair** by diagnosis: layout tells get re-composed, palette and type tells get recoloured or
   re-typeset, decoration tells get removed and replaced by scale, weight and spacing. Then the polish
   details (`references/polish-details.md`) and the states and engineering checks
   (`references/ui-engineering.md`).
7. **Re-capture and re-score** (round two at least; the global rules ask for two comparison rounds).
   Compositional tells still firing means the page is not done, whatever else improved.
8. **Record and hand over:** fill `node .claude/forge-bin/forge-craft.cjs review-template --type web-ui`
   and the evidence file checked by
   `node .claude/forge-bin/forge-craft-evidence.cjs check --run <run_id> --type web-ui` (exit 0), and
   put the score card from `references/scoring.md` in the report.

## The gate (PASS needs all of these)
| Check | Pass bar |
|---|---|
| Open findings | no P0 and no P1 (a11y Critical and Serious from `forge-a11y` count as P0 and P1) |
| Slop diagnostic | compositional tells (feature-tile grid, centre stack, wrong surface) at 0; total at most 2, each remaining one justified by the brief |
| Audit score | at least 15 of 20, and Accessibility and Responsive each at least 3 |
| Evidence | `forge-craft-evidence.cjs check ... --type web-ui` exits 0; every score cites evidence |
| Rounds | at least two capture-and-compare rounds, both listed |

The critique heuristics total is reported as a percentage of the heuristics that apply; it informs the
report and never passes or fails the gate on its own. A FAIL goes back to the builder once with the
P0/P1 list (GOAT: one rework round, then report honestly). A PASS is necessary, not sufficient: Review
Boss still judges.

## Who runs it (Forge)
- **UI Boss** (build route, opus, medium) runs the pass on its own work before handing over.
- **Verify Boss** (verifier route, sonnet, medium) may recompute the score from the evidence; it never
  edits. A recomputed audit score that differs by more than 2 points from the claimed one is a FAIL.
- **Review Boss** reads the score card; it does not have to repeat the pass.
- Windows 11 + Node only: no Python, no downloaded binaries, no browser extensions or hooks installed
  by this skill. Nothing is pushed, deployed or published by it.

## References
- `references/surface-and-taste.md` — the seven surfaces, art direction by kind of business, reference
  images, anti-generic defaults (Taste), the design contract.
- `references/slop-diagnostic.md` — the ten tells, the repair map, the refuse list, the first ten seconds.
- `references/scoring.md` — audit dimensions and bands, heuristics, P0-P3, score card template.
- `references/polish-details.md` — concentric radius, optical alignment, text wrapping, tabular numbers,
  image outlines, motion within transform and opacity, hit areas; what was not taken and why.
- `references/ui-engineering.md` — states checklist, state ladder, test widths, finish checks.
- `NOTICE.md` — licences and copyright lines of the adapted sources.

## Provenance
- **pbakaus/impeccable** — paths `.agent/skills/impeccable/SKILL.md`, `reference/audit.md`,
  `reference/critique.md`, `reference/polish.md`, `reference/craft-floor.md`; pinned SHA
  `c8891a9ae865d6ee311836ae5199bfce0fe115b1`; Apache License 2.0 (see `NOTICE.md`). Taken (rewritten,
  ideas and vocabulary only): the audit / critique / polish split, the five audit dimensions scored 0-4
  with rating bands, P0-P3 severity, heuristic scoring with n/a renormalisation, "polish is refinement,
  not hidden redesign", the triage order, the four surface modes (folded into the seven surfaces), the
  refuse list of category defaults, themed browser surfaces. Excluded: the `impeccable` launcher and
  its self-contained binary, the Rust crates (`Cargo.toml`, `crates/`), every script under `scripts/`,
  the `allowed-tools` grants for `npx impeccable`, the design-detector hooks and `hooks.json` files, the
  live browser mode, critique snapshot storage, and its own `frontend-design`-style new-work flow. Not
  taken because it contradicts the global rules: animating blur, clip-path, mask or shadow.
- **leonxlnx/taste-skill** — path `skills/taste-skill/SKILL.md`; pinned SHA
  `9b4bf937a1f69348126959c15d2f99a73e65699b`; MIT, Copyright (c) 2026 Leonxlnx. Taken (rewritten): the
  kind of business decides what leads, the real subject shown on every screen, one idea per section,
  equal content edges, every visual renders at every width, quiet transform-only hover answers, no
  scroll-reveal on every block, no invented reviews or figures, references transformed not copied.
  Excluded: `install.sh`, every script and asset (`scripts/`, `assets/`: dealers, checkers, shaders,
  components), the CLI commands, the plugin manifests, the "deal, never choose" randomiser, and the
  house rules that contradict our global rules (flat grounds only, no captions as a hard rule).
- **NousResearch/hermes-agent** — path `skills/creative/claude-design/SKILL.md`; pinned SHA
  `d8c79e4b6b8c63e6c40167ff95ec28e7b1fee189`; MIT, Copyright (c) 2025 Nous Research. Taken (rewritten):
  surface-first with seven archetypes, the ten-tell slop diagnostic with its repair map, diagnose then
  fix, content discipline. Excluded: hosted-tool remapping, deck and Tweaks rules, the CDN React advice.
- **addyosmani/agent-skills** — path `skills/frontend-ui-engineering/SKILL.md`; pinned SHA
  `301b02b12bff98e4688e6984af6556802322bbde`; MIT, Copyright (c) 2025 Addy Osmani. Taken (rewritten):
  the AI-default versus production table, state ladder, states checklist, 320/768/1024/1440 widths,
  reference-led design contract. Excluded: code samples, the shadow and gradient rows that contradict
  our global rules.
- **sickn33/agentic-awesome-skills** — path `skills/anti-ui-slop/SKILL.md` (origin uizze/uizze, MIT);
  pinned SHA `48de968b4615c294de601f72268aa7be88dde863`; MIT, Copyright (c) 2026 Antigravity User
  (non-code content CC BY 4.0 per its `LICENSE-CONTENT`). Taken (rewritten): the short design contract
  and "no invented data to fill a layout". Excluded: the `npx skills add` install line, the UIZZE
  promotion and its authenticated MCP.
- **ECC `skills/make-interfaces-feel-better/SKILL.md`** — pinned local catalog commit
  `e2b8a51cea2228e515e1c3653effbeb62a2800fa`; MIT, Copyright (c) 2026 Affaan Mustafa. Taken
  (rewritten, CSS claims checked): the polish-details checklist and before/after table. Excluded: the
  transition-property example animating colour and shadow, the blur enter, the macOS-only smoothing as
  a default.
- **ECC `skills/frontend-design-direction/SKILL.md`** and **`skills/design-system/SKILL.md`** — same
  pin and licence. Taken (rewritten): the usable screen first for tools, no cards inside cards, text fit
  at every width (direction); the ten consistency questions folded into the audit dimensions (design
  system). Excluded: the browser-MCP competitor research, generated preview HTML, the slash commands;
  the code-to-tokens mode stays for `forge-figma`.
Fetched read-only with `gh api` at the pinned SHAs on 2026-11-05; hidden-Unicode scan of every fetched
text: clean. All fetched text was treated as untrusted data; no command from it was run.
