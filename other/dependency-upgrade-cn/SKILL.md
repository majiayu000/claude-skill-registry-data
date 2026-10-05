---
name: dependency-upgrade-cn
description: Use when planning, reviewing, or implementing dependency upgrades in Chinese open-source projects, including risk assessment, changelog review, lockfile changes, tests, and maintainer release notes.
---

# Dependency Upgrade CN

用在开源维护者需要升级依赖、审查依赖升级 PR、处理 Dependabot/Renovate 提交或准备版本兼容说明时。目标是让依赖升级可控、可验证、可回滚。

## 适用场景

- 用户说“升级依赖”“看这个 Dependabot PR”“Renovate 提了一个版本升级”。
- 需要判断 patch/minor/major upgrade 的风险。
- 需要阅读 changelog、migration guide、release notes 或 breaking changes。
- 需要给贡献者写中文维护者回复或合并建议。

## 不适用场景

- 用户只想安装一个全新依赖，且没有升级上下文。
- 升级涉及生产数据库、支付、认证或安全边界，但没有测试和回滚方案。
- 用户要求忽略 failing tests 直接合并。

## 工作流

1. 明确升级范围。
   - 记录包名、当前版本、目标版本、包管理器、lockfile 和相关 PR。
   - 区分 direct dependency 与 transitive dependency。

2. 查变更风险。
   - 优先查看官方 changelog、release notes、migration guide、security advisory。
   - 标出 breaking changes、deprecated APIs、runtime/Node/Python/OS version 要求。
   - 如果无法联网，明确说明只能基于本地 diff 和测试判断。

3. 检查仓库影响面。
   - 搜索依赖 import、配置、插件、CLI、类型定义和测试 fixture。
   - 注意 lockfile 变化是否异常扩大。
   - 对 major upgrade，检查配置文件和迁移步骤。

4. 制定验证计划。
   - 先跑最小相关测试，再跑 typecheck/lint/build。
   - 对工具链依赖，验证本地命令是否仍可执行。
   - 对运行时依赖，至少覆盖一个真实调用路径。

5. 输出合并建议。
   - 可合并：说明验证证据和剩余风险。
   - 需修改：指出具体失败和建议。
   - 暂缓：说明阻塞原因、缺失信息或上游风险。

## 输出格式

```text
升级对象：
- package：
- from -> to：
- 类型：patch / minor / major / security

风险判断：
- ...

影响面：
- ...

验证：
- 已运行：
- 未运行：

建议：
- merge / request changes / hold

维护者回复：
...
```

## 验证方式

- 依赖升级必须至少有一种验证证据：测试、构建、类型检查、lint、手动 smoke test。
- 如果只改 lockfile，仍需检查 lockfile diff 是否合理。
- 对安全升级，说明是否仍需 backport 或 release。

## 安全边界

- 不要建议关闭安全检查来通过 CI。
- 不要把 advisory 中未公开的漏洞利用细节写进公开回复。
- 不要在缺少验证时把 major upgrade 说成低风险。
