---
name: quality-cycle
description: >
  キーワードページ・教科書 MDX の品質サイクル（スコアリング → リライト → 検証 → 人間レビュー）統合スキル。
  `--profile {cem|civil-textbook}` で試験を切替。state ファイル名は profile 別に分離（既存データと互換）。
  旧 /quality-cycle（CEM）/ /civil-textbook-cycle（1級土木）を統合。
  Use when user asks to [品質サイクル, スコアリング, リライト, 品質向上ループ, /quality-cycle].
domain: site
---

キーワードページ・教科書 MDX の品質サイクルを継続的に回すオーケストレータ。プロファイル別に state ファイル・Evaluator / Generator エージェント・拡張パターンが切り替わる。

## 引数

```
/quality-cycle --profile {cem|civil-textbook} --mode {screen|score|rewrite|verify|review|report|issue} [...]
```

| 引数 | 必須 | 説明 |
|---|---|---|
| `--profile` | 必須 | `cem`（総監キーワード）/ `civil-textbook`（1級土木 textbook/guide） |
| `--mode` | 必須 | 実行モード（profile によって一部異なる） |
| `--threshold <X.X>` | 任意 | rewrite モード時、リライト対象の weighted score 上限 |
| `--min-weighted <X.X>` | 任意 | rewrite モード時、スコア下限 |
| `--max <N>` | 任意 | rewrite モード時、1 セッション処理上限 |
| `--batch <N>` | 任意 | 並列度（参考値） |
| `--order <weakest\|newest>` | 任意 | rewrite モードの選定順序 |
| `--max <N>` | 任意 | improve モード時、1セッションで処理する最大記事数（既定: 5） |
| `--slug <slug>` | 任意 | 特定スラッグのみ対象 |
| `--section <X.Y>` | 任意 | frontmatter `section: 'X.Y'` のページのみ対象（章別バルク処理、2026-05-26 追加） |
| `--round <N>` | 任意 | issue モード時のラウンド番号 |
| `--create` | 任意 | issue モード時、gh CLI で実際に issue 作成 |
| `--dry-run` | 任意 | 対象とアクションだけ表示 |
| `--auto-loop` | 任意 | score → rewrite → verify を全件 >= 2.0 になるまで自動反復（最大3ラウンド） |

## プロファイル別テンプレート

| profile | 対象 | 件数 | テンプレート |
|---|---|---|---|
| `cem` | 技術士総監 キーワードページ (`pe-comprehensive-management/{slug}/article.mdx`) | ~690 件 | `templates/cem.md` |
| `civil-textbook` | 1級土木 textbook / guide (`civil-construction-1/{textbook,guide}/**`) | ~40 件 | `templates/civil-textbook.md` |

## モード一覧

| モード | cem | civil-textbook | 役割 |
|---|---|---|---|
| `screen` | ✓ | — | 機械的スクリーニング（690 件の初回絞り込み） |
| `flagship` | ✓ | — | Flagship 100 件の手動選定 |
| `score` | ✓ | ✓ | Evaluator エージェントで全件評価 |
| `rewrite` | ✓ | ✓ | weighted < threshold のページを Generator で改訂 |
| `improve` | ✓ | — | NLM照合主軸で HIGH 項目を外科的修正＋自動コミット（`keyword-rewriter` を使わない） |
| `verify` | ✓ | ✓ | リライト後を Evaluator で再評価 |
| `review` | ✓ | ✓ | 人間レビュー待ちリスト出力 |
| `report` | ✓ | ✓ | ダッシュボード出力（スコア分布・弱点軸頻度） |
| `issue` | ✓ | ✓ | リライト候補から GitHub umbrella issue draft 生成 |
| `auto-loop` | ✓ | ✓ | score → rewrite → verify を全件 >= 2.0 になるまで自動反復 |

**civil-textbook が screen/flagship を省略する理由**: 対象が 40 件と少ないため初回絞り込みは不要。

## 実装

プロファイルに応じて `scripts-{profile}/` 配下のスクリプトを呼び出す:

```
scripts-cem/
├── quality-cycle.mjs       # CEM プロファイルのエントリ
├── log-rewrite.mjs
├── merge-scores.mjs
├── record-verify.mjs       # 採点結果を scores+state(verified) に1ステップ記録（ドリフト防止。進捗は管理画面 /quality/progress）
└── lib/                    # cem 固有のロジック（プロンプト等）

scripts-civil-textbook/
├── civil-textbook-cycle.mjs # civil-textbook プロファイルのエントリ
├── log-rewrite.mjs
├── merge-scores.mjs
└── lib/                    # civil-textbook 固有のロジック
```

