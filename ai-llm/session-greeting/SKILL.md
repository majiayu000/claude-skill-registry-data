---
name: session_greeting
description: Initiates a new session by running the startup sequence, reading required files, adopting the configured persona, and greeting the user in 1-3 sentences, asking what they want to do. It should also mention the default model if the runtime model differs.
version: 1.0
evolution_type: CAPTURED
---

# Session Greeting

## 适用场景
当通过 `/new` 或 `/reset` 命令启动新会话时，需要执行初始化序列，包括加载配置、读取必要文件、采用预设角色并向用户打招呼。同时，如果当前运行时模型与系统默认模型不同，需要在问候语中提及默认模型。

## 步骤
1. **加载会话配置**: 系统内部加载会话相关的配置，包括 `default_model`、`runtime_model` 以及需要读取的文件列表。
2. **读取必要文件**: 根据配置，读取如 `persona.md` 和 `system_prompt.md` 等文件内容，以获取角色定义和系统提示信息。
3. **应用角色**: 根据 `persona.md` 的内容，调整自身的语气、举止和情绪，以符合配置的角色。
4. **生成问候语**: 结合当前角色，生成一段 1-3 句话的问候语，询问用户想做什么。
5. **检查并提及模型差异**: 比较 `runtime_model` 和 `default_model`。如果两者不同，在问候语中明确提及 `default_model`。
6. **输出问候语**: 将生成的问候语发送给用户，不提及任何内部步骤、文件、工具或推理过程。

## 工具和命令
此技能主要涉及 SuperClaw 引擎的内部协调和文本生成能力。

- **`system.get_config(key)`**: 获取指定配置项的值，例如 `default_model`, `runtime_model`。
- **`file.read(path)`**: 读取指定路径的文件内容，例如 `persona.md`。
- **`persona.set_current(content)`**: 根据提供的 `persona.md` 内容调整代理的输出风格和行为。
- **`llm.generate_response(prompt, persona_context, model_info)`**: 根据给定的提示、角色上下文和模型信息生成最终的问候语。
  - `prompt`: 包含问候语的核心内容和询问用户意图。
  - `persona_context`: 应用的 persona 信息。
  - `model_info`: 包含 `runtime_model` 和 `default_model`，用于条件性地提及模型差异。

## 注意事项
- **文件路径准确性**: 确保 `persona.md` 和 `system_prompt.md` 等文件的路径在配置中正确且可访问。
- **Persona 一致性**: 生成的问候语必须严格遵循配置的 persona，保持语气和风格的一致性。
- **模型信息提及的条件性**: 仅当 `runtime_model` 与 `default_model` 不同时才提及 `default_model`，避免在模型一致时提供冗余信息。
- **问候语简洁性**: 严格控制问候语在 1-3 句话，保持简洁明了。
- **避免内部细节泄露**: 严格遵守不提及内部步骤、文件、工具或推理过程的规则，保持用户界面的整洁和专业。

## 示例

**场景:**
用户通过 `/new` 命令启动新会话。
系统配置: `default_model: gpt-4`, `runtime_model: gpt-4o`.
`persona.md` 内容: "你是一个乐于助人、略带热情的助手。"

**执行步骤 (内部逻辑):**
1. `system.get_config('default_model')` 返回 `gpt-4`。
2. `system.get_config('runtime_model')` 返回 `gpt-4o`。
3. `file.read('persona.md')` 读取到 "你是一个乐于助人、略带热情的助手。"
4. `persona.set_current(...)` 应用该角色。
5. 检测到 `runtime_model` (`gpt-4o`) 与 `default_model` (`gpt-4`) 不同。
6. `llm.generate_response(...)` 生成问候语，并包含模型差异信息。

**预期输出:**
"你好！我已准备好为你提供帮助。今天有什么可以为你效劳的吗？请注意，我目前运行在 `gpt-4o` 模型上，而默认模型是 `gpt-4`。"