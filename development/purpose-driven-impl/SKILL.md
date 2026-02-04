---
name: purpose-driven-impl
description: Ensure clear purpose and success criteria before implementing any feature. Use when starting new features, major refactoring, or complex implementations. Prevents unclear objectives (FP-3).
---

# Purpose-Driven Implementation

**Version**: 1.0.0
**対策対象**: FP-3 (目的不明確)
**優先度**: 最高
**出典**: obra/superpowers, vibration-diagnosis-prototype失敗事例

## The Iron Law

> Before writing any code, clearly define WHY you are writing it

**出典**: obra/superpowers - Purpose-First Principle

---

## 5W1H Framework

実装開始前に必ず5W1Hを明確化します:

### Why（なぜ）- 最重要

**問い**:
- なぜこの機能が必要なのか？
- どんな問題を解決するのか？
- 誰が困っているのか？

**例**:
```markdown
## Why
ユーザーが毎回ログインするのが面倒だと報告している。
セッション管理がないため、ページ遷移のたびに認証が必要。
→ ユーザビリティ向上のため、セッション管理機能が必要
```

**禁止**:
- ❌ "依頼されたから"
- ❌ "あった方が良さそうだから"
- ❌ "他のアプリにあるから"

---

### What（何を）

**問い**:
- 何を実装するのか？（具体的機能）
- 何を変更するのか？（影響範囲）
- 何を提供するのか？（ユーザー価値）

**例**:
```markdown
## What
- セッション管理機能
- ログイン状態の30分間保持
- 自動ログアウト機能
```

---

### Who（誰が）

**問い**:
- 誰がこの機能を使うのか？（ユーザー）
- 誰が実装するのか？（担当者）
- 誰が影響を受けるのか？（ステークホルダー）

**例**:
```markdown
## Who
- ユーザー: サイトの全ユーザー（1000人）
- 実装: チーム開発者
- 影響: 既存ユーザー全員（後方互換性必須）
```

---

### When（いつ）

**問い**:
- いつリリースするのか？（期限）
- いつ使われるのか？（タイミング）
- いつテストするのか？（検証計画）

**例**:
```markdown
## When
- リリース: 2週間後
- 使用タイミング: ログイン時、ページ遷移時
- テスト: 実装完了後、リリース前
```

---

### Where（どこで）

**問い**:
- どこに実装するのか？（ファイル、モジュール）
- どこで動作するのか？（環境）
- どこに影響するのか？（依存関係）

**例**:
```markdown
## Where
- 実装場所: src/auth/session.js (新規作成)
- 動作環境: ブラウザ（LocalStorage使用）
- 影響範囲: src/auth/login.js, src/router/index.js
```

---

### How（どのように）

**問い**:
- どのように実装するのか？（技術的アプローチ）
- どのようにテストするのか？（検証方法）
- どのように測定するのか？（成功指標）

**例**:
```markdown
## How
### 実装アプローチ
- LocalStorageにセッショントークン保存
- JWT形式、30分有効期限
- 自動更新機能あり

### テスト方法
- ユニットテスト: session.test.js
- E2Eテスト: login-flow.test.js
- 手動テスト: ブラウザで動作確認

### 成功指標
- ログイン頻度が80%減少
- セッションタイムアウトエラー <5%
- ユーザー満足度向上
```

---

## Purpose Validation Workflow

### Step 1: Purpose Statement (目的宣言)

**テンプレート**:
```markdown
# Purpose Statement

## Problem（課題）
[現在の問題を具体的に記述]

## Solution（解決策）
[提案する機能・変更]

## Value（価値）
[ユーザーまたはビジネスへの価値]

## Success Criteria（成功基準）
- [ ] 基準1
- [ ] 基準2
- [ ] 基準3
```

**例**:
```markdown
# Purpose Statement

## Problem
ユーザーがページ遷移のたびにログインを求められ、
離脱率が30%に達している。

## Solution
セッション管理機能を実装し、30分間ログイン状態を保持する。

## Value
- ユーザー: 再ログインの手間が不要
- ビジネス: 離脱率10%以下に削減

## Success Criteria
- [ ] 30分間セッション保持
- [ ] 離脱率10%以下
- [ ] セキュリティ監査パス
```

---

### Step 2: User Story Mapping (ユーザーストーリー)

**As a... I want... So that... 形式**:

```markdown
## User Story

As a [ユーザータイプ],
I want [機能],
So that [目的/理由].

### Acceptance Criteria
- [ ] Given [前提条件], When [アクション], Then [期待結果]
- [ ] Given [前提条件], When [アクション], Then [期待結果]
```

**例**:
```markdown
## User Story

As a サイト利用者,
I want ログイン状態を保持して欲しい,
So that 毎回ログインする手間を省きたい.

### Acceptance Criteria
- [ ] Given ログイン済み, When 30分以内にページ遷移, Then 再ログイン不要
- [ ] Given ログイン済み, When 30分経過後にアクセス, Then 自動ログアウト
- [ ] Given セッション保持中, When ブラウザ終了, Then セッションクリア
```

