---
name: scammer
description: 骗子.skill — 把骗局套路蒸馏成 AI，检测可疑消息，定位当前阶段，预判下一步。Distill scam patterns into AI, detect suspicious messages, locate current phase, predict next move.
argument-hint: [suspicious-message-or-command]
version: 1.0.0
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **Language / 语言**: 根据用户第一条消息的语言，全程使用同一语言回复。
> Detect the user's language from their first message and respond in the same language throughout.

# 骗子.skill（Claude Code 版）

## 触发条件

以下情况启动**检测模式**：

- `/detect-scam`
- `/scammer [消息内容]`
- "帮我看看这条消息"
- "这是诈骗吗"
- "判断一下这个"
- 用户直接粘贴一段可疑消息或截图

以下情况启动**添加模式**：

- `/add-scam`
- "我想添加一个骗局"
- "记录一下这种骗法"
- `/update-scam {slug}`

以下情况启动**管理命令**：

- `/list-scams`：列出所有骗局库
- `/scam-stats`：统计信息
- `/scam-rollback {slug} {version}`：回滚版本
- `/scam-versions {slug}`：列出历史存档
- `/delete-scam {slug}`：删除本地骗局库（需用户明确确认）

---

## 工具使用规则

| 任务 | 使用工具 |
|---|---|
| 读取截图/图片 | `Read` 工具（原生支持图片） |
| 读取 PDF / TXT / MD | `Read` 工具 |
| 写入/更新骗局库文件 | `Write` / `Edit` 工具 |
| 列出骗局库 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/pattern_writer.py --action list` |
| 版本管理（存档 / 递增 / 回滚 / 列表） | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |
| 删除骗局库（慎用） | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/pattern_writer.py --action delete --slug {slug} --force --base-dir ./scams` |

**基础目录**：骗局库写入 `./scams/{slug}/`（相对于本项目目录）。

---

## 主流程 A：检测可疑消息

### Step 1：接收输入

接受以下任意形式的输入：

- 直接粘贴的文字消息
- 截图（用 `Read` 工具读取图片内容）
- 用户对话的描述（"他说他是xxx，要我做xxx"）
- 多条消息的对话记录

如果用户没有提供消息，引导输入：

```
请提供可疑消息，可以：
  [A] 直接粘贴文字
  [B] 上传截图
  [C] 描述对方说了什么
```

### Step 2：加载骗局库

用 `Read` 工具读取 `${CLAUDE_SKILL_DIR}/scams/` 目录下所有骗局的 `tactic.md`，以及用户本地添加的骗局库。

参考 `${CLAUDE_SKILL_DIR}/prompts/detection.md` 中的匹配逻辑；若某骗局目录下有 `Correction 记录`，优先采纳其中的例外说明。

### Step 3：分析输出

输出格式严格按照以下结构：

```
【{骗局类型}】第 {N} 阶段：{阶段名称}

├ 套路识别：{触发此判断的3个关键信号}
├ 已过阶段：{阶段1} → {阶段2} → {当前阶段}
├ 下一步预判：{骗子接下来大概率会说什么/做什么}
├ 心理钩子：{本阶段利用的心理弱点}
└ 建议：{具体行动建议，1-2句话}
```

**置信度处理**：
- 高置信度（>85%）：直接输出结论
- 中置信度（60-85%）：输出结论，附注"也可能是：{备选类型}"
- 低置信度（<60%）：列出2-3种可能，说明各自的判断依据
- 无法判断：说明缺少什么信息，询问用户补充

**无骗局判断**：如确认不是诈骗，直接说"未检测到常见诈骗特征"，说明原因，不要过度警惕。

---

## 主流程 B：添加新骗局样本

### Step 1：基础信息录入（3个问题）

参考 `${CLAUDE_SKILL_DIR}/prompts/intake.md`：

1. **骗局类型名称**（如：冒充公检法、杀猪盘）
2. **核心特征**（一句话：目标群体、主要套路、最终目的）
   - 示例：`专门针对老年人，假冒医保局，诱导购买保健品`
3. **样本来源**（亲身遭遇 / 朋友转发 / 新闻案例 / 反诈平台）

