---
name: quant-tuning-score-dit
description: Aggregate DiT inference outputs into per-dimension VBench metrics via AISBench. Run after the quant-tuning-evaluate DiT workflow produces a directory of mp4s and the user supplies a VBench-1.0-mini JSON + pre-populated cache dir. Single mode (Standard).
license: Apache-2.0
metadata:
  version: 0.1.0
  domain: quantization
  framework: msmodelslim
  protocol: script
  skill_class: tool
  gating:
    model_family: dit
    enabled_by_default: false
    state: experimental
  aliases:
    - dit-score
    - dit-aggregate
    - vbench-evaluate-dit
  keywords:
    - vbench
    - aisbench
---

# Skill: DiT 调优评分（VBench）

对 `quant-tuning-evaluate` DiT 扩展节产出的 `<subdir>/<idx:04d>.mp4` 视频目录打分：通过 AISBench-VBench 1.0 给出逐维度分数 + Quality / Semantic / Total 加权总分；可选与 FP baseline 对比。

## 调用模式（重要）

**本 Skill 是 tool/script，不是 subagent。**

- ✅ 调：`execute python scripts/score.py --infer-outputs ... ...`
- ❌ 不能：`Task(subagent_type="quant-tuning-score-dit", ...)` —— "quant-tuning-score-dit" 是 **skill 标识符**，**不**是 subagent_type，不能塞进 Task 工具。走 Task 会撞「subagent_type 不在允许的清单内」错误。
- 本文档下文里出现的「路由/委派/接手」等措辞是沿用 orchestrator 的术语，意思就是「orchestrator 在合适的时机 `execute` 调本 skill 的脚本」，**不是**真的起一个同名 subagent。

## 调用流程

orchestrator 每轮末按 `model_family=dit` 调本 Skill 的 score.py 脚本时：

```
1. 跑 scripts/check_vbench_cache.py
   ↓ 拿 candidates
   把 candidates 逐字呈现给用户，等用户确认
   ↓ 用户确认路径
2. 读 NPU 卡号（见下方"显卡配置"） → 拼到命令前 → 跑 scripts/score.py ...
   ↓ JSON 输出
3. 把 ok/scores/overall_score 写进 history.yaml
```

**显卡配置（NPU）：** VBench 打分需给 `ais_bench` 子进程指定 NPU 卡号。

- **卡号取自现有流程**：从 orchestrator 的 `device_indices` / `history.yaml` / `run_manifest.json` / 用户对话上下文里拿到当前轮次使用的物理卡号（如 `[0]` → `"0"`）。**不要凭空假设、不要 export 到环境变量里等子进程继承**。
- **直接拼在命令前**（不是 `export`，不是写在脚本头部）：

  ```bash
  ASCEND_RT_VISIBLE_DEVICES=0 python scripts/score.py \
      --infer-outputs ... --full-json-dir ... --vbench-cache-dir ...
  ```

- 单卡优先（一般取 `device_indices` 的第一个值），避免多卡通信开销。
- 如果拿不到卡号，先 `npu-smi info` 查一下，挑一张空闲卡。

**transformers 版本兼容（NPU 场景）：** VBench 打分依赖的 AISBench 链路在 `transformers >= 4.50` 上可能不兼容；建议使用 `< 4.50`（如 `4.42.3`）。

- **打分前**：先检查当前 transformers 版本，若 `>= 4.50` 则临时降到 `4.42.3`（如 `pip install transformers==4.42.3`）。
- **打分后**：切回用户原本的版本（记下切换前的版本号，跑完恢复）。
- **切换失败不勉强**：装不上 / 切不回去都不要阻塞主流程，记一行 warning 后继续；只在真正触发 AISBench 兼容错误时才回头处理。
- 推荐命令顺序：

  ```bash
  ORIG_VER=$(python -c "import transformers; print(transformers.__version__)")
  python -c "from packaging.version import Version; import transformers, sys; sys.exit(0 if Version(transformers.__version__) >= Version('4.50') else 1)" \
    && pip install transformers==4.42.3 || true

  ASCEND_RT_VISIBLE_DEVICES=0 python scripts/score.py ...

  pip install "transformers==${ORIG_VER}" || echo "warn: failed to restore transformers ${ORIG_VER}"
  ```

**禁止跳过 precheck，禁止命中候选后静默选用第一条，禁止 ok=false 后未经授权下载。**

## CLI 契约

