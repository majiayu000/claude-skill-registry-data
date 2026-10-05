---
name: content-flywheel
description: 围绕一个主题一次交付「选题 + 长文 + 社媒切片」三文件，适用于内容营销飞轮与 mkt-content-flywheel 流程模板。用户提到选题规划、长文成稿、社媒切片、内容飞轮时使用。
---

<!-- NOVA-EXEC-BEGIN -->
## Nova Ai-Studio 集成（优先于下文）

- 所有交付物写入 **`<task-artifact-dir>/`**（系统注入 STDA；勿自建 `artifacts/content-flywheel/` 或 `social-matrix/`）。
- **禁止**首 turn `ask_user_question`；从 user goal 推断主题/受众/平台。
- 中文 UI 优先中文主文件名（与主题一致），**须与 write_file 字符串完全一致**；pathHints 保留英文 legacy：
  - `《{主题}》选题规划.md`（alias: `01-topics.md`）
  - `《{主题}》长文成稿.md`（alias: `02-longform.md`）
  - `《{主题}》社媒切片.md`（alias: `03-social-slices.md`）
- en UI 会话可仍用 `01-topics.md` / `02-longform.md` / `03-social-slices.md` 作主名。
<!-- NOVA-EXEC-END -->

# 内容营销飞轮

## 工作流

1. **选题**：1 个主话题 + 3 个子选题 + 各 1 句卖点 → 写入选题文件（见 NOVA-EXEC alias）。
2. **长文**：小标题、要点、结论；可 `web_search` 1–2 次补事实（勿超过 4 次）。
3. **社媒切片**：从长文拆 3–5 条短文/脚本，标注适配平台与配图一句。

## 禁止

- `read_file skills/` 空转
- Task/subagent 委派
- md 未就绪前 generate_image/bash 空转