### Step 2：原材料导入

```
样本怎么提供？

  [A] 直接粘贴聊天记录
  [B] 上传截图
  [C] 描述骗局流程
  [D] 提供案例链接或新闻报道
```

### Step 3：提取套路

参考 `${CLAUDE_SKILL_DIR}/prompts/pattern_analyzer.md` 提取：

**线路 A（套路图谱）**：
- 完整阶段划分（从接触到得手）
- 每阶段的触发词/信号
- 每阶段的目标和话术模板
- 退出信号（目标不上钩时的转变）

**线路 B（话术库）**：
- 高频词汇和短语
- 心理钩子类型（恐惧/贪婪/权威/情感/紧迫感/从众）
- 信任建立手法
- 常见伪装身份

### Step 4：预览确认

向用户展示摘要（各5-8行），询问确认：

```
套路图谱摘要：
  - 骗局类型：{xxx}
  - 阶段数：{N} 个阶段
  - 核心套路：{xxx}
  ...

话术库摘要：
  - 核心心理钩子：{xxx}
  - 高频词汇：{xxx}
  ...

确认添加？还是需要调整？
```

### Step 5：写入骗局库

用户确认后：

**1. 创建目录**（Bash）：
```bash
mkdir -p scams/{slug}/versions
```

**2. 写入 tactic.md**（Write 工具）：
路径：`scams/{slug}/tactic.md`

参考 `${CLAUDE_SKILL_DIR}/prompts/tactic_builder.md` 生成内容。

**3. 写入 scripts.md**（Write 工具）：
路径：`scams/{slug}/scripts.md`

**4. 写入 meta.json**（Write 工具）：
路径：`scams/{slug}/meta.json`

```json
{
  "name": "{骗局名称}",
  "slug": "{slug}",
  "created_at": "{ISO时间}",
  "updated_at": "{ISO时间}",
  "version": "v1",
  "profile": {
    "target": "{目标群体}",
    "platform": "{主要平台}",
    "goal": "{最终目的}"
  },
  "tags": {
    "psychology": ["恐惧", "贪婪"],
    "method": ["冒充身份", "情感操控"]
  },
  "stages_count": {N},
  "sample_sources": ["..."],
  "corrections_count": 0
}
```

告知用户：
```
✅ 骗局样本已添加！

文件位置：scams/{slug}/
已加入检测库，下次 /detect-scam 时自动使用。

如果有新样本，随时 /add-scam 追加。
```

---

## 进化模式：追加样本

用户提供新样本时：

1. 读取新内容
2. `Read` 读取现有 `scams/{slug}/tactic.md` 和 `scripts.md`
3. 参考 `${CLAUDE_SKILL_DIR}/prompts/merger.md` 分析增量
4. 存档当前快照（**不**改变 `meta.json` 中的版本号）：
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action backup --slug {slug} --base-dir ./scams
   ```
5. `Edit` 追加增量内容
6. 更新 `meta.json` 中的 `updated_at`、`stages_count` 等字段（如有变化）
7. 合并内容确认无误后，**再**递增版本号：
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action bump --slug {slug} --base-dir ./scams
   ```

## 进化模式：用户纠正

用户表达"判断错了"/"这不是诈骗"/"这是另一种骗法"时，按 `${CLAUDE_SKILL_DIR}/prompts/correction_handler.md` 处理：

1. 询问正确类型或正确判断
2. 生成 correction 记录
3. `Edit` 追加到对应文件的 `## Correction 记录` 节
4. 如果是全新骗局，引导进入添加模式

---

## 管理命令

`/list-scams`：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/pattern_writer.py --action list --base-dir ./scams
```

`/scam-stats`：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/pattern_writer.py --action stats --base-dir ./scams
```

`/scam-rollback {slug} {version}`：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action rollback --slug {slug} --version {version} --base-dir ./scams
```

`/scam-versions {slug}`（列出可回滚的快照目录名）：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action list --slug {slug} --base-dir ./scams
```

`/delete-scam {slug}`（删除本地骗局目录，**不可恢复**；需用户明确确认后再执行）：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/pattern_writer.py --action delete --slug {slug} --force --base-dir ./scams
```
