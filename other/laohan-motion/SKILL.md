---
name: laohan-motion
version: "1.1.6"
description: 数字人×Motion模板视频制作总入口（路线④）。从锁定口播稿到成片交付的全链编排：配音→同声口型→拼接→全库模板选型→导演→production-guard门链→异模型复核→交付。Use when 用户说"创作motion视频""做motion片""motion制作""数字人motion路线""走motion模板"或锁定稿后选择数字人×Motion模板路线。
---

# laohan-motion · 数字人×Motion模板制作入口

本skill是Motion正式路线的制作编排入口，**不是方法真源**。方法、门与合同只认视频项目内的现行文件；本skill与项目真源冲突时，以项目真源为准，并按laohan-skillcreator流程回本仓修订skill。本文对齐当前PIPELINE/V4/DH-ROUTE；听感门等会演进的语义以真源现行文本为准，不从本skill复述。

项目根固定：`/Users/hanzhmacbookair/Documents/laohanvideo`（下文相对路径均从此起算）。

## 触发与反触发

**触发**：创作/制作motion视频、motion路线出片、数字人×Motion模板、锁定稿后走Motion。

**反触发（分流到对应入口）**：
- 原生Remotion episode（真人横/竖屏、digital_human_portrait竖屏）→ laohan-bianpai / laohan-daoyan。用户明确要**竖版数字人**也走原生 digital_human_portrait（Motion现行交付要求为landscape 16:9）。Motion期不建 `episodes/<slug>`、不占原生在制期名额、不跑 `new-episode`/`production-route`/`orchestrate-step`/0—⑭回执与0号门。
- 历史AST、双renderer对照、恢复历史episode → laohan-donghua。
- 选题与写稿（未锁定稿）→ laohan-xuanti / laohan-chuangzuo；本skill从锁定稿起接。
- 声音模型训练（复刻博主音色）→ laohan-yinse；v3-05是老韩已训音色模型，其每期WAV由项目侧产出。
- 发布与运营（⑫—⑭）→ 两路共用，授权、目标平台及最终点击方只认生产合同、四平台发布规格与本期明确指令，不在本skill另写永久手动/自动政策。

## 开工必读（漂移自检，每次执行）

按序读取并核对存在；缺任一文件或内容明显改版（如stage清单变化）→ 停止并报告漂移，不凭记忆继续：

1. `motion/mastery/PIPELINE.md` — 命令与门链唯一真源
2. `motion/mastery/PRODUCTION-METHOD-V4.md` — 制作方法现行版
3. `motion/mastery/DH-ROUTE.md` §一A—一C — 声音/口型/拼接真源
4. `motion/mastery/delivery-requirements.json` — 用户画幅与质量要求真源（当前landscape 16:9；质量第一原则、无限用好模板是底线）
5. `motion/mastery/current-release.json` — helper与模板包身份/SHA（当前helper 1.0.0-rc.32；包T01—T06，版本以该文件为准）
6. `motion/mastery/pronunciations.json` — 发音表真源
7. `docs/工作区生产合同.md` §一 — Motion边界与凭据红线
8. `docs/视频生产入口与适配.md`「Motion正式路线接入」节 — 交接点/目录规范/分流/门豁免
9. `docs/HARNESS_COMPATIBILITY.md` — 跨宿主读取与实测范围（不把另一模型已读当自己已读）
10. `STATUS.md` 当前任务区 — 本期状态与在途工程；**开工先查 `motion/projects/` 是否已有同期在途工程（如最新日期目录），有则续接，不另起**

## 输入契约

