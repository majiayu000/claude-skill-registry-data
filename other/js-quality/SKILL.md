---
name: js-quality
description: JavaScript品質チェック。ESLint/Prettier/Jest実行時に使用。「JSの品質チェック」「JavaScriptの静的解析」で起動。Do NOT use for TypeScript（→ ts-quality）。
allowed-tools: Bash, Read, Grep, Glob
---

## Tools
lint: `npx eslint` | format: `npx prettier --check` | test: `npx jest` / `npx vitest run`

## Standards

| 項目 | 目標 |
|------|------|
| ESLint | エラー0 |
| Prettier | エラー0 |
| カバレッジ | 90%+ |

## Reference
- [reference.md](reference.md)
