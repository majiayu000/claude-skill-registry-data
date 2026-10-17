---
name: weekly-plan
description: >
  週次レビュー（/weekly-review）後に翌週の実行計画を並列サブエージェントで生成し、同週の `docs/reviews/weekly/YYYY-Www.md` に「来週の計画」セクションとして追記する（NSM/メトリクス連動・重め・手動のみ。週間計画の正本 .claude/todo/weekly.md は /plan-weekly が書く）。.claude/todo/weekly.md のタスク選定・優先度付けは /plan-weekly の担当で別物。Use when user asks to [戦略的週次計画, NSM込みの来週計画, weekly-review後の計画生成, /weekly-plan].
domain: plan
---

## 共通の判断基準

`docs/strategy/01_プロダクト戦略.md` と `config/business-direction.json`、直近の `data/business/records/` の週次・月次判断を先に読む。対象資格・読者の課題・現物の不足・変更・評価指標・再計測日を一続きにする。記事数や図数を増やすための計画にしない。実験はexperiments.json、単発実装はbacklogへ接続し、計画へ状態を複製しない。未測定の販売・費用・時間は取得を次の一手に含める。

プロジェクトの現状を調査し、戦略的な週次計画を生成する。

## 引数

```
/weekly-plan [YYYY-Www]
```

- 週番号（任意）: ISO 8601 週番号（例: `2026-W11`）。省略時は今週。

## 概要

サブエージェントで並列にコンテキストを収集し（開発状況・コンテンツ・パフォーマンス・トレンド）、優先順位を決定し、批判的にレビューした上で、実行可能な週次計画を出力する。

## 手順

### Phase 0: 週次メトリクス スナップショット（CI 供給が既定）

**スナップショットは `fetch-metrics.yml`（金 06:00 JST）が CI 上でライブ取得してコミットする**（2026-07-04〜。2026-W18 でローカル手動実行が途絶したのを CI 供給へ移行＝恒久ルールと整合）。`data/business/weekly/YYYY-Www.json` に NSM（GA4+GSC 前週比較）＋ **SNS 流入（source 別 WoW）** を保存する。窓は**確定した直近の月〜日**（事業レビュー・成長パックと同じ）で、ファイル名の週はその窓の ISO 週（実行日の週ではない）。Phase 0 で人がやることは通常なし（最新スナップショットを読むだけ）。

ローカルで手動生成したい場合のみ（creds のある Mac 等）:

```bash
node .claude/scripts/snapshot-weekly-metrics.mjs        # 確定した直近の週（既存週は skip・--force で上書き）
```

会社 PC のプロキシ配下などライブ取得できない環境では実行しない。Agent C（および weekly-review の SNS フェーズ）は **CI がコミットした `.claude/state/{weekly-metrics,metrics/{ga4,gsc}}/` のスナップショットを直接読む**（既定経路）。

> 計測は CI/CD 供給が正（`fetch-metrics.yml` 金 06:00 JST / `psi-audit.yml` 日次）。ローカル creds は設計上不要で「計測基盤未整備」とは扱わない。恒久ルール: `.claude/knowledge/reference/measurement-incidents.md`（2026-06-05）。

### Phase 0.5: 閾値違反の抽出（.claude/todo/ 反映候補）

Phase 0 の snapshot 直後、`data/business/weekly/YYYY-Www.json` を読み、以下の閾値ルールで違反項目を抽出する。**task-queue.json 自動登録は廃止（2026-06-11、.claude/todo/ 手動運用へ一本化）**。抽出した違反は Phase 1 Agent C の出力に含め、Phase 3「今週のタスク」候補としてユーザーが `.claude/todo/` にキュレーションする。

#### 抽出対象の閾値

