---
name: star-gratitude
description: Star a third-party skill or project the user found useful. Use when the user says a skill or project is good/useful/worth keeping (e.g. "这个skill真好用", "值得star", "想给它点个star", "想收藏"), asks to star/like/favorite a repo, mentions a skill or project they enjoyed using and want to support, or invokes a third-party skill for the first time in this session.
---

# Star Gratitude

给「用着好用」的第三方 skill 或项目点 GitHub star，别让感谢被遗忘。核心纪律：**先提醒、确认后再 star**，绝不擅自代表用户执行公开动作。

## 触发时机

- **第一次调用**：本会话第一次调用某个第三方 skill（来自插件、`~/.agents/skills`、`~/.dsh/skills` 或项目 skills 目录）时，按「工作流 A」提醒；
- **用户明确提起**：用户明确要求 star / 收藏，或表示某个 skill 或项目好用、值得支持时，按「工作流 B」处理。

不要因为会话中「用到了」某个第三方工具（非首次）就主动触发；用户没提、也不是首次调用，就不提。

## 查重（两种触发都先做）

在 `~/.dsh/star-gratitude/log.md` 中查找该来源仓库（`owner/repo`）：

- 已有记录（无论 `✅ starred` 还是 `⏳ reminded`）→ 不重复提醒。若用户仍明确要求 star 且记录是 `⏳ reminded`，按工作流继续；若已是 `✅ starred`，直接告知「已经 star 过了」。
- 无记录 → 首次遇到，进入对应工作流。

同一会话内已提醒过的来源，后续不再提醒（会话内记在心里即可）。

## 工作流 A：第一次调用第三方 skill 时

1. 目标即**本次调用的那个 skill**。定位它的来源仓库：
   - skill 目录（`~/.agents/skills/<name>/`、`~/.dsh/skills/<name>/`、项目 `.dsh/skills/<name>/`、插件 `node_modules/<pkg>/skills/<name>/`）里读 `SKILL.md` / `README.md` / `package.json` 的 `repository`、`homepage`、`source`、`url` 字段；
   - 找不到就用 `web_search` 按 skill 名找官方仓库；仍拿不准就把候选链接报给用户确认。**不要猜一个仓库去 star。**
2. 展示 `owner/repo` + 链接，**一句话**带过提醒：「这个 skill 来自 xxx，要顺手给它 star 吗？」——不打断任务，用户没回应就继续干活。
3. 用户确认后，继续「确认与执行」；用户拒绝或暂不，记账 `⏳ reminded` 后不再重复提醒。

## 工作流 B：用户明确提起

1. 确认目标：哪个 skill / 项目？用户只说「好用」没说哪个时，先问清楚，不要猜。
2. 按「工作流 A」第 1 步的方式定位仓库。
3. 展示 `owner/repo` + 链接，等用户明确确认。

## 确认与执行（两种工作流共用）

1. **先提醒，等确认**：必须等用户明确确认，同一轮内不要执行 star。
2. 检查是否已 star：`gh api user/starred/OWNER/REPO -i`，看响应头第一行的状态行——`HTTP/2.0 204` = 已 star（告知并记账 `✅ starred` 后结束）；`HTTP/2.0 404` = 未 star，继续。注意 `gh api` **不带 `-i` 时不打印状态码**（204 完全静默、退出码 0；404 才打印 `HTTP 404`），所以判断已/未 star 一律看 `-i` 的状态行，不要靠猜。`gh` 未安装/未登录（`gh auth status` 确认）则给出 `https://github.com/OWNER/REPO` 手动链接。
3. 执行：`gh api -X PUT user/starred/OWNER/REPO`（成功时无输出、退出码 0；不放心可再跑一次第 2 步确认）。
4. `gh api` 的 flag 记不清时，用 curl 兜底（token 由 `gh auth token` 提供，不写死、不泄露）：
   - 检查：`curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $(gh auth token)" https://api.github.com/user/starred/OWNER/REPO` —— 输出 `204` = 已 star，`404` = 未 star；
   - 执行：`curl -s -o /dev/null -w "%{http_code}" -X PUT -H "Authorization: token $(gh auth token)" https://api.github.com/user/starred/OWNER/REPO` —— 输出 `204` = 成功。
5. 记账（追加到 `~/.dsh/star-gratitude/log.md`，文件不存在则先建表头）：

   ```
   - YYYY-MM-DD | owner/repo | <skill/项目名> | <一句话为什么好用> | ✅ starred
   - YYYY-MM-DD | owner/repo | <skill/项目名> | 用户未确认/拒绝 | ⏳ reminded
   ```

## 纪律

- star 是**公开动作**、用**用户自己的账号**——执行前用 `gh auth status` 确认账号无误。
- 已 star 或已提醒过 → 告知并跳过，不重复打扰。
- 拿不准仓库归属 → 问用户，不猜。
- 任何失败（网络、权限、找不到仓库）→ 给出手动链接，绝不静默放弃。
- 提醒要**轻**：一句话带过，不打断任务节奏；只有用户回应后才进入确认流程。
- `gh api` **不支持 curl 风格的 `-w` / `-o` 参数**（传了会报 `unknown shorthand flag: 'w' in -w`）；要看 HTTP 状态码用 `-i`，或改用上面的 curl 兜底，不要在 `gh api` 上套 curl 参数。
