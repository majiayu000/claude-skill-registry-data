---
name: reviewing-silent-failures
description: >
  Silent failure detection patterns for frontend code.
  Triggers: silent failure, empty catch, エラーハンドリング, 握りつぶし, swallowed error.
allowed-tools: [Read, Grep, Glob, Task]
agent: silent-failure-reviewer
user-invocable: false
---

# サイレント障害レビュー

## 検出

| ID  | パターン                             | 修正                                          |
| --- | ------------------------------------ | --------------------------------------------- |
| SF1 | `catch (e) {}`                       | `catch (e) { logger.error(e); throw }`        |
| SF1 | `catch (e) { console.log(e) }`       | ユーザーフィードバック表示 + コンテキストログ |
| SF2 | `.catch()`なしの`.then(fn)`          | `.catch()` 追加またはtry/catch使用            |
| SF2 | `async () => { await fn() }`         | try/catchでラップ、エラー処理                 |
| SF3 | エラーUI状態なし                     | Error Boundary、フィードバックコンポーネント  |
| SF4 | サイレントな `value ?? defaultValue` | フォールバック使用時にログ                    |
| SF4 | `data?.nested?.value`                | 予期せぬnullをチェックして報告                |

## 参考

| トピック | ファイル                           |
| -------- | ---------------------------------- |
| 検出     | `references/detection-patterns.md` |
