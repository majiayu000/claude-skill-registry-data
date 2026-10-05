---
name: bilibili-mcp
description: B站全功能操作：视频上传/搜索/互动、动态发布、直播弹幕、收藏夹管理、关注粉丝、历史记录等。Use when：用户提到 B站、哔哩哔哩、bilibili、投稿、直播、弹幕。NOT for：其他视频平台操作。
---

# B站 MCP

通过 bilibili-api-python 操作哔哩哔哩，支持视频、动态、直播、收藏夹等全功能。

## 工作流程概览

1. 检查登录状态（`check_login`）
2. 如未登录 → 执行扫码登录流程（见下文）
3. 执行目标操作

## 安装（仅首次）

```bash
bash {{SKILL_DIR}}/scripts/install.sh
```

## 凭据存储

登录凭据使用 **加密文件** 存储在 `data/credential.enc` 中（Fernet AES-128-CBC），密钥自动从机器指纹派生。不再写入 `.zshrc` 或 `.bashrc`。

## 扫码登录流程（重要！）

当 `check_login` 返回 `logged_in: false` 时，必须执行以下步骤：

1. 调用 `get_login_qrcode`
2. 二维码图片会**自动弹出预览窗口**（macOS 用 `open` 命令打开）
3. **必须立即回复用户以下内容**（不要省略！）：
   ```
   📱 请扫码登录 B 站账号：
   
   二维码已自动打开，请用哔哩哔哩 App 扫描登录。
   正在等待扫码...（最长等待 120 秒）
   ```
4. `get_login_qrcode` 会**自动轮询等待扫码**（每 3 秒检查一次，最长 120 秒），扫码成功后自动保存凭据并返回结果
5. 如果返回超时，提示用户重新调用

**禁止：**
- ❌ 使用 browser 工具（会占据整个界面无法返回）
- ❌ 说"二维码已保存到桌面"（二维码不再保存到桌面，而是自动弹出预览）

## 调用方式

```bash
python3 {{SKILL_DIR}}/scripts/bili_call.py <tool_name> [json_args]
```

---

## 工具列表

### 📋 账号管理

| 工具 | 说明 | 参数 |
|------|------|------|
| `check_login` | 检查登录状态 | 无 |
| `get_login_qrcode` | 获取登录二维码 | 无 |
| `check_qrcode_status` | 检查扫码状态 | 无 |
| `logout` | 退出登录 | 无 |

### 📤 内容发布

| 工具 | 说明 | 必填参数 |
|------|------|----------|
| `upload_video` | 上传视频 | `video_path`, `title`, `tid`(分区ID) |
| `publish_dynamic` | 发布动态 | `text` |
| `delete_dynamic` | 删除动态 | `dynamic_id` |

**upload_video 可选参数**：`cover`(封面), `desc`(简介), `tags`(标签列表), `dynamic`(动态文字), `original`(是否原创), `source`(转载来源)

**publish_dynamic 可选参数**：`images`(图片路径列表), `topic_id`, `schedule_time`(定时发布)

**常用分区 tid**：
- 17=单机游戏, 171=电子竞技, 172=手机游戏
- 138=搞笑, 21=日常, 75=动物圈
- 183=影视杂谈, 182=影视剪辑
- 122=野生技术协会, 39=演讲公开课

### 🔍 搜索

| 工具 | 说明 | 必填参数 |
|------|------|----------|
| `search_video` | 搜索视频 | `keyword` |
| `search_user` | 搜索用户 | `keyword` |

可选：`page`(页码，默认1)

### 🔥 热门/排行榜

| 工具 | 说明 | 参数 |
|------|------|------|
| `get_hot_videos` | 获取热门视频 | `pn`(页码) |
| `get_rank` | 获取排行榜 | `type_name`(枚举名), `day`(3或7) |
| `get_weekly_hot` | 每周必看 | `week`(期数，0=最新) |

**排行榜 type_name**：All=全站, Douga=动画, Music=音乐, Game=游戏, Ent=娱乐, Technology=科技, Knowledge=知识, Life=生活, Cinephile=影视, Food=美食, Animal=动物, Dance=舞蹈, Kichiku=鬼畜, Fashion=时尚, Sports=运动, Car=汽车, Original=原创, Rookie=新人

### 📺 视频信息

| 工具 | 说明 | 必填参数 |
|------|------|----------|
| `get_video_info` | 获取视频详情 | `bvid` |
| `get_user_info` | 获取用户信息 | `mid` |
| `get_user_videos` | 获取用户投稿 | `mid` |

**get_user_videos 可选**：`page`, `order`(pubdate/click/stow)

### 👍 视频互动

| 工具 | 说明 | 必填参数 |
|------|------|----------|
| `like_video` | 点赞/取消 | `bvid` |
| `coin_video` | 投币 | `bvid` |
| `favorite_video` | 收藏 | `bvid` |
| `comment_video` | 评论 | `bvid`, `text` |
| `get_video_comments` | 获取评论 | `bvid` |
| `reply_comment` | 回复评论 | `bvid`, `rpid`, `text` |

**like_video 可选**：`unlike=true` 取消点赞
**coin_video 可选**：`num`(投币数量，1或2)
**favorite_video 可选**：`add_media_ids`(收藏夹ID列表)

