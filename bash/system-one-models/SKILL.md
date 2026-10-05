---
name: system-one-models
description: 在本机部署、选型并验证 System One 决策模型栈（Laya 421M 非自回归决策模型 + 书生·明决 Intern-Decision 2B/0.8B/4B）的完整执行手册。当需要跑"状态+结构化问题 → 带校准概率的决策"（工单分诊、部门路由、风险评估、转人工判断、guardrail 打分）、或部署/排查 Laya 与 Intern-Decision 时使用。含实测延迟、选型档位、行为差异与全部踩坑点。
metadata:
  version: "1.0.0"
  date: "2026-09-29"
  measured_on: "WSL2 Arch / Ryzen 9 7940HS / RTX 4070 Laptop 8G / driver 616.56"
---

# System One 决策模型栈（Laya + 书生·明决 Intern-Decision）

两类模型解决同一个问题：给一段 **state**（文本/JSON/工单）和若干 **typed questions**，
一次前向返回每个字段的**带校准概率的答案**。不要用 LLM 生成再解析，这两个都是判别式评分模型。

- **Intern-Decision (ID)**：书生·明决，Qwen3.5 混合线性注意力底座（含视觉塔），
  一次前向对每个 `<decision>` 标记处的候选符号打分。需要 `transformers==5.14.1`（内含 `Qwen3_5ForConditionalGeneration`）。
- **Laya**：421M ModernBERT，非自回归，RLCD 训练，单次前向 ~35-50ms（GPU）。

**实测数据写在本文件里，不要引用官方数字当本机预期。**

---

## 1. 硬件定档（先探测，再选档）

```bash
/usr/lib/wsl/lib/nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv   # WSL2 里 nvidia-smi 常不在 PATH
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits                # 原生 Linux
```

| 探测结果 | 选档 |
|---|---|
| 独显 ≥10 GB | ID-4B（最高校准质量）+ Laya |
| 独显 ≥6 GB | **ID-2B** + Laya（本机档位） |
| 独显 3–6 GB | ID-0.8B + Laya |
| 无独显 / 纯 CPU | 只装 Laya；要更高质量再加 ID-0.8B |

⚠️ **按显存总量定档，但要按"可用显存"复核**：WSL2 下 `memory.total` 是整卡，
而 Windows 桌面会长期占走 1–5 GB。本机 8 GB 卡实测只余 3.0 GB 时 ID-2B 仍能跑
（峰值 4.72 GB），因为 Windows 侧会释放——但若 `memory.free` 长期 <4.5 GB 且加载 OOM，
直接降到 ID-0.8B，别硬撑。

Windows 机器一律在 WSL2 里做（原生 Windows 折腾 torch/triton 不值），路径用 Linux 侧。

---

## 2. 安装

工作根目录（本机实际使用）：`/home/po/s1`。仓库里 `scripts/bootstrap.sh` 全自动做完下面全部步骤：

```bash
bash scripts/bootstrap.sh ~/s1            # 自动探测档位
bash scripts/bootstrap.sh ~/s1 2b cu128   # 或显式指定
```

手动等价步骤：

```bash
uv venv ~/s1/venv --python 3.12.12        # 绝不动系统 Python（本机系统 Python 是 3.14.7）
uv pip install --python ~/s1/venv/bin/python torch==2.9.1 torchvision==0.24.1 \
   --index-url https://download.pytorch.org/whl/cu128
uv pip install --python ~/s1/venv/bin/python transformers==5.14.1 Pillow einops packaging numpy safetensors huggingface_hub laya
```

**只用 Python 3.12**。causal-conv1d 的预编译轮子只发到 cp313，3.14 上必然回落慢路径。

### GPU 才装的两件套

```bash
# ① FLA 必须 git 装：PyPI 的 wheel 是残缺包（缺 __init__ / modules）
uv pip install --no-deps 'flash-linear-attention @ git+https://github.com/fla-org/flash-linear-attention@v0.4.2'

# ② causal-conv1d：PyPI 只有 sdist，编译要 nvcc；本机没装 CUDA toolkit → 用官方预编译轮子
python scripts/pick_causal_conv1d.py     # 自动按 torch/cu/ABI/py 版本挑轮子并安装
```

本机装成的确切断子（cp312 / cu12 / torch2.9 / cxx11abiTRUE）：
```
causal_conv1d-1.7.0+cu12torch2.9cxx11abiTRUE-cp312-cp312-linux_x86_64.whl
https://github.com/Dao-AILab/causal-conv1d/releases/download/v1.7.0/<上面那个文件名>
```
torch 必须钉 `2.9.1`：轮子的 ABI 名里带 torch 版本，装别的 torch 就对不上（可用
`torch._C._GLIBCXX_USE_CXX11_ABI` 核对，本机是 `True`）。

