---
name: plan-review-loop
description: "実装計画に対するレビュー→修正の自動ループ。問題0件まで繰り返す。「/plan-review-loop」「計画レビューして」で使用。"
---

**ultrathink**

# 🔁 計画レビューループスキル

> [!IMPORTANT]
> 実装計画（`~/.cache/vibecorp/plans/<repo-id>/` 配下）に対してレビュー → 修正のループを実行する。
> **最大 5 回で打ち切る**（無限ループ防止）。上限到達時は未解決指摘を報告して CEO に判断を委ねる。
> 計画ファイルのみを変更対象とする（コードは変更しない）。`git add` / `git commit` / `git push` は呼び出し元に委ねる。

## 🛠️ 使用方法

```bash
/vibecorp:plan-review-loop                    # 現在のブランチの計画を自動検出
/vibecorp:plan-review-loop <plan_file>        # 計画ファイルを直接指定
/vibecorp:plan-review-loop --worktree <path>  # worktree 内の計画を対象
```

## 🌲 worktree モード

`--worktree <path>` が指定された場合、全操作を指定パス内で実行する。

- **Bash**: 全コマンドを `cd <path> && command` で実行する。
- **Read / Write / Edit**: `<path>/` を基準とした絶対パスを使用する。
- **サブスキル呼び出し**: `--worktree <path>` を引き継ぐ。
- 未指定時は従来通り CWD で実行する（後方互換）。

## 📂 計画ファイルの検出

引数未指定の場合、ブランチ名から計画ファイルを特定する。

```bash
source "$CLAUDE_PROJECT_DIR"/.claude/lib/common.sh
branch=$(git branch --show-current)
plan_file="$(vibecorp_plans_dir)/${branch}.md"
```

ファイルが存在しなければユーザーに報告して停止する。

### 後方互換: 旧パスのフォールバック

既存の `.claude/plans/<branch>.md` に計画が残っているリポジトリでは、新パスが無く旧パスにファイルがある場合のみ旧パスを使う（#334 移行期間の救済）。

```bash
if [ ! -f "$plan_file" ] && [ -f ".claude/plans/${branch}.md" ]; then
  plan_file=".claude/plans/${branch}.md"
fi
```

## 🧑‍🔬 専門家エージェントモード

### 設定の読み取り

`vibecorp.yml` の `plan.review_agents` を読み取り、有効な専門家エージェントを特定する。

```bash
# vibecorp.yml から plan.review_agents を読み取る
awk '
  /^plan:/ { in_plan = 1; next }
  in_plan && /^[^ #]/ { exit }
  in_plan && /review_agents:/ { in_agents = 1; next }
  in_agents && /^    - / { gsub(/^    - /, ""); print }
  in_agents && !/^    / { exit }
' .claude/vibecorp.yml
```

### エージェント名とファイルの対応

| 設定名 | エージェントファイル | プリセット |
|--------|-------------------|-----------|
| `architect` | `.claude/agents/plan-architect.md` | 全プリセット |
| `security` | `.claude/agents/plan-security.md` | standard 以上 |
| `testing` | `.claude/agents/plan-testing.md` | standard 以上 |
| `performance` | `.claude/agents/plan-performance.md` | standard 以上（デフォルトは full で有効） |
| `dx` | `.claude/agents/plan-dx.md` | standard 以上（デフォルトは full で有効） |
| `cost` | `.claude/agents/plan-cost.md` | **full 限定** |
| `legal` | `.claude/agents/plan-legal.md` | **full 限定** |

### プリセット別デフォルト

`install.sh` が生成する `vibecorp.yml` の `plan.review_agents` デフォルト:

| プリセット | デフォルト値 |
|-----------|------------|
| minimal | `[architect]` |
| standard | `[architect, security, testing]` |
| full | `[architect, security, testing, performance, dx, cost, legal]` |

ユーザーは `vibecorp.yml` で個別に追加・削除可能。

### フォールバック

以下の場合は従来の単一レビュー（後述の「レビュー観点」による直接レビュー）にフォールバックする。

- `vibecorp.yml` が存在しない
- `plan.review_agents` が未設定または空
- 設定されたエージェントファイルが `.claude/agents/` に存在しない

