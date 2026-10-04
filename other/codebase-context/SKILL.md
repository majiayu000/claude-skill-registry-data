---
name: codebase-context
description: 项目代码库上下文管理。通读项目生成参考文档(scan)，或加载文档辅助开发(dev)。
trigger: manual
metadata:
  argument-hint: "<scan|dev> [project-name] [--full]"
---

# codebase-context — 项目代码库上下文管理

这是一份写给 AI 执行的 SOP。目的：把"每次开发前重读整个代码库"这个昂贵动作**一次性固化成结构化文档缓存**，后续开发直接加载文档当上下文。

- **scan（生产）**：系统通读源码，生成结构化参考文档。
- **dev（消费）**：加载参考文档进上下文辅助开发，开发完成后自动评估并回写更新文档。

## 参数解析

调用格式：`/codebase-context <mode> [project-name] [--full]`

1. 解析第一个参数为 `mode`：
   - 值为 `scan` → 进入 scan 模式
   - 值为 `dev` → 进入 dev 模式
   - 缺失或为其他值 → 输出用法提示 `用法: /codebase-context <scan|dev> [project-name] [--full]` 并终止
2. 解析第二个非 `--` 开头参数为 `project-name`：
   - 已提供 → 直接使用
   - 未提供 → 用 Bash 执行 `basename "$PWD"`，取当前工作目录最后一段路径名作为 project-name
3. 检查是否存在 `--full` 参数：
   - 存在且 mode=scan → 强制全量扫描
   - 存在且 mode=dev → 忽略该参数并提示"--full 仅 scan 模式有效"
4. 设定文档目录 `DOC_DIR = {PROJECT_ROOT}/docs/codebase-context/`（存于项目工程内,随 git 提交、团队共享、换机不丢）
5. 设定项目根 `PROJECT_ROOT = 当前工作目录`

## 产物清单（固定 10 份文档 + 1 份元数据）

全部存于 `DOC_DIR` 下，文件名固定，不得增删改名：

| 文件 | 内容 |
| ---- | ---- |
| 00-index.md | 索引与快速导航 |
| 01-overview.md | 项目概述与技术栈 |
| 02-directory.md | 目录结构 |
| 03-architecture.md | 架构设计与模块关系 |
| 04-api-routes.md | API 接口汇总 |
| 05-data-models.md | 数据模型与类型 |
| 06-core-modules.md | 核心模块（组件/Hooks/Store） |
| 07-business-logic.md | 关键业务逻辑 |
| 08-conventions.md | 编码规范与约定 |
| 09-changelog.md | 文档变更记录 |
| .scan-meta.json | `{"lastScanTime":"UTC时间","scanType":"full|incremental","projectRoot":"绝对路径"}` |

---

## scan 模式流程

### 步骤 1：初始化

1. 按参数解析规则推导 project-name
1.5 **多项目仓库检测（禁止扫仓库根）**：用 Glob 匹配 `*/package.json`、`*/*/package.json`（及 Cargo.toml/go.mod 等）——若当前目录自身不是单一项目根（无 src/），而多个子目录各含项目描述文件 → **列出候选子项目并让用户选定**（或用 project-name 参数匹配子目录名）；选定后 `PROJECT_ROOT`/`DOC_DIR` 重设为该子项目根。把多个不相干项目扫进一张地图，查重与波及面全部失真——**脏地图比没地图更危险**（实跑教训：4 项目混装仓库靠人肉 cd 才扫对）
2. 设定 DOC_DIR
3. 判断扫描模式（分支条件显式如下）：
   - DOC_DIR 不存在 → **全量扫描**
   - 带 `--full` 参数 → **全量扫描**
   - DOC_DIR 已存在 且 存在 `.scan-meta.json` 且 无 `--full` → **增量扫描**
   - DOC_DIR 已存在 但 缺 `.scan-meta.json` → **全量扫描**（元数据缺失视同首扫）
4. 用 Bash 执行 `mkdir -p {DOC_DIR}` 创建目录

### 全量扫描

#### 步骤 2a：系统读取代码（分 7 轮，每轮用 Glob/Grep/Read）

