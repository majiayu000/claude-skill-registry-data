---
name: pi-sub-agent
description: 将具体执行委派给 pi coding agent + ZenMux 便宜执行模型（默认强档 deepseek/deepseek-v4-pro：1M 上下文、推理型；廉价快档 inclusionai/ling-3.0-flash：256K、非思考、更省），Claude 负责任务-模型匹配判断、任务书编写、驱动（一次性 pi -p 或 tmux 交互长程）、硬超时重试、独立验收与失败裁决。含双模型选型、3D 素材来源、Spec-Driven、强类型可验证节点、推理档位开关等最佳实践。触发词：pi 委派、把执行外包给便宜模型、deepseek、deepseek-v4-pro、v4 pro 执行、ling、ling-3.0-flash、ling flash 执行、pi sub agent
license: MIT
allowed-tools: "Read,Write,Edit,Bash,AskUserQuestion"
version: "2.1.0"
---

# Pi Sub-Agent：贵模型编排，便宜模型执行

把写码/生成类执行工作委派给 `pi + zenmux`，Claude 只做编排、驱动、验收。省的不只是钱，更是 Claude 自己的上下文——执行细节全部留在 pi 会话里，Claude 只接收结论。

> **两个执行模型，按任务选**（都经 ZenMux 聚合，复用同一 ZenMux key）：
>
> | | `deepseek/deepseek-v4-pro`（默认/强档） | `inclusionai/ling-3.0-flash`（廉价快档） |
> |---|---|---|
> | 上下文 | 1M | 256K（pi 显示 262K） |
> | 推理 | **推理型** `reasoning=true` | **非思考** `reasoning=false`（ZenMux 上 `reasoning_effort=none` 仍漏少量 reasoning） |
> | 多模态 | 无（纯文本） | 无（纯文本） |
> | 计费 /M token | ~$0.44 输入 / $0.87 输出 | 2026-07 ZenMux **促销期免费**（07-23 上线，正式价待定——**别把"免费/便宜N倍"写进长期结论或对外话术**，随时会变） |
> | 适合 | 复杂调试、多轮联动、需推理的任务 | 结构化转换、模板化组装、照确切 spec 施工的高频快活 |
>
> **选型原则**：任务难度高 / 要跨多轮推理纠错 → deepseek-v4-pro；任务形状规整、有强类型可验证节点、主要是"照 spec 装配" → ling-3.0-flash 更省更快。拿不准先按 §0 匹配表判断，宁可起手用强档。**下文正文以 deepseek-v4-pro 为默认书写；用 ling 时叠加下面的「ling 实测画像」，纪律收得更紧。**
>
> **方法论溯源（诚实标注）**：本 skill 的核心方法论与多数「坑」来自 **ling-3.0-flash 的实测对照实验**（含 2026-07 一次 xlsx→TS 建站长程实测，见「ling 实测画像」）。`deepseek-v4-pro` 能力档更高，凡标 `⚠️待实测` 的模型专属弱区判断是**尚未在 deepseek 上独立复测的稳妥默认**，按保守做法执行、别当已验证结论。与模型无关的流程纪律（Spec-Driven、独立验收、硬超时、失败裁决）与**仍走 ZenMux 通道**的坑（请求级死挂）对两个模型都适用。

### ling-3.0-flash 实测画像（2026-07，一次干净的 xlsx→TS 数据站长程实测）

带 `tsc` 可验证节点、无空间几何的 TS 建站任务上，ling-3.0-flash 能产出专业成品，但短板明确、纪律要更紧：

- **强区（放心交）**：结构化 `NL→typed JSON + Zod/schema 校验`（R0 一次过，stats 全中）；模板化组件组装；Recharts 图表配置（4 图中 3 图数值一次全对）；**照 Claude 给的确切代码/比较器施工**。
- **实测弱区（必须防）**：
  1. **自报双向都不可信**——自报 "$1.31k" 实渲染 "$1.31b"（代码对、话报错）；反过来也会报"已完成"而实际长歪。**一律 Claude 亲自渲染/断言核对**（§5）。
  2. **模糊逻辑反馈会带歪**——排序"null 恒沉底"用口头描述反馈，它复现了 `-cmp` sign-flip 没修对；**把确切比较器/数值贴给它才一次过**（§4 的"确切值反馈"对 ling 是硬要求，不是可选）。
  3. **琐碎清理会空转**——R4 打磨时一个 `TS6133 未用变量` 让它对同一报错循环 5+ 次不收敛；**盯 §3 第二种"有输出无进展"死循环，及时打断并贴确切一行修法**（或按 §6 机械小修 Claude 直接接手）。
  4. **非思考档**：无自适应推理兜底，跨多轮复杂调试更易架构漂移——这类任务优先给 deepseek-v4-pro。
