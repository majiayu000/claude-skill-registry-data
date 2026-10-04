---
name: amazon-rank-scraper
description: 输入关键词，获取亚马逊自然位与广告位排名数据
title: 亚马逊排名查询
example: 查询“wireless earbuds”在亚马逊美国站（邮编10001）前3页的排名情况。
version: 1.0.1
---
# 亚马逊商品排名获取 Skill

## 角色定位

你负责调用 `amazon-rank-scraper` skill 的高层业务接口，帮助用户完成亚马逊商品排名数据抓取任务。
当用户目标明确属于亚马逊关键词排名查询时，必须优先使用本 skill 提供的高层接口，
而不是自行组合底层步骤。

---

## 调用方式

`run.py` 位于本 SKILL.md 的同级目录。执行前先确认本文件的实际读取路径，取其所在目录作为 `<skill_path>`。

本技能已升级为 BrowserWorker 插件操控架构：`run.py` 通过项目内置 `BrowserWorker` daemon 的 `/execute` 接口加载 `scripts/actions` 中的 action。实现不依赖用户机器预装 Chrome、ChromeDriver、Playwright、Selenium、requests、BeautifulSoup 或 pandas，适合 macOS 和 Windows 安装环境。

action 打开页面后使用 BrowserWorker 框架级 `detect_page_state(domain_hint=...)` 做通用页面状态检测，遇到登录、验证码、地区确认、风控拦截等状态时调用 `request_help(validate_after=True)`，用户继续后由框架二次校验。不要在 skill 中恢复站点专用的验证码绕过或重复刷新逻辑。

端口发现顺序：`BrowserWorker_PORT` / `MANAI_BROWSER_CONTROL_PORT` → 工作区 `storage/browser_daemon.lock` → 兼容旧锁文件 `~/.BrowserWorker/BrowserWorker.lock` → 默认 `12321`。daemon 未响应时会尝试从项目内 `BrowserWorker` 目录自动启动。

**推荐：`--key value` 扁平参数（无引号转义问题）**

```bash
python <skill_path>/run.py <method> --param1 value1 --param2 value2
```

**兼容：单个 JSON 字符串**

```bash
python <skill_path>/run.py <method> '{"param1":"value1","param2":"value2"}'
```

- 成功：stdout 输出 JSON 结果，退出码 0
- 失败：stderr 输出错误信息，退出码非 0

---

## 适用场景

适合以下任务：

- 查询某关键词在亚马逊搜索结果页的商品自然排名和广告排名
- 批量查询多个关键词的排名数据
- 获取指定 ASIN 在某关键词下的排名位置
- 抓取亚马逊搜索结果页商品列表（标题、价格、ASIN）
- 监控竞品在特定关键词下的排名变化

---

## 方法速查表

| 用户需求 | method | 必填参数示例 |
|----------|--------|-------------|
| 查单个关键词排名 | `scrape_keyword` | `--keyword "wireless earbuds"` |
| 批量查多个关键词排名 | `scrape_keywords_batch` | `--keywords "kw1" --keywords "kw2"` |
| 解析商品HTML片段 | `parse_product_html` | `--html "<div...>" --index 0 --keyword "kw"` |

---

## 核心接口

### 排名抓取

| method | 关键参数 | 说明 |
|--------|----------|------|
| `scrape_keyword` | `keyword`（必填）, `amazonUrl?`, `pageCount?`, `zipCode?` | 抓取单个关键词的排名数据 |
| `scrape_keywords_batch` | `keywords`（必填数组）, `amazonUrl?`, `pageCount?`, `zipCode?` | 批量抓取多个关键词 |
| `parse_product_html` | `html`（必填）, `index`（必填）, `natureRank?`, `keyword?`, `page?`, `currentDate?` | 解析单个商品HTML片段（无需浏览器） |

---

## 参数约定

### `amazonUrl`

