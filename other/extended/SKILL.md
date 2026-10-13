---
name: pojia-local
description: "按任务选择逆向、安全与工程技能模块。"
---

# 扩展技能库

用户发送 `hi` 时，报告已读取本地技能目录，说明具体领域正文按任务加载。

## 选择技能

按目标格式和要完成的任务选择下表的入口或模块。只读取与当前任务相关的正文，不默认加载整个库。
库文件位于本指令文件所在客户端目录的 `skills/<名称>/SKILL.md`；如果相对路径不明确，使用客户端配置目录定位。

| 名称 | 技能用途 | 相邻目录中的正文 |
| --- | --- | --- |
| `api-security` | API 安全审查 | [正文](../api-security/SKILL.md) |
| `apk-reverse` | Android APK 逆向 | [正文](../apk-reverse/SKILL.md) |
| `attack-chain` | 多阶段安全验证 | [正文](../attack-chain/SKILL.md) |
| `binary-diff` | 二进制版本差分 | [正文](../binary-diff/SKILL.md) |
| `browser-automation` | 浏览器自动化 | [正文](../browser-automation/SKILL.md) |
| `browser-extension-reverse` | 浏览器扩展逆向 | [正文](../browser-extension-reverse/SKILL.md) |
| `build-release` | 构建与发布制品 | [正文](../build-release/SKILL.md) |
| `cloud-k8s` | 云与 Kubernetes 配置审查 | [正文](../cloud-k8s/SKILL.md) |
| `code-audit` | 代码审计 | [正文](../code-audit/SKILL.md) |
| `container-runtime` | 容器运行时诊断 | [正文](../container-runtime/SKILL.md) |
| `database-security` | 数据库安全 | [正文](../database-security/SKILL.md) |
| `deploy-infra` | 部署与基础设施 | [正文](../deploy-infra/SKILL.md) |
| `digital-forensics` | 数字取证 | [正文](../digital-forensics/SKILL.md) |
| `dotnet-reverse` | .NET 逆向 | [正文](../dotnet-reverse/SKILL.md) |
| `edr-bypass-re` | 终端防护边界分析 | [正文](../edr-bypass-re/SKILL.md) |
| `email-security` | 邮件安全 | [正文](../email-security/SKILL.md) |
| `firmware-pentest` | 固件与 IoT 分析 | [正文](../firmware-pentest/SKILL.md) |
| `game-hacking` | 游戏程序分析与离线调试 | [正文](../game-hacking/SKILL.md) |
| `ghidra-reverse` | Ghidra 逆向 | [正文](../ghidra-reverse/SKILL.md) |
| `go-rust-reverse` | Go 与 Rust 二进制逆向 | [正文](../go-rust-reverse/SKILL.md) |
| `hardware-security` | 硬件接口分析 | [正文](../hardware-security/SKILL.md) |
| `ida-reverse` | IDA 静态分析 | [正文](../ida-reverse/SKILL.md) |
| `identity-federation` | 身份联邦审查 | [正文](../identity-federation/SKILL.md) |
| `js-reverse` | JavaScript 与 WASM 逆向 | [正文](../js-reverse/SKILL.md) |
| `l-gameassist` | 游戏辅助分析入口 | [正文](../l-gameassist/SKILL.md) |
| `l-license` | 授权与激活分析入口 | [正文](../l-license/SKILL.md) |
| `l-reverse` | 逆向分析入口 | [正文](../l-reverse/SKILL.md) |
| `l-webrecon` | Web 与安全测试入口 | [正文](../l-webrecon/SKILL.md) |
| `llm-security` | LLM 应用安全 | [正文](../llm-security/SKILL.md) |
| `macos-reverse` | macOS 与 Mach-O 逆向 | [正文](../macos-reverse/SKILL.md) |
| `malware-analysis` | 恶意样本分析 | [正文](../malware-analysis/SKILL.md) |
| `mobile-reverse` | 移动端逆向 | [正文](../mobile-reverse/SKILL.md) |
| `network-analysis` | 网络流量分析 | [正文](../network-analysis/SKILL.md) |
| `ot-ics` | 工控系统分析 | [正文](../ot-ics/SKILL.md) |
| `patch-diff-exploit` | 补丁差分与漏洞回归 | [正文](../patch-diff-exploit/SKILL.md) |
| `patch-rollback` | 补丁与回滚 | [正文](../patch-rollback/SKILL.md) |
| `pentest-tools` | 安全测试工具流程 | [正文](../pentest-tools/SKILL.md) |
| `pentest-tools__src-hunter` | 源码线索定位 | [正文](../pentest-tools__src-hunter/SKILL.md) |
| `protocol-reverse` | 协议逆向 | [正文](../protocol-reverse/SKILL.md) |
| `pwn-chain` | 内存安全根因分析 | [正文](../pwn-chain/SKILL.md) |
| `radare2` | radare2 分析 | [正文](../radare2/SKILL.md) |
| `radio-sdr` | SDR 与射频分析 | [正文](../radio-sdr/SKILL.md) |
| `reverse-engineering` | 通用逆向分析 | [正文](../reverse-engineering/SKILL.md) |
| `reverse_flow_skill` | 逆向全流程 | [正文](../reverse_flow_skill/SKILL.md) |
| `supply-chain-security` | 软件供应链审查 | [正文](../supply-chain-security/SKILL.md) |
| `thick-client` | 桌面客户端分析 | [正文](../thick-client/SKILL.md) |
| `threat-hunting` | 威胁狩猎与检测 | [正文](../threat-hunting/SKILL.md) |
| `websocket-runtime` | 实时连接诊断 | [正文](../websocket-runtime/SKILL.md) |
| `wifi-wireless` | 无线网络安全 | [正文](../wifi-wireless/SKILL.md) |
| `windows-ad` | Windows 域身份审查 | [正文](../windows-ad/SKILL.md) |

## 使用原则

工具、脚本与附件需按实际运行环境核对。
遵循用户任务范围与当前工程约定。基于实际文件和运行结果报告，不把技能文件存在当成模型已实际使用。
