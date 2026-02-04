---
name: review-parallel
description: 複数のAIレビュアーを並列実行し、結果を統合処理して単一のレポートを生成
allowed-tools: Task, Bash, Read, Grep, Glob
---

# 並列AIレビュー実行スキル

このスキルは4つの専門AIレビュアーを並列実行し、結果を統合処理して包括的なコードレビューレポートを生成します。

## Phase 0: 前提条件確認

実装を開始する前に、必要なツールと環境を確認します。

### 0.1 CLIツールの確認

```bash
# 各CLIツールが利用可能か確認
command -v codex || echo "⚠️ codex CLI not found"
command -v coderabbit || echo "⚠️ coderabbit CLI not found"
command -v copilot || echo "⚠️ copilot CLI not found"
command -v gemini || echo "⚠️ gemini CLI not found"
```

### 0.2 認証状態確認

```bash
# 各ツールの認証状態確認
codex whoami 2>/dev/null || echo "⚠️ codex not authenticated"
coderabbit auth status 2>/dev/null || echo "⚠️ coderabbit not authenticated"
# copilot and gemini auth check
```

### 0.3 Python環境確認

統合スクリプト用のPython 3.8以上が必要：
```bash
python3 --version
```

## Phase 1: レビュー対象の特定（最適化版）

ユーザーリクエストからレビュー対象を判定し、必要なgit diffを取得します。

### 1.1 ターゲット判定

ユーザーのリクエストから以下のいずれかに該当するかを判定：
- **uncommitted**: "uncommitted"、"working directory"、"unstaged" などのキーワード
- **main branch**: "main branch"、"vs main"、"compare to main" など
- **staged**: "staged"、"cached" などのキーワード
- **specific files**: ファイルパスが指定されている

### 1.2 パフォーマンス最適化：git呼び出しを1回にまとめる

大規模リポジトリでの効率化のため、複数のgit diffコマンドではなく1回の呼び出しで全情報を取得：

```bash
# 1回のgit呼び出しで全情報を取得
git_context=$(git status --porcelain && \
              git log --oneline -10 && \
              git diff HEAD --stat)

# 条件分岐で必要な差分のみ取得
case $target in
  uncommitted)
    git_diff=$(git diff HEAD)
    ;;
  staged)
    git_diff=$(git diff --cached)
    ;;
  main)
    git_diff=$(git diff main...HEAD)
    ;;
  *)
    git_diff=$(git diff HEAD)
    ;;
esac
```

### 1.3 Context情報の抽出

```bash
# コミット履歴
git_log=$(git log --oneline -10)

# ファイル統計
git_stat=$(git diff HEAD --stat)

# リポジトリ情報
branch=$(git rev-parse --abbrev-ref HEAD)
```

## Phase 2: 4レビュアーの並列起動

4つのレビュアーを並列（同時）に起動します。

### 2.1 並列実行の要件

- **4つのレビュアー**: Codex、CodeRabbit、Copilot、Gemini
- **同時実行**: 各レビュアーは並列で起動
- **同じ入力**: 全レビュアーに同じgit diff出力を渡す
- **非同期実行**: backgroundモードで実行
- **タイムアウト**: 各レビュアーの最大実行時間3分

### 2.2 レビュアー一覧と専門分野

| レビュアー | 専門分野 | Agent | Focus |
|-----------|---------|-------|-------|
| **Codex** | コード品質、ベストプラクティス、深い推論 | @agent-codex-reviewer | Code Quality Analysis |
| **CodeRabbit** | セキュリティ脆弱性、パフォーマンス、OWASP | @agent-coderabbit-reviewer | Security & Performance |
| **Copilot** | GitHub統合、CI/CD最適化、実践的改善 | @agent-copilot-reviewer | GitHub Workflow Integration |
| **Gemini** | アーキテクチャ分析、システム設計、SOLID原則 | @agent-gemini-reviewer | Architecture Analysis |

### 2.3 並列実行方法

**実装方法の選択**: 以下のいずれかの方法をAgentが選択します。

**オプション1: 複数Task呼び出しの並列実行**
- 各レビュアーに対して個別のTask呼び出しを実行
- TaskOutputで全体の完了を待機

**オプション2: Bashバックグラウンドジョブ**
- Bash内で複数のレビュアー呼び出しをバックグラウンドで実行
- waitコマンドで全ジョブの完了を待機

**オプション3: その他Agentが判断した方法**
- Agentの判断で最適な並列化方法を選択

## Phase 3: 結果収集とエラーハンドリング

各レビュアーの結果を収集し、成功/失敗を判定します。

### 3.1 結果取得

各レビュアーの出力を収集：

```python
# 疑似コード
results = {
    'codex': get_reviewer_output('codex-reviewer'),
    'coderabbit': get_reviewer_output('coderabbit-reviewer'),
    'copilot': get_reviewer_output('copilot-reviewer'),
    'gemini': get_reviewer_output('gemini-reviewer')
}
```

### 3.2 最低成功基準の確認

最低1つのレビュアーが成功していれば処理継続。全て失敗した場合はエラーを返す：

