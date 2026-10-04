---
name: skillforge
description: |
  Generate production-grade Agent Skill packages through a structured 7-step pipeline: requirement analysis, architecture decisions, metadata crafting, body generation, quality audit, resource file creation, and usage documentation. Use when creating new Skills from scratch, upgrading low-quality Skills, or batch-producing Skills for a specific domain. Outputs a complete skill directory with SKILL.md, scripts/, references/, and templates/.
---

# SkillForge — Agent Skill Generator

Generate complete, production-ready Agent Skill packages via a 7-step pipeline. Each step has defined inputs, outputs, and quality constraints.

## Core Design Principles

Apply these principles throughout all 7 steps:

1. **Concise is Key** — Context window is a public good. Only include knowledge the AI model does NOT already have. Challenge each paragraph: "Does this justify its token cost?"
2. **Description is the trigger** — Determines whether the Skill gets selected. Must include WHAT + WHEN.
3. **Progressive disclosure** — SKILL.md < 500 lines. Supporting files in scripts/, references/, templates/ loaded on demand.
4. **Code examples > text** — Prefer concise, runnable examples over verbose descriptions.
5. **Anti-patterns are essential** — Show what NOT to do using ❌/✅ contrast format.
6. **Imperative tone** — "Run" not "You should run".
7. **No auxiliary files** — No README.md, CHANGELOG.md. Skills are for AI agents, not humans.

## Pipeline Overview

```
User requirement
  → Step 1: Requirement deep analysis
  → Step 2: Architecture decisions
  → Step 3: Metadata (YAML frontmatter)
  → Step 4: SKILL.md body
  → Step 5: Quality audit + optimization
  → Step 6: Resource files (scripts/, references/, templates/)
  → Step 7: Usage documentation
  → Complete Skill package
```

Execute steps sequentially. Each step builds on previous outputs.

## Step 1: Requirement Deep Analysis

Analyze the user's requirement. Output a structured document (2000-5000 chars).

Read the full step prompt: `references/step-prompts.md` → Section "Step 1".

**Output structure:**
0. **Skill qualification** (decide FIRST): Is this worth a Skill, or better served by a direct answer / doc / script? Build a Skill only when the job recurs AND needs discovery/triggering AND has a clear boundary AND a reusable output contract. If it's a one-off, explanation, translation, or brainstorm → recommend the lighter alternative instead. "Might be useful later" is speculation, not a reason.
1. Core positioning (name, one-line description, target users, value proposition)
2. Functional boundaries (core features as input→process→output triples, extensions, exclusions)
3. Usage scenarios (at least 5, each with: user request, expected behavior, output format)
4. **Knowledge gap analysis** (most critical):
   - AI already knows → exclude from SKILL.md
   - AI doesn't know → core content of SKILL.md
   - AI often gets wrong → needs anti-pattern examples
5. Dependencies and constraints

## Step 2: Architecture Decisions

Make 5 key decisions. Read full prompt: `references/step-prompts.md` → Section "Step 2".

| Decision | Options |
|----------|---------|
| Structure pattern | Workflow / Task-oriented / Guide / Capability |
| Freedom level | High / Medium / Low |
| Resource file plan | Table of files with paths, types, purposes, line counts |
| Progressive disclosure | What goes in SKILL.md vs references/ vs scripts/ |
| Quality assurance | Validation checklist, common errors, quality standards |

Output a complete directory tree at the end.

## Step 3: Metadata Crafting

Generate YAML frontmatter with optimized description.

1. **Build trigger test cases FIRST**: should_trigger (5-8), should_not (3-5), near_neighbor (3-5, the ambiguous look-alikes), plus 3-6 negative-pattern keywords. Bilingual, phrased like real users.
2. Generate 3 candidate descriptions; self-score on trigger precision / capability coverage / information density
3. **Evaluate each candidate against the test cases** (should_trigger hits, should_not & near_neighbor false-triggers); pick the empirically best candidate — real results outrank self-scores. Tighten the description if a near_neighbor still false-triggers.
4. Keep the trigger set alongside the frontmatter (optionally persist as `references/trigger-cases.md`) for future regression