**実行例**:
```bash
# CEM プロファイル
node .claude/skills/quality/quality-cycle/scripts-cem/quality-cycle.mjs --mode score

# civil-textbook プロファイル
node .claude/skills/quality/quality-cycle/scripts-civil-textbook/civil-textbook-cycle.mjs --mode score
```

SKILL.md では `--profile` フラグを受け取って適切な scripts ディレクトリのエントリを呼び出す。

## state ファイル（profile 別に分離、既存名維持）

**重要**: 既存の state ファイル名は**変更しない**。`--profile` で正しいファイルを参照する。

| profile | scores | cycle-state | mechanical-screen |
|---|---|---|---|
| `cem` | `.claude/state/quality-scores.json` | `.claude/state/quality-cycle-state.json` | `.claude/state/mechanical-screen.json` |
| `civil-textbook` | `.claude/state/civil-quality-scores.json` | `.claude/state/civil-quality-cycle-state.json` | — |

これで既存の 690 件 CEM 進捗・40 件土木進捗が一切失われない。

## ルーブリック・拡張パターンの真実源

**ルーブリック詳細・採点フロー・拡張パターン定義は本ファイルではなく方針 md（Obsidian 可視）が真実源**:

| profile | 採点 | リライト |
|---|---|---|
| `cem` | [`docs/editorial/02_採点ルーブリック方針.md`](../../../../docs/editorial/02_採点ルーブリック方針.md) | [`docs/editorial/03_リライト方法論方針.md`](../../../../docs/editorial/03_リライト方法論方針.md) |
| `civil-textbook` | `templates/civil-textbook.md` | `templates/civil-textbook.md` |

エージェント:

- `cem`: Evaluator `cem-qa` / Generator `keyword-rewriter`
- `civil-textbook`: Evaluator `civil-construction-review` / Generator `civil-textbook-rewriter`

**共通の合否ライン**: 加重合計 ≥ 2.0 で合格、< 2.5 でリライト候補、0 軸があれば即不合格（weighted を 1.0 にクランプ）

### improve モード（cem 専用）

`/quality-cycle --profile cem --mode improve [--max N] [--dry-run]`

`rewrite` との違いは、NLM 照合（`notebooklm-cross-query.mjs`）で HIGH 論点を特定し、`keyword-rewriter` を使わず Claude が直接 Edit で外科的修正＋自動コミットする点。HIGH 自動修正の具体項目（5管理横断テーブル欠落・背景段落欠落・Callout title・SVG フォント・alt 超過・description 乖離など）と各記事パイプラインの詳細 → [03_リライト方法論方針.md](../../../../docs/editorial/03_リライト方法論方針.md)。

記事キュー: `content/site/pe-comprehensive-management/*/article.mdx` から `group: keyword` の記事を `lastRewrittenAt` 昇順、`reviewStatus: approved` はスキップ。

## 採点カバレッジ census（全 profile 横断・未採点の発見）

`npm run quality-census`（`.claude/scripts/build-quality-census.mjs`）で、published 全記事（真実源 `src/config/doc-meta-index.json`）× 全 `*quality-scores.json` を突合し、**資格 × group × {採点済み / 未採点 / 不合格 / 薄層}** の census を `.claude/state/quality/census.json` に出力する。

- **用途**: どの profile を score モードで回すべきか（未採点の母集団）と、rewrite 対象（不合格 ∪ 薄層）を機械抽出する起点。admin 品質タブ冒頭にも表示（`npm run admin`）。
- **薄層（thin）**: `keyword/guide/textbook` かつ 本文実質 3,000 字未満（`check-guide-length` と同じ SoT 計測）。**5軸ルーブリックは「本文の実質分量」軸を持たず Google の index selection と直交する**ため、census の body_chars で薄層を機械補完する（2026-07 gsc-management RCA で確立）。
- **新 profile の score ファイル**は `.claude/state/quality/{profile}-scores.json` に既存2ファイルと同型（`pages{slug:{scores,weighted,...}}`）で置き、**top-level に `categories: ["<category>"]` を必須**とする（census が bare slug → full slug を解決するため）。
- **月次運用**: `/gsc-review` と同タイミングで census を再生成し、新規公開の未採点・薄層への逆戻りを surface。

## 状態遷移（共通）

```
unscored → scored → rewriting → needs-review → verified → approved
                              └→ needs-rework → rewriting (loop)
                              └→ rejected (human decision)
```

