---
name: laohan-daoyan
version: "2.1.2"
description: 老韩AI真人口播新episode的V5.1导演预制入口。分为导演初稿与一次最终复审，共用director-state.md并停在WAITING_FOR_FOOTAGE；不剪辑、不写Remotion、不渲染。METHOD_LAB仅在用户明确要求历史路线时使用。
---

# 老韩V5.1导演预制

本Skill是新episode默认导演预制入口，但不是另一套方法真源。当前方法只读取视频项目中的：

- `animation-method/director-system/method-v5.json`
- `templates/director-state-v5.md`
- `docs/Codex媒体生产接口规格.md`的“V5.1导演预制”部分

项目规则和上述文件优先于本Skill。不得把历史METHOD_LAB、V4 motion-plan或旧episode实现混入V5上下文。

## 路由

### 默认：V5.1新期导演预制

用户说“新建一期”“做导演初稿”“最终导演复审”“只做导演层”或同义表达时，固定进入本路线，并根据`director_draft`与`director_review`进入正确阶段。

### 例外：历史METHOD_LAB

只有用户明确说出“METHOD_LAB”“旧AST/双renderer”“恢复历史episode”之一时，才读取`references/method-lab-legacy.md`。不得根据缺少clean/SRT或看到旧文件自行切换历史路线。

## V5输入

1. 当前最终口播稿；它是内容真值，不在导演阶段改稿。
2. 视频项目的`method-v5.json`和`director-state-v5.md`。
3. 当前episode的`episode-config.json`与`09-导演/director-state.md`。
4. 如果Jeffrey已经提供真人原片，只用于观察显示方向、构图、人物位置、手势和安全区；不剪辑、不转录、不生成clean/SRT。

如果用户要求“新建一期”，从视频项目根运行`node scripts/new-episode.mjs <slug>`；已有当前episode时该命令会阻断，不复制或覆盖旧期。

## 第一阶段：三轮导演初稿

### 1. UNDERSTAND_CONTENT

- 提炼观众真正要理解的判断、论证关系、情绪推进和结尾记忆点。
- 判断哪些内容需要图形解释、真实素材、产品画面或只保留真人。
- 不把每句话机械变成动画。

### 2. DIVERGE_2_TO_3_DIRECTIONS

- 先从内容发散2—3个完整且本质不同的视觉方向，而不是罗列互不相关的特效。
- 各方向必须在核心视觉隐喻、空间组织、运动逻辑或素材角色上形成真实差异，不能只是换配色、换版式或不同特效组合。
- 每个方向说明视觉世界、段落推进、信息层级、真人与overlay关系、素材作用和潜在记忆点；至少一个方向必须突破通用文字/卡片/流程图组合，提出本期专属表达。
- 方向概念形成后，需要Remotion高级能力时才按需读取最小范围相关官方Plugin知识；不得一次加载全部知识，也不得因为本地未知提前降级创意。

### 3. CONVERGE_ONE_COHERENT_PLAN

- 按观众理解、原片构图适配、全片连贯性、手机可读性和记忆点选择一个最适合当前口播的统一方案，并说明取舍。
- 允许吸收另一方向中的一个强表达，但不得把多个视觉世界拼成风格混乱的混合体。
- 每个内容段写画面动作，并补一行：`执行提示：推荐能力或包 + 大致手法 + 时长/节奏 + 安全区与退场。`
- 拍摄前只写大致秒数；已有原片也不在本阶段虚构clean时间轴或精确帧数。
- 最终方案用一句话确认`LIGHTWEIGHT_RESULT_ONLY`视觉底线：手机可读大字、透明/无大面积实体底板、清晰色彩层级、内容专属视觉、完整进入—发展/转折—退出、眼睛/嘴/字幕安全区。
- 不固定字号、坐标、配色、旧组件、模板或高级效果数量。

初稿完成后写：

- `director_draft: COMPLETED`；
- `director_review: PENDING`；
- `status: WAITING_FOR_FOOTAGE`。

随后停止，不能在同一用户请求里自动进入最终复审。

## 第二阶段：一次最终导演复审

