---
name: picvero-review
description: "把商品原图与生成图对照，检查形状、部件、标识和文字有没有改错，并指出具体问题。用于上架前检查或判断图片是否失真；只要求检查时不自动改图。"
metadata:
  short-description: "商品图片检查"
---

# Picvero · 商品图片检查

读取 [共用约定](references/workflow.md) 与 [审核规则](references/review.md)。

必须查看当前商品参考与候选，核对标签、结构、数量、文字和事实。只有候选图时，可检查画面可见问题，但商品一致性为 unknown，不能宣称与原商品一致。

按 identity、text、claims、visual、usage 五项给出依据。使用 [运行记录](references/runtime.md) 的审核模板时，保留全部参考与候选版本哈希，填入实际检查证据。程序验证结构不替代看图。

用户只是让审核时，交付检查与具体修改建议。用户同时授权修正时，再用内置改图工具在限定范围修改并复检，不重复索取已授权的确认。

基础技术测量可以调用本地 inspect/check。报告中的“未检查”或“不确定”不能解释为通过，AI 判断也不等于平台保证审核通过。
