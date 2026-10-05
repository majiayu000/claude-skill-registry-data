---
name: pr-create
description: >
  現在のブランチから GitHub PR を作成する。git status / diff / log を解析し、PR タイトルと body を自動生成、gh CLI で PR を open する。body は HEREDOC で整形し Co-Authored-By を付与、git add は明示指定のみ。
  Use when user asks to [PR作って, PR作成, プルリク, /pr-create, create pull request].
user-invocable: true
domain: ops
---

現在のブランチから GitHub PR を作成する統一スキル。`/deploy`（develop→main 運用フロー）とは別に、**feature ブランチから develop/main への個別 PR 作成** を担う。

## 用途

- 変更を push → PR open までの定型作業を 1 スキルに集約
- PR title 70 文字制限、HEREDOC body テンプレ、Co-Authored-By 付与を自動化
- `git add .` / `-A` の誤爆（.env・認証情報混入）を防ぐ

## 引数

```
/pr-create [--base <branch>] [--draft]
```

- **`--base`**: PR の base ブランチ（省略時は `develop` — CLAUDE.md §2「ブランチ」に準拠）
- **`--draft`**: Draft PR として作成
- 引数省略時: 現在の branch から `develop` への PR を作成。`main` 直指定は本番障害 hotfix のみ

## 実行手順

### Step 1: 前提確認（並列）

以下を並列で取得:

- `git status --short` — 未コミット変更の有無
- `git branch --show-current` — 現ブランチ名
- `git rev-parse --abbrev-ref '@{upstream}'` 2>/dev/null — upstream tracking 有無
- `git log --oneline {base}..HEAD` — base からの差分コミット
- `git diff {base}...HEAD --stat` — ファイル変更サマリ

**中止条件**:
- 未コミット変更がある → 「先に commit or stash してください」と報告して中止
- 現ブランチが `main` / `develop` → 「feature ブランチを切ってください」と報告して中止
- `{base}..HEAD` が空 → 「base との差分なし」と報告して中止

### Step 2: タイトル・body 草案作成

- **title**: コミットメッセージ（最新 1〜3 件）から要約。**70 文字以下**。conventional commits プレフィックス（`feat:` / `fix:` / `chore:` 等）があれば踏襲
- **body**: 以下テンプレ

```markdown
## Summary
- <要点 1>
- <要点 2>
- <要点 3>

## Test plan
- [ ] <検証項目 1>
- [ ] <検証項目 2>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

Summary は `git log` の本文と diff stat から生成。Test plan は「何を確認すれば動いているとわかるか」を書く（テスト実行・ページ表示・型チェック等）。

### Step 3: push（必要な場合）

- upstream tracking が無ければ `git push -u origin {branch}`
- tracking ありで local が進んでいれば `git push`
- base が main なら **force push は絶対に行わない**

### Step 4: PR 作成

```bash
gh pr create \
  --base "<base>" \
  --title "<title>" \
  --body "$(cat <<'EOF'
<body テンプレをここに埋め込む>
EOF
)" \
  [--draft]
```

**重要**: body は必ず HEREDOC で渡す（改行・バッククォート・ダラーの escape を避ける）。

### Step 5: URL 返却 + 次アクション提示

- gh CLI が返した PR URL を報告
- CI が走る場合はその旨を案内（`ci.yml` が PR on main/develop で実行）
- draft で作成した場合は「準備できたら `gh pr ready <number>` で ready に変更」と案内

## 例

### 例 1: feature ブランチから develop への PR（デフォルト）

```bash
/pr-create
```

→ base = develop、現在のブランチとの差分でタイトル・body 生成、`gh pr create` 実行。

### 例 2: develop から main への PR（リリース時のみ、通常は `/deploy` を使う）

```bash
/pr-create --base main
```

→ base = main、develop との差分で PR 作成。リリース用。

### 例 3: 本番障害 hotfix

feature ブランチを main から直接切って:

```bash
/pr-create --base main
```

→ hotfix 用の緊急 PR。merge 後は main → develop 逆 merge を忘れない。

### 例 3: Draft PR

```bash
/pr-create --draft
```

→ Draft として open。レビュー準備中の場合に使う。

## アンチパターン

- **`git add .` / `git add -A` を使わない** — 明示的にファイル指定。`.env` などの混入防止（CLAUDE.md §3「`git add` は変更したファイルだけ明示指定」）
- **未コミット変更のまま PR 作成しない** — 必ず Step 1 で停止
- **PR title を 70 文字超にしない** — 超過する場合は body で補足
- **`--no-verify` を使わない** — pre-commit / pre-push が fail したら原因を直す
- **force push しない** — 特に base が main のとき（CLAUDE.md 明示）
- **`commit.gpgsign=false` などの署名バイパスを使わない** — ユーザが明示的に依頼した場合のみ
- **本スキル内で commit を作らない** — Step 1 で未コミットを検出したらユーザに返す。commit は別タスク

## トラブルシューティング

| エラー | 原因 | 対処 |
|---|---|---|
| `gh: command not found` | gh CLI 未インストール | `brew install gh` |
| `authentication required` | gh 未ログイン | `gh auth login` をユーザに案内 |
| `a pull request already exists` | 既存 PR あり | `gh pr view` で URL を返す |
| push が pre-push でブロック | `npm test` or `type-check` fail | 原因を直してから再実行 |

## 参照

- `CLAUDE.md` ── §2「ブランチ」・§3「外科的に変更する」・§10「チェックポイント」。並行セッションの経緯は `.claude/knowledge/reference/workflows.md`「ブランチ・並行セッション運用」
- `.claude/skills/dev/deploy/SKILL.md` ── develop→main 運用フロー（こちらは push 後のデプロイ確認まで）
- `.github/workflows/ci.yml` ── PR on main で走る CI
- `scripts/install-pre-push.mjs` ── push 時の test + type-check 検証（Phase 2-D）
