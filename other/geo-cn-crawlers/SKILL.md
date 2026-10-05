---
name: geo-cn-crawlers
description: 当用户要检查国内 AI 爬虫可达性、robots.txt、llms.txt、字节/百度/阿里等 bot 规则，或做 GEO 技术基线时使用。
---

# 国内 AI Crawler 与技术可达

面向 **geo_technical**：确保站点对国内主流 AI 爬虫友好。

## 检查项

1. **robots.txt**：Allow/Disallow 对 GPTBot、Bytespider、Baiduspider、通义等
2. **llms.txt**：站点根路径是否存在、是否列出可引用路径
3. **国内 bot 清单**：见 [references/cn-crawlers.md](references/cn-crawlers.md)
4. **页面 meta**：noindex、canonical、hreflang

## 交付

- `aeo-audit.md`：发现与 P0/P1 修复
- `aeo-audit.html`：**与 MD 同步**（`read_skill geo-dual-report`）
- `llms.txt`：建议版（若缺失）
- 可选 `schema.jsonld` 摘要

写入系统分配任务目录。
