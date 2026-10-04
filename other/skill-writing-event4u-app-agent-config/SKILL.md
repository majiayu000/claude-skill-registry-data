---
model_tier: inherit
name: skill-writing
description: "Use when deciding 'should this be a skill or a rule?', creating/improving/reviewing agent skills, SKILL.md frontmatter, or procedure sections — even without saying 'skill-writing'."
source: project
domain: process
meta_skill: true
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

# skill-writing

## When to use

Use this skill when:

* Creating a new skill from scratch
* Improving an existing skill
* Reviewing skill quality
* Deciding what belongs in a skill vs a rule

Typical examples:

* "Create a skill for X"
* "This skill needs improvement"
* "Should this be a skill or a rule?"

Do not use this skill when:

* Writing rules (rules are constraints, not workflows)
* Writing commands (commands are direct invocations)

## Goal

* Create executable skills, not documentation
* Ensure every skill answers: When? How? What output?
* Prevent common mistakes: too broad, too generic, missing validation

## Preconditions

* Clear understanding of the intended task
* Distinction: rules = always apply, skills = triggered workflows
* Access to a skill template or existing reference skill

## Decision matrix: What goes where?

Before creating anything, classify the content:

| If the content is... | Then it is... | Action |
|---|---|---|
| An always-true constraint ("never X", "always Y") | **Rule** | Create/update `.augment/rules/` |
| A step-by-step workflow with decisions and validation | **Skill** | Create/update `.augment/skills/` |
| A coding convention or reference material | **Guideline** | Create/update `.augment/guidelines/` |
| Baseline model knowledge (how jq works, what `docker exec` does) | **Nothing** | Do not create anything |
| Simple tool usage without complex workflow | **Nothing** | Do not create anything |
| Already covered by an existing skill/rule/guideline | **Update** | Extend the existing file |

### The critical test

Ask: **"Does the model need this to do its job correctly?"**

* If the model already knows it → **Nothing**
* If the model knows it but does it wrong in THIS project → **Rule or Guideline**
* If the model needs a multi-step workflow to get it right → **Skill**

### Skills and commands share the `.claude/skills/` namespace

Skills in `src/skills/{name}/SKILL.md` AND commands in
`src/domains/{domain}/{name}/command.md` both project into
`.claude/skills/` (see `scripts/condense.ts` →
`generate_claude_skills` + `generate_claude_commands`). Claude treats
the whole directory as native skills.

Implications for skill authors:

* If a same-name command already exists, the skill takes priority and
  the command is skipped (`generate_claude_commands` honors this).
  Don't reuse a command's slug for a skill unless the command should
  retire.
* Both artifacts compete on `description` for routing. A weak skill
  description is shadowed by a stronger same-domain command — and vice
  versa. Make trigger phrasing precise (§ 1b below).
* When the workflow has both a "user types `/foo`" path AND a "model
  picks this up from intent" path, author the skill first and let the
  command delegate (`skills:` frontmatter). Two artifacts with the same
  trigger surface fight each other in the router.

### When "Nothing" is the right answer

Do NOT create a skill or rule for:

* Standard tool usage (jq, grep, docker exec, git commands)
* Framework basics the model already knows
* Single-command operations without decision logic
* Knowledge that belongs in a skill's procedure as a step, not as its own skill

### Size and structure hints

→ See `docs/guidelines/agent-infra/size-and-scope.md` for full limits.

* Target: 300–900 words. Review for split above 1200 words. Strongly consider split above 1500 words.
* Over the 400-line K6 cap → the **router-head contract** in `templates/skill.md`
  applies: entry head (when-to-use · mode table · routing) plus one `tasks/` or
  `references/` file per mode, and the head never inlines more than one mode's
  procedure. Gated by `lint_skill_router_head` with a shrink-only allowlist.
* If multiple workflows exist → split into multiple skills
* If two skills overlap heavily → merge
* If a skill becomes "read the guideline" → it lost its purpose, restore the workflow

### Progressive disclosure — the directory is `references/`, plural

When a skill needs depth the workflow does not, the depth goes in a
**`references/`** subdirectory beside `SKILL.md` — that exact name, plural. It
was two spellings across nine skills until 2026-08-12 because nothing here
named one; the split cost a rename, not a decision.

* **Body:** the trigger, the workflow, the ownership statement, and every
  heuristic that changes a write decision. A skill whose body is a map to its
  own content is loaded and not applied.
* **`references/`:** corpora, lookup tables, long schemas, worked examples —
  read on the path that needs them, never on every activation.

Splitting is not a size escape hatch. The measured estate (n=289, 2026-08-12):
median 1,077 words, p90 1,867, **only 6 skills above 2,500 and 4 above 3,000**.
So a skill at 1,500 words is ordinary, and moving prose out of the body to hit
a number makes it worse. Split when the material is genuinely
consulted-on-demand; keep the load-bearing part in the body even when that
leaves the file long.

A `references/` split does not change the gates that already apply: a
`token_budget_class: rich` skill still meets its 3,500-token ceiling on the
body alone.

## Modes

This skill is a router head. The decision layer above — what goes where, the
critical test, the namespace note, the size and progressive-disclosure hints —
is true across every mode and stays here, as do the Frugality Standards below.
The procedure body and the section-pattern catalogue live in `references/`; load
the one the task calls for.

