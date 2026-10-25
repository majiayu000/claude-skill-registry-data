---
name: saas-design-review
description: "Reviews one design document for completeness, internal consistency, implementability, and design standards. Before handing to programmers."
argument-hint: "[path-to-design-doc] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Agent, AskUserQuestion, Bash(bash "*/.claude/skills/saas-design-review/../../hooks/yaml-helper.sh" resolve_config *), Bash(bash .claude/scripts/review-receipts.sh check *), Bash(bash .claude/scripts/review-receipts.sh hash *), Bash(bash .claude/scripts/prd-structure-check.sh *), Bash(grep -E '^  - name:' design/registry/entities.yaml), Bash(grep -n -i -E *)
model: sonnet
---

!`bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" resolve_config --keys locale,review_mode,automation,workflow,system_overrides`

Resolved above — use as-is; `--review` overrides `review_mode`. `--depth` is
the pre-1.1 name for the same flag: treat `--depth <mode>` exactly as
`--review <mode>`, and say once that it was renamed. Given both, `--review`
wins and `--depth` is ignored — say so. No block → defaults in
`.claude/docs/config-resolution.md`.

# Design Review

> **Interaction Localization Rule**:
> When `locale: pt-BR` (or user speaks Portuguese), ALL questions (`AskUserQuestion` / `ask_question`), confirmation prompts, and selectable options MUST be translated and presented in **Brazilian Portuguese (PT-BR)**.
> Any English question text or options in this skill are illustrative examples — NEVER display English questions or options to a Portuguese developer.
> Internal reasoning, code synthesis, tests, and documentation files MUST remain in English.


## Phase 0: Parse Arguments


See `.claude/docs/director-gates.md` for the full check pattern. Individual gate definitions live in `.claude/docs/director-gates/[gate-id].md` — the spawned agent reads its own gate file; do not read it in the parent session.


Every `AskUserQuestion` call follows `.claude/docs/automation-modes.md`
(collaborative asks always · guided major-only · autonomous logs and proceeds;
`automation_always_ask` categories always prompt).

**`workflow`** for the PRD under review — use the `system_overrides` row for `<system>` if the block lists one, else the project value. Validation scope follows the tier:
- `full` — all 8 sections validated; any missing section blocks approval.
- `standard` — the 5 required sections (Overview / Problem Statement, Detailed Rules / Functional Requirements, Edge Cases,
  Dependencies, Acceptance Criteria) block if missing; Data Models / Formulas blocks only when
  the system defines numeric rules or schema (rates, quotas, thresholds, tier pricing — the
  category is a hint, not the test); User Personas and
  Configuration Options are advisory (warn, never block) unless `workflow_overrides`
  require them.
- `minimal` — no PRD is expected; if one exists, validate the 5 standard
  sections advisorily.

Resolved mode controls how thorough this review is:

- **`full`**: Complete review — all phases + specialist agent delegation (Phase 3b)
- **`lean`**: All phases, no specialist agents — faster, single-session analysis
- **`solo`**: Phases 1-4 only, no delegation, no Phase 5 next-step prompt — use when called from within another skill

---

## Phase 1: Load Documents

**Freshness check first — a re-review of an unchanged document costs full
price and reproduces the same verdict.** Run:

```
Bash: bash .claude/scripts/review-receipts.sh check "design/prd/reviews/[doc-name]-review-log.md" "[target-doc-path]" "design/registry/entities.yaml" ".claude/skills/saas-design-review/SKILL.md"
```

The registry is in the check because this review consults it for
cross-document facts — an unchanged PRD reviewed against a *changed*
registry can reach different conclusions, so the skip is only safe when
**every** line reads `UNCHANGED` (a registry that never existed doesn't
appear in the output and doesn't block the skip). This skill's file is in it
because a changed skill reviews differently. The check also compares every
other file the log stamps — the related PRDs, concept or brief and narrative
files earlier reviews read — and prints `GONE:` for one that no longer exists.

Then read the latest entry's `Review mode:` line. That review **covers** this
run only when its mode is the same as or deeper than the mode resolved now
(`full` > `lean` > `solo`) and its workflow is the same or deeper (`full` >
`standard` > `minimal`). An entry without the line was written before it
existed and covers nothing.

- **All `UNCHANGED`** and the log's latest entry carries a verdict — surface it:
  *"This document is byte-identical to its last review on [date] ([mode]
  review, verdict: [verdict])."* If that verdict was APPROVED and that review
  covers this run, offer via `AskUserQuestion`:
  `[A] Use the prior verdict (Recommended)` / `[B] Re-review anyway` —
  `guided` proceeds with [A] and notes it; `autonomous` logs via
  `log_decision` and uses the prior verdict. If it was APPROVED but the
  review asked for now is deeper than the logged one, say so — *"That was a
  [mode] review at workflow [tier]; this run asks for [mode] at [tier]."* —
  and offer `[A] Re-review at [mode] (Recommended)` / `[B] Use the prior
  [mode] verdict`; `guided` and `autonomous` re-review (`autonomous` logs it
  via `log_decision`). If it was NEEDS REVISION or
  MAJOR REVISION NEEDED, say so plainly: the document has not changed since
  it failed review — the prior findings stand; revising the document is the
  next step, not re-reviewing it. Offer to display the prior findings from
  the log.
