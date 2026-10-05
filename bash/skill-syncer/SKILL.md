---
name: skill-syncer
description: Sync skills from `.claude/skills` and `.gemini/skills` into `.codex/skills`. Use when the user wants to import other agents' skills, detect newer upstream skill folders, or rewrite agent-specific skill paths for Codex.
---

# skill-syncer

`.claude/skills` と `.gemini/skills` を見て、`.codex/skills` へ不足分を取り込み、source 側のほうが新しい同名スキルだけ更新する。

## Workflow

1. まず dry-run を実行して、`copied` / `updated` / `skipped` を確認する。

```bash
python3 .codex/skills/skill-syncer/scripts/sync_skills.py --json
```

2. `updated` がある場合は、必要なら対象スキルだけ中身を開いて差分を確認する。
   特に絶対パスや `.claude/skills` / `.gemini/skills` 参照が `.codex/skills` に正しく寄っているかを見る。

3. 問題なければ apply を実行する。

```bash
python3 .codex/skills/skill-syncer/scripts/sync_skills.py --apply
```

4. 実行後に `git diff -- .codex/skills` で結果を確認する。

## Notes

- source が 2 つにまたがる同名スキルは、より新しい mtime のほうを採用する
- `.codex/skills` 側が同等内容または新しい場合は上書きしない
- UTF-8 テキストは `.claude/skills` / `.gemini/skills` のパス参照を `.codex/skills` へ自動書換えする
- binary はそのままコピーする
- 自動書換えで足りないケースがあれば、apply 後に対象スキルだけ手で patch する
