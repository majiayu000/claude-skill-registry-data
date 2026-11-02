---
name: help-me-homework
description: 按老师要求与评分细则完成课程题目、代码、实验及 LaTeX 报告，检查并整理未压缩的 submit 材料。
---

# 作业完成与交付

读[共享规则](../help-me-shared/references/core.md)和[作业交付流程](../help-me-shared/references/homework.md)。

**正式报告必须使用 LaTeX：在 `work/report/`（或本任务实际工作目录）维护完整 `.tex` 源码，实际编译 PDF，检查后将最终 PDF 放入 `submit/`。Markdown 仅可作为内部大纲或草稿，不能替代报告交付。** 不因用户未重复指定 LaTeX、已有 Markdown 文件或缺编译器而降级；编译受阻时保留源码并明确报告尚未完成。只有用户明确变更格式才调整；老师明确要求不兼容格式时先核实依据并解决冲突，不能自行换成 Markdown。只分析、只审稿、只要源码或无需报告的任务遵守其实际范围。

1. 复用本次已核验要求；不足时加载[要求技能](../help-me-assignment/SKILL.md)。开始生成前展示要求摘要，明确后继续。
2. 读[运行工具](../help-me-shared/references/runtime.md)创建 work/code、work/report、work/submit；遇冲突使用 work_codex，继续同任务显式复用原目录，不动原材料。
3. 根据要求/文献/评分覆盖实施，先补必做和高权重证据，再做有价值的扩展。只声称实际读过/运行过的内容。
4. 写报告时读[报告路线](../help-me-shared/references/report.md)和[排版规范](../help-me-shared/references/formatting.md)，按其中的 LaTeX 交付约定生成；先理清项目目的、每个实验的目的/对照及相互关系，使大节按问题证据递进、小节按逻辑与实验依赖展开。按需调用 nature skills 时一并传递 LaTeX 输出要求，老师模板优先，不虚构因果或决策历史。
5. 按[验证规则](../help-me-shared/references/verification.md)检查实际解答、代码和结果；核对真实 `.tex` 主入口、配套资源、由最新源码编译的 PDF 及每页显示，再将正式材料整理入 submit。只有 `.md`、改后缀文件或旧 PDF 均不算报告完成。内部来源记录/日志/QA 不放入正式作业。

**默认停在未压缩的 submit。** 老师要求 ZIP、要求 Overleaf 源码或要求“完成全部作业”都不构成本次压缩授权。用户明确说打包/压缩后才创建归档并解压核验；上传课程系统仍需单独明确请求。

交付分别说明要求覆盖、实测/未验证、文件位置、散装/已打包/已提交状态，不把编译成功当作导出和视觉验证。
