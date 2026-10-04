---
name: cloud-upyun
description: 使用 upx CLI 操作又拍云。当用户提到又拍云、Upyun、UPYUN、又拍云存储 等时触发此技能。
---

# 又拍云 Operator Skill

## 安装 CLI
```bash
# macOS
brew install upx

# Linux
curl -o upx https://github.com/upyun/upx/releases/latest/download/upx-linux-amd64
chmod +x upx
```

## 认证
```bash
upx login
# 输入服务名、操作员、密码
```

## 常用命令
```bash
# 文件操作
upx ls                          # 列出文件
upx put <localfile> <remotepath>  # 上传
upx get <remotepath> -o <localfile>  # 下载
upx rm <remotepath>             # 删除

# 目录操作
upx mkdir <remotedir>
upx cd <remotedir>

# 批量操作
upx sync <localdir> <remotedir>  # 同步上传

# CDN 刷新
upx purge <url>

# 信息查看
upx info
upx usage                       # 查看用量
```

## 安全机制
- 只读操作：直接执行
- 写操作：先确认后执行