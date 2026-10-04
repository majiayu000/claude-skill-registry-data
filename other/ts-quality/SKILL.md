---
name: ts-quality
description: TypeScript品質チェック。tsc型チェック/ESLint/テスト実行時に使用。「TSの品質チェック」「TypeScriptの型チェック」で起動。Do NOT use for Pythonのmypy型チェック（→ python-quality）。
allowed-tools: Bash, Read, Grep, Glob
---

## Tools
types: `npx tsc --noEmit` | lint: `npx eslint` | format: `npx prettier --check` | test: `npx jest` / `npx vitest run`

## Standards

| 項目 | 目標 |
|------|------|
| 型エラー | 0 |
| ESLint | エラー0 |
| Prettier | エラー0 |
| カバレッジ | 90%+ |

## Reference
- [reference.md](reference.md)
