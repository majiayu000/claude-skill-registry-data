---
name: github-audit-triage
description: github-audit(統合 6 ドメイン監査)が報告した drift を入力に、LLM で複数リポジトリの findings を一括起草し、1 回の一括レビュー(GO/修正/除外/exempt)を経て一括 PR 化する手順(ADR-0015 の LLM ノード)。charter 一括整地・drift まとめて直す・naming/settings/renovate 一括対応・全リポ横断で直す・github-audit-triage、といった依頼で使う。bulk remediation across repos, triage audit findings, apply drift fixes across repositories、といった英語の文脈でも使う。1 リポだけを対話で適合化する場合は repo-charter を使う — こちらは横断監査の findings をまとめて消化する側。
---

`github-audit` は読み取り専用で drift を報告するだけで、直すのは
`repo-charter` の 1 リポジトリずつの対話型インタビュー(charters/naming)や
`repo-governance` スキル(settings/renovate/rulesets)しかない。多数の
リポジトリが同時に drift している状態では、「次に触るタイミングで個別
retrofit」は事実上収束しない。このスキルは、監査の findings を入力に LLM が
複数リポジトリぶんの修正を一括起草し、人間の確認は 1 回の一括レビュー(表)に
絞ることで、個別インタビューの質を落とさずに収束させる。ADR-0015 が定義する
判断ループの LLM ノードはここだけであり、`github-audit` 自体は LLM を呼ばない。

