---
name: manai_scraping
description: 针对1688、淘宝/天猫、京东等电商平台，自动完成商品页面的高保真物料爬取（标题、属性、SKU、主图、详情图等），并自主编写新平台的抓取插件，输出标准化商品数据
  Excel 与图片目录，助力快速上架。
title: ManAI物料采集
example: 抓取京东商品详情页 https://item.jd.com/1000123456.html，提取全部主图、详情图并整理成包含价格和规格的 Excel
  表格。
version: 1.0.3
---
# E-commerce Product Material Scraping & R&D SKILL

本 SKILL 指引 Agent 扮演**高级电商自动化专家**，针对各种电商平台进行商品页面的高保真物料爬取与采集（包括商品标题、属性、SKU参数、商品主图、详情图、颜色款式图等）。

在面对没有现成抓取脚本的电商平台时，指引 Agent 利用项目内置 BrowserWorker 插件浏览器自动分析网页结构，并自主编写、调试、集成全新的抓取 Action 脚本。

---

## 1. 守护进程与工具链说明 (Daemon & Tool Integration)

本平台使用项目内置 `BrowserWorker` 插件 daemon 操控浏览器。端口发现顺序为 `BrowserWorker_PORT` / `BrowserWorker_LOCK_FILE` / `MANAI_WORKSPACE_ROOT` 或 `MANAI_HOME` 下的 `storage/browser_daemon.lock` / 默认 `12321`。安装到 macOS 或 Windows 用户机器后，不要求用户额外安装 ChromeDriver、Playwright、Selenium 或独立 CDP 调试环境。

### 1.1 浏览器控制机制
1. **自动生命周期管理**：守护进程由 GUI 自动拉起和销毁，Agent **无需手动拉起** 任何后台进程，也无需手动读写本地锁文件或发送 HTTP 网络请求。
2. **免维护调用**：所有网页控制与数据抓取操作，均应通过 BrowserWorker `/execute` 加载 `scripts/actions` 中的 Action，或通过平台内置浏览器控制工具间接调用。
3. **工具参数格式**：
   ```json
   {
     "action": "action_name",
     "action_search_path": "<skill_path>/scripts/actions",
     "args": {
       "url": "..."
     }
   }
   ```

---

## 2. 核心物料采集流程

### 第一阶段：安全前置提示与收集待抓取 URL
1. **前置提示（必须首先告知用户）**：在开始任何采集或分析任务前，Agent **必须主动向用户提示以下三点注意事项**，确认用户知晓后再进行后续操作：
   * **插件浏览器接管**：本工具会通过 BrowserWorker 插件浏览器访问目标平台，不要求用户安装或打开日常 Chrome。
   * **登录要求**：如平台要求登录或验证码，Action 会调用 `request_help`，用户在插件浏览器中完成后继续。
   * **安全频次**：单日抓取量建议不要过大（例如控制在 200 条以内），以防平台检测并封禁账号或 IP。
2. 向用户确认待抓取的商品详情页 URL 列表。
3. **若用户仅提供"平台"和"搜索关键词"**：引导 Agent 使用 BrowserWorker 插件浏览器执行关键词搜索，并将搜索结果页中提取出的前 N 个商品详情链接作为最终要抓取的 URL 列表呈现给用户确认。

### 第二阶段：检查并复用现有插件
1. **优先使用现有抓取插件**：
   在爬取以下平台时，**必须优先使用已有的 BrowserWorker Action，严禁重新研发**：
   * **1688**：使用动作 `scrape_1688` (对应文件为 `scripts/actions/scrape_1688.py`)，支持 `https://detail.1688.com/offer/<offerId>.html` 与带 `offerId=<offerId>` 的移动端链接。
    * **淘宝 (Taobao)**：使用动作 `scrape_taobao` (对应文件为 `scripts/actions/scrape_taobao.py`)
    * **天猫 (Tmall)**：使用动作 `scrape_tmall` (对应文件为 `scripts/actions/scrape_tmall.py`)，针对 `detail.tmall.com` 提取完整 PC 详情页 SPU 物料。
   * **京东 (JD)**：使用动作 `scrape_jd` (对应文件为 `scripts/actions/scrape_jd.py`)，面向 `item.jd.com` 商品详情页，提取清洗后的标题、价格/原价、SKU 与完整参数，下载 `商品主图`、`商品详情页图`、`颜色规格图`，生成两级表头 `商品数据-<ItemId>.xlsx` 与 `商品整理.log`。不要把旧版 JSON-only 结果当作完整物料交付。
   
   例如，调用 BrowserWorker `/execute`：
   ```json
   {
     "action": "scrape_jd",
     "action_search_path": "<skill_path>/scripts/actions",
     "args": {
       "url": "https://item.jd.com/1000123456.html"
     }
   }
   ```
