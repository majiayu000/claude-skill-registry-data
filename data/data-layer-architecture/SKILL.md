---
name: data-layer-architecture
description: Bronze Layer（LLM抽出ログ層）とGold Layer（確定データ層）の2層アーキテクチャ設計。LLM抽出結果の履歴管理と人間修正の保護を実現。抽出処理の実装、ExtractionLogの使用、is_manually_verifiedフラグの扱いに関するガイダンスを提供。
---

# Data Layer Architecture（Bronze Layer / Gold Layer）

## Purpose
LLM抽出結果と確定データを分離する2層アーキテクチャの設計ガイド。AIの抽出履歴を保持しながら、人間の修正を保護する。

## When to Activate
このスキルは以下の場合にアクティベートされます：
- LLM抽出処理を新規実装する時
- ExtractionLogエンティティを使用する時
- `is_manually_verified`フラグを扱う時
- 抽出結果からGoldエンティティを更新する時
- Bronze/Gold Layerの設計について質問された時

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Bronze Layer（抽出ログ層）                 │
│                                                              │
│  - LLM抽出結果を追記専用（Immutable）で保存                   │
│  - 精度分析・トレーサビリティのための履歴                      │
│  - テーブル: extraction_logs                                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ is_manually_verified = false の場合のみ反映
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Gold Layer（確定データ層）                  │
│                                                              │
│  - アプリケーションが参照する唯一の正解データ                   │
│  - 人間の修正が優先される                                     │
│  - テーブル: statements, politicians, speakers, etc.         │
└─────────────────────────────────────────────────────────────┘
```

## Design Principles

### 1. Bronze Layer（抽出ログ層）
- **目的**: LLM抽出結果の履歴保持、精度分析
- **特性**: 追記専用（Immutable）、削除・更新なし
- **用途**:
  - AIモデル改善の検証データ
  - 抽出精度の時系列分析
  - デバッグ・トラブルシューティング

### 2. Gold Layer（確定データ層）
- **目的**: ユーザーに提供する正解データ
- **特性**: 人間の修正が最優先
- **用途**:
  - Streamlit UIでの表示
  - API経由でのデータ提供
  - レポート・分析の基礎データ

## Data Flow

```
LLM抽出実行
    │
    ▼
┌────────────────────────────┐
│ ExtractionLog に必ず保存    │  ← Bronze Layer（常に履歴として残る）
│ （Immutable）               │
└────────────────────────────┘
    │
    ▼
┌────────────────────────────┐
│ is_manually_verified?      │
└────────────────────────────┘
    │                │
    │ false          │ true
    │（未検証）       │（検証済み）
    ▼                ▼
┌──────────┐    ┌──────────────────┐
│ Gold更新  │    │ Gold更新しない    │
│          │    │（人間の修正を保護）│
└──────────┘    └──────────────────┘
```

## Target Entities

| 抽出オブジェクト（Bronze） | → | 確定オブジェクト（Gold） |
|---------------------------|---|-------------------------|
| StatementExtraction | → | Statement（発言） |
| PoliticianExtraction | → | Politician（政治家） |
| SpeakerExtraction | → | Speaker（話者） |
| ConferenceMemberExtraction | → | ConferenceMember（会議体メンバー） |
| ParliamentaryGroupMemberExtraction | → | ParliamentaryGroupMember（議員団メンバー） |

## Key Components

### ExtractionLog Entity

```python
class EntityType(Enum):
    STATEMENT = "statement"
    POLITICIAN = "politician"
    SPEAKER = "speaker"
    CONFERENCE_MEMBER = "conference_member"
    PARLIAMENTARY_GROUP_MEMBER = "parliamentary_group_member"

@dataclass
class ExtractionLog:
    id: UUID
    entity_type: EntityType          # どのエンティティの抽出か
    entity_id: UUID                  # 対象GoldエンティティのID
    pipeline_version: str            # "gemini-2.0-flash-v1" など
    extracted_data: dict             # AIが出した生データ（JSON）
    confidence_score: Optional[float]
    extraction_metadata: dict        # モデル名、トークン数等
    created_at: datetime             # Immutable
```

### Gold Entity Common Fields

```python
# 全Goldエンティティ（Statement, Politician等）に追加
is_manually_verified: bool = False      # 人間が検証済みか
latest_extraction_log_id: Optional[UUID] # 最新の抽出ログへの参照
```

## Behavior Rules

| 状態 | AI再抽出時の動作 | 理由 |
|------|-----------------|------|
| `is_manually_verified = false` | Gold Layerを更新 | 最新AIの精度向上を反映 |
| `is_manually_verified = true` | Gold Layerは更新しない | 人間の判断を最優先 |
| （両方） | Bronze Layerには常に保存 | 履歴・分析用 |

## Implementation Guide

### Adding New Extraction Process

1. `UpdateEntityFromExtractionUseCase` を継承して実装
2. 抽出結果は必ず `ExtractionLog` に保存
3. `is_manually_verified` フラグをチェックしてから Gold を更新

```python
class UpdateStatementFromExtractionUseCase(UpdateEntityFromExtractionUseCase):
    async def execute(
        self,
        entity_id: UUID,
        extraction_result: StatementExtractionResult,
        pipeline_version: str
    ) -> UpdateEntityResult:
        # 1. Bronze Layer: 抽出ログを必ず保存
        log = ExtractionLog(
            entity_type=EntityType.STATEMENT,
            entity_id=entity_id,
            pipeline_version=pipeline_version,
            extracted_data=extraction_result.to_dict(),
            ...
        )
        log_id = await self._extraction_log_repo.save(log)

        # 2. Gold Layer: 人間修正済みならスキップ
        entity = await self._statement_repo.find_by_id(entity_id)
        if entity.is_manually_verified:
            return UpdateEntityResult(updated=False, reason="manually_verified")

        # 3. Gold Layer: 未検証なら更新
        entity.update_from_extraction(extraction_result)
        entity.latest_extraction_log_id = log_id
        await self._statement_repo.save(entity)

        return UpdateEntityResult(updated=True)
```

### Handling Human Modifications

1. Gold エンティティを直接更新
2. `is_manually_verified = true` をセット
3. 以降のAI再抽出では上書きされない

```python
async def mark_as_verified(entity_id: UUID) -> None:
    entity = await repo.find_by_id(entity_id)
    entity.is_manually_verified = True
    await repo.save(entity)
```

## Quick Checklist

新しい抽出処理を実装する際のチェックリスト：

- [ ] `ExtractionLog` にログを保存しているか
- [ ] `is_manually_verified` をチェックしているか
- [ ] `latest_extraction_log_id` を更新しているか
- [ ] `pipeline_version` を適切に設定しているか
- [ ] エラー時もログが保存されるか
- [ ] 単体テストを書いたか

## Related Issues
- Product Goal: [#813](https://github.com/trust-chain-organization/sagebase/issues/813)
- Implementation PBIs: #861〜#872

## References
- [ARCHITECTURE.md](docs/ARCHITECTURE.md): System architecture overview
- [DOMAIN_MODEL.md](docs/DOMAIN_MODEL.md): Domain entities
- [DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md): Database structure