- **The target doc and this skill's file `UNCHANGED`, and only the registry or
  another stamped cross-document file `CHANGED`, `NEW` or `GONE`** — the prior
  verdict stands except for cross-document facts: re-verify the doc's values
  against the changed files and re-issue the verdict; escalate to a full
  re-review if a conflict appears or that review does not cover this run.
- **Target doc or this skill's file `CHANGED` or `NEW`, or `RECEIPT: NONE`** —
  proceed with the full review below. **Do not offer a partial/delta re-review that skips
  reading or re-analyzing unchanged sections.** A section-scoped re-review
  misses defects a full review finds, and saves little or nothing.
  "Unchanged since last review" only means
  byte-identical to what was reviewed then — it says nothing about whether
  that prior pass was itself complete, and attention narrows to the flagged
  change even under an instruction to scan everything anyway.

Read the target design document in full. This step needs the whole PRD: read it by section: if `.basinfy/` exists, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise read it in ranges by its headings (found with the Grep tool: pattern `^#`, content mode), since a whole-file Read over 40 KB is refused. Read CLAUDE.md to understand project context and standards.

**For cross-document facts, prefer the registry over sibling PRDs.** If
`design/registry/entities.yaml` exists **and lists entries for this system**,
grep it — these are the established facts this PRD must not contradict, and they
replace reading sibling PRDs to rediscover them:
```
Grep pattern="source: design/prd/[system].md" path="design/registry/entities.yaml" output_mode="content" -A 6
Grep pattern="design/prd/[system].md" path="design/registry/entities.yaml" output_mode="content" -B 8
```
The first finds entries this system **owns** — the `-A 6` context includes their
`referenced_by:` block. The second finds entries that **reference** this system —
`referenced_by:` is a block sequence (the key and its paths are on separate
lines), so match the path with `-B 8` context to see the owning entry, not a
`referenced_by.*name` one-liner (which never matches the block form).

**If `design/registry/entities.yaml` does not exist, or lists no entry for this
system** — the file ships as an empty stub, so this is the default until
`/saas-design-system` has populated it — fall back to reading the related PRDs the
target doc names in its Dependencies section. Bound the read to those, not to
everything "implied". Do not glob-read all of `design/prd/`.

**Dependency graph validation:** For every system listed in the Dependencies section, use Glob to check whether its PRD file exists in `design/prd/`. Flag any that don't exist yet — these are broken references that downstream authors will hit.

**Product positioning & domain alignment:** If `design/prd/product-concept.md` (or, at `rigor: minimal`, the one-page brief `design/product-brief.md`) exists, read it. Note any functional choices in this PRD that contradict established product scope, tone, or design pillars. Pass this context to `lead-product-manager` in Phase 3b.

**Prior review check:** Check whether `design/prd/reviews/[doc-name]-review-log.md` exists. If it does, read the most recent entry — note what verdict was given and what blocking items were listed. This session is a re-review; track whether prior items were addressed.

---

## Phase 2: Completeness Check

**Step 2a — gather section presence deterministically (no document read):**

```
Bash: bash .claude/scripts/prd-structure-check.sh [target-doc-path]
```

It prints a `PRESENT:` list and, when applicable, an `ABSENT:` list and a
`PLACEHOLDER:` list (present sections holding only `[To be designed]`: not yet
written, so treat them as missing for the checklist). It reports
**presence only** and makes no REQUIRED/ADVISORY judgment — that is Step 2b's
job. It already accepts `## Detailed Design` as satisfying the `Detailed Rules`
requirement, so do not flag that as missing.