### 💬 弹幕

| 工具 | 说明 | 必填参数 |
|------|------|----------|
| `get_video_danmaku` | 获取弹幕 | `bvid` |
| `send_video_danmaku` | 发送弹幕 | `bvid`, `text` |

**send_video_danmaku 可选**：`dm_time`(出现时间秒数)

### 📝 动态

| 工具 | 说明 | 必填参数 |
|------|------|----------|
| `like_dynamic` | 点赞动态 | `dynamic_id` |
| `repost_dynamic` | 转发动态 | `dynamic_id` |
| `get_my_dynamics` | 我的动态 | 无 |
| `get_user_dynamics` | 用户动态 | `mid` |

### 📺 直播

| 工具 | 说明 | 必填参数 |
|------|------|----------|
| `get_live_info` | 直播间信息 | `room_id` |
| `get_live_area_list` | 直播分区列表 | 无 |
| `get_live_list` | 直播列表 | 无 |
| `send_live_danmaku` | 发送直播弹幕 | `room_id`, `text` |

**get_live_list 必填**：`area_id`(子分区ID，通过 get_live_area_list 获取)；**可选**：`page`

### 📁 收藏夹

| 工具 | 说明 | 必填参数 |
|------|------|----------|
| `get_my_favorite_list` | 我的收藏夹 | 无 |
| `get_favorite_content` | 收藏夹内容 | `media_id` |
| `create_favorite_folder` | 创建收藏夹 | `title` |

**create_favorite_folder 可选**：`intro`, `privacy`(是否私密)

### 👥 关注/粉丝

| 工具 | 说明 | 必填参数 |
|------|------|----------|
| `follow_user` | 关注/取关 | `mid` |
| `get_my_followings` | 我的关注 | 无 |
| `get_my_followers` | 我的粉丝 | 无 |

**follow_user 可选**：`unfollow=true` 取消关注

### 📜 历史记录

| 工具 | 说明 | 参数 |
|------|------|------|
| `get_history` | 观看历史 | `page`, `max_count` |
| `clear_history` | 清空历史 | 无 |

---

## 示例

```bash
# 检查登录
python3 {{SKILL_DIR}}/scripts/bili_call.py check_login

# 搜索视频
python3 {{SKILL_DIR}}/scripts/bili_call.py search_video '{"keyword":"AI教程"}'

# 获取热门视频
python3 {{SKILL_DIR}}/scripts/bili_call.py get_hot_videos

# 获取游戏区排行榜
python3 {{SKILL_DIR}}/scripts/bili_call.py get_rank '{"type_name":"Game","day":7}'

# 获取视频信息
python3 {{SKILL_DIR}}/scripts/bili_call.py get_video_info '{"bvid":"BV1xx411c7mD"}'

# 点赞视频
python3 {{SKILL_DIR}}/scripts/bili_call.py like_video '{"bvid":"BV1xx411c7mD"}'

# 发送弹幕
python3 {{SKILL_DIR}}/scripts/bili_call.py send_video_danmaku '{"bvid":"BV1xx411c7mD","text":"666"}'

# 获取直播间信息
python3 {{SKILL_DIR}}/scripts/bili_call.py get_live_info '{"room_id":21452505}'

# 发布动态
python3 {{SKILL_DIR}}/scripts/bili_call.py publish_dynamic '{"text":"今天天气不错"}'

# 发布带图动态
python3 {{SKILL_DIR}}/scripts/bili_call.py publish_dynamic '{"text":"分享图片","images":["/path/to/img.jpg"]}'

# 上传视频
python3 {{SKILL_DIR}}/scripts/bili_call.py upload_video '{"video_path":"/path/to/video.mp4","title":"我的视频","tid":17,"desc":"视频简介","tags":["游戏","实况"]}'

# 关注用户
python3 {{SKILL_DIR}}/scripts/bili_call.py follow_user '{"mid":123456}'

# 创建收藏夹
python3 {{SKILL_DIR}}/scripts/bili_call.py create_favorite_folder '{"title":"我的收藏","privacy":true}'
```

## 视频发布流程

当用户要发布视频但没有提供完整信息时：

1. 询问视频文件路径
2. 询问视频标题
3. 根据内容推荐合适的分区（tid）
4. **自动生成**简短的 B 站风格简介和标签（不要调用其他 skill）
5. 调用 `upload_video` 上传

**简介风格示例**：
- "记录日常生活的小美好~"
- "希望大家喜欢，三连支持一下！"
- "第一次投稿，多多指教"

## 约束

- 视频标题 ≤ 80 字
- 动态文字 ≤ 2000 字
- 弹幕 ≤ 100 字
- 每日投稿上限约 50 个
- 封面会自动从视频提取（需要 ffmpeg 或 opencv-python）
- 部分操作需要登录（会自动提示）

## 故障排查

- **未登录** → 执行扫码登录流程
- **凭据过期** → 调用 `logout` 后重新登录
- **视频上传失败** → 检查文件路径、分区ID是否正确
- **封面提取失败** → 安装 ffmpeg: `brew install ffmpeg`
