---
name: prompts-extract-all
description: "skills/**/SKILL.md 内に embed された 5 行以上のエージェント呼出プロンプトテンプレ・長文ブロックを .claude/rules/notification-prompt-extraction.md 基準で skills/<skill>/prompts/<name>.md に切り出す migration skill。「/prompts-extract-all」「プロンプト切り出し」「プロンプト extract」「SKILL.md プロンプト migration」と言った時に使用。検出は awk でフェンスコードブロックを抽出して行数カウント、要否判定は LLM が閾値・用途軸・命名規約と照合。diff 提案 → CEO 承認 → 書換の 2 段階で挙動を壊さず適用する。自動マージ禁止、自律ループ対象外。"
---

# 🤖 プロンプト切り出し migration スキル

> [!IMPORTANT]
> 本スキルは `skills/**/SKILL.md` に embed された **エージェント呼出プロンプトテンプレ** を `.claude/rules/notification-prompt-extraction.md` 基準で個別 `.md` ファイルに切り出す。
> diff 提案 → CEO 承認 → 書換の 2 段階を必須とする。自動マージは禁止。
> 本スキルは自律改善ループの自動実行対象外（`.claude/rules/autonomous-restrictions.md` 不可領域 4 該当）。

## 🎯 対象範囲

本スキルが切り出し提案の対象とするファイル種別は以下とする。

| 種別 | パス | 切り出し対象 |
|------|------|------------|
| ⚙️ スキル本体 | `skills/**/SKILL.md` | ` ```text ` / ` ```markdown ` フェンスブロック内のエージェント呼出プロンプトテンプレ・長文 |

切り出し先（`notification-prompt-extraction.md` の規定パス）:

| 由来 | 切り出し先 |
|------|----------|
| スキル本体 | `skills/<skill>/prompts/<name>.md` |

### 対象外

- `.github/workflows/**` の通知文 → 兄弟スキル `/notifications-extract-all` の管轄
- `hooks/**/*.sh` の通知文 → 同上（`/notifications-extract-all`）
- `.claude/agents/*.md` / `.claude/rules/*.md` → `/prompts-rewrite-all`（書き直し系、切り出しではない）
- 短いコードブロック（行数閾値未満かつ用途軸非該当）
- frontmatter / 章立て見出し内のフェンスコードブロック（構造要素）

## 📝 使用方法

```bash
/prompts-extract-all
/prompts-extract-all --skill <skill-name>
```

- `--skill` 未指定なら `skills/**/SKILL.md` を順次処理する
- 1 ファイル単位で diff 提案 → CEO 承認 → 書き換えを繰り返す

## 🧭 8 段階動線

本スキルは以下 8 段階を順に進める。各段は前段の出力を受け取り次段へ渡す。

| ステップ | 名称 | 役割 |
|---------|------|------|
| 1️⃣ | **列挙** | 対象ファイルを収集する |
| 2️⃣ | **照合** | 基準と機械的に突き合わせる |
| 3️⃣ | **委譲** | CTO Agent を呼び出す |
| 4️⃣ | **提案** | diff を CEO に提示する |
| 5️⃣ | **承認** | CEO の判断を待つ |
| 6️⃣ | **書換** | 承認分のみファイルに反映する |
| 7️⃣ | **配布版同期** | ローカル配布版スナップショットを同期する |
| 8️⃣ | **レポート** | 結果を CEO 向けに整形する |

### 1️⃣ 列挙: 対象ファイル収集

```bash
find skills -name 'SKILL.md' -type f -print
```

- ファイル一覧を保持してステップ 2 へ渡す
- 隠しファイル・サブディレクトリ配下のテキストは対象外

### 2️⃣ 照合: 基準との機械的突き合わせ

各 SKILL.md 内のフェンスコードブロックを awk で抽出する。

| 抽出対象 | パターン | 行数カウント |
|---------|--------|------------|
| `text` フェンス | ` ```text ` で開いて ` ``` ` で閉じる | 開閉行除く実行内容行数 |
| `markdown` フェンス | ` ```markdown ` で開いて ` ``` ` で閉じる | 同上 |

抽出した候補に対し、`notification-prompt-extraction.md` の **指針 MUST 全項目** と **禁止パターン全項目** を 1 件ずつ突き合わせる。

- 照合対象の項目本体は `.claude/rules/notification-prompt-extraction.md` が Single Source of Truth
- 指針 / 禁止の項目本体は基準ルールに閉じる（スキル側で項目を重複列挙しない）
- 行数軸（プロンプト 5 行以上）と用途軸（エージェント呼出 / 再利用定型文）の OR で判定する
- 各候補に「該当する基準項目（閾値 / 用途軸 / 除外）」と「該当行番号」を表で記録する
- 検出結果が空のファイルはステップ 3 以降の対象から外す

