---
name: issue
description: "GitHub Issue の起票を自動化。タイトル・本文からラベルを自動判定し、Assignees を設定して起票する。「/issue」「Issue作成」と言った時に使用。"
---

# 🎫 Issue 起票自動化

> [!IMPORTANT]
> このスキルは **CEO から Issue 内容を 1 ターンでバッチヒアリングし**、intent ラベル + CC prefix + 3 者承認ゲートを通して起票する。
> 判定の主従順は **intent → CC prefix**（逆引き禁止、`docs/conventional-commits.md` の絶対条件）。1 Issue 1 intent 厳守。
> 3 者承認ゲート（CISO + CPO + SM）は `standard` 以上で有効。`minimal` は 3 者ゲートなしで起票（minimal プリセットの安全性は別経路で担保）。
> 結果のみを簡潔に返す。途中経過は出力しない。

ユーザーから Issue 内容をヒアリングし、ラベル自動判定 + Assignees 設定で起票する。**結果のみを簡潔に返すこと**。途中経過は不要。

## 📝 本文の書き方

Issue タイトル・本文は CEO が読むため `.claude/rules/communication.md` に従って**動作主語**で書く（「〜になった／〜できるようになった」）。関数名・ファイルパスを並べるのではなく、ソフトウェアのふるまいの変化を 30 秒で掴める形にする。

### 関連 Issue / PR への参照

Issue 本文から他の Issue / PR を参照する場合は `Refs #N` 形式で書く。`Closes #N` は使わない（Issue 本文は GitHub の auto-close を発火させないが、PR 本文との表記揺れを避けるため `Refs` に統一する）。

| 関係 | 書式 |
|------|------|
| 親エピック Issue を参照 | `Refs #<親エピック番号>` |
| 関連 Issue / 過去 PR を参照 | `Refs #N` |

PR 本文での `Closes #N` / `Refs #N` 運用は `.claude/rules/workflow.md`「PR 本文の Issue リンク（auto-close キーワード）」を参照する。

## 使用方法

```bash
/vibecorp:issue                  # CEO に 1 ターンでバッチヒアリングして起票
```

ヒアリング項目は **タイトル / 本文 / 完了条件 / 関連ファイル** の 4 項目（ステップ 2 参照）。CEO が一度に全項目を提供した場合はそのまま使用する。

## ワークフロー

### 1. 🔍 リポジトリ情報の取得

```bash
gh repo view --json owner,name,defaultBranchRef --jq '.owner.login + "/" + .name'
```

リポジトリオーナーを Assignees のデフォルトに使用する。

```bash
gh repo view --json owner --jq '.owner.login'
```

### 2. 💬 ユーザーから Issue 内容を取得（1 ターンバッチ質問）

以下の **4 項目を 1 ターンでバッチ質問**する。複数ターンに分けない（公式の `Reduce the number of required user interactions` 原則）。CEO はまとめて入力するため、項目が増えてもターン数は増えない。

- **タイトル**: Issue の内容（タイプは自動付与するため不要）
- **本文**: Issue の詳細（Markdown 形式、💡概要 / 🎯背景 / 📝提案 等を含む）
- **完了条件**: 検証可能なチェックリスト（acceptance criteria）。本文には `## ✅ 完了条件` セクションとして含める
- **関連ファイル**: 触れるファイル・モジュールのパス一覧（relevant file locations）。本文には `## 📍 関連ファイル` セクションとして含める

ユーザーが一度に全項目を提供した場合はそのまま使用する。完了条件・関連ファイルが提供されない場合は、再度の対話を 1 ターン追加するのではなく、最初の 1 ターン内で 4 項目をまとめて要求する文面にする。

#### 設計根拠（Anthropic 公式 Best practices）

