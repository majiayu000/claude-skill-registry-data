---
name: .claude/skills/alert-design/SKILL.md
description: |
  アラート設計とAlert Fatigue回避の専門スキル。
  Mike Julianの『入門 監視』に基づく、アクション可能で過負荷を避けるアラートシステム設計を提供します。

  📚 リソース参照:
  このスキルには以下のリソースが含まれています。
  必要に応じて該当するリソースを参照してください:

  - `.claude/skills/alert-design/resources/actionable-alert-design.md`: アクション可能なアラート設計ガイド
  - `.claude/skills/alert-design/resources/alert-fatigue-prevention.md`: Alert Fatigue回避戦略と実践手法
  - `.claude/skills/alert-design/resources/threshold-setting-guide.md`: 統計的根拠に基づく閾値設定ガイド
  - `.claude/skills/alert-design/templates/alert-rules-template.yaml`: アラートルール定義テンプレート
  - `.claude/skills/alert-design/scripts/analyze-alert-effectiveness.mjs`: アラート有効性分析スクリプト

  使用タイミング:
  - アラートルールと閾値を設計する時
  - Alert Fatigue（アラート疲れ）を回避する時
  - 通知ルーティングとエスカレーションポリシーを設計する時
  - アクション可能なアラートを設計する時
  - 適応的閾値を設定する時
  - アラート有効性をレビューする時

  活性化キーワード: alert, alerting, alert fatigue, threshold, notification,
  escalation, actionable alert, false positive, alert routing

version: 1.0.0
---

# Alert Design - アラート設計とAlert Fatigue回避

## 概要

アラート設計は、本当に重要な問題にのみ集中できるよう、
アクション可能で過負荷を避けるアラートシステムを構築する設計手法です。

このスキルは、Mike Julianの『入門 監視』とGoogle SREの実践に基づく
アラート設計とAlert Fatigue回避の知識を提供します。

## 核心概念

### 1. アクション可能なアラート

**定義**:
受信者が何をすべきか即座に理解でき、明確なアクションが取れるアラート

**アクション可能性の判断基準**:

- [ ] 問題が何かが明確か？
- [ ] 影響範囲が分かるか？
- [ ] 対応手順が存在するか？
- [ ] 受信者が対応できるか？
- [ ] 対応しないとどうなるかが分かるか？

**良いアラート例**:

```
🚨 Critical: API Error Rate > 5%
Impact: 500 requests/minute failing
Action: Check error logs, rollback recent deploy if needed
Runbook: https://runbooks.example.com/api-errors
Dashboard: https://grafana.example.com/d/api-overview
```

**悪いアラート例**:

```
❌ Warning: Something is wrong
（何が問題か不明、対応方法不明）
```

### 2. Alert Fatigueの原因と対策

#### 原因1: 過剰なアラート

**問題**:
毎日何十件ものアラートが発火し、重要なものが埋もれる

**対策**:

- アラート数を制限（チームあたり10-20個推奨）
- 重要度に応じた通知チャネル分離
- アラート集約（時間窓内の複数発火を統合）

#### 原因2: ノイズ（False Positive）

**問題**:
誤検知が多く、アラートを無視するようになる

**対策**:

- 統計的根拠に基づく閾値設定
- 適応的閾値（時間帯、曜日、トラフィックパターン）
- 持続条件（5分間継続した場合のみアラート）

#### 原因3: アクション不明

**問題**:
アラートを受け取っても何をすればいいか分からない

**対策**:

- アラートにランブックへのリンクを含める
- 影響範囲と対応手順を明示
- 関連ダッシュボードへのリンク

### 3. アラート重要度階層

**Critical（緊急）**:

- 定義: ユーザー影響が大きい、即座の対応が必要
- 例: サービス停止、エラー率急増、SLO違反
- 通知先: PagerDuty、即座の電話/SMS
- 対応時間: 15分以内

**Warning（警告）**:

- 定義: 問題の予兆、営業時間内対応
- 例: リソース使用率上昇、レイテンシ増加傾向
- 通知先: Slack、Email
- 対応時間: 営業時間内（4時間以内）

**Info（情報）**:

- 定義: 情報提供、対応不要
- 例: デプロイ通知、設定変更通知
- 通知先: Slackのみ、または通知なし（ダッシュボード表示のみ）
- 対応時間: 対応不要

### 4. 閾値設計

#### 統計的根拠

**過去データ分析**:

```
過去30日のエラー率:
- 平均: 0.05%
- 標準偏差: 0.02%
- P95: 0.08%
- P99: 0.12%

閾値設定:
Warning: 平均 + 2σ = 0.05% + 2×0.02% = 0.09%
Critical: 平均 + 3σ = 0.05% + 3×0.02% = 0.11%
```

#### 適応的閾値

**時間帯別調整**:

```
深夜（0-6時）: トラフィック低 → 閾値を絶対値で設定
日中（9-18時）: トラフィック高 → 閾値を割合で設定
```

**曜日別調整**:

```
平日: 通常閾値
週末: トラフィック20%減 → 閾値を調整
```

**トラフィックパターン連動**:

```
通常時: エラー率 > 1%
高負荷時（トラフィック2倍）: エラー率 > 2%
```

### 5. アラート集約

**問題**:
同一問題で5分間に20件のアラート発火 → ノイズ

**対策**:
時間窓（5分）内の複数発火を単一通知に統合

**実装例**:

```yaml
alert: HighErrorRate
for: 5m # 5分間継続した場合のみ発火
annotations:
  summary: "Error rate is {{ $value | humanizePercentage }}"
  count: "{{ $activeAlerts | len }} occurrences in last 5 minutes"
```

## 設計チェックリスト

### アクション可能性

- [ ] すべてのアラートに明確なアクション指示が含まれるか？
- [ ] アラートから関連ダッシュボード・ログにすぐアクセスできるか？
- [ ] ランブック（対応手順書）が整備されているか？
- [ ] 受信者が実際に対応できる内容か？

### Alert Fatigue回避

- [ ] 誤検知率は許容範囲内か（目標 < 5%）？
- [ ] アラート数はチームが対応可能な量か（10-20個/チーム推奨）？
- [ ] アラート集約で重複通知を防いでいるか？
- [ ] ノイズの多いアラートは定期的に削除されているか？

### 重要度分類

- [ ] Critical/Warning/Infoの分類基準は明確か？
- [ ] 通知先は重要度に応じて適切に設定されているか？
- [ ] オンコール負荷は合理的か（過剰でないか）？

## 関連リソース

詳細な設計パターンと実装ガイドは以下のリソースを参照:

- **アクション可能アラート設計**: `.claude/skills/alert-design/resources/actionable-alert-design.md`
- **Alert Fatigue回避戦略**: `.claude/skills/alert-design/resources/alert-fatigue-prevention.md`
- **閾値設定ガイド**: `.claude/skills/alert-design/resources/threshold-setting-guide.md`
- **アラートルールテンプレート**: `.claude/skills/alert-design/templates/alert-rules-template.yaml`

## 関連スキル

このスキルは以下のスキルと連携します:

- `.claude/skills/slo-sli-design/SKILL.md` - SLOベースアラートの設計
- `.claude/skills/observability-pillars/SKILL.md` - メトリクスとログの統合
- `.claude/skills/structured-logging/SKILL.md` - ログベースアラート

## 使用例

### 開発環境での利用

```bash
# このスキルを参照
cat .claude/skills/alert-design/SKILL.md

# アクション可能アラート設計を確認
cat .claude/skills/alert-design/resources/actionable-alert-design.md

# アラートルールテンプレートを使用
cat .claude/skills/alert-design/templates/alert-rules-template.yaml
```

## 参照文献

- Mike Julian, 『入門 監視』, O'Reilly, 2018
- Betsy Beyer et al., 『Site Reliability Engineering』, O'Reilly, 2016
