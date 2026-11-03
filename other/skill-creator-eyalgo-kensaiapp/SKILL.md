---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, update or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
license: MIT
compatibility: Claude Code CLI
metadata:
  version: "1.6.1"
  created: "2025-02-01"
  category: meta
  tags: automation, skill-creation, evals, benchmarking, description-optimization
  risk: safe
  depends-on: skill-evals, skill-evals-creator, skill-evals-trigger
---

<!-- Changed from Anthropic's skill-creator (Apache-2.0, https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator); this file is not the original. -->

# Skill Creator

A skill for creating new skills and iteratively improving them.

Assess where the user is in the process and jump in accordingly: they may need help defining the skill from scratch, or they may already have a draft and need to go straight to eval/iterate. Stay flexible — if the user wants to skip formal evaluation and iterate conversationally, that's fine too. After the skill is complete, offer to run description optimization to improve triggering accuracy.

---

## Communicating with the user

Users span a wide range of technical familiarity. "Evaluation" and "benchmark" are generally OK; "JSON" and "assertion" need clear signals from the user before using them without definition. When in doubt, add a brief inline explanation.

---

## Creating a skill

### Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow the user wants to capture (e.g., they say "turn this into a skill"). If so, extract answers from the conversation history first — the tools used, the sequence of steps, corrections the user made, input/output formats observed. The user may need to fill the gaps, and should confirm before proceeding to the next step.

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Should we set up test cases to verify the skill works? Skills with objectively verifiable outputs (file transforms, data extraction, code generation, fixed workflow steps) benefit from test cases. Skills with subjective outputs (writing style, art) often don't need them. Suggest the appropriate default based on the skill type, but let the user decide.

### Interview and Research

Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies. Wait to write test prompts until you've got this part ironed out.

Check available MCPs - if useful for research (searching docs, finding similar skills, looking up best practices), research in parallel via subagents if available, otherwise inline. Come prepared with context to reduce burden on the user.

### Write the SKILL.md

Based on the user interview, fill in these components:

- **name**: Skill identifier (kebab-case)
- **description**: Primary triggering mechanism — what the skill does and when to use it. Combined with `when_to_use`, truncated at 1,536 chars in the skill listing. Make descriptions slightly "pushy" to counter Claude's tendency to undertrigger: instead of "How to build a dashboard", write "How to build a dashboard. Use this skill whenever the user mentions dashboards, data visualization, or wants to display company data, even if they don't explicitly ask for a 'dashboard.'"
- **when_to_use** (optional): Additional trigger context appended to `description` in the listing — trigger phrases, example requests, edge-case hints. Counts toward the 1,536-char cap. keep all trigger guidance in frontmatter (`description` or `when_to_use`), not the SKILL.md body. Note: Anthropic supports body "When to Use" sections .
- **license**: MIT
- **Other optional fields** — Anthropic supports `allowed-tools`, `disallowed-tools`, `argument-hint`, `arguments`, `model`, `effort`, `context`/`agent` (run in a forked subagent), `hooks`, `paths`, `disable-model-invocation`, `user-invocable`. Use when the skill needs tool permissions, model overrides, path scoping, or named argument substitution.
- **the rest of the skill :)**

### Skill Writing Guide

#### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name + description required; license required; when_to_use + other fields optional)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### README.md Convention

Skills follow a two-tier README convention based on complexity:

**Simple skill** (single SKILL.md, no agents/, no evals/, no non-obvious structure): no README.md. All metadata goes in SKILL.md frontmatter under `metadata:`.

**Complex skill** (has agents/, has evals/, or invokes other skills): create README.md alongside SKILL.md. README.md is human-readable documentation — not a metadata overflow file.

Required README.md sections for complex skills:
- **Lead paragraph** — the problem this skill solves and why it exists (not a repeat of the description)
- **`## What It Does`** — bullet list of capabilities
- **`## File Structure`** — annotated directory tree
- **`## Depends On`** — only if the skill actively invokes another skill
- **`## When to Use`** — human-readable version of the triggers (complements the description, written for a developer reading the repo)

**File reference integrity**: every file listed in `## File Structure` and in SKILL.md's Reference Files section must exist on disk. Write the file first, then add it to the tree. Don't add entries for files you intend to create later.

