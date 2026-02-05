---
name: lint-checker
description: コード品質チェック専門スキル。TypeScript/JavaScript ファイルの ESLint、型チェック、コーディング規約を検証する。
---

# lint-checker

> **コード品質チェック専門スキル**

---

## 役割

TypeScript/JavaScript ファイルのコード品質を自動チェックし、問題を指摘・修正する。

---

## 発火条件（確定的パターン）

このスキルは以下の場合に**必ず**実行される：

```yaml
トリガー:
  - TypeScript/JavaScript ファイルを作成・編集した後
  - コミット前のコード品質確認
  - ユーザーが「lint して」「コードチェックして」と言った場合
```

---

## チェック項目

```yaml
1. ESLint ルール違反:
   - 未使用変数
   - console.log の残存
   - any 型の多用

2. TypeScript エラー:
   - 型エラー
   - null/undefined チェック漏れ

3. コーディング規約:
   - 命名規則
   - インデント
   - セミコロン

4. ベストプラクティス:
   - async/await の適切な使用
   - error handling の有無
```

---

## 実行手順

```bash
# 1. ESLint 実行
pnpm lint

# 2. TypeScript チェック
pnpm tsc --noEmit

# 3. 結果の解析と報告
```

---

## 出力形式

```
=== Lint Checker Results ===

[ESLint]
✓ No errors found

[TypeScript]
✗ 3 errors found:
  - src/app/page.tsx:15 - Type 'string' is not assignable to type 'number'
  - src/components/Header.tsx:8 - 'useState' is declared but never used

[Recommendations]
1. Fix type error in page.tsx:15
2. Remove unused import in Header.tsx

=== Summary ===
Status: FAIL
Errors: 3
Warnings: 0
```

---

## 修正提案

問題を発見した場合、以下を提案：

```yaml
自動修正可能:
  - pnpm lint --fix で修正

手動修正必要:
  - 型エラーの修正方法を具体的に提案
  - コード例を提示
```

---

## 使用例

### CLAUDE.md への統合（確定的発火）

```markdown
## コード作成後の必須事項

- TypeScript/JavaScript ファイルを作成・編集した後は、必ず `lint-checker` スキルを実行すること
```

この記載により、LLM は TypeScript/JavaScript ファイルを編集するたびに自動的にこのスキルを呼び出す。

---

## 設定ファイル

```yaml
必要なファイル:
  - .eslintrc.json: ESLint 設定
  - tsconfig.json: TypeScript 設定
  - package.json: lint スクリプト

推奨設定:
  - ESLint: next/core-web-vitals
  - TypeScript: strict mode
```
