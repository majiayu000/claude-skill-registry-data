---
name: pdlc-settings
description: 交互式配置 PDLC（当前：状态栏 statusline 的启用/停用/展示项）
argument-hint: [statusline | status]
allowed-tools: Read, Edit, Write, Bash, Glob
layer: 3
stage: ops
produces: []
requires: []
next_step: null
terminal_state: null
---

# PDLC 交互式设置

以**交互菜单**方式配置 PDLC，让用户少敲命令行。**当前只含「状态栏（statusline）」一节**——
把 PDLC 运行状态（当前功能 / 阶段 / 下一步 / 检查 / blocked）显示到 Claude Code 底部状态栏。
未来若有更多设置**可能**并入本命令（非本版承诺）。

> ⚠️ **安全底线**：本命令会读写用户全局 `~/.claude/settings.json`（高影响）。**任何写入前必须**：
> 先备份 → 展示 diff → 用户确认。**写全局配置可能被 Claude Code 安全层拦截**——届时**不谎报成功**，
> 优雅降级为「已算好这一行，请你确认后手动粘贴」。重复运行幂等，绝不覆盖用户其它配置。

## 交互入口

根据本命令的参数分派；参数为空则显示主菜单：

```
⚙️ PDLC 设置

  1) 状态栏 · 启用      在状态栏独占一行显示 PDLC 状态
  2) 状态栏 · 停用      从状态栏移除本段（不动你其它配置）
  3) 状态栏 · 展示项    勾选显示哪些内容（进度条/检查/停留时长…）
  4) 状态栏 · 状态      查看当前是否已接线 + 生效配置 + 预览

  请选择（1-4）：
```

- 参数含 `status` → 直接走「状态栏 · 状态」
- 参数含 `statusline` → 进入状态栏子菜单
- 否则显示上面主菜单，等用户选

## 定位脚本（稳定源优先）

接线依赖状态栏脚本 `bin/pdlc-statusline.sh`。按以下顺序找**第一个存在**的副本作为符号链接源，
**优先稳定源**（升级不改路径）：

1. `~/.claude/plugins/marketplaces/pdlc-skills/bin/pdlc-statusline.sh` （marketplace 克隆，最稳）
2. `${CLAUDE_PLUGIN_ROOT}/bin/pdlc-statusline.sh` （当前插件根，若该环境变量存在）
3. 最新版本缓存：`ls -d ~/.claude/plugins/cache/pdlc-skills/pdlc/*/bin/pdlc-statusline.sh | sort -V | tail -1`（按版本号取最大，不按修改时间：升级时旧版本目录的修改时间可能反而更新）

用 Bash 依次探测，记下命中的路径记为 `$SL`。都找不到 → 提示用户先 `claude plugin install pdlc@pdlc-skills` 再来。

## 动作一：状态栏 · 启用

1. **建稳定链接**：`bash "$SL" --install`
   - 它在固定路径 `~/.claude/pdlc-statusline` 建符号链接指向 `$SL`（升级后重跑本命令即重指，用户侧命令不变）。
2. **读现有状态栏命令**：读 `~/.claude/settings.json`（不存在则视为 `{}`）。取 `.statusLine.command`（可能为空）。
3. **幂等计算新命令**：
   - 若现有命令已包含 `pdlc-statusline`（任意形式）→ 告知「已接线，无需重复」，转去「展示项」或结束。
   - 否则新命令 = `<现有命令>; ~/.claude/pdlc-statusline`（现有为空则新命令就是 `~/.claude/pdlc-statusline`）。
   - 若 `.statusLine` 不存在，需同时补 `"statusLine": { "type": "command", "command": "<新命令>" }`。
4. **备份 + 展示 diff**：把 `~/.claude/settings.json` 复制为 `~/.claude/settings.json.pdlc-bak`（已存在则加时间戳后缀）。
   向用户展示将要变更的**那一行** diff（旧 command → 新 command）。
5. **确认后写入**：用户确认 → 用 Edit/Write 写回 `settings.json`（保持其余字段与格式不变）。
6. **写入被拦截 / 失败时优雅降级**（关键）：
   - **不谎报已启用**。明确告知：「写全局 settings.json 被安全层拦截。已备份到 `<bak>`。
     请把 `~/.claude/settings.json` 的 `statusLine.command` 手动改为：」，并给出**完整新命令原文**一行，供用户复制粘贴。
