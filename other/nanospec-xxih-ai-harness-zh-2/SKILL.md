---
name: nanospec
description: 'NanoSpec 的核心是 AI 工作中间文档的目录规范与 align 纠偏机制；可独立配合其他 plan/research/execute 类 skill 使用，也可在需要时路由为完整的 spec-driven workflow。'
---

# NanoSpec

## 目标

先提供一套稳定的 AI 工作中间文档目录规范，让 plan、research、execute 等其他 skill 也能在同一任务容器里协作；当用户需要时，再由这个 skill 路由并补齐完整的 NanoSpec spec-driven workflow。

这个 skill 的默认定位不是“必须从 init 开始跑完整流程”，而是：

1. 约束中间文档落盘位置、命名和读取顺序。
2. 在出现偏差、变更、缺失、歧义时，用 align 作为统一纠偏入口。
3. 在用户明确要求或上下文显示需要时，再承接 init / clarify / spec / plan / execute / accept / summary / onboard / run。

## 何时使用

- 你想给当前任务建立稳定的中间文档目录，而不是把计划和决策散落在对话里
- 任务已经进入 plan / research / execute，但缺少统一的任务容器和回写规则
- 任务里出现范围变化、需求偏差或临时决策，需要用 `alignment.md` 做统一纠偏
- 你想按 `/init`、`/plan`、`/execute`、`/align` 这类阶段入口推进，而不是每次重新描述流程
- 你明确希望由 NanoSpec 续跑一套完整的 spec-driven workflow

不适用：

- 只是一次性极小改动，不需要任务容器或中间文档
- 用户只要最终答案，不希望保留任何项目内过程产物

## 产物

每次使用本 skill，默认产出以下最小集合：

1. 任务容器
   - `nanospec/<YYYYMMDD-task-name>/`
   - 需要时可同步维护 `.nanospec/.current`
2. 对齐记录
   - 出现偏差、变更、缺失、歧义时写入 `alignment.md`
3. 共享工作面
   - `outputs/1-spec.md`
   - `outputs/2-plan.md`
   - `outputs/3-tasks.md`
4. 辅助资料
   - `assets/` 下的研究、截图、日志、草图和补充文档

默认要求：

- 没有任务容器时，先创建容器，再进入具体阶段
- 发生口径变化时，不能只改对话，必须回写 `alignment.md` 和受影响产物
- `outputs/3-tasks.md` 是跨 skill 的共享执行面，不是 NanoSpec 私有日志

## 任务目录结构

```text
project-root/
├── .nanospec/
│   └── .current                  # 当前任务名，可选
└── nanospec/
    └── <YYYYMMDD-task-name>/
        ├── brief.md              # 简述需求，和 prd.md 二选一或并存
        ├── prd.md                # 更正式的需求文档，可选
        ├── alignment.md          # 对齐记录，可按需创建
        ├── assets/
        │   ├── README.md         # 可选，记录放置建议
        │   └── ...               # 资料、截图、草图、补充文档
        └── outputs/
            ├── 1-spec.md
            ├── 2-plan.md
            ├── 3-tasks.md
            ├── acceptance.md     # 可选，验收阶段生成
            └── summary.md        # 可选，总结阶段生成
```

- 仓库里没有 `nanospec` CLI 时，也按上面的结构直接创建和维护文件。
- 新建任务目录名必须使用 `YYYYMMDD-任务主题` 格式，例如 `20260315-skills跨工具安装指南`。
- `.nanospec/.current` 只是任务指针，不是 skill 生效的前置条件。
- 用户完全可以只采用这套目录规范，而不使用 NanoSpec 的其他阶段能力。
- 简单任务可以把截图、日志、接口样例、参考链接直接平铺在 `assets/` 下。
- 只有材料明显变多、类型混杂时，才建议拆成 `research/`、`bugs/`、`api/`、`data/`、`ui/`、`references/` 等子目录。
- `alignment.md` 不需要预创建；只有真正发生偏差、变更、缺失或歧义时，再由 `/align` 或其他阶段补写。

## 工作流

1. 优先从用户显式输入解析任务目录，其次读取 `.nanospec/.current`；仍无法定位时，按 `YYYYMMDD-任务主题` 格式在 `nanospec/` 下手动创建目录。
2. 按顺序读取 `alignment.md`、`brief.md`/`prd.md`、`assets/*` 与工作区现状。
3. 只执行本次请求真正需要的阶段；如果当前任务来自其他 skill 的 plan、research、execute 指令，也继续沿用这套目录规范。
4. 只要出现需求变化、实现偏差或临时决策，先执行 align：更新 `alignment.md`，同步所有受影响产物，再继续其他阶段或其他 skill。
5. align 产生的后续动作必须回写到 `outputs/3-tasks.md`，不能只停留在对话或 `alignment.md`。
6. 每完成一个可执行事项，立即更新 `outputs/3-tasks.md`。
7. 如果用户要求 `/run`，或明确希望由 NanoSpec 接管完整流程，再按缺失阶段自动续跑完整 workflow。

## 协作边界

