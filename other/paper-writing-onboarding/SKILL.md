---
name: paper-writing-onboarding
version: 1.3.0
description: 学術論文を初めて書く時・新しい研究プロジェクトの開始時に、リポジトリ構造の理解・初期セットアップ・フェーズ別執筆ワークフローの全体像に加え、引用作法・研究倫理など学術コミュニティの基本作法を案内するオンボーディングスキル
---

# 論文執筆オンボーディングスキル (Paper Writing Onboarding)

## 目的
学術論文の執筆が初めてのユーザー（または本スキル集を初めて使うユーザー）が、ソフトウェア開発の品質規範で駆動する執筆ワークフローに迷わず乗れるよう、環境セットアップから初稿完成までの道筋を段階的に案内する。同時に、初心者が陥りやすい失敗（出典のない数値記述・概念の曖昧使用・スコープ過大）を事前に防ぐ。

## 発動タイミング
- 新しい論文・研究プロジェクトを開始する時
- ユーザーが論文執筆の経験が浅い・初めてであると判明した時
- 「何から始めればよいかわからない」という段階

## 前提セットアップチェックリスト

執筆開始前に、以下の環境が整っているか確認する：

1. **スキル集の導入**: 本リポジトリがサブモジュール（`.scholarly-agent-skills/`）またはシンボリックリンクで導入済みであること（導入手順はルートの `AGENTS.md` を参照）。
2. **言語設定**: [`config/user_preferences.json`](../../../config/user_preferences.json) で執筆言語（自国語）が設定済みであること。
3. **AI Ignore 設定**: 生データ・非公開資料を扱う予定がある場合、`scripts/setup_ai_ignore.py` により AI インデックス除外が設定済みであること。
4. **ディレクトリ構造**: 成果物の5分類構造を作成する（複数論文を管理する場合は `docs/<paper-id>/` 配下に配置）：

```text
docs/
├── manuscript/  # 完成論文原稿・ビルド成果物（.md, .html, .pdf）
├── chapters/    # 論文本文（章ごとの Markdown）
├── design/      # 内部設計文書（概念定義・反論リスト・検証レポート）
├── literature/  # 文献調査成果物（文献マトリクス・ギャップ報告・論文ノート）
└── data/        # 一次データ（統計・調査データセット）
```

5. **Git コミット頻度の決定（v1.3.0）**: プロジェクト開始時に、成果物をコミットする頻度・タイミングの最低ラインを著者と合意し、研究計画書または運用設計文書に記録する。推奨の最低ラインは「章ごと・人間のチェック完了時」。未コミットの成果物はエディタ事故・同期障害で失われうるため、頻度の事前決定はリスク対策である。なおエージェントは合意されたタイミングでも自動ではコミットせず、必ず著者の明示指示で実行する（自動コミット禁止は不変）

## フェーズ別執筆ワークフロー

各フェーズは対応する専門スキルに引き継ぐ。初心者はこの順序に従うことで、「いきなり本文を書き始める」最も一般的な失敗を回避できる。

### Phase 0: 研究計画の言語化
→ [`research-plan-workshop`](../research-plan-workshop/SKILL.md) を発動し、対話で `docs/design/research-plan.md` に以下を1ページ以内で記述する：
- 研究問い（Research Question）を1文で
- 想定する読者・提出先（学会・ジャーナル・プレプリントサーバー）
- 完成の定義（何章構成か、目標字数、締切）

### Phase 1: 概念の地盤固め
→ [`scholarly-concept-modeling`](../scholarly-concept-modeling/SKILL.md) を発動し、中核概念の定義と境界づけを行う。多義語のまま執筆を始めると後工程で全体的な書き直しが発生する。

### Phase 2: 文献調査
→ 通時的論文では先に [`diachronic-claim-typing`](../diachronic-claim-typing/SKILL.md) で主張を型付けする。
→ [`literature-search`](../literature-search/SKILL.md) で関連文献を収集し、[`pdf-paper-ingestion`](../pdf-paper-ingestion/SKILL.md) で論文を Markdown 化、必要に応じて [`academic-paper-translation`](../academic-paper-translation/SKILL.md) で対訳化する。
→ 引用候補の情報源は [`source-criticism-gate`](../source-criticism-gate/SKILL.md) で Tier 1/2 のみに選別する。

### Phase 3: 新規性の確立
→ [`literature-gap-analysis`](../literature-gap-analysis/SKILL.md) で先行研究（AS-IS）と自説（TO-BE）のギャップを構造化し、序論の貢献記述の核を作る。

