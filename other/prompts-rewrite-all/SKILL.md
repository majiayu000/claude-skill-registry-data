---
name: prompts-rewrite-all
description: "skills/**/SKILL.md・agents/*.md・.claude/rules/*.md を .claude/rules/prompt-writing.md 基準で一括書き直し提案するスキル。「/prompts-rewrite-all」「プロンプト書き直し」「スキル一括書き直し」「エージェント書き直し」と言った時に使用。claude-code-guide サブエージェントで Claude Code 公式仕様（docs.claude.com）を確認し、prompt-writing.md の指針 MUST / 禁止パターンと照合する。diff 提案 → CEO 承認 → 書き換えの 2 段階で挙動を壊さず適用する。自動マージ禁止。"
---

# 🤖 プロンプト一括書き直しスキル

> [!IMPORTANT]
> 本スキルは `.claude/rules/prompt-writing.md` 基準で LLM 向けプロンプト群を一括書き直しする。
> 書き直し前に必ず `claude-code-guide` サブエージェントで Claude Code 公式仕様（`docs.claude.com`）を確認する。
> diff 提案 → CEO 承認 → 書き換えの 2 段階を必須とする。自動マージは禁止。

## 🎯 対象範囲

本スキルが書き直しの対象とするファイルは以下とする。

| 種別 | パス |
|------|------|
| ⚙️ スキル | `skills/**/SKILL.md` |
| 🤝 エージェント | `agents/*.md` |
| 📜 ルール | `.claude/rules/*.md` |

本体の書き換えに応じて、プロジェクト固有の配布版があれば同期チェックする（例: vibecorp での運用は後述）。

### 対象外

- YAML / TOML 等の `.md` 以外のプロンプトファイル
- README.md・docs/ 配下の純粋なドキュメント（→ `/docs-rewrite-all`）
- コード内コメント

## 📝 使用方法

```bash
/prompts-rewrite-all
/prompts-rewrite-all --target skills
/prompts-rewrite-all --target agents
/prompts-rewrite-all --target rules
```

- `--target` 未指定なら 3 種別を順次処理する
- 1 ファイル単位で diff 提案 → CEO 承認 → 書き換えを繰り返す

## 🔁 ワークフロー

### 1. 対象ファイル列挙

3 種別の対象を列挙する。

```bash
find skills -name 'SKILL.md' -type f
find agents -maxdepth 1 -name '*.md' -type f
find .claude/rules -maxdepth 1 -name '*.md' -type f
```

- 隠しファイルやサブディレクトリ配下は対象外
- プロジェクト固有の配布版がある場合は本体書き換え後にステップ 8 で同期する（例: vibecorp での運用は後述）

### 2. 基準ファイル特定

基準ファイルは以下 2 本とする。

| 基準 | 照合対象 |
|------|---------|
| `.claude/rules/prompt-writing.md` | プロンプト本文（行動主語・トリガー語句・frontmatter 等） |
| `.claude/rules/comment-writing.md` | プロンプト md 内に登場する GitHub コメント例（Issue/PR テンプレ例・レビュー例・Bot 通知例） |

- 照合観点（指針 MUST / 禁止パターン）は各基準ルール本体が Single Source of Truth。
- スキル側で照合項目を重複定義しない。
- プロンプト本文と md 内コメント例の両方を持つファイルは両基準で照合する。
- 実際の照合はステップ 4「基準照合」で行う。

### 3. 📡 claude-code-guide サブエージェント呼出（MUST）

書き直し提案を生成する前に `claude-code-guide` サブエージェントを呼ぶ。

依頼内容のテンプレートは `skills/prompts-rewrite-all/prompts/agent-call-claude-code-guide-check.md` を参照する。

#### 🛟 フォールバック

`claude-code-guide` が利用不可な時は代替手段を取る。

- `docs.claude.com` を WebFetch で直参照する
- 完全省略は禁止（仕様ドリフト検出の最後の砦）

### 4. 🔍 基準照合

`claude-code-guide` の結果とステップ 2 で特定した 2 基準
（`.claude/rules/prompt-writing.md` + `.claude/rules/comment-writing.md`）の
**指針 MUST 全項目**および**禁止パターン全項目**を 1 件ずつ照合する。

- 指針 / 禁止の項目本体・検証観点は各基準ルールが Single Source of Truth。
- スキル側で項目を重複定義しない。
- プロンプト本文は `prompt-writing.md`、md 内 GitHub コメント例は `comment-writing.md` で照合する。
- 1 項目でも逸脱があれば書き直し対象とする。

### 5. 書き直し提案

基準照合の結果を踏まえ書き直し案を生成する。

提案ルール:
- frontmatter と本文の両方を対象とする
- 既存セクション構造（見出し・表・コード）は可能な限り保持する
- 1 文 50 文字以下のスキャン性を担保する
- マークダウンフェンスには言語指定を付ける（`markdown.md` 整合）

