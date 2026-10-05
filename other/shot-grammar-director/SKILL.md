---
name: shot-grammar-director
description: 将已确定 Beat／Shot Intent 且完成必需专业预设计的镜头或段落转为最终 Shot Partition、Shot DNA、静态分镜和动态控制，维护 SHOT_HANDOFF、专业路由门禁、可运动性、图像／视频验收与局部修复。用于镜头设计、正式交接及生产门禁；不创建全片创意、不代定或冒充抽象、3D、实景合成、VFX 专业贡献，不输出平台最终 Prompt。
---

# 镜头语法与验证中心

当前写入 SHOT_HANDOFF v1.2。先读 [公共政策](references/production-policy.md)，同版本已有则复用。请求范围决定流程长度：合格已有帧直接复用；仅动态／提示词请求不强制生资产与宫格。

## 所有权与模式

上游决定镜头目的和事实，本 Skill 设计观看立场／构图、静态与动态表达，校验协议和实际证据。原 ID 与用户锁项继承，改变锁项提交最小 change_requests，不重做全片。

| 模式 | 执行工作 | 按需读取 |
|---|---|---|
| PROTOCOL | 建立或校验当前阶段字段；旧版明确迁移 | [v1.2 协议](references/production-protocol-v1-2.md)、[迁移](references/migration-v1-1-to-v1-2.md) |
| CREATE | Beat／Shot Intent → 最终 Shot Partition → Shot DNA → Rhythm & Duration Pass → 静态状态，出图前检查草稿运动可行性 | [创作语法](references/creation-grammar.md) |
| CONTROL_PREFLIGHT | 批量出图前检查草稿起止、控制信号、运行端组合；不锁正式动态 | [控制路由](references/generation-unit-routing.md) |
| VISUAL_GATE | 查看真实资产／入选帧／必要段落板，检查静态和可运动性 | [门禁](references/review-gate.md) |
| GU_ROUTE | 分镜选定后完善原 Motion Card，正式 GU 和最小合法控制 | [控制路由](references/generation-unit-routing.md) |
| RESULT_VALIDATE | 实际输出逐项验证，失败先诊断再修复 | [门禁](references/review-gate.md) |

阶段不足时不虚构结果。没有上游的孤立镜头只建最小项目／段落／镜头记录；未决定媒介事实时交相应专业导演。

## 专业执行防绕过门禁

执行 CREATE 或 CONTROL_PREFLIGHT 前读取 SEQUENCE_CARD 的 `professional_route` 和原卡内的专业贡献。凡已声明主导或辅助 Skill，必须满足：对应 Skill 已在当前任务按指定 DELEGATED 模式执行；贡献覆盖当前 object_ids；可见证据、事实／参考、专业不变量、必要资产、草稿运动、风险和接口已写回；结果为 PASS；主辅接口无未解决冲突。

任一条件不满足时返回 `BLOCKED` 或 `REVISE`，`next_gate.gate_id: PROFESSIONAL_PREDESIGN`，owner 指向缺失或需修订的准确 Skill。不得调用本 Skill 的媒介参考自行补齐，也不得仅凭“由3D／实景／VFX／抽象导演负责”的标签放行。主导与全部必要辅助通过后，入口导演完成 `PROFESSIONAL_ROUTE_CONFIRM`，本 Skill 才进入 SHOT_GRAMMAR_CREATE。没有声明专业路由的简单孤立镜头按最小流程处理，但一旦核心专业事实未定，仍须路由而非猜测。

上游经过 Front-end Creative Reasoning Core 时，读取同一卡的 `shot_intent`。本 Skill 拥有最终 Shot Partition：一个 Intent 可以保留一镜，也可因信息、动作、视角或专业可行性拆为多镜；每个最终 Shot 保留原 intent_id 与 coverage_role。Shot Intent 只约束 why／must_show／audience_change／cut_trigger，不把上游的 viewing_intent 当成精确 Camera 命令。本 Skill 不静默改变 Target Change、Beat 或 Copy；需要改变时通过 change_requests 返回入口导演。

## 专业知识按需加载

