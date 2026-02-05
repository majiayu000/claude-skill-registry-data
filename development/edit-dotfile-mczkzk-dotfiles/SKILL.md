---
name: edit-dotfile
description: dotfileの編集・修正を依頼されたとき、ホームディレクトリのファイルではなくchezmoiで管理されているファイルを優先的に確認・編集する。対象：~/.bashrc、~/.zshrc、~/.vimrc、~/.rsync-exclude、~/.config/**、~/.ssh/**、~/.claude/**など、ホームディレクトリの`.`で始まるファイル・フォルダ配下の全ファイル。
---

# CRITICAL: 必ずchezmoi配下のファイルを変更する

**ホームディレクトリ（`~/.zshrc`など）を直接読んだり変更してはいけない。**

## 最初のアクション

dotfile編集要求を受けたら、**必ず最初に** `~/.local/share/chezmoi/` 配下のファイルを検索・確認する。

## パスマッピング

- `~/.zshrc` → `~/.local/share/chezmoi/dot_zshrc`
- `~/.rsync-exclude` → `~/.local/share/chezmoi/dot_rsync-exclude`
- `~/.config/zsh/aliases/*.zsh` → `~/.local/share/chezmoi/dot_config/zsh/aliases/*.zsh`
- `~/.config/zsh/functions/*.zsh` → `~/.local/share/chezmoi/dot_config/zsh/functions/*.zsh`
- `~/.claude/CLAUDE.md` → `~/.local/share/chezmoi/dot_claude/CLAUDE.md`
- `~/.claude/skills/*/SKILL.md` → `~/.local/share/chezmoi/dot_claude/skills/*/SKILL.md`

## Zsh: エイリアス vs 関数

- **引数なし** → `dot_config/zsh/aliases/` 内の適切なファイルに追加
- **引数あり** → `dot_config/zsh/functions/` に新規ファイル作成 + `dot_zshrc` にsource行追加

フォーマット: `name() { ... }` （`function`キーワード省略）

## 最後に

編集後、必ず `chezmoi apply` をユーザーに案内する。
