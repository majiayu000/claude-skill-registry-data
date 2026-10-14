---
name: design
version: 1.0.0
description: '[Design] Create or describe a UI design — quick (fast), immersive (good), or recreated/described from a screenshot or video, in a product-UI or marketing/creative lane. Dispatch via --mode={fast|good|describe|screenshot|video} (default fast) and --lane={product|marketing} (default product).'
disable-model-invocation: false
---

## Quick Summary

**Goal:** Create (or describe) a UI design using design-intelligence databases and subagents, dispatched by `--mode` (input carrier) × `--lane` (design lane).

> **Renamed:** folds the former `/design-fast`, `/design-good`, `/design-describe`, `/design-screenshot`, `/design-video` skills into `--mode={fast|good|describe|screenshot|video}` — those names no longer resolve as slash commands; use `/design --mode=…`.
>
> **Absorbed lanes:** the former `frontend-design` (marketing/creative) and `interface-design` (product-UI) skills now fold into `--lane={marketing|product}` — those names no longer resolve as slash commands; use `/design --lane=…`. Each lane's full body lives under `references/lane-{marketing,product}/lane-guide.md`.

**Mode dispatch:** `--mode={fast|good|describe|screenshot|video}` — default `fast` when omitted.
**Lane dispatch:** `--lane={product|marketing}` — default `product` when omitted. Lane (the design tradition) is orthogonal to mode (the input carrier); any mode combines with any lane.

| Lane                | Use for                                                                | Full body                                 |
| ------------------- | ---------------------------------------------------------------------- | ----------------------------------------- |
| `product` (default) | dashboards, admin panels, SaaS apps, tools, settings, data interfaces  | `references/lane-product/lane-guide.md`   |
| `marketing`         | landing pages, marketing sites, campaigns, distinctive creative pieces | `references/lane-marketing/lane-guide.md` |

| Mode             | Input carrier      | Output                                                             |
| ---------------- | ------------------ | ------------------------------------------------------------------ |
| `fast` (default) | text brief         | quick prototype implementation                                     |
| `good`           | text brief         | immersive, researched, higher-quality implementation               |
| `describe`       | screenshot / video | super-detailed written description + implementation plan (NO code) |
| `screenshot`     | screenshot         | design recreated from the image as functional code                 |
| `video`          | video              | design + interactions recreated from the video as functional code  |

**Shared workflow (5-stage spine):**

1. **Research** — Run `ui-ux-pro-max` searches for design intelligence (ALWAYS FIRST)
2. **Ingest** — For visual modes (`describe`/`screenshot`/`video`), use `visual analysis tooling` to analyze the screenshot/video in super-detail
3. **Design** — Use `ui-ux-designer` subagent to create the design (or, for `describe`, an implementation plan), applying the selected lane's craft body
4. **Implement** — Build as code following the selected lane guide: `references/lane-product/lane-guide.md` (product UIs) or `references/lane-marketing/lane-guide.md` (marketing/creative). Skipped in `describe` mode.
5. **Document** — Present to user for approval; update `./docs/design-guidelines.md` if needed

**Key Rules:**

- Always activate `ui-ux-pro-max` FIRST for design intelligence
- Default to pure HTML/CSS/JS if the user doesn't specify a framework
- Use `visual analysis tooling` for generating AND reviewing real visual assets
- Use media processing tooling (RMBG) to remove backgrounds from generated assets when needed

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

## Arguments & Mode Dispatch

`/design --mode={fast|good|describe|screenshot|video} --lane={product|marketing} <brief | screenshot | video>`

- When `--mode` is omitted, default to `--mode=fast`.
- When `--lane` is omitted, default to `--lane=product` (the dominant PBI/app use). Pick `marketing` for landing pages, campaigns, and distinctive creative pieces.
- `--mode` (input carrier) and `--lane` (design tradition) are orthogonal — e.g. `--mode=screenshot --lane=product` recreates a dashboard screenshot in the product-UI craft tradition.
- `$ARGUMENTS` carries the full input after the command. Interpret it per mode: `fast`/`good` → a text design brief; `describe`/`screenshot` → a screenshot reference (path/URL/attachment); `video` → a video reference.

### Lane selection (apply the chosen lane's craft body at stages 3-4)

