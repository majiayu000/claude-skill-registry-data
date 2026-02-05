---
name: commit-push
description: git status / diff を確認し、Conventional Commits 形式でコミットしてプッシュするための手順。差分の断面を残したいときや一定量の修正がまとまったときに使用する。
---

# 目的
- 差分を整理し、適切なコミットメッセージでローカル変更をリモートに送る。
- 大きな変更前に安全なスナップショットを残す。

# 前提
- ブランチは作業内容に合致している（例: feat|fix|chore|docs/<slug>）。
- ステージングするファイルに不要物や秘密情報が含まれていない。

# 手順
1. 差分と不要ファイルを確認する  
   - `git status -sb`
   - `git diff` で内容を精査する（必要に応じて `git diff --stat`）。
2. コミットメッセージを決める  
   - 形式: `type(scope): subject [refs #<番号>]`
   - type 例: `feat`, `fix`, `chore`, `docs`, `ci`, `refactor`
   - scope 例: `ui`, `core`, `cli`, `infra`
   - subject は簡潔な現在形で。Issue 番号が無い場合は `refs #...` を省略。
3. Issue 参照の有無を確認する  
   - 関連 Issue があれば番号を記録する。無ければ省略してよい。
4. ステージングする  
   - 例: `git add <path>` または差分単位で `git add -p`
5. コミットする  
   - 例: `git commit -m "feat(ui): add preview button [refs #123]"`
6. 漏れがないか再確認する  
   - `git status -sb` で未コミットが無いことを確認する。
7. プッシュする  
   - `git push origin <ブランチ名>`

# サンプル
- Issue 参照あり: `fix(core): adjust layout [refs #482]`
- Issue 参照なし: `chore(ci): update workflow cache key`
