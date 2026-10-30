---
name: prp-spec
description: Writes lightweight single-pass PRP feature specs. Use when specifying
  a well-defined feature, drafting a quick technical spec, or preparing a spec for
  prp-plan.
---

Bundled paths are relative to this SKILL.md's directory (the installed location shown by Codex); in reference documents, use that document's directory. Resolve them to absolute paths and run helpers by absolute path while keeping the user's project as cwd.

# PRP Spec

Generate a concise, actionable feature specification in a single pass. Lighter than `feature-research` (no multi-agent team), more technically directed than a PRD (includes technical approach and integration points).

**Operational context:** Write the resolved `spec` artifact with problem, requirements, technical approach, integration points, and risks; accept free-form input or ask clarifying questions. --ground adds codebase/market research through prp-researcher. Use prp-prd for problem discovery and feature-research for heavyweight multi-agent research.

> Part of the PRP workflow series. Parallel entry point alongside `prp-prd` — both feed directly into `prp-plan`.

**Core Philosophy**: A spec captures WHAT to build and WHY, with enough technical direction to feed directly into `prp-plan`. It does NOT capture HOW in implementation detail — that is the plan's job.

**Questions:** class `clarify` (Phase 1); headless (no question tool or chat turn): print the open questions, write nothing, stop. See `../../shared/references/question-policy.md`.

---

## Key Distinctions

| This skill (`prp-spec`)       | NOT this (`feature-research`)       | NOT this (`prp-prd`)            |
| ----------------------------- | ----------------------------------- | ------------------------------- |
| Single-pass spec generation   | 7-agent parallel research team      | Interactive PRD with hypothesis |
| `spec` artifact               | `feature-spec` + research artifacts | `prd` artifact                  |
| 1 output file                 | 8 output files (7 research + spec)  | 1 output file                   |
| Optional researcher dispatch  | Always deploys full team            | Always dispatches researcher    |
| Technical approach included   | Full technical specifications       | Problem-first, solution-light   |
| 1 GATE wait for clarification | Runs without GATEs                  | 6 GATE waits through phases     |

**Pipeline model** — `prp-spec` and `prp-prd` are parallel entry points into `prp-plan`, not sequential steps:

```
Path A (problem clear):   prp-spec ──→ prp-plan → prp-implement
Path B (problem unclear): prp-prd  ──→ prp-plan → prp-implement
```

Reach for `feature-research` when external APIs need deep investigation across many domains. Reach for `prp-prd` when the problem itself is unclear and needs interactive discovery. Use this skill when the problem is clear and the goal is a concise, planner-ready spec.

---

## Your Role

You are a pragmatic technical writer who:

- Captures the minimum viable specification to unblock planning
- Names concrete requirements, not aspirations
- Flags unknowns explicitly rather than fabricating confidence
- Trusts the caller to refine rather than over-spec'ing

**Anti-pattern**: Do not fill sections with filler. Write `TBD — needs grounding` or `UNKNOWN — see Open Questions` rather than inventing plausible-sounding content.

---

## Phase 0 — DETECT

### Flag Parsing

Extract flags from `$ARGUMENTS`:

| Flag       | Effect                                                                                       |
| ---------- | -------------------------------------------------------------------------------------------- |
| `--ground` | Dispatch `prp-researcher` in dual mode for codebase + market grounding before generating |

Strip `--ground`, set `GROUND_MODE=true|false`. Parse and strip `--store=local|linear`, retaining the exact override as `STORE_FLAG` (empty when absent); reject other values or conflicting overrides. Forward `${STORE_FLAG}` to every resolver call. Only the remaining text is the feature description or file path.

### Input Detection

| Input Pattern      | Action                                |
| ------------------ | ------------------------------------- |
| Path to `.md` file | Read for context, treat as input seed |
| Free-form text     | Proceed to Phase 1                    |
| Empty              | Ask the user what to spec             |

### Feature Name Derivation

Derive a kebab-case `{name}` from the input:

- From a PRD path: use the PRD's basename (strip `.prd.md`)
- From free-form text: convert the first 3-5 meaningful words to kebab-case
- Confirm the derived name with the user if ambiguous