```python
successful_reviewers = [name for name, output in results.items()
                       if output and 'error' not in output.lower()]
failed_reviewers = [name for name in results.keys()
                   if name not in successful_reviewers]

if len(successful_reviewers) == 0:
    raise Error("全てのレビュアーが失敗しました。実行環境と認証設定を確認してください。")
```

### 3.3 セキュリティレビュアー失敗時の特別処理

CodeRabbit（セキュリティ専門）が失敗した場合、セキュリティカテゴリの問題は優先度を自動昇格：

```python
if 'coderabbit' in failed_reviewers:
    # OWASP関連のセキュリティ問題の優先度を昇格
    for finding in findings:
        if finding['category'] == 'security':
            finding['priority'] = escalate_priority(finding['priority'])
```

### 3.4 失敗レビュアーの警告生成

失敗したレビュアーがある場合、レポート冒頭に警告を追加：

```markdown
⚠️ 以下のレビュアーが失敗しました：
- CodeRabbit: セキュリティ観点が不足している可能性があります
  → 手動でのセキュリティレビューを推奨します
```

## Phase 4: 統合処理

各レビュアーの出力を統合処理して、重複排除・優先度付けを実行します。

### 4.1 外部統合スクリプトの呼び出し

統合処理は外部Pythonスクリプトで実行されます。詳細はALGORITHMS.mdを参照。

```bash
python ~/.claude/skills/review-parallel/parallel-review-merge.py \
  --codex <(echo "$codex_output") \
  --coderabbit <(echo "$coderabbit_output") \
  --copilot <(echo "$copilot_output") \
  --gemini <(echo "$gemini_output") \
  --output integrated-findings.md
```

### 4.2 統合処理のステップ

1. **パース処理**: 各レビュアーの出力からFindingを抽出
   - ファイルパス: `**[path/to/file.ts:123]**` パターンマッチ
   - カテゴリ: セキュリティ、パフォーマンス、コード品質等

2. **重複排除**: 同一問題を統合
   - キー: `{file}:{line}:{category}`
   - Fuzzy Matching: ±2行以内で同一問題と判定

3. **優先度付け**: レビュアー数ベースで優先度を計算
   - 4つ全て: Critical
   - 3つ: High
   - 2つ: Medium
   - 1つ: Low
   - セキュリティ脆弱性: 自動的にCriticalに昇格

4. **カテゴリ分類**: キーワードベースで分類
   - セキュリティ: injection、xss、csrf、auth等
   - パフォーマンス: n+1、slow、inefficient等
   - コード品質: readability、dry、naming等
   - アーキテクチャ: pattern、coupling、solid等

## Phase 5: 統合レポート生成

統合処理の結果から最終レポートを生成します。

### 5.1 レポート構造

```markdown
# 並列AIレビュー統合レポート

## 📊 サマリー
- レビュー対象: [git情報]
- 起動したレビュアー: [成功したもの] ([数]/4)
- 検出問題総数: [X]件

## 🔴 Critical（即座に対応すべき）
[複数レビュアーが指摘した最重要問題]

## 🟡 High（優先的に対応）
[重要な問題]

## 🟢 Medium（重要）
[中程度の問題]

## ℹ️ Low/Informational
[提案レベルの指摘]

## 📂 カテゴリ別分析
### 🔒 セキュリティ
### ⚡ パフォーマンス
### 📝 コード品質
### 🏗️ アーキテクチャ
### 🧪 テスト
### 🔧 GitHub統合

## 🤖 レビュアー別の独自指摘
[各レビュアーが単独で指摘した重要ポイント]

## 💡 次のステップ
1. 🔴 Criticalの問題を即座に修正
2. 🟡 Highの問題を優先的に対応
3. 🟢 Mediumの問題をスプリントに組み込み
4. ℹ️ Lowの問題は検討
```

### 5.2 Finding表示フォーマット

```markdown
#### [{file_path}:{line_number}] {short_description}

**カテゴリ**: {category}
**指摘したレビュアー**: {reviewers} ({count}/4)

**問題**:
{unified_description}

**各レビュアーの視点**:
- **Codex**: {comment}
- **CodeRabbit**: {comment}
- **Copilot**: {comment}
- **Gemini**: {comment}

**推奨アクション**:
{recommended_fix}
```

### 5.3 大量指摘時の処理

指摘が100件以上の場合：
- Criticalのみ詳細表示
- 完全版は別ファイル `detailed-review.md` に出力

## エラーハンドリング

### スキル実行時のエラー処理

| シナリオ | 対処方法 |
|---------|---------|
| レビュアー失敗 | 成功したレビュアー結果で処理、冒頭に警告追加 |
| 空の結果 | "問題なし"として扱う |
| Conflicting指摘 | 両論併記し、ユーザーに検証推奨 |
| 大量指摘（100+件） | Criticalのみ詳細、完全版はファイル出力 |
| Taskタイムアウト | タイムアウトしたレビュアーをスキップ |

## 実装上の注意

1. **並列実行の選択**: Agentが最適な並列化方法を判断
2. **大規模リポジトリ対応**: git呼び出しを最小化
3. **セキュリティ優先**: OWASP Top 10を完全カバー
4. **ユーザーフォーカス**: Criticalな問題に即座に対応できる設計
