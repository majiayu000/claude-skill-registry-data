---
name: repo-charter
description: 新規リポジトリ作成時(gh repo create)、または既存リポジトリの目的が曖昧になってきたときに、README + CONTRIBUTING.md に機械検査可能な charter(目的1文・Scope・Issue受け入れ判定・命名クラス・topics)を播き、AGENTS.md/CLAUDE.md ルーティングと skills 配置を整える手順。charter・リポジトリの目的を言語化・Issue受け入れ判定・スコープが曖昧・迷走している・gh repo create、といった文脈で使う。repo purpose statement, Issue acceptance criteria, README charter, gh repo create checklist、といった英語の文脈でも使う。github-audit(事後の横断監査)・github-audit-triage(監査駆動の一括裁定)とは役割が異なる — こちらは 1 リポジトリを播く/適合化する側。
---

新規リポジトリは「何を作るか」だけが先に決まり、「どの Issue がこのリポジトリに
属するか」を判定する軸が言語化されないまま育つことが多い。軸が無いと、AI Agent
は目指すべき方向性がブレ、人間は何を期待すべきかブレて、見当外れの Issue を切る
(あるいは切ってよいか判断できない)。charter はこの軸を、README/CONTRIBUTING の
中の機械検査可能な形に固定する。

事後の横断検査は `github-audit`(手順は `docs/github-audit.md`)、監査 findings
からの一括裁定は `github-audit-triage`(`docs/agents/github-audit-triage.md`)。
このスキルは 1 リポジトリを**播く/適合化する**側の手順。README 正形・
ルート文書 allowlist・AGENTS.md 正本化は ADR-0016、CONTRIBUTING.md 自体の
固定スキーマは ADR-0017(いずれも tarotene/dotfiles)の裁定に従う。

## 1. charter インタビュー

次の順で、1 つずつ確定させる(飛ばさない)。

1. **目的 1 文**(≤120 字) — このリポジトリが存在する理由を 1 文で。README の
   H1 直後の段落の書き出しになり、そのまま GitHub の description にもなる
   (両者は同じ文字列 — description は README のミラーであって独立した二つ目の
   要約ではない)。
2. **命名クラス**(ADR-0014 + ADR-0020 + ADR-0026) — このリポジトリは
   `naming-codename`(恒久ツール・一語、意味を持たない恣意的ラベル)/
   `naming-coined`(著者固有の命名形態論に基づく、意味を持つ造語)/
   `naming-descriptive`(研究・記録・コンテンツ系の複合語)/
   `naming-pj`(期限付きプロジェクト、`pj-` prefix)/ `naming-site`
   (公開ドメインのサイト、FQDN)の 5 クラスのどれか。**新規作成は常に
   ADR-0020 の cutoff より後なので、字句パターンだけでなく閉じた語彙も
   ここで強制する**(github-audit の naming ドメインが後から drift 検出
   するのを待たない — 生成側で先に閉じる)。ADR-0020 の閉語彙アプローチは
   `naming-codename` にのみ継続適用され、`naming-coined` には適用しない
   (ADR-0026 Amends 節):
   - `naming-descriptive` を選ぶ場合: 名前の末尾トークンが
     `config/github-audit/descriptive-species.tsv` の種別語に**ないと
     作成に進めない**。ここにない種別語(特に「完了しうる行為」を表す
     語 — cleanup, migration 等)は `naming-pj` へ倒す。種別語を追加したい
     場合は先にそのファイルの改訂 PR を立てる。
   - `naming-codename` を選ぶ場合: 名前が
     `config/github-audit/codename-registry.tsv`(PUBLIC)または
     `~/.config/github-audit/codename-registry.local.tsv`(PRIVATE)に
     **登録されていないと作成に進めない**。未登録なら先にレジストリへの
     追記(PUBLIC は PR、PRIVATE はローカルファイルへの直接追記)を行う。
   - `naming-coined` を選ぶ場合: 閉語彙チェックは無い(各リポジトリごとに
     個別の意図を持って作られる造語のため)。その代わり、なぜその造語を
     選んだか(形態素パターン・比較審査の記録)を当該リポジトリの ADR 等に
     残すことを推奨する(dotfiles 側は強制しない)。
   - `naming-site` を選ぶ場合: ドメインが対応する
     `site-domains.tsv`/`.local.tsv` に登録されている前提で進める。
   - `naming-pj` は対象スロットが字句規則のみ(閉じた語彙なし)。
   名前が選んだクラスのパターン・語彙に一致しない場合、リポジトリ名を
   変えるかクラスを選び直すかをここで決める(改名は既存リンクを壊すので、
   新規作成時に決めるのが一番安い)。
