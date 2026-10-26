---
name: rite-spec
description: Specify new, vague, or high-risk behavior before code. Use for features, auth, migrations, or public API changes; not for planning an approved spec.
argument-hint: "<feature or idea>"
user-invocable: true
---

<!-- loads: {"always":["devrites-lib/reference/standards/core.md","devrites-lib/reference/standards/code-navigation.md","devrites-lib/reference/standards/code-index.md","devrites-lib/reference/standards/elicitation.md","devrites-lib/reference/standards/agents.md","rite-spec/reference/investigation.md","rite-spec/reference/question-protocol.md","rite-spec/reference/spec-template.md","rite-spec/reference/spec-checklists.md","rite-spec/reference/state-workspace.md","rite-spec/reference/acceptance-criteria.md","rite-spec/reference/interview-patterns.md","rite-spec/reference/ai-spec-template.md","rite-spec/reference/anti-patterns.md"],"triggers":{"afk":["devrites-lib/reference/standards/afk-hitl.md"],"applicability":["devrites-lib/reference/standards/repository-topology.md","devrites-lib/reference/standards/data-integrity.md","devrites-lib/reference/standards/integration-reliability.md"],"documentation":["devrites-lib/reference/standards/documentation.md"],"edge-cases":["devrites-lib/reference/standards/edge-case-trace.md"],"frontend":["rite-build/reference/frontend-trigger.md"],"grammar":["devrites-lib/reference/standards/spec-grammar.md"],"principles":["devrites-lib/reference/standards/principles.md"],"references":["rite-spec/reference/references-intake.md"]},"workspace":["brief.md","spec.md","state.md","decisions.md","assumptions.md","questions.md"],"workspaceByRole":{"evidence-scout":["brief.md","spec.md","state.md","questions.md"]},"rootOnly":["devrites-lib/reference/standards/code-index.md","devrites-lib/reference/standards/afk-hitl.md"]} -->
> Read-set manifest: `devrites-engine context --skills-root .omp/skills <slug> --phase spec` bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.


# /rite-spec: investigate and write the spec

Investigate and resolve material gaps into a placed, covered `spec.md`.
`/rite-clarify` audits topology next. Write no plan, task, or code here.

> Use `/rite-quick` for a typo, copy/config edit, or one-function fix. It returns
> here for auth, data, migration, public API, or multi-slice work.

