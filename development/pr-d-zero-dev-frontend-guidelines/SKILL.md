---
name: pr
description: プルリクエストの作成とプッシュ（プリフライトチェック、base 追従、コンフリクト検知含む）
---

1. `dev` ではないトピックブランチにいることを確認する。
2. **base 追従（コンフリクト予防）**: `git fetch origin dev` を実行し、`git log HEAD..origin/dev --oneline` で base が進んでいないか確認する。進んでいれば push 前に `git rebase origin/dev` する。ドキュメント系のコンフリクトは機械的に解決せず、base 側で追加された内容を方針（sidebar 構成・見出し構造）に沿って取り込むこと。
3. **プリフライトチェック（必須 — 省略不可）:**
   - `yarn lint`、`yarn build` がこのセッション内でまだ実行・成功していない場合、続行する前に**今すぐ実行**する。rebase を行った場合は rebase 後に再実行する。
   - このリポジトリに `yarn test` は存在しない。
   - 全てがパスしなければならない。失敗があれば続行前に修正する。
4. 適切な `git` コマンドを使って現在のトピックブランチの変更をレビューする。
   - **機密・案件情報とサンプル慣例のダブルチェック**: base branch との全 diff（`git diff dev...HEAD`）に対して、`.claude/skills/git/SKILL.md` の「機密・案件情報の検出」と「サンプル値の慣例チェック」を再実行する。コミット単位のチェックをすり抜けた企業名・顧客情報・実在ドメイン・未取得ドメイン・案件識別子・実データ断片がないかを PR 全体で確認する。検出したら汎用値へ書き換えて追加コミットする。
5. **PR body を一時ファイルに保存する**: scratchpad ディレクトリに PR body（markdown）を書き出す。**PR body は diff の要約であり会話の要約ではない** — セッション中に出てきた顧客名・案件名・社外秘情報は、diff 自体に含まれていない限り書き込まない。
6. **push と PR 作成はユーザーが実行する**: エージェントは `git push` / `gh pr create` を実行せず、ユーザーがそのまま実行できる `!` 付きコマンドを提示する。ファイルパス引数は必ずダブルクオーテーションで囲む。

   ```
   ! git push -u origin <branch>
   ! gh pr create --base dev --title "<title>" --body-file "<PR body の一時ファイルパス>"
   ```

7. **マージ可能性の確認（CI watch では捕捉できない）:**
   - ユーザーから PR 作成の報告を受けたら、まず `gh pr view <number> --json mergeable,mergeStateStatus` で **`CONFLICTING` / `DIRTY` を検知**する。`gh pr checks --watch` はステータスチェックしか見ないため、コンフリクトは黙って素通りする。
   - `CONFLICTING` なら CI を待たずにステップ 2 の base 追従（rebase + 方針に沿った解決）に戻り、解決後にユーザーへ `! git push --force-with-lease` を依頼する。
8. **CI 監視:**
   - `gh pr checks --watch` を**バックグラウンド実行**で起動して CI の完了を待機する（フォアグラウンド実行はターン内タイムアウトで出力が欠損する）。
   - テストが途中で失敗した場合は完了を待たずに修正作業に戻る。
   - 全テストが通ったら、`gh pr view <number> --json mergeable,mergeStateStatus` で再度 `CONFLICTING` / `DIRTY` になっていないか確認する（CI 実行中に base が進んで新たにコンフリクトが発生している可能性があるため）。
   - `CONFLICTING` ならステップ 7 の対処に戻る。問題なければ `gh pr view <number> --web` でブラウザを開き、マージ可能であることをユーザーに報告してマージを促す。
