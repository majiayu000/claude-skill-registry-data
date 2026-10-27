---
name: kiro-steering
description: Maintain .kiro/steering/ as persistent project memory (bootstrap/sync). Use when initializing or updating steering documents.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
metadata:
  shared-rules: "steering-principles.md"
---

> **移植说明**｜本文件是 `kiro` skill 的阶段规范（源自 `kiro-steering` skill），由 kiro 总控按需读取并就地执行。
> 文中出现的 `kiro-xxx` / `/kiro-xxx` skill 引用，一律按 `kiro/SKILL.md` 的「阶段解析规则」处理：
> 宿主已注册同名 skill → `Skill(kiro-xxx)`；否则读 `phases/xxx/SKILL.md` 就地执行。
> 相对路径（`rules/`、`templates/`）一律相对本文件所在目录 `phases/steering/`。

# kiro-steering Skill

## Role
You are a specialized skill for maintaining `.kiro/steering/` as persistent project memory.

## Core Mission
**Role**: Maintain `.kiro/steering/` as persistent project memory.

**Mission**:
- Bootstrap: Generate core steering from codebase (first-time)
- Sync: Keep steering and codebase aligned (maintenance)
- Preserve: User customizations are sacred, updates are additive

**Success Criteria**:
- Steering captures patterns and principles, not exhaustive lists
- Code drift detected and reported
- All `.kiro/steering/*.md` treated equally (core + custom)

## Execution Steps

### Step 1: Gather Context

If steering context is already available from conversation, skip redundant file reads.

- For Bootstrap mode: Read templates from `.kiro/settings/templates/steering/`
- For Sync mode: Read all existing `.kiro/steering/*.md` files
- Read `rules/steering-principles.md` from this skill's directory for steering principles

## Scenario Detection

Check `.kiro/steering/` status:

**Bootstrap Mode**: Empty OR missing core files (product.md, tech.md, structure.md)
**Sync Mode**: All core files exist

---

## Bootstrap Flow

1. Load templates from `.kiro/settings/templates/steering/`
2. Analyze codebase (JIT):

#### Parallel Research (concurrent subagent dispatch)

Follow `../../rules/parallel-dispatch.md`. These three areas map one-to-one onto the three core steering files and share nothing — dispatch them as **concurrent subagents in a single message** (`subagent_type: "Explore"`):

1. **Product analysis**: README, package.json, documentation files → purpose, value, core capabilities
2. **Tech analysis**: Config files, dependencies, frameworks → technology patterns and decisions, plus the repo's validation commands. Record **both** scopes, because impl dispatches them to different actors: the canonical full suite (every test face — root, sub-packages, integration, e2e; note explicitly if the root command skips any) **and** how to run tests against specific file paths only (the runner invocation, e.g. `pnpm vitest run <paths>`). Without the scoped form recorded here, every implementer subagent falls back to running the full suite.
3. **Structure analysis**: Directory tree, naming conventions, import patterns → organization

Each subagent returns **patterns and principles under ~100 lines**, not file catalogs — say so in the prompt, since the granularity principle below is exactly what a naive explorer gets wrong.

After all three return, synthesize in the parent context and write the steering files there (the parent owns all writes).

3. Extract patterns (not lists):
   - Product: Purpose, value, core capabilities
   - Tech: Frameworks, decisions, conventions
   - Structure: Organization, naming, imports
4. Generate steering files (follow templates)
5. Load principles from `rules/steering-principles.md` from this skill's directory
6. Present summary for review

**Focus**: Patterns that guide decisions, not catalogs of files/dependencies.

---

## Sync Flow

1. Load all existing steering (`.kiro/steering/*.md`)
2. Analyze codebase for changes (JIT) — **one concurrent `Explore` subagent per steering file**, dispatched in a single message (follow `../../rules/parallel-dispatch.md`). Each gets one steering file path and one question: "这份文件的哪些断言与当前代码库已经不符？哪些新出现的模式它还没记录？只返回具体不符项与候选补充，各带证据路径，不超过 60 行。" With many custom steering files this is where sync spends its wall clock — never walk them one by one.
3. Detect drift (parent synthesizes the returned reports):
   - **Steering → Code**: Missing elements → Warning
   - **Code → Steering**: New patterns → Update candidate
   - **Custom files**: Check relevance
4. Propose updates (additive, preserve user content)
5. Report: Updates, warnings, recommendations

**Update Philosophy**: Add, don't replace. Preserve user sections.

---

## Granularity Principle

From `rules/steering-principles.md` (in this skill's directory):

> "If new code follows existing patterns, steering shouldn't need updating."

Document patterns and principles, not exhaustive lists.

**Bad**: List every file in directory tree
**Good**: Describe organization pattern with examples

## Tool Guidance

- `Glob`: Find source/config files
- `Read`: Read steering, docs, configs
- `Grep`: Search patterns
- `Bash` with `ls`: Analyze structure

**JIT Strategy**: Fetch when needed, not upfront.

## Output Description

Chat summary only (files updated directly).

### Bootstrap:
```
Steering Created

## Generated:
- product.md: [Brief description]
- tech.md: [Key stack]
- structure.md: [Organization]

Review and approve as Source of Truth.
```

### Sync:
```
Steering Updated

## Changes:
- tech.md: React 18 → 19
- structure.md: Added API pattern

## Code Drift:
- Components not following import conventions

## Recommendations:
- Consider api-standards.md
```

## Examples

### Bootstrap
**Input**: Empty steering, React TypeScript project
**Output**: 3 files with patterns - "Feature-first", "TypeScript strict", "React 19"

### Sync
**Input**: Existing steering, new `/api` directory
**Output**: Updated structure.md, flagged non-compliant files, suggested api-standards.md

## Safety & Fallback

- **Security**: Never include keys, passwords, secrets (see principles)
- **Uncertainty**: Report both states, ask user
- **Preservation**: Add rather than replace when in doubt

## Notes

- All `.kiro/steering/*.md` loaded as project memory
- Templates and principles are external for customization
- Focus on patterns, not catalogs
- "Golden Rule": New code following patterns shouldn't require steering updates
- `.kiro/settings/` content should NOT be documented in steering files (settings are metadata, not project knowledge)
