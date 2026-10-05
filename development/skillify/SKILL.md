---
name: skillify
description: "Create a reusable, self-healing, self-evolving global skill — either from the current conversation context OR from a plain-language description of a workflow. Triggers: on: 'turn this into a skill', 'make a skill from this', 'skillify this', 'capture this as a skill'."
version: "1.1.1"
category: meta
platforms:
  - CLAUDE_CODE
---

You are a skill distillation engine. Your job is to produce a production-quality,
self-healing, self-evolving Claude Code skill — either by distilling the current
conversation OR by interpreting a direct prompt description of the desired workflow.

Do NOT ask the user questions. Determine the source mode and proceed autonomously.
The result should be immediately installable and better than if the user had written it by hand.

ARGUMENTS:
$ARGUMENTS

---

## PHASE 0: DETERMINE SOURCE MODE

Parse `$ARGUMENTS` to decide how to build the skill:

**Mode A — Prompt-driven** (use when `$ARGUMENTS` contains a description of a workflow,
e.g. "a skill that analyzes PRs and posts a summary comment" or "skill that deploys to staging"):

- The arguments ARE the spec. Treat them as a natural-language description of what the skill
  should do, what inputs it takes, and what it should output.
- Derive the skill name from the description (kebab-case, 2-3 words).
- Skip reading conversation history — the prompt is the source of truth.

**Mode B — Name-only** (use when `$ARGUMENTS` is a short name with no workflow description,
e.g. "my-skill" or "deploy-flow"):

- Use the name as the target name.
- Derive the workflow from the conversation history (see PHASE 0B below).

**Mode C — No arguments** (use when `$ARGUMENTS` is empty):

- Derive both the name and workflow from the conversation history (see PHASE 0B below).

---

### PHASE 0A: PROMPT-DRIVEN SPEC (Mode A only)

Expand the prompt into a full internal spec:

1. **Core workflow** — What is the repeatable thing the skill should do? One sentence.
2. **Trigger context** — What user phrases or situations should invoke this skill?
3. **Inputs** — What does the user provide via `$ARGUMENTS`? (name, path, URL, flags, nothing?)
4. **Outputs** — What does the skill produce? (files, a report, code changes, a deployment?)
5. **Key phases** — What are the 2-5 logical stages of the work?
6. **Likely failure modes** — What could go wrong? (missing deps, empty input, API errors?)
7. **Quality criteria** — How would you know the skill did its job well?

Fill in any gaps using general knowledge and best practices. Do not wait for clarification.

---

### PHASE 0B: CONVERSATION-DRIVEN SPEC (Modes B and C)

Re-read the full conversation history and answer these internally:

1. **Core workflow** — What is the repeatable thing that was just done? One sentence.
2. **Trigger context** — What kind of user prompt would start this workflow?
3. **Inputs** — What does the user provide? (a file, a URL, a description, nothing?)
4. **Outputs** — What does the skill produce? (files, a report, code changes, a deployment?)
5. **Key phases** — What are the 2-5 logical stages of the work?
6. **Failure modes** — What went wrong (or could go wrong) during the conversation?
7. **Decisions made** — What approaches were chosen and why?
8. **Patterns that worked** — What steps consistently produced good results?

If the conversation has no clear repeatable workflow, say so:
"I can see we discussed X, but I didn't find a repeatable workflow. Can you describe the steps you'd want the skill to run?"

Use the spec as the source of truth for the rest of the skill. Do not skip it.

---

## PHASE 1: DERIVE SKILL IDENTITY

**Naming:**

- If `$ARGUMENTS` is provided, use it as-is (convert to kebab-case).
- Otherwise derive a short (2-3 word) kebab-case name from the workflow.

**Description:**

- Write a triggering description: what the skill does + when to invoke it.
- Be "pushy" — list the specific phrases, file types, or contexts that should trigger it.
- Include non-obvious triggers (e.g., "even if the user doesn't say 'deploy', use this when they say 'push to prod' or 'ship it'").

**Category:** Pick the most fitting: `build`, `deploy`, `meta`, `analyze`, `generate`, `test`, `ops`, `content`.

---

## PHASE 2: WRITE THE SKILL

Read `references/skill-anatomy.md` for the full structure guide.

Build the skill with these four embedded layers — they distinguish a self-healing,
self-evolving skill from a simple recipe:

### Layer 1: Pre-Flight Checks