- **`--lane=product` (default)** — product UIs: dashboards, admin panels, SaaS apps, tools. Domain-driven craft (intent → domain exploration → signature → layered surfaces/tokens). Full body: `references/lane-product/lane-guide.md`.
- **`--lane=marketing`** — marketing/creative: landing pages, campaigns, screenshot replication. Bold aesthetic direction (distinctive type, cohesive palette, atmosphere, motion). Full body: `references/lane-marketing/lane-guide.md`.

Do NOT inline the lane bodies here — read the matching `lane-guide.md` when the lane is selected.

## Required Skills (Priority Order)

1. **`ui-ux-pro-max`** — Design intelligence database (ALWAYS ACTIVATE FIRST)
2. **In-skill lane references** — `references/lane-{product|marketing}/lane-guide.md` (+ their reference files) own implementation, screenshot/video analysis, and design replication for the selected lane.

**Ensure token efficiency while maintaining high quality.**

## Shared First Step (ALL modes)

> **[BLOCKING] Step 0 — Understand the existing UI first** (per the `SYNC:existing-ui-research` protocol carried by this skill). Before designing or updating any screen/component, inventory the existing related UI (screens, pages, components already serving this feature/domain) and map every connected feature flow that links to / embeds / navigates to-or-from it, so the design faithfully matches the current UI system. Skip only for non-UI work (state it explicitly).

**FIRST**, run `ui-ux-pro-max` searches to gather design intelligence:

```bash
python $HOME/.claude/skills/ui-ux-pro-max/scripts/search.py "<product-type>" --domain product
python $HOME/.claude/skills/ui-ux-pro-max/scripts/search.py "<style-keywords>" --domain style
python $HOME/.claude/skills/ui-ux-pro-max/scripts/search.py "<mood>" --domain typography
python $HOME/.claude/skills/ui-ux-pro-max/scripts/search.py "<industry>" --domain color
```

## Design Principles Contract (all modes)

The 40 UI/UX Design Principles (`UI-1.1`–`UI-9.4`) carried as the `SYNC:ui-ux-design-principles` block below bind EVERY mode of this skill. Project design-system docs OUTRANK them — surface a genuine conflict to the user with both sides, NEVER resolve it silently.

**Generative modes (`fast`, `good`) — APPLY the clauses as an output contract on the design you produce:**

1. **States first.** Design and build the empty, loading and error state BEFORE the populated state (`UI-1.5`), and reserve space for anything that loads so nothing shifts in (`UI-9.3`).
2. **All 5 interaction states per interactive element** — default, hover, focus, active, disabled — plus loading where it applies (`UI-5.2`); keep a visible focus ring, restyled if it clashes but NEVER removed (`UI-5.5`).
3. **Declare the scales, never improvise them.** State the type scale as 6 named steps with no one-off sizes (`UI-2.5`), body 16px web / 17px mobile and never below 14px (`UI-2.2`), measure 45–75 characters (`UI-2.3`); and declare ONE spacing unit — 4px or 8px base, every gap a multiple of it (`UI-4.1`). Both declarations belong in the summary you report back at stage 5; an undeclared scale is an incomplete design, not a style choice.
4. **Contrast is measured, not eyeballed** — state the target AND the measured value: 4.5:1 text, 3:1 UI edges (`UI-3.1`); colour NEVER carries meaning alone — pair it with an icon, label or position (`UI-3.3`).
5. **Touch surfaces.** When the design covers a mobile/touch surface, hit targets are ≥44×44pt and 8px apart (`UI-8.1`) and primary actions sit in the bottom third where the thumb lives (`UI-8.2`). When it does not, state that explicitly so the §8 skip is auditable.

**Reporting modes (`describe`, and the analysis pass of `screenshot` / `video`) — REPORT against the clauses:** the super-detailed description MUST name which clauses the OBSERVED design SATISFIES and which it VIOLATES, cited by ID — e.g. type-scale drift (`UI-2.5`), contrast failure with the measured ratio (`UI-3.1`), undersized touch targets (`UI-8.1`), missing empty/loading/error states (`UI-1.5`), a removed focus ring (`UI-5.5`). A violation is RECORDED, never silently reproduced: `describe` carries it into the implementation plan as a correction; `screenshot` / `video` then apply the five generative obligations above so the recreation FIXES the violation rather than inheriting it — flag any correction that changes the visual match and confirm it with the user before shipping it.

## Mode Branches

### `--mode=fast` (default) — quick design

