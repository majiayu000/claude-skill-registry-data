---
name: local-ci
description: Run local CI checks before merge or push
---

push前にCIを通すため、`deno task ci` を実行する。エラー時は `deno task ci --log-mode debug` で詳細確認する。

全チェック通過までpush禁止。
