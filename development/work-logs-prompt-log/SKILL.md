---
name: work-logs-prompt-log
description: プロンプトログを出力する
allowed-tools: Read, Write, Grep, Glob
---

# プロンプトログの書き出し

ユーザーの求めに応じて対話セッション中のログを書き出してください。長い入力であっても省略しないでください。
書き出し先は `~/.claude/prompt-log/${repo_name}/${date time prefix}_$description.md` とします。

date time prefix は以下のようにしてください。

- date コマンドを利用してログ出力処理時の現在時刻を取得する
  - フォーマットは `+%Y-%m-%d_%H-%M` とする
- タイムゾーンはAsia/Tokyoとする

## ログの目的

目的としては、開発の再現性担保のためにpull requestに「このような対話によって生成されました」というログを書き込んでおくためのものです。

内容としては
- ユーザーの入力
- あなたの出力結果の概要
- ユーザーに対する確認を求める内容の場合は確認内容

などを含めてください。