只有用户明确要求继续完善当前导演稿、最终复审或使用固定第二阶段提示词时进入。读取同一个`director-state.md`，不重跑完整初稿，不改变已成立的内容主线和视觉世界：

### DENSITY_REVIEW

- 逐段判断适合低、中还是高动画密度。
- 查真人或静态画面过久、密度失衡、只有字体动画而缺少关系/空间/过程/因果/真实素材表达、注意力竞争、高潮不足和跨段断裂。

### ADVANCED_EXPRESSION_CHALLENGE

- 只选择真正值得增强的位置，先明确观众理解任务和导演意图，再为每个重点位置在内部发散2—3个本质不同的候选；至少一个候选不能只是现有文字或卡片效果换皮。
- 根据视觉任务按需读取最小范围Remotion官方Plugin知识，不一次加载全部能力。
- 高级表达必须承担关系、过程、因果、空间或记忆任务，不能只增加字体弹入、放大或变色。
- 不因本地能力未知提前降低创意，也不把技术选择题交给Jeffrey。
- 使用以下非穷尽技术搜索地图提醒搜索维度，但不能逐项打勾或强制使用：Shared Element/形态连续变换；透明2.5D或3D/景深/视差/虚拟镜头；关系线/路径/节点/因果链/数据流程；遮罩/拆解/透视合成/corner pin/真实产品融合；粒子/拖尾/motion blur/shader；跨段空间转场和语义接力。必须允许发现地图之外的技术。

### COHERENT_RECONVERGENCE

- 选择最适合整片而不是最复杂的组合，检查效果之间是否争抢或重复；只把入选增强写回原分段，未入选候选不落盘。
- 补齐进入、发展/转折、退出、跨段接力、工程建议、节奏、安全区和等价实现。
- 不设效果数量配额；全片新增独立依赖包总数最多2项，Remotion core与已核验runtime能力可自由组合。
- 保留已成立部分，不推倒重写。

复审完成后写`director_review: COMPLETED`并继续保持`status: WAITING_FOR_FOOTAGE`，随后停止。

## 落盘与停止

唯一新增业务产物是当前episode的`09-导演/director-state.md`。新建episode产生的配置、状态和准入骨架不算导演产物；`_status.md`是必须同步的编排元数据，不是第二个业务产物。

完成时必须满足：

- `method: V5`；
- `workflow_revision: V5.1`；
- `status: WAITING_FOR_FOOTAGE`；
- 已绑定当前稿件版本；
- 内容理解、2—3个发散方向、最终统一方案均非空；
- 每个内容段都有画面动作和轻量执行提示；
- 高级技术、素材策略和拍摄后待确认项已记录；
- 最终方案明确确认轻量视觉底线。
- 初稿请求结束时是`director_draft: COMPLETED / director_review: PENDING`；最终复审请求结束时是`director_review: COMPLETED`。
- `_status.md`已把当前位置同步为对应的D1导演初稿或D2最终复审，并勾选正确阶段；已有raw但缺shooting record时不得把⑦误写为完成。
- 最后一次写入后实时运行`bash scripts/check-episode-contract.sh episodes/<slug> config`并取得PASS；不得引用窗口开始时的旧PASS，也不得用干净Git状态替代episode准入。

随后立即停止并向Jeffrey报告`director-state.md`地址。即使真人原片已经存在，也不得在本窗口继续剪辑或实现；下一制作窗口再读取导演状态进入⑧—⑪。

若实时config因registry/runtime漂移失败，必须报告实际错误并停止，不能手改executor lock。只有Jeffrey明确授权时，才可交由工作流受控迁移命令修复；修复后仍要重新运行实时config gate。

## V5禁止产物

本路线不得创建或修改：

- `clean.mp4`、转录、SRT和剪辑决定；
- `beat-sheet.md`、EDL、animation brief/AST、styleframe、animatic或旧renderer route；
- direct brief、source manifest的拍摄后时间轴版本；
- Remotion/React代码、candidate或final；
- 网络素材下载、发布或外部回复。

若这些产物已由其他阶段存在，只读判断边界，不在导演预制窗口重写。
