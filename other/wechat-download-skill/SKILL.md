---
name: wechat-download
description: Use when the user asks to download, archive, crawl, scrape, or export articles from a WeChat official account (公众号).
version: 1.0.1
---

# 微信公众号文章下载

通过本地部署的 [wechat-download-api](https://github.com/tmwgsicp/wechat-download-api) 服务，批量下载任意微信公众号的全部历史文章（含完整内容）。

## 触发条件

- 用户要求下载/爬取微信公众号文章
- 用户要求搜索公众号并获取文章
- 用户说「下载 XX 公众号的文章」
- 用户提到 wechat-download / 公众号下载 / 微信文章抓取

## 架构

```
本 skill (调用脚本)  →  wechat-download-api (本地 HTTP 服务 :8765)  →  微信公众平台 API
```

- **wechat-download-api**：第三方开源服务，使用 Chrome TLS 指纹（curl_cffi）模拟浏览器，通过微信公众平台后台凭证调用接口
- **本 skill 脚本**：封装了 API 的搜索、列表、下载功能，带限频自适应和断点续传

## 使用方式

用户安装本 skill 后，只需要在 agent 里说「下载 XXX 的公众号文章」。除扫码登录外，不要要求用户手动部署底层服务；agent 应优先自动运行本目录脚本完成环境准备。

### 1. 启动服务

从 skill 目录运行：

```bash
cd ~/.claude/skills/wechat-download
bash scripts/start_wechat_api.sh
# 默认端口 8765，可指定: bash scripts/start_wechat_api.sh 9876
```

脚本会自动发现 `./wechat-download-api`、`../wechat-download-api`，也支持通过 `WECHAT_API_REPO` 环境变量定位。找不到时会自动 clone `wechat-download-api` 到当前 skill 目录，并安装底层服务依赖。

> **端口说明**：本 skill 默认使用 `8765` 而非 upstream 的 `5000`，因为 macOS 上 `5000` 常被系统服务占用。如果你用 upstream 的 `start.sh` 启动了服务（端口 `5000`），请在命令前加 `WECHAT_API_URL=http://localhost:5000`。

脚本会自动：
- 查找或下载 wechat-download-api 仓库
- 创建 `.env`（如果不存在）
- 安装缺失的 Python 依赖
- 后台启动服务

### 2. 扫码登录

**前提：用户需要有一个微信公众号（订阅号/服务号均可）。**

1. 浏览器打开 `http://localhost:8765/login.html`
2. 用公众号管理员微信扫码
3. 登录成功后凭证自动保存到 `.env`，有效期约 **4 天**

> 如果用户没有公众号，见下方「备选方案」。

---

## 操作流程

### 第一步：检查/启动服务

如果服务还没启动，先运行：

```bash
bash scripts/start_wechat_api.sh
```

然后检查服务状态：

```bash
python3 scripts/download_wechat.py status
```

### 第二步：检查登录

```bash
curl -s http://localhost:8765/api/admin/status
```

如果 `isExpired: true` → 重新扫码登录。

### 第三步：搜索公众号

```bash
python3 scripts/download_wechat.py search "公众号名称"
```

从输出中获取 `fakeid`。

### 第四步：下载文章

```bash
python3 scripts/download_wechat.py download "fakeid" 200 ./output_dir
```

功能：
- 自动分页获取全部文章列表
- 逐篇下载完整内容，保存为 `.txt` 文件
- **断点续传**：已下载的文件自动跳过
- **限频自适应**：检测到 Rate limited 自动等待
- 失败记录保存到 `failures.json`

### 其他命令

```bash
python3 scripts/download_wechat.py list "fakeid" 0 50     # 查看文章列表
python3 scripts/download_wechat.py rss "fakeid"            # 获取 RSS 地址
```

---

## 常见错误及解决方法

### 错误 1：端口被占用

```
ERROR: [Errno 48] address already in use
```

**解决**：换一个端口：`bash scripts/start_wechat_api.sh 9876`

### 错误 2：文章 URL 字段名（关键）

```python
url = a.get("url", "")   # ❌ 错误！
url = a.get("link", "")  # ✓ 正确
```

API 返回的文章列表使用 `link` 字段，不是 `url`。

### 错误 3：Rate Limited（限频）

```
Rate limited: 请求过于频繁，请X秒后重试
```

**解决**：脚本已内置自适应退避。如果仍然频繁触发，增大 `MIN_DELAY`（默认 3.2 秒）。

### 错误 4：触发微信安全验证

```
触发微信安全验证。
```

**解决**：
- 降低请求频率
- 在浏览器中打开提示的文章 URL 完成人机验证
- 等待 30 分钟后重试
- 如频繁触发，在 `.env` 中配置 `PROXY_URLS`（SOCKS5 代理池）

### 错误 5：无法获取文章内容

```
无法获取文章内容。可能原因：文章被删除、访问受限或需要验证。
```

**原因**：文章已被删除 / 是广告推广 / 图片分享 / 微信风控。跳过即可，通常占 30-50%。

### 错误 6：登录过期

**原因**：微信凭证有效期约 4 天。

**解决**：重新访问 `http://localhost:8765/login.html` 扫码。

### 错误 7：curl_cffi 编译失败

```
ModuleNotFoundError: No module named 'curl_cffi'
```

**解决**：需要可用的 C 编译器。macOS 需安装 Xcode CLT（`xcode-select --install`），Linux 需 `build-essential` 和 `libcurl4-openssl-dev`。预编译 wheel 在 PyPI 上覆盖主流平台。

---

## 备选方案：无公众号时下载

如果用户没有微信公众号无法登录，可以用以下方法：

1. **搜索引擎反查**：搜索 `"公众号名" mp.weixin.qq.com/s` 获取文章链接，直接访问 mp.weixin.qq.com 提取 `#js_content` 中的内容
2. **转载平台**：在 guancha.cn（观察者网）、36kr、新浪财经等平台搜索转载文章
3. **镜像站**：jintiankansha.me 等平台有文章列表（但通常需要 VIP 才能看全文）

---

## 参考

- [wechat-download-api](https://github.com/tmwgsicp/wechat-download-api) — 底层 API 服务，AGPL 3.0
- 文章 URL 格式说明：`https://mp.weixin.qq.com/s/{short_id}` 或带 `__biz`/`mid`/`idx`/`sn` 参数的完整链接
