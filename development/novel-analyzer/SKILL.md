---
name: novel-analyzer
description: 四阶段小说精读分析工作流。用于深度分析长篇小说的情节、人物、文风和主题。触发条件：用户请求分析/精读/深度解读小说文本，或需要生成文学分析报告、人物弧光追踪、文风研究、角色档案。执行流程：粗读提取元数据 → 并行精读分块（自动计算分块数和边界）→ 整合生成中文深度报告 → (可选)生成角色档案。输出包含情节梳理、人物列传、文体分析、修辞手法、黄金语录、角色心理侧写。适用于中长篇小说（5k行以上）。
---

# 小说深度分析工作流

你是小说分析工作流编排器。收到小说文件路径后，执行多阶段分析流程，最终生成专业的文学批评报告，并可选择性生成单个角色的深度档案。

## 工作流程概览

```
阶段1: 粗读 (你自己执行)
  ↓ 生成 metadata.json
阶段2: 精读 (并行 general-purpose agents)
  ↓ 生成 chunk_01.json, chunk_02.json, ...
阶段3: 整合 (1个 general-purpose agent)
  ↓ 生成 report.md
阶段4: 角色档案生成 (可选, 1个 general-purpose agent)
  ↓ 生成 characters/profile_<角色名>.md
```

---

## 阶段 1: 粗读元数据提取

**执行者**: 你自己（不启动 agent）

### 1.1 前置准备

```bash
# 1. 统计总行数
wc -l <文件路径>

# 2. 创建输出目录（使用绝对路径）
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="/tmp/novel_analysis/<书名>_${TIMESTAMP}"
mkdir -p "${OUTPUT_DIR}/chunks"
```

### 1.2 读取文件样本

由于文件可能很大，分段读取：
- 开头: `offset=0, limit=2000`
- 中间: `offset=<total_lines/2>, limit=2000`
- 结尾: `offset=<total_lines-2000>, limit=2001`

### 1.3 生成元数据

根据提示词模板 `prompts/skim.md` 的要求，生成 JSON 并保存到：

```
${OUTPUT_DIR}/metadata.json
```

**元数据结构**:
```json
{
  "metadata": {
    "title": "书名",
    "author": "作者",
    "genre": "具体类型",
    "tone": "基调关键词",
    "total_lines": 9301,
    "total_estimated_tokens": 173500
  },
  "main_characters": ["角色1 (身份)", "角色2 (身份)"],
  "chunking_guide": {
    "chapter_pattern": "^第\\d+章",
    "average_chapter_length": "约120行"
  },
  "world_setting": "世界观概述（两句话）"
}
```

**估算公式**:
- 中文: `total_tokens = total_chars / 1.35`
- 英文: `total_tokens = total_words * 1.3`

完整提示词要求见: `prompts/skim.md`

---

## 阶段 2: 并行精读分块

**执行者**: 多个并行的 `general-purpose` agents

### 2.1 计算分块参数

```python
target_tokens_per_chunk = 50000  # 配置值
overlap_lines = 200              # 配置值

# 计算分块数
num_chunks = ceil(total_estimated_tokens / target_tokens_per_chunk)

# 每块基准行数
chunk_size = total_lines / num_chunks

# 为每个 chunk 计算边界
for chunk_id in range(1, num_chunks + 1):
    target_start = (chunk_id - 1) * chunk_size
    target_end = chunk_id * chunk_size

    # 上下文（前一块的结尾 200 行，仅用于连续性检查）
    if chunk_id > 1:
        context_start = target_start - overlap_lines
        context_end = target_start
    else:
        context_start = None  # 第一块无需上下文
```

### 2.2 启动并行 agents

**关键**: 在**单个消息**中启动多个后台 Task，实现真正并行：

```python
# 在一个 response 中发送多个 Task tool calls
Task(subagent_type="general-purpose", run_in_background=True, ...)  # chunk 1
Task(subagent_type="general-purpose", run_in_background=True, ...)  # chunk 2
Task(subagent_type="general-purpose", run_in_background=True, ...)  # chunk 3
# ...
```

### 2.3 Agent Prompt 模板

从 `prompts/chunk.md` 读取完整模板，注入以下变量：

**必需变量**:
- `{{book_title}}` - 从 metadata.json
- `{{book_genre}}` - 从 metadata.json
- `{{main_characters}}` - 从 metadata.json (转为字符串)
- `{{world_setting}}` - 从 metadata.json
- `{{chunk_id}}` - 当前块编号
- `{{total_chunks}}` - 总块数
- `{{file_path}}` - 原始文件路径（绝对路径）
- `{{output_dir}}` - 输出目录（绝对路径）
- `{{context_offset}}` / `{{context_limit}}` - 上下文范围（chunk 1 则省略）
- `{{target_offset}}` / `{{target_limit}}` - 目标分析范围

### 2.4 角色追踪模式（可选）

**触发条件**: 用户在分析请求中明确提到要生成特定角色档案

如果用户提出"分析小说，并生成XX角色档案"，则在每个 chunk agent 的 prompt 末尾追加：

