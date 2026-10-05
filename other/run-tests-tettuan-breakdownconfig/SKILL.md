---
name: run-tests
description: Run a specific test file with debug logging
argument-hint: "[test-file-path]"
---

指定テストをデバッグ出力で実行する。引数なしなら全テスト実行。

```bash
LOG_LEVEL=debug deno test $ARGUMENTS --allow-env --allow-write --allow-read
```

テスト・フィクスチャは `tests/` に配置する。
