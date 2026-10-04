---
name: ai-request-skill
description: Request or contribute a new AI skill that does not exist yet. Use when DSPy supports something but there is no skill for it — helps you build the skill and submit a PR, or file an issue requesting it. Also use when the user says there should be a skill for this, can we make a skill, I want to contribute a skill, none of the ai- skills cover my use case, how do I add a new skill, submit a skill, or open a PR for a missing skill.
argument-hint: "[describe the missing capability]"
---

# Request or Build a Missing Skill

The user needs a DSPy capability that doesn't have a skill yet. Help them contribute it or request it.

**This skill always ends with a concrete action on GitHub:**
- **Path A (Build)**: Create the skill files, commit, push, and open a **pull request** to `lebsral/DSPy-Programming-not-prompting-LMs-skills`
- **Path B (Request)**: File a **GitHub issue** on `lebsral/DSPy-Programming-not-prompting-LMs-skills` describing what's needed

Do not stop at "here's what the PR/issue would look like" — actually create it using `gh pr create` or `gh issue create`.

## Step 1: Confirm the gap

If `$ARGUMENTS` is provided, use it. Otherwise ask: "What DSPy capability do you need that isn't covered by an existing skill?"

Verify this is something DSPy actually supports. If it's outside DSPy's scope entirely (e.g., "build a React frontend"), say so and suggest appropriate tools instead.

