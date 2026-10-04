---
name: xiaohongshu
description: 小红书内容发布与管理 - 发帖、搜索、评论、获取推荐等操作
version: 1.2.0
author: openclaw-community
metadata: {"openclaw": {"emoji": "📕", "category": "social-media", "tags": ["小红书", "社交媒体", "内容发布", "种草"]}}
---

# 📕 小红书 

当用户要求操作小红书（发帖、搜索、获取推荐、评论等）时，使用此技能。

**重要**：
- 所有命令都在**云服务器本地**执行，MCP 服务运行在 `http://localhost:18060/mcp`。

## 使用流程（每次操作小红书前必须按此顺序执行）

### 第 1 步：前置检查

```bash
bash {baseDir}/check_env.sh
```

**返回码**：
- `0` = 一切正常，已登录 → 跳到"调用工具"
- `1` = MCP 未安装或服务启动失败 → 执行"安装 MCP 服务"
- `2` = 未登录，需要扫码 → 执行"未登录时自动获取二维码流程"

### 第 2 步：调用工具

**⚠️ 极其重要**：小红书 MCP 使用 Streamable HTTP 模式。每次调用都必须：初始化 → 获取 Session ID → 带 Session ID 调用工具。三步在同一个 exec 中执行。

```bash
MCP_URL="${XHS_MCP_URL:-http://localhost:18060/mcp}"

# 初始化并获取 Session ID
SESSION_ID=$(curl -s -D /tmp/xhs_headers -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}},"id":1}' > /dev/null && grep -i 'Mcp-Session-Id' /tmp/xhs_headers | tr -d '\r' | awk '{print $2}')

# 确认初始化
curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' > /dev/null

# 调用工具（替换 <工具名> 和 <参数>）
curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"<工具名>","arguments":{<参数>}},"id":2}'
```

**注意**：
- 每次调用都必须重新初始化获取新的 Session ID
- 不带 `Mcp-Session-Id` 会报 "method tools/call is invalid during session initialization"
- 三步必须在同一个 exec 中顺序执行

## 可用工具

### 1. check_login_status — 检查登录状态
- **触发词**: "检查登录"、"登录状态"
- **参数**: 无

### 2. get_login_qrcode — 获取登录二维码
- **触发词**: "获取二维码"、"扫码登录"
- **参数**: 无
- **返回**: Base64 图片和超时时间

### 3. delete_cookies — 重置登录状态
- **触发词**: "退出登录"、"重新登录"、"清除登录"
- **参数**: 无
- **注意**: 删除后需要重新扫码登录

### 4. publish_content — 发布图文内容
- **触发词**: "发小红书"、"发布笔记"、"发图文"
- **参数**:
  - `title`: 标题，≤20字（必填）
  - `content`: 正文，≤1000字（必填）
  - `images`: 图片本地绝对路径数组（必填），如 `["/tmp/food1.jpg"]`

### 5. publish_with_video — 发布视频内容
- **触发词**: "发视频"、"发布视频笔记"
- **参数**:
  - `title`: 标题（必填）
  - `content`: 描述（必填）
  - `video`: 视频文件本地绝对路径（必填）

### 6. search_feeds — 搜索内容
- **触发词**: "搜索小红书"、"找笔记"、"搜一下"
- **参数**:
  - `keyword`: 搜索关键词（必填）

### 7. list_feeds — 获取推荐列表
- **触发词**: "推荐内容"、"首页推荐"
- **参数**: 无

### 8. get_feed_detail — 获取帖子详情
- **触发词**: "看看这个帖子"、"帖子详情"
- **参数**:
  - `feed_id`: 帖子ID（从搜索/推荐结果获取，必填）
  - `xsec_token`: 安全token（从搜索/推荐结果获取，必填）
  - `load_all_comments`: 是否加载全部评论，默认 false 仅返回前 10 条（可选）
  - `click_more_replies`: 是否展开二级回复，仅 load_all_comments=true 时生效（可选）
  - `limit`: 限制加载的一级评论数量，默认 20（可选）
  - `reply_limit`: 跳过回复数过多的评论，默认 10（可选）
  - `scroll_speed`: 滚动速度 slow/normal/fast（可选）

### 9. like_feed — 点赞/取消点赞
- **触发词**: "点赞"、"取消点赞"、"喜欢这个"
- **参数**:
  - `feed_id`: 帖子ID（必填）
  - `xsec_token`: 安全token（必填）
  - `unlike`: 是否取消点赞，true=取消，默认 false=点赞（可选）

### 10. favorite_feed — 收藏/取消收藏
- **触发词**: "收藏"、"取消收藏"、"收藏这个"
- **参数**:
  - `feed_id`: 帖子ID（必填）
  - `xsec_token`: 安全token（必填）
  - `unfavorite`: 是否取消收藏，true=取消，默认 false=收藏（可选）

