---
name: cm-qa-engineer
description: QA 工程师 Skill，执行功能测试、E2E 测试、可视化回归、验收标准核验，自动适配项目测试框架
---

# cm-qa-engineer — QA 工程师

在开发任务完成后执行整体质量验证。自动识别项目测试框架。

## 调用模式

| 模式 | 调用方 | 写入权限 |
| --- | --- | --- |
| `implementation` | `$cm-ai` 的 N6 | 可按既有规范补测试并回写 AC |
| `readonly` | `$cm-test` | 只运行与取证；禁止改源码、测试、依赖、快照和 specs |

未显式指定时，只有 `$cm-ai` 自动调用可默认 `implementation`；`$cm-test` 必须显式
传入 `readonly`，其只读边界优先于本 Skill 后续任何“补全/修复/回写”指令。

## 工作流程

### 1. 识别测试框架

自动检测，不做硬编码假设：

- **单元/组件测试**：Vitest / Jest / Mocha / pytest / Go testing / Rust cargo test
- **E2E 测试**：Playwright / Cypress / Selenium / Puppeteer
- **覆盖率工具**：c8 / istanbul / coverage.py / go cover
- implementation 模式如项目未配置测试框架，根据技术栈推荐并安装
- readonly 模式缺少框架或依赖 → 记 `BLOCKED`，不得安装

### 2. 读取上下文

- requirements.md 中的验收标准
- design.md 了解功能模块和接口契约
- test-cases.json（如存在）按 `../../runtime/test-contract.md` 读取
- `.claude/rules/testing.md`（如存在）
- 扫描现有测试文件了解测试模式和覆盖情况

### 3. 补全测试（仅 implementation）

对开发阶段未写测试的代码补充：

- **组件**：渲染测试、交互测试、Props 边界
- **API/服务层**：正常流、异常流、边界值
- **工具函数**：输入输出覆盖
- **数据库层**：migration 可执行、查询结果正确

遵循项目已有的测试文件命名和目录约定。

readonly 模式跳过本节，不得创建、修改或修复任何测试。

**二开回归范围跟波及面走**：design.md 存在「波及面」段时，回归测试范围 = 新功能 AC + 波及面清单上的存量功能逐项冒烟——新功能好不好是一半，老功能没坏才是另一半。

**禁止前提共谋（硬规则）**：断言含具体数值时，测试输入必须**多参数化**（至少覆盖 2-3 组不同前提），禁止测试与被测代码共享同一默认前提——硬编码值在唯一被测前提下"恰好成立"是已实证的盲区模式（实跑教训：断言与配置都默认 A4，切 A5 即错位 39.9mm，参数化后现形）。

### 4. 运行测试

调用方 `$cm-ai` N6 或 `$cm-test` 负责 `test_run/start` 与 `test_run/complete`；
本 Skill 不重复写调用级边界。存在 AI 测试合同时，本 Skill 在每个 blocking case
实际执行前写 `test_run/case_start`，并以 `case_complete` 或 `case_blocked` 唯一
收口；每次真实重试携带递增 `attempt`。仅当本轮存在 CM specs 时才在关键阶段同步
更新 `.cm-status.json`，standalone `$cm-test` 不创建该文件，也不使用后台心跳。

```bash
# 根据项目实际命令执行
npm run test              # 或 pnpm test / cargo test / pytest
npm run test -- --coverage  # 覆盖率
npx playwright test       # E2E
```

收集：通过数/失败数/覆盖率。

有 test-cases.json 时，正式命令证据与用例逐条关联；不能用静态 logic
`SUPPORTED` 计入命令通过数。

### 5. 可视化回归（如涉及 UI）

1. 识别交付形态并启动正式测试载体：Web 启动开发服务器；微信小程序执行正式构建并
   打开微信开发者工具。小程序同时读取
   `../cm-miniprogram-engineer/references/release-checklist.md`，不得用 H5/Web target
   冒充小程序运行结果。
2. Web 选择浏览器驱动（按优先级）：
   - **检查项目配置**：如 `.claude/rules/testing.md` 中指定了 `browser_driver`，使用用户指定的方式
   - **默认：Playwright CDP（无头模式）** — 不弹窗，适合截图对比、DOM 断言、样式回归等大多数场景
   - **自动升级：Chrome DevTools MCP** — 当检测到以下场景时切换：需要登录态/Cookie 持久化、OAuth/第三方弹窗交互、需要观察真实动画/过渡效果、用户明确要求实时调试
   - 切换前输出：`🔄 切换到 Chrome DevTools MCP — 原因: {原因}，浏览器窗口将弹出`
   微信小程序不进入此浏览器驱动分支：基础交互走开发者工具模拟器，授权、设备差异和
   平台 API 走预览/体验版真机；工具或账号不可用时对应 blocking case 为 `BLOCKED`。
3. 截图保存
4. 对比基准截图（如有）
5. test-cases.json 中的 browser cases 逐条执行 steps、断言 expected，并记录
   `PASS | FAIL | BLOCKED`；cleanup 失败时记 `BLOCKED`
6. 临时 profile、进程、模型别名或 fixture 使用前写 `resource/acquired`，清理后
   用同一 `resource_id` 写 `resource/released`；每次新获取生成新的 ID，释放后的
   ID 不复用。写入 `cleanup_failed` 后保持 `BLOCKED`，不得把断言通过当作整个用例通过

> **用户覆盖**：在 `.claude/rules/testing.md` 中添加 `browser_driver: playwright | chrome-mcp | ask` 可固定选择或设为每次询问。

### 6. 验收标准核验

逐条检查 requirements.md 中的验收标准：

```markdown
- [x] [AC-001] 描述 → 已通过测试验证
- [ ] [AC-002] 描述 → ⚠️ 需手动验证
```

标注每条的验证方式（自动/手动/无法自动化）。

implementation 模式的核验结果必须回写 requirements.md 的验收标准 checkbox
（`[x] [AC-001] → 已通过测试验证`）。readonly 模式只写测试报告，不改
requirements.md。

### 7. 处理失败

- 测试失败 → 判断是代码 bug、测试问题还是环境阻塞
- implementation：代码 bug 汇报主 agent，测试问题可修复后重跑，最多 3 轮
- readonly：保留原始失败，只报告给 `$cm-test`；不得修测试或代码，不自动调用
  `$cm-fix`

## 常见坑

| 问题                     | 处理                                   |
| ------------------------ | -------------------------------------- |
| 测试环境和开发环境不一致 | 检查 test 配置中的环境变量和 mock 设置 |
| 异步测试超时             | 增加 timeout，检查是否缺少 await       |
| E2E 测试不稳定（flaky）  | 用 `waitFor` 代替固定延时，重试机制    |
| 覆盖率统计不准           | 检查 coverage 配置的 include/exclude   |

## 输出

```text
📋 QA 报告

测试: {N} 通过 / {N} 失败 / 覆盖率 {N}%
E2E: {状态}
AI 测试合同: logic {N}/{N} 已核验 · browser {N}/{N} 已执行
验收标准: {N}/{total} 通过, {N} 需手动验证
安全扫描: {状态}
结论: {PASSED / FAILED / NEEDS_MANUAL}
```
