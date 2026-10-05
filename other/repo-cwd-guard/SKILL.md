---
name: repo-cwd-guard
description: MoneyForward クラウド会計のデータ (仕訳・証憑・バックアップ) を扱う前に、セッションが c:\moneyforward で起動しているかを確認するためのスキル。「別ディレクトリから moneyforward を触ろうとしている」「MCP ツールが見当たらない」「hook が鳴っていない」「監査ログに残っていない」「同期されていない」といった状況、および repo-cwd-guard の警告が出たときに参照する。書き込み (仕訳の登録・更新、取引先の作成) を行う前には必ず確認すること。
---

# 起動ディレクトリの確認

## 結論

**MoneyForward クラウド会計のデータに書き込む作業は、必ず `c:\moneyforward` を cwd にして起動したセッションで行う。**

## なぜ

Claude Code の `.mcp.json` と `.claude/settings.json` は、**セッションの primary working
directory からしか読まれない**。別のディレクトリで起動すると、次がすべて黙って無効になる。

| 失われるもの | 影響 |
|---|---|
| `.mcp.json` の mfc_ca サーバー | MCP ツールが存在しなくなる。HTTP 直叩き等の迂回に流れやすい |
| `PostToolUse` の監査ログ | 操作が `audit-logs/operations/` に残らない |
| `PostToolUse` の同期 | バックアップがクラウドに上がらない |

エラーは出ない。**動くが記録されない**という壊れ方をする。

## 実際に起きた事故 (2026-09-01)

リポジトリ外のディレクトリで起動したセッションから仕訳を登録した。結果:

- `.mcp.json` 未ロードで MCP ツールが無く、MCP サーバーの HTTP エンドポイントを直接叩いた
- ツール名が `mcp__*` にならず PostToolUse hook が一度も鳴らなかった
- **書き込みが監査ログに残らなかった**
- 登録直前に取ったバックアップがクラウドに同期されなかった

3 つの障害に見えるが、原因は起動ディレクトリ 1 つ。

## 警告が出たときの対処

ユーザーレベルの PreToolUse フック (`~/.claude/hooks/repo-cwd-guard.sh`) が、cwd 外からの
操作を検知して警告する。**deny ではなく warn** なので処理は止まらない。

- **読み取り調査だけ** (残高確認、差分調査、ファイル閲覧) → そのまま続行してよい
- **書き込みを含む** (仕訳の登録・更新、取引先の作成、バックアップの取得) → 中断し、
  `c:\moneyforward` で起動し直すようユーザーに依頼する

## どうしても cwd 外から書き込む場合

やむを得ず迂回するなら、**hook が代行していた処理を手で行う**。省略すると記録が欠ける。

1. 書き込み前に全仕訳をバックアップする
2. 実行した操作を `audit-logs/operations/YYYY-MM-DD.json` に自分で追記する
3. 終了後に `rclone` でクラウドへ同期する

## 補足 (moneyforward)

- 監査ログを書く `log_mf_op.py` は POST/PUT のとき `tool_input["journal"]` しか読まない。
  `postTransactionJournalize` / `postTransactions` / `postTradePartners` は `journal` を
  持たないフラット構造なので、**hook が正常に鳴っても中身が記録されない**。明細から仕訳を
  起こす操作は全部この経路なので、実質一番記録したい操作が残らない。
- skills は `.claude/skills/` に置く。repo ルート直下の `skills/` は自動認識されない。
