---
name: event-venue-kit
description: 当使用者说"给我们的活动做个网站"、"展会/开放日/校园导览/博物馆/市集要一个手机导览站"、"做个可以拖动的 3D 楼层图"、"展位地图和路线导航"、"每个展商/学校一页"、"像 College Fair 那个网站一样好看"时使用。适用于有真实场地的活动网站：入口首页、实体列表与搜索、实体长页、3D 场地图、分步路线、主题路线、印刷物同源。方法来自一个很受欢迎的大学展网站，但每个项目先抽一个设计方向，不复制原站外观；原站外观只在使用者明说时作为规范出口取用。不编造场地几何，不随包分发第三方校徽、照片和字体。
category: coding-helper/ui-design
version: 0.1.0
status: draft
priority: P1
compatible_agents:
  - claude-code
  - codex
  - cursor
  - generic-llm-agent
display_name: 活动与场馆网站套件
outputs:
  - chat
max_rounds: 40
suggest_hint: 给活动做网站？用「活动与场馆网站套件」先抽一个设计方向，再用现成的 3D 场地图、路线和弹层引擎
---

# 活动与场馆网站套件 / Event Venue Kit

给一个**发生在真实场地里的活动**做手机优先的网站：入口首页、实体（展位、学校、展商、展品）列表与长页、可拖动的 3D 场地图、分步路线。

这套方法来自 SDSZ College Fair 网站（Varsity '28）。要带走的不是它长什么样，而是它怎么长出来的：
1. 身份从活动自己的实物里推出来；
2. 一层质量地板托住所有细节；
3. 一套手写的地图与动效引擎让它好用。

所以每个新项目都先**抽一个设计方向**，原站只是方向池里权重很低的一张牌。

## 何时使用 / When to use

- 学校活动、展会、开放日、市集、博物馆、校园导览、会议，需要一个手机上看的网站。
- 要做楼层图、展位地图、3D 场地图，或者"从我在的地方走到某个展位"的导航。
- 有一批实体（学校、展商、摊位、展品），每个都要一页，并且要能搜索。
- 使用者说"要好看""不要模板味""像 College Fair 那个网站一样"。

**不适用于** / Not for：
- 没有场地的普通落地页或产品官网：用 `ui-design-system-builder` 从项目意象推 token。
- 想直接套 MaestrWave 那套深色衬线视觉：用 `maestrwave-ui-system`。
- 已有完整品牌规范、也不需要地图：照规范实现。本套件里只有地板（`references/floor.md`）还用得上。

## 三层 / Three layers

| 层 | 内容 | 随机？ | 在哪 |
|---|---|---|---|
| 地板 Floor | 对比度角色与实体色算法、双语层级、CJK 断行、触控与焦点、减弱动效、只为状态而动的弹簧、地图静止不重绘、UX 契约 | 否 | `references/floor.md`、`references/ux-contracts.md`、`assets/floor/base.css` |
| 表面 Surface | 配色结构与色相、展示与标签字体、形状语言、分隔线、实体页头、地图标记、数字样式、导航呈现、地图投影与材质、动效性格、密度 | **是**：先整套抽方向，再在方向包络内抽参数 | `library/directions.json`、`assets/recipes/<方向>.css`、`references/randomness.md` |
| 引擎 Engine | 伪 3D 场地图、网格寻路与分步文字、弹簧、底部弹层、分部导航、实体色计算 | 否；外观全部由 token 驱动 | `assets/engine/*.js`、`assets/engine/venue.schema.json` |

## 流程 / Process

1. **读项目，把硬要求翻成冻结项**：已有品牌色、logo、字体、平面图、实体名单吗？brief 里白纸黑字的要求，抽牌前就写成 `--keep`：
   - 品牌色 → `--keep palette=#主色,#强调色`；指定字体 → `--keep display="字体名"`；
   - "可旋转 / 能转" → `--keep projection=rotate`（orbit 或 exploded）；"3D、能看到几层、不必转" → `--keep projection=3d`；"平面图就行" → `--keep projection=plan`；
   - 以中文为主（中文为主或只给中文读者）→ `--keep lead=zh`；双语且现场有外国访客 → 默认 `lead=en`，或按 brief 定。
   - **没有平面图就问要平面图**（照片也行）。不要凭空画楼。实在没有，只画示意，并在页面上写"示意图"。
   - 场地数据写成 `venue.json`（格式见 `assets/engine/venue.schema.json`：房间、开放区或走廊、中庭挑空、楼梯电梯、实体、活动信息）。写完先跑 `node assets/engine/wayfind.js --selftest 你的 venue.json`，所有起点到所有实体都要走得通。
