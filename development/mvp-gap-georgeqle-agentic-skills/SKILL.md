---
name: mvp-gap
description: Evaluate codebase against ICP to identify gaps blocking first sales and retention
type: research
version: v0.10
required_conventions: [alignment-page]
argument-hint: "[optional: path-to-icp-spec]"
context_intake: artifact_only
visual_tier: visual
---

## Pack Availability Guard

When recommending a skill from another pack, verify the target pack is installed via `.agents/project.json` `enabled_packs`. If it is not enabled, recommend `npx skillpacks install <pack>` from the project shell. After install, tell Claude users to run `/reload-skills`, then `/clear` or restart if the skill remains invisible. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# MVP Gap — Startup Readiness Audit

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the proposed scope, available source categories, known context, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, spec, or task files in Stage 1.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run required source/code checks, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. Raw evidence or search logs may remain as supporting evidence where this skill already requires them, but synthesized deliverables stay in the working packet. Update the `review` HTML alignment page so it renders the complete working-packet substance as structured HTML review UI: purpose-built sections, tables, matrices, gates, cards, and tier-appropriate charts or diagrams that preserve every packet section, finding, caveat, and decision detail without summary loss. Raw Markdown packet text may appear only as a supplemental source view after the rendered review UI; do not make a `Full Preliminary Packet` or `Full Working Packet` raw Markdown dump, giant `<pre><code>` block, link-only view, or source-only view the primary review surface. Include the evidence matrix, assumptions/confidence register, source coverage gaps, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, or source-backed claims: verify against available evidence. If the user appears to misunderstand the evidence or states something factually incorrect, push back clearly and cite the evidence. Do not rewrite findings merely to agree.
- For taste, brand, positioning preference, risk appetite, prioritization, or other subjective judgment calls: weigh user feedback heavily and adapt the recommendation unless it conflicts with verified evidence.
- When feedback mixes facts and preference, separate them explicitly: correct the factual part, then incorporate the preference where it is a legitimate judgment call.
- When uncertain, say what is known, what is inferred, and what would change the conclusion.

## Prerequisites

`research/icp.md` (or `research/{slug}/icp.md`) must exist. If it doesn't, tell the user to run `/customer-discovery` first and stop.

## Process

### 0. Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint. Suggest creating a missing `research/{slug}/` product path when code clearly exposes an app, but do not require code or monorepo detection before using `research/{slug}/`.

When product path `{slug}` is active, read and write research under `research/{slug}/`, specs under `specs/{slug}/`, and treat top-level `research/*.md` files as flat-mode documents or cross-path summaries.

### 1. Load Context

- Read `research/icp.md` (or `research/{slug}/icp.md`) — customer profile, user profile(s), current-state journey, pain map, current alternatives, stated value drivers
- Read `research/enterprise-icp.md` (or `research/{slug}/enterprise-icp.md`) if it exists (for awareness, not primary evaluation)
- Read `research/metrics.md` (or `research/{slug}/metrics.md`) if it exists — check if defined metrics can actually be measured (instrumentation gaps are MVP gaps)
- Read CLAUDE.md, README, package config for project conventions
- Read existing specs from `specs/` (or `specs/{slug}/`) for planned but unbuilt features
- Read `tasks/roadmap.md`, `tasks/todo.md`, `tasks/manual-todo.md`, `tasks/record-todo.md`, and `tasks/recurring-todo.md` if they exist for work in progress or advisory records

### 2. Analyse the Codebase

Read source files, routes, components, data models, auth setup, config, dependencies, and infrastructure files. Build a picture of what the product actually does today.

### 3. Evaluate Against ICP

#### User Journey Coverage
For each step in the current-state journey from `research/icp.md`:
- Can the product replace or improve this step?
- Where does the UX break down, require workarounds, or not exist?
- Does the interaction model match the user's technical sophistication?

If `research/journey-map.md` (or `research/{slug}/journey-map.md`) exists, map each gap to its **journey stage** (e.g., Discovery, Onboarding, Aha Moment, Habit Loop, Expansion). This enables downstream skills to understand *where* in the experience each gap bites.

