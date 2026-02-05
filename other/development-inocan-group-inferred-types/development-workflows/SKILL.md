---
name: development-workflows
description: Polibaseの開発ワークフローとパターンを説明します。Docker-first開発、環境変数管理、新機能追加手順など、日常的な開発作業のベストプラクティスをカバーします。
---

# Development Workflows（開発ワークフロー）

## 目的
Polibaseの開発パターン、ワークフロー、ベストプラクティスを理解し、効率的で一貫性のある開発を実現します。

## いつアクティベートするか
このスキルは以下の場合に自動的にアクティベートされます：
- 新機能の実装を開始する時
- ユーザーが「新機能」「フィーチャー追加」「開発フロー」と言った時
- セットアップや環境構築時
- Docker関連の作業時

## 開発パターン

### 1. Docker-first開発

**すべてのコマンドはDockerコンテナ内で実行します**

#### 基本パターン
```bash
# コマンド実行の基本形
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase <command>

# 例: Pythonスクリプト実行
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase uv run python src/script.py

# 例: テスト実行
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase uv run pytest

# 例: データベース接続
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec postgres psql -U sagebase_user -d sagebase_db
```

#### ショートカット（just コマンド）
```bash
# just を使った短縮形
just exec uv run python src/script.py
just test
just db
```

#### 理由
- 環境の一貫性
- 依存関係の管理
- CI/CDとの整合性
- チーム全体で同じ環境

### 2. Multi-phase Processing

**処理は必ず決められた順序で実行します**

#### 議事録処理の順序
```bash
# ステップ1: 議事録を分割
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase uv run sagebase process-minutes

# ステップ2: 話者を抽出
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase uv run python src/extract_speakers_from_minutes.py

# ステップ3: 話者をマッチング
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase uv run python update_speaker_links_llm.py
```

**⚠️ この順序を変更しないこと！**

#### Web Scraping → GCS → Processing
```bash
# ステップ1: スクレイピング + GCS アップロード
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase uv run sagebase scrape-minutes --upload-to-gcs

# ステップ2: GCSから処理
docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] exec sagebase uv run sagebase process-minutes --meeting-id <id>

# ステップ3: 以降は標準フローと同じ
```

### 3. 環境変数の使い分け

#### Docker環境
```bash
# docker-compose.yml で定義
DATABASE_URL=postgresql://sagebase_user:sagebase_password@postgres:5432/sagebase_db
GOOGLE_API_KEY=${GOOGLE_API_KEY}
```

#### ローカル環境
```bash
# .env ファイルで定義
DATABASE_URL=postgresql://sagebase_user:sagebase_password@localhost:5432/sagebase_db
GOOGLE_API_KEY=your-api-key-here
```

**注意:** DATABASE_URLのホスト名が異なります
- Docker: `postgres` (サービス名)
- ローカル: `localhost`

### 4. 新機能追加の手順

Clean Architectureに従って、内側から外側へ実装します：

#### ステップ1: Domain層
```bash
# Entity定義
src/domain/entities/new_entity.py

# Repository Interface定義
src/domain/repositories/i_new_entity_repository.py

# Domain Service（必要な場合）
src/domain/services/new_entity_domain_service.py
```

#### ステップ2: Application層
```bash
# UseCase実装
src/application/usecases/manage_new_entity_usecase.py

# DTO定義
src/application/dtos/new_entity_dto.py
```

#### ステップ3: Infrastructure層
```bash
# Repository実装
src/infrastructure/persistence/new_entity_repository_impl.py

# マイグレーション作成
database/migrations/XXX_create_new_entity.sql
```

#### ステップ4: Interfaces層
```bash
# CLI追加（必要な場合）
src/interfaces/cli/new_entity_commands.py

# Web UI追加（必要な場合）
src/interfaces/web/streamlit/views/new_entity_view.py
```

#### ステップ5: テスト
```bash
# 各層のテスト作成
tests/unit/domain/test_new_entity.py
tests/unit/application/test_manage_new_entity_usecase.py
tests/integration/test_new_entity_repository.py
```

## クイックチェックリスト

### 環境セットアップ
- [ ] **Dockerが起動しているか**
- [ ] **`.env` ファイルが存在するか** (`cp .env.example .env`)
- [ ] **GOOGLE_API_KEYが設定されているか**
- [ ] **コンテナが起動しているか** (`docker compose -f docker/docker-compose.yml [-f docker/docker-compose.override.yml] up -d`)

### 新機能実装前
- [ ] **Domain層から開始するか**
- [ ] **Repository Interfaceを定義したか**
- [ ] **DTOを定義したか**
- [ ] **マイグレーションファイルを作成したか**

### 実装中
- [ ] **Docker内でコマンド実行しているか**
- [ ] **処理順序を守っているか**
- [ ] **環境変数を正しく使い分けているか**

### 実装後
- [ ] **各層のテストを書いたか**
- [ ] **ドキュメントを更新したか**
- [ ] **マイグレーションをテストしたか** (`./reset-database.sh`)

## 詳細リファレンス

詳細なワークフローとトラブルシューティングは [reference.md](reference.md) を参照してください。

## 関連スキル

- [clean-architecture-checker](../clean-architecture-checker/): アーキテクチャガイド
- [test-writer](../test-writer/): テスト作成ガイド
- [migration-helper](../migration-helper/): データベース移行ガイド
- [data-processing-workflows](../data-processing-workflows/): データ処理フロー
