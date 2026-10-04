---
name: md-to-word
description: 将一个或多个 Markdown 文档转换为格式优美的 Word（.docx），基于 Pandoc + 内置 reference.docx 模板（可选自定义模板），并确保不修改任何原始 Markdown 文件。内置模板已修复命名空间兼容性问题，支持 RGBA 图片自动转换。
metadata:
  author: Bensz Conan
  short-description: Markdown → Word（Pandoc + 多模板 + 安全不覆写）
  keywords:
    - md-to-word
    - markdown
    - docx
    - word
    - pandoc
    - convert
    - template
    - reference.docx
    - RGBA PNG fix
    - 命名空间修复
---

# md-to-word（Markdown 转 Word）

## 目标

将一个或多个 Markdown 文档转换为格式优美的 Word（.docx），基于 Pandoc + 内置 reference.docx 模板（可选自定义模板），并确保不修改任何原始 Markdown 文件。内置模板已修复命名空间兼容性问题，支持 RGBA 图片自动转换。

## 流程

### 输入

输入为一个或多个 Markdown 文件；可选输入包括内置或自定义 `reference.docx`、输出目录、Pandoc 参数和图片处理选项。转换不得修改原始 Markdown，输出路径须在用户授权范围内。

### 执行步骤

#### 你要解决的问题

用户给你一个或多个标准 Markdown 文档，希望把它们转换成**排版美观、可审查、可交付**的 Word（`.docx`），并且能在不同项目里复用同一套转换流程与样式模板。

**常见问题解决方案**：
- **RGBA PNG 导致 Word 警告**：使用 `--fix-images` 自动转换为 RGB 模式
- **图片路径问题**：脚本自动处理相对路径资源引用
- **中文排版问题**：使用 `--template cn-modern` 获得更好的中文样式

#### 内置模板（Pandoc reference.docx）

内置模板文件位于 `assets/`：
- `default`：`assets/reference-default.docx`
- `cn-modern`：`assets/reference-cn-modern.docx`（中文更友好字体/样式）
- `compact`：`assets/reference-compact.docx`（更紧凑段落间距）

#### 推荐执行方式

优先运行确定性脚本 `scripts/md_to_word.py`，避免 AI 手写 Pandoc 命令导致参数缺失或误覆盖。

示例：

```bash
python3 md-to-word/scripts/md_to_word.py \
  --template cn-modern \
  --output-dir /path/to/out \
  /path/to/a.md /path/to/b.md
```

如用户需要自定义样式，允许：
- 使用 `--reference-doc /path/to/reference.docx` 覆盖内置模板（用户自带）。
- 需要用同一份 Markdown 生成多套风格时，使用 `--output-suffix` 避免覆盖（默认不覆盖）。
- 用户不确定模板可选项时，先运行 `python3 md-to-word/scripts/md_to_word.py --list-templates`。

#### 核心工作流

##### 步骤 0：预检查（不写任何输出前）

1. 校验 `md_files` 均存在且为文件。
   - 默认仅接受 `.md/.markdown`；如用户确实给了其他扩展名，必须显式使用 `--allow-any-extension`。
2. 确认 Pandoc 可用（默认执行 `pandoc --version`）；不可用时给出明确安装提示，并停止。
3. 选择模板：
   - 优先 `--reference-doc`（用户显式指定）；
   - 否则使用 `--template`（默认 `default`）。
4. 计算输出路径：
   - 默认：`{input_dir}/{basename}.docx`
   - 单输入且用户想指定输出文件名：使用 `--output /path/to/out.docx`
   - 指定 `--output-dir`：`{output_dir}/{basename}.docx`
   - 若输出已存在：默认报错并停止（除非用户明确要求 `--overwrite`）。

##### 步骤 1：逐文件转换（必须覆盖全部输入）

对每个 Markdown 文件：
- **图片处理**（可选，`--fix-images`）：
  - 在 MD 所在目录创建 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/md-to-word/{yyyy-mm-dd-hh-mm}/` 隐藏工作目录
  - 创建 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/md-to-word/{yyyy-mm-dd-hh-mm}/output/images-rgb/` 存放转换后的图片
  - 创建 MD 副本，更新所有图片链接指向 RGB 版本
  - 仅转换非 RGB 模式的图片（RGBA/P/L 等），RGB 图片直接复制
- 以**非 shell**方式调用 Pandoc（防止命令注入）。
- 自动设置 `--resource-path`，包含 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/md-to-word/{yyyy-mm-dd-hh-mm}/` 目录。
- 生成 `.docx` 到目标输出路径。
- 可选：使用 `--clean` 转换后清理 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/md-to-word/{yyyy-mm-dd-hh-mm}/` 工作目录（默认保留便于增量转换）