#### Customer Journey Coverage
- **Discovery**: Is there a landing page, marketing site, or clear product description?
- **Evaluation**: Can someone try the product? Free tier, trial, demo?
- **Purchase**: Is there billing, pricing, a checkout flow?
- **Provisioning**: Can the customer set up the product for their users? Invite flow, admin panel?
- **Onboarding**: Does a new user have a clear path to the "aha moment" from the ICP?

#### Table-Stakes Gaps
- Authentication and authorization
- Error handling and user-facing error messages
- Data export and portability
- Responsive design and accessibility basics
- Help, documentation, or in-app guidance
- Email notifications or transactional messaging
- Settings and user preferences

#### Integration Gaps
- Does the ICP's current-state journey reveal tools they already use?
- Which integrations are required vs. nice-to-have for replacing the current workflow?

#### Competitive Differentiation
- Does the product deliver the stated value drivers from `research/icp.md`?
- Where does it fall short of the claimed wedge?
- Would the ICP actually switch from their current alternative to this?

#### Spec Validation
For each gap identified above, check if a spec already exists in `specs/` (or `specs/{slug}/`):
- If a spec covers the gap **fully**, mark the gap as "Spec exists — ready to build" and link the spec file.
- If a spec covers the gap **partially**, mark it as "Spec exists — needs expansion" and suggest `/user-flow-map [topic]` when flow/design shape is missing, or `/ux-variations --layout-mode [topic]` when flow and UI requirements already exist but layout alternatives are missing.
- If no spec exists, suggest `/user-flow-map [topic]` to map flow/design shape before UI requirements, layout variants, and production speccing.

#### Metrics Tie-In
If `research/metrics.md` (or `research/{slug}/metrics.md`) exists, identify for each gap:
- Which metric(s) will indicate this gap is closed (e.g., activation rate, retention at day-7)
- If no metric exists to measure gap closure, flag it as an **instrumentation gap** — this becomes an additional item under the gap.

### 4. Prioritise

Tag each gap with one of:
- **`blocks-first-sale`** — Without this, no rational customer would pay. Deal-killer.
- **`blocks-retention`** — Customer might try it, but won't stay without this.
- **`nice-to-have`** — Adds value but not a deciding factor for early customers.

Order gaps within each priority tier by estimated effort (S/M/L).

#### GTM Alignment
If `research/gtm.md` (or `research/{slug}/gtm.md`) exists:
- Cross-reference the build sequence against GTM launch gates and timeline
- Flag conflicts where a high-effort gap blocks a near-term GTM milestone
- Surface gaps that can be deferred to post-launch without losing the GTM window

### 5. Populate Next Steps

Before writing, check which files exist to populate the `## Next Steps` section contextually. Include a **Recommended** item and 2–4 other applicable options. Choose the recommendation by the first matching condition:

- IF downstream impact is **Major**: `/reconcile-research` — audit and fix affected downstream research documents.
- IF a `blocks-first-sale` gap lacks flow/design shape or a full spec: `/user-flow-map [top gap]` — map the highest-priority gap into concrete screen flow, decisions, branches, states, and recovery paths before UI/layout planning.
- IF any other gap lacks flow/design shape or a full spec: `/user-flow-map [top gap]` — map the highest-priority unspecced gap from `research/mvp-gap.md` before UI/layout planning.
- IF required context is missing: the corresponding research skill (`/journey-map`, `/competitive-analysis`, `/metrics`, or `/brainstorm` when creative alternatives could reduce high-effort gaps).
- OTHERWISE: `/roadmap` — sequence the existing specs into implementation phases.

Only recommend `/roadmap` as the primary next step when the MVP gap analysis found no unspecced priority gaps.
If downstream impact has not been classified yet, run the downstream impact check before finalizing `## Next Steps`.

### 6. Downstream Impact Check

Before finalizing the output, check for downstream research documents that may be affected by what was just decided. Only check documents that exist on disk.

