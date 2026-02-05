---
name: mcp-memory-first-development
description: Memory-First development workflow integrating Serena short-term project memory and Cipher long-term design knowledge for efficient LoRAIro development
allowed-tools: mcp__serena__list_memories, mcp__serena__read_memory, mcp__serena__write_memory, cipher_memory_search, cipher_store_reasoning_memory, cipher_extract_entities
---

# Memory-First Development Skill

このSkillは、Serena短期メモリとCipher長期メモリを統合した2重メモリ戦略による効率的な開発ワークフローを提供します。

## 使用タイミング

Claudeは以下の開発フェーズでこのSkillを自動的に使用すべきです：

- **実装前**: 過去の類似実装パターンと現在のプロジェクト状況を確認
- **実装中**: 進捗、判断、課題を継続的に記録
- **完了後**: 実装知識と教訓を長期記憶として蓄積

## 2重メモリ戦略

### Serena Memory（短期・プロジェクト固有）

**用途**: 現在の開発進捗と一時的な開発メモ

**保存内容**:
- 現在の実装状況と次のステップ
- 進行中の開発判断
- 一時的な課題と解決策
- デバッグ情報と検証結果
- リファクタリング計画

**特性**:
- **高速アクセス** (0.3-0.5秒)
- **頻繁な更新**: 実装中に何度も読み書き
- **一時的**: タスク完了後はアーカイブまたは削除
- **プロジェクト固有**: LoRAIro専用の状況記録

### Cipher Memory（長期・設計知識）

**用途**: 将来参照可能な設計パターン資産

**保存内容**:
- 設計アプローチと判断根拠
- アーキテクチャ設計の意図と背景
- パフォーマンス・保守性の評価
- 実装時の課題と解決策
- ベストプラクティスとアンチパターン
- 技術選定の基準と結果

**特性**:
- **永続的**: プロジェクト全体で参照可能
- **検索可能**: cipher_memory_searchで過去事例を発見
- **汎用的**: 他プロジェクトでも参照可能な知見
- **構造化**: タイトル、コンテキスト、判断、根拠、結果、教訓

## Memory-First開発サイクル

### Phase 1: 実装前の事前確認

```
目的: 過去の知見を活用し、重複作業を回避

1. プロジェクト状況確認 (Serena):
   mcp__serena__list_memories()
   → 利用可能なメモリ一覧

   mcp__serena__read_memory("current-project-status")
   → 現在のブランチ、最新の実装変更、次の優先事項

2. 過去の類似実装検索 (Cipher):
   cipher_memory_search(query="実装対象のキーワード")
   → 過去の設計パターン、実装アプローチ、教訓

3. 設計要素抽出 (Cipher):
   cipher_extract_entities(text="実装計画")
   → 重要な技術要素、アーキテクチャコンポーネント

結果: 既存知識を活用した効率的な実装開始
```

### Phase 2: 実装中の継続記録

```
目的: 進捗と判断を可視化し、中断時の再開を容易に

実装中の定期的記録 (Serena):
   mcp__serena__write_memory(
     memory_name="active-development-tasks",
     content='''
# 現在の実装状況 - YYYY-MM-DD

## 進行中タスク
- [現在作業中の内容]

## 完了した作業
✅ [完了項目1]
✅ [完了項目2]

## 次のステップ
1. [次に実装すること]
2. [その次の作業]

## 技術的判断
- [実装中に行った重要な判断]
  理由: [なぜその判断をしたか]

## 課題・ブロッカー
- [現在の問題点]
- [解決策候補]
'''
   )

更新頻度: 重要な判断後、作業区切り時、中断前
```

### Phase 3: 完了後の知識蓄積

```
目的: 実装知識を永続化し、将来の開発資産に

完了時の長期記憶化 (Cipher):
   cipher_store_reasoning_memory(
     title="[実装内容の簡潔な要約]",
     content='''
# 実装概要
[何を実装したか]

## 背景・動機
[なぜこの実装が必要だったか]

## 設計アプローチ
[どのような設計判断をしたか]

## 技術選定
[使用した技術とその選定理由]

## 実装詳細
[重要な実装パターン、コード構造]

## 結果・効果
[実装による改善、パフォーマンス向上、コード削減等]

## 課題と解決策
[実装中に直面した課題とその解決方法]

## 教訓・ベストプラクティス
[将来の実装で活用できる知見]

## アンチパターン
[避けるべき実装方法、失敗から学んだこと]
''',
     tags=["実装分野", "技術タグ"],
     context="LoRAIro [feature名] 実装"
   )

実施タイミング: 機能完了時、リファクタリング完了時、重要な技術判断後
```

