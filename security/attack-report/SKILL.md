---
name: attack-report
description: security-scan結果をMarkdownレポートに変換。脆弱性をCVSSスコア降順でソートし、Executive Summary・推奨事項を含むレポートを生成。「レポート生成」「attack report」「脆弱性レポート」「スキャン結果をまとめて」で起動。Do NOT use for スキャン実行（→ security-scan）やスキャン+レポート一括実行（→ security-audit）。
allowed-tools: Read, Write
---

# Attack Report

security-scan結果をMarkdownレポート形式で出力するスキル。

## Usage

```bash
/attack-report              # 直前のsecurity-scan結果をレポート化
/attack-report ./report.md  # 指定ファイルに出力
```

## Input Format

security-scan が出力するJSON形式を入力として受け取る。

```json
{
  "metadata": {
    "scan_id": "<uuid>",
    "scanned_at": "<timestamp>",
    "target_directory": "<path>"
  },
  "recon": {
    "framework": "Laravel",
    "endpoints_count": 15,
    "high_priority_count": 5
  },
  "summary": {
    "total": 3,
    "critical": 0,
    "high": 2,
    "medium": 1,
    "low": 0
  },
  "vulnerabilities": [...]
}
```

## Output Format

Markdown形式のレポートを生成。脆弱性はCVSSスコア降順でソート。

### Report Sections

| Section | Content |
|---------|---------|
| Executive Summary | リスク評価、優先対応Top 3、影響システム |
| Summary | スキャンメタデータ、脆弱性件数サマリ |
| Vulnerabilities | 重大度別の脆弱性一覧 (Critical -> Low) |
| Recommendations | 対応優先度に基づく推奨事項 |

### Vulnerability Entry

各脆弱性は以下を含む:
- ID, Type, CVSS 4.0 Score/Vector
- File and line number
- Agent, CWE/OWASP references
- Description, Remediation

## Reference

詳細・レポートテンプレート: [reference.md](reference.md)