Every skill opens with a validation block. Before any work begins, verify that
prerequisites exist. The goal is to fail fast with a clear message rather than
silently produce wrong output:

```
=== PRE-FLIGHT ===
Before starting, verify:
- [ ] <prerequisite 1>
- [ ] <prerequisite 2>

If any check fails:
- <recovery action or clear error message>
- Do NOT proceed until resolved.
```

Tailor the checklist to what the conversation revealed could go wrong.

### Layer 2: Phased Execution with Validation Gates

Structure the work into named phases. After each phase, add a checkpoint:

```
=== PHASE N: [NAME] ===
<instructions>

VALIDATION: [what to verify before moving on — e.g., "file exists", "tests pass", "output is non-empty"]
FALLBACK: [what to do if validation fails — try an alternative, inform the user, skip gracefully]
```

This prevents silent failures from cascading into later phases.

### Layer 3: Self-Review Scoring

At the end of the skill body, include a self-review block. The executing model
scores its own output and decides whether to iterate:

```
=== SELF-REVIEW ===
Score the output (1–5):
- Complete: Did the skill accomplish its stated goal?
- Robust: Were edge cases handled? Were fallbacks needed?
- Clean: Is the output free of noise, well-formatted, usable?

If any score is below 4:
- Identify the specific gap.
- If it's fixable in this run, fix it and re-score.
- If not, note it in the output as a known limitation.
```

### Layer 4: Learnings Capture (Self-Evolution)

At the very end of the skill, after output is delivered, append a learnings block:

```
=== LEARNINGS CAPTURE ===
After completing, append one entry to `~/.claude/skills/<skill-name>/LEARNINGS.md`:

## <YYYY-MM-DD> — <brief context of this run>
- **What worked:** <approach, tool, or pattern that produced good results>
- **What was awkward:** <step that required backtracking, retrying, or manual fix>
- **Suggested patch:** <one concrete improvement to these skill instructions>
  - e.g., "Add pre-flight check for X", "Add fallback when Y returns empty", "Skip phase Z when input is already processed"
- **Verdict:** [Smooth / Minor friction / Major friction]
```

The LEARNINGS.md file is the skill's memory. Over time it accumulates enough
signal that running `/evolve` can patch the skill based on real usage patterns.

---

## PHASE 3: WRITE LEARNINGS.MD TEMPLATE

Create `~/.claude/skills/<skill-name>/LEARNINGS.md` with this starter content:

```markdown
# <Skill Name> — Learnings Log

This file is auto-appended by the skill after each run.
Run `/evolve` periodically to apply accumulated learnings as patches.

---

## <today's date> — Initial creation

- **What worked:** Distilled from conversation context via /skillify
- **What was awkward:** n/a (first run)
- **Suggested patch:** n/a
- **Verdict:** Smooth
```

---

## PHASE 4: INSTALL THE SKILL

Write the final SKILL.md to:
`~/.claude/skills/<skill-name>/SKILL.md`

Then verify installation:

1. Confirm the file exists and is readable.
2. Confirm frontmatter is valid (name, description, version, category all present).
3. Print the first 10 lines to confirm it looks right.

---

## PHASE 5: OUTPUT SUMMARY

Report back in this format:

```
## Skill Created: /<skill-name>

**What it does:** <one sentence>
**Triggers:** <the key phrases or contexts that invoke it>
**Phases:** <N phases — list them>
**Self-healing:** <which pre-flight checks and fallbacks were embedded>
**Self-evolving:** <confirm LEARNINGS.md is in place>

**Install path:** ~/.claude/skills/<skill-name>/SKILL.md

To use: /<skill-name> [optional arguments]
To evolve after usage: /evolve
```

---

## STRICT RULES

- Do NOT ask for user approval between phases. Decide autonomously.
- Do NOT produce a shallow "recipe list." The skill must include pre-flight checks, validation gates, self-review, and learnings capture — all four layers.
- Do NOT name the skill something generic like "workflow" or "helper." The name must describe the specific thing it does.
- The description field is a triggering mechanism, not documentation. Make it work hard.
- If the conversation doesn't contain enough signal for a specific workflow (e.g., it's a back-and-forth discussion with no clear repeatable task), tell the user what you need: "I can see we discussed X, but I didn't find a repeatable workflow. Can you tell me what steps you'd want the skill to run?"
- Version starts at `1.0.0`. Bump with `/evolve` as learnings accumulate.
