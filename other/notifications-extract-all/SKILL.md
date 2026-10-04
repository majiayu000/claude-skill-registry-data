---
name: notifications-extract-all
description: ".github/workflows/**/*.{yml,yaml} の --body 通知文と hooks/**/*.sh の長文 echo/printf/heredoc を .claude/rules/notification-prompt-extraction.md 基準で個別 .md ファイルに切り出す migration skill。「/notifications-extract-all」「通知文切り出し」「通知文 extract」「workflow 通知 migration」と言った時に使用。検出は grep で機械絞り込み、要否判定は LLM が閾値・命名規約と照合。diff 提案 → CEO 承認 → 書換の 2 段階で挙動を壊さず適用する。自動マージ禁止、自律ループ対象外。"
---

# 🤖 通知文切り出し migration スキル

> [!IMPORTANT]
> 本スキルは `.github/workflows/**` と `hooks/**` に embed された **CEO 向け通知文** を `.claude/rules/notification-prompt-extraction.md` 基準で個別 `.md` ファイルに切り出す。
> diff 提案 → CEO 承認 → 書換の 2 段階を必須とする。自動マージは禁止。
> 本スキルは自律改善ループの自動実行対象外（`.claude/rules/autonomous-restrictions.md` 不可領域 4 / 6 該当）。

## 🎯 対象範囲

本スキルが切り出し提案の対象とするファイル種別は以下とする。

| 種別 | パス | 切り出し対象 |
|------|------|------------|
| 🤖 GHA workflow | `.github/workflows/**/*.yml`, `.github/workflows/**/*.yaml` | `gh issue comment --body "..."` / `gh pr comment --body "..."` / `actions/github-script` の `script:` 等 |
| 🪝 hook シェル | `hooks/**/*.sh` | `echo` / `printf` / `cat <<EOF` で出力する CEO 向けエラー・警告文 |

切り出し先（`notification-prompt-extraction.md` の規定パス）:

| 由来 | 切り出し先 |
|------|----------|
| GHA workflow | `.github/workflows/messages/<name>.md` |
| hook シェル | `hooks/messages/<name>.md` |

### 対象外

- `skills/**/SKILL.md` のプロンプトテンプレ → 兄弟スキル `/prompts-extract-all` の管轄
- `docs/` 配下の純粋なドキュメント → `/docs-rewrite-all`
- コード内コメント
- 動的生成文（実行時に値を埋め込む 1〜2 行）

## 📝 使用方法

```bash
/notifications-extract-all
/notifications-extract-all --target workflows
/notifications-extract-all --target hooks
```

- `--target` 未指定なら workflow / hook を順次処理する
- 1 ファイル単位で diff 提案 → CEO 承認 → 書き換えを繰り返す

## 🧭 8 段階動線

本スキルは以下 8 段階を順に進める。各段は前段の出力を受け取り次段へ渡す。

| ステップ | 名称 | 役割 |
|---------|------|------|
| 1️⃣ | **列挙** | 対象ファイルを収集する |
| 2️⃣ | **照合** | 基準と機械的に突き合わせる |
| 3️⃣ | **委譲** | CISO Agent を呼び出す |
| 4️⃣ | **提案** | diff を CEO に提示する |
| 5️⃣ | **承認** | CEO の判断を待つ |
| 6️⃣ | **書換** | 承認分のみファイルに反映する |
| 7️⃣ | **配布版同期** | ローカル配布版スナップショットを同期する |
| 8️⃣ | **レポート** | 結果を CEO 向けに整形する |

### 1️⃣ 列挙: 対象ファイル収集

```bash
find .github/workflows -type f \( -name '*.yml' -o -name '*.yaml' \) -print
find hooks -type f -name '*.sh' -print
```

- ファイル一覧を保持してステップ 2 へ渡す
- 隠しファイル・除外ディレクトリ（`node_modules`, `vendor` 等）は対象外

### 2️⃣ 照合: 基準との機械的突き合わせ

各ファイル内の通知文候補を以下のパターンで grep / awk 抽出する。

| 由来 | 抽出パターン |
|------|------------|
| GHA workflow | `--body "..."`、`script:` ブロック、heredoc（`<<EOF` / `<<-EOF`） |
| hook シェル | `echo "..."` / `printf "..."` / `cat <<EOF`（連続行） |

抽出した候補に対し、`notification-prompt-extraction.md` の **指針 MUST 全項目** と **禁止パターン全項目** を 1 件ずつ突き合わせる。

- 照合対象の項目本体は `.claude/rules/notification-prompt-extraction.md` が Single Source of Truth
- 指針 / 禁止の項目本体は基準ルールに閉じる（スキル側で項目を重複列挙しない）
- 各候補に「該当する基準項目（閾値 / 用途軸 / 除外）」と「該当行番号」を表で記録する
- 検出結果が空のファイルはステップ 3 以降の対象から外す

