---
name: blender-realism
description: Diagnose and improve physical and visual realism in editable Blender models and scenes, including products, props, furniture, interiors, architecture and landscapes. Use when shapes look blocky, materials look plastic or flat, scale or contact feels wrong, lighting looks artificial, or a project needs a realistic modeling and review workflow. Verify changes with actual scene renders. Not for raster-only retouching, unrelated rigging tasks, or imposing photorealism on an intentionally stylized brief.
---

# Blender 真实化

把“看起来不真实”的反馈转成可执行的三维修改，用当前场景实际渲染确认结果。适用于单件产品、道具、家具、室内、建筑和景观；按用户目标与展示距离定义真实感，不强制追求某种摄影风格。保留可编辑模型，记录仍未解决的问题。

## 先定位本轮工作

- 新建项目：先确定对象用途、尺寸基准、主要构造、材质、环境、交付形式与检查视角，再分阶段制作。建筑项目细化为空间、家具和景观清单；产品项目细化为部件、装配与表面工艺。只询问会影响设计或交付的缺失信息。
- 修改现有项目：先定位当前文件、用户指出的物件和画面，不为套用流程重建已完成内容。
- “继续”承接已有目标和约束。用户已允许视频或发布时，不再把旧记录里的“等待审批”当作新的阻塞；也不能把历史审批当成新修改已获认可。
- 用户要求“先出图审批再做视频”时，交付实际修改后的全景和细节图，视频等待后续授权。没有这项要求时，不人为增加审批关卡。

## 查明场景再修改

确认 Blender 版本、活动文件与场景、单位、相机、对象集合、材质、实例、灯光、渲染器及外部资源。使用 Blender MCP 时先调用可用的状态和场景查询工具；没有 MCP 可用 Blender 后台脚本，不把某个插件当作必需依赖。

可用 [scripts/scene_audit.py](scripts/scene_audit.py) 导出基础清单：

```sh
blender --background scene.blend --python-exit-code 1 --python /path/to/blender-realism/scripts/scene_audit.py -- --output review/scene-audit.json --match "Sofa|Bed|Towel|Chair"
```

它只读场景、写 JSON，不修改或渲染模型。它报告资源、变换和基础边界，**不验证碰撞、通行距离或视觉真实感**，也不展开庞大的几何节点草坪实例。

将修改保存到可追溯版本或副本。不要清空用户场景、盲删同名集合，或把当前交付模型覆盖为低分辨率渲染代理。

## 以通用物理诊断驱动修改

先按 [references/diagnostic-framework.md](references/diagnostic-framework.md) 的诊断框架，将问题定位为尺度与轮廓、制造结构、受力与支撑、材质尺度与光学、照明与成像、环境关系或变化规律。先提出可检验原因，再选择修改；不要把“缺细节”统一解释成需要加噪声。

把用户反馈和主动发现的问题逐物件登记，至少包括：

| 字段 | 记录内容 |
| --- | --- |
| 定位 | 稳定编号、空间、实际对象名、画面编号与相机 |
| 可见症状 | 例如“柜内被褥像六个白色方块” |
| 原因与行动 | 例如“缺连续折返与填充压缩；重建布壳并校准层板承托” |
| 验证证据 | 模型版本、全景、局部图，必要时几何测量 |
| 状态 | 未改／模型已改／当前渲染已检查；用户审批单独记录 |

按影响范围和因果依赖排序：结构错误优先修结构；若症状主要来自光照、曝光或材质，先做隔离测试，不强行重建几何。提高采样、加噪声或加深阴影不能修复错误几何。优先处理主视角中显眼的问题及影响多个镜头的共用对象。

用户用“白块”“那把椅子”等表述时，以场景位置和截图指认；只有存在多个合理对象且会导致不同修改时才澄清。不要猜中一个物件后忽略它与邻近物件的关系。

## 选择相关专项

- 产品、道具或任何类型的“哪里不真”诊断：先用 [references/diagnostic-framework.md](references/diagnostic-framework.md)，没有对应专项也可据此工作。
- 沙发、床、枕头、卷巾、折被、书籍、柜体、灯具、家具摆放：读 [references/furniture-and-materials.md](references/furniture-and-materials.md)。
- 草坪、土壤、树根、硬地边界或泳池异常：读 [references/landscape-and-contact.md](references/landscape-and-contact.md)。
- 局部渲染、影片、显存内存约束、配乐或可移植交付：读 [references/render-and-delivery.md](references/render-and-delivery.md)。
- 需要历史例子时，可选读 [references/luma-lessons.md](references/luma-lessons.md)。主流程不依赖这个项目、对象名、文件或参数；案例数值不是通用验收标准。

## 实施与复核

1. 保留有用的模型与资产。已有细节良好的扫描模型可调整比例、材质和摆放，不必替换成基础几何。
2. 修改应有物理原因：制造决定分件与接缝，材料决定厚度与变形，受力决定接触和褶皱。先确保轮廓及大中尺度形态正确；微小表面细节再按视距使用法线、粗糙度或几何。
3. 每次移动或替换对象后，检查装配、支撑和邻接关系。空间场景还需检查动线、开启范围和植物枝叶；实例与父对象也纳入检查。
4. 先渲染能暴露缺陷的局部和对应全景。尽量保持修改前后的相机、曝光和构图一致。近景看结构，最终展示距离看是否有效。
5. 打开新图实际观察：轮廓、接触阴影、高光、纹理尺度、重复性、穿插和摆放。检查失败时重开问题，不以脚本成功或采样完成代替视觉判断。
6. 更新所有能看到改动物件或其影子、反射的视角。复用旧图需注明旧版本并确认不受影响；不能把文件已存在当作当前版本渲染成功。

不使用生成图片或二维修图假装三维模型已修复。若用户另行要求概念图或后期效果，将其与真实场景渲染明确区分。

## Blender 实施中容易踩的坑

- 导入对象可能使用四元数。只写 `rotation_euler` 不保证改变朝向；检查 `rotation_mode`、父级、约束及实际世界矩阵。用座面与椅背等几何关系验证朝向，不以角度数值作为证明。
- 非英文 Blender 的节点名称会本地化。按节点类型查询，不假定 `Principled BSDF` 等显示名存在。改变基色时修改实际着色节点输入，而不是只改视口颜色。
- 枚举与 API 按运行版本查询。渲染引擎是动态注册项，RNA 列表可能不完整；保留当前可用引擎，必要时捕获赋值错误。不要固定要求 ONEAPI、CUDA 或某台机器的设备。
- 对象缩放会影响纹理。先检查映射空间、UV、单位与材质真实覆盖尺寸；不要为“应用缩放”破坏实例、绑定或动画。
- 几何边界检查与接触射线是诊断证据。射线没命中不是接地通过；包围盒不重叠也不能证明细长枝叶、布面与实例全部无穿插。

## 完成时给出可核对结果

说明改了哪些问题、用哪些新图和测量复核、还存在哪些限制，附模型和渲染路径。分别记录建模完成、内部视觉检查和用户认可；仅对确有用户回复的版本标注已认可。

如果用户要求在 Blender 中打开，打开对应交付文件并检查窗口标题、活动场景和可见视图；后台进程加载成功不能证明用户已看到窗口。音乐、发布、删除旧版等扩展动作以当前用户指示为准，调用此 skill 本身不授予额外权限。
