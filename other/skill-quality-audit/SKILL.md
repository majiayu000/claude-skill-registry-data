---
name: skill-quality-audit
description: Audits an Agent Skill for routing clarity, scope, executability, safety, portability, and repository consistency. Use when the user asks to review, validate, improve, approve, or quality-check a SKILL.md file, a proposed skill, or a collection of skills before publishing or merging.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: skill-authoring
  task_type: review
  audience: agent-skill-authors-and-maintainers
  tags:
    - agent-skills
    - quality
    - review
    - routing
    - portability
  status: draft
  side_effects: none
---

# Skill Quality Audit

## Purpose

Review an Agent Skill as an executable instruction package rather than as ordinary documentation.

The audit checks whether an agent can reliably decide when to use the skill, follow its workflow, avoid unsafe or undeclared actions, return a predictable result, and integrate the skill consistently into its source repository.

The default behavior is review-only. Do not edit files unless the user explicitly requests implementation.

## When to use this skill

Use this skill when:

- The user asks to review, validate, improve, approve, or quality-check a `SKILL.md` file.
- A new skill is ready for pre-merge or pre-publication review.
- A skill has a vague description, inconsistent behavior, unreliable triggering, or unclear output.
- Multiple skills need a consistency audit.
- A repository maintainer wants to detect duplicate, overlapping, unsafe, or non-portable skills.
- A skill was generated from a brief and needs verification against repository rules.

Do not use this skill when:

- The user only wants to brainstorm skill ideas.
- The user needs a new skill drafted from scratch rather than reviewed.
- The task is primarily a domain audit, such as accessibility, security, npm publishing, or CI correctness. Use the relevant specialist skill first, then use this skill to review the resulting skill package.
- The user asks to install, publish, deploy, delete, or remotely modify a skill package.

## Inputs to inspect

Inspect the smallest relevant set of files.

Required when available:

- The target `SKILL.md` file or proposed skill content.
- The skill folder path.
- Any referenced support files used by the skill.

Repository context when available:

- `AGENTS.md`
- `README.md`
- `docs/PROJECT_SOURCE.md`
- `docs/TAXONOMY.md`
- `docs/AUTHORING_GUIDE.md`
- `docs/REVIEW_CHECKLIST.md`
- `templates/SKILL_TEMPLATE.md`
- `catalog/skills.json`
- Sibling skills with related names, triggers, or responsibilities.

Optional support folders:

- `references/`
- `scripts/`
- `assets/`
- `agents/`

If repository guidance is unavailable, audit against the portable baseline in this skill and clearly mark repository-integration checks as not verified.

## Audit modes

Select one mode from the request and available inputs:

- Single-skill audit — Review one complete skill.
- Proposal audit — Review a draft or incomplete skill before files are created.
- Batch audit — Review multiple skills for consistency, duplication, and routing overlap.
- Pre-merge audit — Review the skill plus repository catalog and navigation changes.
- Repair review — Produce a prioritized correction plan for a failed audit.

Do not silently switch from review to implementation.

## Workflow

1. Establish the audit target

   Identify:

   - Skill name.
   - Target path.
   - Audit mode.
   - Whether the user requested review only or file changes.
   - Which repository rules are authoritative.
   - Which files are missing or unavailable.

   Do not infer that absent files are valid. Mark them as unverified or missing.

2. Validate package identity and frontmatter

   Check that:

   - The skill has a valid lowercase hyphenated name.
   - The folder name, frontmatter `name`, catalog name, and README link agree.
   - The category is valid and matches the category folder.
   - The description is action-first and specific enough for routing.
   - The description names the target artifact or workflow.
   - The description says when the skill should be used.
   - `license`, `compatibility`, `task_type`, `audience`, `tags`, `status`, and `side_effects` are present when required by the repository.
   - Metadata values are internally consistent.

   Treat formatting differences as findings only when they break parsing, routing, consistency, or repository policy.

