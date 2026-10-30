---
name: mcd-saver
description: 麦麦省钱助手——基于麦当劳中国官方 MCP Server 的省钱点餐技能。当用户提到麦当劳、麦乐送、麦麦、点麦当劳、想省钱/薅羊毛/领券/优惠、查优惠怎么用、积分兑换、麦麦商城、积分抽奖、麦当劳活动，或询问"怎么点麦当劳最划算"时使用本技能。核心能力：在下单前自动完成"领券→选券→比价→积分抵扣评估"，用 35 个官方工具帮用户以最低价格吃到同样的麦当劳。
version: 2.6.0
license: MIT
---

# 麦麦省钱助手（McD Saver）

本技能通过麦当劳中国官方远程托管的 MCP Server（`https://mcp.mcd.cn`，
Streamable HTTP 协议）为用户提供**以省钱为核心目标**的点餐、优惠、积分服务。

**角色定位**：你不是"点餐员"，而是"省钱顾问"——目标不是帮用户点餐，
而是**帮用户用最少的钱吃到同样的餐**。每一次报价都必须附带省钱明细
（原价、优惠、实付、节省金额）。

## Agent 兼容性

本技能遵循开放的 Agent Skills 标准（SKILL.md + 目录结构），同一份文件可在
WorkBuddy（`~/.workbuddy/skills/`）、Claude Code（`~/.claude/skills/` 或
`.claude/skills/`）、Cursor（`.cursor/skills/` 或 `~/.cursor/skills/`，
兼容 `.agents/skills/`）、OpenAI Codex（`.agents/skills/` 或
`~/.agents/skills/`）直接安装。各平台安装步骤、显式调用方式（`/mcd-saver`
或 `$mcd-saver`）与 MCP 配置位置见 `references/agent-skill-installation.md`。

> ⚠️ 本技能为社区开源项目，与麦当劳公司无关联、无官方背书。
> 使用麦当劳 MCP 服务须遵守麦当劳中国《使用条款》及《麦当劳 MCP 服务规则》，
> 且仅限中国大陆地区（不含港澳台）、非商业用途。

## 前置条件：申请 MCP Token

1. 打开麦当劳 MCP 开放平台：<https://open.mcd.cn/mcp>
2. 点击右上角【登录】，使用手机号验证登录
3. 点击右上角【控制台】→【激活】按钮，申请 MCP Token
4. 同意服务协议后，一键复制 Token

**Token 安全铁律**：
- 绝不将 Token 写入任何会提交到 GitHub 的文件（`config/mcp.example.json` 中的占位符除外）
- 绝不在对话回复、日志、异常信息中展示 Token
- 推荐通过环境变量 `MCD_MCP_TOKEN` 或本机文件 `~/.mcd_mcp_token` 提供

## 接入方式（二选一）

### 方式 A：MCP 客户端直连（推荐）

将以下配置写入 MCP 客户端（WorkBuddy 的 `~/.workbuddy/mcp.json`、Cursor 的
`mcp.json` 等），替换 `YOUR_MCP_TOKEN`：

```json
{
  "mcpServers": {
    "mcd-mcp": {
      "type": "streamablehttp",
      "url": "https://mcp.mcd.cn",
      "headers": {
        "Authorization": "Bearer YOUR_MCP_TOKEN"
      }
    }
  }
}
```

接入后，客户端会自动暴露全部 35 个 `mcp__mcd-mcp__*` 工具，本技能的价值在于
**省钱决策方法论**：何时领券、如何选券、怎样比价、何时用积分
（见下文"省钱四步检查"与 `references/money-saving-strategies.md`）。

### 方式 B：本技能自带 CLI（无需 MCP 客户端支持）

`scripts/mcd.py` 直接通过 Streamable HTTP 调用 MCP Server，仅依赖 Python 3.9+
标准库：

