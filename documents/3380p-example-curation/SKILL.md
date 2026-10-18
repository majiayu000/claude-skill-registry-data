---
name: 3380p-example-curation
description: "根据用户反馈、生成代码、legacy 片段或评审结果沉淀 Chroma 3380P 的优秀示例和坏示例。用于新增优秀示例、新增坏示例、把片段分类为 good/bad、抽取可复用规则、更新示例 README、维护 `examples/good_clean/`、创建或维护 `examples/bad/`，以及同步技能侧示例索引。"
---

# 3380P 示例沉淀

## 示例沉淀流程

1. 读取 `rules/3380P_project_style.md` 和 `references/example_catalog.md`。
2. 判断用户反馈属于优秀示例、坏示例、混合示例，还是只有规则但代码不足。
3. 完整示例放在项目内：
   - 清理后的优秀示例：`examples/good_clean/<slug>.README.md` 加最小可用 `.pln`、`.dec`、`.pat` 或 helper 片段。
   - 坏示例：`examples/bad/<slug>.README.md` 加最小片段，用来展示 smell。
4. 更新 `references/example_catalog.md`，记录标签、路径、来源链路、适合模仿什么、不适合模仿什么、验证状态。
5. 如果反馈改变 review 策略，同时更新 `skills/3380p-code-review/references/review_checklist.md`。
6. 不要把长篇 raw-doc 或 legacy code 复制进示例。片段只保留足以说明可复用模式或反模式的最小内容。

## README 必备字段

每个 example README 必须包括：

- 这个示例用于什么。
- Codex 应该模仿什么。
- Codex 不应该模仿什么。
- 来源链路：用户反馈、notes、indexes、原始文件、适用时的 PDF 页码/幻灯片，或 legacy 路径。
- 验证状态：已编译、已在 tester 跑过、未编译参考示例，或未知。
- 对坏示例：风险、推荐改法，以及它要强化的检查清单规则。

## 分类规则

- 只有当示例展示了可复用结构，并且边界清楚时，才标为 good。
- 即使原 legacy code 能运行，只要展示的是重复风险，也可以标为 bad。
- 如果片段既有可取模式又有风险，标为 mixed；能拆分时优先抽取成 clean good example。
- 除非已经编译并在 tester 跑过，不要暗示 clean example 可以直接量产。

## 同步规则

`examples/` 是完整示例的事实来源。`references/example_catalog.md` 是技能侧快速索引。新增、重命名或重新分类示例时，两边必须同步。