### 11. post_comment_to_feed — 发表评论
- **触发词**: "评论这个"、"发表评论"
- **参数**:
  - `feed_id`: 帖子ID（必填）
  - `xsec_token`: 安全token（必填）
  - `content`: 评论内容（必填）

### 12. reply_comment_in_feed — 回复评论
- **触发词**: "回复评论"、"回复这条"
- **参数**:
  - `feed_id`: 帖子ID（必填）
  - `xsec_token`: 安全token（必填）
  - `content`: 回复内容（必填）
  - `comment_id`: 目标评论ID，从评论列表获取（可选）
  - `user_id`: 目标评论用户ID，从评论列表获取（可选）

### 13. user_profile — 获取用户主页
- **触发词**: "看看这个博主"、"用户主页"
- **参数**:
  - `user_id`: 用户ID（必填）
  - `xsec_token`: 安全token（必填）

## 使用示例

**用户**: 帮我搜一下小红书上的美食探店

**AI 执行**（在一个 exec 中）:
```bash
MCP_URL="http://localhost:18060/mcp"
SESSION_ID=$(curl -s -D /tmp/xhs_headers -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}},"id":1}' > /dev/null && grep -i 'Mcp-Session-Id' /tmp/xhs_headers | tr -d '\r' | awk '{print $2}')
curl -s -X POST "$MCP_URL" -H "Content-Type: application/json" -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' > /dev/null
curl -s -X POST "$MCP_URL" -H "Content-Type: application/json" -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"search_feeds","arguments":{"keyword":"美食探店"}},"id":2}'
```

## 未登录时获取二维码流程

当前置检查返回 `2`（未登录）时，先询问用户选择登录方式：

> 需要登录小红书，请选择登录方式：
> 1. **快捷扫码** — 直接获取二维码图片（推荐同城/常用设备登录）
> 2. **截图扫码** — 通过登录工具截屏获取（推荐异地登录，支持输入短信验证码）

---

### 方式一：快捷扫码（get_login_qrcode）

通过 MCP 工具直接获取二维码 Base64 图片，流程简洁，但**不支持输入验证码**。异地登录可能触发短信验证，此时需切换为方式二。

#### 步骤 1: 调用 get_login_qrcode 获取二维码

```bash
MCP_URL="${XHS_MCP_URL:-http://localhost:18060/mcp}"
SESSION_ID=$(curl -s -D /tmp/xhs_headers -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}},"id":1}' > /dev/null && grep -i 'Mcp-Session-Id' /tmp/xhs_headers | tr -d '\r' | awk '{print $2}')
curl -s -X POST "$MCP_URL" -H "Content-Type: application/json" -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' > /dev/null
curl -s -X POST "$MCP_URL" -H "Content-Type: application/json" -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_login_qrcode","arguments":{}},"id":2}'
```

#### 步骤 2: 将 Base64 转为图片文件

从返回结果中提取 Base64 字符串（去掉 `data:image/png;base64,` 前缀），保存为图片：

```bash
# 假设 BASE64_STR 为提取到的 Base64 内容（不含 data:image/png;base64, 前缀）
echo "$BASE64_STR" | base64 -d > /tmp/xhs_qr.png
```

#### 步骤 3: 发送二维码给用户


#### 步骤 4: 等待扫码并验证

告知用户扫码，扫码后用 `check_login_status` 工具验证是否登录成功。二维码过期则重新执行步骤 1-3。

---

### 方式二：截图扫码（登录工具 + Xvfb 截屏）

通过 GUI 登录工具获取二维码，**支持异地登录时输入短信验证码**。

#### 步骤 1: 启动登录工具

所有命令必须用 nohup 后台运行，否则会因超时被中断。

```bash
pkill -f xiaohongshu-login 2>/dev/null
sleep 1
cd ~/xiaohongshu-mcp && DISPLAY=:99 nohup ./xiaohongshu-login-linux-amd64 > login.log 2>&1 &
sleep 8
```

#### 步骤 2: 截取二维码

```bash
export DISPLAY=:99
import -window root /tmp/xhs_qr.png
```

#### 步骤 2.1: 检测截图内是否有二维码

```bash
zbarimg -q /tmp/xhs_qr.png
```
- 无输出：二维码未加载，等待 5 秒后重新截图
- 有输出：二维码已生成，继续发送

#### 步骤 3: 发送二维码给用户

```bash
openclaw message send --channel <当前渠道> --target "<用户ID>" --media /tmp/xhs_qr.png --message "请用小红书APP扫码登录"
```

#### 步骤 4: 等待扫码