- **纪律加码**：§0/§0.1 的"剥离空间推理/开放式设计"对 ling 收得更紧；反馈永远给确切值不给口头；每轮验收不省。

## 0. 先判断值不值得委派（最重要的一步）

原则不变：**执行模型能力 < 任务难度时，委派比自己写更贵**（驱动开销 + 返修轮次可能反超）。deepseek-v4-pro 能力档明显高于 ling 级，这条风险显著下降，但不为零——仍先做任务-模型匹配：

| 放心委派 | 需谨慎 / 剥离弱项后再委派 |
|---|---|
| 逻辑/状态机、CRUD、模板化页面 | 复杂空间几何推理（尺度归一、bbox、Raycaster 命中）`⚠️待实测` |
| 结构化转换：NL→JSON、schema 约束输出 | 开放式设计决策（该 Claude 定，别外包） |
| 单文件或多文件自包含产物、按明确 spec 施工 | 需要跨很多轮的复杂调试（给它推理档 + 强类型可缓解，见 §1/§2） |
| 资源核验（会自己 curl/API 确认 URL 存在） | 视觉/听觉自检（**无多模态**，见 §5） |
| 视觉/美术导向产物（**按 §0.2 拆成"眼睛/手"后可委派**） | 单轮产物体量超过执行方 `maxTokens`（见 §2.4） |

设计任务时主动**把最容易翻车的部分从执行方职责里剥离或前置**（如：空间数学放进确定性代码层由 Claude 预算，只让执行方做 NL→命令翻译 / 照 spec 装配）——同一个模型，任务形状对了，成绩能翻几个档。

### 0.1 资源/3D 类任务：复杂空间推理仍建议 Claude 预算 `⚠️待实测`

两条对执行方友好的形状，共同点是不让它同时既设计几何又算空间关系：

- **要真实/复杂模型** → 别让它手搓几何，**把免费素材库入口当显式步骤写进任务书**，它只管加载、场景逻辑与交互调度。
- **要风格化/自建几何**（如 Q 版角色、磁带机）→ 让它堆 primitive，但**坐标、尺度、比例、朝向尽量由 Claude 预先算好写进 spec**，执行方做"照 spec 逐件拼装"。

**稳妥默认**：尺度归一（`updateMatrixWorld(true)` + bbox）、Raycaster 命中、自适应相机距离这类确定性数学，**由 Claude 预算成成品代码块贴进任务书**，执行方只粘贴不改公式。deepseek-v4-pro 推理更强、也许能自己做对，但这是历史上最易翻车处；复杂几何**至少**让它先复述空间方案再动手（Spec-Driven，§2）。（实测教训：任务书里 Claude 写错一句 `rotation.x=Math.PI/2`，执行方照抄不误——spec 正确性永远是你的责任。）

- **免费 3D/游戏素材来源**（可写进任务书，均于 2026-07 curl 200 复核）：
  - `https://threejsassets.com/` — three.js 就绪素材
  - `https://www.kenney.nl/` — CC0 游戏素材（模型/贴图/音效）
  - `https://github.com/Fasani/three-js-resources` — three.js 素材/工具资源索引
  - `https://github.com/KhronosGroup/glTF-Sample-Assets` — 官方 glTF 样例，raw 直链稳定可用（实测可作 rigged 替身模型）
- **免登录 rigged 替身模型的直链**（找不到特定角色时按规格降级用，raw 直连、可跨域 fetch，2026-07 复核 200）：
  - `https://raw.githubusercontent.com/mrdoob/three.js/master/examples/models/gltf/RobotExpressive/RobotExpressive.glb` — 带骨骼动画的机器人
  - `https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/main/Models/RiggedFigure/glTF-Binary/RiggedFigure.glb` — 简易 rigged 人形
  用替身时在页面**如实标注"替代模型"**。
- **别写进"免登录直链"任务书的坑**：poly.pizza 下载走 reCAPTCHA 实测 403，Sketchfab 要 OAuth——某些角色的免登录直链就是不存在。
- **3D 草图/运镜走 Blender MCP**：让执行方调 Blender MCP 用基础几何体搭布局、设摄像机轨迹，产出粗模当视频生成底稿，而非死磕手写几何。