3. **ライフサイクルトピック**(ADR-0026、任意・`naming-*` と直交併用可) —
   このリポジトリに次のいずれかが当てはまるか、当てはまらないなら
   「無し」と確定させる。1 リポジトリに `naming-*` 1 個 + ライフサイクル
   トピック 0〜1 個を付けられる:
   - `lifecycle-timeboxed`: 外部成果物を持つ時限プロジェクト。`naming-pj`
     と併用できる(prefix は命名パターン、このトピックは「今なお時限性を
     持つか」を独立に表現する)。プロジェクト完了後も `naming-pj` の
     命名は変えないが、このトピックは外してよい。
   - `lifecycle-study`: 研究・学習記録。対象が自分の知識・学位であり
     外部成果物を持たない。完了済み(archived)・進行中いずれの状態も
     取る。`naming-descriptive` や `naming-pj` のどちらとも併用できる。
   - 無し: 上記いずれにも当てはまらない恒久的なリポジトリ。
4. **Scope**(地の文、In/Out ラベルなし) — このリポジトリが担うこと・担わない
   ことを、境界と代表的な caveats だけ数文で書く。担わない側は「関連するが
   別リポジトリの責務」を具体的に書く(例: 「現像ワークフローの自動化は
   downstream リポジトリの責務」)。箇条書きの羅列にせず、読んで文脈が繋がる
   ようにする(standard-readme の簡潔性規範、ADR-0016)。
5. **Issue 受け入れ判定(判定問 + 実例)** — 「その Issue はこのリポジトリの
   [目的 1 文の核心] を前進させるか?」型の判定問を 1 個。判定問だけでは
   曖昧なので、採用例・棄却例を各 1〜2 行で添える(長文の弁明は書かない —
   1 項目 1〜2 行に収める)。実例はパターンマッチで判定できることが目的なので、
   実在または実在しそうな具体的な Issue を書く(抽象的な原則の言い換えにしない)。
   この判定問 + 実例は CONTRIBUTING.md の `## Issues` 節の冒頭に書く(次々節)
   — 見出し名としての「Issue litmus」という自作語彙は ADR-0017 で廃止した。