**Step 2b — apply the tier.** Using the Step 2a lists, evaluate against the
Design Document Standard checklist below. **Mark each section REQUIRED or
ADVISORY per the resolved workflow tier (Phase 0).** A missing REQUIRED section
blocks approval; a missing ADVISORY section is surfaced as a recommendation but
does not block.

A section reported PRESENT can still fail review if it is an empty heading —
spot-read any section the verdict actually turns on.

- [ ] Has Overview / Problem Statement section (one-paragraph summary) — REQUIRED at all tiers
- [ ] Has User Personas & Workflows section (target users and core use cases) — REQUIRED at `full`; ADVISORY at `standard`
- [ ] Has Detailed Rules / Functional Requirements section (unambiguous specifications) — REQUIRED at `full`/`standard`. The PRD template titles this section `## Detailed Design` or `## Requirements Pool` (it carries Core Rules / States / Functional specs); accept either heading as satisfying this requirement.
- [ ] Has Business Rules & Formulas section (all math, pricing, or quota rules defined) — REQUIRED at `full`; at `standard` REQUIRED whenever the system defines numeric rules (rates, quotas, thresholds, tier costs), else ADVISORY.
- [ ] Has Edge Cases section (unusual situations handled) — REQUIRED at `full`/`standard`
- [ ] Has Dependencies section (other systems and external APIs listed) — REQUIRED at `full`/`standard`
- [ ] Has Configuration & Parameters section (configurable values, feature flags identified) — REQUIRED at `full`; ADVISORY at `standard` unless `workflow_overrides.tuning_knobs` or `configuration_parameters`
- [ ] Has Acceptance Criteria section (testable success conditions) — REQUIRED at `full`/`standard`

---

## Phase 3: Consistency and Implementability

**Internal consistency:**
- Do the formulas produce values that match the described behavior?
- Do edge cases contradict the main rules?
- Are dependencies bidirectional (does the other system know about this one)?

**Implementability:**
- Are the rules precise enough for a programmer to implement without guessing?
- Are there any "hand-wave" sections where details are missing?
- Are performance implications considered?
- Is every acceptance criterion independently testable? Flag each one that is
  not, quoting it — "feels balanced", "works correctly", "performs well" are not
  criteria — with a measurable rewrite. In `full` mode `qa-lead` also checks them
  (Phase 3b); in `lean` and `solo` no specialist runs, so this main-review check
  is the only one.

**Cross-system consistency:**
- Does this conflict with any existing workflow or feature?
- Does this create unintended interactions with other systems?
- Is this consistent with the application's established tone and pillars?

**Registry values, wherever the PRD states them.** A value restated in a table,
a catalogue entry or a variant note contradicts the registry as surely as one in
Detailed Rules, and reading by section makes those bodies easy to skim. List the
registry's entry names (`grep -E '^  - name:' design/registry/entities.yaml`),
then search the whole target document once for all of them plus the numeric
keys they carry, case-insensitive, writing each `_` as `[_ ]` so `goblin_scout`
also matches "Goblin scouts":

```
grep -n -i -E 'workspace[_ ]slug|billing[_ ]plan|user[_ ]role' [target-doc-path]
```

Check every line it prints against the registry, whatever section it sits in.
A line that gives an entry a different value, even for one room, variant, level
or exception, contradicts the owning PRD: list it under Required Before
Implementation with its line number, this document's value and the registry's.
With no registry entries, run the same search for the entities and values the
related PRDs define.

---

## Phase 3b: Adversarial Specialist Review (full mode only)

**Skip this phase in `lean` or `solo` mode.**

**This phase is MANDATORY in full mode.** Do not skip it.

**Before spawning any agents**, print this notice:
> "Full review: spawning specialist agents in parallel. This typically takes 8–15 minutes. Use `--review lean` for faster single-session analysis."

### Step 1 — Identify all domains the PRD touches

Using the PRD **already loaded in Phase 1** — do not re-read it — identify every domain present. A PRD can touch multiple domains simultaneously — be thorough. Common signals:

| If the PRD contains... | Spawn these agents |
|------------------------|-------------------|
| Pricing models, billing plans, discounts, usage economics | `billing-engineer` |
| Billing quotas, subscription tiers, usage limits | `lead-product-manager`, `database-architect` |
| LLM integrations, embeddings, semantic search, prompt chaining | `ai-engineer` |
| User flows, multi-step wizards, onboarding | `user-flow-architect` |
| Subscription tiers, usage quotas, feature gating | `billing-engineer`, `lead-product-manager` |
| UI, App Shell, navigation, user-facing displays | `ux-designer`, `frontend-engineer` |
| UX writing, microcopy, emails, documentation | `ux-content-strategist` |
| UI micro-interactions, responsive states | `ui-motion-designer`, `frontend-engineer` |
| Real-time collaboration, WebSockets, multi-tenant sync | `realtime-websockets-specialist` |
| Marketing funnel, viral loops, technical SEO | `growth-director` |
| Performance, Core Web Vitals, API latency | `web-perf-analyst` |
| Stack-specific patterns or APIs | Primary stack specialist (`<engine>-specialist` from `stack.frontend` — Next.js→`nextjs-specialist`, FastAPI→`fastapi-specialist`, Cloudflare→`cloudflare-specialist`) |
| Acceptance criteria, test coverage | `qa-lead` |
| Data schema, resource structure | `database-architect` |
| Any core business workflow system | `lead-product-manager` (always) |

Spawn `lead-product-manager` for all PRDs that describe core business workflows or user-facing rules.
Spawn `database-architect` for all PRDs that contain data models or system interaction rules.
These are the most common baselines — but not required for pure UI component styling specs or internal dev notes. Use the domain table above to determine which specialists are truly relevant.

### Step 2 — Spawn all relevant specialists in parallel

**CRITICAL: `Agent` in this skill spawns a SUBAGENT — a separate independent Claude session
with its own context window. It is NOT task tracking. Do NOT simulate specialist
perspectives internally. Do NOT reason through domain views yourself. You MUST issue
actual `Agent` calls. A simulated review is not a specialist review.**

Issue all `Agent` calls simultaneously. Do NOT spawn one at a time.

**Prompt each specialist adversarially:**
> "Here is the PRD for [system] and the main review's structural findings so far.
> Your job is NOT to validate this design — your job is to find problems.
> Challenge the design choices from your domain expertise. What is wrong,
> underspecified, likely to cause problems, or missing entirely?
> Be specific and critical. Disagreement with the main review is welcome.
> Read the PRD by section: find the headings: if `.basinfy/` exists, use `basinfy_search` and `basinfy_read`; otherwise use the Grep tool (pattern `^#`,
> content mode) and Read those ranges with offset and limit."

**Additional instructions per agent type:**

- **`lead-product-manager`**: Anchor your review to the Problem Statement and Success Metrics stated in this PRD. Does this design actually solve the core customer problem? Would a user experience the intended value proposition? Flag any rules that serve implementability but undermine the stated value.

- **`database-architect`**: For every formula in the PRD, plug in boundary values (minimum and maximum plausible inputs). Report whether any outputs go degenerate — negative values, division by zero, infinity, or nonsensical results at the extremes.

- **`qa-lead`**: Review every acceptance criterion. Flag any that are not independently testable — phrases like "feels balanced", "works correctly", "performs well" are not ACs. Suggest concrete rewrites for any that fail this test.

### Step 3 — Senior lead review

After all specialists respond, spawn `product-director` as the **senior reviewer**:
- Provide: the PRD, all specialist findings, any disagreements between them
- Ask: "Synthesise these findings. What are the most important issues? Do you agree with the specialists? What is your overall verdict on this design — APPROVED, NEEDS REVISION or MAJOR REVISION NEEDED?"
- The product-director's synthesis becomes the **final verdict** in Phase 4, in this skill's verdict words — never a director-gate word such as READY or REJECT.

### Step 4 — Surface disagreements

If specialists disagree with each other or with the product-director, do NOT silently pick one view. Present the disagreement explicitly in Phase 4 so the user can adjudicate.

Mark every finding with its source: `[lead-product-manager]`, `[billing-engineer]`, `[product-director]` etc.

---

## Phase 4: Output Review

