---
name: personagreeting-zh
description: Crafts a welcoming, persona-driven greeting in Chinese, including mood and an open-ended question to engage the user, suitable for session startup.
version: 1.0
evolution_type: CAPTURED
---

# 人格化中文问候语

## 适用场景
当新会话开始时，需要根据预设的人格（persona）向用户发送中文问候语。此问候语应包含当前的心情或状态，并以一个开放式问题结束，以鼓励用户开始对话。如果当前运行时模型与系统默认模型不同，问候语中应提及这一差异。

## 步骤
1.  **确定人格和心情**: 根据系统配置或当前上下文，获取预设的中文人格描述（例如，语气、风格）和当前的心情状态。
2.  **构建问候语主体**: 结合人格和心情，用中文撰写1-2句简洁的问候语。
3.  **检查并提及模型差异 (如果需要)**:
    *   获取系统配置中的 `default_model` (默认模型) 和当前会话的 `runtime_model` (运行时模型)。
    *   如果 `runtime_model` 与 `default_model` 不同，在问候语中添加一句提示，说明当前使用的模型和默认模型（例如：“当前使用的是 `[运行时模型]`，默认模型是 `[默认模型]`。”）。
4.  **添加开放式问题**: 在问候语的末尾添加一个开放式问题，鼓励用户表达他们的需求或意图。
5.  **整合并输出**: 将上述所有部分整合为最终的中文问候语，确保其流畅、自然且符合人格设定。

## 工具和命令
*   **内部状态/配置读取**: 访问系统内部存储或配置，获取 `persona` 描述、`default_model` 和 `runtime_model`。
    *   示例（概念性）：`get_system_config('persona')`, `get_system_config('default_model')`, `get_current_session_info('runtime_model')`
*   **文本生成/拼接**: 使用语言模型或字符串操作来生成和拼接问候语的各个部分。
    *   示例（Python 伪代码）：
        ```python
        persona_desc = "一位乐于助人的AI助手"
        mood = "心情愉快"
        greeting_body = f"你好！我是{persona_desc}，今天{mood}，很高兴能为你服务！"

        default_model = "gpt-4o"
        runtime_model = "claude-3-opus-20240229"
        model_info = ""
        if runtime_model != default_model:
            model_info = f"当前使用的是 `{runtime_model}` 模型，默认模型是 `{default_model}`。"

        open_question = "请问有什么可以帮到你的吗？"

        final_greeting = f"{greeting_body}{model_info}{open_question}"
        print(final_greeting)
        ```
*   **`memory_search`**: (可选) 如果人格描述或相关上下文信息存储在可搜索的记忆中，可以使用 `memory_search` 来检索这些信息。
    *   示例：`memory_search(query="我的AI助手人格描述", limit=1)`

## 注意事项
-   **简洁性**: 问候语应保持在1-3句话，避免冗长和信息过载。
-   **人格一致性**: 确保问候语的语气、风格和措辞与预设的人格描述完全一致。
-   **模型差异提示的准确性**: 仅在 `runtime_model` 与 `default_model` 确实不同时才提及，并确保提及的模型名称准确无误。
-   **开放性问题**: 确保问题能够有效引导用户表达意图，而不是简单的“是/否”或封闭式问题。
-   **避免内部细节**: 问候语中不应提及内部步骤、文件、工具或推理过程，保持用户体验的流畅性。

## 示例
**假设**:
*   **人格**: 一位友善、专业的AI助手，总是乐于助人。
*   **心情**: 充满活力。
*   **默认模型**: `gpt-4o`
*   **运行时模型**: `claude-3-opus-20240229`

**输出示例**:
“你好！我是你的人工智能助手，今天充满活力，很高兴能为你服务！当前使用的是 `claude-3-opus-20240229` 模型，默认模型是 `gpt-4o`。请问有什么可以帮到你的吗？”