```
### SPECIAL INSTRUCTION: Character Tracking

The user wants a detailed profile for character: {{target_character}}

**If this character appears in your chunk:**
- Pay extra attention to ALL information about them
- Record detailed appearance descriptions
- Capture ALL their dialogue (verbatim)
- Note their actions, emotions, and interactions
- Track their relationships with other characters
- Document any character development or status changes

**In the JSON output:**
- Ensure {{target_character}} is in the `characters` list with rich details
- Include them in relevant `plot_events`
- Add their quotes to `key_passages` with context
- Note any psychological changes in `status_update`

**If this character does NOT appear in your chunk:**
- Proceed with normal analysis
- No need to mention them
```

**重要**: 这个追加指令必须在每个 chunk agent 启动时都添加，因为无法预知角色会在哪些 chunk 中出现。

**Prompt 结构示例**:

```
You are an expert Literary Stylist and Data Analyst.

**Global Context:**
- Book: {{book_title}}
- Genre: {{book_genre}}
- Key Characters: {{main_characters}}
- World Setting: {{world_setting}}

You are reading **Chunk #{{chunk_id}} of {{total_chunks}}**.

### INPUT

Read file: `{{file_path}}`
- Context (for continuity): offset={{context_offset}}, limit={{context_limit}}
- **Target to analyze**: offset={{target_offset}}, limit={{target_limit}}

[剩余部分见 prompts/chunk.md]

### SPECIAL INSTRUCTION: Character Tracking (如果启用)
The user wants a detailed profile for character: {{target_character}}
[如果用户请求了角色档案，追加2.4中的角色追踪指令]
```

### 2.5 等待并监控

```python
# 使用 AgentOutputTool 等待所有 agents 完成
AgentOutputTool(agentId=agent1_id, block=True)
AgentOutputTool(agentId=agent2_id, block=True)
# ...
```

**预期输出**: `${OUTPUT_DIR}/chunks/chunk_01.json`, `chunk_02.json`, ...

---

## 阶段 3: 整合生成报告

**执行者**: 1 个同步的 `general-purpose` agent

### 3.1 启动整合 agent

