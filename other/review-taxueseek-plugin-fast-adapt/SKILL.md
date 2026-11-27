---
name: dsh-plugin-review
description: DSH 插件代码审查与防御性架构审核车道。基于 Git 范围或工作区源码，检查 Cordis 生命周期泄漏、未逆向注销、单例状态漂移、已废弃模板变量（如 {{cwd}}）、Vendored Peer 依赖污染、准入账本覆盖，按 P0/P1/P2/P3 输出精炼结构化报告；提供子 Agent 隔离委派协议（Sub-agent Dispatch Pattern），在后台沙箱运行紧凑分析并回传精炼结果，防止主会话上下文污染。触发词：代码审查、代码审核、code review、插件体检、防御性审查、生命周期检查、单例泄漏、Peer污染、子Agent审查、紧凑报告。
---

# 代码审查与防御性架构车道

在插件适配或交付前，对代码进行深度架构审计。重点排查 Cordis 生命周期泄漏、单例漂移、Vendored Peer 依赖污染以及废弃 API，按统一严重度（P0/P1/P2/P3）给出明确判定。

同时定义**子 Agent 隔离委派协议（Sub-Agent Dispatch Pattern）**：当面对复杂插件或批量巡检时，主 Agent 派发独立子 Agent 执行重型静态分析与冒烟，仅回传结构化紧凑报告（`<20` 行），避免海量日志填满主会话上下文。

以下命令都相对工具根目录执行，工具根即本文件真实路径往上两级、含 `scripts/` 的那一层。脚本用自身文件的绝对路径定位，不必先 cd。`<插件目录>` 指被查插件的仓库根。

## 第一步：会话内极速体检

```sh
node scripts/plugin-audit.mjs <插件目录> --compact
```

使用 `--compact` 参数时，脚本仅输出高密度结构化 JSON 摘要与关键结论，屏蔽全量文件遍历噪音：

```json
{
  "plugin": "my-plugin@1.0.0",
  "overallScore": 95,
  "scores": { "performance": 100, "resilience": 90, "contextBudget": 100, "lifecycle": 90 },
  "priorityCounts": { "P0": 0, "P1": 1, "P2": 0, "P3": 0 },
  "blockers": [
    {
      "priority": "P1",
      "dimension": "lifecycle",
      "file": "lib/index.js",
      "title": "事件监听或定时器未绑定清理逻辑",
      "detail": "Cordis 插件重载时未清理的监听器与定时器会泄漏，建议注册进 ctx.effect 或提供 dispose。"
    }
  ]
}
```

## 第二步：子 Agent 隔离委派协议（Sub-Agent Dispatch Pattern）

当审查整个插件仓库或运行全流程适配验证时，主 Agent 应按以下协议委派后台子 Agent：

1. **派发子 Agent**：通过 `subagent`（或需要继承本会话上下文时用 `subagent_fork`）唤醒子 Agent，指定只读工作区；需要长期跟进时给它一个 `name`，后续用名字寻址；
2. **执行紧凑流水线**：
   ```sh
   node scripts/run.mjs <插件目录> --compact
   ```
3. **回传协议**：子 Agent **严禁**直接复制全量调试日志或终端文本到父会话，必须提炼为以下三段式紧凑摘要返回：
   - **通过性总账**：宿主版本、窗口、体检分（各维度分）、冒烟与 typecheck 状态；
   - **阻断项账本**：仅列出 `P0`（致命阻断）与 `P1`（严重缺陷）条目（文件 + 标题 + 根因）；
   - **下一步行动**：具体的修改建议（如 peer 替换、dispose 补充、模板变量清理）。
4. **主 Agent 决策**：主会话上下文保持清爽，主 Agent 仅依据紧凑报告决定修改代码或交付用户。

**寻址用名字或 Session id**：`send_message` 与 `interrupt_agent` 的 `agent` 参数接受名字或 Session id；`list_agents` 返回 `{ name, status, description? }`；启动回执是 `started subagent <name>`。传 `agent_id` 会参数校验失败。子 Agent 回传时把「宿主版本、窗口、分维度分」一并带上，是因为这些字段决定了报告该怎么读——脱离版本与窗口的分数没有意义。

