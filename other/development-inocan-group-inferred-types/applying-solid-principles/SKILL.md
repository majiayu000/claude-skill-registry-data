---
name: applying-solid-principles
description: Applies SOLID principles and clean code practices. Required for all code implementations. Covers single responsibility, open-closed, and dependency injection principles.
---

# SOLID原則とクリーンコード

## 🎯 使用タイミング
- **すべてのコード実装時（必須）**
- **リファクタリング時**
- **コードレビュー時**
- **設計判断時**

## 📚 ドキュメント構成

このスキルは以下のドキュメントで構成されています：

### 1. [SOLID原則の詳細](./SOLID-PRINCIPLES.md)
5つのSOLID原則の詳細解説とコード例：
- **S**: Single Responsibility（単一責任）
- **O**: Open/Closed（開放閉鎖）
- **L**: Liskov Substitution（リスコフの置換）
- **I**: Interface Segregation（インターフェース分離）
- **D**: Dependency Inversion（依存関係逆転）

各原則について、悪い例と良い例を対比して解説します。

### 2. [クリーンコードの基礎](./CLEAN-CODE-BASICS.md)
日常的なコーディングで適用すべき基本原則：
- 意図を明確にする命名規則
- 小さく単一責任の関数設計
- 早期リターンによるネスト削減
- マジックナンバーの排除

### 3. [品質チェックリスト](./QUALITY-CHECKLIST.md)
実装完了前の確認項目：
- 設計原則の遵守チェック
- コードスメルの検出
- リファクタリングの判断基準

### 4. [クイックリファレンス](./QUICK-REFERENCE.md)
素早く参照できる簡潔な情報：
- SOLID原則の1行まとめ
- よくある間違いと修正方法
- コードレビューポイント

## 🎯 SOLID原則の概要

### S - Single Responsibility Principle（単一責任の原則）
**「変更する理由」は1つだけ**
- 各クラス・関数は単一の責任のみを持つ
- 例: UserServiceはユーザー管理のみ、EmailServiceはメール送信のみ

### O - Open/Closed Principle（開放閉鎖の原則）
**拡張に開いており、修正に閉じている**
- 新機能追加時は既存コードを変更せず、拡張で対応
- インターフェースや抽象クラスを活用

### L - Liskov Substitution Principle（リスコフの置換原則）
**派生クラスは基底クラスと置換可能**
- サブクラスは親クラスの契約を破らない
- 継承よりコンポジションを優先

### I - Interface Segregation Principle（インターフェース分離の原則）
**クライアントが使用しないメソッドへの依存を強制しない**
- 大きなインターフェースより小さな特化したインターフェース
- 必要なメソッドのみを実装

### D - Dependency Inversion Principle（依存関係逆転の原則）
**上位モジュールは下位モジュールに依存しない**
- 両者は抽象に依存する
- 依存性注入（DI）を積極的に活用

## 🚀 実装時のアプローチ

### 1. 設計フェーズ
1. SOLID原則を念頭に置いて設計
2. 責任を明確に分離
3. インターフェースで抽象化

### 2. 実装フェーズ
1. クリーンコードの基本原則を適用
2. 小さく、テストしやすい関数を作成
3. 意図が明確な命名を心がける

### 3. レビューフェーズ
1. 品質チェックリストで確認
2. コードスメルを検出
3. リファクタリングの必要性を判断

## 💡 重要な原則

### DRY（Don't Repeat Yourself）
- コードの重複を避ける
- 共通処理は関数化・モジュール化

### YAGNI（You Aren't Gonna Need It）
- 不要な機能を実装しない
- 必要になってから実装する

### KISS（Keep It Simple, Stupid）
- シンプルな設計を心がける
- 過度な抽象化を避ける

## 🔗 関連スキル

- **[enforcing-type-safety](../enforcing-type-safety/SKILL.md)**: 型安全性の確保
- **[testing](../testing/SKILL.md)**: テストファーストアプローチ
- **[securing-code](../securing-code/SKILL.md)**: セキュアコーディング

## 📖 次のステップ

1. **初めての方**: [SOLID原則の詳細](./SOLID-PRINCIPLES.md)から読み始めてください
2. **日常的な実装**: [クリーンコードの基礎](./CLEAN-CODE-BASICS.md)を参照
3. **コードレビュー時**: [品質チェックリスト](./QUALITY-CHECKLIST.md)を活用
4. **素早い確認**: [クイックリファレンス](./QUICK-REFERENCE.md)で要点をチェック
