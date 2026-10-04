---
name: research-toolkit
description: "显式调用的共享学术检索工具层：统一查询 OpenAlex、Crossref、PubMed、arXiv 和 ClinicalTrials.gov，规范化记录、去重并核验 DOI/PMID/arXiv/NCT。Use when 调试研究工具、批量规范化论文元数据、查重或验证学术标识符；一般论文问题应使用相应专业研究 Skill。"
license: MIT
metadata:
  architecture: "shared-tool-layer"
  language: "zh-CN"
---

# 统一研究工具层

本技能提供稳定、低依赖的命令行接口，不判断论文质量，也不直接给医学建议。

## 使用

脚本仅依赖 Python 标准库：

    python scripts/researchctl.py search --provider openalex --query "retrieval augmented generation" --limit 10 --output results.json
    python scripts/researchctl.py verify --id-type doi --identifier "10.1038/s41586-021-03819-2" --output verified.json
    python scripts/researchctl.py dedupe --input combined.json --output deduped.json

可用 provider：openalex、crossref、pubmed、arxiv、clinicaltrials。默认输出 [references/evidence-schema.md](references/evidence-schema.md) 的统一 JSON；网络失败以非零状态退出并在 stderr 给出原因。

## 操作纪律

- 一次搜索先取 10–20 条；筛选后才扩大或深读。
- PubMed 无 API key 时保持低请求频率；不要并发轰击公共 API。
- verify 会用主注册源核验标识符；DOI 再用 OpenAlex 补查撤稿/OA 状态。它不证明研究结论正确。
- 以 DOI、PMID、arXiv、NCT 为首选去重键；无标识符时才使用规范化题名和年份。
- 开放获取状态为 unknown 时不要猜测；只使用合法 OA 全文。
- is_retracted=false 仅表示所查来源没有标记撤稿，不等于完成所有撤稿/勘误检查。
- 输出文件可能含长摘要；进入模型上下文前只选任务需要的字段。

数据源与限制见 [references/source-registry.md](references/source-registry.md)。
