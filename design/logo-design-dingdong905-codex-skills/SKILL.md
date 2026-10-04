---
name: logo-design
description: "设计与评审 Logo，提供本地风格检索和位图/矢量交付。"
license: MIT
metadata:
  source: "dingdong905/design-skills"
  language: "zh-CN"
---

# Logo 设计与评审

明确品牌名称及准确写法、用途、已有标识、视觉约束与交付格式。Logo 请求不自动重做品牌战略；已有品牌资料先读相关部分。缺少会影响方案的关键输入时询问，其余用标注为建议的设计简报推进。

## 简报与检索

根据 [简报与风格判断](references/brief-and-style.md) 确定标识类型、识别重点及真实使用场景。本地 Python 标准库检索可辅助选择，数据是上游设计建议，不是用户研究或行业定律。以真实路径替换 `<skill-dir>`：

```powershell
python "<skill-dir>/scripts/search.py" "minimalist geometric" --domain style --json
python "<skill-dir>/scripts/search.py" "technology modern" --brand "用户品牌" --json
```

domain 为 `style`、`color`、`industry`；不指定时检索各域形成候选简报，不自动采用每个域的第一条。中文需求提炼为少量英文关键词；偏题时限定域重试一次。颜色心理与行业符号仅作启发，现有品牌规范优先。不要整批读取 CSV。

## 设计与交付

照片式展示、位图概念、纹理或现有位图修改使用可用 `imagegen` 技能的内置工具；不需要用户提供 API Key。准确字标、既有矢量修改及用户要求的可编辑 SVG 在原生设计源中完成，不能把 PNG 包进 SVG 就声称获得矢量。

生图与原生设计路径见 [生成与格式](references/generation-and-formats.md)。保留用户提供的 Logo 特征和准确品牌文字；背景按用途选择，需要透明时明确请求真实透明背景，不强制白底。不要每次默认生成多个收费变体。

按 [评审与交付](references/review-and-delivery.md) 检查小尺寸、单色、不同背景、文字与轮廓。交付所要求的文件、预览、格式及已验证/未验证项；概念图不表示已经完成商标检索或生产矢量定稿。

品牌事实和规范用 `brand`，物料应用用 `brand-collateral`。现有界面图标集的扩展遵循项目图标库，参见 [图标与标识边界](references/icons-and-marks.md)，不把普通 UI 图标任务自动变成 Logo 项目。
