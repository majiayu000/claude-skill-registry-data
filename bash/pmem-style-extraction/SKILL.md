---
name: pmem-style-extraction
description: 从多模态信息源（文章、URL、Skill、图像）中提取写作风格特征并存储至 powermem 知识库。支持风格冲突检测和人工仲裁（抛弃/覆盖/分支）。当用户提到"提取风格"、"学习风格"、"分析文章风格"、"保存写作特征"或提供文章/URL 要求分析其写作特色时使用此 skill。
---

# Style Extraction

从多模态输入中提取写作风格特征，并存储到 powermem 知识库中，支持智能冲突检测和人工仲裁。

## 核心流程

执行以下步骤提取和存储风格特征：

### 0. 环境准备（首次执行）

在运行任何脚本前，先准备 `.venv`。下面的写法不依赖固定绝对路径：

```bash
ROOT_DIR="$(cd ../.. && pwd)"
PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
test -d "$ROOT_DIR/.venv" || python3 -m venv "$ROOT_DIR/.venv"
"$PYTHON_BIN" -m pip install -U pip
"$PYTHON_BIN" -m pip install -U powermem python-dotenv
```

后续所有 Python 脚本都使用 `$PYTHON_BIN` 执行，不依赖当前 shell 是否已激活虚拟环境。

**配置管理说明**：
- 首次使用时，脚本会自动创建 `../pmem-config/` 共享配置目录
- 包含 `pmem-key.env`（用户配置）和 `.env`（完整模板）
- 配置优先级：系统环境变量 > `pmem-config/pmem-key.env` > `pmem-config/.env`
- 两个 skills（extraction 和 generation）共享同一配置，配置一次即可

### 0.1 配置检测（必需步骤）

**每次运行前必须执行配置检测**：

```bash
"$PYTHON_BIN" scripts/check_config.py
```

**如果配置检测失败（退出码为 1）**：

1. **检测输出说明（固定文案保留在 Skill 中，仅缺失项由脚本动态输出）**：
   ```bash
   # 运行配置检测（脚本会动态输出“当前缺失的配置项”）
   "$PYTHON_BIN" scripts/check_config.py
   ```
   
   输出结构示例（缺失项列表以脚本实际检测结果为准）：
   ```
   ⚠️  检测到以下配置项缺失或未设置:
   
   [这里的缺失项列表由 check_config.py 动态输出]
   
   📝 共享配置文件位置: /path/to/skills/pmem-config/pmem-key.env
   
   请点击上面的共享配置文件路径，进入文件夹后手动编辑文件：`pmem-key.env`。
   手动填写完成后，返回聊天框回复：已完成
   ```

2. **Agent 应执行以下操作**：
   - 明确告知用户共享配置目录路径：`../pmem-config/`
   - 明确告知用户需要编辑的文件名：`pmem-key.env`
   - 不在对话中逐项收集配置值，仅等待用户手动填写
   - 用户回复“已完成”后，重新运行 `check_config.py` 验证配置

3. **写入配置示例**：
   ```bash
   # 用户手动打开并编辑：../pmem-config/pmem-key.env
   # 在文件中填写缺失项，例如：
   LLM_API_KEY=sk-xxxxx
   EMBEDDING_API_KEY=sk-yyyyy
   
   # 重新检测
   "$PYTHON_BIN" scripts/check_config.py
   ```

4. **重要提示**：
   - 配置会持久化保存在 `../pmem-config/pmem-key.env`
   - 下次使用任一 skill 时无需重复配置
   - 用户也可以手动编辑该文件修改配置

**配置检测通过后**，继续执行后续步骤。

### 1. 获取内容

根据输入类型选择处理方式：

**URL 输入**：调用 baoyu-url-to-markdown 获取网页内容

```bash
SKILL_URL_DIR="$HOME/.cursor/skills/baoyu-url-to-markdown"
npx -y bun ${SKILL_URL_DIR}/scripts/main.ts <url> -o /tmp/extracted_content.md
```

