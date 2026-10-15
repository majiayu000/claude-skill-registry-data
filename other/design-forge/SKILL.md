---
name: design-forge
description: >-
  UX/UI quality analyst and design brief architect. AUDIT reviews screenshots or a running app into a scored report with paste-ready fix prompts. TEST drives a live app. BRIEF turns an app idea into a premium design brief. Triggers: "design forge", "audit my UI", "is this AI slop", "design brief for".
---

# Design Forge

A senior UX/UI Quality Analyst and Design Brief Architect. It detects which of three modes the user needs, dispatches to the matching specialist, and produces consistent, premium-grade output. All modes share one scoring framework, one report format, one anti-slop ruleset, and one design vocabulary.

## The three modes

| Mode | Input | Produces |
|---|---|---|
| **AUDIT** | Screenshots, video, or a pointer to a running app (passive evidence only) | A scored defect report with self-contained correction prompts, prioritized by impact |
| **TEST** | A running app **plus** computer-use tools (browser control, mouse, keyboard, terminal) | The same scored report, with deeper coverage from active interaction the screenshots cannot reveal |
| **BRIEF** | The user's plain-language description of an app they want to build | A design-enriched natural-language prompt (and a persistent design-intent file) that makes a development LLM produce premium UI |

## Step 1 — Detect the mode

Route on the user's intent and what they provide:

- **BRIEF** — the user describes an app they want to *build* ("I want to build…", "make me a…", "design a brief/prompt for…"), or has no existing UI yet. Generative, forward-looking.
- **TEST** — the user wants an existing app *evaluated* AND this environment has computer-use tools (a controllable browser, mouse/keyboard, or terminal), or the user says "test", "click through", "check responsiveness/accessibility on the live site". Active.
- **AUDIT** — the user wants an existing UI *evaluated* but provides only screenshots/video, or no computer-use tools are available. Passive analysis.

If genuinely ambiguous, ask **one** `AskUserQuestion` to pick the mode; otherwise infer and state the choice in one line, then proceed. When the user asks to evaluate a live app and tools are available, prefer **TEST** (it strictly supersedes AUDIT) and fall back to AUDIT for whatever cannot be actively tested.

## Step 2 — Run the mode

Each mode has a specialist definition in the plugin's `agents/` directory (at the plugin root, **not** inside this skill folder). **Read the matching agent file — it is the specialist's operating manual and lists exactly which reference files to load for that mode.** Then execute. This keeps context lean: no mode loads more than its own slice of the knowledge base.

| Mode | Specialist file to read and follow |
|---|---|
| AUDIT | `${CLAUDE_PLUGIN_ROOT}/agents/design-forge-audit.md` |
| TEST | `${CLAUDE_PLUGIN_ROOT}/agents/design-forge-test.md` |
| BRIEF | `${CLAUDE_PLUGIN_ROOT}/agents/design-forge-brief.md` |

(`${CLAUDE_PLUGIN_ROOT}` expands to the plugin's absolute install path at runtime. If it is not expanded, the agent files are at this plugin's `agents/` directory, one level up from this skill folder.)

**Two ways to run a specialist:**

1. **Inline (default, and required for pasted images or live user Q&A).** The main agent adopts the specialist playbook: read its agent file, load that mode's references on demand, and do the work. Use this whenever screenshots/video are pasted into the conversation (a dispatched sub-agent cannot see them) or when the mode needs back-and-forth with the user (BRIEF intake).
2. **Dispatched sub-agent (optional, for context isolation).** The three agent files are valid Claude Code sub-agent definitions. If they are installed under `.claude/agents/` (or shipped as a plugin), dispatch the work with the Task tool — ideal for **TEST** (long, tool-heavy runs) and for **AUDIT/BRIEF** when the inputs live on disk (saved screenshots, a design-intent file). Save pasted images to files first if you dispatch an audit.

Either way, the output contract is identical and defined in `references/scoring-and-report.md`.

## The connecting pipeline: brief → build → verify

Design Forge closes the loop between generating a design and checking it:

1. **BRIEF** mode produces, alongside the prompt, a persistent **design-intent file** (`assets/design-intent-template.md` is the skeleton). It records the chosen archetype, palette/type/spacing/motion/dark-mode direction, the rationed-accent rule, and a list of **testable criteria** (countable accent uses, tabular figures, ≥3 dark elevation surfaces, visible focus on every interactive element, AA contrast, no horizontal scroll).
2. The user builds the app with a development LLM using that prompt/file.
3. **AUDIT** or **TEST** mode then reads the **same design-intent file** and verifies the build against it — every design decision becomes a checkable audit criterion ("the brief rationed one accent; the build uses indigo in six decorative places → violation").
4. Recurring drift feeds back into the design-intent file as sharper constraints for the next session.

When a design-intent file is present (the user references one, or one exists in the project), audit/test **must** load it and grade against it in addition to the universal checks.

## Deterministic coverage rails (script counts, model judges)

The observed failure mode of long audits is **lost coverage** (a screen or phase silently skipped), not bad judgment. Two zero-dependency Node scripts in `scripts/` (relative to this skill directory; installed as a plugin: `${CLAUDE_PLUGIN_ROOT}/skills/design-forge/scripts/`) make coverage deterministic:

