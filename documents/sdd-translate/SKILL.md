---
name: sdd-translate
description: |-
  Use when translating or migrating existing specs from another tool or format (Spec Kit, Kiro, ADRs, Jira, Confluence, Word docs, or custom markdown requirements) into SDD spec format. Also use when the user says "convert these specs", "migrate to SDD", "translate from X to SDD", or "import specs".
---

# SDD Translate

Convert existing specifications from other frameworks, tools, or formats into SDD spec files.

> `SPECS_ROOT` is resolved by the `sdd` router before this skill runs.
> Replace `.specs/` with your project's actual specs root in all paths below.

## Writing Style

Write the translated specs in the voice of a professional technical writer; do not carry the source document's register across.
Prefer ASD-STE100 Simplified Technical English: short sentences, one instruction per sentence, active voice, and one term per concept.
Keep identifiers, commands, paths, and RFC 2119 keywords exact.

## When to Use

- Migrating from Spec Kit, Kiro, ADRs, Jira, Confluence, or similar
- Converting structured requirements documents into SDD format
- Reverse-engineering third-party spec output into SDD specs

## When Not to Use

- No existing specs to translate — use `sdd-derive` instead
- Already in SDD format — run `sdd-verify` to check completeness

## Invocation Notice

- Tell the user when this skill is running: `sdd-translate`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## Determine Output Type

Baseline specs (`.specs/specs/`) document **implemented** behavior.
Translated specs should only go to baseline when the codebase already implements the described behavior.

```dot
digraph output_type {
    "Codebase implements\nthe described behavior?" [shape=diamond];
    "Translate to baseline specs\n(.specs/specs/)" [shape=box];
    "Translate to change directory\n(.specs/changes/<name>/)\nADDED-only delta specs" [shape=box];

    "Codebase implements\nthe described behavior?" -> "Translate to baseline specs\n(.specs/specs/)" [label="yes — documenting what exists"];
    "Codebase implements\nthe described behavior?" -> "Translate to change directory\n(.specs/changes/<name>/)\nADDED-only delta specs" [label="no — greenfield or aspirational"];
}
```

**How to check:** After inventorying source specs (Phase 1), survey the codebase for relevant implementation.
If the capabilities described in the source specs have no corresponding code, the translated specs are aspirational — generate a change directory with ADDED-only delta specs, a `proposal.md`, and optionally a `tasks.md`.
If the codebase already implements the described behavior, translate directly to baseline.

## Process

### Phase 1: Inventory Source Specs

1. **Identify source format and structure:**

   - Spec Kit → `spec.md` + `plan.md` with Markdown headings
   - Kiro → steering docs + requirements files
   - ADRs → architecture decision records (context/decision/consequences)
   - Jira/Linear → issue descriptions + acceptance criteria
   - Prose documents → natural language requirements

2. **Read all source files** before generating anything.

3. **Group into capabilities** — logical groupings that will each become one `.specs/specs/<capability>/spec.md`:

   - By feature area: `auth/`, `payments/`, `notifications/`
   - By component: `api/`, `frontend/`, `workers/`
   - By bounded context: `ordering/`, `fulfillment/`

### Phase 2: Assess Scope and Plan Decomposition

Before generating specs, count requirements across all source material:

| Signal                 | Action                                                  |
| ---------------------- | ------------------------------------------------------- |
| ≤ 8 requirements total | Single capability, proceed directly                     |
| 9–20 requirements      | Split into 2–4 capabilities, proceed                    |
| 20+ requirements       | Present capability split to user, wait for confirmation |

When decomposing, present the proposed split:

```text
Proposed capabilities:
- auth/      → login, session, token management (5 reqs)
- payments/  → billing, subscriptions (6 reqs)
- ui/        → themes, layout (4 reqs)

Proceed with this split? (or suggest changes)
```

When the output type is a **change directory** (greenfield or aspirational — see Determine Output Type above), present capabilities in build-dependency order rather than alphabetically; the implementer will work through them in the order shown.
See `references/sdd-change-formats.md` § 4.
For **baseline** output (code already exists), ordering is a presentation choice — alphabetical is fine.

### Phase 3: Translate Each Capability

