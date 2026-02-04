---
name: mongo-ts
description: MongoDB CLI 工具。直接執行 MongoDB 查詢語法，支援 CRUD、聚合、索引管理。輸出格式：table/json/csv/yaml。預設唯讀模式保護生產環境。
---

# mongo-ts

MongoDB 命令列工具，直接執行查詢語法。

## 執行方式

Plugin 安裝後首次需 build：

```bash
cd ${PLUGIN_ROOT} && pnpm install && pnpm build
```

執行查詢：

```bash
node ${PLUGIN_ROOT}/dist/bin/mongots.js -u "mongodb://..." -q "db.users.find()"
```

## 命令選項

| 選項 | 說明 |
|------|------|
| `-q, --query <query>` | 執行查詢字串（必填） |
| `-u, --uri <uri>` | MongoDB 連線字串 |
| `-d, --db <database>` | 指定資料庫 |
| `-f, --format <type>` | 輸出格式：table/json/csv/yaml（預設 table）|
| `--allow-write` | 允許寫入操作（預設唯讀）|
| `--quiet` | 靜默模式，只輸出資料 |
| `--verbose` | 詳細模式 |

## 使用範例

```bash
# 查詢
mongots -u "mongodb://..." -q "db.users.find()"
mongots -q "db.users.findOne({name: 'test'})"

# 新增（需 --allow-write）
mongots --allow-write -q "db.users.insertOne({name: 'test'})"

# 更新
mongots --allow-write -q "db.users.updateOne({_id: '...'}, {\$set: {name: 'new'}})"

# 刪除
mongots --allow-write -q "db.users.deleteOne({_id: '...'})"

# 聚合
mongots -q "db.orders.aggregate([{\$group: {_id: '\$status'}}])"

# 管理
mongots -q "show dbs"
mongots -q "show collections"
mongots -q "db.stats()"
```

## 連線設定

優先順序：CLI 參數 > 環境變數 > 設定檔

### 首次使用

若不知道連線資訊，使用 `AskUserQuestion` 詢問以下環境變數，並詢問是否寫入 `.env`：

| 變數 | 說明 | 範例 |
|------|------|------|
| `MONGO_TS_URI` | MongoDB 連線字串（必填）| `mongodb://localhost:27017/mydb` |
| `MONGO_TS_DB` | 預設資料庫（選填，覆蓋 URI）| `mydb` |
| `MONGO_TS_FORMAT` | 輸出格式（選填）| `table`/`json`/`csv`/`yaml` |
| `MONGO_TS_ALLOW_WRITE` | 允許寫入（選填）| `true` |

### 設定方式

1. **CLI 參數**：`-u "mongodb://localhost:27017"`
2. **環境變數**：`.env` 檔案或系統環境變數
3. **設定檔**：`~/.mongots/config.json`

```json
{
  "uri": "mongodb://localhost:27017",
  "defaultDb": "mydb",
  "format": "table",
  "allowWrite": false
}
```

## 支援的查詢語法

| 類型 | 範例 |
|------|------|
| 查詢 | `db.coll.find({})`, `db.coll.findOne({})` |
| 新增 | `db.coll.insertOne({})`, `db.coll.insertMany([])` |
| 更新 | `db.coll.updateOne({}, {})`, `db.coll.updateMany({}, {})` |
| 刪除 | `db.coll.deleteOne({})`, `db.coll.deleteMany({})` |
| 聚合 | `db.coll.aggregate([])` |
| 計數 | `db.coll.countDocuments({})` |
| 索引 | `db.coll.createIndex({})`, `db.coll.getIndexes()` |
| 管理 | `show dbs`, `show collections`, `db.stats()` |

## 唯讀模式（預設）

預設為唯讀模式，使用 `--allow-write` 啟用寫入操作。

**唯讀允許**：find, findOne, countDocuments, aggregate（無 $out/$merge）, getIndexes, stats, show dbs/collections

**需要 `--allow-write`**：insert*, update*, delete*, drop*, createIndex, dropIndex

## 輸出格式

### Table（預設，Markdown 格式）

```text
_id                      | name  | age
------------------------ | ----- | ---
507f1f77bcf86cd799439011 | Alice | 25
507f1f77bcf86cd799439012 | Bob   | 30
```

### JSON

```bash
mongots -q "db.users.find()" -f json
```

### CSV

```bash
mongots -q "db.users.find()" -f csv
```

### YAML

```bash
mongots -q "db.users.find()" -f yaml
```
