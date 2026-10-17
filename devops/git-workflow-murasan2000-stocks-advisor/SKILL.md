---
name: git-workflow
description: Claude が実装作業を行う際のブランチ運用・コミット/push・コミットメッセージ規約。作業を開始する前（ブランチ作成）と、実装が一区切りついた時（commit + push）に必ず使う。作業の消失防止と、コミット履歴からタスク・スコープが分かる状態を保つのが目的。
---

# Git ワークフロー（ブランチ・コミット・push）

Claude Code が実装作業を行う際は、以下を必ず守る。ローカルセッション・
Claude.ai セッションのどちらで作業していても同じルールを適用する。

## 1. 作業開始時に必ずブランチを切る

- `main` 上で直接作業しない。実装に着手する前に必ず`main`に移動して、最新化してからブランチを切る。
- ブランチ名: `claude/feature/<topic>`（例: `claude/feature/fix-harness`）
  - `<topic>` は作業内容が分かる kebab-case の短い名前にする。
- 既に作業用ブランチ（`claude/...` や `feature/...`）上にいる場合は切り直さない。

```bash
git switch -c claude/feature/<topic>
```

## 2. 作業が一区切りついたら必ず commit して push する

- 目的は「ローカル or Claude.ai セッションが途中で終了・切断しても、やっていた
  作業がリモートに残っている」状態を常に保つこと（作業消失の防止）。
- 実装が一区切りついた時点（1機能・1修正の実装が終わった、lint/test が通った、
  など）で、指示を待たずに commit → push まで行ってよい。
- push は `.claude/settings.json` で `allow` に設定されているため、確認なしで
  実行してよい（PR時に人間がレビューする前提のため）。

## 3. コミットメッセージ規約

```
<type>(<scope>): <description>
```

Conventional Commits の type 語彙をベースにし、scope はこのリポジトリの構成に
合わせる（Claude Code が実装しPRで人間がレビューする、という運用上、
自動化・機械可読性を優先する）。

### type

| type | 意味 |
|---|---|
| `feat` | 新機能・新規実装の追加 |
| `fix` | 不具合・想定外動作の修正 |
| `refactor` | 外部の動作を変えない内部構造の変更 |
| `perf` | パフォーマンス改善 |
| `test` | テストの追加・修正のみ |
| `docs` | ドキュメントのみの変更 |
| `chore` | 上記に当てはまらない雑務・依存更新 |
| `ci` | `.github/workflows/` の変更 |

### scope

「プロダクトのコード」と「Claude Code 自身の運用ルール」を区別する。

| scope | 対象 |
|---|---|
| `api` | `api/` 配下（`agents` 以外。エンドポイント・スクリーナー・チャット・Jobs等） |
| `agent` | `api/app/services/agents/` 配下（LangGraphによるAIエージェント＝プロダクト機能） |
| `web` | `web/` 配下（フロントエンド） |
| `infra` | デプロイ・実行環境（devcontainer・CI/CD基盤・環境変数まわり等） |
| `harness` | `.claude/` 配下（権限・フック・スキル・サブエージェント定義）と `CLAUDE.md`。Claude Code 自身がどう動くか（実装のためのAI DevOps基盤）を規定する設定 |

- scope 省略可なのは `docs` / `chore` / `ci` など、特定領域に閉じない変更のみ。

### `agent` と `harness` の使い分け

紛らわしいので明確に区別する。

- `agent`: プロダクトが提供するAIエージェント機能そのもの（LangGraphのグラフ・ノード実装）。
- `harness`: Claude Code というツール自体をこのリポジトリでどう運用するか（権限・フック・
  スキル・サブエージェント定義・CLAUDE.md）。プロダクトコードではない。
- 例:「並列サブエージェントのworktreeパスが誤ってガードレールのaskルールに
  引っかかる問題の修正」はプロダクトの`agent`機能ではなくClaude Code運用の問題なので
  `fix(harness): ...` になる（`fix(infra)` ではない）。

例:

- `feat(web): 銘柄比較モーダルを追加`
- `fix(agent): 意図判定の誤分類を修正`
- `fix(harness): worktree配下の実装編集がガードレールaskに誤爆する問題を修正`
- `refactor(api): スクリーナー処理を分割`
- `docs: CLAUDE.mdの開発フロー節を更新`
- `chore(api): 依存パッケージを更新`