orchestrator 调本 skill 时，**通过 `execute` 跑** `scripts/score.py`（脚本形式），例如：

```bash
python scripts/score.py \
    --infer-outputs     {workdir}/infer_outputs/round_N \
    --full-json-dir     <VBench_kmeans_info*.json> \
    --vbench-cache-dir  <用户提供的路径> \
    [--baseline-outputs {workdir}/baseline_outputs/round_N] \
    [--score-dimensions dim1,dim2,...] \
    [--max-num-workers N] \
    [--baseline-tolerance 0.05] \
    [--round N] \
    [--timeout-sec 7200] \
    [--output-json {workdir}/history/scores_round_N.json]
```

输出 shape（msagent-io v1）：

```json
{
  "protocol": "msagent.subagent_io",
  "subagent_type": "quant-tuning-score-dit",
  "status": "ok",
  "output": {
    "ok": true,
    "round": 2,
    "scorer": "vbench",
    "scores": {
      "subject_consistency": 0.842,
      "background_consistency": 0.913,
      "aesthetic_quality": 0.612,
      "motion_smoothness": 0.978
    },
    "quality_score": 76.4,
    "semantic_score": 0.0,
    "overall_score": 61.1,
    "loss_vs_baseline": 1.2,
    "is_satisfied": true,
    "baseline_overall_score": 59.9,
    "duration_sec": 1834.5,
    "commands": [{"name": "vbench_score", "command": "ais_bench ..."}],
    "inference_params": {  // 来自 {infer_outputs}/run_manifest.json（如有）
      "round": 2,
      "vbench_args": ["--task", "t2v-A14B", ...],
      "auto_env_overrides": {...}
    }
  }
}
```

失败时 `status: failed`、`error.code` 是稳定字符串（见 `references/aisbench_vbench.md` 错误码表）。退出码：`ok` → 0；`failed` → 2。

## 实现路径

```
score.py (单进程)
  ├─ patch_config.py     → 改写 AISBench 模板三处变量
  ├─ subprocess:         ais_bench <patched> --mode eval --max-num-workers N
  ├─ 解析 {work_dir}/results/{model_abbr}/vbench_<dim>.json
  ├─ 解析 summary/summary_*.txt 的 vbench_quality / semantic / total
  ├─ 可选: 同样的流程对 --baseline-outputs 再跑一次
  └─ 读 {infer_outputs}/run_manifest.json 填 inference_params
```

**Quality / Semantic / Total 不本地重算**——直接读 AISBench `VBenchSummarizer` 官方值。

## AISBench 输出布局（自动识别）

不同 AISBench 版本 / 配置会把结果写到不同的目录布局，score.py 通过 `_resolve_output_dirs(work_dir)` 自动探测，按以下顺序匹配：

| 优先级 | 布局 | 触发条件 |
|---|---|---|
| 1 | `{work_dir}/results/` + `{work_dir}/summary/` | 旧版配置或显式把 `output_dir` 重定向到 work 根 |
| 2 | `{work_dir}/outputs/default/<latest-ts>/{results,summary}/` | AISBench 默认配置；多次跑会累积多个时间戳目录，**取最新** |
| ✗ | — | 都不存在 → `error.code = "AISBENCH_NO_OUTPUT"` |

两种布局并存时走优先级 1（路径更短、好排障）。回归覆盖见 `scripts/test_score_paths.py`（6 个用例）。

## 约束

- **不下载权重**：错误信息引导 orchestrator 跑 `check_vbench_cache.py` 把候选呈现给用户
- **环境错误可定位**：stderr 被分类为 `ENV_DECORD_MISSING` / `ENV_DETECTRON2_MISSING` / `ENV_TORCH_MISSING` / `ENV_CUDA_MISMATCH` 等，每条都附官方 doc URL：`https://github.com/AISBench/benchmark/blob/master/docs/source_zh_cn/extended_benchmark/lmm_generate/vbench.md`
- **错误即停**：评分失败立即回传 `failed`
- **不修改 AISBench 上游**：纯消费者
- **错误码稳定**：错误码字符串不能改

## 参考

- 错误码表 / KI 速查：`references/aisbench_vbench.md`
- 缓存预检：`scripts/check_vbench_cache.py`
- AISBench VBench 官方文档：<https://github.com/AISBench/benchmark/blob/master/docs/source_zh_cn/extended_benchmark/lmm_generate/vbench.md>
- Orchestrator 路由：`quantization-accuracy-tuning-orchestrator/SKILL.md`