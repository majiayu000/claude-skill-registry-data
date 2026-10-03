---
name: 竞品监控 Skill
description: 用少量竞品网址和关注字段，生成适合人工复核的竞品变化汇总。首版默认复用 changedetection.io 做上游监控底座。
---

# 竞品监控 Skill

## 适用场景

- 想持续跟踪几个重点竞品官网
- 想重点看价格、上新、促销、页面结构变化
- 想把零散页面变动变成可讨论的业务摘要

## 最小输入

- 竞品名称
- 监控网址
- 页面名称 / 页面类型
- 监控目的
- 关注字段
- 检查频率

参考：

- `examples/minimal-monitoring-input.json`

## 核心输出

- 变化摘要 Markdown
- 结构化变化结果 JSON
- 人工复核建议

参考：

- `examples/minimal-monitoring-output.md`
- `examples/changedetection-watch-seed.json`

## 默认工作流

1. 用 `changedetection.io` 建立少量监控项。
2. 先锁定 3 个真实公开页面：产品详情页、新品集合页、首页促销区。
3. 只对高价值页面做字段级关注，不追求全站覆盖。
4. 拉取当日变动结果，或先用最小模拟变化输入跑通摘要脚本。
5. 生成面向人工复核的变化摘要。
6. 标注哪些变化值得业务跟进，哪些只是噪音。
7. 真实 watch 稳定后，再补字段级选择器。

## 文档流转规则

- 运行脚本、样例输入输出、watch seed 等执行层内容留在当前仓库
- 长期判断与人类阅读说明沉淀到 `工作间/`
- 会被课程、品牌、产品表达反复引用的说明，应在 Obsidian `工具工作间/02_场景拆解/外贸业务主干Skill` 有对应展现

## 核心规则

- 只基于公开网页变化，不伪造价格和页面含义。
- 无法确认时写成推断，不写成确定事实。
- 首版只做 3 个真实页面、少量字段，不扩成多站点系统。
- 重点是让业务更快判断，不是追求全自动监控系统。

## 当前首版页面

- 产品详情页：`https://www.allbirds.com/products/mens-tree-runners`
- 新品集合页：`https://www.allbirds.com/collections/mens-new-arrivals`
- 首页促销区：`https://www.allbirds.com/`

## 当前脚本入口

```bash
python3 '工作间/孵化中/竞品监控skill/scripts/build_change_summary.py' \
  --input-json '工作间/孵化中/竞品监控skill/examples/sample-change-events.json' \
  --markdown-out '工作间/孵化中/竞品监控skill/examples/minimal-monitoring-output.md' \
  --json-out '工作间/孵化中/竞品监控skill/examples/minimal-monitoring-output.json'
```

```bash
python3 '工作间/孵化中/竞品监控skill/scripts/build_watch_seed.py' \
  --input-json '工作间/孵化中/竞品监控skill/examples/minimal-monitoring-input.json' \
  --json-out '工作间/孵化中/竞品监控skill/examples/changedetection-watch-seed.json'
```

## 风险与边界

- 页面结构改动可能导致选择器失效。
- 价格和库存变化可能需要人工二次确认。
- 某些 JS 页面或登录态页面需要更复杂抓取能力，首版默认不覆盖。

## 推荐阅读

- `立项方案.md`
- `references/首版接入方案.md`
- `references/changedetection-watch-落地口径.md`