3. Test routing quality

   Evaluate the description as a routing contract, not as marketing copy.

   Create a trigger test matrix containing at least:

   - Three prompts that should trigger the skill.
   - Two prompts that should not trigger the skill.
   - One near-miss or ambiguous prompt.

   For each test, record:

   - The test prompt.
   - Expected routing result.
   - Whether the current description supports that result.
   - Any missing phrase, scope boundary, or disambiguation.

   Flag descriptions that are:

   - Too vague, such as “helps with documentation.”
   - Too broad, causing unrelated requests to trigger the skill.
   - Too narrow, omitting common user phrasing.
   - Focused on benefits without naming the action and target.
   - Missing clear exclusions when overlap with sibling skills is likely.

4. Assess scope and cohesion

   Check that the skill performs one reusable job.

   Identify:

   - The primary job.
   - In-scope tasks.
   - Explicitly out-of-scope tasks.
   - Responsibilities that belong in another skill.
   - Overlap with sibling skills.
   - Whether the title, description, workflow, and output all describe the same job.

   Flag unrelated workflows bundled together merely because they affect the same repository.

5. Assess workflow executability

   Verify that an agent can perform the workflow without guessing major steps.

   Check that the skill:

   - Names the files, artifacts, or inputs to inspect.
   - Uses ordered, operational steps.
   - Explains important decisions and branches.
   - Distinguishes required checks from optional checks.
   - Explains how to handle missing files or incomplete context.
   - Requires evidence for findings.
   - Does not invent commands, files, tools, URLs, or validation results.
   - Separates review from implementation.
   - Includes a final validation step.
   - Avoids circular instructions such as “ensure quality is high.”

   A long workflow is not automatically better. Flag repetition that obscures execution.

6. Assess the output contract

   Check whether the skill defines a predictable result.

   The output should make clear:

   - What summary is returned.
   - How findings are prioritized.
   - What evidence is included.
   - Whether recommendations or file changes are reported.
   - How unresolved items are represented.
   - How validation status is communicated.

   Flag output instructions that depend on hidden reasoning, expose private chain-of-thought, or allow unsupported claims.

7. Review safety and side effects

   Compare declared side effects with the actual workflow.

   Check for:

   - File creation or edits.
   - Local command execution.
   - Network or registry access.
   - Publishing, deployment, sending, deletion, or remote mutation.
   - Secret, credential, token, or private-context handling.
   - Destructive actions without explicit approval.
   - Instructions that exceed the minimum required permissions.

   A skill fails this section when its declared side effects materially understate what it instructs the agent to do.

8. Review portability and maintainability

   Check that the skill:

   - Can be copied without relying on undocumented local context.
   - Declares required tools, files, or external access.
   - Avoids user-specific secrets and private data.
   - Avoids unnecessary hard-coded repository names or paths.
   - Uses repository-specific rules only where the skill is intentionally repository-specific.
   - Keeps long examples or specialist reference material in support files when appropriate.
   - Adds scripts only when they materially improve repeatability.
   - Uses stable language rather than implementation trivia likely to become stale.

9. Validate repository integration

   When repository files are available, check that:

   - The source path is correct.
   - The skill folder and `SKILL.md` exist.
   - The category exists in the taxonomy.
   - `catalog/skills.json` contains a matching entry.
   - The catalog entry uses the correct path and metadata.
   - The README navigation contains a matching row.
   - Catalog entries and README rows follow repository sorting rules.
   - Optional support folders exist only when useful.
   - No duplicate skill name or conflicting path exists.

   Do not fail a portable standalone skill for missing repository files when no repository integration was requested. Mark those checks as not applicable or not verified with a reason.

10. Score the applicable dimensions

    Score each applicable dimension from 0 to 2:

    | Dimension | 0 | 1 | 2 |
    |---|---|---|---|
    | Package identity | Missing or contradictory | Partially consistent | Fully consistent |
    | Routing clarity | Unreliable | Usable with ambiguity | Clear and discriminating |
    | Scope cohesion | Mixed responsibilities | Minor scope drift | One focused job |
    | Input contract | Missing | Partial | Explicit and sufficient |
    | Workflow executability | Not actionable | Actionable with gaps | Operational and complete |
    | Output contract | Unpredictable | Partially specified | Predictable and useful |
    | Safety and side effects | Unsafe or understated | Minor ambiguity | Accurate and controlled |
    | Portability | Hidden dependencies | Some local assumptions | Portable or clearly constrained |
    | Edge-case handling | Missing | Partial | Relevant and actionable |
    | Repository integration | Broken | Partial | Consistent |

    For dimensions that genuinely do not apply, use `N/A` with a reason and exclude them from the percentage.

    Calculate:

    `score percentage = earned points / maximum applicable points × 100`

    Assign the result:

    - Pass — 85–100%, with no blocker.
    - Pass with changes — 65–84%, with no blocker.
    - Fail — Below 65%, or any blocker is present.

    The score summarizes the audit; it does not replace evidence.