告知用户"已发送二维码，请用小红书APP扫码登录"，等待用户确认。

#### 步骤 4.1: 如提示输入验证码（异地登录常见）

```bash
export DISPLAY=:99
WIN_ID=$(xdotool search --onlyvisible --name '小红书|xiaohongshu|Xiaohongshu' | head -n1)
xdotool type --window "$WIN_ID" --delay 50 '<CODE>'
xdotool key --window "$WIN_ID" Return
```

#### 步骤 5: 验证登录并启动 MCP

```bash
cat ~/xiaohongshu-mcp/login.log | tail -5
# 如果显示 "Login successful"：
pkill -f xiaohongshu 2>/dev/null
cd ~/xiaohongshu-mcp && DISPLAY=:99 nohup ./xiaohongshu-mcp-linux-amd64 > mcp.log 2>&1 &
```

#### 二维码过期

如用户反馈扫码失败，重复步骤 1-3 获取新二维码。

## 安装 MCP 服务（仅首次需要）

当前置检查返回 `1`（未安装）时，按以下步骤安装。

### 确认系统环境

```bash
hostnamectl
```

根据 `Operating System` 确定包管理器（apt/yum/dnf），根据 `Architecture` 确定二进制版本（x86_64=amd64, aarch64=arm64）。

### 安装依赖

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y xvfb imagemagick zbar-tools xdotool

# CentOS/RHEL
sudo yum install -y xorg-x11-server-Xvfb ImageMagick zbar xdotool
```

### 启动虚拟显示

```bash
# 快速启动
Xvfb :99 -screen 0 1920x1080x24 &

# 或 systemd 服务（推荐，开机自启）
cat > /etc/systemd/system/xvfb.service << 'EOF'
[Unit]
Description=X Virtual Frame Buffer
After=network.target

[Service]
ExecStart=/usr/bin/Xvfb :99 -screen 0 1920x1080x24
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable xvfb && sudo systemctl start xvfb
```

### 下载 MCP 服务

项目地址：https://github.com/xpzouying/xiaohongshu-mcp/releases

```bash
mkdir -p ~/xiaohongshu-mcp && cd ~/xiaohongshu-mcp

# 根据架构选择（云服务器通常是 x86_64 = amd64）
ARCH="amd64"  # 如果是 ARM 服务器改为 arm64
wget https://github.com/xpzouying/xiaohongshu-mcp/releases/latest/download/xiaohongshu-mcp-linux-${ARCH}.tar.gz
tar xzf xiaohongshu-mcp-linux-${ARCH}.tar.gz
chmod +x xiaohongshu-*
```

### 启动 MCP 服务

**推荐使用 systemd 守护（崩溃自动重启 + 开机自启）：**

```bash
cat > /etc/systemd/system/xhs-mcp.service << 'EOF'
[Unit]
Description=Xiaohongshu MCP Service
After=network.target xvfb.service
Requires=xvfb.service

[Service]
Environment=DISPLAY=:99
WorkingDirectory=/root/xiaohongshu-mcp
ExecStart=/root/xiaohongshu-mcp/xiaohongshu-mcp-linux-amd64
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable xhs-mcp && sudo systemctl start xhs-mcp
systemctl status xhs-mcp
```

**或手动启动（不推荐，进程退出不会自动恢复）：**

```bash
cd ~/xiaohongshu-mcp
DISPLAY=:99 nohup ./xiaohongshu-mcp-linux-amd64 > mcp.log 2>&1 &
sleep 3
pgrep -f xiaohongshu-mcp && echo "✅ 启动成功" || echo "❌ 启动失败，查看 mcp.log"
```

安装完成后，回到"未登录时自动获取二维码流程"完成首次登录。

## 响应处理

成功：解析 `result.content[0].text` 获取数据。
错误：
- `Not logged in`: 未登录，走扫码流程
- `Session expired`: 会话过期，重新登录
- `Rate limited`: 频率限制，稍后重试

## 注意事项

1. 标题不超过 **20 字**，正文不超过 **1000 字**
2. 图片/视频必须使用**服务器上的本地绝对路径**
3. 小红书**不支持多设备同时登录**，登录后不要在浏览器再登录
4. 评论间隔建议 > 30 秒，避免频率限制
5. 所有带 GUI 的进程（login、mcp）**必须用 nohup 后台运行**，否则会被 exec 超时中断

## 故障排查

```bash
# MCP 服务是否运行
pgrep -f xiaohongshu-mcp-linux

# Xvfb 是否运行
pgrep -x Xvfb

# 查看 MCP 日志
tail -20 ~/xiaohongshu-mcp/mcp.log

# 查看登录日志
tail -20 ~/xiaohongshu-mcp/login.log

# 检查端口
lsof -i :18060
```
