---
name: banner-design
description: "制作横幅、封面与社交图片，结合 imagegen 素材、可编辑排版及导出检查。"
license: MIT
metadata:
  source: "dingdong905/design-skills"
  language: "zh-CN"
---

# 横幅、封面与社交素材

明确用途、平台或自定义尺寸、准确文案、品牌素材和交付格式。已提供的信息不重复询问；缺少影响交付的尺寸或内容时再问。选项数量按用户要求和任务规模决定，不默认生成三套付费素材或强制调研 Pinterest。

## 设计与素材

从 [尺寸与风格参考](references/sizes-and-styles.md) 选画布，检查平台当前规格及头像/裁切/UI 遮挡。已有 `brand` 或 Token 可直接使用；纯排版不必同时加载 UI 检索和品牌全套资料。

用户需要照片、插画、纹理或位图编辑时读取可用的 `imagegen` 技能，使用内置 image_gen 工具。新图描述题材、风格、构图、留白及约束；修改现有图先查看目标图，保持明确的不变项。透明素材明确请求透明背景。工具不需要用户提供 API Key；工具不可用时说明缺口，只有用户选择 CLI/API 方案后才走其回退流程。

imagegen 的结果不保证广告位的精确像素尺寸。需要准确文案、Logo 和多尺寸版本时，优先把素材放入 HTML/CSS 或项目已有可编辑设计源，再导出。文字、商标与品牌资产使用用户提供或授权的版本；生成素材若自带文案须逐字检查。

素材提示与合成见 [生图与构图](references/imagegen-composition.md)。精确排版优先沿用项目字体和颜色，设计内容的来源不能改变用户要求。

## 导出与交付

按 [导出验证](references/export.md) 在目标画布尺寸导出 PNG。浏览器操作读取环境已有 browser-act/computer-use 的工具文档；精确导出可使用项目已有截图能力。实际工具不支持目标尺寸或导出时说明限制，不能把普通视口截图当精确交付。

导出后查看最终图片，并运行只读的标准库检查：

```powershell
python "<skill-dir>/scripts/check_export.py" "<banner.png>" --width 1500 --height 500 --max-bytes 5000000
```

将 `<skill-dir>` 替换为真实技能目录。检查覆盖 PNG 容器、物理像素与文件大小，不证明文案、裁切、色彩或视觉质量。2x 导出按实际像素核对，例如 1500×500 的逻辑画布对应 3000×1000 文件，交付明确写出两者。

交付最终图片预览、准确尺寸、文件路径和必要的可编辑源。项目使用的生成素材复制到项目资产目录，沿用已有命名约定；没有约定时可用 `assets/banners/<campaign>/<variant>-<width>x<height>.png`。迭代先修改用户指出的部分；PNG 通过不代表印刷生产文件已就绪。
