---
name: agent-chrome
description: |
  本机 AI 浏览器自动化的统一 Chrome 启动器与约定：每个登录态一个 profile（~/.chrome-profiles/<站点>-<别名>），用正式版 Google Chrome 在固定 CDP 端口上 up/down，agent-browser、Playwright、python CDP 都只连端口、不自己起浏览器。Use when 需要浏览器自动化、需要某网站的登录态、要起 Chrome / 开 profile / 拿 CDP 端口、接 agent-browser --cdp、Playwright connectOverCDP、登录过期要重新登录或从主 Chrome 引导 cookie、新增一个网站账号。
trigger: /agent-chrome
compatibility: Claude Code, Codex (macOS)
license: MIT
---

# agent-chrome

一个脚本管所有带登录态的自动化 Chrome：`scripts/agent_chrome.py`（python3 标准库；种 cookie、开后台窗口、优雅关闭用 Node ≥ 22 内置 WebSocket）。

## 约定

1. **二进制**：需要登录态的一律用正式版 `/Applications/Google Chrome.app`。Chrome for Testing / Playwright 自带 Chromium 只用于无登录的渲染测试。
2. **根目录与命名**：profile 都在 `~/.chrome-profiles/`（`$AGENT_CHROME_ROOT` 可改），登记在 `registry.json`。名字一律 `<站点>-<别名>`，首个账号别名固定 `main`（`x-main`、`goofish-main`），永不用裸站点名；`site_defaults` 把站点简名映射到默认 profile，所以 `up x` 等于 `up x-main`。
3. **登录态只存 profile 一份**：不导出 cookie 文件、不用 `--state` / `--session-name` 另存、不每次注入。
4. **主 Chrome 只读**：用户自己的 Chrome 不启动、不 kill、不写；只在 `seed --from-main` 时复制它的 Cookies 库读一次，作为新 profile 的首次引导。
5. **启动与端口**：端口池 19300–19399，登记时分配、固定不变；禁用 9222。headless 优先；有头窗口用 `open -g` + 无启动窗口 + CDP 后台开窗，不抢焦点。
6. **生命周期**：用前 `up`，用完 `down`（走 Browser.close，cookie 才落盘）。脚本里只 `down` 自己拉起的（`up` 输出 `reused:false`），`reused:true` 说明别人在用，不要关。`daemon:true` 的常驻 profile 没有 `--force` 拒绝关闭。
7. **keychain 自动识别**：Playwright 建的 profile 用 mock keychain 加密 cookie，正式 Chrome 建的用系统钥匙串；`add` 时自动检测写进 registry，`up` 据此决定是否加 `--use-mock-keychain`，否则会整体掉登录。
8. **新代码只走本脚本**：老代码（registry 里 note 写着 legacy 的）逐步迁，迁之前它们仍用自带端口或 Playwright 直接起，别同时用两边打开同一个目录。

## CLI 速查

```bash
AC="$(dirname "$(readlink -f "$0")")/scripts/agent_chrome.py"   # skill 目录下的脚本
python3 "$AC" ls                                    # name/port/sites/daemon/running
python3 "$AC" add x-alt --sites x.com,twitter.com   # 新账号；--dir 已有目录名 / --daemon / --note / --default-for x
python3 "$AC" resolve x                             # -> x-main
python3 "$AC" up x --headless [--url URL]           # -> {"profile","dir","port","ws","pid","headless","reused"}
python3 "$AC" down x-main [--force]
python3 "$AC" status [x-main]                       # running/pid/port/headless/started/occupied_by_other
python3 "$AC" seed x-main --from-main --domains x.com,twitter.com
bash "$(dirname "$AC")/test_agent_chrome.sh"        # 改脚本后跑，临时根目录，全 headless
```

失败时退出码非 0，stderr 一句中文原因。`down` 例外：Browser.close 走不通（缺 node、helper 超时）时降级为 SIGTERM，仍关掉浏览器，stderr 提示最近的 cookie 改动可能没落盘，退出码 0。目录被别的 Chrome 占着（端口不对）时只报 pid，不杀。

## 接法

**agent-browser**：每条命令带 `--cdp <port>`，并用独立 `--session`；`close` 在 `--cdp` 下只断开，不关浏览器。

```bash
PORT=$(python3 "$AC" up x --headless | python3 -c 'import json,sys;print(json.load(sys.stdin)["port"])')
agent-browser --session my-task --cdp "$PORT" open https://x.com/home
agent-browser --session my-task --cdp "$PORT" get title
```

**Playwright（Node）**：`chromium.connectOverCDP`，用已有 context，不要 `launch*`。

```js
const { port } = JSON.parse(execFileSync("python3", [AC, "up", "x", "--headless"], { encoding: "utf8" }));
const browser = await chromium.connectOverCDP(`http://127.0.0.1:${port}`);
const page = browser.contexts()[0].pages()[0] ?? await browser.contexts()[0].newPage();
```

**python CDP**：取 `ws` 字段直连浏览器级 WebSocket，或用 Playwright for Python 同样 `connect_over_cdp`。

```python
info = json.loads(subprocess.check_output(["python3", AC, "up", "x", "--headless"]))
browser = sync_playwright().start().chromium.connect_over_cdp(f"http://127.0.0.1:{info['port']}")
# 或者裸 CDP: websocket 连 info["ws"]，发 {"id":1,"method":"Target.getTargets"}
```

## 登录过期

业务脚本发现登录页时不要自己尝试登录，打印下面两条之一交给用户：

1. **有头扫码**：`python3 "$AC" down <name>`（若在跑）→ `python3 "$AC" up <name> --url <登录页>`，窗口在后台打开，告诉用户去 Chrome 里扫码 / 输验证码，完成后 `down <name>`。
2. **从主 Chrome 引导**：用户的主 Chrome 已登录同一账号时，`python3 "$AC" seed <name> --from-main --domains <主域,...>`。只读复制主 Chrome 的 Cookies 库，用钥匙串（首次可能弹授权框）解密后经 CDP 写进 profile，打印导入条数；之后登录态就只在 profile 里续期。

新增账号同理：`add <站点>-<别名>` 后用上面任一方式登录一次。