[Best practices for using Claude Opus 4.7 with Claude Code](https://claude.com/blog/best-practices-for-using-claude-opus-4-7-with-claude-code) の `Structuring interactive coding sessions` セクションに基づく。

- **`Specify the task up front`**: 初回プロンプトに `intent / constraints / acceptance criteria / relevant file locations` の 4 要素を含める
- **`Reduce the number of required user interactions`**: 質問はバッチ化する（every user turn adds reasoning overhead）

vibecorp での 4 要素の肩代わり状況:

| 要素 | 肩代わり手段 |
|---|---|
| `intent` | 本文（💡概要 / 🎯背景）に CEO が記述 |
| `constraints` | `.claude/rules/` 一式が CLAUDE.md 経由で常駐（ヒアリング不要） |
| `acceptance criteria` | 本文の `## ✅ 完了条件` セクション |
| `relevant file locations` | 本文の `## 📍 関連ファイル` セクション |

constraints は常駐ルールで自動補完されるため、CEO に追加で質問しない。残る 3 要素（intent / acceptance criteria / relevant file locations）を **1 ターンでバッチ質問**する。

### 3. 🧭 SM 自動判定（エピック/単発ルーティング）

`full` プリセットの場合のみ、SM エージェント（`.claude/agents/sm.md`）を **1 回だけ** 呼び、Issue の内容を「単発」か「エピック化」かに自動判定する。合議は行わず SM 1 人で判定する（CEO 判断: コスト抑制と意思決定の単純化のため）。

#### 適用条件

vibecorp.yml が存在する場合のみ preset を確認する。

```bash
if [ -f "$CLAUDE_PROJECT_DIR/.claude/vibecorp.yml" ]; then
  awk '/^preset:/ { print $2 }' "$CLAUDE_PROJECT_DIR/.claude/vibecorp.yml"
fi
```

- preset が `full` の場合のみ SM 自動判定を実行する
- preset が `minimal` / `standard`、vibecorp.yml が存在しない、または preset キーが未定義の場合 → このステップを **スキップ** し、ステップ 4 以降の従来挙動（単発起票）に進む
- `/vibecorp:plan-epic` スキルが配置されていない場合 → このステップをスキップし、単発起票にフォールバックする

#### 判定基準

SM エージェントは以下の観点で「単発判定 / エピック化判定」を行う。

- **複数要件の列挙**: 本文が複数の独立した要件を列挙しているか（箇条書き・番号付きリストで 3 件以上の独立タスクが存在する）
- **ファイル領域の複数跨ぎ**: 影響範囲が複数のディレクトリ・モジュールに跨るか（例: hooks + skills + agents の同時変更）
- **並列実行可否**: 各要件が独立して並列実装可能か（同一ファイル競合がない / 直列依存がない）

3 観点のうち 2 つ以上が当てはまればエピック化候補、それ以外は単発と判定する。

#### SM への依頼テンプレート

プロンプトは `skills/issue/prompts/agent-call-sm-epic-judgment.md` を参照する。

#### CEO override

ユーザー入力（タイトル・本文・補足指示）に以下の明示指示が含まれる場合、SM 判定を上書きする。

- **単発に上書き**: 「単発でいい」「単発で起票」「単発で OK」等
- **エピックに上書き**: 「エピックにして」「エピック化して」「エピックで起票」等

override が適用された場合、返却時に「CEO override: あり」を明記する（透明性確保）。

#### 判定結果の扱い

- **単発判定** → ステップ 4 以降に進む（従来通りタイプ判定 → 3 者承認ゲート → 起票）
- **エピック化判定** → `/vibecorp:plan-epic` スキルにタイトル・本文をそのまま渡してルーティングし、`/issue` の処理は終了する
  - `/vibecorp:plan-epic` の出力（親 Issue URL + 子 Issue URL 一覧）をそのまま CEO に返す
  - エピック化判定時は本スキルのステップ 4 以降（タイプ判定・3 者承認ゲート・起票）は実行しない（`/plan-epic` 側で必要なゲートが実装される前提）

### 4. 🏷️ intent ラベル判定 + CC prefix 選択（COO 主体・FIX）

#### 4a. COO による intent 判定

旧 type 14 種のキーワード判定表は **廃止**（Issue #469 議論結論）。COO（メインセッション）が Issue 本文を読んで文脈で intent ラベルを判定する。

判定対象は **`.claude/rules/intent-labels.md` の 7 種**:

- `intent/feature` — 新機能を確実に動かす（影響を与える系）
- `intent/bugfix` — 既存バグを最小修正で直す（影響を与える系）
- `intent/performance` — 性能を測定可能な形で改善する（影響を与える系）
- `intent/security` — 脆弱性を塞ぐ（影響を与える系）
- `intent/refactor` — 構造の品質を高める（挙動不変系）
- `intent/infra` — 開発基盤の品質を底上げする（挙動不変系）
- `intent/docs` — ドキュメントの正確性を担保する（挙動不変系）

**絶対条件**: 1 Issue 1 intent 厳守。複数 intent にまたがる変更は Issue を分割するよう CEO に提案する。

#### 4b. COO による CC prefix 選択

intent → prefix の主従順で対応 prefix を選ぶ（逆引き禁止、`docs/conventional-commits.md` の絶対条件）。

| intent ラベル | 対応する CC prefix |
|--------------|------------------|
| `intent/feature` | `feat` |
| `intent/bugfix` | `fix`, `revert`（差し戻しは regression 修正の一形態） |
| `intent/performance` | `perf`, `feat`（性能向上目的の機能）, `fix`（パフォーマンス系バグ） |
| `intent/security` | `fix`（脆弱性修正）, `feat`（セキュリティ機能追加）, `chore`（依存パッケージのセキュリティアップデート） |
| `intent/refactor` | `refactor`, `style` |
| `intent/infra` | `test`, `ci`, `chore`, `build` |
| `intent/docs` | `docs` |

同じ intent に対応する prefix が複数ある場合は、内容に応じて最も適切なものを COO が選ぶ。

#### 4c. CC prefix → 絵文字 1:1 マッピング

`docs/conventional-commits.md` 確定の絵文字 11 種:

| CC prefix | 絵文字 |
|-----------|------|
| feat | ✨ |
| fix | 🐛 |
| perf | ⚡ |
| refactor | 🔄 |
| style | 💄 |
| docs | 📖 |
| test | 🧪 |
| ci | 🔧 |
| chore | ⚙️ |
| build | 📦 |
| revert | ⏪ |

**タイトル形式**: `<emoji> <CC prefix>: <動作主語の subject>`

- COO が intent → prefix → 絵文字の順で確定する（逆順禁止）
- 既存ラベル（`bug` / `enhancement` 等）はリポジトリに存在する場合のみ付与する
- ユーザーが既にタイプ付きタイトルを入力していても、判定は **常に本文から intent を先に確定**する（intent → prefix の主従順、絶対条件）。本文から確定した intent と既存タイトルの prefix が整合しない場合は、本文を優先して prefix と絵文字をタイトル側で修正する
- 既存ラベル一覧は `gh label list --json name --jq '.[].name' --limit 100` で取得する

### 5. 👤 Assignees 決定

1. `.claude/vibecorp.yml` に `issue.default_assignee` が定義されていればその値を使用する
2. 未定義の場合はリポジトリオーナー（手順 1 で取得）を使用する

### 6. 🛡️ 3者承認ゲート（standard 以上）

vibecorp.yml が存在する場合のみ preset を確認する。

```bash
if [ -f "$CLAUDE_PROJECT_DIR/.claude/vibecorp.yml" ]; then
  awk '/^preset:/ { print $2 }' "$CLAUDE_PROJECT_DIR/.claude/vibecorp.yml"
fi
```

preset が `standard` または `full` の場合のみ、CISO + CPO + SM の 3 者で `.claude/rules/autonomous-restrictions.md` に定義された自律実行不可領域（認証 / 暗号 / 課金構造 / ガードレール / MVV / CI エージェント）と、プロダクト方針の整合性を判定する。いずれかのエージェントが「除外」判定した場合は起票を中止する。

**責務分離の根拠**: `/vibecorp:autopilot` / `/vibecorp:ship-parallel` の自律ループが全 open Issue を対象とするため、不可領域の門番は起票側（本スキルと `/vibecorp:diagnose`）に集約する。ship 側は起票済み Issue を信頼して実行する。

#### 6a. CISO フィルタリング（不可領域チェック）

CISO エージェント（`.claude/agents/ciso.md`）に依頼する。プロンプトは `skills/issue/prompts/agent-call-ciso-issue-check.md` を参照する。

#### 6b. CPO フィルタリング（MVV / docs 整合 + 4 要素チェック）

CPO エージェント（`.claude/agents/cpo.md`）に依頼する。プロンプトは `skills/issue/prompts/agent-call-cpo-issue-check.md` を参照する。

**4 要素チェックの位置づけ**: Anthropic 公式が「初回プロンプトに含めろ」と明記している 4 要素のうち、constraints は `.claude/rules/` 常駐で自動補完されるため Issue 本文には不要。intent / constraints / acceptance criteria / relevant file locations が揃っていない Issue は後段の `/vibecorp:plan-review-loop` が空欄を前提に走り品質が落ちるため、起票時点で書き忘れを検出して除外する。

#### 6c. SM フィルタリング（自律実行可否チェック）

SM エージェント（`.claude/agents/sm.md`）に依頼する。プロンプトは `skills/issue/prompts/agent-call-sm-issue-check.md` を参照する。

#### 判定結果の扱い

- 3 者全員が「OK」→ ステップ 7（起票）へ進む
- いずれかが「除外」→ 起票を中止し、却下フォーマット（後述）で報告して終了する
- preset が `minimal`、vibecorp.yml が存在しない場合、または preset キーが未定義の場合 → このステップを全てスキップ（3 者フィルタなし）

**minimal プリセットの安全性**: minimal では 3 者フィルタが動作しないが、`/vibecorp:autopilot` / `/vibecorp:ship-parallel` が full プリセット専用のため、不可領域 Issue が自動実装される経路は存在しない。CEO が明示的に `/vibecorp:ship` を呼ぶ手動実装のみ可能で、これは CEO の意思による承認ルートとして許容される。

### 7. 🚀 Issue 起票

```bash
gh issue create --title "<emoji> <CC prefix>: <subject>" --body "<本文>" --assignee "<assignee>" --label "intent/<intent>" --label "<additional_label_if_any>"
```

- **`intent/*` ラベルは必須**（COO が ステップ 4a で確定したもの 1 つだけ）
- 既存ラベル（`bug` / `enhancement` 等）はリポジトリに存在し、内容に該当する場合のみ追加付与する
- ラベルが intent のみの場合は `--label "intent/<intent>"` のみ指定する

### 8. ✅ 結果報告

起票した Issue の URL を返す。`full` プリセットで SM 自動判定が動作した場合は判定結果も併記する。

## 制約

- **jq では string interpolation `\(...)` を使わない** — Bash 上で `\` がエスケープ文字、`()` がサブシェルとして解釈され、意図しない展開やパースエラーを引き起こすため。必ず `+` で結合する
- **コマンドをそのまま実行する** — `2>/dev/null`、`|| echo`、`; echo` 等のリダイレクトやフォールバックを付加しない（[根拠](docs/design-philosophy.md#コマンドリダイレクトフォールバックの禁止)）
- リポジトリに存在しないラベルは `--label` に渡さない（`gh issue create` がエラーになるため）
- `vibecorp.yml` が存在しない、または `issue.default_assignee` が未定義でも正常に動作すること

## 📤 返却フォーマット

### 通過時（単発起票）

```text
<Issue URL>
タイトル: <emoji> <type>: <subject>
ラベル: <付与したラベル一覧（なしの場合は「なし」）>
担当者: <assignee>
```

`full` プリセットで SM 自動判定が動作した場合は、上記の末尾に判定結果を追記する。

```text
### 判定結果（full プリセットのみ）
- SM 判定: 単発
- 判定根拠: <SM が判定の根拠とした要素を 1〜2 行で>
- CEO override: あり / なし
```

### 通過時（エピック化ルーティング）

`full` プリセットでエピック化と判定された場合は、`/vibecorp:plan-epic` の出力に判定結果を併記して返す。

```text
✨ エピック化して起票しました

親 Issue: <親 Issue URL>
子 Issue:
  - <子 Issue URL #1>
  - <子 Issue URL #2>
  ...

### 判定結果
- SM 判定: エピック化
- 判定根拠: <SM が判定の根拠とした要素>
- CEO override: あり / なし
```

### 却下時（3 者承認ゲート）

```text
❌ 起票を見送りました

### 判定結果
- CISO: {OK / 除外（理由）}
- CPO: {OK / 除外（理由）}
- SM: {OK / 除外（該当領域: 認証 / 暗号 / 課金構造 / ガードレール / MVV / CI エージェント のいずれか）}

### 却下理由
<除外と判定したエージェントの理由を要約>

### 対処方針
- 不可領域に該当する場合: MVV に立ち返って Issue の目的を再検討するか、CEO による手動承認・実装を検討してください
- MVV 不整合の場合: MVV.md に照らし合わせて Issue タイトル・本文を修正してください
```

## 🔗 関連ルール

- intent ラベル定義: `.claude/rules/intent-labels.md`
- CC prefix 厳格定義: `docs/conventional-commits.md`
- 不可領域定義: `.claude/rules/autonomous-restrictions.md`
- CEO 報告向け文面規約: `.claude/rules/communication.md`
- ブランチ命名・PR 本文の Issue リンク: `.claude/rules/workflow.md`
- エピック起票: `/vibecorp:plan-epic`
- プロンプト作成基準: `.claude/rules/prompt-writing.md`
- マークダウン規約: `.claude/rules/markdown.md`
