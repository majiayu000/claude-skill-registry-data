---
name: repo-standardize
description: 新規リポの組成、または既存リポの公開前点検を行う。リポ類型の判定・ファイル衛生・.gitignore・LICENSE・.claude/settings.json（deny/allow/attribution）・CLAUDE.md と context/・CI の要否を基準に照らして整える。リポを初期化・標準化・点検したいとき、新規ディレクトリを作って足場を整えたいときに使う。
disable-model-invocation: true
---

# repo-standardize

リポの足場の基準と手順を持つ。設計意図は3点。**全リポ一律の衛生ラインを1本持つ**（軽いリポでも最低ラインは満たし、成熟度で分岐させない）。**禁止は設定に書き、指示ファイルは短く保つ**。**検証手段を Agent に与え、PR 前に自己確認させる**。

CI/CD の基準は `reference/cicd.md`（`repo-readme` の Deploy 節も読む）。Issue まわりの運用は `new-issue` Skill、README の中身は `repo-readme` Skill、図は `mermaid-diagram` Skill の管轄で、本 Skill は触らない。

**公開パイプラインの固定順**: `repo-standardize → guarantee-audit → repo-readme → readme-i18n → repo-publish → repo-about`。本 Skill は**第1**（足場とコアメッセージの確定が先、README の本格化は後）。この順は都度再判断しない。

動くソースコードがあるリポに対して実行する。コードがない段階では実行しない。

## 1. 文脈を確定する

既存のソースコードと設定から読み取る。**読み取れない項目は推測で埋めず、必ず user に質問する。** 引数は使わない。

| 項目 | 取りうる値 | 影響先 |
|---|---|---|
| 類型 | 設定 / ロジック / Web / ツール | deny・allow、検証手段、CI |
| 公開 | Public / Private | LICENSE、CI の要否 |
| スタック | 例: Go+Vue / Python+React / Astro / Nix | コマンド・conventions・CI ステップ |
| 検証手段 | 例: `make test` / `nix flake check` | CLAUDE.md・CI |

類型ごとの検証手段。test とは限らず、「自分の変更が壊れていない」と確かめる経路を1つ以上持てばよい。

| 類型 | 検証手段 |
|---|---|
| 設定（IaC・dotfiles） | 構文チェック（`flake check`・`zsh -n`・`py_compile` 等） |
| ロジック（バッチ・常駐・解析） | 構文チェック ＋ import・caller 確認。可能ならドライラン。test があれば実行 |
| Web（API・サイト） | 型チェック ＋ test |
| ツール（自動化・Agent 駆動） | 構文チェック。副作用コマンドを強く絞る |

検証手段は**追加インストールなしに走るもの**を選ぶ。グローバル導入（`pip install`・`npm install -g` 等）はしない。標準にないツールは `nix-shell -p {pkg} --run "..."` で取り込む。Agent 側で完結しない確認（デプロイ・ブラウザ・本番動作）は PR の `## 検証手順` に書いて user に委ねる。

## 2. 層を敷く

| 層 | 内容 | 適用 |
|---|---|---|
| 層1 事故防止 | `.claude/settings.json` の deny ＋ attribution（行為の判定が要るものは PreToolUse フック） | 全リポ |
| 層2 運用基盤 | CLAUDE.md / context/ ＋ 検証手段 | Agent を走らせる全リポ |
| 層3 公開検証 | CI（`reference/cicd.md`） | Public または自動デプロイあり |

### 層1: settings.json

`.claude/settings.json` をチェックインする（`.local.json` は gitignore される個人上書き用）。雛形は `reference/settings-json-{type}.json`。

- **deny（共通）**: `git push --force *` と `git push -f *` だけを塞ぐ。`git push origin main` 自体は塞がない。実行者がリモートに触れない分業は `pr-workflow` と `issue-finish` で既に効いており、同じ禁止を二重に敷かない
- **deny（類型別に追加）**: 設定＝適用コマンド（`*-rebuild *` 等）・シークレット読み書き・ロックファイル編集／ロジック＝本番起動・外部副作用（実発注・実送信・実課金）／Web＝デプロイ CLI（`wrangler` 等）／ツール＝役割に応じた副作用コマンド。デプロイ経路は Agent に握らせない（リモートへ配る構成が残るリポでは `ssh`・`rsync` も）
- **allow（共通）**: `Bash(git *)`・`Bash(gh pr *)`。push 系は deny が優先するので両立する。リポ外（機密辞書等）を読ませるなら `permissions.additionalDirectories` に足す
- **allow（類型別）**: 設定＝パーサ・構文チェック系／ロジック＝言語ランタイム（本番コマンドは deny で個別遮断）／Web＝`npm run *`・test ランナー・ビルド CLI
- **attribution**: `{ "commit": "", "pr": "" }`。Agent は道具であり共著者ではない

deny は文字列の前方一致しか見ない。禁止したい対象が文字列ではなく行為なら PreToolUse フックで判定する（書き方は本リポの `.claude/hooks/README.md`）。

型のある言語を持つリポでは LSP プラグインを入れる（`claude plugin install {lang}-lsp@claude-plugins-official`。言語サーバ本体は Nix 側に用意する）。文字列検索より前でシンボルに絞り込めるので、リポが大きいほどコンテキストが節約される。Nix・zsh には利得が薄い。