1. Run the shared `ui-ux-pro-max` searches above.
2. Use `ui-ux-designer` subagent to start the design process.
3. If the user doesn't specify, create the design in pure HTML/CSS/JS.
4. Report back with a brief summary of the changes; ask the user to review and approve.
5. On approval, update `./docs/design-guidelines.md` if needed.

### `--mode=good` — immersive, high-quality design

Same spine as `fast`, raised to a higher quality bar (iterate on details):

1. Run comprehensive `ui-ux-pro-max` searches across all domains.
2. Use `researcher` subagent to research design style, trends, fonts, colors, borders, spacing, elements' positions, etc.
3. Use `ui-ux-designer` subagent to implement the design step by step based on the research.
4. If the user doesn't specify, create the design in pure HTML/CSS/JS.
5. Report back with a summary; ask the user to review and approve.
6. On approval, update `./docs/design-guidelines.md` if needed.

- **ALWAYS REMEMBER you have the skills of a top-tier UI/UX Designer who won many awards on Dribbble, Behance, Awwwards, Mobbin, TheFWA.**
- Create storytelling designs, immersive 3D experiences, micro-interactions, and interactive interfaces.

### `--mode=describe` — describe only (NO implementation)

Treat `$ARGUMENTS` as the screenshot/video to describe.

1. Use `visual analysis tooling` to describe super-details of the screenshot/video so a developer can implement it easily.
    - Be specific about design style, every element, elements' positions, every interaction, every animation, every transition, every color, every border, every icon, every font style/size/weight, every spacing/padding/margin, every size/shape/texture/material/light/shadow/reflection/refraction/blur/glow/image, background transparency, etc.
    - **IMPORTANT:** Predict the font name (Google Fonts) and font size — don't just use Inter or Poppins.
2. Use `ui-ux-designer` subagent to create a design implementation **plan** following the progressive-disclosure structure so the result matches the screenshot/video:
    - Create a directory using the naming pattern from the `## Naming` section.
    - Save the overview access point at `plan.md`, keep it generic, under 80 lines, listing each phase with status/progress and links.
    - For each phase, add `phase-XX-phase-name.md` with sections (Context links, Overview with date/priority/statuses, Key Insights, Requirements, Architecture, Related code files, Implementation Steps, Todo list, Success Criteria, Risk Assessment, Security Considerations, Next steps).
3. Report back with a summary of the plan. **Do NOT implement.**

### `--mode=screenshot` — recreate from image as code

Treat `$ARGUMENTS` as the screenshot to recreate exactly.

