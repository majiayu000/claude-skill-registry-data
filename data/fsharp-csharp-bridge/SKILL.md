---
name: fsharp-csharp-bridge
description: F# Domain/Application層とC# Infrastructure/Web層の型変換パターンを自律的に適用。F#↔C#境界コード実装時・型変換エラー発生時・contracts-bridge Agent作業時に使用。Phase B1で確立した4つの変換パターンをガイド。
allowed-tools: Read, Grep
---

# F#↔C# Type Conversion Patterns

## 概要

このSkillは、F# Domain/Application層とC# Infrastructure/Web層の境界で発生する型変換パターンを自律的に適用します。Phase B1 Step7で確立・実証された4つの変換パターンを提供します。

## 使用タイミング

Claudeは以下の状況でこのSkillを自律的に使用すべきです：

1. **F#↔C#境界コード実装時**
   - Contracts層のTypeConverter実装
   - Blazor ServerコンポーネントからF# Applicationサービス呼び出し
   - C# Infrastructure層からF# Domainモデル変換

2. **型変換エラー発生時**
   - `IsOk`アクセスエラー
   - Record型のRead-onlyプロパティエラー
   - Discriminated Unionのパターンマッチングエラー
   - Option型のnull参照エラー

3. **契約層作業時**
   - contracts-bridge Agent作業時の自動参照
   - DTOとDomainモデル間の変換実装時

## 4つの型変換パターン

### 1. F# Result型 ↔ C# 統合パターン

**詳細**: [`patterns/result-conversion.md`](./patterns/result-conversion.md)

**概要**:
- **IsOk/ResultValueアクセスパターン**（推奨）
- NewOk/NewError生成パターン
- Railway-oriented Programming統合

**典型的なエラー**: `Error CS1061: 'FSharpResult<T, E>' does not contain a definition for 'IsOk'`

### 2. F# Option型 ↔ C# 統合パターン

**詳細**: [`patterns/option-conversion.md`](./patterns/option-conversion.md)

**概要**:
- Some/None生成パターン
- IsSome/Valueアクセスパターン
- null許容型変換パターン

**典型的なエラー**: Option型のnull参照エラー

### 3. F# Discriminated Union ↔ C# 統合パターン

**詳細**: [`patterns/du-conversion.md`](./patterns/du-conversion.md)

**概要**:
- switch式パターンマッチング
- Role型（Discriminated Union）のC#統合
- Enumとの違い（重要）

**典型的なエラー**: `Error CS0246: The type or namespace name 'Role' could not be found`

### 4. F# Record型 ↔ C# 統合パターン

**詳細**: [`patterns/record-conversion.md`](./patterns/record-conversion.md)

**概要**:
- コンストラクタベース初期化パターン（必須）
- camelCaseパラメータ使用
- Read-onlyプロパティ対応

**典型的なエラー**: `Error CS0200: Property or indexer cannot be assigned to -- it is read only`

## 品質基準

このSkillを適用した実装は以下を満たすべきです：

- ✅ **型安全性**: コンパイル時型チェック完全通過
- ✅ **実行時安全性**: null参照例外ゼロ
- ✅ **パフォーマンス**: 不要な変換オーバーヘッドなし
- ✅ **可読性**: F#/C#それぞれの慣用句に準拠

## Phase B1での実証結果

- **実装箇所**: 36ファイル（Contracts層7ファイル・Web層3コンポーネント）
- **修正エラー数**: 36件の型変換エラーを完全解決
- **品質評価**: 97/100点（Clean Architecture準拠）
- **成功率**: 100%（0 Warning/0 Error達成）

## 関連Agents

- **contracts-bridge**: F#↔C#境界実装専門Agent（このSkillの知見を活用）
- **csharp-web-ui**: Blazor Server実装時にこのSkillを参照
- **csharp-infrastructure**: Infrastructure層実装時にこのSkillを参照

## 注意事項

1. **F# Record型は不変型**: C#のオブジェクト初期化子は使用不可
2. **Discriminated UnionはEnumではない**: switch式でパターンマッチング必須
3. **Option型はnullではない**: IsSome/Noneチェック必須
4. **Result型は例外ではない**: IsOk/ErrorValueで明示的処理

## 参考資料

- Phase B1 Step7実装記録: `Doc/08_Organization/Completed/Phase_B1/Step07_完了報告.md`
- contracts-bridge Agent定義: `.claude/agents/contracts-bridge.md`
- tech_stack_and_conventionsメモリー: F#↔C# 型変換パターンセクション
