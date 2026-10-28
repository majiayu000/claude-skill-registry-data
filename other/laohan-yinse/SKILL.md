---
name: laohan-yinse
description: 复刻博主声音模型工作流（硬性前置，唯一方法=服务器微调训练）。任何要复刻博主做数字人视频的，生成视频前必须先在 pro6000 算力机用 CosyVoice3 微调训练该博主的声音模型（8-10 分钟素材），训完拷回本地使用。覆盖：多条视频声音提取→质检→拼接训练素材→pro6000-a 服务器特征提取+微调训练→模型回迁注册→验收。Use when 复刻博主、克隆音色、声音模型、voice clone、训练音色、数字人声音、给博主教声音、声音微调。
---

# laohan-yinse — 复刻博主声音模型（服务器微调）

## 使命与合同

**每个复刻博主一个专属声音模型，唯一方法 = pro6000 算力机 CosyVoice3 微调训练**（Jeffrey 2026-10-27 钉死：不走零样本）。声音模型是博主复刻的核心资产：数字人=形象克隆+口型驱动，声音来自 TTS——没有本人音色模型，出来的是"通用音色配这张脸"，瞬间违和。

硬性流程：形象处理/视频生成之前，先完成声音模型训练与登记。一次建立、所有视频复用。

## 素材标准

| 项 | 要求 |
|---|---|
| 总量 | ≥8-10 分钟纯人声（多条原视频） |
| 质量 | 单人清晰口播、领夹麦/近场；无明显 BGM/混响（BGM 混入训练=音色污染） |
| 格式 | WAV 44.1kHz 单声道（提取时归一） |
| 同源 | 与形象素材同一博主 |

## 工作流（六步）

### 1. 提取（本机 ffmpeg，逐条）

```bash
ffmpeg -y -i <视频>.mp4 -vn -ac 1 -ar 44100 <博主>-<条目名>.wav
```

### 2. 质检

每条转录抽听（SenseVoice/whisper）确认纯人声；BGM 重/混响/多人的条目剔除。

### 3. 拼接训练主素材

```bash
for f in <博主>-*.wav; do case "$f" in *-full-*) continue;; esac; echo "file '$f'"; done > concat.txt
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy <博主>-full-<总秒数>s.wav
```

### 4. 上传服务器并准备数据（pro6000-a）——2026-10-27 实战验证版

训练机：`ssh pro6000-a`（AutoDL RTX PRO 6000 Blackwell 96G，seetacloud 西部；生产算力机，跑 7 进程服务）。训练工作目录：`/root/autodl-tmp/cosyvoice-train/`（Jeffrey 先例 model-jeffrey-v3-05 在此）。

**切段（本机，已验证）**：ffmpeg silencedetect 找静音点，静音中点作切点，聚成 4-15s 段：
```python
# ffmpeg -i full.wav -af silencedetect=noise=-35dB:d=0.45 -f null -
# 解析 silence_start/end 取中点为切点，4-15s 聚段，<3.5s 丢弃，>15.5s 硬切 10s
```
段命名 `<人名>_b<批>_s<毫秒6位>.wav`（对齐 Jeffrey 判例）。78 段/483s 实测一次通过。

**每段转录（本机）**：SenseVoice 批量；转录后**清洗噪声符号**（🎼😊 等表情要删，否则进训练文本污染）。

**数据目录结构（六件套，缺一训练必挂——三个坑全踩过）**：
```
data-<人名>/{train,dev}/     # 9:1 分
  *.wav                     # 切段音频（与文本同目录）
  text            # 每行: <utt_id> <转录文本>
  utt2spk         # 每行: <utt_id> <说话人名>
  spk2utt         # 一行: <说话人名> <所有utt_id空格连>
  wav.scp         # 每行: <utt_id> <wav绝对路径>   ★坑1：缺它 extract_embedding 直接 FileNotFoundError
  instruct        # 每行: <utt_id> You are a helpful assistant.<|endofprompt|>   ★坑2：缺它训练 forward KeyError instruct_token（不是目录是文件）
  parquet/ + *.data.list  # ★不手写：管线 make_parquet_list 自动生成
```
打包上传：`tar czf data-<人名>.tar.gz data-<人名>/ && scp ... pro6000-a:/root/autodl-tmp/cosyvoice-train/`（mac tar 的 xattr 警告无害）。

### 5. 特征提取 + 微调训练（服务器，2026-10-27 实战验证配方）

**独立脚本模式（不碰 Jeffrey 原 data/ 与脚本）**：复制 `pipeline.sh`→`pipeline-<人名>.sh`、`train.sh`→`train-<人名>.sh`，改四处：`D=data-<人名>`、`--model_dir exp/<人名>/llm`、`--tensorboard_dir tb/<人名>/llm`、`--rdzv_endpoint=localhost:1235`（端口错开 1234 防撞）。

```bash
# 服务器上一键跑（特征提取CPU → parquet → GPU训练，自动串接）
nohup bash /root/autodl-tmp/cosyvoice-train/pipeline-<人名>.sh > <人名>-train.log 2>&1 &
# 日志盯关键行：PIPELINE_DONE → "train start" → "Epoch N Step M" → TRAIN_DONE
```

