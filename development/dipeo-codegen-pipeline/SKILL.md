---
name: dipeo-codegen-pipeline
description: Router skill for DiPeO code generation pipeline (TypeScript specs → IR → Python/GraphQL). Use when task mentions TypeScript models, IR builders, generated code diagnosis, or codegen workflow. For simple tasks, handle directly; for complex work, escalate to dipeo-codegen-pipeline agent.
allowed-tools: Read, Grep, Glob, Bash, Skill
---

# DiPeO Codegen Pipeline Router

**Domain**: Complete TypeScript → IR → Python/GraphQL pipeline (`/dipeo/models/src/`, `/dipeo/infrastructure/codegen/`, generated code diagnosis).

## Quick Decision: Skill or Agent?

### ✅ Handle Directly (This Skill)
- **Simple lookups**: Understanding codegen workflow, reviewing TypeScript specs
- **Read-only tasks**: Checking generated code structure, reviewing IR output
- **Pattern reference**: snake_case naming rules, type mapping examples
- **Small spec tweaks**: Minor TypeScript field changes (<5 lines, 1 file)
- **Workflow questions**: "How do I run codegen?", "What's the IR structure?"

### ❌ Escalate to Agent
- **New node types**: Creating complete TypeScript specs with IR builders
- **IR builder changes**: Modifying AST processing, type conversion logic
- **Generated code diagnosis**: Tracing why generated code is wrong
- **Template modifications**: Changing Jinja templates for code generation
- **Complex spec changes**: Multi-field changes affecting multiple generated files
- **Type system updates**: Changes to UnifiedTypeConverter or type mappings

**Agent**: `Task(dipeo-codegen-pipeline, "your detailed task description")`

## Documentation Sections (Load On-Demand)

Use `Skill(doc-lookup)` with these anchors when you need detailed context:

**Part 1: TypeScript Model Design**:
- `docs/agents/codegen-pipeline.md#your-role-as-model-architect` - Model locations and structure
- `docs/agents/codegen-pipeline.md#type-system-design-principles` - **CRITICAL**: snake_case and type safety
- `docs/agents/codegen-pipeline.md#workflows` - Creating/modifying node types

**Part 2: IR Builder System**:
- `docs/agents/codegen-pipeline.md#ir-builder-architecture` - Architecture and directory structure
- `docs/agents/codegen-pipeline.md#pipeline-system` - Pipeline, type conversion, AST processing

**Part 3: Code Generation**:
- `docs/agents/codegen-pipeline.md#template-system` - Templates and generated code structure
- `docs/agents/codegen-pipeline.md#generation-workflow` - Complete make codegen workflow

**Part 4: Diagnosis**:
- `docs/agents/codegen-pipeline.md#your-critical-responsibility` - Tracing TypeScript → IR → Python

**Part 5 & 6: Workflow & Collaboration**:
- `docs/agents/codegen-pipeline.md#complete-workflow` - End-to-end steps and validation
- `docs/agents/codegen-pipeline.md#when-to-engage-other-agents` - Escalation paths

**Example doc-lookup call**:
```bash
python .claude/skills/doc-lookup/scripts/section_search.py \
  --query "naming-standards" \
  --paths docs/agents/codegen-pipeline.md \
  --top 1
```

## Escalation to Other Agents

**To dipeo-package-maintainer**: Runtime handler issues, service architecture (if generated code is correct)
**To dipeo-backend**: GraphQL schema deployment, server config (if generation is correct)

## Typical Workflow

1. **Assess complexity**: Simple lookup/guidance vs. complex generation task
2. **If simple**: Load relevant section via `Skill(doc-lookup)`, provide guidance
3. **If diagnosis needed**: Trace TypeScript → IR → Python (use diagnosis docs)
4. **If complex**: Escalate with `Task(dipeo-codegen-pipeline, "task details")`
