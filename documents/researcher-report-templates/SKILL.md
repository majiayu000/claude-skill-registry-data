---
name: researcher-report-templates
description: |
  Generate structured research reports with findings, comparisons, recommendations, and citations. Use when documenting investigation results or creating technical comparisons.

  This skill provides comprehensive research report templates:
  - Investigation findings with proper structure
  - Technology comparison tables
  - Best practices summaries
  - Citation and reference management
  - Executive summaries

  Triggers: "create report", "summarize findings", "compare technologies", "research report", "調査レポート", "技術比較", "ベストプラクティス"
allowed-tools:
  - Read
  - Write
---

# Researcher Report Templates Skill

## 概要

このSkillは、researcherエージェントが調査結果を構造化されたレポートにまとめる際に使用します。調査レポート、技術比較、ベストプラクティス文書などのテンプレートを提供し、一貫性のある高品質なドキュメントを作成できます。

## 主な機能

1. **調査レポートテンプレート**: 標準化されたフォーマットで調査結果を整理
2. **技術比較テーブル**: 複数の技術やサービスの特徴を比較
3. **ベストプラクティステンプレート**: 推奨事項をまとめた文書
4. **引用・参照管理**: 情報源を適切に記録
5. **エグゼクティブサマリー**: 要点を簡潔にまとめた概要

## 使用方法

### テンプレート一覧

```
templates/
├── research-report-template.md       # 調査レポート
├── tech-comparison-template.md       # 技術比較
├── best-practices-template.md        # ベストプラクティス
└── executive-summary-template.md     # エグゼクティブサマリー
```

### 使用例

**1. 調査レポート作成**

```markdown
# AWS Lambda 調査レポート

## エグゼクティブサマリー

AWS Lambdaは、サーバーレスコンピューティングサービスであり、以下の特徴があります:
- 自動スケーリング
- 実行時間に基づく従量課金
- 複数のランタイムサポート（Node.js、Python、Java等）

本調査では、Lambdaのアーキテクチャ、ベストプラクティス、コスト最適化手法を調査しました。

## 調査結果

### 1. アーキテクチャ

AWS Lambdaは、イベント駆動型のコンピューティングサービスです...

### 2. パフォーマンス最適化

**コールドスタート対策**:
- プロビジョニング済み同時実行数の使用
- 関数サイズの最小化
- レイヤーの活用

### 3. コスト最適化

- 適切なメモリ配分（メモリとCPUは比例）
- タイムアウト設定の最適化
- 不要な実行の削減（冪等性の確保）

## 技術比較

| 項目 | AWS Lambda | Google Cloud Functions | Azure Functions |
|------|-----------|----------------------|----------------|
| 最大実行時間 | 15分 | 9分 | 10分（Consumption） |
| 対応言語 | 10+ | 8+ | 10+ |
| 最小メモリ | 128MB | 128MB | 128MB |
| 価格 | $0.20/100万リクエスト | $0.40/100万リクエスト | $0.20/100万リクエスト |

## 推奨事項

1. **本番環境での推奨設定**:
   - メモリ: 1024MB以上（コスト効率とパフォーマンスのバランス）
   - タイムアウト: 実際の処理時間 + 30%のバッファ
   - プロビジョニング済み同時実行数: ピークトラフィックの50%

2. **監視・ロギング**:
   - CloudWatch Logsの有効化
   - X-Rayトレーシングの有効化
   - カスタムメトリクスの設定

3. **セキュリティ**:
   - 最小権限の原則（IAMロール）
   - VPC統合（必要な場合のみ）
   - 環境変数の暗号化

## 参考リンク

- [AWS Lambda公式ドキュメント](https://docs.aws.amazon.com/lambda/)
- [Lambda ベストプラクティス](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [コスト最適化ガイド](https://aws.amazon.com/lambda/pricing/)

## 結論

AWS Lambdaは、スケーラブルで費用対効果の高いサーバーレス実装に最適です。適切な設定と監視により、本番環境での安定運用が可能です。
```

**2. 技術比較レポート**

