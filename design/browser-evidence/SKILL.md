---
name: browser-evidence
description: 浏览器取证能力的统一入口：探测本机可用后端（ego-browser / agent-browser / Playwright），按平台与任务选型，统一截图与录屏产物契约并给出降级档位；缺能力时明确告知、绝不自行安装。触发："能不能截图走查"、"用哪个浏览器跑"、"取证档位怎么定"、"browser evidence"。
---

# 浏览器取证（browser-evidence）

## 概述

**目的**：把"用什么浏览器取证"从每个 skill 各自猜，变成**一次探测、全仓同口径**。消费方（`frontend-walkthrough` / `product-manager` / `ui-designer` / `frontend-index`）只读结论，不重复实现探测逻辑。

**功能**：
- **三后端探测**：按 `ego-browser → agent-browser → Playwright` 探测，**允许全部失败**，失败不阻塞
- **平台硬门**：ego-browser 仅 macOS / Windows；Linux / WSL 直接出局到下一候选
- **任务选型**：过门后按"要不要登录态 / 要不要批量多视口 / 要不要可复用脚本"决定用谁——不是"有就一律用"
- **统一产物契约**：截图命名 + `meta.json`，下游不感知后端差异
- **档位映射**：输出与既有档位语言（`A/B/C`、`L0–L3`）对应，**不新造一套**
- **降级链**：无后端 → 用户供图 → 纯静态，每级写明证据上限

**使用场景**：
- 走查 / 体验评审 / 视觉核对前，确定"这轮能不能拿到画面、是什么档"
- 用户问"我这台是 Linux，能截图吗""用哪个浏览器跑"
- 上游 skill 里写着"无浏览器工具时标 `[未截图]`"，需要判定到底有没有

---

## 定位

| 邻接能力 | 它做什么 | 本 skill 做什么 |
|---|---|---|
| `frontend-walkthrough` A/B/C 档 | 走查流程与缺陷知识（十族 / 时序矩阵 / 证据包） | 只回答"这轮是 A 还是 B/C，以及拿什么取证" |
| `product-manager` M4 L0–L3 | 产品视角界面走查 | 同上，供其能力探测步骤调用 |
| `ui-designer` | 视觉方案与 demo | demo 的多视口截图由本 skill 给后端、命令与产物路径 |
| `index-lookup` | 同类"统一入口 + 自动降级"门面（管索引） | 同一模式，本 skill 管的是**工具** |

> 本 skill 是**能力门面**，不承担走查判断：发现什么、算不算缺陷、多严重，归各消费方。

---

## 核心原则

1. **探测一次，全轮复用**：一轮任务开头探完，中途不反复试；确需换后端要先说明原因，且保留旧产物
2. **平台是硬门，不是优先级**：ego-browser 在 Linux / WSL 上不是"优先级低"，是**不存在**——别写成"优先尝试 ego-browser"
3. **有后端 ≠ 该用它**：先问任务要什么（登录态 / 多视口 / 脚本化 / 只要一张图），再选后端
4. **绝不自行安装 / 升级 / 下载**：`agent-browser install`、`playwright install`、`ego-browser upgrade`、裸 `npx playwright` 一律只提示用户执行
5. **降级不是失败**：拿不到画面是常态，写明档位与证据上限即可；**禁止为了"能截图"编造画面**
6. **产物对外一致**：不管哪个后端，产出同一套文件名与 `meta.json`，下游不感知后端
7. **探测结果同样不许编造**：没真跑探测就不能说"browser-evidence 判定为 A 档"；**未探测一律按 C 档**并声明。这条是"档位诚实"在能力层的延伸——上游 skill 的 `🟢` 全靠它撑着

---

## 工作流（三步，一次跑完）

### 1. 判平台

| 环境 | 判定 |
|---|---|
| macOS / Linux | `uname -s` → `Darwin` / `Linux` |
| Windows（PowerShell） | `$env:OS` 为 `Windows_NT`；或 `$IsWindows` 为 `$true` |
| Windows（Git Bash / MSYS） | `uname -s` → `MINGW64_NT-*` / `MSYS_NT-*` |
| **WSL** | `uname -s` 为 `Linux` **且** `grep -qi microsoft /proc/version` 命中 |

