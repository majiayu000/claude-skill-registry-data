---
name: gitnexus-index
description: 管理 GitNexus 代码索引：创建（首次 analyze）、增量更新（status 检测过期后自动更新）、强制重建与修复（--force / --repair-fts / --embeddings）。触发："创建代码索引"、"更新代码索引"、"索引过期了"、"重新建索引"、"修复索引"、"gitnexus 索引"。
---

# GitNexus 代码索引管理

## 概述

**目的**：让 AI 能快速、可靠地为代码仓库创建或更新 GitNexus 代码索引，消除"不知道索引怎么建、过期了怎么更新、坏了怎么修"的运维盲区。

**功能**：环境检测（CLI 是否可用、仓库是否已索引）→ 状态判定（增量更新 or 全量重建 or 修复）→ 执行 `gitnexus analyze` → 校验索引新鲜度 → 故障排查兜底。

**使用场景**：
- AI 首次接手一个新仓库，需要用 GitNexus 查询前，先建立索引
- 代码变更后，检测到索引过期，需要更新
- 索引损坏（查询不全、向量维度不匹配、全文搜索失效）需要修复

## 定位

```
索引请求 → gitnexus-index（本 skill）→ 创建/更新/修复 → gitnexus list/status 校验
```

- **输入**：目标仓库路径（默认当前工作目录）+（可选）操作意图（创建/更新/修复）
- **输出**：索引操作结果 + 索引新鲜度确认
- **边界**：本 skill **生产/管理**索引（建、更新、修），不**消费**索引做规划/审查/执行。与 GitNexus MCP 使用规则（rules/gitnexus-mcp-rules.md）互补：本 skill 保证 MCP 能查到新鲜数据。

## 核心原则

1. **先检测后动手**：执行 `analyze` 前必须先确认仓库是否已索引、索引是否过期，避免盲目全量重建浪费算力
2. **增量优先，全量兜底**：默认 `analyze`（增量更新）；只有索引异常或用户明确要求时才 `--force` 全量重建
3. **以 status 为证据**：索引新鲜度以 `gitnexus status` 输出为准，不凭猜测下结论
4. **结果可校验**：每次操作后用 `gitnexus list`/`status` 确认索引确实建立/更新成功
5. **环境不可用要降级**：CLI 缺失、npx 不可用、非 Git 仓库时，明确告知并给替代方案，不伪造操作结果

## 工作流

```
Step 0 环境检测 → Step 1 状态判定 → Step 2 创建/更新 → Step 3 修复 → Step 4 校验
```

### Step 0：环境检测

1. **解析 runner**（按顺序）：
   ```bash
   # 1) 项目自带 runner（上次 analyze 已落在索引旁）
   test -f .gitnexus/run.cjs && echo "run.cjs 可用"
   # 2) 全局 CLI
   gitnexus --version
   # 3) npx 临时拉取
   npx --yes gitnexus --version
   ```
   - 取第一个可用的作为 runner：`node .gitnexus/run.cjs analyze` → `gitnexus analyze` → `npx gitnexus analyze`。优先项目自带 runner（版本与索引构建一致，避免全局版本漂移导致索引不兼容），全局 CLI 次之，`npx` 临时拉取兜底。
   - 三者都不可用 → 告知用户需安装：`npm install -g gitnexus`，并中止流程。
2. 确认目标仓库（默认当前目录，可传路径）：
   - 非 Git 仓库：`analyze --skip-git` 可索引普通文件夹；否则提示需 Git 仓库。
3. 检查是否已有 `.gitnexusignore`：**仅当仓库含生成物/大型依赖（node_modules、dist、build、vendored 等）时建议配置**排除文件（语法同 `.gitignore`）；纯源码小仓库可跳过，避免过度配置。

### Step 1：状态判定

判断目标仓库索引现状：

```bash
gitnexus status
# 或列出所有已索引仓库
gitnexus list
```