## Memory命名規則

### Serena Memory（短期）
- **current-project-status**: プロジェクト全体の状況
- **active-development-tasks**: 現在の開発タスクと進捗
- **{feature}_wip_{YYYY_MM_DD}**: 作業中の機能実装メモ
- **debug_{issue}_{YYYY_MM_DD}**: デバッグ情報と解決策
- **archived_{name}**: 完了タスクのアーカイブ

### Cipher Memory（長期）
- **Title形式**: "LoRAIro [機能名] [実装内容] 設計/実装"
- 例: "LoRAIro Direct Widget Communication パターン採用"
- 例: "LoRAIro Repository Pattern データベース設計"
- 例: "LoRAIro QRunnable非同期処理実装"

## 実装例: 新機能開発の完全フロー

### シナリオ: 新しいGUIウィジェット実装

```
=== Phase 1: 実装前 ===

1. 現在状況確認:
   mcp__serena__list_memories()
   mcp__serena__read_memory("current-project-status")

2. 過去の類似実装検索:
   cipher_memory_search(query="widget implementation pattern signal slot")

3. 設計要素抽出:
   cipher_extract_entities(text="新ウィジェット実装計画")

結果: 既存のWidget実装パターンを発見、重複実装を回避

=== Phase 2: 実装中 ===

実装開始時:
   mcp__serena__write_memory(
     "active-development-tasks",
     "## 進行中: NewWidget実装
     - Signal/Slot定義
     - UI layout構築
     - イベントハンドリング実装"
   )

重要な判断時:
   mcp__serena__write_memory(
     "active-development-tasks",
     "## 技術的判断
     - Direct Widget Communication採用
       理由: パフォーマンス向上、コード簡素化"
   )

=== Phase 3: 完了後 ===

長期記憶化:
   cipher_store_reasoning_memory(
     title="LoRAIro NewWidget PySide6実装パターン",
     content='''
# NewWidget実装

## 設計アプローチ
- Direct Signal/Slot接続
- PySide6 Designerによる UI定義
- 型安全なシグナル定義

## 実装パターン
```python
class NewWidget(QWidget):
    data_changed = Signal(str)  # 型安全なシグナル

    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        # Qt Designer generated UI
        pass

    def _connect_signals(self):
        # Signal/Slot接続
        pass
```

## 教訓
- Qt Designerで効率的なUI構築
- 型ヒント付きSignal定義で安全性確保
- Direct Widget Communication で高速化
''',
     tags=["gui", "pyside6", "widget-pattern"],
     context="LoRAIro GUI feature development"
   )

Serenaメモリ更新:
   mcp__serena__write_memory(
     "current-project-status",
     "✅ NewWidget実装完了 → 次: 単体テスト作成"
   )
```

## ベストプラクティス

### 効率的なMemory使用
1. **実装前は必ずMemory確認**: 過去の知見を活用
2. **実装中は定期的に記録**: 中断からの再開を容易に
3. **完了後は必ず長期記憶化**: 将来の開発資産として蓄積

### 記録のタイミング
- **Serena write**: 重要な判断後、作業区切り、中断前
- **Cipher store**: 機能完了時、リファクタリング完了時、重要な技術判断後

### 記録すべき内容
#### Serena（短期）
- 今何をしているか
- 次に何をするか
- どんな課題があるか
- どんな判断をしたか（一時的）

#### Cipher（長期）
- なぜその設計をしたか
- どのような技術選定をしたか
- どんな結果が得られたか
- 何を学んだか（教訓）

## LoRAIro固有のMemory戦略

### Serena Memoryの活用
- **current-project-status**: 毎日の開発開始時に確認
- **active-development-tasks**: 実装中は1-2時間ごとに更新
- **feature実装メモ**: 複数日にまたがる実装の継続記録

### Cipher Memoryの活用
- **アーキテクチャ判断**: Repository Pattern、Service Layer、Direct Widget Communication
- **技術選定**: SQLAlchemy、PySide6、pytest の選定根拠
- **パフォーマンス改善**: キャッシュ統一、非同期処理、最適化アプローチ
- **リファクタリング**: 大規模変更の意図、効果、教訓

### 検索キーワード
- **Cipher検索**: 具体的パターン名（"repository pattern", "widget communication"）
- **技術名 + 用途**: "sqlalchemy transaction", "pyside6 threading"
- **LoRAIro固有用語**: "direct widget communication", "memory-first development"

## Examples
詳細な使用例は [examples.md](./examples.md) を参照してください。

## Reference
Memory操作の完全なワークフローとパターンは [reference.md](./reference.md) を参照してください。