### 下模型

```bash
python scripts/dl_model.py internlm/Intern-Decision-2B ~/s1/Intern-Decision-2B
python scripts/dl_model.py convaiinnovations/laya    ~/s1/laya
```

- **必须用 `local_dir` 且是真名目录**（`~/s1/Intern-Decision-2B`）。落 HF cache 会变 symlink，
  `inference.py` 按自身路径定位权重，运行时会挂。
- `HF_HUB_DISABLE_XET=1`（不禁 xet 会 401）。
- ⚠️ **本机不要设 `HF_ENDPOINT=https://hf-mirror.com`**：该镜像现在对 `/resolve/` 返回
  **308 跳回 huggingface.co**，huggingface_hub 随即抛
  `FileMetadataError: Distant resource does not seem to be on huggingface.co`。
  走 clash 代理直连 huggingface.co 正常（本机实测 ~5-9 MB/s）。
  `scripts/dl_model.py` 里已写成直连；只有你确认镜像可用时才加 `HF_ENDPOINT`。

实测下载量：ID-2B 4.2 GB（language 3.76 GB + vision 0.61 GB + projector 50 MB），
laya 全仓 2.3 GB（含 multilingual 与 typed-decisions 子目录）。

---

## 3. 验证（跑通才算完）

```bash
bash scripts/verify.sh ~/s1        # 一键：依赖自检 + 各引擎 20 次计时
```

单引擎：

```python
# ID：模型目录里带 inference.py，先把它加进 sys.path 或 cd 过去
import sys; sys.path.insert(0, "/home/po/s1/Intern-Decision-2B")
from inference import DecisionEngine
eng = DecisionEngine(checkpoint="/home/po/s1/Intern-Decision-2B", device="cuda")  # CPU 机器 device="cpu"
req = {"state": "客户:我的信用卡被扣了两次,要求今天之内退款。",
       "questions": {"department": {"type": "choice", "instructions": "Which team?",
                        "criteria": {"billing": "charges, refunds", "technical": "bugs"}},
                     "need_human": {"type": "noul", "instructions": "Needs a human agent?"}}}
print(eng.predict(req)["answers"])
```

```python
# Laya：load 传本地 snapshot 绝对路径（传 repo id 会打 HF，断网就挂）
import laya
agent = laya.load("/home/po/s1/laya", device="cuda")                 # 英文档（仓根）
# agent = laya.load("/home/po/s1/laya", device="cuda", subfolder="multilingual")  # 中文/多语档
print(agent.system_one(state, questions)["answers"])
```

验收物：返回含 `probabilities` / `decision` 的 JSON。

### 本机实测（2026-09-29，warm up 后连测 20 次，batch=1）

硬件：WSL2 Arch，Ryzen 9 7940HS（6 vCPU），15 GiB RAM，RTX 4070 Laptop 8188 MiB，
driver 616.56 / CUDA UMD 13.4，空闲态 SM 285 MHz（max 3105）/ P4 / 12 W。

独立跑两轮（第一轮空载、第二轮 `verify.sh` 全流程），**延迟有 10-25% 抖动，报告区间**：

| 引擎 | device | median（两轮） | mean | min | load | 峰值显存 |
|---|---|---|---|---|---|---|
| **ID-2B** | cuda bf16 | **76.65 / 89.64 ms** | 80.99 / 89.33 | 68.75 | 17.4 s | 4.72 GB |
| ID-2B（FLA 关，纯 torch 回退） | cuda bf16 | 191.96 ms | — | 172.73 | 5.7 s | 4.46 GB |
| **Laya 英文档** | cuda | **49.52 / 41.57 ms** | 53.10 | 37.42 | 7.5 s | 2.43 GB |
| **Laya 多语档** | cuda | **35.84 / 31.54 ms** | 36.57 | 26.21 | 8.4 s | 1.57 GB |
| Laya 英文档 | cpu | 774.20 ms | 777.26 | 725.93 | 6.1 s | — |
| Laya 多语档 | cpu | 221.44 ms | 223.23 | 202.17 | 8.0 s | — |

一句话记法：**ID-2B ≈ 77-90 ms，Laya GPU ≈ 32-50 ms，Laya CPU 英文档 ≈ 0.77 s、多语档 ≈ 0.22 s。**

