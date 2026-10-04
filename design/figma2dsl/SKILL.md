---
name: figma2dsl
description: figma 节点树 → 高保真界面还原 + 可交互 harness。两条产物:全保真 .ui.json(渲染真源,逐节点真样式不折叠)+ DSL .md(语义抽象,喂 aigd/KB)。要把 figma 设计帧导成"可还原/可点/可跑"的客户端、或导成结构化 DSL 时用。文法权威在 references/界面DSL规范-figma2dsl扩展.md;本 skill 只编排、不复制文法。可移植、项目无关。
---

## 这个 skill 能干什么

把 **figma 设计帧**(节点树 JSON)还原成界面,两条并行产物、各司其职:

| 产物 | 生成脚本 | 性质 | 用途 |
|------|---------|------|------|
| **`<屏>.ui.json`** | `figma_capture.py` | **全保真**(每可见节点 + 全部样式,不折叠) | **渲染真源**:harness `render.js` / 实际 app / aigd 还原 |
| `<屏>.tree.html` | `figma_capture.py`(同次) | 全保真静态预览 | 眼比设计稿 |
| `<屏>.md`(DSL) | `figma_to_dsl.py` | **语义抽象**(折叠+flat skin,有损是本职) | 给人读 / AI 按意图生成 / KB 检索 / 喂 aigd |

**核心认知**:折损不是 DSL 造成的,是"折叠+压扁"这套抽象选择。要**完全还原画面走 `.ui.json`**;要**语义/意图走 DSL**。唯一躲不掉的损失=矢量路径→栅格 PNG(与 DSL 无关,由 DOM 渲染目标决定)。

---

## 第0步 读真源(每次必做,用 Read)

- `references/界面DSL规范-figma2dsl扩展.md` — 增补规范(§0 双轨架构 + .ui.json schema + 坐标系/原图/parent/跳隐藏 + 样式字段)
- `scripts/figma_capture.py` — **全保真捕获**(主路径)
- `scripts/figma_to_dsl.py` — DSL 转写(派生语义视图)
- `scripts/ui_render.py` — DSL→html 渲染校验(给 DSL 用)
- `scripts/export_assets.py` — 素材导出(figma REST)

## 第1步 准备输入

- `nodes.json` — figma 节点树(REST API `/v1/files/<key>/nodes?ids=...` 拉)
- `frameId`、`屏名/NN`、`fileKey`、`outdir`、`_assets/s<NN>/` 素材目录

## 第2步 全保真捕获(主路径)

```
python3 scripts/figma_capture.py <nodes.json> <frameId> <sNN> <assetDir> <assetRelPrefix> <out_basepath>
# 产物: <out_basepath>.ui.json  +  <out_basepath>.tree.html
```

保留每节点:几何/旋转/不透明度/圆角/描边/阴影/模糊/填充(纯色含透明+渐变+图片)/文字(含字形描边)。关键规则:
- **资产感知折叠**:矢量簇有导出 PNG 才整组折叠成图;缺 PNG 则不折叠、递归渲染可渲染形状子(白盒/椭圆/底色),纯矢量叶子各自透明。配 `vector_leaf_count≤4 + has_renderable_shape` 守卫,避免密集矢量装饰爆 div。
- **图片填充按 imageRef 命名**(优先 `<imageRef>.png`,回退节点 id 名)→ 跨屏天然复用、可直接喂 figma 导出。
- **阴影方框修正**:节点无圆角但带 DROP_SHADOW 时,继承铺满圆角子的圆角。

## 第3步 导素材

- **图片填充**(底图/装饰/图标的位图):`GET /v1/files/<key>/images` 取 imageRef→URL 映射,下载存 `<imageRef>.png`。**不卡节点渲染配额**。
- **矢量节点渲染**(图标/勾号等):`export_assets.py` 走 `GET /v1/images?ids=...&format=png`,**有配额**(429 时 Retry-After 可达数天)。
- 缺图:`.ui.json` 里 `vec` 元素回退透明(不平涂黑);`img` 回退无背景。

## 第3.5步 DSL 转写(可选,喂 KB/aigd)

```
python3 scripts/figma_to_dsl.py <nodes.json> <frameId> <NN> <屏名> <outdir> \
       [--prefix screen] [--brand figma] [--file-key KEY] [--meta meta.json]
# 产物: <outdir>/<prefix>-<NN>.md + .nodes.json
```

- **项目无关**:file key 走 `--file-key`/环境变量 `FIGMA_FILE_KEY`;屏位元数据(用途/布局/标签/点评)走 `--meta meta.json`(项目私有数据放项目里,键=NN)。

## 第4步 渲染/校验

- 全保真:`.ui.json` 由 harness `render.js` 渲染(嵌套、绝对→父相对、逐节点真样式),Edge 无头截图眼比。
- DSL:`python3 scripts/ui_render.py <屏>.md <屏>.html` 渲染语义预览。

## harness(可点可跑客户端)参考实现

**已抽成同级 skill `figma2html`**(runtime 引擎 + 自足 login 示例),要"可点可跑客户端"直接用它;模式要点:
- **架构 = 底屏 + 弹窗叠加**(非一屏屏 swap):一个全屏底(底部 UI 只一份),弹窗用 `render.js` 的 `subtreeOf(cap, 根id|根id数组)` 抽面板子树叠加 + 半透明遮罩。状态(勾选/已选)才不跨屏串错。
- **字体内嵌**:`fonttools` 子集化(只收集本界面用字)→ 几十 KB woff2 + `@font-face` → 离线可移植。
- 服务端:Node 零依赖(POST /api + SSE /events + 静态服务)即可。

## 硬约束

- UTF-8 无 BOM。
- **FIGMA_TOKEN**:只读进单条子进程、绝不进对话/文件/CHANGELOG;只验长度不验值;用完即删。
- 跳隐藏节点(`visible:false` / opacity≈0 / 0尺寸)。
- 不改 aigd 原件;本 skill 自带 bundle 副本。文法以规范页为准。
- **figma_capture.py 主拷贝在同级 `figma2html/scripts/`**,本处为镜像;`tests/test_capture_parity.py` 守两份逐字节一致(兄弟目录不存在时跳过)。
- 测试:`python3 scripts/tests/run_all.py`(改 figma_to_dsl / ui_render 后必跑,勿回归)。