2. 解析返回的 JSON 结果，向用户展示抓取到的商品标题、SKU 数量与保存路径。

### 第三阶段：进入新脚本研发 (R&D) 流程
若无匹配脚本，必须严格按照以下五个步骤自主研发新插件：

#### 步骤 1：启动采样与源码提取
为了分析网页结构，Agent 应优先读取当前页面匹配的 `page_semantics`，按 `semantic_key` 理解页面上的稳定业务元素（如 `search.primary_input`、`search.submit`、`result_card.primary_link`）。缺少语义记录或置信度不足时，再通过 BrowserWorker 插件浏览器执行页面导航、滚动、DOM 快照及页面内 JS 提取。真实截图能力在当前 BrowserWorker 规范中禁用时，不要强依赖截图；优先使用 `snapshot` / `evaluate` / `document.body.innerText` 来验证当前页面事实并补充语义证据。

**`flexible_access` 采样与源码提取工具调用示例：**
```json
{
  "action": "flexible_access",
  "action_search_path": "<BrowserWorker>/browser_service/actions",
  "args": {
    "steps": [
      {"op": "goto", "args": ["<target_url>"]},
      {"op": "wait_for_timeout", "args": [5000]},
      {"op": "evaluate", "args": ["window.scrollBy(0, 800)"]},
      {"op": "wait_for_timeout", "args": [1500]},
      {"op": "content"}
    ],
    "keep_open": true
  }
}
```
*执行完毕后，将返回的 `content` 源码写入临时文件夹中的 `page_source.html`（临时目录路径优先使用 `temp/` 下按日期建的子目录），并在命令行向用户展示"HTML 已保存"，然后立即自主进入步骤 2。当前 BrowserWorker 禁用真实浏览器截图，验证页面状态时使用 `snapshot`、`title`、`url`、`content` 或 `evaluate`。snapshot 返回的 `ref` / `handle` 只能用于当前页面的一次性闭环验证，不得写入可复用脚本；需要长期复用时写入或更新 `page_semantics` 中的 `semantic_key` 与定位证据。*

#### 步骤 2：分析结构
1. **元素搜索**：读取并检索保存的临时 HTML 页面源码。
2. **提取定位**：
   * 搜索包含商品名、价格、商品属性、规格、轮播主图等数据的 DOM Class、ID 或包含配置信息的 JSON 数据块（例如 script 标签里的 `window.__INITIAL_STATE__` 或 `window.pageData` 等全局变量）。
   * 提炼出能够使用页面内 JavaScript `browser.evaluate` 获取对应信息的规则或选择器。优先使用 `semantic_key`、稳定业务属性、文本匹配和 DOM 结构，不依赖动态 CSS 哈希类名；页面关键控件和重复数据卡片应沉淀为 `page_semantics` 证据，后续执行时先解析语义键再重验证当前 DOM。

#### 步骤 3：编写新抓取插件脚本
在 `scripts/actions/` 目录下新增文件 `scrape_<platform_name>.py`（全小写，下划线分隔，如 `scrape_pinduoduo.py`）。脚本必须严格遵循以下规范：

##### 插件规范一：元数据声明
脚本顶部必须声明 `metadata`，格式示例如下：
```python
metadata = {
    "name": "scrape_pinduoduo",
    "description": "输入拼多多商品 URL，提取商品标题、价格、SKU 并下载主图/详情图/属性表到指定的物料上架目录中。",
    "parameters": {
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "商品详情页的完整 URL"},
            "output_dir": {"type": "string", "description": "用户指定的物料输出目录路径"}
        },
        "required": ["url"]
    }
}
```

