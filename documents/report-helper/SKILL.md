---
name: report-helper
description: |
  当用户说「深度研究 X」「深入研究 X」或要求生成某产品、公司、概念、人物、产业链、政策、趋势的深度研究/发展研究报告时触发，自动进行联网搜索和研究，产出排版后的 PDF 文档，总字数通常 1-3 万字。
  作者：嘉然 | GitHub: https://github.com/Jiaranbb/report-helper
---

# Report Helper

## 触发提示

触发：用户明确说 `深度研究`、`深入研究`、`深度分析报告`、`发展研究报告`、`产业研究报告`，对象可以是产品、公司、概念、人物、产业链、政策或趋势。

不触发：简单名词解释、普通概述、一般「分析一下」、不需要长报告和 PDF 的问答。

拿到触发请求后，先在 chat 里输出范围对齐简报：

```markdown
【关卡一 · 研究范围对齐】
研究对象：{具体名称，模糊的先收敛}
类型：产品 / 公司 / 概念 / 人物 / 产业链 / 政策 / 趋势
研究动机：{为什么研究，最近发生了什么}
特别关注：{用户希望深入的方向；没有就写「无特别指定」}
成品体裁：{按用户原话判断，如「正式发展研究报告」「产业研究报告」「叙事型深度研究」}
交付格式：PDF
报告署名：{读取 config.local.json 的 author；如果为空，必须请用户填写}

执行模式（请选）：
- 【交互模式】默认。关卡二、三会停下等你审核后再继续
- 【auto 模式】一路跑到底，中间不等你。关卡二、三的自评简报还是会输出，但不等确认

以上理解是否正确？选哪种模式？
```

用户确认前不要进入搜集。用户说「自动进行」「一路跑」可理解为 auto 模式，但仍需完成关卡一复述并拿到确认。

## 模式分流

- **交互模式**：关卡一、二、三都要停住等用户确认。
- **auto 模式**：关卡二、三照样输出简报，但不等确认；信息严重不足必须补搜，原创性/体裁自评失败必须回炉。
- 任何模式下都不能编造缺失事实。搜不到的信息写入「未搜到 / 存疑」。

## 工作流

1. **搜集资料**：读取 `references/workflow.md` 和 `references/subagent-research-prompt.md`。按三路 research worker 分工搜集，并把中间资料落盘到配置的 `intermediate_dir`（默认 `./output/intermediate/{topic-slug}-{YYYY-MM-DD}/`）。
2. **信息充分性审计**：按 `references/workflow.md` 输出关卡二审计。交互模式等待用户；auto 模式按建议继续，严重缺口必须补搜。
3. **形成判断**：按 `references/workflow.md` 做写作准备审计，确认核心判断、证据链和体裁路由足以进入写作。
4. **选择体裁并写正文**：读取 `references/report-template.md`、`references/writing-style.md` 和 `references/source-citation-rules.md`。对象是产品、公司、概念或人物时，再读取 `references/adaptations-by-type.md`；对象是公司时，正文必须包含成长性和估值相关的定量分析。
5. **审核**：读取 `references/review-checklist.md`，命中即改，直到通过。
6. **生成交付物**：读取 `references/delivery.md`；保存内部 Markdown 构建稿，按需追加 log，生成 PDF。
7. **经验沉淀**：遇到 PDF、事实核查、log、未来预测、报告结构或 skill 维护问题时读取 `references/gotchas.md`；本次发现新坑，或用户指出流程/事实/结构问题时，先补充 gotchas，再继续交付。

## 配置与隐私

- 共享配置模板是 `config.example.json`；本地私有配置写入 `config.local.json`，不要提交。
- 首次安装时必须让用户填写报告署名 `author`；不要默认使用工具作者名。
- 首次使用或环境不明确时，先运行 `python3 scripts/check_environment.py`；不通过时按脚本提示安装依赖或补配置。
- 脚本读取顺序：内置默认值 → `config.local.json`（或 `REPORT_HELPER_CONFIG` 指向的 JSON）→ `REPORT_HELPER_*` 环境变量。
- 报告署名在首次配置时自定义昵称；本地绝对路径、私有日志标题、账号标识等个人配置只放在 `config.local.json` 或环境变量里。

## 输出规则

- 正文结构以 `references/report-template.md` 为准，不在 `SKILL.md` 里展开目录。
- 用户要「发展研究报告 / 产业研究报告 / 政策研究 / 趋势报告 / 2026-2030 报告」时，使用 `report-template.md` 的 **A. 正式研究报告结构**。
- 用户要产品、公司、人物、概念深度研究且未指定正式体裁时，使用 `report-template.md` 的 **B. 叙事型深度研究结构**。
- 用户明确指定目录或栏目时，用户指定优先；仍需保留必要的信息来源章节。
- 进入正文写作前必须完成最新数据校验；如果研究对象有近 12-24 个月数据更新，必须优先查到最新官方/监管/财报/原始披露或权威报道后再写。
- 公司研究不能只写叙事深度；必须加入成长性、盈利质量、现金流/融资、估值或可比公司等定量分析。非上市公司缺少公开估值或收入数据时，要写明缺口和替代观察指标。
- 正文关键事实判断必须使用 `<sup>a1</sup>` 这类上标标注来源等级和编号；正文前声明编号规则，末尾用「信息来源与分级」按 a/b/c/d 分组列出完整来源，没有 c 和 d 就不写对应小节。
- 默认输出到 `./output/`；可用 `config.local.json` 或 `REPORT_HELPER_*` 环境变量改路径。
- PDF 文件名建议为 `{研究对象}深度研究报告.pdf`，封面标题使用正文 H1。
- 内部 Markdown 构建稿只作为 PDF 渲染输入；如果配置了 log 目录，交付时追加记录。
- PDF 的报告署名来自 `author` 配置；不要把工具作者名当成默认报告署名。
- PDF 最末尾必须追加工具签名：`本报告由 report-helper skill 工具协助生成`、`开源地址：https://github.com/Jiaranbb/report-helper`、`交流和建议可联系作者：嘉然 Jiaran（+v: evadebot）`。
- 交付前验证：中间资料可追溯；PDF 页数和首页排版正常；PDF 文件存在且大小不为 0。
- 常用脚本：`scripts/check_environment.py`、`scripts/append_report_log.py`、`scripts/md_to_pdf.py`、`scripts/render_pdf_with_fallback.py`。具体用法见 `references/delivery.md`。
