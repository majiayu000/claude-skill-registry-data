---
name: run-e2e
description: |-
  worktree環境のdevcontainer内でE2Eテスト（Playwright）をセットアップ・実行するスキル。稼働中のdevcontainerがあれば再利用し、なければ新規作成する。INSTANCE_ID判定、ポート計算、DBリセット、ブラウザインストール、サーバー起動確認、テスト実行、結果報告までを一括で行う。「E2E実行」「Playwright実行」「e2eテスト走らせて」「run e2e」「E2Eテストを動かす」「worktreeでテスト」など、E2Eテストの実行依頼があった際に使用する。
allowed-tools: Bash, Read
---

> **前提**: 本スキルは git worktree + devcontainer を用いた並列実行フローを前提とする。`.stdd.config.yml` で `worktree` プラグインを併せて有効化すること。

# Worktree上でE2Eテストを実行するスキル

worktree環境のdevcontainer内でE2Eテストをセットアップ・実行する。
稼働中のdevcontainerがあればそれを使い、なければ新規作成する。

## 1. 稼働中のworktree devcontainerを検索

```bash
for i in 1 2 3 4; do
  wt_dir="{{worktree.base_path}}/worktree-${i}"
  container=$(docker ps --filter "label=devcontainer.local_folder=${wt_dir}" --format "{{.Names}}" 2>/dev/null)
  if [ -n "$container" ]; then
    echo "FOUND:${i}:${container}"
  fi
done
```

### 判定ロジック

- **`FOUND:N` が出力された場合** → そのINSTANCE_ID=Nのdevcontainerを使用。ステップ2へ進む
- **何も出力されない場合** → 稼働中のworktree devcontainerなし。ステップ1-Bで新規作成する

## 1-B. Worktree＋devcontainerを新規作成

稼働中のworktree devcontainerがなかった場合のみ実行する。

### 空きINSTANCE_IDを特定

```bash
for i in 1 2 3 4; do
  wt_dir="{{worktree.base_path}}/worktree-${i}"
  if [ ! -d "$wt_dir" ]; then
    echo "AVAILABLE:${i}"
    break
  fi
done
```

最初に見つかった空きIDを使用する。空きがない場合はユーザーに不要なworktreeの破棄を案内して中断する。

### worktree作成

```bash
./scripts/create-worktree.sh -b claude/e2e-run -i <INSTANCE_ID>
```

### devcontainer起動

```bash
devcontainer up --workspace-folder {{worktree.base_path}}/worktree-<INSTANCE_ID> --override-config {{worktree.base_path}}/worktree-<INSTANCE_ID>/.devcontainer/devcontainer.override.json
```

起動完了を待ってからステップ2へ進む。

## 2. 環境変数の算出

特定したINSTANCE_IDから以下を算出する:

```
WORKTREE_DIR = {{worktree.base_path}}/worktree-<INSTANCE_ID>
OVERRIDE_CONFIG = ${WORKTREE_DIR}/.devcontainer/devcontainer.override.json

# ポート計算（INSTANCE_IDに応じてオフセット）
# 各アプリのベースポートは .stdd.config.yml の apps[].port を用いる（apps[] の数だけ繰り返す）
APP_PORT(<apps[].id>) = <apps[].port> + INSTANCE_ID * 100   (例: base=3000, ID=1 → 3100, ID=2 → 3200)
SUPABASE_API_PORT = 54321 + INSTANCE_ID * 1000
SUPABASE_DB_PORT = 54322 + INSTANCE_ID * 1000
```

以降のdevcontainer execコマンドはすべて以下の形式で実行する:

```bash
devcontainer exec --workspace-folder <WORKTREE_DIR> --override-config <OVERRIDE_CONFIG> bash -c "COMMAND"
```

**重要**: 変数代入をコマンドの先頭に置かないこと。必ず `devcontainer exec` からコマンドを始める（auto-approve対象パターンに合致させるため）。

## 3. E2Eテスト環境のセットアップ

`--skip-setup` が引数に含まれていればこのステップ全体をスキップする。

### 3-1. DBリセット（テストデータ準備）

