---
name: project-verifier
description: テストやリンターを実行してプロジェクトの状態を検証します。コード変更後や、動作確認を求められた際に使用します。
---

# Project Verifier (プロジェクト検証ランナー)

プロジェクトの検証スイートを実行し、品質と仕様への準拠を確認します。

## Instructions (手順)

1.  **判定**: プロジェクトの種類（Node.js, Python, Go など）を `package.json` や `Makefile` などから特定してください。
2.  **テスト**: 適切なテストコマンドを実行してください（例: `npm test`, `pytest`）。
3.  **リント**: リンターコマンドを実行してください（例: `npm run lint`, `flake8`）。
4.  **報告**:
    - 成功した場合: すべての仕様が満たされていることを報告してください。
    - 失敗した場合: エラー出力を分析し、修正案を提示してください（修正が必要な場合は `tdd-workflow` の使用を提案）。

## Commands Reference

- Node.js: `npm test`, `npm run lint`
- Python: `pytest`, `pylint`
- Rust: `cargo test`
- Go: `go test ./...`