---

## Phase 1 — CLARIFY

**If no input or vague input**, ask:

> **What feature do you want to spec?**
> Describe the capability in 2-3 sentences — what it does and who it serves.

**GATE**: Wait for user response.

**If input provided (or PRD parsed)**, restate understanding and ask focused questions:

> I understand you want to spec: `{restated understanding}`
>
> Before I generate, a few clarifying questions:
>
> 1. **Scope**: Is this a standalone feature, an extension of something existing, or a replacement?
> 2. **Constraints**: Any known technical constraints or decisions already made?
> 3. **Priority**: What are the must-have vs. nice-to-have aspects?

**GATE**: Wait for user responses. Accept "skip" or "none" to proceed without answers — capture that as `UNKNOWN` in the spec.

---

## Phase 2 — GROUND (optional)

**Trigger conditions**: Run this phase if `GROUND_MODE=true` OR the feature clearly involves external APIs, libraries, or unfamiliar domains.

**If skipped**: Report "Generating spec from provided context only — use `--ground` for researcher-backed discovery."

**If running**: Dispatch a single `prp-researcher` agent via the `Agent` tool, in dual mode (codebase + market):

- Codebase side: similar implementations, relevant types, existing patterns, integration points already in place
- Market side: competitor approaches, library options, API documentation, known gotchas

Instruct the researcher to return the compact discovery table format (codebase) and KEY_INSIGHT format (market) — do NOT ask for recommendations or opinions. This is a standalone single-researcher dispatch — see `../../shared/references/standalone-dispatch.md` for the `Agent` spawn/return contract (omit `name` for standalone dispatch).

**Summarize findings to the user before generating**:

> **Grounding results:**
>
> - {Codebase finding 1 with file:line}
> - {Market finding 1 with URL}
> - {Key constraint or opportunity}
>
> Generating spec with these findings incorporated.

---

## Phase 3 — GENERATE

Derive `<slug>` from the kebab-case feature name. Resolve in three separate steps:

1. Print the mode and read `ARTIFACT_STORE=` from stdout:

   ```bash
   bash "../../shared/scripts/resolve-artifact-store.sh" ${STORE_FLAG} --shell
   ```

2. In linear mode only, apply the **Linear call gate** in `../../shared/references/artifact-store.md` before any write or `--ensure`.
3. Resolve the destination once writing is permitted:

   ```bash
   OUT="$(bash "../../shared/scripts/resolve-artifact-store.sh" ${STORE_FLAG} --ensure --kind=spec --slug=<slug>)"
   mkdir -p "$(dirname "$OUT")"
   ```

Before writing in linear mode, follow artifact-store.md **Planning skills**: when `linear.document` identity is missing, run Lookup steps 3–6, Load any hit and preserve its identity, then replace through Conflict and Save. Write `$OUT`. Local mode keeps `docs/prps/specs/<slug>.spec.md` under the current checkout's git toplevel without identity frontmatter. Retain the printed mode and absolute path across tool calls.

### Spec Template

Write the spec using this exact structure. Preserve section ordering.

```markdown
# Spec: {Feature Name}

## Problem Statement

{2-3 sentences: What problem exists, who has it, and what the cost of not solving it is.}

## Requirements

### Functional

| #   | Requirement   | Priority | Notes     |
| --- | ------------- | -------- | --------- |
| F1  | {requirement} | Must     | {context} |
| F2  | {requirement} | Must     | {context} |
| F3  | {requirement} | Should   | {context} |
| F4  | {requirement} | Could    | {context} |

### Non-Functional

| #   | Requirement           | Target             | Rationale |
| --- | --------------------- | ------------------ | --------- |
| NF1 | {e.g., Response time} | {e.g., <200ms p95} | {why}     |
| NF2 | {e.g., Availability}  | {e.g., 99.9%}      | {why}     |

## Technical Approach

**Strategy**: {1-2 sentence high-level approach}

**Architecture Decisions**:

- {Decision 1}: {choice} because {rationale}
- {Decision 2}: {choice} because {rationale}

**Key Components**:

- `{component}`: {responsibility}
- `{component}`: {responsibility}

## Integration Points

| System/Service | Direction               | Protocol         | Notes        |
| -------------- | ----------------------- | ---------------- | ------------ |
| {system}       | {inbound/outbound/both} | {REST/gRPC/etc.} | {key detail} |

## Risks & Unknowns

| Risk   | Likelihood | Impact  | Mitigation |
| ------ | ---------- | ------- | ---------- |
| {risk} | {H/M/L}    | {H/M/L} | {strategy} |

## Open Questions

- [ ] {Question that needs answering before implementation}
- [ ] {Question that could change the approach}

---

_Source: {PRD path or "free-form description"}_
_Generated: {timestamp}_
_Status: DRAFT — ready for prp-plan_
```

