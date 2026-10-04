---
name: pdlc-i18n
description: 国际化（i18n）
argument-hint: <目标语言 | 模块名>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 3
stage: engineering
produces: []
requires: []
next_step: null
terminal_state: null
---

# 国际化（i18n）

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

为指定的前端应用或后端服务添加国际化支持。

## 工作流程
1. **扫描硬编码文本**: 查找代码中所有硬编码的中文字符串
2. **提取文本资源**: 生成多语言资源文件
3. **替换硬编码**: 用 i18n 函数调用替换原有的硬编码文本
4. **生成翻译清单**: 输出待翻译的文本列表

## 前端（React/Vue）
- 资源文件位置: `src/locales/zh-CN.json`、`src/locales/en-US.json`
- 使用 `react-i18next` 或 `vue-i18n`
- Key 命名规范: `模块.页面.组件.描述`，如 `user.login.form.username`

## 后端（Java/Go/Python/Node）
- 错误提示信息国际化
- API 响应消息国际化
- 根据请求头 `Accept-Language` 返回对应语言

## 资源文件格式
```json
{
  "common": {
    "confirm": "确认",
    "cancel": "取消",
    "save": "保存",
    "delete": "删除"
  },
  "user": {
    "login": {
      "title": "用户登录",
      "username": "用户名",
      "password": "密码"
    }
  }
}
```

## 要求
- 默认语言为中文（zh-CN）
- Key 使用英文，值使用对应语言
- 先生成中文版本，英文版本标记 `// TODO: 待翻译`
- 日期、数字、货币使用 Intl API 格式化

目标: $ARGUMENTS

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
✅ 国际化资源文件 完成
📦 产出：src/locales/<语言>.json
👉 下一步：（本次流程结束，无后续）
```