## 第三步：四级严重度标准（Priority Standards）

| 级别 | 定义与影响 | 典型案例 | 处理原则 |
| --- | --- | --- | --- |
| **P0** | **阻断发版/启动失败**：宿主启动必崩溃或类型严重分裂 | 强 import 已废弃包、提示词含已移除 `{{cwd}}` 抛错、核心 Peer 依赖写在 `dependencies` 产生 Vendored 污染 | 立即阻断，必须清零后才能交付 |
| **P1** | **资源泄漏/状态异常**：运行时静默失效或跨会话污染 | `ctx.on` / `setInterval` 缺失清理逻辑、准入账本范围未覆盖目标宿主、高频热路径同步 I/O 阻塞 | 适配阶段应优先修复 |
| **P2** | **架构异味/上下文开销**：不影响当前运行但存在隐患 | 模块顶层定义可变全局集合（Map/Set/数组）重载残留、无字节上限文件读取、工具 Schema 文件偏大 | 建议重构，顺带优化 |
| **P3** | **规范建议/提示**：声明性约定或类型维护 | `import type` 引用即将变动包、工具描述中引用已消亡宿主路径、peer 声明严格 semver 提示 | 人工知悉，按需调整 |

## 常见缺陷与标准修复模式

### 1. 核心 Peer 依赖污染（P0）
- **错误**：`package.json` 的 `dependencies` 里声明了 `"cordis": "^4.0.0"` 或 `"@deepseek-ai/dsh": "^0.2.1"`;
- **修复**：将其移至 `peerDependencies`，并在 `devDependencies` 保留开发类型支持。

### 2. 严格模板变量移除（P0）
- **错误**：系统提示词模板中包含 `{{cwd}}`；
- **修复**：删除模板中的 `{{cwd}}` 子句，直接依赖 DSH 运行时每轮注入的上下文。

### 3. Cordis 生命周期清理（P1）
- **错误**：`ctx.on('chat', handler)` 未保存 dispose 句柄；
- **修复**：改用 `ctx.effect(() => { ctx.on('chat', handler) })` 或在 `ctx.on('dispose', () => { ... })` 中解绑。

### 4. 语言缺失不等于删除（P1，来自生态实证）

- **错误**：写 `if (!name) delete ctx.services[name]` 或把空值当成「没配置」跳过，从而连带丢掉合法的空值配置；
- **机制**：空值与缺失是两件事。上游一个真实事故是工具导出索引式配置块时把空值项丢掉，导致从 CLI 启动编辑器后整条 Git 发现链断掉。本生态里对应的是「`Config` 给了默认值却被当成未声明」「`inject` 空数组与不声明混为一谈」；
- **修复**：要区分 `undefined` 与 `''` / `[]` / `0` / `false`；删除判断用「键是否存在」而不是「值是否真」。

### 5. 注册表按名字写入前先查重（P2）

- **错误**：注册工具、服务、命令、slot 时直接覆盖同名条目；
- **机制**：多数宿主的注册表是后写覆盖先写且不报警，两个插件抢同一个名字时表现为「其中一个静默失效」，排查成本极高。上游多个 Agent 宿主已把这条从「静默覆盖」改成「拒绝重复注册并快速失败」；
- **修复**：注册前查重，冲突时抛明确错误或加命名空间前缀，不要静默覆盖。

### 6. 环境变量擦除按变量组原子处理（P1，本工具自身实录）

- **错误**：按名字过滤环境变量（例如「凡名字含 KEY/SECRET/TOKEN 就删」）却只删了组里的部分成员；
- **机制**：git 的索引式配置是一个**原子组**（`GIT_CONFIG_COUNT` + `GIT_CONFIG_KEY_n` + `GIT_CONFIG_VALUE_n`），缺任一键就整体拒跑并 fatal。宿主的子进程凭证擦除正好会摘掉 `KEY_n`（KEY 三个字母既在 git 配置通道名里、也在密钥字段名里），留下计数与值，于是一切 git 子进程全挂；
- **修复**：擦除逻辑按组原子处理；需要起子进程的一方在**自己的边界**上净化（本工具的做法见 `scripts/lib/proc-env.mjs`），不要假设上游环境一定干净。