## 🔁 ループフロー

以下を問題が0件になるまで繰り返す。**最大5回でループを打ち切る。上限到達時は未解決の指摘一覧を報告してユーザーに判断を委ねる。**

### 1. レビュー実行

#### 専門家エージェントモード（`plan.review_agents` が設定されている場合）

1. 計画ファイルの内容を読み込む
2. Issue の完了条件を取得する
3. 各エージェントを SubAgent（Agent tool）として **並列起動** する
4. 各 SubAgent に以下を渡す
   - 計画ファイルの内容
   - Issue の完了条件
   - プロジェクトの既存コード構造の概要

SubAgent 起動例:

```text
Agent tool で以下を実行:
「.claude/agents/plan-architect.md の指示に従い、以下の計画をレビューしてください。
計画ファイル: {plan_content}
Issue 完了条件: {completion_criteria}」
```

5. 全エージェントのレビュー結果を収集する
6. フィードバックを統合する（後述の「フィードバック統合」参照）

#### 単一レビューモード（フォールバック）

計画ファイルを読み込み、以下のレビュー観点で評価する。

#### レビュー観点

| 観点 | チェック内容 |
|------|------------|
| **網羅性** | Issue の完了条件が全て計画に反映されているか |
| **実現可能性** | 参照しているファイル・関数が実在するか、変更内容が技術的に正しいか |
| **独立性** | タスクが並行実行可能な粒度に分解されているか |
| **テスト** | 各タスクにテスト項目が含まれているか |
| **影響範囲** | 変更による副作用が考慮されているか |
| **既存パターンとの整合** | プロジェクトの既存コード・規約と矛盾しないか |

#### 検証手順

1. Issue 本文を取得し、完了条件を抽出する
2. 計画の各タスクが完了条件をカバーしているか照合する
3. 計画に記載されたファイルパス・関数名が実在するか確認する
4. 既存の実装パターンとの整合性を確認する

### フィードバック統合（専門家エージェントモード時）

各エージェントのレビュー結果を以下のルールで統合する（2 段階）。

#### 第 1 段階: 平社員層統合

`plan.review_agents` に設定された専門家エージェント（plan-architect 等）の結果を統合する。

1. **重複排除**: 複数エージェントが同じ問題を指摘した場合、1件にまとめる。
2. **優先順位付け**: セキュリティ指摘 > その他の指摘。
3. **矛盾解決**: エージェント間の意見が矛盾した場合は Issue の完了条件を優先基準とする（調停の基準）。
4. **好みレベル除外**: 好みレベルの改善提案は問題として扱わない。

#### 第 2 段階: C\*O メタレビュー（full プリセット限定）

後述の「C\*O メタレビュー層」セクションで条件起動された C\*O エージェントが、平社員層統合結果をメタレビューする。

- C\*O が「指摘妥当」と判定 → 平社員指摘を採用する。
- C\*O が「指摘不要」と判定 → 該当指摘を除外する（理由を記録）。
- C\*O が新規懸念を提起 → 追加問題として扱う。
- C\*O 間の矛盾 → Issue 完了条件を優先基準とする（調停の基準）。

## 🎩 C\*O メタレビュー層（full プリセット限定）

full プリセットでは、計画ファイルが管轄領域に触れる場合に該当 C\*O を条件起動し、平社員層の指摘をメタレビューする。

### 起動条件

- `vibecorp.yml` の `preset: full` であること。
- 計画ファイル内で下表のキーワードパターンがヒットすること（複数ヒット時は該当全 C\*O を並列起動）。

### 起動トリガー & キーワード検出表

| 領域 | キーワードパターン（計画ファイル内で検出） | 起動 C\*O | 平社員合議 |
|---|---|---|---|
| 課金影響 | `API call`, `model:`, `claude -p`, `ANTHROPIC_API_KEY`, `rate limit`, `従量`, `トークン消費` | CFO | accounting-analyst×3 |
| セキュリティ | `auth`, `token`, `secret`, `encrypt`, `permission`, `credential`, `暗号` | CISO | security-analyst×3 |
| 法務 | `dependency`, `LICENSE`, `third-party`, `規約`, `プライバシー`, `第三者` | CLO | legal-analyst×3 |
| 組織運営 | `agents/`, `hooks/`, `rules/`, `skills/` | SM | （単独） |
| 仕様 | `MVV.md`, `specification.md`, `UX` | CPO | （単独） |
| 技術選定 | `architecture`, `技術選定`, 新規依存バージョン | CTO | （単独） |

