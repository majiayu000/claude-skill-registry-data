---
name: amazon-1688-selection
description: 从Amazon Best Sellers/Movers & Shakers榜单自动采集数据，智能筛选评论少、利润高的蓝海品类，再匹配1688工厂货源，并输出含风险提示的全链路利润测算报告，实现“选品—找厂—算利润”一站式闭环。
title: 亚马逊1688选品
example: '`从Amazon的“Home & Kitchen”大类选品，帮我筛选蓝海机会，然后找1688货源，最后测算全链路利润。`'
version: 1.0.1
---
# Amazon-1688 全链路选品工作流

从Amazon拆品类→筛蓝海→子类目深挖→1688比价→利润测算，五步闭环。

## 调用方式

`run.py` 位于本 SKILL.md 的同级目录。执行前先确认本文件的实际读取路径，取其所在目录作为 `<skill_path>`。

```bash
python <skill_path>/run.py <method> --param1 value1 --param2 value2
```

## 方法与核心接口

| 需求步骤 | method | 必填参数示例 | 说明 |
|------|------|------|------|
| **Step 1：趋势发现** | `step1_collect` | `--categoryUrl "https://www.amazon.com/gp/bestsellers/home-garden/"` | 采集指定大类的 Best Sellers 及 reviews 差评 |
| **Step 3：品类分析** | `step3_analyze` | `--subCategoryUrl "https://www.amazon.com/gp/bestsellers/kitchen/289668"` | 对子类目Top100数据深度分析（品牌集中度与评论中位数） |
| **Step 5：利润测算** | `step5_calculate` | `--purchasePrice 15.0 --sellingPrice 29.9 --weight 0.5` | 测算全链路物流与平台费用，并输出测算结果 |

---

## 使用前必读

- **BrowserWorker 插件架构**：执行 Step 1/Step 3 时，`run.py` 会通过项目内 BrowserWorker daemon + Chrome extension plugin transport 控制浏览器；daemon 未启动时会尝试按当前工作区启动。禁止使用旧 CDP attach 或直接接管用户日常 Chrome。
- **无新增环境依赖**：本技能的浏览器采集使用 Python 标准库 HTTP 客户端和 BrowserWorker 插件 API，不要求 Playwright、Selenium、ChromeDriver 或 beautifulsoup4。
- **页面状态检测**：Step 1/Step 3 打开 Amazon 页面后会调用 BrowserWorker `detect_page_state(domain_hint="amazon.com")`；如遇登录、验证码、地区选择或风控页，会通过 `request_help(validate_after=True)` 请求用户在已打开 Chrome 页面处理，并在继续前二次校验。
- **人工等待超时**：Step 1/Step 3 可传 `--helpTimeoutMs 300000` 调整人工处理等待时间；`run.py` 会同步放大 `/execute` 外层 timeout，避免浏览器还在等用户时 CLI 提前断开。
- **释放锁不关页**：BrowserWorker `/lock/release` 只释放并发锁，默认不关闭页面；需要关闭页面时显式调用 `/session/close` 或 release 时传 `close_browser: true`。
- **子类名不可猜**：从大类主页左侧类目树提取真实的亚马逊子类目节点 URL（不要胡乱编造类目的 Node ID）。
- **价格统一**：Amazon 使用美金（$），国内供应链 1688 使用人民币（¥）。
- **利润范围**：利润测算时请给出一个区间，注明合理假设的前提（如浮动范围 ±15%）。

---

## 报告收尾规范

每份输出必须包含：
1. **风险清单**（至少 2-3 条，如版权、物流超重、退货率高）
2. **合规追问**（"需要我继续排查合规风险吗？"）
3. **数据完整性声明**（标注一手采集/第三方推断/未采集项）

## 工具依赖

| 工具 | 用途 |
|------|------|
| `1688-product-find` skill | 1688 文本/图片搜商品、比价 |
| `1688-source-suppliers` skill | 1688 供应商信息查询 |
| BrowserWorker `/execute` + `action_search_path` | 通过插件浏览器读取 Amazon 榜单和评论页 DOM |