> **WSL 必须单独判**：它属 Linux 侧（ego-browser 用不了），不要因为"宿主是 Windows"就归到 Windows。命令全表见 [reference.md](reference.md#1-平台判定全表)。

### 2. 探测后端（三条命令，全部允许失败）

| 后端 | 探测命令 | 成功判据 |
|---|---|---|
| **ego-browser** | `command -v ego-browser`（Win: `Get-Command ego-browser`） | 存在 **且** `ego-browser skill` 输出末尾出现 `[ego-browser:skill] end of guide` |
| **agent-browser** | `command -v agent-browser` + `agent-browser --version` | 输出版本号（如 `agent-browser 0.25.4`） |
| **Playwright** | `node -e "require.resolve('playwright')"` 或 `<项目>/node_modules/.bin/playwright --version` | 能解析到模块 |

- **不要用 `npx playwright` 探测**：未安装时 npx 会去下载，探测变成安装
- **不要用 `npx agent-browser`**：它自己文档明写走 Node 慢，且直接二进制才是快路径
- 三条都不通 → 直接进降级链，**不重试、不装东西**

### 3. 选型并声明

按「后端选型矩阵」定后端。**两条捷径优先于探测顺序**：

- **项目已 pin Playwright**（`package.json` 里有 `playwright` / `@playwright/test`）且任务要求可复用脚本或进 CI → **直接选 Playwright**，不必先试前两个。探测顺序是兜底顺序，不是"谁先装好就用谁"
- **环境已被明确告知**（用户说"这台是 WSL、没装浏览器"，或本轮开头已判定过）→ 跳过探测直接用结论，不重复跑三条命令

否则按 1 → 2 → 3 顺序探测，命中即停。定好后在报告头写一行：

```text
取证后端：{ego-browser | agent-browser x.y.z | playwright x.y | 无}｜平台：{macOS 14 | Windows 11 | WSL2 | Linux}｜档位：{A | B1 | B2 | C}
```

> 落到下游报告头时按各自口径改写：`frontend-walkthrough` 里 B1 / B2 **一律记 `B`**；`product-manager` 里分别记 **L2 / L3**。本 skill 的 B1 / B2 只是取证动作的细分，不是新档位。

---

## 后端选型矩阵

| 需求 | ego-browser | agent-browser | Playwright |
|---|---|---|---|
| **平台** | **仅 macOS / Windows** | 全平台 | 全平台 |
| 复用**用户真实登录态** | ✅ 原生（就是用户自己的浏览器） | ◐ `--profile` / `--auto-connect` 借用 Chrome profile | ◐ `storageState`（需先导出） |
| 与用户并行、不抢窗口 | ✅ Space 隔离 | ❌ 另起浏览器或接管用户 Chrome | ❌ |
| 多视口批量截图 | ◐ 逐次设置 | ✅ `set viewport` + `batch` | ✅ 脚本循环 |
| 页面结构理解 | ✅ 原生 snapshot | ✅ `snapshot`（带 `@eN` 引用可直接点击） | ◐ `ariaSnapshot` |
| HAR / trace / 录屏 | ◐ 视版本 | ✅ `network har` / `trace` / `record` | ✅ |
| 可复用脚本 / CI / 断言 | ❌ | ◐ `batch` | ✅ 首选 |
| 零配置（本机常已就绪） | ❌ 需装 GUI 应用 + onboarding | ✅ 常已装，且自动复用现有 Chrome / Playwright 浏览器 | ◐ 需模块 + 浏览器二进制 |

**选择顺序（是判据，不是排名）**：

1. 要**用户已登录**的页面，且平台是 macOS / Windows → **ego-browser**
2. 要**多视口批量 / HAR / trace / 录屏** → **agent-browser**（快）或 **Playwright**（要脚本化时）
3. 要**写成可复用脚本、进 CI、做断言** → **Playwright**
4. 只求"看一眼" → **agent-browser**（零依赖，一条命令）

---

## 产物契约

```text
{artifactRoot}/{slug}/
├── screenshots/{state|issue}-{NNN}[-step-N].png
├── videos/{issue}-{NNN}-repro.webm        # 静态类问题不产视频
└── meta.json
```

`meta.json` 字段（各消费方**只统一格式，不统一目录**）：

```json
{
  "backend": "agent-browser",
  "backendVersion": "0.25.4",
  "os": "wsl2",
  "url": "http://localhost:3000/orders",
  "viewport": "1440x900",
  "dpr": 1,
  "fullPage": false,
  "tier": "A",
  "constructedBy": "Slow 3G",
  "ts": "2026-11-12T16:27:00+08:00"
}
```

`artifactRoot` 归消费方：`frontend-walkthrough` → `.walkthrough/`，`product-manager` → `.pm/shots/`，`ui-designer` → `.ui-review/shots/`。

---

## 档位映射（不新造语言）

| 本 skill 结论 | frontend-walkthrough | product-manager M4 | 条件 |
|---|---|---|---|
| **A** | A 可实操 | L1 自主 | 任一后端可用 **且** 服务可达 |
| **B1** | B 半实操 | L2 半自主 | 页面能打开，但拿不到渲染画面（如只有 `preview_url`） |
| **B2** | B 半实操 | L3 手动上传 | 无后端 / 服务起不来，由用户按拍摄清单供图 |
| **C** | C 纯静态 | L0 纯静态 | 无任何画面 |

> B1 / B2 在本 skill 里分开（取证动作不同），在两边原档位里分别归 `B` 与 `L2 / L3`——**映射是多对一，不要强行 1:1**。

---

## 降级链

```text
1. ego-browser      仅 macOS / Windows；登录态原生
2. agent-browser    全平台；零配置；快
3. Playwright       全平台；要脚本 / CI / 断言时
4. B1 只能开预览     拿不到画面 → 静态推演 🟡 + 肉眼清单
5. B2 用户供图       给拍摄清单（哪几屏 / 什么状态 / 什么分辨率）
6. C  纯静态         体验类结论强制 🔴，报告头声明
```

每级都必须说清"能做什么 / 证据上限"，**不得跳级宣称**。

---

## 红线

1. **不自动安装 / 升级 / 下载**：四个入口（`agent-browser install`、`playwright install`、`ego-browser upgrade`、裸 `npx`）一律只给用户命令，不代跑
2. **不碰用户真实凭据**：ego-browser 的 **profile 级** cookie / 缓存清除不可逆（须用户批准）；agent-browser 的 `cookies clear`、`--profile` 复用登录态同理
3. **不指向生产**：`baseURL` 限 localhost / 内网 dev / 用户明确指定的环境；环境不明先问
4. **默认不用远程 provider**：`browserbase` / `kernel` / `browserless` / `agentcore` 会把页面内容送出本机，需用户显式同意
5. **截图只证那一帧**：不证流程、不证交互（与 `frontend-walkthrough` 同口径）
6. **落盘前看有没有他人数据**：列表页可能含真实用户 PII，对外交付前提示
7. **证据产物不入库**：截图 / 视频动辄几十 MB，整页长图更大——`.walkthrough/`、`.pm/shots/`、`.ui-review/` 一类目录建议进 `.gitignore`，只在需要交接时单独打包

---

## 集成（消费方清单 · SSOT）

| 消费方 | 接入点 | 用法 |
|---|---|---|
| `frontend-walkthrough` | 阶段 0 档位判定 / 阶段 2 取证 / 阶段 3 性能 | 调本 skill 拿 A/B/C 与后端；证据包规格仍按其 `02-timing.md` |
| `product-manager` | M4「能力探测」 | 调本 skill 拿 L0–L3 对应档；无画面时按其拍摄清单降级 |
| `ui-designer` | 阶段 7 demo 验证 | 要 375 / 768 / 1440 截图时按本 skill 选后端与视口命令 |
| `frontend-index` | 建库后加强版实测 | 用本 skill 取后端，比对网络面板实际请求与索引条目 |
| `e2e-testing` | 需要真实浏览器驱动时 | 只取后端与启动方式，断言逻辑归其自身 |

> 集成方**必须自行降级**：探测不到就按原档位退，不阻塞、不报错。

---

## 常见坑

| 现象 | 原因 | 处理 |
|---|---|---|
| `npx playwright --version` 报 canceled / 要下载 | 未安装，npx 想拉包 | 改用 `require.resolve` 探测；要装请用户执行 |
| agent-browser 能跑但从没跑过 `install` | 它会**自动复用**已有的 Chrome / Brave / Playwright / Puppeteer | 正常路径，不必 install |
| WSL 里 `ego-browser` 找不到 | 装在 Windows 宿主，WSL 的 PATH 不通 | 归 Linux 侧，走 agent-browser / Playwright |
| `--auto-connect` 后用户浏览器被导航走 | 该参数就是**接管**正在跑的 Chrome | 只在用户知情时用；默认用独立会话 |
| 截图全白 | 页面没加载完 / 视口设成 0 | 先 `wait --load networkidle`，再设视口后截 |
| 录出来的视频看不清 | 动作之间没停顿 | 每步之间加约 1s（规格见 `frontend-walkthrough` 的「证据包最小规格」） |

---

## 更多资源

- 探测命令全表（POSIX / PowerShell）、三后端最小命令集、登录态三条路径、WSL 与远程开发特例、故障排查：见 [reference.md](reference.md)
- 三个端到端示例（macOS 有 ego / WSL 只有 agent-browser / 全都没有）：见 [examples.md](examples.md)
