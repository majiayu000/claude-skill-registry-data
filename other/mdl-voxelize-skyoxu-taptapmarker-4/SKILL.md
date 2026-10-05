---
name: mdl-voxelize
description: 将 UrhoX/TapMaker 的 UMD2 .mdl 3D 模型资产和 diffuse 贴图转换为生产可用的 voxel JSON 资产，供 TapMaker 体素渲染使用。当 Codex 需要体素化 .mdl、生成或校验 TapMaker voxel JSON 资产、准备 Higgsfield 风格体素资产、解释 MDL 到体素 JSON 的交接流程时使用。用户提供 prefab/model UUID、资产搜索结果、Tripo 生成模型或本地 TapMaker 项目资产，并希望转成 voxel JSON 时也使用本 skill。
---

# MDL 体素化

本 skill 用于把 UrhoX 运行时模型 `.mdl` 和可选 diffuse 贴图转换成 TapMaker 可用的 voxel JSON 资产。它不负责创建源模型，也不直接渲染场景；它只产出 TapMaker Lua 代码可以读取并绘制的彩色体素方块数据。

## 工作流

1. 定位源资产。
   - 优先使用用户明确给出的本地 `.mdl` 路径和一个或多个 diffuse 贴图路径。
   - 如果用户只描述了想要的资产，先在可用时使用 UrhoX MCP 资产搜索或模型生成功能；见 `references/mdl-source-options.md`。
   - 如果用户提供 `--model-uuid` 或 `--prefab-uuid`，可以直接调用 Python 工具并传 `--asset-root`；同时确认项目里有相关 `.meta`、`.material`、prefab、model 和 texture 文件。

2. 确定项目根目录。
   - 使用包含 `scripts/` 和 `assets/` 的 TapMaker/UrhoX 项目根目录。
   - 默认先 `cd` 到项目根目录再运行脚本；这与 `sprite-gen` 的工作区定位习惯一致。
   - 相对路径形式的 `--mdl`、`--texture`、`--out` 和 `config.json.output_dir` 默认都从当前工作目录解析。
   - 只有当脚本从项目根以外的位置被调用时，才传 `--project-root` / `-ProjectRoot` 覆盖解析根目录。
   - UrhoX 本地运行时，`-tapcode_dir=<project>` 会把 `<project>/scripts` 和 `<project>/assets` 加入 `ResourceCache`；Lua 资源路径里不要再写 `assets/` 前缀。见 `references/engine-ai-dev-kit.md`。

3. 检查当前 Python 环境依赖。
   - 在全新或不确定的环境中首次运行前，使用内置环境检查脚本：

```bash
sh <skill>/scripts/check_env.sh
```

   - 这个流程与 `sprite-gen` 一致：使用选中的 Python 解释器，不创建 venv，检测缺失包，只用 `<selected-python> -m pip install` 安装缺失依赖。
   - 生产 launcher 会自动执行同一检查；如果马上要跑 launcher，手动检查不是必需步骤。

4. 按需调整配置。
   - 默认读取 `<skill>/config.json`。
   - `output_dir` 默认是 `assets/voxels`，输出文件名默认是 `<输入名>_voxel.json`。
   - 命令行参数优先级高于 `config.json`。

5. 运行生产 launcher。
   - POSIX / 容器默认入口：

```bash
cd <tapmaker_project>
sh <skill>/scripts/run_voxelize.sh \
  --mdl assets/Meshes/model.mdl \
  --texture assets/Textures/model_diffuse.png
```

   - Windows 兼容入口：

```powershell
cd <tapmaker_project>
<skill>\scripts\run_voxelize.cmd `
  -Mdl assets\Meshes\model.mdl `
  -Texture assets\Textures\model_diffuse.png
```

   - 从项目根以外调用时，才额外传 `--project-root <tapmaker_project>` 或 `-ProjectRoot <tapmaker_project>`。
   - 需要覆盖默认输出时，传 `--out <path>` 或 `-Out <path>`。
   - 需要覆盖默认配置时，传 `--config <path>` 或 `-Config <path>`。

6. 校验输出。

```bash
python3 <skill>/scripts/verify_voxel_json.py assets/voxels/model_voxel.json
```

   期望的物理体素尺寸只能是 `0.5` 和 `1.0` 米。

7. 把 JSON 交给 TapMaker 项目代码。
   - 生成的 JSON 放在项目 `assets/` 下，默认是 `assets/voxels/`。
   - 项目侧必须有能读取并渲染该 voxel JSON 格式的 Lua 代码，例如 `scripts/higgsfield/VoxelSceneLoader.lua`、`scripts/higgsfield/VoxelSceneRenderer.lua` 和 `scripts/main.lua`。

## 输入

必需：

