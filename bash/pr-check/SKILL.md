---
name: pr-check
description: PR がレビューを受け付けてよい前提条件（差分サイズ）を満たすかを判定し、結果を PR にコメントする。「pr-check」「PRをチェックして」と指示されたとき。
argument-hint: '[PR番号]'
allowed-tools: Bash(node scripts/pr-check.mjs:*)
---

# PR Check

次のスクリプトを実行する。PR 番号が無ければ現ブランチの PR が対象になる。

```bash
node scripts/pr-check.mjs $ARGUMENTS
```

判定と PR へのコメントはスクリプトが行う。

> [!IMPORTANT]
> **（AI・必須）** スクリプトが出した判定（OK / NG）・行数・コメントの URL をそのまま報告する。自分で行数を数え直したり、判定を言い換えたりしない。AI が数えると、同じ PR でも実行のたびに結果が変わりうるため。

スクリプトが失敗したとき（PR が見つからないなど）は、エラーメッセージをそのまま伝えて終える。