**Output path depends on the output type decision above:**

- **Baseline** (code exists): produce `.specs/specs/<capability>/spec.md` following SDD baseline format.

- **Change directory** (greenfield/aspirational): create `.specs/changes/<name>/` with:

  - `proposal.md` — intent, **user stories**, scope, approach (see `references/sdd-change-formats.md` § 1.1)
  - `specs/<capability>/spec.md` — ADDED-only delta specs, each requirement carrying a `Serves:` backlink to a proposal story
  - `tasks.md` — when implementation steps are clear (optional)

Also seed `.specs/NORTH-STAR.md` if absent — draft a candidate product north star from the source specs for the user to ratify; each user story ladders to it.
When the source uses user-story grammar ("As a … I want … so that …"), the story belongs in `proposal.md` § User Stories (keep the "so that {value}" clause); translate only the WHAT into the requirement and point its `Serves:` line back at the story.

Preserve the Phase 2 build-dependency order in `proposal.md` Scope and `tasks.md` when present.
If implementation steps are unclear and `tasks.md` is omitted, mention any ordering assumptions in the output summary.

See `references/sdd-spec-formats.md` for both baseline and delta spec formats.

Add a source attribution blockquote at the top of each generated spec (see format reference Section 2):

> Translated from {source tool/format} on {date}
> Source: {source file or description}

**Read `references/sdd-spec-formats.md` § 1 before translating.**
The translation is from the source doc's grammar into SDD contract statements (see § 1.1 contract shapes).
Source docs from other tools (Spec Kit, Jira, ADRs, prose) commonly mix WHAT and HOW in the same sentence; translate only the contract, and route mechanism detail to `design.md` or discard it.

When the translated requirement is a universal SHALL, apply the **partition heuristic** in `references/sdd-spec-formats.md` § 1.6 to the source's acceptance criteria.
Source docs frequently capture only the happy-path acceptance criterion; if the heuristic flags a partition the source did not cover, surface the gap as an Uncertainty rather than fabricating scenarios.

**Translation rules:**

| Source pattern                                                                               | SDD translation                                                                                                                                                                                                                     |
| -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Users can X"                                                                                | `The system SHALL allow users to X`                                                                                                                                                                                                 |
| Acceptance criteria bullets                                                                  | `#### Scenario:` entries with GIVEN/WHEN/THEN (as evidence of the requirement — see § 1.5)                                                                                                                                          |
| "It should Y"                                                                                | `The system SHOULD Y`                                                                                                                                                                                                               |
| "Required: Z"                                                                                | `The system MUST Z`                                                                                                                                                                                                                 |
| Implementation detail (class names, libraries)                                               | Move to `## Technical Notes` (baseline) or `design.md` (change directory); omit from the requirement                                                                                                                                |
| Named algorithm / threshold / strategy (e.g., "use TF-IDF bottom quartile", "retry 3 times") | Translate to the property it produces (e.g., "queries that produce no relevant documents"); route the named strategy to `design.md`                                                                                                 |
| Phase-gated steps (plan.md, tasks.md)                                                        | Omit — not behavior                                                                                                                                                                                                                 |
| "As a user, I want X so that Y"                                                              | Baseline: `The system SHALL allow users to X` (value layer dropped — baseline is value-free). Change directory: capture the story incl. "so that Y" in `proposal.md` § User Stories and add a `Serves:` backlink on the requirement |
| "Shall not / Must not"                                                                       | `The system SHALL NOT / MUST NOT {prohibited behavior}`                                                                                                                                                                             |
| Numbered requirement IDs (e.g., `REQ-001:`)                                                  | Strip the ID prefix; preserve the requirement text                                                                                                                                                                                  |

**Critical rules:**

- Every translated requirement is a contract statement in one of the shapes from `references/sdd-spec-formats.md` § 1.1 (guarantee, invariant, prohibition, precondition-consequence, observable-state relationship)
- Every scenario must have **GIVEN**, **WHEN**, **THEN** (bold labels, exact casing)
- Scenarios use `####` (4 hashtags), requirements use `###` (3 hashtags)
- **Baseline output:** no delta markers (ADDED/MODIFIED/REMOVED)
- **Change directory output:** use ADDED sections only (all behavior is new); no `## Purpose` or `## Technical Notes`
- **Change directory value layer:** author `## User Stories` in `proposal.md` (keep each "so that {value}" clause) and add a `Serves:` backlink to each delta requirement; seed `.specs/NORTH-STAR.md` if absent.
  Baseline output is value-free — no stories or backlinks.

