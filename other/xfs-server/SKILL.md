---
name: xfs-server
description: 连接并管理夏凡盛的阿里云服务器（47.115.210.223）。当用户说"帮我管理服务器"、"服务器xxx"、"重启服务"、"查看日志"、"部署项目"、"修改Nginx"、"查看状态"等涉及服务器操作的请求时使用此技能。
---

# 阿里云服务器管理

自动通过 SSH 连接并操作 xfs-server，无需用户手动登录。

## 服务器基本信息

| 项目 | 值 |
|------|-----|
| IP | 47.115.210.223 |
| 用户 | root |
| SSH 别名 | `xfs-server`（已配置免密登录） |
| 系统 | Alibaba Cloud Linux 8 (x86_64) |
| 磁盘 | 49G 总量，~20G 已用 |
| 内存 | 3.5G |

## SSH 连接方式

所有操作通过以下方式执行，无需密码：

```bash
ssh xfs-server "命令"
```

文件读取：
```bash
rclone cat xfs-server:/path/to/file
rclone ls xfs-server:/home/
```

文件上传：
```bash
rclone copy /本地路径 xfs-server:/远程路径
```

## 服务器目录结构

```
/home/
├── xiafansheng-site/          # 个人主页（VitePress 静态站点）
│   └── docs/.vitepress/
│       ├── config.mts         # 站点配置
│       └── dist/              # 构建产物（生产环境）
├── myproject/                 # 个人项目
│   ├── 行业生命周期/           # 行业生命周期分析系统（Flask）
│   └── asset_allocation/      # 多资产配置回测系统
└── admin/                     # 管理员目录
```

## 运行中的服务

| 服务名 | 描述 | 端口 | 配置文件 |
|--------|------|------|---------|
| `xiafansheng-site.service` | 个人主页静态服务 | 3000 | `/etc/systemd/system/xiafansheng-site.service` |
| `lifecycle.service` | 行业生命周期分析系统（Flask） | 8081 | `/etc/systemd/system/lifecycle.service` |
| `nginx.service` | 反向代理 | 80/443 | `/etc/nginx/conf.d/` |
| `docker.service` | Docker 容器引擎 | — | — |

## Nginx 配置

配置文件目录：`/etc/nginx/conf.d/`

当前虚拟主机：
- `xiafansheng.conf` → `xiafansheng.com` → 代理到 localhost:3000（主站）
- `lifecycle.conf` → `lifecycle.xiafansheng.com` → 代理到 localhost:8081

SSL 证书（Let's Encrypt）：
- `/etc/letsencrypt/live/xiafansheng.com/` — 已配置，自动续期

## 常用操作命令

### 查看状态
```bash
ssh xfs-server "systemctl status lifecycle"
ssh xfs-server "systemctl list-units --type=service --state=running --no-pager"
ssh xfs-server "df -h / && free -h"
ssh xfs-server "ss -tlnp | grep LISTEN"
```

### 服务管理
```bash
ssh xfs-server "systemctl restart lifecycle"
ssh xfs-server "systemctl restart xiafansheng-site"
ssh xfs-server "systemctl restart nginx"
ssh xfs-server "nginx -t && nginx -s reload"   # 只重载配置，不重启
```

### 查看日志
```bash
ssh xfs-server "journalctl -u lifecycle -n 50"         # 最近50行
ssh xfs-server "journalctl -u lifecycle --since '10 min ago'"
ssh xfs-server "tail -100 /var/log/nginx/error.log"
ssh xfs-server "tail -100 /var/log/nginx/access.log"
```

### 部署主站
```bash
# 在服务器上重新构建 VitePress
ssh xfs-server "cd /home/xiafansheng-site && npm run docs:build"
```

### 新增项目（模板）
```bash
# 1. 创建 systemd 服务
ssh xfs-server "cat > /etc/systemd/system/新项目.service << 'EOF'
[Unit]
Description=新项目描述
After=network.target

[Service]
Type=simple
User=admin
WorkingDirectory=/home/myproject/新项目
Environment=\"PORT=808X\"
ExecStart=/usr/local/bin/python3.10 /home/myproject/新项目/app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF"

# 2. 启动服务
ssh xfs-server "systemctl daemon-reload && systemctl enable --now 新项目"

# 3. 添加 Nginx 子域名配置
ssh xfs-server "cat > /etc/nginx/conf.d/新项目.conf << 'EOF'
server {
    listen 80;
    server_name 新项目.xiafansheng.com;
    location / {
        proxy_pass http://localhost:808X;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF"

# 4. 重载 Nginx
ssh xfs-server "nginx -t && nginx -s reload"

# 5. 申请 SSL（DNS 配好后执行）
ssh xfs-server "certbot --nginx -d 新项目.xiafansheng.com --non-interactive --agree-tos -m xiafansheng9619@gmail.com"
```

## 执行流程

收到服务器相关请求时：

1. **先确认意图**：明确用户要做什么（查看/修改/重启/部署）
2. **执行操作**：用 `ssh xfs-server "命令"` 直接操作
3. **验证结果**：执行后检查服务状态或返回值，确认成功
4. **报告结果**：简洁告知用户操作结果

## 注意事项

- Flask 项目目前运行 `debug=True`，生产环境建议改为 gunicorn（可按需升级）
- `lifecycle.xiafansheng.com` 子域名需要在阿里云 DNS 控制台添加 A 记录指向 `47.115.210.223`
- 阿里云安全组需要放行端口：22（SSH）、80（HTTP）、443（HTTPS）、8081（lifecycle 直连）
- 服务器密码建议尽快修改：`ssh xfs-server "passwd root"`
