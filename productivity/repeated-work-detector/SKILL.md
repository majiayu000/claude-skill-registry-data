---
name: repeated-work-detector
description: Detects recurring workflows across repository history, task notes, issue records, prompts, and project documentation, then evaluates whether each pattern should become a reusable Agent Skill, an extension of an existing skill, a script, a checklist, or remain ad hoc. Use when the user asks what work they repeat, what should become a skill, where automation opportunities exist, or which recurring Codex tasks are worth standardizing.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access. May use read-only local commands such as Git history inspection when available.
metadata:
  category: skill-authoring
  task_type: research
  audience: agent-skill-authors
  tags:
    - workflow-analysis
    - repetition
    - automation
    - skill-discovery
    - codex
  status: draft
  side_effects: command-run
---

# Repeated Work Detector

## Purpose

Identify work that is being performed repeatedly and determine the best way to standardize it.

The skill does not assume that every repeated task deserves a new Agent Skill. It distinguishes among:

- a new reusable skill
- an extension to an existing skill
- a skill chain or router
- a deterministic script
- a checklist or reference document
- project-specific instructions
- work that should remain ad hoc

The goal is to find high-value reusable workflows without filling the skill library with trivial, overlapping, or overly specific skills.

## When to use this skill

Use this skill when:

- The user asks what recurring work should become a skill.
- The user asks Codex to inspect recent work for automation opportunities.
- Similar implementation, review, documentation, debugging, or planning tasks appear repeatedly.
- A repository has accumulated repeated TODO patterns, issue types, or maintenance routines.
- The user wants to expand a skill library based on real work rather than speculative ideas.
- Several existing prompts appear to describe variations of the same workflow.
- The user asks whether a recurring task is better handled by a skill, script, checklist, or project instruction.
- The user asks for an audit of repeated Codex tasks across one or more projects.

Do not use this skill when:

- The user has already selected a workflow and wants the complete skill authored.
- The task occurred only once and there is no other evidence of recurrence.
- The request is primarily about duplicated source code rather than repeated human or agent work.
- The user wants a general brainstorming list without analysis of actual work history.
- The task is a single deterministic command that is better documented as a shell alias or script.
- Another skill already performs the requested workflow and only needs to be invoked.
- The available sources contain no task history, repository history, notes, or other evidence of repeated work.

## Operating constraints

- Treat this as an evidence-based analysis.
- Do not invent occurrences that are not present in the inspected sources.
- Separate observed evidence from inferred patterns.
- Do not count the same task multiple times merely because it appears in a commit, changelog, README, and issue.
- Do not inspect secrets, credentials, private communications, or unrelated personal files.
- Use only sources available in the current environment or explicitly provided by the user.
- Run read-only commands only.
- Do not create, edit, move, or delete files.
- Do not create candidate skills automatically.
- Do not modify the skill catalog.
- Require the user to select a candidate before handing it to a skill-authoring workflow.

## Inputs to inspect

Inspect only the sources relevant and available to the request.

Possible sources include:

### Repository guidance

- `AGENTS.md`
- project instruction files
- contribution guides
- architecture notes
- implementation roadmaps
- decision records
- repository-specific skills

### Work history

- recent Git commits
- commit messages
- changed-file patterns
- pull-request descriptions
- issue titles and descriptions
- changelog entries
- release notes
- session handoff notes
- completed TODO records

### Current project files

- `README.md`
- `docs/`
- `examples/`
- `demo/`
- `tests/`
- `.github/`
- `package.json`
- build configuration
- maintenance scripts

### Provided material

- pasted prompts
- chat exports
- task lists
- meeting notes
- client requests
- planning documents
- collections of previous Codex instructions

### Existing skill library

- `catalog/skills.json`
- `README.md` skill navigation
- `skills/*/*/SKILL.md`
- taxonomy documentation
- skill naming and authoring rules

## Evidence scope

Before analyzing patterns, define the scope.

Record:

- repositories included
- files or task records included
- date range, when known
- branches included
- number of commits, issues, prompts, or notes inspected
- unavailable sources that may limit the result

If the user gives no range, inspect a representative recent sample first.

Prefer:

- recent work over obsolete history
- completed work over speculative TODOs
- multiple independent occurrences
- patterns appearing across more than one project
- workflows with visible inputs, decisions, outputs, and validation

Expand the search only when the initial sample is too small or ambiguous.

## What counts as repeated work

A repeated workflow normally contains the same underlying sequence:

```txt
trigger
→ inputs inspected
→ decisions made
→ actions performed
→ output produced
→ validation completed
```

The wording, repository, framework, or file names may differ while the workflow remains the same.

Example:

```txt
Add new plugin feature
→ inspect source and addons
→ update implementation
→ update tests
→ add demo
→ update README and docs
→ verify build
```

This may be one repeated workflow even when each occurrence involves a different plugin.

## What does not count as independent repetition

Do not count the following as separate occurrences:

- One implementation represented in both a commit and its changelog entry.
- One pull request represented in an issue, branch, commit, and release note.
- Repeated generated files created by a single command.
- Multiple changed files that belong to one task.
- Several TODO comments copied from the same template.
- Repeated wording without repeated execution.
- A task divided into several commits only for review convenience.

Group related evidence into one occurrence before scoring frequency.

## Workflow

### 1. Define the analysis boundary

Determine:

- which repositories or materials are in scope
- which time range is relevant
- whether the user wants project-specific or cross-project patterns
- whether existing skills should be considered for overlap
- whether command execution is available

State important limitations before drawing conclusions.

### 2. Gather work evidence

Collect representative work records.

When Git is available, use only read-only commands such as:

```bash
git status --short
git log --oneline --decorate --all
git log --name-status --format=fuller
git show --stat <commit>
git diff --stat <range>
```

Narrow the range when the repository has extensive history.

Also inspect relevant notes, roadmaps, issue exports, changelogs, prompts, and project documentation.

Do not treat command output as self-explanatory. Read enough context to understand what task each occurrence represented.

### 3. Normalize records into work units

Convert each occurrence into a normalized work unit:

```md
- Trigger
- Goal
- Inputs inspected
- Decisions required
- Steps performed
- Files or systems affected
- Output
- Validation
- Problems encountered
```

Ignore superficial differences such as:

- repository names
- package names
- component names
- client names
- individual filenames
- minor framework syntax

Preserve differences that materially change the workflow.

### 4. Cluster similar work units

Group occurrences by shared workflow.

Use workflow similarity rather than keyword similarity.

A valid cluster should normally share:

- a similar trigger
- comparable inputs
- a stable decision process
- a repeated sequence of steps
- a predictable output
- similar validation requirements

Do not merge clusters merely because they share a broad domain such as accessibility, documentation, or frontend development.

### 5. Record evidence for every cluster

For each candidate pattern, create an evidence table:

```md
| Occurrence | Source | Date or reference | Repeated workflow evidence | Meaningful variation |
|---|---|---|---|---|
```

Every proposed candidate must point to concrete evidence.

Mark each statement as one of:

- **Observed** — directly supported by inspected material.
- **Inferred** — a reasonable abstraction across observed occurrences.
- **Unknown** — not supported by the available material.

### 6. Check existing skills before proposing a new one

Search the existing skill catalog and relevant `SKILL.md` files.

Determine whether the repeated workflow is:

- already covered
- partially covered
- a specialization of an existing skill
- a broader version of several narrow skills
- suitable for a skill chain
- genuinely missing

Compare:

- trigger descriptions
- purpose
- inputs
- workflow steps
- outputs
- side effects
- intended audience

Do not recommend a new skill based only on a different name.

### 7. Classify the best treatment

Choose one primary recommendation for each pattern.

#### New skill

Choose when the workflow:

- contains reusable reasoning or judgment
- has stable inputs and outputs
- appears repeatedly
- is portable beyond one task
- is not already covered
- benefits from a predictable agent workflow

#### Extend an existing skill

Choose when:

- most steps already exist in another skill
- only one missing phase or edge case is recurring
- a new skill would create confusing overlap

#### Skill chain or router

Choose when:

- the repeated work consistently combines several existing skills
- each individual workflow should remain independent
- the missing value is orchestration rather than new behavior

#### Script or command

Choose when:

- the work is deterministic
- the same inputs should always produce the same result
- little or no judgment is required
- repeatability matters more than explanation

