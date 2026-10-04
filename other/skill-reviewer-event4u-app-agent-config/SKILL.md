---
model_tier: high
name: skill-reviewer
description: "Use when reviewing, auditing, or optimizing skills — validates against the 7 Skill Killers checklist and produces fix recommendations."
domain: quality
scope:
  write: []
  verification_reason: "execution.handler is internal, so this skill spawns no subprocess — writes happen through the agent's declared allowed_tools. No command can prove a scope the skill never executes."
execution:
  type: assisted
  handler: internal
  allowed_tools: []
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

# Skill Reviewer

## When to use

Use when reviewing, auditing, or optimizing existing skills — checking quality against the 6 Skill Killers checklist. Also for validating a new skill before saving.

Reviews skills against the **7 Skill Killers** — the most common anti-patterns
that waste tokens, cause misfires, or degrade agent performance.

## The 7 Skill Killers Checklist

### Killer 1: Vague or Quiet Description

The description is the **most critical line** — it's a trigger, not a summary.

**Good pattern:**
```yaml
description: >
  Use when the user says "create a DTO", "new data transfer object",
  or asks to convert request/response data into a typed PHP class.
  Also triggers on "map this to a DTO" or "I need a value object".
  Creates DTO classes following project conventions with SimpleDto
  base class, attribute mapping, and validation.
```

**Bad patterns:**
- ❌  `"Creates DTO classes following project conventions"` — no trigger phrases
- ❌  `"Handles DTOs"` — too vague, won't fire
- ❌  Only describes WHAT, never WHEN

**Fix rules:**
- Start with `Use when the user says "..."` or `Use when [situation]`
- Include 3-5 trigger phrases people actually say
- Write in third person (injected into system prompt)
- Be LOUD — models skip past quiet descriptions
- End with 1 sentence describing what the skill does
- For explicit-only skills: `"ONLY when user explicitly requests: [X]. NOT for [Y]."`

### Killer 2: Over-Defining (Railroading)

The skill dictates every micro-step instead of guiding.

**Check:** Are there >15 numbered steps? Does it prescribe HOW to think?
**Fix:** Set degrees of freedom — tight for fragile ops (migrations, deployments),
loose for creative tasks (design, planning). Use bullets over numbered steps
when order doesn't matter.

### Killer 3: Stating the Obvious

Content the model already knows — wasting tokens on every invocation.

**Check:** For each paragraph, ask: "Does the model really need this?"
**Examples of waste:**
- ❌  Explaining what PHP strict types do
- ❌  Describing how Laravel middleware works (in a middleware skill)
- ❌  Listing basic Git commands

**Keep only:** Project-specific conventions, non-obvious patterns, YOUR way of doing things.

### Killer 4: Missing Gotcha Section

The highest-signal content in a skill. Documents failure patterns.

**Check:** Does the skill have a `## Gotcha` or `## Common Mistakes` section?
**Fix:** Add one with real failure patterns:
```markdown
## Gotcha

- Don't assume X — check Y first because Z
- The model tends to forget A when doing B
- Edge case: when C happens, do D instead of E
```

### Killer 5: Monolithic Blob

Skill exceeds size limits (see `docs/guidelines/agent-infra/size-and-scope.md`).

**Check:** Review at >400 lines. Strongly consider split at >1200 words / >1500 words.
**Fix:** Extract reference tables, templates, and examples into separate files
in the skill folder, or split by responsibility.

### Killer 6: Guideline-Dependent (Pointer-Only)

The skill delegates to guidelines instead of containing its own executable workflow.

**Iron Rule:** If a skill is not executable without opening a guideline, it is broken.

**Check:** Cover all guideline references in the skill — is the Procedure still executable?
**Litmus test:** Remove `→ See guideline ...` lines. Does the skill still tell the agent what to do?

**Fail if:** ≥3 guideline delegations AND ≤1 action verb AND <3 procedure steps
**Warn if:** ≥2 guideline delegations AND ≤2 action verbs AND <3 procedure steps

**Fix:** Inline the essential workflow steps from the guideline. Keep the guideline reference
for deep-dive details, but the Procedure must work standalone.

### Killer 7: Created Without Analysis

The skill/rule/command was written without inspecting existing state or defining expected behavior.

**Check:** Was the artifact created based on:
- Reading the existing implementation or related artifacts?
- Comparing with current behavior, tests, or requirements?
- Defining expected behavior before writing?
- Using targeted tools for investigation?