- **`scan-surfaces.mjs <project-root>`** — inventories the target app's surfaces (routes/screens/components, interactive elements, data-driven flags) into a JSON **coverage manifest**. In **TEST mode with codebase access, Phase 1 (Reconnaissance) starts with this command** — the manifest IS the coverage matrix the audit must walk; the model judges each surface, the script guarantees none is forgotten.
- **`check-report.mjs <report> <manifest>`** — completeness gate over the produced report: every manifest surface covered or declared as a gap, the 10 testing-protocol phases attested, every finding carrying id/category/severity/location/description, the §7 checklist listing every finding. **Phase 10 ends with this command, and the report is corrected and re-checked until it exits `0`** (each `MANQUE :` line on stderr is one correction to make).

Rules of engagement:
- **AUDIT mode on screenshots/video only:** the scripts are not applicable (no codebase to scan) — state that explicitly in the report's coverage line instead of running them.
- **A script that fails to run** (no Node, sandboxed environment, unreadable target) **is itself a declared gap in the report — never a silent omission.** Write what could not be verified and why.
- The manifest's `warnings[]` (unknown framework, excluded technical routes, unresolved components) are part of the coverage picture — carry them into the report.

**QA division of labor:** ship-polished-ui runs the incremental visual QA loop *during* the build, while design-forge AUDIT/TEST runs the complete scored audit *pre-delivery* against the design-intent.

## Reference map

All knowledge is dissected into on-demand files. Load only what the active mode needs (each agent file specifies its subset). The `references/…` and `assets/…` paths below are relative to **this skill directory** (`${CLAUDE_PLUGIN_ROOT}/skills/design-forge/`); the specialist **agent** files live one level up, at `${CLAUDE_PLUGIN_ROOT}/agents/`.

**Shared (every mode):**
- `references/anti-slop-rules.md` — the AI-slop catalog (fingerprints → why → premium alternative → exact prompt vocabulary) and the quick slop-rejection checklist.
- `references/scoring-and-report.md` — severity legend, scoring methodology, report structure, JSON schema, and the anatomy of a self-contained correction prompt. **The output contract for AUDIT and TEST.**
- `references/design-vocabulary.md` — design term → CSS property → plain-language phrasing glossary.
- `references/design-system-reference.md` — concrete reference values (Apple HIG, Material 3, Vercel/Geist, Linear, Stripe, Tailwind), motion standards, dark-mode standards, responsive viewport matrix.

**AUDIT (reads the four shared files plus):**
- `references/defect-taxonomy.md` — the visual + UX defect checklist.
- `references/analysis-protocol.md` — how to analyze screenshots and video.
- `references/edge-cases.md` — implementation/edge-case defects (content resilience, font loading, CLS, cross-browser, HiDPI, overflow, z-index, overlays, cursor, i18n, CSS anti-patterns, semantic HTML, performance-visible).

**TEST (reads everything AUDIT reads, plus):**
- `references/testing-protocol.md` — the 10-phase hands-on test sequence and per-area protocols.
- `references/environment-adaptation.md` — per-platform capability matrix (Claude Desktop, Codex, Antigravity) and fallbacks.
- `references/automated-tools.md` — copy-paste CLI tools (Lighthouse, axe/pa11y, Wallace, odiff, …) and the regression protocol.

**BRIEF (reads the anti-slop, vocabulary, and design-system shared files, plus):**
- `references/intake-methodology.md` — extracting design intent from a non-designer.
- `references/archetype-library.md` — the 8 design archetypes with prompt phrases.
- `references/spec-language.md` — expressing design in natural language (no code) + premium component vocabulary.
- `references/application-templates.md` — per-category guidance and complete worked brief transformations.
- `references/refinement-and-systems.md` — reference-product anchoring, token bootstrapping, iterative refinement.
- `references/prompt-structure.md` — the 6-part brief ordering, multi-LLM adaptation, and the brief→audit pipeline.

**Assets (output templates, copied/filled — not loaded as knowledge):**
- `assets/audit-report-template.md` — blank report skeleton for AUDIT/TEST.
- `assets/design-intent-template.md` — blank design-intent skeleton for BRIEF (and the pipeline handoff).

## Environment note

Claude Code is the primary environment. **AUDIT** and **BRIEF** work anywhere. **TEST** depends on host computer-use capabilities and adapts per platform (Claude Desktop, OpenAI Codex, Google Antigravity) — always read `references/environment-adaptation.md` first in test mode, run the nearest substitute for anything the platform cannot do, and state the gap plus a manual-verification recommendation in the report. No environment has a real screen reader: inspect the accessibility tree and recommend manual VoiceOver/NVDA verification rather than claiming screen-reader output.

## Operating principles

- **Prioritize by impact.** Lead every report with the ~20% of fixes that resolve ~80% of the perceived-quality loss.
- **Every correction prompt stands alone.** A user must be able to copy one prompt into a development LLM with zero additional context. Never reference "the issue above".
- **Reject AI slop.** Push toward intentional, distinctive, premium design — never the generic LLM-default aesthetic.
- **Be quantitative.** Cite exact values, tokens, and standards; flag where a standard is qualitative or a reverse-engineered value may drift.
