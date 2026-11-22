---
name: "shodan"
description: ">"
---

# Shodan

*Sourced from killvxk-malskills-zh*

# Shodan CLI

通过 Shodan 进行被动侦察 — 无需接触目标即可发现互联网范围内的主机/服务。

## 快速开始

```bash
# 使用 API 密钥初始化
shodan init YOUR_API_KEY

# 搜索服务/banner
shodan search "apache 2.4.49"

# 主机查询
shodan host 203.0.113.10

# 账户信息/余量
shodan info
```

## 核心命令

| 命令 | 说明 |
|------|------|
| `shodan search <query>` | 搜索 Shodan 索引 |
| `shodan host <ip>` | 详细主机信息（开放端口、banner、漏洞） |
| `shodan count <query>` | 统计结果数量（不消耗查询积分） |
| `shodan download <file> <query>` | 下载结果为压缩 JSON |
| `shodan parse <file>` | 解析已下载的结果 |
| `shodan domain <domain>` | 域名情报 |
| `shodan alert` | 管理监控告警 |
| `shodan stats <query>` | 查询结果统计 |
| `shodan honeyscore <ip>` | 蜜罐评分（0-1） |
| `shodan myip` | 查看本机公网 IP |

## 搜索过滤器

| 过滤器 | 示例 |
|--------|------|
| `hostname:` | `hostname:example.com` |
| `ip:` | `ip:1.2.3.0/24` |
| `org:` | `org:"Target Corp"` |
| `port:` | `port:8080` |
| `product:` | `product:Apache` |
| `version:` | `version:2.4.49` |
| `country:` | `country:IT` |
| `os:` | `os:Windows` |
| `vuln:` | `vuln:CVE-2021-44228` |
| `http.title:` | `http.title:"Login"` |
| `html:` | `html:"admin panel"` |
| `ssl:` | `ssl:"example.com"` |
| `asn:` | `asn:AS12345` |
| `net:` | `net:192.168.0.0/16` |

## 常用工作流

```bash
# 查找某组织的基础设施
shodan search org:"Target Corp" --fields ip_str,port,product

# 下载并解析组织结果
shodan download results.json.gz org:"Target Corp"
shodan parse --fields ip_str,port,product results.json.gz

# 查找暴露的登录面板
shodan search http.title:"administration" org:"Target"

# 基于 CVE 的研究
shodan search vuln:CVE-2021-44228

# SSL 证书横向关联 — 查找共享同一证书的所有主机
shodan search ssl:"example.com"

# 统计结果（不消耗查询积分）
shodan count org:"Target Corp"

# 反向查询/主机详情
shodan host 8.8.8.8
```

## 资源文件

| 文件 | 加载时机 |
|------|----------|
| `references/search-filters.md` | 完整过滤器参考、dork 配方及 API 集成示例 |