#### Checklist or reference

Choose when:

- the task is mainly remembering checks
- execution remains manual
- a full agent workflow would add little value
- the information is stable and concise

#### Project instruction

Choose when:

- the workflow is specific to one repository
- it describes local conventions rather than a portable process
- portability would require removing most of the useful detail

#### Leave ad hoc

Choose when:

- repetition is weak
- the workflow changes substantially each time
- the cost of formalization exceeds the likely benefit
- the task is trivial
- the task is unlikely to recur

### 8. Score skill candidates

Score each pattern from 0 to 2 for each factor.

| Factor | 0 | 1 | 2 |
|---|---|---|---|
| Repetition | One occurrence | Two credible occurrences | Three or more credible occurrences |
| Portability | One task or repository | Adaptable with project-specific changes | Reusable across projects |
| Stable contract | Inputs and outputs are unclear | Partly predictable | Clear inputs, workflow, and output |
| Judgment value | Fully deterministic | Mix of rules and judgment | Meaningful recurring reasoning |
| Time or risk reduction | Minimal benefit | Moderate benefit | Significant time, quality, or risk benefit |
| Distinctness | Already covered | Partial overlap | Clear gap in the library |

Maximum score: `12`.

Interpretation:

| Score | Interpretation |
|---:|---|
| 10–12 | Strong new-skill candidate |
| 7–9 | Conditional candidate; refine boundaries or inspect more evidence |
| 4–6 | Usually better as an extension, script, checklist, or project instruction |
| 0–3 | Keep ad hoc |

Additional rules:

- A pattern with only one credible occurrence cannot be rated as a strong candidate.
- A candidate already substantially covered by another skill cannot be recommended as a new skill.
- A high score does not override poor boundaries.
- A deterministic workflow should still be recommended as a script even when it scores highly.
- Security-sensitive or destructive workflows require stricter side-effect boundaries.

### 9. Design provisional candidate boundaries

For each recommended skill candidate, define:

- proposed skill name
- primary category
- trigger description
- reusable purpose
- inputs
- core workflow
- output contract
- in-scope behavior
- out-of-scope behavior
- expected side effects
- existing skills it overlaps with
- evidence supporting the candidate

Use lowercase hyphenated names.

Use one primary taxonomy category.

Do not write the complete `SKILL.md` unless the user separately requests skill creation.

### 10. Rank the findings

Rank candidates using:

1. strength of evidence
2. frequency
3. cross-project portability
4. time or risk saved
5. distinctness from current skills
6. clarity of workflow boundaries
7. ease of validating the output

Do not rank speculative but exciting ideas above well-supported mundane workflows.

### 11. Recommend the next action

For every pattern, recommend exactly one next action:

- create a skill brief
- inspect more occurrences
- extend an existing skill
- design a skill chain
- create a script
- add a checklist
- update project instructions
- leave unchanged

The detector ends at recommendation and evidence.

It must not automatically perform the recommended action.

## Output format

Return:

````md
# Repeated Work Analysis

## Scope

- Sources inspected:
- Repositories:
- Date range:
- Work records reviewed:
- Existing skills reviewed:
- Limitations:

## Executive summary

Briefly state:

- how many recurring patterns were found
- how many are strong skill candidates
- how many should use another treatment
- the highest-value recommendation

## Ranked opportunities

| Rank | Pattern | Recommendation | Score | Evidence count | Existing overlap | Why it matters |
|---:|---|---|---:|---:|---|---|

## Detailed findings

### 1. Proposed pattern name

**Recommendation:** New skill | Extend skill | Skill chain | Script | Checklist | Project instruction | Leave ad hoc  
**Score:** X/12  
**Confidence:** High | Medium | Low

#### Evidence

| Occurrence | Source | Date or reference | Repeated workflow evidence | Meaningful variation |
|---|---|---|---|---|

#### Normalized workflow

```txt
trigger
→ inspect inputs
→ make decisions
→ perform actions
→ produce output
→ validate result
```

#### Why this treatment fits

Explain why the pattern should become a skill, extension, chain, script, checklist, instruction, or remain ad hoc.

#### Existing overlap

- Existing skill:
- Shared behavior:
- Missing behavior:
- Overlap risk:

#### Provisional candidate

Include this section only for new-skill candidates.

- **Name:** `candidate-name`
- **Category:** `category`
- **Task type:** `type`
- **Side effects:** `value`
- **Trigger description:** ...
- **Inputs:** ...
- **Output:** ...
- **In scope:** ...
- **Out of scope:** ...

#### Next action

State one concrete next step.

## Rejected candidates

| Pattern | Why it was rejected | Better treatment |
|---|---|---|

## Consolidation opportunities

List cases where:

- several candidate ideas should become one broader skill
- one broad workflow should remain several narrow skills
- existing skills should be connected through a router
- an existing skill should absorb the repeated behavior

## Recommended creation order

1. ...
2. ...
3. ...

Explain dependencies between candidates.

## Validation

- [ ] Every pattern has concrete evidence.
- [ ] Duplicate representations of one task were deduplicated.
- [ ] Observations and inferences are clearly separated.
- [ ] Existing skills were checked for overlap.
- [ ] Each pattern received one primary treatment.
- [ ] Skill candidates have stable inputs and outputs.
- [ ] Deterministic work was considered for scripts.
- [ ] Project-specific work was not falsely presented as portable.
- [ ] No files were modified.
````

## Quality bar

The task is complete only when:

- Every proposed pattern is supported by at least two credible occurrences, unless explicitly marked as speculative.
- Strong candidates normally have at least three independent occurrences.
- The same task is not counted more than once through mirrored documentation.
- Patterns are based on repeated workflows, not shared keywords.
- Existing skills are inspected before proposing new ones.
- The analysis distinguishes skills from scripts, checklists, routers, and project instructions.
- Candidate names follow repository naming rules.
- Each candidate has a narrow and reusable purpose.
- Inputs and outputs are predictable.
- Project-specific details are abstracted without removing the workflow’s useful meaning.
- Rankings reflect evidence and value rather than novelty.
- Uncertainty and unavailable evidence are stated.
- No candidate skill or repository file is created automatically.
- No destructive or write commands are run.

## Edge cases

### Only one repository is available

Identify repository-specific repetition, but reduce confidence in portability.

Mark candidates as:

```txt
portable hypothesis — needs cross-project validation
```

### Only prompts or chat exports are available

Treat repeated requests as evidence of demand, but distinguish between:

- repeatedly discussed ideas
- repeatedly executed workflows
- repeatedly revised versions of the same task

Discussion alone is weaker evidence than completed work.

### Commit messages are vague

Inspect changed files, diffs, related documentation, and surrounding commits before classifying the task.

Do not infer a workflow from messages such as:

```txt
fix
update
cleanup
changes
```

### One task spans many commits

Combine commits into one occurrence when they belong to the same implementation or pull request.

### Many tasks use the same files

Do not infer the same workflow merely because tasks repeatedly modify:

- `README.md`
- `package.json`
- tests
- documentation
- configuration files

Compare the actual sequence and intent.

### A pattern is frequent but trivial

Recommend a script, alias, template, or checklist rather than a skill.

### A pattern contains multiple independent workflows

Split it into narrow candidates or recommend a router.

Do not create one giant assistant skill.

### An existing skill almost covers the pattern

Recommend an extension when the missing behavior fits the existing purpose.

Recommend a separate skill only when the trigger, workflow, or output contract is materially different.

### Evidence is contradictory

Report the competing patterns separately.

Do not force them into one abstraction.

### Historical work is obsolete

Exclude or reduce the weight of workflows that no longer match the current stack, repository structure, or project direction.

### Sensitive material appears in the sources

Do not quote or transfer secrets, credentials, personal data, client-confidential details, or private correspondence into a reusable candidate.

Describe the workflow using generic terms.

## Related skills

- `workflow-to-skill-candidate` *(proposed)* — turns an approved repeated workflow into a structured skill proposal.
- `skill-overlap-detector` *(proposed)* — compares a candidate against the existing library in greater depth.
- `skill-brief-writer` *(proposed)* — creates a formal brief after the user selects a candidate.
- `skill-quality-audit` — reviews the completed skill after authoring.
- `daily-work-router` *(proposed)* — may invoke this skill periodically to surface automation opportunities.
