---
name: sync-check
description: >
  コード変更に対する docs/, knowledge/, README.md の整合性チェック（読み取り専用）。
  各職種エージェントを立ち上げ、管轄ファイルのみをチェックさせる。
  push 前に必ず実行される。「/vibecorp:sync-check」「整合性チェック」と言った時に使用。
---

# 🔍 sync-check: 整合性チェック（読み取り専用）

> [!IMPORTANT]
> コード変更と `docs/` / `knowledge/` / `README.md` の整合性を **読み取り専用** で確認する。
> 各職種エージェントに **管轄ファイルのみ** をチェックさせる（編集は一切しない）。
> 総合判定 ✅ のときだけスタンプを発行する。⚠️ / ❌ は `/vibecorp:sync-edit` に橋渡しする。

コード変更に対して `docs/` / `knowledge/` / `README.md` が整合しているかを、各職種エージェントに委任して確認する。本スキルはチェックのみ行い、ファイルの編集は一切しない。

## 🔄 ワークフロー

### 1. 変更内容の把握

```bash
# ベースブランチとの差分（PR スコープ）
git diff main...HEAD --name-only

# 未コミットの変更も含める
git diff --staged --name-only
git diff --name-only
```

### 2. 対象外の判定

以下のケースは整合性チェック不要。エージェント起動をスキップしてステップ 6 のスタンプ発行に進む。

- `docs/` や `knowledge/` や `README.md` のみの変更（コードとの整合問題が発生しない）
- `.gitignore` 等の軽微な変更のみ

### 3. 担当エージェントの起動

変更内容に基づき、関連する職種のエージェントを **Agent ツールで並列起動** する。各エージェントは **自分の管轄ファイルだけ** を読み取りチェックする。

#### プリセット検出

`.claude/vibecorp.yml` から `preset` を取得する。

```bash
awk '/^preset:/ { sub(/^preset:[[:space:]]*/, ""); print; exit }' .claude/vibecorp.yml
```

- `minimal` / `standard` → デフォルト（CTO / CPO のみ）
- `full` → デフォルト + 差分キーワードにヒットした C*O を自動起動

#### デフォルト管轄（全プリセット共通）

CTO / CPO は常時起動する。

| エージェント | 管轄ファイル | 起動条件 |
|-------------|------------|---------|
| CTO | `docs/` 内の技術設計ドキュメント、`knowledge/cto/` | アーキテクチャ・技術設計・エージェント定義・hooks・スキル関連の変更 |
| CPO | `docs/specification.md`、`knowledge/cpo/`、`README.md` | 仕様・UI・プロンプト・スキル・フック・エージェント・README 関連の変更 |

#### full プリセット時の自動起動

`preset: full` の場合、以下のトリガー表に従い `git diff main...HEAD -U0` に対してキーワード検出する。ヒットした領域の C*O を CTO / CPO に **加えて** 並列起動する（Phase 3 `/vibecorp:review-loop` と同一のトリガー表）。

| 領域 | diff 内キーワード | 起動 C*O | 管轄ファイル |
|---|---|---|---|
| 課金影響 | `API call`, `model:`, `claude -p`, `ANTHROPIC_API_KEY`, `rate limit`, `従量`, `トークン消費`, `npx`, `bunx` | CFO | `docs/cost-analysis.md`, `knowledge/accounting/` |
| セキュリティ | `auth`, `token`, `secret`, `encrypt`, `permission`, `credential`, `curl`, `wget`, `eval`, `exec` | CISO | `docs/SECURITY.md`, `knowledge/security/` |
| 法務 | `dependency`, `LICENSE`, `third-party`, `規約`, `プライバシー`, `第三者`, `package.json`, `requirements.txt`, `go.mod` | CLO | `docs/POLICY.md`, `knowledge/legal/` |
| 組織運営 | `.claude/agents/`, `.claude/hooks/`, `.claude/rules/`, `.claude/skills/` | SM | `docs/ai-organization.md`, `knowledge/sm/` |