### Phase 4: Validate Output

**Common to both output types:**

- [ ] `scripts/check_spec_format.py` passes on every translated spec — heading levels, the `## Requirements` container, delta sections, bold GIVEN/WHEN/THEN, and RFC 2119 keywords:

  ```text
  uv run --quiet <skill_root>/scripts/check_spec_format.py <specs-dir>
  ```

- [ ] Each requirement is a contract statement in one of the shapes from `references/sdd-spec-formats.md` § 1.1 — a property about observable state that stands on its own without its scenarios

- [ ] Universal SHALL claims have partition coverage per the heuristic in `references/sdd-spec-formats.md` § 1.6 — when a positive signal fires, scenarios cover each partition (or the gap is recorded as an Uncertainty)

- [ ] Implementation details and named strategies from source were routed to `## Technical Notes` (baseline) or `design.md` (change directory), not left in the requirement text

**Change directory output only:**

- [ ] All specs use ADDED sections only (delta format)
- [ ] `proposal.md` exists with Intent, User Stories, Scope, Approach
- [ ] Each user story keeps its "so that {value}" clause and ladders to `NORTH-STAR.md`
- [ ] Each delta requirement carries a `Serves:` backlink to a proposal story
- [ ] `proposal.md` Scope and `tasks.md` preserve build-dependency order when the translation produced implementer-facing change artifacts

### Phase 5: Schema Snapshot (if schemas configured)

If `.specs/.sdd/schema-config.yaml` exists:

1. Generate schema snapshots using the configured extraction commands.
2. Store in `.specs/schemas/` — this establishes the baseline for all future `sdd-verify` conformance checks.
3. Update `.specs/schemas/.schema-sources.yaml` with the generation date.

If no schema config exists but schema artifacts are detected in the repo (e.g., `openapi.yaml`, `.proto` files, `schema.graphql`), suggest creating `.specs/.sdd/schema-config.yaml` before the first `sdd-verify` run:

> "Detected schema artifacts. A `.specs/.sdd/schema-config.yaml` would let `sdd-verify` cross-validate implementation against these specs. See `references/sdd-schema.md` § 3 for the format. Say 'skip' to dismiss."

If no schema config and no artifacts detected, skip silently.

## Output

**Baseline (code exists):**

- `.specs/specs/<capability>/spec.md` per capability

**Change directory (greenfield/aspirational):**

- `.specs/changes/<name>/proposal.md`
- `.specs/changes/<name>/specs/<capability>/spec.md` (ADDED-only delta format)
- `.specs/changes/<name>/tasks.md` (when applicable)

Summary: capabilities created, requirement count per capability, translation notes and assumptions.

## Common Mistakes

- Translating source-doc grammar without translating the _content_ — a Jira ticket saying "POST to `/users` then insert into `users` table" is mechanism in both the source and a literal translation.
  Translate to the property the source was trying to guarantee ("a user account is created") and route the mechanism to `design.md`.
  See `references/sdd-spec-formats.md` § 1.
- Using non-RFC-2119 language ("the system will", "users can") instead of SHALL/MUST/SHOULD
- One giant spec instead of capability decomposition for large surface areas
- Including delta markers (ADDED/MODIFIED) in baseline specs
- Not reading all source files before generating output
- Writing baseline specs for a greenfield project — `.specs/specs/` asserts implemented behavior; if nothing is built yet, use a change directory with ADDED-only delta specs
- Discarding the "so that {value}" clause when producing a change directory — it should become a proposal user story with the requirement's `Serves:` backlink; only baseline output (which is value-free) drops the value layer

## References

- `references/sdd-spec-formats.md` — baseline spec and scenario formats
- `references/sdd-schema.md` — schema config format and lifecycle policy
- `scripts/check_spec_format.py` — checks each translated spec's heading structure; exits non-zero on a malformed spec
