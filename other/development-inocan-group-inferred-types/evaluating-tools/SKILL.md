---
name: evaluating-tools
description: 開発ツール、フレームワーク、ライブラリの評価と比較を支援します。PoC計画、複数候補の比較分析、意思決定フレームワークを提供します。技術選定、ツール導入の判断が必要な場合に使用してください。
---

# ツール・技術評価

## 概要

開発ツール、フレームワーク、ライブラリ、サービスの評価と比較を包括的に支援するスキルです。

## 実行フロー

### Step 1: 評価基準の設定

#### 重み付け評価フレームワーク

**Speed to Market (40%)**

- Setup time: <2時間 = excellent
- First feature: <1日 = excellent
- Learning curve: <1週間 = excellent

**Developer Experience (30%)**

- Documentation: 例付きの包括的ドキュメント
- Error messages: 明確で対処可能
- Community: 活発で協力的

**Scalability (20%)**

- Performance at scale
- Cost progression
- Vendor stability

**Flexibility (10%)**

- Customization options
- Integration options

### Step 2: Quick Evaluation Tests

| テスト      | 目標   | 評価ポイント |
| ----------- | ------ | ------------ |
| Hello World | <30分  | セットアップ容易さ |
| CRUD Test   | <4時間 | 生産性 |
| Integration | <1日   | 統合の柔軟性 |
| Scale Test  | 許容内 | パフォーマンス |
| Debug Test  | 容易   | デバッグ体験 |

### Step 3: 比較分析

#### 候補比較マトリクス

- 機能適合度
- 学習コスト
- パフォーマンス
- コミュニティ活発度
- ドキュメント充実度
- ライセンス/価格
- ベンダー安定性

### Step 4: Red Flags & Green Flags

#### Red Flags（警告サイン）

- 不明確な価格体系
- 古い/不足したドキュメント
- 衰退するコミュニティ
- 頻繁な破壊的変更
- 強いベンダーロックイン

#### Green Flags（好材料）

- 10分以内のクイックスタート
- 活発なコミュニティ
- 定期的なリリース
- 明確なアップグレードパス
- 充実した無料枠

### Step 5: ベストプラクティス調査

#### 調査カテゴリ

- セキュリティ
- パフォーマンス
- 運用（CI/CD、監視）
- コード品質

### Step 6: 総合評価

#### レコメンデーションレベル

- **ADOPT**: 積極的に採用
- **TRIAL**: 試験的に導入
- **ASSESS**: 評価継続
- **AVOID**: 採用見送り

## 出力成果物

1. **評価レポート**: 技術評価とレコメンデーション
2. **比較マトリクス**: 複数候補の横断比較
3. **PoC計画**: 検証ステップと成功基準
4. **ベストプラクティスガイド**: 業界標準とチェックリスト
5. **移行ガイド**: 既存ツールからの移行手順
6. **コスト分析**: 初期費用とランニングコスト

## 評価の原則

1. **実践的評価を優先**: 実際に試す
2. **長期的な視点**: スケール時を考慮
3. **チームとの適合性**: 既存スキルセットとの親和性
4. **データに基づく判断**: 測定可能な指標
5. **リスク管理**: 脱出戦略の確認

## 関連ファイル

- [TEMPLATES.md](./TEMPLATES.md) - 評価レポートテンプレート
- [CRITERIA.md](./CRITERIA.md) - 評価基準リファレンス
