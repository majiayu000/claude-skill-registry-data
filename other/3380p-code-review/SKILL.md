---
name: 3380p-code-review
description: "评审 Chroma 3380P ATE 的 `.pln`、`.dec`、`.pat`、helper header 和生成的测试程序草稿，重点检查 bug、可维护性风险、cleanup 缺失、multi-site 处理缺失、无依据假设、测试或验证缺口。用于代码评审、检查清单评审、审计、质量门禁，以及根据重复反馈维护 3380P 评审检查清单。"
---

# 3380P 程序代码评审

## 评审流程

1. Review 前读取 `rules/3380P_project_style.md` 和 `references/review_checklist.md`。
2. 按被评审代码类型读取相关 topic note 或 index：DEC、PAT、PLN、DC measure、supply sweep、register helper、WRITE_PAT_MEM、capture、TMU 或操作工具主题。
3. 如果有路径，检查引用到的项目文件，尤其是 `.dec`、`.pln`、`.pat`、helper header、clean/bad examples。
4. 先输出 findings，按严重程度排序；本地文件可定位时附文件和行号。
5. 优先关注行为风险：pin/resource 假设错误、multi-site 逻辑破损、cleanup 缺失、helper contract 编造、sweep 方向错误、datalog/judge 缺失、语法未验证。
6. 摘要放在后面。没有发现问题时，也要说明剩余验证风险，例如未编译或未在 tester 验证。

## 检查清单维护

- `references/review_checklist.md` 是维护中的检查清单。
- 用户给出新评审反馈，或发现重复问题时，在最接近的章节追加简短检查项。
- 新检查项必须带来源指针：用户反馈、示例路径、note/index 路径或 legacy 文件路径。
- 除非用户明确说某条规则已废弃，否则不要删除检查项。
- 不要把长代码块复制进检查清单；描述 smell、风险和推荐检查方式。

## 评审输出格式

按这个顺序输出：

1. Findings，包含严重程度；有本地文件时附文件和行号。
2. Open questions 或 assumptions。
3. 测试或验证缺口。
4. Findings 之后再给简短摘要。

评审生成草稿时，要明确检查回答是否保留来源链路，并声明未编译或未在 tester 验证状态。
