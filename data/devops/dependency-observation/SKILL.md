---
name: dependency-observation
description: "依存関係の取り違えを検出する観測。lockfile固定、クリーンビルド、統合スモークで再現性を担保。Use when: 依存追加/更新、CI設定、ローカルでは動く問題、新環境セットアップ、バージョン差異の疑い。"
---

# Dependency Observation（依存取り違え観測）

## 目的

生成コードは「見たことあるAPIっぽいもの」を書きがちで、依存取り違えは頻出。
このスキルは"works on my machine"を潰し、**依存の再現性を確保**する。

## 観測の恩恵

- "works on my machine"を潰す（再現性の確保）
- 依存の更新がどこに影響するかが見える
- セキュリティ（供給網）にも直結する

## Procedure

### Step 1: 依存固定の確認

lockfile が存在し、かつCIで固定が破られたら即failするか確認。

**言語別lockfile**：
| 言語 | lockfile |
|------|----------|
| Node.js | package-lock.json / yarn.lock / pnpm-lock.yaml |
| Python | poetry.lock / Pipfile.lock / requirements.txt (pip-compile) |
| Go | go.sum |
| Rust | Cargo.lock |
| Ruby | Gemfile.lock |

### Step 2: クリーンビルドの実施

キャッシュに頼らないビルドを実行：

```bash
# Node.js
rm -rf node_modules && npm ci

# Python (poetry)
rm -rf .venv && poetry install

# Go
go clean -cache && go build ./...

# Rust
cargo clean && cargo build
```

### Step 3: 依存グラフの観測

どのバージョンが入っているかを出力：

```bash
# Node.js
npm ls --all

# Python
pip list --format=freeze

# Go
go list -m all

# Rust
cargo tree
```

### Step 4: 統合スモークテスト

"本物の依存"で最小経路だけ叩く：

```python
# 例: DB接続→1クエリのスモークテスト
def test_database_smoke():
    conn = get_db_connection()
    result = conn.execute("SELECT 1").fetchone()
    assert result[0] == 1
```

### Step 5: 起動時の依存情報ログ

起動時に依存バージョンと設定をログ出力（トラブルシュートの生命線）：

```json
{
  "event": "app_started",
  "runtime": "python 3.11.5",
  "dependencies": {
    "sqlalchemy": "2.0.23",
    "pydantic": "2.5.2"
  }
}
```

## 最小セット

- **(C1)** lockfile固定 ＋ CIで"固定破り即fail"
- **(C2)** クリーンビルド ＋ 最小の統合スモーク（1本で良い。ゼロは危険）

## CI設定例

詳細は `references/ci-templates.md` を参照。

## Outputs

- 依存チェックリスト
- CI設定ファイル（.github/workflows/ 等）
- 統合スモークテストコード

## Examples

### GitHub Actions での依存固定チェック

```yaml
name: Dependency Check
on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check lockfile exists
        run: |
          if [ ! -f package-lock.json ]; then
            echo "❌ package-lock.json not found"
            exit 1
          fi

      - name: Clean install (fail on lockfile mismatch)
        run: npm ci

      - name: Smoke test
        run: npm run test:smoke
```

### 統合スモークテスト例

```typescript
// tests/smoke.test.ts
describe('Integration Smoke', () => {
  it('connects to database', async () => {
    const db = await createConnection();
    const result = await db.query('SELECT 1 as value');
    expect(result[0].value).toBe(1);
    await db.close();
  });

  it('external API is reachable', async () => {
    const response = await fetch(process.env.API_ENDPOINT + '/health');
    expect(response.ok).toBe(true);
  });
});
```
