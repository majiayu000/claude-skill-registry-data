---
name: brand-collateral
description: "制作名片、信纸、包装等品牌物料及展示稿，复用既有品牌。"
license: MIT
metadata:
  source: "dingdong905/design-skills"
  language: "zh-CN"
---

# 品牌物料与展示稿

先确定具体物料、品牌源、准确文案、交付用途与格式。已有 Logo、品牌指南和 Token 是输入，不能在做名片时随机换品牌色或重设计标识。缺少 Logo 时按用户需求另用 `logo-design`，用户接受占位时明确标注。

## 物料简报

按 [规格与交付](references/specifications.md) 区分屏幕预览、可编辑平面稿和生产文件。只制作用户要求的物料，不默认生成整套 50 件 CI。

本地 Python 标准库检索帮助选规格、风格和展示场景，结果是建议；品牌规范、当前供应商规格和用户选择优先：

```powershell
python "<skill-dir>/scripts/search.py" "business card" --domain deliverable --json
python "<skill-dir>/scripts/search.py" "letterhead minimal" --brand "用户品牌" --json
python "<skill-dir>/scripts/search.py" "office reception" --domain mockup --json
```

以真实目录替换 `<skill-dir>`；domain 是 `deliverable`、`style`、`industry`、`mockup`，省略时检索全部候选。中文需求可提炼为英文关键词；偏题则收窄一次。CSV 的尺寸和材质是快照建议，不是印厂规范；颜色/材质也不自动成为已确认事实。

## 制作与展示

准确 Logo、联系方式和版面使用项目已有可编辑工具或原生源完成。摄影式 mockup、纹理和位图展示使用可用 imagegen 的内置工具，参考 Logo 先查看再编辑并保留标识比例；按 [展示稿](references/mockups.md) 区分演示与生产。

需要文档或 PDF 时使用环境已有对应技能；不导入 Gemini 生图或硬编码 HTML 渲染脚本。按 [一致性检查](references/consistency.md) 核对品牌、文本、规格和实际输出，再交付预览、源文件与用途限制。

社交横幅和封面用 `banner-design` 的尺寸与导出流程，相关组合见 [社交素材](references/social-assets.md)。物料扩展不授权发布、下单或发送到外部账户。