**Downstream documents to check** (use `{slug}/` prefix when product-path scope is active):
- `research/journey-map.md`
- `research/metrics.md`
- `research/gtm.md`
- `research/monetization.md`
- `tasks/roadmap.md`

For each existing downstream document:
1. Read it — focus on `> Based on:` header, `## Summary`, and sections that reference concepts this skill just defined or changed
2. Identify **specific conflicts**: claims, assumptions, or references that contradict what was just decided. Examples:
   - Journey stages that assume features exist which are now identified as gaps
   - Metric targets anchored to capabilities the product doesn't have yet
   - GTM launch plan that depends on features flagged as missing
   - Monetization pricing tied to features identified as gaps
   - Roadmap phases that don't account for newly identified first-sale blockers
3. Note each conflict: downstream file, section, the stale claim (quote it), and what it should now say

**Classify the impact**:
- **None**: No downstream documents exist, or no conflicts found. Skip display entirely.
- **Minor** (1–2 small conflicts): Display conflicts to user inline.
- **Major** (3+ conflicts OR a foundational gap was identified that changes the build sequence — e.g., a new first-sale blocker, a key assumption invalidated): Display conflicts and strongly recommend `/reconcile-research`.

Display to the user with the written file confirmation.

## Output

### `research/mvp-gap.md` (or `research/{slug}/mvp-gap.md`)

```markdown
# MVP Gap Analysis

> Evaluated against: research/icp.md (or research/{slug}/icp.md)
> Date: [current date]
> Codebase state: [brief summary of what exists]

## Summary
[2-3 sentences: overall readiness assessment and the most critical gaps]

## Blocks First Sale
- **[Gap title]** — [What's missing and why it matters to the ICP]. Effort: S/M/L
  _Journey stage:_ [stage from journey-map, or "N/A" if no journey-map exists]
  _Closure metric:_ [metric from metrics.md, or "⚠ No metric defined" if none]
  _Spec:_ [link to spec if exists + status, or `/user-flow-map [topic]` if no spec]
- ...

## Blocks Retention
- **[Gap title]** — [What's missing and why it matters]. Effort: S/M/L
  _Journey stage:_ [stage]
  _Closure metric:_ [metric or "⚠ No metric defined"]
  _Spec:_ [spec link/status or `/user-flow-map [topic]`]
- ...

## Nice to Have
- **[Gap title]** — [What's missing and why it matters]. Effort: S/M/L
  _Journey stage:_ [stage]
  _Closure metric:_ [metric or "⚠ No metric defined"]
  _Spec:_ [spec link/status or `/user-flow-map [topic]`]
- ...

## Recommended Build Sequence
[Ordered list of gaps to address, combining priority and dependency logic.
 First sale blockers first, then retention blockers, then nice-to-haves.
 Within each tier, order by dependency — what must exist before other things can be built.
 If GTM exists: note conflicts between build order and GTM launch gates.]

## Downstream Impact
[Only if conflicts found in step 6 — list each conflict with file, section, stale claim, and correction needed. If Major, recommend `/reconcile-research`.]

## Next Steps

**Recommended:** [first matching command from step 5] — [reason grounded in this analysis]

Other options:
- [conditional items from step 5 — only include items whose conditions are met]
```

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **Do not make code changes.** Analysis only.
- **Every gap must cite evidence** — a missing route, missing component, absent dependency, no billing integration, etc. No vague claims.
- **Prioritise by market impact**, not technical interest. Things that block the first sale come before things that block the 10th.
- **If no code exists yet**, report that clearly and suggest running `/user-flow-map` to map flow/design shape first. Do not fabricate gaps for a nonexistent codebase.
- **Include `/user-flow-map` prompts** for gaps lacking flow/design shape or full specs. Use `/ux-variations --layout-mode` only when flow and UI requirements already exist but layout alternatives are missing.
- **Do not duplicate work already tracked** in `tasks/roadmap.md`, `tasks/todo.md`, `tasks/manual-todo.md`, `tasks/record-todo.md`, or `tasks/recurring-todo.md` — note it as "in progress" or "advisory" instead.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/mvp-gap-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
