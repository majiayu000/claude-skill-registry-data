---
name: amazon-review-scraper
description: 批量采集亚马逊商品评论，输出结构化数据
title: 亚马逊评论采集
example: 抓取指定亚马逊商品的最新50条评论，并把带图片的评论和差评单独提取出来。
version: 1.0.1
---
# Amazon亚马逊商品评论采集 Skill

## 角色定位

你负责调用 `amazon-review-scraper` skill 的高层业务接口，帮助用户完成亚马逊商品评论数据采集相关自动化任务。
当用户目标明确属于亚马逊评论采集时，必须优先使用本 skill 提供的高层接口，而不是自行组合底层浏览器步骤。

---

## 调用方式

`run.py` 位于本 SKILL.md 的同级目录。执行前先确认本文件的实际读取路径，取其所在目录作为 `<skill_path>`。

本技能已升级为 BrowserWorker 插件操控架构：`run.py` 通过项目内置 `BrowserWorker` daemon 的 `/execute` 接口加载 `scripts/actions/run_scrape.py`。action 使用 `browser.goto`、`browser.evaluate`、`browser.wait_ms` 和 `browser.request_help` 完成页面交互，不再直接操作 Chrome DevTools Protocol，也不依赖用户机器安装 ChromeDriver、Playwright、Selenium、requests 或 BeautifulSoup。

action 打开评论页后使用 BrowserWorker 框架级 `detect_page_state(domain_hint=...)` 做通用页面状态检测，遇到登录、验证码、地区确认、风控拦截等状态时调用 `request_help(validate_after=True)`，用户继续后由框架二次校验。不要自动反复刷新评论页或尝试绕过验证码。

端口发现顺序：`BrowserWorker_PORT` / `MANAI_BROWSER_CONTROL_PORT` → 工作区 `storage/browser_daemon.lock` → 兼容旧锁文件 `~/.BrowserWorker/BrowserWorker.lock` → 默认 `12321`。daemon 未响应时会尝试从项目内 `BrowserWorker` 目录自动启动。

**推荐：`--key value` 扁平参数（无引号转义问题）**

```bash
python <skill_path>/run.py run_scrape --urls "https://www.amazon.com/product-reviews/B0xxx/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews" --commentNumber 20
```

**兼容：单个 JSON 字符串**

```bash
python <skill_path>/run.py run_scrape '{"urls":["https://www.amazon.com/product-reviews/B0xxx/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"],"commentNumber":20}'
```

- 成功：stdout 输出 JSON 结果
- 失败：stderr 输出错误信息，退出码非 0

**前提**：ManAI 已启动，或项目内 `BrowserWorker` 可被 `run.py` 自动启动。

---

## 适用场景

适合以下任务：

- 批量采集指定亚马逊商品的用户评论数据
- 竞品评论分析——提取评分、评论内容、评论类型等结构化信息
- 获取评论中的图片和视频 URL 用于素材收集
- 跨多个 ASIN 的评论数据聚合

---

## 方法速查表

| 用户需求           | method       | 必填参数示例                                                                         |
| ------------------ | ------------ | ------------------------------------------------------------------------------------ |
| 采集亚马逊商品评论 | `run_scrape` | `--urls "https://www.amazon.com/product-reviews/B0xxx/...&reviewerType=all_reviews"` |

---

## 核心接口

### 评论采集

| method       | 关键参数                                                       | 说明                     |
| ------------ | -------------------------------------------------------------- | ------------------------ |
| `run_scrape` | `urls`, `commentNumber?`, `downloadPicture?`, `downloadVideo?` | 批量采集 Amazon 商品评论 |

---

## 参数约定

### `urls`

Amazon 评论页面链接或商品详情页链接。推荐提供评论页面链接并包含 `reviewerType=all_reviews`，如果用户只提供商品详情页，技能会从 URL 提取 ASIN 并自动转换为评论页。

链接格式示例：

```
https://www.amazon.com/product-reviews/B0XXXXXXXX/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews
```

多个链接可通过重复 `--urls` 传入：

```bash
python <skill_path>/run.py run_scrape --urls "链接1" --urls "链接2"
```

### `commentNumber`

| 值           | 含义                     |
| ------------ | ------------------------ |
| `10`（默认） | 每商品最多采集 10 条评论 |
| `1~999`      | 自定义每商品最大采集数量 |

### `downloadPicture`

| 值              | 含义                                |
| --------------- | ----------------------------------- |
| `false`（默认） | 不采集评论图片 URL                  |
| `true`          | 在结果中包含每条评论的图片 URL 列表 |

### `downloadVideo`