| 值 | 含义 |
|----|------|
| `"https://www.amazon.com/"` | 美国站（默认） |
| `"https://www.amazon.co.jp/"` | 日本站 |
| `"https://www.amazon.co.uk/"` | 英国站 |
| `"https://www.amazon.de/"` | 德国站 |

### `pageCount`

数字字符串，表示每个关键词抓取的搜索结果页数。默认 `3`，建议不超过 `10`。

### `zipCode`

美国邮政编码，用于设置配送地址（影响价格和库存显示）。默认 `90001`（洛杉矶）。

### 浏览器会话

BrowserWorker daemon 统一管理插件浏览器会话和域名级并发锁。旧版 `incognito` 参数不再作为控制项使用；如果外部调用仍传入该参数，技能会忽略它并复用 BrowserWorker 管理的会话。

---

## 参数校验规则（调用守门）

**⚠️ 强制约束：LLM 在执行任何 method 之前，必须先按下表校验参数，全部通过才允许执行脚本命令。任何一项不通过，禁止执行，直接向用户反馈缺失或不合法的参数。**

### `scrape_keyword` 参数校验

| 参数 | 必填 | 类型 | 校验规则 | 不满足时的反馈话术 |
|------|------|------|----------|-------------------|
| `keyword` | ✅ | `string` | 非空字符串 | "缺少必填参数 `keyword`，请提供要搜索的关键词。" |
| `amazonUrl` | ❌ | `string` | 若提供，必须以 `https://www.amazon.` 开头 | "参数 `amazonUrl` 格式不合法，请提供合法的亚马逊站点URL，如 `https://www.amazon.com/`。" |
| `pageCount` | ❌ | `number` | 若提供，必须为 1-20 之间的整数 | "参数 `pageCount` 须为 1-20 之间的整数，表示抓取页数。" |
| `zipCode` | ❌ | `string` | 若提供，须为 5 位数字 | "参数 `zipCode` 须为 5 位数字邮编，如 `90001`。" |

### `scrape_keywords_batch` 参数校验

| 参数 | 必填 | 类型 | 校验规则 | 不满足时的反馈话术 |
|------|------|------|----------|-------------------|
| `keywords` | ✅ | `string[]` | 至少包含 1 项；每项非空字符串 | "缺少必填参数 `keywords`，请至少提供一个关键词（可重复使用 `--keywords`）。" |
| `amazonUrl` | ❌ | `string` | 若提供，必须以 `https://www.amazon.` 开头 | "参数 `amazonUrl` 格式不合法，请提供合法的亚马逊站点URL。" |
| `pageCount` | ❌ | `number` | 若提供，须为 1-20 之间的整数 | "参数 `pageCount` 须为 1-20 之间的整数。" |
| `zipCode` | ❌ | `string` | 若提供，须为 5 位数字 | "参数 `zipCode` 须为 5 位数字邮编，如 `90001`。" |

### `parse_product_html` 参数校验

| 参数 | 必填 | 类型 | 校验规则 | 不满足时的反馈话术 |
|------|------|------|----------|-------------------|
| `html` | ✅ | `string` | 非空字符串，应为 HTML 片段 | "缺少必填参数 `html`，请提供商品 HTML 片段。" |
| `index` | ✅ | `number` | 非负整数 | "缺少必填参数 `index`，请提供商品在当前页中的 0-based 位置索引。" |

### 校验流程

```
用户发出调用意图
  → LLM 识别目标 method
  → LLM 逐项检查「参数校验规则」表
  → 全部通过？
      ├─ 是 → 组装命令并执行
      └─ 否 → 列出所有不满足的参数及反馈话术，返回给用户，不执行命令
```

---

## 使用示例

### 抓取单个关键词排名（美国站，3页）

```bash
python <skill_path>/run.py scrape_keyword --keyword "wireless earbuds" --pageCount 3 --zipCode 10001
```

### 抓取单个关键词排名（日本站）

```bash
python <skill_path>/run.py scrape_keyword --keyword "ワイヤレスイヤホン" --amazonUrl "https://www.amazon.co.jp/" --pageCount 2
```

