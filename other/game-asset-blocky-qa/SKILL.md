---
name: game-asset-blocky-qa
description: 检查方块角色的旋转、UV、共面闪烁、镜像、接缝和动态边界，解释结构检查能证明的范围，适用于普通角色或场景的导出前质量验证。
---

# 方块模型检查与共面修复

先记录源文件哈希、格式、可见变体、贴图和目标引擎，所有报告/截图对应同一版本。优先现成 Blockbench 校验器、MCP 原生渲染、mcbemodelingmasterAI 检查与 SciPy HiGHS；本包仅附项目的诊断和连接代码。

## 几何与 UV

- 递归应用分组和元素的枢轴旋转。参考实现为 `Rz·Ry·Rx`，不能把父旋转加成角度；区分独立 groups 与 outliner 内嵌属性。
- `inflate` 后才算有效尺寸；负 inflate 可能形成切片。已转换坐标不可再次镜像。
- 跳过 `texture:null`、显式禁用和真实零面积面；零跨度 UV 仍能采样一个纹素并铺到有面积的面，不能按 UV 面积删几何。
- 逻辑 UV 标尺与实际 PNG 像素尺寸独立；多贴图逐张处理。提取子树不能把同名的其他角色/物件混进来。

## 共面与镜像

1. 先在当前可见状态找同向、同平面、有面积重叠且颜色不同的面，再渲染判断；同色重叠也应记录，但不能直接等同可见闪烁。
2. 仅修最终副本。已略错开的面保留原上下层；真正共面才根据明确叠放关系选前后。不能用“小块永远在上”推翻参考本有的覆盖顺序。
3. 位移/膨胀取最小必要值，左右镜像同步，零厚度片不要因膨胀重新画出侧边。需要按原 bbox 匹配的上游模板不得先修几何。
4. 修后重跑候选、层序翻转、左右差和多角度渲染，检查是否引入新缝或改轮廓。静态共面为零不排除 MSAA 边缘闪烁、透明排序与动态穿插。

## 配套入口

进入 `assets/workspace/`，`FORGE_TOOLS_DIR` 指向从 mcbemodelingmasterAI 获取的 `tools/`：

```sh
python scripts/blocky-step-check.py model.bbmodel --include "coat|skirt"
python scripts/blocky-zfight-check.py model.bbmodel --out before.json
python scripts/blocky-zfight-check.py model.bbmodel --fix fixed.bbmodel --step 0.02 --mirror --move --out after.json
```

`--move` 只用于最终副本；先确认几何变更不会破坏其他按 bbox 匹配的步骤。面容/发型等天然台阶不宜用统一剪影阈值处罚；明确 include 的部位及允许折角。

## 动态与证据

测试 rest、走/跑、急停、转头、镜像与最大摆幅；检查屏幕外轮廓、接口、脚底和附件，而不仅看内部骨骼数值。软体/衣摆连接处固定，外缘仍应运动，不能靠钉死整个体积“修掉”裂缝。

报告分别列结构错误、警告、选定 SAT 关系、共面候选、逐帧采样和实际渲染覆盖。原生警告不能统一吞掉；美术评审、运行时物理与引擎验收各自说明。源项目修复共面/镜像的一般规律已提炼，原成人主题示例和资源不发布。

资源获取见 [sources.md](references/sources.md)，附带代码及适配边界见 [implementation.md](references/implementation.md)。