- **锁定口播稿**：script-pool或episode候选经Jeffrey接受/锁定；未锁定→先回xuanti/chuangzuo链，不代写代锁。
- **显示稿与发音稿分开**：标识符按原名显示；`laohan-*`标识符按`pronunciations.json`中文读音（如laohan-sousuo读"老韩搜索"），未知项报未定，不按拉丁字母拼读。
- **交付要求只认delivery-requirements.json**：手机反馈、竖屏人物源、模板portrait能力都不是变更授权；只有Jeffrey明确新指令才更新该文件。
- **新稿必有新WAV**：每期v3-05合成整稿WAV，登记路径/SHA/采样数；听感门语义按`DH-ROUTE.md` §一B现行文本执行（2026-10-28起Jeffrey授权默认通过、明确反馈问题才回退重合成并重绑——以该文件现行版本为准）；不消费历史162.68s音轨，不因模板自带TTS重念。

## 制作七步（骨架）

细节、失败处置与逐步输入输出见 `references/full-chain.md`。

| # | 步骤 | 执行位置 | 关键产物 |
|---|------|---------|---------|
| 1 | 文案定稿（锁定稿交接） | Mac | 冻结显示稿+发音稿 |
| 2 | 最终配音（v3-05合成；合成方法真源=`~/Documents/声音资产/Jeffrey/数字人专属音色融合方法.md`，执行前必读；听感门按DH-ROUTE §一B现行文本执行） | pro6000-a服务器GPU，Mac保存试听 | 本期WAV+SHA+采样数登记 |
| 3 | 基础形象（合格素材复用优先；确需新素材走`motion/tools/dh-generate-clean.mjs`） | 本地/产品服务器 | 人物素材 |
| 4 | 同声口型（WAV驱动，`same-voice-local.py`分块+`run-same-voice-remote.py`推理） | pro6000-a GPU，Mac调度 | 口型分块+清单SHA |
| 5 | 画面拼接（唯一入口`same-voice-local.py assemble`，拒绝手搓ffmpeg拼接） | Mac | 完整人物画面，原WAV为唯一主声 |
| 6 | 导演与模板（模板/分支验证→整段构思与编舞→声学绑定及production-guard门链） | Mac本地 | 官方工程+参数+回执 |
| 7 | 混音与交付（check-delivery带--video→Jeffrey实际听看接受） | Mac | 成片+accepted-final登记 |

## 导演执行（先于字段登记）

第6步按V4“直接使用模板”“从实际效果认识模板”完成整段构思、人物/主辅关系、素材与动作编舞，再登记；具体落点见 `references/full-chain.md` 第6b节。选中模板名不等于选中分支已经保留其表现力。技术排障、可读性修复和门链通过分别留证，不能代替“本期关键内容被怎样讲清”的实际效果判断。

## 门链（命令形态；字段与argv细节以PIPELINE为准）

所有plan/render/delivery必须经共同入口，直接调helper是显式旁路、不登记门通过。原包 `read/new/setup/doctor/prepare/preview` 保持官方命令原样执行，**不经guard**（guard只前置检查plan/render）：

