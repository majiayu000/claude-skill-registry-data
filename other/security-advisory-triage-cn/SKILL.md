---
name: security-advisory-triage-cn
description: Use when triaging security advisories or vulnerability reports in Chinese OSS projects, including impact assessment, affected versions, responsible disclosure, remediation planning, and safe public communication.
---

# Security Advisory Triage CN

用在开源维护者处理安全公告、漏洞报告、依赖漏洞、GitHub Security Advisory 或疑似安全 issue 时。目标是安全、克制、可追踪地完成 triage 和修复计划。

## 适用场景

- 用户说“这个安全漏洞影响我们吗”“帮我看这个 advisory”“有人报了安全问题”。
- 需要判断受影响版本、攻击前置条件、严重程度和修复优先级。
- 需要准备私密沟通、维护者回复、修复计划或 release note。
- 需要处理依赖安全升级。

## 不适用场景

- 用户要求编写 exploit、绕过权限、扩大攻击细节。
- 漏洞涉及第三方系统且没有授权。
- 用户要求在公开 issue 中披露未修复漏洞细节。

## 工作流

1. 保护信息边界。
   - 判断信息是否应留在私密渠道。
   - 不复述 token、cookie、账号、私有 URL、POC 细节或可直接利用步骤。

2. 收集事实。
   - advisory ID、受影响包/模块、版本范围、修复版本、来源链接。
   - 项目是否使用该依赖或代码路径。
   - 是否暴露到用户输入、网络边界、认证边界或权限边界。

3. 判断影响。
   - 是否可达：代码路径是否真的被调用。
   - 是否可利用：需要什么权限、配置、环境或用户交互。
   - 影响范围：机密性、完整性、可用性、权限提升、数据泄露。

4. 制定响应。
   - 立即缓解：禁用危险功能、限制入口、升级依赖、回滚版本。
   - 修复计划：补丁、测试、release、backport。
   - 沟通计划：私密确认、公开 advisory、release notes。

5. 验证修复。
   - 跑安全相关测试和回归测试。
   - 确认受影响版本和修复版本。
   - 对依赖漏洞，确认 lockfile 和实际安装版本。

## 输出格式

```text
结论：
- 影响：confirmed / likely / unlikely / unknown
- 严重度：critical / high / medium / low / unknown

依据：
- ...

受影响范围：
- package / module：
- versions：
- reachable path：

建议动作：
1. ...
2. ...

公开沟通建议：
- ...

不能公开的信息：
- ...
```

## 验证方式

- 结论必须基于 advisory、代码路径、依赖版本或测试证据。
- 修复后确认 lockfile、运行时版本和相关测试。
- 如果影响未知，明确列出缺失信息，不要强行下结论。

## 安全边界

- 不提供 exploit、绕过步骤或攻击自动化。
- 不公开未修复漏洞的利用细节。
- 不把安全问题当普通 issue 处理；优先建议私密渠道。