- 底座：`Fun-CosyVoice3-0.5B-2512`（英文素材走其中 CosyVoice-BlankEN，对路）
- 训练配方：torchrun 单卡 `cosyvoice/bin/train.py --model llm --use_amp`（conf/cosyvoice3.yaml 默认档）
- 实测速度：70 段/8 分钟数据，PRO 6000 单卡几分钟一个 epoch，全程约 10-30 分钟级
- GPU 与生产 TTS 共存：训练约再占 16-20G（共 97G），不冲突；但别在生成高峰训

**产物**：`exp/<人名>/llm/epoch_N_whole.pt`（含 epoch/step 元数据键——★坑3：直接 cp 当 llm.pt 用会 `Unexpected key(s): epoch, step` 加载失败，必须剥离）。

### 5.5 模型组装与合成验收（2026-10-27 实战验证）

```bash
# ① 组装推理目录（底座全家 + 微调 llm.pt）；PM=底座权重根
PM=/root/autodl-tmp/laohan/weights/cosyvoice3/Fun-CosyVoice3-0.5B-2512
cp -r $PM /root/autodl-tmp/cosyvoice-train/model-<人名>-v1
# ② 剥离元数据键后存 llm.pt（坑3修复）
python -c "import torch; sd=torch.load('exp/<人名>/llm/epoch_N_whole.pt',map_location='cpu',weights_only=True); sd.pop('epoch',None); sd.pop('step',None); torch.save(sd,'model-<人名>-v1/llm.pt')"
# ③ 合成验收：PYTHONPATH 必须=仓目录，REF_WAV 必须绝对路径（坑4/坑5）
cd CosyVoice && PYTHONPATH=$PWD python synth.py   # AutoModel(model_dir) + inference_zero_shot(英文测试句, prompt=BlankEN模板+参考段文本, REF_WAV)
```

- 合成产物 SYNTH_DONE 后 scp 回本地给 Jeffrey 听审（相似度≥8/10 拍板）
- 模型回迁：只回迁 llm.pt（约 2GB），底座本地/服务器都有不重复迁

### 完成证据（训练环节怎么算完成）

① data-{博主}/{train,dev}/parquet 生成且 pipeline-<博主>.sh 日志打印 PIPELINE_DONE；② `model-<博主>-<版本>/llm.pt`（微调权重，剥离 epoch/step 键后）产出并拷回本地 assets/voice-models/<博主>/；③ 验收三条（见第 6 步）全过并登记。任一不满足=未完成，不进形象/渲染阶段。

### 6. 模型回迁 + 登记 + 验收

- checkpoint 拷回本地项目 assets/voice-models/<博主>/（Jeffrey 惯例：服务器训完放本地）
- 登记表（项目内维护）：博主/建模日期/素材/模型路径/验收状态
- 验收三条：①固定测试句（英文+中文各一）与原声主观相似度 ≥8/10（Jeffrey 听审）②F0 基频域 ±20Hz ③连续 10 次生成无破音/吞字/漂移

### 7. 整稿合成（交付给口型链的最终 WAV——laohan-laowai ⑤ 的输入契约）

```python
# 服务器 CosyVoice 仓内跑（PYTHONPATH=$PWD）；长文分 chunk 返回必须 torch.cat 拼接（★坑：只取首 chunk=截断）
speech = torch.cat([c["tts_speech"] for c in cv.inference_zero_shot(全文案, prompt, REF_WAV, stream=False)], dim=-1)
torchaudio.save(out, speech, cv.sample_rate)
# 下载回 Mac 后统一转 24kHz 单声道 PCM16（口型链硬要求，此步由本 skill 交付时完成）：
ffmpeg -y -i <整稿>.wav -ar 24000 -ac 1 -c:a pcm_s16le <整稿>-24k.wav
```
- 完成证据：整稿时长与文案语速匹配（英文≈7-8 词/s 抽查）+ Jeffrey 整轨听审通过 + SHA 绑定。

## 反触发（不用本 skill 的场景）

- 只需临时试听/应急验证音色（走产品零样本）——已被 Jeffrey 禁止用于交付，不从这里走
- 真人实拍项目的音频处理（不涉及博主复刻）
- 训练服务器不可达且无替代 GPU——报告阻塞，不降级零样本冒充完成

## 失败路径

- 素材质检不过（BGM/混响）→ 换条或降噪后复检，不强行训练
- 训练中断 → run.sh 分 stage 重跑已完成跳过；产物缺失如实报未完成
- 验收相似度 <8/10 → 排查素材纯度/切段质量后重训，不降标准登记

## 红线

- 只训练**已决策复刻**的博主（复刻合规决策先行：**需 Jeffrey 逐博主明确决策并留证**；商业化前必须切纯生成形象）
- 服务器操作限训练目录 `/root/autodl-tmp/cosyvoice-train/`，不碰生产 7 进程与 `/data/laohan/laohan-node`
- GPU 训练费用按既有授权，不新增付费点；AutoDL 关机后生产进程不自启（勿随意重启算力机）