然后读取 `/tmp/extracted_content.md` 作为后续分析的输入。

**文本/文件输入**：直接使用提供的内容。

**Skill 文件输入**：读取 SKILL.md 文件内容。

**图像输入**：使用视觉能力提取图像中的文字排版和视觉风格元素。

### 2. 特征提取

使用 LLM 从内容中剥离事实信息，仅保留风格骨架。使用以下 Prompt 模板：

```
你是一位专业的写作风格分析师。请从下面的内容中提取纯粹的风格特征，忽略所有具体的事实、观点和信息内容。

请从以下维度提取风格特征：

1. **叙事节奏 (narrative_rhythm)**：句子长度偏好、段落节奏、信息密度
2. **金句位置 (key_phrase_placement)**：强调内容的位置习惯（段首/段中/段尾）
3. **排版符号 (formatting_symbols)**：特殊引号、列表符号、分隔符使用习惯
4. **标点习惯 (punctuation_habits)**：省略号、破折号、感叹号等使用频率和场景
5. **段落结构 (paragraph_structure)**：段落组织方式（总分总、递进、并列等）
6. **情感基调 (emotional_tone)**：理性/感性、克制/热烈、严肃/幽默等
7. **修辞手法 (rhetorical_devices)**：比喻、排比、反问等惯用修辞
8. **开篇风格 (opening_style)**：如何引入话题（直入主题/铺垫/引用/提问）
9. **结尾风格 (closing_style)**：如何收束内容（总结/升华/留白/号召）

请以 JSON 格式输出，每个维度用简洁的描述性语言概括：

{
  "narrative_rhythm": "描述",
  "key_phrase_placement": "描述",
  "formatting_symbols": "描述",
  "punctuation_habits": "描述",
  "paragraph_structure": "描述",
  "emotional_tone": "描述",
  "rhetorical_devices": "描述",
  "opening_style": "描述",
  "closing_style": "描述"
}

待分析内容：
---
{CONTENT}
---
```

将提取的特征保存为 JSON 格式（例如 `/tmp/extracted_features.json`），**然后自动进入下一步冲突检测**。

### 3. 自动冲突检测

**无需用户操作**，系统自动使用脚本搜索 powermem 中已存在的相似 Profile，并检测是否存在冲突：

```bash
"$PYTHON_BIN" scripts/search_profiles.py \
  --features /tmp/extracted_features.json \
  --threshold 0.85
```

脚本将输出：
- 是否发现相似 Profile
- 相似度分数
- 是否存在冲突特征
- 冲突详情（如果有）

### 4. 人工仲裁（仅在有冲突时）

**只有当检测到冲突时才暂停**，向用户展示对比并等待选择：

```
检测到风格特征冲突：

【已存 Profile: default】
- 叙事节奏: 短句为主，每段2-4行
- 情感基调: 理性克制

【新提取特征】
- 叙事节奏: 长句排比，情绪化段落
- 情感基调: 热烈煽情

请选择处理方式：
1. 抛弃 - 仅作参考，不写入
2. 覆盖 - 用新特征替换旧 Profile
3. 分支 - 保留旧 Profile，新建独立风格变体（需指定名称）
```

等待用户输入选择（1/2/3）。

**如果无冲突，直接跳到步骤 5 收集元数据**。

### 5. 交互式收集元数据

**无论是否有冲突，确定存储模式后，立即进入元数据收集**，通过对话方式逐个询问用户：

**交互流程**（Agent 逐个询问，用户回答一个后再问下一个）：

**步骤 1/6 - 适用平台**：
```
Agent: 📱 这个风格适合哪些平台？请从以下选项中选择（可多选，用逗号分隔）：
1. 小红书
2. Twitter / X
3. 公众号
4. 知乎
5. LinkedIn
6. 通用（不限平台）
7. 其他（请说明）

请输入序号或平台名称（例如：2,3 或 Twitter,公众号）
```

用户回答后，Agent 确认并继续。

