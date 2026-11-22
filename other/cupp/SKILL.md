---
name: "cupp"
description: ">"
---

# Cupp

*Sourced from killvxk-malskills-zh*

# CUPP

自定义用户密码画像工具——从个人 OSINT 数据生成定向字典。

## 快速开始

```bash
# Interactive profile mode
python3 cupp.py -i

# Download predefined wordlists
python3 cupp.py -l

# Show all options
python3 cupp.py -h
```

## 核心参数

| 参数 | 描述 |
|------|-------------|
| `-i` | 交互模式——提示输入目标信息 |
| `-w <file>` | 使用 leet-speak + 特殊字符增强现有字典 |
| `-l` | 从仓库下载字典 |
| `-a` | 从 Alecto DB 解析默认用户名 |
| `-v` | 详细输出 |

## 交互式画像字段

运行 `-i` 时，CUPP 会询问：

```
Name, surname, nickname
Birthdate (DDMMYYYY)
Partner name, nickname, birthdate
Child name, nickname, birthdate
Pet name
Company name
Keywords (e.g., favorite team, car, city)
Special chars to append? [y/N]
Random numbers to append? [y/N]
Leet mode? [y/N]
```

## CUPP 生成内容

根据提供的数据，CUPP 创建以下排列组合：
- 姓名 + 出生年份：`john1990`、`John1990!`
- 反转 + 数字：`nhoj123`
- 组合姓名：`johnjane`、`jane&john`
- Leet 替换：`j0hn`、`p@ssword`
- 大小写变体：`JOHN`、`John`
- 附加特殊字符：`john!`、`john@`、`john#`
- 日期组合：`01011990`、`john1990!`

## 常见工作流程

```bash
# Build a targeted wordlist interactively
python3 cupp.py -i
# Output: john.txt (or custom name)

# Use the generated list with Hydra
hydra -l john.doe@company.com -P john.txt smtp://mail.company.com

# Use with Hashcat
hashcat -a 0 -m 1000 hashes.txt john.txt

# Augment an existing wordlist with cupp transformations
python3 cupp.py -w existing_list.txt

# Combine with Hashcat rules for more coverage
hashcat -a 0 -m 0 hash.txt john.txt -r /usr/share/hashcat/rules/best64.rule
```

## 画像用 OSINT 来源

- LinkedIn（姓名、公司、职位、日期）
- Facebook / Instagram（人际关系、生日、宠物）
- Twitter/X（兴趣、昵称、关键词）
- 公司网站（员工姓名、产品）
- HaveIBeenPwned（泄露密码作为基准）

## 参考资源

| 文件 | 加载时机 |
|------|--------------|
| `references/wordlist-strategy.md` | OSINT 收集工作流、结合规则使用、字典扩展技术 |