Read full prompt: `references/step-prompts.md` → Section "Step 3".

**description quality rules:**
- 30-80 words, objective descriptive tone
- Must include WHAT the skill does AND WHEN to use it
- Every word must earn its place

## Step 4: SKILL.md Body Generation

Generate the complete body (excluding frontmatter). Target: 150-450 lines.

Read full prompt: `references/step-prompts.md` → Section "Step 4".

**Structure (adapt as needed):**
1. Overview (2-3 sentences)
2. Core workflow (numbered steps or decision flow)
3. Detailed rules and instructions (domain-specific)
4. Code examples (✅ Good / ❌ Bad contrast format)
5. Edge case handling
6. Output format specification
7. Validation checklist (Markdown checkboxes)

**Key constraints:**
- No generic knowledge AI already has
- No repetition of description content
- Sections > 100 lines → split to references/
- All code examples must be complete and runnable

## Step 5: Quality Audit

Audit the generated SKILL.md (Step 3 frontmatter + Step 4 body) against 10 dimensions, then output the optimized version.

Read full prompt: `references/step-prompts.md` → Section "Step 5".

**10-dimension scoring (1-10 each):**

| # | Dimension |
|---|-----------|
| 1 | Description trigger precision |
| 2 | Knowledge increment (only AI-unknown content) |
| 3 | Code example quality (runnable, representative) |
| 4 | Anti-pattern coverage (❌/✅ contrast) |
| 5 | Structure clarity |
| 6 | Progressive disclosure (<500 lines) |
| 7 | Tone consistency (imperative throughout) |
| 8 | Edge case handling |
| 9 | Actionability (instructions directly executable) |
| 10 | Completeness (no missing critical content) |

Fix any dimension scoring below 8. Output optimized complete SKILL.md.

## Step 6: Resource File Generation

Generate all supporting files planned in Step 2.

Read full prompt: `references/step-prompts.md` → Section "Step 6".

**Rules:**
- Strictly follow Step 2 file plan — no omissions, no extras
- If Step 2 says "no resource files needed" → skip this step
- Every file must be complete — no `...` or `TODO` placeholders
- Scripts must include shebang lines

## Step 7: Usage Documentation

Generate usage guide with 4 sections:

1. **Installation** (1-3 sentences)
2. **Trigger examples** (at least 5 natural language requests)
3. **Iteration suggestions** (3-5 specific improvement directions)
4. **Validation checklist** (completeness checks with checkboxes)

Read full prompt: `references/step-prompts.md` → Section "Step 7".

## Execution Workflow

When a user requests Skill generation:

1. Collect requirement: skill name, target domain, core capabilities, usage scenarios (optional), notes (optional)
2. Execute Steps 1-7 sequentially, presenting each step's output to the user
3. After Step 5, write the final SKILL.md to disk
4. After Step 6, write all resource files to disk
5. After Step 7, present the complete skill package

**File output structure:**
```
{skill-name}/
├── SKILL.md
├── scripts/       (if planned)
├── references/    (if planned)
└── templates/     (if planned)
```

## Quality Gate

Before delivering the final package, verify:

- [ ] Skill qualification passed (this genuinely warrants a Skill, not a doc/script/direct answer)
- [ ] SKILL.md exists with valid YAML frontmatter (name + description)
- [ ] description includes WHAT + WHEN, 30-80 words
- [ ] description was validated against trigger test cases (should / should-not / near-neighbor)
- [ ] SKILL.md body < 500 lines
- [ ] All code examples are complete and runnable
- [ ] Anti-patterns use ❌/✅ contrast format
- [ ] Imperative tone throughout
- [ ] All Step 2 planned resource files exist
- [ ] No README.md, CHANGELOG.md, or auxiliary docs
- [ ] No generic knowledge AI already has
- [ ] Directory structure matches Step 2 plan