### Phase 4: 本文執筆（反論駆動）
→ [`counter-argument-tdd`](../counter-argument-tdd/SKILL.md) に従い、各節の執筆前に想定反論を `docs/design/test-cases.md` に列挙してから本文を書く。
→ 一次データを使う場合は [`primary-data-integration`](../primary-data-integration/SKILL.md) で PII マスキングとインベントリ化を先に行う。
→ **章着手時の SoT 同期チェック（v1.2.0）**: 各章の着手前に、`paper-outline.md` の該当節とその「入力」SoT 群（`domain-concepts.md`・`literature-gap-report.md` 等）の最終更新を照合する。健全条件は「アウトラインの最終改訂日 ≥ 依存 SoT の最終更新日」。満たさない場合は章ではなくアウトラインを先に更新する（SoT-first。章をアウトラインに合わせてごまかさない）。章は概念を再定義せず `domain-concepts.md` を参照する。SoT の陳腐化が章へ連鎖的に伝播するのを防ぐための手順である。

### Phase 5: 検証・校閲
→ [`claim-evidence-gate`](../claim-evidence-gate/SKILL.md) で全主張のエビデンス強度を監査し、[`citation-traceability-audit`](../citation-traceability-audit/SKILL.md) で引用の1対1対応を確認する。

### Phase 6: 提出・公開
→ [`submission-venue-advisor`](../submission-venue-advisor/SKILL.md) で分野・言語に適した提出先を選定し、公開フォームのメタデータをフィールド単位で草案してから投稿手順に従う。

## 初心者の典型的失敗と防止策

| 失敗 | 症状 | 防止策 |
|---|---|---|
| 出典なし数値 | 「〜は2.3倍である」と根拠なく書く | `rules/` のファクト・グラウンディングルールに従い、数値は必ず一次情報取得→`docs/data/` 実体化→本文参照の順で記述する |
| スコープ過大 | 1本の論文に複数の大きな主張を詰め込む | Phase 0 の研究問いを「1文」に限定し、逸脱したら計画を見直す |
| 概念の曖昧使用 | 同じ語を文脈ごとに違う意味で使う | Phase 1 の概念インベントリを作ってから本文に入る |
| 完璧主義による停滞 | 序論を永遠に推敲し続ける | 各章は「反論リストをクリアする粗い初稿」で一旦通し、Phase 5 で検証する |
| 着手麻痺 | 何から始めていいか分からずフリーズする | エージェントが Phase 0 を自動的にマイクロステップへ分解して提示する（[認知スキャフォールディング原則 S1](../../../rules/ja/cognitive-scaffolding-rule.md) 参照） |

## 学術作法の基礎（初学者向け）

本スキル集はワークフロー（どう書くか）を機械化するが、学術コミュニティの作法（何が許され何が求められるか）は暗黙知として前提にされがちである。初学者は以下の領域を執筆開始前に概観しておく。なお、これらの作法は**分野・投稿先の規定で変わる**ため、ここに挙げるのは一般的な領域の見取り図であり、最終判断は必ず投稿先の現行規定（投稿規程・著者ガイドライン）の一次確認をもって行うこと。

| 領域 | 初学者が押さえるべき点 |
|---|---|
| 引用作法 | 直接引用（逐語・ページ番号必須）と言い換え引用の区別。原論文を読めず二次資料経由で引用する場合の「as cited in」明示の作法。本リポジトリの `manual-stub`（ページ番号付き検証済み抜粋ノート）は内部管理用語であり、原稿には露出しない |
| 文献の信頼性階層 | 査読つき論文・学術書・プレプリント・グレー文献（機関レポート等）・Web 記事の重みの差。引用は [`source-criticism-gate`](../source-criticism-gate/SKILL.md) の Tier 1/2 に限定する |
| 研究倫理 | 二重投稿・サラミ出版（細切れ出版）の禁止。捏造・改竄・剽窃（FFP）の定義。著者資格の基準（ICMJE 等）。AI ツール利用の開示方針は投稿先ごとに異なるため必ず現行規定を確認する |
| 査読文化 | 査読コメントへの反論は証拠を示して礼儀正しく行う。リジェクト（不採択）は研究活動では普通の出来事であり、コメントを次の投稿に活かす |
| データ・再現性 | 一次データの保存・開示義務、プライバシー保護（PII）の扱いは [`primary-data-integration`](../primary-data-integration/SKILL.md) に従う |

## セッションを跨ぐ場合

長期プロジェクトでは、各作業セッションの終了時に [`session-research-handoff`](../session-research-handoff/SKILL.md) を発動し、文脈を `docs/session-handoff.md` に記録する習慣を最初から付ける。

## 認知スキャフォールディング
本スキルの全対話において、[認知スキャフォールディング原則](../../../rules/ja/cognitive-scaffolding-rule.md)（S1〜S4）を遵守する。特に Phase 0 ではユーザーの着手障壁が最も高いため、S1（着手障壁の極小化）を優先的に適用する。

## 成果物
- `docs/design/research-plan.md` (研究計画書: 研究問い・提出先・完成の定義)
- 上記5分類ディレクトリ構造の初期化