11. Identify blockers

    Treat any of the following as a blocker:

    - Missing or unusable routing description.
    - No executable workflow.
    - Contradictory instructions that prevent reliable execution.
    - Undeclared destructive or external side effects.
    - Publishing, deletion, deployment, or remote mutation without explicit approval requirements.
    - Secrets, private credentials, or user-specific private context embedded in a reusable skill.
    - A name, path, or category mismatch that makes the package undiscoverable or invalid in its repository.
    - Instructions requiring fabricated evidence, commands, files, or test results.

12. Recommend or apply corrections

    For review-only requests:

    - Return prioritized recommendations.
    - Include replacement wording for high-impact routing or workflow defects when useful.
    - Do not modify files.

    For implementation requests:

    - Make the smallest coherent changes that resolve confirmed findings.
    - Preserve the skill’s narrow purpose.
    - Update catalog or README metadata only when affected.
    - Re-run the audit after changes.
    - Report remaining manual checks honestly.

## Output format

Return the audit using this structure:

```md
## Audit summary

- Skill: `<name>`
- Path: `<path>`
- Mode: `<mode>`
- Result: Pass | Pass with changes | Fail
- Score: `<earned>/<maximum applicable> (<percentage>%)`
- Blockers: `<count>`
- Files changed: none | `<files>`

## Findings

| Severity | Dimension | Evidence | Impact | Recommendation |
|---|---|---|---|---|

Severity values:

- Blocker
- High
- Medium
- Low

## Trigger tests

| Prompt | Expected | Current routing | Result | Notes |
|---|---|---|---|---|

## Scorecard

| Dimension | Score | Evidence |
|---|---:|---|

## Recommended changes

1. ...

## Repository consistency

- [ ] Path matches repository convention.
- [ ] Frontmatter name matches folder name.
- [ ] Category matches folder and taxonomy.
- [ ] Catalog entry matches.
- [ ] README row matches.
- [ ] Side effects are declared accurately.

## Validation

- [ ] All blockers are identified.
- [ ] Findings cite actual skill content or repository evidence.
- [ ] Trigger tests include positive, negative, and ambiguous cases.
- [ ] Unavailable checks are marked unverified.
- [ ] No file changes were made unless requested.
```

If the user requested implementation, replace `Recommended changes` with `Changes made` and add `Remaining TODOs`.

## Quality bar

The audit is complete only when:

- The actual skill content was inspected.
- Findings cite specific sections, metadata, paths, or missing artifacts.
- Routing was tested with positive, negative, and ambiguous prompts.
- Structural compliance and behavioral quality were both reviewed.
- Side-effect declarations were compared with the workflow.
- Repository-specific and portable-baseline findings are distinguished.
- Scores are based only on applicable dimensions.
- A passing result has no blocker.
- Recommendations are concrete enough to implement.
- No files were changed unless the user requested implementation.

## Edge cases

- Only a brief is available: Audit routing, scope, expected inputs, side effects, and proposed output. Mark file and repository checks unverified.
- The skill uses a nonstandard schema: Follow the repository’s documented schema. Do not force this template when another explicit standard applies.
- The skill is intentionally repository-specific: Do not penalize necessary local paths; require the limitation to be clear in compatibility or purpose.
- Several skills overlap: Compare their trigger descriptions and boundaries. Recommend clearer routing before recommending a merge.
- A support script is present: Review what the script is expected to do, its inputs, outputs, failure handling, and side effects. Do not claim code correctness without inspecting it.
- Domain correctness cannot be verified: Separate skill-structure findings from specialist-domain findings and request or invoke the appropriate specialist review.
- Batch audits are large: Report shared systemic defects first, then list skill-specific blockers. Do not hide individual failures behind an average score.

## Related skills

- `skill-brief-writer`
- `release-readiness-review`
- `repository-consistency-audit`
