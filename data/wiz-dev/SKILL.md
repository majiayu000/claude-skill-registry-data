---
name: wiz-dev
description: |
  wizプロジェクト開発支援スキル。specs/ディレクトリの仕様書を参照し、TODOタスクを実装する。
  使用タイミング: (1) wizプロジェクトの開発作業、(2) specs/のTODOを進めたい時、
  (3) 「次のタスク」「TODO」「実装して」などの開発リクエスト時。
  作業完了後はdocs/を更新する。
---

# wiz Development Skill

## Workflow

1. **specs/を確認** - `specs/SPECIFICATION.md`を読み、現在のTODO状況を把握
2. **タスク選択** - ユーザーに次に取り組むタスクを確認（または提案）
3. **要件確認** - 詳細要件が不明な場合はユーザーに質問
4. **実装** - タスクを実装
5. **ドキュメント更新** - `docs/`に進捗や技術ドキュメントを追加/更新

## Specs Structure

`specs/SPECIFICATION.md`には以下のフェーズでTODOが定義されている:

- **Phase 1: Foundation (MVP)** - プロジェクト構造、ROS2 Bridge、WebSocket Server、Renderer、Frontend
- **Phase 2: Core Features** - TFフレーム、Marker、Path、PoseStamped
- **Phase 3: Extended** - Image、OccupancyGrid、パフォーマンスプロファイラ
- **Phase 4: Polish** - URDF、ドキュメント、E2Eテスト

## Task Selection

タスクを選ぶ際は以下を確認:

1. 現在のPhaseの未完了TODO
2. 依存関係（例: cxx FFIはCargo workspace後に実装）
3. ユーザーの優先度

不明な点があれば質問する:
- 「どのタスクから着手しますか？」
- 「〇〇の実装方針について確認させてください」

## Documentation (docs/)

作業完了後、`docs/`を更新:

- `docs/architecture.md` - アーキテクチャ決定事項
- `docs/api.md` - API仕様
- `docs/setup.md` - セットアップ手順
- `docs/progress.md` - 進捗状況

ファイルが存在しない場合は作成。既存ファイルは追記/更新。

## Implementation Notes

### Project Tech Stack
- **Frontend**: Rust + wgpu + egui (Native/WASM両対応)
- **Backend**: Rust + axum + tokio
- **ROS2 Bridge**: C++ (rclcpp) + cxx FFI
- **Protocol**: MessagePack over WebSocket

### Key Files
- `Cargo.toml` - Workspace root
- `crates/` - 各クレート
- `specs/SPECIFICATION.md` - 仕様書とTODO一覧
