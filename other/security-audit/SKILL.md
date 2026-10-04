---
name: security-audit
description: セキュリティスキャン+レポート生成を一括実行するオーケストレータ。Task()でsecurity-scan→attack-reportを委譲。「セキュリティ監査」「security audit」「脆弱性診断して」で起動。
allowed-tools: Task, Read, Write, Bash, Grep, Glob
---

# Security Audit

security-scan と attack-report を Task() で順次委譲し、一括実行するオーケストレータ。

## Usage

```bash
/security-audit              # 現在のディレクトリを監査
/security-audit ./src        # 指定ディレクトリを監査
/security-audit ./src --auto-e2e  # 監査後にE2Eテスト自動生成
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| --full-scan | 全13エージェント並列実行 | Off |
| --auto-e2e | レポート後にE2E生成 | Off |
| --dynamic | SQLi動的テストを有効化 | Off |
| --target | 検証対象URL | Required if --dynamic |

## Workflow

```
1. Task(security-scan) → JSON結果を取得
2. Task(attack-report) → JSON → Markdownレポート生成
3. [optional] Task(generate-e2e) → E2Eテスト生成（--auto-e2e時）
```

### Step 1: security-scan

```
Task(subagent_type: "general-purpose", model: "sonnet",
  prompt: "Skill(dev-crew:security-scan) を実行。対象: [target] [options]")
→ JSON結果を取得
```

### Step 2: attack-report

```
Task(subagent_type: "general-purpose", model: "sonnet",
  prompt: "Skill(dev-crew:attack-report) を実行。入力: [scan結果JSON]")
→ Markdownレポート生成
```

### Step 3: E2E生成 (optional)

`--auto-e2e` 指定時のみ:

```
Task(subagent_type: "general-purpose", model: "sonnet",
  prompt: "Skill(dev-crew:generate-e2e) を実行。入力: [scan結果JSON]")
```

### Step 4: 完了

```
================================================================================
SECURITY AUDIT完了
================================================================================
スキャン+レポート生成が完了しました。
レポート: [output path]
================================================================================
```