**Fail or warn if:**
- No evidence of inspecting existing state before creating/refactoring
- Looks like blind trial-and-error or copy-paste-and-hope
- Expected behavior is only implied, never explicitly stated
- Refactor made artifact cleaner but weaker (lost validation, examples, or gotchas)
- Requirements were ambiguous but no clarification was sought

**Fix:** Add analysis step, define expected outcome, verify with linter/tests, restore any lost content.

## Pre-check: Should this be a skill at all?

Before scoring the 5 Killers, ask: **Does this belong as a skill?**

| If the content is... | Verdict |
|---|---|
| Standard tool usage (jq, docker exec, git commands) | ❌ **Not a skill** — baseline model knowledge |
| Single-command operations without decision logic | ❌ **Not a skill** — too thin for a workflow |
| Always-true constraint ("never X", "always Y") | ❌ **Not a skill** — should be a Rule |
| Coding conventions / reference material | ❌ **Not a skill** — should be a Guideline |
| Step-by-step workflow with decisions and validation | ✅ **Skill** — proceed with review |
| Error-prone process that models get wrong without guidance | ✅ **Skill** — even if steps seem simple |

If the skill fails this pre-check → recommend: migrate (rule/guideline), absorb (into existing skill), or delete.

## Structural Validation (pre-review)

Before scoring the 5 Killers, verify structure:

**Skills** — required sections:
- When to use (with "Do not use when")
- Procedure (numbered steps OR `###` sub-headings — NOT just a renamed heading with prose)
- Concrete validation step inside Procedure (must contain: verify, confirm, must pass, run test, etc.)
- Gotchas
- Do NOT

**Linter:** Run `./scripts-run src/scripts/skill_linter` on any skill after review — must be 0 FAIL.

**Rules** — must be:
- Short and directive
- Always-applicable (no situational triggers)
- Not procedural (no numbered steps — that's a skill)

**Condensation safety** (if condensed version exists):
- Trigger clarity preserved
- Decision hints or equivalent present
- Concrete validation still present
- Gotchas/anti-failure protection retained

**Merge/refactor safety** (if reviewing a merge, refactor, or restructuring):
- Apply `preservation-guard` rule checklist
- Strongest validation, example, and anti-pattern must survive
- Scope must not broaden from merging unrelated concerns
- Strong language must not be weakened

**Scope check:**
- No overlap with existing skill or rule (name + description)
- Single workflow per file (multiple workflows → split)
- Update existing preferred over creating new file

## Procedure: Review a skill

### Single skill
1. Validate structure (required sections present)
2. Score each killer: ✅ Pass / ⚠️ Weak / ❌ Fail
3. Check condensation safety (if applicable)
4. Produce a verdict table + specific fix suggestions

### Batch audit
1. Scan all skills in `.augment/skills/`
2. For each: check description format, line count, gotcha presence
3. Produce a summary table sorted by severity
4. Group fixes by type (e.g., "these 20 need description rewrites")

## Output Format

```markdown
| Skill | K1 Desc | K2 Over | K3 Obvious | K4 Gotcha | K5 Size | K6 Pointer | K7 Analysis | Verdict |
|---|---|---|---|---|---|---|---|---|
| laravel-dto | ❌ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | Fix description |
```

## Output format

1. Review report with pass/fail per checklist item
2. Prioritized fix recommendations — ordered over the **complete** per-killer table above, never a subset of it. Priority is a sort, not a filter.

## Gotcha

- Don't rewrite skills unnecessarily — only fix actual killer violations.
- A description that works (triggers correctly) is fine even if not perfect.
- Gotcha sections grow organically — seed them, don't force 10 entries.
- "Stating the obvious" is relative to the MODEL, not to junior developers.
  If the model consistently gets something wrong, it's NOT obvious — keep it.
- Skills under 50 lines rarely have Killer 5 problems — skip that check.
- Flag any "Related skills" section — the agent discovers skills via `<available_skills>` descriptions. Cross-links waste tokens and create maintenance burden. Recommend removal.


## Do NOT

- Do NOT rewrite skills that pass all 7 killers — leave them alone.
- Do NOT add "Related skills" cross-links — the agent discovers via descriptions.
- Do NOT force Gotcha entries — seed naturally from real failures.