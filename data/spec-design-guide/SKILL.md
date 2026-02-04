---
name: spec-design-guide
description: 仕様（Why）と設計（How）を記録し、Living Documentation原則でコードと常に同期させる
---

# Spec-Design-Guide Skill

このスキルは、プロジェクトの仕様・設計ドキュメント作成をガイドし、Living Documentation原則に基づいてドキュメントとコードを同期管理します。

## エイリアス

このスキルは以下のように呼ぶことができます：

- `spec-design-guide` → 「仕様設計ガイド」
- `sdg` → 「仕様設計ガイド」の略称

## 目的

実装前に仕様と設計を明確にし、実装の助けとなるドキュメントを体系的に管理します。
ドキュメントは「生きた写像」としてコードと常に同期し、技術的負債を防ぎ、生きたメモリーとして機能します。

## ストレージ

**重要**: すべてのドキュメントはCreo Memoriesに保存されます。

- **ドメイン**: `sdg`（domain:019b1c05-b0d6-7eb8-95a6-1aa0c5601338）
- **カテゴリ**: `spec`, `design`, `guide`
- **タグ**: 機能名、技術名などで分類

### Creo Memoriesとの連携

ドキュメントの操作にはCreo Memories MCPツールを使用します：

```typescript
// ドキュメントを保存
remember_context({
  content: "# Core Concepts - 仕様書\n...",
  category: "spec",
  tags: ["core-concepts", "architecture"],
  metadata: {
    title: "Core Concepts - 仕様書",
    docType: "spec"
  }
})

// ドキュメントを検索
recall_relevant({
  sessionId: "...",
  query: "認証システム設計",
  threshold: 0.7
})

// カテゴリで一覧
search_memories({
  category: "spec",
  limit: 20
})
```

## スキルの起動タイミング

このスキルは以下の場合に自動的に適用されます：

- ✅ コード変更・追加を行う際
- ✅ 新機能の設計・実装を行う際
- ✅ 既存機能のリファクタリングを行う際
- ✅ バグ修正で設計に影響がある際

**ユーザーがスキルを明示的に呼び出す方法**:

- `/spec-design-guide` または `/sdg` コマンド
- 「spec」「design」「SPEC.md」「設計書」などのキーワードを含む質問

## 関連リファレンス

- [Living Documentation原則](reference/living-documentation.md) - ドキュメントとコードの同期管理の詳細

## ドキュメントの役割

### spec（カテゴリ）- コンセプト、仕様、哲学

**What & Why** - 何を作るか、なぜ作るか

- コンセプト・ビジョン
- 設計哲学・原則
- 機能仕様
- ユーザー体験

### design（カテゴリ）- モデル、手法、実装

**How** - どう作るか

- データモデル
- アーキテクチャ
- 実装手法
- 技術的詳細

### guide（カテゴリ）- ガイド

**Usage** - どう使うか

- 使い方
- ベストプラクティス
- トラブルシューティング

## spec のテンプレート

**目的**: コンセプト、仕様、哲学
**カテゴリ**: `spec`
**タグ**: 機能名（例: `core-concepts`, `storage`, `mcp`）

```markdown
# {機能名} - 仕様書

## コンセプト

### ビジョン

この機能が目指すもの、解決する問題、提供する価値。

### 哲学・設計原則

- 原則1: なぜこの設計を選んだか
- 原則2: トレードオフと判断基準
- 原則3: ユーザー体験への配慮

### 他との違い

既存のソリューションとの違い、独自性。

### システム概要図

\`\`\`mermaid
flowchart TD
A[入力] --> B[処理]
B --> C[出力]
B --> D{条件分岐}
D -->|Yes| E[処理A]
D -->|No| F[処理B]
\`\`\`

## 仕様

### 機能仕様

#### FS-001: 機能名

**目的**: この機能が何をするか

**入力/出力**:

- 入力: ...
- 出力: ...

**振る舞い**:

1. ステップ1
2. ステップ2

**制約**:

- 制約1

### インターフェース仕様

\`\`\`typescript
// ユーザーが使う形式
function example() {
// ...
}
\`\`\`

### 非機能仕様

- **パフォーマンス**: 期待される性能
- **セキュリティ**: セキュリティ考慮事項
- **互換性**: 後方互換性の方針

## 哲学的考察

### なぜこの仕様か

選択の理由、背景にある思想。

### ユーザー体験

ユーザーがどう感じるか、どう使うか。

### 進化の方向性

将来どう発展させるか、拡張の余地。

## 変更履歴

### YYYY-MM-DD: 変更内容

- **理由**: なぜこの変更が必要だったか
- **影響**: どのコンポーネントに影響するか
- **コミット**: コミットハッシュ
```