### 批量抓取多个关键词

```bash
python <skill_path>/run.py scrape_keywords_batch \
  --keywords "bluetooth speaker" \
  --keywords "wireless mouse" \
  --keywords "usb hub" \
  --pageCount 3 \
  --zipCode 90001
```

### JSON 格式调用

```bash
python <skill_path>/run.py scrape_keywords_batch '{"keywords":["bluetooth speaker","wireless mouse"],"pageCount":2,"zipCode":"90001"}'
```

### 解析 HTML 片段（离线解析，无需浏览器）

```bash
python <skill_path>/run.py parse_product_html --html "<div data-asin='B0XXXXXX'...>" --index 0 --keyword "wireless earbuds" --page 1
```

---

## 返回数据结构

### `scrape_keyword` / `scrape_keywords_batch` 返回字段

```json
{
  "keyword": "wireless earbuds",
  "pagesFetched": 3,
  "totalProducts": 48,
  "products": [
    {
      "Date": "2026/04/14",
      "Asin": "B0XXXXXXXXX",
      "Title": "Product Title",
      "Price": "$29.99",
      "Keyword": "wireless earbuds",
      "PageRank": "1—3",
      "Page": 1,
      "NatureRank": 2,
      "AdIndex": "",
      "Sponsored": "False",
      "SponsoreId": "",
      "Feautrued_brand": "False",
      "Recommended_by_Amazon": "False",
      "AdId": "",
      "CampaignId": ""
    }
  ]
}
```

| 字段 | 说明 |
|------|------|
| `Asin` | 商品 ASIN 编码 |
| `PageRank` | 页数—位置，如 `1—3` 表示第1页第3位 |
| `NatureRank` | 自然排名（广告商品为空） |
| `AdIndex` | 广告排名位置 |
| `Sponsored` | 是否广告商品（`"True"` / `"False"`） |
| `Feautrued_brand` | 是否品牌精选（`"True"` / `"False"`） |
| `Recommended_by_Amazon` | 是否亚马逊推荐（`"True"` / `"False"`） |

---

## 执行策略

当用户提出亚马逊排名相关任务时，按以下顺序处理：

1. **参数收集**：从用户消息中提取 method 和参数（关键词、站点、页数等）
2. **参数校验**：按「参数校验规则」逐项检查，不满足则反馈用户并停止
3. **调用执行**：组装命令并执行，等待结果（抓取耗时较长，默认超时 300s）
4. **结果呈现**：将排名数据整理后展示给用户，重点突出自然位和广告位信息
5. **失败处理**：若接口执行失败，返回真实错误并说明下一步排查方向

---

## 常见失败场景

### BrowserWorker daemon 服务未启动

表现：
- 错误信息包含 `无法连接到浏览器守护进程` 或 `Connection refused`

处理：
- 确认 ManAI 主程序或 BrowserWorker daemon 已启动
- 检查端口是否正确（默认 `12321`），可通过 `storage/browser_daemon.lock`、`BrowserWorker_PORT` 或 `MANAI_BROWSER_CONTROL_PORT` 覆盖

### 插件浏览器未连接

表现：
- 错误信息包含插件浏览器连接失败、页面无法创建或超时

处理：
- 确认 BrowserWorker 插件环境正常
- 由 ManAI 主程序重新启动 BrowserWorker 后重试，不要求用户手动安装浏览器驱动

### 亚马逊验证码阻断

表现：
- 抓取结果 `totalProducts` 为 0 或极少
- products 列表中 Asin 均为空

处理：
- 根据 `request_help` 提示，在插件浏览器中完成验证码或登录后继续
- 不要自动反复刷新或重复执行同一关键词，避免触发更强风控
- 考虑使用 `--zipCode` 切换配送地址或降低抓取频率

### 关键词无搜索结果

表现：
- `totalProducts` 为 0，无错误

处理：
- 检查关键词拼写或更换关键词
- 检查 `amazonUrl` 是否与关键词语言匹配（如日文关键词用日本站）