Check the existing skills in `skills/` or [ai-*](https://github.com/lebsral/dspy-programming-not-prompting-lms-skills) to make sure there isn't already a skill that covers this. If there's a close match, suggest it instead.

Summarize back to the user:
- **What they need**: one sentence
- **DSPy features involved**: which DSPy modules, integrations, or patterns are relevant
- **Closest existing skill**: what's close but doesn't quite fit

## Step 2: Choose a path

Ask the user:

> Would you like to:
> 1. **Build the skill** — I'll help you create it with proper testing and prepare a PR
> 2. **Request the skill** — I'll draft a GitHub issue so the maintainers know it's needed

## Path A: Build the skill

### Use skill-creator if available

Check whether the `/skill-creator` skill is available (it's from the [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/skill-creator) repo). If available, delegate to it — it handles the full create-test-iterate workflow including evaluation, benchmarking, and description optimization.

When delegating to `/skill-creator`, first read the repo standards so the skill matches conventions:

1. Read `docs/skill-standards.md` — the full authoring checklist (naming, descriptions, gotchas, cross-refs, progressive disclosure, provider-agnostic code)
2. Read `docs/skills-spec.md` — the Claude Code skills format (frontmatter fields, file structure, supporting files)
3. Read `CLAUDE.md` — repo-level conventions (dual naming, web-developer language, 500-line limit)

Pass the contents of these files as context to `/skill-creator` so it generates a skill that matches repo standards on the first pass.

Then let skill-creator run its workflow: draft → test → review → iterate → package.

### If skill-creator is NOT available

Build the skill manually. First read the standards:

1. Read `docs/skill-standards.md` for the full authoring checklist
2. Read `docs/skills-spec.md` for the Claude Code skills format
3. Read 2-3 existing skills in `skills/` to match tone and structure

Install skill-creator for future use:

```bash
npx skills add anthropics/skills/skill-creator
```

#### Write the SKILL.md

Follow the structure in `docs/skill-standards.md`. Key points:

- **Description**: `<WHAT>. Use when <triggers>. Also: <more triggers>.` — plain YAML scalar, no quotes
- **Body**: Step 1 gathers context (2-4 questions) → Steps 2-4 core work → Gotchas (3-5) → Cross-references → Additional resources
- **Code**: provider-agnostic with `# or ...` comment, copy-pasteable with imports
- **Standalone**: every skill must be self-contained — include a `reference.md` for `dspy-` skills or `ai-` skills that heavily reference DSPy APIs
- **Verify API usage** against https://dspy.ai/api/ for correct patterns

#### Test the skill

Create 2-3 test prompts — realistic requests a developer would make. Run them with the skill active and verify the outputs make sense.

### Submit the PR

After creating (and optionally testing) the skill files, submit a pull request. Do all of these steps — don't stop at "here's what to do":

1. Update `README.md` — add a row to the problem catalog table in the appropriate position
2. Create a branch: `git checkout -b add-ai-<problem-name>`
3. Stage and commit: `git add skills/ai-<problem-name>/ README.md && git commit -m "Add ai-<problem-name> skill"`
4. Push: `git push -u origin add-ai-<problem-name>`
5. Open the PR:

```bash
gh pr create \
  --repo lebsral/DSPy-Programming-not-prompting-LMs-skills \
  --title "Add ai-<problem-name> skill" \
  --body "$(cat <<'EOF'
## Summary
- **Problem**: <what the user is solving>
- **DSPy features**: <modules, patterns used>
- **Example invocation**: `/ai-<problem-name> <example prompt>`

## Files
- `skills/ai-<problem-name>/SKILL.md` — main instructions
- `skills/ai-<problem-name>/examples.md` — worked examples
- `README.md` — catalog table updated
EOF
)"
```

Return the PR URL to the user when done.

## Path B: Request the skill

File a GitHub issue on the repo. Do not just draft it — actually submit it:

```bash
gh issue create \
  --repo lebsral/DSPy-Programming-not-prompting-LMs-skills \
  --title "Skill request: ai-<problem-name>" \
  --assignee lebsral \
  --body "$(cat <<'EOF'
## Problem
<What the user is trying to do, in their words>

## DSPy capability
<Which DSPy modules, integrations, or patterns would power this>

## Example use case
<A concrete scenario where this skill would help>

## Suggested trigger phrases
<2-3 phrases a developer might say that should route to this skill>
EOF
)"
```

Return the issue URL to the user when done.

## Quality checklist

Validate against `docs/skill-standards.md` (the authoritative checklist). Key items:

- [ ] Description: plain YAML scalar, trigger phrases users would actually say
- [ ] SKILL.md under 500 lines with progressive disclosure structure
- [ ] Gotchas section with 3-5 Claude/DSPy-specific failure modes
- [ ] Cross-references with install hint blockquote and `/ai-do` back-link
- [ ] Code examples provider-agnostic with `# or ...` comment
- [ ] `reference.md` for `dspy-` skills (or `ai-` skills that heavily use DSPy APIs)
- [ ] README.md catalog table updated with new row
- [ ] `/ai-do` catalog updated with new routing entry

## Gotchas

- **Writing descriptions wrapped in quotes.** YAML descriptions must be plain scalars — no double quotes, no apostrophes. Claude defaults to quoting strings but this causes parse failures or ambiguity. Write `description: Monitor AI quality...` not `description: "Monitor AI quality..."`.
- **Forgetting to update `/ai-do` routing table.** New skills are invisible if `/ai-do` cannot route to them. Every PR adding a skill must also add a row to the ai-do catalog so the routing skill knows the new skill exists.
- **Building a `dspy-` skill when the user describes a problem.** If the user says "I need AI that monitors quality," build an `ai-observability` skill (problem-first), not `dspy-langfuse` (tool-first). The `dspy-` prefix is only for users who already know which DSPy concept they want.
- **Submitting a skill without testing trigger phrases.** The description determines whether Claude ever loads the skill. After writing the description, mentally simulate 3-5 ways a user might describe this need and verify at least 3 would match keywords in the description.
- **Delegating to `/skill-creator` without passing DSPy context.** If skill-creator is available, it does not know DSPy conventions by default. Always pass the DSPy-specific context block (dual naming, provider-agnostic code, reference.md pattern) or the resulting skill will not match repo standards.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Route to existing skills first** — see `/ai-do`
- **Skill format and conventions** — see repo `docs/skill-standards.md`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
