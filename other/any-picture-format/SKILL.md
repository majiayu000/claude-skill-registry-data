---
name: any-picture-format
description: 当用户明确要求转换、修改或批量转换图片格式时使用。支持常见本地或网络图片输入与常见目标格式输出。⚠️ 不适用：仅调整尺寸/裁剪、查看图片信息，或没有明确格式转换意图。
metadata:
  author: Bensz Conan
  short-description: 任意格式图片转换工具
  keywords:
    - any-picture-format
    - 图片格式转换
    - PNG转JPEG
    - WEBP转换
    - 批量图片转换
    - 图片格式标准化
---

# Any Picture Format

## 目标

当用户明确要求"转换图片格式"、"修改图片格式"、"图片格式转换"时使用。支持任意格式图片到目标格式的转换，包括：本地文件/网络URL/剪贴板图片输入，PNG/JPEG/WEBP 等常见格式输出，单文件或批量处理模式。核心特点：自动检测输入格式、支持透明度处理、批量处理保持原始文件名结构。⚠️ 不适用：用户只是想调整图片大小/裁剪（应使用图片编辑工具）、只是想查看图片信息（应直接使用文件查看器）、没有明确"格式转换"意图。

## 流程

### 输入

输入为本地图片路径、HTTP/HTTPS URL 或 `clipboard`；目标格式可选，未指定时使用配置中的默认格式 `PNG`，批量模式还需目录和递归选项。可选输入包括输出路径、`new/overwrite` 策略、质量参数和配置文件中的格式列表；只在用户明确要求格式转换时触发。

### 执行步骤

#### 核心功能

##### 输入来源

| 来源类型 | 说明 | 示例 |
|---------|------|------|
| **本地文件** | 支持所有常见图片格式（PNG/JPEG/WEBP/GIF/BMP/TIFF/ICO/HEIC等） | `/path/to/image.png` |
| **网络URL** | 自动下载后转换，支持HTTP/HTTPS | `https://example.com/image.webp` |
| **剪贴板** | 直接读取系统剪贴板中的图片 | 用户刚截图后 |

##### 输出格式

默认支持的目标格式（可在config.yaml中扩展）：
- **PNG**：无损压缩，支持透明度
- **JPEG**：有损压缩，文件体积小
- **WEBP**：现代Web格式，体积与质量平衡
- **GIF**：支持动画（静态图片转GIF时首帧）
- **BMP**：无压缩Windows位图
- **TIFF**：专业用途，支持多页

##### 输出策略

| 策略 | 说明 | 文件名变化 |
|------|------|-----------|
| **新建** | 保留原文件，生成新文件 | `image.png` → `image.jpg` |
| **覆盖** | 替换原文件 | `image.png` → `image.png`（格式已变） |

#### 工作流程

##### 1. 需求确认

AI需要确认以下信息（可从用户请求推断）：

- **输入来源**：文件路径/URL/剪贴板
- **目标格式**：输出格式（默认PNG）
- **输出策略**：新建/覆盖/指定路径（默认新建）
- **处理范围**：单文件或批量目录

##### 2. 输入验证

使用脚本验证输入：
```bash
python3 scripts/convert.py validate --source <输入>
```

验证内容：
- 输入来源是否可访问
- 文件是否为有效图片
- URL是否可下载

##### 3. 执行转换

###### 单文件转换
```bash
python3 scripts/convert.py convert \
  --source <输入> \
  --format <目标格式> \
  --output <输出路径> \
  --strategy <new/overwrite>
```

###### 批量转换
```bash
python3 scripts/convert.py batch \
  --directory <目录> \
  --format <目标格式> \
  --recursive \  # 递归处理子目录
  --strategy <新建/覆盖>
```

##### 4. 结果验证

转换后验证：
- 输出文件是否存在
- 文件格式是否正确
- 文件大小是否合理
- 图片质量是否可接受

#### 脚本接口

##### scripts/convert.py

核心转换脚本，提供以下子命令：

###### validate - 验证输入
```bash
python3 scripts/convert.py validate --source <输入>
```

返回：
- `valid`: true/false
- `format`: 检测到的输入格式
- `size`: 图片尺寸
- `error`: 错误信息（如有）

###### convert - 单文件转换
```bash
python3 scripts/convert.py convert \
  --source <输入> \
  --format <目标格式> \
  --output <输出路径> \
  --strategy <new/overwrite> \
  --quality <质量参数>  # 可选，1-100
```

返回：
- `success`: true/false
- `input_path`: 输入文件路径
- `output_path`: 输出文件路径
- `size_before`: 转换前大小
- `size_after`: 转换后大小
- `error`: 错误信息（如有）

###### batch - 批量转换
```bash
python3 scripts/convert.py batch \
  --directory <目录> \
  --format <目标格式> \
  --recursive \
  --strategy <新建/覆盖> \
  --quality <质量参数>
```

返回：
- `total`: 总文件数
- `success`: 成功转换数
- `failed`: 失败数
- `results`: 每个文件的详细结果
- `errors`: 错误信息列表

