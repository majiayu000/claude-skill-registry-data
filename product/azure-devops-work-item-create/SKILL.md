---
name: azure-devops-work-item-create
description: Use when the user wants to create Azure DevOps Work Items from a discussion, investigation, rough idea, plan, bug report, or feature request.
---

# Azure DevOps Work Item Create

## Scope

Use this skill to turn user intent into one or more well-scoped Azure DevOps
Work Items in the current repository's Azure DevOps project.

Read `../azure-devops-common/references/context.md` before resolving the Azure
DevOps target or creating anything.

## Workflow

1. Resolve the current Azure DevOps organization, project, and repository from
   local git context and `az devops configure --list`.
2. Understand the source material.
   - If the current conversation is enough, summarize it into Work Item-ready
     points.
   - If requirements are vague, ask focused questions one at a time.
   - Split work when separate deliverables, dependencies, risks, or parallel
     workstreams would make implementation and review easier.
   - Estimate each Work Item's touched areas: the files, directories, or
     modules it is expected to change, plus shared resources such as schemas,
     config, migrations, lockfiles, or public interfaces.
   - When otherwise parallel Work Items need the same schema, interface,
     config, workflow, or policy decision, extract that decision into a
     precursor Work Item that settles the contract, and make the dependent
     Work Items blocked by it instead of serializing all of them.
   - Group Work Items into waves: each wave contains Work Items whose blockers
     are all in earlier waves. Mark Work Items in the same wave as
     parallelizable only when their touched areas do not overlap.
3. Look for a repo-local template:
   - `docs/agents/azure-devops-work-item-template.md`
   - If absent, use a compact body with `Summary`, `Background`, `Acceptance
     Criteria`, `Implementation Notes`, `Touched Areas`, `Dependencies`, and
     `Parallelization`.
   - When the template has no equivalent fields, append `Touched Areas` and
     `Dependencies` sections after the template content.
4. Determine Work Item type.
   - Do not hardcode `Issue`.
   - Prefer repository guidance when present.
   - Otherwise infer a candidate such as `Bug`, `User Story`, `Product Backlog
     Item`, `Task`, or `Issue` from available project types and the request.
   - If the type is unclear, stop and ask before creating.
5. Draft each Work Item title, type, description, and optional fields.
   - Optional fields include area, iteration, assigned-to, tags, and custom
     fields only when explicitly supported by repo docs or user input.
   - Write touched areas as a list of repository paths or module names,
     marking each entry as an estimate.
   - Write dependencies as one `Blocked by #<id>` line per blocking Work Item.
     Use a placeholder such as `Blocked by <precursor title>` in the preview
     and replace it with the real ID at creation time.
   - Include only supported facts.
   - Put unknowns in open questions instead of inventing answers.
6. Show a preview before creating anything:
   - target organization, project, and repository
   - proposed Work Item count and split rationale
   - title, type, body, optional fields, touched areas, dependencies, and
     parallelization notes
   - the waves, any precursor Work Items and the contract each one settles,
     and any touched-area overlaps that kept Work Items out of the same wave
   - the relations that will be added: `Parent`/`Child` links to a tracker and
     `Predecessor`/`Successor` links for each blocker
   - creation order when dependencies exist
7. Wait for explicit user confirmation.
8. Create approved Work Items with `az boards work-item create`.
   - Create blocking Work Items before the items they block, so every
     `Blocked by #<id>` line uses the real ID.
   - Add the previewed relations with `az boards work-item relation add`.
     Confirm the relation type names with
     `az boards work-item relation list-type` first.
   - If a relation cannot be added, keep the body text as the source of
     truth, continue, and report which relations were not added.
9. Return created IDs and URLs plus dependency and implementation-order notes,
   the waves and safe parallel groups, and any relations that were not added.

## Guardrails

- This skill is current-repository only.
- Do not create Work Items before preview and explicit confirmation.
- Do not assign, tag, set custom fields, or create relations unless approved or
  clearly specified by repository guidance.
- Do not mutate existing Work Items unless the user explicitly asks.
- Do not put Work Items with overlapping touched areas in the same parallel
  wave.
- Stop if Azure DevOps organization, project, or repository is ambiguous.
