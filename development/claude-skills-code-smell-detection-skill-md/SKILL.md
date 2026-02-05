---
name: .claude/skills/code-smell-detection/SKILL.md
description: |
  コードスメル（悪臭）とアーキテクチャアンチパターンの検出を専門とするスキル。
  📚 リソース参照:
  このスキルには以下のリソースが含まれています。
  必要に応じて該当するリソースを参照してください:

  - `.claude/skills/code-smell-detection/resources/architecture-antipatterns.md`: アーキテクチャ・アンチパターン
  - `.claude/skills/code-smell-detection/resources/class-smells.md`: クラス関連のコードスメル
  - `.claude/skills/code-smell-detection/resources/method-smells.md`: メソッド関連のコードスメル
  - `.claude/skills/code-smell-detection/templates/code-smell-report.md`: コードスメル検出レポート
  - `.claude/skills/code-smell-detection/scripts/detect-code-smells.mjs`: コードスメル検出スクリプト

  専門分野:
  - クラススメル: God Object、Feature Envy、Data Class
  - メソッドスメル: Long Method、Long Parameter List、Switch Statements
  - 構造スメル: Shotgun Surgery、Parallel Inheritance Hierarchies
  - アーキテクチャアンチパターン: Big Ball of Mud、Golden Hammer

  使用タイミング:
  - コードレビューで品質問題を検出する時
  - リファクタリング対象を特定する時
  - 技術的負債を可視化する時
  - 保守性低下の原因を分析する時

  Use proactively when reviewing code quality, identifying refactoring targets,
  or analyzing technical debt in the codebase.
version: 1.0.0
---

# Code Smell Detection

## 概要

このスキルは、Martin Fowlerが『Refactoring』で体系化したコードスメルの知識に基づき、
保守性を低下させる構造的問題を検出し、改善方針を提案します。

**核心概念**:
コードスメルは「コードに深刻な問題が存在する可能性を示す表面的な兆候」である。
スメル自体はバグではないが、放置すると技術的負債となり、将来の変更を困難にする。

**主要な価値**:

- 保守性低下の早期検出
- リファクタリング優先順位の明確化
- 技術的負債の可視化
- コード品質の継続的改善

**対象ユーザー**:

- アーキテクチャレビューを行う.claude/agents/arch-police.md
- コード品質を管理する開発者
- リファクタリングを計画するチーム

## リソース構造

```
code-smell-detection/
├── SKILL.md                                    # 本ファイル
├── resources/
│   ├── class-smells.md                         # クラスレベルのスメル
│   ├── method-smells.md                        # メソッドレベルのスメル
│   ├── structural-smells.md                    # 構造的スメル
│   └── architecture-antipatterns.md            # アーキテクチャアンチパターン
├── scripts/
│   └── detect-code-smells.mjs                  # スメル検出スクリプト
└── templates/
    └── smell-report.md                         # 検出レポートテンプレート
```

## コマンドリファレンス

### リソース読み取り

```bash
# クラスレベルのスメル
cat .claude/skills/code-smell-detection/resources/class-smells.md

# メソッドレベルのスメル
cat .claude/skills/code-smell-detection/resources/method-smells.md

# 構造的スメル
cat .claude/skills/code-smell-detection/resources/structural-smells.md

# アーキテクチャアンチパターン
cat .claude/skills/code-smell-detection/resources/architecture-antipatterns.md
```

### スクリプト実行

```bash
# スメル検出スクリプト
node .claude/skills/code-smell-detection/scripts/detect-code-smells.mjs src/

# 特定カテゴリのスメル検出
node .claude/skills/code-smell-detection/scripts/detect-code-smells.mjs src/ --category=class
```

## コードスメルカタログ

### クラスレベルのスメル

#### 1. God Class（神クラス）

**定義**: 多すぎる責務を持つ巨大なクラス

**検出基準**:

- 行数 > 500行
- メソッド数 > 20
- フィールド数 > 15
- 複数の異なる関心事を扱う

**検出方法**:

```bash
# 大きなクラスを検出
wc -l src/**/*.ts | sort -n | tail -20

# メソッド数が多いクラス
grep -c "^\s*(public|private|protected)" src/**/*.ts
```

**兆候**:

- [ ] クラス名が抽象的（Manager、Handler、Service）
- [ ] 関連のないメソッドが同居
- [ ] 変更時に複数の理由がある

**是正方針**:

1. 責務を列挙
2. 関連するメソッドをグループ化
3. グループごとにクラスを抽出
4. ファサードで統合（必要に応じて）

#### 2. Feature Envy（機能の横恋慕）

**定義**: あるクラスのメソッドが、他クラスのデータに過度に依存

**検出基準**:

- 他クラスのgetterを3回以上呼び出し
- 自クラスのデータよりも他クラスのデータを多く使用
- 計算ロジックが依存データと異なるクラスに存在

**検出方法**:

```bash
# getter呼び出しの多いメソッドを検出
grep -n "\.get[A-Z]\|\.is[A-Z]" src/**/*.ts
```

**兆候**:

- [ ] メソッドが他クラスのメソッドを多数呼び出す
- [ ] データの取得と計算が分離している
- [ ] 「このメソッドは本当にこのクラスに属すべきか？」

**是正方針**:

1. 依存先のクラスにメソッドを移動
2. 必要なデータとロジックを同じ場所に
3. Tell, Don't Ask原則の適用

#### 3. Data Class（データクラス）

**定義**: getter/setterのみを持ち、振る舞いがないクラス

**検出基準**:

- publicフィールドまたはgetter/setterのみ
- ビジネスロジックが存在しない
- 他クラスがデータを取り出して処理

**検出方法**:

```bash
# getter/setterのみのクラスを検出
grep -l "get\|set" src/**/*.ts | xargs grep -L "function\|method"
```

**兆候**:

- [ ] クラスがgetter/setterのみ
- [ ] ロジックが別のクラスに存在
- [ ] DTOとしてのみ使用される

**是正方針**:

1. 関連するロジックをデータクラスに移動
2. カプセル化を強化
3. 意図を明確にするメソッド名を使用

### メソッドレベルのスメル

#### 4. Long Method（長いメソッド）

**定義**: 行数が多すぎるメソッド

**検出基準**:

- 行数 > 30行
- 複数の抽象度レベルが混在
- コメントで「セクション」を区切っている

**検出方法**:

```bash
# 長いメソッドを検出（awkで行数カウント）
awk '/function|method/{start=NR} /^}$/{if(NR-start>30)print FILENAME":"start":"NR-start"lines"}' src/**/*.ts
```

**兆候**:

- [ ] スクロールが必要
- [ ] コメントでブロックを区切っている
- [ ] ローカル変数が多い

**是正方針**:

1. Extract Methodでメソッドを分割
2. 各メソッドに意図を明確にする名前
3. 抽象度を統一

#### 5. Long Parameter List（長いパラメータリスト）

**定義**: パラメータが多すぎるメソッド

**検出基準**:

- パラメータ数 > 4
- 同じパラメータの組み合わせが複数メソッドで登場
- パラメータの順序が覚えられない

**検出方法**:

```bash
# パラメータが多いメソッドを検出
grep -n "function.*,.*,.*,.*," src/**/*.ts
```

**兆候**:

- [ ] 呼び出し側でパラメータの順序を間違える
- [ ] 同じパラメータグループが繰り返し登場
- [ ] デフォルト値が多い

**是正方針**:

1. パラメータオブジェクトの導入
2. 関連パラメータをグループ化
3. Builderパターンの検討

#### 6. Switch Statements（switch文の乱用）

**定義**: 同じ条件によるswitch文が複数箇所に散在

**検出基準**:

- 同じ型による分岐が複数メソッドに存在
- 新しいケース追加時に複数箇所を修正
- ポリモーフィズムで置き換え可能

**検出方法**:

```bash
# switch文を検出
grep -rn "switch\s*(" src/
grep -rn "case\s\+[A-Z]" src/
```

**兆候**:

- [ ] 型による分岐が複数箇所
- [ ] 新しいケース追加時に「散弾銃手術」
- [ ] if-else連鎖が長い

**是正方針**:

1. ポリモーフィズムの導入
2. Strategyパターンの適用
3. Factory + インターフェースで置き換え

### 構造的スメル

#### 7. Shotgun Surgery（散弾銃手術）

**定義**: 1つの変更のために多くのクラスを修正する必要

**検出基準**:

- 小さな変更で多くのファイルを編集
- 関連する変更が分散している
- 変更漏れが発生しやすい

**検出方法**:

```bash
# Gitの変更履歴から検出
git log --name-only --oneline | head -100 | sort | uniq -c | sort -n
```

**兆候**:

- [ ] 1つの機能変更で5ファイル以上を編集
- [ ] 同様の変更を複数箇所で行う
- [ ] 変更漏れが頻発

**是正方針**:

1. 関連するコードを1クラスに集約
2. 変更理由ごとに責務を分離
3. モジュールの凝集度を高める

#### 8. Parallel Inheritance Hierarchies（並行継承階層）

**定義**: あるクラスのサブクラスを作ると、別の階層でも対応するサブクラスが必要

**検出基準**:

- 2つの継承階層が並行して存在
- 新しいサブクラス追加時に両方の階層を変更
- 類似した名前のサブクラスが対で存在