#### AI执行指南

##### 场景1：用户要求转换单个图片

```
用户："把这个PNG转成JPEG"
AI执行：
1. 确认输入文件（从上下文获取或询问）
2. 调用 validate 验证
3. 调用 convert 转换（默认strategy=新建）
4. 报告结果（文件路径、大小变化）
```

##### 场景2：批量转换文件夹

```
用户："把images文件夹里的图片都转成WEBP"
AI执行：
1. 确认目录和格式
2. 调用 batch 批量转换
3. 汇总结果（成功/失败统计）
4. 报告任何失败的文件
```

##### 场景3：URL图片转换

```
用户："把 https://example.com/image.webp 转成PNG"
AI执行：
1. 调用 validate 验证URL可访问性
2. 调用 convert 转换（脚本会自动下载）
3. 报告结果
```

##### 场景4：剪贴板图片转换

```
用户："把刚才的截图转成JPEG"
AI执行：
1. 调用 convert --source clipboard
2. 指定输出路径（询问或使用默认）
3. 报告保存位置
```

#### 配置参数

见config.yaml，可配置：
- 默认输出格式
- 默认输出策略
- 默认质量参数
- 支持的格式列表

### 输出

#### 输出报告

转换完成后应向用户报告：

```
✓ 转换完成

输入：image.png (2.3 MB)
输出：image.jpg (456 KB)
压缩比：80%

保存位置：/path/to/image.jpg
```

批量转换时：

```
✓ 批量转换完成

总计：25个文件
成功：23个
失败：2个

失败文件：
- corrupted.png：图片损坏
- locked.jpg：权限不足

输出目录：/path/to/output/
```

### 输出管理

#### BenszAPI 任务工作区


### 校验

转换前运行 `scripts/convert.py validate`，确认来源可访问且为有效图片；转换后核对输出存在、格式与目标一致、大小合理、质量可接受，并在批量结果中报告成功数、失败数和每个错误。

### 失败与恢复

#### 特殊处理

##### 透明度处理

- **PNG→JPEG**：自动将透明背景替换为白色
- **带透明度的图片**：保留透明度需选择PNG/WEBP格式

##### 动画处理

- **GIF→其他格式**：使用 PIL 默认行为（提取首帧）
- **其他格式→GIF**：生成静态 GIF（不支持动画生成）

如需动画处理，请使用专门的 GIF 编辑工具。

##### 质量参数

- **JPEG/WEBP**：quality参数控制压缩质量（1-100，默认85）
- **PNG**：使用压缩级别（0-9，默认6）

#### 错误处理

常见错误及处理：

| 错误 | 原因 | 处理 |
|------|------|------|
| 文件不存在 | 路径错误 | 询问用户确认路径 |
| 不支持的格式 | 输入格式无效 | 提示支持的格式列表 |
| 转换失败 | 图片损坏 | 提示原文件可能损坏 |
| 权限错误 | 无写入权限 | 提示更改输出路径 |
| URL无法访问 | 网络问题或URL失效 | 提示检查URL或网络 |


## 约束

<!-- BEGIN COMMON CONSTRAINTS -->
<!-- Source-Hash: sha256:15120201e9e0c7569517261d57ecefb63ac279c26ed13876f8e95b6dc35854d3 -->
<!-- Template-ID: skill-common-constraints; Template-Version: 1; Sync-Policy: exact-block -->

### 公共硬约束

本块由 `docs/templates/skill-common-constraints.md` 统一维护；每个 `SKILL.md` 的 `## 约束` 必须逐字同步本块，不得在副本中改写公共规则。

- 任务需要落盘时，使用唯一的 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/` 根目录；共享材料放入 `shared/`，Skill 专属材料放入该 Skill 的 `input/`、`output/`、`log/`。
- 正式交付物、源代码和正式计划按项目约定保存，不写入任务工作区；未经授权不覆盖、删除、迁移或远程写入。
- 项目维护变更检查 BAC 可用性并记录需求、AI 产出、工具结果、文件改动和验证摘要；BAC 只做过程审计，不替代署名、责任或合规判断。
- 不记录 API Key、访问令牌、密码、Cookie、环境/凭据文件、私有 Prompt、身份信息、本地用户名、主机名或不必要的大体积原始数据。
- 文件路径必须规范化并限制在授权项目范围内；外部 URL、子进程和网络访问遵循最小权限，防止路径遍历、SSRF 和命令注入。
- Skill 版本唯一记录在自身 `config.yaml:skill_info.version`；公开 API、协议、目录或配置变更同步文档与 `CHANGELOG.md`。
- `bensz-collect-bugs` 是一个 Agent Skill；仅将 Bensz Agent Skill 或 Bensz 基础设施本身的设计缺陷交给它。先脱敏写入 `~/.bensz-skills/bugs/`，当前任务不中断，只有用户明确要求才公开上报，禁止直接修改用户已安装的 Skill 源码。

<!-- End of canonical common constraints. -->
<!-- END COMMON CONSTRAINTS -->
