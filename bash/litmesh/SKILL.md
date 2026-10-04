---
name: litmesh
description: 免 API Key 的学术文献检索与引用技能。提供 36 个直连免费公共 API 的工具：Semantic Scholar、PubMed、OpenAlex(Google Scholar)、arXiv、bioRxiv/medRxiv、DOI 全文、统一跨平台检索、自动引用(auto_cite，本地生成 IEEE/BibTeX)。通过 node litmesh.mjs 调用，支持 --render 输出 Markdown。适用于文献调研、综述写作、引用格式化。
agent_created: true
---

# LitMesh 学术文献技能

LitMesh 把多个学术数据库的检索/引用能力聚合成**一个免密钥的命令行工具箱**。默认 `direct` 模式直连免费公共 API，**无需任何 API Key** 即可使用全部 36 个工具。

## 这是什么

- **一份核心，三处适配**：核心是一个环境无关的 Node CLI（`litmesh.mjs` + 编译好的 `lib/`）。WorkBuddy / Claude Code / Codex 三种环境各自用一份说明文件接入，**配置仅走环境变量，互不冲突、可各自自定义**。
- **来源聚合（Mesh）**：一次调用可跨 Semantic Scholar、PubMed、OpenAlex、arXiv、bioRxiv/medRxiv、DOI 检索；`search_papers` 还能统一跨平台检索。
- **自动引文**：`auto_cite` 在本地把正文里的论文提及标注出来，并生成 IEEE 参考文献 + BibTeX（断句 → 真实检索 → 格式化）。

> 需要计费的 `sci_draw` 与额度查询（proxy 模式，需 ai4scholar.net Key）**不在本技能范围内**；本技能严格遵循「免 Key 服务是安装前提」。

## 快速使用（WorkBuddy / Claude Code）

安装后（见下方），直接描述需求即可，例如：「用 LitMesh 检索最近关于 graph neural network 的 PubMed 论文」。技能会运行：

```bash
node "$(dirname "$0")/litmesh.mjs" search_pubmed '{"query":"CRNA anesthesia outcomes","max_results":3}' --render
```

常用命令：

```bash
# 列出全部 36 个工具
node litmesh.mjs --list

# 检索并渲染 Markdown
node litmesh.mjs search_pubmed '{"query":"CRNA anesthesia outcomes","max_results":3}' --render

# 自动引文（文本至少 100 字符）
node litmesh.mjs auto_cite '{"text":"<至少100字符、提及若干论文的句子>","style":"ieee"}'

# 统一跨平台检索
node litmesh.mjs search_papers '{"query":"graph neural network","sources":["semantic-scholar","pubmed","arxiv"]}'

# 查看某工具精确 JSON 参数 schema（便于复现，无需查源码）
node litmesh.mjs --schema search_papers
```

## 配置（仅环境变量，三环境互不冲突、可各自自定义）

| 变量 | 取值 | 说明 |
| --- | --- | --- |
| `LITMESH_MODE` | `direct`（默认）\| `proxy` | 本技能固定用 `direct`（免 Key）。 |
| `LITMESH_TIMEOUT_MS` | 毫秒（可选） | 单工具 HTTP 超时，网络慢可调大（如 `60000`）。 |
| `SEMANTIC_SCHOLAR_API_KEY` | 可选 | 仅提高 Semantic Scholar 匿名限流额度；不设也能用。 |

## 工具总览（36 个，direct 模式）

**统一检索**：`search_papers`

**PubMed**：`search_pubmed` / `get_pubmed_paper_detail` / `get_pubmed_paper_batch` / `get_pubmed_citations` / `get_pubmed_related`

**Semantic Scholar**：`search_semantic` / `get_semantic_paper_detail` / `get_semantic_paper_batch` / `get_semantic_references` / `get_semantic_citations` / `get_semantic_author_papers` / `get_semantic_author_detail` / `get_semantic_author_batch` / `search_semantic_authors` / `search_semantic_bulk` / `search_semantic_paper_match` / `search_semantic_snippets` / `get_semantic_paper_authors` / `get_semantic_recommendations` / `get_semantic_recommendations_for_paper` / `read_semantic_paper` / `download_semantic`

**arXiv**：`search_arxiv` / `download_arxiv` / `read_arxiv_paper`

**bioRxiv**：`search_biorxiv` / `download_biorxiv` / `read_biorxiv_paper`

**medRxiv**：`search_medrxiv` / `download_medrxiv` / `read_medrxiv_paper`

**Google Scholar（经 OpenAlex）**：`search_google_scholar`

**DOI 全文**：`read_by_doi` / `download_by_doi`

**自动引文**：`auto_cite`

完整参数见 `references/api-cheatsheet.md`。

## 安装位置

- WorkBuddy：`~/.workbuddy/skills/litmesh/`
- Claude Code：`~/.claude/skills/litmesh/`（复用本文件）
- Codex：项目根目录（读取 `codex.md`）

详见 `README.md`。