```python
Task(
  subagent_type="general-purpose",
  run_in_background=False,  # 同步等待结果
  description="整合小说分析报告",
  prompt=f"""
You are the Chief Literary Critic combining parallel reading reports.

### Input Files

1. Read metadata: `{output_dir}/metadata.json`
2. Use Glob to find all chunks: `{output_dir}/chunks/*.json`
3. Read all chunk JSONs (可并行读取)

### Your Task

Compile a comprehensive Markdown report in **CHINESE**.

完整要求见提示词模板，但核心结构如下：

# 深度阅读报告: {{{{book_title}}}}

## 1. 核心评价
**【题材与标签】**: ...
**【一句话点评】**: ...
**【整体评分】**: ...

## 2. 文体学分析
### 2.1 语言风格与基调
### 2.2 典型修辞手法

## 3. 情节脉络
[按阶段划分情节发展]

## 4. 人物列传
[主要角色的完整弧光]

## 5. 黄金语录画廊
### 🖋️ 景物与意境
### ⚔️ 动作与场面
### 🧠 哲思与心理

**Output file**: `{output_dir}/report.md`

**IMPORTANT:**
- 整合模式: Synthesize，不是 list
- metadata.json 可能有误，以 chunks 为准
- 报告用中文，引用保持原文语言
"""
)
```

完整提示词模板见: `prompts/synthesize.md`

---

## 阶段 4: 角色档案生成（可选）

**执行者**: 1 个同步的 `general-purpose` agent
**触发条件**: 用户明确请求分析特定角色（如："生成裴语涵的角色档案"）

### 4.1 前置检查

在启动角色档案生成前，确认以下条件：
- 阶段3已完成，`report.md` 已生成
- 所有 `chunk_*.json` 文件完整存在
- 用户指定了明确的角色名称

### 4.2 启动角色档案 agent

```python
Task(
  subagent_type="general-purpose",
  run_in_background=False,  # 同步等待结果
  description="生成角色档案",
  prompt=f"""
从提示词模板 prompts/character-profile.md 读取完整模板。

关键变量替换：
- {{{{target_character}}}}: {用户指定的角色名}
- {{{{book_title}}}}: {从 metadata.json 读取}
- {{{{output_dir}}}}: {当前分析的输出目录}

执行步骤：
1. 使用 Glob 找到所有 chunks: {output_dir}/chunks/*.json
2. 读取 report.md: {output_dir}/report.md
3. 从所有 chunks 中过滤包含目标角色的信息
4. 按照模板要求生成角色档案
5. 创建目录: mkdir -p {output_dir}/characters
6. 保存到: {output_dir}/characters/profile_{角色名}.md

CRITICAL:
- 报告用简体中文
- 原文引用必须保留原语言，禁止翻译
- 自动识别角色别名（如"林玄言"="叶临渊"）
- 重点分析角色成长弧光和心理变化
"""
)
```

完整提示词模板见: `prompts/character-profile.md`

### 4.3 支持批量生成

如果用户请求多个角色档案，可并行启动多个 agents：

```python
# 在单个消息中启动多个角色档案 agents
Task(..., description="生成裴语涵档案", prompt=...)  # 角色1
Task(..., description="生成季婵溪档案", prompt=...)  # 角色2
Task(..., description="生成陆嘉静档案", prompt=...)  # 角色3
```

### 4.4 输出示例

成功后，目录结构更新为：

```
/tmp/novel_analysis/<书名>_<timestamp>/
├── metadata.json
├── chunks/
│   ├── chunk_01.json
│   └── ...
├── report.md
└── characters/              # 新增目录
    ├── profile_裴语涵.md
    ├── profile_季婵溪.md
    └── ...
```

**角色档案内容包含**：
- 基础信息卡（姓名、别名、身份、登场时间、结局）
- 外貌与形象（容貌、衣着、形象演变）
- 性格侧写（核心特质、深度分析、语言风格）
- 能力与技能（战斗风格/专业技能）
- 个人履历（按时间线梳理关键事件）
- 人际关系网（与其他角色的互动）
- 印象深刻的原文（台词和侧写引用）
- 心理分析与主题意义
- 总结评价

---

## 配置参数

以下参数可根据需要调整：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `target_tokens` | 50000 | 每块目标 token 数 |
| `overlap_lines` | 200 | 块间重叠行数 |
| `chars_per_token` | 1.35 | 中文字符/token 比率 |
| `max_concurrent` | 16 | 最大并行 agent 数 |

---

## 错误处理

| 场景 | 处理方式 |
|------|---------|
| 文件不存在 | 立即终止，报告错误 |
| 文件过大无法一次读取 | 使用 offset/limit 分段读取 |
| 部分 chunk agent 失败 | 继续处理其他，报告中标注缺失块 |
| 整合 agent 失败 | 保留 chunk JSONs，建议用户手动整合 |

---

## 最终输出

成功完成后，输出目录结构：

```
/tmp/novel_analysis/<书名>_<timestamp>/
├── metadata.json      # 全书元数据
├── chunks/            # 各分块详细分析
│   ├── chunk_01.json
│   ├── chunk_02.json
│   └── ...
├── report.md          # 📖 最终深度阅读报告（中文）
└── characters/        # 📋 角色档案（如果执行了阶段4）
    ├── profile_角色A.md
    └── ...
```

**向用户报告**:
```
分析完成！

输出目录: /tmp/novel_analysis/<书名>_<timestamp>/
├── metadata.json      # 元数据
├── chunks/            # 分块分析 (N 个文件)
│   ├── chunk_01.json
│   └── ...
├── report.md          # 深度阅读报告
└── characters/        # 角色档案（如有）
    └── profile_XX.md

查看完整报告: cat <输出目录>/report.md
查看角色档案: cat <输出目录>/characters/profile_XX.md
```

---

## 使用示例

### 示例 1: 完整分析

**用户**: "帮我深度分析 novel.txt"

**你的执行**:
1. 创建 todo list 跟踪进度
2. 统计行数，创建输出目录
3. 分段读取，生成 metadata.json
4. 计算分块边界
5. **在单个消息中**启动所有并行 chunk agents
6. 等待全部完成
7. 启动整合 agent（同步）
8. 报告完成，提供目录路径

### 示例 2: 分析 + 角色档案（带角色追踪）

**用户**: "分析 novel.txt，并生成主角的角色档案"

**你的执行**:
1. 执行阶段1（粗读元数据）
2. 从 metadata.json 识别主角名称（假设为"张三"）
3. **启动阶段2时，在每个 chunk agent 的 prompt 末尾追加角色追踪指令**：
   ```
   ### SPECIAL INSTRUCTION: Character Tracking
   The user wants a detailed profile for character: 张三

   If 张三 appears in your chunk:
   - Record ALL details (appearance, dialogue, actions, emotions)
   - Capture verbatim quotes
   - Note relationship developments

   If 张三 does NOT appear: proceed normally
   ```
4. 等待所有 chunk agents 完成（此时每个包含张三的chunk都有详细记录）
5. 启动阶段3（整合报告）
6. 启动阶段4（角色档案），此时有充足的原始数据支持
7. 报告完成，提供 report.md 和 profile_张三.md 的路径

### 示例 3: 仅生成角色档案（已有分析数据）

**用户**: "帮我生成裴语涵的角色档案"（前提：已经分析过琼明神女录）

**你的执行**:
1. 确认输出目录存在（如 `/tmp/novel_analysis/琼明神女录_20251208_154904/`）
2. 检查 metadata.json、chunks/、report.md 都存在
3. 直接启动角色档案 agent（阶段4），目标角色="裴语涵"
4. 报告完成，提供 profile_裴语涵.md 的路径

### 示例 4: 批量生成多个角色档案

**用户**: "生成所有主要女性角色的档案"

**你的执行**:
1. 从 report.md 或 metadata.json 识别主要女性角色
2. **在单个消息中**并行启动多个角色档案 agents
3. 等待全部完成
4. 报告完成，列出所有生成的档案路径

**注意**: 始终使用 TodoWrite 跟踪各阶段的进度。