| status 结果 | 判定 | 动作 |
|-------------|------|------|
| 未索引（列表中没有该仓库） | **创建** | 走 Step 2 首次 `analyze` |
| 已索引且新鲜 | **无需操作** | 告知用户索引是最新的，结束 |
| 已索引但过期 | **增量更新** | 走 Step 2 普通 `analyze` |
| 已索引但查询异常/用户要求 | **重建/修复** | 走 Step 3 |

### Step 2：创建 / 增量更新

在仓库根目录执行：

```bash
gitnexus analyze
```

- 首次 = 创建索引；后续 = 增量更新（只解析变更部分）。
- 首次索引默认完成：结构遍历、Tree-sitter 解析、跨文件引用解析、社区聚类、执行流追踪、混合检索索引。
- **大型仓库**建议加 `--skip-embeddings` 提速（语义搜索关闭）；需要语义搜索再加 `--embeddings`。

**仓库别名**：两个仓库 basename 相同（如两个 `app/`）时用 `--name <alias>` 注册别名消歧。

### Step 3：修复

| 故障 | 命令 |
|------|------|
| 查询结果不完整、索引不一致 | `gitnexus analyze --force`（强制全量重建） |
| 仅全文搜索异常 | `gitnexus analyze --repair-fts` |
| 向量维度不匹配/需重建向量 | `gitnexus analyze --embeddings --drop-embeddings`（清旧向量重建） |
| 非 Git 目录误判 | `gitnexus analyze --skip-git` |

### Step 4：校验

操作后必须确认索引就绪：

```bash
gitnexus list     # 确认仓库已注册
gitnexus status   # 确认新鲜度（不再过期）
```

校验不通过 → 回到 Step 3 按故障类型修复；两次修复仍失败 → 停止并报告，不无限重试。

## 配置 .gitnexusignore

大型仓库或需排除生成物时，在仓库根目录创建 `.gitnexusignore`（语法同 `.gitignore`）：

```bash
node_modules/
dist/
build/
*.min.js
```

始终生效，不受环境变量控制。支持 `.gitignore` 式取反（如 `!__tests__/` 强制收录被默认过滤的目录）。

## 环境变量调优

| 变量 | 作用 | 默认 |
|------|------|------|
| `GITNEXUS_MAX_FILE_SIZE` | 大文件跳过阈值（KB） | 512 |
| `GITNEXUS_WORKER_POOL_SIZE` | 解析 worker 数 | 内核数-1（≤16） |
| `GITNEXUS_NO_GITIGNORE=1` | 跳过 `.gitignore` 解析（仍读 `.gitnexusignore`） | - |
| `GITNEXUS_EMBEDDING_DIMS` | 向量维度（需与索引构建一致） | - |

## 索引就绪后

索引建好后，AI 即可用 GitNexus MCP（`context`/`impact`/`query`/`trace` 等）查询。若 MCP 尚未配置，可运行 `gitnexus setup` 配置到编辑器。

## 故障排查速查

| 现象 | 排查 |
|------|------|
| "command not found: gitnexus" | 未安装 CLI；用 `npx gitnexus` 或先安装 |
| 查询结果不完整 | `gitnexus status` 看是否过期，过期则 `analyze` 更新 |
| 索引仍不完整 | `gitnexus analyze --force` 全量重建 |
| 仅搜索异常 | `gitnexus analyze --repair-fts` |
| 向量维度不匹配 | 设 `GITNEXUS_EMBEDDING_DIMS` 或 `analyze --embeddings --drop-embeddings` |
| 索引超时/太慢 | 加 `--skip-embeddings`、`GITNEXUS_MAX_FILE_SIZE` 调大阈值、配置 `.gitnexusignore` |
| 误索引非 Git 目录 | `analyze --skip-git` |

## 更多资源

- 完整命令选项与环境变量清单，参见 [reference.md](reference.md)
- GitNexus MCP 使用规则，参见 `rules/gitnexus-mcp-rules.md`
