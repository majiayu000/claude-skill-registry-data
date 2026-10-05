---
name: pr-workflow
description: Issueファイルに基づく実装からローカルコミットまでの標準フロー。push・PR作成はしない（issue-finish が行う）
disable-model-invocation: true
---
以下の手順でissueを実行する。$ARGUMENTSにissueファイルのパスを渡す。
**前提: AIはコードを書いてローカルにコミットするまでが担当。push・PR作成・マージ・実行確認はuserと issue-finish が行う。リモート（origin / GitHub）には一切触れない。**

1. issueファイルを読む
2. `git status` で、ブランチが `claude/{id}-{branch-slug}` かつワーキングツリーがクリーンなことを確認する（ブランチとworktreeは issue() が作成済み）。違えば報告して止まる
3. 対象ファイルを読んで実装
4. issueの「確認」項目と、リポ CLAUDE.md の「静的チェック / 検証手段」に従い提出前確認を行う。コードを読んでcaller・importの整合性も確認する。実行系・デプロイ系コマンド（rebuild / deploy / 本番起動）は実行しない
5. issueの保証節がリポの保証台帳 `docs/guarantees.md` の記載に影響する場合（新保証・変更・廃止）、テストと同じPR内で台帳（保証の文言と対応テストの表）を更新する。台帳の更新漏れは実装未完了として扱う
6. `git add {変更したファイル}` し、`git diff --name-only --cached` がissueの「対象」フィールドと完全一致することを確認する（保証台帳を更新した場合はそれも対象に含まれていること）。不一致なら実装に戻る
7. コミットする（保証台帳を更新した場合は同じコミットに含める）。メッセージ本文に報告を入れる（issue-finish がこの本文をそのままPR本文として使う）。一時ファイルは作らず、heredoc で標準入力から渡して1コマンドに収めること:
   ```
   git commit -F - <<'EOF'
   {type}: {タイトル}

   ## 変更内容
   {issueの内容フィールドを展開}

   ## 保証
   {issueの保証節の各項目 → それを固定したテスト（ファイル・テスト名）の対応。テストを伴わない場合は Issue と同じく `なし（理由）` }

   ## 静的確認結果
   {確認項目に対する結果。git diff --name-only --cached の出力を含める}

   ## 検証手順
   {Agent側で完結しない確認（実行・デプロイ・目視）を、リポ CLAUDE.md の検証手順の雛形に従って記載。なければ省略}
   EOF
   ```
8. `crit` でレビューを受ける。`crit --base-branch main` を `run_in_background: true` で起動し、出力された URL（`http://localhost:<port>`）を「ブラウザでレビューし、終わったら Finish Review を押してください」と添えてそのまま伝える。ユーザーが Finish Review を押すまでブロックし、**先にレビューファイルを読んだり、ユーザーに何かを入力させたりしない**。完了したら stdout の指示に従って指摘に対応し、必要なら追加コミットする。指摘が無ければそのまま次へ進む（この往復は1周だけ。対応後に再度 crit は開かない）
9. push・PR作成はせずに終了。以下を出力する:
   ✅ Committed on {branch}: {type}: {タイトル}
   Review: git diff main...{branch}
   Next: issue-finish → push・PR作成・マージ