**步骤 2/6 - 风格标签**：
```
Agent: 🏷️ 用几个词描述这个风格的特点，请从以下选项中选择（可多选，用逗号分隔）：
1. 轻松
2. 口语化
3. 专业
4. 严谨
5. 情绪化
6. 理性
7. 幽默
8. 简洁
9. 详细
10. 煽情
11. 克制
12. 热烈
13. 其他（请说明）

请输入序号或标签（例如：1,2,7 或 轻松,口语化,幽默）
```

用户回答后，Agent 确认并继续。

**步骤 3/6 - 总体基调**：
```
Agent: 🎭 这个风格的总体基调是？请选择一个：
1. 轻松愉快
2. 理性克制
3. 热烈煽情
4. 专业严谨
5. 幽默风趣
6. 深沉内敛
7. 激情澎湃
8. 其他（请说明）

请输入序号或描述
```

用户回答后，Agent 确认并继续。

**步骤 4/6 - 简短说明**：
```
Agent: 📝 请用一句话描述这个风格的适用场景（可跳过，直接回复"跳过"或留空）

例如：适合日常分享类内容，语气轻松亲切
```

用户回答后，Agent 确认并继续。

**步骤 5/6 - Profile ID**：
```
Agent 首先调用脚本获取智能建议：
"$PYTHON_BIN" scripts/collect_metadata.py --features /tmp/extracted_features.json --get-suggestions
{"id": "casual-style", "name": "轻松风格"}

Agent: 💡 系统建议的 Profile ID 是：casual-style

🆔 请选择：
1. 使用默认建议（casual-style）
或直接输入自定义 ID（只能使用小写字母、数字和连字符）
```

用户回答后，Agent 确认并继续。

**步骤 6/6 - Profile 名称**：
```
Agent: 💡 系统建议的显示名称是：轻松风格

📛 请选择：
1. 使用默认建议（轻松风格）
或直接输入自定义名称
```

用户回答后，Agent 汇总所有信息并确认。

**收集完成后，Agent 调用脚本保存元数据**：

```bash
"$PYTHON_BIN" scripts/collect_metadata.py \
  --features /tmp/extracted_features.json \
  --platforms "Twitter,公众号" \
  --tags "轻松,口语化,幽默" \
  --tone "理性克制" \
  --description "适合日常分享类内容，语气轻松亲切" \
  --profile-id "xiaohongshu-casual" \
  --profile-name "小红书轻松版" \
  --output /tmp/metadata.json
```

### 6. 存储 Profile

使用收集的元数据执行存储：

**无冲突 - 自动新建**：

```bash
"$PYTHON_BIN" scripts/store_profile.py \
  --features /tmp/extracted_features.json \
  --mode new \
  --source "来源标题或URL" \
  --profile-id $(jq -r '.profile_id' /tmp/metadata.json) \
  --profile-name $(jq -r '.profile_name' /tmp/metadata.json) \
  --tags $(jq -r '.tags | join(",")' /tmp/metadata.json) \
  --platforms $(jq -r '.platforms | join(",")' /tmp/metadata.json) \
  --tone $(jq -r '.tone' /tmp/metadata.json) \
  --description $(jq -r '.description' /tmp/metadata.json)
```

**覆盖模式** 和 **分支模式** 同理，使用相同的参数。

### 7. 确认结果

存储完成后，列出当前所有 Profile 供用户确认：

```bash
"$PYTHON_BIN" scripts/list_profiles.py
```

## 辅助工具

**列出所有已存 Profile**：

```bash
"$PYTHON_BIN" scripts/list_profiles.py
```

**查看 Profile 数据结构说明**：参考 [references/profile_schema.md](references/profile_schema.md)

## 环境要求

- Python 环境：使用项目的 `.venv` 虚拟环境
- 依赖：powermem SDK（脚本启动时自动加载/初始化 `.env` 配置）
- baoyu-url-to-markdown skill（处理 URL 输入时需要）

## 使用示例

