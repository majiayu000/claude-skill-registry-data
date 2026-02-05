---
name: 階層IDの競合安全な採番（counters 方式）
description: >
  REQ/TSK/SUB の三階層IDを同時作成でも重複させないため、counters(scope,last) を
  トランザクションでインクリメントして採番する手法。ユニーク違反時は指数バックオフでリトライする。
---

# 使い方
- scope 例: `REQ`, `REQ-001.TSK`, `REQ-001.TSK-001.SUB`
- 1 Tx 内で `SELECT ... FOR UPDATE` → `UPDATE last=last+1`
- 失敗（ユニーク違反）が発生した場合はバックオフしてリトライ

## 手順（擬似）
1. BEGIN
2. `SELECT last FROM counters WHERE scope=:scope FOR UPDATE`
3. `UPDATE counters SET last=last+1 WHERE scope=:scope`
4. COMMIT
5. `hier_id = f"{scope}-{last:03}"` を生成

## 例
- `examples/id_alloc.sql`