```bash
devcontainer exec --workspace-folder <WORKTREE_DIR> --override-config <OVERRIDE_CONFIG> bash -c "cd /workspace/supabase && <commands.db_reset>"
```

### 3-2. Playwrightブラウザインストール

```bash
devcontainer exec --workspace-folder <WORKTREE_DIR> --override-config <OVERRIDE_CONFIG> bash -c "cd /workspace/e2e && npx playwright install --with-deps chromium"
```

### 3-3. アプリケーションサーバー起動確認

`.stdd.config.yml` の各 `apps[]` について、算出した `APP_PORT(<apps[].id>)` で疎通確認する（apps[] の数だけ繰り返す）。

```bash
devcontainer exec --workspace-folder <WORKTREE_DIR> --override-config <OVERRIDE_CONFIG> bash -c "curl -s -o /dev/null -w '%{http_code}' http://localhost:<APP_PORT> && echo ' <apps[].id> OK' || echo ' <apps[].id> NOT RUNNING'"
```

起動していない場合はバックグラウンドで起動する:

各 `apps[]` について、`apps[].path` ディレクトリで dev サーバを起動する（apps[] の数だけ繰り返す）。

```bash
devcontainer exec --workspace-folder <WORKTREE_DIR> --override-config <OVERRIDE_CONFIG> bash -c "cd /workspace/<apps[].path> && SKIP_EMAIL_SEND=true nohup npm run dev > /tmp/<apps[].id>.log 2>&1 &"
```

起動後、全 `apps[]` が応答するまで待機（各 `APP_PORT(<apps[].id>)` を列挙）:

```bash
devcontainer exec --workspace-folder <WORKTREE_DIR> --override-config <OVERRIDE_CONFIG> bash -c "npx wait-on http://localhost:<APP_PORT> ... --timeout 120000"
```

## 4. E2Eテスト実行

引数の内容に応じてテストを実行する（`--skip-setup` は除外して解釈）。

### 引数のパターン

プロジェクト名には `.stdd.config.yml` の `apps[].id` を用いる。

| 引数                       | 実行内容                                 |
| -------------------------- | ---------------------------------------- |
| なし / `all`               | 全テスト実行                             |
| `<apps[].id>`              | 指定アプリのプロジェクトのみ             |
| `<apps[].id> <spec名>`     | 指定アプリの特定specファイル             |
| その他の文字列             | Playwrightの `--grep` パターンとして使用 |

### 実行コマンド

**全テスト実行（引数なし / all）:**

```bash
devcontainer exec --workspace-folder <WORKTREE_DIR> --override-config <OVERRIDE_CONFIG> bash -c "cd /workspace/e2e && npx playwright test"
```

**プロジェクト指定:**

```bash
devcontainer exec --workspace-folder <WORKTREE_DIR> --override-config <OVERRIDE_CONFIG> bash -c "cd /workspace/e2e && npx playwright test --project=<PROJECT>"
```

**プロジェクト＋specファイル指定:**

```bash
devcontainer exec --workspace-folder <WORKTREE_DIR> --override-config <OVERRIDE_CONFIG> bash -c "cd /workspace/e2e && npx playwright test --project=<apps[].id> tests/<apps[].id>/<SPEC>.spec.ts"
```

**grepパターン指定:**

```bash
devcontainer exec --workspace-folder <WORKTREE_DIR> --override-config <OVERRIDE_CONFIG> bash -c "cd /workspace/e2e && npx playwright test --grep '<PATTERN>'"
```

## 5. テスト結果の報告

テスト完了後、以下を報告する:

1. **成功/失敗の概要**: passした数、failした数、スキップ数
2. **失敗テストの詳細**: 失敗したテスト名とエラーメッセージ
3. **次のアクション提案**:
   - 全テスト成功 → 「テストすべてパスしました」
   - 失敗あり → 失敗原因の分析と修正提案

## 注意事項

- テスト実行中のタイムアウトはPlaywright設定（30秒/テスト）に従う
- devcontainer内のポートはINSTANCE_IDに応じてオフセットされる（create-worktree.shが `.env.local` のポートを自動書き換え済み）
- 新規作成したworktreeはテスト後も残る。不要になったら `remove-worktree` skill で破棄すること
