---
name: figma2unity
description: 把 figma2html 管线捕获的中间表示(IR:.ui.json 像素快照 + flow.json 交互声明)编译成 Unity UI Toolkit 资产(UXML+USS)与 C# 运行时 flow 绑定器。输入 = figma2html capture 的产物;本 skill 是编译后端,不含 capture。要在 Unity 里还原 figma 界面像素与交互(底屏+弹窗/守卫/列表/勾选)时使用。
---

# figma2unity — figma2html IR → Unity UI Toolkit

## 这个 skill 干什么

figma2html 产的 **`.ui.json`(像素 IR)+ `flow.json`(交互声明)** → **UXML + USS**(每屏一对)+ **FlowBinder**(C# 运行时把 flow 语义装起来)。

- **像素**:`ui_to_unity.py` 确定性转写——每元素一个 VisualElement/Label、绝对定位父相对几何(算法同 render.js pass2)、样式逐项映射,USS 不支持的项**诚实降级**(跳过 + 文件头注释列丢弃项)。
- **交互**:`FlowBinder.cs` 按 assemble.js 语义实现——底屏常驻 + 弹窗叠加(抽 roots 子树 + 黑色半透 backdrop)、click 事件按 name 绑、guard 全真放行、内置 openModal/closeModal/toggleFlag/send、列表行克隆、checkbox 双态;域内语义走 `IAppHook`。

边界:**capture 归 figma2html**(拉节点树/导素材),本 skill 只吃它的产物;HTML 目标继续用 figma2html,Unity 目标走这里。

## 内容

```
scripts/    ui_to_unity.py(IR→UXML+USS,纯标准库、确定性)
            tests/(run_all.py 发现式 runner + 单测 + golden;fixtures 自带)
runtime/    FlowBinder.cs(flow 绑定器,MonoBehaviour)· IAppHook.cs(域内钩子接口)
references/ mapping.md(IR→USS/UXML 映射全表 + known-loss 表 + 坐标缩放 + 资源摆放)
```

## 用法(管线)

1. **拿 IR**:用 figma2html 跑到第 5 步,得到各屏 `.ui.json` + 手写的 `flow.json`
2. **转换**:每屏一次 `python3 scripts/ui_to_unity.py <屏.ui.json> <outdir>` → `<stem>.uxml + <stem>.uss`
3. **进 Unity**:UXML/USS 与 `_assets/` 同放一目录(url 相对 USS 解析);PanelSettings 设 **Scale With Screen Size**,参考分辨率 = `cap.w × cap.h`(见 references/mapping.md)
4. **挂绑定器**:场景放 UIDocument + `FlowBinder`,Inspector 配 flow.json(TextAsset)+ `screens[]`(capName→VisualTreeAsset,capName 用 flow.caps 的键名)
5. **写 hook**:实现 `IAppHook`(RegisterActions 注册 send/selectServer 等域内 action;Init 里拉数据 → `binder.RenderRows(...)`、回填)

## 关键规则

- **name = figma id 把 `':'` 换 `'_'`**(UXML name 不许冒号);USS 选择器用 `.el-<name>` 类(name 可数字开头,`#id` 会非法)。flow.json 仍写原始 id,FlowBinder 用 `SafeName` 换算。
- **z 序 = 文档序**:同父下按 z 稳定排序生成兄弟顺序(UI Toolkit 无 z-index,后者在上)。
- **诚实降级**:shadow / blur / text-stroke / line-height USS 不支持 → 跳过;渐变 → 第一停靠色回退;全部记录在生成 `.uss` 文件头注释,全表见 `references/mapping.md` 的 known-loss。
- **弹窗抽子树要带样式表**:UI Toolkit 样式表挂元素上,`Q(root)` 抽离后必须把整树样式表拷给根(FlowBinder 已做,自己改代码别丢)。
- **RenderRows 须布局完成后调用**(行距采样读 resolvedStyle):`IAppHook.Init` 里用 `schedule.Execute` 延一帧。

## 硬约束

- 产物与脚本一律 **UTF-8 无 BOM**。
- `ui_to_unity.py` 纯标准库、**确定性输出**(禁时间戳/随机),同输入必逐字节同产物(golden 测试守着)。
- `FlowBinder.cs` 目标 **Unity 2022.3+ / UI Toolkit**。**2026-07-03 已实机冒烟(Unity 6000.4.8f1 batchmode)**:FlowBinder.cs/IAppHook.cs **编译零错零警告**;三屏生成 UXML/USS 全部通过 Unity 导入器(VisualTreeAsset/StyleSheet 非空);CloneTree 结构断言过(name 映射 1_21→"开始游戏"、嵌套 1_12∈1_10、元素数 12/5/13)。**视觉渲染与交互链未实机点验**(batchmode 无图形;同一 IR 几何在 html/godot 已双双眼比对齐),接入后按 mapping.md 集成步骤跑一眼。
- 改转换逻辑必跑 `python3 scripts/tests/run_all.py` 全绿;映射有意变更时同步重生成 `tests/golden/` 并在 mapping.md 更新对应行。
