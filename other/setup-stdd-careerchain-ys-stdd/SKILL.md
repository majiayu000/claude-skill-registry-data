---
name: setup-stdd
description: |-
  STDD の導入入口（ルーター）。「STDD を導入して / 始めて / セットアップして」と言われたとき最初に起動し、対象プロジェクトが新規（コードがまだ無い）か既存（稼働コードがある）かを自動判定して、適切な駆動スキル（新規=starting-new-with-stdd / 既存=introducing-stdd）へ委譲する薄いディスパッチャ。再開中の導入PLAN/立ち上げPLANがあればそれを優先して続きから再開する。判定はユーザーに一言確認してから委譲する。
when_to_use: |-
  「STDDを導入して」「STDDを始めて」「STDDをセットアップ」「STDDを使い始める」「setup stdd」「start stdd」「stddを入れて」など、どちらのフローか未確定のままSTDD導入を頼まれた最初のとき。新規/既存が明確で続きから進める場合は starting-new-with-stdd / introducing-stdd を直接使う。
allowed-tools: Read, Glob, Grep, Bash, Skill
---

# STDD 導入ルーター

「STDD を導入して」と言われたときの**最初の受け口**。対象プロジェクトを調べ、
**新規（コードなし）** か **既存（稼働コードあり）** かを判定し、適切な駆動スキルへ委譲する。
自分自身は spec を書いたり実装したりせず、判定と委譲だけを行う薄い役割。

---

## 手順

### 1. 再開中の PLAN を最優先で確認

すでに導入/立ち上げが始まっている場合は、続きから再開する。次が存在するか確認する:

```
□ docs/common/plans/stdd-introduction.md がある → 既存フロー継続 → introducing-stdd へ
□ docs/common/plans/stdd-bootstrap.md がある    → 新規フロー継続 → starting-new-with-stdd へ
```

どちらかがあれば、ユーザーに「導入を途中から再開します」と伝えて該当スキルへ委譲し、以降の判定はスキップする。

### 2. 新規 / 既存 を判定

PLAN が無ければ、リポジトリにアプリケーションのソースコードが実在するかで判定する。

```
□ アプリのソース（src / app / pages / packages の実装ファイル等）が実在するか
□ package.json の dependencies に実プロダクトの依存があるか（雛形のみではないか）
□ git 履歴に機能実装のコミットがあるか
```

判定基準:
- **コードが実質ゼロ**（空ディレクトリ、または README / `.stdd.config.yml` / `.claude/` / `docs/` の雛形だけ）→ **新規**
- **アプリのソースが存在する**（既に動く機能がある）→ **既存**

判定材料の集め方の例:

```bash
# .git / node_modules / .claude / docs / 設定ファイルを除いた実ソースの有無をざっと見る
git ls-files 2>/dev/null | grep -vE '^(\.claude/|docs/|\.stdd\.config\.yml|README|LICENSE|\.gitignore)' | head -50
```

### 3. ユーザーに確認してから委譲

判定結果を一言で伝え、合っているか確認してから委譲する（誤判定を防ぐ）。

- 例（既存）: 「アプリのソースを検出しました。**既存プロジェクトへの導入**として進めます。よいですか？」
- 例（新規）: 「コードはまだ無いようです。**新規プロジェクトの立ち上げ**として進めます。よいですか？」

確認が取れたら、対応する駆動スキルを起動する:

| 判定 | 委譲先スキル |
| --- | --- |
| 新規（コードなし） | `starting-new-with-stdd` |
| 既存（コードあり） | `introducing-stdd` |

委譲後は、そのスキルが以降のフロー（spec 生成・フォーマット策定・機能ループ等）を駆動する。

---

## 前提

- このスキルは `stdd init`（`.claude/` と `.stdd.config.yml` の配置）が済んだプロジェクトで使う想定。
  `.stdd.config.yml` が無い場合は、まず `npx @careerchain/stdd init` を案内する。
- 判定がどうしても曖昧な場合は決め打ちせず、ユーザーにどちらで進めるか尋ねる。

---

## When NOT to Use This Skill

- **新規/既存が明確で続きから進めたい**: `starting-new-with-stdd` / `introducing-stdd` を直接呼ぶ。
- **単一機能のリバースだけしたい**: `reverse-engineering-feature-spec` を直接使う。
- **個別機能の新規実装**: `auto-implement`（順行 STDD）を使う。
