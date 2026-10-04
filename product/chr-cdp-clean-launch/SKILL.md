---
name: chr-cdp-clean-launch
description: 在 macOS 上从 Hermes/terminal 干净启动 Chrome CDP，避免被 benign ERROR 日志与重复实例误导。
version: 1.0.0
author: hermes
license: MIT
---

# Chrome CDP 干净启动

用于：需要在 macOS 上起 `Google Chrome --remote-debugging-port=PORT`，但 Hermes 背景进程被 Chrome 的噪音日志刷屏，或端口/实例冲突。

## 结论先行

1. 起长驻 Chrome 时，用 `terminal(background=true)`；不要在前台命令里自己加 `&`。
2. 不要给 Chrome 进程挂 `watch_patterns: ["ERROR"]`。Chrome 常年会输出 benign 噪音：
   - `ssl_client_socket_impl.cc ... net_error -100`
   - `Crashpad/settings.dat: No such file or directory`
   这会导致 Hermes 持续系统通知，污染会话。
3. 启动前先杀旧的同端口/旧 profile 实例，否则常见：`bind() failed: Address already in use (48)`。
4. 若日志已出现 `DevTools listening on ws://...`，则 CDP 基本已活；即使 `curl http://127.0.0.1:PORT/json/version` 一时为空，也别先被后台 `ERROR` 误导。优先检查是否绑在 IPv6 `::1`。

## 推荐流程

### 1) 先清旧实例

```bash
pkill -f '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome --remote-debugging-port=19825' || true
pkill -f '/tmp/bb-browser-profile' || true
pkill -f '~/.bb-browser/browser/user-data' || true
mkdir -p /tmp/bb-browser-clean
```

按实际 port/profile 改。

### 2) 背景启动，禁用大部分后台噪音源

```bash
'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
  --remote-debugging-port=19825 \
  --user-data-dir=/tmp/bb-browser-clean \
  --no-first-run \
  --no-default-browser-check \
  --disable-background-networking \
  --disable-background-timer-throttling \
  --disable-breakpad \
  --disable-component-update \
  --disable-domain-reliability \
  --disable-features=AutofillServerCommunication,CertificateTransparencyComponentUpdater,OptimizationHints,MediaRouter,Translate,ChromeWhatsNewUI \
  --disable-sync \
  --metrics-recording-only \
  --no-pings \
  --password-store=basic \
  about:blank
```

在 Hermes 里应用：
- `terminal(background=true, ...)`
- `watch_patterns` 最多只挂 `"DevTools listening on"`
- 不挂 `"ERROR"`

### 3) 验证

优先顺序：

1. `process(action="poll")` 看日志里是否已有 `DevTools listening on ws://...`
2. 再试：
   - `curl -s http://127.0.0.1:19825/json/version`
   - 若空，再试 IPv6：`curl -g -s 'http://[::1]:19825/json/version'`
3. 再看进程：

```bash
ps -ef | grep -i '[G]oogle Chrome.*19825'
```

## 常见误判

### 1. `ssl_client_socket_impl.cc ... net_error -100`

多为 Chrome 后台联网/证书握手失败。通常不影响你眼前的网页调试，也不代表 CDP 挂了。

### 2. `Crashpad/settings.dat: No such file or directory`

多为 Google 组件/Crashpad 上报目录缺失。属噪音，不是主流程致命错。

### 3. `bind() failed: Address already in use (48)`

端口已被旧实例占用。先杀旧实例；若不想清理，换新端口。

### 4. Hermes 一直弹系统消息

通常是你给 Chrome 后台进程挂了 `watch_patterns: ["ERROR"]`。直接 kill 该 background process，重起时删掉此 watch。

## 最小排障决策

- 看到 `DevTools listening`：先继续，不要因噪音停手。
- 没看到 `DevTools listening` 且端口空：杀旧实例，重起。
- 已活但通知泛滥：kill 背景 watcher，静默重起。

## 适用场景

- Hermes 里准备接真实 Chrome/CDP
- bb-browser / 自建 Chrome remote-debugging 启动混线
- 会话被 Chrome `ERROR` 噪音淹没时

## 重要分流：不要误开洁净 profile

若用户明确要“当前正在用的 Chrome / 已登录账号 / 现有指纹”，本技能只能用于排障与验证，不能直接默认起 `--user-data-dir=/tmp/...` 的洁净实例。

先判定目标是否为用户真 profile：

1. 查 `~/Library/Application Support/Google/Chrome/Default/Preferences`
   - `profile.name` 可确认本地 profile 名
   - `account_info[0].full_name` / `email` 可确认已登录账号
2. 查 `~/Library/Application Support/Google/Chrome/Local State`
   - `devtools.remote_debugging.user-enabled` 可确认是否已允许 remote debugging
3. 若目标是现有登录态：
   - 优先接管该 `Default` profile 对应的现有 Chrome
   - 不要先开 `/tmp/bb-browser-clean` 一类新 profile
   - 若必须重启 Chrome 才能挂 CDP，应先向用户确认会影响当前窗口/会话

经验结论：
- 用户说“我只有一个 Chrome，登录了某账号”时，默认目标是 `~/Library/Application Support/Google/Chrome/Default`
- 误开洁净 profile 会直接偏离真实登录态，即便 CDP 技术上可用，也不满足任务目标
