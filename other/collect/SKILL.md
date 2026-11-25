---
name: collect
description: ネタ系スキルの新規候補を発掘する。「新しいネタスキル探して」「候補集めて」「巡回して」と言われたら使う。GitHub を定型クエリで巡回し、未掲載のリポジトリ候補をリストアップする。
---

# ネタ系スキルの候補を発掘する

掲載対象は **GitHub リポジトリのみ**(スキル/プラグイン/Claude Code 連動ツール)。記事(Zenn/Qiita 等)は掲載対象外。記事で見つけたスキルでも、リポジトリが公開されていればリポジトリを候補にする。

1. `data/skills.yaml` を読み、掲載済み URL の一覧を把握する(重複提案を防ぐ)
2. GitHub を巡回する: `gh search repos "<kw>" --sort stars --limit 15 --json fullName,description,stargazersCount,updatedAt`
   - キーワード例: `claude persona`, `claude personality`, `claude character`, `claude roast`, `claude joke`, `claude tamagotchi`, `claude pet`, `claude code game`, `claude code rpg`, `claude output style`
   - 新着を狙うなら `--created ">直近2ヶ月の日付"` を付けてもう1周
   - 補助: Hacker News(WebFetch で `https://hn.algolia.com/api/v1/search?query=claude%20persona&tags=story`)で話題のリポジトリを拾ってもよい
3. 候補の判定基準(すべて満たすこと):
   - ネタ系・エンタメ系であること(実務・生産性系は除外。例: ゲーム「開発」支援は実務系、Claude と「遊ぶ」ものはネタ系)
   - GitHub リポジトリとして公開されており、実体があること(`gh api "repos/<owner>/<repo>/contents"` で SKILL.md・プラグイン構成・プロンプト等を確認)
   - 未掲載であること(手順1の一覧と突き合わせ)
   - 質を優先: スター数の高いものから検討する(ニッチ全体が低スターなので絶対値は問わないが、同種なら高い方)
4. 候補を表形式でユーザーに提示する: スキル名 / URL / スター数 / 一言説明 / おすすめ度
5. ユーザーが選んだものを add-skill の手順で追加する(1件ずつ)
