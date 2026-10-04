---
name: figma2cocos
description: 把 figma2html 管线产的 IR(.ui.json 像素快照 + flow.json 交互声明)落到 Cocos Creator 3.x —— TS 运行时解释器(组件加载 ui.json 动态建节点树 + flow 绑定器)+ python 离线校验器(引用完整性 + 资产清单)。要在 Cocos 工程里还原 figma 界面与交互(底屏+弹窗/守卫/列表/勾选)时使用;capture 本身归 figma2html。
---

# figma2cocos — figma IR → Cocos Creator 3.x

## 这个 skill 干什么

figma2html 已把 figma 帧变成 **`.ui.json`(像素真值)+ `flow.json`(声明的交互)**。本 skill 是这套 IR 的
**Cocos 落地端**:

- **TS 运行时解释器**(`runtime/`):`FigmaUI` 组件读 JsonAsset(cap)动态建节点树(Graphics/Label/Sprite);
  `FlowBinder` 读 flow.json 组装"底屏常驻 + 弹窗叠加 + 事件 + guard + 列表克隆 + checkbox",域内语义走
  `FigmaAppHook`(对齐 assemble.js 的 APPHOOK)。
- **python 离线校验器**(`scripts/ui_check.py`):不开 Cocos 就能测的部分——IR/flow 引用完整性 + 资产清单。

分工:**capture / flow 编写规范 → figma2html**;**HTML 落地 → figma2html**;**Cocos 落地 → 本 skill**。

## 内容

```
runtime/    parse-css.ts(rgba/渐变/radius四角/border/shadow 解析,纯函数)
            figma-ui.ts(@ccclass FigmaUI:cap→节点树;buildSubtree=弹窗抽子树;paintRect 复用)
            flow-binder.ts(@ccclass FlowBinder:flow→层/事件/guard/列表/勾选;FigmaAppHook 注册口)
references/ mapping.md(IR→Creator 映射全表 + 坐标转换推导 + known-loss 表 + 集成冒烟清单)
scripts/    ui_check.py(离线校验:caps 可载入、el id 引用完整、列表模板行、assets-manifest.json)
            bake_motion.py(flow.json → motion.json:转场缓动解成采样点,TS 侧只插值)
            motion.py(figma2html 主拷贝的**逐字节镜像**,tools/conformance 逐字节守)
            tests/(run_all.py 发现式 runner + test_ui_check.py + test_runtime_source.py;
                   fixtures/=figma2html login 三屏夹具)
```

## 用法(管线)

1. **capture**(figma2html):figma 帧 → `screen-*.ui.json` ×N + 手写 `flow.json` + 导出图片素材。
2. **离线校验**:`python3 scripts/ui_check.py <flow.json> <capDir>` —— 全部引用过了才进 Cocos;
   顺手产出 `assets-manifest.json`(去重图片清单)。
3. **烘动效**:`python3 scripts/bake_motion.py <flow.json> <outdir>` → `motion.json`
   (每条转场曲线 17 个采样点)。**曲线一律在 python 侧解算**,TS 侧只做线性插值 ——
   换成 Creator 内置的 `easing.quadOut` 之流就是同名不同形,与其它五个后端手感分叉
   (实测最大差 19.8 个百分点)。不烘也能跑,弹窗就是瞬时显隐。
4. **资产导入**:manifest 里的图放进 `assets/resources/<assetRoot>/`(保持 `_assets/...` 路径、文件名 stem 不变);
   `.ui.json` / `flow.json` / `motion.json` 拷进工程任意 assets 目录(Creator 自动导成 JsonAsset,名为路径 stem 如 `screen-login.ui`)。
5. **挂组件**:Canvas designResolution=cap.w×cap.h;根节点(锚(0,1)+Widget 左上对齐)挂
   `FigmaUI`(单屏预览,拖 capAsset)或 `FlowBinder`(整流程,拖 flowAsset + capAssets[] + motionAsset)。
6. **hook**:域内语义(数据→行、选中回填、状态色)写一个组件,在其 `onLoad` 里
   `FlowBinder.registerHook({ register(app){ app.registerActions({send, selectServer, onGuardFail, ...}) }, init(app){ app.renderRows(...) } })`
   —— 语义与 figma2html 的 `app.js`/`APPHOOK` 一一对应,`renderRows/openModal/setFlag/getNode` 同名同义。
7. **冒烟**:按 `references/mapping.md §6` 清单逐项核(几何对照截图、事件逐个点验)。

## 硬约束

- **坐标转换是本 skill 的命门**:IR 是 y 向下/左上原点的绝对 px,Creator 是 y 向上/锚点系。
  约定 = 每节点锚 (0,1),`child.position = (dx, -dy)`;旋转节点换锚 (0.5,0.5) 补偿。改动前必读 `references/mapping.md §2/§3`。
- **TS 验证等级(2026-07-31 复跑)**:三件 runtime TS 已过 **严格类型编译门**(tsc --noEmit 对 Cocos 官方 `@cocos/creator-types` 3.8.3 engine 声明,含 @ccclass 装饰器路径;故意错用 API 会被抓=门有牙)。**这道门已经进仓、也进 CI**:`cd tools/cocos-typecheck && npm ci && python3 check.py`(它连"门有牙"那半句一起验:种一个必然的类型错误,tsc 必须报出来)。此前它只在作者本机存在 —— 声明是真的,但没人能复现。**Creator 内实机运行仍未验证**,交付态 = 源码 + 集成说明(mapping.md 顶部有声明);python 侧
  `python3 scripts/tests/run_all.py` 必须全绿才算校验器可用。
- **动效不许在 TS 侧解曲线**:烘焙归 `scripts/bake_motion.py`,`flow-binder.ts` 只做**线性**插值。
  采样点一致只保证关键帧上一致,插值模式不对齐照样各算各的(godot/unity 都在这儿栽过)。
  位移/缩放**只贴 `flow.modals[*].panel`**,贴到弹窗层上遮罩会跟着滑/缩 —— 数值看不出来,
  实机截图才抓得到。这两条有源码级守卫(`tests/test_runtime_source.py`)。
- 引擎 vs hook 边界不破:runtime 只管结构与机制,任何"某个项目的某块颜色/数据"都进 hook,不进引擎。
- 项目无关、可移植;中文文档、英文标识符;UTF-8 无 BOM。
- 上游 IR 契约(字段、已知限制如实例内 rot=0)以 figma2html `references/` 为准,本 skill 不复制不改写。
