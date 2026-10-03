---
name: pdr-intake
description:
  'Trigger: PDR, PRD, pdr-intake, early idea, I have an idea, mature idea. Converts ambiguous ideas
  into minimum PDRs without triggering SDD.'
license: Apache-2.0
metadata:
  author: AutanaSoft
  organization: AutanaSoft
  version: '1.0'
  date: 'Jul 2026'
---

# PDR Intake

## Activation Contract

Use this skill when the user opens with an early product idea and wants to mature it or close open
questions. This skill does not start an SDD cycle.

Triggers (aligned with the `description`):

- Artifact references: `PDR`, `PRD`, `pdr-intake`.
- Conversational phrases: "I have an idea", "early idea".
- Intent verbs: "mature idea".

Do not use this skill when the scenario is different:

- The user already brings a spec or formal PRD → go to `sdd-spec`.
- The conversation is open technical exploration → go to `sdd-explore`.
- The idea has already gone through SDD and is back for review → go to `sdd-verify`.

The final result is a minimum PDR persisted at `docs/prd/{module}/{area}/{slug}-pdr.md` and an
inline executive summary.

## Hard Rules

### Structure and scope

- Use `assets/minimal-pdr-template.md` as the base structure.
- Do not turn the PDR into technical design, detailed spec, or implementation plan.
- If problem, objective, or scope are missing, ask before completing the PDR.
- If several critical data points are missing, ask one question per turn, starting with the real
  problem.
- Mark open questions explicitly; do not invent decisions or requirements.

### Persistence and delivery

- The skill always creates the PDR file; there is no inline-only flow. On completion, it also
  returns an inline executive summary.
- Default file path: `docs/prd/{module}/{area}/{slug}-pdr.md`. If the user does not specify `module`
  or `area`, ask before creating.
- Create the directory `docs/prd/{module}/{area}/` with `mkdir -p`; if it fails for permissions,
  return a clear message and do not write the file.
- If a file already exists at the destination path, read it and compare intent with the new idea
  before writing. If the intent matches, ask the user: overwrite, minor update, or major change? If
  the intent is different, derive a new slug (do not overwrite the existing PDR).
- There is no formal escape hatch to discard a draft; if the user does not want to keep it, they
  delete it manually.

### Lifecycle and versioning

- `status: draft` while the PDR has not been approved by the user.
- `version` stays fixed during `draft`. Only on user approval, the skill analyzes whether the change
  is minor (`1.0` → `1.1`) or major (`1.0` → `2.0`) and bumps the frontmatter.
- Versioning lives in the frontmatter, never in the file name.

### Frontmatter

- The `owner` field must indicate the module or workspace responsible for the PDR, for example
  `packages-ui`, `apps-web`, or `apps-cli`.
- The `{slug}` must be kebab-case, use lowercase ASCII, describe the change or problem, and avoid
  dates unless the user explicitly asks.
- The `{module}` and `{area}` segments must reuse existing names when applicable, for example
  `apps-dash/pages`, `apps-dash/components`, or `packages-ui/components`.

### Language

- PDR file content (the markdown document at `docs/prd/{module}/{area}/{slug}-pdr.md`) defaults to
  neutral and professional English regardless of the conversation language or the agent's active
  persona.
- If the user explicitly requests another language, use it. Spanish is the most common case but any
  language is acceptable on explicit request.
- All non-English output must be neutral and professional. Do not introduce regional variants
  (voseo, slang, dialect-specific grammar) unless the user explicitly asks for them.

## Decision Gates

| Situation                                           | Action                                                                                 |
| --------------------------------------------------- | -------------------------------------------------------------------------------------- |
| The idea has clear problem, objective, and scope    | Create the minimum PDR as a file + inline executive summary                            |
| Critical data is missing                            | Ask one question at a time, starting with the real problem                             |
| `module` or `area` is missing for the path          | Ask before creating the file                                                           |
| A PDR already exists at the path and intent matches | Ask: overwrite, minor update, or major change?                                         |
| A PDR already exists and intent is different        | Derive a new slug; do not overwrite the existing PDR                                   |
| `mkdir -p` fails for permissions                    | Return a clear message and do not write the file                                       |
| Premature technical design is present               | Convert it into implementation notes                                                   |
| Several features are mixed together                 | Recommend splitting before creating the PDR                                            |
| The user approves the PDR                           | Analyze change magnitude and bump `version` (minor `1.0` → `1.1`, major `1.0` → `2.0`) |
| The user asks to start SDD when finished            | Finish the PDR first and ask for explicit confirmation to switch to another flow       |

## Execution Steps

1. Read `assets/minimal-pdr-template.md`.
2. Extract intent, problem, objective, scope, key concepts, implementation notes, and acceptance
   criteria from the user's idea.
3. If `module` or `area` is missing, ask before continuing.
4. Build the first coherent draft of the PDR using the template.
5. Create the file at `docs/prd/{module}/{area}/{slug}-pdr.md` with `mkdir -p` for parent
   directories.
6. Update the file on each clarification round, keeping `version` fixed while `status: draft`.
7. If a file already exists at the destination path, read it and compare intent before writing (see
   Decision Gates).
8. On user approval, analyze whether the change is minor or major and bump `version` in the
   frontmatter.
9. At closure, return an inline executive summary with: title, problem, objective, scope (in/out),
   acceptance criteria, open questions + path, status, and version.
10. Stop after delivering the PDR.

## Output Contract

Return:

- Path of the file created or updated under `docs/prd/{module}/{area}/{slug}-pdr.md`.
- Inline executive summary: title, problem, objective, scope (in/out), acceptance criteria, open
  questions.
- Current `status` and `version` from the frontmatter.
- Explicit recommendation: approve, adjust, or split.
- Confirmation that no SDD cycle was started.

## Final Verification Checklist

Before returning the PDR, verify:

- [ ] The real problem is explicit.
- [ ] The objective fits in one sentence.
- [ ] The scope includes `In scope` and `Out of scope`.
- [ ] Acceptance criteria are verifiable.
- [ ] Open questions are marked explicitly.
- [ ] No premature technical design.
- [ ] The file exists at `docs/prd/{module}/{area}/{slug}-pdr.md` and parent directories were
      created with `mkdir -p`.
- [ ] The frontmatter includes `owner`, `module`, `area`, `slug`, `status`, and `version`.
- [ ] If a previous file existed, it was read, intent was compared, and the correct policy was
      applied.
- [ ] Status remains `draft` unless there is explicit human approval.
- [ ] `version` stays fixed during `draft` and only bumps on approval.
- [ ] The inline executive summary includes the relevant points and references the file path.
- [ ] No proposal, spec, design, tasks, apply, or SDD preflight was started.

## References

- `assets/minimal-pdr-template.md` — base template to build the minimum PDR.