| 值              | 含义                                |
| --------------- | ----------------------------------- |
| `false`（默认） | 不采集评论视频 URL                  |
| `true`          | 在结果中包含每条评论的视频 URL 列表 |

---

## 参数校验规则（调用守门）

**⚠️ 强制约束：LLM 在执行任何 method 之前，必须先按下表校验参数，全部通过才允许执行脚本命令。任何一项不通过，禁止执行，直接向用户反馈缺失或不合法的参数。**

### `run_scrape` 参数校验

| 参数              | 必填 | 类型       | 校验规则                                                           | 不满足时的反馈话术                                                                             |
| ----------------- | ---- | ---------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| `urls`            | ✅   | `string[]` | 至少包含 1 项；每项须为合法 Amazon URL，并能从 URL 中识别 ASIN | "缺少必填参数 `urls`，请提供至少一个 Amazon 商品详情页或评论页链接。" |
| `commentNumber`   | ❌   | `number`   | 若提供，须为 1~999 的整数；默认 10                                 | "参数 `commentNumber` 须为 1~999 之间的整数。"                                                 |
| `downloadPicture` | ❌   | `boolean`  | 若提供，须为 `true` 或 `false`；默认 `false`                       | "参数 `downloadPicture` 须为 `true` 或 `false`。"                                              |
| `downloadVideo`   | ❌   | `boolean`  | 若提供，须为 `true` 或 `false`；默认 `false`                       | "参数 `downloadVideo` 须为 `true` 或 `false`。"                                                |

### 校验流程

```
用户发出调用意图
  → LLM 识别目标 method
  → LLM 逐项检查「参数校验规则」表
  → 全部通过？
      ├─ 是 → 组装命令并执行
      └─ 否 → 列出所有不满足的参数及反馈话术，返回给用户，不执行命令
```

### 校验示例

**通过 → 执行：**

```
用户：帮我采集这个商品的评论 https://www.amazon.com/product-reviews/B0xxx/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews
LLM 校验：
  ✅ urls = ["https://www.amazon.com/product-reviews/B0xxx/...&reviewerType=all_reviews"]（非空，合法 Amazon URL，可识别 ASIN）
  ✅ commentNumber 使用默认值 10
→ 执行命令
```

**不通过 → 反馈：**

```
用户：帮我采集亚马逊商品评论
LLM 校验：
  ❌ urls = []（必填参数缺失）
→ 反馈："缺少必填参数 `urls`，请提供至少一个包含 `&reviewerType=all_reviews` 的 Amazon 评论页面链接。"
```

---

## 使用示例

### 采集单个商品评论（默认 10 条）

```bash
python <skill_path>/run.py run_scrape --urls "https://www.amazon.com/product-reviews/B0XXXXXXXX/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
```

### 采集多个商品评论，每个最多 50 条，包含图片

```bash
python <skill_path>/run.py run_scrape --urls "https://www.amazon.com/product-reviews/B0xxx/...&reviewerType=all_reviews" --urls "https://www.amazon.com/product-reviews/B0yyy/...&reviewerType=all_reviews" --commentNumber 50 --downloadPicture true
```

### 使用 JSON 参数

```bash
python <skill_path>/run.py run_scrape '{"urls":["https://www.amazon.com/product-reviews/B0xxx/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"],"commentNumber":30,"downloadPicture":true,"downloadVideo":true}'
```

---

## 执行策略

当用户提出亚马逊评论采集相关任务时，应按以下顺序处理：

1. **参数收集**：从用户消息中提取评论链接、采集数量等参数
2. **参数校验**：按「参数校验规则」逐项检查，特别确认链接包含 `&reviewerType=all_reviews`，不满足则反馈用户并停止
3. **链接修正**：如果用户给的是商品详情页链接而非评论页链接，帮助转换为评论页格式
4. **执行采集**：调用 `run_scrape` 方法
5. **结果整理**：将返回的 JSON 结果整理为用户易读的格式（如表格），高亮统计信息
6. 如果接口执行失败，必须返回真实错误并说明下一步排查方向

---

## 常见失败场景

### 链接格式错误

表现：

- 报错无法识别 ASIN 或未返回评论

处理：

- 提醒用户提供合法 Amazon 商品详情页或评论页链接
- 优先帮助用户从商品详情页 URL 转换为评论页 URL

### Amazon 反爬限制

表现：

- 返回空评论或评论数量远低于预期
- 页面加载超时

处理：

- 建议减少单次采集数量
- action 已内置页面等待和低频翻页，必要时降低 `commentNumber`
- 根据 `request_help` 提示，在插件浏览器中完成验证码或登录后继续
- 不要自动反复请求同一评论页，避免触发更强风控
