---
name: pr-agent
description: |
  PRAgent スキル - Pull Request自動作成・Conventional Commits準拠・Draft PR自動生成。
  コード実装完了後、GitHub PRを自動作成し、レビュワー割り当て・説明文生成・関連Issue紐付けを実行。

  Use when:
  - Pull Requestを作成する時
  - Conventional Commits形式のタイトルが必要な時
  - レビュワーの自動割り当てが必要な時
  - 関連Issueの紐付けが必要な時
  - "PR作成", "プルリクエスト", "マージ" がキーワードに含まれる時
allowed-tools: Read, Grep, Glob, Bash
---

# PR Agent Skill

Pull Request自動作成Agent - Conventional Commits準拠・Draft PR自動生成。

## 役割

- Pull Request自動作成 (Draft状態)
- PRタイトル生成 (Conventional Commits準拠)
- PR説明文自動生成 (変更内容・テスト結果・チェックリスト)
- レビュワー自動割り当て (CODEOWNERS参照)
- Label自動付与
- 関連Issue紐付け (Closes #xxx)

## Conventional Commits準拠

```yaml
title_format:
  pattern: "{prefix}({scope}): {description}"

  prefix_mapping:
    feature: "feat"
    bug: "fix"
    refactor: "refactor"
    docs: "docs"
    test: "test"
    deployment: "ci"

  example:
    feature: "feat(auth): Add Firebase authentication"
    bug: "fix(api): Resolve invalid-credential error"
    docs: "docs(readme): Update installation guide"
```

## PR説明文構造

```markdown
## 概要
{Issue説明またはタスク概要}

## 変更内容
- {変更ファイル1} (変更行数)
- {変更ファイル2} (変更行数)

## テスト結果
- Unit Tests: Passed
- E2E Tests: Passed
- Coverage: 85%
- Quality Score: 92/100

## チェックリスト
- [x] ESLint通過
- [x] TypeScriptコンパイル成功
- [x] テストカバレッジ80%以上
- [x] セキュリティスキャン通過
- [ ] レビュー完了

## 関連Issue
Closes #{issue_number}

---
Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

## Scope決定ルール

変更ファイルから最も多く変更されたディレクトリを自動検出:

```typescript
// 例: src/services/authService.ts を変更
// → scope = "services"
// → title = "fix(services): Resolve auth error"
```

## レビュワー自動割り当て

### 1. CODEOWNERS参照
```
# .github/CODEOWNERS
agents/          @ai-agent-team
src/services/    @backend-team
src/components/  @frontend-team
```

### 2. デフォルトレビュワー
CODEOWNERS不一致時: TechLead

## Label自動付与

```yaml
labels:
  - "bug"              # Task Type
  - "Sev.2-High"       # Severity
  - "CodeGenAgent"     # Agent
  - "review-required"  # Review Status
```

## 実行コマンド

```bash
# PRAgent単体実行
npm run agents:pr -- --issue 270 --branch "feature/auth-fix"

# CodeGenAgent → ReviewAgent → PRAgent の自動連携
npm run agents:parallel:exec -- --issue 270
```

## 成功条件

### 必須条件
- PR作成成功率: 100%
- Draft状態: 必須 (人間レビュー待ち)
- 関連Issue紐付け: 100%

### 品質条件
- タイトル形式準拠: Conventional Commits 100%
- 説明文完全性: 100%
- レビュワー割り当て: 90%以上

## エラーハンドリング

### Branch not pushed
```bash
git push -u origin feature/my-branch
```

### PR already exists
既存PRを使用 or ブランチ名変更

### Permission denied (403)
GITHUB_TOKEN権限確認 → TechLeadへエスカレーション

## メトリクス

- **実行時間**: 通常10-20秒
- **PR作成成功率**: 98%+
- **Draft状態率**: 100%
- **タイトル形式準拠率**: 100%