検出コマンド例（課金領域）:

```bash
git diff main...HEAD -U0 | grep -iE 'API call|model:|claude -p|ANTHROPIC_API_KEY|rate limit|従量|トークン消費|npx|bunx'
```

該当した領域のみ起動する（複数ヒット時は該当全 C*O を並列）。`standard` / `minimal` プリセットでは C*O の自動起動は行わない（既存挙動を維持）。

#### 起動方法

各エージェントは `name` を指定した永続 teammate として起動する。結果返却後も idle で残るため、ステップ 5 で必ず shutdown する。起動した `name` はステップ 5 で参照するため全て保持する。

各エージェントに以下を渡して Agent ツールで起動する。プロンプトは `skills/sync-check/prompts/agent-call-cxo-sync-check.md` を参照する。

### 4. 結果の統合・レポート出力

全エージェントの結果を統合し、以下のフォーマットで出力する。

```text
## sync-check 結果

### 変更ファイル
- {変更ファイル一覧}

### チェック結果

#### CTO（技術設計）
- docs/design-philosophy.md: ✅ OK
- knowledge/cto/decisions.md: ⚠️ 要更新 — {詳細}

#### CPO（プロダクト）
- docs/specification.md: ✅ OK

#### CFO / CISO / CLO / SM（full プリセットかつキーワードヒット時のみ）
- docs/cost-analysis.md: ✅ OK
- docs/SECURITY.md: ✅ OK
- docs/POLICY.md: ✅ OK
- docs/ai-organization.md: ✅ OK

### 総合判定
- ✅ 問題なし → push してよい
- ⚠️ 要更新あり → /vibecorp:sync-edit を実行してください
- ❌ 矛盾あり → /vibecorp:sync-edit を実行してください
```

### 5. 起動エージェントの shutdown

ステップ 3 で起動した全エージェントへ `shutdown_request` を SendMessage で送信し、チームを解散する。`name` 付きで起動された teammate は結果を返却した後も idle 状態でペインを占有し続けるため、**総合判定（✅ / ⚠️ / ❌）にかかわらず必ず送信する**。

```json
{"to": "<エージェント名>", "message": {"type": "shutdown_request", "reason": "sync-check 完了"}}
```

- 起動した全エージェントに対して 1 件ずつ送信する（同一メッセージで並列送信して構わない）
- teammate 側は `shutdown_response` を返した時点で terminate されるため、メイン側での応答待ちコードは不要
- ステップ 2 で整合性チェックをスキップした場合（エージェント未起動）は、本ステップをスキップしてステップ 6 へ進む

### 6. スタンプ発行

**総合判定が ✅ の場合のみ** スタンプを発行する。スタンプは `~/.cache/vibecorp/state/<repo-id>/` 配下に作成され、`.claude/` 配下への書込確認プロンプトを回避する。

```bash
. "$CLAUDE_PROJECT_DIR/.claude/lib/common.sh"
STAMP_DIR="$(vibecorp_stamp_mkdir)"
touch "${STAMP_DIR}/sync-ok"
```

⚠️ または ❌ がある場合はスタンプを発行しない。`/vibecorp:sync-edit` による修正後、再度 `/vibecorp:sync-check` を実行する。

## 🧭 判定基準

- **❌ 矛盾**: コードとドキュメントが明確に食い違っている。
- **⚠️ 要更新**: コード変更がドキュメントに反映されていない。
- **✅ OK**: 整合性に問題なし。

## 🚧 制約

- **jq では string interpolation `\(...)` を使わない** — Bash 上で `\` がエスケープ文字、`()` がサブシェルとして解釈され、意図しない展開やパースエラーを引き起こすため。必ず `+` で結合する。
- **コマンドをそのまま実行する** — `2>/dev/null`、`|| echo`、`; echo` 等のリダイレクトやフォールバックを付加しない（[根拠](docs/design-philosophy.md#コマンドリダイレクトフォールバックの禁止)）。