2. **盘点活动的物理世界**：按 `references/derive.md` 的问题清单列出 8–12 件只属于这个活动的东西，并打上标签。没有照片时按常识推断，标"假设"，交付时请使用者确认。
3. **抽牌，看样张，再选**：按 `references/randomness.md` 跑 `draw.py`（三张牌），再用 `specimen.py --venue 你的 venue.json` 出三页样张（用这个活动自己的名字和场地）。
   - 不能下载字体时加 `--offline`，样张才和成品一样用系统回落字体。
   - 在浏览器的**前台**标签里打开三页看过再选（后台或隐藏的窗格里画布不绘制）。
   - 开不了新标签时：
     - 先关掉自己以前开过、已经不用的标签；
     - 仍不行，用 `specimen.py --png` 让本机 Chrome 无头渲染截图来看；
     - 连 Chrome 也没有，就按牌面参数、recipe 和 lint 结果比较，交付时写明"样张未在浏览器里看过"。
   - 理由要点名盘点里的一件实物。选定之后要改参数用 `draw.py adjust`，再 `install.py --update`；不要重抽、也不要手改 `roll.json`。
4. **落地**：`install.py --starter --venue 你的 venue.json` 写入 token、`base.css`、所选方向的 recipe、引擎、项目自己的 `DESIGN.md`，以及一套能用的页面骨架：首页、地图页（路线弹层、搜索、URL 状态、无 JS 名录）、每个实体一页。在骨架上改，不要从零写胶水代码。
   - **字体**：牌上的字体都是免费字体，但套件不带字体文件，页面运行时也不向第三方请求字体（地板 F27）。
     - 先问使用者能不能下载字体。能，就按 `references/print-parity.md` §5 自托管并裁成子集。
     - 不能，就用 token 里的系统回落字体栈，并在 `DESIGN.md` 写明"字体：系统回落"。
5. **把页面做满**：骨架已经满足 `references/ux-contracts.md` 的契约；改动时别破坏它们。
   - 方向自带的品类道具（`directions.json` 里的 `props`，如标本叶形、网点、盾形）只在盘点清单支持时保留；不支持就把对应的 `--prop-*` 设成关闭值。
   - 再用以下文件把细节做满：
     - `references/craft-details.md`（界面）
     - `references/reading.md`（实体长页）
     - `references/map-craft.md`（地图）
     - `references/wayfinding-copy.md`（路线文案与搜索）
     - `references/print-parity.md`（门牌、告示、二维码、徽章、照片）
6. **检查**：
   - 跑 `lint_floor.py` 和 `similarity.py`；
   - 在 375 px 宽、浅色和深色下各看一遍（深底方向的"浅色"也是深底，这是预期）；
   - 地图拖动和捏合；
   - 走一条跨楼层路线；
   - 对照 `references/floor.md` 逐条看。`lint_floor.py` 只查 token 和样式表里能静态看出的东西；按钮、填色标签、按下的分段按钮里的字要在浏览器里亲眼看。
   - 浏览器会缓存样式和脚本，改完看不到变化时，给资源地址加内容哈希或 `?v=`。
   - 踩过的坑在 `references/lessons.md`。
7. **记录**：把方向、预设码（它能复现这张牌）、抽牌种子、改过的参数写进项目的 `DESIGN.md`。以后在这个项目里继续做，先读它。

## 速查 / Quick reference

```bash
python3 scripts/draw.py --tags campus,science --keep projection=rotate --out .evk/roll.json   # 抽三张牌（--keep / --steer / --canon）
python3 scripts/specimen.py .evk/roll.json --all --venue data/venue.json --out .evk/specimens   # 每张牌一页样张，用自己的场地（不能下载字体加 --offline）
python3 scripts/draw.py choose 2 --reason "…" --roll .evk/roll.json       # 选定并写历史
python3 scripts/draw.py adjust pitch=30 --reason "…" --roll .evk/roll.json   # 选定后改参数（不重抽，记进 adjusted）
python3 scripts/install.py .evk/roll.json ./site --starter --venue data/venue.json   # 落地：token、样式、引擎、页面骨架
python3 scripts/install.py .evk/roll.json ./site --update                 # adjust 之后只重写 token 与 roll
python3 scripts/tones.py "#8C1515" --roll .evk/roll.json                 # 一个实体色的全部角色（按这张牌的纸色与夜色）
node assets/engine/wayfind.js --selftest data/venue.json                 # 场地数据：每个起点到每个实体都走得通
node assets/engine/wayfind.js --describe-all data/venue.json --from entrance:1F   # 从入口到每个实体的分步路线（JSON，起步页用它生成静态"怎么走"）
python3 scripts/lint_floor.py site/evk/tokens.css                         # 地板检查
python3 scripts/similarity.py .evk/roll.json                              # 与原站的指纹距离
```

