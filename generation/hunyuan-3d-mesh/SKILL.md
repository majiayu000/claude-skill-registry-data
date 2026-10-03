---
name: hunyuan-3d-mesh
description: Process existing 3D meshes through Tencent TokenHub. Use HY-3D-Component for FBX component splitting, HY-3D-Retopology for polygon reduction and triangle/quad retopology, or HY-3D-Format for OBJ/GLB/FBX format conversion and MP4/GIF output; includes task queries, recovery, and downloads.
---

# 混元 3D 网格处理

当前支持**组件拆分、智能重拓扑减面和格式转换**。文字/图片生成模型使用 `hunyuan-3d-generator`；UV、材质、绑骨和动作生成尚未接入本技能。

| 目标 | 命令与模型 | 输入 | 按需参考 |
|---|---|---|---|
| 拆分部件、编辑分割数据 | `split` / `hy-3d-component` | FBX 链接 | [组件拆分](references/component.md) |
| 降低面数、生成三角/四边面拓扑 | `reduce` / `hy-3d-retopology` | OBJ / GLB / FBX 链接 | [减面与重拓扑](references/retopology.md) |
| 转换模型格式或输出 MP4/GIF | `convert` / `hy-3d-format` | OBJ / GLB / FBX 链接，≤60m | [格式转换](references/format.md) |

先按用户目标选择模型，只执行用户要求的处理步骤。重拓扑及部分格式转换可能改变面索引，不能未经验证就将原组件分割数据套到处理后的模型。

## 输入与运行环境

- 三个接口都通过可访问的 HTTPS 模型链接输入，支持签名 URL。组件拆分和格式转换使用 `file: {url: ...}`；减面使用 `file_3d: {url: ..., type?: ...}`。输入格式按上表选择，不要把 ZIP、本地路径或改后缀文件当作已支持格式。
- 本地模型先用 Blender 等软件导出相应格式的独立副本，再使用用户指定或已授权的存储提供链接。导出属于本地准备；公开上传或第三方托管需要已有授权。已有混元生成任务若返回可访问且格式符合要求的链接，可直接作为输入。
- 三个接口均未提供本地 Base64 形式。格式转换明确限制输入≤60m；组件和减面的页面未列出大小/面数上限，不套用转换限制。离线校验不能验证远端模型内容或大小，无后缀 URL 须另行确认实际格式。
- Python 3.10+，运行无需第三方库。依赖**相邻安装的最新版 `hunyuan-3d-generator`**，复用其共用客户端 API v1。两个技能保持同级目录；不复制鉴权、网络重试、轮询和下载实现。运行前解析脚本及输出目录的绝对路径。
- 从进程环境读取 `TOKENHUB_API_KEY`，兼容 `HUNYUAN_3D_API_KEY` / `TENCENT_HUNYUAN_API_KEY`。不把密钥写入文件、命令行或日志。只支持 TokenHub，不能用旧 AI3D 任务 ID 恢复。

## 拆分流程

1. 检查来源确实为 FBX。脚本离线检查 URL 与已知后缀，不下载输入或验证远端文件内容；无后缀链接须另行确认其返回 FBX。保留原模型及材质资源。
2. 默认一次生成组件；`--enable-staged-generation` 用于取得可编辑的分割结果。分阶段流程、字符串参数和文档缺口见 [references/component.md](references/component.md)，使用此模式前阅读。
3. `--enable-post-process` 默认关闭。官方说明开启后只输出一个模型链接，**额外增加 20 积分**。仅在用户明确选择后处理，或已批准的设置包含该选项时开启。
4. 按下文的共用提交与恢复规则执行；不自动追加阶段或开启后处理。
5. `split` 提交、等待并下载全部组件与分割资源；`submit` 仅提交。需要检查质量时在 Blender 导入副本，检查组件数量、几何、材质与原模型的位置关系；未检查就不声称组件可直接用于游戏或动画。

## 减面流程

1. 阅读 [references/retopology.md](references/retopology.md)，检查 OBJ / GLB / FBX 来源。`--file-type` 是可选输入类型，不能与 URL 后缀冲突，也不用于控制输出格式。
2. `--polygon-type triangle` 为三角面，`quadrilateral` 为四边面；未指定时使用服务端三角面默认值。`--face-level high|medium|low` 控制输出面数档位；文档未公布每档面数、比例或默认档位，不把档位解释成固定数量或固定减面百分比。用户要求精确面数时先说明该接口限制，不能声称档位满足精确目标。
3. `reduce`（别名 `retopology`）固定用于减面；只提交使用 `submit --model retopology`。不传组件拆分的阶段、分割数据或后处理参数，也不传生成接口的 `face_count`、`result_format` 等选项。
4. 减面后及时下载 `data` 中的所有结果，包括模型和附属图片。需要检查质量时比较减面前后面数、轮廓、孔洞、UV/材质及关节区域；四边面输出不等于已验证可用于动画，未检查就不保证贴图、蒙皮或变形质量。