**规模档位（先数源码文件再动手）**：≤200 个源文件 → 按下述七轮正常执行；**>200 个** → 第 4/5/6 轮不逐个 Read，改用 Grep 收 export 签名清单入表（函数名/类型名/位置），精读仍限抽样 3–5 个最复杂文件；**>500 个** → 同上，并提示用户"项目较大，建议按模块分次 scan（cd 到子模块根分别执行）"。防止扫到一半上下文耗尽——成本花了、地图没产出是最差结果。

**第 1 轮 项目元信息**：用 Read 读取 `package.json`、`README.md`；用 Glob 匹配构建配置 `vite.config.*`、`webpack.config.*`、`tsconfig.json`、`next.config.*`、`.env.example`，逐个 Read。提取：项目名/版本/依赖清单/脚本命令/构建工具/环境变量键名。

**第 2 轮 目录结构**：用 Bash 执行 `ls -R`（或用 Glob `src/*/*` 展开 src 两层）。识别 `pages/`、`components/`、`api/`、`store/`、`hooks/`、`utils/`、`types/` 等目录及其职责。

**第 3 轮 入口与路由**：用 Glob 定位 `main.*`、`index.*`、`App.*`、`router/`、`routes/`，逐个 Read；用 Grep 搜索全局 store 初始化与全局 service 入口。提取：启动链路、路由表、全局状态挂载点。

**第 4 轮 API 接口层**：用 Glob 匹配 `**/api/**` 与 `**/services/**`，逐个 Read。提取每个接口函数的：函数名 / HTTP 方法 / URL / 参数 / 返回类型 / 定义位置（文件:函数）。

**第 5 轮 数据模型与类型**：用 Glob 匹配 `**/types/**`、`**/models/**`、`**/interfaces/**`、`**/enums/**`，逐个 Read。提取：实体 / 枚举 / DTO 及各自定义位置。

**第 6 轮 核心模块**：用 Glob 展开 `components/`（区分公共组件 vs 业务组件）、`hooks/`、`store/`，逐个 Read 提取签名与职责；再用 Grep 按 import 次数与文件行数**抽样精读 3–5 个最复杂的页面/组件**（Read 全文），提取其状态、关键流程。

**第 7 轮 规范与工具**：用 Glob 匹配 `**/constants/**`、`**/config/**`、`**/utils/**` 及 `.eslintrc*`、`.prettierrc*`，逐个 Read。提取：常量清单 / 工具函数清单 / 可推断的代码规范。

#### 步骤 3a：生成文档

依据下方【文档模板】，按 00 → 09 顺序逐份用 Write 生成 10 份文档，照模板填空。

#### 步骤 4a：写元数据与摘要

1. 用 Bash 执行 `date -u +"%Y-%m-%dT%H:%M:%SZ"` 取 UTC 时间
2. 用 Write 写 `.scan-meta.json`：`{"lastScanTime":"{UTC}","scanType":"full","projectRoot":"{PROJECT_ROOT}"}`
3. 输出终端摘要：

```text
✅ codebase-context 全量扫描完成 — {project-name}
📁 文档目录: {DOC_DIR}
📄 生成文档: 10 份（00-index ~ 09-changelog）
📊 扫描统计: 接口 {N} 个 | 类型 {N} 个 | 组件 {N} 个 | Hooks {N} 个 | 精读页面 {N} 个
▶ 开发时执行: /codebase-context dev {project-name}
```

### 增量扫描

#### 步骤 2b：变更检测

1. 用 Read 读 `.scan-meta.json`，取 `lastScanTime` 与 `projectRoot`
2. 用 Bash 执行：

```bash
find {projectRoot}/src -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.vue" -o -name "*.json" \) -newer {DOC_DIR}/.scan-meta.json
```

3. 将结果与 `02-directory.md` 记录的文件清单对比，推断**新增文件**（结果里有、文档里无）与**删除文件**（文档里有、磁盘上无——用 Bash `test -f` 验证）
4. mtime 检测未命中不证明地图最新（可能遗漏 src 外文件、其他语言或分支切换）。补查项目实际源码/配置路径及 Git 工作树变化；无可信历史基线时明确本次检测范围与限制，不能输出“全仓无变更/文档已是最新”