| 要做什么 | 读哪份 |
|---|---|
| 从活动推身份、标签词表 | `references/derive.md` |
| 抽牌规则、何时重抽、降级做法 | `references/randomness.md` |
| 必须守住的规则 | `references/floor.md` |
| 每个 UX 部件的契约与可变呈现 | `references/ux-contracts.md` |
| 界面微细节（梯度、细线、按压、深色） | `references/craft-details.md` |
| 实体长页、块词汇、阅读导航 | `references/reading.md` |
| 3D 场地图的全部手艺 | `references/map-craft.md` |
| 路线文案、搜索、URL 状态 | `references/wayfinding-copy.md` |
| 门牌、告示、二维码、徽章、照片、文案语气 | `references/print-parity.md` |
| 原站踩过的坑 | `references/lessons.md` |
| 原站完整规格（只在使用者要原站外观时） | `references/reference-direction/DESIGN.md` |

## 红旗 / Red flags

出现任何一条，说明你正在滑回默认值或复制原站。回到对应的步骤：

- 还没跑 `draw.py` 就开始写 CSS。
- 只看了方向名，没打开样张就选了。
- 选择理由里没有盘点清单上的任何一件实物。
- 页面上的母题来自品类，而不是这个活动。比如科学节就用元素周期表，书市就用邮戳。
  - 换成盘点清单里的东西，或者写清楚它为什么就是这个活动的东西。
- 页面上出现倒计时胶囊、底部 Tab 栏、入场依次上浮这类"活动网站标配"，但说不出它服务哪条 UX 契约。
- 双语靠切换按钮把另一种语言藏起来，而 brief 没说只用一种语言。
  - 现场人群是混合的。两种语言同时出现、分主次，见 `references/floor.md`。
- `similarity.py` ≥ 0.5，而使用者没要原站外观。
- 地图在不动的时候还在跑 `requestAnimationFrame`，或者动效用的是固定时长的缓动、不能从当前速度接手。

## 输出格式 / Output

交付时一次说完：

````markdown
**方向**：<方向名>（预设码 <EVK1-…>，抽牌种子 <draw.py 打印的 seed>）；三张牌是 <A> / <B> / <C>，选 <B> 因为 <盘点里的实物>
**冻结**：<--keep 的内容，或"无">
**页面**：<做了哪些页面和部件>
**检查**：lint_floor <通过/问题>；与原站相似度 <x>；375 px 浅色/深色、地图手势、跨楼层路线 <结果>
**我替你定了的**：<方向内手调的参数 + 理由 + 怎么改回去>
````

## 边界 / Boundaries

- **不编造场地。** 楼层、房间、门、楼梯来自平面图或使用者确认的数据。示意图必须标"示意"。
- **不随包分发第三方素材。** 校徽、logo、照片要有授权并注明出处（做法见 `references/print-parity.md`）。套件本身只提供标记渲染器的插槽。
- **不放个人信息。** 学生姓名、班级、联系方式默认不上页面，除非使用者明确要求，且有当事人同意。
- **品牌和 brief 优先于抽牌。** 抽牌只决定 brief 没有决定的部分。
- **原站外观只在被要求时用。** 使用者明说"一样的"或"同一家族"，才用 `--canon`。

## Token 控制 / Token discipline

- 先读本文件、`references/randomness.md`，以及 `references/derive.md` 的问题清单与标签词表。其余参考按上表在做到那一步时再读，并且只读用得上的小节（各文件开头有目录）：没有长页就不读 `reading.md`，没有印刷物就不读 `print-parity.md`。
- `library/directions.json` 让脚本去读，不必整份读进上下文；要看某个方向，只看那一项。
- 样张用浏览器看，不要把样张 HTML 读进上下文。

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.0 | 2026-10-24 | 初始版本：方法与细节总结自 SDSZ College Fair 网站；三层结构（地板 / 抽牌表面 / 引擎）；12 个方向（含原站规范出口，色相分家族），抽牌带历史降权与手内差异；无框架引擎（场地图、寻路、搜索、弹层、阅读导航、实体色）与起步页骨架；经五轮独立实做测试修订 | minor |
