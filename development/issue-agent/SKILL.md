---
name: issue-agent
description: |
  IssueAgent スキル - GitHub Issue分析・Label管理・自動分類。
  識学理論65ラベル体系による自動分類、Severity評価、影響度評価、担当者自動アサイン。

  Use when:
  - GitHub Issueを分析する時
  - 自動ラベル付与が必要な時
  - Severity/影響度を判定する時
  - 担当者をアサインする時
  - "Issue分析", "ラベル", "分類", "アサイン" がキーワードに含まれる時
allowed-tools: Read, Grep, Glob, Bash
---

# Issue Agent Skill

Issue分析・Label管理Agent - 識学理論65ラベル体系による自動分類。

## 役割

- Issue種別判定 (feature/bug/refactor/docs/test/deployment)
- Severity評価 (Sev.1-5)
- 影響度評価 (Critical/High/Medium/Low)
- 識学理論65ラベル自動付与
- 担当者自動アサイン (CODEOWNERS参照)
- 依存関係抽出 (#123形式)
- 所要時間見積もり
- Agent種別自動判定

## 判定ルール詳細

### Issue種別判定

| キーワード | Issue種別 | Agent | 優先度 |
|-----------|----------|-------|-------|
| feature/add/new/implement | feature | CodeGenAgent | Medium |
| bug/fix/error/problem/broken | bug | CodeGenAgent | High |
| refactor/cleanup/improve | refactor | CodeGenAgent | Medium |
| doc/documentation/readme | docs | CodeGenAgent | Low |
| test/spec/coverage | test | CodeGenAgent | Medium |
| deploy/release/ci/cd | deployment | DeploymentAgent | High |

### Severity判定

| キーワード | Severity | 対応時間 | Label |
|-----------|---------|---------|-------|
| critical/urgent/emergency/blocking | Sev.1-Critical | 即座 | Sev.1-Critical |
| high priority/asap/important/major | Sev.2-High | 24時間以内 | Sev.2-High |
| (デフォルト) | Sev.3-Medium | 1週間以内 | Sev.3-Medium |
| minor/small/trivial/typo | Sev.4-Low | 2週間以内 | Sev.4-Low |
| nice to have/enhancement | Sev.5-Trivial | 優先度低 | Sev.5-Trivial |

### 影響度判定

| キーワード | Impact | 説明 |
|-----------|--------|------|
| all users/entire system/data loss | Critical | 全ユーザー影響 |
| many users/major feature | High | 主要機能影響 |
| some users/workaround exists | Medium | 一部機能影響 |
| few users/cosmetic | Low | 軽微な影響 |

## 識学理論65ラベル体系

### ラベルカテゴリ

1. **業務カテゴリ** (Issue Type)
   - feature, bug, refactor, documentation, test, deployment

2. **深刻度** (Severity)
   - Sev.1-Critical, Sev.2-High, Sev.3-Medium, Sev.4-Low, Sev.5-Trivial

3. **影響度** (Impact)
   - 影響度-Critical, 影響度-High, 影響度-Medium, 影響度-Low

4. **責任者** (Responsibility)
   - 担当-開発者, 担当-テックリード, 担当-PO, 担当-AI Agent

5. **Agent種別** (Agent Type)
   - CoordinatorAgent, CodeGenAgent, ReviewAgent, IssueAgent, PRAgent, DeploymentAgent

## 所要時間見積もり

| Issue種別 | 基本時間 | 調整係数 |
|----------|---------|---------|
| feature | 120分 | large: ×2, quick: ×0.5 |
| bug | 60分 | major: ×2, minor: ×0.5 |
| refactor | 90分 | complex: ×2, simple: ×0.5 |
| docs | 30分 | - |
| test | 45分 | - |
| deployment | 30分 | - |

## 実行コマンド

```bash
# Issue分析実行
npm run agents:issue -- --issue 270

# 複数Issue一括分析
npm run agents:issue -- --issues 270,240,276
```

## 分析コメント出力例

```markdown
## IssueAgent Analysis

**Issue Type**: bug
**Severity**: Sev.2-High
**Impact**: High
**Responsibility**: Developer
**Assigned Agent**: CodeGenAgent
**Estimated Duration**: 60 minutes

### Applied Labels
- bug
- Sev.2-High
- 影響度-High
- 担当-開発者
- CodeGenAgent

### Dependencies
- #270
```

## エスカレーション条件

### Sev.2-High → CISO
- セキュリティ関連Issue

### Sev.2-High → TechLead
- アーキテクチャ設計に関わるIssue

### Sev.2-High → PO
- ビジネス要件に関わるIssue

## メトリクス

- **実行時間**: 通常5-10秒
- **Label付与精度**: 95%+
- **Severity判定精度**: 90%+
- **依存関係抽出精度**: 100%