| ソース | メトリクス | 閾値 | 優先度 |
|---|---|---|---|
| GA4 | チャネル別 sessions 前週比 | -20% 以上 かつ 前週 ≥10 | **High** (Traffic-Drop) |
| GSC | 全体 CTR 前週比 | -30% 以上 | Medium |
| GSC | position ≤ 3 クエリの CTR | < 5% | Medium |
| PSI | **field LCP / INP / CLS の category** | AVERAGE または SLOW | **Critical**（実害） |
| PSI | LCP (lab) 直近5バッチ中央値 | > 2500ms | Medium（field が FAST のとき）／High（field も悪いとき） |
| PSI | CLS (lab) 直近5バッチ中央値 | > 0.1 | Medium／High（同上） |
| PSI | Performance スコア (lab) 中央値 | < 70 | Medium |
| PSI | 中央値比 Performance | -10 以上 | High（回帰） |
| PSI | 中央値比 LCP | +500ms 以上 | High（回帰） |

> **PSI の判定原則（誤報防止・必読）**: **実害＝Critical は field(CrUX 実ユーザー p75) が AVERAGE/SLOW のときだけ**。lab は合成スロットリング値で日次の振れが大きく（同一ページが同一週内に 2,026〜7,201ms を往復）、**単発値・単発差分で Critical を立ててはいけない**。field が FAST なら lab がどれだけ悪くても最大 Medium（改善余地であって障害ではない）。回帰は前回比ではなく**直近5バッチ中央値**で見る。
> 真実源: [measurement-incidents.md](../../../knowledge/reference/measurement-incidents.md)「2026-07-27: lab と field の判定原則」／機械可読: `config/psi-config.json` の `judgment`。
> ※ 2026-07-27（W30）に lab の単発スパイクを CRITICAL と報告し、実際は field p75 822ms=FAST で実害ゼロだった。1週間分の優先順位が歪んだ。

詳細な条件式は `.claude/agents/metrics-analyzer.md` および `.claude/agents/performance-auditor.md` 参照。

#### 抽出手順

1. 上記閾値に該当する違反を一覧化する（URL × メトリクス）
2. 前週の `.claude/todo/weekly.md` と照合し、既に起票済みの項目は「継続」、新規のみ「今週新規」とする（重複起票を避ける）
3. 抽出結果を Phase 1 Agent C の出力に含める（「閾値違反: 新規 N 件 / 継続 M 件」）。Phase 4 で `.claude/todo/weekly.md` への反映候補として提示する

**違反なしの場合**: 「閾値違反なし」と明示的にログに残す。

### Phase 1: コンテキスト収集（並列サブエージェント）

#### Agent A: 開発状況

```
調査項目:
- git log --oneline -20（直近の開発活動）
- git diff --stat（未コミット変更）
- docs/ 配下のページ数（カテゴリ別）

出力形式: 「今週何が開発されたか」「未完了の作業」をまとめる
```

#### Agent B: コンテンツ状況

```
調査項目:
- docs/ 配下の .mdx ファイル数（カテゴリ別: general, road, river, low）
- 最近更新されたファイル
- カテゴリごとのコンテンツ充実度

出力形式: 「コンテンツの充実度」「不足しているカテゴリ」「ボトルネック」
```

#### Agent C: NSM / 実験サイクル

