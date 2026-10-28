---
name: cdk-ci
description: CDKインフラコードの静的解析・スナップショットテスト・cdk synthを実行する。インフラコードのCDK CIチェックを依頼されたときに使用すること。
context: fork
agent: cdk-ci-runner
---

CDK インフラストラクチャコードの静的解析、Snapshotテスト、cdk synth を実行し、結果をレポートしてください。

出力フォーマット:

- 成功時: `.claude/skills/cdk-ci/assets/success-report.md` を読み込んでテンプレートを使用すること
- 失敗時: `.claude/skills/cdk-ci/assets/failure-report.md` を読み込んでテンプレートを使用すること
