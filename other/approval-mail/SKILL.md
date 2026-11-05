---
name: approval-mail
description: 人間の承認・判断が必要な作業の直前に、ユーザーへ通知メールを送る。Use BEFORE pausing for human approval in any project - AI-DLC/official stage gates, plan or Code Generation Plan approval, verification-command approval, escalated/sandbox-bypass commands, destructive or outward-facing actions (push, PR, deploy, delete, publish), or any question the user must answer before work can continue.
---

# approval-mail

承認待ちで作業が止まる前に、ユーザーへメールで知らせる。ユーザーが PC の前にいなくても、戻るべきタイミングが分かるようにするのが目的。

## いつ送るか

次のどれかで「ユーザーの返答なしには先へ進めない」状態になる直前に 1 通送る。

- AI-DLC などの公式承認ゲート（Inception plan、stage gate、Code Generation Plan Approval、検証コマンド承認）
- 権限昇格・サンドボックス外実行が必要なコマンド
- 破壊的・外部公開を伴う操作（push、PR 作成、merge、deploy、削除、公開、外部サービスへの送信）
- 要件・設計・スコープの判断をユーザーに求める質問

送らない場面: ファイル読み取りなど承認不要の作業、同じ承認待ちに対する 2 通目、ユーザーが直前（数分以内）まで会話で応答していて明らかに画面の前にいる場合。

## 手順

1. 承認を求める内容を 1〜3 行にまとめる。
2. 送信する（Claude Code は Bash/PowerShell ツール、Codex はシェル実行）:

   ```powershell
   pwsh -NoProfile -File "$HOME\.agent-mail\bin\send-agent-mail.ps1" -Subject "承認待ち: <プロジェクト名> - <要点>" -Body "<本文>"
   ```

   Windows の Codex では、AI-DLC の承認ゲートを含め、この送信コマンドだけを `exec_command` の `sandbox_permissions: "require_escalated"` で実行する。サンドボックス内では Windows TLS が `Authentication failed` / `セキュリティ パッケージで利用できる資格情報がありません` で失敗することがあるため、最初からこの指定を使う。`justification` は通知メール送信の目的を書く。SMTP パスワードを変更したり、他の作業の権限を広げたりしない。権限昇格を申請するためのメールを再帰的に送らない。昇格が拒否された場合は送信失敗として下記の手順に従い、承認依頼を続ける。

   本文には次を入れる:
   - プロジェクト（作業ディレクトリ名）とブランチ
   - 使用中のエージェント（Claude Code / Codex）
   - 承認してほしい内容（ゲート名、実行したいコマンド、判断事項）とその理由
   - 承認しない場合の影響（どこで止まっているか）

3. 送信後、通常どおりチャットで承認を求める。メールの返信を承認として扱わない。承認は必ずセッション内の正式な手段（ゲート、権限プロンプト、ユーザーの発言）で受け取る。

## 守ること

- 秘密情報（API キー、パスワード、トークン、.env の値）、個人情報、ユーザーの文書・画像・OCR テキスト・生成物の中身をメールに書かない。要点だけ書く。
- メール送信を承認ゲートの代わりにしない。承認の回避・自動承認・承認記録の捏造はしない。
- メール設定の `.env`（`~/.agent-mail/config.json` の `envFile`）は開かない・表示しない。送信はスクリプトに任せる。
- 送信に失敗しても作業や承認依頼を止めない。チャットで「メール送信に失敗した（理由）」と一言伝えて続ける。未設定エラーなら `configure-agent-mail.ps1` をユーザー自身が実行するよう案内する（エージェントは実行しない。パスワード入力があるため）。
- Codex のサンドボックスでネットワークが遮断されている場合は、このコマンドだけ権限昇格を求める。
