---
name: musubix-sdd-workflow
description: Guide for MUSUBIX SDD (Specification-Driven Development) workflow. Use this when asked to develop features using MUSUBIX methodology, create requirements, designs, or implement code following the 9 constitutional articles.
license: MIT
---

# MUSUBIX SDD Workflow Skill

This skill guides you through the complete SDD workflow for MUSUBIX projects.

## Prerequisites

Before starting any development task:

1. Read `steering/` directory for project context
2. Check `steering/rules/constitution.md` for the 9 constitutional articles
3. Review existing specs in `storage/specs/`

## Workflow Steps

### Step 1: Requirements Phase (Article IV - EARS Format)

Create requirements using EARS patterns:

```markdown
# REQ-[CATEGORY]-[NUMBER]

**種別**: [UBIQUITOUS|EVENT-DRIVEN|STATE-DRIVEN|UNWANTED|OPTIONAL]
**優先度**: [P0|P1|P2]

**要件**:
[EARS形式の要件文]

**トレーサビリティ**: DES-XXX, TEST-XXX
```

EARS Patterns:
- **Ubiquitous**: `THE [system] SHALL [requirement]`
- **Event-driven**: `WHEN [event], THE [system] SHALL [response]`
- **State-driven**: `WHILE [state], THE [system] SHALL [response]`
- **Unwanted**: `THE [system] SHALL NOT [behavior]`
- **Optional**: `IF [condition], THEN THE [system] SHALL [response]`

### Step 2: Design Phase (Article VII - Design Patterns)

Create C4 model design documents:

1. **Context Level**: System boundaries and external actors
2. **Container Level**: Technology choices and container composition
3. **Component Level**: Internal structure of containers
4. **Code Level**: Implementation details

Design document template:
```markdown
# DES-[CATEGORY]-[NUMBER]

## トレーサビリティ
- 要件: REQ-XXX

## C4モデル
### Level 2: Container
[PlantUML diagram]

## コンポーネント設計
[Component details]
```

### Step 3: Task Generation

Generate implementation tasks from design:

```markdown
# TSK-[CATEGORY]-[NUMBER]

## 関連設計: DES-XXX
## 関連要件: REQ-XXX

## タスク内容
[Implementation task description]

## 受入基準
- [ ] Criterion 1
- [ ] Criterion 2
```

### Step 4: Implementation (Article III - Test-First)

Follow Red-Green-Blue cycle:

1. **Red**: Write failing test first
2. **Green**: Write minimal code to pass
3. **Blue**: Refactor while keeping tests green

### Step 5: Traceability Validation (Article V)

Ensure 100% traceability:
```
REQ-* → DES-* → TSK-* → Code → Test
```

Add requirement IDs in code comments:
```typescript
/**
 * @see REQ-INT-001 - Neuro-Symbolic Integration
 */
```

## CLI Commands

```bash
# Requirements
npx musubix requirements analyze <file>
npx musubix requirements validate <file>

# Design
npx musubix design generate <file>
npx musubix design patterns <context>

# Code Generation
npx musubix codegen generate <file>

# Traceability
npx musubix trace matrix
npx musubix trace validate
```

## Constitutional Articles Checklist

- [ ] **Article I**: Library-First - Is this a standalone library?
- [ ] **Article II**: CLI Interface - Does it expose CLI?
- [ ] **Article III**: Test-First - Are tests written first?
- [ ] **Article IV**: EARS Format - Are requirements in EARS?
- [ ] **Article V**: Traceability - Is everything traceable?
- [ ] **Article VI**: Project Memory - Did you check steering/?
- [ ] **Article VII**: Design Patterns - Are patterns documented?
- [ ] **Article VIII**: Decision Records - Is ADR created?
- [ ] **Article IX**: Quality Gates - Are quality checks passed?
