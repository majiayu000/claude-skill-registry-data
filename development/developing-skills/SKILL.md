---
name: developing-skills
description: >
  Provides authoritative guidance for creating and managing Claude skills
  following Anthropic best practices across both Cowork plugin skills and
  Claude Code skills. Covers skill structure, YAML frontmatter, trigger phrase
  density, gerund naming, progressive disclosure patterns, evaluation-driven
  authorship, the 500-line rule, enforcement levels, hook mechanisms, and
  session tracking. Activates when creating new skills, modifying
  skill-rules.json, understanding trigger patterns, working with hooks,
  debugging skill activation, or implementing progressive disclosure. Also
  triggers on: how do I write a skill, SKILL.md not working, skill not firing,
  write a SKILL.md, skill authoring guide, or how do skills work.
version: "2.0.0"
---

# Developing Skills — 2026 Authorship Guide

Authoritative guide to skill authorship across Cowork plugins and Claude Code. Covers everything from YAML frontmatter to evaluation-driven development to the 500-line rule.

## Quick-Start Decision Tree

```
What are you building?
  ├─ Cowork plugin skill ──────── Uses SKILL.md in plugin structure, triggers via description matching
  ├─ Claude Code project skill ── Uses .claude/skills/{name}/SKILL.md, triggers via hooks + rules
  ├─ Claude Code personal skill ─ Uses ~/.claude/skills/{name}/SKILL.md, same mechanics
  └─ Unsure ────────────────────── Start with Cowork plugin skill (wider reach, simpler activation)
```

---

## Usage Examples

**Example 1 — Create a new Cowork skill from scratch**
User: "Build a skill that helps write API documentation."
→ Pick gerund name: "documenting-apis". Write 3 eval scenarios first. Then write SKILL.md with frontmatter, decision tree, examples, golden path, and self-verification. Add references/ if over 100 lines.

**Example 2 — Debug a skill that isn't triggering**
User: "My skill never activates even when I mention the right keywords."
→ Check: Is the description keyword-dense enough? Does the name match the directory? Is the YAML frontmatter parseable? For Claude Code: are hooks registered in settings.json?

**Example 3 — Convert a Claude Code skill to a Cowork plugin skill**
User: "I have a .claude/skills/ skill. Make it work in Cowork."
→ The activation mechanism changes. Cowork matches on description text, not hook-based rules. Rewrite the description to be trigger-phrase dense. Package in plugin structure with manifest.

---

## Cowork Plugin Skills vs. Claude Code Skills

These are different contexts with different activation mechanisms.

### Cowork Plugin Skills

Activation is driven by the `description` field in SKILL.md frontmatter. The Cowork runtime matches user prompts against skill descriptions to decide which skills to surface. There is no hook system — activation is purely description-based.

**Key implications:** The description must contain every keyword and phrase that should trigger the skill. A skill with a vague description will never activate. Trigger phrase density is the single most important factor.

**Structure:** Lives inside a plugin directory: `plugin-name/skills/skill-name/SKILL.md`. May include reference files in subdirectories.

### Claude Code Skills

Activation is driven by hooks (UserPromptSubmit, PreToolUse, Stop) configured in `.claude/hooks/` and rules in `.claude/skills/skill-rules.json`. Much more granular control: you can trigger on file paths, content patterns, intent regex, and explicit keywords.

