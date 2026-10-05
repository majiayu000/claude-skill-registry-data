---
name: pmem-style-generation
description: 基于 powermem 中的 Style Profile 生成带有个人烙印的文稿。先中立提取素材核心信息，再拉取风格 Profile 组装 Compiler Prompt 驱动大模型输出。当用户提到"帮我写一篇"、"按我的风格写"、"生成文章"、"写条推特"、"写个小红书"、"写公众号文章"，或提供素材要求创作时使用此 skill。
---

# Style Generation

两步走：先对素材做"信息脱水"，再用风格 Profile 做"注魂"，最终一次性输出专属文稿。

## 核心流程

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

### 1. 确认创作指令

从用户输入中明确以下信息（如有缺失则主动询问）：

| 参数 | 说明 | 示例 |
|------|------|------|
| **目标平台** | 决定文体和篇幅 | Twitter、小红书、公众号、通用长文 |
| **风格意图** | 用户的模糊描述（非技术 profile_id） | "轻松点"、"专业严肃"、"情绪化" |
| **原始素材** | 待创作的原始内容（文章/URL/要点列表） | 粘贴文章、提供 URL、列出几个事实 |

如果用户提供了 URL 素材，先调用 baoyu-url-to-markdown 获取内容：

```bash
SKILL_URL_DIR="$HOME/.cursor/skills/baoyu-url-to-markdown"
npx -y bun ${SKILL_URL_DIR}/scripts/main.ts <url> -o /tmp/source_content.md
```

### 2. 信息脱水（中立大纲提取）

**不调用任何风格**，仅对原始素材做客观信息提取。使用以下 Prompt：

```
你是一位中立的信息提炼专家。请从下面的素材中提取纯粹的事实信息和核心论点，不加入任何情感或风格倾向。

输出格式为结构化大纲：

## 核心主题
[一句话概括素材的主题]

## 关键事实
- [事实1]
- [事实2]
- [事实3，最多5-8条]

## 核心论点/观点
- [论点1]
- [论点2]

## 数据与引用
- [数据或引用（如有）]

## 背景上下文
[必要背景信息，1-3句]

待提炼素材：
---
{MATERIAL}
---
```

将提炼结果保存为 `/tmp/material_outline.md`。

### 3. 智能匹配 Style Profile（Human-in-the-loop）

**关键改进**：不直接使用固定的 Profile，而是根据用户意图智能匹配并让用户确认。

```bash
"$PYTHON_BIN" scripts/match_profile.py \
  --intent "用小红书风格写，轻松一点" \
  --output /tmp/selected_profile.json
```

脚本会：
1. 分析用户意图关键词（"小红书"、"轻松"）
2. 匹配所有 Profile 的 tags、suitable_platforms、tone
3. 按匹配度排序，展示前 5 个
4. 让用户确认选择（输入序号）
5. 返回选定的 Profile

**输出示例**：

```
🎯 根据您的需求，推荐以下风格：

1. [xiaohongshu-casual] 小红书轻松版
   匹配原因：适合小红书平台, 风格特点：轻松, 风格特点：口语化
   说明：适合日常分享类内容，语气轻松亲切
   标签：轻松, 口语化, 亲切
   平台：小红书

2. [default] 默认风格
   匹配原因：适合小红书平台
   平台：小红书, 公众号, 通用

请选择要使用的风格（输入序号），或输入 0 退出：
> 1

✅ 已选择：[xiaohongshu-casual] 小红书轻松版
```

**如果完全没有匹配**：

```
⚠️  未找到精确匹配，以下是所有可用风格：

1. [default] 默认风格
   理性克制，适合通用内容

2. [tech-article] 技术文章风格
   专业严谨，适合技术博客

请选择要使用的风格（输入序号），或输入 0 退出：
```

从返回的 JSON 读取选定的 Profile：

```bash
# 读取选定的 Profile
profile_id=$(jq -r '.profile_id' /tmp/selected_profile.json)
```

### 4. 组装 Compiler Prompt

读取 `/tmp/active_profile.json`，从中提取风格参数，结合平台规则（见 [references/platform_templates.md](references/platform_templates.md)），组装最终 Prompt。

使用以下 Compiler 模板：

