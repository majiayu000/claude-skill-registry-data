---
name: laohan-laowai
description: 老外博主复刻→数字人→抖音视频全流程总控（含调用 laohan-yinse）。从"选一个外国博主"到"数字人视频发布"的端到端自动化流程：博主选型与资料包下载→声音模型（服务器微调，硬性前置，调 laohan-yinse）→形象素材处理（字幕检测/裁剪/硬门槛）→same-voice 同声口型本地工具链（pro6000-a 音色合成+TBDub 口型）→双语字幕后期→发布与流量复盘。Use when 复刻老外博主、数字人账号、老外数字人、复刻博主做视频、老外IP起号、数字人全流程、新博主资料包、数字人怎么生成。
---

# laohan-laowai — 老外博主复刻数字人全流程

## 使命与合同

**用老外的脸+外国独特教育/文化内容，做中国家长/观众共鸣的数字人爆款**。本 skill 是总控：七阶段端到端，全自动（API 直调，不上网页）。首个实战案例：`~/Documents/laowai/1chengzhang`（海思博士账号，Deborah 形象）——细节合同以该项目 docs/ 为准。

## 七阶段流程

### ① 博主选型与资料包

- 选型标准：教育者可信度 > 第一视角口播形态（talking head，非 vlog/skit/旁白）> 数据 > 类型差异
- 下载 5-8 条视频（laohan-xiazai：TikTok 用 yt-dlp 直下）+ info.json 元数据
- **口播形态逐帧验证**（抽帧+视觉模型确认正脸对镜头说话；抽帧落在无字幕间隙≠干净，必须多点验证）
- 合规决策先行：形象克隆+虚构新身份（绝不冒用真人姓名/履历）；起号期灰色可接受、商业化前换纯生成

### ② 声音模型（硬性前置，唯一方法=服务器微调）

**调用 skill `laohan-yinse`**：8-10 分钟素材 → pro6000-a 服务器 CosyVoice3 微调 → 模型回迁。视频生成前必须完成，否则声音违和。

### ③ 形象素材处理

- 硬门槛（laohanagent 官方）：竖版（高>宽）/短边≥720p/时长≥8s（推荐 30-60s，越长越好）/≤30fps/MP4/<200MB
- **字幕必须去除**（会被引擎复制进成片）：博主视频普遍带字幕 → 底部 crop 或换无字幕条；多点抽帧验证（首/中/尾/多段）
- 转码 h264；处理实录与判例参照项目 docs/dh-production-guide.md

### ④ 形象与声音资产（复用已有素材，不走产品注册）

- **形象素材：已有博主视频直接复用**（prepare 前多点抽帧验证全程同一正脸；开头 B-roll 插入画面必须掐掉——见⑤坑）
- **声音：laohan-yinse 微调模型整稿合成**（见②调用，24kHz PCM16 WAV 由 yinse 第 7 步产出）
- ~~产品 avatar-assets/voice-assets API 注册~~ **已淘汰**（2026-10-28）：那是产品网页向导链（零样本参考录音+29积分/次渲染），与本 skill 的 same-voice 路线互斥，且违反"声音不走零样本"红线。历史踩坑记录（MIME 显式 type / consentVersion=voice-reference-v2 / loudnorm 电平门禁）仅当未来确需产品链时参考。

### ⑤ 同声口型渲染（DH-ROUTE 路线④，2026-10-28 实战验证——唯一正确流程）

**方法真源：`~/Documents/laohanvideo/motion/mastery/DH-ROUTE.md` + `motion/tools/README-same-voice.md`（本节只是入口索引，冲突以真源为准）。**

不走的路（都验证过不是正路）：产品 lease/operations 报价链（29积分/次，网页向导已淘汰）、ispeech 图+音频（另一条产品链）、直控生产 worker。

```
① 最终 WAV：音色模型在 pro6000-a 合成整稿（laohan-yinse 流程）→ 24kHz 单声道 PCM16
② 形象素材：已有素材直接复用（无需产品订单）
③ Mac prepare：python3 motion/tools/same-voice-local.py prepare \
     --audio <24k.wav> --avatar <形象.mp4> --max-input-frames 180 --out <全新目录>
④ validate manifest → 上传 manifest/inputs/chunks/run-same-voice-remote.py 到
   pro6000-a:/root/autodl-tmp/laohan/motion-same-voice/<小写实验名>/
⑤ 预检（无 --run）→ 真跑：--run（total_timeout 3600s，单块 480s 上限）
⑥ Mac assemble：same-voice-local.py assemble → same-voice-candidate.mp4（原 WAV 主声）
```