**完整流程（推荐）**：
```
用户："帮我分析这篇文章的写作风格并保存：[粘贴文章内容]"

Agent（自动执行，无需用户干预）：
  1. 提取特征 → 保存到 /tmp/extracted_features.json
  2. 自动检测冲突 → 无冲突
  3. 开始逐个询问元数据（用户交互）：
     步骤 1/6：适用平台？
       → Agent 展示选项，等待用户回答
       → 用户："2,3"（Twitter 和公众号）
       → Agent："✓ 已选择：Twitter, 公众号"
     
     步骤 2/6：风格标签？
       → Agent 展示选项，等待用户回答
       → 用户："轻松,口语化,幽默"
       → Agent："✓ 已选择：轻松, 口语化, 幽默"
     
     步骤 3/6：总体基调？
       → Agent 展示选项，等待用户回答
       → 用户："2"（理性克制）
       → Agent："✓ 已选择：理性克制"
     
     步骤 4/6：简短说明？
       → Agent 询问
       → 用户："适合日常分享类内容，语气轻松亲切"
       → Agent："✓ 已填写"
     
     步骤 5/6：Profile ID？
       → Agent 获取智能建议并展示："系统建议：casual-style"
       → Agent："请选择：1. 使用默认建议 或直接输入自定义 ID"
       → 用户："1"（使用建议）或 "xiaohongshu-casual"（自定义）
       → Agent："✓ 已设置：casual-style"（或用户输入的值）
     
     步骤 6/6：Profile 名称？
       → Agent 展示建议："系统建议：轻松风格"
       → Agent："请选择：1. 使用默认建议 或直接输入自定义名称"
       → 用户："1"（使用建议）或 "小红书轻松版"（自定义）
       → Agent："✓ 已设置：轻松风格"（或用户输入的值）
  
  4. Agent 汇总并调用 Python 脚本保存元数据
  5. 自动存储 Profile
  6. 显示确认信息

整个流程中，用户只需要在元数据收集时依次回答6个问题，其他步骤自动进行。
```

**从 URL 学习风格**：
```
用户："学习这篇文章的风格：https://example.com/article"

Agent（自动）：
  1. 调用 url-to-markdown → 获取内容
  2. 提取特征 → 自动检测冲突 → 无冲突
  3. 开始逐个询问元数据（用户依次回答6个问题）
  4. 自动存储
```

**处理风格冲突**：
```
用户："分析这篇情绪化的文章"

Agent（自动）：
  1. 提取特征 → 自动检测冲突
  2. 发现与 default 冲突 → **暂停，展示冲突对比**
  
  ⚠️  检测到风格冲突...
  请选择：1.抛弃 2.覆盖 3.分支
  
  用户选择：3（分支）
  
  3. Agent 继续：开始逐个询问元数据（系统建议 profile_id: emotion-style）
  4. 自动存储为独立分支
```

## 注意事项

- 特征提取时严格排除具体事实信息，只保留风格骨架
- **自动化流程**：特征提取 → 冲突检测应自动进行，无需用户等待确认
- **仅在必要时暂停**：只有检测到冲突时才暂停等待用户决策（抛弃/覆盖/分支）
- **元数据收集是主要交互点**：Agent 通过对话逐个询问6个问题，用户回答一个问题后再问下一个
- **不使用交互式 CLI 工具**：通过 Agent 对话收集元数据，最后调用 Python 脚本保存
- 运行脚本前优先确保 `$PYTHON_BIN` 可用，并已安装 `powermem`
- 冲突检测阈值（0.85）可根据实际情况调整
- Profile 以 `user_id="style_owner"` 固定命名空间存储，支持多个 Profile 共存
- 每个 Profile 通过 `profile_id` 唯一标识（如 default、emotion-style）
- 所有脚本都会先执行环境自举：自动创建 `.env`（若缺失）并加载配置
- 分支模式下建议使用描述性命名（如"学术严谨版"、"轻松幽默版"）
- 元数据对 Generation Skill 的智能匹配至关重要，不可省略