### 検出方法

計画ファイルをキーワードパターンで検査する。

```bash
grep -iE 'API call|model:|claude -p|ANTHROPIC_API_KEY|rate limit|従量|トークン消費' "$plan_file"
```

該当領域の C\*O と平社員合議（accounting / security / legal analyst ×3）を並列起動する。

### フォールバック

- `preset: full` 以外（minimal / standard）では C\*O メタレビュー層を起動しない。
- キーワードが一つもヒットしない場合も C\*O メタレビュー層を起動しない（平社員層のみで完了）。
- preset 取得コマンド: `awk '/^preset:/ { sub(/^preset:[[:space:]]*/, ""); print; exit }' .claude/vibecorp.yml`

#### 出力形式

```text
## 計画レビュー結果

### 問題あり

1. [エージェント: architect / 観点: 構造設計] 問題の説明
2. [エージェント: security / 観点: 入力検証] 問題の説明
3. ...

### 問題なし

- architect: 責務分離は適切
- testing: テストカバレッジは十分
```

**問題0件ならループ終了。**

### 2. 修正計画

問題リストに対して修正方針を策定する。**このステップでは計画ファイルの変更は行わない**。

手順:

1. 指摘された観点の具体的な問題箇所を特定する
2. 必要に応じて追加のコードベース調査を行う
3. 修正方針を策定する

#### 出力形式

```text
## 修正方針

### 1. [観点: 網羅性] 完了条件「○○」の対応タスク追加

- **修正内容**: Phase 2 にタスクを追加
- **根拠**: Issue の完了条件に明記されている

### 2. [観点: 実現可能性] 関数参照の修正

- **修正内容**: foo() → bar() に変更（bar() が同等機能を提供）
- **根拠**: grep で確認した実在する関数
```

### 3. 修正実行

修正方針に従って計画ファイルを更新する。

- **方針に記載された範囲のみを変更する**（方針外の変更は行わない）。
- 修正後、計画ファイル内の整合性（フェーズ番号、タスク番号の連番等）を確認する。

#### 出力形式

```text
## 修正内容

1. Phase 2 にタスク「○○」を追加
2. タスク3 の関数参照を foo() → bar() に修正
```

### 4. 結果報告（ループ終了後）

全イテレーションの結果をまとめて報告する。

```text
## plan-review-loop 結果

### レビューモード
- {専門家エージェント / 単一レビュー}
- 起動エージェント: {architect, security, testing}（専門家モード時のみ）

### 修正した問題
- [観点: 網羅性] 完了条件「○○」のタスク追加
- [観点: 実現可能性] 関数参照の修正

### サマリ
- ループ回数: {n}回
- 修正: {n}件
- 最終レビュー: 問題0件
- 計画ファイル: ~/.cache/vibecorp/plans/<repo-id>/{branch_name}.md
```

## 🚧 制約

- 計画ファイル（`~/.cache/vibecorp/plans/<repo-id>/*.md`）のみを変更対象とする（コードは変更しない）。
- `git add` / `git commit` / `git push` は実行しない（呼び出し元に委ねる）。
- 最大 5 回でループを打ち切る（無限ループ防止）。
- レビュー観点に該当しない「好み」レベルの改善提案は問題として扱わない。
- 専門家エージェント未設定時は単一レビューモード（フォールバック）にフォールバックする。

## 🔗 関連

| 種別 | 参照先 |
|------|--------|
| 関連スキル | `/vibecorp:plan`（計画策定）/ `/vibecorp:ship`（包括オーケストレーション） |
| 関連エージェント | `.claude/agents/plan-architect.md` / `.claude/agents/plan-security.md` / `.claude/agents/plan-testing.md` 等 |
| CEO 向け文面規約 | `.claude/rules/communication.md` |
| プロンプト作成基準 | `.claude/rules/prompt-writing.md` |
| マークダウン規約 | `.claude/rules/markdown.md` |