7. **预览**：调用一次脚本渲染当前项目状态给用户看：
   `printf '{"workspace":{"current_dir":"%s"}}' "$PWD" | bash "$SL"`
   （当前项目非 PDLC / 无状态文件则为空，属正常。）
8. 提示：状态栏是**每个终端会话/刷新**生效，可能需重开会话或等下次刷新。

## 动作二：状态栏 · 停用

1. 读 `.statusLine.command`。若不含 `pdlc-statusline` → 告知「未接线，无需停用」。
2. **只摘自己那段**：从命令串里去掉 `; ~/.claude/pdlc-statusline`（及等价的仅本段情形；若本段是唯一内容则清空 command 或移除 statusLine——按用户意愿）。**绝不动**用户其它命令片段。
3. 备份 → 展示 diff → 确认 → 写入；**被拦截同样降级**为「请手动改回：`<旧命令去掉本段后的值>`」。
4.（可选）询问是否一并 `bash "$SL" --uninstall` 移除稳定链接。

## 动作三：状态栏 · 展示项

交互勾选，写入配置文件（**不碰 settings.json**，无 gate 风险）：

1. 逐项询问（回车用默认）：

   | 项 | 键 | 默认 |
   |---|---|---|
   | 迷你进度条 | `show_progress_bar` | on |
   | 下一步 | `show_next` | on |
   | 运行态图标 | `show_run_icon` | on |
   | 检查结果（auto=仅 autonomous 显） | `show_checks` | auto |
   | 停留时长（auto=blocked/autonomous 显） | `show_elapsed` | auto |
   | 显示完整 ID（否则仅功能名） | `show_full_id` | off |
   | 多 feature 选谁（auto/latest/具体 ID） | `pick_feature` | auto |
   | 颜色 | `color` | on |

2. 询问写全局还是项目级：
   - 全局：`~/.claude/pdlc-statusline.json`
   - 项目级（覆盖全局）：`<当前项目>/docs/.pdlc-state/statusline.json`
3. 用 Write 写入选定 JSON（参考 `references/templates/pdlc-statusline.example.json` 的键）。这两个文件不受安全层 gate（非 settings.json）。
4. **当场预览**：同上用脚本渲染一行给用户确认效果。

## 动作四：状态栏 · 状态

只读、不改任何东西：

1. 是否已接线：读 `.statusLine.command`，报告是否含 `pdlc-statusline`。
2. 稳定链接：`~/.claude/pdlc-statusline` 是否存在、指向哪。
3. 生效配置：合并 `~/.claude/pdlc-statusline.json` 与项目级 `docs/.pdlc-state/statusline.json`（后者覆盖），列出各项当前值（缺省即默认）。
4. 预览：渲染当前项目一行。

## 要求

<!-- @include templates/prompts/output-language.md（已内联于下方，无需另读） -->
🌐 **Output language for generated artifacts**

All generated artifacts (PRDs, design docs, code comments, review reports,
test plans, deployment manuals, changelog entries, etc.) follow this policy:

1. **Default — match the conversation language exactly**:
   - 用户用中文与 Claude 对话 → 产中文文档、中文代码注释、中文报告
   - User talks to Claude in English → produce English artifacts
   - User talks in another language → produce artifacts in that language
   - **Never silently default to a fixed language regardless of the user's input.**

2. **Explicit override always wins**: when the user specifies a language for
   an artifact (e.g. "write the PRD in English", "用英文写 API 设计文档",
   "output the deploy doc in Japanese"), use that language for that artifact,
   regardless of conversation language.

3. **Mixed-language requirements**: if the user wants some artifacts in one
   language and others in a different language (common: Chinese PRD + English
   API docs for partners), honour each per-artifact instruction.

4. **Uncertain**: if you cannot reliably detect the conversation language,
   ask once before producing the first artifact.

This policy applies to **content** (prose, comments, headings). It does
**not** override technical conventions like English variable names, English
git commit subjects, or English error codes when the project's conventions
require them.
<!-- @include-end templates/prompts/output-language.md -->
- **只读脚本、不改状态机**：本命令不读写 `docs/.pdlc-state/<id>.json` 的业务字段，只读它们用于预览。
- 写 `settings.json` **必须**备份 + diff + 确认；被 gate 时降级为「算好 + 用户粘贴」，**严禁**假装已写成功。
- 幂等：重复启用不叠加；停用只摘本段。
- 不安装依赖、不联网。jq 缺失时预览可能为空——如实告知，不阻断配置。

参数：$ARGUMENTS