#### 步骤 3b：确定受影响轮次（映射表）

按下表将每个变更文件路径映射到扫描轮次，**只重跑受影响的轮次**：

| 文件路径模式 | 扫描轮次 | 需更新文档 |
| ---- | ---- | ---- |
| package.json / README / vite・webpack・tsconfig・next 配置 / .env.example | 第 1 轮 | 01-overview |
| 目录新增/删除（任何路径层级变化） | 第 2 轮 | 02-directory |
| main.* / index.* / App.* / router/ / routes/ / 全局 store・service 入口 | 第 3 轮 | 03-architecture |
| \*\*/api/\*\* 、 \*\*/services/\*\* | 第 4 轮 | 04-api-routes |
| \*\*/types/\*\* 、 \*\*/models/\*\* 、 \*\*/interfaces/\*\* 、 \*\*/enums/\*\* | 第 5 轮 | 05-data-models |
| components/ 、 hooks/ 、 store/ | 第 6 轮 | 06-core-modules |
| pages/ 下的页面文件 | 第 6 轮 | 06-core-modules、07-business-logic |
| \*\*/constants/\*\* 、 \*\*/config/\*\* 、 \*\*/utils/\*\* 、 eslint/prettier 配置 | 第 7 轮 | 08-conventions |
| （任何变更，无条件） | — | 09-changelog、00-index（日期） |

#### 步骤 4b：增量合并

1. 用 Read 读取受影响的现有文档（只读需更新的那几份）
2. 用 Read **只读变更文件**（不重读全库）
3. 用 Edit 增量合并，禁止全量覆盖：
   - 新增内容 → 在对应章节**追加**行/条目
   - 修改内容 → **替换**对应行/条目
   - 删除文件涉及的条目 → **移除**对应行/条目

#### 步骤 5b：收尾更新

1. 用 Edit 更新 `00-index.md` 的"最后更新"日期
2. 用 Edit 在 `09-changelog.md` 追加本次条目（日期/类型 incremental/变更摘要/涉及文档）
3. 仅在变更检测覆盖项目实际源码/配置且基线可信时更新 `.scan-meta.json`（`scanType: "incremental"`）；否则保留原元数据，在索引/日志标明本次局部核实范围，不用新时间掩盖未知区域

#### 步骤 6b：输出变更检测摘要

```text
✅ codebase-context 增量扫描完成 — {project-name}
🔍 变更检测: 新增 {N} 个 | 修改 {N} 个 | 删除 {N} 个
📄 已更新文档: {文档列表，如 04-api-routes、05-data-models、09-changelog、00-index}
```

---

## dev 模式流程

### 步骤 1：加载

1. 按参数解析规则推导 project-name，设定 DOC_DIR
2. 分支判断：
   - DOC_DIR 不存在或缺少索引 → 按 `references/writeback.md` 先查项目指定地图，否则从代码定向建立本次链路；任务目标缺失时先补问目标，不盲扫全仓
   - 有索引 → 按索引读取本次任务相关且实际存在的文档；局部地图只代表标注的覆盖范围
3. 按 `references/writeback.md` 核实地图与当前代码；过期、错误或缺少相关链路时定向补查，确认本次影响范围后才能改业务代码。授权范围内审前回写，不强制全量 scan
4. 输出已加载确认（项目概要从已读资料提取，缺失则不猜）：

```text
📚 已加载 {project-name} 参考文档（{实际数量} 份，覆盖 {相关模块}，最后更新 {日期}）
📌 项目概要: {已核实的一句话或待核实}
```

### 步骤 2：辅助开发

开发过程中强制遵循：

1. 编码风格遵循 `08-conventions.md` 的规范与约定
2. 调用接口前先查 `04-api-routes.md`——**已有接口直接复用，不重复造**
3. 定义类型前先查 `05-data-models.md`——**已有类型直接引用，不重复定义**
4. 写组件/Hook 前先查 `06-core-modules.md`——**已有组件/Hook 直接复用**
5. 新代码放置位置参考 `03-architecture.md` 的分层与模块归属

### 步骤 3：开发完成后强制评估回写

