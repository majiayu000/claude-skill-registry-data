---
name: bird-bookmark-folders
description: "Organize X/Twitter bookmark folders (collections) via GraphQL with Chrome cookie auth. Actions: list folders, list folder contents, add/remove/move a bookmark between folders, create a folder. Keywords: twitter, x, bookmark folder, collection, 收藏夹, 书签分类, 整理收藏夹, 移动书签."
---

# X Bookmark Folders Skill (Write-Capable)

管理 X/Twitter 的书签收藏夹（bookmark collections）。与只读的 `bird-twitter` 分开，因为本 skill 包含**写操作**。

Bird CLI 没有收藏夹管理命令（只有 `bookmarks --folder-id` 读取），所以这里直接调 X 的 GraphQL 接口。

## 授权要求

**每一次写操作都必须先获得用户对该次操作的明确同意。** 不要因为用户批准过一次移动就自行扩展到其他条目。

- 读操作（`list`、`items`）随时可执行，无需确认
- 写操作（`add`、`remove`、`move`、`create`、`delete`）必须带 `--yes`，且执行前要向用户说明将改动哪些条目
- **`delete`（取消收藏）是其中唯一不可逆的一个**：推文会从「所有书签」移除、所有收藏夹同时消失，本 skill 无法撤销。它必须单独确认，不能并入批量操作的一次性授权
- 批量操作前先列出完整清单让用户确认，执行时逐条汇报结果
- 脚本内置 1.5 秒写操作节流；批量超过 20 条时进一步放慢或分批

## 前置条件

1. X 凭据按 环境变量 -> 钥匙串 -> Chrome cookie 库 的顺序解析（见 `resolve_x_credentials`）。主路径是钥匙串，不需要完全磁盘访问权限，与 `bird-twitter` skill 共用同一对条目：
   ```
   security add-generic-password -U -a "$USER" -s bird-x-auth-token -w
   security add-generic-password -U -a "$USER" -s bird-x-ct0 -w
   ```
   填充方式推荐用 `bird-x-cookies-to-keychain`（在持有完全磁盘访问权限的终端里跑一次，自动从 Chrome 提取并写入，过期时重跑刷新）；手动填则从 Chrome DevTools 取值：F12 -> Application -> Cookies -> `https://x.com`。回退到 Chrome cookie 库那条路需要当前进程持有完全磁盘访问权限，而 Claude Code 每次升级换目录都会让该授权失效，不要依赖
2. 凭据失效（401）时，在 Claude 桌面 app 的终端面板里运行 `bird-x-cookies-to-keychain` 刷新即可，无需用户介入：该面板继承桌面 app 本体的完全磁盘访问权限，而 Bash 工具所属的 claude-code helper 没有。
3. 已安装 `bird-twitter` skill —— 本脚本复用它的 cookie 提取与 bearer token 常量；新机器上先跑它的 `scripts/install_local.zsh`
4. 网络走本地代理：`HTTP_PROXY=http://127.0.0.1:7897`、`HTTPS_PROXY=http://127.0.0.1:7897`

## 命令

```bash
SKILLS_HOME="$HOME/.codex/skills"
S="$SKILLS_HOME/bird-bookmark-folders/scripts/bookmark_folders.py"
export HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897
```

### 列出所有收藏夹（只读）

```bash
python3 "$S" list
```

输出 `<folder_id>  <名称>`。后续命令的 folder 参数既接受 id 也接受**精确名称**。

### 列出某个夹的内容（只读）

```bash
python3 "$S" items 方法论 -n 100
```

配合 bird 读取推文详情：

```bash
bird --timeout 20000 bookmarks --folder-id <id> --all --json
```

### 移动书签（最常用）

```bash
python3 "$S" --yes move <tweet_id> <源夹> <目标夹>
```

`move` = 先 `add` 到目标夹，确认返回 `Done` 后再从源夹 `remove`。add 失败时不会执行 remove。

### 单步操作

```bash
python3 "$S" --yes add    <tweet_id> <目标夹>
python3 "$S" --yes remove <tweet_id> <源夹>
python3 "$S" --yes create "投资"
```

## 关键语义（容易搞错）

- **`bookmarkTweetToFolder` 是"添加"，不是"移动"。** 单独调用后推文会同时存在于新旧两个夹里。要真正移动必须配合 `RemoveTweetFromBookmarkFolder`，这正是 `move` 子命令做的事。
- **`RemoveTweetFromBookmarkFolder` 不会取消收藏。** 它只把推文移出该收藏夹，书签本身仍在「所有书签」里。要彻底取消收藏用 `delete` 子命令（`DeleteBookmark`），它会让推文从所有收藏夹一起消失。
- 一条书签可以同时属于多个收藏夹，X 不强制单一归属。

## GraphQL 操作表

