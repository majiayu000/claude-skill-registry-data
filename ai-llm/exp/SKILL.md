---
name: exp
description: "跑实验并记录 provenance：先写假设和成功判据，跑时记录 git hash、完整 resolved config 和 seed，跑完把结论写回 research-log.md 并标 [AI-DRAFT] 与 [source: run_id]。任何要跑训练/评测/对比的场景都走这里。"
argument-hint: "[实验描述]"
allowed-tools: Read, Write, Edit, Glob, Grep, Task, Bash
---

# 跑实验并记录 provenance

实验：$ARGUMENTS

> 为什么 `allowed-tools` 里是完整的 `Bash`：本 skill 要**真的启动训练/评测**，长任务还要后台跑、
> 查日志，命令形态事先不可枚举。`allowed-tools` 是「本轮免批准的范围」，**不构成硬限制**，
> 收窄它只会让每一步都卡权限确认，并不会真的挡住什么。真正的护栏在
> `.claude/hooks/protect_paths.py` 和下面的硬约束里。

## 第 1 步 跑之前：先写判据

**先写判据再跑，是这个 skill 存在的全部理由。** 先跑再解释，人一定会把任何结果讲成故事。

run_id 格式固定 `YYYYMMDD-<slug>`（slug 小写英文加短横线），例如 `20260722-attn-cache-seed1`。

在 `research-log.md` **末尾追加**一节（此时实验还没开始）。字段顺序照抄，不要改名：

```text
## 2026-07-22  run_id: 20260722-<slug>
- 假设: <一句话，可证伪。例：把 lr 降到 1e-4 能让 loss 在 5k step 内不再发散>
- 成功判据: <具体数值/条件。例：step 5000 时 train_loss < 2.0 且无 NaN>
- 失败判据: <什么结果算假设被证伪>
- 对照: <baseline 是哪个 run_id；没有就写「无对照，仅探索」>
- git hash: <跑之前留空，第 2 步填>
- 结果: <跑完填>
- 结论: <跑完填>
```

判据写不出具体数字，就说明这个实验还没想清楚——先想清楚再跑。

## 第 2 步 跑之前：检查可复现性

```bash
git status --short
git rev-parse HEAD
```

工作区不干净（`git status` 有输出）时，**先警告用户**：

> 工作区有未提交改动，本次结果将无法复现（跑的代码和任何 commit 都不对应）。
> 建议先 commit 再跑。要继续吗？

用户坚持就继续，但必须在 run 记录里标 `dirty: true` 并列出脏文件。

## 第 3 步 跑：把 provenance 落到输出目录

产物目录一律是 `experiments/`（不要用 `results/` `runs/` `outputs/`），每个 run 一个独立目录
`experiments/<run_id>/`。

**只写新建的 run 目录，绝不修改已有 run。** `protect_paths.py` 对 `experiments/**` 的规则是
「文件已存在才阻断，新建放行」，所以往新 run 目录里落 provenance 是允许的；一旦你去写一个
已经存在的文件，hook 会直接 exit 2 挡下来——那不是配置错误，那是你走错了路，换个新 run_id。

跑之前先往新目录里写：

- `git rev-parse HEAD` 的结果，以及是否 dirty
- **完整的 resolved config** —— 展开之后的最终配置内容，不是 config 文件路径，
  也不是命令行片段。路径会随代码变，展开后的配置才是这次真正跑的东西。
- seed（所有相关的：数据、初始化、框架全局）
- 完整启动命令
- 环境：`python3 --version`，关键库版本

然后启动。长任务用后台运行并说明怎么看日志，不要傻等。

## 第 4 步 跑完：派 result-analyst 读日志，再写结论

**派 `result-analyst` subagent 去读日志和输出文件，不要自己读。** 训练日志动辄几千行，
拉进主 context 就再也清不掉了；而且它是 fresh eyes，不知道你希望看到什么结果。
派给它的 prompt 要写明：run 目录路径、成功判据原文、要对比的 baseline run_id（如果有）。
要求它回报：指标名 = 值 + **每个数字来自哪个文件**，以及判据逐条「达成 / 未达成」。

拿到它的回报后，把结论补进 `research-log.md` 里**本次那一节**（只补自己这节的空字段，
不碰任何别的条目）：

```text
- git hash: <hash>（dirty: false；dirty 时列出脏文件）
- 结果: <指标名 = 值，出处 experiments/<run_id>/metrics.json>
- 结论: [AI-DRAFT] <假设成立 / 被证伪 / 判据外的意外现象> [source: 20260722-<slug>]
```

然后提示用户：

> 以上结论标的是 `[AI-DRAFT]`。你人工核过原始输出之后，把它改成 `[HUMAN-VERIFIED]`。

## 硬约束（违反即本次实验作废）

1. **不得口算或估算任何指标。** 不许从日志里心算平均值、不许目测曲线报数字、
   不许把「大概 0.85」写成 0.85。
2. **不得报告没有落盘文件支撑的数值。** 每个数字要能指到 `experiments/<run_id>/` 下的某个文件。
3. **不得修改或删除 `research-log.md` 里已有的条目**，只能 append。写错了就新增一条更正，
   注明更正的是哪条。
4. **不得复用别的 run 的输出目录。** 覆盖等于毁掉那次实验的证据。
5. **不得在工作区脏的情况下静默开跑**，必须先警告。
6. **不得把 `[AI-DRAFT]` 自行升级成 `[HUMAN-VERIFIED]`。** 只有用户能升。

### 需要一个还没有的指标时怎么办（合法路径）

不要绕过约束 1 自己算。正确做法：

1. 写一个脚本来算，放 `explorations/`（沙箱目录，随便试）。
2. 脚本要能从 `experiments/<run_id>/` 的产物读入、把结果写成文件。
3. 脚本进版本控制（`git add`），这样这个数字以后可以被重新算一遍。
4. 跑脚本，报告它输出的文件里的数字。

脚本稳定下来、要反复用了，再从 `explorations/` 提升为正式脚本。
`experiments/` 里**已有的东西是只读的**（新 run 目录可以建、可以落 provenance），
任何时候都不要往里手写数字——数字只能由脚本产生。
