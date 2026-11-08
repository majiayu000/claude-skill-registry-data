---
name: verl-omni-msprobe-dump
description: >
  为 verl-omni 接入或修复 MSProbe 训推一致性采集，生成打点代码、样本关联日志和诊断启动脚本。
  用于 diffusion/omni 的 rollout 与 actor 数据采集、dump 缺失或配对失败；不负责精度根因分析。
---

# verl-omni 训推一致性采集

交付能追溯到同一样本、同一计算片段的两侧 dump，以及输入和权重的可比依据。

## 工作流程

### 1. 定位运行链路

读取用户启动脚本、配置和实际加载的源码，沿入口追到执行模型的 rollout worker 与 actor engine。
涉及继承或外部引擎时继续追踪依赖源码；以下 reference 中的符号仅作搜索起点。

| 本次采集路径 | 按需读取 |
| --- | --- |
| diffusion 去噪前向 | [diffusion.md](references/diffusion.md) |
| omni / AR 的指定 stage prefill | [omni.md](references/omni.md) |

### 2. 确定配对依据

追踪一条样本：请求 ID → rollout 输出 → 队列 / batch 转换 → actor micro-batch。
确认 ID 映射、输入来源、权重版本及 timestep / token 区间、分支和样本布局。
输入未复用或不等价时，明确可比范围；需要重放的路径见对应 reference。

### 3. 接入采集

按 [公共接入约定](references/implementation.md) 实现依赖导入、单 global step 窗口、debugger 生命周期和关联日志。
按当前代码确认两侧 global step 的来源、含义和实际类型；解包并与环境变量统一为整数后比较，用两侧实际输入验证窗口命中。
在实际模型前向处打点；已有集成优先复用，不能仅包裹请求提交层。

采集关闭时保持原执行路径。开发环境缺少 msprobe 不阻塞接入；实际采集初始化失败或窗口未命中须明确报告。

### 4. 生成诊断脚本

生成调用用户原脚本的短 wrapper，只追加环境变量和采集参数，不复制原脚本全文。
先检查最终命令的 `"$@"` 透传，再确认 override 实际生效。
默认限制单个 global step、关闭训练前 validation、每卡 micro-batch=1、引擎请求并发=1。
diffusion 默认必须将两侧 guidance 收敛到同一个 cond 单分支，并验证实际前向布局；具体规则见 [分支收敛](references/diffusion.md#分支收敛)。
全局 batch 与采样数量取当前 recipe 的最小合法组合，保留模型、数据和并行配置。

参数规则与 wrapper 示例见 [共用采集参数](references/implementation.md#共用采集参数) 和 [诊断启动脚本](references/implementation.md#诊断启动脚本)。

### 5. 验证采集

执行修改文件的语法检查和 wrapper 的 `bash -n`；环境允许时运行一次短采集：

- 最终配置与 worker 收到的参数一致，两侧均实际执行 start / stop 且目标模块 dump 非空；任一侧漏采都须修复并重新采集，不能交付单侧产物作为成功结果。
- diffusion 展示两侧实际分支名称、调用次数和输入 batch 布局；多分支聚合统计与单分支统计不能作为可比产物交付。
- 用样本身份、计算片段和权重版本定位一对产物，核对输入及布局；不按目录顺序或本地 step 配对。
- validation、warmup、dummy 和其他 global step 不混入有效配对；重复调用和多进程产物可区分。
- 关闭采集后恢复原执行路径。没有运行条件时，明确仅完成静态检查。

statistics 用于统计筛查；逐元素核验需要 tensor。详细验收见 [配置与验收](references/implementation.md#配置与验收)。

## 交付内容

- 修改文件及打点位置、诊断脚本路径、覆盖参数、开启 / 关闭方式。
- 已执行的检查、未验证项和运行环境缺失的依赖。
- 完成采集时提供一对 dump 路径、关联日志与配对依据；注明输入、分片或模块结构造成的可比范围限制。