| Task | Mode body | Covers |
|---|---|---|
| Author a new skill, or rewrite one end to end | [`references/procedure.md`](references/procedure.md) | Steps 0 → 7: inspect + Drafting Protocol, skill-growth gate, trigger definition, pushy description, trigger-eval stub, procedure, validation, safe/unsafe example, output format, quality checklist, eval loop |
| Pick or write an optional / required section pattern | [`references/section-patterns.md`](references/section-patterns.md) | Description-optimizer loop, self-QA loop, known-pitfalls, rationalizations-to-reject, non-negotiable-deliverable, destructive-operation gates, upstream-version-notes, security-constraints, action-reference split, mechanism-teaching, illustrative-not-verbatim, headline metric, contrastive-example |
| Ship a script inside a skill | [`references/read-only-scripts.md`](references/read-only-scripts.md) | The read-only-by-default rule and its allowlist, whose violation fails the build |

## Procedure

1. **Inspect first.** Read the existing skill (or the nearest three matches) and
   run the decision matrix above before writing anything. If the answer is
   "Nothing", stop — that is a real answer and the cheapest one.
2. Authoring or rewriting a skill → load
   [`references/procedure.md`](references/procedure.md) and follow steps 0 → 7
   in order. The steps are sequenced, not a menu.
3. Reaching for a named section pattern → load
   [`references/section-patterns.md`](references/section-patterns.md) and use
   the one pattern that matches; the catalogue is not a checklist to satisfy.
4. **Validate before saving** — the quality checklist in
   [`references/procedure.md`](references/procedure.md) § 6, the Frugality
   Standards below, and `./scripts-run src/scripts/skill_linter` at 0 FAIL.

## Output format

1. Complete SKILL.md file
2. No explanations outside the file
3. Fully copyable
4. No empty sections

## Core rules

* Skills are executable thinking processes
* Always include: When to use, Procedure, Output format, Gotchas, Do NOT
* Steps must be verifiable
* Validation must be concrete
* One skill = one job

### Cross-references and paths

* Body links to guidelines / contracts use the verbatim relative form
  (`../../docs/guidelines/<group>/<name>.md`,
  `../../docs/contracts/<name>.md`). The condense-time rewriter
  resolves them to depth-aware single-up form — do not pre-rewrite in
  source.
* Skills do **not** declare `load_context:` / `load_context_eager:`;
  those frontmatter keys are rule-only. If a skill needs to point at a
  context, link to it inline (`[context-name](../../contexts/<area>/<file>.md)`).
* Never write `.agent-src.uncondensed/` in any skill body link or
  example — it ships into `.augment/skills/` and breaks consumer
  resolution. See `rule-writing` § 3b for the canonical reference.

### Execution metadata (optional)

Skills may declare an `execution` frontmatter block (`type`, `handler`,
`timeout_seconds`, `safety_mode`, `allowed_tools`). Default is `manual`
(instructional only). See `docs/guidelines/agent-infra/runtime-layer.md` for
the full specification and `assisted` / `automated` semantics.

### When to create a `project-analysis-*` skill

Only if the framework has its own lifecycle producing unique debugging
patterns that `project-analysis-core` cannot explain (e.g. Laravel,
Symfony, Express, React, Next.js). **Not** for Tailwind, CSS frameworks,
utility libs, or simple state managers.

## Gotchas

* Writing documentation instead of executable steps
* Skipping validation — every Procedure MUST end with a concrete verify step
* Including baseline knowledge the model already has
* Description too long or not a trigger
* Renaming a heading to "Procedure:" without numbered steps or `###` sub-headings
* **Always run `./scripts-run src/scripts/skill_linter` before saving — 0 FAIL required**

## Frugality Standards

Apply the [Frugality Charter](../../contexts/contracts/frugality-charter.md)
to every skill you author.

**Examples in this artifact:**
- Per the charter's default-terse rule, the SKILL.md `## Procedure`
  opens with the action ("Run the linter"), not "Let me walk you
  through…".
- Per the cheap-question check, only emit numbered-options output
  when consequences differ — never as a stylistic choice.
- Per the post-action summary suppression, the example output ships
  the artifact, not a wrapping `## Status` / `## Summary` block.

**Scope-exclusion clause.** A skill can shed assumed-knowledge prose without
losing correctness by naming what it does NOT cover: "this skill covers only
`<X>`; standard `<Y>` is assumed". One sentence replaces the paragraph that
would otherwise re-teach `<Y>`, and it is stronger than silence — a reader who
does not have `<Y>` learns that from the clause instead of from a wrong result.

**Pre-save self-check:**
1. Does any procedure step open with "Let me", "Now I will", "Found
   it", "OK", or "Alright"?
2. Does the skill prescribe numbered-options output without a real
   consequence trade-off?
3. Does the example output include a post-action summary block?
4. Does the description carry filler ("comprehensive", "advanced",
   "powerful")?


## Section patterns

The thirteen optional and required section patterns moved verbatim to
[`references/section-patterns.md`](references/section-patterns.md). Two of them
are marked **required** for a named population — security-constraints for
script-bearing skills, and the action-reference split for `safety_mode: strict`
skills — so a skill in either population reads that file rather than skipping it.
The read-only-by-default script rule moved to
[`references/read-only-scripts.md`](references/read-only-scripts.md).

## Do NOT

* Write documentation-style, pointer-only, or too-broad skills ("Laravel skill", "Django skill")
* Skip Procedure or use vague validation
* Exceed size limits (see `docs/guidelines/agent-infra/size-and-scope.md`)
* Duplicate rules
* Ship a skill script that mutates the filesystem on its default invocation — gate it behind a flag or allowlist it with a rationale

## Encode usage policy in the description

Workflow sequencing, preconditions, ID/output provenance ("copy ids verbatim,
never from memory"), a mandatory "why" intent field, and turn-end contracts
belong INSIDE this artifact's description/frontmatter — where they fire at the
decision point — not in always-on prose. See
[`tool-description-as-policy`](../../../docs/guidelines/agent-infra/tool-description-as-policy.md).
