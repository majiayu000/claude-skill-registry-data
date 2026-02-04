---
name: concurrency-observation
description: "並行性の観測。データレース、デッドロック、タイミング依存バグを検出。Use when: async/await実装、スレッド/goroutine使用、共有状態操作、本番でだけ起きる問題、たまに落ちるテスト調査。"
---

# Concurrency Observation（並行性観測）

## 目的

並行性バグは「通常テストが通るのに本番で死ぬ」の代表。
このスキルは、非決定性を**再現可能な失敗に変える**。

## 観測の恩恵

- 非決定性を"再現可能な失敗"に変える
- 「怖いから触れない」を減らし、変更可能性が上がる
- 事故が起きたときの原因切り分けが可能になる

## 典型的な並行性バグ

| バグ種別 | 症状 | 検出方法 |
|---------|------|---------|
| データレース | 同時書き換え／読み書き競合 | レースデテクタ |
| デッドロック | ロック順、待ち合わせ | デッドロック検出 |
| ライブロック | 特定条件で進まない | タイムアウト監視 |
| await忘れ | 非同期順序の取り違え | 静的解析 |
| キャンセル漏れ | リソースリーク | ストレステスト |

## Procedure

### Step 1: 共有可変状態の特定

並行アクセスされる共有可変状態を列挙：

```
[ ] グローバル変数
[ ] シングルトンの可変フィールド
[ ] キャッシュ（in-memory）
[ ] 接続プール
[ ] ファイルシステム
```

### Step 2: レースデテクタの適用

**言語別の実行方法**：

```bash
# Go
go test -race ./...

# Rust
cargo +nightly miri test

# C/C++
clang -fsanitize=thread -g program.c

# Python (ThreadSanitizer with C extensions)
# 直接サポートなし → ストレステストで補完

# Node.js
# 直接サポートなし → ストレステストで補完
```

### Step 3: ストレステストの実施

"たまたま通る"を潰すための増幅器：

```python
import concurrent.futures
import threading

def test_counter_under_stress():
    counter = SharedCounter()

    def increment_many():
        for _ in range(1000):
            counter.increment()

    # 100スレッドで同時実行
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(increment_many) for _ in range(100)]
        concurrent.futures.wait(futures)

    # 期待値: 100 * 1000 = 100,000
    assert counter.value == 100000
```

### Step 4: タイムアウトと飽和の監視

```python
# キュー飽和の監視
def test_queue_does_not_saturate():
    queue = TaskQueue(max_size=1000)

    # 大量タスク投入
    for i in range(10000):
        queue.put(Task(i))

    # 一定時間内に処理完了
    start = time.time()
    queue.join()
    elapsed = time.time() - start

    assert elapsed < 60  # 60秒以内に完了
    assert queue.dropped_count == 0  # ドロップなし
```

### Step 5: 運用メトリクスの設定

```yaml
# 並行性関連メトリクス
metrics:
  - name: thread_pool_active_threads
    type: gauge
    labels: [pool_name]

  - name: queue_depth
    type: gauge
    labels: [queue_name]

  - name: request_timeout_total
    type: counter
    labels: [endpoint]

  - name: lock_wait_seconds
    type: histogram
    labels: [lock_name]
```

## 最小セット（条件付き）

並行性がある領域のみ適用：

- **(E1)** レースデテクタ/サニタイザをCIで回す（対象モジュールだけでも）
- **(E2)** ストレス（反復）を1本
- **(E3)** タイムアウト＋飽和メトリクス（運用で"詰まり"を見える化）

## 設計パターン（予防）

並行性バグを予防する設計パターン：

| パターン | 説明 |
|---------|------|
| スレッド閉じ込め | 特定スレッドのみがデータにアクセス |
| イミュータブル | 変更不可なデータ構造 |
| メッセージパッシング | チャネル/アクター経由の通信 |
| 読み書きロック | 読み取りは並行、書き込みは排他 |

## Outputs

- 共有可変状態の一覧
- レースデテクタ設定（CI統合）
- ストレステストコード
- 並行性メトリクス設定

## Examples

### Go のレースデテクタ CI設定

```yaml
# .github/workflows/race.yml
name: Race Detection
on: [push, pull_request]

jobs:
  race:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v4
        with:
          go-version: '1.21'

      - name: Run tests with race detector
        run: go test -race -v ./...
```

### Node.js のストレステスト

```typescript
import { Worker } from 'worker_threads';

describe('Concurrency Stress', () => {
  it('handles concurrent writes without data loss', async () => {
    const writes: Promise<void>[] = [];

    // 100並列で書き込み
    for (let i = 0; i < 100; i++) {
      writes.push(db.insert({ id: i, value: `data-${i}` }));
    }

    await Promise.all(writes);

    // 全件書き込まれていること
    const count = await db.count();
    expect(count).toBe(100);
  });
});
```
