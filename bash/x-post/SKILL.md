---
name: x-post
description: |
  Publish a tweet or a multi-post thread (with images) to X/Twitter using the login that already exists in the user's local Chrome profile: no API key, no manual cookie copying. Dry-run first (compose + screenshot for human review), then `--post`. Use when the user says 发 X, 发推, 发到 X, 发个线程, post to X, tweet this, publish on Twitter, or hands you post text to send.
version: 1.0.0
author: doing
metadata:
  hermes:
    tags: [X, Twitter, 发推, 发帖, 线程, thread, agent-browser, Chrome cookie, 对外发布]
    category: publishing
---

# x-post

把一段文字或一条线程（主帖 + 若干回复，可配图）发到 X。登录态直接取自用户本机 Chrome 已登录的 profile，脚本解密 cookie 注入独立的 agent-browser 会话，用 X 网页编辑器发出，最后回到帖子页核对段数与配图。**默认只预览不发布**，人审过截图后再加 `--post`。

## 前置检查（先做，缺一不可）

- macOS；`agent-browser`、`sqlite3`、`security`、Node ≥ 20 在 PATH 中。
- 用户的 Chrome 某个 profile 已登录目标 X 账号。先跑 `--check-login` 确认账号名，不要猜 profile：

```bash
node "$(dirname "$(readlink -f "$0")")/scripts/x_post.mjs" --check-login --profile Default
```

返回 `{"loggedIn":true,"account":"<handle>"}`。若报无登录 cookie，换 `--profile "Profile 1"` 等重试；仍无则让用户在 Chrome 里登录 x.com 后重来。
- 第一次读取钥匙串会弹 macOS 授权框，用户点"允许"即可；这是 Chrome Safe Storage 密码，脚本不落盘。

## 执行步骤

1. **把内容写成文件**（不要把长文本塞进命令行参数）。格式：帖子之间用单独一行 `---` 分隔，第一段是主帖；`image: 相对路径` 给该段配图，最多 4 张，**只支持主帖配图**。

```
主帖正文，可多行，可含 emoji
image: ./card.png
---
第一条回复
---
第二条回复
```

2. **先预览**：

```bash
node "<skill>/scripts/x_post.mjs" --file posts.md --profile Default --out ./x-post-out
```

脚本会：解密 cookie → 打开 x.com/home（带界面窗口）→ 校验已登录 → 填主帖、上传图片 → 每多一段点一次"+"（此时草稿会移入弹窗）→ 逐段回读文本、数附件、查发布按钮是否可用 → 截图到 `x-post-out/dry-run.png` → 输出 JSON。编辑器保持打开，用户可在窗口里看。

3. **给用户看**截图和四段原文，拿到明确同意。对外发布不可撤回，没有同意不要进入下一步。

4. **发布**：同一命令加 `--post`。脚本重新组稿（会先关闭上一步的窗口）、点击 Post/Post all、等弹窗关闭，再去个人主页找到新帖，打开帖子页核对：自己发的段数 = 输入段数，配图存在。输出：

```json
{"mode":"posted","account":"...","url":"https://x.com/<handle>/status/<id>","verified":{"posts":4,"expectedPosts":4,"image":true,"expectedImage":true}}
```

5. **记录链接**：仓库若有 `docs/launch-posts.md`（"已发布"表），把日期、渠道、链接、备注补进去；运营账本另记。

## 字数

X 按加权长度限 280：URL 记 23，中日韩字符和 emoji 记 2，其余记 1。中文纯文本上限约 140 字。脚本会在组稿前拒绝超限段落；Premium 账号可 `--allow-long`。写中文帖时按 140 字一段规划，线程比硬塞更好读。

## 已踩过的坑（脚本已处理，改脚本时别退回去）

- 点"+"后草稿进入 `div[role="dialog"]` 弹窗，首页内联编辑器仍留在页面上：不限定弹窗作用域时 `tweetTextarea_0` 会命中两个元素报 strict mode violation，内联的 Post 按钮显示 disabled 也不代表弹窗里的 Post all 不可用。校验和点击都要以弹窗为根。
- 文本用 `keyboard inserttext`，不用 `type`/`fill`：编辑器是 Draft.js，`fill` 不触发状态更新，`type` 对 emoji 和换行不稳。
- `agent-browser eval` 对对象只打印末行且是 JSON 编码后的字符串，脚本里用 `JSON.stringify` 包一层再解析两次。
- Chrome 的 Cookies 数据库被 Chrome 锁着，必须复制一份再读；Chrome ≥ 130 解密后前 32 字节是 host key 的哈希，要剥掉。
- 解密后的 cookie 状态文件只存在临时目录，`finally` 里删除；agent-browser 会以 `--session-name` 持久化登录态，属于本机用户自己的数据，不要复制到仓库或日志。
- 发出后不要用首页判断成功，去个人主页按主帖前 20 字定位新帖，再打开帖子页数段数。
- zsh 下 `rm /tmp/x-*.sqlite` 这种无匹配的通配会让整行命令中止；清理用脚本，不用 shell 通配。

## 边界

- 只做发布，不做定时、不做回复别人的帖子、不做删帖。需要回复某条帖子时另写流程。
- 图片只支持主帖；视频、投票、GIF 搜索不支持。
- 依赖 X 网页的 `data-testid`，改版即失效；失效时先跑 `--check-login` 与预览，看截图定位哪一步断了，再改选择器。
