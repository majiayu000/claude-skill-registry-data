---
name: figma2html
description: Use when you have a figma design frame (or several) and want to turn it into a high-fidelity, runnable HTML client — pixel-faithful rendering plus declared interactions (modals, data binding, guards). For figma-sourced UIs; non-figma authoring (brief/screenshot) goes through the 界面 DSL instead.
---

# figma2html — figma 节点树 → 高保真可跑 HTML

## 这个 skill 干什么

figma 帧 → **全保真 `.ui.json`(像素)** + **`flow.json`(声明的交互/Events)** → 通用引擎组装成**可点可跑**的 HTML 客户端。

- **像素**:`figma_capture.py` 把每个可见节点 + 全部样式抠成 `.ui.json`,`render.js` 1:1 重建 DOM。
- **交互**:figma 没有交互逻辑,**Events 在 `flow.json` 手写**(按 figma node id、抗重抓);`assemble.js` 读 flow 把"底屏 + 弹窗叠加 + 事件 + 绑定"装起来。**域内语义(数据→行、回填、状态色)由 app hook 注册**,引擎不写死。

边界:**figma 进 → 本 skill**(像素优先);**非 figma 进(brief/截图)→ 界面 DSL → ui_render**(语义优先)。两边共享 figma node id 键空间 + Events 语法。

## 内容

```
scripts/   figma_capture.py(节点树→ui.json+tree.html)· flow_from_figma.py(figma 原型交互→flow.json 初稿)
           subset_font.py(字体子集woff2)· shoot.py(Edge无头截图)
           tests/(capture 冒烟:夹具→断言 records;`python3 scripts/flow_check.py <flow.json>   # 手写完 flow.json 先跑这个:坏引用离线就报,
                                            # 别等浏览器里"点了没反应"才发现
python3 scripts/tests/run_all.py`)
runtime/   render.js(ui.json→DOM,subtreeOf抽子树)· assemble.js(通用引擎:flow→底屏+弹窗+事件+绑定)· app.tmpl.html
references/ ui.json-schema.md(含「已知限制:旋转」)· flow-events.md(flow/Events 契约)
examples/login/ 自足可跑示例(**合成**):make_fixture.py 手搭三屏节点树 → 走真 capture 管线 + flow.json + app.js + net.js(mock)+ app.html + README。演管线本身,界面刻意最小
examples/mail/  自足可跑示例(**真 figma 捕获**):四屏 + 三个弹窗 + 图片填充 + 设计字体子集 + bundle.py。演合成夹具够不着的那半 —— 实例 id 带分号、描边带是预裁环、isMask 圆角、椭圆角,以及 `@in:` 弹窗内按钮与「原地换态」这类只能由 app hook 做的语义
```

## 用法(管线)

1. **拉节点树**:figma REST `/v1/files/<key>/nodes?ids=…&geometry=paths` → `nodes.json`(token 只进单子进程、用完即删)
   **`geometry=paths` 别漏**:带上它 figma 才给每个矢量的 SVG 路径,矢量于是**画出来**而不是下成图 ——
   不吃 `/v1/images` 的渲染配额(真会被打爆)、分辨率无关、改色不用重导、下游引擎拿到的是几何不是位图。
2. **捕获**:`python3 scripts/figma_capture.py nodes.json <frameId> <sNN> <assetDir> <assetRel> <out>` → `.ui.json` + `.tree.html`
3. **导素材**:只有**真图片填充**才需要素材,走 `/v1/files/<key>/images`(按 imageRef,**不卡配额**)。
   矢量默认走 §2 的路径、不下图;只有拿不到几何的才回退 `/v1/images`(**有配额,能打爆**)。
   素材 PNG **必须与 `absoluteBoundingBox` 同尺寸**:figma 出图按渲染边界(含阴影外溢),直接用会被缩放居中、系统性错半格。
