---
name: github-raw-fetch
description: 当用户提供 GitHub 文件页面链接，或希望读取某个仓库中的源码、配置、README、Markdown、docs 内容时，使用此技能。技能支持将 `github.com/<owner>/<repo>/blob/<ref>/...` 转换为 `raw.githubusercontent.com` 链接并获取内容；读取仓库 docs 时先列出仓库根目录、按真实结构定位 `docs/` 目录（语言子目录、索引），不要假设所有仓库都有固定目录或 `agent_router.md`（该文件仅当根目录确实存在时才可选参考）。
---

# GitHub Raw Content 与仓库文档读取

## 1. 技能目标

当用户要求读取 GitHub 上的源码、配置、README、Markdown 或 docs 内容时，按下面的顺序执行：

1. 先识别仓库、`ref`、目标文件或目标主题
2. 需要定位文档时，先列出仓库根目录，找到真实存在的文档目录与入口
3. 按实际目录结构逐层定位目标文件（不猜路径、不假设固定布局）
4. 将最终路径转换成 raw 链接
5. 使用 `curl` 获取文件内容

## 2. 适用范围

- 用户提供的是 GitHub 文件页面链接，例如：
  - `https://github.com/<owner>/<repo>/blob/<ref>/<path-to-file>`
- 用户提供的是 raw 链接，例如：
  - `https://raw.githubusercontent.com/<owner>/<repo>/<ref>/<path-to-file>`
- 用户要读取的是 README、源码、配置、脚本、JSON、YAML、Markdown 等纯文本文件
- 用户要读取的是某个仓库的 docs、文档入口、FAQ、指南、设计文档、API 文档
- 用户只给出了仓库和想看的文档主题，但真实 docs 路径需要按仓库实际结构定位

以下场景不属于本技能的直接处理范围：

- 仓库首页、目录页、Pull Request、Issue、Commit 页面本身
- 需要递归遍历整个仓库或批量抓取大量文件
- 明显的二进制文件，例如图片、压缩包、模型权重

## 3. 核心规则

### 3.1 标准 GitHub 文件页转 raw 链接

如果输入链接满足：

```text
https://github.com/<owner>/<repo>/blob/<ref>/<path-to-file>
```

则转换为：

```text
https://raw.githubusercontent.com/<owner>/<repo>/<ref>/<path-to-file>
```

转换时必须遵守以下规则：

1. 将域名 `github.com` 替换为 `raw.githubusercontent.com`
2. 删除路径中的 `/blob/`
3. 其余路径保持不变
4. 分支、tag、commit SHA 等 `<ref>` 必须原样保留

### 3.2 已是 raw 链接

如果用户提供的本身就是 `raw.githubusercontent.com` 链接，则不要重复转换，直接使用该链接。

### 3.3 读取仓库 docs：先列目录，按真实结构定位

`agent_router.md` **不是前置依赖，不是所有仓库都有该文件**。读取仓库文档的默认流程是：

1. 先列出目标仓库根目录（见 §3.5 的目录探查方式），确认：
   - 根 `README.md` / `README_EN.md` 是否存在；
   - 文档目录的真实名称与位置：`docs/`、`doc/`、`documentation/`、`docs_zh/` 等都以列表结果为准；
2. 进入文档目录后按实际结构继续定位：语言子目录（如 `docs/zh/`、`docs/en/`，以实际为准）→ 索引文件（`README.md`、`index.md` 等）→ 目标文档；
3. 每层都用目录列表确认，**不要凭经验猜测路径**；
4. 找不到 `docs/` 等文档目录时，退化为读取根 README 或仓库内与主题相关的 Markdown，并如实说明所依据的结构。

### 3.4 可选加速：`agent_router.md` 仅在确实存在时使用

如果根目录列表里**确实存在** `agent_router.md`（部分仓库用它声明文档目录结构与入口映射），可先读取它辅助定位：

```text
https://raw.githubusercontent.com/<owner>/<repo>/<ref>/agent_router.md
```

规则：

1. `agent_router.md` 必须与目标文档使用相同的仓库和相同的 `ref`
2. 该文件缺失或返回 404 时**不要阻塞**：直接回到 §3.3 按真实目录结构继续定位，并说明“未发现 router，按实际 docs 目录定位”
3. router 中的目录映射只作提示，最终以目录列表确认的真实路径为准

### 3.5 目录探查与内容获取方式

- 目录列表使用 GitHub Contents API（单层、一次一个目录）：

```bash
curl.exe -s -L "https://api.github.com/repos/<owner>/<repo>/contents/<path>?ref=<ref>"
```

`<path>` 为空时列出仓库根目录。响应为 JSON 数组，逐项含 `name`、`type`（file/dir）、`path`、`html_url`、`download_url`。

- 获取文件正文时使用 raw 链接：

