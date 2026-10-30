---
name: game-asset-spine-cutout
description: 把完整角色切件制作成 Spine 侧视骨骼动画，支持视频姿态拟合、武器握点和 Godot 播放检查。适用于重复使用同一套部件的二维动作。
---

# 切件骨骼与复杂动作

输入同画风的完整头、躯干、左右手臂、左右腿，可选武器/刀鞘和参考视频。先确定面向、骨骼枢轴、遮挡层级和动作是否循环。输出骨骼 JSON、图集和实际运行时预览。

## 执行

1. 优先比较 See-through 完整部件、Spine 原生网格/IK/物理与官方引擎运行时。附带生成器是历史侧视模板；`00头、01身体、02/03臂、04/05腿` 的排序与身体尺寸绑定测试角色。新角色先改语义映射、枢轴和长度，不直接照搬常数。
2. 部件应包含被遮挡区域和自己的完整描边。关节保留重叠区，静态重合后再测极限转角；把原画颜色差分切开会在运动中裂缝。
3. 从视频提取动作时，先检查 DWPose 叠加图。侧视左右标签会互换，循环步态可联合拟合近侧与半周期后的远侧；不要将该假设用于不对称攻击。
4. 复杂动作先定义关键姿势和时序，再约束握点与脚底。刀鞘挂点按真实髋部定位，高腰衣服腰带不等于佩刀位置。出鞘前后分别确定父子关系和绘制顺序。
5. 优先用运行时 IK。为不支持约束的目标烘焙时，保存接触残差；回身压缩与镜像只是二维表现，不能冒充 3/4 转身。一次性动作的裙摆从静止积分，不能沿用周期预热。
6. 切动作时恢复 setup pose，给被覆盖的旋转、位移、缩放和 drawOrder 明确恢复值。Godot 数字轨道写浮点数，整数 0 曾导致整条旋转轨道被当成整数。

## 附带入口

在 `assets/workspace/` 运行，部件顺序须先核对：

```sh
python scripts/spine-cutout-parts.py parts-sheet.png parts
python scripts/spine-cutout-rig.py parts rig
python scripts/spine-pack.py rig --name kurumi
node scripts/spine-verify.mjs rig kurumi
python scripts/spine-to-godot.py rig godot --check
```

Node 先安装包内 package.json 声明的依赖。官方 `spine-godot` 可保留更多原生约束；自写 Skeleton2D 转换只是可选后备。

## 验收与边界

分别测单动作和动作切换、正反向、起跳/落地、武器出入层、握点偏差、脚底滑移。用目标引擎真实截图与同机位预览比较，历史姿势 IoU 约 0.96–0.99 仅是该角色结果。运行时能加载不代表动作自然。

早期模板拉长小腿上端代替大腿，大角度关节仍可见接痕；视频手肘数据受遮挡影响。攻击段的收刀动作未做，水平锁脚与正式游戏接入也不能写成已完成。

资源获取见 [sources.md](references/sources.md)，附带代码及适配边界见 [implementation.md](references/implementation.md)。