4. **字体**:`python3 scripts/subset_font.py <font.ttf> fonts/cjk.woff2 <ui.json...>` → 几十 KB,@font-face 离线可移植
5. **flow.json —— 先导后补,别从零手写**
   - 导:`python3 scripts/flow_from_figma.py nodes.json flow.json base=<a>.ui.json <name>=<b>.ui.json …`
     把 figma 里已经连好的原型交互(`interactions[]`:overlay / back / 转场)变成初稿。
     **搬不动的逐条报在 stderr 并说明原因,绝不猜** —— 猜错的事件长得跟对的一模一样。
     加 `--motion-defaults` 还会把**引擎自己拥有的机制**的默认动效一并写进草稿:
     按下态 / 弹窗入场**与出场** / 列表逐项 / guard 拒绝时抖一下。
     (真实 figma 文件多半没连原型线;而点下去毫无反应的按钮,玩家读到的是"卡了"。)
     优先级恒为 **figma > 项目覆盖 > 预设**,补进来的每条带 `source`,看得见、能改能删、重跑不重复。
   - 补:守卫 guard / 列表 list / 绑定 bindings / app hook —— 这些是**应用语义**,figma 里根本没有,
     照 `references/flow-events.md` 手写。(v1.0 已知缺口:events 只能绑 base 屏,弹窗里的关闭按钮要手写 `@panelOutside:<modal>`。)
6. **组装**:`app.tmpl.html` 套 `render.js + assemble.js + flow.json + app.js(hook)` → 可跑;`python3 scripts/shoot.py <url> out.png` 截图核验

## 关键规则(都在 figma_capture / assemble 里)

- **只有纯矢量簇才折叠成图**:簇内但凡有能直接写出来的形状(带填充的矩形/椭圆/文字)就**下沉递归**,把圆角、实色、渐变写成真节点;只有纯矢量簇(且有导出 PNG)才整块折成一张图,缺 PNG 则留透明占位。**figma 里不是图片的东西,不该在任何后端变成图片** —— 否则产物退化成"截图+热区":改色要重导、位置只能靠位图对齐、下游引擎拿到的全是位图。
- **素材 PNG 必须与 `absoluteBoundingBox` 同尺寸**:capture 按 boundingBox 定位、`contain` 贴图,而 figma `/v1/images` 是按**渲染边界**出图(含阴影/描边外溢),直接拿来用会被缩放居中 → 系统性错半格。导出时按 boundingBox 裁/补齐再落盘。
- **图片填充按 imageRef 命名** → 跨屏复用、可直接喂 figma 导出。
- **阴影圆角修正**:无圆角但带 DROP_SHADOW → 继承铺满圆角子的圆角。
- **架构 = 底屏 + 弹窗叠加**(非一屏屏 swap):底部 UI 只一份,弹窗 `subtreeOf` 抽子树叠加 + 遮罩 → 状态不跨屏串。
- **引擎 vs hook**:`assemble.js` 管结构/机制(底屏/弹窗/事件/守卫/勾选/列表克隆);`app.js` 管域内语义(数据→行、回填、状态色)。
- **capture 拿不到的 → app hook 覆盖**:figma 实例内部子节点常无 `relativeTransform` → `rot` 回退 0(API 限制,见 references「已知限制:旋转」);任何 capture 取不到或想做设计覆盖的视觉(角度、菱形宝石等),在 hook 按 `data-id`/`data-name` 定位手改,别去捕获层硬凑。
- **改样式同步两处**:`figma_capture.py rec_to_css`(出 tree.html 预览)与 `render.js applyRecStyle`(出运行时 DOM)是同一套贴样式逻辑,改一处必同步另一处(`../../` 路径差是有意的,别对齐)。

## 硬约束

- UTF-8 无 BOM。**FIGMA_TOKEN** 只读进单子进程、绝不进对话/文件/CHANGELOG、用完即删。
- **figma_capture.py 主拷贝在本 skill**;同级 `figma2dsl/scripts/` 持镜像(其 tests 有 parity 守卫)。改捕获逻辑只在这里改,再同步过去。
- 运行时全局名 `window.FigApp`(app hook 一律用 register(app) 的形参,别直引全局);子集字体族名 `FigCJK`。
- **下游引擎后端**:同级 `figma2unity / figma2godot / figma2cocos` 消费本 skill 产的 `.ui.json + flow.json`(它们不含 capture,只做编译/解释)。
- 跳隐藏节点(visible:false / opacity≈0 / 0尺寸)。
- 服务端零依赖(Node)即可:POST /api + SSE + 静态服务(**.woff2 MIME**)。
