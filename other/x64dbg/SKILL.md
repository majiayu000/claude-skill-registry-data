---
name: "x64dbg"
description: ">"
---

# X64Dbg

*Sourced from killvxk-malskills-zh*

# x64dbg

用于动态恶意软件分析、脱壳和 API 追踪的 Windows 调试器。

## 快速开始

1. 从 x64dbg.com 下载 → 解压 → 运行 `x96dbg.exe`（启动器自动选择 x32/x64）
2. **文件 > 打开** → 目标可执行文件
3. 设置断点：在指令处按 `F2`，或输入 `bp CreateRemoteThread`
4. **运行**：`F9` | **步过**：`F8` | **步入**：`F7`
5. **插件**：加载 ScyllaHide（反反调试）、xAnalyzer

## 主要面板

| 面板 | 用途 |
|-------|---------|
| CPU | 反汇编 + 寄存器 + 栈 + 十六进制视图 |
| Log | API 调用、插件输出 |
| Breakpoints | 管理所有断点 |
| Memory Map | 虚拟内存区域 |
| References | 选中内容的交叉引用（XREF） |
| Symbols | 模块导入/导出表 |

## 常用命令

| 操作 | 快捷键 / 命令 |
|--------|--------------|
| 运行 / 暂停 | F9 |
| 步过 | F8 |
| 步入 | F7 |
| 执行到返回 | Ctrl+F9 |
| 设置断点 | F2 |
| 在 API 处下断点 | 在命令栏输入 `bp VirtualAlloc` |
| 在转储中跟随 | 在地址处按 Ctrl+D |
| 搜索字符串 | 在反汇编窗口按 Ctrl+F |

## 常用工作流

**恶意软件脱壳：**
1. 打开样本 → 运行至 OEP（解密循环结束后关注 `jmp eax/rax`）
2. 使用 Scylla 插件转储进程 → 修复导入表 → 保存

**定位 C2 回连：**
```
bp WS2_32.connect
bp WS2_32.send
F9 → 检查栈上的参数
```

## 参考资源

| 文件 | 何时加载 |
|------|--------------|
| `references/` | 插件列表及脱壳方法论 |