6. **banner 画像の選定**(ADR-0028 Amendment、必須) — README の H1 直上に置く
   画像を 1 点選ぶ。素材源の既定はいらすとや(<https://www.irasutoya.com/>)で、
   自作のロゴでもよい。何を描くかは手順 2 の命名クラスで決まる:
   - `naming-codename` / `naming-coined`: 名前の由来(namesake)を描く
     (例: 伝書鳩を意味する名前なら鳩)。
   - `naming-descriptive` / `naming-pj` / `naming-site`: 目的 1 文の主題を描く。
   候補探しは `scripts/irasutoya-search.sh <検索語>` で機械化する(検索ページは JS 描画で
   画像 URL が取れないが、Blogger の JSON フィードは題名・投稿 URL・画像 URL を 1 回で返す。
   出力は `title`・`url`・`s400`・`s800` の JSON 配列。#940)。`--dry-run` で走らせる curl だけを
   表示し、`--selftest` で抽出(jq)だけを確かめる。
   alt text は英語 1 文で、何を描いたか、それが由来か主題か、出所の順に書く
   (例: `Cartoon illustration of a carrier pigeon delivering a letter, the
   repository name's namesake, by Irasutoya`)。第三者素材を使うなら §5 の手順を踏む。監査は
   「H1 より前に `<img` があるか」だけを見る(`readme-banner-missing`)。

インタビューは人間との対話で埋める。埋まらない項目があるなら、それは
「リポジトリの目的がまだ固まっていない」ということなので、charter を書くこと
自体を急がず、目的の言語化を先に済ませる。

## 2. README への反映(ADR-0016 の固定スキーマ)

見出しリテラル(英語)は固定・順序も固定 — `github-audit` の charters ドメインが
この形で機械検査する。日本語で書くリポジトリでも見出しはこの英語表記を使う。
`## Background` は任意(知的出自のみ)、それ以外は必須。banner も必須(ADR-0028 Amendment)。

```markdown
<!-- 必須(ADR-0028 Amendment)。第三者素材を使う場合は後述の「第三者素材アセットの同梱」節に従う -->
<p align="center">
  <img src="docs/assets/<file>" alt="<英語 alt text>" width="240">
</p>

# <repo-name>

<目的 1 文>。<自由記述の続き。省略可>

## Background

(任意。なぜこの形で存在するに至ったかの知的系譜のみ。改名の経緯・日付・
「〜待ち」のような時限状態は書かない — 履歴は git log/CHANGELOG の責務。
個別 Issue 番号も焼き込まない。)

## Install

<環境構築手順>

## Usage

<最小の実行可能な例>

## Scope

<地の文。境界と代表的な caveats>

## Development

<build/test/lint の定型コマンド>

## License

<ライセンス表記>
```

**書いてはいけないもの(出典は `docs/adr/0016-repository-document-canon.md`)**:
履歴・時限記述(「改名した」「follow-up 待ち」等、Google style guide の
timeless documentation 規範)、個別 Issue 番号の引用(Art of README の
永続性原則)、`## Issue litmus` 見出し(CONTRIBUTING.md へ移設、次節)、
許可外の見出し。既存の `CONTEXT.md` のような詳細ドキュメントは中身を精査し、
恒久的な内容だけ README/`docs/` へ移し、それ以外は破棄する(ルート allowlist、
次々節)。**ディレクトリ構成図(tree)・ファイル/コンテンツの手書き一覧・
他ファイルの中身の転記も書かない(ADR-0033)** — 詳細は
`## 4a. 導線文書に書かないもの(ADR-0033)` を参照。

**監査の目的文抽出には罠が 3 つある**(`github-audit` charters ドメインの
実装挙動、#182)。監査は H1 直後の**最初の非空段落**をそのまま目的段落として
取るので、キャッチコピーやバッジ行を H1 と目的 1 文の間に挟むとそれが目的文と
誤認される — 目的 1 文の段落を H1 の直後に置く。同じ理由で **banner は
H1 より上に置く**(H1 と目的 1 文の間に挟まない) — `extract_purpose()` は
最初の `^# ` 行より前を一切読まないため、H1 より上に置いた banner は監査に
不可視で済む(ADR-0028)。また目的 1 文は**最初の `.` / `。` で切り出して**
description と照合するため、URL やバージョン番号のような埋め込みピリオドを
目的 1 文の中に書くと途中で切れて `purpose-mismatch` になる。

### 日本語が正本のリポジトリ(ADR-805)

README と CONTRIBUTING の読者が日本語話者に限られ、英語の原文を読める人が
実質的にいないリポジトリ(団体の運営など)は、日本語を正本にしてよい。
見出しのリテラルは英語のまま(上の固定スキーマ)、本文を日本語で書き、
トピック `lang-ja` を付ける(§8)。宣言があると、監査は
`readme-cjk-present` / `contributing-cjk-present` を出さない。README を
英語に直したのにトピックを外し忘れると `lang-ja-stale` で検出される。
手順は `docs/agents/lang-ja-declaration.md`。

## 3. CONTRIBUTING.md への反映(ADR-0013 部分 supersede、固定スキーマは ADR-0017)

CONTRIBUTING.md は GitHub が Issue/PR 作成画面で自動リンク表示する標準ファイル
(GitHub Docs "Setting guidelines for repository contributors")。この標準
機構が最も生きる 2 節 — issue の切り方・PR の出し方 — を固定見出しにする
(出典・調査範囲・却下した代替案は `docs/adr/0017-contributing-schema.md`)。
環境構築/テストの定型コマンドは README の `## Development` が既に正本なので、
ここでは重複させず参照 1 行に留める。

```markdown
# Contributing

See [README](../../../../docs/README.md) for what this repository is and how to set up a
development environment.

## Issues

Judging question: <このリポジトリの目的を前進させるかを問う疑問文>

Accepted:
- ...

Rejected:
- ...(別リポジトリの責務ならその名前を書く)

## Pull requests

<PR の出し方・レビュー方針・マージ方式の定型文>
```

`## Expectations`(単独メンテナの応答期待値)は任意節として `## Pull
requests` の後に追加してよい。見出しリテラル(英語)・順序ともに
`github-audit` の charters ドメインが機械検査するため固定 — 日本語で書く
リポジトリでもこの英語表記を使う。「Issue litmus」という見出し名の自作語彙は
ADR-0017 で廃止した(判定問 + 採用例・棄却例という**内容の形**は `## Issues`
冒頭に維持 — AI エージェントがコントリビュータになるケースへの言及は
調査した一次情報のいずれにも無く、ここは先行例のない領域)。

## 4. ルート文書 allowlist(ADR-0016)

リポジトリのルートに置いてよい Markdown は `README.md` / `CONTRIBUTING.md` /
`CHANGELOG.md` / `AGENTS.md` / `CLAUDE.md` の 5 種(+ `LICENSE*`)のみ。
`CONTEXT.md` / `NOTES.md` のような野良ルート文書は作らない — 深い文書は
`docs/` 配下に置く。既存リポジトリの適合化でこの種のファイルが見つかったら、
恒久的な内容は README の `## Background` か `docs/` へ吸収し、ファイル自体は
削除する。

## 4a. 導線文書に書かないもの(ADR-0033)

「導線文書」= ルート文書 allowlist(前節)+ 各ディレクトリの
`<dir>/README.md`。判定軸は**情報の寿命**(この記述は、指す実体が変わる
たびに書き換えが要るか)。次の 3 種は寿命が短いので導線文書に書かない
— 実体の隣に置き、導線文書からは 1 行のポインタで指す。

- **ディレクトリ構成図(tree)。** ファイル追加・リネームで壊れる。
  各ディレクトリが何をするかは、そのディレクトリ自身の
  `<dir>/README.md` 冒頭 1〜3 行に書く(一覧ではなく自分自身の説明
  なので `<dir>/README.md` 自身は書いてよい)。
- **ファイル/コンテンツの手書き一覧。** ADR 索引、ワークフロー一覧、
  コマンド一覧など。コンテンツ追加のたびに壊れ、実際に運用ではすぐ
  drift する(欠落項目が出る)。索引が要るなら `docs/` 配下に生成
  スクリプトを書くか、単に列挙をやめて「詳細は `docs/` を見よ」の
  1 行に留める。
- **他ファイルの中身の転記。** YAML/JSON スキーマ、設定値、CLI の
  使用法などを README にコピーしない。正本(実ファイル自身の先頭
  コメント、または `--help`)を 1 行で指す。

目的・方針・命名規約・Issue 受け入れ判定基準のような寿命の長い記述は
対象外 — 実体が変わっても書き換えが要らない。

機械検査(節内のユニークなパス様文字列が 4 個以上、またはツリー罫線
文字の出現)は `github-audit` の charters ドメインが行う
(`docs/github-audit.md`)。生成された一覧や第三者素材の帰属注記
(ADR-0028)のように意図的に一覧を書く必要がある場合は、直前に
`<!-- nav-doc-exempt: <path-inventory|tree-fence> — <理由> -->` を
置いて対象チェックを名指しで除外する。チェック名・理由のどちらかを
欠くマーカーは `nav-doc-exempt-malformed` として drift になる。出典・
Alternatives・却下した代替案は `docs/adr/0033-nav-doc-no-materialisation.md`
を参照。

## 5. 第三者素材アセットの同梱(ADR-0028)

repo ライセンス(MIT 等)と異なる利用規約を持つ第三者素材(README banner の
イラスト等)を同梱する場合は次の手順を踏む。

1. **素材源の利用規約を確認し、記録する。** 確認する 4 点: (a) 再配布可否、
   (b) 商用利用の条件(点数制限の有無を含む)、(c) 改変可否(リサイズ・
   トリミングを含む)、(d) 帰属表示の要否。確認した規約の URL と取得日を
   このあとの帰属注記または PR 本文に残す。
2. **`docs/assets/` に commit する。** ルート直下への配置と外部 URL への
   hotlink は禁止。ファイル名は英語ケバブケース(例 `readme-banner.png`)。
3. **banner は H1 の直上に置く。**
   `## 2. README への反映` の banner ブロックの罠(監査の目的文抽出との
   衝突)を参照。
4. **README の `## License` 節の末尾に、素材 1 点につき 1 行で帰属注記を
   置く。**

   ```markdown
   The banner illustration ([`docs/assets/<file>`](docs/assets/<file>))
   is by [<出所名>](<出所トップページ URL>)
   ([source page](<素材ページ URL>)) and is **not** covered by this
   repository's license; it is used under the
   [<出所名> terms of use](<規約 URL>).
   ```

   1 点 1 行にすることで、同一素材源の使用点数を License 節の行数を数える
   だけで把握できる(点数制限を持つ素材源への対応)。
5. **LICENSE ファイルには書かない。** 第三者素材の例外は README `## License`
   節側のみで行い、LICENSE ファイル自体はリポジトリのライセンス原文のみに
   保つ。

本規則は README banner に限らず、`docs/` 配下に置く第三者由来の図版・
スクリーンショット一般に適用する。出典・調査範囲・却下した代替案は
`docs/adr/0028-readme-banner-and-third-party-assets.md` を参照。

## 6. AGENTS.md / CLAUDE.md ルーティング(ADR-0016)

AI 向け正本は `AGENTS.md` 1 本。README/CONTRIBUTING を参照する側に置き、
内容を複製しない。

```markdown
# Agent instructions for <repo-name>

See [README.md](../../../../docs/README.md) for what this repository is and does, and
[CONTRIBUTING.md](CONTRIBUTING.md) for what Issues and pull requests are
accepted. This file is for agent operating instructions only.
```

Claude Code を使うリポジトリでは `CLAUDE.md` を `@AGENTS.md` import 1 行 +
Claude 固有差分のみのルータにする:

```markdown
@AGENTS.md

<!-- Claude-specific differences from AGENTS.md, if any, go below. -->
```

CLAUDE.md に実内容を書き足していく(AGENTS.md との二重管理になる)構成は
`github-audit` の charters ドメインが drift として検出する。

## 7. skills を持つ場合のルーティング(ADR-0016)

このリポジトリ自身が Claude Code の repo スコープ skill を持つ(`.claude/
skills/<name>/SKILL.md` を新設する)場合、正本はツール中立の
`.agents/skills/<name>/SKILL.md` に置き、`.claude/skills/<name>` はそこへの
相対 symlink にする(Codex CLI・Copilot CLI は `.agents/skills/` を
ネイティブ読取、Claude Code は `.claude/skills/` のみ読取のため):

```bash
mkdir -p .agents/skills/<name>
# SKILL.md 等を .agents/skills/<name>/ に置いてから:
mkdir -p .claude/skills
ln -s ../../.agents/skills/<name> .claude/skills/<name>
```

## 8. GitHub メタデータへの反映

**新規作成は `scripts/create-repo.sh` で行う**(#754)。素の `gh repo create` は
repo-create-guard が deny する。guard が強制したいのは「この手順に載せること」
なので、手順そのもの(閉語彙チェック → `gh repo create` → `--add-topic` →
governance 播種)を 1 本で実行するスクリプトが正規の入口で、バイパス用の環境変数
(`SKIP_REPO_CREATE_GUARD=1`)は要らない — auto モードの分類器は、これを
safety bypass と判定して拒否する。guard は Bash のコマンド文字列しか見ないので、
スクリプト内の `gh repo create` は deny に当たらない(`apply-rulesets` と同じ形、#707)。

```bash
~/.claude/skills/repo-charter/scripts/create-repo.sh \
  --owner <owner> --repo <repo> --description "<目的 1 文>" \
  --class <naming-クラス> --topic <topic> [--topic <topic2> ...] \
  [--lifecycle <lifecycle-timeboxed|lifecycle-study>] [--public] \
  --type <rust|typst|astro|core> --dest <ローカルの checkout パス> [-- <seed.sh のオプション>]
# まず --dry-run で、検査の結果と走らせるコマンドを確かめる
```

スクリプトは作成の**前に**手順 2 の閉じた語彙チェックを行い(ADR-0020)、通らなければ
`gh` を 1 回も呼ばずに止まる — `naming-codename` を選んだのにレジストリ未登録のまま
作成すると、直後の `github-audit naming` が `codename-not-registered` で即 drift 報告
する。リポジトリが既に存在すれば作成を飛ばして topic の反映と播種へ進むので、途中で
止まっても同じコマンドで再開できる。

**無料プランの非公開リポジトリ。** 所有者のプランが `free` で、リポジトリが非公開のとき、
自動マージと rulesets は使えない。`create-repo.sh` は所有者のプランを検出し(`--plan
auto|free|paid`、既定は `auto`)、該当すればトピック `plan-free-private` を播く。この宣言が
あると、`pr-title` の検査と `github-audit` は、成り立たない前提(自動マージの有効化、live の
branch ruleset)だけを外す。Team に切り替えたら宣言を外せば元に戻る(workflow の編集は不要)。
宣言が実態と食い違えば `plan-free-private-stale` で監査が検出する。判定の中身、宣言の付け方、
Team 切替の手順は `docs/agents/free-plan-declaration.md`。プランを検出できなかったときは注意が
出るので、無料の非公開リポジトリなら `--plan free` を付けて同じコマンドを再実行する(作成は
飛ばされる)。

既存リポジトリの適合化(新規作成ではない)は、従来どおり直接 `gh repo edit` する:

```bash
gh repo edit <owner>/<repo> --description "<目的 1 文>"
gh repo edit <owner>/<repo> --add-topic <naming-クラス> --add-topic <topic2>
```

`--description` は charter インタビューの目的 1 文と**一字一句**一致させる
(監査は正規化した文字列一致で判定する — `docs/github-audit.md`)。命名クラス
の topic(`naming-codename` 等、5 クラスのうち 1 つ)は必ず 1 つ、加えて
リポジトリの技術領域・ドメインを表す topic を最低 1 つ。手順 3 でライフ
サイクルトピック(`lifecycle-timeboxed` / `lifecycle-study`)を選んだ場合は
`--add-topic` にもう 1 つ追加する(ADR-0026、`naming-*` とは独立に 0〜1 個)。
README と CONTRIBUTING の正本言語を日本語にするなら、`--add-topic lang-ja` も
付ける(ADR-805)。

**メタデータを反映する時機(この規定が正本。`github-audit-triage` §6 の 6・§9 は参照する)。**
description と topics は README・CONTRIBUTING の鏡で、正本は README・CONTRIBUTING である。
既存リポジトリの適合化で README・CONTRIBUTING を PR で直すときは、**その PR が merge された後**に
`gh repo edit` を実行する。README の merge より前に鏡だけを書き換えると、メタデータと README が
食い違う状態が一時的にできる。例外は 2 つ。(a) 新規作成: `create-repo.sh` が作成時に topics を
付ける(README がまだ無いので、食い違う相手がいない)。(b) `naming-*` topic だけを足し、改名を
伴わず、対応する README の PR が無い場合: 待つ相手の PR が無いので、すぐ
`gh repo edit --add-topic naming-<クラス>` してよい。改名を伴う場合(`naming-pj` への移行など)は、
改名の PR の merge を待つ。

**新規作成の場合、続けて標準 governance を播く**(#153、
ADR-503)。`create-repo.sh --type …` がこれを行う(`gh` 自体には `repo create` 直後に
走るフック機構が無いため、この手順が事実上の自動適用になる)。以下はスクリプトが
内部で呼ぶ個々のコマンドで、スクリプトが失敗したときのフォールバック手順でもある。
required status check の正本は対象リポジトリ自身の `.github/rulesets/*.json` に
一本化されている(`apply-rulesets.sh` は型を引数に取らない)。リポジトリの
型が rust/typst/astro のいずれかで `repo-governance` に該当する profile を持つ場合:

```bash
~/.claude/skills/repo-governance/<rust|typst|astro-site>/scripts/seed.sh \
  --owner <owner> --repo <repo> --dest <ローカルの checkout パス> [エコシステム固有オプション]
```

(`seed.sh` が template ファイルのコピーと `.github/rulesets/*.json` の
apply を両方行う。まだ CI が 1 度も走っていないため apply は
`--unverified-contexts` で行われる — CI が 1 回走った後、
`apply-rulesets.sh <owner>/<repo> --reconcile` で検証付きに切り替える。)

いずれの `repo-governance` profile にも属さない場合(`core` 型、#337)の手順(settings → files →
rulesets の呼び出し順、`ci.yml`・`CI passed`・rulesets の宣言を同じ段に置くこと)は、
`repo-governance` SKILL.md の「Without a language profile (`core`)」節が正本である。
`create-repo.sh --type core` はその節の最初の 2 コマンドを呼び、失敗したときのフォールバック
もその節にある。ここには複写しない。続けて、作業先に**根コミット**まで作る(`root_commit`、F57): 作業先が git の作業ツリーでなければ
`git init -b main`、origin を **https** の URL で足し(SSH の URL で足すと、鍵の無い環境で push が publickey で落ちた)、
播種したファイルを 1 つのコミットにする。署名は利用者の git の設定どおりなので、**sandbox の外で**(署名の鍵が見える場で)実行する。
すでにコミットがあれば何もしない(続きから進められる)。push は、資格情報が要るので、案内(`next:`)に出すだけにする。
main への直コミットは、HEAD が未生成の間だけ pre-commit が通す(`docs/git-sync.md`)ので、`GIT_ALLOW_MAIN_COMMIT` は要らない。

review 層(Copilot code review + 会話 resolve 必須)は ADR-0021 のとおり
初期は付けない。開発初期フェーズを過ぎたら `--with-review` を付けて再実行する。

## 9. 自己検証

```bash
github-audit charters naming workflows rulesets
```

対象リポジトリが 4 ドメインとも `ok` と出れば完了。`drifted` の場合は
`missing=` の項目を読んで埋め直す(`docs/github-audit.md` に各項目の説明)。

`workflows` と `rulesets` は CI の構成を見る(ADR-1005)。`core` 型(言語別テンプレ
が無い)は、`ci.yml` が `ci-passed` だけの最小形なので `ci-gate-empty` が出る。
ADR-1005 D1 の基準 — ① 落ちたまま main に入ると main の不変条件(ビルド・テスト・
整形・秘密なし等)が壊れる job だけを `ci.yml` に足し、② flaky・外部依存・p75 10 分
超の job は `ci.yml` の外へ置く — を読んで、足す job を決める。足す job が今は無い
リポジトリ(文書だけ等)は、exempt にする(`github-audit-triage` の三択)。足したら
`ci-passed.needs` にも入れる。

## 10. 既存 Issue への適用(適合化のとき)

既存リポジトリに charter を播いた直後は、居座っている open Issue の中に
CONTRIBUTING.md `## Issues` の棄却例に該当するものがないか一度だけ棚卸しする。
該当する Issue は「`## Issues` の棄却例(<該当する棄却例>)に該当」という
理由をコメントして close する。理由を書かずに close しない — 後から見た人が
「なぜ切られたか」を charter に立ち戻って再確認できることが目的。

## 11. 一括適合化が必要なとき

多数のリポジトリが同時に drift しており 1 リポジトリずつのインタビューでは
収束しない場合は、監査駆動で一括起草・一括レビューする
`github-audit-triage` スキルを使う(このスキルのスキーマ定義を正本として
参照する)。

事例は `cases.md` を参照。追記時のサニタイズ規則は `agent-tooling-authoring` を参照。