考试要点：**ID-2B 是 76.65 ms 不是 191.96 ms**——差的这 2.5× 就是 FLA 有没有装对。
本机实测 `191.96 / 76.65 = 2.50×`，并且关掉 FLA 时 transformers 会明说：
`The fast path is not available because one of the required library is not installed.
Falling back to torch implementation.`
**看到 ~170ms+ 就是回退了，回第 2 步查 FLA。**

76 ms 而非桌面级的 ~50 ms，原因是笔记本 4070 空闲在 P4/285 MHz 且显存与 Windows 桌面共享；
不是 FLA 的问题。（对照实验：`scripts/bench_id_nofla.py` 强制关闭 FLA。）

**CPU 档要重新校准预期**：本机 Laya 英文档 CPU 是 **774 ms**、多语档 **221 ms**，
不是"10-50ms 级"。CPU 上要的是多语档；英文档 421M 在 6 vCPU 上很吃力。

---

## 4. 选型

| 引擎 | 官方 Jevbench | 定位 |
|---|---|---|
| ID-4B | **90.02** | 最高校准质量，需 ≥10 GB 显存 |
| （TypeSafe Jev 基线） | 88.74 | — |
| ID-2B | 84.68 | GPU ≥6 GB 的默认档 |
| Laya | 57.77 | 最快、最省显存、任何机器（含纯 CPU）都装得起 |

- GPU ≥6 GB → 默认 **ID-2B**；显存小 → ID-0.8B；纯 CPU → 只装 Laya。
- 只要最高校准质量且显存 ≥10 GB → ID-4B。
- 要**低延迟**（<40 ms）或要和 LLM 串在同一张卡上 → Laya 多语档。
- ID 与 Laya 可以并存（本机共占 ~6.3 GB，8 GB 卡能同时装下但有余量紧张）。

---

## 5. 行为特性（换引擎/换阈值前必读）

- **ID 的 urgency 判分普遍偏高**，且**爱判"转人工"**：本机同一工单
  ID-2B `need_human` P(yes) = **0.684**（→ yes）。
- **Laya 几乎从不转人工**：同工单英文档 **0.0002**、多语档 **0.1734**（→ 都不转）。
  两家在这一个字段上的极性差异是数量级的，不能共用阈值。
- **阈值判断用 `probabilities`，别硬卡 `decision`**。`decision` 只是 argmax，
  温度缩放后仍可能停在 0.5 附近；要的是概率再看你自己定的业务线。
- **换引擎后阈值必须重校**，ID↔Laya 之间尤其。
- ID 的 `noul` 返回 `{"no": x, "yes": y}` **dict**；Laya 的 `noul` 直接返回
  **float P(yes)**。写通用适配层时这里是分手点。
- ID 带**温度缩放校准**（默认 `temperature=2.100509348278`），`calibration` 字段可见。
- Laya 英文档会打一条 `RuntimeWarning: this checkpoint ships invalid temperatures ... 
  Treat confidence from the affected entries as uncalibrated`——标签概率仍可用，
  `confidence` 字段受影响，别用。

---

## 6. Pitfalls（全踩过）

1. **FLA 必须 git 装**。PyPI 的 flash-linear-attention wheel 是残缺包（缺 `__init__`/modules），
   装了等于没装 → `ModuleNotFoundError` 或**静默回退慢 2.5×**（本机实测 191.96 → 76.65 ms）。
   用 `--no-deps` + `git+https://github.com/fla-org/flash-linear-attention@v0.4.2`。
   判据：`is_flash_linear_attention_available()` 需 `fla>=0.2.2` **且 CUDA 可用**。
2. **`HF_HUB_DISABLE_XET=1`**，否则 401。
3. **`local_dir` 真名目录**，别落 HF cache（cache 里是 symlink，运行时会挂）。
4. **laya.load 传 snapshot 绝对路径**，传 repo id 会联网打 HF。
5. **本机 `HF_ENDPOINT=hf-mirror.com` 是有害的**（308 跳回 HF → `FileMetadataError`）。直连可用。
6. **causal-conv1d 不要试图源码编译**：PyPI 无 Linux 轮子，且驱动-only 的 WSL2 没有 nvcc。
   用 GitHub release 的预编译轮子，且 torch/cu/ABI/cp 四项都要对上。
