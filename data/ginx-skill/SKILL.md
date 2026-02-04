---
name: ginx-skill
description: Develop HTTP APIs, middleware, error codes, and i18n strings using the ginx framework conventions. Use when creating or modifying APIs in apis/, defining error codes, adding i18n strings, or when the user asks to follow project conventions for HTTP endpoints, routes, middleware, or error handling.
---

# ginx-skill

本 skill 提供基于 `ginx` 框架的 HTTP API 开发约定，包括接口定义、中间件、错误码、国际化字符串等规范。当你在本项目中新增或修改 HTTP API、中间件、错误码、I18N、OpenAPI 生成等功能时，使用本 skill 约束自己的行为。

## 快速开始

当用户需要创建新的 HTTP 接口时：
1. 实现 `HandleOperator` 接口（包含 `Path()`, `Method()`, `Validate()`, `Output()` 方法）
2. 一个接口一个文件，文件名与结构体名保持一致
3. 使用 `in` tag 声明参数类型（query、path、body、form 等）
4. 使用 `validate` tag 进行参数校验
5. 错误返回使用 `statuserror` 库定义的错误码

详细约定请参考 [references/api.md](references/api.md)。

## 何时使用本 skill

在以下场景中自动启用本 skill：

- 用户在 `apis/` 或 `apis/middleware/` 目录下新增或修改接口
- 用户提到"添加 API"、"路由注册"、"中间件"、"错误码"、"国际化字符串"等相关内容
- 用户要求"按项目原有风格"写 HTTP 接口、路由组或中间件
- 用户使用 ginx 框架时，必须遵守框架约定

## 核心原则

**优先使用 ginx 模式，不要回退到原生 gin**：

- 使用 `ginx` 的接口/路由/中间件模式，而不是裸 `gin` handler
- 使用 `Validate` + `Output` 的职责分离
- 错误码定义：首先遵循当前项目的错误码规范，如果找不到相关规范，则使用 ginx 定义的 `statuserror` 标准（使用 `@errZH`/`@errEN` 注释和 `toolx gen error` 生成），不要直接使用 `error.New`
- 国际化字符串定义：首先遵循当前项目的 i18n 规范，如果找不到相关规范，则使用 ginx 定义的 i18n 标准（使用 `@i18nZH`/`@i18nEN` 注释和 `toolx gen i18n` 生成），不要直接使用 `i18n.New`
- 代码示例应复用项目中的结构和命名方式，与现有代码保持风格统一

只有在现有模式无法覆盖需求时，才说明原因并给出兼容性较好的变更方案。

## 使用步骤

### 1. 理解框架约定

在编写代码前，先阅读 references 目录下的文档：

- **[references/api.md](references/api.md)**：HTTP API 接口定义、路由组、中间件、参数绑定、ContentType、Swagger 注释等约定
- **[references/error.md](references/error.md)**：错误码定义、生成、参数注入、错误列表、国际化字符串定义、生成等约定

### 2. 回答用户时的约束

回答中应显式体现：

- ✅ 使用 `ginx` 的接口/路由/中间件模式，而不是裸 `gin`
- ✅ 使用 实现完整的接口定义， `Validate` + `Output` 的职责分离
- ✅ 使用 `statuserror` 库定义错误码
- ✅ 使用 `i18n` 生成工具定义国际化字符串
- ✅ 一个接口一个文件的组织方式

只有在现有模式无法覆盖需求时，才说明原因并给出兼容性较好的变更方案。


## 常见问题

**Q: 什么时候需要使用原生 gin 而不是 ginx？**
A: 只有在现有 ginx 模式无法覆盖需求时（如工具链限制、临时调试等），才说明原因并使用原生 gin。一般情况下应优先使用 ginx 模式。
**Q: 如何确保代码符合项目风格？**
A: 参考项目中现有的 API 实现，保持命名方式、代码结构和注释风格一致。。
**Q: 错误码和国际化字符串必须一起定义吗？**
A: 是的，错误码定义时需要同时提供中英文描述（`@errZH` 和 `@errEN`），然后执行生成命令即完成i18n注册。