## design のテンプレート

**目的**: モデル、手法、実装
**カテゴリ**: `design`
**タグ**: 設計種類（例: `architecture`, `data-model`, `api`）

```markdown
# {設計種類} - 設計書

## 設計思想: Simplicity（シンプルさ）

シンプルなコードを実現するため、以下の原則に従う。

### 型の分類

基本的に、全ての型は以下に分類される：

- **data**: 値を保持する
- **calculations**（主に同期）: 値を計算する
- **actions**（主に非同期）: 値を操作する

calculations, actionsは関数的に実装されるのが望ましい。

### Straightforward原則

入力から出力までの経路を直線的に、最小限のステップになるように、ロジックを組み立てる。

**これらの原則を守ることで、理解しやすく保守しやすいシンプルなコードが実現される。**

## データモデル

### 構造定義

\`\`\`typescript
interface Example {
  field1: Type1
  field2: Type2
}
\`\`\`

### モデルの関係性

\`\`\`mermaid
classDiagram
class ModelA {
+field1: Type1
+field2: Type2
+method1()
}
class ModelB {
+field1: Type1
+method1()
}
class ModelC {
+field1: Type1
}
ModelA --> ModelB : uses
ModelA --> ModelC : contains
\`\`\`

## アーキテクチャ

### コンポーネント構成

\`\`\`mermaid
flowchart LR
Input[入力] --> Parser[パーサー]
Parser --> Validator[バリデーター]
Validator --> Processor[プロセッサー]
Processor --> Output[出力]
\`\`\`

### コンポーネント詳細

#### Component A

**責務**: ...
**インターフェース**:
\`\`\`typescript
interface ComponentA {
  method(): Promise<T>
}
\`\`\`

## 実装手法

### アルゴリズム

処理の流れ、アルゴリズムの選択理由。

\`\`\`mermaid
sequenceDiagram
participant User
participant System
participant Database

    User->>System: リクエスト
    System->>Database: データ取得
    Database-->>System: データ
    System->>System: 処理
    System-->>User: レスポンス

\`\`\`

### エラーハンドリング

\`\`\`typescript
class MyError extends Error {
  constructor(message: string) {
    super(message)
  }
}
\`\`\`

### パフォーマンス最適化

- 最適化ポイント1
- 最適化ポイント2

## テスト戦略

### ユニットテスト

- テスト対象1
- テスト対象2

### 統合テスト

- シナリオ1
- シナリオ2

## 実装チェックリスト

- [ ] データモデル実装
- [ ] コア機能実装
- [ ] エラーハンドリング
- [ ] テスト作成
- [ ] ドキュメント更新

## 変更履歴

### YYYY-MM-DD: 変更内容

- **理由**: なぜこの変更が必要だったか
- **影響**: どのコンポーネントに影響するか
- **コミット**: コミットハッシュ
```

## guide のテンプレート

**目的**: 実用的な使い方ガイド
**カテゴリ**: `guide`
**タグ**: トピック名（例: `getting-started`, `deployment`, `troubleshooting`）

````markdown
# {トピック名}

## 概要

このガイドの目的と対象読者。

## 前提条件

- 必要な環境
- 必要な知識
- 必要なツール

## 手順

### ステップ1: ...

詳細な説明とコード例。

```bash
# コマンド例
```
````

### ステップ2: ...

## コード例

```typescript
// 実用的なコード例
```

## ベストプラクティス

- 推奨される使い方
- アンチパターン

## トラブルシューティング

### 問題1: ...

**症状**: ...
**原因**: ...
**解決策**: ...

## よくある質問

**Q**: ...
**A**: ...

## 次のステップ

関連するガイドへのリンク。

````

## ワークフロー

### 新機能追加時

1. **spec** にドキュメントを保存
   ```typescript
   remember_context({
     content: "# 新機能 - 仕様書\n...",
     category: "spec",
     tags: ["new-feature", "v2"]
   })
````

2. **design** に設計を保存
   ```typescript
   remember_context({
     content: "# 新機能 - 設計書\n...",
     category: "design",
     tags: ["new-feature", "architecture"]
   })
   ```

3. **guide** に使い方を追加（必要に応じて）

4. 実装開始

5. 実装完了後、ドキュメント更新

### 既存機能修正時

1. 関連する仕様を検索
   ```typescript
   recall_relevant({
     sessionId: "...",
     query: "該当機能の仕様"
   })
   ```

2. 設計ドキュメントを検索・確認

3. 変更が設計に影響する場合、ドキュメントを更新

4. 実装

### ドキュメント検索の方法

```typescript
// セマンティック検索（意味で検索）
recall_relevant({
  sessionId: "...",
  query: "認証システムの設計",
  threshold: 0.7
})