- 这个 skill 可以只提供“目录规范 + align”，把 spec、plan、research、execute 交给别的 skill 完成。
- 当其他 skill 采用“先 plan 后 xxx”模式时，只要装载了本 skill，就应按本目录规范读写中间文档。
- `outputs/2-plan.md` 和 `outputs/3-tasks.md` 不是 NanoSpec 私有产物；它们也是跨 skill 协作时的共享工作面。
- align 是核心能力，不依赖完整 workflow 才能使用。
- 完整的 spec-driven workflow 是可选路由，不是使用本 skill 的前提条件。

## Align 机制

align 不是一个孤立阶段，而是贯穿整个任务生命周期的变更传播机制。参考领域 `_AGENTS.md` 中的通用规则，它的核心循环是：

1. 发现问题。
2. 记录到 `alignment.md`。
3. 同步受影响产物。
4. 回写新的执行动作到 `outputs/3-tasks.md`。

触发 align 的时机不限于 `/align`：

- 在 spec 阶段发现需求冲突、歧义、缺失时，要立即 align。
- 在 plan 阶段发现口径不一致、方案风险时，要立即 align。
- 在 execute 阶段发现实现偏差、阻塞问题时，要立即 align。
- 在 accept 或 summary 阶段发现遗漏决策点时，也要立即 align。

align 记录应使用统一标签：`[偏差] [变更] [缺失] [歧义] [冲突]`。需要用户确认时，再追加 `` `⏳ 待确认` ``。

只要口径发生变化，就必须同步更新受影响的 `outputs/1-spec.md`、`outputs/2-plan.md`、`outputs/3-tasks.md`，以及存在时的 `acceptance.md`。不能只改 `alignment.md`，也不能只留在对话里。

## 路由方式

使用这个 skill 时，可以直接用 `/xxx` 把请求路由到对应阶段，而不必先声明“进入某个内部模式”。

- `/init`：初始化任务目录或建立当前任务上下文。
- `/clarify`：补需求澄清。
- `/spec` 或 `/1-spec`：产出规格说明。
- `/plan` 或 `/2-plan`：产出方案与任务拆解。
- `/execute` 或 `/3-execute`：按任务清单推进实现。
- `/align`：执行对齐纠偏，并传播变更。
- `/accept`：生成或更新验收产物。
- `/summary`：沉淀总结。
- `/onboard`：进入带教学解释的引导模式。
- `/run`：让 NanoSpec 按缺失阶段续跑完整 workflow。

如果外部工具或团队约定使用的是带前缀命令，例如 `/spec.align`、`/spec.2-plan`，也可以继续使用；本 skill 的要求是“按当前意图路由到对应 reference 和目录规范”，而不是强绑定某一种命名形式。

## 辅助脚本

skill 目录内自带 `scripts/create_task_skeleton.py`，用于快速创建符合约定的任务骨架。优先使用 Python 标准库脚本，是为了比 shell 更容易跨不同 agent 环境复用：

```bash
python3 scripts/create_task_skeleton.py "支付回调重试"
python3 scripts/create_task_skeleton.py "20260315-支付回调重试" --set-current
```

脚本会创建：

- `nanospec/<YYYYMMDD-task-name>/brief.md`
- `nanospec/<YYYYMMDD-task-name>/assets/README.md`
- `nanospec/<YYYYMMDD-task-name>/outputs/1-spec.md`
- `nanospec/<YYYYMMDD-task-name>/outputs/2-plan.md`
- `nanospec/<YYYYMMDD-task-name>/outputs/3-tasks.md`

如果传入的是不带日期前缀的主题名，脚本会自动补上当天的 `YYYYMMDD-` 前缀；传入 `--set-current` 时，会同步写入 `.nanospec/.current`。

## 渐进加载

只加载当前意图需要的参考文件：

- 创建或初始化任务：`references/init.md`
- 快速续跑全流程：`references/run.md`
- 需求澄清：`references/clarify.md`
- 规格产出：`references/spec.md`
- 对齐更新：`references/align.md`
- 规划与任务拆解：`references/plan.md`
- 任务执行：`references/execute.md`
- 验收校验：`references/accept.md`
- 交付总结：`references/summary.md`
- 新人上手：`references/onboard.md`

## 全局规则

- align 不是可选补记；出现偏差或变更时，继续 spec / plan / execute 之前必须先完成 align 回写。
- 当其他 plan / research / execute skill 已经装载本 skill 时，也要沿用同样的目录规范与 align 约束。
- 使用 `/xxx` 路由阶段时，也必须遵守同一套目录规范、align 机制与回写要求。
- 需求变化统一记录到 `alignment.md`，并使用标签：`[偏差] [变更] [缺失] [歧义] [冲突]`。
- 只有真正阻塞推进的确认项，才使用 `` `⏳ 待确认` ``。
- 不要把后续行动只留在对话里，必须回写到 `outputs/3-tasks.md`。
- `outputs/3-tasks.md` 只跟踪交付动作与状态，不记录 commit hash、提交信息或“补任务日志”这类 git 元信息。
- 除非用户明确要求调用 CLI，否则不要把 `nanospec init`、`nanospec new`、`nanospec status`、`nanospec switch` 当成前置步骤。
- 保持现有文件语言和风格，除非用户明确要求调整。
