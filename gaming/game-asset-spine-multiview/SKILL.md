---
name: game-asset-spine-multiview
description: 制作正面、侧面和背面多套 Spine 角色，并在 three.js 场景按镜头夹角切换，适用于饥荒式二维角色与三维场景结合的游戏。
---

# 多方向 Spine 与三维场景

先确定视角数量、角色朝向约定、镜头俯仰范围和动作相位。先完成三方向小样，更多方向、换装与 Godot 集成需另验证。

## 执行

1. 同一次图像编辑中生成同高、同地面的正/侧/背设定图，再分栏。当前试验中单独正面转侧/背七轮失败；这是一条优先级经验，不是所有生成模型的定律。不要用形体不匹配的三维底图覆盖空栏。
2. 侧面须为真正侧面，背面无五官或正面装饰。共用缩放和脚底对齐；清理接近透明的 alpha 底噪后再用于裁切/图生 3D。
3. 三张分别用 See-through 拆层，核对本次头部高清输出，按深度合并。侧/背面 DWPose 不可靠时，从层几何定关节；侧面复制远侧手脚只是已知近似。
4. 同一动捕循环经同一角色坐标系投到三台正交相机，保存角度、投影长度和深度。方向只取水平位移/肩轴；近乎朝镜头的骨段投影方向不稳定，需按投影长度降权。
5. 三套动作同名、同周期、同相位。正/背面朝镜头弯膝无法靠平面旋转表达时，增加抬膝和过渡关键姿势换图；头部须与基础图对齐，深度靠前的腿另画在衣身前。
6. 镜头夹角按扇区选 front/side/back，边界加回差，侧面镜像补另一边；切视角继承动作时间。B+ 视差只缓解轮廓跳变，不生成缺失视角。
7. 物理冲量来自角色真实位移，不来自屏幕横坐标。转镜头、镜像、切视角和视差突变时重置物理，否则原地绕镜头会让头发猛烈摆动。

## 附带入口

在 `assets/workspace/`：

```sh
python scripts/dir-rig.py layers-side rig/side --view side --name character_side
python scripts/spine-pack.py rig/side --name character_side
node scripts/spine-verify.mjs rig/side character_side
python scripts/dst-manifest.py rig
python scripts/dst-demo-build.py rig/manifest.json web
```

先以同样方式准备 front/back。`--motion walk=...,run=...` 接入投影数据，`--run-pose/--run-pass` 接入关键姿势层；查看各脚本帮助。附带演示源页，依赖通过固定版本包加载。

## 验收

绕角色一圈、站立转镜头、走跑切视角、镜像及有限动画帧率逐项检查。保持真实移动速度与步长对应，比较同机位 3D 参照。历史示例的阈值、侧臂幅度和直膝系数是调校起点，不是所有角色默认值。

换装人台、更多方向、真正的侧面远侧腿与引擎集成不属于已完成能力；旧报告与教程对裙摆状态不一致时，以当前脚本、实际运行和明确遗留为准。

资源获取见 [sources.md](references/sources.md)，附带代码及适配边界见 [implementation.md](references/implementation.md)。
