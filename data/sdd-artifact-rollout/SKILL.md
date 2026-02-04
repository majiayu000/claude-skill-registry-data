---
name: sdd-artifact-rollout
description: Guides SDD artifact implementation for NEW and EXISTING projects. Use for DDD glossary, context map, domain models, ADRs, user stories with acceptance criteria. For existing projects, supports gap analysis, code-to-spec reverse engineering, and phased migration. Triggers on SDD, spec-driven, artifact, glossary, context map, domain vision, ADR, legacy documentation, reverse engineering, existing project documentation, gap analysis.
---

# SDD Artifact Rollout

Implements the 5-phase rollout methodology for Specification-Driven Development artifact frameworks, enabling teams to create AI-ready specifications that drive code generation.

## When to Use This Skill

### 新規プロジェクト
- SDD/スペック駆動開発の導入
- ドメイン用語集（Glossary）やユビキタス言語の作成
- Bounded Context Mapの設計
- 形式的受け入れ基準付きUser Storiesの構造化
- ドメインモデル（Aggregate, Entity, Value Object）の構築
- ADR（Architecture Decision Record）の確立

### 既存プロジェクト
- 既存コードベースの包括的文書化
- レガシープロジェクトへのSDD準拠アーティファクト追加
- コードからGlossary/Domain Modelのリバースエンジニアリング
- 既存APIからOpenAPI仕様書の生成
- 技術的負債・設計判断の事後記録（ADR）
- 文書化ギャップの診断と優先順位付け

## Quick Start: Context Gathering

Before proceeding, gather these inputs from the user:

```
1. Domain: What is the target domain? (e.g., order management, billing)
2. Team: How many people? What roles? (PO, Tech Lead, Dev, QA, DevOps)
3. Timeline: Available weeks? (Standard: 12 weeks for full rollout)
4. Regulatory: Any compliance requirements? (affects Phase 5 depth)
5. Existing Artifacts: Any glossary, domain model, or specs already exist?
6. Project Type: NEW project or EXISTING codebase?
```

---

## 既存プロジェクト向けガイド

既存コードベースにSDD準拠のアーティファクトを導入する場合は、以下のガイドを参照：

| ガイド | 用途 |
|--------|------|
| [ギャップ診断](existing-project/gap-analysis.md) | 現状分析、何が欠けているか診断、優先順位付け |
| [リバースエンジニアリング](existing-project/reverse-engineering.md) | コード→Glossary、コード→Domain Model、API→OpenAPI抽出 |
| [暗黙知の明示化](existing-project/knowledge-extraction.md) | インタビュー手順、PR履歴分析、事後ADR作成 |
| [段階的移行ロードマップ](existing-project/migration-roadmap.md) | MVP定義、移行計画、日常業務への組み込み |

### 既存プロジェクトでの推奨フロー

```
1. ギャップ診断（何が欠けているか）
   ↓
2. 優先順位付け（どこから着手するか）
   ↓
3. MVP Level 1 作成（Vision, Glossary 15用語, Context Map）
   ↓
4. リバースエンジニアリング（コードから抽出）
   ↓
5. 暗黙知収集（インタビュー、事後ADR）
   ↓
6. 段階的に Level 2, 3 へ拡充
```

---

## 新規プロジェクト向け: Phase Overview (12-Week Standard)

| Phase | Weeks | Focus | Key Deliverables |
|-------|-------|-------|------------------|
| 1 | 1-2 | Foundation | Domain Vision, Glossary v0.1, Context Map |
| 2 | 3-5 | Requirements | User Stories, Formal ACs, Feature Breakdown |
| 3 | 6-8 | Conceptual Design | Domain Model, Events, Service Specs |
| 4 | 8-10 | Data & API | Data Models, OpenAPI Specs, Code Skeleton |
| 5 | 10-12 | Operations | ADRs, Validation Automation, CI/CD |

## Execution Flow

### Phase 1: Foundation (Weeks 1-2)

**Goal**: Establish ubiquitous language and AI context foundation.

**Deliverables**:
1. Domain Vision Statement (1-2 pages)
2. Core Glossary v0.1 (20-30 terms in YAML)
3. Bounded Context Map (3-5 contexts)

**AI Usage**: Heavy (glossary generation, context refinement)

For detailed templates and procedures, see [phase-1-foundation.md](phase-1-foundation.md).

### Phase 2: Requirements (Weeks 3-5)

**Goal**: Structure user stories for AI code generation compatibility.

