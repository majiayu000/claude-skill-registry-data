---
name: l-license
description: "授权/激活机制、客户端判断与服务器授权边界分析"
---

# l-license Local Entry

Scope: cracking / bypassing activation / removing verification / license keys / keygen (local exe/apk/file). This skill is a local routing entry; the detailed capabilities live in local modules.

## Selection Rules (avoid mis-picking)
1. First read the "Module List" below.
2. Scan the "Module List" below **top to bottom**; use the first one that matches the current task.
   When multiple capabilities are needed, stack at most 3, with entries higher up taking priority.
3. Read the selected local module from `../<MODULE_ID>/SKILL.md`, then apply its task guidance.
4. When none matches exactly, fall through to the "Fallback" at the bottom of this page.

## Module List (ordered by priority)

- `reverse-engineering` — Reverse-engineering master guide: format identification, protection analysis, evidence-driven progress.
- `reverse_flow_skill` — Reversing workflow skill: the full sample-to-report reversing workflow.
- `dotnet-reverse` — .NET reversing: dnSpy/ILSpy decompilation and debugging.
- `apk-reverse` — Android APK reversing: jadx/apktool decompilation, smali edits, Frida dynamic hooking.
- `binary-diff` — Binary diffing: compare two versions to find patched changes.
- `patch-diff-exploit` — Patch diffing and exploitation: infer exploitable points from a patch.
- `protocol-reverse` — Protocol reversing: recover the format of a proprietary communication protocol.
- `js-reverse` — JS reversing: deobfuscation, locating encryption algorithms.
- `mobile-reverse` — Mobile reversing: shared iOS/Android reversing workflow.
- `thick-client` — Thick-client security: desktop app local storage, communication, and trust-boundary testing.
- `browser-extension-reverse` — Browser-extension reversing: analyze an extension's manifest, background scripts, and logic.
- `code-audit` — Code audit: source-level security vulnerability review.

## Fallback
When no listed method matches, return to the installed edition's local directory and choose a relevant available module.

## 本版可用模块

| 模块 | 用途 | 正文 |
| --- | --- | --- |
| `reverse-engineering` | 分析 PE/ELF、壳、混淆、加载器或配置恢复 | [读取](../reverse-engineering/SKILL.md) |
| `reverse_flow_skill` | 需要从样本识别、静态分析到验证和报告的完整逆向流程 | [读取](../reverse_flow_skill/SKILL.md) |
| `dotnet-reverse` | 分析托管程序集、IL、资源、混淆和托管/native 交互 | [读取](../dotnet-reverse/SKILL.md) |
| `apk-reverse` | 分析 APK、DEX、Smali、Android 组件与 JNI 边界 | [读取](../apk-reverse/SKILL.md) |
| `binary-diff` | 比较两个版本的二进制并定位行为变化 | [读取](../binary-diff/SKILL.md) |
| `patch-diff-exploit` | 通过补丁差分理解漏洞根因和修复完整性 | [读取](../patch-diff-exploit/SKILL.md) |
| `protocol-reverse` | 从实现或样本流量还原消息帧、字段和状态机 | [读取](../protocol-reverse/SKILL.md) |
| `js-reverse` | 理解压缩 JS、Webpack、签名算法、混淆代码或 WASM 模块 | [读取](../js-reverse/SKILL.md) |
| `mobile-reverse` | 分析 iOS/IPA 或跨平台移动客户端、存储与运行时边界 | [读取](../mobile-reverse/SKILL.md) |
| `thick-client` | 检查桌面应用、本地存储、更新与进程间信任边界 | [读取](../thick-client/SKILL.md) |
| `browser-extension-reverse` | 分析 CRX/扩展权限、内容脚本、后台与页面桥接 | [读取](../browser-extension-reverse/SKILL.md) |
| `code-audit` | 对指定代码路径检查正确性、权限、数据处理与实际缺陷 | [读取](../code-audit/SKILL.md) |
