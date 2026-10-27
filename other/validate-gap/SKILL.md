---
name: kiro-validate-gap
description: Analyze implementation gap between requirements and existing codebase. Use when planning integration with existing systems.
allowed-tools: Read, Write, Grep, Glob, WebSearch, WebFetch, Skill, AskUserQuestion
argument-hint: <feature-name>
metadata:
  shared-rules: "gap-analysis.md"
---

> **移植说明**｜本文件是 `kiro` skill 的阶段规范（源自 `kiro-validate-gap` skill），由 kiro 总控按需读取并就地执行。
> 文中出现的 `kiro-xxx` / `/kiro-xxx` skill 引用，一律按 `kiro/SKILL.md` 的「阶段解析规则」处理：
> 宿主已注册同名 skill → `Skill(kiro-xxx)`；否则读 `phases/xxx/SKILL.md` 就地执行。
> 相对路径（`rules/`、`templates/`）一律相对本文件所在目录 `phases/validate-gap/`。

# kiro-validate-gap Skill

## Role
You are a specialized skill for analyzing the implementation gap between requirements and existing codebase to inform implementation strategy.

## Core Mission
- **Mission**: Analyze the gap between requirements and existing codebase to inform implementation strategy
- **Success Criteria**:
  - Comprehensive understanding of existing codebase patterns and components
  - Clear identification of missing capabilities and integration challenges
  - Multiple viable implementation approaches evaluated
  - Technical research needs identified for design phase

## Execution Steps

### Step 1: Gather Context

If steering/spec context is already available from conversation, skip redundant file reads.
Otherwise, load all necessary context:
- Read `.kiro/specs/{feature}/spec.json` for language and metadata
- Read `.kiro/specs/{feature}/requirements.md` for requirements
- Core steering context: `product.md`, `tech.md`, `structure.md`
- Additional steering files only when directly relevant to the feature's domain rules, integrations, runtime prerequisites, compliance/security constraints, or existing product boundaries
- Relevant local agent skills or playbooks only when they clearly match the feature's host environment or use case and provide analysis-relevant context

### Step 2: Read Analysis Guidelines
- Read `rules/gap-analysis.md` from this skill's directory for comprehensive analysis framework

### Step 3: Execute Gap Analysis

#### Parallel Research (concurrent subagent dispatch)

Follow `../../rules/parallel-dispatch.md`. Gap analysis is the most fan-out-friendly phase in kiro — its dimensions share nothing. Dispatch as **concurrent subagents in a single message**:

1. **Codebase analysis** (`Explore`): Existing implementations, architecture patterns, integration points, extension possibilities → what already exists that these requirements could extend
2. **External dependency research** (`general-purpose`, needs WebSearch/WebFetch): Dependency compatibility, version constraints, known integration challenges
3. **Context loading** (`Explore`): Requirements, core steering, feature-relevant extra steering, relevant local agent playbooks, and `rules/gap-analysis.md`

Split area 1 further when the feature spans several subsystems — one subagent per subsystem beats one subagent sweeping the repo. Each returns a findings summary with concrete file paths, under ~150 lines.

After all return, synthesize the gap analysis in the parent context. **Cross-dimension judgments (extend vs new vs hybrid) belong to the parent** — the subagents cannot see each other's findings.

- Follow gap-analysis.md framework for thorough investigation
- Evaluate multiple implementation approaches (extend/new/hybrid)
- Use language specified in spec.json for output

### Step 4: Generate Analysis Document
- Create comprehensive gap analysis following the output guidelines in gap-analysis.md
- Present multiple viable options with trade-offs
- Flag areas requiring further research

### Step 5: Write Gap Analysis to Disk

**Write the gap analysis to disk so it survives session boundaries and can be referenced during design phase.**

- Use the Write tool to save the gap analysis to `.kiro/specs/{feature}/research.md`
- If the file already exists, append the new analysis (separated by a horizontal rule `---`) rather than overwriting previous research
- Verify the file was written by reading it back

## Important Constraints
- **Information over Decisions**: Provide analysis and options, not final implementation choices
- **Multiple Options**: Present viable alternatives when applicable
- **Thorough Investigation**: Use tools to deeply understand existing codebase
- **Explicit Gaps**: Clearly flag areas needing research or investigation
- **Context Discipline**: Start with core steering and expand only with analysis-relevant steering or use-case-aligned local agent skills/playbooks

## Tool Guidance
- **Read first**: Load spec, core steering, relevant local playbooks/agent skills, and rules before analysis
- **Grep extensively**: Search codebase for patterns, conventions, and integration points
- **WebSearch/WebFetch**: Research external dependencies and best practices when needed
- **Write last**: Generate analysis only after complete investigation

## Output Description
Provide output in the language specified in spec.json with:

1. **Analysis Summary**: Brief overview (3-5 bullets) of scope, challenges, and recommendations
2. **Document Status**: Confirm analysis approach used
3. **Next Steps**: Guide user on proceeding to design phase

**Format Requirements**:
- Use Markdown headings for clarity
- Keep summary concise (under 300 words)
- Detailed analysis follows gap-analysis.md output guidelines

## Safety & Fallback

### Error Scenarios
- **Missing Requirements**: If requirements.md doesn't exist, stop with message: "Run `/kiro-spec-requirements {feature}` first to generate requirements"
- **Requirements Not Approved**: If requirements not approved, warn user but proceed (gap analysis can inform requirement revisions)
- **Empty Steering Directory**: Warn user that project context is missing and may affect analysis quality
- **Complex Integration Unclear**: Flag for comprehensive research in design phase rather than blocking
- **Language Undefined**: Default to English (`en`) if spec.json doesn't specify language

### Next Phase: Design Generation

**If Gap Analysis Complete**:
- Review gap analysis insights
- Run `/kiro-spec-design {feature}` to create technical design document
- Or `/kiro-spec-design {feature} -y` to auto-approve requirements and proceed directly

**Note**: Gap analysis is optional but recommended for brownfield projects to inform design decisions.
