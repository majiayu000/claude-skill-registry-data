---
name: hunyuan-3d-material
description: Generate textures with HY-3D-Texture or unwrap UVs with HY-3D-UV through Tencent TokenHub. Use for existing model texturing, PBR, preserving UVs, automatic UV unwrapping, task queries, and model/material downloads. Baking is not implemented.
---

# 混元 3D 材质

接入 **HY-3D-Texture 纹理贴图生成**和 **HY-3D-UV 自动 UV 展开**。模型生成使用 `hunyuan-3d-generator`，拆分/减面/格式转换使用 `hunyuan-3d-mesh`；烘焙和动画尚未接入本技能。

## 操作选择

- **生成纹理：** `texture`，模型 `texture`，输入单几何 OBJ/GLB 和文字或参考图。图片限制、多视图 schema 和版本说明见 [references/texture.md](references/texture.md)。
- **展开 UV：** `uv`（别名 `unwrap`），模型 `uv`，输入 FBX/OBJ/GLB，不传文字、图片或纹理参数。请求使用 `file.url`，可选 `--file-type`，与纹理的 `file_3d.url` 不同。
- UV 文档标注输入 60M、3 万面、最多 100 个组件/连通域。提交前核对已知大小和几何统计，可用 `--input-size-bytes`、`--face-count`、`--component-count` 做本地预检；这些是输入测量值，不是输出目标，也不发送给 API。单位和面数口径及超限处理见 [references/uv.md](references/uv.md)。
- 展开 UV 后再贴图时，先检查 UV 结果，选择其中的 OBJ/GLB 链接作为纹理输入，按需启用 `--enable-keep-uv`。这是两次独立任务，按用户授权范围执行；UV 操作自身不自动减面或生成纹理。

## 纹理输入

- 模型为可访问的 HTTPS OBJ/GLB 链接，请求字段为 `file_3d.url`。纹理接口不接受 FBX/ZIP。两类操作都不直接提交本地模型路径；需要时先准备相应格式的副本，再使用用户指定或已授权的存储链接，不自动上传到第三方。
- 文字与主参考图必选其一，不能同时传。文字最多 200 字符，优先中文正向材质描述；本地参考图支持 JPEG/PNG，使用请求体 `image.base64`，远端图使用 `image.url`。不要发送专业版的顶层 `image_base64` / `image_url`。
- `--enable-pbr` 请求 PBR 材质；`--enable-keep-uv` 请求保留已有 UV。两者默认关闭。用户需要保留既有 UV 时先确认模型具备所需 UV；保留 UV 与 UV 展开是不同任务。
- `--texture-size` 接受 720～4096 的整数，表示正方形贴图边长，未指定使用服务端默认 4096；不额外限制为 2 的幂。
- 多视图使用 `--view VIEW=FILE_OR_HTTPS_URL`；每个视角只传一张。纹理接口的视图字段是 `view` / `image`，与生成接口不同。使用前阅读 [references/texture.md](references/texture.md)，其中记录了版本说明缺口及与主参考图不同的尺寸/容量限制。

## 执行与恢复

1. 使用 Python 3.10+。依赖相邻安装的最新版 `hunyuan-3d-generator`，共用客户端须支持纹理图片脱敏；运行时不需要第三方库。解析脚本、输入和输出为绝对路径。
2. 凭据优先读取进程环境变量 `TOKENHUB_API_KEY`，兼容 `HUNYUAN_3D_API_KEY` / `TENCENT_HUNYUAN_API_KEY`。真实密钥不进入脚本、命令行参数或日志；仅支持 TokenHub，不混用旧 AI3D 密钥或任务。
3. 检查输入，再用 `--dry-run` 校验。预检不联网，只检查参数、本地参考图和提供的测量值，不能据此证明远端模型大小、面数、组件数量、UV 或图片内容符合要求。未知的统计值不填零或猜测值。
4. 用户已授权相应操作且输入充分时提交一次；仅要求接入 API 或完善技能时不提交付费任务。`texture` / `uv` 提交、等待并下载；`submit` 只提交，默认纹理，UV 须传 `--model uv`。收到 ID 后报告任务 ID、模型和地域。
5. 默认并发 1，轮询至少间隔 5 秒。中断/超时/下载失败后用原 ID、模型和地域查询。`query` 兼容既有纹理流程，默认仍为 `texture`；UV 任务必须传 `--model uv`。提交结果不确定或没有 ID 时先检查服务端记录，不自动重提，也不因参数拒绝换模型重做。
6. 任务 ID 有效期 24 小时，完成后及时下载 `data` 中全部模型、图片、纹理及 MTL 资源，保留原有资源关系。返回文件绝对路径，并区分云端完成、下载完成和材质检查完成。
7. 需要质量检查时在 Blender 导入副本：UV 结果检查 UV 层、重叠、拉伸和几何变化，纹理结果核对绑定、接缝和 PBR 通道。预览图不能替代模型检查；未检查就不保证 UV 质量、贴图完整或游戏就绪。

## 命令

以下从技能目录展示命令结构；实际运行使用已解析的绝对路径，`example.com` 是占位链接。

```powershell
python scripts/hunyuan_material.py texture --file-url "https://example.com/model.glb" --prompt "青绿色釉面陶瓷，细腻裂纹" --enable-pbr --texture-size 2048 --dry-run
python scripts/hunyuan_material.py texture --file-url "https://example.com/model.glb" --prompt "青绿色釉面陶瓷，细腻裂纹" --enable-pbr --texture-size 2048 --output-dir textures
python scripts/hunyuan_material.py texture --file-url "https://example.com/model.obj" --image reference.png --enable-keep-uv --output-dir textures
python scripts/hunyuan_material.py submit --file-url "https://example.com/model.glb" --image-url "https://example.com/reference.png"
python scripts/hunyuan_material.py query JOB_ID --wait --download --output-dir textures
python scripts/hunyuan_material.py uv --file-url "https://example.com/model.fbx" --face-count 30000 --component-count 20 --dry-run
python scripts/hunyuan_material.py uv --file-url "https://example.com/model.glb" --output-dir uv-output
python scripts/hunyuan_material.py submit --model uv --file-url "https://example.com/model.obj"
python scripts/hunyuan_material.py query UV_JOB_ID --model uv --wait --download --output-dir uv-output
python scripts/hunyuan_material.py check-auth
```

模型可写短名 `texture` / `uv` 或完整名 `hy-3d-texture` / `hy-3d-uv`，须与操作及原任务一致。`--base-url` 采用共用客户端的 TokenHub 官方地域白名单，默认广州；`check-auth` 只读取模型目录，不证明特定模型权限或额度充足。

## 维护

- 图片限制、视图 schema 和服务端差异：[references/texture.md](references/texture.md)。
- UV 输入限制、测量值和服务端字段：[references/uv.md](references/uv.md)。
- 从本技能目录运行 `python -B -m unittest discover -s scripts -p 'test_*.py' -v`，测试模拟网络并阻止真实连接。
- 修改共用客户端时同时运行生成与网格技能回归测试；用 skill-creator 的 `quick_validate.py` 检查结构。