**Key implications:** The hook system allows blocking enforcement (exit code 2 prevents tool execution), session tracking (don't repeat in same session), and file-path-based triggers. Skills can be guardrails (block) or advisory (suggest).

**Structure:** Lives at `.claude/skills/{name}/SKILL.md` (project) or `~/.claude/skills/{name}/SKILL.md` (personal).

---

## Evaluation-Driven Authorship

Write 3 or more eval scenarios before writing any documentation. This prevents over-engineering skills that don't trigger correctly.

### Process

1. **Write 3 eval prompts** — real user messages that should trigger this skill
2. **Write 2 negative evals** — messages that should NOT trigger this skill
3. **Test activation** — does the skill fire on the positive evals and stay silent on negatives?
4. **Only then write the full SKILL.md** — you now know what trigger phrases matter

### Eval Template

```markdown
## Eval: [skill-name]

### Should trigger:
1. "Build me an API documentation generator"
2. "How do I document my REST endpoints?"
3. "Create OpenAPI specs for this service"

### Should NOT trigger:
1. "Write a blog post about APIs" (content creation, not documentation)
2. "Debug this API endpoint" (debugging, not documenting)

### Observed behavior:
- Eval 1: [PASS/FAIL] — triggered / did not trigger
- Eval 2: [PASS/FAIL]
- ...
```

---

## Skill Structure

### YAML Frontmatter (Required)

```yaml
---
name: gerund-name-here          # Must match directory name exactly
description: >                  # Third-person, keyword-dense, max 1024 chars
  Generates API documentation from source code and OpenAPI specs.
  Activates when creating docs, generating OpenAPI, documenting endpoints,
  writing API reference guides, or producing developer documentation.
version: "1.0.0"               # Semver
allowed-tools: Bash, Read, Write, Edit  # Optional: restrict tool access
---
```

### Gerund Naming

The first hyphen-separated segment must end in "-ing". This convention makes skill names read as actions: "What is this skill doing? It is documenting-apis."

**Valid:** documenting-apis, building-dashboards, tracking-expenses
**Invalid:** api-documenter, dashboard-builder, expense-tracker

### Description — Trigger Phrase Density

For Cowork skills, the description IS the trigger. Pack it with every synonym, variant, and related phrase a user might say.

**Bad (sparse):** "Helps with API docs."
**Good (dense):** "Generates API documentation from source code, OpenAPI specs, and inline comments. Activates when creating API docs, generating OpenAPI specifications, documenting REST endpoints, writing developer reference guides, producing SDK documentation, or building API portals."

**Rule of thumb:** 4–6 trigger phrases minimum. Each phrase should be a distinct way a user might describe the task.

---

## The 500-Line Rule

SKILL.md must not exceed 500 lines. This is enforced by the validator as a FAIL.

### How to Enforce

If your skill needs more than 500 lines of content, split into progressive disclosure:

1. **SKILL.md** (under 500 lines) — TL;DR, decision tree, examples, golden path, key rules, self-verification, CLAIMS footer
2. **references/** — detailed content organized by topic

### Valid Subdirectories

Any of these count for progressive disclosure: references/, examples/, resources/, scripts/, templates/, workflows/, assets/. The validator accepts any of them.

### What Goes Where

**In SKILL.md:** Everything a user needs for 80% of use cases. The decision tree, 3+ examples, the primary workflow, key constraints, and the self-verification checklist.

**In references/:** Deep dives, pattern libraries, troubleshooting guides, advanced configurations, edge case documentation. One topic per file, no cross-linking between reference files (nested refs are a FAIL).

---

## Enforcement Levels (Claude Code Only)

### BLOCK
Exit code 2 from hook. Prevents Edit/Write tool execution. Claude sees error message and must use skill to proceed. Use for critical mistakes: data integrity, security, column name verification.

### SUGGEST
Reminder injected before Claude processes the prompt. Advisory — Claude is aware but not forced. Use for domain guidance, best practices, architectural patterns. This is the most common level.

### WARN
Low-priority advisory. Minimal enforcement. Rarely used — most skills are either BLOCK or SUGGEST.

---

## Hook Mechanisms (Claude Code Only)

### UserPromptSubmit
Fires before Claude sees the user's prompt. Injects skill suggestions as context via stdout. Used for topic-based activation and implicit work detection.

### PreToolUse
Fires before a tool executes. Can block execution (exit code 2). Used for guardrail skills that prevent edits to files without verification.

### Stop
Fires after Claude finishes responding. Used for gentle post-response reminders (e.g., "did you handle errors in the code you just wrote?"). Does not block.

See the Hook Mechanisms reference for detailed flow diagrams, exit code behavior, and session state management.

---

## Skip Conditions

**Session tracking:** First trigger blocks/suggests. Same session, same skill, same context — skips to avoid nagging. State stored in `.claude/hooks/state/`.

**File markers:** `// @skip-validation` in a file permanently skips guardrail checks for that file. Use sparingly.

**Environment variables:** `SKIP_SKILL_GUARDRAILS=true` disables all PreToolUse blocks. Emergency escape hatch only.

---

## Pre-Flight: Research Before Writing

If the skill wraps or coaches an **established methodology, framework, or specification** (e.g., SPARC, TDD, Shape Up, OWASP, RFC process, Design Sprints, DORA), **search for authoritative sources before writing a single line of SKILL.md**. Do not paraphrase from memory. Do not invent phase names or step counts. Go get the canonical definition.

```
Does this skill wrap an established methodology?
  ├─ Yes → web_search for authoritative source, read it, then write the skill
  └─ No (original workflow, internal process) → proceed to Golden Path directly
```

**Why this matters:** A skill that misrepresents SPARC, TDD, or any other named methodology will produce incorrect coaching and confuse users who know the real thing. Wrong phase names, missing steps, and invented constraints are worse than no skill at all.

**What to search for:** The original author or canonical repo (e.g., `ruvnet/sparc GitHub`, `Kent Beck TDD`, `Ryan Singer Shape Up`). Read the primary source, not a summary blog.

---

## Golden Path: Creating a Skill End-to-End

1. **Research first** — if wrapping an established methodology, search authoritative sources before writing
2. **Name it** — gerund form, lowercase, hyphens (e.g., documenting-apis)
3. **Write 3 eval scenarios** — what prompts should trigger it?
4. **Write the description** — trigger-phrase dense, third-person, max 1024 chars
5. **Write SKILL.md** — TL;DR, decision tree, 3 examples, golden path, self-verification, CLAIMS footer
6. **Add references/** — required if SKILL.md exceeds 100 lines; split deep content there
7. **Test evals** — do positive evals trigger? Do negative evals stay silent?
8. **Validate** — run validate_skills.py, confirm 0 WARN 0 FAIL
9. **Package** — use the packaging-skills skill for distribution

## Power Path: Advanced Patterns

For Claude Code skills with hooks: configure skill-rules.json with keyword triggers, intent patterns, file path globs, and content detection regex. Add session tracking. Test hooks manually with `npx tsx`. See the Trigger Types, Skill Rules, and Patterns Library references.

## Edge Case: Skill Won't Trigger

Check in order: (1) description is keyword-dense enough, (2) YAML frontmatter is valid (no syntax errors), (3) name matches directory name exactly, (4) for Claude Code: hooks are registered in settings.json, (5) for Cowork: the skill is inside a properly structured plugin. See the Troubleshooting reference.

---

## Self-Verification Checklist

Before shipping a skill:
0. If skill wraps an established methodology: authoritative source was searched and read first
1. Name is gerund form and matches directory name
2. Description is third-person, keyword-dense, under 1024 chars
3. SKILL.md is under 500 lines
4. 3+ eval scenarios written and tested
5. references/ subdirectory present if SKILL.md exceeds 100 lines
6. No nested references (reference files don't link to siblings)
7. No placeholders — every section has substantive content
8. CLAIMS/COUNTEREXAMPLE/CONTRADICTIONS footer present
9. Validator passes with 0 WARN 0 FAIL

---

## CLAIMS
- Trigger phrase density in the description is the single most important factor for Cowork skill activation
- Evaluation-driven authorship (write evals first) produces better-triggering skills than documentation-first approaches
- The 500-line rule forces progressive disclosure, which improves skill readability and maintenance

## COUNTEREXAMPLE
- A skill with a perfectly dense description can still fail to activate if the YAML frontmatter has a syntax error that prevents parsing
- Eval-first authorship can lead to over-fitting: a skill tuned to 3 specific prompts may miss valid variations

## CONTRADICTIONS
- "Pack the description with trigger phrases" conflicts with "max 1024 chars" — you will run out of space for genuinely complex skills
- "Write evals before documentation" assumes you know the trigger space upfront, but some skills emerge from documentation work