7. **transformers 必须 5.14.1**（`Qwen3_5ForConditionalGeneration` 在内；旧版没有这个 head）。
8. **uv venv 里没有 pip**：`python -m pip list/freeze` 静默为空，用 `uv pip list --python <venv>/bin/python`。
9. 长任务用 `setsid nohup` 挂后台：会话被挂起/中断会杀掉普通后台任务，本机曾因此白等 4 小时。
10. 机器有 NVIDIA 卡但 WSL 里 `nvidia-smi` 不在 PATH：用 `/usr/lib/wsl/lib/nvidia-smi`。
11. **`noul` 的 `criteria` 键两个引擎不一样，写错会被静默丢弃**：
    - **Laya** 只认 `{"true": ..., "false": ...}`；写成 `{"yes":...,"no":...}` 直接 `ValueError`
      （报错原文：*any other key was silently dropped and replaced with the defaults*）。
    - **Intern-Decision** 认 `{"no":..., "yes":...}`（也接受 false/true）。
    - **不给 criteria 就等于用通用 yes/no 措辞**：实测判"这个操作会不会毁数据"时，
      `rm -rf ~/s1/venv` 只给 0.11 分，看起来像完全不能用。补上 criteria 后 ID-2B 的 AUC
      从 0.896 升到 1.000。**抽象判断类 noul 必须写死 criteria。**
12. **`predict_batch` 才是吞吐路径**：同一条打分，Laya 单条 73 ms vs `predict_batch`(batch=10)
    **6.9 ms/条**（10×）。批量打标一律用 `predict_batch`。

---

## 6.5 能力边界（本机实测——决定"能拿它干什么"）

这两个是**判别式打分器**，不是检索器、不是推理器、不是安全网关。三条实测边界：

| 任务 | 实测结果 | 结论 |
|---|---|---|
| 抽象风险判断（10 个操作，4 个真危险，给了 criteria） | ID-2B **AUC 1.000**、Laya 0.875 | 只能当**排序**信号，不能当硬闸门 |
| 同批任务不给 criteria | ID-2B AUC 0.896；Laya 绝对值崩坏 | criteria 是必需项 |
| 当 skill 检索/路由（真实 135 个 skill，8 个标注请求） | **Recall@5 = 0.00，MRR = 0.042** | **不要拿它做检索**，改用 BM25/embedding |
| ID-2B 图像输入（发票 vs 面单） | 类型全对（0.943 / 0.921），重复扣款 0.943 | 准，但 **≈26 s/张**，只能离线批处理 |

**危险样例（为什么不能当 safety gate）**：Laya 对 `git push origin main --force` 的
"会不会毁数据"打分 **0.30**，低于 `df -h`（0.35）和 `curl`（0.51）。按阈值自动放行/拦截会出事；
**只适合把待审队列按分数排序交给人类看**。

**擅长**：闭合小标签集 + 写死 criteria 的类型化分类（部门路由 / 紧急度 / 是否转人工 / 是否营销 /
是否含 PII），以及批量打标（GPU 批处理 6.9 ms/条）。
**不擅长**：开放式相关性判断、生成、多步推理、任何依赖绝对概率可信的自动决策。

⚠️ 样本量：以上 10 条 / 8 条是小样本，AUC 1.000 建立在 4 个正例上，**不是可靠性保证**。
上生产前必须用你自己的数据重测。

---

## 7. 跑不通时的排查顺序

1. **`transformers` 是不是 5.14.1**？不是就先装对（`import transformers; transformers.__version__`）。
2. **FLA 来源**：`pip show flash-linear-attention` 是不是 git 装的；`import fla; fla.__version__` 应为 0.4.2；
   看加载日志有没有 `Falling back to torch implementation`。
3. **device 是否真在 GPU**：`torch.cuda.is_available()` 与 `DecisionEngine(device="cuda")`；
   用 `nvidia-smi` 看推理时显存有没有涨。
4. **显存够不够**：ID-2B 峰值 4.72 GB。OOM 就降档到 0.8B，或 `dtype="float16"`，
   或 `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`。
5. 还不行才怀疑精度：ID 用 `attn_implementation="sdpa"`（默认），`dtype="bfloat16"`。

---

## 8. 本机实际路径（复制即用）

```
venv        /home/po/s1/venv              (Python 3.12.12, uv-managed)
ID-2B       /home/po/s1/Intern-Decision-2B
Laya        /home/po/s1/laya             (仓根=英文档, /multilingual=多语档)
日志        /home/po/s1/logs/{bootstrap,bench_id,bench_laya_*,bench_id_nofla}.log
脚本        /home/po/s1/{bootstrap.sh,dl_model.py,bench_id.py,bench_laya.py,bench_id_nofla.py}
```
