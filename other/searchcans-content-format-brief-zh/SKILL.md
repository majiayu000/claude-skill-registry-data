---
name: searchcans-content-format-brief-zh
description: 使用 SearchCans 将地域化 Google 网页、图片、视频和短视频结果映射为有界的内容形式简报。适用于 SEO/GEO 内容规划、编辑形式发现、视觉搜索研究，以及决定哪些形式需要进一步页面级验证。
metadata:
  author: SearchCans
  version: 1.1.0
  tags: [serp-api, google-images-api, google-videos-api, google-short-videos-api, chinese]
---

# SearchCans 内容形式简报

映射一个地域化查询当前返回的网页、图片、视频和短视频页面形式。结果是规划用的形式清单，不是流量预测、排名保证、互动报告或内容复用许可。

## 收集地域化形式清单

确认主题、目标国家/语言、目标受众和规划决策。默认运行请求四个搜索面：Google 网页、图片、视频和短视频。

```bash
python scripts/content_format_brief.py "AI 研究 Agent" \
  --country us --language zh --max-results 10 \
  --out content-format-brief.json
```

需要回答更窄的问题时，重复使用 `--surface` 并选择 `web`、`images`、`videos` 或 `short-videos`。这会明确减少成本和范围。

## 账户感知范围与解释

默认的 `--account-mode auto` 为每个选定形式估算一次 SERP 请求，执行脱敏 Account API 预检，在必要时按固定优先级收缩搜索面，并遵循可用 Parallel Lane。`warn`、`enforce` 和 `off` 可选择不同策略。

使用 [报告模板](references/content-format-report.md) 输出：

1. 查询、市场、已获取形式和限制。
2. 各搜索面已观察到的形式/页面类型模式。
3. 作为后续线索的搜索问题和相关搜索。
4. 一个内容形式假设，以及仍需要的来源/页面验证。

不得仅凭此输出称某形式“热门”“高互动”“最佳表现”或“排名靠前”。Google 结果展示只是一次观察快照。图片和视频 URL 仅供参考，不代表可复用、所有权或授权。

## 官网

[SearchCans 官网](https://www.searchcans.com/)

## 资源

- `scripts/content_format_brief.py`：生成四搜索面的 JSON 清单。
- `references/content-format-report.md`：规划简报结构和边界。