2026-07-28 从 `bundle.BookmarkFolders` / `bundle.Bookmarks` / `shared~bundle.BookmarkFolders~bundle.Bookmarks` 三个 chunk 中提取，已实测可用：

| operationName | queryId | 类型 | 成功判据 |
|---|---|---|---|
| `BookmarkFoldersSlice` | `i78YDd0Tza-dV4SYs58kRg` | query | `bookmark_collections_slice.items` |
| `BookmarkFolderTimeline` | `g5l-N4fpbp7B-1OAbOdGzw` | query | `bookmark_collection_timeline.timeline` |
| `Bookmarks` | `aqjes8lRHRFG0HUglVTfNg` | query | — |
| `bookmarkTweetToFolder` | `4KHZvvNbHNf07bsgnL9gWA` | mutation | `bookmark_collection_tweet_put == "Done"` |
| `RemoveTweetFromBookmarkFolder` | `2Qbj9XZvtUvyJB4gFwWfaA` | mutation | `bookmark_collection_tweet_delete == "Done"` |
| `createBookmarkFolder` | `6Xxqpq8TM_CREYiuof_h5w` | mutation | `bookmark_collection_create` |
| `EditBookmarkFolder` | `a6kPp1cS1Dgbsjhapz1PNw` | mutation | `bookmark_collection_update` |
| `DeleteBookmarkFolder` | `2UTTsO-6zs93XqlEUZPsSg` | mutation | — |
| `DeleteBookmark` | `Wlmlj2-xzyS1GN3a6cj-mQ` | mutation | `tweet_bookmark_delete == "Done"` |

mutation 的 variables 统一是 `{"bookmark_collection_id": <folder_id>, "tweet_id": <tweet_id>}`；`createBookmarkFolder` 用 `{"name": "..."}`；`DeleteBookmark` 用 `{"tweet_id": <tweet_id>}`。

## queryId 失效时的恢复流程

X 前端发版后 queryId 可能变化，表现为 `404 Query not found` 或 `422 GRAPHQL_VALIDATION_FAILED`（脚本会直接报出并指向本节）。

**注意：chunk 名到文件的映射表不在任何静态 JS 文件里**（`main.js`、`vendor.js`、`i18n/en.js`、HTML 内联脚本都没有），必须在浏览器里执行 webpack runtime 才能拿到。所以这个流程无法做成无人值守的脚本。

5. 用 Claude in Chrome 打开 `https://x.com/explore`。**不需要登录态**，登录页同样会加载 webpack runtime。

6. 挂探针取出 webpack require：

```javascript
window.webpackChunk_twitter_responsive_web.push([
  ['__probe_chunk__'],
  { '__probe_mod__': (m, e, r) => { window.__wr = r; } },
  (rt) => { rt(rt.s = '__probe_mod__'); }
]);
```

7. 从 `__wr.u` 的源码里筛出 bookmark 相关 chunk 的完整 URL：

```javascript
const wr = window.__wr, src = wr.u.toString();
[...src.matchAll(/(\d+):"([^"]+)"/g)]
  .filter(([, , name]) => /bookmark/i.test(name))
  .map(([, id]) => wr.p + wr.u(id));
```

8. 下载这些 chunk 并提取操作 id：

```bash
curl -s -o chunk.js "<chunk url>"
grep -ohE 'queryId:"[A-Za-z0-9_-]+",operationName:"[A-Za-z]+",operationType:"[a-z]+"' chunk.js | sort -u
```

关键的两个文件通常是 `bundle.BookmarkFolders.<hash>.js` 和 `shared~bundle.BookmarkFolders~bundle.Bookmarks.<hash>.js`。

9. 用新值更新 `scripts/bookmark_folders.py` 里的 `OPS` 表和上面的操作表，并更新提取日期。

## 已知陷阱

- **bearer token 必须引用 `dft.DEFAULT_BEARER_TOKEN`，不要手抄。** 它在 `device_follow_timeline.py:29-31` 是跨两行的字符串拼接，`grep` 单行只会拿到前半截；用半截 token 会稳定返回 `401 code 32 Could not authenticate you`，而这个症状极容易被误判成 cookie 失效或缺少预热请求。
- **不需要"预热"请求。** 曾有过先打一次 REST endpoint 才能成功的说法，实测是 bearer token 截断造成的假象——token 正确时直接调 GraphQL 即可。
- `cf_clearance` cookie 过期会被 Cloudflare 拦截，此时在 Chrome 里正常打开一次 x.com 即可刷新。
- 写操作有账号风控风险。本 skill 覆盖收藏夹整理与取消收藏这类低频操作；发推、关注、拉黑、改资料等一律不提供。

## 不提供的操作

以下操作风险更高，刻意排除：

- 发推、回复、关注、取关
- `BookmarksAllDelete`（清空全部书签）
