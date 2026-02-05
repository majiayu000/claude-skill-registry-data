---
name: coding
description: 代碼撰寫與自動化。觸發：code, script, tool, automate, batch, crawler, API, 寫程式, 腳本, 自動化
---

# Coding Skill

寫代碼解決問題，創建自動化腳本。

## Core Principle

**任何重複或可自動化的工作都值得寫腳本。**

## 與 Memory 整合

### 開始寫代碼前
```
→ memory_search: "coding style preference"
→ 找到用戶的代碼風格偏好
→ 套用偏好（語言、框架、風格）
```

### 學到新偏好時
```
→ 用戶表達偏好（如：「我喜歡用 async/await」）
→ memory_save:
    content: "偏好使用 async/await 而非 .then()"
    category: "preference"
    importance: 4
```

## 與 Reflection 整合

### 遇到錯誤時
```
→ 分析錯誤原因
→ 如果是常見錯誤模式
→ memory_save: 保存教訓
→ 下次避免同樣錯誤
```

### 完成後
```
→ 代碼是否符合預期？
→ 有沒有更好的方法？
→ 學到了什麼？
```

## 與 Proactive 整合

- 看到重複操作 → 主動建議自動化
- 發現可以用現有工具 → 主動提供
- 完成後 → 建議測試方式或下一步

## Workspace Structure

```
./
├── site/           # 網站檔案（Caddy serve）
├── projects/       # Git repos
├── scripts/        # 一次性腳本
├── tools/          # 可重用工具
└── data/           # 資料檔案
```

## Technology Stack

| 場景 | 推薦 |
|------|------|
| 通用腳本 | TypeScript + Bun |
| 資料處理 | TypeScript 或 Python |
| 網頁爬蟲 | Playwright / Cheerio |
| API 整合 | TypeScript + fetch |
| CLI 工具 | TypeScript + Commander |

## Workflow

1. **評估** - 會重複嗎？值得自動化嗎？
2. **查 Memory** - 有相關偏好或過去經驗嗎？
3. **設計** - 輸入/輸出？邊界情況？
4. **實作** - 寫到適當目錄
5. **測試** - `bun run <script>`
6. **反思** - 有什麼可以改進？

## Code Style

- **簡潔** - 10 行優於 100 行
- **可讀** - 清晰命名，必要註解
- **可靠** - 處理錯誤
- **可重用** - 考慮未來擴展

## TDD Approach

1. **理解** - 確認目標和驗收標準
2. **先測試** - 定義預期行為
3. **最小實作** - 只做需要的
4. **重構** - 測試通過後清理
5. **記錄** - 必要的文檔

原則：Make it work → Make it right → Make it fast

## Templates

### Simple Script
```typescript
#!/usr/bin/env bun

const main = async () => {
  // Main logic
}

main().catch(console.error)
```

### CLI Tool
```typescript
#!/usr/bin/env bun
import { parseArgs } from "util"

const { values } = parseArgs({
  args: Bun.argv.slice(2),
  options: {
    input: { type: "string", short: "i" },
    output: { type: "string", short: "o" },
  },
})
```

### Web Scraper
```typescript
#!/usr/bin/env bun
import * as cheerio from "cheerio"

const url = "https://example.com"
const html = await fetch(url).then(r => r.text())
const $ = cheerio.load(html)
```