主导证据是人物行为读 [实景](references/medium-live-action.md)，结构空间读 [工业三维](references/medium-industrial-3d.md)，Plate／虚拟附着读 [合成](references/medium-live-composite.md)，文字数据关系读 [VFX](references/medium-vfx-motion.md)，隐喻变换读 [抽象](references/medium-abstract.md)。这些参考只帮助镜头表达与核查，不能替代对应专业 Skill 的执行贡献。第二媒介对结论不可替代时才增加；不重复专业真源判断。

## 镜头设计和图板

先问观众看到什么新证据，再选择机位。静态卡写主体状态／位置／尺度、机位、前中后景、空间关系和冻结瞬间。草稿运动另进同一 GU.motion_card，不能把“然后／逐渐／环绕”当静态画面。完整项目与普通多镜段落默认 `STORYBOARD_FIRST`，具体规则读取 [故事板模式](references/storyboard-mode.md)。

多镜项目在专业贡献 PASS、最终 Shot Partition 与 Shot DNA 草案后、Director Shot Card／正式故事板前完成 Rhythm & Duration Pass：先继承全片与段落预算，再按最终视觉解法、片型、镜头功能、信息负载、动作完成下限和必要停留决定每镜 `duration_plan`。Shot Intent 的 timing_need 只是观看需求，不能直接充当秒数。时长与累计切点默认整数；只有明确 `FAST_CUT` 才可使用 0.5 秒步进，禁止 0.6、0.7、0.8 等任意十分位。预算冲突先删并、合并或重构，不等比压缩，不按镜头数平均。此 Pass 不新增用户确认门。

故事板每格只代表一个独立剪辑镜头的代表性 Frozen Moment，按叙事顺序在一张板上比较；图外显示镜号、累计时间范围、shot_function 与 rhythm_role。严格转场或复杂动作的首／中／尾 VN 进入独立 `TRANSITION_CONTROL_BOARD`，不得与正式故事板混排。默认一 VN 一方案，整段最多九个独立镜头优先一张板生成。单节点有真实未定表达才追加 3／6／9 候选，填写探索问题，不因默认不确定度自动抽六张。入选单帧检查尺寸、格子污染与结构；合格直接用，失败局部修，不要求每镜都有候选板。已有合格素材可以复用。

出图前为整个段落建立镜头组合差异合同，至少比较认知功能、观看立场、景别、方位、高度／俯仰、焦段／景深感、主体尺度／位置、空间层次、视觉载体和转场接口。普通快剪或广告故事板中，相邻独立镜头原则上至少改变三项；连续比较、产品身份建立、匹配转场或状态递进允许少改，但必须写明新增信息。可运动性检查空间余量、接触证据、姿态、运动线索、相机通道与终态可达；状态正确不代表动态必然成立。

## 控制与结果

出图前的 CONTROL_PREFLIGHT 使用已知目标与实际运行端能力，不假定所有参考可组合；入选帧后再次核对才 MOTION_LOCKED。相机、主体与环境分别描述，普通复合后拉上升可是一条连续轨迹。分轴参考只表达控制职责，不承诺物理独立和像素级复现。

文字证明意图，图片证明静态，视频证明时间与动态物理。动态检验需实际相关时间段；完整成片需实际回放。先记录失败症状和可能原因，按最小实验区分，再局部修复并检查耦合接口。父运行和变更范围保留。

## 工具与交接

正式 JSON 记录可运行 `python scripts/validate_handoff.py record.json --base-dir media_root`；与旧版比较用 `--previous old.json`；迁移用 `--migrate new.json`。工具只做确定性检查，输出通过不等于图像／视频通过。新旧字段冲突必须显式处理。

维护多个 Skill 的公共政策时运行 `python scripts/check_policy_consistency.py --root personal_skills_root`。行为病例和证据标准见 [评测](evals/rubric.md) 与 `evals/cases.json`；实际回归命令 `python scripts/test_validate_handoff.py`。不要为了普通镜头调用全部开发检查。

交接使用 from_skill／to_skill／pipeline_mode／object_ids／completed／locked／unresolved／change_requests／next_gate，gate_id 和 owner 按 v1.2 规范。返回 PASS／RETRY／REVISE／BLOCKED、实际证据、最小动作和下一门；缺媒体时标为待验证，禁止用协议 PASS 替代 RESULT_VALIDATE。平台编译交对应编译器。
