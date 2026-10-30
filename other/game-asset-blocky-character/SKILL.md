---
name: game-asset-blocky-character
description: 用旋转方块和像素贴图制作普通着装的 Minecraft/YSM 风格角色，按社区样本选比例、组织衣身和逐面 UV，并区分 Generic 与目标游戏格式。
---

# 方块角色建模

原画决定辨识特征，目标画风的模型决定比例与构造。先确认输出 Generic、Bedrock、YSM 或其他格式；只导出 Bedrock 几何不等于已经接入 YSM 游戏。

## 执行

1. 先看可编辑参考、Blockbench MCP 与 mcbemodelingmasterAI。量头骨高 S、总高、肩腰深度、四肢、眼位、鞋长和纹素密度。不同统计的样本数/筛选不同，不能混加；中位数仅作候选，用户偏好仍需评审。
2. 角色配置只写发型、服装、配件、颜色，画风预设写比例。不要从原画真实比例直接缩成方块人，也不要把别人的方块化示意当官方角色设定。
3. 先用少量块定正/侧/背剪影。斜面用旋转链接、角对角衔接、凹处适当插入；零厚度面片只保留有用的面。曲线不能靠缩小箱子叠台阶。
4. 衣身和裙腰共用真实连接，腰盒延续到裙圈内、分界可画在贴图上。避免一圈独立短板形成锯齿与缝；也不要将所有衣服简化成长箱子。手臂、配件、领带按实际表面与运动范围定位。
5. 每面 UV 按纹素密度分配，先设工程/材质的逻辑 UV 尺寸，再导入贴图。逻辑 UV 与实际 PNG 分辨率分别处理。身体、头发、微小饰品可不同密度，避免无收益的高分辨率。
6. 形状由几何表达，眼睛、眉毛和图案靠贴图/薄层。逐面重画硬高光会让分段变横纹，先做连贯底色。单纯增加方块、贴图密度和噪声不能补错误轮廓。

## 配套入口

进入 `assets/workspace/`：

```sh
python scripts/blocky-template.py --char miku --preset ysm --bust none --out work/spec.json
python scripts/blocky-clip-check.py work/spec.json
python scripts/blocky-build.py work/spec.json --out work/build --bbmodel work/character.bbmodel
```

第三条生成 atlas 和 MCP 操作表，不会独立完成 `.bbmodel`；交给已配置的 Blockbench 工具创建、验证和渲染。本包不假定现场存在某个 MCP 名称。历史 `jenny` 字符串只是普通着装模板的旧预设名，不附该模组资源。

## 验收与经验

同光照同机位比较正面、侧面、背面、3/4 和头部特写。透视近景会放大头，先量再改。SAT 仅覆盖脚本定义的关系，不能证明头皮不露出、全身不穿模或审美合格。静态校验通过后再测走跑和极限姿势。

历史连续衣身、盲目加发束和高密度修细节被用户否定的轮次保留为失败经验，不当默认模板。模型借用与学习统计是不同授权行为；未明确可分发的社区模型只提供作者入口。

资源获取见 [sources.md](references/sources.md)，附带代码及适配边界见 [implementation.md](references/implementation.md)。
