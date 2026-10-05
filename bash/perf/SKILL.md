---
name: perf
description: 效能分析與最佳化：量測 baseline、定位瓶頸、優化最高影響項、驗證改善效果。適用於應用程式慢、API 超時、前端 Core Web Vitals 問題。
disable-model-invocation: true
context: fork
---

# Perf — 效能工程

## 觸發條件

- 應用程式慢或無回應
- API 回應時間超標
- 前端頁面載入過慢
- 擴充基礎設施前，先確認是否有軟體層優化空間
- Core Web Vitals 警示（LCP / FID / CLS）

## 優化流程（4 步驟）

1. **Measure** — 先量測，有 baseline 才能比較（不要憑感覺優化）
2. **Identify** — 找到最大瓶頸（用 80/20 原則：20% 的程式碼造成 80% 的效能問題）
3. **Optimize** — 優先修復影響最大的問題，一次一個
4. **Verify** — 用相同工具重新量測，確認改善數字

## Profiling 指令

```bash
# Node.js
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Python
python -m cProfile -o output.prof script.py
python -m pstats output.prof

# Go
go tool pprof http://localhost:6060/debug/pprof/profile

# CLI 效能比較（用 hyperfine，需安裝）
hyperfine 'command_a' 'command_b' --warmup 3
```

## 常見瓶頸分類

### 資料庫
- 缺少索引（在 WHERE / JOIN 欄位加索引）
- N+1 查詢（改用 eager loading 或 JOIN）
- 大結果集（加分頁）

### 記憶體
- 記憶體洩漏（檢查 event listener、closure 未釋放）
- 大物件緩衝（改用 stream 處理）
- 無 TTL 的 cache（加過期時間）

### CPU
- 同步阻塞操作（改 async）
- 複雜演算法（加 memoize 或改更優算法）
- 不必要的重複計算（cache 中間結果）

### 網路
- 請求過多（batch / 合併）
- 大 payload（壓縮、分頁）
- 未使用快取（加 CDN、browser cache header）

## 效能預算（參考值）

| 指標 | 目標 | 說明 |
|------|------|------|
| API 回應 | <200ms (P95) | 排除網路 RTT |
| 頁面載入（4G） | <1s | Time to Interactive |
| LCP | <2.5s | Largest Contentful Paint |
| FID / INP | <100ms | 互動回應 |
| CLS | <0.1 | 版面穩定性 |
| Bundle Size | <500KB gzip | JS bundle |

## 輸出格式

```markdown
## Performance Report

**Before:** [baseline 量測數字]
**After:**  [優化後數字]
**Improvement:** [百分比改善]

### Bottlenecks Identified
1. [問題] — Impact: High / Medium / Low

### Optimizations Applied
1. [改動] → [結果]

### Remaining Headroom
[還有哪些可以優化但本次未做]
```

## Gotcha

- **不要在沒有 baseline 的情況下優化**：沒有量測就是猜測
- **一次只改一件事**：否則無法判斷哪個改動有效
- **優化後重跑相同場景**：確保量測條件一致才能比較
- **搭配 `context-report` skill**：若問題是 Claude Code session 效率，用 `/context-report` 而非本 skill