設計根拠は `docs/agents/github-audit-triage.md`。前身の charter-sweep
(#180)の設計(低確信フラグ・exempt 処分・self-verify)を継承しつつ、
完了定義を「PR 作成まで」に変更して巻き取っている — charter-sweep は
merge・merge 後のメタデータ反映まで自動で行っていたが、それは人間裁定を
経ない正本への書き込みであり ADR-0015 のループ設計と矛盾するため廃止した。

`repo-charter` / `repo-governance` との役割分担: このスキルは複数リポジトリ
ぶんの**起草と一括レビューの取りまとめ**を担う。README/CONTRIBUTING のスキーマ
定義・見出しリテラル・settings/renovate の基準値は `repo-charter` SKILL.md・
`repo-governance` SKILL.md と言語ごとの reference を正本として常に参照する(二重定義しない)。

## 1. 入力の取得

セッション冒頭で `github-audit --json` を**新規実行**する(state の
`ledger.json` はいつ生成されたか分からないため読まない)。ユーザーが対象
ドメインを指定していれば `github-audit <domain...> --json` に絞る。
`verdict` が `drifted` または `ungoverned` のリポジトリ×ドメインの組が
作業リストになる。

対象 owner が個人アカウント以外(org)のときは、実行の前に
`~/.config/github-audit/<org>/overrides.tsv` の有無を確かめる。あれば
`GITHUB_AUDIT_OWNER` / `GITHUB_AUDIT_VIEWER_PERMISSION` とあわせて
`GITHUB_AUDIT_OVERRIDES_FILE=<そのパス>` で渡す。渡さないと、過去に exempt
裁定済みの組が drifted として再び出る(#708)。

**起草に入る前に、`drifted` の種類(domain と token)ごとに 1〜2 件を、API の一次情報で
読み戻して偽陽性でないことを確かめる。** 監査の出力を信じて起草に進むと、偽陽性や
直せない要求に起草を費やす(2026-10-17 の監査では、drifted と ungoverned の 126 組の
約半分がこれだった。#838)。確かめ方の例:

- settings: `gh api repos/O/R/automated-security-fixes` で実際の状態を読む(Rust 版が
  非公開リポジトリのフォールバックを持たず、実際は無効のものが drifted と出ることがあった)
- rulesets: live と宣言を正規化して diff する(GitHub がサーバ側の既定値で埋める 1 項目
  だけの差を、差として出すことがあった)
- 全般: そのリポジトリが読み取り専用(アーカイブ済み)でないか。アーカイブ後はトピック等を
  書き換えられず、`class-undeclared` のような要求は直せない

偽陽性が見つかったら、起草ではなく監査の修正に回す(既存 Issue の有無を先に確かめる)。

## 2. 一括起草

drifted な (repo, domain) の組ごとに background subagent へ委譲する。各
subagent は `gh api`(README/CONTRIBUTING/AGENTS.md/CLAUDE.md の raw・
description・topics・settings フィールド・ファイルツリー・open Issue 一覧)
だけを読み、**clone しない**。

- 起草するのは `missing=` に挙がった項目のみ(最小差分)。ただし charters
  ドメインで purpose 文・見出しスキーマ・CONTRIBUTING の Issues 節
  (judging question / Accepted / Rejected、ADR-0017)のいずれか 1 つでも
  欠けている場合は、矛盾なく整合させた 1 セットとして起草する(purpose 文
  だけ直して Scope と噛み合わなくなる、という事故を避けるため)。
- README/CONTRIBUTING のスキーマ・見出しリテラル・禁止事項(時限記述・
  Issue 番号焼き込み・長文弁明の禁止)は `repo-charter` SKILL.md §2〜3 の
  テンプレートをそのまま使う。**品質ガードレールを外して急がない** —
  ここで規範から外れた起草をすると、次の監査サイクルでまた drift として
  戻ってくるだけで何も収束しない。
- naming ドメインの `class-undeclared`/`class-ambiguous`/`pattern-mismatch`
  は、自由裁定ではなく**盲再導出(ADR-0021)**で提案する — subagent には
  対象リポジトリの実際の名前を伏せた状態で README・ファイルツリー・open
  Issue だけを渡し、「本 ADR の語彙・文法のみで命名するなら何と付けるか」
  (クラス + 規範名)を導出させてから、実名を開示して一致度を報告させる。
  表には「導出クラス / 導出名 / 実名 / 一致度 / 処分案」を書く。処分案は
  高一致なら「宣言のみ」、不一致なら「改名 + 宣言」。`naming-codename` を
  提案する場合は、`config/github-audit/codename-registry.tsv`(PUBLIC)
  または `~/.config/github-audit/codename-registry.local.tsv`(PRIVATE、
  dotfiles には書かない)への追記案も併記する。**閉じた語彙(species set・
  命名クラス等)を既存の実データから帰納的にシードするときは、トークン
  単体の語感だけで採否を判定しない — 必ず対応する README・Scope・
  ファイル構成を読んでから確定する**(#232: 語感で「恒久的な主題」と
  誤認した末尾トークンが、実際には「完了・凍結した研究アーカイブ」の
  主題名に過ぎなかった事例がある。閉集合が際限なく増える設計は ADR-0020
  自体の目的と矛盾する)。
- rulesets ドメインの `ci-absent` は、リポジトリごとに
  {最小 CI 播種 PR / CI 播種を促す誘導 Issue の起票 / exempt} の三択を
  提案する(ADR-0021)。コードを持つリポジトリは播種 PR、記録・ノート系は
  exempt、判断が割れる場合は Issue 起票を既定の推奨にする。
- settings/renovate ドメインは、対象の言語の `repo-governance` スキル(profile)の
  `apply-repo-settings.sh` / renovate テンプレートをそのまま適用する提案
  として表に書く。`auto-merge-disabled` / `dependabot-security-updates-
  enabled`(docs/adr/568-renovate-automerge-shared-preset.md D2/D5b)は
  `apply-repo-settings.sh --owner <owner> --repo <repo>` の再実行で両方
  一度に直る。`renovate-policy-preset-missing`(同 ADR D4)は対象 repo の
  `renovate.json` の `extends` に `github>tarotene/dotfiles//renovate/
  policy` を追記する提案にする — テンプレート全体で上書きしない(repo
  固有の `packageRules` を消さないため)。
- titles ドメイン(ADR-0031、#337)は `missing` トークンごとに機械的に
  決まる:
  - `pr-title-workflow-missing` — `.github/workflows/pr-title.yml`
    (dotfiles の composite action を呼ぶ caller。reusable workflow を呼ぶ
    旧形は ADR-591 D3 で退役し、`legacy-reusable-pr-title-call` が検出する)
    が無い。対象リポジトリの
    言語に対応する `repo-governance` の profile があれば、その
    `copy-files.sh` を(`--owner`/`--repo` のみ渡し、他フラグは
    テンプレート適用に必要な最小限)実行する提案を表に書く。対応する
    profile が無いリポジトリ(`core` 型。`repo-governance` SKILL.md の
    「Without a language profile (`core`)」)は
    `repo-governance-common/templates/.github/workflows/pr-title.yml`
    (単一正本、rust/typst/astro-site の 3 profile はこのファイルへの symlink)
    をそのまま `.github/workflows/pr-title.yml` にコピーする提案にする。
  - `pr-title-check-not-required` — 対象リポジトリの ruleset に required
    check context の完全一致(`"PR title"` または `"PR Title / PR title"`
    のいずれか)が無い(ADR-0031 2026-09-26 Amendment で完全一致化。旧・
    接尾辞後方一致の判定は #337 の事故 — 呼び出し側 job に `name:` が無い
    テンプレートの実際の check 名 `"check / PR title"` を誤って ok と
    判定し続けていた — を受けて廃止した)。対象リポジトリに
    `.github/rulesets/quality.json` 宣言が無ければ、対応する
    `repo-governance` skill の言語 profile(rust/typst/astro-site)の `copy-files.sh` または
    `core` 型(`repo-governance` SKILL.md の「Without a language profile (`core`)」)の
    `copy-files.sh` で宣言を播く提案を先に書く
    (ADR-503、`rulesets-declaration-missing`
    が該当)。宣言は既にあり live だけが古い場合は、
    `apply-rulesets.sh <owner>/<repo> --reconcile` を適用する提案として
    表に書く(`--reconcile` が無いと既存 ruleset は skip されて追加されない、
    #337 で判明。型を問わず同じ汎用スクリプト 1 本)。**dotfiles 自身と
    同じ手動 `gh api PUT` は使わない** — `crates/rulesets-write-guard` が
    deny する。
  - `pr-title-context-mismatch` — ruleset の required context 文字列は
    正しいが、最新の `pr-title.yml` run が実際に報告した job 名と一致しない
    (ground-truth 突き合わせ、ADR-0031 2026-09-26 Amendment)。原因は
    ほぼ必ず呼び出し側テンプレートの job に `name: PR Title` が無いこと
    (現行テンプレートは固定済みなので、播き直し後の初回 run では発生
    しないはず)か、旧型の別 PR タイトル検査ワークフローが残っていること
    (下記)。提案は「呼び出し側 job の `name:` をテンプレートに合わせて
    追加する PR」または「旧型 workflow の置換 PR」のいずれか、原因に応じて
    起草時に判別する。
  - 上記いずれか 1 つだけが立っている場合(caller はあるが required
    check だけ足りない、context だけ mismatch、等)は、該当する提案だけを
    表に書けばよい — 複数を揃えるための追加確認は不要(rulesets ドメインの
    `review_layer=partial-drift` と違い、これらのトークンに解釈の分岐は
    無い)。
  - 旧 `amannn/action-semantic-pull-request` 等、別の PR タイトル検査
    ワークフローが既に存在するリポジトリ(ADR-0031 D2 追補の訂正
    参照、2026-09-24)は、置き換え(旧 workflow ファイルの削除 + 旧
    context 名を required check から外す)を提案に含める — 追加ではなく
    置換であることを起草の時点で明記する。
- charters ドメインで `nav-doc-*` トークン(ADR-0033)が立った場合、当該
  ファイル(README.md / CONTRIBUTING.md / AGENTS.md / CLAUDE.md)を
  fetch して人間の目で読み、次の 3 種をまとめて起草する(決定論
  チェックが取れるのは前 2 つだけなので、機械フラグが 1 つでも立った
  ファイルは、フラグの立った箇所に留めず**ファイル全体**を読んで
  3 種目(転記)も併せて拾う — `repo-charter` SKILL.md §4a の判定軸
  「情報の寿命」で 1 箇所ずつ判定する):
  1. `nav-doc-tree-fence` / `nav-doc-path-inventory` が挙がった節 —
     ディレクトリ構成図・手書き一覧を削除し、運んでいた役割説明を
     実体の隣(`<dir>/README.md` の冒頭 1 文、無ければ新設)へ移す。
     生成物・第三者素材の帰属注記(ADR-0028)など意図的に残す一覧は、
     削除ではなく直前に `<!-- nav-doc-exempt: <check> — <理由> -->`
     を足す(理由は具体的に — 「必要だから」のような同語反復は書かない)。
  2. `nav-doc-exempt-malformed` — マーカーの書式(`<check> — <理由>` の
     両方が要る)を直す。何を exempt しているか不明な場合は、マーカー
     ごと削除して該当ブロックも上記 1 と同様に処理する。
  3. `nav-doc-exempt-unused` — マーカーを削除する(exempt しなくても
     drift しない箇所に残す理由がない)。
  4. 他ファイルの中身の転記(YAML/JSON スキーマ・設定値・CLI 使用法
     など、機械検査の対象外)— 転記元ファイルと突き合わせ、字面が
     一致しているか・古くなっているかに関わらず削除し、転記元への
     1 行ポインタに置き換える。転記元ファイル自身に説明が無い場合は、
     ポインタを書く前に転記元へ最小限の説明を足す(情報を消すだけで
     終わらせない)。
  charters の要約欄には「nav-doc: <削除した節数> 節削除、<新設した
  `<dir>/README.md` 数> 件新設」のように定量的に書く。
- rulesets ドメインは `review_layer`(ADR-0021)を読んで扱いを分ける。
  `missing` のコア層項目(`deletion`/`pull_request.allowed_merge_methods`
  等)は `apply-rulesets.sh <owner>/<repo> --reconcile`(型を問わず同じ
  汎用スクリプト、宣言済みのコア 3 ファイルのみ)適用提案として表に書く。
  `review_layer=partial-drift`(`missing` に `review_layer.*` が立つ)は、
  対応する skill の `copy-files.sh --with-review` で `review.json` 宣言を
  足してから apply するか、`apply-rulesets.sh <owner>/<repo>
  --delete-ruleset Review`(宣言から `review.json` を先に外しておく必要
  がある)で剥がすかの二択として表に書き、低確信フラグ相当として
  **起草せず人間裁定に回す**(片方だけ入った経緯が読み取れないため)。
  `review_layer=absent` は drift ではないので表に出さない — 既存の低速
  シグナル(`ungoverned`)と同様、レビュー層は opt-in であって欠落ではない。
  `rulesets-declaration-missing`(宣言そのものが無い)・
  `rulesets-declaration-drift:<name>`(宣言 ≠ live)・
  `required-context-unreportable:<context>`(live の context がこの
  リポジトリのどの job も報告しない)は
  ADR-503 で追加された機械判定 — それぞれ
  「該当 skill の `copy-files.sh` で宣言を播く」「`apply-rulesets.sh
  --reconcile` で live を宣言に合わせる」「宣言または対象リポジトリの
  workflow のどちらを直すべきかを人間裁定に回す」提案として表に書く。
- workflows ドメイン(ADR-591、docs/adr/591-ci-workflow-naming.md)は
  `missing` トークンごとに機械的に決まる。`ci.yml` は対象リポジトリ
  固有の実ステップを持つため titles ドメインの `pr-title.yml` と違い
  **丸ごとテンプレートで上書きしない** — 既存の job 本体(ステップ)は
  そのまま残し、構造(集約 job・`needs:`・`name:` 大小文字)だけを
  外科的に直す。
  - `ci-yml-missing` — 対象リポジトリの言語に対応する `repo-governance`
    の profile があれば、その `<profile>/templates/.github/workflows/ci.yml` を土台に
    `# ADJUST:` 箇所を埋めて起草する。対応する profile が無い(`core` 型。
    `repo-governance` SKILL.md の「Without a language profile (`core`)」)場合は
    言語別のテンプレートが無いので低確信フラグに回す(§3)。分割された workflow(`fmt.yml`・`test.yml` など)が既にある
    リポジトリは、それらを `ci.yml` に統合する。このとき既存 job の
    `name:` は変えない: live の ruleset の必須 check は旧 job 名のままで、
    名前を変えると reconcile の前に必須 check が「Expected」のまま PR を
    止める(#337 の循環)。`ci-passed.needs` は統合後の実在する job id を
    漏れなく列挙する。
  - `file-not-yml:<name>` / `file-not-kebab:<name>` — 該当ファイルを
    `.yml` 拡張子・kebab-case にリネームする(内容は変更しない)。
  - `workflow-name-missing` / `workflow-name-lowercase` — `ci.yml` 先頭の
    `name:` を追加・先頭大文字化する(sentence case、`CI`/`PR`/`MSRV` 等の
    固有表記はそのまま保持)。
  - `ci-passed-job-missing` — 対象リポジトリの `ci.yml` に集約 job
    `ci-passed`(`name: CI passed`)を追加する。job 本体はいずれかの
    `repo-governance` の言語テンプレート(または本リポジトリ自身の
    `.github/workflows/ci.yml`)の `ci-passed` job をそのまま流用する
    (`needs:` を除き全リポジトリでバイト同一)。`needs:` には対象
    リポジトリの `ci.yml` に実在する job id を(`ci-passed` 自身を除き)
    漏れなく列挙する。
  - `ci-passed-needs-missing` / `ci-passed-needs-incomplete:<job-id>` —
    既存の `ci-passed` job の `needs:` 配列に、抜けている job id を
    追加する(他の job には触れない)。
  - `ci-passed-not-always` / `ci-passed-failure-step-missing` — `ci-passed`
    job の形が ADR-591 D1/D3 から外れている(ADR-1005 D6)。前者は job 直下に
    `if: always()` を足し、後者は `steps:` に失敗判定 step
    (`if: contains(needs.*.result, 'failure') || contains(needs.*.result,
    'cancelled')` / `run: exit 1`)を足す。形は
    `repo-governance-common` 以外の `repo-governance` の言語テンプレートの `ci-passed`
    と同一で、他の job には触れない。
  - `ci-gate-empty` — `ci.yml` に gate job(`ci-passed` 以外の job)が 1 つも無い
    (監査だけの finding、ADR-1005 D7)。`ci-absent` と同じく、{gate job を足す
    PR / 誘導 Issue の起票 / exempt} の三択を表に書く。足す job は ADR-1005 D1 の
    基準で決める — ① 落ちたまま main に入ると main の不変条件(ビルド・テスト・
    整形・秘密なし等)が壊れる job だけを足し、② flaky・外部依存(共有キュー・
    外部 API・時刻)・p75 10 分超の job は足さない(`ci.yml` の外へ置く)。
    どの job が①に当たるかは、リポジトリの中身を読んで人が決める(低確信フラグ、§3)。
  - `advisory-workflow-no-push:<file>` — `ci.yml` の外の検査 workflow が PR では
    走るのに既定ブランチへの push で走らない(ADR-1005 D3)。処分は 2 つ。
    ADR-1005 D1 ① を満たす(落ちたまま main に入ると main の不変条件が壊れる)なら
    `ci.yml` に移し、`ci-passed.needs` に足す。そうでなければ `on:` に `push:`
    (`branches: [<既定ブランチ>]`)を足して main でも走らせ、`default-branch-run-failed`
    で拾えるようにする。PR の番号や本文を使う補助(プレビュー・コメント)は、検出の
    時点で除かれている。
  - `default-branch-run-failed:<file>` — その workflow の既定ブランチでの最新の完了 run
    が失敗している(ADR-1005 D4)。構造の drift ではなく、直すのは workflow の中身
    (または環境)なので、表では「失敗の run の URL と原因」を書き、一括修正の
    対象にせず個別の Issue か PR に回す。
  - `gate-job-slow:<job>` / `gate-job-flaky:<job>` — `gate-health` ドメイン
    (明示指定でだけ走る opt-in、ADR-1005 D5)。`ci.yml` の job が、ADR-1005 D1 ②
    の除外条件に当たっている。`slow` は直近の成功 run の p75 が 10 分超、`flaky` は
    同じ head SHA で失敗と成功の両方を出した。処分は、{`ci.yml` の外へ出す(workflow を
    分け、`ci-passed.needs` から外し、main への push でも走らせる)/ job を分割して
    p75 を縮める / flaky の原因を直す}。どれにするかは job の中身を読んで人が決める
    (低確信フラグ、§3)。job 名は matrix の展開後の名前なので、`ci.yml` の `name:` と
    一致しないことがある。
  - `job-name-missing:<job-id>` / `job-name-lowercase:<job-id>` — 該当
    job に `name:` を追加・先頭大文字化する(意味を変えない範囲の
    sentence case)。
  - `quality-json-not-canonical` — 対象リポジトリの `.github/rulesets/
    quality.json` の `required_status_checks` を、
    `repo-governance-common/templates/.github/rulesets/quality.json`
    (単一正本)と同じ `[{"context":"CI passed","integration_id":15368},
    {"context":"PR title","integration_id":15368}]` に更新する提案を
    表に書く。GO 後、PR の作成(§6)に続けて `apply-rulesets.sh
    <owner>/<repo> --ref <このPRのブランチ> --verify-sha <このPRの head
    SHA> --reconcile` を実行する — **`--ref main`
    や省略値では未マージの宣言・実測が読めず必ず失敗する**(実測: PR
    作成直後は `CI passed`/`PR title` 自体がまだ report されておらず
    `--verify-sha` に PR の最新 head を明示しないと「required context が
    走っていません」で拒否される、grill-me セッション 2026-09-30)。
    reconcile は対象リポジトリの他の open PR にも影響する外向き操作
    なので、一括レビュー表の段階でどのリポジトリに reconcile を伴うかを
    明記し、実行前にユーザーに確認する。
  - `legacy-reusable-pr-title-call` — `.github/workflows/pr-title.yml`
    を `repo-governance-common/templates/.github/workflows/pr-title.yml`
    (単一正本)でまるごと置き換える(titles ドメインの
    `pr-title-workflow-missing` と同じ扱い — この 1 ファイルは元々
    リポジトリ固有の中身を持たない)。**同じ PR で、`.github/rulesets/
    quality.json` の宣言が無いリポジトリには宣言を播く**(対応する
    `repo-governance` の言語 profile の `copy-files.sh`、無ければ `core` 型として
    `repo-governance` SKILL.md の「Without a language profile (`core`)」の `copy-files.sh`
    (`repo-governance-common/templates/.github/rulesets/` を播く))。live の ruleset
    が旧 context `PR Title / PR title` を必須にしている repo では、置換した瞬間
    head がその context を報告しなくなる。宣言が無いと `apply-rulesets --ref
    <branch> --verify-sha <head> --reconcile` で live を直す正本が無く、PR が
    緑にならない(workflows ドメインは「宣言があれば比較」なので、宣言の欠落は
    ここでは検出されない)。順序は PR 作成 → head で新 context の報告を待つ →
    reconcile → `PR title` の再実行 → merge(ADR-591 D8)。
  - **rollout PR の `PR title` は reconcile まで必ず赤い(#744)。** live の
    ruleset がまだ旧 context `PR Title / PR title` を必須にしていると、
    head はその context を報告しないので、撒いた直後の PR は全部 `PR title`
    が赤になる。ADR-591 D8 の設計どおりで、壊れているのではない。本人が
    「どの PR も CI が full pass していない」と受け取った実例(2026-10-06、
    9 本)があるので、次を一続きの手順にする:
    1. 一括レビュー表と**各 PR 本文の `## 要確認`** に、「作成直後の `PR title` の赤は
       reconcile 待ちで想定内」と書く。
    2. PR 作成後、head で新 context の報告を待つ。
    3. `apply-rulesets.sh <owner>/<repo> --ref <ブランチ> --verify-sha <head>
       --reconcile --dry-run` を実行し、**宣言と live の required context の差分**
       (`-` が live にだけある旧 context、`+` が宣言にだけある新 context)を
       PR 本文に貼る。別の比較スクリプトは要らない。
    4. 本人の GO(reconcile は他の open PR にも影響する外向き操作)で
       `--dry-run` を外して reconcile し、`gh run rerun` で `PR title` を
       再実行して、緑になったことを読み戻してから報告する。
  - `ci-yml-unreadable` は fetch 失敗によるものなので起草せず低確信
    フラグに回す(§3)。
- docs ドメイン(ADR-640、docs/adr/640-stack-standard-api-docs.md)は
  「そのスタックの標準 API doc を strict にビルドする job を `ci.yml` に
  置き、`ci-passed.needs` に入れる」までが一続きの修正。`workflows`
  ドメインと同じく `ci.yml` は丸ごと上書きせず、job の追加と `needs:` の
  追記だけを外科的に行う。`missing` トークンごとに:
  - `docs-absent:<stack>` — `ci.yml` に次の job を追加し、`ci-passed.needs`
    に job id を足す。`<stack>` は `rust` / `python` / `typescript` で、
    `uses:` の action 名は `docs-<stack>`:
    ```yaml
      docs:
        name: API docs
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@<既存 job と同じ SHA>
          - uses: tarotene/dotfiles/.github/actions/docs-<stack>@main
            with:
              upload: 'false'
    ```
    スタックを複数持つリポジトリは job id を `docs-<stack>` で分ける。
    `repo-governance` の rust profile テンプレート(`repo-governance/rust/
    templates/.github/workflows/ci.yml`)の `docs` job が実例。
  - `docs-wrong-ref:<stack>` — `uses:` の参照を `@main` に直す(他の行は
    触れない)。SHA や tag に固定しているのは意図的な pin の可能性が
    あるので、変更理由が読み取れなければ低確信フラグに回す(§3)。
  - **既存の doc 警告の修正も同じ PR に含める。** strict ビルドは
    `-D warnings` / `sphinx-build -W -n` / `--treatWarningsAsErrors` なので、
    これまで警告を抱えていたリポジトリは job を足すだけでは `CI passed` が
    赤くなる。起草の前に、対象リポジトリで同じコマンドを手元で実行して
    (`RUSTDOCFLAGS="-D warnings" cargo doc --no-deps --workspace` など、
    `.github/actions/docs-<stack>/action.yml` のコマンド)警告の有無を確認し、
    見つかったものは doc コメントの修正として同じ PR に入れる。警告が
    多数(目安: 20 件超)で機械的に直せない場合は、起草せず低確信フラグに
    回す(§3)— 警告を `#[allow]` や lint 無効化で黙らせない。
  - python では `docs/conf.py` が無くても job は動く(action が
    `sphinx-apidoc` で最小構成を生成する)ので、Sphinx の設定ファイルを
    新規に起草しない。docstring の相互参照が nitpicky(`-n`)で警告に
    なる場合は、参照を直すか `docs/conf.py` に `nitpick_ignore` を足す。
  - 公開(Pages)は別の判断で、`missing` には出ない。**PUBLIC かつ
    docs.rs / pkg.go.dev の対象外**(crates.io 未公開の Rust、PyPI/npm 公開の
    有無は問わない)のリポジトリに限り、`repo-governance-common/templates/
    .github/workflows/docs-pages.yml` を `__DOCS_ACTION__` / `__DEFAULT_
    BRANCH__` を置換して `.github/workflows/docs-pages.yml` にコピーする
    提案を、表の「処分案」に**選択肢として**書く(既定では提案しない —
    公開は取り消しづらい外向きの操作なので、一括レビューで GO が出た
    ものだけ)。Settings → Pages の Source を「GitHub Actions」にする
    手順は人手の作業なので、後続 Issue に払い出す(PR 本文の `## 要確認`
    にはそのポインタだけを書く)。`docs-linkcheck.yml`(週次の外部リンク
    検査)も同様に、docs job を足すリポジトリに任意で付ける提案にする。
  - `private-pages-enabled` — PRIVATE リポジトリで Pages が有効。個人
    アカウントでは private repo の Pages も公開されるので、**起草では
    直せない**(Settings → Pages の操作)。**推奨を決める前に、公開が意図的かを
    確かめる**: README の目的文と、Pages を配信するワークフロー(`build_type`、
    `docs-pages.yml` など)を読み、公開が成果物の目的(例: 本として配信)かを見る。
    意図が読み取れれば、推奨は `exempt`(§7)にする。読み取れないときだけ、表に
    「Pages を無効化する」を処分案として書き、実行はユーザーに依頼する(外向きの
    設定変更で、公開済みの内容を取り戻せるわけでもない)。質問には、読んだ根拠
    (どのファイルの何行目か)を添える。依頼の手順は後続 Issue に払い出す(#837)。
  - `not-applicable` のスタック(Astro サイト・Nix・Go・Typst・GAS・設定のみ)
    には何も提案しない。`package.json` が `exports`/`main`/`types` を
    持つのに API doc が不要なライブラリ(内部ツールなど)は、`exempt`
    (§7)で理由付きに外す。

## 3. 低確信フラグ(起草しないレーン)

次のいずれかに該当するリポジトリ×ドメインは起草せず、「`repo-charter` の
個別インタビュー送り」として一括レビュー表に列挙するだけにする:

- リポジトリ名と中身から読み取れる責務が食い違う(naming クラス裁定が
  改名を要する可能性がある場合を含む)
- open Issue が、そのリポジトリの目的そのものを争っている(何を作るか自体が
  未決着)
- 中身(README・コード構成)から目的文・命名クラスを一意に確定できない
  (空・スタブリポジトリを含む)

これらは `docs/agents/repo-charter.md` の pilot retrofit で改名級の構造
問題が見つかった実績がある領域であり、機械起草に任せず人間の対話に残す。

## 4. 一括レビュー表と GO 確認(1 回だけ)

drifted な組全体を、chat 本文の表ではなく **`Artifact` ツールで HTML
として** 提示する(`artifact-design` スキルに従う)。ファイル名は
`github-audit-triage-review.html` のようにスキル名をプレフィックスにし、
セッション内で最初に一度だけ publish する。表の列は:

| repo | domain | 提案内容の要約 | 処分案 |
|---|---|---|---|

charters ドメインは「起草した purpose 文 / Scope 要約 / judging question」
に加え、`nav-doc-*` が起因の場合は「nav-doc: <削除した節数> 節削除、
<新設した `<dir>/README.md` 数> 件新設」(§2 参照)を併記する。naming は
「提案クラス」、settings/renovate は「適用するテンプレート差分」、docs は
「追加する job / 修正する doc 警告の件数 / Pages deploy を併せて提案するか」
を要約欄に書く。低確信フラグの組は要約欄を空にし、処分案を「repo-charter へ
送る」と書く。ユーザーはリポジトリ×ドメイン単位で **GO / 修正 / 除外 /
exempt** を返す。確認はこの 1 回だけで、GO 後は項目ごとに止まらない
(`my-cleanup` と同じ「一括 triage → GO 1 回 → 一括処理」の型)。

review artifact は **GO 待ちの間も GO 後も編集しない** — 承認時点の
スナップショットとして凍結する。GO 後に判明した訂正・実際の適用結果は
§6 の作業記録 artifact(別ファイル・別 URL)に書く。同一ファイルを
上書きすると、GO を出した時点で何を承認したかという決定記録が消える。

## 5. Issue 棚卸し(charters ドメインで GO が出たリポジトリのみ)

起草時に、そのリポジトリの open Issue を新しい CONTRIBUTING の Issues 節
(ADR-0017)の Rejected 例へ照らし、合致するものを表の「close 候補 Issue」欄
(charters 行にのみ追加)に挙げておく。**close するのは GO が出た後のみ**。
close するときは、合致した Rejected 例を名指しするコメントを必ず付ける
(理由なし close は禁止 — `repo-charter`
SKILL.md §9 と同じ作法)。

## 6. 一括適用(GO 分のみ、リポジトリ×ドメインごとに)

1. scratchpad へ shallow clone(`git clone --depth 1`)。この clone は
   main-checkout-guard(ADR-705)の言う「本物の checkout」なので、**読み取り
   だけ**に使う(編集・commit は deny される、#734)
2. `herdr worktree create --cwd <clone> --branch <名前>` で worktree を切り、
   以降はその `checkout_path` で対象ドメインの修正を適用する。worktree の
   土台は親 clone の HEAD なので、clone 直後の既定ブランチの先頭であることを
   `git merge-base --is-ancestor origin/<default> HEAD` で確かめる
3. commit → push → `gh pr create`(そのリポジトリの PR 本文規約に従う。
   このリポジトリ自身が対象なら `pr-description` スキルの 5 節スケルトン)
4. **merge はしない。PR 作成までがこのスキルの完了定義**(ADR-0015 —
   人間裁定なしの merge・メタデータ反映は正本を直接書き換えることになり、
   判断ループの設計と矛盾する)。ruleset で CI 待ちになるリポジトリも、
   単に「PR 作成済み、merge 待ち」として最終報告に列挙するだけでよい。
   rulesets の適用(`apply-rulesets.sh ...`)は rulesets-write-guard の対象外で、
   `RULESETS_WRITE_GUARD_ALLOW=1` を前置してはいけない — auto モードの分類器が
   safety bypass と判定して拒否し、適用が止まる(#707)。素のコマンドで実行する。
5. 一括適用が完了したら、**別ファイル**(`github-audit-triage-record.html`
   のように review とは異なるファイル名 → 別 URL)で作業記録 artifact を
   新規 publish する。中身の骨子:
   - 先頭に「今すぐ確認してほしいこと」ブロック — まだ merge していない
     PR 等、ユーザーの判断が要る項目へのリンクを最優先で置く
   - ドメイン別の適用サマリ(件数・self-verify 結果)
   - セッション中に見つかった問題とその対処(解決済み/持ち越しを明記)
   - 次回セッションへの持ち越し事項
   - review artifact への相互リンク
   両 artifact とも private リポジトリ名を含むため既定非公開のまま
   (docs には残さない、§9 参照)。favicon は review と record で区別
   できるものを選ぶ。
6. charters ドメインの description/topics 反映(`gh repo edit`)、naming
   ドメインの `naming-*` topic 反映も、`repo-charter` SKILL.md §8 の
   「メタデータを反映する時機」の規定(正本)に従い、**該当 PR が merge された後**に
   人間が個別に行う(この段階では行わない)。naming ドメインで改名を伴わず、
   対応する PR が無い場合(盲再導出の一致度が高く、宣言のみで済む場合)は、
   同じ規定の例外のとおり GO 直後に `gh repo edit --add-topic naming-<class>` を
   直接実行してよい。

## 6a. サブエージェントへの委譲の運用(複数リポジトリを並列で回すとき)

**書き込みの委譲は例外である。** 既定は本線が順に回す(本人の指示 2026-11-08、#1394。払い出すたびに文脈の
受け渡し・中断の再開・結果の読み戻しが要り、全体では効率が落ちた)。この節は、利用上限(HTTP 429)に近く
本線で回し切れないときなど、例外として委譲するときの運用を定める。§2 の起草のような読み取りだけの調査は、
本線を止めないために委譲してよい。

暗号化資料が必要な場合、指示に「復号・PIN 入力・復号ラッパーを実行せず、
必要な暗号文のパスと箇所を本線へ返す」と含める。本線が必要範囲だけを渡し、
取得できなかった部分は未確認として扱う。委譲先へ復号の再試行を指示しない。

`my-cleanup` §7 も同じ運用に従う(#735)。10 repo ぶんを 10 本のサブ
エージェントに 1 度に渡したところ、セッション上限で 3 件が commit も push も
無いまま止まり、作業が残らなかった実例がある。

- **波に分ける。** 1 度に起動する並列数は 4 件以内にし、波が終わってから
  次を起動する。
- **止まる前に残す。** 各担当に「止まる前に commit と push を済ませる」
  「途中の状態(clone・worktree・ブランチ・PR)があれば作り直さず再利用する」
  を指示に含める。
- **指示をファイルに置く。** 共通の指示は scratchpad のファイルに書き、
  担当ごとの指示はそのファイルへのポインタ + 担当固有の値(repo・ブランチ名)
  だけにする。再起動のときも同じファイルを指せば足りる。

## 6b. rulesets ドメインの ci-absent 適用(GO 分のみ)

- {最小 CI 播種 PR} 選択: 対象リポジトリに最小の CI ワークフローを追加する
  PR を、そのリポジトリの通常の PR フローで作成する(merge は待つ —
  §6 4 と同じ完了定義)。
- {誘導 Issue の起票} 選択: 対象リポジトリに CI 播種を促す Issue を起票する
  (attribution フッター必須)。self-verify では「Issue 起票済み・追跡中」
  として報告する(ADR-0021)。
- {exempt} 選択: §7 の overrides.tsv に追記する。

## 7. exempt 処分

一括レビューで「このリポジトリ×ドメインには基準を適用しない」と裁定された
組は、`$XDG_CONFIG_HOME/github-audit/overrides.tsv` に
`<repo>\t<domain>\texempt` を追記する(`*` ドメインで全ドメイン免除も可、
`docs/github-audit.md` 参照)。

## 8. self-verify

最後に `github-audit`(対象にしたドメインのみでよい)を再実行し、次の
いずれかで全対象が説明できることを確認して報告する:

- `ok`(今回 PR 作成済み、または既に merge 済みで再監査に反映)
- `exempt`(今回除外)
- 依然 `drifted` だが「`repo-charter`/`repo-governance` へ送った」
  「PR 作成済み・merge 待ち」「Issue 起票済み・追跡中」(ci-absent、
  ADR-0021)のいずれかとして最終報告に明記されている

## 9. 注意

- **並列サブエージェントが `bleep`(旧 `publish-guard`、または他の
  PreToolUse ガード)に deny されたら、そこで停止してユーザーに報告する**
  — 迂回・回避・自己判断での続行は禁止(#256)。具体的に禁止する行動:
  無許可の環境変数上書き(`BLEEP_ALLOW=1` 等)、guard 自身の
  ローカル設定ファイル(allowlist)の書き換え、`gh` の CLI ラッパーを
  経由せず `gh api` を直接叩く迂回、検知パターン回避のための作業
  ディレクトリ名・PR 本文からのリポジトリ名除去、検知回避目的の動的な
  文字列構築。正しい対応は `gh pr create --repo owner/repo` のように
  ターゲットを明示すること、または deny 自体が false positive の疑いが
  あれば起票して人間に判断を委ねることの 2 つだけ。
- private/company リポジトリ名は、このリポジトリ(公開)の成果物・会話ログ
  以外の永続物に書かない(`docs/agents/public-publish-guard.md`)。一括
  レビュー表はそのセッション内限りで、docs には残さない。
- `github-audit annotations --json` などの出力を**公開**リポジトリの Issue・PR
  に書くときは、先にリポジトリごとの `visibility`(`PUBLIC`/`PRIVATE`)を読み、
  公開は名前を書き、非公開は名前を伏せて件数だけにする(例: 「非公開 14 件」)。
  名前を書いてから `bleep` の `repo-ref` に止められて書き直す往復を避ける(#1094)。
- GitHub description/topics の反映は `gh repo edit` の即時反映であり、`repo-charter`
  SKILL.md §8 の時機の規定に従う(対応する README/CONTRIBUTING の PR が merge されるまで
  実行しない。§6 の 6)。
- `github-audit` の実行結果(ledger)には private リポジトリ名が含まれる
  ため、ローカルの `$XDG_STATE_HOME/github-audit/ledger.json` 以外の場所に
  コピーしない。

## CI 障害の調査

CI の失敗を扱うときは `reference/ci-failures.md` を必ず読み、環境障害と実行済みテストの失敗を区別する。
