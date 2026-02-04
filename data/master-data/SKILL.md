---
name: master-data
description: マスターデータ（SQLite）のパターンとチェックリスト。新規マスタ追加時に参照。
---

# Master Data Patterns

## 概要

マスターデータはSQLiteから読み込む読み取り専用データ。

```
SQLite → SQLiteMasterDataManager → MasterDataLoader → MasterDataCache
                                                            ↓
                                                    各サービスで使用
```

## Definition型

`Domain/MasterData/` に配置。

ルール:
- `struct` + `Identifiable` + `Sendable` + `Hashable`
- `let` で不変
- ネストした構造体で関連データをグループ化

## SQLiteクエリ

`Application/MasterData/SQLite/SQLiteMasterDataQueries.*.swift` に配置。

ルール:
- `SQLiteMasterDataManager` のextensionとして実装
- ファイル名は `SQLiteMasterDataQueries.{Entity}.swift`
- 複雑な結合はBuilderパターンを使用

## 新規マスターデータ追加時のチェックリスト

1. `Domain/MasterData/` に `*MasterModels.swift` 作成
   - `*Definition` 構造体を定義
2. `Application/MasterData/SQLite/SQLiteMasterDataQueries.*.swift` 作成
   - `fetchAll*()` メソッドを実装
3. `MasterDataCache.swift` にプロパティ追加
4. `MasterDataLoader.swift` でロード処理追加
5. 必要に応じてゲーム用語定義を更新