- `.mdl`：UrhoX 运行时模型文件，要求是 UMD2 格式；也可以用 `--model-uuid` 或 `--prefab-uuid` 作为输入源。

推荐：

- 一个或多个 diffuse 贴图。可以重复传 `--texture`，也可以在 launcher 中传逗号分隔值。贴图按 geometry index 顺序映射；如果贴图数量少于 geometry 数量，后续 geometry 会复用最后一张贴图。
- `--out`：输出 voxel JSON 路径。不传时默认写到 `config.json.output_dir` 下。
- `--scene-id`：输出 JSON 内部使用的稳定 ID。不传且配置为空时，会从输入名派生。
- `--max-width`、`--max-height`、`--max-depth`：最大体素网格边界。不传时使用 `config.json`。

高级可选：

- `mdl_to_voxel.py` 支持 `--prefab-uuid` / `--model-uuid`，通过 `--asset-root` 下的本地 `*.meta` 文件解析资源。仅在完整本地资产树存在时使用。
- launcher 也支持 `--prefab-uuid` / `--model-uuid`，优先使用 launcher，因为它会读取配置、检查依赖并补齐生产参数。

## 配置

默认配置文件是 `<skill>/config.json`，默认只填写用户通常需要改的输出目录：

| 字段 | 默认 | 说明 |
|------|------|------|
| `output_dir` | `assets/voxels` | 默认输出目录，相对于当前项目根 |

launcher 还支持在 `config.json` 中覆盖 `scene_id`、`max_width`、`max_height`、`max_depth`、`fill_mode`、`surface_thickness`、`max_palette_colors`、`color_levels`、`raster_color_samples`、`raster_coverage_samples` 和 `raster_min_coverage`。这些字段不写时使用 launcher 内置默认值。命令行参数覆盖 `config.json`。如果需要为单个项目使用不同默认值，复制一份配置文件并用 `--config <path>` / `-Config <path>` 指定。

## 输出

输出 voxel JSON 包含：

- `version`、`scene_id` 和 `source` 来源信息。
- `size`：体素网格尺寸。
- `origin`：底部中心 pivot 元数据。
- `palette`：带 RGB 的材质/颜色表。
- `voxels`：方块坐标。每项包含 `x`、`y`、`z`、`p`；可选 `s=2` 表示合并后的 1m 方块，省略 `s` 表示 0.5m 方块。
- `metadata`：三角面数量、palette 数量、grid unit、合并参数、源模型包围盒和 quality gate 结果。

## 生产规则

生产用途默认使用 launcher，除非有明确诊断原因才直接调用 `mdl_to_voxel.py`。launcher 会强制：

- `--grid-unit-m 0.5`
- `--hybrid-merge-size 2`
- `--hybrid-merge-min-fill 4`
- `--hybrid-merge-min-color-ratio 0.75`
- `--surface-mode raster`
- `--no-flip-v`

不要按题材选择体素尺寸。生产输出只能包含：

- 0.5m 基础格：`metadata.grid_unit_m = 0.5`，voxel `s` 省略或 `s = 1`
- 1m 合并格：voxel `s = 2`

`--allow-custom-voxel-size` 只能用于本地诊断，并且必须明确说明不是生产输出。

## 运行依赖

脚本需要：

- Python 3
- pip
- Pillow (`Pillow>=10.0.0`)

使用 `scripts/check_env.py` / `.sh` / `.bat` 做环境准备。这些脚本不创建虚拟环境，也不假设 Python 的安装方式；它们会检查选中的解释器，并把缺失依赖安装到这个解释器里。POSIX 环境优先使用 `.sh` wrapper，因为它会先选 `python3`，再 fallback 到 `python`，与 `sprite-gen` 保持一致。生产 launcher 会自动调用 `check_env.py`。除此之外，`mdl_to_voxel.py` 只依赖 Python 标准库。

## 排障

- `PATH 中找不到 python3 或 python`：安装 Python 3，或切到能找到 Python 的环境。
- `依赖检查失败` 或 `pip install 失败`：POSIX 下运行 `sh <skill>/scripts/check_env.sh`，Windows 下运行 `<skill>\scripts\check_env.bat`，查看打印出的 pip 错误。若环境禁止运行时联网安装，需要提前在镜像或环境里预装 `Pillow>=10.0.0`。
- `请提供 --mdl、--model-uuid 或 --prefab-uuid`：传入明确模型路径，或正确使用 UUID 解析参数。
- `当前 MDL 路径只支持 UMD2 文件`：输入文件不是 UrhoX UMD2 `.mdl`。
- `体素质量门禁失败`：提高最大网格尺寸或检查源 mesh；生产用途不要随意关闭 `--quality-gate`。
- `包含非标准体素尺寸`：用 launcher 重新生成，或移除诊断用的自定义尺寸参数。