### 7. 删路径不要跟随链接（P2，常设规则锚点）

- **错误**：对可能是软链/junction 的路径用 `rmSync(p, { recursive: true })`；
- **机制**：POSIX 上会穿过链接删掉目标内容（纯数据丢失），Windows 上对 junction 抛 `ERR_FS_EISDIR`；
- **修复**：先 `lstatSync().isSymbolicLink()`，链接用 `unlinkSync`（只删链接本身、拒绝真实目录），真实目录才递归删。本工具的实现是 `removeDirSafely`。

## 常设规则从哪读（不复制进技能）

上表第 4/5/7 条不是自己编的，出处是上游仓库 `docs/defensive-patterns/`（五篇：package-surface / general / client-components / conversation-and-session / remote-and-api）。那一层是**不随版本变的硬要求**，`docs/upgrade-guide/` 是**随版本变的破坏性变更**，两者互不覆盖：只扫升级指南会漏掉「从来没变过但插件一直违反」的那一半。

读法：先按上表定位到大致类别，再去对应那一篇核对规则原文、判定条件、边界与例外，**以原文为准**；技能里这几条只是指路牌，不是规则的副本——上游改了原文，这里不该跟着漂移。

## 哪些已经自动化，哪些仍要人看

常设规则那层不再全靠人工。`node scripts/standards-scan.mjs <插件目录>` 做掉了照原文读必然得出同一结论的七条，每条都带 `defensive-patterns` 的原文出处（`--rules` 出完整规则表），确定性项可由 `node scripts/codemod.mjs <插件目录> --apply` 自动重构修补：

| 规则 | 机械判据 | 没查什么 |
| --- | --- | --- |
| `top-level-await` | 缩进为 0 的 `await` | 动态 `import()` 的顶层等待 |
| `loader-entry-shape` | 入口的值导出集合（`export type` 不计） | 导出物是不是「同一个东西的两种写法」 |
| `shared-state-no-owner` | `globalThis._X` 赋值；被导出的模块级 `let`/`var` 在函数里被重新赋值 | 容器被写、但从未被重赋值的一类（写一次的标志位）；判据要求「被导出」，所以只在本模块内共享的那种不算 |
| `cross-package-relative-import` | import 说明符以 `/` 开头，或相对路径解析后跑出包根 | 别名（`@/...`）指向包外——要读 tsconfig 才知道 |
| `lifecycle-unpaired-resource` | 代码区使用了原生 `setInterval` 或 `process.on`，但全模块未见配对的 `clearInterval`/`off` 或 `dispose` 清理 | `ctx.on` 业务事件分发的精细清理时机；注册与注销跨文件（a.ts 注册、b.ts dispose）看不到 |
| `vendor-rescope-unscoped` | `from`/动态 `import()`/`declare module` 的包名命中未 rescope 的裸名清单，或 package.json 依赖键命中同名 | 别名与子路径（`cordis/xxx`）形式；vendored 副本目录里的引用 |
| `waterfall-missing-next` | 只看 `<ctx>.on("<waterfall 事件>", <函数字面量>)`，取该监听器函数体的配对花括号区间（不是字符窗口），区间内无 `next(` 才报 | 第二个实参是具名引用或调用表达式时不判；`next(` 是否真被 `return` 出去、以及 `Promise.all` 里的顺序语义不判 |

**故意没进自动扫描的**：`dispose 必须达到完全停稳`、`在分发器中隔离回调异常`、`slot 注册物是稳定的 function component`、`Store 用法窄而明确`、`Projection 是唯一的读取与计算路径`。这些要判断意图与边界，静态文本判不出可信结论；报错了只会消耗使用者对整个工具的信任。它们留在本车道的表里人工核对。

同一套规则也进了 `plugin-audit` 的第五维（`standards` 分），所以 `run.mjs` 与 `write-gate` 自动带上，不必单独跑。`write-gate` 里它属于**软指标（透传待裁量）**，不是硬门禁——分数低不等于不能发，要人看过才算。