### 0.2 视觉/美术任务：Claude 当眼睛，pi 当手

执行方无多模态，但**本 skill 总是被一个多模态 agent 调用**——所以"看"这件事本来就该留在编排侧。
别因为"它看不见"就放弃委派，而是把职责切干净：

| | Claude（眼睛 + 大脑） | pi 执行方（手） |
|---|---|---|
| 需求 | 读参考图 → **转写成文字规格** | 只读文字规格，永远看不到原图 |
| 架构 | 定坐标系/数据流/关键不变量 | 照 spec 施工 |
| 每轮 | 起服务、渲染、截图、**读图诊断 → 开数值处方**（§4） | 应用处方、跑 Claude 给的 harness（§2.3） |
| 判定 | 唯一有权说"画面对了"的一方 | **明确告知"不用自己验画面，我来渲染"** |

- **图 → 文字规格**至少要含：主色板（hex）、图层清单（天空/远景/中景/前景/道具）、构图比例、
  光照色温关系、每类物件的形状拆解。写完自问一句"只看这段文字，我能画出那张图吗"——
  **这份转写的质量就是产出的上限**。
- **别让执行方自证画面**。它不仅看不见，还会因为 shell 里的 `http_proxy` 把 `curl localhost`
  跑成 502 死循环（§3）。一句"渲染验收归我"能省掉整轮空转。
- **成本要如实预期**：每轮 Claude 都得读一张截图，读图 token 不可省。委派省下的是**代码输出
  token**（一个 900 行的单文件产物，这部分是大头），不是验收成本。做经济性结论时分开记（§6）。

## 1. 前置检查

```bash
pi --list-models 2>/dev/null | grep -iE 'deepseek-v4-pro|ling-3.0-flash' || echo "NOT-CONFIGURED"
```

`NOT-CONFIGURED` → 目标模型未接入。经 ZenMux 接入（复用现有 ZenMux key）只需在 `~/.pi/agent/models.json` 的 `zenmux` provider `models` 数组里加对应条目。**强档 deepseek-v4-pro**：

```json
{
  "id": "deepseek/deepseek-v4-pro",
  "name": "DeepSeek V4 Pro (ZenMux)",
  "reasoning": true,
  "thinkingLevelMap": { "minimal":"high","low":"high","medium":"high","high":"high","xhigh":"high","max":"high" },
  "input": ["text"],
  "contextWindow": 1000000,
  "maxTokens": 32768,
  "cost": { "input": 0.435, "output": 0.87, "cacheRead": 0.003625, "cacheWrite": 0 }
}
```

**廉价快档 ling-3.0-flash**（非思考，无 `thinkingLevelMap`；cost 促销期为 0，正式价出来后按 catalog 回填）：

```json
{
  "id": "inclusionai/ling-3.0-flash",
  "name": "Ling-3.0-flash (ZenMux)",
  "reasoning": false,
  "input": ["text"],
  "contextWindow": 262144,
  "maxTokens": 8192,
  "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
}
```

（ZenMux catalog id 与实时价用 `curl -s https://zenmux.ai/api/v1/models -H "Authorization: Bearer $ZENMUX_API_KEY"` 复核。若无 ZenMux key，跑 `/pi-setup` 配一个。）加完 `pi --list-models | grep -E 'deepseek-v4-pro|ling-3.0-flash'`：deepseek 应显示 `context 1M / thinking yes / images no`，ling 应显示 `context 262K / thinking no / images no`。再对目标模型发一条 `pi -p "回OK"` 冒烟确认联通。

**推理档位**：deepseek-v4-pro 是推理型，**委派编码任务建议开思考**（让它在"写-测-喂报错"里自查纠错）。上表 `thinkingLevelMap` 已把常用档位映射到 `high`（DeepSeek 低档位多为 `null`/不支持，映射到 high 最稳）。纯批量/低延迟的结构化转换任务想省 token，可临时压低。**ling-3.0-flash 无思考档**（ZenMux 上 `reasoning=false`，实测 `reasoning_effort=none` 仍会漏出少量 reasoning，无法完全关闭也无法调高）——它靠的是 tsc/schema 这类外部可验证节点纠错，不是内部推理，所以给它的任务**务必带强类型编译或 schema 校验**当兜底。

## 2. 写任务书（一次给全，不指望澄清）

任务书质量决定产出质量（即便执行方会推理，仍别指望它猜你的意图）。必含五要素：

