---
name: bio-doc-fetcher
description: 专门用于获取生物信息学工具文档（如 Bioconductor, CRAN, PyPI）的技能，具备处理特定领域文档站点的重定向、反爬及镜像切换能力。
version: 1.0
evolved_from: none
evolution_type: CAPTURED
---

# Bio-Doc Fetcher

## 适用场景
- 需要获取 R (Bioconductor/CRAN) 或 Python (PyPI) 生物信息学软件包的安装指南、API 文档或教程（Vignettes）。
- 官方主站访问缓慢、触发反爬机制或需要查找特定版本的旧文档。
- 需要从复杂的文档结构中快速定位核心代码示例。

## 步骤
1. **源识别**：根据包名和用途确定其所属仓库：
   - R 语言统计包 -> CRAN
   - R 语言组学分析包 -> Bioconductor
   - Python 包 -> PyPI
   - 实验室内部工具 -> GitHub/GitLab
2. **构造初始 URL**：
   - Bioconductor: `https://bioconductor.org/packages/release/bioc/html/[PACKAGE].html`
   - CRAN: `https://cran.r-project.org/web/packages/[PACKAGE]/index.html`
   - PyPI: `https://pypi.org/project/[PACKAGE]/`
3. **执行抓取与重定向处理**：
   - 使用 `web_fetch` 访问。如果返回 403 或 404，立即尝试 `web_search` 搜索该包的 `pkgdown` 页面或 ReadTheDocs 页面。
4. **镜像切换（可选）**：
   - 若主站不可用，构造镜像站 URL（如清华 TUNA 镜像）：`https://mirrors.tuna.tsinghua.edu.cn/CRAN/web/packages/[PACKAGE]/index.html`。
5. **核心信息提取**：
   - 提取 `Installation` 部分的命令（如 `BiocManager::install()`）。
   - 提取 `Vignettes` 或 `Tutorial` 的 HTML 链接。
   - 提取 `Dependencies` 列表以预判安装风险。

## 工具和命令
- `web_fetch(url="...")`: 直接抓取已知结构的文档页。
- `web_search(query="site:bioconductor.org [PACKAGE] vignette")`: 定位深度文档。
- `web_search(query="[PACKAGE] R package documentation mirror")`: 寻找备用源。

## 注意事项
- **PDF 陷阱**：Bioconductor 和 CRAN 默认提供大量 PDF 手册，`web_fetch` 无法直接阅读。应优先寻找 `vignettes/` 目录下的 HTML 版本。
- **版本差异**：Bioconductor 的包与 R 版本强绑定，抓取时需确认是 `release` 还是 `devel` 分支。
- **反爬策略**：部分生物信息学门户网站（如某些大学的服务器）对频繁请求敏感，建议在 `web_fetch` 失败后间隔使用 `web_search`。

## 示例
**任务：获取 R 包 `DESeq2` 的安装和基本用法**
1. **Action**: `web_fetch(url="https://bioconductor.org/packages/release/bioc/html/DESeq2.html")`
2. **Result**: 发现页面，提取安装命令 `BiocManager::install("DESeq2")`。
3. **Action**: 发现 Vignettes 链接为 `../vignettes/DESeq2/inst/doc/DESeq2.html`，构造完整 URL 并再次抓取。
4. **Output**: 提供安装步骤及 `DESeqDataSetFromMatrix` 的核心代码示例。