---
name: ui-ux-pro-max
description: "检索本地 UI/UX 设计资料，辅助界面配色、字体、布局、交互、可访问性和技术栈选择。用于设计、实现或审查 Web、移动及桌面界面；纯后端任务不使用。"
metadata:
  source: "dingdong905/design-skills"
  language: "zh-CN"
---

# UI/UX 设计检索

这是本地设计建议检索器，使用 Python 标准库，无联网、API Key 或第三方包要求。检索结果是建议，不是经过用户研究验证的结论，也不能覆盖项目品牌、用户要求或既有组件库。

## 工作方式

先确定产品、任务范围、目标平台和已有技术栈。局部组件修复只查相关问题；新页面才需要综合设计建议。保留项目现有栈，不因示例而改用某个框架、字体或图标库。

以本技能真实目录替换 `<skill-dir>`；Windows 用 `python`，其他平台按可用运行时执行。不要依赖当前工作目录来定位脚本。

```powershell
python "<skill-dir>/scripts/search.py" "keyboard focus modal" --domain ux
python "<skill-dir>/scripts/search.py" "internal analytics dashboard" --design-system -p "Ops Console" -f markdown
python "<skill-dir>/scripts/search.py" "virtualized list" --stack react-native
```

优先使用一个主意图和 2–5 个英文关键词。中文需求先提炼为英文设计词。结果为空或偏题时，限定 domain/stack 后重试一次；仍无匹配就说明缺口，使用标明为一般建议的方案。检查结果的身份、平台、版本和适用范围，不能把匹配分数当作事实可信度。版本相关指导需要与项目实际版本核对，必要时查官方文档。

常用 domain：`product`、`style`、`color`、`typography`、`landing`、`ux`、`chart`、`icons`、`google-fonts`、`gsap`、`react`、`web`。`web` 数据实际偏向原生 App 接口，浏览器键盘/ARIA 问题优先查 `ux`。技术栈名称以 `search.py --help` 为准；本快照缺少 SwiftUI 数据，不能声称支持其专用检索。

## 持久化与交付

仅在任务需要保存设计系统时使用 `--persist`，明确项目根目录；先检查已有 MASTER/page 文件，再使用默认不覆盖的行为。

```powershell
python "<skill-dir>/scripts/search.py" "internal analytics dashboard" --design-system --persist -p "Ops Console" --output-dir "<project-root>"
```

只把非敏感设计关键词送入检索。项目生成的 `design-system/<project-slug>/MASTER.md` 是设计建议文件，与本技能旁的 `design-system` 技能目录无关；修改任务页时先读 MASTER，再读对应 page override。

交付应说明采用的设计判断及验证结果。按目标平台检查文字和控件对比、键盘/读屏、目标尺寸、缩放、响应式、暗色模式和减少动效；Web CSS px、iOS pt、Android dp 分别处理。数据目录只用于脚本检索，不要整批加载。

需要细则时查 [UI 规则参考](references/ui-guidance.md) 的相关章节，跳过无关原生 App 条款。需要品牌事实用 `brand`；需要 JSON Token/CSS 变量与组件状态用 `design-system`。网站发布、Figma 写入和 PPTX 制作由对应已有工具处理，本技能只提供设计输入。