```
## Design Review: [Document Title]
Specialists consulted: [list agents spawned]
Re-review: [Yes — prior verdict was X on YYYY-MM-DD / No — first review]

### Completeness: [X/N sections present, where N is the count REQUIRED at this project's `modes.workflow`]
[List only sections missing that are REQUIRED at this tier. Mark ADVISORY gaps
separately as "advisory at `standard`" — do not list them as missing.]

> **N is not 8 unless `workflow: full`.** The tier table earlier in this skill is
> authoritative: 8 required at `full`, 5 at `standard` (+ Data Models / Formulas when the system
> defines numeric rules), 0 at `minimal`. Do not hardcode `/8` here: reporting a
> `standard` project as "5/8 missing Edge Cases, Security & Permissions, Configuration Parameters"
> warns about sections that project's own configuration says it does not
> need, which trains the reader to ignore the review.

### Dependency Graph
[List each declared dependency and whether its PRD file exists on disk]
- ✓ pricing-tier-data.md — exists
- ✗ billing-system.md — NOT FOUND (file does not exist yet)

### Registry Values
[The whole-document search from Phase 3: the terms searched, how many lines it
printed, and each conflict with its line number. With nothing to search, say so:
"No registry entries or related-PRD values: values not cross-checked."]

### Required Before Implementation
[Numbered list — blocking issues only. Each item tagged with source agent.]

### Recommended Revisions
[Numbered list — important but not blocking. Source-tagged.]

### Specialist Disagreements
[Any cases where agents disagreed with each other or with the main review.
Present both sides — do not silently resolve.]

### Nice-to-Have
[Minor improvements, low priority.]

### Senior Verdict [product-director]
[Product director's synthesis and overall assessment.]

### Scope Signal
Estimate implementation scope based on: dependency count, formula count,
systems touched, and whether new ADRs are required.
- **S** — single system, no formulas, no new ADRs, <3 dependencies
- **M** — moderate complexity, 1-2 formulas, 3-6 dependencies
- **L** — multi-system integration, 3+ formulas, may require new ADR
- **XL** — cross-cutting concern, 5+ dependencies, multiple new ADRs likely
Label clearly: "Rough scope signal: M (delivery-producer should verify before sprint planning)"

### Verdict: [APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED / NOT ASSESSED]

> **`NOT ASSESSED` when the review could not actually be performed.**
> The other three verdicts are all claims about the design's quality, so each one
> asserts that the document was read and judged. Use `NOT ASSESSED` instead when
> the target document is absent, unreadable, or empty of the sections being
> reviewed, or when a document it depends on is missing so the criteria cannot be
> applied. **Name what was unavailable and which skill produces it.**
>
> `APPROVED` is the dangerous default here: a review that could not find its
> input has not approved anything, and this verdict is consumed downstream as a
> sign-off. `NOT ASSESSED` outranks `APPROVED` in any aggregate — it does not
> outrank the two revision verdicts, because a known problem is more actionable
> than an unknown one.
```

This skill is read-only — no files are written during Phase 4.

---

## Phase 5: Next Steps

Use `AskUserQuestion` for ALL closing interactions. Never plain text.

**First widget — what to do next:**

If APPROVED (first-pass, no revision needed), proceed directly to the systems-index widget, review-log widget, then the final closing widget. Do not show a separate "what to do" widget — the final closing widget covers next steps.

If NOT ASSESSED, nothing was reviewed: offer no tracking update and go straight
to the final closing widget, leading with the skill that produces the missing
input (e.g. `/saas-design-system [system]` for a PRD that does not exist).

If NEEDS REVISION or MAJOR REVISION NEEDED, build the options from the findings:
- `[A] Revise the PRD now — address blocking items together`
- `[B] Stop here — revise in a separate session`
- `[C] Accept as-is and move on` — include only when every finding is advisory
  (Required Before Implementation is empty). With any blocking item, offer [A]
  and [B] only.

**If user selects [A] — Revise now:**

Work through all blocking items, asking for design decisions only where you cannot resolve the issue from the PRD and existing docs alone. Group all design-decision questions into a single multi-tab `AskUserQuestion` before making any edits — do not interrupt mid-revision for each blocker individually.

After all revisions are complete, show a summary table (blocker → fix applied) and use `AskUserQuestion` for a **post-revision closing widget**:

- Prompt: "Revisions complete — [N] blockers resolved. What next?"
- Note current context usage: if context is above ~50%, add: "(Recommended: /clear before re-review — this session has used X% context. A full re-review runs 5 agents and needs clean context.)"
- Options:
  - `[A] Re-review in a new session — run /saas-design-review [doc-path] after /clear`
  - `[B] Accept revisions for now — mark In Review in the systems index; a re-review decides Approved`
  - `[C] Move to next system — /saas-design-system [next-system] (#N in design order)`
  - `[D] Stop here`

In collaborative and guided modes, never end the revision flow with plain text —
always close with this widget. In autonomous mode, summarize the outcome and
record via `log_decision`.

