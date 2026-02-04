---
name: tanaoroshi
description: セッションログから価値ある発見を抽出し、カテゴリ別に整理する。「棚卸し」「セッションログの整理」「発見をまとめて」などと言われたら実行。
---

# 棚卸し (Tanaoroshi) Skill

セッションログから価値ある Findings（発見）を抽出し、プロジェクト知識として蓄積する。

---

## 設定

`.claude/tanaoroshi.json` があれば読み込む。なければデフォルト値を使用。
```json
{
  "outputDir": ".claude/findings",
  "categories": []
}
```

| キー | デフォルト | 説明 |
|------|-----------|------|
| `outputDir` | `.claude/findings` | 発見の出力先 |
| `categories` | `[]`（空配列） | ユーザーが特に分類を明示する場合に設定。カテゴリ定義の配列 |

### categories の形式
```json
{
  "categories": [
    { "name": "docker" },
    { "name": "testing" },
    { 
      "name": "decisions",
      "description": "技術選択の理由、方針決定の経緯"
    }
  ]
}
```

| フィールド | 必須 | 説明 |
|-----------|:----:|------|
| `name` | ✓ | カテゴリ名（英語小文字ケバブケース） |
| `description` | - | 補足説明（名前だけでは意図が伝わりにくい場合） |

Claude Codeが `name` のみでカテゴライズできそうな場合は `description` は省略可能。
Claude Codeに推測されては困る場合に `description` を指定する。

---

## 実行手順

### 1. 設定の読み込み

`.claude/tanaoroshi.json` を確認。なければデフォルト設定を使用。

### 2. 未処理のセッションログを取得
```bash
ls .claude/.tanaoroshi/logs/pending/session-*.jsonl 2>/dev/null
```

ファイルがなければ「未処理のセッションログはありません」と報告して終了。

### 3. セッションログの読み込み

**重要**: セッションログはサイズが大きい（数百KB〜数MB）ため、`Read()` ツールを使わない。必ず `bash` + `jq` で処理する。

#### 3-1. 各ログの概要を確認
```bash
# 行数とファイルサイズ
wc -l .claude/.tanaoroshi/logs/pending/session-*.jsonl

# メッセージタイプの分布
cat {file} | jq -r '.type' | sort | uniq -c
```

#### 3-2. user/assistant メッセージを抽出
```bash
cat {file} | jq -r '
  select(.type == "user" or .type == "assistant") |
  .message.content // .message |
  if type == "array" then
    map(select(.type == "text") | .text) | join("\n")
  else
    .
  end
' 2>/dev/null
```

#### 3-3. 大きすぎる場合は分割処理

抽出結果が大きい場合、`head`/`tail` や行番号指定で分割：
```bash
# 前半
cat {file} | jq -r '...' | head -n 500

# 後半
cat {file} | jq -r '...' | tail -n 500
```

### 4. 棚卸しセッション自体のログを除外

以下のパターンが含まれるログは棚卸し作業のログなので、発見抽出の対象外：

- 「棚卸し」「tanaoroshi」への言及が最初のユーザーメッセージにある
- `Launching skill: tanaoroshi` が含まれる

これらは処理済みとして削除する。

### 5. 発見を抽出

抽出したメッセージから、価値ある発見を探す（判定基準は後述）。

### 6. カテゴリを判断して保存

発見の内容と設定された `categories` を照合：

- **マッチするカテゴリがある** → `{outputDir}/{name}/` に保存
- **どれにもマッチしない** → `{outputDir}/_etc/{autoCategoryName}/` に保存

### 7. index.md を更新

`{outputDir}/index.md` に新しい発見への参照を追加。

### 8. 参照ルールの生成

`.claude/rules/findings.md` を生成/更新：
```markdown
# プロジェクト知識（Findings）

このプロジェクトの技術知見は `{outputDir}/` に蓄積されている。

関連する作業を行う際は、まず `{outputDir}/index.md` を確認し、
過去の発見や決定事項を参照すること。

特に以下の場合は必ず確認：
- 同じ技術・ライブラリを扱う時
- エラーや問題に遭遇した時
- 設計・実装の方針を決める時
```

### 9. 処理済みログを振り分け

