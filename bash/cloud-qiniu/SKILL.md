---
name: cloud-qiniu
description: 使用 qshell CLI 操作七牛云。当用户提到七牛、七牛云、Qiniu、Kodo、七牛对象存储 等时触发此技能。
---

# 七牛云 Operator Skill

## 安装 CLI
```bash
# macOS
brew install qiniu

# 或手动下载
curl -o qshell https://developer.qiniu.com/kodo/tools/3829/qshell
chmod +x qshell
```

## 认证
```bash
qshell account <AccessKey> <SecretKey> <Name>
```

## 常用命令
```bash
# 存储桶
qshell listbucket <bucket>
qshell buckets

# 上传下载
qshell fput <bucket> <key> <localfile>
qshell get <bucket> <key> -o <outputfile>
qshell qupload <upload-config.json>

# 批量操作
qshell batchdelete <bucket> -i <key-list-file>
qshell batchchtype <bucket> -i <key-list-file> -t <mimetype>

# CDN
qshell cdnrefresh -i <url-list-file>
qshell cdnprefetch -i <url-list-file>

# 域名
qshell domains <bucket>
```

## 安全机制
- 只读操作：直接执行
- 写操作：先确认后执行