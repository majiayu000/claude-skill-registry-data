---
name: academic-search
description: "为模糊、跨学科或尚未确定领域的论文检索请求选择专业研究 Skill，并汇总跨领域证据。Use for 跨学科论文搜索、多个学科共同回答一个问题、尚不清楚应走哪个专业检索流程；明确的 AI/计算机任务直接用 ai-computing-research，明确的临床医学/健康任务直接用 biomedical-evidence。"
license: MIT
metadata:
  source: "ustc-ai4science/academic-search"
  upstream_version: "1.2.0"
  upstream_commit: "3ae68445"
  architecture: "thin-router"
  language: "zh-CN"
---

# 学术检索编排器

本技能只做三件事：识别领域、把任务交给最窄的专业流程、合并不同领域的证据。不要在这里复制专业检索规则。

## 路由

1. 读取 [references/routing.md](references/routing.md)。
2. 只有一个明确领域时，按路由表使用对应专业 Skill，不继续加载本技能的其他参考资料。
3. 涉及两个以上领域时，为每个领域分别形成查询与证据账本，再按统一字段合并；不要用同一证据等级跨领域机械排序。
4. 目标只是总结用户已给材料时，使用 research-summarizer；需要网页和非学术来源交叉核验时，组合 evidence-research。
5. 尚无专业 Skill 的领域，采用 [references/fallback.md](references/fallback.md) 的保守通用流程，并在结果中标明“通用回退”。

## 共享工具

如环境中安装了 research-toolkit，用它完成元数据检索、规范化、去重和 DOI/PMID/arXiv/NCT 核验。工具输出只是候选证据，不替代专业质量判断。工具不可用时可使用已有连接器、官方 API 或浏览器，但保持同一证据字段。

## 跨领域合并规则

- 先按领域分别报告结论和证据强度，再说明它们能否共同支持最终判断。
- 冲突可能来自研究问题、因果标准、时间尺度或“证据”定义不同；先解释差异，不强行投票。
- 每个重要主张紧邻可核验引用；不存在或未核验的标识符绝不补造。
- “对生活有用”不等于立刻行动。医学建议始终服从 biomedical-evidence 的安全边界。
- 默认输出精选证据而非长链接清单，并附数据库、查询式、截至日期和主要缺口。

## Token 纪律

- 先路由再加载：单领域任务只加载一个专业 Skill。
- 每个领域先看元数据/摘要，筛选后才读少量全文。
- 跨领域传递紧凑证据账本：主张—证据—强度—局限—标识符。
- 达到停止条件后停止，不用重复搜索制造“全面”的错觉。