```bash
export MCD_MCP_TOKEN="你的Token"
python scripts/mcd.py check                              # 检查 Token 与连通性
python scripts/mcd.py tools                              # 列出全部工具
python scripts/mcd.py schema available-coupons           # 查看工具入参 Schema
python scripts/mcd.py call available-coupons             # 查可领的麦麦省券
python scripts/mcd.py call query-my-account              # 查积分余额
```

退出码：0 成功 / 1 工具错误 / 2 鉴权失败 / 3 限流 / 4 网络错误。

## 省钱工具地图（35 个，按省钱场景分组）

完整目录见 `references/tools.md`（2026-10-10 实测校准）。

| 省钱场景 | 工具 | 用途 |
|---|---|---|
| 领券 | `available-coupons`、`auto-bind-coupons` | 查可领券 → 一键领取麦麦省全部可领券 |
| 选券 | `query-store-coupons`、`query-my-coupons` | 查指定门店/订单类型下可用的券 |
| 比价 | `calculate-price`、`query-promotions` | 带券试算应付总价；团餐满减/满折规则 |
| 商品优化 | `query-meals`、`query-meal-detail`、`list-nutrition-foods` | 套餐组成与零成本替换项 |
| 积分抵扣 | `query-my-account`、`mall-points-products`、`mall-product-detail`、`mall-create-order` | 积分余额、积分兑换券对比现金购买 |
| 活动情报 | `campaign-calendar`、`now-time-info`、`query-lottery-info`、`draw-lottery`、`query-my-prizes` | 活动日历、抽奖机会与免费次数 |
| 下单闭环 | `create-order`、`cancel-order`、`query-order`、`order-list`、`query-survey-coupon` | 下单、订单管理、满意度答卷奖券回收 |
| 门店与地址 | `query-nearby-stores`、`delivery-query-addresses`、`delivery-create-address`、`delivery-query-stores` | 到店/外送场景前置查询 |
| 团餐 | `query-meal-assistance`、`query-promotions` | 助餐服务与团餐促销 |
| 全渠道比价 | `scripts/deal_compare.py`（本地工具，非 MCP） | 结合美团/抖音等团购券（手动录入）与官方价格估算比价 |
| 组合优化 | `scripts/optimizer.py`（本地工具，非 MCP） | 枚举无券/单券/凑单/改点套餐候选方案，支持预算/热量/蛋白/钠约束，--mcp 模式经 calculate-price 真实计价，输出最优组合 |
| 沉默成本 | `scripts/silent_cost.py`（本地工具，非 MCP） | 临期券扫描 + **用券排程**（可实现 vs 注定过期）+ **多单排程时间轴**（--timeline，逐单给出用哪张、哪天、净价值）+ 消费画像 + 积分体检 + **无面值券实测**（--probe）+ **可分享 HTML 报告**（--html）；数据来自 query-my-coupons/order-list/query-my-account |
| 其他 | `query-party-city/store/date/session`、`party-order-create`、`mall-order-list/detail` | 主题活动与商城订单 |

**入参不确定时**：先执行 `python scripts/mcd.py schema <tool>`（方式 B）或
查看 MCP 客户端展示的工具 Schema（方式 A），不要凭空猜测参数名。

## 省钱四步检查（下单前强制执行）

**规则：任何 `create-order` 之前，必须完成以下四步并向用户展示省钱明细。
用户明确表示"不用优惠直接下单"时可跳过第 1/2 步，但仍需展示无优惠价格。**

### 第 1 步：领券
```
available-coupons（查可领券列表，向用户展示）
→ 用户同意 → auto-bind-coupons（一键领取，写操作需确认）
```

### 第 2 步：选券
```
query-store-coupons（指定门店 + 订单类型 orderType：1=到店含得来速，2=外送含团餐）
→ 结合 query-my-coupons，筛选出对当前购物车最优的券
```

### 第 3 步：比价
```
calculate-price（不带券）→ calculate-price（带最优券组合）
→ 向用户展示：原价 / 优惠金额 / 实付 / 节省比例
→ 若有多个券组合，选择实付最低的组合，并向用户说明选择理由
```

