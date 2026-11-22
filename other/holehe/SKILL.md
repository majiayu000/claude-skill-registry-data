---
name: "holehe"
description: ">"
---

# Holehe

*Sourced from killvxk-malskills-zh*

# Holehe

邮箱账号映射工具 — 检查邮箱是否在 120+ 个服务中注册。

## 快速开始

```bash
pip install holehe

# 检查单个邮箱
holehe target@gmail.com

# 仅输出已注册的站点
holehe target@gmail.com --only-used

# JSON 输出
holehe target@gmail.com --only-used --json > results.json
```

## 核心参数

| 参数 | 用途 |
|------|------|
| `--only-used` | 仅显示邮箱已注册的站点 |
| `--no-color` | 禁用颜色输出 |
| `--json` | JSON 输出 |
| `-T N` | 每个请求的超时时间 |

## 检查的站点（示例）

`Google` · `Twitter/X` · `GitHub` · `Instagram` · `LinkedIn` · `Reddit` · `Snapchat` · `Spotify` · `Adobe` · `Airbnb` · `Amazon` · `Dropbox` · `Flickr` · `Pinterest` · `Tumblr` + 100 余个

## 常用工作流

**对目标邮箱进行 OSINT：**
```bash
holehe ceo@targetcompany.com --only-used --json | tee email_presence.json
```

**从文件批量检查：**
```bash
cat emails.txt | xargs -I {} holehe {} --only-used
```

## 参考资源

| 文件 | 加载时机 |
|------|----------|
| `references/` | 结果解读和账号接管路径 |