人間ゲート必須: AI リライト後は `reviewStatus: needs-review`。`approved` への変更は人間のみ。

## 旧コマンドからの移行

| 旧コマンド | 新コマンド |
|---|---|
| `/quality-cycle --mode score` | `/quality-cycle --profile cem --mode score` |
| `/civil-textbook-cycle --mode score` | `/quality-cycle --profile civil-textbook --mode score` |

## 使い方の例

```bash
# CEM: 全件評価
/quality-cycle --profile cem --mode score

# CEM: NLM照合で HIGH を外科的修正（5件）
/quality-cycle --profile cem --mode improve --max 5

# CEM: improve 対象の確認（dry-run）
/quality-cycle --profile cem --mode improve --dry-run

# CEM: スコア < 2.5 のページを 5 件リライト
/quality-cycle --profile cem --mode rewrite --threshold 2.5 --max 5

# 1級土木: 全 40 件評価
/quality-cycle --profile civil-textbook --mode score

# 1級土木: umbrella issue draft 生成
/quality-cycle --profile civil-textbook --mode issue --round 1

# CEM: 全件 >= 2.0 になるまで自動ループ（最大3ラウンド、1ラウンド10件）
/quality-cycle --profile cem --mode auto-loop --max 10

# 1級土木: 全件 >= 2.0 になるまで自動ループ
/quality-cycle --profile civil-textbook --mode auto-loop

# 対象確認（dry-run）
/quality-cycle --profile cem --mode rewrite --dry-run
```

## auto-loop モードの動作

`/quality-cycle --profile {cem|civil-textbook} --mode auto-loop [--max N]`

1. `score` で全件評価 → weighted < 2.0 の件数を確認
2. 件数 > 0 なら `rewrite --threshold 2.0 --max {N（既定: 10）}` を実行
3. `verify` で再評価
4. ラウンド境界でサマリーを出力（改善件数・残件数）
5. 1〜4 を繰り返す。**停止条件**:
   - weighted < 2.0 の件数が 0 になった
   - 3 ラウンド完了（無限ループ防止）
   - エラーが 3 件以上発生
6. 最終レポートを出力して終了

## プロファイル詳細

- **cem**: [templates/cem.md](./templates/cem.md)
- **civil-textbook**: [templates/civil-textbook.md](./templates/civil-textbook.md)

## 関連スキル・エージェント

| 連携先 | 役割 |
|---|---|
| `cem-qa` エージェント | CEM プロファイルの Evaluator |
| `keyword-rewriter` エージェント | CEM プロファイルの Generator |
| `civil-construction-review` エージェント | civil-textbook プロファイルの Evaluator |
| `civil-textbook-rewriter` エージェント | civil-textbook プロファイルの Generator |
| `/improve-article` | 単一記事版の品質改善（本スキルはバルク版） |
| `/audit-exam-mapping` | 過去問⇔キーワード紐づけ精度の semantic 監査（旧 `/exam-keyword-cycle` Phase 2 を継承） |
| `/pe-essay-cycle` | 総監記述式（模範論文・note 有料記事）版のオーケストレーター（本スキルと補完、対象が記述式） |

## ハーネス設計上の位置づけ

- **Orchestrator スキル**（Opus inherit 相当で動作、判断質が重要）
- **Generator/Evaluator 厳密分離**: プロファイルごとに担当エージェントを使い分け
- **人間ゲート必須**: AI リライト後は `reviewStatus: needs-review`
- **データは git 管理**: state ファイルはリポジトリにコミット

## 参照

- [`docs/editorial/02_採点ルーブリック方針.md`](../../../../docs/editorial/02_採点ルーブリック方針.md) — **真実源** cem 採点ルーブリック・改善議論
- [`docs/editorial/03_リライト方法論方針.md`](../../../../docs/editorial/03_リライト方法論方針.md) — **真実源** cem 拡張パターン A-G・改善議論
- `templates/cem.md` — CEM プロファイル運用スペック（パス・スクリプト）
- `templates/civil-textbook.md` — civil-textbook プロファイル運用スペック
- `.claude/agents/cem-qa.md` — CEM Evaluator
- `.claude/agents/keyword-rewriter.md` — CEM Generator
- `.claude/agents/civil-construction-review.md` — 1級土木 Evaluator
- `.claude/knowledge/reference/content-principles.md` — §1-18 コンテンツ原則
- `.claude/scripts/lib/mdx-io.mjs` — CRLF 保持 I/O（リライト時に必須）