**坑（全部实战踩过）**：
- ★形象素材开头可能是插入 B-roll（案例画面）——prepare 前多点抽帧验证全程同一正脸；mediapipe 丢脸 >10 帧直接 RuntimeError（chunk-001 判例：开头 5 秒小女孩 B-roll）
- ★生产活动保护：GPU 有生产 TBDub 任务时本任务自动 STOP_UNKNOWN_CUDA_PID 让路——等生产空闲 --resume（已存在 outputs 目录不能重跑，只能 resume）
- 音频必须 24k 单声道 PCM16；180 帧分块上限（1080 宽输入 20GiB 内存保护）
- 隔离 runner SHA 必须匹配 `469d820e...`（冻结保护）
- 完成证据：assemble 产物 same-voice-candidate.mp4 全帧数一致+完整解码；状态=候选待听审，Jeffrey 过目后才算验收

**Motion 模板包装（⑥后期）：不需要学习/执行**（Jeffrey 2026-10-28 指示——口型成片即交付物）。

### ⑥ 后期

- 字幕：**中文大在上、英文小在下**（同屏成对；目标语言 > 中文观众阅读优先级）
- BGM（低音量钢琴避让人声）+ **AI 生成标识（平台声明必勾）**
- 违规检测过 laohan-weigui；后期管线可接 laohanvideo（Remotion 出片）；**成片不加 AI 标识（Jeffrey 死规定 2026-10-28）**

### ⑦ 发布与复盘

- 抖音：养号 2-3 天再发；账号装修（人设简介前 3 行钩子）
- 数据：opencli douyin stats/videos 拉取；10 条内决策点（引流款 vs 人设款占比调整）

## 完成证据（全流程怎么算完成）

① 最终 WAV 绑定 SHA 且 Jeffrey 整轨听审通过；② assemble 产物 same-voice-candidate.mp4 全帧数一致+完整解码（ffprobe 无错）；③ 字幕/AI 标识在成片可见；④ **发布前必须 Jeffrey 明确批准**（外部发布授权不可由 agent 自拍板）——发布动作本身另按项目合同执行。

## 反触发（不用本 skill 的场景）

- 真人实拍/老韩本人出镜项目（走 laohanvideo 真人路线）
- 只做选题/文案/装修（单一环节走对应 skill：chuangzuo/weigui 等；本 skill 是复刻数字人全流程总控）
- 声音模型单环节细节（进入 laohan-yinse，本 skill 只在②处调用它）

## 失败路径

- 声音模型未建成 → 全流程停在②，不跳过训练直接渲染（零样本已被禁用）
- 形象素材字幕去不净/硬门槛不达 → 换素材条或重新选型，不降门槛上传
- 渲染链失败 → 按真源 DH-ROUTE/README 排障；同一故障重试上限 3 次，仍失败报阻塞并上报 Jeffrey（不无限重试、不退回网页/产品链绕路）
- 验收（深肤色还原/口型/音色）不过 → 回退候选形象名单（persona-candidates 排序），不硬发

## 关键红线

1. 声音不走零样本（Jeffrey 钉死，唯一=服务器微调）
2. 全流程 API 自动化，不退回网页手动操作
3. 不冒充真实存在的人（虚构人设身份）
4. pro6000-a 是生产算力机：训练限 cosyvoice-train 目录，不碰生产进程
5. 不加 AI 标识（Jeffrey 2026-10-28 死规定，覆盖此前所有合规条款）

## 素材资产清单（每个博主资料包标准结构）

```
assets/
  persona-candidates/  原始视频（形象候选）
  upload/              形象上传母版（无字幕/达标）
  voice-training/      声音素材（逐条 WAV + 拼接主素材）
  voice-models/        微调模型 checkpoint（服务器回迁）
  benchmark/           对标视频库+转录
docs/
  persona-*.md         人设卡     topic-library-*.md  选题库
  scripts-*.md         文案       account-setup.md    装修
```

## 服务器协作判例（2026-10-28 实战，pro6000-a）

- **AutoDL↔ECS 线路丢包**（曾 45%→90%）：症状=worker 间歇 fetch failed 而 curl 偶通；ECS/nginx 全正常（请求到端有 204 应答）。修复=平台侧修线路；线路恢复后 worker 连接池可能仍坏 → `laohan-node restart worker`
- **dsub 去字幕批处理**（另一工作线的 GPU 任务，PAUSE 文件协调）：杀法 `kill -9 <主控PID> <guardPID>` + `pkill -f paint_strips`——**pkill pattern 陷阱**：主控进程名是 `run2` 不是 `run2.py`，pattern 写 `run2.py` 杀不中，主控会持续拉起新 worker；杀完放 PAUSE 防复活
- **runner resume 三死锁**：①resume 沿用首次 baseline，中途重启过 worker/日志变化=baseline 永久脏（STOP_PRODUCTION_LOG_CHANGED 复发无解）→ **换全新目录重跑**（cp manifest/inputs/chunks/脚本到新 base）；②`--expected-checkpoint-sha256`=**batch-state.json 文件本身的 SHA**（不是内部字段）；③STOP_CONTAINER_INCREMENT_20_GIB=容器内存增量相对判定，服务内存波动会漂，低成本重试新目录即可过
- **分块断点**：18 块跑到 17 块被打断 → `--start-chunk 17 --end-chunk 18` 单补，assemble 时 `--additional-outputs` 合并
