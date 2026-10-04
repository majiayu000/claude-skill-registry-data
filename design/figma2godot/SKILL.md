---
name: figma2godot
description: 把 figma2html 管线捕获的中间表示(IR:.ui.json 像素快照 + flow.json 交互声明)编译成 Godot 4 文本场景(.tscn)与 GDScript 运行时 flow 绑定器。输入 = figma2html capture 的产物;本 skill 是 Godot 4 编译后端,不含 capture。要在 Godot 工程里还原 figma 界面像素与交互(底屏+弹窗/守卫/列表/勾选)时使用。
---

# figma2godot — figma2html IR → Godot 4 场景 + flow 绑定

## 这个 skill 干什么

figma2html 产的 IR(`.ui.json` 像素 + `flow.json` 交互)→ **确定性编译**成 Godot 4 资产:

- **像素**:`scripts/ui_to_tscn.py` 把每屏 `.ui.json` 编成一个 `.tscn` 文本场景
  (format=3):根 Control 固定舞台、每元素一节点、父相对 offset 几何、
  StyleBoxFlat(圆角四角/描边/**原生阴影**)、Label、TextureRect、真线性渐变。
- **交互**:`runtime/flow_binder.gd` 读 `flow.json`,按 assemble.js 同语义组装:
  底屏常驻 + 弹窗叠加(整场景实例按 roots 剪枝 + 半透明 Backdrop)、事件/守卫/
  toggleFlag/send、列表行克隆、checkbox 双态;域内语义走 `app_hook` action 注册。

边界:**capture(figma→IR)归 figma2html,本 skill 只做 Godot 落地**;两边共享
figma node id 键空间(节点名 = id 冒号换下划线,flow 里照写原始 id)。

## 内容

```
scripts/    ui_to_tscn.py(.ui.json → .tscn;纯标准库、确定性、argv 驱动)
            tests/(run_all.py 发现式 runner + 单元/golden;fixtures = login 三屏)
runtime/    flow_binder.gd(flow.json → 底屏+弹窗+事件+绑定;Godot 4.2+)
            app_hook.example.gd(域内 action 注册示例:send/选服/回填)
references/ mapping.md(IR→Godot 映射全表 + known-loss 表 + 坐标/缩放/命名约定)
```

## 用法(管线)

1. **上游**:用 figma2html 跑到第 5 步,拿到每屏 `<stem>.ui.json` + 手写 `flow.json` + `_assets/`。
2. **编场景**:每屏一跑 `python3 scripts/ui_to_tscn.py <stem>.ui.json <godot工程>/scenes/`
   → `scenes/<stem>.tscn`。
3. **摆素材**:`_assets/` 整目录原样拷进 Godot 工程根(ext_resource 按 `res://<IR路径>` 引用);
   配一个 CJK 字体主题(字体/字重映射见 `references/mapping.md §6`)。
4. **拷运行时**:`flow_binder.gd`(+ 参照 `app_hook.example.gd` 写自己的 hook)放进工程;
   `flow.json` 放 `res://`。
5. **组装**:主场景里 `FlowBinder.new()` → 设 `flow_path`/`scene_dir` → hook `register(binder)`
   → `add_child(binder)`(先注册后入树)→ 引擎内冒烟核验。

## 硬约束

- **UTF-8 无 BOM、LF 换行**;转换器纯 Python 标准库、argv 驱动、**确定性**
  (同输入同字节输出,tests/golden 逐字节守卫)。
- **只编译不发明**:IR 里没有的视觉不脑补;转不动的显式降级并记录在
  `references/mapping.md` 的 known-loss 表(blur 丢弃、径向渐变平均色、字距丢弃等),
  改转换行为必须同步该表和 golden。
- **引擎 vs hook**:`flow_binder.gd` 只管结构/机制,域内语义(数据→行、回填、状态色)
  一律走 action 注册,不许写死进引擎。
- `flow_binder.gd` 目标 Godot 4.2+。**2026-07-03 已实机冒烟(Godot 4.3-stable)**:ui_to_tscn 产的 screen-login.tscn 实例化渲染与 figma2html 截图逐项对齐(底色/标题/圆角条/宝石/按钮/勾选框/CJK 字体),flow_binder.gd + app_hook.example.gd 编译零错。**坑:直接 `godot --path <proj>` 跑从未导入过的工程,`class_name` 全局注册缓存(.godot/)不存在会报"找不到类型 FlowBinder"——先跑一次 `godot --headless --import --path <proj>`**。事件/弹窗/列表交互链未实机点验,接入后按下方冒烟清单过一遍
  再叠业务。
- 改动本 skill 的转换逻辑后必跑 `python3 scripts/tests/run_all.py` 全绿。
