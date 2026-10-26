---
name: minecraft-xiantu-vfx-library
description: 复用仙途九组可编辑特效预览，包括九霄剑幕与万剑归宗、金白剑气拖尾、五行气海和沿边缘传播的焚空裂隙；附灵气、闪电、护盾、空间裂隙及拖尾。用于从现有特效原型修改形态、贴图、挂点和着色器；游戏接入需单独实现与验证。
---

# 仙途特效库

用 `python scripts/serve.py` 启动本地目录，或用 `python scripts/create_project.py <新目录>` 复制独立特效库。两者仅用Python标准库。入口与用途见 `references/effects.md`，首次使用可先读 `references/usage.md`。

- 先看目标效果已有参数和贴图，沿现有算法修改，保留单独暂停、时间与观察控制。
- 焚空裂隙的“边缘呼吸”指沿边界弧长传播的局部波包、光带厚薄和分层流光；保持整体尺寸和尖角锚点，不能改成整片缩放。高度是独立静态参数。修改共享 `shader/rift-core.glsl` 后运行该目录 `scripts/build.py` 生成WebGL2与GLSL150。
- 剑阵中人物和剑刃挂点应一并检查，拖尾从实际尾端采样；内置通用演示皮肤，不依赖个人皮肤或Minecraft纹理提取。
- 气海预览自带共享GLSL及两张玉盘贴图，以独立修为参数平滑积分五行相位；不把灵气比例与修为比例混为一个值。
- 密度/辉光属于视觉参数，不应暗中改变游戏伤害频率。浏览器变体与当前模组战斗版本不保证逐帧相同。
- 接入Minecraft时明确世界/局部坐标、真实场景颜色和深度、暂停与取消清理、外部光影兼容性。测试背景折射不代表Minecraft世界折射；浏览器通过不等于游戏通过。

修改后运行 `python scripts/check_library.py`。该检查覆盖九组入口及本地资源；焚空裂隙可运行 `python scripts/verify_rift_gpu.py --output <目录>` 进行桌面GPU验证（需moderngl、glfw、numpy、Pillow；`--video`另需FFmpeg）。人物穿插与游戏实测按受影响效果补做。来源、子目录许可证和验证范围见 `references/provenance.md`，不要将组合全部标为MIT。