开发结束、独立审查前**必须**按 [业务地图增量回写](references/writeback.md) 评估并更新受影响章节；
无需更新时说明依据。需求开发和缺陷修复复用同一判据，不重复扫描或在批准后回写。

---

## 文档模板

生成时照模板填空；某章节在本项目无对应内容时保留标题并填"本项目未发现此类文件"。

### 00-index.md

````markdown
# {project-name} — 代码库参考文档索引

- 最后更新: {YYYY-MM-DD HH:MM UTC}
- 扫描类型: {full | incremental}
- 项目根: {projectRoot}

## 文档导航

| 文档 | 内容 | 什么时候看 |
| ---- | ---- | ---- |
| 01-overview | 项目概述与技术栈 | 初次接触项目 |
| 02-directory | 目录结构 | 找文件放哪/在哪 |
| 03-architecture | 架构与模块关系 | 新代码归属、理解依赖方向 |
| 04-api-routes | API 接口汇总 | 调接口前查重 |
| 05-data-models | 数据模型与类型 | 定义类型前查重 |
| 06-core-modules | 组件/Hooks/Store | 写组件前查复用 |
| 07-business-logic | 关键业务逻辑 | 改业务流程前看线路 |
| 08-conventions | 编码规范与约定 | 动手写代码前 |
| 09-changelog | 文档变更记录 | 追溯文档演进 |

## 快速定位

| 我想找… | 去 |
| ---- | ---- |
| 某个接口怎么调 | 04-api-routes |
| 某个字段的类型定义 | 05-data-models |
| 有没有现成组件/Hook | 06-core-modules |
| 某业务流程的完整线路 | 07-business-logic |
| 命名/风格规矩 | 08-conventions |
````

### 01-overview.md

````markdown
# 项目概述与技术栈

## 项目定位

{一句话说明这个项目是什么、给谁用、解决什么问题}

## 技术栈

| 层 | 技术 | 版本 |
| ---- | ---- | ---- |
| 语言 | {TypeScript/…} | {x.y} |
| 框架 | {React/Vue/…} | {x.y} |
| 构建 | {Vite/Webpack/…} | {x.y} |
| 状态管理 | {…} | {x.y} |
| 其他关键依赖 | {…} | {x.y} |

## 脚本命令

| 命令 | 作用 |
| ---- | ---- |
| `npm run dev` | {…} |
| `npm run build` | {…} |
| `npm run test` | {…} |

## 环境变量（仅键名与用途，不含值）

| 键 | 用途 | 来源 |
| ---- | ---- | ---- |
| {ENV_KEY} | {…} | .env.example |
````

### 02-directory.md

````markdown
# 目录结构

## 目录树（src 两层）

```text
src/
├── pages/          # {职责}
├── components/     # {职责}
├── api/            # {职责}
├── store/          # {职责}
├── hooks/          # {职责}
├── utils/          # {职责}
└── types/          # {职责}
```

## 目录职责

| 目录 | 职责 | 典型文件 |
| ---- | ---- | ---- |
| {src/pages} | {…} | {…} |

## 文件清单（供增量扫描对比新增/删除）

| 文件 | 所属轮次 |
| ---- | ---- |
| {src/api/user.ts} | 4 |
````

### 03-architecture.md

````markdown
# 架构设计与模块关系

## 分层结构

```text
{页面层 pages}
    ↓ 调用
{逻辑层 hooks / store}
    ↓ 调用
{服务层 api / services}
    ↓ 请求
{后端 / 云函数}
```

## 启动链路

{main.* → App.* → 路由挂载 → 全局 store 初始化，逐步说明，每步带 文件:位置}

## 路由表

| 路径 | 页面 | 定义位置 |
| ---- | ---- | ---- |
| {/home} | {pages/home} | {router/index.ts} |

## 模块依赖关系

