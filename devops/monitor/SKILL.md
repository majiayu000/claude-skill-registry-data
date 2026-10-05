---
name: monitor
description: >
  Monitor toolでバックグラウンド監視を起動する（dev/mojibake/ci/build/r2/frontmatter/health/mdx-validation）。
  Use when user asks to [監視, モニター, monitor, /monitor].
domain: ops
---

バックグラウンド監視をMonitor toolで起動するスキル。引数で監視タイプを指定する。

## 使い方

```
/monitor <type>
```

`<type>` は以下のいずれか（複数スペース区切りで同時起動可）:

| type | 監視内容 | persistent |
|---|---|---|
| `dev` | 開発サーバーのエラー監視 | yes |
| `mojibake` | Unicode文字化け (U+FFFD) 検出 | yes |
| `ci` | GitHub Actions ワークフロー監視 | no |
| `build` | ビルド進捗・完了通知 | no |
| `r2` | R2 画像アップロード進捗 | no |
| `frontmatter` | frontmatter 必須フィールド漏れ | yes |
| `health` | デプロイ後ヘルスチェック | no |
| `mdx-validation` | MDX変更時の自動バリデーション | yes |

### ショートカット

| ショートカット | 展開先 |
|---|---|
| `dev-all` | `dev` + `mojibake` |
| `deploy-all` | `ci` + `health` |
| `content-all` | `mojibake` + `frontmatter` + `mdx-validation` |

## 各モニターの実装

### 1. dev — 開発サーバーのエラー監視

開発サーバー（npm run dev）のstdoutからエラー行だけをフィルタして通知する。

```
Monitor:
  command: cd "$CLAUDE_PROJECT_DIR" && npm run dev 2>&1 | grep --line-buffered -iE "(error|ERR_|failed|ENOENT|SyntaxError|warning.*mdx|Module not found)"
  description: "Next.js dev server errors"
  persistent: true
```

**注意**: dev モニターは開発サーバー自体を起動する。既に `npm run dev` が動いている場合はユーザーに確認すること。

### 2. mojibake — Unicode文字化け検出

LLM出力で発生しやすいマルチバイト文字の破損 (U+FFFD) を定期スキャン。

```
Monitor:
  command: bash .claude/skills/dev/monitor/scripts/check-mojibake.sh 15
  description: "Unicode mojibake (U+FFFD) detection in MDX"
  persistent: true
```

### 3. ci — GitHub Actions ステータス監視

push後の最新ワークフロー実行を追跡し、完了時に結果を通知する。

```
Monitor:
  command: cd "$CLAUDE_PROJECT_DIR" && gh run watch --exit-status 2>&1
  description: "GitHub Actions workflow status"
  persistent: false
  timeout_ms: 600000
```

**代替（ポーリング版）**: gh run watch が使えない場合:

```
Monitor:
  command: |
    cd "$CLAUDE_PROJECT_DIR"
    prev_status=""
    while true; do
      run=$(gh run list --limit 1 --json status,conclusion,name,headBranch --jq '.[0] | "\(.name) [\(.headBranch)]: \(.status) \(.conclusion // "")"' 2>/dev/null || echo "API error")
      if [ "$run" != "$prev_status" ]; then
        echo "$run"
        prev_status="$run"
        # completed なら終了
        echo "$run" | grep -q "completed" && exit 0
      fi
      sleep 30
    done
  description: "GitHub Actions workflow polling"
  persistent: false
  timeout_ms: 600000
```

### 4. build — ビルド進捗・完了通知

npm run build の出力からマイルストーン行だけを通知。ビルド中に別作業を続けられる。

```
Monitor:
  command: cd "$CLAUDE_PROJECT_DIR" && npm run build 2>&1 | grep --line-buffered -iE "(Generating|Generated|Route|error|✓|✗|Compiling|Building|entries|sitemap|Export)"
  description: "Next.js build progress"
  persistent: false
  timeout_ms: 600000
```

### 5. r2 — R2 アップロード進捗監視

upload-images-to-r2.mjs の出力から進捗と失敗を通知。

```
Monitor:
  command: cd "$CLAUDE_PROJECT_DIR" && node .claude/scripts/upload-images-to-r2.mjs 2>&1 | grep --line-buffered -iE "(Found|Progress|FAILED|Done|Error|Uploading|Skipped)"
  description: "R2 image upload progress"
  persistent: false
  timeout_ms: 600000
```

### 6. frontmatter — frontmatter 必須フィールド漏れ

title, description, category, tags, published の欠損を定期チェック。

```
Monitor:
  command: node .claude/skills/dev/monitor/scripts/check-frontmatter.mjs 60
  description: "frontmatter required fields check"
  persistent: true
```

### 7. health — デプロイ後ヘルスチェック

デプロイ後に主要URLのHTTPステータスを確認する。ワンショット実行。

```
Monitor:
  command: bash .claude/skills/dev/monitor/scripts/health-check.sh 30
  description: "Post-deploy health check"
  persistent: false
  timeout_ms: 120000
```

### 8. mdx-validation — MDX変更時の自動バリデーション

MDXファイルの変更を検知し、変更ファイルのバリデーションを実行する。

```
Monitor:
  command: |
    cd "$CLAUDE_PROJECT_DIR"
    echo "Watching content/site/ for MDX changes (10s interval)..."
    marker_file=$(mktemp)
    touch "$marker_file"
    while true; do
      sleep 10
      changed=$(find content/site -name "*.mdx" -newer "$marker_file" 2>/dev/null | head -10)
      if [ -n "$changed" ]; then
        touch "$marker_file"
        count=$(echo "$changed" | wc -l)
        echo "MDX CHANGED: $count file(s) detected"
        for f in $changed; do
          result=$(node .claude/scripts/validate-mdx.mjs "$f" 2>&1)
          if echo "$result" | grep -q "✗\|error"; then
            echo "VALIDATION ERROR: $f"
            echo "$result" | grep -E "✗|error|→" | head -5
          else
            echo "VALIDATION OK: $f"
          fi
        done
      fi
    done
  description: "MDX auto-validation on file change"
  persistent: true
```

## 手順

### Step 1: 引数を解析

ユーザーの引数を解析し、起動するモニターを決定する。

- 引数なし → ユーザーに一覧を表示し選択を促す
- `dev-all` → `dev` + `mojibake` を起動
- `deploy-all` → `ci` + `health` を起動
- `content-all` → `mojibake` + `frontmatter` + `mdx-validation` を起動
- 個別のtype名 → 該当モニターを起動

### Step 2: 競合チェック

- `dev` モニター起動前: 既に開発サーバーが起動していないか確認（ポート3020）
- `build` モニター: 開発サーバーと同時実行は非推奨（リソース競合）
- `ci` モニター: `gh auth status` でGitHub CLIの認証状態を確認

### Step 3: Monitor tool で起動

上記「各モニターの実装」セクションに記載されたコマンド・パラメータでMonitor toolを呼び出す。

複数モニターを同時起動する場合は、並列にMonitor toolを呼び出す。

### Step 4: 起動確認

起動したモニターの一覧をユーザーに報告する:
- モニター名
- persistent かどうか
- 停止方法（TaskStop を使用）

## 停止方法

- persistent モニターは TaskStop で停止できる
- ワンショットモニター（build, ci, r2, health）は完了時に自動終了
- 全モニター停止: ユーザーに TaskStop の使用を案内
