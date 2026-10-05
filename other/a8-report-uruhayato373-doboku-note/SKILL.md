---
name: a8-report
description: >
  A8.net のレポート CSV を Playwright で取得し、doboku-note 分だけを正規化して SSOT
  （a8-report-log.json）へ upsert する成果データパイプライン。
  サイト別・プログラム別（詳細）・期間別（月別/日別）の 4 レポートを扱い、EPC 判定の分母を自動供給する。
  この A8 口座は stats47（統計で見る都道府県）と共用。**サイト切替は存在せず**、分離できるのはサイト別レポートのみ。
  Use when user says "A8レポート", "アフィリ成果を取り込む", "A8のCSVを取得", "EPCを更新", "a8-report".
  **初回 or UI 変更後は必ず `--dry-run --probe-isolation` で分離方式とセレクタを確定すること**.
disable-model-invocation: true
argument-hint: "[--reports all|site-summary,program-detail,period-monthly,period-daily] [--dry-run] [--probe-isolation] [--probe-period] [--headed]"
domain: affiliate
---

A8.net メディア管理画面（media-console.a8.net）のレポートを CSV でダウンロードし、
**収集 → 検証 → 正規化 → SSOT → 分析** を回す。判定はすべて決定的スクリプトに委譲し、
「伸ばす/畳む」の意思決定だけ人が持つ。

> **正典は `.claude/knowledge/reference/a8-affiliate-pipeline.md`**（レポート節）。本 skill は手順のみ。
> ラベル・URL・列名・プログラム写像は `config/a8-report-automation.json` が SSOT、
> 解析ロジックは `scripts/lib/a8-report-csv.mjs`（node:test 済み）が SSOT。
> 提携申請を回す `/scout-asp` とは別サブシステム（あちらは提携運用・こちらは成果レポート）。

## なぜ必要か

A8 は公開 API が無く、成果は長らく月 1 の手入力前提だった（月次の成果は空のまま）。
その結果、消費側の `report-buildjob-affiliate.mjs`（GA4 クリック × A8 成果 → EPC）が
**分母を持てず**、ビルドジョブ vs 建設JOBs の A/B 勝者判断が保留になっていた。ここを埋める。

## 安全弁（迂回しない）

| 弁 | 実体 |
|---|---|
| 口座 assert | メディアID が一致しなければ **1 バイトも DL しない**（exit 5）。A8 にサイト切替は無いので、ここで見るのは口座 |
| サイト分離 | 分離できるのは `/report/site` のみ。他は口座横断で allowlist 抽出＋サイト別との検算 |
| ログイン | 人間。CAPTCHA/2FA を自動突破しない |
| セレクタ | 候補が 0/複数なら推測クリックせず debug dump して停止 |
| 取りこぼし | programIdMap 未登録のプログラムは黙って捨てず `missingProgramCandidates` に出す（サイト別を説明しきれないときだけ） |
| 生データ | raw CSV と manifest は書き換えない（append-only・監査可能性） |

## フェーズ

### 1. preflight

- `git branch --show-current` / `git status`
- `config/a8-report-automation.json` の `mediaId` / `targetSite` / `reports[].siteScope` を Read
- 前回実行: `data/a8/ui-last-run.json`

### 2. collect（`a8-report-collector` エージェント）

```bash
npm run a8-ui:fetch -- --dry-run
```

初回 / UI 変更後は siteScope 宣言と実機の整合も確かめる:

```bash
npm run a8-ui:fetch -- --dry-run --probe-isolation
```

**単月取得（`--month`）を実装する前提作業**として、期間フォームの実機 DOM を観察する
（read-only＝入力もクリックもしない。`input name=start`/`end` が月レンジと日レンジの 2 組あり、
どちらを操作するかを推測しないために必要）:

```bash
npm run a8-ui:fetch -- --dry-run --probe-period --headed
```

出力を見て `config/a8-report-automation.json` の `a8.periodForm` を人間が確定する。
なぜ要るか: 現在は A8 既定の累計期間しか取れず月次の成果（単月の期間）が空＝**EPC の分母が無い**
（手順は backlog「A8 レポートの期間指定」）。

dry-run が `not-signed-in` なら、開いたブラウザで人間がログインする（スクリプトが待って storageState を保存するので、
次回以降は不要。`scout-asp/login.mjs` は Mac パス固定なのでこの経路では使わない）。

問題なければ本取得:

```bash
npm run a8-ui:fetch
```

### 3. validate（`a8-csv-auditor` エージェント）

manifest / raw CSV / rejects / 前回差分 / **サイト帰属（`crossCheck` の超過＝stats47 混入の疑い）** を
PASS/WARN/FAIL で判定。FAIL なら normalize へ進まない。

### 4. normalize + rollup（決定的）

```bash
npm run a8-ui:normalize -- --latest --dry-run   # 差分だけ見る
npm run a8-ui:normalize -- --latest             # SSOT へ書く
```

- `data/a8/report-log.json` — `siteSummary`（doboku 分離済み＝真実源）/
  `programPeriod`（案件に対応した行＋当期の口座横断の行だけ残す）/ `monthly`・`daily`（**口座横断**）/ `crossCheck` を upsert
- 月次の成果（月×案件）は持たない。読み手（`report-buildjob-affiliate`・`report-career-funnel`）が
  `programPeriod` の**単月の期間**から導く（`resultsFromReportLog`）。A8 の既定期間は年初〜当月の累計なので、
  累計の行は月次に写せず `notAttributable` に退避される

`missingProgramCandidates` が出たら config の `a8.programIdMap` に追記して再実行する（黙って無視しない）。

### 5. analyze（親が実施）

```bash
npm run report-buildjob-affiliate
```

正規化 JSON と併せて読み、プログラム別 EPC・面別クリックの伸び・撤退候補を surface する。
**判断（伸ばす/畳む/価格改定）はユーザー**。「数値がこう動いた」と「だから何をすべきか」を分けて出す。

### 6. finalize

- SSOT の差分を確認して commit（raw run は gitignore・`last-run.json` のみ commit）
- 大きな変化があれば `.claude/todo/weekly.md` の週次レビューに 1 行残す

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| `account-mismatch` | 別口座でログインしている。config の `a8.mediaId` と実機ヘッダーのメディアIDを照合 |
| `site-mismatch` | サイト別レポートに doboku-note 行が無い。A8 側のサイト登録状態を確認 |
| `export-button-ambiguous` | `exportButtonLabels` は `["CSV"]` の 1 語だけにする（増やすと同一ボタンに複数ヒットして曖昧になる） |
| `report-unreachable` | `reports.*.path` の URL が変わった。実機の URL を config へ |
| 文字化け | `csvEncoding` を切替（normalize は U+FFFD を数えて自動フォールバックもする） |
| `fatal: 必須列が見つからない` | `columnAliases` に実機のヘッダー文言を追記 |
| `missingProgramCandidates` | `programIdMap` に raw 名を追記 |

## 参照

- `.claude/knowledge/reference/a8-affiliate-pipeline.md` — A8 運用 SSOT
- `config/a8-report-automation.json` — ラベル/URL/列名/写像
- `scripts/lib/a8-report-csv.mjs` — 解析コア（`tests/a8-report-csv.test.mjs`・`npm test` に含まれる）
- `.claude/scripts/report-buildjob-affiliate.mjs` — EPC 消費側