## Rules consulted (read on demand from `.omp/skills/devrites-lib/reference/standards/`)
Pull [`documentation.md`](skill://devrites-lib/reference/standards/documentation.md) for significant decisions and [`principles.md`](skill://devrites-lib/reference/standards/principles.md) for
declared invariants; an unavoidable principle violation is blocking.
For behavioral/high-risk acceptance, use [`spec-grammar.md`](skill://devrites-lib/reference/standards/spec-grammar.md) plus workspace schema;
simple criteria stay flat `AC-###`. Apply
[`acceptance-criteria.md`](reference/acceptance-criteria.md) so each is binary and observable.
Use [`edge-case-trace.md`](skill://devrites-lib/reference/standards/edge-case-trace.md)
to populate only relevant edge/prohibition rows (trigger `edge-cases`). The spec's applicability map routes
topology, data, integration, security, and delivery concerns to their focused standard;
load a routed standard to discover required behavior, not to prescribe implementation.

## Operating rules (DevRites core)
- No silent assumptions or guessing; prefer conventions; ask on scope,
  placement, data, UX, security, migration, or acceptance changes.
- **Root authority:** controlling chat asks humans, decides, and writes workspace;
  evidence work follows [`agents.md`](skill://devrites-lib/reference/standards/agents.md).
- **Author one section at a time:** problem → goal → requirements → acceptance →
  edges. For contested requirements/boundaries/assumptions, apply
  [`elicitation.md`](skill://devrites-lib/reference/standards/elicitation.md) before continuing.

## Workflow
0. Read core; if `.devrites/ACTIVE` exists, require its `state.md`.
0a. **Adoption check.** For a never-adopted existing codebase, route first to
   `/rite-adopt` with `$ARGUMENTS`; it derives baseline spec/principles. HITL
   offers ranked adopt-first and spec-only choices; permitted AFK adopts.
   Silently skip greenfield/onboarded projects, and never block solely on absence:
   ```bash
   if [ ! -d .devrites/archive ] \
      && [ -z "$(ls .devrites/work 2>/dev/null)" ] \
      && [ -n "$(git ls-files 2>/dev/null | grep -vE '^\.(devrites|claude)/' | head -1)" ]; then
     echo "brownfield, not yet adopted → recommend /rite-adopt first (carry this idea as its next objective)"
   else echo "greenfield or already onboarded → continue spec"; fi
   ```
1. **Understand the request** (`$ARGUMENTS`). State outcome and underlying
   problem in one sentence. List each distinct explicit ask under `brief.md` `## Asks`,
   quoted from the user's own words or a cited issue/PRD, never the invocation (`spec this`).
   Readiness maps every ask to REQ/AC, a reasoned Non-goal, or a blocking question; an ask
   with two readings that change acceptance is a question, never a silent pick.
   **Completion:** it includes both, and every ask is listed. **Failing case:** "CSV export
   and an email digest" yields a CSV-only spec; the digest is neither Non-goal nor question.
1a. **Dedupe.** Search local issues/PRDs, work, and archive. On a close match ask
   extend/adopt/new, then record the choice; otherwise continue silently. A slug handed
   off by `/rite-adopt` extends that adopted workspace without asking. Adopting a
   pressure-test provisional slug turns each `Hold:` in its `investigation-map.md` into an
   open `gate: blocking` question in `questions.md`.
   A recorded [feature-sequence continuation](skill://rite-plan/reference/slicing.md#continuation-workspaces)
   is a **new** workspace (`<parent>-2`): carry the parent slug and position into
   `brief.md`, read the parent artifacts as design input, and do not route to
   `/rite-plan revise` on the parent. When the ask is open and archived work records
   an unfinished sequence, propose that next continuation (slug + objective) as the
   recommended option instead of a fresh slug.
2. **Investigate:** follow [investigation](reference/investigation.md) through its
   complete findings and done-when gate. Resolve the project's **test /
   build/typecheck/lint** commands with `devrites-engine detect commands`
   (Makefile → package.json → language manifests; read-only) and record the
   resolved text — an `unresolved` slot means the plan must name the concrete
   command later, never an invented one. Discover frontend/backend systems, and declared project guidance
   (`PRODUCT.md`, `DESIGN.md`, `CLAUDE.md`, `AGENTS.md`, and `.devrites/principles.md` when
   present).
   **Consult the capability ledger**, which records current system behavior
   ([`ledger.md`](skill://rite-polish/reference/ledger.md)); Polish folds accepted deltas
   before Review. List `.devrites/specs/*/spec.md` with the
   host filesystem and read only capabilities this feature touches. Search accepted ADRs and
   relevant `.devrites/**/decisions.md` files directly before asking the human to revisit a
   settled architecture, API, or auth choice. Compare exact requirement headers and meanings
   with the current ledger to choose ADDED/MODIFIED/REMOVED; never classify from memory. Use
   [`spec-grammar.md`](skill://devrites-lib/reference/standards/spec-grammar.md)'s singular `Capability impact:` declaration to name the affected
   capabilities and change, or give its specific `none` justification.
   Inventory affected observable behavior from current test/contract/runtime/source
   evidence; map each outcome to preserving REQ/AC. Greenfield `none` needs the
   template's specific justification.
   Identify proof constraints now: human-only credentials, unavailable environments, approval
   windows, or acceptance not observable through existing test/runtime/browser surfaces.
   An unfamiliar framework/version routes to `devrites-source-driven`; missing or
   contradictory documentation is evidence to reconcile, never a license to guess.
   Split independent placement, blast-radius, and external-fact questions into at most three
   bounded `devrites-evidence-scout` tasks on one frozen candidate. Wait for and reconcile every
   cited dossier before step 4. The scout supplies facts only; it never asks the human or writes
   the spec.
3. **Gather design references when provided:** [references-intake](reference/references-intake.md).
   The human may attach screenshots, mockups, a Figma link, a video, links, or nothing.
   Skip this step when none are provided. Otherwise, **view or fetch**
   them, **save local files** into `.devrites/work/<slug>/references/`, and index them in
   `references.md` as target, constraint, or inspiration. Later phases honor that role
   rather than treating every reference as a fidelity target.
   **Completion:** every supplied reference is saved and classified, or absence is explicit.
3a. **Shape UX/UI before code when the feature is frontend**
   ([frontend-trigger](skill://rite-build/reference/frontend-trigger.md)). Apply
   `devrites-ux-shape` within the spec phase. It turns the
   references and spec into a feature-level **`design-brief.md`** (design direction, key
   states, interaction model, optional Figma/image visual-direction probe) that `/rite-build`
   targets for the build. In HITL it pauses for the human to
   confirm the direction; in AFK it asserts the best guess and logs it. Pure
   backend/data/CLI features skip this.
4. **Resolve human-owned gaps.** Recommend an option and let the human decide. Apply
   [question-protocol](reference/question-protocol.md), the shared
   [[`afk-hitl.md`](skill://devrites-lib/reference/standards/afk-hitl.md) option-set and decision-ownership rules](skill://devrites-lib/reference/standards/afk-hitl.md#decision-ownership-search-before-asking),
   and [`interview-patterns.md`](reference/interview-patterns.md) for a vague ask. Every
   material dimension is resolved by a human pick or explicitly deferred as non-blocking;
   only genuinely reversible, low-impact details go to `assumptions.md`. A paper-only
   uncertainty may take one scoped `/rite-prototype` detour. A declared-principle conflict
   remains blocking until the human approves a recorded, scoped exception.
4a. **Build-interruption forecast.** Search first, then list and close foreseeable human needs:
   product/acceptance ambiguity, irreversible/external approval, or human-only access. Record
   owned prerequisites. Keep a build checkpoint only for unavailable pre-code evidence or a
   mandatory action-time approval. **Completion:** no foreseeable human choice is deferred.
5. **Create or update the workspace** + set `.devrites/ACTIVE` from
   [state-workspace](reference/state-workspace.md); a `--lookahead` run
   leaves `.devrites/ACTIVE` unchanged. If the slug already exists,
   update the existing workspace rather than overwrite it; preserve history and
   unrelated settled content. Write every required artifact and conditional
   annex exactly from [spec-template](reference/spec-template.md)
   ([ai-spec-template](reference/ai-spec-template.md)), including its
   capability impact, existing-behavior preservation, grammar/delta,
   stakeholder/constraint/invariant, failure/recovery, applicability, coverage-seed,
   qualified backstop, edge/prohibition, UI, and AI rules. Native
   hierarchical instructions remain stable; do not rewrite `AGENTS.md` or
   `CLAUDE.md` for the active workspace.
5a. **Check the spec prose** with [spec-checklists](reference/spec-checklists.md).
   Emit every applicable domain checklist and fix each CRITICAL by correcting the spec,
   never by softening the question.
6. **Run the complete readiness gate** at the bottom of
   [spec-template](reference/spec-template.md), then apply the
   **Native grammar re-read checklist** in [`spec-grammar.md`](skill://devrites-lib/reference/standards/spec-grammar.md) to the complete
   saved `spec.md`. Re-open the file after corrections and verify every
   applicable item; there is no parser or replacement script. Natively compare
   deltas with the current ledger using exact header semantics and the ledger's
   complete-block preservation rule.
   `tasks.md` deliberately does not exist yet; cross-artifact traceability starts in
   `/rite-define`. Any grammar or delta failure blocks. The interruption forecast must be resolved, owned, or a justified
   action-time gate. Run the [`spec-grammar.md`](skill://devrites-lib/reference/standards/spec-grammar.md) marker sweep; a kept hit blocks. Then record
   `passed <iso>; marker sweep: …` in the `state.md` `spec_gate` row, never in `spec.md`.
6a. **Existing-spec delta.** For a pre-existing slug/workspace, compare old/new
   spec and questions, then show `Acceptance delta` (added/removed/reworded IDs)
   and `Open-question delta` (opened/resolved/reworded IDs), using `none` for
   empty categories. Show before proceeding; new workspaces skip.
6b. **Review-before-code digest.** Before planning, render the compact human review:
   `Intent` (one sentence), `Done means` (top acceptance/scenario IDs), `Scope/risk` (what is in/out
   plus the hard gates), `Assumed:` (each `assumptions.md` id, one line, or `none`), and
   `Build exactly this?` (yes → next phase; no → revise now). A "no" on one `Assumed:` line
   reopens only that line as a human decision under step 4. The digest
   is a view over `spec.md` and `assumptions.md`, not a new artifact. **Stop** after the digest.

> **Mid-flight discipline.** Do not skip investigation, gap resolution, or placement
> decisions. See [`anti-patterns`](reference/anti-patterns.md).

## Output

When the ask overlaps the ACTIVE feature (same intent, >50% scope), route to
`/rite-plan revise` (its gate decides) rather than minting a parallel workspace.