### 第 4 步：积分抵扣评估
```
query-my-account（积分余额、即将过期积分——即将过期积分要主动提醒）
→ mall-points-products 检索同款/同类餐品券
→ 若"积分兑换的餐品券"折算价值 ≥ 购物车中对应商品现金价，提示用户对比方案
→ 由用户决定走"现金+券"还是"积分兑换"
```

**积分价值估算口径**：1 积分 ≈ 0.01 元人民币（常见量级，仅作参考基准），
实际以 `mall-points-products` 返回的兑换价为准。

### 第 5 步（可选增强）：外部团购比价

```
用户从美团/抖音 App 查询麦当劳团购券 → deal_compare.py add 录入
→ deal_compare.py compare --mcd-face <商品合计原价> --mcd-price <MCP带券实付>
→ 输出"官方渠道 vs 团购"估算比价报告与推荐
```

- 数据由用户手动录入（团购平台无公开 API），报告为**估算值**，须明确标注
  "估算，以平台实际页面为准"
- 推荐团购时必须提示：团购券通常**不可叠加**官方优惠券、需核对适用门店/时段
- 方法论详见 `references/group-buy-comparison.md`

## 标准工作流

### 1. 省钱版麦乐送（外送）点餐 —— 主推流程
```
[省钱检查 1-4 步]
delivery-query-addresses（无地址则 delivery-create-address）
→ delivery-query-stores（确定门店）
→ query-meals → query-meal-detail（确定商品 + 零成本替换项）
→ calculate-price（无券 / 带券对比，展示省钱明细）
→ 【用户明确确认】→ create-order → 返回支付链接给用户
→ query-order（跟踪进度）
```

### 2. 省钱版到店取餐 / 堂食 / 得来速
```
query-nearby-stores → query-meals → query-meal-detail
→ [省钱检查 2-4 步] → 【用户确认】→ create-order → query-order
```

### 3. 主题活动（派对/品鉴会）预约
```
query-party-city → query-party-store（选定城市）
→ query-partystore-date（选定门店）→ query-partystore-session（选定日期）
→ 【用户确认】→ party-order-create
```

### 4. 积分兑换 / 抽奖
```
query-my-account → mall-points-products → mall-product-detail
→ 【用户确认】→ mall-create-order
（抽奖：query-lottery-info → 消耗规则与免费次数 →【用户确认】→ draw-lottery）
```

### 5. 最优组合点单（optimizer 工作流）
```
query-meals / query-meal-detail → 写 menu.json（含价格，记录零成本替换项）
→ query-store-coupons + query-my-coupons → 写 coupons.json
   （threshold/discount 从券详情提取，不确定则留空字段）
→ 用户声明想吃清单 → 写 wants.json
→ python scripts/optimizer.py plan --wants wants.json --menu menu.json \
     --coupons coupons.json [--mcp --store-code ...] [--budget 30] [--max-kcal 800]
   （--mcp 真实计价模式的结果才能作为下单依据；估算模式输出必须标注"未经验证"；
     --budget/--max-kcal 为可选约束，违反约束的方案排后展示并标注超出量；
     v1.5 起菜单含 protein/sodium 字段时可用 --min-protein 20 --max-sodium 1500
     做营养约束——数据缺失的方案按不满足处理并如实标注「蛋白质未知」，
     绝不虚构达标。健身/控盐用户主动提出时使用）
→ optimizer plan 输出后自动衔接团购终局建议（本地券库非空时）：
   「官方最优 vs 团购估算」结论 + 适用限制原样提示；`--no-deals` 可关闭
→ 向用户展示方案排名与省钱明细；凑单方案必须附
   "仅当你本来就需要该商品才划算"提示，且不得以凑单方案为默认推荐
→ 营养约束触发时的替换建议策略（味热比思想）：
   最优方案仍超热量/钠上限时，按「热量代价从小到大」逐项给出替换
   （例：中可乐→无糖可乐、中薯条→玉米杯），用户明确表达喜爱的单品
   最后才动；每处替换讲清楚"少多少热量、多多少蛋白"
→ 用户口味偏好（去酸黄瓜、可乐去冰等）在会话内记住并写入后续
   特调参数，不必每次重说
→ 【用户明确确认】→ calculate-price 复核 → create-order
```

