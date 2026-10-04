---
name: hackathon-strategist
description: >
  あらゆるハッカソンを攻略するための戦略立案・アイディア出し・設計・ピッチ準備を
  包括的に支援するスキル。リーンスタートアップ手法とハッカソン勝利パターンを統合。
  Use when the user asks to:
  - Prepare for a hackathon / ハッカソンの準備 / 作戦を立てる
  - Generate hackathon ideas / アイディア出し / テーマ選定
  - Plan hackathon architecture or MVP / アーキテクチャ設計 / MVP設計
  - Prepare a hackathon pitch or demo / ピッチ準備 / デモ準備
  - Review hackathon strategy / 戦略レビュー / 攻略法
  - "ハッカソンに出る" "ハッカソンで勝ちたい" "ハッカソン攻略"
  Covers the full lifecycle: pre-hackathon research → ideation → architecture → development
  timeline → pitch/demo preparation. Outputs actionable battle plans as Markdown documents.
---

# Hackathon Strategist — Victory Playbook

## Core Philosophy

**「動くデモ > 完璧なコード」** — ハッカソンは"伝わる"プロダクトを作る競技。
審査員が見るのは完成度ではなく **課題の切実さ × 解決策の鮮やかさ × 実現可能性** の掛け算。

## Workflow — 5 Phases

### Phase 1: Recon（偵察）

ハッカソン情報を収集し、勝利条件を逆算する。

**収集すべき情報:**
1. **テーマ・課題**: 主催者が何を求めているか
2. **審査基準**: 配点と重みづけ（不明なら推定）
3. **スポンサー技術**: 使うと加点される API / SDK / サービス
4. **時間制約**: 総開発時間、ピッチ時間、中間発表の有無
5. **過去の受賞作**: 傾向分析（技術重視 or ビジネス重視 or デザイン重視）
6. **チーム構成**: 人数、スキルセット、役割分担

See `references/judging-criteria.md` for scoring pattern analysis and optimization tactics.

### Phase 2: Ideation（アイディア出し）

3段階の発散→収束プロセスで最強のアイディアを選出。

**Step 1 — 発散（10分）**: 量を出す
- Crazy 8s: 8分で8個のアイディアスケッチ
- How Might We: 「どうすれば〇〇できるか？」で問いを立てる
- スポンサー API 逆引き: 技術から逆算してユースケースを生む

**Step 2 — 評価（5分）**: 4軸マトリクスで絞る

| 軸 | 質問 |
|---|------|
| Impact | 課題はどれだけ切実か？（感情に訴えるか） |
| Feasibility | 制限時間内にデモ可能か？ |
| Wow Factor | 審査員が「おっ」と思うか？ |
| Sponsor Fit | スポンサー技術を自然に活用できるか？ |

**Step 3 — 収束（5分）**: 1つに決断し、エレベーターピッチを書く
> 「[ターゲット] が [課題] に困っている。[プロダクト名] は [解決策] で、[数値的効果] を実現する。」

See `references/ideation-frameworks.md` for detailed methods and idea quality checklist.

### Phase 3: Architecture（設計）

**原則: 最小構成で最大インパクト**

1. **MVP定義**: デモで見せる最小機能セット（3機能以内）
2. **技術選定**: チームの既知技術 + スポンサー技術の組合せ
3. **モック先行**: UI は Figma / HTML モックを最初に作り、審査員が"見える"状態を早期に作る
4. **逃げ道設計**: 動かない場合のフォールバック（ハードコード、モックデータ）

See `references/tech-architecture.md` for quick-build patterns and tech stack decision matrix.

### Phase 4: Execution（開発タイムライン）

時間配分が勝敗を分ける。以下は標準テンプレート:

**24時間ハッカソン:**
```
[0-2h]  Recon + Ideation + アーキテクチャ確定
[2-4h]  環境構築 + UIモック + API疎通
[4-14h] コア機能実装（3機能を並列開発）
[14-18h] 統合 + デモフロー構築
[18-21h] ピッチ資料作成 + デモリハーサル
[21-23h] バグ修正 + 仕上げ（新機能追加禁止）
[23-24h] 最終リハーサル + 提出
```

**Critical Rules:**
- **残り3時間で新機能を追加しない** — 壊れるリスクが大きすぎる
- **ピッチ資料は開発の50%時点で着手** — 後回しにすると必ず時間不足
- **30分ごとに統合テスト** — 最後にまとめてマージは破滅への道

See `references/timeline-templates.md` for 8h / 24h / 48h / 1week templates.

### Phase 5: Pitch（ピッチ・デモ）

**ハッカソンは"プレゼンで"勝つ。** コードの質より伝え方。

**3分ピッチ構成:**
```
[0:00-0:30] Hook — 課題の切実さを感情的に伝える（数字 or ストーリー）
[0:30-1:30] Demo — 動くプロダクトを見せる（ライブ or 動画）
[1:30-2:30] How — 技術的な仕組み（アーキテクチャ図1枚）
[2:30-3:00] Impact — ビジネスモデル or 社会的インパクト + CTA
```

**Demo の鉄則:**
- ライブデモは必ずバックアップ動画を用意
- 最も印象的な機能を最初に見せる
- 「もし○○だったら」のシナリオで審査員の想像力を刺激

See `references/pitch-playbook.md` for pitch script templates and demo strategies.

## Output Deliverables

このスキルの最終出力は **Battle Plan（作戦書）** — 以下を含むMarkdownファイル:

```markdown
# [ハッカソン名] Battle Plan

## 1. Mission（勝利条件）
## 2. Idea（1行エレベーターピッチ + 詳細）
## 3. Architecture（技術構成図 + MVP機能リスト）
## 4. Timeline（時間割 + マイルストーン）
## 5. Pitch Script（ピッチ台本 + デモシナリオ）
## 6. Risk & Fallback（リスクと逃げ道）
```

## Quick Modes

| Mode | Phases | Trigger |
|------|--------|---------|
| Full Strategy | 1→2→3→4→5 | "ハッカソン攻略" "作戦を立てて" |
| Idea Only | 2 | "アイディア出し" "テーマ選定" |
| Architecture | 3 | "アーキテクチャ設計" "技術選定" |
| Timeline | 4 | "タイムライン" "スケジュール" |
| Pitch Prep | 5 | "ピッチ準備" "デモ準備" |
