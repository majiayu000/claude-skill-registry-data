---
name: pdlc-security
description: 安全审计
argument-hint: <模块 | 服务名>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 3
stage: quality
produces:
  - docs/04_testing/security/<feature-id>-audit.md
requires: []
next_step: null
terminal_state: null
---

# 安全审计

<!-- @include templates/prompts/iron-law.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁**

以下规则为**不可协商**的执行约束：

1. **文件必须落盘**：所有带编号（功能ID / 缺陷ID）的文档，必须作为实际文件写入磁盘，不可仅在对话中输出。
2. **阶段必须落章**：每个阶段完成后必须在状态机 `docs/.pdlc-state/<feature-id>.json` 追加 history，不可跳过。
3. **测试必须存在**：进入 `/pdlc-implement` 前，对应测试必须存在且处于红灯状态。违反则中止。
4. **自检必须执行**：段二自检为强制步骤，不得以"已经很好了"为由跳过。
5. **防循环**：段三修复为单次，不递归。无法自动修复的问题记录到报告，继续往下走。
6. **状态必推进**：成功执行某 phase 后 `current_stage` 必须变更。收尾时若发现 `current_stage` 未推进，视为失败并报错，**不得静默返回**（防止外层循环拿滞后的状态空转烧额度）。唯一例外：命中人工点主动 block 时，`current_stage` 保持不变但必须写 `last_phase_result.ok=false` + `blocked_reason`。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law.md -->

对指定服务或应用进行安全审计，检查常见安全漏洞。

## 审计范围
1. **OWASP Top 10 检查**
   - SQL 注入
   - XSS（跨站脚本）
   - CSRF（跨站请求伪造）
   - 不安全的直接对象引用
   - 安全配置错误
   - 敏感数据泄露
   - 缺失的访问控制
   - 不安全的反序列化
   - 使用含已知漏洞的组件
   - 日志记录和监控不足

2. **认证与授权**
   - 密码存储方式（是否加盐哈希）
   - Token 生成与验证
   - 接口权限控制
   - 会话管理

3. **数据安全**
   - 敏感信息是否加密存储
   - 环境变量中是否有硬编码密钥
   - 日志中是否打印敏感数据
   - API 响应中是否泄露内部信息

4. **依赖安全**
   - 检查依赖包是否有已知漏洞
   - 检查是否使用了过时的库版本

## 输出格式

> ⚠️ **必须创建文件，不可仅在对话中输出。**

**【必须创建文件】** 在 `docs/07_reviews/code/` 下创建安全审计报告：
- 文件名: `YYYYMMDD-<服务名>-security-audit.md`
- **文档顶部包含 PDLC 追溯头**：
  ```
  <!-- PDLC-TRACE -->
  <!-- 功能名称: <服务名> -->
  <!-- 阶段: 安全审计 -->
  <!-- 创建时间: <ISO 8601> -->
  ```
- 按严重程度分级：紧急 / 高危 / 中危 / 低危 / 信息
- 每个问题包含：位置、描述、风险、修复建议、参考链接
- **创建后验证**：确认文件已存在于 `docs/07_reviews/code/` 目录
- 在对话中输出报告摘要，但**完整报告必须在文件中**

## 要求
<!-- @include templates/prompts/output-language.md（已内联于下方，无需另读） -->
🌐 **Output language for generated artifacts**

All generated artifacts (PRDs, design docs, code comments, review reports,
test plans, deployment manuals, changelog entries, etc.) follow this policy:

1. **Default — match the conversation language exactly**:
   - 用户用中文与 Claude 对话 → 产中文文档、中文代码注释、中文报告
   - User talks to Claude in English → produce English artifacts
   - User talks in another language → produce artifacts in that language
   - **Never silently default to a fixed language regardless of the user's input.**

2. **Explicit override always wins**: when the user specifies a language for
   an artifact (e.g. "write the PRD in English", "用英文写 API 设计文档",
   "output the deploy doc in Japanese"), use that language for that artifact,
   regardless of conversation language.

3. **Mixed-language requirements**: if the user wants some artifacts in one
   language and others in a different language (common: Chinese PRD + English
   API docs for partners), honour each per-artifact instruction.

4. **Uncertain**: if you cannot reliably detect the conversation language,
   ask once before producing the first artifact.

This policy applies to **content** (prose, comments, headings). It does
**not** override technical conventions like English variable names, English
git commit subjects, or English error codes when the project's conventions
require them.
<!-- @include-end templates/prompts/output-language.md -->
- 给出具体的代码位置和修复代码示例
- 关键漏洞标注修复优先级

审计目标: $ARGUMENTS

<!-- @include templates/prompts/handoff.md（已内联于下方，无需另读） -->
## 段四：交接（Handoff）

命令完成后必须输出以下格式的最终消息：

```
✅ <阶段名> 完成：<主要产出物路径>
📊 自检：<通过数>/<总数> 通过（若有未通过，附要点）
📦 状态快照：docs/.pdlc-state/<feature-id>.json
👉 下一步：/pdlc-<next_step>
   （如果有分叉）或 /pdlc-<alt>（条件：<选择依据>）
```

**规则：**
- 主流程命令（写状态机的命令；下一跳见正文里「本命令的状态机取值」）必须显式输出"下一步"，不可省略
- 工具型命令（Layer 3）可以没有 `next_step`，此时输出 `👉 下一步：（本次流程结束，无后续）`
- 分叉场景必须说明**选择条件**，例如"若需补充测试用例 → `/pdlc-tdd`；若测试已齐 → `/pdlc-review`"
<!-- @include-end templates/prompts/handoff.md -->

**本命令的 handoff 输出：**

```
✅ 安全审计报告 完成
📦 产出：docs/04_testing/security/<feature-id>-audit.md
👉 下一步：（本次流程结束，无后续）
```