### 6. 沉默成本体检（silent_cost 工作流）
```
python scripts/mcd.py call query-my-coupons --raw > coupons.json
python scripts/mcd.py call order-list --raw > orders.json
python scripts/mcd.py call query-my-account --raw > points.json
→ python scripts/silent_cost.py report --coupons coupons.json \
     --orders orders.json --points points.json \
     [--probe --store-code 门店编码] [--html 报告.html]
→ 向用户展示报告（临期券排程给出「可实现 vs 注定过期」金额）；
   临期券与临期积分必须给出优先处理建议；用户要求分享时可给 HTML 报告
```
（--probe：无面值券实测精确价值——实测优先、估算兜底、失败如实标注；
  --html：零依赖单文件报告，可截图分享，不含任何敏感字段）

更多流程（团餐、营养咨询、活动日历等）与分支处理见 `references/workflows.md`；
十一大省钱策略详解见 `references/money-saving-strategies.md`。

## 调用规范（必须遵守）

1. **先查后改**：任何写操作（`create-order`、`cancel-order`、`mall-create-order`、
   `draw-lottery`、`party-order-create`、`delivery-create-address`、
   `auto-bind-coupons`）之前，必须先用查询工具收集完整上下文。
2. **下单必确认**：`create-order` 及所有下单类工具执行前，必须向用户完整展示
   **门店、商品清单、优惠券、省钱明细、总价**，并获得明确确认（如"确认下单"）。
   用户的模糊表述不构成确认，需复述订单要点再次确认。
3. **支付安全**：`create-order` 返回的支付链接只原样转交给用户，由用户自行完成
   支付；本技能不代付、不引导用户在任何非麦当劳域名完成支付。
4. **取消订单**：仅当用户明确表达取消意图时调用 `cancel-order`，并先通过
   `query-order` 核对订单号与订单状态。
5. **限流纪律**：每个 Token 每分钟最多 600 次请求。批量操作时应控制节奏。
6. **不虚构优惠**：省钱明细中的每一笔优惠必须来自 `calculate-price` 的返回值，
   不得自行估算或承诺未经验证的折扣。
7. **比价透明**：团购比价结果必须标注"估算"属性与数据来源（用户录入），
   推荐团购时须同步提示叠加规则限制；不做贬损任何渠道的比较表述。

## 错误处理

| 情形 | 判定 | 处理 |
|---|---|---|
| 401 鉴权失败 | AuthError / HTTP 401 | 引导用户到 open.mcd.cn/mcp 重新申请 Token，不重试 |
| 429 限流 | RateLimitError / HTTP 429 | CLI 已内置指数退避重试；仍失败则告知用户稍后再试 |
| 工具参数错误 | McpToolError | 读取错误详情，用 `schema` 重新核对参数后修正重试（最多 2 次） |
| 网络错误 | TransportError | CLI 已自动重试；仍失败则提示用户检查网络 |

详见 `references/error-handling.md`。

## 目录结构

