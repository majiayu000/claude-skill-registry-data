---
name: lorairo-repository-pattern
description: SQLAlchemy repository pattern implementation for LoRAIro database operations with type-safe transactions, session management, and ORM best practices
allowed-tools: mcp__serena__find_symbol, mcp__serena__get_symbols_overview, mcp__serena__read_memory, Read, Edit, Write
---

# LoRAIro Repository Pattern Skill

このSkillは、LoRAIroプロジェクトにおけるSQLAlchemyリポジトリパターンの実装ガイドを提供します。

## 使用タイミング

- 新しいデータベースアクセス層の実装
- 既存リポジトリの拡張・リファクタリング
- データベーストランザクション処理の実装
- ORM クエリの最適化

## LoRAIroのRepository Pattern

### 基本構造

```python
from typing import Optional
from sqlalchemy.orm import Session
from src.lorairo.database.schema import Image

class ImageRepository:
    """画像データアクセスリポジトリ"""

    def __init__(self, session_factory):
        """
        Args:
            session_factory: SQLAlchemy session factory（scoped_session）
        """
        self.session_factory = session_factory

    def get_by_id(self, image_id: int) -> Optional[Image]:
        """IDで画像を取得"""
        with self.session_factory() as session:
            return session.query(Image).filter(Image.id == image_id).first()

    def get_all(self) -> list[Image]:
        """全画像を取得"""
        with self.session_factory() as session:
            return session.query(Image).all()

    def add(self, image: Image) -> Image:
        """新規画像を追加"""
        with self.session_factory() as session:
            session.add(image)
            session.commit()
            session.refresh(image)  # IDなどを更新
            return image

    def update(self, image: Image) -> Image:
        """画像を更新"""
        with self.session_factory() as session:
            session.merge(image)
            session.commit()
            return image

    def delete(self, image_id: int) -> bool:
        """画像を削除"""
        with self.session_factory() as session:
            image = session.query(Image).filter(Image.id == image_id).first()
            if image:
                session.delete(image)
                session.commit()
                return True
            return False
```

## 重要な実装パターン

### 1. Session管理

```python
# ✅ Good: with文による自動管理
with self.session_factory() as session:
    result = session.query(Image).all()
    return result  # with終了時に自動commit/rollback

# ❌ Bad: 手動Session管理
session = self.session_factory()
try:
    result = session.query(Image).all()
    session.commit()
    return result
finally:
    session.close()  # 冗長で エラープローン
```

### 2. トランザクション管理

```python
def batch_add_images(self, images: list[Image]) -> list[Image]:
    """複数画像を一括追加（単一トランザクション）"""
    with self.session_factory() as session:
        session.add_all(images)
        session.commit()
        # 全てのimagesにIDが設定される
        return images

def complex_operation(self, data: dict) -> bool:
    """複雑な複数テーブル操作"""
    with self.session_factory() as session:
        # 複数の操作を1トランザクションで
        image = Image(**data['image'])
        session.add(image)

        annotation = Annotation(image_id=image.id, **data['annotation'])
        session.add(annotation)

        session.commit()  # 全て成功時のみcommit
        return True
```

### 3. 型安全なクエリ

```python
from typing import Optional
from dataclasses import dataclass

@dataclass
class SearchCriteria:
    """検索条件（型安全）"""
    tags: Optional[list[str]] = None
    min_score: Optional[float] = None
    max_score: Optional[float] = None

class ImageRepository:
    def search(self, criteria: SearchCriteria) -> list[Image]:
        """型安全な検索"""
        with self.session_factory() as session:
            query = session.query(Image)

            if criteria.tags:
                # タグ条件
                query = query.filter(Image.tags.contains(criteria.tags))

            if criteria.min_score is not None:
                query = query.filter(Image.score >= criteria.min_score)

            if criteria.max_score is not None:
                query = query.filter(Image.score <= criteria.max_score)

            return query.all()
```

### 4. エラーハンドリング

```python
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from loguru import logger

def add_image_safe(self, image: Image) -> Optional[Image]:
    """安全な画像追加（エラーハンドリング付き）"""
    try:
        with self.session_factory() as session:
            session.add(image)
            session.commit()
            session.refresh(image)
            return image
    except IntegrityError as e:
        logger.error(f"Integrity error adding image: {e}")
        return None
    except SQLAlchemyError as e:
        logger.error(f"Database error adding image: {e}")
        return None
```

## LoRAIro固有のガイドライン

### ファイル配置
- **Repository**: `src/lorairo/database/db_repository.py`
- **Schema**: `src/lorairo/database/schema.py`
- **Manager**: `src/lorairo/database/db_manager.py`
- **Core**: `src/lorairo/database/db_core.py`

### 命名規則
- Repository class: `{Entity}Repository`（例: `ImageRepository`）
- Methods: CRUD操作 → `get_*`, `add`, `update`, `delete`
- Methods: 検索操作 → `search`, `find_*`, `filter_*`

### テスト戦略
```python
import pytest
from src.lorairo.database.db_core import create_test_engine
from src.lorairo.database.db_repository import ImageRepository

@pytest.fixture
def test_repository():
    """テスト用リポジトリ"""
    engine = create_test_engine()
    session_factory = scoped_session(sessionmaker(bind=engine))
    yield ImageRepository(session_factory)
    session_factory.remove()

def test_add_image(test_repository):
    """画像追加テスト"""
    image = Image(path="/test/image.jpg", phash="abc123")
    result = test_repository.add(image)

    assert result.id is not None
    assert result.path == "/test/image.jpg"
```

## ベストプラクティス

### DO ✅
- **with文使用**: Session管理を自動化
- **型ヒント**: 全メソッドに型ヒント
- **単一責任**: 1 Repositoryは1 Entity
- **トランザクション統一**: 関連操作は1トランザクション
- **ロギング**: エラー時は必ずログ

### DON'T ❌
- **Session手動管理**: try-finally は避ける
- **ビジネスロジック混入**: Repositoryは純粋なデータアクセスのみ
- **N+1 クエリ**: eager loading（`joinedload`）を使用
- **文字列SQL**: ORM メソッドを使用
- **グローバルSession**: 常にsession_factoryから取得

## 参考リソース
- 既存実装: `src/lorairo/database/db_repository.py`
- スキーマ定義: `src/lorairo/database/schema.py`
- テスト例: `tests/database/test_db_repository.py`
