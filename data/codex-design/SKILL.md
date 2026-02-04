---
name: codex-design
description: |
  Consult Codex for architectural decisions. Use when: (1) introducing patterns not in codebase, (2) 3+ design options exist, (3) performance-critical implementation, (4) major refactoring. Get risk assessment before coding.
---

# Codex Design Consultation

## 🎯 Purpose

**設計段階でのCodex相談**: Consult with Codex before making complex design decisions.
Get expert validation, alternative approaches, and risk assessment early in the development process.

## 📋 When to Use

### Mandatory Triggers
- Introducing implementation patterns NOT found in existing codebase
- Architecture decision with 3+ viable options
- Performance-critical implementations (high-traffic endpoints, real-time processing, etc.)
- Major refactoring affecting multiple modules
- New technology/framework introduction
- Security-sensitive design (authentication, authorization, cryptography)

### Optional but Recommended
- Database schema design for new features
- API design for public/external consumption
- Distributed system component design
- Complex algorithm implementation

## 🔄 Consultation Flow

### Step 1: Problem Analysis

Claude Code analyzes the design problem:
```
- Current situation and constraints
- Requirements (functional and non-functional)
- Existing codebase patterns
- Performance/security requirements
- Team expertise and maintenance considerations
```

### Step 2: Generate Design Options

Claude Code proposes 2-3 viable approaches:

```markdown
## Option 1: [Approach Name]
**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Drawback 1]
- [Drawback 2]

**Implementation Complexity:** Low/Medium/High
**Maintenance Cost:** Low/Medium/High
**Performance Impact:** Low/Medium/High

## Option 2: [Approach Name]
...

## Option 3: [Approach Name]
...
```

### Step 3: Codex Consultation

Execute Codex in read-only sandbox for design review:

```bash
codex exec --sandbox read-only "$(cat <<'EOF'
# Design Consultation Request

## Context
[プロジェクトの概要と現在の状況]

## Problem Statement
[解決したい問題の詳細な説明]

## Constraints
- Performance: [パフォーマンス要件]
- Security: [セキュリティ要件]
- Scalability: [スケーラビリティ要件]
- Maintainability: [保守性要件]
- Team: [チームのスキルセット]
- Timeline: [スケジュール制約]

## Proposed Design Options

### Option 1: [アプローチ名]
[詳細な説明]

**Pros:**
- [メリット1]
- [メリット2]

**Cons:**
- [デメリット1]
- [デメリット2]

### Option 2: [アプローチ名]
[詳細な説明]
...

### Option 3: [アプローチ名]
[詳細な説明]
...

## Existing Codebase Patterns
[既存のコードベースで使用されているパターン]

## Questions for Codex

1. 各アプローチの妥当性評価
2. 見落としている潜在的な問題点
3. 推奨されるアプローチとその理由
4. 実装時の注意点
5. 類似プロジェクトでの成功/失敗事例

## Required Output Format (JSON in Japanese)

以下のJSON形式で回答してください:

{
  "recommended_option": "Option 1|Option 2|Option 3|Alternative",
  "reasoning": "推奨理由の詳細説明(日本語)",
  "risk_assessment": {
    "option_1": {
      "technical_risks": ["リスク1", "リスク2"],
      "mitigation": ["対策1", "対策2"]
    },
    "option_2": { ... },
    "option_3": { ... }
  },
  "additional_considerations": [
    {
      "category": "performance|security|maintainability|scalability",
      "point": "考慮すべき点(日本語)",
      "importance": "critical|high|medium|low"
    }
  ],
  "alternative_approach": {
    "description": "代替アプローチの説明(Option 1-3以外に良い方法があれば)",
    "why_better": "なぜこちらが良いか"
  },
  "implementation_guidance": [
    "実装時のガイダンス1",
    "実装時のガイダンス2"
  ],
  "similar_patterns": [
    {
      "project": "類似プロジェクト名",
      "approach": "採用されたアプローチ",
      "outcome": "結果(成功/失敗とその理由)"
    }
  ],
  "confidence": "high|medium|low",
  "caveats": ["注意事項1", "注意事項2"]
}
EOF
)"
```

### Step 4: Analysis and Synthesis

Claude Code analyzes Codex's response:
- Evaluate recommendation validity
- Consider project-specific context
- Synthesize with existing codebase patterns
- Identify any conflicting advice

### Step 5: Present to User

Present comprehensive analysis to user for final decision:

```markdown
## 設計相談結果: [問題のタイトル]

### 問題概要
[解決したい問題の簡潔な説明]

### 提案した設計オプション
1. **Option 1**: [概要]
2. **Option 2**: [概要]
3. **Option 3**: [概要]

### Codex推奨
- **推奨アプローチ**: Option 2
- **信頼度**: High
- **推奨理由**:
  [Codexの推奨理由を日本語で説明]

### リスク評価

#### Option 1: [名前]
- **技術的リスク**:
  - [リスク1]
  - [リスク2]
- **リスク軽減策**:
  - [対策1]
  - [対策2]

#### Option 2: [名前] ⭐ 推奨
- **技術的リスク**:
  - [リスク1]
- **リスク軽減策**:
  - [対策1]

#### Option 3: [名前]
- **技術的リスク**:
  - [リスク1]
  - [リスク2]
- **リスク軽減策**:
  - [対策1]

### 追加考慮事項

#### Critical
- [重要な考慮点1]

#### High
- [高優先度の考慮点1]
- [高優先度の考慮点2]

#### Medium
- [中優先度の考慮点1]

### 代替アプローチ (Codex提案)
[Codexが提案した代替案があれば]

**なぜ良いか**: [理由]

### 実装ガイダンス
1. [実装時の注意点1]
2. [実装時の注意点2]
3. [実装時の注意点3]

### 類似プロジェクトの事例
- **プロジェクト**: [名前]
  - **アプローチ**: [採用手法]
  - **結果**: [成功/失敗の理由]

### 注意事項
- [注意事項1]
- [注意事項2]

### Claude Codeの所見
[Codexの推奨を踏まえた、プロジェクト固有の考察]

どのアプローチで進めますか? または、さらに詳細を検討しますか?
```

## 🔍 Specific Use Cases

### Use Case 1: Database Schema Design

```markdown
## Problem
新しいマルチテナント機能のためのデータベース設計

## Options
1. Single database with tenant_id column
2. Database per tenant
3. Schema per tenant (PostgreSQL)

[Codex consultation...]

## Codex Recommendation
Option 3 (Schema per tenant) for this scale
- Reasoning: Balance of isolation and management
- Risk: Schema migration complexity
- Mitigation: Use migration tool like Flyway
```

### Use Case 2: API Design Pattern

```markdown
## Problem
新しいマイクロサービス間のAPI設計

## Options
1. REST with JSON
2. gRPC
3. GraphQL

[Codex consultation...]

## Codex Recommendation
Option 2 (gRPC) for internal services
- Reasoning: Type safety, performance, streaming support
- Risk: Steeper learning curve
- Mitigation: Start with simple unary calls, add streaming later
```

### Use Case 3: State Management

```markdown
## Problem
React アプリケーションの状態管理

## Options
1. Redux Toolkit
2. Zustand
3. Jotai

[Codex consultation...]

## Codex Recommendation
Option 2 (Zustand) for this project size
- Reasoning: Simplicity, less boilerplate, sufficient for current needs
- Risk: Might need migration if app grows significantly
- Mitigation: Keep state logic modular for easier migration
```

## 🚨 Error Handling

### Codex Timeout
- Wait up to 10 minutes (10 polls)
- If timeout: Present options to user without Codex input
- Explain that consultation couldn't complete

### Codex API Failure
- Retry once after 5 seconds
- If retry fails: Proceed with Claude Code's analysis only
- Inform user that external validation unavailable

### Conflicting Recommendations
- If Codex recommendation contradicts project constraints
- Claude Code highlights the conflict
- Provides reasoning for both perspectives
- Lets user make informed decision

## 📊 Output Quality Indicators

### High Confidence Output
- Clear recommendation with strong reasoning
- Multiple supporting examples
- Specific implementation guidance
- Risk assessment with mitigations

### Low Confidence Output
- Multiple viable options with trade-offs
- Insufficient context for firm recommendation
- Suggests gathering more information
- Recommends prototyping or spike

## 🔧 Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| timeout_minutes | 10 | Codex consultation timeout |
| min_options | 2 | Minimum design options to present |
| max_options | 4 | Maximum design options to present |
| require_risk_assessment | true | Require risk analysis for each option |
| include_examples | true | Include similar project examples |

## 🎯 Success Criteria

Consultation is successful when:
- ✅ Codex provides clear recommendation
- ✅ All options have risk assessment
- ✅ Implementation guidance provided
- ✅ User has sufficient information to decide
- ✅ Potential pitfalls identified

## 📝 Best Practices

### Before Consultation
1. Clearly define the problem and constraints
2. Research existing patterns in codebase
3. Identify at least 2 viable options
4. Document non-functional requirements

### During Consultation
1. Wait for complete Codex response
2. Validate recommendations against project context
3. Identify any missed considerations
4. Synthesize with project-specific knowledge

### After Consultation
1. Document the decision and rationale
2. Update architecture documentation if needed
3. Share decision with team
4. Reference consultation in implementation

## ⚠️ Important Reminders

1. **Use early** - Consult before writing code, not after
2. **Be specific** - Provide detailed context and constraints
3. **Consider context** - Codex doesn't know your project specifics
4. **Final decision** - Human makes the final call, not AI
5. **Document** - Record the decision for future reference
6. **Output in Japanese** - All user-facing text in Japanese
