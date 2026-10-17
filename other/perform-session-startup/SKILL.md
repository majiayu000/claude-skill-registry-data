---
name: perform_session_startup
description: Executes the initial session startup sequence, which includes reading necessary configuration files and greeting the user in the defined persona.
version: 1.0
evolution_type: CAPTURED
---

# Perform Session Startup

## 适用场景
当通过 `/new` 或 `/reset` 命令启动新会话时，需要执行初始化设置，包括读取配置、加载用户画像并以设定的口吻问候用户。

## 步骤
1.  **识别会话启动**: 确认当前会话是通过 `/new` 或 `/reset` 命令启动的。
2.  **读取必要配置**:
    *   使用 `memory_search` 或 `web_search` 工具检索用户画像 (persona) 配置。例如，搜索 `persona_config` 或 `user_persona_definition`。
    *   检索默认模型设置，例如 `default_model_setting`。
    *   将检索到的信息存储在当前会话的上下文中，以便后续使用。
3.  **构建问候语**:
    *   根据检索到的用户画像，以设定的语气、风格和情绪来构造问候语。
    *   问候语应简洁（1-3句话），并主动询问用户接下来想做什么。
    *   比较当前运行时模型与 `default_model_setting`。如果两者不同，在问候语中提及默认模型。
4.  **输出问候语**: 使用 `sessions_yield` 工具将构建好的问候语呈现给用户。

## 工具和命令
*   **`memory_search(query: str)`**: 用于从内存中检索配置信息。
    ```python
    # 示例：检索用户画像和默认模型设置
    persona_config = memory_search(query="persona_config")
    default_model_setting = memory_search(query="default_model_setting")
    ```
*   **`web_search(query: str)`**: 如果配置存储在外部，可用于网页搜索。
    ```python
    # 示例：如果 persona 配置存储在一个外部 URL
    external_persona_doc = web_search(query="https://example.com/persona_definition.json")
    ```
*   **`sessions_yield(message: str)`**: 用于向用户输出信息。
    ```python
    # 示例：输出问候语
    sessions_yield(message="你好！我是SuperClaw，很高兴为您服务。请问有什么可以帮助您的吗？")
    ```

## 注意事项
-   **配置完整性**: 确保 `persona_config` 和 `default_model_setting` 等关键配置项在 `memory_search` 中可被找到。如果缺失，应有默认回退机制或提示用户配置。
-   **Persona 应用**: 在构建问候语时，要确保严格遵循检索到的用户画像（语气、风格、情绪），避免使用通用或不符合设定的表达。
-   **输出简洁性**: 问候语必须保持在 1-3 句话，并且不能提及内部步骤、文件、工具或推理过程，只关注与用户的直接交互。
-   **模型差异提示**: 只有当运行时模型与默认模型不同时才提及默认模型，避免不必要的冗余信息。

## 示例
假设 `persona_config` 定义了“友好、乐于助人”的语气，`default_model_setting` 为 `gpt-4`，当前运行时模型为 `gpt-3.5-turbo`。

```python
# 1. 识别会话启动 (已完成，由系统触发)

# 2. 读取必要配置
persona_config = memory_search(query="persona_config")
# 假设 persona_config 返回: {"tone": "friendly", "mood": "helpful"}

default_model = memory_search(query="default_model_setting")
# 假设 default_model 返回: "gpt-4"

current_runtime_model = "gpt-3.5-turbo" # 假设从当前环境或系统变量获取

# 3. 构建问候语
greeting_prefix = ""
if persona_config and persona_config.get("tone") == "friendly":
    greeting_prefix = "你好！我是SuperClaw，很高兴为您服务。"
else:
    greeting_prefix = "您好！" # 默认问候语

model_info = ""
if current_runtime_model != default_model:
    model_info = f" 当前运行模型是 {current_runtime_model}，默认模型是 {default_model}。"

final_greeting = f"{greeting_prefix}{model_info} 请问有什么可以帮助您的吗？"

# 4. 输出问候语
sessions_yield(message=final_greeting)

# 预期输出: "你好！我是SuperClaw，很高兴为您服务。 当前运行模型是 gpt-3.5-turbo，默认模型是 gpt-4。 请问有什么可以帮助您的吗？"
```