```sh
# ① 声学对齐（写参数前；先按PIPELINE核解释器可导入stable_whisper/torch，缺环境停止）
"/Users/hanzhmacbookair/Documents/laohanvideo/.tools/whisper-align-env/bin/python" motion/tools/align-source.py --audio 实际候选声音.wav --spoken-script 发音稿.txt --out 全新词源目录

# ② 正式片共同制作入口（--record指向本期production.json）
python3 motion/tools/production-guard.py --record 本期/production.json --stage direct    # 登记编排+全库选型，封存revision（不要求已有params/captions）
python3 motion/tools/production-guard.py --record 本期/production.json --stage plan  -- node 已核helper.mjs run 实际.motion 原包plan其余参数

# ③ 首次动态样段：独立kind=pilot记录，先走样段自己的 direct→plan→preview，再pilot渲染
python3 motion/tools/production-guard.py --record 本期/pilot.production.json --stage direct
python3 motion/tools/production-guard.py --record 本期/pilot.production.json --stage plan  -- node ... plan参数
python3 motion/tools/production-guard.py --record 本期/pilot.production.json --stage pilot -- node ... render ...
# 父编排不要求已有plan或pilot审核（避免首单循环）；父编排新revision后样段须重新登记

# ④ 复核任务（--sample可重复；数量按未证明风险决定，不是两段配额）
python3 motion/tools/production-guard.py --record 本期/production.json --stage review-brief --sample 本期/qa/样段A.mp4 --sample 本期/qa/样段B.mp4

# ⑤⑥ 渲染与交付
python3 motion/tools/production-guard.py --record 本期/production.json --stage render -- node ... render ...
python3 motion/tools/production-guard.py --record 本期/production.json --stage delivery

# 画幅/字幕只读检查：plan前一次；交付前同命令加 --video 实际成片.mp4
# --source-record/--pronunciations 新制作必带（缺失则发音稿一致性校验不执行）
PATH="/opt/homebrew/bin:$PATH" python3 motion/tools/check-delivery.py \
  --params 本期参数.json --captions 本期字幕 --script 冻结纯口播稿.txt \
  --asr 原ASR.json --input-root 本期素材目录 \
  --source-record 词源目录/source.json --pronunciations motion/mastery/pronunciations.json
```

顺序硬约束：正式plan必须引用direct登记的当前revision；pilot在review-brief之前完成样段自己的登记链；真实plan/preview+实际样段齐备后先review-brief生成完整复核任务，异模型复核通过才完整render；render/delivery重核全部bindings。变化分两类：**新素材/声音/契约/编排变化→先新revision再plan**；**参数调整→不强制新revision，但必须重新plan/预览/复核**。旧回执不补签。

MK渲染只按本包公开命令传`render <prepared-project>`；不要把poster-kit的`--plan/--preview-review`强加给新版MK。共同入口核prepared project路径、当前plan审阅摘要与origin的planInputsSha256一致，再由原包核预览/素材字节；具体红字和其它分支见PIPELINE的argv表。

执行环境也须实核：`PATH`前缀可能改变实际Node/Python版本，不能用终端先前的`node --version`替本次命令签名。长JSON解析失败先按PIPELINE的stdio入口诊断；helper可能隔离`NODE_OPTIONS`，不能只设该变量就声称后代已加载修复。使用本期已核真实Node的临时PATH包装与该变量配合，原包/helper不改，保留同输入的红→绿证据；不把截断当文稿容量上限。

## 模板全库选型（正式片direct前置，强制）

四步：**全库刷新→候选比较→按需取得并验证→确认或重选**。`production.json`提供`template_selection`指向本期`template-selection.json`（schema=`laohan.motion-template-selection/1`）。要点：从本稿提取必须完成的视觉任务→全catalog轻量筛2—4个入围候选（本地与库外同池，各带"本稿哪段需要什么→模板哪项能力承担→依据→待验证"理由；**新模板无画像不得直接淘汰，也不强制最终选库外**）；选中不在本地按官方流程下载验签登记current-release（**作者免费公开分发模板包视为已有下载授权（2026-10-28 Jeffrey指令）；付费或需新凭证的包仍先取得明确授权**）；同族复用必须写`reuse_comparison`与最强异族备选比较；否决项记`rejections`理由（同版本同分支且无新证据不重复尝试已否决项；下载失败与表达不匹配分开记录；候选耗尽回到文案端重新计划）。不从本机已装包惯性重复；刷新是轻量catalog级动作，不重做全库深度审计。字段细节见PIPELINE「模板全库选型」节。

**字幕设计选择纪律**：选路线时把原模板演示/相关工程中的字幕作为视觉依据，核对原生与组件分支实际保留的排版/强调/语言能力并记录本片采用哪种；不能只因组件分支接SRT方便就绕过这项选择、用通用字幕层掩盖设计降级。

## 异模型复核与验收

