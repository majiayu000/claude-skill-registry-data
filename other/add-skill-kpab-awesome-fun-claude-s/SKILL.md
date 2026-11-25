---
name: add-skill
description: ネタ系スキルをリストに1件追加する。「このスキル追加して」「これ載せて」とURLを渡されたら使う。skills.yaml への追記と README 再生成までを一貫して行う。掲載対象は GitHub リポジトリのみ。
---

# スキルをリストに追加する

1. 渡された URL から情報を収集する
   - GitHub リポジトリなら: `gh repo view <owner>/<repo> --json name,description,stargazerCount,updatedAt,url`
   - 記事(Zenn/Qiita等)の URL を渡されたら WebFetch で内容を確認し、記事内のリポジトリリンクを正とする。リポジトリが存在しなければ掲載対象外(その旨をユーザーに伝えて終了)
2. 掲載基準を確認する: ネタ系・エンタメ系(ペルソナ・ジョーク・遊び系)であること。実務・生産性系なら掲載せず、その旨をユーザーに伝えて終了
3. `data/skills.yaml` の既存エントリと重複していないか確認する(URL とスキル名で検索)
4. YAML エントリを作成して `data/skills.yaml` に追記する
   - `description` は英語で1〜2文。スキルの「ネタ」が伝わる書き方にする(例: "Turns Claude into a Hakata-dialect gal who explains tech terms with youthful slang")
   - `category` は既存カテゴリから選ぶ。どれにも合わなければ新カテゴリをユーザーに提案して確認を取る
   - スキーマの詳細は `data/skills.yaml` 冒頭のコメントを参照
5. README を再生成する: `go run ./cmd/genreadme`
6. 生成後の README.md の該当箇所を表示してユーザーに確認してもらう
