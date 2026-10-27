---
name: kiro-validate-design
description: Interactive technical design quality review and validation. Use when reviewing design before implementation.
allowed-tools: Read, Grep, Glob, AskUserQuestion, Skill
argument-hint: <feature-name>
metadata:
  shared-rules: "design-review.md"
---

> **移植说明**｜本文件是 `kiro` skill 的阶段规范（源自 `kiro-validate-design` skill），由 kiro 总控按需读取并就地执行。
> 文中出现的 `kiro-xxx` / `/kiro-xxx` skill 引用，一律按 `kiro/SKILL.md` 的「阶段解析规则」处理：
> 宿主已注册同名 skill → `Skill(kiro-xxx)`；否则读 `phases/xxx/SKILL.md` 就地执行。
> 相对路径（`rules/`、`templates/`）一律相对本文件所在目录 `phases/validate-design/`。

# kiro-validate-design Skill

## Role
You are a specialized skill for conducting interactive quality review of technical design to ensure readiness for implementation.

## Core Mission
- **Mission**: Conduct interactive quality review of technical design to ensure readiness for implementation
- **Success Criteria**:
  - Critical issues identified (maximum 3 most important concerns)
  - Balanced assessment with strengths recognized
  - Clear GO/NO-GO decision with rationale
  - Actionable feedback for improvements if needed

## Execution Steps

### Step 1: Gather Context

If steering/spec context is already available from conversation, skip redundant file reads.
Otherwise, load all necessary context:
- Read `.kiro/specs/{feature}/spec.json` for language and metadata
- Read `.kiro/specs/{feature}/requirements.md` for requirements
- Read `.kiro/specs/{feature}/design.md` for design document
- Core steering context: `product.md`, `tech.md`, `structure.md`
- Additional steering files only when directly relevant to architecture boundaries, integrations, runtime prerequisites, domain rules, security/performance constraints, or team conventions that affect implementation readiness
- Relevant local agent skills or playbooks only when they clearly match the feature's host environment or use case and provide review-relevant context

#### Parallel Research (concurrent subagent dispatch)

Follow `../../rules/parallel-dispatch.md`. Dispatch as **concurrent subagents in a single message** (`subagent_type: "Explore"`):

1. **Context & rules loading**: Spec documents, core steering, feature-relevant extra steering, relevant local agent playbooks, and `rules/design-review.md` for review criteria
2. **Codebase pattern survey**: Existing architecture patterns, naming conventions, component structure → the reference the design will be judged against
3. **Feasibility spot-check**: For each external contract / API / library the design depends on, verify it actually exists and works as the design assumes (`general-purpose` when this needs commands or web access) → the single highest-value dimension, since designs fail most often on assumptions that were never checked

After all return, synthesize in the parent context. **The GO/NO-GO call and the "3 most important concerns" cut are the parent's job** — a subagent only sees its own dimension and cannot rank across them.

### Step 2: Execute Design Review
- Reference conversation history: leverage prior requirements discussion and user's stated design intent
- Follow design-review.md process: Analysis → Critical Issues → Strengths → GO/NO-GO
- Limit to 3 most important concerns
- Engage interactively with user — ask clarifying questions, propose alternatives
- Use language specified in spec.json for output

### Step 3: Decision and Next Steps
- Clear GO/NO-GO decision with rationale
- Provide specific actionable next steps (see Next Phase below)

## Important Constraints
- **Quality assurance, not perfection seeking**: Accept acceptable risk
- **Critical focus only**: Maximum 3 issues, only those significantly impacting success
- **Conversation-aware**: Leverage discussion history for requirements context and user intent
- **Interactive approach**: Engage in dialogue, ask clarifying questions, propose alternatives
- **Balanced assessment**: Recognize both strengths and weaknesses
- **Actionable feedback**: All suggestions must be implementable
- **Context Discipline**: Start with core steering and expand only with review-relevant steering or use-case-aligned local agent skills/playbooks

## Tool Guidance
- **Read first**: Load spec, core steering, relevant local playbooks/agent skills, and rules before review
- **Grep if needed**: Search codebase for pattern validation or integration checks
- **Interactive**: Engage with user throughout the review process

## Output Description
Provide output in the language specified in spec.json with:

1. **Review Summary**: Brief overview (2-3 sentences) of design quality and readiness
2. **Critical Issues**: Maximum 3, following design-review.md format
3. **Design Strengths**: 1-2 positive aspects
4. **Final Assessment**: GO/NO-GO decision with rationale and next steps

**Format Requirements**:
- Use Markdown headings for clarity
- Follow design-review.md output format
- Keep summary concise

## Safety & Fallback

### Error Scenarios
- **Missing Design**: If design.md doesn't exist, stop with message: "Run `/kiro-spec-design {feature}` first to generate design document"
- **Design Not Generated**: If design phase not marked as generated in spec.json, warn but proceed with review
- **Empty Steering Directory**: Warn user that project context is missing and may affect review quality
- **Language Undefined**: Default to English (`en`) if spec.json doesn't specify language

### Next Phase: Task Generation

**If Design Passes Validation (GO Decision)**:
- Apply any suggested improvements if agreed
- Run `/kiro-spec-tasks {feature}` to generate implementation tasks
- Or `/kiro-spec-tasks {feature} -y` to auto-approve and proceed directly

**If Design Needs Revision (NO-GO Decision)**:
- Address critical issues identified in review
- Re-run `/kiro-spec-design {feature}` with improvements
- Re-validate with `/kiro-validate-design {feature}`

**Note**: Design validation is recommended but optional. Quality review helps catch issues early.