```bash
curl.exe -L "https://raw.githubusercontent.com/<owner>/<repo>/<ref>/<path-to-file>"
```

不要依赖 GitHub HTML 页面渲染结果作为文件正文。

### 3.6 docs 路径拼接原则

在按目录定位时，重点识别这些信息：

- docs 实际根目录在哪里
- 是否存在多语言目录
- 逻辑名称（如 `quick_start`、`user_guide`）对应的真实子目录
- 文档入口是 `README.md`、`index.md` 还是其他文件

最终原则：

1. 先列目录，再决定路径；路径以列表结果为准，而不是以仓库默认习惯为准
2. 不确定时给出已确认的目录片段，不要硬造不存在的路径

## 4. 标准操作流程

1. 识别用户给的是 GitHub 文件页链接、raw 链接，还是“读取某仓 docs”的意图
2. 从链接或上下文中提取 `<owner>`、`<repo>`、`<ref>`、目标路径或目标主题
3. 如果目标属于 docs 体系，先列出仓库根目录定位真实文档目录（可选：根目录存在 `agent_router.md` 时先读它加速）
4. 按真实目录结构定位目标文件
5. 将最终路径转换为 raw 链接
6. 使用 `curl` 获取内容
7. 将结果返回给用户：
   - 用户想快速了解内容时，优先给摘要和关键片段
   - 用户明确要求原文时，再返回全文或尽量完整展示
   - 必要时附上最终 raw URL，方便复用

## 5. 推荐命令模板

### 5.1 列出仓库根目录

```bash
curl.exe -s -L "https://api.github.com/repos/<owner>/<repo>/contents/?ref=<ref>"
```

### 5.2 列出文档子目录

```bash
curl.exe -s -L "https://api.github.com/repos/<owner>/<repo>/contents/docs/zh?ref=<ref>"
```

### 5.3 读取真实文档或普通文件

```bash
curl.exe -L "https://raw.githubusercontent.com/<owner>/<repo>/<ref>/<actual-path>"
```

## 6. 示例（Ascend 官方仓，均真实存在）

### 示例 1：标准 GitHub 文件页转 raw

输入：

```text
https://github.com/Ascend/msprof/blob/master/README.md
```

转换后：

```text
https://raw.githubusercontent.com/Ascend/msprof/master/README.md
```

再使用：

```bash
curl.exe -L "https://raw.githubusercontent.com/Ascend/msprof/master/README.md"
```

### 示例 2：读取某仓库的文档（按真实 docs 目录定位）

输入：

```text
请读取 Ascend/msprof 仓库中关于交付文件字段含义的说明文档
```

正确流程：

1. 列出根目录：`https://api.github.com/repos/Ascend/msprof/contents/?ref=master`，确认存在 `docs/`、`README.md` 等
2. 列出 `docs/zh/user_guide`：确认真实文件名（以列表结果为准），例如存在 `profile_data_file_references.md`
3. 读取真实路径：

```bash
curl.exe -L "https://raw.githubusercontent.com/Ascend/msprof/master/docs/zh/user_guide/profile_data_file_references.md"
```

说明：`Ascend/msprof` 根目录存在 `agent_router.md`，读取时可先读它作为路径提示；但流程不以它为前提，按 §3.3/§3.4 处理。

### 示例 3：没有 `agent_router.md` 的仓库

输入：

```text
请读取 Ascend/community 仓库的文档目录结构
```

正确流程：直接列出根目录并逐层确认文档目录，例如：

```bash
curl.exe -s -L "https://api.github.com/repos/Ascend/community/contents/?ref=master"
```

然后按列表结果继续定位。不要假设该仓存在 `agent_router.md`，也不要以某个固定 `docs/` 路径直接拼接。

## 7. 错误处理与约束

- 如果链接不是 GitHub 文件页或 raw 文件链接，要明确告知该 URL 不符合本技能处理模式
- 如果列表或 raw 返回 404：
  - 先确认仓库、`ref` 是否正确
  - 若目录确实不存在，报告已确认的目录列表片段，不要硬造路径
- 如果 `agent_router.md` 返回 404：说明“未发现 router”，回到真实 docs 目录结构继续定位，不要中断
- 如果返回的是 HTML 而不是文本，说明抓取方式不对，优先检查是否误用了 GitHub 页面链接而非 raw 链接
- 如果目标内容明显为二进制或体积过大，不要强行按纯文本展开；应告知用户文件类型，并优先返回链接或简要说明
- Contents API 未认证时有访问限额，尽量少列表、多直接读取已知文件

## 8. 输出建议

- 如果用户是为了阅读或分析文件，优先提炼关键内容，而不是机械粘贴全文
- 如果用户明确要求 raw content 或原文，再按需返回完整文本
- 读取 docs 时可以顺带说明最终路径是如何按目录结构定位出来的
- 分析代码或配置时，可顺带说明关键函数、入口、配置项或用途