```
調査方法:
1. NSM データの取得（既定 = スナップショット読み）:
   - CI がコミットした `data/{ga4,gsc}/reports/` の最新スナップショットを読む（既定）
   - Phase 0 で `data/business/weekly/YYYY-Www.json` が生成済みならそれを使ってもよい
   - creds + 外部到達性がある環境に限り、任意で metrics-reader を直接呼んでもよい
2. data/business/experiments.json を読んで以下を把握:
   - `kind: search-strategy` は汎用10日/28日・metrics-reader比較と start 候補から除外（search-strategy は `npm run search-improvement -- status` に従う。proposed はカードの時期で進む）。計測中のページへ別実験を提案しない。
   - running 実験: 経過日数、baseline との gap
   - measuring 実験: 前後比較の中間サマリ
   - proposed 実験: 優先順位（次に start すべきもの）
3. `data/business/weekly/` の新しい 4 本（YYYY-Www.json）から直近 4 週分のトレンドを読む（運用中の場合）
4. 上記を統合して次の実験候補を 3-5 件提案
   - .claude/skills/management/nsm-experiment/references/playbook.md の典型パターンから
   - .claude/skills/management/nsm-experiment/references/rubric.md で優先順位付け

出力形式:
## NSM 現況
- Organic Search users: {今週} (前週比 {delta})
- GSC clicks: {今週} (前週比 {delta})
- 直近 4 週トレンド: (運用中の場合) 図表

## 実験の状態
| ID | title | status | 経過日数 | 進捗 |
|---|---|---|---|---|

### running の警告
- EXP-??? は started_at から 10 日超、そろそろ /nsm-experiment measure を実行

## 次の実験候補（rubric 順）
1. [加重 2.7] title 改善: ...
2. [加重 2.0] description 改訂: ...

### 提案アクション
- Must: 候補 1 を /nsm-experiment start で開始
- Should: 候補 2 を backlog に追加（experiments.json に proposed で残す）
```

**取得元の優先順位**:
- 既定: CI がコミットした `data/{ga4,gsc}/reports/` スナップショットを読む（creds 不要）
- 任意: creds（.env.local の GOOGLE_SERVICE_ACCOUNT_KEY_PATH / GA4_PROPERTY_ID）+ 外部到達性が
  両方ある環境のみライブ fetch 可。会社 PC のプロキシ配下では不可
- スナップショットも揃わない真のデータ欠損時のみ「NSM セクション: スキップ（データ未取得）」と記録。
  creds 未設定そのものは「計測基盤未整備」ではない（基盤は CI 側で稼働）

#### Agent C2: オープンの改善タスク

```
調査方法:
- 前週の `.claude/todo/weekly.md` の未完了項目（継続タスク。task-queue.json は廃止）
- `.claude/state/improvements/psi-*.md` の直近 7 日分（performance-auditor の改善候補レポート）
  - 違反パターン別（LCP 肥大・CLS 発生等）の Critical / High 候補

分析項目:
- 前週から継続している項目 — 2 週以上の継続は Must 候補
- priority: high の改善候補は件数多くても上位 2-3 件を Should に入れる
- 同一 URL に複数タスクがある場合はまとめて 1 タスク化

出力形式: 「## オープンの改善タスク」セクションとして以下構造で:

## オープンの改善タスク

### Critical（前週から継続 または LCP/CLS 大幅超過）
| 対象 | 内容 | 継続 | 対応方針 |
|---|---|---|---|
| /docs/xxx | LCP 4.2s | 2 週 | Hero 画像 priority 指定 |

### High（PSI 改善候補から）
| 候補 | 対象 URL | 改善パターン |
|---|---|---|

これらを Phase 3 の Must / Should 候補として組み込む。
```

#### Agent D: トレンド・検索需要

```
調査項目:
- 土木系資格試験の日程（施工管理技士: 6月・11月、技術士: 7月・10月）
- 季節性の需要変動（試験前の学習需要増）
- 関連ニュース（インフラ、防災、建設業界）

出力形式: 「今週のトレンド機会」「試験シーズンとの関連」
```

### Phase 2: 戦略分析

エージェントの結果を統合し分析する:

1. **KPI との距離**: 目標に対する現在地
2. **ギャップ**: 計画と実行の乖離
3. **機会**: 季節性・トレンドに応じた施策
4. **リスク**: 放置すると悪化すること

### Phase 3: 優先度提案

**選定基準**（タスクを Must/Should/Could に振るときの判断軸。この3点を満たさないものは格下げする）:

1. **収益・PV に直結するか** — 「技術的に面白い」だけのタスクを Must に入れない
2. **前週と同じ失敗の繰り返しでないか** — 前週の計画・申し送りと照合する
3. **今週やらないと機会損失か** — 試験シーズン・受験期などのタイミング依存を優先