**兆候**:

- [ ] XxxとXxxFactoryが対で存在
- [ ] 新しい型追加時に2つのクラスを作成
- [ ] 継承階層が鏡像のように対応

**是正方針**:

1. 一方の階層を他方に統合
2. 合成による再構築
3. ジェネリクスの活用

### アーキテクチャアンチパターン

#### 9. Big Ball of Mud（泥団子）

**定義**: 認識可能な構造がない、無秩序なシステム

**検出基準**:

- 明確なレイヤー構造がない
- 依存関係が網の目状
- 「どこでも何でもできる」状態

**兆候**:

- [ ] ディレクトリ構造が意味不明
- [ ] 循環依存が多数
- [ ] 新メンバーが理解に時間がかかる

**是正方針**:

1. 段階的にレイヤーを導入
2. 最も重要なモジュールから境界を明確化
3. 長期的なリファクタリング計画

#### 10. Golden Hammer（金のハンマー）

**定義**: 慣れたツールや技術をあらゆる問題に適用

**検出基準**:

- 同じパターンがあらゆる場所で使用
- 問題に適さない技術選択
- 「いつもの方法」への固執

**兆候**:

- [ ] すべてがシングルトン
- [ ] あらゆる場所でORMを使用
- [ ] 不適切なデザインパターンの適用

**是正方針**:

1. 問題に適した解決策を検討
2. チームの技術スキルを拡大
3. 技術選択の理由を文書化

## ワークフロー

### Phase 1: 自動検出

**目的**: 定量的な基準でスメルを検出

**ステップ**:

1. 静的解析ツールの実行
2. メトリクス収集（行数、複雑度等）
3. 閾値超過の特定

**検出項目**:

```bash
# 行数
wc -l src/**/*.ts

# 循環的複雑度
npx ts-complexity src/

# 依存関係
npx madge --circular src/
```

### Phase 2: 手動レビュー

**目的**: 文脈を考慮したスメル評価

**ステップ**:

1. 自動検出結果のレビュー
2. 偽陽性の除外
3. 追加スメルの特定

**判断基準**:

- [ ] 技術的負債として認識すべきか？
- [ ] 意図的な設計決定か？
- [ ] リファクタリングの費用対効果は？

### Phase 3: 優先順位付け

**目的**: リファクタリング対象の優先順位決定

**評価軸**:

- **影響度**: 変更頻度、依存モジュール数
- **深刻度**: バグ発生リスク、保守コスト
- **修正コスト**: 必要な工数、リスク

**優先度マトリクス**:

```
        影響度
        高    低
深刻度
高    [P1]  [P2]
低    [P3]  [P4]
```

### Phase 4: レポート生成

**目的**: 検出結果の構造化と共有

**レポート項目**:

1. エグゼクティブサマリー
2. スメル一覧（カテゴリ別）
3. 優先順位と是正方針
4. 推奨アクション

## ベストプラクティス

### すべきこと

1. **定期的な検出**:
   - CIに静的解析を組み込み
   - スプリントごとにレビュー

2. **段階的な改善**:
   - 新規コードでスメルを発生させない
   - 既存スメルは計画的に解消

3. **知識の共有**:
   - チームでスメルカタログを共有
   - コードレビューで指摘

### 避けるべきこと

1. **完璧主義**:
   - ❌ すべてのスメルを即座に修正
   - ✅ 優先順位に基づく計画的改善

2. **スメルの正当化**:
   - ❌ 「動いているから問題ない」
   - ✅ 技術的負債として認識し管理

## 関連スキル

- **.claude/skills/solid-principles/SKILL.md** (`.claude/skills/solid-principles/SKILL.md`): 原則違反の検出
- **.claude/skills/clean-architecture-principles/SKILL.md** (`.claude/skills/clean-architecture-principles/SKILL.md`): 構造的問題
- **.claude/skills/dependency-analysis/SKILL.md** (`.claude/skills/dependency-analysis/SKILL.md`): 依存関係の問題

## メトリクス

### スメル検出率

**測定方法**: (検出されたスメル数 / コードベースサイズ) × 1000

**目標**: スプリントごとに減少

### 技術的負債指数

**計算方法**: Σ(スメルの深刻度 × 影響度)

**目標**: 管理可能なレベルを維持

## 変更履歴

| バージョン | 日付       | 変更内容                            |
| ---------- | ---------- | ----------------------------------- |
| 1.0.0      | 2025-11-25 | 初版作成 - コードスメル検出の体系化 |

## 参考文献

- **『Refactoring』** Martin Fowler著
  - Chapter 3: Bad Smells in Code
- **『Clean Code』** Robert C. Martin著
  - Chapter 17: Smells and Heuristics
