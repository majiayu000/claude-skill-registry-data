---
name: doc-generator
description: コードからドキュメントを自動生成するスキル。関数やクラスのJSDoc/TSDocコメント、README、APIリファレンスなどを生成する際に使用します。
allowed-tools: Read, Write, Grep, Glob
---

# ドキュメント生成スキル

このスキルは、コードベースからドキュメントを自動生成します。

## 対応するドキュメント形式

### 1. インラインドキュメント
- **JSDoc/TSDoc**: JavaScript/TypeScript の関数・クラス・インターフェース
- **Docstring**: Python の関数・クラス・モジュール
- **GoDoc**: Go の関数・構造体・パッケージ

### 2. スタンドアロンドキュメント
- **README.md**: プロジェクト概要、セットアップ手順、使用方法
- **API リファレンス**: エンドポイント一覧、リクエスト/レスポンス例
- **CHANGELOG.md**: バージョン履歴、変更内容

## 生成ルール

### JSDoc/TSDoc の場合
```typescript
/**
 * [関数の簡潔な説明]
 *
 * @param {型} paramName - パラメータの説明
 * @returns {型} 戻り値の説明
 * @throws {ErrorType} エラーが発生する条件
 * @example
 * // 使用例
 * const result = functionName(arg);
 */
```

### README.md の場合
1. プロジェクト名とバッジ
2. 概要（1-2文で説明）
3. 特徴・機能一覧
4. インストール方法
5. 使用方法（コード例付き）
6. 設定オプション
7. ライセンス

## テンプレート参照

JSDoc/TSDocを生成する際は、以下のテンプレートに従ってください：

@.claude/skills/doc-generator/templates/jsdoc.md

## 品質基準

- 説明は具体的かつ簡潔に
- 技術的に正確であること
- 実際のコードと整合性があること
- 使用例は動作するコードであること
