---
name: rate-limit-reset-mail
description: Claude / Codex / API のレートリミット・使用量上限の解除時刻に、Windows タスクスケジューラで通知メールを予約する。Use when a usage limit or rate limit is hit or about to be hit ("You've hit your limit", "usage limit reached", "try again at ...", "resets 11pm", 429), or when the user asks to be mailed when a limit resets, and to list or cancel such scheduled mails.
---

# rate-limit-reset-mail

レートリミットで作業が止まったとき、解除時刻にメールが届くよう予約する。ユーザーは解除を待たずに離れられ、メールを見たら作業を再開できる。

自動監視タスク（`\AgentMail\AgentMail-RateLimitWatcher`）が動いていれば、使用率がしきい値以上になった枠の更新時刻にはメールが自動で予約される。まず `-List` で既存の予約を確認し、足りない場合だけ下の手順で手動予約する。

## 手順

1. **解除時刻を特定する。** 次の順で探す。
   - エラーメッセージ・ユーザーの発言（例: `resets 11pm (Asia/Tokyo)`, `try again at 11:05 PM`, `in 2 hours`, `Retry-After: 3600`）
   - Codex なら `/status`、Claude Code なら `/usage` の表示をユーザーに確認してもらう
   - 分からなければユーザーに聞く。推測で予約しない。

2. **ローカル時刻に直す。** タイムゾーン付きならローカル時刻に変換する。時刻だけで現在より前なら翌日とみなす。相対時間なら `-InMinutes` を使う。

3. **予約する:**

   ```powershell
   # 絶対時刻
   pwsh -NoProfile -File "$HOME\.agent-mail\bin\schedule-agent-mail.ps1" -At "2026-10-23 23:00" -Subject "<ツール名> のレートリミット解除: <プロジェクト名>" -Body "<本文>"
   # 相対時間（分）
   pwsh -NoProfile -File "$HOME\.agent-mail\bin\schedule-agent-mail.ps1" -InMinutes 150 -Subject "..." -Body "..."
   ```

   既定で解除時刻の 2 分後に送る（`-BufferMinutes` で変更可）。本文には次を入れる:
   - どのツール（Claude Code / Codex / どの API）のリミットか
   - プロジェクト（作業ディレクトリ）とブランチ
   - 再開時にやること（中断した作業と次の一手を 1〜3 行。引き継ぎメモがあればそのパス）

4. **結果を伝える。** 出力されたタスク名と送信予定時刻をユーザーに伝える。

## 管理

```powershell
pwsh -NoProfile -File "$HOME\.agent-mail\bin\schedule-agent-mail.ps1" -List
pwsh -NoProfile -File "$HOME\.agent-mail\bin\schedule-agent-mail.ps1" -Cancel <TaskName>
```

同じリミットに対して予約が既にあれば重複させない（`-List` で確認）。解除時刻が変わったら古い予約を `-Cancel` してから入れ直す。

## 守ること

- 秘密情報・個人情報・ユーザーの文書や生成物の中身を本文に書かない。予約内容は送信まで `~/.agent-mail/queue/` に平文で残る。
- メールは通知だけ。解除時刻に作業を自動再開したり、別アカウント・別キーでリミットを回避したりしない。
- 予約はタスクスケジューラの `\AgentMail\` に作られ、送信後に自動で消える。PC がスリープ中なら復帰後に送られる。PC の電源が切れていると届かないことをユーザーに伝える。
- Codex のサンドボックスでタスク登録が拒否された場合は、このコマンドだけ権限昇格を求める。