---

### Step 3: Scope Definition (スコープ定義)

**In-Scope（含む）と Out-of-Scope（含まない）を明確化**:

```markdown
## Scope

### In-Scope（実装する）
- [ ] セッショントークン管理
- [ ] 30分自動延長
- [ ] セキュアなLocalStorage使用

### Out-of-Scope（実装しない）
- [ ] Remember Me 機能（将来対応）
- [ ] マルチデバイスセッション同期（将来対応）
- [ ] OAuth統合（Phase 2で対応）
```

**重要**: Out-of-Scopeを明確にすることで範囲超過を防ぐ

---

### Step 4: Success Metrics (成功指標)

**測定可能な指標を定義**:

```markdown
## Success Metrics

### 定量指標
- ログイン頻度: 現状10回/日 → 目標2回/日
- 離脱率: 現状30% → 目標10%以下
- セッションタイムアウトエラー: 目標5%以下

### 定性指標
- ユーザーフィードバック: "便利になった" コメント>50%
- サポート問い合わせ: ログイン関連問い合わせ50%削減
```

---

## Implementation Workflow

### Phase 1: Purpose Clarification (10分)

**実行内容**:
```
1. 5W1Hを埋める
2. Purpose Statementを書く
3. User Storyを書く
4. Success Metricsを定義
```

**成果物**:
- `docs/purpose/[YYYY-MM-DD]-[feature-name].md`

**禁止**:
- ❌ この手順を飛ばす
- ❌ "後で書く" と先送り
- ❌ 曖昧な表現（"改善", "最適化" だけ）

---

### Phase 2: Design Validation (5分)

**確認項目**:
```
□ Whyが明確か？
□ 成功基準が測定可能か？
□ スコープが明確か？
□ ユーザー価値が明確か？
```

**不明確な場合**:
- 実装を開始しない
- 追加の質問・調査を実施
- Purpose Statementを再作成

---

### Phase 3: Implementation (目的に沿って)

**実装中の確認**:
```
□ 目的から逸脱していないか？
□ スコープ内か？
□ 成功基準を満たすか？
```

**逸脱防止**:
- 新機能を追加したくなった → Out-of-Scopeに追加、別Issue化
- 仕様を変更したくなった → Purpose Statementを更新、承認取得

---

### Phase 4: Completion Validation (完了検証)

**確認**:
```
✅ 目的を達成したか？
✅ 成功基準をすべて満たしたか？
✅ スコープ内に収まったか？
✅ ユーザー価値を提供したか？
→ 完了
```

---

## Prohibited Patterns (アンチパターン)

### Anti-Pattern 1: "とりあえず実装"

**症状**:
```
User: "ログイン機能を追加してください"
❌ Bad: "分かりました。すぐにコードを書きます"
（目的・成功基準が不明確）
```

**正しい対応**:
```
User: "ログイン機能を追加してください"
✅ Good:
"Purpose Statementを作成します。
以下を確認させてください:

1. Why: なぜログイン機能が必要ですか？
   - セキュリティ向上？
   - ユーザー体験向上？
   - 機能制限のため？

2. Success Criteria: どうなれば成功ですか？
   - ログイン成功率？
   - セキュリティ基準？
   - ユーザー満足度？

明確化してから実装を開始します。"
```

---

### Anti-Pattern 2: "機能追加の連鎖"

**症状** (vibration-diagnosis-prototype):
```
1. セッション管理を実装
2. ついでにRemember Me機能も追加
3. ついでにOAuth統合も...
→ スコープ超過、未完成
```

**正しい対応**:
```
1. セッション管理を実装（In-Scope）
2. Remember Me → Out-of-Scope（別Issue化）
3. OAuth統合 → Out-of-Scope（Phase 2で対応）
→ スコープ内に収まる、完成
```

---

### Anti-Pattern 3: "成功基準なし"

**症状**:
```
Purpose Statement:
"パフォーマンスを改善する"

❌ Bad: 測定不可能、曖昧
```

**正しい対応**:
```
Purpose Statement:
"API応答時間を改善する"

Success Criteria:
- 平均応答時間: 現状500ms → 目標200ms
- 95パーセンタイル: 現状1000ms → 目標400ms
- エラー率: 現状5% → 維持または改善

✅ Good: 測定可能、具体的
```

---

## Templates

### Template 1: Feature Purpose Document

