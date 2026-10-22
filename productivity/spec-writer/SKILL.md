---
name: spec-writer
description: Generate numbered repo spec folders with clear requirements, implementation plans, and task lists for non-trivial project work.
version: 1.1.0
---

# Spec Writer Skill

## Intent

Use this skill to turn a rough repo change, feature idea, cleanup effort, or migration into a numbered spec folder with practical planning documents. The goal is to create a working spec package that another engineer can pick up and execute without guessing what the work means.

## Use When

- The user wants a new spec for a repo change, feature, refactor, migration, or workflow
- A project needs structured `requirements.md`, `plan.md`, and `tasks.md` documents
- The repo already uses numbered spec folders and new work should follow that pattern
- The request is large enough that ad hoc notes would be too loose

## Do Not Use When

- The change is tiny and does not need formal planning
- The repo has no spec workflow and the user only wants direct implementation
- The user wants a README, assessment, or changelog instead of an execution spec
- The available context is too thin to produce honest requirements and next steps

## Workflow

1. Read the repo context first.
2. Confirm where specs live and how numbering works.
3. Pick the next available spec number unless the user provided one.
4. Create a short kebab case spec folder name tied to the actual work.
5. Write the core documents:
   - `requirements.md`
   - `plan.md`
   - `tasks.md`
6. Keep each file practical:
   - requirements explain the problem, scope, constraints, and success criteria
   - plan explains the implementation approach, touched areas, risks, and validation path
   - tasks break the work into ordered, checkable execution steps
7. Make assumptions explicit. Do not pretend unknown details are settled facts.
8. Recheck that the spec matches the live repo, existing conventions, and the user's real goal.

## Spec Status

Give every spec a visible state so a folder listing tells the truth about the work. Put a status line at the top of `requirements.md`:

```text
Status: draft | in progress | done | abandoned
Last updated: YYYY-MM-DD
```

When asked to update or review specs, update the status line as part of the change. When creating a new spec, check whether an existing spec already covers the work and is merely stale; updating its status beats creating a duplicate.

## Template Variants

Shape the documents to the work type instead of using one generic skeleton:

- `feature`: requirements emphasize user-facing behavior and acceptance criteria; plan covers integration points and new surface area
- `refactor`: requirements define behavior that must not change and how that is verified; plan emphasizes sequencing and safe checkpoints; tasks alternate change and verify steps
- `migration`: requirements define the end state and cutover criteria; plan covers dual-running, rollback, and data integrity; tasks include a rehearsal step before the real cutover

Name the variant in `requirements.md` so the reader knows which lens the spec uses.

## Requirements Guidance

- State the problem in plain language
- Define in scope and out of scope
- List constraints from the repo, tooling, platform, or user instructions
- Include acceptance criteria that can actually be verified
- Keep wording concrete enough that implementation decisions can be judged against it

## Plan Guidance

- Name the files, modules, folders, scripts, or systems likely to change
- Explain the intended implementation shape without drifting into code
- Call out dependencies, sequencing, migration concerns, and rollback or safety issues where relevant
- Include a validation section with realistic checks such as tests, linting, manual flows, or document review

## Task Guidance

- Break work into an execution order that another engineer can follow
- Prefer tasks that map to real deliverables, not vague activity labels
- Separate implementation, validation, and documentation work when that helps execution
- Keep tasks small enough to complete and review, but not so small that the list becomes noise
- Give each task a rough size of `S` (under an hour), `M` (half a day), or `L` (a day or more) so the spec communicates effort, not just steps; an `L` task is usually a sign it should be split

## Constraints

- Match the repo's existing spec layout if one already exists
- Prefer editing existing planning structure over inventing a new one
- Use direct language and skip filler
- Do not pad specs with generic boilerplate
- Do not hide major assumptions or risks
- If numbering or naming is ambiguous, choose the clearest consistent option

## References

- `shared/skill-standard.md`
- Existing `specs/` folders in the target repo
- Any repo handoff docs such as `assessment.md`, `project-analysis.md`, or roadmap files if they exist

## Help And Examples

Use this skill when the user wants a real execution spec instead of loose notes.

Minimum useful input:

- the repo or project context
- what needs to be built, changed, or cleaned up
- any scope limits or constraints

Example prompts:

```text
Use spec-writer to create the next numbered spec for moving this repo from ad hoc scripts to a module layout with tests and CI.
```

```text
Create a spec folder for adding OAuth refresh handling and export retry logic to this CLI project.
```

```text
Write a numbered repo spec with requirements, plan, and tasks for a README audit plus stale doc cleanup.
```

## Validation Checklist

- The spec folder name and number fit the repo's existing pattern
- `requirements.md`, `plan.md`, and `tasks.md` are all present
- The requirements are specific enough to judge success
- The plan matches the actual repo context
- The tasks are ordered, practical, and executable
