---
name: life
description: 生活管理系統。觸發：早安, 晚安, 今天, 規劃, 回顧, 健康, 投資, 股票, 追蹤, watchlist, morning, evening, daily, plan, review
---

# Life Skill

生活驅動的 AI 助理系統。整合健康、任務、投資追蹤，讓生活事件驅動 AI 主動行動。

## 核心理念

**生活驅動，而非被動回應**

- 早上問好 → 自動整理今日概覽
- 提到股票 → 關聯 watchlist 記憶
- 健康數據異常 → 主動提醒
- 月底 → 產生月報

## Workflow Routing

| 觸發 | Workflow |
|------|----------|
| 早安 / morning / 今天計畫 | [workflows/morning.md](workflows/morning.md) |
| 晚安 / evening / 回顧 | [workflows/evening.md](workflows/evening.md) |
| 週報 / weekly | [workflows/weekly.md](workflows/weekly.md) |

## Domain Routing

| 領域 | 觸發詞 | Domain File |
|------|--------|-------------|
| 健康 | 運動, 睡眠, 心率, garmin, 體重 | [domains/health.md](domains/health.md) |
| 投資 | 股票, 買, 賣, 持倉, watchlist | [domains/investment.md](domains/investment.md) |

## MCP Tools 整合

### 必用工具

| 工具 | 用途 | 何時使用 |
|------|------|----------|
| `memory_search` | 搜尋相關記憶 | 每次對話開始 |
| `memory_save` | 保存重要資訊 | 發現可複用資訊時 |
| `google_calendar_events` | 今日行程 | Morning workflow |
| `google_tasks_list` | 待辦事項 | Morning/Evening workflow |
| `garmin_summary` | 健康摘要 | Morning workflow、健康話題 |

### 記憶分類

| Category | 用途 | 範例 |
|----------|------|------|
| `health` | 健康狀況 | 「最近睡眠品質不佳」「體重 72kg」 |
| `investment` | 投資紀錄 | 「AAPL 買在 $182」「TSM 觀望中」 |
| `watchlist` | 持續追蹤項 | 「關注 AI 領域發展」「追蹤某專案進度」 |
| `preference` | 偏好設定 | 「喜歡簡潔回覆」 |
| `event` | 重要事件 | 「完成 Merlin 部署」 |
| `work` | 工作相關 | 「正在開發 X 功能」 |

## Morning Flow

```
用戶：早安 / 今天有什麼

1. garmin_summary → 健康摘要
2. google_calendar_events → 今日行程
3. google_tasks_list → 待辦事項
4. memory_search "watchlist investment" → 追蹤項目

輸出：整合後的今日概覽
```

## Evening Flow

```
用戶：晚安 / 今天回顧

1. garmin_summary → 今日健康數據
2. google_tasks_list → 完成了什麼
3. memory_search "today" → 今日發生的事

輸出：今日摘要 + 明日建議
如有重要發現 → memory_save
```

## 投資追蹤邏輯

```
用戶：我買了 AAPL 在 $180

→ memory_save:
  content: "2024-01-15 買入 AAPL @ $180"
  category: "investment"
  importance: 4

用戶：AAPL 現在多少

→ memory_search "AAPL"
→ 找到買入紀錄
→ 回報持倉成本 + 可選：查詢現價
```

## 健康追蹤邏輯

```
用戶：我的健康狀況

→ garmin_summary
→ memory_search "health"
→ 整合 Garmin 數據 + 歷史記憶

如果發現異常：
→ memory_save 記錄觀察
→ 建議行動
```

## Watchlist 邏輯

Watchlist 是「需要持續追蹤」的事項：

```
用戶：幫我追蹤 X

→ memory_save:
  content: "追蹤：X - [原因/目標]"
  category: "watchlist"
  importance: 4

Morning workflow 會自動搜尋 watchlist 類別
提醒用戶目前追蹤中的項目
```

## 任務優先級

- **P0**: 今天必做
- **P1**: 本週完成
- **P2**: 有空再做
- **P3**: 靈感/想法

## 主動行為

### 記憶保存時機

- 用戶說「記住 X」
- 買入/賣出股票
- 健康相關決定
- 重要里程碑
- 反覆出現的話題

### 主動提醒

- P0 任務超時未完成
- 連續幾天睡眠不佳
- 追蹤項目有更新
- 投資觀察點到達

## 與其他 Skill 整合

- **Memory**: 核心依賴，所有追蹤都存記憶
- **Scheduling**: 設定提醒和排程
- **Google**: Calendar + Tasks 作為 source of truth
- **Garmin**: 健康數據來源