##### 插件规范二：核心处理接口
必须实现 `handler(browser, args)` 接口，其中 `browser` 是 BrowserWorker 插件浏览器对象，`args` 包含传入参数。不得使用 `cdp.send_cmd`、`Target.*`、`Page.*`、`Runtime.*` 或直接连接 Chrome DevTools Protocol。它必须包含以下流程：
1. **导航与加载**：使用 `browser.goto(url, timeout_ms=45000, tab_key="main")` 打开商品 URL，并用 `browser.wait_ms` 等待页面稳定。
2. **获取与解析**：通过 `browser.evaluate` 在页面上下文中执行 JS，提取商品名、店铺/商家名、参数表、SKU 数据（规格、价格、库存等）。**在解析商品属性时，必须尽可能完整地提取并保留所有页面能获取到的字段（如材质、品牌、各项规格参数等），不得遗漏。**
3. **输出物料文件**：
   * 在用户指定的本地输出目录下（格式为：`{平台名}商品{时间戳}`，若用户未指定输出目录，则默认为全局配置 `data_directory` 目录下的 `{平台名}商品{时间戳}/`），并在该父目录下新建三位序号递增 of SPU 目录（如 `001聚氨酯pu棒...`）。
   * 新建 SPU 目录下的子目录：`商品主图`、`商品详情页图`、`颜色规格图`（**颜色规格图目录同时用于存放颜色款式图与规格尺寸图**）。
   * **标准 Excel 导出**：使用 `openpyxl` 导出 `商品数据-<OfferID>.xlsx`。**表头必须是两级合并表头**，第一行是字段分组标题（"商品名称"、"商品规格"、"价格与库存"、"商品属性"等），第二行是具体字段名。
   * **分级过滤图片下载**：
     * 主图：过滤并保留大小 >= 50KB 的图片。
     * 详情图：过滤并保留大小 >= 50KB 的图片。
     * 款式颜色图：过滤并保留大小 >= 50KB 的图片。**所有款式颜色与规格图片需统一存放在 `颜色规格图` 目录下。图片下载与保存时，其命名必须按照在页面上出现的先后顺序带上三位数字编号前缀（从 `001` 开始一直往后编号，如 `001黄色.jpg`，`002大号黑色.jpg`），以便于人工 Review 与整理归档，严禁使用无意义的哈希或纯随机命名。**
     * **URL 黑名单过滤**：自动跳过包含 `banner`, `logo`, `cert`, `promise`, `service`, `shipping` 等非商品素材关键词的图片 URL。
4. **更新商品日志**：
   * 将当前 SPU 的名称、状态、SKU 数量、主图/详情图/颜色规格图数量，追加写入父目录下的 `商品整理.log`。

*直接参考同目录下已有的 `scrape_1688.py`、`scrape_taobao.py`、`scrape_jd.py` 的 BrowserWorker 插件写法进行编写。*

#### 步骤 4：运行测试与回显
1. **热加载运行**：
   守护进程在处理调用请求时会自动重新加载 `actions/` 目录下的最新脚本。
   Agent 通过 BrowserWorker `/execute`，传入 `action: "scrape_<platform>"` 与 `action_search_path` 运行该脚本。
2. **反馈确认**：
   展示运行结果的 JSON 报告（包含 SKU 数量、主图与详情图的下载张数、以及输出的物料目录路径），并向用户发出询问：
   > "已成功运行新编写的 `scrape_<platform>` 采集脚本进行测试。生成的物料目录为 `...`，包含 SPU 和 SKU 数据。请您检查或确认结果是否正确？"

#### 步骤 5：循环迭代与批量抓取
1. **反馈修正**：
   如果用户指出数据或图片有缺失或不正确，根据反馈重新阅读 `page_semantics`、页面 HTML、`snapshot` 或页面内 `evaluate` 结果，修改 `scripts/actions/scrape_<platform>.py` 的解析逻辑；若发现新的重要语义元素，更新对应 `semantic_key` 的证据，再调用工具重新测试，直到用户确认无误。
2. **批量运行**：
   用户确认无误后，Agent 对用户给出的剩余 URL 列表进行批量迭代抓取，记录所有爬取日志，并生成总的物料文件夹。

---

## 3. 商品图片与详情缺失的补图引导

在物料采集过程中，如果发现以下情况：
- 原电商页面缺少主图或详情图。
- 详情图分辨率过低，无法用于拼多多上架。
- 用户抓取后，提出"帮我重新做几张主图/场景图"等补图要求。

**必须立即引导用户切换至【商品图片生成 SKILL (manai_image_generation_skill.md)】**，使用 Manai 智能生图工具对采集回来的基础素材进行补充生成。

---

## 4. 安全与规范约束 (Constraints)

1. **绝对路径禁止**：生成的脚本和日志中不得包含任何形式硬编码的个人电脑绝对路径，必须使用相对路径或系统变量动态获取。
2. **错误处理与清理**：不要在 Action 内直接管理 Chrome Target。`/lock/release` 只释放并发锁，默认保留页面；需要关闭浏览器页面时，显式调用 `/session/close`、`/browser/close-session`、`/tabs/close`，或在 `/lock/release` 请求中传入 `close_browser: true`。
3. **临时文件清理**：在临时目录下生成的临时 DOM 源码、快照 JSON 等中间结果，一旦采集脚本研发成功并投入运行，必须在任务结束前将其删除，做到"用完即删"。