### 3️⃣ 委譲: CISO Agent 呼出

通知文は CEO が GitHub UI で読む文面であり、情報露出経路を含むため **CISO** に委譲する。

Agent ツールで CISO を起動し、以下のプロンプト要素を含める。

- 対象ファイルと抽出された通知文候補（行番号付き）
- ステップ 2 の照合結果（該当した閾値・用途軸・除外条件）
- 適用基準 (`.claude/rules/notification-prompt-extraction.md` / `.claude/rules/communication.md` / `.claude/rules/markdown.md`)
- 制約: 文面の意味改変禁止、切り出し前後で厳密一致（whitespace 含む）、規定パス・命名規約遵守
- 出力フォーマット: 切り出し先パス候補・命名・diff 形式の対比表・判断根拠

CISO は複数並列で起動してよい（各 CISO は別ファイルを扱うため競合しない）。

### 4️⃣ 提案: diff を CEO に提示

ステップ 3 で集めた書き換え案をファイル単位の diff として整形し、以下を明示する。

- ✅ **適用候補**: 基準逸脱を解消する切り出し
- ⚠️ **要判断**: 用途軸 vs 行数軸が拮抗する候補
- 📍 **根拠**: 該当する閾値・用途軸・命名規約の引用
- 🔒 **除外確認**: `permissions:` / `secrets:` セクションを巻き込んでいないこと

提示は **ファイル単位** にまとめる。CEO の指示で「まとめて見る」と言われた場合のみ複数ファイル同時提示に切り替える。

### 5️⃣ 承認: CEO 判断を待つ

CEO に以下の選択肢を提示する。

| 選択肢 | 効果 |
|--------|------|
| ✅ **全採用** | 提示した diff を全て切り出し対象に取る |
| 🔢 **項目選択** | 採用したい項目の番号を指定する |
| ⏭️ **スキップ** | このファイルの切り出しを保留する |
| ✋ **中止** | スキル全体を中止する |

CEO 承認なしに本体ファイルを書き換えない。`AskUserQuestion` ツールで選択肢を明示提示してもよい。

### 6️⃣ 書換: 承認分のみファイル反映 + 挙動不変性検証

ステップ 5 で承認された項目のみ反映する。手順は以下。

1. 切り出し先 `.md` ファイルを `Write` で新規作成（通知文本体をそのまま配置）
2. 元ファイルを `Edit` で書き換え（`--body "..."` → `--body-file <path>`、`echo "..."` → `cat "${SCRIPT_DIR}/messages/<name>.md"`）
3. **挙動不変性検証（必須、2 層）**:
   - 文字列層: 切り出し先 `.md` の中身と元の通知文を `diff -q` または `cmp -s` で **whitespace 含めて厳密一致** することを確認
   - テスト層: `bash tests/test_*.sh` を全件走らせ、通過することを確認
4. 破壊が出た場合はその場で書き換えをロールバックし、CEO に報告する

書き換えは **ファイル単位の commit** で行う（後追いで diff を追跡できるように）。

> [!NOTE]
> workflow yaml の実 CI 動作確認はローカル不能。SKILL.md の本動線では文字列厳密一致 + テスト全件通過までを担保し、push 後の CI 結果は CEO がレビューする運用とする。

### 7️⃣ 配布版同期チェック

書き換えた本体に対応するローカル配布版スナップショット（`.claude/vibecorp-base/`）があれば同内容で同期する。

- 配布版は `install.sh` が生成するローカルスナップショット（`.claude/.gitignore` で除外）
- 配布版が存在しない種別は同期不要（CI / fresh clone では未生成）
- 差分が残ったら CEO に再提示する
- 切り出し先 `.md` 自体は `templates/claude/` 配下に同期する経路は持たない（vibecorp プラグインの skills/hooks は `skills/` / `hooks/` ディレクトリそのものが配布元）

### 8️⃣ レポート: CEO 向け結果整形

`.claude/rules/communication.md` の 30 秒ルール（一覧性・状態絵文字で変化が一目で掴める）を満たすレポートを返す。

```text
## /notifications-extract-all レポート

- ✅ 対象ファイル数: N
- ✅ 切り出し提案: M
- ✅ CEO 承認: A
- ✅ 切り出し完了: A
- ✅ 配布版同期: B
- ⚠️ スキップ: S
- 🔒 除外保護（permissions/secrets）: 検出 K 件、全て除外維持
- ✅ 挙動不変性検証: 文字列厳密一致 全件 PASS / テスト全件 PASS
```

状態絵文字の選び方:

- ✅: 全件成功 / 完了している
- ⚠️: 一部スキップ / 警告あり（スキップ件数が 0 でないなど）
- ❌: 失敗・却下が発生した（テスト破壊・CEO 却下など）

## 🚧 除外ルール（MUST）