1. **目标**：一句话 + 产物形态（如"单文件 index.html，无构建步骤"）。
2. **硬性约束**：技术选型、禁止事项（如"禁止手搓几何体"）、CDN/依赖方式。
3. **资源**：外部 URL **Claude 先自己 `curl -sI -L` 验证过再写进任务书**；把"先确认资源存在再用"写成显式步骤。
4. **验收标准**：写明你将如何验收（零 console error、截图哪些功能等），让它对着靶子施工。
5. **汇报格式**：完成后报告最终选用的资源 URL、验证方式、自检结果，以及**是否改动了你给的成品代码/坐标（应为「无」）**。

**spec 的正确性是你的责任**：执行方会**忠实执行**任务书，包括你写错的地方——它不会替你 catch spec bug。几何/坐标/朝向这类你替它算好的数，写进任务书前自己先过一遍脑子。

两条放大产出质量的写法：

- **施工前先对规格（Spec-Driven）**：复杂/多文件改动，先让它**复述任务并列出"本次要改哪些部分"**，你核对无误再放它动手。deepseek 有 1M 上下文，漏改风险低于 ling 级，但联动修改仍易架构漂移，先对齐一次比事后返工便宜。
- **优先强类型语言**：能上 TypeScript 就别用裸 JS。编译器的严格报错是它"写-测-喂报错"自愈闭环的**可验证节点**。同理批量结构化输出用 JSON Schema/Pydantic 约束。
- **「替换函数/整块重写」要显式写"删除旧的 X"**：实测执行方在"用新函数替换旧函数"时**容易留下旧定义**，JS 里重复的 `function` 声明是**致命 SyntaxError→整页白屏**。任务书里把"删除原 X"写成显式步骤；验收时优先对产物做语法检查（见 §5 第 2 条）。

### 2.3 没有编译器，就自己造一个可验证节点

给 ling 的核心拐杖是"强类型编译或 schema 兜底"。但有整类任务天然没有：**单文件 + CDN 的
前端产物**（无 tsc、无 schema，`node --check` 只能抓语法）、纯 canvas/WebGL 渲染、shell 胶水。
这时**由 Claude 写一个无头验证脚本，当任务书的一部分交付**，让它替代编译器：

```js
// Claude 预先写好；任务书写明"只运行，不修改"
await page.goto('http://localhost:8099/');
await page.click('#btnStart');
await new Promise(r => setTimeout(r, 2000));
const probe = await page.evaluate(() => ({
  errs:  window.__errs,                              // console + pageerror 收集
  h:     [-80,-40,0,40,80].map(x => terrainH(x, 0)), // 关键函数值域探针
  calls: renderer.info.render.calls,                 // draw call 上限
}));
```

要点：

- **断言给数值，不给形容词**：`terrainH` 在 `x∈[-80,80]` 必须落在 `[-8, 30]`；
  `calls < 400`；`errs.length === 0`。执行方要的是红/绿信号，不是审美判断。
- 把探针挂在 `window` 上（或导出）作为**硬性接口写进 spec**，否则每轮 harness 都要改。
- 无头跑 WebGL 需要 `--enable-unsafe-swiftshader --use-angle=swiftshader`；
  帧率会掉到个位数（"滑了 5 米速度 94 km/h"就是这么来的），但**画面正确性不受影响**，
  截图照样能用来判断渲染对不对。

### 2.4 产物规模 vs `maxTokens`：一条可以先算的硬约束

写任务书前先估产物行数，跟执行方的 `maxTokens` 对一下：

| 模型 | `maxTokens` | 单轮可写代码量（约 3 字符/token） |
|---|---|---|
| `ling-3.0-flash` | 8192 | ~25k 字符 ≈ **600–800 行** |
| `deepseek-v4-pro` | 32768 | ~100k 字符 ≈ 2500+ 行 |

超了就必须提前拆，二选一：

- **拆成多文件**（前端可用 `<script type="module">` 引外部 `.js`，依然零构建），每个单元单轮写得完；
- **禁止全文件重写**，任务书写死"只允许定点补丁 / 只输出改动的函数"。

不拆的后果是它中途被截断、或者自作主张精简掉一半功能还报"已完成"。
**产物量级本身就是选模型的一个理由**——900 行的单文件产物，光这一条就该走 deepseek 档。

## 3. 驱动