##### 步骤 2：轻量自检（输出后必须做）

- [ ] 输入 Markdown 文件的内容未被修改（可选：对关键输入做 hash 前后对比）
- [ ] 输出 `.docx` 均成功生成且路径符合预期
- [ ] 未发生意外覆盖（除非用户明确要求）
- [ ] 如存在图片/链接，Word 中渲染正常（无法验证时说明原因与建议）

### 输出

#### 输入输出

**输入**
- `md_files`：一个或多个 Markdown 文件路径（建议 `.md` / `.markdown`）
- 可选：`template`（内置模板名）或 `reference_doc`（自定义 reference.docx 路径）
- 可选：`output_dir`（输出目录）

**输出**
- 对每个输入 Markdown，生成一个同名 `.docx`（默认输出到输入文件同目录；也可输出到 `output_dir`）

### 输出管理

#### BenszAPI 任务工作区


### 校验

转换前检查输入扩展名、文件存在性、Pandoc/Pillow 可用性和模板；转换后核对每个 `.docx` 存在、可打开、图片/链接渲染正常（无法验证时明确说明），且源 Markdown 未被覆盖。

### 失败与恢复

#### Word 兼容性问题与解决方案

##### 问题 1：Word 打开时提示"发现无法读取的内容"（模板命名空间问题）

**原因**：自定义 Word 模板使用了非标准的 XML 命名空间前缀（`ns0:`），与 Pandoc 的 `--reference-doc` 参数结合时可能导致 Word 兼容性问题。

**解决方案**：
1. **内置模板已修复**：所有内置模板（`cn-modern`、`compact`、`default`）已更新为使用标准命名空间
2. **自动兼容性参数**：脚本自动添加 `--markdown-headings=atx` 参数提高兼容性
3. **自定义模板修复**：使用 `scripts/fix_template_namespace.py` 修复自定义模板

```bash
# 修复自定义模板
python3 md-to-word/scripts/fix_template_namespace.py \
  --input /path/to/custom-template.docx \
  --output /path/to/custom-template-fixed.docx \
  --verify
```

##### 问题 2：RGBA PNG 图片导致 Word 警告

**原因**：Markdown 中引用的 PNG 图片使用 RGBA 模式（带透明通道），这种格式在嵌入 Word 文档时可能导致兼容性问题。

**解决方案**：使用 `--fix-images` 参数自动转换

```bash
python3 md-to-word/scripts/md_to_word.py \
  --fix-images \
  --template cn-modern \
  your-document.md
```

**工作原理**：
1. 在 MD 所在目录创建 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/md-to-word/{yyyy-mm-dd-hh-mm}/` 隐藏工作目录
2. 创建 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/md-to-word/{yyyy-mm-dd-hh-mm}/output/images-rgb/` 存放转换后的图片
3. 扫描 Markdown 中引用的所有图片（支持 PNG/JPG/GIF/BMP/WebP）
4. 检测图片模式，仅转换非 RGB 模式的图片
   - RGBA → RGB（白色背景）
   - P/PA/LA 等 → RGB
   - RGB/L → 直接复制
5. 创建 MD 副本，更新图片链接指向 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/md-to-word/{yyyy-mm-dd-hh-mm}/output/images-rgb/`
6. 使用 MD 副本执行 Pandoc 转换
7. 默认保留 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/md-to-word/{yyyy-mm-dd-hh-mm}/` 便于增量转换，使用 `--clean` 清理

**工作目录结构**：
```
your-doc.md
your-doc.docx
.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/md-to-word/{yyyy-mm-dd-hh-mm}/              # 隐藏工作目录（默认保留）
├── your-doc.md          # MD 副本（图片链接已更新）
└── output/
    └── images-rgb/      # RGB 模式图片
        ├── figure1.png  # 转换后（RGBA→RGB）
        └── photo.jpg    # 直接复制（已是 RGB）
```

**依赖**：
- 需要 Pillow 库：`pip install Pillow`
- 如未安装，脚本会跳过图片修复并给出提示

**清理选项**：
- 默认保留 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/md-to-word/{yyyy-mm-dd-hh-mm}/` 工作目录，便于后续增量转换
- 使用 `--clean` 转换后自动清理工作目录
- 手动清理：`rm -rf /path/to/md/.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/md-to-word`


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

### Skill 专属约束

#### 安全约束

- 你**只能读取**用户提供的 Markdown 文件及其引用资源（如图片）。
- 你**绝不能修改/覆盖/重命名/删除**任何输入 Markdown 文件或其同目录已有文件。
- 默认**不覆盖**任何已存在的输出 `.docx`；除非用户明确要求覆盖，才可使用 `--overwrite`。
- 输出文件只能是**新生成的** `.docx`（以及测试目录中的中间产物）。
