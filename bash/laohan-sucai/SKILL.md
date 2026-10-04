---
name: laohan-sucai
version: "1.2.1-candidate"
description: B-roll 素材供应器。读取⑨导演的 source manifest，搜索、下载、抽帧并记录可授权现实素材；只有视觉复核通过的资产可交⑪动画生产。Use when 用户说配素材、找B-roll、补真实场景、下载素材、审核素材、进入⑩素材，或⑨导演将 beat 路由为 BROLL_STOCK。
---

# B-roll 素材供应器

只为已经判定为 BROLL_STOCK 的现实场景找素材。它不决定动画、不把库存素材伪装成事实、不合成视频。V5默认采用“永久本地素材Top-K＋网络高权重多样性”策略：本地catalog负责快速复用，Pexels/Pixabay/Coverr仍并行提供新候选；只下载最终选择项。

## 输入与停止条件

正式入口是 09-导演/source-manifest.json 的 broll_requests，以及已批准的 PROOF_PUBLIC/PROOF_USER source_entries。每项 BROLL 必须有 beat_id、source_mode=BROLL_STOCK、visual_need 和 must_not_imply；PROOF 必须有 evidence.id。

🛑 STOP：没有 broll_requests 或请求不是 BROLL_STOCK 时，不搜索、不下载。是否生成请求由⑨素材策略决定；只要真实B-roll能增加具体性或画面变化，默认生成请求，只有明确`SKIP_WITH_REASON`才跳过网络。没有 provider key 时记录`provider_errors`并继续永久本地素材召回。

## 命令

~~~bash
# 搜索候选：默认读取项目本地catalog，同时并行检索Pexels/Pixabay/Coverr
node scripts/sucai.mjs search --source 09-导演/source-manifest.json --out 10-素材/network

# 非项目cwd时可显式指定本地库；local候选会复制到本episode后再抽帧
node scripts/sucai.mjs search --source 09-导演/source-manifest.json --out 10-素材/network --local-library "/绝对路径/你的素材库"

# accepted final使用过的网络素材才晋升永久素材库
node scripts/material-library.mjs promote-episode episodes/<slug>

# 下载一个候选，并生成缩略图供实际视觉检查
node scripts/sucai.mjs download --manifest 10-素材/network/素材清单.json --beat B01 --candidate pexels:123

# 先实际查看缩略图或 contact sheet，再记录判定
node scripts/sucai.mjs verify --manifest 10-素材/network/素材清单.json --beat B01 --candidate pexels:123 --verdict pass --reason "主体、构图和事实边界均匹配"

# 查看当前清单
node scripts/sucai.mjs report --manifest 10-素材/network/素材清单.json

# PROOF 只物化已批准证据；显式视觉确认后复制到本期并登记
node scripts/register-proof-asset.mjs episodes/<slug> B03 <proof-file> <thumb-file> --visually-verified
~~~

环境变量和官方申请入口见 references/providers.md。不要把 key 写入 SKILL.md、JSON、episode 或 Git。

## 工作流

1. 读取 broll_requests 的 query_terms；缺 query_terms 时只用 visual_need，记录搜索理由。
2. 默认读取项目`本地素材库/catalog.json`，只返回相关度最高的本地视频候选；catalog不存在时才回退到文件名扫描。不得把整个素材库塞进导演上下文。
3. 无论本地是否命中，Pexels、Pixabay、Coverr默认仍并行提供网络候选，以增加画面多样性。只有本期明确`--providers local`时才只查本地；Mixkit不做自动抓取。
4. 记录每个provider的status、candidate_count、elapsed_ms、rate_limits，并分别记录本地/网络候选数；单个provider的无key、限流或失败不阻断其他provider。
5. 写入`10-素材/network/素材清单.json`、`素材清单.md`、`_credits.md`；清单绑定当前source manifest，候选初始状态都是candidate_unverified。`material-library.mjs promote-episode`仍兼容历史episode的`10-素材/素材清单.json`，新episode只使用network分区。
6. 只下载选择的candidate并使用FFmpeg抽帧；local候选先复制到本episode。
7. 实际检查人物、动作、画幅、水印、错误文字、字幕安全区和must_not_imply。
8. 只有verify pass才标为visually_verified；selected candidate必须位于本期`10-素材/network/broll-assets/`并绑定文件/缩略图SHA，⑪只读取这种资产。
9. Jeffrey接受final后，只把实际使用且已核验的网络素材通过`material-library.mjs promote-episode`晋升永久库；未采用的网络候选不入库。
10. PROOF不进入库存B-roll搜索池。只把⑨已批准且绑定⑤`SUPPORTED claim_id`的同源evidence复制到`10-素材/network/proof-assets/`，不重做事实判断。

## 失败处理

| 情况 | 动作 |
|---|---|
| 某 provider 无 key 或 API 失败 | 写 provider_errors，继续其他 provider |
| 本地素材库不存在或不可读 | 标 local provider error，继续远程 provider |
| 全部无候选 | 标 no_result，返回⑨重新判断，不凑素材 |
| 全部候选视觉不匹配 | 标 no_approved_candidate，修改检索词或手动补充，不得进入⑪ |
| 下载失败 | 标 download_failed，不改变其他候选 |
| 视觉不匹配 | verify reject，不能因文本相关就通过 |

## 禁止事项

- 不对整篇口播逐句配图；
- 不自动把 no_result 变成动画；
- 不把候选文本分数当视觉通过；
- 不把本地文件名命中当视觉通过；
- 不使用 Mixkit 爬虫或把库存素材当用户 proof；
- 不在本 skill 中裁切、烧字幕、渲染或发布。
