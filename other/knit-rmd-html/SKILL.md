---
name: knit-rmd-html
description: Knit/render R Markdown (.Rmd) to HTML reliably in this repo (auto-bootstrap pandoc, set correct knit_root_dir, and run rmarkdown::render via a Python wrapper).
metadata:
  author: Bensz Conan
  keywords:
    - knit-rmd-html
---

# Knit Rmd → HTML（项目高频场景）

## 目标

Knit/render R Markdown (.Rmd) to HTML reliably in this repo (auto-bootstrap pandoc, set correct knit_root_dir, and run rmarkdown::render via a Python wrapper).

当用户说"knit 出 html / render Rmd / 生成 HTML 报告"时使用本 skill。

版本由 `config.yaml:skill_info.version` 统一管理。

## 流程

### 输入

输入为待渲染的 `.Rmd` 路径；可选输入包括项目根目录、输出文件路径、Pandoc 版本/下载选项和 `rmarkdown::render` 参数。渲染前需确认项目 `knit_root_dir`、R 和必要模板资源可用。

### 执行步骤

#### 直接用法

- 在仓库根目录执行：
  - `python3 skills/knit-rmd-html/scripts/knit_rmd_html.py <input>.Rmd`
  - 输出默认写到 `<input>.Rmd` 同目录：`<input>.html`

#### 常用参数

- 指定输出文件：
  - `python3 skills/knit-rmd-html/scripts/knit_rmd_html.py <input>.Rmd -o <output>.html`
- 指定 pandoc 版本（默认 `3.8.3`）：
  - `python3 skills/knit-rmd-html/scripts/knit_rmd_html.py <input>.Rmd --pandoc-version 3.8.3`
- 不自动安装依赖（只做检测；缺什么就报错）：
  - `python3 skills/knit-rmd-html/scripts/knit_rmd_html.py <input>.Rmd --no-install`
- 静默渲染输出：
  - `python3 skills/knit-rmd-html/scripts/knit_rmd_html.py <input>.Rmd --quiet`

#### 设计要点（为何这样做）

- **不依赖 R 写脚本**：外层用 Python 做编排与环境自检；真正的 knit 仍由 `rmarkdown::render()` 执行。
- **自动补齐 pandoc**：若系统无 `pandoc`，自动下载安装到 `~/.local/pandoc/` 并将 `~/.local/bin` 放到子进程 `PATH` 前面。
- **兼容 Windows ZIP**：安全解压后递归寻找唯一的 `pandoc` / `pandoc.exe`，兼容根目录与 `bin/` 布局并拒绝歧义结果。
- **输出编码稳定**：Rscript 日志始终按 UTF-8 解码并保留真实退出码，不依赖 Windows 控制台 locale。
- **相对路径更稳**：用 `knit_root_dir=dirname(input)`，确保 Rmd 内 `source("xxx.R")` 等相对路径在 knit 时仍可用。

#### 工作原理

1. **环境检测**：检查 `pandoc` 和 `Rscript` 是否在 PATH 中
2. **自动安装**：若缺少 pandoc，根据平台自动下载对应版本到 `~/.local/pandoc/`
3. **渲染执行**：通过 R 的 `rmarkdown::render()` 执行 knit
4. **输出定位**：默认输出到输入文件同目录，可通过 `-o` 参数指定

### 输出

成功时在同级目录生成与 Rmd 同名的 HTML，或写入由 `-o` 指定的输出文件路径；同时保留渲染日志、Pandoc/依赖诊断和任务工作区中的临时产物，不改变输入 Rmd。

### 输出管理

#### BenszAPI 任务工作区


### 校验

校验 Rmd 路径和项目根目录、Pandoc/R 依赖、`knit_root_dir` 与输出 HTML 存在性；渲染退出码为 0 且 HTML 可读取时才报告成功。

### 失败与恢复

Pandoc/R 缺失、引导下载失败、路径越界、渲染超时或 `rmarkdown::render` 返回非零时，保留日志和诊断输出并报告可复现命令；若产生部分输出，由用户按需清理或隔离后再修复依赖/参数重试。


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