## 格式转换流程

1. 阅读 [references/format.md](references/format.md)，确认输入是 OBJ / GLB / FBX，且符合文档≤60m的大小限制。已核实字节数时可传 `--input-size-bytes` 做离线校验；该参数只作本地检查，不进入 API 请求，未知时不能声称大小已验证。
2. `convert --format` 必填，支持 `STL / USDZ / FBX / MP4 / GIF / OBJ / GLB`，脚本按文档发送大写值。输入支持范围与输出范围不同，不能把 STL、GIF 等结果反向当作受支持输入。MP4/GIF 是媒体输出，不代表生成了骨骼或动作数据。
3. 只提交使用 `submit --model format --format ...`。恢复使用 `query --model format`，无需重复目标格式。结果兼容 `type` / `format` 两种格式字段，下载全部资源；检查目标格式、材质和层级是否满足用途，不把文件下载成功当作无损转换证明。

## 共用提交与恢复

- 先执行 `--dry-run`。用户已授权对应处理且输入充分时提交一次；只要求接入 API、完善技能或讨论方案时不提交真实任务。
- 三个模型文档的默认并发均为 1，批量任务按模型控制；轮询至少间隔 5 秒。收到 ID 后报告 ID、所用模型与地域。
- `submit` 和 `query` 为兼容原命令默认使用 `component`。**减面用 `--model retopology`，格式转换用 `--model format`**；同一 ID 的模型与地域必须保持一致。中断或下载失败后查询原任务，不自动重提；提交结果不确定或没有 ID 时先检查服务端记录。
- 任务 ID 有效期 24 小时，完成后及时下载，返回实际文件绝对路径。区分云端任务完成、文件下载完成与质量检查完成。

## 命令

以下是从技能目录执行的命令结构；实际执行使用已解析的绝对路径。`example.com` 仅为占位链接。

```powershell
python scripts/hunyuan_mesh.py split --file-url "https://example.com/character.fbx" --dry-run
python scripts/hunyuan_mesh.py split --file-url "https://example.com/character.fbx" --output-dir components
python scripts/hunyuan_mesh.py submit --file-url "https://example.com/character.fbx"
python scripts/hunyuan_mesh.py query JOB_ID --wait --download --output-dir components
python scripts/hunyuan_mesh.py reduce --file-url "https://example.com/high-poly.glb" --face-level medium --polygon-type quadrilateral --dry-run
python scripts/hunyuan_mesh.py reduce --file-url "https://example.com/high-poly.glb" --face-level medium --polygon-type quadrilateral --output-dir reduced
python scripts/hunyuan_mesh.py submit --model retopology --file-url "https://example.com/high-poly.obj" --face-level low
python scripts/hunyuan_mesh.py query RETOPOLOGY_JOB_ID --model retopology --wait --download --output-dir reduced
python scripts/hunyuan_mesh.py convert --file-url "https://example.com/model.glb" --format fbx --dry-run
python scripts/hunyuan_mesh.py convert --file-url "https://example.com/model.glb" --format fbx --output-dir converted
python scripts/hunyuan_mesh.py submit --model format --file-url "https://example.com/model.fbx" --format gif
python scripts/hunyuan_mesh.py query FORMAT_JOB_ID --model format --wait --download --output-dir converted
python scripts/hunyuan_mesh.py check-auth
```

`--base-url` 沿用生成客户端的官方 TokenHub 地域白名单；默认广州，恢复时保持提交地域。`check-auth` 只读取模型目录，不能证明所选模型的额度充足。`--no-download` 可用于只等待完成。

## 维护

- 参数与分阶段操作：[references/component.md](references/component.md)。
- 减面档位、多边形类型、输入格式与模型恢复：[references/retopology.md](references/retopology.md)。
- 格式转换支持范围、大小限制、结果字段兼容：[references/format.md](references/format.md)。
- 从两个技能目录分别执行 `python -B -m unittest discover -s scripts -p 'test_*.py' -v`。测试模拟网络，不需要真实凭据或付费调用。
- 修改共用客户端时运行生成技能回归测试；同时用 skill-creator 的 `quick_validate.py` 校验技能结构。
