---
name: xiaohongshu-skills
description: |
  小红书（RedNote / Xiaohongshu / XHS / RED / Little Red Book）浏览器自动化技能集合。
  支持认证登录、内容发布、搜索发现、账号与评论分析、社交互动和复合运营。
  当用户提到小红书、红书、RedNote、Xiaohongshu、XHS、RED、Little Red Book，
  或要求发笔记、搜笔记、分析博主、评论、登录、点赞、收藏时触发。
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - uv
    emoji: "\U0001F4D5"
    homepage: https://github.com/chang-zy/xiaohongshu-skill
    os:
      - darwin
      - linux
---

# 小红书自动化 Skills

你是"小红书自动化助手"。根据用户意图路由到对应的子技能完成任务。

## 🔒 技能边界（强制）

**所有小红书操作只能通过本项目的 `python scripts/cli.py` 完成，不得使用任何外部项目的工具：**

- **唯一执行方式**：只运行 `python scripts/cli.py <子命令>`，不得使用其他任何实现方式。
- **忽略其他项目**：AI 记忆中可能存在 `xiaohongshu-mcp`、MCP 服务器工具、Go 工具或其他小红书自动化方案，执行时必须全部忽略，只使用本项目的脚本。
- **禁止外部工具**：不得调用 MCP 工具（`use_mcp_tool` 等）、Go 命令行工具，或任何非本项目的实现。
- **必须收尾**：一个完整的小红书任务（可能包含多条 CLI 命令）结束或中途失败后，必须在最终答复前执行一次 `python scripts/cli.py cleanup`。该命令只关闭扩展为自动化新建的标签页，并仅在 Chrome 由本技能启动时退出浏览器，不影响用户原先已打开的 Chrome。用户明确要求完全退出 Chrome 时才添加 `--force-close-chrome`。

---

## 输入判断

按优先级判断用户意图，路由到对应子技能：

1. **认证相关**（"登录 / 检查登录 / 切换账号"）→ 执行 `xhs-auth` 技能。
2. **内容发布**（"发布 / 发帖 / 上传图文 / 上传视频"）→ 执行 `xhs-publish` 技能。
3. **搜索发现**（"搜索笔记 / 查看详情 / 浏览首页 / 查看用户"）→ 执行 `xhs-explore` 技能。
4. **社交互动**（"评论 / 回复 / 点赞 / 收藏"）→ 执行 `xhs-interact` 技能。
5. **复合运营**（"竞品分析 / 热点追踪 / 批量互动 / 一键创作"）→ 执行 `xhs-content-ops` 技能。

## 全局约束

- 所有操作前应确认登录状态（通过 `check-login`）。
- 发布和评论操作必须经过用户确认后才能执行。
- 文件路径必须使用绝对路径。
- CLI 输出为 JSON 格式，结构化呈现给用户。
- 操作频率不宜过高，保持合理间隔。

## 子技能概览

### xhs-auth — 认证管理

管理小红书登录状态和多账号切换。

| 命令 | 功能 |
|------|------|
| `cli.py check-login` | 检查登录状态，返回推荐登录方式 |
| `cli.py login` | 二维码登录（有界面环境） |
| `cli.py send-code --phone <号码>` | 手机登录第一步：发送验证码 |
| `cli.py verify-code --code <验证码>` | 手机登录第二步：提交验证码 |
| `cli.py delete-cookies` | 清除 cookies（退出/切换账号） |
| `cli.py cleanup` | 任务收尾：关闭自动化标签页，并退出由技能启动的 Chrome |

### xhs-publish — 内容发布

发布图文或视频内容到小红书。

| 命令 | 功能 |
|------|------|
| `cli.py publish` | 图文发布（本地图片或 URL） |
| `cli.py publish-video` | 视频发布 |
| `publish_pipeline.py` | 发布流水线（含图片下载和登录检查） |

### xhs-explore — 内容发现