> 下方命令以 `--model deepseek/deepseek-v4-pro` 示例；用廉价快档时把它换成 `--model inclusionai/ling-3.0-flash`，其余流程一致。tmux 里也可用 `--model` 启动或进 pi 后 `Ctrl+P` 切换，发任务前**先看状态栏确认是目标模型**。

### 一次性任务：`pi -p`（含硬超时）

```bash
cd <工作目录> && pi --provider zenmux --model deepseek/deepseek-v4-pro -p "<任务书>"
```

**必须包硬超时**：ZenMux 偶发**请求级死挂**（进程 CPU 冻结、零输出，实测约 1/10 会话）。macOS 默认**没有 `timeout`**，用以下之一：

- 有 GNU coreutils：`gtimeout 600 pi --provider zenmux --model deepseek/deepseek-v4-pro -p "..."`
- 便携看门狗（无 coreutils）：
  ```bash
  pi --provider zenmux --model deepseek/deepseek-v4-pro -p "..." & PID=$!
  ( sleep 600; kill -0 $PID 2>/dev/null && kill $PID 2>/dev/null ) & WD=$!
  wait $PID; kill $WD 2>/dev/null
  ```
- 在本 agent 环境里：直接用 Bash 工具的 `run_in_background: true` 起 pi，再用 Monitor/轮询看输出——这天然带超时且不占前台。

超时后先 `curl -s -o /dev/null -w '%{http_code}' https://zenmux.ai/api/v1` 确认网关可达（秒回即可，404 也算通），然后原样重跑——瞬态故障重跑通常立刻成功。最多重试 2 次。

### 多轮/长程任务：tmux 交互会话（推荐，天然免 `timeout`）

同一会话连续多轮（保留 pi 侧上下文），Claude 轮询驱动：

```bash
tmux new-session -d -s pi-sub -x 220 -y 50 -c "<工作目录>"
tmux send-keys -t pi-sub -l 'pi'; tmux send-keys -t pi-sub Enter
# 首次启动可能出 trust-folder 提示（Enter 确认）；确认状态栏显示 deepseek/deepseek-v4-pro 再发任务
# 若默认模型不是它：进 pi 后可 Ctrl+P 切换，或用 --model 启动：pi --provider zenmux --model deepseek/deepseek-v4-pro

tmux send-keys -t pi-sub -l '<任务书或反馈>'; tmux send-keys -t pi-sub Enter
tmux capture-pane -t pi-sub -p | tail -40   # 轮询，间隔 20-60s；本 agent 里可用后台循环检测 "Working..." 消失来判空闲
```

**启动即挂起（job control quirk，实测高频）**：`pi` 一起就被 shell 挂到后台，`capture-pane` 返回**完全空白**、trust 提示都不显示。判据：`ps aux | grep '[p]i'` 看到 pi 进程状态为 `T`（stopped）。解法：`tmux send-keys -t pi-sub -l 'fg'; tmux send-keys -t pi-sub Enter` 拉回前台，trust 提示随即出现。别把空白 pane 误判为启动失败去重开。

挂死判定两条都要：
- **5 分钟零新输出** → 杀掉重开，计一次挂死；
- **有输出但无进展**（陷入重复执行相同 grep/自检命令的死循环）→ 同样按挂死处理，发一条打断消息或重开。

## 4. 修复反馈（结构化，限量）

验收失败时用结构化 bug 报告喂回：**「当前情况是…（含具体报错/截图观察），预期情况是…（引用验收标准）」**。一次只报一个问题域；坐标/数值类修复**把算好的确切值直接写进反馈**（执行方照抄=它的强项）。**同一问题最多 2 次反馈**——2 次修不好即触发裁决（§6），继续喂只会烧 token 不会收敛。

**视觉缺陷必须翻译成数值处方**。执行方看不见画面，"太白了""不好看"对它是纯噪音；
诊断（哪个参数错了）是 Claude 的活，它只负责施工。对照示例（均为实测）：

| 截图上看到的 | ❌ 无效反馈 | ✅ 数值处方 |
|---|---|---|
| 两侧白墙挡住天空 | "山谷太窄" | 侧壁项 `0.055*d*d` → `Math.min(0.0062*d*d, 21)` |
| 雪面全屏死白、没有体积 | "雪没层次" | `HemisphereLight` skyColor `0xdcecff`→`0x8fb9e2`、intensity `1.15`→`1.05`、`toneMappingExposure` `1.06`→`0.98` |
| 近处粒子是白色方块 | "雪雾很丑" | `PointsMaterial` 加 64×64 径向渐变 canvas 作 `map`，配 `depthWrite:false` |
| 角色脚下一块灰色多边形 | "阴影不对" | 删掉假接触阴影圆片，改依赖已启用的 shadow map |

