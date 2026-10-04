---
name: session-harvest
description: "セッション中の知見を knowledge/buffer ブランチに自動蓄積。マージ前にセッション内で生まれた知識を吸い上げ、専用ブランチ経由で main に反映する。「/session-harvest」「知見を吸い上げて」と言った時に使用。"
---

# 🪺 セッション知見の吸い上げ

> [!IMPORTANT]
> このスキルは **セッション中の会話・差分** から知見を抽出し、`knowledge/buffer` ブランチに自動蓄積する。
> CTO / CPO / CISO / CFO / CLO に一括委任して `.claude/knowledge/` / `.claude/rules/` / `docs/` に追記する。
> 1 session-harvest 実行 = **C*O 最大 5 呼出 + 30K トークン切り詰め** にコストを制限する。
> `ANTHROPIC_API_KEY` 設定時は **従量課金** が発生する（未設定時は Claude Max サブスク利用）。

セッション中の会話から知見を抽出し、CTO / CPO / CISO / CFO / CLO に一括委任して `knowledge/buffer` ブランチ配下の `.claude/knowledge/` / `.claude/rules/` / `docs/` に追記する。

## 💰 コスト前提

| 観点 | 内容 |
|------|------|
| 課金経路 | `ANTHROPIC_API_KEY` 設定時は **従量課金**、未設定なら Claude Max サブスク利用 |
| 実行頻度 | 自動化ループ（`/vibecorp:pr` 経由・`/vibecorp:autopilot` 経由）で呼ばれる頻度が高い |
| コスト制御 | C*O 5 呼出上限 + 30K トークン切り詰めのみ |

## 📖 使用方法

```bash
/vibecorp:session-harvest                    # 現在のセッションの知見を吸い上げ
/vibecorp:session-harvest --worktree <path>  # worktree 内で実行
```

## ⚙️ 環境変数

| 変数 | デフォルト | 用途 |
|---|---|---|
| `VIBECORP_TOKEN_RATIO` | 0.8 | 文字数 → トークン換算係数（日本語混在保守値） |
| `VIBECORP_LOCK_TIMEOUT` | 60 | buffer worktree 排他ロックのタイムアウト（秒） |

## 🔄 ワークフロー

### 1. buffer worktree の準備

書込先は `knowledge/buffer` ブランチの worktree（`~/.cache/vibecorp/buffer-worktree/<repo-id>/`）。

```bash
. "$CLAUDE_PROJECT_DIR/.claude/lib/knowledge_buffer.sh"
knowledge_buffer_ensure || exit 1
knowledge_buffer_lock_acquire || exit 2
trap knowledge_buffer_lock_release EXIT
BUFFER_DIR="$(knowledge_buffer_worktree_dir)"
```

### 2. 変更内容の把握

呼出元の作業ブランチから変更を抽出する（書込先は buffer、取得元は作業ブランチ）。

```bash
# ベースブランチとの差分（PR スコープ）
git diff main...HEAD --name-only

# コミットメッセージ一覧
git log main..HEAD --oneline
```

### 2.5. 差分ゼロの早期終了（コスト保護）

差分も commit も無いセッションは委任対象が存在しないため、5 C\*O 呼出（約 $0.45）を回避するため即終了する。

```bash
if git diff main...HEAD --quiet && [ -z "$(git log main..HEAD --oneline)" ]; then
  echo "[session-harvest] 差分・コミットなし — スキップ" >&2
  exit 0
fi
```

### 3. 吸い上げ対象の判定

セッション中の変更と会話から、以下の知見を抽出対象とする。

| 対象 | セッション内の知見例 | 反映先（buffer worktree 内） |
|---|---|---|
| コーディング規約 | 発見したパターン・アンチパターン、繰り返し指摘された内容 | `${BUFFER_DIR}/.claude/rules/` |
| ナレッジ | デバッグで判明した仕様上の注意点、役割別の判断記録 | `${BUFFER_DIR}/.claude/knowledge/` |
| 設計ドキュメント | 実装中に決まった設計判断、API 設計・アーキテクチャ決定 | `${BUFFER_DIR}/docs/` |

**吸い上げ不要の判定:**

- 変更が軽微（タイポ修正、フォーマット調整のみ）。
- 既に rules / knowledge / docs に反映済み。
- 一過性のデバッグ対応で汎用性がない。

吸い上げ不要と判断した場合はステップ 5 の commit / push へ進む（差分なしなら自動的に skip される）。

### 4. コンテキスト切り詰め + 専門職エージェントに一括委任

**重要**: 各エージェントは `name` を指定した永続 teammate として起動する。起動した `name` はステップ 4.5 で shutdown 対象として参照するため保持しておく。

変更内容と会話差分のトークン数を概算する（`VIBECORP_TOKEN_RATIO` × 文字数、保守値 0.8）。**1 session-harvest 実行 = C*O 最大 5 呼出 + 30K トークン** に制限する。30K 超過時は新しい差分を優先して切り詰め、stderr に「コンテキスト超過のため古い差分を次回に繰越」と通知する。

CTO / CPO / CISO / CFO / CLO の **5 エージェントを並列起動** する（レガシーな順次起動は廃止、ファイル競合は buffer worktree 内の担当ディレクトリ分離で回避）。

各エージェントに以下を渡す:

````text
あなたは {役職名} として、このセッションで生まれた知見を管轄の規約・ナレッジ・ドキュメントに反映してください。

## ⚠️ パス指定ルール（必須・最優先）

書込先パスは **必ず絶対パスで指定** すること。`${BUFFER_DIR}` は呼出元で展開済みの絶対パス（例: `/Users/me/.cache/vibecorp/buffer-worktree/vibecorp-XXXXXXXX`）として渡されている。

