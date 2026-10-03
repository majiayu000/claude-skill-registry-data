---
name: integration-e2e-testing
description: Design and write repeatable integration or end-to-end tests for a concrete cross-component user flow. Use when the user wants runnable API, service, message, or browser flow tests; not for unit tests or one-off browser automation.
---

# 集成与端到端测试

围绕一条明确的业务流程编写可重复运行的测试，验证组件之间真实的输入、输出和状态。用户只要求测试方案时，交付用例与环境条件；要求测试代码时，遵循项目既有测试框架和目录。

## 工作方式

1. **确定验证边界。** 明确入口、经过的组件、可观察的终点、期望行为以及必须保留的环境边界。先查看项目现有测试运行方式、测试数据和外部依赖。测试环境、凭据来源或依赖替身未定且会改变测试意义时，先确认。
2. **选最小有效场景。** 根据需求和真实故障风险覆盖主成功路径与关键失败或边界路径。断言最终业务结果和必要副作用，不照抄内部实现、页面 DOM 细节或每一步临时状态。
3. **让测试可重复。** 使用隔离的测试账号、数据库或命名空间；准备与清理数据；对外部支付、邮件等副作用使用项目已有的沙箱或替身。异步流程等待可观察条件并设置截止时间，不用任意固定睡眠。浏览器测试优先沿用项目现有测试运行器。
4. **运行并解释结果。** 运行相关测试，区分断言失败、环境不可用与不稳定测试；保留必要的失败日志、请求 ID、截图或 trace，避免输出敏感数据。修复由本次测试代码造成的问题后重跑。无法连接目标环境时说明未验证，不把未运行的测试说成通过。

不要让测试访问生产系统、发送真实通知或改变真实数据，除非用户明确授权了该环境与副作用。需要新增测试框架或测试环境时，先核对项目约定并说明具体取舍。

## 边界

- 单元测试、进程内 API 测试和用例文档：`code-testing`。
- 临时打开页面、截图、提取数据或手工调试 UI：`automation-playwright`。
- 功能本身的端到端开发：`code-vibe-workflow`；本 skill 只负责验证流程。
- 性能与负载测试：`performance-investigation`。
