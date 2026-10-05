---
name: spec-driven
description: "给任务建立统一的 spec-driven 工作目录，约束共享工作面和 align 纠偏机制，不内置阶段路由。"
---

# Spec-Driven

## 目标

给当前任务建立一套统一的工作目录，让 plan、research、execute、review 等其他 skill 能在同一套中间文档里协作，并把 `alignment.md` 作为统一的变更传播入口。

这里不负责内置流程阶段，也不提供 `init`、`clarify`、`spec`、`plan`、`execute`、`accept`、`summary`、`onboard`、`run` 这类命令式入口。使用时只解决三件事：

1. 中间文档应该放在哪。
2. 其他 skill 应该按什么顺序读取和回写这些文档。
3. 出现偏差、变更、缺失、歧义时，如何通过 align 统一纠偏。

## 何时使用

- 你想给当前任务建立稳定的中间文档容器，但不想绑定一套内置阶段流程
- 多个 skill 会协作推进同一个任务，需要共享 `spec`、`plan`、`tasks` 和 `alignment` 文件
- 任务过程中经常出现范围变化、决策变更或实现偏差，需要一个统一的变更传播机制
- 你想保留 spec-driven 的工作面，但把具体阶段执行交给其他 skill

不适用：

- 只是一次性极小改动，不需要任务容器或过程文档
- 你需要的是一套可直接路由的完整 workflow，而不是纯目录规范

## 产物

每次使用本 skill，默认产出以下最小集合：

1. 任务容器
   - `nanospec/<YYYYMMDD-task-name>/`
   - 需要时可维护 `.nanospec/.current`
2. 对齐记录
   - `alignment.md`
3. 共享工作面
   - `outputs/1-spec.md`
   - `outputs/2-plan.md`
   - `outputs/3-tasks.md`
4. 辅助资料
   - `assets/` 下的研究、截图、日志、草图和补充文档

默认要求：

- 没有任务容器时，先创建容器，再交给其他 skill 回写内容
- 发生口径变化时，不能只改对话，必须回写 `alignment.md` 和受影响产物
- `outputs/3-tasks.md` 是共享执行面，不是某个单独 skill 的私有日志

## 任务目录结构

```text
project-root/
├── .nanospec/
│   └── .current
└── nanospec/
    └── <YYYYMMDD-task-name>/
        ├── brief.md
        ├── prd.md
        ├── alignment.md
        ├── assets/
        │   ├── README.md
        │   └── ...
        └── outputs/
            ├── 1-spec.md
            ├── 2-plan.md
            ├── 3-tasks.md
            ├── acceptance.md
            └── summary.md
```

- `.nanospec/.current` 只是任务指针，不是生效前置条件。
- 没有 CLI 时，也按这套结构直接创建和维护文件。
- 简单任务可以把资料直接平铺在 `assets/` 下；只有材料变多时，才拆子目录。
- `alignment.md` 不需要预创建；只有真正出现偏差、变更、缺失或歧义时，再补写。

## 工作流

1. 优先从用户显式输入定位任务目录；如果没有，就读取 `.nanospec/.current`；仍无法定位时，再手动创建 `nanospec/<YYYYMMDD-task-name>/`。
2. 按顺序读取 `alignment.md`、`brief.md`/`prd.md`、`outputs/*`、`assets/*` 与工作区现状。
3. 让其他 skill 在同一个任务容器里继续工作，而不是各自新建平行记录。
4. 只要出现需求变化、实现偏差或临时决策，先执行 align：更新 `alignment.md`，同步所有受影响产物，再继续后续工作。
5. align 产生的后续动作必须回写到 `outputs/3-tasks.md`，不能只停留在对话或 `alignment.md`。
6. 每完成一个可执行事项，立即更新 `outputs/3-tasks.md`。

## 协作边界

- 这里只提供“目录规范 + align”，不接管完整阶段流程。
- 具体的 spec、plan、research、execute、accept、summary 由其他 skill 决定如何产出。
- 当其他 skill 在同一任务上协作时，都应按本目录规范读写中间文档。
- `outputs/1-spec.md`、`outputs/2-plan.md`、`outputs/3-tasks.md` 是跨 skill 协作时的共享工作面。

## Align 机制

align 是贯穿整个任务生命周期的变更传播机制。核心循环固定为：

1. 发现问题。
2. 记录到 `alignment.md`。
3. 同步受影响产物。
4. 回写新的执行动作到 `outputs/3-tasks.md`。

触发时机包括但不限于：

- 需求冲突、歧义、缺失
- 方案口径变化
- 实现偏差、阻塞问题
- 验收或总结阶段补发现的遗漏决策

align 记录应使用统一标签：`[偏差] [变更] [缺失] [歧义] [冲突]`。需要用户确认时，再追加 `` `⏳ 待确认` ``。

只要口径发生变化，就必须同步更新受影响的 `outputs/1-spec.md`、`outputs/2-plan.md`、`outputs/3-tasks.md`，以及存在时的 `acceptance.md` 和 `summary.md`。不能只改 `alignment.md`，也不能只留在对话里。

## 全局规则

- align 不是可选补记；出现偏差或变更时，继续其他工作前必须先完成 align 回写。
- 只要其他 skill 继续推进同一任务，也要沿用同样的目录规范与 align 约束。
- 不要把后续行动只留在对话里，必须回写到 `outputs/3-tasks.md`。
- `outputs/3-tasks.md` 只跟踪交付动作与状态，不记录 commit hash、提交信息或“补任务日志”这类 git 元信息。
- 除非用户明确要求调用 CLI，否则不要把 `nanospec` 命令当成前置步骤。
- 保持现有文件语言和风格，除非用户明确要求调整。