```markdown
# データベース選定: PostgreSQL vs MySQL vs MongoDB

## 概要

プロジェクトに最適なデータベースを選定するため、3つの主要データベースを比較しました。

## 比較表

| 項目 | PostgreSQL | MySQL | MongoDB |
|------|-----------|-------|---------|
| **タイプ** | リレーショナル | リレーショナル | NoSQL（ドキュメント） |
| **トランザクション** | ACID準拠 | ACID準拠 | ACID準拠（4.0+） |
| **スケーラビリティ** | 垂直 + レプリケーション | 垂直 + レプリケーション | 水平シャーディング |
| **JSON サポート** | ネイティブ | 5.7+ | ネイティブ |
| **全文検索** | あり | あり | あり |
| **地理空間データ** | PostGIS | あり | あり |
| **学習曲線** | 中 | 低 | 低〜中 |
| **コミュニティ** | 大 | 大 | 大 |

## 詳細分析

### PostgreSQL

**長所**:
- 高度なSQL機能（ウィンドウ関数、CTE、配列型）
- JSONBによる高速JSONクエリ
- 拡張性が高い（PostGIS、pg_vector等）
- ACID準拠の堅牢性

**短所**:
- 水平スケーリングが複雑
- 初期設定・チューニングが必要
- メモリ使用量が多い

**適用場面**:
- 複雑なクエリが必要
- データ整合性が最重要
- 地理空間データ（PostGIS）
- 分析ワークロード

### MySQL

**長所**:
- シンプルで学習しやすい
- 高速な読み取り性能
- 豊富なホスティングオプション
- レプリケーションが簡単

**短所**:
- 複雑なクエリのパフォーマンス
- トランザクション分離レベルの制限
- 拡張性がPostgreSQLより低い

**適用場面**:
- シンプルなCRUD操作
- 読み取り中心のワークロード
- WordPressなどCMS
- 高速な書き込みが必要

### MongoDB

**長所**:
- スキーマレス（柔軟性）
- 水平スケーリングが容易
- JSONネイティブ
- 高速な書き込み

**短所**:
- 複雑なJOINが苦手
- データ重複の可能性
- メモリ使用量が多い
- トランザクションサポートが限定的（古いバージョン）

**適用場面**:
- スキーマが頻繁に変わる
- 大量のJSONデータ
- 水平スケーリングが必要
- リアルタイムアプリ

## 推奨

**プロジェクトの要件**:
- ユーザー、注文、商品データ
- トランザクション整合性が重要
- 複雑な集計レポート
- 将来的なスケーラビリティ

**推奨データベース**: **PostgreSQL**

**理由**:
1. ACID準拠の堅牢性
2. 複雑なクエリのサポート
3. JSONデータの効率的な処理
4. 豊富な拡張機能

## 移行計画

1. PostgreSQL 16のセットアップ
2. スキーマ設計とインデックス最適化
3. パフォーマンステスト
4. 段階的なデータ移行
5. 監視・チューニング

## 参考リンク

- [PostgreSQL vs MySQL](https://www.postgresql.org/about/)
- [MongoDB Use Cases](https://www.mongodb.com/use-cases)
- [Database Selection Guide](https://database.guide/)
```

## テンプレートの構造

### 調査レポート

1. **エグゼクティブサマリー**: 要点を3-5行で
2. **調査目的**: なぜこの調査を行ったか
3. **調査方法**: どのように情報を収集したか
4. **調査結果**: 詳細な発見事項
5. **技術比較**: 表形式での比較
6. **推奨事項**: アクションプラン
7. **参考リンク**: 情報源
8. **結論**: まとめ

### 技術比較

1. **概要**: 比較の目的
2. **比較表**: 項目別の比較
3. **詳細分析**: 各技術の長所・短所
4. **推奨**: 選定結果と理由
5. **移行計画**: 実装手順（必要に応じて）

### ベストプラクティス

1. **背景**: なぜこれが重要か
2. **推奨パターン**: 具体的な方法
3. **アンチパターン**: 避けるべきこと
4. **実装例**: コードサンプル
5. **参考リンク**: 詳細情報

## スクリプト機能

### generate-report.js

調査データを構造化されたレポートに変換します。

**使用方法**:
```bash
node scripts/generate-report.js research-notes.md
```

**機能**:
- Markdown形式の調査メモを読み込み
- テンプレートに従って整形
- 目次の自動生成
- 参考リンクの整理
- `issues/`または指定ディレクトリに保存

## ベストプラクティス

### DO（推奨）

✅ **構造化された形式**: テンプレートに従う
✅ **客観的な事実**: 主観を排除
✅ **引用元を明記**: 情報源を記録
✅ **比較表を活用**: 視覚的に比較
✅ **エグゼクティブサマリー**: 要点を最初に

### DON'T（非推奨）

❌ **主観的な評価**: データに基づく評価を
❌ **情報源の記載漏れ**: すべての情報源を記録
❌ **冗長な説明**: 簡潔に
❌ **不完全な比較**: すべての選択肢を公平に評価

## Progressive Disclosure

このSKILL.mdはメインドキュメント（約300行）です。詳細なテンプレートは `templates/` ディレクトリ内のファイルを参照してください。

## 関連リソース

- **templates/research-report-template.md**: 調査レポートテンプレート
- **templates/tech-comparison-template.md**: 技術比較テンプレート
- **templates/best-practices-template.md**: ベストプラクティステンプレート
- **scripts/generate-report.js**: レポート生成スクリプト
