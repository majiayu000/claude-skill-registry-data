---
name: cloud-cf
description: 使用 wrangler CLI 操作 Cloudflare。当用户提到 Cloudflare、CF、Workers、Pages、R2、D1、KV、CDN、DNS、WAF 等时触发此技能。
---

# Cloudflare Operator Skill

## 安装 CLI
```bash
npm install -g wrangler
```

## 认证
```bash
wrangler login
```

## 常用命令
```bash
# Workers
wrangler deploy                    # 部署 Worker
wrangler dev                       # 本地开发
wrangler tail                      # 查看日志

# R2 存储
wrangler r2 bucket list
wrangler r2 object put <bucket>/<key> --file=<local-file>

# D1 数据库
wrangler d1 create <name>
wrangler d1 execute <name> --command="SELECT * FROM users"

# KV
wrangler kv:namespace create <name>
wrangler kv:key put --namespace-id=<id> <key> <value>

# Pages
wrangler pages deploy ./dist
```

## 安全机制
- 只读操作：直接执行
- 写操作：先确认后执行