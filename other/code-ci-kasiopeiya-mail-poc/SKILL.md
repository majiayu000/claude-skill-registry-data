---
name: code-ci
description: 各npmワークスペースの静的解析・単体テストを実行する（CIパイプラインシミュレーション）。CIチェックやコミット・PR前のコード品質検証を依頼されたときに使用すること。
context: fork
agent: code-ci-runner-agent
---

各 npm ワークスペースの静的解析と単体テストを実行してください。

出力フォーマットは `references/report-template.md` のテンプレートに従ってください。
