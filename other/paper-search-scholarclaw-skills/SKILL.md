---
name: "paper-search"
description: "Searches academic papers using scholar.club API with query keywords. Returns search results in either structured format or raw API response. Use --raw parameter to get original search results without any formatting. Invoke when user asks to search academic papers or query research topics."
version: "1.0.1"
---

# Paper Search

## 功能说明
This skill searches for academic papers using the scholar.club API with user-provided query keywords. It supports two modes:
1. **Formatted Output (Default)**: Returns up to 10 search results in structured format including title, abstract, authors, year, and links. If there are fewer than 10 papers, it will display all available results.
2. **Raw API Response (--raw parameter)**: Returns the complete, unmodified API response in JSON format for further processing.

The results are optimized for easy reading and analysis in Feishu conversations, with support for both formatted presentations and raw data access.

## 返回内容说明

### 默认模式（格式化输出）
- 最多返回10篇相关论文
- 如果搜索结果少于10篇，会展示所有实际找到的论文
- 每篇论文都会进行完整的结构化展示，包含标题、作者、年份、期刊、引用次数、摘要、链接等信息
- 结果格式化为Markdown，便于阅读和分享

### 原始API响应模式（--raw参数）
- 直接返回完整的API响应，没有任何格式化处理
- 包含所有搜索结果的原始数据，便于进一步处理和分析
- 使用JSON格式，保留了API返回的所有字段和结构

两种模式都支持搜索关键词的中文和英文输入。

## 使用方法
@openclaw paper-search [QUERY_KEYWORDS]

### 必选参数
- **QUERY_KEYWORDS**: 搜索关键词或问题（支持中文和英文）

### 可选参数
- **--raw** 或 **-r**: 输出原始API响应（JSON格式），而不是格式化后的结果
- **--output** 或 **-o**: 输出文件路径，将结果保存到指定文件

### 示例
@openclaw paper-search climate change impacts on infectious diseases
@openclaw paper-search 人工智能在医疗诊断中的应用
@openclaw paper-search "machine learning for protein structure prediction"
@openclaw paper-search --raw climate change impacts on infectious diseases
@openclaw paper-search -r 人工智能在医疗诊断中的应用
@openclaw paper-search --raw "machine learning for protein structure prediction"
@openclaw paper-search climate change impacts on infectious diseases --output results.md
@openclaw paper-search -r 人工智能在医疗诊断中的应用 --output raw_results.json

## Input Requirements
- 提供有效的搜索关键词或查询问题
- 关键词应与学术研究相关
- 支持中文和英文查询

## 输出格式说明
该技能会为每篇搜索到的论文生成完整的结构化展示，包含以下所有信息：

```markdown
### [Paper Number]. [Paper Title]
**Authors**: [Author List]
**Year**: [Publication Year]
**Journal**: [Journal Name]
**Citations**: [Citation Count]

**Abstract**: [Paper Abstract]

**Link**: [Semantic Scholar URL]
{% if openAccessPdf %}
**PDF Access**: [Open Access PDF Link]
{% endif %}
```

### 输出示例
```markdown
### 1. Climate change & infectious diseases in India: Implications for health care providers
**Authors**: V. R. Dhara, P. Schramm, G. Luber
**Year**: 2013
**Journal**: The Indian Journal of Medical Research
**Citations**: 67

**Abstract**: Climate change has the potential to influence the earth's biological systems, however, its effects on human health are not well defined. Developing nations with limited resources are expected to face a host of health effects due to climate change, including vector-borne and water-borne diseases such as malaria, cholera, and dengue. This article reviews common and prevalent infectious diseases in India, their links to climate change, and how health care providers might discuss preventive health care strategies with their patients.

**Link**: https://www.semanticscholar.org/paper/b0b901ebe9464c17ab186fe7235989c9afbf0669
```

## Implementation Details

### API Integration
The skill uses the scholar.club API for paper search:
- **API Endpoint**: https://scholar.club/api/v1/papers/search
- **Request Parameters**: 
  - query: URL-encoded search keywords
  - offset: 0 (fixed)
  - limit: 10 (fixed, returns 10 results per request)

### Results Processing

#### 默认模式（格式化输出）
The skill processes the API response to extract and structure:
- Paper title and metadata
- Authors list with affiliations
- Publication information (year, journal, volume, pages)
- Paper abstract and TLDR summary
- Citations count and influential citations
- Open access PDF links (when available)
- Semantic Scholar paper links

#### 原始API响应模式（--raw参数）
The skill returns the complete, unmodified API response:
- No processing or formatting is applied to the results
- Raw JSON data is directly passed through to the user
- All fields and data structures from the API are preserved
- Ideal for further data processing or analysis

### Error Handling
The skill includes error handling for:
- API connection failures
- Invalid API responses
- Network timeouts
- Empty search results

## Dependencies
- requests>=2.31.0: HTTP requests library for API calls
- urllib3>=2.0.7: HTTP client library