1. Use `visual analysis tooling` to describe super-details of the screenshot (design style, trends, fonts, colors, border, spacing, elements' positions, size, shape, texture, material, light, shadow, reflection, refraction, blur, glow, image, background transparency, transition, etc.).
    - **IMPORTANT:** Predict the font name (Google Fonts) and font size — don't just use Inter or Poppins.
2. Use `ui-ux-designer` subagent to create a design plan following the progressive-disclosure structure (as in `describe`) so the final result matches the screenshot. Keep every research markdown report concise (≤150 lines).
3. Implement the plan step by step.
4. If the user doesn't specify, create the design in pure HTML/CSS/JS.
5. Report back with a summary; ask the user to review and approve.
6. On approval, update `./docs/design-guidelines.md` if needed.

- **ALWAYS REMEMBER you have the skills of a top-tier UI/UX Designer who won many awards on Dribbble, Behance, Awwwards, Mobbin, TheFWA.**
- Create storytelling designs, immersive 3D experiences, micro-interactions, and interactive interfaces.

### `--mode=video` — recreate from video as code

Treat `$ARGUMENTS` as the video to recreate exactly. Same as `--mode=screenshot`, but ingest a VIDEO and capture BOTH static layout AND interaction/animation/transition patterns.

1. Use `visual analysis tooling` to describe super-details of the video: every element, every interaction, every animation, every transition, every color, every font, every border, every spacing, every size/shape/texture/material/light/shadow/reflection/refraction/blur/glow/image, background transparency, etc.
    - **IMPORTANT:** Predict the font name (Google Fonts) and font size — don't just use Inter or Poppins.
2. Use `ui-ux-designer` subagent to create a design plan following the progressive-disclosure structure so the final result matches the video. Keep every research markdown report concise (≤150 lines).
3. Implement the plan step by step.
4. If the user doesn't specify, create the design in pure HTML/CSS/JS.
5. Report back with a summary; ask the user to review and approve.
6. On approval, update `./docs/design-guidelines.md` if needed.

- **ALWAYS REMEMBER you have the skills of a top-tier UI/UX Designer who won many awards on Dribbble, Behance, Awwwards, Mobbin, TheFWA.**
- Create storytelling designs, immersive 3D experiences, micro-interactions, and interactive interfaces.

## Notes (all modes)

- **Design system (canonical):** When implementing UI — HTML, CSS, or SCSS — read the project canonical design-system doc `docs/project-reference/design-system/design-system-canonical.md` first for design tokens, component patterns, and BEM conventions. Prefer `designSystem.canonicalDoc` + `tokenFiles` (resolved from `docs/project-config.json`) over per-app docs for new design work.
- Remember you have the capability to generate images, videos, edit images, etc. with `visual analysis tooling` skills. Use them to create the design and real assets.
- Always review, analyze, and double-check generated assets with `visual analysis tooling` skills to verify quality.
- Use media processing tooling (RMBG) to remove background from generated assets if needed (`good`/`screenshot`/`video`).
- Maintain and update `./docs/design-guidelines.md` docs if needed.

---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ATTENTION ask user whether to skip.

Think hard to plan & start working on these tasks follow the Orchestration Protocol, Core Responsibilities, Subagents Team and Development Rules. Parse `--mode` from the input (default `fast`) and route to the matching branch above:
<tasks>$ARGUMENTS</tasks>

<!-- SYNC:existing-ui-research -->

> **[BLOCKING] Understand the existing UI before you design or spec a new/updated screen.** Before producing any wireframe, mockup, screen design, or UI spec:
>
> 1. **Inventory existing related UI** — search the project for screens, pages, and components already serving this feature or its domain (consult design-system docs + the real component inventory).
> 2. **Map connected flows** — identify every feature that links to, embeds, includes, or navigates to/from the new screen; trace its entry and exit flows so the new screen fits them.
> 3. **Reuse before invent** — prefer existing components, patterns, and layout conventions; justify any new component against what already exists.
> 4. **Record findings** — note the matched existing screens/components + connected flows in the artifact so downstream design faithfully matches the current UI system.
>
> **Skip ONLY** when the feature is backend-only (no UI) — state that explicitly.

<!-- /SYNC:existing-ui-research -->

<!-- SYNC:ui-ux-design-principles -->

> **UI/UX Design Principles (Rev 1.0 — 40 clauses, web + mobile)** — the working rule set for ANY task that designs, plans, implements, or reviews a user interface. Applies to BOTH platforms unless a clause names one (§8 is mobile/touch). Cite clauses by ID: `UI-3.1`, `UI-8.2`.
>
> **Precedence:** project design-system / SCSS / frontend-pattern docs OUTRANK these clauses; these clauses outrank generic taste. A genuine conflict is SURFACED to the user with both sides — NEVER resolved silently. — why: the project's own recorded decision is the authority; these clauses are the default when it is silent.
>
> **1.0 Visual Hierarchy & Layout**
>
> - `UI-1.1` One focal point per screen. Two elements competing for first read → demote one.
> - `UI-1.2` Signal order: size → weight → colour → position. Use the cheapest signal that works before adding another.
> - `UI-1.3` Group by proximity, NEVER by border. Whitespace separates cleanly; boxes inside boxes do not.
> - `UI-1.4` Align to a shared edge. Every unexplained indent reads as an accident.
> - `UI-1.5` Design the empty, loading and error state FIRST. The full state is the easy one.
>
> **2.0 Typography**
>
> - `UI-2.1` Max 2 families, 3 weights each. More variety reads as inconsistency, not range.
> - `UI-2.2` Body text 16px web, 17px mobile. NEVER below 14px for anything a user must read.
> - `UI-2.3` Line length 45–75 characters. Constrain the measure, not the container.
> - `UI-2.4` Leading scales inversely with size: 1.5 body, 1.1–1.2 display.
> - `UI-2.5` Fixed type scale — 6 named steps shared with engineering. NEVER one-off sizes.
>
> **3.0 Colour & Contrast**
>
> - `UI-3.1` Contrast 4.5:1 text, 3:1 UI edges. Measure it — NEVER judge by eye on a bright screen.
> - `UI-3.2` One accent, one job. An accent that is everywhere points at nothing.
> - `UI-3.3` Colour NEVER carries meaning alone — pair it with an icon, label or position.
> - `UI-3.4` Dark mode is NOT inverted light mode. Lift surfaces to signal elevation; soften pure-white text.
>
> **4.0 Spacing & Grid**
>
> - `UI-4.1` One spacing unit, multiplied — 4px or 8px base; every gap a multiple of it.
> - `UI-4.2` Space belongs to the container, not the child. Use `gap`; reserve margins for exceptions.
> - `UI-4.3` Tighter inside, looser between — inner padding always smaller than the gap to the next group.
> - `UI-4.4` Breakpoints follow content, not devices. Break where the layout stops working.
>
> **5.0 Interaction & Feedback**
>
> - `UI-5.1` Every action gets a response under 100ms, even when the result takes longer.
> - `UI-5.2` Specify all 5 states — default, hover, focus, active, disabled — plus loading where it applies.
> - `UI-5.3` Prefer undo over confirmation. Confirm ONLY what cannot be reversed.
> - `UI-5.4` Motion clarifies cause and effect: 150–250ms, ease-out, honours reduced-motion.
> - `UI-5.5` Keep the visible focus ring. Restyle it if it clashes; NEVER remove it.
>
> **6.0 Navigation & IA**
>
> - `UI-6.1` Every screen answers: where am I, what's here, where next.
> - `UI-6.2` Max 5 top-level destinations. Depth beats a crowded first level.
> - `UI-6.3` Label by the user's word, not the internal one. Team vocabulary is not a taxonomy.
> - `UI-6.4` Every state deserves a URL or a back path. Deep links and hardware back must land somewhere sensible.
>
> **7.0 Forms & Input**
>
> - `UI-7.1` Ask for less. Every field needs a reason it exists today.
> - `UI-7.2` Labels stay visible. Placeholders are hints, NEVER labels.
> - `UI-7.3` Validate on blur, not on keystroke. Errors sit next to the field and say how to fix it.
> - `UI-7.4` Match keyboard to data type — correct input type, autocomplete and autocapitalise on every field.
> - `UI-7.5` NEVER lose entered data. Preserve input across errors, navigation and refresh.
>
> **8.0 Mobile & Touch** _(mobile/touch surfaces)_
>
> - `UI-8.1` Hit target ≥44×44pt, 8px apart. The target may exceed the visible icon.
> - `UI-8.2` Primary actions in the bottom third — that is where the thumb lives.
> - `UI-8.3` Gestures are shortcuts, NEVER the only route. Anything swipeable is also tappable.
> - `UI-8.4` Respect safe areas and the keyboard. Notch, home indicator and on-screen keyboard all steal space.
>
> **9.0 Speed & Perceived Speed**
>
> - `UI-9.1` Show structure before data — skeletons for known layouts, spinners only for unknown waits.
> - `UI-9.2` Assume success optimistically. Update UI first, reconcile after, roll back visibly on failure.
> - `UI-9.3` Reserve space for anything that loads. Images, ads and fonts must NEVER shift the layout.
> - `UI-9.4` Design for the slow connection. Offline, timeout and retry are states, NOT edge cases.
>
> **Apply by role** — the clauses are one set; what you DO with them depends on the task:
>
> | Role                                | Obligation                                                                                                                                                              |
> | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | DESIGN / PLAN a surface             | Clauses shape the artifact: empty/loading/error specified first (`UI-1.5`), all 5 states enumerated (`UI-5.2`), type scale + spacing unit declared (`UI-2.5`, `UI-4.1`) |
> | IMPLEMENT a component               | Pre-completion gate: states · tokens · contrast · focus ring · touch target · reserved space (`UI-5.2`, `UI-2.5`/`UI-4.1`, `UI-3.1`, `UI-5.5`, `UI-8.1`, `UI-9.3`)      |
> | REVIEW UI code or a design artifact | Each clause is a fail-condition; every finding cites `UI-<clause>` + `file:line` + severity. NEVER a tick-box sweep — one focused pass per section                      |
> | SCAN / document a UI system         | Record where the PROJECT deliberately deviates, so the overriding doc becomes the recorded authority                                                                    |
>
> **Skip ONLY** when the change has no user-facing surface (backend-only, tooling, docs) — state that explicitly so the skip is auditable, not an omission.

<!-- /SYNC:ui-ux-design-principles -->

<!-- SYNC:ai-mistake-prevention -->

> **AI Mistake Prevention** — Failure modes to avoid on every task:
>
> **Re-read files after context changes.** Context compaction, resume, or long-running work can make memory stale; verify current files before acting.
> **Verify generated content against source evidence.** AI hallucinates APIs, names, claims, and document facts. Check the relevant source before documenting or referencing.
> **Check downstream references before deleting or renaming.** Removing an artifact can stale docs, generated mirrors, configs, and callers; map references first.
> **Trace the full impact chain after edits.** Changing a definition can miss derived outputs and consumers. Follow the affected chain before declaring done.
> **Verify ALL affected outputs, not just the first.** One green check is not all green checks; validate every output surface the change can affect.
> **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Before changing or reporting a constant, limit, flag, cutoff, wording, or pattern, read nearby context and history, the CALLER's ordering, and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard.
> **Surface ambiguity before acting — don't pick silently.** Multiple valid interpretations require an explicit question or stated assumption with risk.
> **Assert the outcome your system owns, not the intermediate state your infrastructure owns.** When verifying async work, assert the final business state — never the delivery/retry bookkeeping held in shared infrastructure that any co-running process can write. Such a check passes when run alone and flakes the moment anything else shares that infrastructure.
> **Keep shared guidance role-relevant.** Universal guidance must help every receiving skill or agent; code-specific obligations belong only in code-specific protocols.

<!-- /SYNC:ai-mistake-prevention -->

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->

<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

<!-- SYNC:ui-ux-design-principles:reminder -->

- **MUST ATTENTION** apply the 40 UI/UX Design Principles (`UI-1.1`–`UI-9.4`) to any user-facing surface: one focal point, proximity grouping, empty/loading/error designed FIRST (§1) · ≤2 families, 16px web / 17px mobile body, never <14px, 45–75ch, fixed 6-step scale (§2) · 4.5:1 text / 3:1 edges measured, one accent, colour never alone, dark mode ≠ inversion (§3) · one 4/8px unit, `gap` over margins, tighter-inside-looser-between, content-driven breakpoints (§4) · <100ms response, all 5 states, undo over confirm, 150–250ms ease-out honouring reduced-motion, visible focus ring (§5) · where-am-I/what's-here/where-next, ≤5 top-level destinations, user's words, URL or back path (§6) · fewer fields, visible labels, validate on blur, matched keyboard, NEVER lose input (§7) · ≥44×44pt targets 8px apart, bottom-third primaries, gestures never the only route, safe areas (§8) · structure before data, optimistic update with visible rollback, reserved space, slow-connection states (§9). Project design-system docs OUTRANK these clauses — a genuine conflict goes to the user, NEVER resolved silently. Cite every finding as `UI-<clause>` + `file:line`. Skip ONLY for changes with no user-facing surface, stated explicitly.

<!-- /SYNC:ui-ux-design-principles:reminder -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

## Closing Reminders

**MUST ATTENTION — Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.
- **Critical Thinking:** traced `file:line` proof, confidence >80%; NEVER present a guess as fact.

- **MANDATORY IMPORTANT MUST ATTENTION** break work into small todo tasks using `TaskCreate` BEFORE starting
- **MANDATORY IMPORTANT MUST ATTENTION** search codebase for 3+ similar patterns before creating new code
- **MANDATORY IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim (confidence >80% to act)
- **MANDATORY IMPORTANT MUST ATTENTION** add a final review todo task to verify work quality
- **MANDATORY IMPORTANT MUST ATTENTION** apply the 40 UI/UX Design Principles (`UI-1.1`–`UI-9.4`) to every design: empty/loading/error states designed FIRST (`UI-1.5`), all 5 interaction states per interactive element (`UI-5.2`), type scale (6 named steps, `UI-2.5`) and spacing unit (4/8px base, `UI-4.1`) DECLARED not improvised, contrast measured and stated (4.5:1 text / 3:1 edges, `UI-3.1`), ≥44×44pt touch targets + bottom-third primaries on mobile surfaces (`UI-8.1`, `UI-8.2`); `fast`/`good` APPLY them, `describe`/`screenshot`/`video` also REPORT by clause ID which the observed design satisfies or violates — project design-system docs outrank the clauses, conflicts go to the user

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using TaskCreate.