// カテゴリ検索
search_memories({
  category: "spec",
  limit: 20
})

// タグ検索
search_memories({
  tags: ["authentication"],
  limit: 10
})
```

## Claudeへの指示

**重要**: このスキルが有効な場合、コード変更を提案・実装する際は必ず以下を実行してください：

### 設計思想: Simplicity（シンプルさ）の追求

コード設計・実装時は、**Simplicity（シンプルさ）** を最優先してください。
以下の原則を守ることで、理解しやすく保守しやすいコードを実現します。

#### 型の分類

全ての型は以下に分類されます：

- **data**: 値を保持する不変データ構造
  - 例: `interface User { id: UserId; name: string }`
  - 純粋なデータ、ビジネスロジックを持たない

- **calculations**（主に同期）: 値を計算する純粋関数
  - 例: `function calculateTotal(items: Item[]): Money`
  - 副作用なし、同じ入力に対して常に同じ出力
  - 関数的に実装（引数を受け取り、結果を返す）

- **actions**（主に非同期）: 値を操作する副作用のある関数
  - 例: `async function saveUser(user: User): Promise<void>`
  - I/O、状態変更、外部システムとの通信
  - 関数的に実装（引数を受け取り、Resultを返す）

#### Straightforward原則

- 入力から出力までの経路を**直線的**に
- **最小限のステップ**でロジックを組み立てる
- 不要な中間層、抽象化、間接参照を避ける
- コードの流れが追いやすく、理解しやすいことを優先

**→ これらの原則 = Simplicity（シンプルさ）の実現**

### コード変更時の必須手順

1. ✅ Creo Memoriesで関連するspecドキュメントを検索
2. ✅ specを読んで「なぜ」（What & Why）を理解
3. ✅ 関連するdesignドキュメントを検索して読む（How）
4. ✅ コード変更を実施
5. ✅ spec/designドキュメントとの乖離をチェック
6. ✅ 乖離があればドキュメントを更新（remember_contextで保存）
7. ✅ 必要に応じてguideも更新

### 視覚化の推奨

**マーメイド図を積極的に活用**してください：

#### specでの図の使用

- ✅ **フローチャート**: システムの処理の流れ、ユーザーの操作フロー
- ✅ **状態遷移図**: ステートマシン、ライフサイクル
- ✅ **シーケンス図**: ユーザーとシステムの対話

#### designでの図の使用

- ✅ **クラス図**: データモデルの関係性
- ✅ **フローチャート**: アーキテクチャ、コンポーネント構成
- ✅ **シーケンス図**: コンポーネント間の相互作用
- ✅ **ER図**: データベース設計（該当する場合）

### 禁止事項

- ❌ specを確認せずにコード変更
- ❌ designの関連ドキュメントを確認せずに設計変更
- ❌ ドキュメント更新を忘れる
- ❌ 古い情報を放置
- ❌ 実装とドキュメントの不一致を許容
- ❌ 図で表現できるものをテキストだけで説明

### Living Documentation原則

> **ドキュメントは死んだテキストではなく、生きたコードベースの鏡である**

#### 基本原則

- ドキュメントとコードは常に同期
- 一方が変われば他方も変わる
- 不一致は技術的負債（バグ）として扱う

#### 生きたメモリーとしての機能

ドキュメントは**AIエージェント（Claude）が信頼して活用できる生きたメモリー**として機能する：

- ✅ **常に新鮮**: 最新のコード状態を正確に反映
- ✅ **信頼できる**: 実装と完全に一致し、嘘がない
- ✅ **活用可能**: AIエージェントが読んで理解し、意思決定の根拠にできる
- ✅ **進化する**: コードの変化とともに成長・更新される
- ✅ **検索可能**: セマンティック検索で関連ドキュメントを即座に発見

## まとめ

このスキルは、仕様と設計を明確にし、Living Documentation原則に基づいてドキュメントとコードを同期させることで、プロジェクトの品質と保守性を高めます。

**キーポイント**:

- 📝 **spec**: What & Why（Creo Memoriesに保存）
- 🏗️ **design**: How（Creo Memoriesに保存）
- 📖 **guide**: Usage（Creo Memoriesに保存）
- 🎯 **Simplicity**: 型分類 + Straightforward原則 = シンプルさ
- 🔄 **Living Documentation**: ドキュメントとコードの同期
- 🔍 **セマンティック検索**: 関連ドキュメントを意味で検索
- 📊 **マーメイド図**: 積極的な視覚化で理解しやすく
