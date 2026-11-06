---
name: science-experiment-runbook
description: Use when turning an approved plan into an actual run — when the design and sample size are settled and someone needs to produce data, execute code, or reproduce a result; when a run must be recordable (inputs, outputs, environment, seed) so that six months later the numbers in the paper can be traced back; when a result cannot be reproduced and the difference has to be explained rather than waved away; also use when deciding where raw data, analysis code and generated artifacts belong.
---

# 从方案到一次可复现的执行

## 这一层要守住的三件事

1. **原始数据只进 `data/`，只读。**
   清洗结果放 `data/clean/`，分析产物放 `experiments/<slug>/<runId>/`。
   一旦在原始文件上直接改，你永远回不到采集当天的状态——而审稿人问的第一个问题往往就是那个状态。
2. **每次执行都要能被别人重跑。**
   `science_exp_run` 记的是：脚本内容指纹、输入文件 sha256、输出文件 sha256、
   Python 与关键库版本、seed、是否允许网络。缺任何一项，这次执行就只是"你跑过一次"。
3. **Python 层默认无网。**
   数据下载在采集阶段做完，分析阶段不该联网。要联网就显式 `network: true`，
   记录里会写明——这是给自己留的证据，不是给别人看的仪式。

## 顺序

```
science_study_coach { projectId }             ← 先确认 S2/S3 的门过了
science_exp_plan  { projectId, effect: … }    ← 样本量与前置条件（若还没做）
把数据放进 data/
写 code/run.py                                ← 一个脚本一件事，参数从 argv 进来
science_exp_run   { projectId, slug, script: 'code/run.py', inputs: ['data/raw.csv'], seed: 42 }
science_exp_query { projectId, what: 'runs' } ← 确认状态、产物、耗时
```

## `science_exp_run` 的字段怎么填

| 字段 | 什么时候用 | 坑 |
| --- | --- | --- |
| `script` | 已有脚本 | 路径必须在课题目录内；`../../x.py` 会被拒 |
| `code` | 一次性验证 / 小实验 | 会写成 run 目录里的 `run.py`，同样留痕 |
| `inputs` | 有输入文件 | 相对课题根；文件不存在直接报错，不静默跳过 |
| `seed` | 任何有随机性的分析 | 写进 `seed.txt` 并导出 `DSH_SEED`；不传就用默认值并记录下来 |
| `network` | 需要下载/调用 API | 默认 `false`。Python 层会被 hook 拦住；`curl` 子进程拦不住，这一点要在记录里自己注意 |
| `timeoutMs` | 长任务 | 超时按失败记，不会假装成功 |

## 失败了怎么办

失败的执行**也进溯源链**，这是刻意的：一份只记录成功的历史没有诊断价值。

1. 先读 `stderrTail` 和 run 目录里的 `stderr.log`。
2. 分类：代码错（改脚本重跑）／数据错（回去看采集）／环境错（`probeEnv` 对比版本）／超时（拆任务）。
3. **不要**为了让结果出来而降低检验标准、删样本、换主结局。那一步一旦迈出去，后面所有数字都要重做。

## 复现性检查（交给别人之前）

- 同一 seed 跑两次，输出文件的 sha256 应完全一致。不一致就说明有未受控的随机源（时间、字典序、并行度、浮点归约顺序）。
- `env/env.json` 里的版本与当前环境一致；不一致时先说清差异，再谈结果。
- `science_provenance { projectId }` 链完整：`verified: true`，没有 `hash-mismatch`。
  链断了不是"系统问题"，是有人改过库——先查清再往下写。

## 常见错误

- 在 `code/` 里 `open('../data/raw.csv')` 然后就地覆盖 → 原始数据永久丢失。
- 用 notebook 跑完把结果数字抄进论文，却没记录那次执行 → 数字无法回溯。
- 把中间产物（模型、缓存）提交进 `figures/` → 目录语义混乱，别人找不到真图。
- 只在本机能跑，没锁版本 → 换台机器结论就变，且无法判断是代码还是环境。
