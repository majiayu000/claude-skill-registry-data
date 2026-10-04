---
name: generate-e2e
description: security-scan結果からPlaywright E2Eテストコードを自動生成。脆弱性タイプ別にテストファイルをtests/security/に出力。「E2Eテスト生成」「generate e2e」「セキュリティテスト作成」「Playwrightテスト生成」で起動。security-auditの--auto-e2eオプションでも自動実行される。Do NOT use for スキャン実行（→ security-scan）やレポート生成（→ attack-report）。
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Generate E2E

security-scan結果からPlaywright E2Eテストコードを自動生成するスキル。

## Usage

```bash
/generate-e2e                    # 直前のscan結果からテスト生成
/generate-e2e ./scan-result.json # 指定JSONから生成
/generate-e2e --force            # 既存ファイル上書き
```

## Options

| Option | Description | Required |
|--------|-------------|----------|
| [path] | security-scan JSON file | No (uses last scan) |
| --force | 既存ファイルを上書き | No |

## Input Format

security-scan が出力するJSON形式を入力として受け取る。

```json
{
  "metadata": {
    "scan_id": "<uuid>",
    "scanned_at": "<timestamp>",
    "target_directory": "<path>"
  },
  "summary": {
    "total": 3,
    "critical": 1,
    "high": 1,
    "medium": 1,
    "low": 0
  },
  "vulnerabilities": [
    {
      "id": "XSS-001",
      "vulnerability_class": "xss",
      "severity": "high",
      "file": "app/Controllers/UserController.php",
      "line": 45,
      "endpoint": "/users/{id}"
    }
  ]
}
```

## Output

生成されるファイルは `tests/security/` ディレクトリに出力される。

```
<target-project>/
└── tests/
    └── security/
        ├── playwright.config.ts  # Playwright設定
        └── <vuln-type>.spec.ts   # 脆弱性別テストファイル
```

## Behavior

### Empty Vulnerabilities (0件)

脆弱性が0件の場合、`playwright.config.ts` のみ生成される。テストファイルは生成されない。

### File Overwrite

- **デフォルト**: 既存ファイルがある場合は警告して中断
- **--force**: 既存ファイルを強制的に上書き

## Workflow

```
1. security-scan JSON読み込み
2. 脆弱性タイプ別にグループ化
3. テンプレートから設定ファイル生成
4. 各脆弱性タイプのテストファイル生成
5. tests/security/ に出力
```

## Reference

詳細は [reference.md](reference.md) を参照。
