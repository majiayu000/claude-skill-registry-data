---
name: model-prompt-audit
description: |
  Audit the global agent configuration (CLAUDE.md / AGENTS.md, rules, settings, behavioral plugins) against the current official prompting guide of the Claude model in use. Fetches the guides live at run time instead of relying on memory, derives how prompting paradigms shifted across model generations, flags anti-patterns, duplicates, stale rules and unused patterns, proposes changes, and applies them only after approval. Use when the user says /model-prompt-audit, 提示词范式审计, 我的 CLAUDE.md 过时了吗, 新模型该怎么改 prompt, 审计全局配置, audit my prompts for the new model, prompt drift.
trigger: /model-prompt-audit
compatibility: Claude Code, Codex
license: MIT
---

# model-prompt-audit

模型换代后，写给上一代模型的规则会变成负担：曾经需要的"多想一步""再检查一遍"在新模型上变成过度验证，为旧缺陷写的禁令在新模型上压住了它本来会做对的事。本 skill 用**当前**官方文档做一次差距审计：范式怎么变了、你的配置里哪些已经反范式、哪些新范式还没用上，然后经你批准再改。

## 铁律

- **文档现取，不用记忆。** 模型指引每次发版都在变，训练记忆里的"最佳实践"很可能就是要被清理的旧范式。所有结论必须能指向本次抓取到的文档段落；抓取失败就停下报告，不用记忆补位。
- **先提案后动手。** 盘点与判定阶段只读；任何文件改动、插件启停、设置修改都在用户批准之后，且改前备份。
- **只判模型行为类指令。** 领域规则（时区、身份、危险操作清单、真实事故教训）不因为写成"禁止"就算反范式；要审的是那些试图矫正模型行为的指令。

## 执行步骤

### 0. 前置检查

1. `python3 --version` 可用；能访问文档站（`curl -sI https://platform.claude.com/llms.txt` 返回 200）。任一失败，报告并停止。
2. 确定当前模型 ID，优先级：用户参数 > 宿主设置文件的 `model` 字段（Claude Code 为 `~/.claude/settings.json`，可带 `[1m]` 后缀）> 会话自述。用会话自述时明确标注"未从设置核实"。

### 1. 抓取当前文档

```bash
SKILL_DIR="$(dirname "$(readlink -f "$0")")"   # 在 SKILL.md 相邻目录取脚本，不假设安装路径
OUT="$(mktemp -d -t model-prompt-audit-XXXXXX)"
python3 "$SKILL_DIR/scripts/fetch_guides.py" --model <model-id> --out "$OUT"
```

脚本从文档站的 `llms.txt` 索引挑出：所有 `prompting-claude-*` 模型指引、跨模型的 best-practices 页、当前模型家族的 what's new 与 migration guide，下载为 Markdown 并写 `index.json`。退出码 1 表示没找到当前模型自己的指引：改用同家族最近的指引并在报告里注明，不要假装它就是当前模型的。

### 2. 建立谱系并通读

1. 读当前模型的指引，找出它对比的上一代（开头通常写 "differences from X"），再读 X 的指引，再往前一代。至少两跳；指引总数不多时全读。
2. 读 best-practices 页里的 "Migration considerations" 与模型专属提示段落。
3. 读 what's new 的 "Behavior differences"；migration guide 只看 "Recommended changes" 与行为变化，API 参数细节与本审计无关。

大文件用分段读取，跳过代码示例块；不要只读目录就下结论。

### 3. 提炼范式变化

按维度整理成表，每行注明来源页面与小节：思考控制与 effort、防偷懒还是防越界、指令风格（枚举 vs 一句意图、正例 vs 禁令）、任务完成与 turn 结束、进度更新、沟通与格式、证据与验证、harness 契约（历史 append-only、turn-scoped 提醒、compaction、子代理）、安全分类器。**只写文档明说的**；你自己的推断标"推测"。

### 4. 盘点用户配置

```bash
python3 "$SKILL_DIR/scripts/inventory.py" [--project <当前项目目录>]
```

输出：全局指令文件（解析软链与 `@` 导入）、规则文件、设置摘要（模型、影响模型的 env、modelSettings、已启用插件；密钥值已打码）、已启用插件中疑似行为准则类的 skill。逐个读取正文。

另外核对 harness 自带了什么：宿主的 system prompt 常已内置指引里的段落（如进度更新要求、交付范围段、自主运行段）。若本轮上下文里能看到与文档相同措辞的段落，视为 harness 已提供，用户配置里的同义条目按"重复"处理。

### 5. 判定

对每条模型行为类指令给一个标签，并引用第 1 步抓到的文档依据：

| 标签 | 含义 |
|---|---|
| 反范式 | 与当前指引相反，例如要求写出推理过程、要求额外自检、反格式化规则、"不确定就停下来问" 与 "把任务做完" 冲突 |
| 过时 | 为旧模型某个缺陷写的补丁，当前指引说该缺陷已不存在或应由 effort/设置控制 |
| 重复 | 同一规则出现在两个以上文件，或 harness 已内置 |
| 模板 | 与用户自己声明的原则冲突的通用模板规则（常见特征：语言风格与其它文件不同、带示例代码、逐条 checklist） |
| 未用上 | 指引推荐、且与用户工作流相关，但配置里没有的做法（如 effort 档位、子代理硬上限、compaction 保留清单、粘贴内容标记、无人值守续做） |
| 保留 | 领域规则、真实事故教训、用户偏好 |

种子清单见 `references/antipattern-seeds.md`，**每条都要用本次文档重新核实**：文档不再这么说的种子直接丢弃。

### 6. 报告并请批准

输出两部分再加提案表：

1. 代际范式变化表（第 3 步）。
2. 差距清单：先反范式与过时，再重复与模板，最后未用上；每项一句现状、一句依据（页面 + 小节）、一句建议动作。
3. 提案表：编号、文件、动作（删除/合并到某文件/改写/新增设置/停用插件）、影响范围。

用宿主的提问机制让用户逐项勾选（Claude Code 用 AskUserQuestion 多选；没有交互能力时列出编号等用户回复）。**未批准前不改任何文件。**

### 7. 执行批准项

1. `BK="$(mktemp -d -t model-prompt-audit-backup-XXXXXX)"`，每个将改动的文件先复制进去，报告里给出该目录。
2. 最小改动：删文件、合并条目、改写段落；设置文件用 JSON 解析后写回，保留其它键；插件用宿主 CLI 停用或卸载。
3. 验证：JSON 能解析；改到的脚本 `python3 -m py_compile`；被改 skill 有测试就跑；再跑一次 `inventory.py` 确认文件与体积变化符合提案。
4. 结尾列出改动文件的绝对路径与备份目录。

### 8. 沉淀

建议用户把本次文档 URL 清单和审计日期记到其记忆或笔记系统，下次换模型时直接重跑本 skill。不把用户的个人配置内容写进本 skill。

## 错误处理

- 文档站不可达或索引里没有 prompting 指引：停止，说明无法在无文档情况下审计。
- 用户配置文件是软链或 `@` 导入：改原始文件，不改链接。
- 配置里有本 skill 无法判定的自定义 hook/脚本：列为"需人工判断"，不猜。
