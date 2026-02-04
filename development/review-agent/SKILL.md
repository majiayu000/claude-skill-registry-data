---
name: review-agent
description: |
  ReviewAgent スキル - コード品質判定・静的解析・セキュリティスキャン・品質スコアリング。
  生成されたコードに対して100点満点で品質評価し、80点以上で合格判定。

  Use when:
  - コード品質をレビューする時
  - 静的解析（ESLint、TypeScript）が必要な時
  - セキュリティスキャンが必要な時
  - 品質スコアを算出する時
  - "レビュー", "品質チェック", "セキュリティ", "スキャン" がキーワードに含まれる時
allowed-tools: Read, Grep, Glob, Bash
---

# Review Agent Skill

コード品質判定Agent - 静的解析・セキュリティスキャン・品質スコアリング。

## 役割

- 静的コード解析 (ESLint、TypeScript)
- セキュリティ脆弱性スキャン (npm audit、Secret検出)
- 品質スコア算出 (0-100点、合格ライン: 80点)
- レビューコメント自動生成
- Critical脆弱性時のCISOエスカレーション
- 修正提案生成

## 品質スコアリングシステム

```yaml
scoring_algorithm:
  base_score: 100点

  deductions:
    eslint_error: -20点/件
    typescript_error: -30点/件
    critical_vulnerability: -40点/件
    high_vulnerability: -20点/件
    medium_vulnerability: -10点/件

  passing_threshold: 80点
```

## 検査項目

1. **ESLint**: コードスタイル・ベストプラクティス
2. **TypeScript**: 型エラー・型安全性
3. **Secret検出**: APIキー・パスワード・トークン漏洩
4. **脆弱性パターン**: eval(), innerHTML, document.write
5. **npm audit**: 依存関係の既知脆弱性

## セキュリティスキャン

### Secret検出パターン
```regex
- API Key: api[_-]?key[\s]*[:=][\s]*['"]([^'"]+)['"]
- Password: password[\s]*[:=][\s]*['"]([^'"]+)['"]
- Token: token[\s]*[:=][\s]*['"]([^'"]+)['"]
- Anthropic Key: sk-[a-zA-Z0-9]{20,}
- GitHub Token: ghp_[a-zA-Z0-9]{36,}
```

### 脆弱性パターン

| パターン | リスク | Severity | 減点 |
|---------|-------|----------|-----|
| `eval()` | コードインジェクション | Critical | -40点 |
| `innerHTML =` | XSS攻撃 | High | -20点 |
| `document.write()` | XSS攻撃 | High | -20点 |
| `exec()` | コマンドインジェクション | High | -20点 |

## 成功条件

### 必須条件 (合格ライン: 80点以上)
- TypeScriptエラー: 0件
- Critical脆弱性: 0件
- 品質スコア: ≥80点

### 推奨条件
- ESLintエラー: 0件
- テストカバレッジ: ≥80%
- High脆弱性: 0件

## 実行コマンド

```bash
# ReviewAgent単体実行
npm run agents:review -- --files="src/**/*.ts"

# CodeGenAgent後に自動実行
npm run agents:parallel:exec -- --issue 270
```

## レビューコメント出力例

```markdown
## ReviewAgent 品質レポート

### 品質スコア: 85/100 PASSED

### スコア内訳
- **ESLint**: 90点 (2 warnings)
- **TypeScript**: 100点 (0 errors)
- **Security**: 80点 (1 medium issue)
- **Test Coverage**: 85点

### 検出された問題

#### src/services/authService.ts:45
**[ESLINT]** Unused variable 'tempData'
- Severity: medium
- Suggestion: Remove unused variable

#### src/utils/validator.ts:102
**[SECURITY]** Possible XSS risk: innerHTML assignment
- Severity: high
- Suggestion: Use textContent or sanitize HTML
```

## エスカレーション条件

### Sev.1-Critical → CISO
- Critical脆弱性検出 (APIキー漏洩、SQLインジェクション等)
- セキュリティポリシー違反
- データ漏洩リスク

### Sev.2-High → TechLead
- TypeScriptエラー多数 (10件以上)
- アーキテクチャ整合性違反
- 品質スコア50点未満

## メトリクス

- **実行時間**: 通常15-30秒
- **スキャンファイル数**: 平均10-50ファイル
- **検出精度**: False Positive率 <5%
- **合格率**: 85%
