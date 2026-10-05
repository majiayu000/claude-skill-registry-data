---
name: pe-note-plan
description: >
  技術士総合技術監理部門 記述式の note 有料記事・magazine の編集ロードマップを提案する企画スキル。
  既存の段階投下プラン・magazine 在庫・価格 yaml・過去問カバレッジを読み、次に出すべき記事（属性 × 年度・投下順・無料/有料ティア・価格・バンドル・クロスプロモ）を優先度付きで提示する。
  Use when user asks to [note 有料記事の企画, note の次の一手, magazine の企画, 記述式コンテンツの投下計画, /pe-note-plan].
user-invocable: true
domain: product
---

# /pe-note-plan — 総監記述式 note 有料記事 企画

総監記述式の note 有料記事・magazine の **編集ロードマップ** を提案する企画スキル。このスキルは記事本文を書かない（生成は `pe-essay-draft` や `/social-post`、公開前検査は `/note-prepublish-review`）。「次に何を、どの順で、いくらで出すか」の意思決定を支援する。

## 用途

note の段階投下は `content/note/技術士総監/noteコンテンツ計画.md` に方針があるが、「今ある在庫を踏まえて次の一手は何か」を毎回手で棚卸しするのは手間でミスも出る。このスキルは在庫・カバレッジ・価格・Red Line を機械的に突き合わせ、抜け漏れのない企画候補を出す。

## 引数

```
/pe-note-plan [--horizon {next|quarter}] [--attr <attr>] [--dry-run]
```

| 引数 | 必須 | 説明 |
|---|---|---|
| `--horizon` | 任意 | `next`（直近 1 本・既定）/ `quarter`（四半期ロードマップ） |
| `--attr` | 任意 | 特定属性に絞る（`general-contractor` 等） |
| `--dry-run` | 任意 | 読み取った在庫サマリのみ表示し提案しない |

## 実行手順

### Step 1: 入力資料を読む（read のみ・改変しない）

1. **段階投下方針**: `content/note/技術士総監/noteコンテンツ計画.md` — Phase 区分・Red Line・無料/有料の線引き
2. **収益化親戦略**: `docs/strategy/04_収益化戦略.md`・`content/note/技術士総監/noteコンテンツ計画.md` の参照先
3. **magazine 在庫**: `content/note/magazines/総監模範論文-{属性}/R0X/` と `content/note/magazines/総監テキスト精読ガイド/5管理-*/` の存在状況（どの属性 × 年度・どの管理が公開済み/未着手か）
4. **単体 note 記事**: `content/note/*/article.md` の `notePricing` / `notePublishedAt` / `noteUrl`（公開済みか・無料か有料か）
5. **価格**: `src/lib/note-magazines.ts` の各エントリ `price`（マガジン/セット価格の真実源）＋各記事 `article.md` frontmatter `price:`（単品）。**模範論文ペルソナ別マガジンに `_meta.yaml` は無い**（2026-06-09 廃止）。精読ガイド等で価格 yaml を持つ商品は `project_paid_note_pricing` メモ参照
6. **過去問カバレッジ**: `content/site/pe-comprehensive-management/{r0X-essay-*,pattern-essay-*}/` — 模範論文ページが揃っている属性 × 年度

### Step 2: ギャップを突き合わせる

- **属性 × 年度マトリクス**: 3 属性（general-contractor / river-consultant / road-municipality）× R03〜R07 で、(a) doboku-note 模範論文ページの有無、(b) magazine 公開の有無 を埋める
- **5 管理精読ガイド**: 5 管理（経済性・人的資源・情報・安全・社会環境）のうち未公開のもの
- **Red Line 抵触チェック**: 合格前は「模範解答」「採点基準解説」の有料販売不可等（`noteコンテンツ計画` の Red Line 1〜5）。抵触する企画候補は除外または「無料/テンプレ化」へ振り替え

### Step 3: 優先度付きで提案する

各候補に以下を付ける:

- **何を**: 属性 × 年度 or 5 管理 or 単体テーマ
- **媒体・ティア**: note 無料 / note 有料 / magazine セット
- **価格**: `note-magazines.ts` の `price`（＋記事 frontmatter `price:`）に整合（新規価格は note-magazines.ts 更新を別途提案。模範論文ペルソナ別マガジンは `_meta.yaml` を作らない）
- **投下順の根拠**: 在庫の穴・季節性（試験 7 月）・既存導線（doboku-note ページとの連携）
- **バンドル**: magazine セット化の可否（例: 属性別 R03-R07 5 本セット）
- **クロスプロモ**: 紐づけるべき doboku-note キーワードページ / 過去問ページ
- **依存**: 先に `pe-essay-draft` で作るべきページ等

### Step 4: 出力

`--horizon next` は最優先 1 本、`--horizon quarter` は 3 ヶ月ロードマップ（表）。出力は会話に提示する（ファイル書き込みはしない）。ロードマップを永続化したい場合はユーザー判断で `content/note/技術士総監/noteコンテンツ計画.md` への追記を提案する。

## content-planner エージェントとの境界

`content-planner`（Phase 2 休止中のエージェント）は **サイト全体のコンテンツ戦略**（キーワードギャップ・検索需要・季節性の統合）を担う。`pe-note-plan` は **総監記述式 note 有料記事に限定したオペレーショナルな企画** に絞る。サイト横断の戦略判断が必要になったら `content-planner` / `strategy-advisor` に委譲する。重複して戦略を立てない。

## 例

```bash
# 次に出すべき note 記事 1 本を提案
/pe-note-plan

# ゼネコン属性に絞って四半期ロードマップ
/pe-note-plan --horizon quarter --attr general-contractor

# 在庫サマリだけ確認
/pe-note-plan --dry-run
```

## トラブルシューティング

- **価格が見つからない**: まず `src/lib/note-magazines.ts` の該当エントリ `price` と記事 frontmatter `price:` を確認（模範論文ペルソナ別マガジンの真実源）。精読ガイド等の価格 yaml はこれと別系統。いずれも無ければユーザーに確認（推測で価格を出さない）
- **Red Line に抵触する候補**: 除外せず「なぜ抵触するか」と「無料/テンプレ化での代替案」をセットで提示する
- **magazine と単体記事で重複しそう**: `noteコンテンツ計画` の Red Line 5（note と doboku-note の重複コンテンツ禁止）を適用。役割分離（note = 体験談・要約 / doboku-note = 体系解説）を守る

## 参照

- `content/note/技術士総監/noteコンテンツ計画.md` — 段階投下方針・Red Line（最重要入力）
- `docs/strategy/04_収益化戦略.md` — 親戦略
- `.claude/skills/authoring/pe-essay-cycle/SKILL.md` — 統括オーケストレーター（`--mode plan` から本スキルを呼ぶ）
- `.claude/skills/authoring/pe-essay-draft/SKILL.md` — 提案後に実際の記事を作る Generator
- `.claude/skills/quality/note-prepublish-review/SKILL.md` — 公開前ゲート
- `.claude/knowledge/reference/note-publish-enhancement.md` — note 公開引き上げ工程