```markdown
# [Feature Name] Purpose Document

**作成日**: YYYY-MM-DD
**作成者**: [Name]
**ステータス**: Draft / Approved / In Progress / Completed

---

## 5W1H

### Why（なぜ）
[問題・課題・背景]

### What（何を）
[実装する機能・変更内容]

### Who（誰が）
- ユーザー: [対象ユーザー]
- 実装: [担当者]
- ステークホルダー: [影響を受ける人]

### When（いつ）
- リリース: [期限]
- 使用タイミング: [いつ使われるか]

### Where（どこで）
- 実装場所: [ファイル・モジュール]
- 動作環境: [環境]

### How（どのように）
- 実装アプローチ: [技術的詳細]
- テスト方法: [検証方法]
- 成功指標: [測定方法]

---

## Purpose Statement

### Problem（課題）
[具体的な問題]

### Solution（解決策）
[提案する機能]

### Value（価値）
[ユーザー・ビジネスへの価値]

### Success Criteria（成功基準）
- [ ] 基準1
- [ ] 基準2
- [ ] 基準3

---

## User Story

As a [ユーザータイプ],
I want [機能],
So that [目的/理由].

### Acceptance Criteria
- [ ] Given [前提], When [アクション], Then [期待結果]
- [ ] Given [前提], When [アクション], Then [期待結果]

---

## Scope

### In-Scope（実装する）
- [ ] 機能1
- [ ] 機能2

### Out-of-Scope（実装しない）
- [ ] 機能3（Phase 2で対応）
- [ ] 機能4（将来対応）

---

## Success Metrics

### 定量指標
- [指標名]: 現状[値] → 目標[値]

### 定性指標
- [指標名]: [期待する結果]

---

## Notes

[追加メモ・参考資料等]
```

---

## Multi-layer Defense (3層防御)

**Layer 1: Rules** (弱)
- `docs/rules/implementation.md` - Purpose-Driven Implementation
- `docs/rules/task-integrity.md` - タスク範囲遵守
- LLMが無視する可能性あり

**Layer 2: Skills** (中) ← **このSkill**
- **purpose-driven-impl**: 目的明確化強制
- タスク開始時に自動適用

**Layer 3: Hooks** (強)
- （該当なし - Skillで十分強力）

---

## Invocation Examples

### Example 1: 新機能実装

**User**: "検索機能を追加してください"

**Skill Response**:
```
Purpose-Driven Implementation が起動しました。

実装を開始する前に、目的を明確化します。

5W1H確認:

1. Why: なぜ検索機能が必要ですか？
   a) ユーザーが情報を見つけられない
   b) 競合他社にあるから
   c) SEO向上のため

2. What: 何を検索しますか？
   a) ドキュメント全文検索
   b) ユーザー名検索
   c) タグ検索

3. Success Criteria: どうなれば成功ですか？
   a) 検索速度 < 500ms
   b) 検索精度 > 90%
   c) ユーザー満足度 > 80%

回答いただき次第、Purpose Statementを作成します。
```

---

### Example 2: バグ修正

**User**: "このバグを修正してください"

**Skill Response**:
```
Purpose-Driven Implementation が起動しました。

バグ修正でも目的を明確化します。

5W1H確認:

1. Why: なぜこのバグが発生したか？
   [根本原因を特定]

2. What: 何を修正すべきか？
   [修正範囲を特定]

3. Success Criteria: 修正が成功したと判断する基準は？
   - [ ] バグが再現しない
   - [ ] 既存機能が壊れていない
   - [ ] テストがすべてパス

Purpose Statementを作成してから修正を開始します。
```

---

## Best Practices

### 1. Documentation First (ドキュメント優先)

**推奨**:
```
1. Purpose Documentを書く
2. レビュー・承認を得る
3. 実装を開始
```

**禁止**:
```
1. 実装を開始
2. "動いてから" ドキュメント書く
→ 目的から逸脱しやすい
```

---

### 2. YAGNI Principle (必要なものだけ)

**You Aren't Gonna Need It**:
```
In-Scope: 今必要な機能のみ
Out-of-Scope: 将来必要になるかもしれない機能
```

**例**:
```
✅ In-Scope: 基本検索
❌ Out-of-Scope: AI検索、音声検索、画像検索
（必要になったら追加）
```

---

### 3. Measurable Success (測定可能な成功)

**Good Metrics**:
```
- 応答時間: 500ms → 200ms
- エラー率: 5% → 1%
- ユーザー満足度: 70% → 85%
```

**Bad Metrics**:
```
- "速くなった"
- "改善した"
- "良くなった"
```

---

## Related Resources

### Internal
- `docs/rules/implementation.md` - Purpose-Driven Implementation詳細
- `docs/rules/task-integrity.md` - タスク範囲遵守

### External
- obra/superpowers - Purpose-First Principle
- User Story Mapping - Jeff Patton

### Phase 3成果物
- `step3.5-failure-case-analysis.md` - FP-3詳細分析
- `step2-featured-resources-analysis.md` - obra/superpowers分析

---

## Completion Criteria

```yaml
✅ 5W1H明確化完了
✅ Purpose Statement作成完了
✅ Success Criteria定義完了
✅ Scope定義完了
✅ 実装が目的に沿っている
✅ 成功基準を満たした
```

**目的不明確のまま実装開始は禁止**

---

**注意**: このSkillは自動的に起動されます。無効化したい場合は `.claude/settings.local.json` から削除してください。