```
你是一位专业的自媒体内容创作者，拥有鲜明的个人写作风格。

## 你的写作风格指令（必须严格遵守，不可违背）

**叙事节奏**：{narrative_rhythm}
**金句位置**：{key_phrase_placement}
**排版符号**：{formatting_symbols}
**标点习惯**：{punctuation_habits}
**段落结构**：{paragraph_structure}
**情感基调**：{emotional_tone}
**修辞手法**：{rhetorical_devices}
**开篇风格**：{opening_style}
**结尾风格**：{closing_style}

## 当次创作任务

**目标平台**：{platform}
**平台规范**：{platform_rules}

## 素材大纲（核心事实，保持中立使用，不可凭空添加）

{material_outline}

## 输出要求

基于以上素材，完全按照你的写作风格，为{platform}创作一篇文章。
- 素材中的事实不可歪曲，但表达方式完全按你的风格来
- 严格遵守平台字数和格式规范
- 直接输出正文，无需说明你在做什么
```

将 `{...}` 替换为实际值后，直接调用 LLM 执行。

### 5. 输出文稿、记录日志并自动落盘

先将 LLM 返回的最终正文保存到临时文件 `/tmp/generated_body.md`，然后记录本次生成日志（供 Reflection Skill 溯源）：

```bash
"$PYTHON_BIN" scripts/log_generation.py \
  --profile-id <profile_id> \
  --platform <platform> \
  --topic "<核心主题一句话>" \
  --output /tmp/generation_log.json
```

接着将最终正文自动保存到指定路径（默认 `outputs/`）：

```bash
"$PYTHON_BIN" scripts/save_generation.py \
  --profile-id <profile_id> \
  --log-json /tmp/generation_log.json \
  --title "<标题>" \
  --content-file /tmp/generated_body.md \
  --output-dir outputs
```

默认文件名规则：

```text
outputs/{profile_id}_{generation_id}_{title}.md
```

其中 `generation_id` 来自 `/tmp/generation_log.json`。执行后向用户返回两个信息：
1. `generation_id`（便于 Reflection Skill 追踪效果）
2. 最终正文文件绝对路径（便于直接查看/发布）

## 平台规范速查

详细模板见 [references/platform_templates.md](references/platform_templates.md)，核心规范如下：

| 平台 | 篇幅 | 特殊要求 |
|------|------|---------|
| Twitter / X | 每段≤140字，总≤2000字 | 首句即金句，结尾引导转发 |
| 小红书 | 300-800字 | 标题用数字/疑问，正文emoji适量，结尾引导收藏 |
| 公众号 | 800-3000字 | 有小标题分节，完整起承转合，结尾引发思考 |
| 通用长文 | 自由 | 遵循风格 Profile，结构完整 |

## 辅助工具

**列出所有可用 Profile**：
```bash
"$PYTHON_BIN" ../pmem-style-extraction/scripts/list_profiles.py --format detailed
```

**查看生成日志**：
```bash
"$PYTHON_BIN" scripts/log_generation.py --list
```

**保存最终正文到 outputs/**：
```bash
"$PYTHON_BIN" scripts/save_generation.py \
  --profile-id <profile_id> \
  --log-json /tmp/generation_log.json \
  --title "<标题>" \
  --content-file /tmp/generated_body.md
```

## 使用示例

**最简单的使用**：
```
用户："帮我写一篇小红书，素材是这篇文章：[粘贴文章]"
Agent：
  1. 脱水 → 提取核心事实
  2. 智能匹配 Profile（意图："小红书"）→ 展示匹配结果 → 用户选择
  3. 组装 Compiler Prompt（小红书规范）
  4. 输出文稿 + 记录日志 + 自动保存到 outputs/
```

**指定风格特点**：
```
用户："用轻松点的风格，写一篇关于AI的推特长文，素材：[要点列表]"
Agent：
  智能匹配（意图："轻松 推特"）→ 展示推荐 Profile → 用户确认 → 生成
```

**从 URL 生成**：
```
用户："把这篇文章改写成公众号风格：https://example.com/article"
Agent：获取网页内容 → 脱水 → 匹配风格 → 用户确认 → 生成
```

## 注意事项

- 信息脱水步骤必须独立执行，确保素材中的事实不被风格污染
- **必须使用 match_profile.py 进行智能匹配**，让用户确认选择，不要直接使用固定 profile_id
- 用户的意图通常是模糊的（"小红书"、"轻松点"），而不是技术性的 profile_id
- Compiler Prompt 中所有 `{...}` 占位符必须替换完毕再发给 LLM
- 如果 Profile 中某个维度为空，跳过该行，不要写"无"或默认值
- 生成日志 ID 务必告知用户，便于后续 Reflection 归因
- 运行脚本前优先确保 `$PYTHON_BIN` 可用，并已安装 `powermem`