**Second widget — tracking records (combined, for APPROVED path):**

When the verdict is APPROVED, use a single `AskUserQuestion` with `multiSelect: true` to batch the two tracking updates:
- Prompt: "Verdict: APPROVED. I can update the tracking records now. Select any you'd like me to complete:"
- Options:
  - `Update features-modules-index.md status to 'Approved' for [system]`
  - `Append approval entry to design/prd/reviews/[doc-name]-review-log.md`

If the review-log option is selected, append the same format as below. Execute both selected actions before showing the final closing widget.

When the verdict is NEEDS REVISION or MAJOR REVISION NEEDED, use separate widgets as before:

Use a second `AskUserQuestion`:
- Prompt: "May I update `design/prd/features-modules-index.md` to mark [system] as [Needs Revision / In Review]?" — `Needs Revision` (that exact string) while the revisions are outstanding, `In Review` once they are applied and await re-review. This prompt never offers `Approved`: a revision verdict is not an approval.
- Options: `[A] Yes — update it` / `[B] No — leave it as-is`

Use a third `AskUserQuestion`:
- Prompt: "May I append this review summary to `design/prd/reviews/[doc-name]-review-log.md`? This creates a revision history so future re-reviews can track what changed."
- Options: `[A] Yes — append to review log` / `[B] No — skip`

If yes, append an entry in this format:
```
## Review — [YYYY-MM-DD] — Verdict: [APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED]
Review mode: [full / lean / solo] · Workflow: [full / standard / minimal]
Scope signal: [S/M/L/XL]
Specialists: [list]
Blocking items: [count] | Recommended: [count]
Summary: [2-3 sentence summary of key findings from product-director verdict]
Prior verdict resolved: [Yes / No / First review]
Findings:
- [BLOCKING] [section]: [one-line finding]
- [RECOMMENDED] [section]: [one-line finding]
[output of: Bash: bash .claude/scripts/review-receipts.sh hash "[target-doc-path]" "design/registry/entities.yaml" ".claude/skills/saas-design-review/SKILL.md" [every other file this review read for cross-document facts: the related PRDs in design/prd/, design/prd/product-concept.md or design/product-brief.md, the design/content/ files] — a file that does not exist prints `not stamped, no such file` and is left out]
```

Findings rules: one line per finding, named by the section it lives in;
write `- none` when the verdict carried no findings. This is documentation
for a human reader of the revision history, not a mechanism the skill reads
back.

The hash line is the receipt Phase 1 reads on the next run to detect a
byte-identical re-review — the one form of skip that's actually safe,
because the input is provably the same, not merely believed to be adequately
covered by a prior pass. Stamp every file the review read: Phase 1's check
compares each stamped file on the next run, whether or not it names it. Always include it, whatever the verdict — an
unchanged document that previously FAILED review is exactly the case where
skipping a redundant re-review saves the most (the prior findings stand
verbatim).

---

**Final closing widget — always show after all file writes complete:**

Once the systems-index and review-log widgets are answered, check project state and show one final `AskUserQuestion`:

Before building options, read:
- `design/prd/features-modules-index.md` — find any system with Status: In Review or Needs Revision (other than the one just reviewed). Read it by section: check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise find the headings: if `.basinfy/` exists, use `basinfy_search` and `basinfy_read`; otherwise use the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Grep tool (pattern `^#`, content mode) and Read those ranges with offset and limit.
- Count `.md` files in `design/prd/` (excluding product-concept.md, features-modules-index.md) to determine if `/saas-review-all-prds` is worth offering (≥2 PRDs)
- Find the next system with Status: Not Started in design order

Build the option list dynamically — only include options that are genuinely next:
- `[_] Run /saas-design-review [other-prd-path] — [system name] is still [In Review / Needs Revision]` (include if another PRD needs review)
- `[_] Run /saas-consistency-check — verify this PRD's values don't conflict with existing PRDs` (always include if ≥1 other PRD exists)
- `[_] Run /saas-review-all-prds — holistic design-theory review across all designed systems` (include if ≥2 PRDs exist)
- `[_] Run /saas-design-system [next-system] — next in design order` (always include, name the actual system)
- `[_] Stop here`

Assign letters A, B, C… only to included options. Mark the most pipeline-advancing option as `(recommended)`.

In collaborative and guided modes, never end the skill with plain text after
file writes — always close with this widget. In autonomous mode, print the next
step and record via `log_decision`.