### 層2: CLAUDE.md と context/

実コードを読んで書く。雛形は無い。

| 成果物 | 書くべき内容 |
|---|---|
| `CLAUDE.md` | `@context/conventions.md` と `@context/structure.md` の import、実際に動くコマンド（setup / dev / build / 検証）、アーキテクチャの要点、検証手段。200行以下 |
| `context/conventions.md` | 実コードから読み取った命名規則・コード規約。汎用ルール（「PEP8 準拠」等）の羅列ではなく**このリポ固有の判断** |
| `context/structure.md` | **実在するファイル**のディレクトリ構成・データフロー・レイヤー構成 |
| `context/domain.md` | このリポの世界に何が存在するか。エンティティ・処理段・情報ソースの**名前と境界**（何を乗せてよく、何を乗せてはいけないか）。`PLAN.md` があればその概念定義を移設する。概念が実質1つなら作らない |

CLAUDE.md に**書かないもの**: 禁止・強制（→ deny）、attribution（→ settings.json）、長大な仕様、秘密情報（→ `secrets-agents/` を参照する指示だけを書く）。

`domain.md` は構造ではなく**区別**を書く。`structure.md` が「どう流れるか」なら、`domain.md` は「なぜ A と B を別のものとして扱うか」。

`.claude/`・`CLAUDE.md`・`context/`・`issues/` は公開リポでも追跡対象（無視は `.claude/settings.local.json` のみ）。

## 3. ファイル衛生を整える

- **0 バイト／プレースホルダだけのファイルを残さない。** 例外は、ディレクトリの存在自体が構成の一部であるときの `.gitkeep` のみ
- **成果物を追跡しない。** ビルドバイナリ・`dist/`・`*.db`・`node_modules/`・`.env`。原本（設定の JSON 等）は追跡し、そこから生成される DB・ビルド資産は無視する
- **LICENSE を置く（Public）。** 無いと法的に全権留保になる。`Copyright` の年と owner まで確かめる
- **`.gitignore` はそのスタックに要る行だけ。** 他スタックの boilerplate を残さない。重複行を残さない。OS ファイル・依存・ビルド成果物・ローカル DB・`.env` はカバーする。既存の `.gitignore` は上書きせず、`reference/gitignore-base.txt` の共通行が不足していれば足す
- **`.env` は無視し、`.env.example`（キーのみ）を置く。** ホスト側の本番 `.env` はリポの管轄外（`reference/cicd.md`）
- **地の文に固有接続情報を直書きしない。** `secrets-agents/` の `<PLACEHOLDER>` を使う

## 4. 雛形から生成する

雛形の `<!-- FILL: 説明 -->` の箇所だけを埋め、それ以外は一字一句変えない（FILL コメント自体は出力から消す）。

| 雛形（`reference/`） | 出力先 |
|---|---|
| `settings-json-{type}.json` | `.claude/settings.json`（JSON はコメント不可。allow にスタック固有の行を足し、deny・attribution は変えない） |
| `gitignore-base.txt` | `.gitignore` |
| `license-mit.txt` | `LICENSE`（Public のみ） |
| `dependabot-base.yml` | `.github/dependabot.yml` |
| `dependabot-auto-merge.yml` | `.github/workflows/dependabot-auto-merge.yml`（CI 有リポのみ。運用は `reference/cicd.md` §6） |

`.claude/skills/pr-workflow/SKILL.md` は、正本（本リポの `.claude/skills/pr-workflow/SKILL.md`。稼働環境では home-manager が `~/.claude/skills/` へ配置したもの）をそのまま `cp` する（FILL を持たず、検証手段はリポの CLAUDE.md に委ねる設計）。`issues/done/.gitkeep` も作る。

## 5. 決定的チェック

生成・修正後、機械確認して結果を表で報告する。push / 公開前の点検もこの表で行う。

```
[ ] LICENSE 有・年/owner が正しい（Public）
[ ] 0バイト/プレースホルダのみのファイルなし（.gitkeep/__init__.py 等の慣用は除外）
[ ] 追跡済みに成果物（bin/dist/db/node_modules/.env）なし（git ls-files）
[ ] .gitignore に無関係スタックの残骸・重複行なし
[ ] .env 非追跡 ＋ .env.example 有（.env 使用時）
[ ] .claude/settings.json 有（JSON 妥当・deny に push --force/-f、attribution 空）
[ ] CLAUDE.md / context/{conventions,structure}.md / skills/pr-workflow/SKILL.md 有・非空
[ ] README の H1 直下にコアメッセージ1文がある（型は repo-readme Skill §3）。無ければ種別を判定（同 §1）して1文を書く。それ以上のセクションは書かない（肉付けは publish 前に repo-readme が行う）
[ ] CI 有（Public / 自動デプロイ時）
[ ] dependabot.yml 有（grouping＋レジストリ系 cooldown）。CI 有なら auto-merge workflow＋allow_auto_merge＋ruleset（reference/cicd.md §6）
[ ] 地の文・コミット・PR にシークレット直書きなし
```

## 6. コミット・push はしない

変更はワーキングツリーに残し、差分を要約して止まる。コミット/push は user の指示があったときのみ。
