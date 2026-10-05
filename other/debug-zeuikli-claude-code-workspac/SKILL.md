---
name: debug
description: 系統性 debug 工作流：捕捉錯誤、分析日誌、關聯跨系統 pattern，產出有根因與修復驗證的報告。適用於 bug、test 失敗、生產異常。
disable-model-invocation: true
context: fork
---

# Debug — 系統性除錯

## 觸發條件

- 出現錯誤訊息或 stack trace
- 測試失敗
- 程式行為非預期
- 生產環境出現異常（日誌分析、error spike）

## 除錯流程（6 步驟）

1. **Capture** — 取得完整錯誤訊息、stack trace、重現步驟
2. **Isolate** — 縮小故障範圍（模組、函式、時間點）
3. **Hypothesize** — 形成 2-3 個可能根因假設
4. **Test** — 用證據驗證假設（不要憑感覺猜）
5. **Fix** — 實作最小修復（不要順手清理無關的程式碼）
6. **Verify** — 確認修復有效，並排除引入新問題

## 快速診斷指令

```bash
# 查看最近哪些變更可能引起問題
git log --oneline -10
git diff HEAD~3

# 搜尋日誌中的錯誤模式
grep -rn "error\|Error\|ERROR" logs/ 2>/dev/null | tail -20

# 執行測試並捕捉輸出
npm test 2>&1 | tail -50       # Node.js
pytest -x --tb=short 2>&1      # Python
cargo test 2>&1 | tail -50     # Rust
go test ./... 2>&1             # Go
```

## 日誌分析

```bash
# 最近的錯誤與上下文
grep -B 5 -A 10 "ERROR" /var/log/app.log

# 統計錯誤類型頻率
grep -oE "Error: [^:]*" app.log | sort | uniq -c | sort -rn

# 某時段的錯誤
awk '/2026-04-18 14:/ && /ERROR/' app.log

# 找出高頻錯誤
grep "ERROR" app.log | cut -d']' -f2 | sort | uniq -c | sort -rn | head -20

# 錯誤 spike 分析
grep "ERROR" app.log | cut -d' ' -f1-2 | uniq -c | sort -rn
```

## 常見 Error Pattern

| Pattern | 指向 | 行動 |
|---------|------|------|
| NullPointer / undefined | 缺少 null check | 加入防衛性驗證 |
| Timeout | 依賴服務慢 | 加 timeout + retry |
| Connection refused | 服務未啟動 | 檢查 health endpoint |
| OOM | 記憶體洩漏 | 用 profiler 找洩漏點 |
| Rate limit | 請求過多 | 加 backoff + 佇列 |

## 跨系統關聯查詢（SQL）

```sql
-- 某 endpoint 的錯誤頻率
SELECT endpoint, count(*) as errors
FROM logs
WHERE level = 'ERROR' AND time > NOW() - INTERVAL '1 hour'
GROUP BY endpoint ORDER BY errors DESC;

-- 用 request_id 跨服務追蹤
SELECT service, message, time
FROM logs
WHERE request_id = 'req-xxxxx'
ORDER BY time;
```

## 輸出格式

```markdown
## Debug Report

**Issue:** [一句話描述問題]
**Root Cause:** [實際根因]

### Evidence
- [找到的具體證據 1]
- [找到的具體證據 2]

### Fix
[程式碼或設定的最小修復]

### Verification
[如何確認修復有效：指令或測試]

### Prevention
[如何預防此問題再次發生]
```

## Gotcha

- **只做最小修復**：debug 不是重構，不要順手改不相關的程式碼
- **假設要有證據**：每個假設必須由工具呼叫驗證，不憑直覺
- **先跑相關測試**：不要跑全套測試套件，先跑最相關的一個測試確認方向
- **記錄 root cause**：修完後把根因和修復方式寫進 commit message，有助於日後 retro 分析