- review-brief生成完整复核任务（真源=`motion/mastery/VISUAL-REVIEW-BRIEF.md`），连同样段交异模型实际观看，不能只转发文件路径；交接时只带完整目标、当前编排与真实材料，**不转抄旧批准/旧QA摘要**；执行者已接触过历史结论须声明暴露范围，不称完全盲审。
- 复核模型按全局优先级：GLM→codex→Magpie免费DeepSeek→官方ds（禁guiji；与实现者同家族被guard拒绝）；**调用满配：思考档最高合法档不降级、不人为压缩等待/超时、不限制上下文窗口与输出token上限；免费档当场核实该provider/model当前免费标记（同名DeepSeek有收费款）**。
- review schema=`laohan.motion-visual-review/1`，scope八项（技术四项+创意四项）：subtitle-style/subtitle-breaks/action-sequence/semantic-content/viewer-comprehension/presenter-staging/pacing-hierarchy/sample-coverage；final另有独立字段`whole_film_review`。pilot_review必须覆盖请求中全部样段。
- 负责人逐项裁决后登记（裁决前自审：从实际叠加动态逐项读回承载意义的画面文字、核疑点原尺寸与声明的观看尺度、检查首末及切换时人物/字幕/主图进退）；不编JSON冒充调用；原REVISE不得改写。
- Jeffrey实际接受才算final；机械PASS（`MACHINE_CHECKS_PASSED_NOT_ACCEPTANCE`）≠接受。

## 红线

- **无授权不发布**；Motion期按现行实践登记`deliveries/accepted-final.json`并用真实Chrome预填/页面回读。是否代理终选、最终点击与目标平台以生产合同及本期实际授权为准；仅预填授权不能冒充发布授权，本期例外不外延到其它期或平台。
- `motion/assets/`、`motion/baselines/`、`motion/runs/`、`motion/projects/`、`motion/deliveries/`均不入git（证据靠STATUS登记+工程目录本机留证）；原包只读、不私改、不手拆保护核心。
- 凭据零入档；Motion标识疑似泄露按合同§一处置（停调用、记录、账号持有人官网撤销），不擅自换Key。
- 线上产品代码不动；产品侧只读；服务器成片回传本地并登记SHA后，同批删该任务chunk与preprocess缓存（批量删非本任务产物先跨模型复核）。
- 物理变速另建候选派生（人物/原声同倍率保音高，字幕/词界/时点统一换算一次），原速输入不覆盖；`speed=1`时声音SHA必须相等。**不为凑模板截短/拉伸已验人声或改变嘴型时间**；容量不足换真实表达，不缩减模板能力。
- 首次使用共同入口的新宿主，须先以本片负例验证（错误词源/缺样段审核会被拒绝）再做正确制作；未实际验证的宿主不标VERIFIED。
- Motion期豁免的门只限原生Remotion链；共用门照常：发布信息与#AI新星计划、违规检测、候选接受与发布授权、远程算力纪律、Git纪律。

## 输出与完成证据

- 工程目录：`motion/projects/YYYYMMDD-<slug>/`（production.json、director.md、inputs/、qa/、references/、instance/、publish/、`deliveries/`子目录）。
- 候选/定稿成片与manifest/qa回执归工程`deliveries/`子目录（V4旧文"交付成片归motion/deliveries/"已被接入规格取代，以工程deliveries/为准）；输入、最终参数、官方工程及QA归工程目录。
- STATUS.md登记本期制作状态；接受记录=工程`deliveries/accepted-final.json`。
- 完成证据链：来源回执（align-source）→direct revision回执→plan成功回执→样段自己的direct/plan/pilot回执→review-brief请求+异模型response→render bindings→delivery final_review→check-delivery(--video)通过→Jeffrey接受登记。缺环不称完成。
- 检查器未支持的合法原包结构：沿其公开原生校验补核并分别记录官方结果与本工具未核范围（UNVERIFIED），官方补核不得冒签production-guard通过；不为过检查改分支或删槽。