以下は **絶対に切り出さない**（巻き込み禁止）。

| 除外対象 | 理由 |
|---------|------|
| `permissions:` セクション | `autonomous-restrictions.md` 不可領域 6（CI エージェント） |
| `secrets:` セクション | 同上 |
| `$'...'`（ANSI-C クォート） | 機械検出困難、初版スコープ外 |
| `$(cat ...)` / `$(echo ...)` 動的展開 | 文脈依存で意味が変わる |
| 短い通知文（閾値以下） | `notification-prompt-extraction.md` の閾値で除外 |
| エージェントログ・デバッグ出力 | CEO 向けではない開発者向け出力（`>&2` リダイレクト等） |

ステップ 2 の照合フェーズで除外検出を必ず実行し、ステップ 4 の提案で「🔒 除外確認」を明示する。

## 🛡️ 自律ループ対象外宣言

本スキルは以下の理由により `.claude/rules/autonomous-restrictions.md` の **不可領域 4（ガードレール: `skills/**`）** と **不可領域 6（CI エージェント: `.github/workflows/**`）** に該当する。

- `.github/workflows/**` 配下の yaml を書き換える（不可領域 6）
- `hooks/**` 配下のシェルを書き換える（ガードレール周辺）

そのため:

- 自律改善ループ（`/vibecorp:diagnose` → `/vibecorp:autopilot` → `/vibecorp:ship-parallel`）の自動実行対象外
- `diagnose-active` スタンプ中は `diagnose-guard.sh` のデフォルト deny で実行不可
- CEO 明示起動時のみ動作
- 自動マージ禁止（ステップ 5 の CEO 承認ゲート必須）

## 🤝 委譲先エージェント

| エージェント | 専門領域 | 本スキルでの担当 |
|-------------|---------|----------------|
| `ciso` | セキュリティ・情報露出 | 通知文の切り出し提案（CEO 向け文面、情報露出経路を含むため） |

CISO は **管轄ファイルのみ** 切り出し提案する。

## ✅ 指針（MUST）

本スキル固有の指針のみを定義する。切り出し基準そのものは `.claude/rules/notification-prompt-extraction.md` を Single Source of Truth として参照する。

1. 🔒 **除外ルールを必ず先に確認する**
   - `permissions:` / `secrets:` / `$'...'` / `$(cat ...)` / 動的展開 / 短文を巻き込まない
   - ステップ 2 の照合で除外検出を実行し、ステップ 4 で「🔒 除外確認」を明示する

2. 🛑 **diff 提案 → CEO 承認 → 書換の 2 段階を守る**
   - CEO 承認なしに本体ファイルを書き換えない
   - 自動マージは禁止する

3. 🔍 **挙動不変性検証（文字列厳密一致 + テスト全件通過）を必ず実行する**
   - 切り出し前後で whitespace 含めて厳密一致することを確認
   - 書き換え後に `bash tests/test_*.sh` 全件を走らせ通過させる
   - 破壊が出たらロールバックして CEO に報告

4. 📦 **ローカル配布版スナップショットを同期する**
   - `.claude/vibecorp-base/` 配下に対応ファイルがあれば同内容で同期する
   - 未配置なら同期不要（CI / fresh clone では未生成）

5. 🛡️ **自律ループ対象外宣言を尊重する**
   - 本スキルは自律実行の対象外、CEO 明示起動時のみ動作する

## ❌ 禁止パターン

本スキル固有の禁止のみを定義する。切り出し基準の禁止パターンは `notification-prompt-extraction.md` を参照する。

- ❌ **`permissions:` / `secrets:` セクションに踏み込む**
  - `autonomous-restrictions.md` 不可領域 6 違反、最大の攻撃経路を開く
- ❌ **CEO 承認なしにファイルを書き換える**
  - 自動マージ禁止に違反する
- ❌ **挙動不変性検証をスキップして commit する**
  - 通知文面が変わる事故を見逃す
- ❌ **動的展開（`$(cat ...)` / `$(echo ...)`）を機械的に切り出す**
  - 文脈依存で意味が変わる、初版スコープ外
- ❌ **自律ループから起動する**
  - 不可領域 4 / 6 に該当する skill であり、CEO 明示起動時のみ動作する

## 🔗 関連

- 切り出し基準（Single Source of Truth）: `.claude/rules/notification-prompt-extraction.md`
- 動作主語ルール: `.claude/rules/communication.md`
- マークダウン規約: `.claude/rules/markdown.md`
- shell 規約: `.claude/rules/shell.md`
- 自律実行不可領域（人間承認必須）: `.claude/rules/autonomous-restrictions.md`
- 兄弟スキル（プロンプト切り出し）: `/prompts-extract-all`
- 類似多段動線スキル: `/docs-rewrite-all` / `/prompts-rewrite-all`
- 親エピック: Issue #636