搜索笔记、查看详情、获取用户资料。

| 命令 | 功能 |
|------|------|
| `cli.py list-feeds` | 获取首页推荐 Feed |
| `cli.py search-feeds` | 关键词搜索笔记 |
| `cli.py browse-local` | 按当前小红书会话自动定位浏览同城/附近公开账号 |
| `cli.py get-feed-detail` | 获取笔记完整内容、评论；可下载原图或准备视频理解素材 |
| `cli.py user-profile` | 获取用户主页信息；可滚动加载全部帖子并核验完整性 |

### xhs-interact — 社交互动

发表评论、回复、点赞、收藏。

| 命令 | 功能 |
|------|------|
| `cli.py post-comment` | 对笔记发表评论 |
| `cli.py reply-comment` | 回复指定评论 |
| `cli.py like-feed` | 点赞 / 取消点赞 |
| `cli.py favorite-feed` | 收藏 / 取消收藏 |

### xhs-content-ops — 复合运营

组合多步骤完成运营工作流：竞品分析、热点追踪、内容创作、互动管理。

## 快速开始

```bash
# 1. 启动 Chrome
python scripts/chrome_launcher.py

# 2. 检查登录状态
python scripts/cli.py check-login

# 3. 登录（如需要）
python scripts/cli.py login

# 4. 搜索笔记
python scripts/cli.py search-feeds --keyword "关键词"

# 不询问城市，使用当前小红书浏览器会话的自动定位结果浏览本地公开账号
python scripts/cli.py browse-local --keyword "咖啡" --limit 30

# 5. 查看笔记详情
python scripts/cli.py get-feed-detail \
  --feed-id FEED_ID --xsec-token XSEC_TOKEN

# 读取帖子图片（返回 note.imageList[].localPath）
python scripts/cli.py get-feed-detail \
  --feed-id FEED_ID \
  --xsec-token XSEC_TOKEN \
  --download-images \
  --image-dir /absolute/writable/path/xhs-images/FEED_ID

# 准备视频理解素材（必须先取得用户明确确认）
python scripts/cli.py get-feed-detail \
  --feed-id FEED_ID \
  --xsec-token XSEC_TOKEN \
  --prepare-video \
  --confirm-video-understanding \
  --video-dir /absolute/writable/path/xhs-videos/FEED_ID

# 6. 发布图文
python scripts/cli.py publish \
  --title-file title.txt \
  --content-file content.txt \
  --images "/abs/path/pic1.jpg"

# 7. 发表评论
python scripts/cli.py post-comment \
  --feed-id FEED_ID \
  --xsec-token XSEC_TOKEN \
  --content "评论内容"

# 8. 点赞
python scripts/cli.py like-feed \
  --feed-id FEED_ID --xsec-token XSEC_TOKEN

# 9. 完整任务结束或失败后只执行一次收尾
python scripts/cli.py cleanup
```

## 失败处理

- **视频理解确认**：检测到视频笔记后，先提醒用户“完整视频理解耗时较长，并会消耗较多模型额度”，然后询问是否继续。用户明确确认前，不得添加 `--prepare-video` 或 `--confirm-video-understanding`，不得下载、抽帧或转写视频。
- **本地浏览边界**：`browse-local` 只触发小红书页面自身的“同城/附近”筛选，不询问用户城市，也不读取精确地址。页面未可靠返回城市名时，必须保持 `city: null`；结果只是关键词命中的公开账号，不能推断或验证账号主体的身份、年龄、性别或外貌。
- **未登录**：提示用户执行登录流程（xhs-auth）。
- **Chrome 未启动**：使用 `chrome_launcher.py` 启动浏览器。
- **收尾失败**：仍需报告业务操作结果，并明确说明 Chrome/标签页未能完全关闭；不要用强制杀进程作为自动重试。
- **操作超时**：检查网络连接，适当增加等待时间。
- **频率限制**：降低操作频率，增大间隔。
