---
name: create-skill
description: >
  新しいスキルの作成ガイドを提供する。Use when user asks to [スキルを作りたい, 新しいスキル, /create-skill].
domain: ops
---

### frontmatter の使い分け

| パターン | 設定 | 用途 |
|----------|------|------|
| ユーザー＆Claude両方が呼出し | (デフォルト) | 汎用リファレンス・軽い作業 |
| ユーザーのみ呼出し | `disable-model-invocation: true` | デプロイ・副作用のある操作 |
| Claudeのみ呼出し | `user-invocable: false` | 背景知識・規約 |

### 本文の構成パターン

**タスク型**（手順を実行するスキル）:
```markdown
## 用途
## 引数
## 手順
### Phase 1: ...
### Phase 2: ...
## 注意
## 参照
```

**リファレンス型**（知識を提供するスキル）:
```markdown
## いつ適用するか
## 規約
## 例外
```

### 変数置換

| 変数 | 内容 |
|------|------|
| `$ARGUMENTS` | スキル呼出し時の全引数 |
| `$ARGUMENTS[0]`, `$0` | 位置引数（0始まり） |
| `${CLAUDE_SKILL_DIR}` | SKILL.md のあるディレクトリ絶対パス |
| `${CLAUDE_SESSION_ID}` | セッション ID |

スクリプト参照は `${CLAUDE_SKILL_DIR}` を使う:
```bash
node "${CLAUDE_SKILL_DIR}/scripts/helper.js" $ARGUMENTS
```

### 動的コンテキスト注入

`` !`command` `` 構文でシェルコマンドの出力をスキル内容に埋め込める:
```markdown
## 現在の状態
- ブランチ: !`git branch --show-current`
- 未コミット: !`git status --short`
```

## scripts/ の設計

### 2つのパターン

**パラメータ駆動型**（推奨: 繰り返し使うスクリプト）:
- JSON 設定ファイルを受け取り、出力を生成
- スクリプト自体は変更不要
- 例: `scatter.js config.json output.svg`

**テンプレート型**（カスタマイズが必要なスクリプト）:
- `// CUSTOMIZE:` コメントで編集箇所を明示
- 記事ディレクトリにコピーして使う
- 例: `cover-template.js`

### スクリプトの原則

1. **自己完結**: 外部パッケージへの依存は最小限（`require('fs')`, `require('path')` 等の Node.js 標準 + プロジェクトの `node_modules`）
2. **引数は `process.argv`**: 設定は JSON ファイル or コマンド引数で渡す
3. **出力先は引数で指定**: ハードコードしない
4. **エラーメッセージは具体的に**: 設定ファイルがない場合は使い方を表示

## reference/ の設計

`SKILL.md` が 500 行を超えそうなとき、詳細を分離する:

- **デザインシステム**: 色・フォント・サイズ等の定数
- **チャートパターン**: 種別ごとの選び方・実装方法
- **API リファレンス**: 関数シグネチャ・オプション一覧

`SKILL.md` からの参照:
```markdown
詳細は [reference/design-system.md](reference/design-system.md) を参照。
```

## examples/ の設計

**完成物の実例**を置く。Claude が構造を理解する最良のリファレンス。

- 実際の記事から生成した SVG / JSON / マークダウン
- コメント付きで「なぜこの構造か」を説明（任意）

## スキルの配置場所

| 場所 | パス | 適用範囲 |
|------|------|----------|
| プロジェクト | `.claude/skills/<name>/SKILL.md` | このリポジトリ |
| 個人 | `~/.claude/skills/<name>/SKILL.md` | 全プロジェクト |
| エンタープライズ | managed settings | 組織全体 |

同名の場合の優先順位: エンタープライズ > 個人 > プロジェクト。

## ベストプラクティス

1. **SKILL.md は 500 行以内**: 詳細は reference/ に分離
2. **description は具体的に**: Claude の自動呼出し判断の根拠になる
3. **副作用のあるスキルは `disable-model-invocation: true`**: デプロイ・DB変更・外部API呼出し等
4. **一時ファイルは後処理で削除**: CLAUDE.md の作業規約に従う
5. **スクリプトは `${CLAUDE_SKILL_DIR}` で参照**: 作業ディレクトリに依存しない
6. **`context: fork` は明確なタスクがあるときのみ**: ガイドラインだけのスキルをforkすると空の結果が返る
7. **`allowed-tools` で最小権限**: 読み取り専用スキルには `Read, Grep, Glob` のみ

## サブエージェント作成時の model 指定ルール

新しいサブエージェント（`.claude/agents/*.md`）を作成・改修するときは、frontmatter の `model:` を必ず決める。既定値は **`sonnet`**。

### 判定フロー

1. **Generator か？**（コンテンツ生成・変換・リライト・データ収集・ルーブリック適用）
   → `model: sonnet`
2. **Evaluator で、評価基準が定型化されているか？**（5軸ルーブリック・チェックリスト・HIGH/MEDIUM/LOW 判定）
   → `model: sonnet`
3. **オーケストレーターで、親の思考力を借りたいか？**（戦略判断・批判的レビュー・事前検死）
   → `model: inherit`
4. **上記に当てはまらず、サブエージェント側で Opus が必要な理由があるか？**
   → frontmatter の description と本文「モデル方針」欄に理由を明記した上で `model: opus`。これは例外扱い

### テンプレート frontmatter

```yaml
---
name: {agent-name}
description: {一行説明 — 種別（Generator/Evaluator/Orchestrator）を含める}
model: sonnet  # または inherit（オーケストレーターのみ）
domain: {領域 id — config/domains.json（skills-design-guide.md「domain フィールド」）}
---

# {Agent Name}

{本文}

> **モデル方針**: このエージェントは `model: {sonnet|inherit}` で動作します。{理由を1-2文で}。詳細は CLAUDE.md「ハーネス設計原則」参照。
```

### 既存エージェントの model 指定一覧

CLAUDE.md §5「ハーネス設計原則」の既定（サブエージェントは sonnet・Opus は親のみ）に従う。エージェントを追加したら `.claude/knowledge/reference/agents-registry.md`「エージェント一覧」を更新すること（CLAUDE.md に per-agent の表は無い）。

### なぜこうするか

親エージェント（Claude Code 本体）が Opus で計画・判断・統合を担い、サブエージェントは Sonnet で高速・低コストに実行する。これによりコスト効率と判断の質を両立できる。Opus を固定指定するのはサブエージェント側で深い推論が不可欠なケースのみで、原則は親の Opus がレビューする前提で Sonnet に任せる。詳細は CLAUDE.md「ハーネス設計原則」§5。

## このプロジェクト固有の規約

詳細は [reference/project-conventions.md](reference/project-conventions.md) を参照。
