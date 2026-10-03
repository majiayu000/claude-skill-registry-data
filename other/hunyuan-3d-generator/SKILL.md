---
name: hunyuan-3d-generator
description: Generate and download Tencent Hunyuan 3D Professional (HY-3D-3.1/3.0) and Express (HY-3D-Express) models through TokenHub. Use for text/image-to-3D, professional multi-view generation, authentication checks, existing task queries, and model downloads; includes explicit legacy AI3D compatibility.
---

# 混元 3D 模型生成

使用附带的 Python 标准库客户端。默认接入 **TokenHub / hy-3d-3.1**。本技能用于生成、查询和下载模型；用户只要求修改技能或讨论接入时，不提交生成任务。

用户指定极速版或 HY-3D-Express 时使用 `--model express`；它支持文字、单图和白模生成。需要多视图、面数控制等专业版功能时使用 3.1/3.0。不要在模型之间自动切换。

## 接入与凭据

- TokenHub：默认提供商，使用 Bearer 鉴权。优先读取进程环境变量 `TOKENHUB_API_KEY`，兼容 `HUNYUAN_3D_API_KEY` 和 `TENCENT_HUNYUAN_API_KEY`。
- 旧版 AI3D：仅在用户明确要求旧接口或恢复旧任务时使用 `--provider legacy`；只读取后两个环境变量。TokenHub 与旧版的密钥、请求体及任务 ID 不应互换。
- 不将真实密钥写入技能、脚本、示例、日志或命令行。使用环境变量或可用的安全凭据注入；缺少安全配置时说明缺少什么，不把用户贴出的密钥复制进文件。
- 默认地域为广州；根据账户开通地域显式选择官方地址。不因鉴权失败自动切换地域、提供商或再次提交。
- 可用 `check-auth` 读取 TokenHub 模型列表验证鉴权。它不会生成模型；成功不代表该账户一定有生成额度或特定模型权限。
- Python 3.10+，生成客户端无第三方依赖。先确认可用解释器、技能目录和实际存在的输出工作区，执行时将脚本、输入和输出路径解析为绝对路径。

## 工作流程

1. 从用户目标选择文字、单图或多视图。检查本地参考图；优先完整、独立的主体和清晰轮廓。多视图应为同一对象的不同角度，不将含多个角色副本的拼图直接当作单张参考图。
2. 默认 3.1 + Normal。制作带材质资产时可开启 PBR；Geometry 为白模。需要 LowPoly/Sketch 时明确使用专业版 3.0。专业版默认不传结果格式以获取 GLB/OBJ；Express 普通模式默认返回 OBJ，供 Blender 使用时显式加 `--result-format glb`。Express 白模使用 `--enable-geometry`，默认返回 GLB，不能指定 OBJ。
3. 先用 `--dry-run` 验证来源和参数；该模式不读取密钥、不联网、不消耗生成额度，图片内容会脱敏。
4. 真实提交可能消耗额度。用户在本次会话中已明确授权生成且来源/设置充分时直接执行，不重复确认；仅要求准备、修改技能或缺少关键输入时不提交。需要用户决策时先完成可离线完成的工作，再说明具体缺少的信息。
5. 使用 `generate` 提交一次并等待下载，或用 `submit` 仅提交。收到 ID 后立即告诉用户任务 ID、提供商和模型；脚本同时输出恢复命令。
6. 轮询至少间隔 5 秒。超时、中断或下载失败后使用同一 ID 查询；提交响应丢失、连接中断或无 ID 时，先检查控制台任务记录，不自动重提。专业版默认并发上限为 3，Express 为 1；批量任务按所选模型限制活跃任务数。
7. 完成后立即下载模型和预览，返回实际文件的可点击绝对路径。任务 ID 有效期为 24 小时，结果链接也有时效。OBJ 可能以 ZIP 返回，保留原包及其材质资源。
8. 区分“生成成功”和“下载成功”。模型下载失败要报告已有文件并恢复同一任务；预览失败不否定模型文件。不要声称已完成生产验证、自动绑骨或游戏就绪，除非确实完成对应检查。

## 常用命令

以下从技能目录展示命令结构；实际运行请替换为已解析的绝对路径。示例不含真实凭据。

文字生成：

```powershell
python scripts/hunyuan_3d.py generate --prompt "一台原创街机风格摩托车，完整物体，纯色背景" --enable-pbr --output-dir output
```

单图生成；本地文件通过请求体直接发送，不上传第三方图床：

```powershell
python scripts/hunyuan_3d.py image-to-3d --image reference.png --model 3.1 --enable-pbr --output-dir output
```

多视图：主图作为正面，最多再传 7 个不同视角，每个视角仅一张：

```powershell
python scripts/hunyuan_3d.py image-to-3d --image front.png --view "left=left.png" --view "back=back.png" --model hy-3d-3.1 --enable-pbr --output-dir output
```

只校验参数 / 验证鉴权 / 查询恢复：

```powershell
python scripts/hunyuan_3d.py generate --prompt "一只小猫" --dry-run
python scripts/hunyuan_3d.py check-auth
python scripts/hunyuan_3d.py query JOB_ID --model 3.1 --wait --download --output-dir output
```

旧任务必须显式指定旧接口：

```powershell
python scripts/hunyuan_3d.py query JOB_ID --provider legacy --wait --download --output-dir output
```

Express 极速版生成与恢复：

```powershell
python scripts/hunyuan_3d.py generate --model express --prompt "一只小猫" --enable-pbr --result-format glb --output-dir output
python scripts/hunyuan_3d.py image-to-3d --model express --image reference.png --enable-geometry --output-dir output
python scripts/hunyuan_3d.py query JOB_ID --model express --wait --download --output-dir output
```

Express 不支持 `--view`、`--face-count`、`--polygon-type`、LowPoly 或 Sketch。不要复制专业版的 20 万面参数到极速版。Express 的 `--generate-type Geometry` 可作为 `--enable-geometry` 的别名；请求中实际发送 `enable_geometry=true`。

`--model` 接受 `3.1` / `hy-3d-3.1`、`3.0` / `hy-3d-3.0`、`express` / `hy-3d-express`；生成类型接受原有大小写或下划线形式。恢复 TokenHub 任务时须使用提交时的模型、地域和提供商。Express 仅支持 TokenHub 接入。

## 按需参考与维护

- 组件拆分使用相邻安装的 `hunyuan-3d-mesh`。它复用本技能客户端的 `COMMON_CLIENT_API_VERSION=1`、`submit_payload` 和 `run` 任务流程；分发时保留两个技能为同级目录，更新共用客户端后同时运行两套离线测试。
- 专业版参数、共用鉴权/地域、图片限制、错误诊断及新旧协议对照：[references/api.md](references/api.md)。
- Express 参数、白模限制、输出格式和命令示例：[references/express.md](references/express.md)。使用极速版时阅读，不套用专业版参数。
- 改动客户端后运行 `python -B -m unittest discover -s scripts -p 'test_*.py' -v`。这些测试使用模拟网络，不需要密钥或付费任务。
- 用 skill-creator 的 `scripts/quick_validate.py` 校验技能结构。结构校验需要 PyYAML，生成客户端本身不需要。