#### Must（必ずやる: 2-3件）
- 各タスクに: 理由, 成功基準, 推定工数(S/M/L)

#### Should（できればやる: 2-3件）

#### Could（余力があれば: 1-2件）

### Phase 4: 出力（週次 PDCA md に追記）

生成した markdown を、同週の `docs/reviews/weekly/YYYY-Www.md` に「---」区切りで追記する。

```bash
# /weekly-review が先に docs/reviews/weekly/YYYY-Www.md を作成している前提
PDCA_FILE=docs/reviews/weekly/YYYY-Www.md
{
  echo ""
  echo "---"
  cat /tmp/weekly-plan-section.md
} >> "$PDCA_FILE"
```

`docs/reviews/weekly/YYYY-Www.md` が存在しない場合は計画のみで新規作成してよい（この場合ファイル冒頭に `# 週次 PDCA YYYY-Www` の H1 を追加）。

## 出力フォーマット（週次 PDCA md の追記セクション）

> **分量バジェット**（真実源: [docs-markdown-style.md](../../../knowledge/reference/docs-markdown-style.md)「長さの既定」）:
> 各表は**上位 5 行＋「他 N 件」**。タスクの理由は 1〜2 文。批判的レビューは**最大 4 点**。
> 該当ゼロのセクションは「なし」の 1 行で閉じ、見出しごと空欄で残さない。
> **検出と表示は別**: 閾値違反は全件抽出したうえで、載せきれない分は件数と参照先を必ず書く。

```markdown
## 来週の計画

### 前週の振り返り (W-1)

| タスク | 分類 | 状態 | メモ |
|---|---|---|---|

## 現状サマリー

| 指標 | 現在値 | 目標 |
|---|---|---|
| 公開ページ数 | N | — |
| 推定月間 PV | N | — |

## トレンド機会

| トレンド | 関連コンテンツ | アクション |
|---|---|---|

## 今週の実験

<!-- Agent C が experiments.json と nsm-experiment の rubric 評価から自動生成。
     running / measuring / 新規 start 候補 を一覧で表示。 -->

| ID | title | status | 次のアクション |
|---|---|---|---|

## オープンの改善タスク（前週からの継続）

<!-- Agent C2 が前週 .claude/todo/weekly.md の未完了項目と
     .claude/state/improvements/psi-*.md から生成。
     Must/Should 候補の根拠となる。 -->

### Critical（前週から継続）
| 対象 | 内容 | 継続 |
|---|---|---|

### High（今週対応候補）
| 候補 | 対象 URL | 改善パターン |
|---|---|---|

## 今週のタスク

### Must
1. **タスク名** [S/M/L]
   - 理由:
   - 成功基準:

### Should

### Could

## 批判的レビュー

> Phase 3 の選定基準（収益直結か／前週の繰り返しでないか／今週やらないと機会損失か）で
> 引っかかった点を、最大 4 点まで書く。無ければ節ごと省略する。

## 次週への申し送り
```

## 運用ルール

- **毎週金曜に実行**（/weekly-review 直後に同日連続実行）
- 前週の計画ファイルが存在する場合、**自動で振り返りを生成**する
- 計画ファイルは蓄積する（削除しない）

## 参照

- `.claude/skills/management/weekly-review/SKILL.md` — 週次レビュー
- `.claude/skills/management/nsm-experiment/SKILL.md` — 実験ライフサイクル管理
- `.claude/skills/management/nsm-experiment/references/playbook.md` — 実験パターン
- `.claude/skills/management/nsm-experiment/references/rubric.md` — 実験優先順位
- `.claude/scripts/snapshot-weekly-metrics.mjs` — Phase 0 スナップショット
- `.claude/scripts/lib/metrics-reader.mjs` — NSM 計測本体
- `.claude/skills/management/nsm-experiment/references/definition.md` — NSM 定義