规律：**处方 = 具体符号 + 旧值 → 新值**。给得出这个三元组才发反馈；给不出说明诊断还没做完，
先自己再读一遍截图，别把诊断工作转嫁给执行方。

## 5. 独立验收（绝不信任执行方自报"完成"）

执行方会自报 "All checks passed / 已完成"，照单全收等于没验收。Claude 亲自跑：

1. **外链**：产物里全部外部 URL `curl -sI -L` 逐个 200。
2. **静态 review / 语法检查**：API 用法、回调结构、明显 bug；单文件 web 产物**先抽出脚本体 `node --check`**（能一秒逮到重复声明/括号不配等致命 SyntaxError——这类会让整页白屏而 console 未必立刻可见）。
   ```bash
   awk '/<script type="module">/{f=1;next} /<\/script>/{f=0} f' index.html > /tmp/m.mjs && node --check /tmp/m.mjs
   ```
3. **运行时**：web 产物起 `python3 -m http.server` + agent-browser 打开——console 零 error、截图确认功能可见（含**手机竖屏视口**）、模拟点击/拖拽/按键验证交互；脚本类直接跑并断言输出。
4. 验收产物（截图、curl/node --check 结果）存盘，和结论一起写进运行日志。

deepseek-v4-pro **纯文本、无多模态**（catalog `input_modalities:["text"]` 复核）——看不懂截图/音频，做不了视觉自检。这正是运行时/截图验收必须由 Claude 亲自跑的原因：执行方连"页面长歪了 / 磁带被挡住看不见"都感知不到，却照报"已完成"。

连它能做的文本级自检也别过度指望：执行方起本地 server 后自己 `curl localhost` 可能因 shell 里的 `http_proxy` 一路 502、卡进"反复重试 curl"的死循环（§3 第二种挂死）。别让它自证运行时——直接告诉它"不用自己验，我来渲染验收"，把轮次省下来。

**视觉任务里，第 3 步不是闸门而是回路的一环。** 实测一个 three.js 场景的四个缺陷里有三个
（侧壁把山谷做成峡谷、环境光导致全屏死白、无贴图粒子渲染成方块）——**代码不报错、逻辑没问题、
console 干净**，只有把帧渲染出来看才发现。所以别把"渲染截图"排在最后当放行检查，
要**每轮都跑**：执行方改完 → Claude 立刻渲染读图 → 开数值处方（§4）→ 下一轮。
跑三轮截图比读三遍代码有效得多。

## 6. 失败裁决与记录

- 同一问题 2 次反馈未修复 → 判定**超出能力圈**：Claude 收回自己写、或重设计任务形状（见 §0）再委派。如实记录降级原因——这是数据不是丢脸。
- **纯机械小修（删死代码/改一个常量）Claude 可直接接手**，比再走一个委派往返更省（生产模式下，见边界）。
- 全程计量：pi 侧轮次、挂死/重试次数、Claude 侧驱动 token + deepseek 计费。事后对比"委派总成本 vs 自己写"，回填 §0 的判断表（尤其把 deepseek 的真实弱区补进 `⚠️待实测` 处）。
- **视觉任务的计量要拆两笔**：①执行侧代码输出 token（委派真正省下的）②Claude 侧读图 token
  （每轮一张截图，不可省，且随轮数线性增长）。只报总账会看不出委派到底赚没赚——
  轮数一多，②完全可能吃掉①。这也是判断"下次这类任务还委不委派"的唯一依据。

## 边界

- 密钥绝不进任务书/日志（pi 配置已用惰性 shell 读 ZenMux key）。
- 生产模式下验收通过即可交付，Claude 可在裁决后 / 对机械小修接手改码；若是对照实验/评测，执行方必须独立完成全部代码，Claude 只反馈不改码。
- tmux 会话任务结束后保留供用户复查，报告里给出 `tmux attach -t <session>`。
- 两个执行模型按开头选型表选：默认强档 deepseek-v4-pro；任务规整、有强类型可验证节点、主要是"照 spec 装配"时用廉价快档 ling-3.0-flash（叠加「ling 实测画像」的加码纪律）。全程计量时分别记录用的是哪个模型与其计费（ling 促销期为 0，正式价出来后据实回填）。