- **有用**（発見が抽出された）→ `.claude/.tanaoroshi/logs/{year}/{month}/` に移動
- **不要**（価値ある発見なし、または棚卸しセッション自体）→ 削除

---

## カテゴリの振り分け

### ディレクトリ構造
```
{outputDir}/
├── index.md
├── {category}/           # ユーザー定義カテゴリ
└── _etc/                 # 自動振り分け
    └── {autoCategoryName}/
```

### 運用

- **`_etc/` に同じカテゴリが増えてきたら**: `.claude/tanaoroshi.json` の `categories` に追加して正式なカテゴリに昇格
- **カテゴリの昇格時**: `_etc/{name}/` から `{outputDir}/{name}/` に移動し、index.md を更新

### カテゴリ名のルール

- 英語小文字のケバブケース（例: `docker`, `api-design`, `ci-cd`）
- 短く具体的に

---

## 価値ある Findings の判定基準

### 記録すべきもの

- **マニュアルに書いてないこと**: 公式ドキュメントでは説明されていない挙動
- **実際にやってみて初めてわかったこと**: 試行錯誤の結果得られた知見
- **特定の組み合わせでの挙動**: 複数の機能・設定を組み合わせた際の動作
- **ハマりポイントと解決策**: エラーや予期しない挙動とその対処法
- **ベストプラクティス**: 効率的・推奨される実装パターン
- **技術選択の理由と経緯**: なぜこの技術・バージョン・環境を選んだか
- **環境構築で遭遇した問題**: セットアップ時のエラーや依存関係の問題と解決策
- **プロジェクト固有の方針決定**: このプロジェクトで決めたルールや前提条件

### 記録しないもの

- **概念の一般的な説明**: 「エンティティとは」「シリアライザとは」など
- **公式ドキュメントのコピー**: マニュアルを読めばわかること
- **単純な使い方**: 基本的なコマンドや設定方法
- **棚卸し作業自体のログ**: このスキルの実行ログは対象外

### 判定の例
```
NG: 「Dockerの基本的な使い方」
    → マニュアルに書いてある

OK: 「docker-compose.ymlでvolumesのパーミッションが原因でビルドが失敗する件」
    → 実際にやってみないとわからない

NG: 「ReactのuseStateの説明」
    → 公式ドキュメント参照

OK: 「React 18のSuspenseとTanStack Queryを組み合わせた際のハイドレーションエラー」
    → 両者を組み合わせた実践的知見
```

---

## ファイル命名規則

具体的なトピックを反映したファイル名にする。

パターン: `{対象}-{状況や組み合わせ}-{何についてか}.md`
```
# OK
docker-compose-volume-permission-fix.md
react-suspense-tanstack-query-hydration.md
vitest-mock-esm-module-workaround.md

# NG（抽象的すぎる）
docker.md
error.md
config.md
```

---

## Markdown 書式
```markdown
# {タイトル: 具体的な発見内容}

- **発見日**: YYYY-MM-DD
- **タグ**: 関連キーワード（カンマ区切り）

## 状況

何をしようとしていたか、どういう前提条件だったか。

## 問題 / 疑問

何が起きたか、何がわからなかったか。

## 発見 / 解決策

何がわかったか、どう解決したか。

## コード例

（該当する場合、動作確認済みのコードを記載）
```

---

## index.md の形式

カテゴリごとにセクションを作成。`_etc/` のカテゴリも含める。
```markdown
# Findings Index

このプロジェクトで蓄積された技術知見の一覧。

## Docker
- [docker-composeのボリュームパーミッション問題](docker/docker-compose-volume-permission-fix.md)

## Testing
- [Vitestでのモジュールモック](testing/vitest-mock-esm-module-workaround.md)

## _etc/performance
- [N+1クエリの検出と対策](_etc/performance/n-plus-one-query-detection.md)
```

---

## 出力（実行完了時の報告）

棚卸し完了後、以下を報告する：

1. 処理したセッションログのファイル名一覧
2. 抽出した findings の数（カテゴリ別）
3. 作成/更新したファイル一覧
4. 新しく作成した `_etc/` カテゴリがあればその旨
5. 「価値ある発見なし」と判断したログがあればその旨
6. CLAUDE.md / .claude 内の更新提案（該当がある場合）
