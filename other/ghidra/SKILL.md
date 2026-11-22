---
name: "ghidra"
description: ">"
---

# Ghidra

*Sourced from killvxk-malskills-zh*

# Ghidra

NSA 开源逆向工程 (RE) 套件 — 反汇编器 + 反编译器 + 脚本，用于静态分析。

## 快速开始

1. 从 ghidra-sre.org 下载
2. `./ghidraRun`（Linux/macOS）或 `ghidraRun.bat`（Windows）
3. 新建项目 → 导入文件 → 目标二进制文件
4. 双击打开 CodeBrowser → 分析（自动分析）

## 关键窗口

| 窗口 | 用途 |
|--------|---------|
| Symbol Tree | 函数、标签、导入表 |
| Decompiler | 所选函数的 C 伪代码 |
| Listing | 汇编视图 |
| Data Type Manager | 结构体/枚举定义 |
| Program Trees | 段/节 |
| References | 交叉引用（到/来自） |

## 常用分析任务

**查找感兴趣的函数：**
```
Search > For Strings → 搜索 "password"、"exec"、"http"
Window > Symbol Tree > Functions → 按名称过滤
```

**重命名与注释：**
```
右键点击函数 → Edit Function → 重命名
右键点击变量 → Rename Variable
```

**脚本（Python/Java）：**
```python
# Script Manager > New Script (Python)
from ghidra.program.flatapi import FlatProgramAPI
api = FlatProgramAPI(currentProgram)
funcs = list(api.getFunctions(True))
print([f.getName() for f in funcs[:10]])
```

## 常用工作流

**恶意软件静态分析：**
1. 导入样本 → 自动分析
2. Symbol Tree → Imports：检查可疑 API（VirtualAlloc、CreateRemoteThread）
3. 反编译每个可疑函数

**查找硬编码凭据：**
```
Search > For Strings → password/key/secret
双击结果 → 反编译周围函数
```

## 资源

| 文件 | 何时加载 |
|------|--------------|
| `references/` | 脚本示例和结构体恢复技巧 |

