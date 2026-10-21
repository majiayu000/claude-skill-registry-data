---
name: cf-pages-deploy
description: 把 GitHub 上的纯静态前端仓库（HTML/CSS/JS、无构建）一键部署到 Cloudflare Pages，生成国内免翻墙可访问的 *.workers.dev 地址，且后续 push 自动同步。适用于用户要求"国内镜像""免注册点开就看""映射一份到国内"等场景。Gitee Pages 已永久下线，不要再试。
---

# CF Pages 一键部署国内镜像

## 何时用
- 用户说"部署到国内""国内镜像""免翻墙打开""映射一份到国内网页"
- 仓库是纯静态（index.html 在根目录，无 npm build）
- 本地 `git push` 被 GFW 443 卡住，必须走 GitHub MCP

## 死路清单（别再试，浪费时间）
- ❌ **Gitee Pages**：2023 年起因监管永久下线，新账号菜单里根本没有入口（官方 issue I9RGKI / IA6DQ6 / I6YDKR 确认）
- ❌ **gh-proxy.com / ghfast.top / ghproxy.net**：只代理 raw 文件，不代理 `*.github.io` 整站，全部 403/404
- ❌ **本地 git push origin**：GFW 443 必挂，改用 MCP `push_files`

## 标准流程（10 分钟）

### 1. 确认仓库有 index.html
用 MCP `get_file_contents` 看根目录，必须有 `index.html`。Python 技能包、纯 README profile 仓库跳过。

### 2. 浏览器登录 Cloudflare
- 打开 https://dash.cloudflare.com
- 用 GitHub OAuth 登录（**注意：Chrome 可能登错账号，先去 github.com 确认是目标账号，再回 CF**）
- 路径：左侧 Compute → Workers & Pages → Create application → Connect GitHub

### 3. 授权 GitHub App
- 弹窗里确认账号名是用户本人（不是另一个 GitHub 号）
- 选 "All repositories" 或 "Only select repositories" → Install & Authorize

### 4. 选仓库
- 下拉选目标 repo → Next
- Project name 默认（会变成 `<name>.<account>.workers.dev`）
- Build command **留空**，Root directory `/`
- 点 Deploy

### 5. 拿地址
- 构建 25s 左右完成（绿勾）
- 点右上角 Visit，URL 形如 `https://<project>.<account>.workers.dev/`
- 这就是国内免翻墙地址

### 6. 自动同步
- Cloudflare 已绑定 GitHub，以后每次 `git push origin main` 自动重新部署，**零操作**

## 常见坑
- **Chrome 登错 GitHub 账号**：OAuth 弹窗显示的账号不是用户的 → 去 github.com 头像 → Sign out from all accounts → 重新登录目标账号 → 回 CF 重来
- **新 Workers 流程要 Build command**：纯静态项目直接留空即可，CF 自动识别
- **国内访问速度**：workers.dev 电信联通秒开，移动偶尔慢；要更快就绑自定义域名（CF 后台 Domains 加 CNAME）
- **"Missing git connection" 报错**：GitHub App 已选 All repositories 仍报此错，是 CF 前端缓存。**刷新当前创建页（F5）后重走一遍选仓库流程即可**，不要去 GitHub 改授权，权限本来就有。
- **点仓库旁箭头跳转 github.com 是对的**：用来确认仓库存在和 index.html 位置，不是让你在那授权。

## 已部署清单（jin2004-cmd 账号，2026-10-17）
| 仓库 | 国内镜像地址 |
|---|---|
| talkcal | https://talkcal.jinjiaxin2004.workers.dev/ |
| ai-video-portfolio | https://ai-video-portfolio.jinjiaxin2004.workers.dev/ |
| ad-compliance-checker | https://ad-compliance-checker.jinjiaxin2004.workers.dev/ |
| ecom-script-agent | https://ecom-script-agent.jinjiaxin2004.workers.dev/ |
| daypilot | https://daypilot.jinjiaxin2004.workers.dev/ |

跳过的仓库：jin-memory-sync（私人记忆）、codex-practical-skills（Python 技能包非网站）、jin2004-cmd（profile README）、awesome-claude-skills / awesome-codex-skills（fork）。

## 相关工具
- GitHub MCP `push_files`：本地 git 不通时用它推代码
- GitHub MCP `get_file_contents`：确认仓库结构
- 浏览器：`computer_use_tool` plane="cu" 驱动 Chrome