```
mcd-saver/
├── SKILL.md                            # 本文件：省钱顾问方法论与技能入口
├── README.md / README_EN.md            # 项目说明（中/英，结构与锚点逐位对齐）
├── CHANGELOG.md                        # 版本变更记录（Keep a Changelog 格式）
├── CONTRIBUTING.md                     # 贡献指南与发布流程
├── CODE_OF_CONDUCT.md                  # 贡献者行为准则（Contributor Covenant 2.1 改编）
├── LICENSE                             # MIT 许可证 + 第三方条款声明
├── SECURITY.md                         # 漏洞报告与安全边界（对外披露入口）
├── CONTEST_DECLARATION.md              # 参赛声明（官方原文，未改动）
├── MCP_INTEGRATION.md                  # MCP 集成说明（参赛要求文件）
├── mcp-config.example.json             # 脱敏 MCP 配置（参赛要求文件，与 config/ 版内容一致）
├── workbuddy.md                       # WorkBuddy 开发上下文（WorkBuddy 专项核验用）
├── pyproject.toml                      # 打包元数据与 pytest 配置（版本号随发版同步）
├── requirements-dev.txt                # 开发依赖（pytest / pytest-cov）
├── install.ps1                         # Windows WorkBuddy 一键安装脚本
├── demo.py                             # 离线全链路演示（内嵌 fixture，不联网）
├── .github/
│   ├── workflows/ci.yml                # CI：3.9 / 3.11 / 3.13 矩阵 + 覆盖率门槛
│   ├── ISSUE_TEMPLATE/                 # Bug / 功能建议模板与讨论区入口
│   └── PULL_REQUEST_TEMPLATE.md        # PR 检查清单
├── docs/
│   ├── demo.html                       # 在线试算页（四维约束滑杆 + 数值输入、Token 导入）
│   ├── index.html                      # Pages 根路径索引页（自动进入试算页）
│   ├── coverage-report.md              # 覆盖率报告（--cov=scripts 口径与补测路线）
│   └── assets/banner.svg               # 品牌横幅（版本与测试数随发版同步）
├── config/
│   └── mcp.example.json                # MCP 客户端配置示例（占位符 Token）
├── scripts/
│   ├── console.py                      # 控制台 UTF-8 兜底（Windows 非中文区域不再因中文输出崩溃）
│   ├── mcd_client.py                   # MCP Streamable HTTP 客户端核心（纯标准库、主动限速）
│   ├── mcd.py                          # CLI 入口：check / tools / schema / call
│   ├── deal_compare.py                 # 外部团购比价引擎（美团/抖音券手动录入）
│   ├── optimizer.py                    # 券组合优化器（估算 / --mcp 真实计价双模式、Top-K 预筛）
│   ├── silent_cost.py                  # 沉默成本体检（临期券排程/消费画像/积分/实测）
│   ├── silent_report.py                # HTML 体检报告渲染与省钱等级（silent_cost 再导出）
│   ├── version.py                      # 版本号递增工具（自定义 z.x.y：y≤3、x≤6）
│   ├── verify_run.py                   # 真实运行验证记录生成（自动脱敏）
│   ├── check_toc.py                    # README 目录锚点与中英结构校验
│   ├── sync_readme.py                  # README「近期版本」区块自动生成（源自 CHANGELOG）
│   ├── audit_readme.py                 # README 事实一致性审计（命令表/用例数/版本/许可证）
│   └── build_releases.py               # 发布产物构建与校验（英文 zip + 中文说明）
├── references/
│   ├── tools.md                        # 35 个工具完整目录与使用要点
│   ├── money-saving-strategies.md      # 十一大省钱策略详解（核心参考）
│   ├── group-buy-comparison.md         # 外部团购比价方法论
│   ├── workflows.md                    # 各业务场景的详细调用流程
│   ├── mcp-pitfalls.md                 # MCP 实战踩坑与参数串联指南
│   ├── agent-skill-installation.md     # 各客户端 Agent Skill 安装细则
│   └── error-handling.md               # 错误码、重试策略与排查指南
├── examples/
│   ├── order-flow-example.md           # 一次完整省钱点餐的示例会话
│   ├── three-ways.md                   # 一单三种买法的可复现算例（离线可跑）
│   ├── silent-cost-example.md          # 沉默成本体检离线示例与读法
│   └── verified-run.md                 # 真实环境验证记录（脱敏，可复现）
├── fixtures/                           # 7 份离线回归数据（菜单/券/订单/积分/团购等）
├── releases/                           # 发布产物：每版英文 zip + 中文说明 + 索引
└── tests/                              # pytest 单元测试（337 个用例 + 一致性校验）
```