Do NOT include a `## Metadata` table in README.md. All metadata (version, author, created, category, tags, risk, depends-on) goes in SKILL.md frontmatter under the `metadata:` map:

```yaml
metadata:
  author: Your Name
  version: "1.0.0"
  created: "YYYY-MM-DD"
  category: <category>
  tags: tag1, tag2
  risk: safe
  depends-on: other-skill  # only if applicable
```

#### Progressive Disclosure

Three loading levels: **Metadata** (always in context, ~100 words), **SKILL.md body** (in context when triggered, <500 lines ideal), **Bundled resources** (loaded as needed, unlimited). Keep SKILL.md under 500 lines — if approaching the limit, move content to `references/` with clear pointers. For reference files over ~300 lines, add a table of contents.

**Domain organization**: When a skill supports multiple domains/frameworks, organize by variant:
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude reads only the relevant reference file.

#### Writing Patterns

Use the imperative form in instructions. Define output formats with an explicit template block (e.g., `ALWAYS use this exact template: ...`). Include examples using `Input:`/`Output:` pairs when the transformation is concrete.

When a skill supports multiple output formats, mode routing must connect an intake signal (user's stated goal, audience, or scope) to a specific output format via an explicit if-then or table — not a free-standing scope variant menu.

When a skill defines output templates, every template must include a named `##` section for missing or unavailable data — e.g., `## Intelligence Gaps`, `## Data Gaps`, `## What We Don't Know`. Handle incomplete information in the template itself; a shared global footer or inline prose is not sufficient.

### Writing Style

Explain why things matter rather than issuing heavy-handed MUSTs. Keep the skill general — not narrowly fit to your test examples. Write a draft, then read it with fresh eyes before finalizing.

### Test Cases

Delegate authoring the behavior evals to the `skill-evals-creator` skill. Invoke it with the skill path and the mode: **Mode 1 (TDD)** when the SKILL.md doesn't exist yet — design evals from the intent description — or **Mode 2 (post-skill)** when the SKILL.md already exists. `skill-evals-creator` owns the full eval-authoring loop: designing 3–5 realistic test cases, writing structural-first assertions, showing them to the user for confirmation, and saving `evals/evals.json`.

Do not hand-write `evals/proposed-evals.md` or `evals/evals.json` yourself. Inlining eval authoring here drifts from the shared schema and assertion rules that `skill-evals-creator` owns — the same reason eval *running* is delegated to `skill-evals` below.

Step-by-step instructions and the evals.json schema live in `<CORE>/../skills/interactive/.claude/skills/skill-evals-creator/SKILL.md`.

---

## Running and evaluating test cases

Delegate to the `skill-evals` skill. Invoke it with the skill path being evaluated. `skill-evals` owns the full eval loop: spawning parallel with-skill and without-skill runs, grading, aggregation, and launching the viewer.

File structure, workspace paths, and all step-by-step instructions are in `<CORE>/../skills/experimental/.claude/skills/skill-evals/SKILL.md`.

---

## Improving the skill

### Before improving: check what the body's rule is copied into

A skill's rule is rarely stated once. It lives in the `SKILL.md` body, and again in whatever the body routes through — a `references/` template the run copies its shape from, an example, a sibling skill that restates it. **Change the body and the copies keep the old rule**, and the copy usually wins, because the template is what a drafting run actually opens.

Before editing a rule, list its copies: `grep` the skill's own folder for the rule's distinctive phrase, then the `references/` templates for the field or vocabulary it governs, then the sibling skills that cite this one. Change them together or say in the commit which were deliberately left.

Measured in this instance: a field retired in a body stayed in three templates for two months and nine separate audits, each filing it as a fresh finding, because no run that changed the body was asked what the body was copied into.

### Before improving: read the trigger eval data

If `<skill-dir>/evals/trigger-eval.json` (or `<skill-dir>/evals/<eval-name>/trigger-eval.json`) exists, read it first. It contains labeled queries — `should_trigger: true/false` — that are the ground truth for whether the skill's description is working. Use it to identify *specific* queries the current description would fail on, not just general domain gaps. Quote those queries in your gap analysis before proposing description changes.

### After improving: verify the description

After writing the updated SKILL.md, before running the full eval loop:

1. Re-run the specific trigger-eval queries that were previously failing — confirm they now pass.
2. Run at least one `should_trigger: false` query from the trigger-eval set to confirm the updated description hasn't introduced false positives.

If either check fails, revise the description before running the full eval loop.

### How to think about improvements

- **Generalize, don't overfit.** Skills must work across many future prompts, not just the test cases. If a stubborn issue appears, try different metaphors or patterns rather than adding rigid constraints.
- **Keep the prompt lean.** Read transcripts (not just outputs) and remove anything that causes unproductive work. If you find yourself writing ALWAYS or NEVER in all caps, reframe as reasoning — LLMs respond better to understanding why than to rigid rules.
- **Explain the why.** Give the model enough context to make good judgment calls. Surface the reasoning behind requirements, not just the requirements themselves.
- **Bundle repeated work.** If multiple test case transcripts all produced the same helper script independently, put it in `scripts/` and tell the skill to use it.
- **Show the exact before/after.** When documenting description changes, quote the specific old phrase alongside the specific new phrase — not category-level labels ("broadened scope", "removed technical restriction"). The comparison should be self-evident without reading both files.
- **Apply current structural conventions.** When improving an existing skill, also close structural gaps: move any trigger guidance from body sections (e.g., `## When to Use`) to the frontmatter `description` or `when_to_use` field, and add a `metadata:` map (version, category, risk at minimum) if it's missing from frontmatter.

### The iteration loop

After improving the skill:

1. Apply your improvements to the skill
2. Rerun all test cases into a new `iteration-<N+1>/` directory, including baseline runs. If you're creating a new skill, the baseline is always `without_skill` (no skill) — that stays the same across iterations. If you're improving an existing skill, use your judgment on what makes sense as the baseline: the original version the user came in with, or the previous iteration.
3. Launch the reviewer with `--previous-workspace` pointing at the previous iteration
4. Wait for the user to review and tell you they're done
5. Read the new feedback, improve again, repeat

Keep going until:
- The user says they're happy
- The feedback is all empty (everything looks good)
- You're not making meaningful progress

---

## Advanced: Blind comparison

For situations where you want a more rigorous comparison between two versions of a skill (e.g., the user asks "is the new version actually better?"), there's a blind comparison system. Read `agents/comparator.md` and `agents/analyzer.md` for the details. The basic idea is: give two outputs to an independent agent without telling it which is which, and let it judge quality. Then analyze why the winner won.

This is optional, requires subagents, and most users won't need it. The human review loop is usually sufficient.

---

## Description Optimization

After creating or improving a skill, offer to optimize the description for better triggering accuracy.

Delegate to the `skill-evals-trigger` skill. Invoke it with the skill path once the SKILL.md is committed (that is its prerequisite). `skill-evals-trigger` owns the full trigger-optimization loop: generating 20 should-trigger / should-not-trigger queries, reviewing them with the user via the HTML template, running the optimization loop (60/40 train/test split, multiple runs per query, up to 5 iterations), and applying the winning `best_description` back to the skill's SKILL.md frontmatter.

Do not inline the query generation or the optimization run here — `skill-evals-trigger` owns them, for the same reason eval authoring and eval running are delegated to their own sub-skills.

Step-by-step instructions live in `<CORE>/../skills/interactive/.claude/skills/skill-evals-trigger/SKILL.md`.

---

## Package and Present (only if `present_files` tool is available)

Check whether you have access to the `present_files` tool. If you don't, skip this step. If you do, package the skill and present the .skill file to the user:

```bash
cd "<CORE>/../skills/interactive/.claude/skills/skill-creator"
python -m scripts.package_skill <path/to/skill-folder>
```

After packaging, direct the user to the resulting `.skill` file path so they can install it.

---

## Claude.ai-specific instructions

Claude.ai lacks subagents, so adapt as follows: run test cases sequentially yourself (no baselines, no parallel execution); present results inline in the conversation instead of launching the browser reviewer; skip quantitative benchmarking, description optimization (requires `claude -p`), and blind comparison. The core draft → test → feedback → improve loop still works. Packaging via `package_skill.py` works anywhere with Python.

---

## Reference files

- `agents/comparator.md` — Blind A/B comparison between two outputs
- `agents/analyzer.md` — Analyze why one version beat another
- `references/schemas.md` — JSON schemas for evals.json, grading.json, benchmark.json

---

GENERATE THE EVAL VIEWER *BEFORE* evaluating inputs yourself. Get outputs in front of the human ASAP.