**Deliverables**:
1. User Stories v1 (5-10 per sprint)
2. Acceptance Criteria (formal + natural language)
3. Feature Breakdown & Dependencies

**AI Usage**: Medium (story generation, AC refinement)

For detailed templates and procedures, see [phase-2-requirements.md](phase-2-requirements.md).

### Phase 3: Conceptual Design (Weeks 6-8)

**Goal**: Develop domain models with explicit invariants.

**Deliverables**:
1. Domain Model (Aggregates, Entities, Value Objects)
2. Domain Events & Event Flow
3. Service Specifications (Application/Domain)

**AI Usage**: Medium-High (code skeleton generation)

For detailed templates and procedures, see [phase-3-domain-design.md](phase-3-domain-design.md).

### Phase 4: Data & Implementation Design (Weeks 8-10)

**Goal**: Define data schemas and external interfaces.

**Deliverables**:
1. Logical & Physical Data Models
2. OpenAPI Specifications
3. Implementation Code Skeleton

**AI Usage**: Heavy (code generation, schema inference)

For detailed templates and procedures, see [phase-4-data-api.md](phase-4-data-api.md).

### Phase 5: Integration & Operations (Weeks 10-12)

**Goal**: Complete artifact lifecycle management with CI/CD integration.

**Deliverables**:
1. ADRs for all major decisions
2. Validation & Quality Check Automation
3. CI/CD integration, deployment pipeline
4. Artifact versioning & change management

**AI Usage**: Light (validation logic generation)

For detailed templates and procedures, see [phase-5-ops-automation.md](phase-5-ops-automation.md).

## Validation at Each Phase

Before advancing to the next phase, verify:

- [ ] All deliverables created and reviewed
- [ ] Glossary terms used consistently across artifacts
- [ ] Referential integrity checked (all referenced concepts defined)
- [ ] Stakeholder approval obtained

For validation scripts and detailed checks, see [validation.md](validation.md).

## Templates

AI prompt templates for each phase are provided in [templates.md](templates.md).

## Checklists

Phase-by-phase implementation checklists are in [checklist.md](checklist.md).

## Success Factors

1. **Early Commitment**: Team understands why documentation matters for AI
2. **Tool Simplicity**: Start with Git + Markdown + YAML
3. **Iterative Refinement**: Don't aim for perfect; iterate
4. **AI Usage Clarity**: Define which stages use AI generation
5. **Feedback Loop**: Implementation feedback flows back to artifacts

## Required Roles

| Role | Responsibilities |
|------|------------------|
| Domain Expert / PO | Glossary, Business Rules, Story validation |
| Architect / Tech Lead | Context Map, ADR, Framework design |
| Senior Developer | Domain Model, code generation |
| Mid Developer | Feature implementation, story completion |
| QA / Tester | AC validation, test case generation |
| DevOps | CI/CD, artifact versioning, validation automation |

## Recommended Repository Structure

```
project-repo/
├── domain/
│   ├── vision.md
│   └── glossary.yaml
├── architecture/
│   ├── context-map.md
│   └── strategic-rules.md
├── requirements/
│   ├── user-stories.md
│   └── features/
├── domain-design/
│   ├── domain-model.ts
│   └── aggregates/
├── data-model/
│   ├── schema.sql
│   └── migrations/
├── api-specs/
│   └── openapi.yaml
├── adr/
│   └── ADR-001-*.md
├── ai/
│   └── prompt-templates.yaml
└── scripts/
    └── validate-artifacts.sh
```

## Adaptation Guidelines

### 新規プロジェクト
- **Startup (small team)**: Focus on Phase 1-2, minimal Phase 5
- **Growth-stage**: Full 5-phase rollout over 12 weeks
- **Enterprise**: Add regulatory artifacts, extend Phase 5

### 既存プロジェクト
- **レガシー（文書なし）**: [ギャップ診断](existing-project/gap-analysis.md)から開始、MVP Level 1を最優先
- **部分的に文書あり**: ギャップ診断で欠けている部分を特定、優先順位付けして補完
- **リファクタリング予定**: [リバースエンジニアリング](existing-project/reverse-engineering.md)でDomain Model抽出を優先
- **新メンバー頻繁**: Glossary, Domain Vision, Context Mapを最優先

## Next Steps

After gathering context, proceed to Phase 1:
1. Read [phase-1-foundation.md](phase-1-foundation.md)
2. Create Domain Vision Statement using template
3. Generate initial Glossary with AI assistance
4. Draft Bounded Context Map
5. Validate and get approval before Phase 2