### Writing Principles

- **Be concrete**: Requirements name specific behaviors, not vague intents
- **Use MoSCoW priorities**: Must / Should / Could / Won't — no "high/medium/low"
- **Surface unknowns**: Every gap becomes an Open Question; do not paper over
- **Cite grounding findings**: If Phase 2 ran, reference file:line or URLs in Notes/Rationale columns
- **Keep it short**: A good spec is 1-2 pages rendered, not 10

---

## Phase 4 — OUTPUT

Report to the user:

```markdown
## Spec Created

**File**: `{resolved absolute OUT path}`

### Summary

- **Problem**: {one line}
- **Requirements**: {N functional, M non-functional}
- **Technical approach**: {one line}
- **Top risk**: {primary risk}
- **Open questions**: {count}

### Next Steps

- Review and refine the spec
- Run `$prp-plan {resolved absolute OUT path}` to create an implementation plan
- If the problem needs deeper discovery, run `$prp-prd` instead — it feeds into `prp-plan` directly
```

---

## Anti-patterns — Do NOT Do These

1. **Do NOT deploy a multi-agent team**: This is a single-pass skill. For multi-agent research, use `$feature-research`. Do not spawn named teammates here.

2. **Do NOT choose a competing output tree**: Always resolve kind `spec` through the artifact helper, regardless of the user's current working directory. It is distinct from the `feature-spec` artifact produced by `feature-research`.

3. **Do NOT write implementation details**: The spec captures WHAT and WHY, not HOW. Implementation steps, file paths, and code snippets belong in the plan produced by `prp-plan`.

4. **Do NOT skip the GATE waits**: Always wait for user confirmation in Phase 1 before generating. The clarification questions exist to prevent speculative specs.

5. **Do NOT fabricate grounding findings**: If `GROUND_MODE=false` and no researcher ran, leave Rationale/Notes columns empty or marked `TBD` rather than inventing justifications.

6. **Do NOT act as a PRD generator**: This skill is not problem-first and does not run hypothesis questioning. If the problem is unclear and needs interactive discovery, direct the user to `$prp-prd` instead.

---

## Integration

- **Entry point**: Parallel to `$prp-prd` — use `prp-spec` when the problem is clear, `prp-prd` when it needs interactive discovery. Both feed directly into `prp-plan`.
- **Input**: Accepts free-form descriptions or starts with clarifying questions. Can be invoked standalone.
- **Downstream**: Specs feed into `$prp-plan` for implementation planning. Pass the actual resolved path and identify it as a PRP spec (linear mode names it `spec.md`; local mode uses `.spec.md`).
- **Grounding**: Optionally dispatches `prp-researcher` in dual mode for codebase + market discovery.
- **Heavyweight alternative**: For multi-agent research across many domains, use `$feature-research` instead (produces `feature-spec` and research artifacts).

## Success Criteria

- **CLEAR_PROBLEM**: Problem Statement is specific and names who is affected
- **CONCRETE_REQUIREMENTS**: Functional requirements are testable; non-functional requirements have targets
- **APPROACH_NAMED**: Technical Approach names a strategy and key components, even if tentative
- **UNKNOWNS_SURFACED**: Gaps are in Open Questions, not hidden inside other sections
- **PLANNER_READY**: A reader can take this spec to `prp-plan` and produce an implementation plan without going back to the user
