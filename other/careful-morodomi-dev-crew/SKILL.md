---
name: careful
description: prod作業時に破壊コマンドをブロック。rm -rf /, DROP TABLE, force-push, git reset --hard, kubectl deleteを検出しexit 2でBLOCK。
allowed-tools:
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "bash ${CLAUDE_PLUGIN_ROOT}/scripts/hooks/careful-guard.sh"
---

# careful

本番作業時に破壊的なコマンドをブロックするスキル。

## 検出対象

| パターン | 理由 |
|---------|------|
| `rm -rf /` or `rm -rf ~` | ルート/ホーム全削除 |
| `DROP TABLE` / `DROP DATABASE` | DB破壊 |
| `git push --force` (`--force-with-lease` は許可) | リモート履歴破壊 |
| `git reset --hard` | ローカル変更消失 |
| `kubectl delete` | K8sリソース削除 |

## Usage

```
/careful
```

スキル呼び出し後、セッション内で上記コマンドが Bash ツール経由で実行されると exit 2 でブロックされる。
