---
name: dianping-explore
description: Auth-first Dianping merchant discovery and low-volume review sampling. Use when Codex needs to search Dianping shops, collect a small public review sample, wrap an existing Dianping crawler, prepare the local Playwright runtime, normalize CSV/JSONL output, or troubleshoot Dianping crawler login, cookie, and environment setup; if cookies are missing, prefer the visible login helper before any fallback.
---

# Dianping Explore

帮助用户以低频、人工可控的方式搜索大众点评商户并导出少量评论样本。技能本身只提供流程、包装器、环境检查和输出规范；第三方爬虫源码应放在技能目录外，由 `scripts/cli.py setup-source` 克隆或由用户指定。

## 技能边界

所有操作优先通过本技能目录执行：

```powershell
python scripts\cli.py <子命令>
```

不要把 Cookie、账号、代理密钥或浏览器 profile 写入 skill 仓库。不要在回答里输出 Cookie。不要做高频、大规模、绕过验证码或绕过访问控制的采集。遇到验证码或风控页面时，暂停并要求用户在可见浏览器中手动处理；不能自动破解。

Auth-first is the default. If a requested Dianping collection needs cookies and `DIANPING_COOKIE` is missing, run the visible login helper and let the user complete login/CAPTCHA/MFA before collecting. Do not silently fall back to no-auth/public snippets or conclude that comments were not collected merely because cookies were initially absent. For review collection, fail closed when visible login is declined or fails; use public/discovery fallback only when the user explicitly asks for discovery-only work.

默认第三方适配源是 `HDdssX/dianping_crawler`。它必须安装在外部目录，例如 `%LOCALAPPDATA%\Codex\dianping-explore\HDdssX_dianping_crawler`，并通过 `DIANPING_CRAWLER_ROOT` 或 `--crawler-root` 指向。更多适配说明见 `references/third-party-adapters.md`。

CLI 会自动读取技能私有 `.env`：`%USERPROFILE%\.codex\skills\dianping-explore\.env`。这个文件只能保存在用户级目录，不能提交进 repo。

## 子命令

| 子命令 | 用途 |
|---|---|
| `setup-source` | 克隆默认第三方爬虫到外部目录，可选创建 venv 和安装依赖 |
| `status` | 检查爬虫目录、关键文件、Python/venv、Cookie 环境变量是否就绪 |
| `run-crawler` | 调用现成爬虫搜索商户并采集少量评论，默认使用可见浏览器 |
| `normalize-csv` | 将第三方爬虫输出 CSV 规范化为 JSONL |
| `schema` | 输出本技能的规范化结果字段 |

## 常用流程

### 1. 准备第三方爬虫

```powershell
python scripts\cli.py setup-source --with-venv
```

如需安装 Playwright 浏览器：

```powershell
python scripts\cli.py setup-source --with-venv --install-browser
```

也可以使用 PowerShell 辅助脚本：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_dianping_explore.ps1 -WithVenv -RunSmoke
```

### 2. 配置 Cookie / 可见登录

默认不要要求用户复制粘贴 Cookie。用登录辅助脚本打开可见浏览器；用户在浏览器中完成登录/验证后，程序会自动检测登录 Cookie 并保存本次 Playwright 会话里的大众点评 Cookie。不要回到终端按 Enter；这个 helper 不依赖终端 stdin。

```powershell
powershell -ExecutionPolicy Bypass -File scripts\assist_dianping_cookie.ps1
```

这个辅助脚本不会读取现有 Chrome/Edge profile，不需要用户复制粘贴 Cookie，也不会打印 Cookie 值。它只写入技能私有 `.env`。

默认要求检测到登录标记后才保存 Cookie。如果站点改版导致已登录但标记识别失败，先报告阻塞；只有在用户确认浏览器里已经登录后，才可用 `-AllowUnverifiedSave` / `--login-allow-unverified-save` 作为人工确认逃生口。

`run-crawler` 也会走同一条主流程：如果 `DIANPING_COOKIE` 缺失，默认自动打开可见登录助手，用户完成验证后自动保存并继续爬虫。这个流程不依赖终端 stdin。显式传入 `--no-auto-login` 只会禁用自动登录并失败关闭，不会改走无 Cookie 评论采集。

### 3. 检查状态

```powershell
python scripts\cli.py status
```

### 4. 低频采集

先从很小样本开始：

```powershell
python scripts\cli.py run-crawler `
  --keyword "咖啡" `
  --cities "Shanghai" `
  --max-pages 1 `
  --comment-pages 1 `
  --output ".\outputs\dianping-coffee.csv"
```

`run-crawler` 会打开有头浏览器。若出现验证页面，请让用户手动完成验证，再回到终端继续。采集完成后再进入规范化步骤。

### 5. 规范化输出

```powershell
python scripts\cli.py normalize-csv `
  --input ".\outputs\dianping-coffee.csv" `
  --output ".\outputs\dianping-coffee.jsonl"
```

规范化字段见：

```powershell
python scripts\cli.py schema
```

## 结果呈现

向用户汇报时优先给：

- 运行目录和输出文件路径。
- 采集范围：关键词、城市、页数、评论页数。
- 结果摘要：商户数、评论数、字段是否完整。
- 风控状态：是否出现验证码、是否需要用户手动登录或更换更小范围。

## 失败处理

- **找不到爬虫目录**：运行 `setup-source`，或让用户提供 `DIANPING_CRAWLER_ROOT`。
- **Cookie 未配置**：默认运行 `scripts\assist_dianping_cookie.ps1` 或让 `run-crawler` 自动触发可见登录；不要要求用户在聊天里粘贴真实 Cookie，不要直接降级到 fallback。
- **依赖缺失**：运行 `setup-source --with-venv --install-browser`。
- **验证码/安全验证**：暂停，要求用户在可见浏览器中手动处理。
- **无结果或字段缺失**：缩小城市/关键词/页数，先跑 `--max-pages 1 --comment-pages 1`。
- **需要换底层项目**：读取 `references/third-party-adapters.md`，按相同 CLI 输出契约新增适配，不要把第三方源码直接提交进 skill 仓库。