### 3️⃣ 委譲: CTO Agent 呼出

プロンプトテンプレはエージェント呼出（技術的判断の伝達手段）であり **CTO** に委譲する。

Agent ツールで CTO を起動し、以下のプロンプト要素を含める。

- 対象 SKILL.md と抽出されたプロンプトテンプレ候補（行番号付き）
- ステップ 2 の照合結果（該当した閾値・用途軸・除外条件）
- 適用基準 (`.claude/rules/notification-prompt-extraction.md` / `.claude/rules/prompt-writing.md` / `.claude/rules/markdown.md`)
- 制約: プロンプト文面の意味改変禁止、切り出し前後で厳密一致（whitespace 含む）、規定パス・命名規約（`agent-call-` プレフィックス + kebab-case）遵守
- 出力フォーマット: 切り出し先パス候補・命名・diff 形式の対比表・判断根拠

CTO は複数並列で起動してよい（各 CTO は別 SKILL.md を扱うため競合しない）。

### 4️⃣ 提案: diff を CEO に提示

ステップ 3 で集めた書き換え案をファイル単位の diff として整形し、以下を明示する。

- ✅ **適用候補**: 基準逸脱を解消する切り出し
- ⚠️ **要判断**: 用途軸 vs 行数軸が拮抗する候補（短いが再利用される定型文等）
- 📍 **根拠**: 該当する閾値・用途軸・命名規約の引用
- 🛡️ **不可領域確認**: `skills/**` を書き換える操作なので CEO 明示承認が必須であることを毎回明示する

提示は **ファイル単位** にまとめる。CEO の指示で「まとめて見る」と言われた場合のみ複数ファイル同時提示に切り替える。

### 5️⃣ 承認: CEO 判断を待つ

CEO に以下の選択肢を提示する。

| 選択肢 | 効果 |
|--------|------|
| ✅ **全採用** | 提示した diff を全て切り出し対象に取る |
| 🔢 **項目選択** | 採用したい項目の番号を指定する |
| ⏭️ **スキップ** | この SKILL.md の切り出しを保留する |
| ✋ **中止** | スキル全体を中止する |

CEO 承認なしに本体ファイルを書き換えない。`AskUserQuestion` ツールで選択肢を明示提示してもよい。

### 6️⃣ 書換: 承認分のみファイル反映 + 挙動不変性検証

ステップ 5 で承認された項目のみ反映する。手順は以下。

1. 切り出し先 `skills/<skill>/prompts/<name>.md` を `Write` で新規作成（フェンス内のテキスト本体をそのまま配置）
2. 元 SKILL.md を `Edit` で書き換え（フェンスブロックを「以下のプロンプトは `skills/<skill>/prompts/<name>.md` を参照」のような相対パス記述に置き換える）
3. **挙動不変性検証（必須、2 層）**:
   - 文字列層: 切り出し先 `.md` の中身と元のフェンス内容を `diff -q` または `cmp -s` で **whitespace 含めて厳密一致** することを確認
   - テスト層: `bash tests/test_*.sh` を全件走らせ、通過することを確認（特に `test_*_skill.sh` 系の構造テスト）
4. 破壊が出た場合はその場で書き換えをロールバックし、CEO に報告する

書き換えは **ファイル単位の commit** で行う（後追いで diff を追跡できるように）。

### 7️⃣ 配布版同期チェック

書き換えた本体に対応するローカル配布版スナップショット（`.claude/vibecorp-base/skills/`）があれば同内容で同期する。

- 配布版は `install.sh` が生成するローカルスナップショット（`.claude/.gitignore` で除外）
- 配布版が存在しない場合は同期不要（CI / fresh clone では未生成）
- 切り出し先 `skills/<skill>/prompts/<name>.md` 自体も含めて同期する（snapshot 内に prompts ディレクトリを作る）
- 差分が残ったら CEO に再提示する

### 8️⃣ レポート: CEO 向け結果整形

`.claude/rules/communication.md` の 30 秒ルール（一覧性・状態絵文字で変化が一目で掴める）を満たすレポートを返す。

```text
## /prompts-extract-all レポート

- ✅ 対象 SKILL.md 数: N
- ✅ 切り出し提案: M
- ✅ CEO 承認: A
- ✅ 切り出し完了: A
- ✅ 配布版同期: B
- ⚠️ スキップ: S
- 📐 行数閾値該当: P 件 / 用途軸該当: Q 件
- ✅ 挙動不変性検証: 文字列厳密一致 全件 PASS / テスト全件 PASS
```

状態絵文字の選び方:

- ✅: 全件成功 / 完了している
- ⚠️: 一部スキップ / 警告あり（スキップ件数が 0 でないなど）
- ❌: 失敗・却下が発生した（テスト破壊・CEO 却下など）

## 🚧 除外ルール（MUST）