| 模块 | 依赖谁 | 被谁依赖 |
| ---- | ---- | ---- |
| {store/user} | {api/user} | {pages/*, hooks/useAuth} |
````

### 04-api-routes.md

````markdown
# API 接口汇总

## {模块名，如 user}

| 函数名 | 方法 | URL | 参数 | 返回类型 | 定义位置 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| {getUser} | GET | {/api/user/:id} | {id: string} | {User} | {src/api/user.ts} |

（按模块分节重复上表；无 api/ 与 services/ 目录时填"本项目未发现此类文件"）
````

### 05-data-models.md

````markdown
# 数据模型与类型

## 实体

| 名称 | 字段摘要 | 定义位置 | 主要使用方 |
| ---- | ---- | ---- | ---- |
| {User} | {id, name, role…} | {src/types/user.ts} | {api/user, store/user} |

## 枚举

| 名称 | 取值 | 定义位置 |
| ---- | ---- | ---- |
| {OrderStatus} | {pending/paid/closed} | {src/types/order.ts} |

## DTO / 请求响应类型

| 名称 | 用于接口 | 定义位置 |
| ---- | ---- | ---- |
| {CreateOrderReq} | {POST /api/order} | {src/types/dto.ts} |
````

### 06-core-modules.md

````markdown
# 核心模块

## 公共组件

| 组件 | Props 摘要 | 定义位置 | 复用场景 |
| ---- | ---- | ---- | ---- |
| {Button} | {type, onClick…} | {src/components/common/} | {全局} |

## 业务组件

| 组件 | 职责 | 定义位置 | 所属业务 |
| ---- | ---- | ---- | ---- |

## Hooks

| 名称 | 输入 | 输出 | 定义位置 |
| ---- | ---- | ---- | ---- |
| {useAuth} | {—} | {user, login, logout} | {src/hooks/useAuth.ts} |

## Store

| 模块 | state 摘要 | 主要 actions | 定义位置 |
| ---- | ---- | ---- | ---- |

## 复杂页面精读（3–5 个）

### {页面名}（{文件路径}）

- 职责: {…}
- 关键状态: {…}
- 关键流程: {步骤 1 → 步骤 2 → …，每步带函数名}
````

### 07-business-logic.md

````markdown
# 关键业务逻辑

## {业务线名，如：下单}

**线路**：{页面 pages/order} → {hook useOrder} → {api createOrder} → {POST /api/order} → {模型 Order}
（每个环节标注 文件:函数）

**关键规则**：

- {规则 1，如：金额用分存储，展示层才转元 —— src/utils/money.ts}
- {规则 2}

**边界与注意**：

- {已知坑/特殊分支/兼容逻辑，带位置}

（按业务线重复本节）
````

### 08-conventions.md

````markdown
# 编码规范与约定

## 命名

| 对象 | 规则 | 示例 |
| ---- | ---- | ---- |
| 组件文件 | {PascalCase} | {UserCard.tsx} |
| hooks | {use 前缀} | {useAuth} |

## 代码风格（自 ESLint/Prettier 推断）

- {缩进/引号/分号/import 排序 等要点}

## 常量

| 常量 | 值/含义 | 定义位置 |
| ---- | ---- | ---- |

## 工具函数

| 函数 | 用途 | 定义位置 |
| ---- | ---- | ---- |

## 其他约定

- {错误处理方式/请求封装规则/目录放置约定}
````

### 09-changelog.md

````markdown
# 文档变更记录

| 日期(UTC) | 类型 | 变更摘要 | 涉及文档 |
| ---- | ---- | ---- | ---- |
| {2026-07-14T08:00Z} | full | 首次全量扫描 | 全部 10 份 |
| {…} | incremental | {新增 2 接口/修改 1 类型} | {04、05} |
| {…} | dev回写 | {开发 xx 功能后回写} | {04、06、07} |
````

---

## 错误处理

1. **无 package.json**：项目根不存在 package.json → 输出 `⚠ 当前目录未发现 package.json，请确认 {PROJECT_ROOT} 是正确的项目目录（回复继续则按非 npm 项目扫描）`，等用户确认后再继续。
2. **某轮目标目录不存在**（如无 `api/`）：跳过该轮，在对应文档的相应章节标注"本项目未发现此类文件"，不报错不中断。
3. **超大文件（>1000 行）**：不复制全文，只用 Grep/Read 提取关键导出（export 的函数/类/类型签名），并在文档条目备注 `(大文件,仅提取签名)`。
4. **dev 模式文档缺失或陈旧**：按 `references/writeback.md` 定向核实/补齐；证据不足暂停相关修改，不猜测，不强制全量 scan。