### 必須手順（ファイル書込前に毎回実行）

```bash
echo "BUFFER_DIR: ${BUFFER_DIR}"
```

期待出力例（OK）: `BUFFER_DIR: /Users/me/.cache/vibecorp/buffer-worktree/vibecorp-XXXXXXXX`

出力が空 / 相対パス / `/` から始まらない場合は **書込を中止して呼出元に報告** すること。

### 禁止事項

- 相対パスでの書込（例: `vibecorp-XXXXXXXX/.claude/knowledge/...`）
  - これは worktree dir 内に同名サブディレクトリを誤作成し、`git add -A` で commit に混入する事故の原因になる（Issue #559 の主犯）
- `${BUFFER_DIR}` を含まないパス（例: `.claude/knowledge/...` だけで書く）
- 変数展開せずに `$BUFFER_DIR` をそのまま文字列として書込先パスに使うこと

## 書込先（buffer worktree 内）
- CTO のみ: ${BUFFER_DIR}/.claude/rules/
- 全員: ${BUFFER_DIR}/.claude/knowledge/{role}/
- 管轄ドキュメント: ${BUFFER_DIR}/docs/（CPO 等）

## 最初にやること（必須）

管轄の knowledge ディレクトリが存在しない場合は作成する:

```bash
mkdir -p ${BUFFER_DIR}/.claude/knowledge/{role}/
```

## セッションの変更内容
{git diff の概要（切り詰め済み）}

## コミット履歴
{git log の内容}

## 判断基準
各知見について、以下の 4 つから判断すること:

1. **rules/ に追加**: 全エージェントが守るべきルール（CTO のみ）
2. **docs/ に追加**: 設計判断・仕様・MUST/MUST NOT 制約
3. **knowledge/{role}/ に記事として蓄積**: 自分の判断ノウハウ
4. **反映不要**: 一過性の対応、既に反映済み

## 制約
- 管轄ファイルのみ編集（buffer worktree 内限定）
- 既存の記述スタイル・フォーマットを維持する
- 過剰な加筆をしない

## 出力
- 反映したファイルと内容の要約
- 反映不要と判断した知見とその理由
````

### 4.5. 起動エージェントの shutdown

ステップ 4 で起動した全エージェントへ `shutdown_request` を SendMessage で送信し、チームを解散する。

- `name` 付きで起動された teammate は結果返却後も idle 状態でペインを占有し続けるため、**反映結果の成否にかかわらず必ず送信** する。
- teammate 側は `shutdown_response` を返した時点で terminate されるため、メイン側での応答待ちコードは不要。

```json
{"to": "<エージェント名>", "message": {"type": "shutdown_request", "reason": "session-harvest 完了"}}
```

### 5. commit + push

```bash
knowledge_buffer_commit "chore(knowledge): harvest session $(date +%Y-%m-%d)" || true
if ! knowledge_buffer_push; then
  echo "[session-harvest] push 失敗。commit は worktree に保持" >&2
  exit 3
fi
```

差分なしの場合は `knowledge_buffer_commit` が自動 skip（exit 0）。

### 6. 結果報告

```text
## session-harvest 結果

### 反映内容

#### CTO
- ${BUFFER_DIR}/.claude/rules/xxx.md: 「...」を追加
- ${BUFFER_DIR}/.claude/knowledge/cto/yyy.md: ... を記事化

#### CPO
- ${BUFFER_DIR}/docs/specification.md: 設計判断を追記
- ${BUFFER_DIR}/.claude/knowledge/cpo/zzz.md: ... を記事化

### 反映不要と判断した知見
- [タイポ修正] — 一過性の修正のため

### コンテキスト
- 推定トークン: {est_tokens}
- 切り詰め有無: {yes/no}
- 繰越: {繰越差分の概要 or なし}
```

## 🤝 /vibecorp:review-harvest との責務境界

| スキル | 入力 | 反映先 |
|---|---|---|
| `/vibecorp:session-harvest` | セッション中の会話に埋もれた暗黙知（設計判断・パターン・注意点） | `knowledge/buffer` |
| `/vibecorp:review-harvest` | マージ済み PR のレビュー指摘 | `knowledge/buffer` |

両者とも書込先は `knowledge/buffer` ブランチ。main への反映は `/vibecorp:knowledge-pr` が担当する（Issue 起票 → PR 作成 → auto-merge）。

## 🚧 制約

- **書込は buffer worktree 内に限定** — 作業ブランチには一切書き込まない。
- knowledge/ の記事は、既存の記事がある場合は追記する（新規ファイル乱立を防ぐ）。
- rules/ への追加は慎重に行う。全エージェントに影響するため、本当に全員が守るべきルールかを確認する。
- **push 失敗時は exit 3** — commit は worktree に保持したまま終了し、reset ロストを回避する。
- **jq では string interpolation `\(...)` を使わない** — `+` で結合する。
- **コマンドをそのまま実行する** — `2>/dev/null` / `|| echo` / `; echo` 等のリダイレクトやフォールバックを付加しない（明示的にリトライ・タイムアウトが必要な箇所を除く）。
- preset minimal では呼ばれない（install.sh の minimal 引き算で除外）。

## 🔗 関連ルール

- 動作主語ルール: `.claude/rules/communication.md`
- プロンプト作成基準: `.claude/rules/prompt-writing.md`
- マークダウン規約: `.claude/rules/markdown.md`
- シェル規約: `.claude/rules/shell.md`
- 兄弟スキル（PR レビュー指摘収集）: `/vibecorp:review-harvest`
- 反映スキル（buffer → main）: `/vibecorp:knowledge-pr`
