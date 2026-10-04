---
name: security-scan
description: セキュリティスキャンを実行。RECON→SCAN→REPORT→LEARNワークフローで脆弱性を検出。「セキュリティスキャン」「security scan」「脆弱性チェック」「セキュリティ診断」「OWASPチェック」で起動。Do NOT use for レポートのみ（→ attack-report）やスキャン+レポート一括（→ security-audit）。
allowed-tools: Task, Read, Write, Bash, Grep, Glob
---

## Usage

```bash
/security-scan           # 現在のディレクトリをスキャン
/security-scan ./src     # 指定ディレクトリをスキャン

# フルスキャン（13エージェント並列）
/security-scan ./src --full-scan

# 動的テスト有効化（--target必須）
/security-scan ./src --dynamic --target http://localhost:8000
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| --full-scan | 全13エージェント並列実行 | Off (5 core agents) |
| --dynamic | SQLi動的テストを有効化 | Off |
| --enable-dynamic-xss | XSS動的テストを有効化 | Off |
| --target | 検証対象URL | Required if --dynamic |
| --no-sca | SCAスキャンをスキップ | Off |
| --no-memory | 起動時注入自体は止められない（agent 定義が静的に `memory: project` を持つ）。`--no-memory` は注入済み memory を参照しない指示であり、隔離を保証しない | Off |

## Workflow

```
1. RECON Phase
   └── recon-agent

2. SCAN Phase (parallel)
   ├── Core Agents (default: 5)
   └── Extended Agents (--full-scan: +8)

3. REPORT Phase
   └── JSON output

4. LEARN Phase
   └── スキャン結果を report に出力。memory への蓄積は人間の手動作業（details: reference.md）
```

## Completion
Output: SCAN完了。検出件数サマリ。次: /attack-report or /security-audit

## Agent Integration

| Phase | Agent | Role |
|-------|-------|------|
| RECON | recon-agent | 情報収集・優先度付け |
| SCAN | 5 core / 13 full | 脆弱性検出（並行実行） |

## Reference

詳細は [reference.md](reference.md) を参照。
