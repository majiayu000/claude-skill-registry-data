---
name: sharding-pattern
description: シャーディング対応のコードを書く際に使用。user_idベースのhash sharding、テーブル分割、クロスシャードクエリ、Repository実装時に自動適用。シャーディング、分散DB、テーブル分割、クロスDBクエリを扱う場合に使用。
allowed-tools: Read, Grep, Glob
---

# Sharding パターン

このプロジェクトのシャーディング実装パターンを定義します。

## シャーディング戦略

- **アルゴリズム**: Hash-based sharding (FNV-1a)
- **Shard Key**: `user_id` または エンティティの `id`
- **計算式**: `shard_id = hash(key) % shard_count + 1`
- **Shard数**: 4 DB

## テーブル分割

- **全テーブル数**: 32
- **DBあたりのテーブル数**: 8
- **テーブル名形式**: `{base_name}_{000-031}` (例: `users_000`, `users_031`)
- **テーブル番号計算**: `table_number = id % 32`
- **DB ID計算**: `db_id = (table_number / 8) + 1`

## 参照ファイル

シャーディング実装の参照:
- `server/internal/db/sharding.go` - ShardingStrategy, TableSelector
- `server/internal/db/group_manager.go` - GroupManager (DB接続管理)

Repository実装の参照:
- `server/internal/repository/user_repository.go` - 標準SQL版
- `server/internal/repository/user_repository_gorm.go` - GORM版

## コードパターン

### 1. テーブル名の取得

```go
tableSelector := db.NewTableSelector(32, 8)
tableName := tableSelector.GetTableName("users", userID)
// 例: userID=100 → "users_004"
```

### 2. DB接続の取得

```go
conn, err := groupManager.GetShardingConnectionByID(userID, "users")
if err != nil {
    return nil, fmt.Errorf("failed to get sharding connection: %w", err)
}
```

### 3. クロステーブルクエリ (List操作)

全シャードからデータを取得する場合:

```go
connections := r.groupManager.GetAllShardingConnections()
results := make([]*model.Entity, 0)

for _, conn := range connections {
    // このDBに含まれるテーブル（8つずつ）
    startTable := (conn.ShardID - 1) * 8
    endTable := startTable + 7

    for tableNum := startTable; tableNum <= endTable; tableNum++ {
        tableName := fmt.Sprintf("entities_%03d", tableNum)
        // クエリ実行...
    }
}
```

### 4. SQLインジェクション対策

動的テーブル名を使用する場合は必ず検証:

```go
if !db.ValidateTableName(tableName, []string{"users", "posts"}) {
    return nil, fmt.Errorf("invalid table name: %s", tableName)
}
```

## マイグレーション

シャーディングDBのマイグレーションは4つのディレクトリに分かれています:
- `db/migrations/sharding_1/`
- `db/migrations/sharding_2/`
- `db/migrations/sharding_3/`
- `db/migrations/sharding_4/`

各DBで同じテーブル構造を持ちますが、テーブル名のサフィックスが異なります。