### 6. 🛑 diff を CEO に提示（承認ゲート）

書き直し案を `git diff` 形式の差分で CEO に提示する。

提示フォーマット例:

```diff
--- a/<path>
+++ b/<path>
@@ -1,3 +1,3 @@
- description: ぼんやりした説明
+ description: 「/foo」「foo して」と言った時に使用。...
```

承認ゲートのルール:
- CEO が「承認」と返した場合のみ次ステップに進む
- 「却下」または無回答ならスキップして次のファイルに移る
- 自動マージは禁止する
- CEO 承認なしに本体ファイルを書き換えない

### 7. 承認後にファイル書き換え

CEO 承認を受けたファイルのみ `Edit` または `Write` で書き換える。

- 対象は本体（`skills/**/SKILL.md` / `agents/*.md` / `.claude/rules/*.md`）
- 書き換え後に `git status` と `git diff` で差分が想定どおりか確認する
- 想定外の差分があれば CEO に再提示する

### 8. 📦 配布版同期チェック

書き換えた本体に対応する配布版があれば同内容で同期する。

- プロジェクト固有の配布構造（配布パッケージ / 配布元テンプレート）に合わせて同期する。
- 配布版が存在しない種別は同期不要。
- 差分が残ったら CEO に再提示する。

#### 例: vibecorp での運用

vibecorp 本体内で実行されるとき、以下のマッピングで同期する。

| 本体 | 配布版 |
|------|--------|
| `skills/**/SKILL.md` | `.claude/vibecorp-base/skills/**/SKILL.md` |
| `agents/*.md` | `agents/*.md` |
| `rules/*.md`（SSOT、`.claude/rules/*.md` は symlink） | `rules/*.md`（SSOT 1 箇所、別途の配布版コピーは持たない） |

利用先プロジェクトでは自プロジェクトの配布パスを使う。

### 9. レポート出力

最終的に以下のレポートを返す。CEO 向け出力物なので `.claude/rules/communication.md` の 30 秒ルール（一覧性・状態絵文字で変化が一目で掴める）を満たす。各行頭に状態絵文字（✅ 完了・成功 / ⚠️ 注意・警告 / ❌ 失敗・却下）を 1 つ付与する。

```text
## /prompts-rewrite-all レポート

- ✅ 対象ファイル数: N
- ✅ 書き直し提案: M
- ✅ CEO 承認: A
- ✅ 書き換え完了: A
- ✅ 配布版同期: B
- ⚠️ スキップ: S
- ✅ claude-code-guide: 呼出 / フォールバック / エラー の内訳
```

状態絵文字の選び方:

- ✅: 全件成功 / 完了している
- ⚠️: 一部スキップ / 警告あり（スキップ件数が 0 でないなど）
- ❌: 失敗・却下が発生した（claude-code-guide エラーが残存、CEO 却下など）

## ✅ 指針（MUST）

本スキル固有の指針のみを定義する。プロンプト本体の指針は基準ルールを参照する。

- プロンプト書き方そのものの指針: `.claude/rules/prompt-writing.md`
- ドキュメント書き方の基底指針: `.claude/rules/document-writing.md`

### スキル固有の指針

1. 📡 **claude-code-guide 経由で仕様確認してから書き直す**
   - 各ファイル書き直し提案前に `claude-code-guide` を呼ぶ
   - フォールバック時も `docs.claude.com` を WebFetch する
   - 完全省略は禁止

2. 🛑 **diff 提案 → CEO 承認 → 書き換えの 2 段階を守る**
   - CEO 承認なしに本体ファイルを書き換えない
   - 自動マージは禁止する

3. 📦 **配布版を同期する**
   - 本体書き換え後に配布版を同期する
   - 差分が残ったら CEO に再提示する

## ❌ 禁止パターン

本スキル固有の禁止のみを定義する。プロンプト本体の禁止パターン
（行動主語逸脱・frontmatter 公式キー以外の追加など）は
`prompt-writing.md` を参照する。

- ❌ **claude-code-guide を経由せずに書き直し提案を生成する**
  - 仕様ドリフト検出の最後の砦を破壊する
- ❌ **CEO 承認なしにファイルを書き換える**
  - 自動マージ禁止に違反する
- ❌ **本体だけ書き換えて配布版を放置する**
  - 利用先プロジェクトに伝搬しない

## 🔗 関連

- 基準ルール（プロンプト本文）: `.claude/rules/prompt-writing.md`
- 基準ルール（md 内コメント例）: `.claude/rules/comment-writing.md`
- ベース基準: `.claude/rules/document-writing.md`
- 動作主語規約: `.claude/rules/communication.md`
- マークダウン規約: `.claude/rules/markdown.md`
- 兄弟スキル（ドキュメント類）: `/vibecorp:docs-rewrite-all`
- 兄弟スキル（コード内コメント）: `/vibecorp:comments-rewrite-all`
- 仕様確認 SubAgent: `claude-code-guide`
