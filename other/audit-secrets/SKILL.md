---
description: 公開側 (home/ と scripts/) とコミット履歴に秘匿値が混ざっていないかを走査する。コミット・push の前や、管理対象を増やした直後に使う。ユーザーが「秘匿値をチェックして」「公開して大丈夫か見て」「/audit-secrets」等を指示したときに使う。
allowed-tools: Bash(git status:*) Bash(git diff:*) Bash(git log:*) Bash(git grep:*) Bash(git ls-files:*) Bash(git cat-file:*) Bash(git rev-list:*) Bash(git check-ignore:*) Bash(grep:*) Bash(python3:*)
---

このリポジトリは GitHub 上で public。**`home/` と `scripts/` に置いたものは全世界から読める。** 置き場の定義は `docs/placement.md`。

## 進め方

1. **除外が効いているか**: `git check-ignore -v private/.aws/credentials private/.ssh` で `/private/` が効いていることを確認する。`git status --porcelain` に `private/` が現れたら**そこで止める**

2. **公開側の走査**: 追跡ファイルと未追跡ファイルの両方を見る

   ```sh
   git status --porcelain --untracked-files=all | awk '{print $2}' | \
     xargs grep -lniE 'sk-ant|sk-proj|ghp_|github_pat_|AKIA[0-9A-Z]{16}|xox[bpsa]-|_authToken|BEGIN [A-Z ]*PRIVATE KEY'
   ```

   併せて `[A-Za-z0-9_-]{25,}` の長いリテラルを拾い、変数参照か実値かを 1 件ずつ判定する

3. **検出したら値と参照を切り分ける**: `$SWITCHBOT_API_KEY` のような参照は問題ない。実値なら 1Password の Environment 「dotfiles」へ移し、参照に置き換え、使うコマンドを `with-secrets` 経由にする

4. **履歴の走査**: 全ブランチの全 blob を舐める。パターン一致だけでなく、`.aws` / `.ssh` / `.config` 等のパスが履歴に現れていないかも見る

   ```sh
   git rev-list --objects --all | awk '{print $1}' | sort -u > /tmp/objs.txt
   git cat-file --batch-check='%(objectname) %(objecttype)' < /tmp/objs.txt | awk '$2=="blob"{print $1}' | \
     while read -r b; do git cat-file blob "$b" | grep -qaE '<パターン>' && echo "HIT: $b"; done
   git log --all --pretty=format: --name-only --diff-filter=A | sort -u | grep -E '\.aws|\.ssh|\.gcp|credentials|\.env'
   ```

5. **`.npmrc` / `.yarnrc` 等の見落としやすいファイル**は、パターンに頼らず全リビジョンの中身を直接見る

6. **`private/.zsh_history` の走査**: シェル履歴は**日々書き足される**ため、一度きれいにしても再び混入する。`grep` は履歴を binary と判定して出力を抑止するので **`-a` を付ける**

   ```sh
   grep -acE '(API_KEY|TOKEN|SECRET|PASSWORD)=[A-Za-z0-9_/+=-]{16,}' private/.zsh_history
   ```

   検出したら値を `REDACTED` へ置換する。**行の削除ではなく置換**にする（履歴の行番号がずれると、複数行にまたがる項目が壊れる）

7. **履歴に見つかった場合はユーザーへ報告して止まる**。`reset --soft` での書き換えと force push はユーザーの判断事項

## 出力の目安

走査ごとに「対象範囲」と「検出件数」を表で示し、検出があれば**ファイル:行と、実値か参照かの判定**を添える。**値そのものは出力しない**（会話ログに残るため）。

```markdown
| 走査 | 範囲 | 結果 |
| --- | --- | --- |
| 除外の確認 | private/ 配下 4 パス | 全て ignore 済み |
| 公開側 | 追跡 56 + 未追跡 8 ファイル | 検出ゼロ |
| 履歴 | 全ブランチ 115 blob | 検出ゼロ |
```

## やってはいけないこと

- 検出した値を会話に出力すること。`${VAR:-×}` のように**未設定時の代替を書くと設定時に実値が出る**。`${VAR:+○}` を使う
- **該当行を加工して出すこと。** マスクを掛けた変数と、実際に出力する変数が別になっていると素通りする（`awk '{print $1}'` は行頭の `TOKEN=<値>` をそのまま出す）。**出してよいのは行番号と件数だけ**で、それで判断には足りる
- 追跡ファイルだけを見て終えること。**次のコミットで入るのは未追跡ファイル**
- `private/.config` 等の巨大ディレクトリを走査対象に含めること（ミニファイされた JS が大量に一致して出力が溢れる）
- 履歴に見つかったものを、指示を待たずに書き換えること
