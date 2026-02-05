---
name: error-recovery-prompts
description: |
  エラー復旧プロンプトの設計と改善を専門とするスキル。
  ユーザーがエラーから回復するための効果的なガイダンスを提供。

  Anchors:
  - The Pragmatic Programmer / 適用: エラーハンドリング原則 / 目的: 回復可能なエラー処理
  - Nielsen Norman Group UX Guidelines / 適用: エラープロンプト設計 / 目的: ユーザビリティ向上

  Trigger:
  Use when designing error recovery flows, creating user-friendly recovery prompts, implementing retry mechanisms, or improving error handling UX.
  error recovery, recovery prompt, retry, user guidance, error handling UX
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Error Recovery Prompts

## 概要

エラー復旧プロンプトの設計と改善を専門とするスキル。
ユーザーがエラーから回復するための効果的なガイダンスを提供し、フラストレーションを最小化する。

## ワークフロー

### Phase 1: 復旧フロー設計

**目的**: エラータイプに応じた復旧フローを設計

**アクション**:

1. エラータイプと発生シナリオを分析
2. 自動/手動回復の可能性を判断
3. 段階的な復旧オプションを設計
4. プロンプト文言を作成

**Task**: `agents/design-recovery-flow.md` を参照

### Phase 2: プロンプト実装

**目的**: 設計に基づき復旧プロンプトを実装

**アクション**:

1. テンプレートを選択
2. プロンプトコンポーネントを実装
3. アクセシビリティを確保
4. アニメーション/進捗表示を実装

### Phase 3: 検証と記録

**目的**: 復旧フローの動作確認

**アクション**:

1. 各エラーシナリオをテスト
2. ユーザビリティを確認
3. `scripts/log_usage.mjs` で記録

## Task仕様ナビ

| Task | 起動タイミング | 入力 | 出力 |
|------|----------------|------|------|
| design-recovery-flow | 設計時 | エラーシナリオ | 復旧フロー設計書 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## 復旧プロンプトの基本原則

### 1. 明確なアクション提示

ユーザーが次に何をすべきかを明確に示す。

**悪い例**: "エラーが発生しました"
**良い例**: "エラーが発生しました。[再試行]ボタンをクリックしてください"

### 2. 段階的な回復オプション

```
1. 再試行 (最も簡単)
2. ページを更新
3. サポートに問い合わせ (最後の手段)
```

### 3. 進捗の保持

可能な限りユーザーの入力/進捗を保持する。

## ベストプラクティス

### すべきこと

- 復旧オプションをボタンで明示
- 自動リトライには進捗表示を追加
- データロスを防止（自動保存）
- キーボードショートカットをサポート
- フォーカス管理（プロンプトにフォーカス）

### 避けるべきこと

- 復旧方法なしでエラーを表示
- 無限リトライ
- ユーザーを責める表現
- 技術的詳細の露出

## リソース参照

### agents/（Task仕様書）

| Task | パス | 用途 |
|------|------|------|
| 復旧フロー設計 | See [agents/design-recovery-flow.md](agents/design-recovery-flow.md) | フロー設計 |

### references/（詳細知識）

| リソース | パス | 用途 |
|----------|------|------|
| プロンプトパターン | See [references/recovery-prompt-patterns.md](references/recovery-prompt-patterns.md) | パターンカタログ |

### scripts/（決定論的処理）

| スクリプト | 用途 | 使用例 |
|------------|------|--------|
| `log_usage.mjs` | フィードバック記録 | `node scripts/log_usage.mjs --result success` |

### assets/（テンプレート）

| テンプレート | 用途 |
|--------------|------|
| `recovery-prompt-template.md` | 復旧プロンプトテンプレート |

## 変更履歴

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-01-01 | 18-skills.md仕様完全準拠、agents追加、Level1-4削除 |
| 1.0.0 | 2025-12-24 | 初版作成 |
