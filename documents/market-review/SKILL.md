---
name: market-review
description: 生成市场指数复盘报告。自动执行iChoice+AKShare数据获取、Excel生成、JSON转换、前端展示和截图保存的完整流程。当用户要求"生成市场复盘"、"市场回顾"、"生成截止某日期的市场复盘"、"市场数据更新"时使用此技能。
---

# 市场指数复盘

自动化生成多资产市场复盘仪表板，包括权益、债券、汇率、商品四大类资产的行情数据和分位数分析。

## 前置条件

1. **iChoice 账号** - xylczh0181 / ef465509（已内置于脚本，无需手动配置）
2. **Python环境就绪** - 需要 `pandas, numpy, openpyxl, EmQuantAPI, akshare`
   - AKShare 版本需 ≥1.18.50：`pip3 install --upgrade akshare`
3. **前端依赖已安装** - dashboard 目录需要已运行过 `npm install` 或 `pnpm install`

**数据源说明**:
- 主数据源：iChoice (EMQuantAPI) — 股指、债指、汇率、商品10个资产、EDB宏观指标
- 补充数据源：AKShare（免费）
  - `fx_swap_quote()` — USD/CNY 1Y掉期点实时报价（用于锚定锁汇成本）
  - `bond_zh_us_rate()` — 中美国债收益率日频（锁汇成本历史走势代理序列）
  - `bond_cb_index_jsl()` — 集思录转债市场指标（转股溢价率、价格中位数，1年历史）

## 执行流程

### 步骤 1: 解析用户请求的日期

从用户输入中提取截止日期。如果未指定，使用当天日期。

日期格式: `YYYY-MM-DD`

**日期范围说明**: 近一月走势包含完整31天。例如截止日期为2026-01-24，则起始日期为2025-12-24。

### 步骤 2: 生成 iChoice + AKShare 数据

```bash
cd /Users/fanshengxia/Desktop/市场观点美化/data
python generate_tables_from_ichoice.py --date YYYY-MM-DD
```

**注意**: iChoice 登录需要约 30-60 秒初始化时间，设置 timeout=300000。

生成文件:
- `指标值.xlsx` - 36个指标的当前值、历史统计和分位数
  - 权益9个（含转债：转股溢价率、纯债溢价率占位、价格中位数）
  - 债券9个、汇率6个（含锁汇成本、掉期点1Y代理）、商品12个
- `近1月净值走势.xlsx` - 完整31天的日度行情数据（含锁汇成本走势）

### 步骤 3: 转换 Excel 为 JSON

```bash
cd /Users/fanshengxia/Desktop/市场观点美化/data
python excel_to_json_converter.py
```

输出文件:
- `data/asset_data.json` - 数据备份
- `asset-analysis-real-data/asset-analysis-dashboard/src/assets/asset_data.json` - 前端数据

### 步骤 4: 启动前端服务

**重要**: 使用 `./node_modules/.bin/vite` 而不是 `pnpm dev`，避免环境变量问题。

```bash
cd /Users/fanshengxia/Desktop/市场观点美化/asset-analysis-real-data/asset-analysis-dashboard
./node_modules/.bin/vite --port 5173 --host 0.0.0.0
```

后台运行时使用 `run_in_background: true` 参数。

**注意**: 必须加 `--host 0.0.0.0`，否则 vite 只监听 IPv6，puppeteer 用 IPv4 连接会超时。

前端服务启动后访问: `http://$(ipconfig getifaddr en0):5173`（IP 动态获取，勿硬编码）

### 步骤 5: 截图保存

等待前端完全加载后（约15秒），使用 puppeteer 进行截图：

```bash
cd /tmp && npm install puppeteer --no-save 2>/dev/null
```

```javascript
// /tmp/screenshot_market.js
const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });
    try {
        await page.goto('http://LOCAL_IP:5173/', { waitUntil: 'domcontentloaded', timeout: 60000 });
    // LOCAL_IP 通过 `ipconfig getifaddr en0` 动态获取，每次执行前替换
    } catch(e) { console.log('goto:', e.message); }
    await new Promise(resolve => setTimeout(resolve, 15000));
    await page.screenshot({
        path: '/Users/fanshengxia/Desktop/市场观点美化/市场复盘_YYYY-MM-DD.png',
        fullPage: true
    });
    await browser.close();
    console.log('Screenshot saved!');
})();
```

**关键配置**:
- URL 使用 `ipconfig getifaddr en0` 动态获取的 IPv4 局域网地址，**不要硬编码**，不用 `127.0.0.1` 或 `localhost`
- `waitUntil: 'domcontentloaded'`（不用 `load`，防止超时后空白页）
- 等待 **15秒**（不是5秒），确保 SVG 图表和分位数条全部渲染完成

截图保存路径: `/Users/fanshengxia/Desktop/市场观点美化/市场复盘_YYYY-MM-DD.png`

### 步骤 6: 关闭前端服务

使用 `TaskStop` 工具停止后台运行的前端服务。

## 项目路径

| 路径 | 说明 |
|------|------|
| `/Users/fanshengxia/Desktop/市场观点美化` | 项目根目录 |
| `data/` | 数据脚本和生成的文件 |
| `data/generate_tables_from_ichoice.py` | iChoice+AKShare 数据生成脚本（当前使用） |
| `data/excel_to_json_converter.py` | Excel 转 JSON 脚本 |
| `asset-analysis-real-data/asset-analysis-dashboard/` | React 前端项目 |

## 示例用法

用户: "生成截止2026年1月24日的市场复盘"

响应流程:
1. 提取日期: 2026-01-24
2. 运行数据生成: `python generate_tables_from_ichoice.py --date 2026-01-24`
   - 数据范围: 2025-12-24 至 2026-01-24（完整31天）
   - timeout=300000（iChoice 登录初始化需要约60秒）
3. 运行 JSON 转换: `python excel_to_json_converter.py`
4. 启动前端: `./node_modules/.bin/vite --port 5173 --host 0.0.0.0`（后台运行）
5. 等待15秒后使用 puppeteer 截图，URL: `http://$(ipconfig getifaddr en0):5173/`（动态IP）
6. 截图保存为: `市场复盘_2026-01-24.png`
7. 停止前端服务

## 错误处理

| 错误 | 解决方案 |
|------|----------|
| iChoice 登录失败 | 检查网络连接，账号 xylczh0181 / ef465509 |
| EDB代码错误 | 检查 iChoice 代码是否有效 |
| AKShare 导入错误 | `pip3 install --upgrade akshare`（需要 ≥1.18.50）|
| pnpm 未找到 | 使用 `./node_modules/.bin/vite` 替代 |
| 前端启动失败 | 运行 `npm install` 安装依赖 |
| puppeteer 未安装 | 运行 `cd /tmp && npm install puppeteer --no-save` |
| 截图空白/超时 | IP 可能变了，先 `ipconfig getifaddr en0` 确认当前 IP，再更新截图脚本中的 URL |
| timeout | 增大 Bash timeout 至 300000ms |

## 辅助脚本

提供一键执行脚本（含截图）:

```bash
/Users/fanshengxia/.claude/skills/market-review/scripts/run_market_review.sh 2026-01-24
```