以下は **絶対に切り出さない**。

| 除外対象 | 理由 |
|---------|------|
| 短いプロンプト（5 行未満かつ用途軸非該当） | `notification-prompt-extraction.md` の閾値で除外 |
| 動的生成プロンプト（変数展開を多量に含む） | 実行時に値を埋め込む文面はテンプレ化が難しい |
| 文脈依存で意味が変わる短文 | 周辺コードと一体で意味を成すもの |
| 構造要素（章立て見出しの直下にあるサンプル） | embed が読み手の理解を助ける場合 |
| frontmatter 内のフェンスブロック | 構造要素、切り出し対象外 |

ステップ 2 の照合フェーズで除外検出を必ず実行し、ステップ 4 の提案で除外判定の根拠を明示する。

## 🛡️ 自律ループ対象外宣言

本スキルは以下の理由により `.claude/rules/autonomous-restrictions.md` の **不可領域 4（ガードレール: `skills/**`）** に該当する。

- `skills/**` 配下の SKILL.md を書き換える（スキル定義はエージェント行動制御の中核）

そのため:

- 自律改善ループ（`/vibecorp:diagnose` → `/vibecorp:autopilot` → `/vibecorp:ship-parallel`）の自動実行対象外
- `diagnose-active` スタンプ中は `diagnose-guard.sh` のデフォルト deny で実行不可
- CEO 明示起動時のみ動作
- 自動マージ禁止（ステップ 5 の CEO 承認ゲート必須）

## 🤝 委譲先エージェント

| エージェント | 専門領域 | 本スキルでの担当 |
|-------------|---------|----------------|
| `cto` | 技術・アーキテクチャ | プロンプトテンプレの切り出し提案（エージェント呼出は技術的判断の伝達手段） |

CTO は **管轄ファイルのみ** 切り出し提案する。

## ✅ 指針（MUST）

本スキル固有の指針のみを定義する。切り出し基準そのものは `.claude/rules/notification-prompt-extraction.md` を Single Source of Truth として参照する。

1. 📐 **行数軸 + 用途軸の OR で判定する**
   - 5 行以上のプロンプト OR エージェント呼出 OR 再利用定型文 → 切り出し対象
   - 行数閾値だけで機械的に切り出すと「短いが再利用される定型文」を見落とすため、LLM 判断を必ず挟む

2. 🛑 **diff 提案 → CEO 承認 → 書換の 2 段階を守る**
   - CEO 承認なしに本体ファイルを書き換えない
   - 自動マージは禁止する

3. 🔍 **挙動不変性検証（文字列厳密一致 + テスト全件通過）を必ず実行する**
   - 切り出し前後で whitespace 含めて厳密一致することを確認
   - 書き換え後に `bash tests/test_*.sh` 全件を走らせ通過させる
   - 破壊が出たらロールバックして CEO に報告

4. 📦 **ローカル配布版スナップショットを同期する**
   - `.claude/vibecorp-base/skills/` 配下に対応ファイルがあれば同内容で同期する
   - 切り出し先 `prompts/<name>.md` も snapshot 内に同期する
   - 未配置なら同期不要（CI / fresh clone では未生成）

5. 🛡️ **自律ループ対象外宣言を尊重する**
   - 本スキルは自律実行の対象外、CEO 明示起動時のみ動作する

## ❌ 禁止パターン

本スキル固有の禁止のみを定義する。切り出し基準の禁止パターンは `notification-prompt-extraction.md` を参照する。

- ❌ **行数閾値だけで機械的に切り出す**
  - 短いが再利用される定型文を見落とす、LLM 判断を必ず挟む
- ❌ **CEO 承認なしにファイルを書き換える**
  - 自動マージ禁止に違反する
- ❌ **挙動不変性検証をスキップして commit する**
  - プロンプト文面が変わるとエージェント挙動が変わる
- ❌ **動的展開を多量に含むプロンプトを機械的に切り出す**
  - テンプレ化困難で逆に追跡コストが上がる
- ❌ **自律ループから起動する**
  - 不可領域 4 に該当する skill であり、CEO 明示起動時のみ動作する

## 🔗 関連

- 切り出し基準（Single Source of Truth）: `.claude/rules/notification-prompt-extraction.md`
- プロンプト書き方基準: `.claude/rules/prompt-writing.md`
- 動作主語ルール: `.claude/rules/communication.md`
- マークダウン規約: `.claude/rules/markdown.md`
- shell 規約: `.claude/rules/shell.md`
- 自律実行不可領域（人間承認必須）: `.claude/rules/autonomous-restrictions.md`
- 兄弟スキル（通知文切り出し）: `/notifications-extract-all`
- 類似多段動線スキル: `/docs-rewrite-all` / `/prompts-rewrite-all`
- 親エピック: Issue #636
