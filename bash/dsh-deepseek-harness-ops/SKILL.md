---
name: dsh-deepseek-harness-ops
description: Operate dsh on WSL systemd — boot, autostart, market proxy.
---

# DeepSeek Harness (dsh) operations

DeepSeek Harness (`dsh`, installed at `~/.npm-global/bin/dsh`, versioned e.g. `0.1.1-rc.2`) is a Cordis-based agent harness. On this box it runs as a **user systemd service** (`~/.config/systemd/user/dsh-web.service`), web UI on `127.0.0.1:3080`. WSL user manager has `Linger=yes`, so it starts at boot without any login session.

## The three recurring failure modes (and root causes)

### 1. `dsh web` exits instantly when launched from Hermes/background/non-TTY shell
`dsh` boot loads a `dsh-tui` plugin (`@deepseek-harness-tui/dsh-tui`) which refuses to load unless `process.stdout.isTTY`:
```
Error: dsh-tui requires an interactive terminal (stdout must be a TTY).
```
Only visible with `pty=true` in Hermes — with `background=true` (no TTY) the process dies silently and the error is swallowed.

**Fix (permanent):** disable `dsh-tui` via the profile patch layer `~/.dsh/profiles/web/cordis.patch.yml`:
```yaml
- id: dsh-tui
  disabled: true
```
`dsh web --dump-config` shows entry ids (`- id: dsh-tui`). This is the documented seam ("Edit cordis.patch.yml, not cordis.yml").

### 2. Plugin market "插件目录加载失败，稍后重试 / The operation was aborted due to timeout (30s, 2 attempts)"
dshmarket fetches its catalog from `https://awesome-dsh-plugin.com/plugins.json`. Two traps:
- **Node's global `fetch` IGNORES `HTTP_PROXY`/`HTTPS_PROXY` entirely.** dshmarket's `marketFetch` (in `node_modules/dshmarket/lib/net.js`) deliberately routes through undici's `EnvHttpProxyAgent` — but ONLY when those env vars are present (`configuredProxy()` reads them). Unset → falls back to bare global `fetch` (direct connection).
- **systemd user services do NOT inherit exported proxy env from your shell.** The service runs with only the env you hardcode via `Environment=`.

So a service started from an interactive shell that happens to have proxy env exported works; one started by systemd with no `Environment=` lines has neither proxy nor a reliable direct route and times out.

**Fix:** add to `~/.config/systemd/user/dsh-web.service`:
```
Environment=HTTP_PROXY=http://127.0.0.1:7890
Environment=HTTPS_PROXY=http://127.0.0.1:7890
```
then `systemctl --user daemon-reload && systemctl --user restart dsh-web`. Env is read once at process start.

**Verify** without screenshotting the UI — hit the registry endpoint directly:
```
curl -sS http://127.0.0.1:3080/dsh-market/registry -w "%{http_code} %{time_total}s\n"
# expect 200, fast — ~0.4s — and a JSON blob with "count":1884
```
The catalog is fetched fresh (no bundled fallback) — network failure returns HTTP 502 with the message, matching the UI error.

### 3. Duplicate enabled services → EADDRINUSE crash loop
Two units had both been `enabled` against `default.target` (`dsh.service` old + `dsh-web.service` new); both try port 3080. The loser restarts forever with `listen EADDRINUSE`. A shell-launched orphan can also hold the port and starve systemd.

**Fix:** inspect `systemctl --user is-enabled <unit>`, remove the stale unit's symlink + file, `daemon-reload`, confirm only one `enabled`. Kill any orphan `node .../dsh web` not owned by systemd before checking status.

### 4. Browser "bundle script /plugins/<pkg>/client.js?rev=… failed to load" — the named plugin is usually innocent
`dsh-client-modules` loads every client bundle via `<script src="/plugins/<id>/client.js?rev=<sha1-12>">`; a script `error` event (HTTP 404/connection refused) surfaces as `client-modules: bundle script … failed to load` and the UI blames the first plugin in the boot manifest. The `/plugins/*` route 404s when `clientPath` isn't in the registry — which happens when **host boot died earlier on another plugin's import error**, so nothing got registered. The rev is `sha1(bundle).slice(0,12)`; verify the bundle itself is fine by hashing `lib/client.js` — if it matches the URL's rev, stop suspecting that plugin.

**Fix:** reproduce host-side to see the real exception:
```bash
cd ~/.dsh/profiles/web && timeout 30 dsh web --host 127.0.0.1 --port 3081 --no-open
# look for: "plugin tree failed to load: failed to import loader entry <id> (<pkg>): <real error>"
```
Observed root cause: a plugin linked into the profile (`node_modules/@scope/pkg -> /home/user/projects/pkg`) whose `lib/index.js` imports a peer dep (`@deepseek-ai/schemastery`) — pnpm's strict layout resolves a linked package's peers against its **real path**, not the profile's node_modules, so the peer is invisible.

**Verified fix paths (2026-08-31):**
- `dsh plugin --profile web add link:<path>` — **does NOT fix it**. pnpm 11 `link:` is a pure symlink, no peer wiring, same error after reinstall.
- Working: symlink the missing peers into `<project>/node_modules/` yourself. Profile root only has `@deepseek-ai/{cordis,schemastery,cosmokit}`; the rest (`dsh-settings`, `dsh-host-webserver`, `dsh-client-runtime`, `dsh-client-ui-settings`, `dsh-client-locale`, `dsh-web`, …) live under the global dsh install: `~/.npm-global/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai/<pkg>`. Link the whole peerDependencies list in one pass — fixing one at a time just surfaces the next.
- Verify by actually booting and curling the bundle, not just process-alive: `curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:<port>/plugins/<@scope>/<pkg>/client.js` → 200. dsh web needs a TTY; under Hermes `background=true` it dies silently, wrap with `execute_code` + `subprocess.Popen(..., start_new_session=True)` to health-check.

### 5. dsh 升级到 0.1.2-rc.x 后 linked 插件 `disabled: true` 也炸 boot（"plugin(s) failed to load: <name>, <name>"）
新版 dsh-app-boot 的 `assertEntriesLoaded` 审计所有 fiber 为空的 entry；linked 插件（`link:` dep）在升级后 fiber 永远为空，**即使 patch 里 `disabled: true` 也一样**（dump-config 显示 entry 正常、disabled 生效，但 boot 仍 reject，且名字重复出现两次）。这不是配置写错，是上游 loader 回归。

**Fix（2026-09-05 验证）：** 别试图在 cordis.patch.yml 里 disable —— 直接把插件从 `~/.dsh/profiles/<profile>/package.json` 的 `dependencies` 和 `dsh.profile.bundles` 两处删掉，再删掉 patch 里对应的 disabled entry。`dsh web` 试 boot 验证。

**同类：** `@nanmicoder/dsh-agent-teams` ≤0.1.15 调 `ctx.subagents.registerContinuableSetup`（新版 dsh 已移除）——同样必须整个移除，patch disable 无效。升级 dsh 后所有第三方 bundle 都要按这个模式过一遍：boot 挂 → 看 journal 里 "failed to apply loader entry <id>" → 从 package.json 两处删掉。

**同类：** 两个插件注册同一个 webserver 路由前缀也会整个炸 boot（`webserver: duplicate prefix route "<prefix>"`，例：套件包里的子插件与 `dsh-better-sidebar` 同抢 `/sidebar/api`）——无法 disable 其一绕过，同样整个移除冲突的那方。另外手动 `dsh web` 测试实例与 systemd 实例共用 `$DSH_HOME` 会触发 `dsh-im-gateway 检测到另一个 DSH 进程…并发写坏 session log` —— 测试 boot 必须设独立 `DSH_HOME`。

**同类：** 插件 import 的命名导出被新版 dsh 子包删掉（`The requested module '@deepseek-ai/<pkg>' does not provide an export named '<x>'`）——不是配置问题，是插件版本 < dsh 版本。查该插件 npm 新版是否已修（`npm view <pkg> peerDependencies` 看 range 是否覆盖当前 dsh 版本），有就升，没有就移除。例：dshmarket ≤1.36 import `installSettingsSection`（dsh-settings 0.1.2 已删），1.37+ 修好。

**0.1.7 新症状（2026-09-29 验证）：** link: 插件即使 patch 里早有 `disabled: true`，升级后首次 boot 会以随机 hash id（如 `c2eccf5f`）被强制激活——若它注册 webserver 路由则报 `duplicate exact route`（entry id 是 hash 不是 patch 里的 id，这就是 disable 没拦住的证据）；之后 boot 变成 `failed to import` 警告（fiber undefined 但 entry.disabled 求值为 falsy，dump-config 却显示 disabled: true——dump 与运行时对 link: 条目不一致）。修法不变：三处（dependencies + bundles + patch）整个移除。

**0.1.7 session format v4：发消息时报「本轮运行失败 format v4 message requires a producer-owned source kind」**——插件注入消息还在用 v3 旧 source 形状 `{kind:"plugin", plugin:"..."}`，v4 追加事件时拒收。运行期错误不进 journal，只在 UI。排查：grep 插件目录 `kind: "plugin"`。修法：升插件（例：@openviking/dsh-memory-plugin 0.3.x→0.5.8 已修，peer 覆盖 ^0.1.7-rc.2；0.x caret 不自动跨 minor，要手动改 package.json 版本再 `pnpm install --config.minimumReleaseAge=0`）。没新版就手改：source 改 `kind: "plugin:<name>"` 并同步改插件里所有 `kind === "plugin"` 判断点。

### 7. 升 0.1.7-rc.2 后插件页出现「异常」+ 市场 React #130 崩（2026-09-29 验证）
**查法：** UI 里 设置→插件→点异常条目的「查看」读「原因」。dsh 0.1.7 新增 plugin manager 兼容审计（`evaluatePluginCompatibility`，读插件 package.json 的 peerDependencies dsh range）——peer 不满足整包判 problem，组件不加载。

- **`@linxin666/dsh-web-all@0.4.4` 是为未发布的 dsh 0.2.0-rc.1 提前发的（peer `>=0.2.0-rc.1`，0.2.0 还是 next 不是 latest）**。`^0.4.3` 会解析到 0.4.4 → 与 0.1.7-rc.2 不兼容 → 异常，市场 UI（其组件 `dsh-client-ui-market`）整包不加载。**修法：package.json 钉死 `"@linxin666/dsh-web-all": "0.4.3"`（去 caret）再 install。注意：市场里「全部更新」会把它升回 0.4.4 再炸——dsh 0.2.0 进 latest 前别接它。**
- dshmarket 1.66.x 会在更新前弹同类兼容确认框（“X 声明需要 DSH >=0.2.0-rc.1，你运行 0.1.7-rc.2，已停止”）——这是拦截成功不是 bug，别点「仍可继续更新」。消除提示：市场「已安装」页将该包 **屏蔽/忽略**（「已屏蔽」页可找回）。
- **dshmarket 1.45.1 客户端对 0.1.7 的 client runtime 崩 `Minified React error #130`**（组件 import 到 undefined，ui primitive 变了）。升级 → `pnpm add dshmarket@latest --config.minimumReleaseAge=0`（1.66.5，2026-09-28 发，晚于 dsh 0.1.7-rc.2，修好了）。
- **验证市场 UI 不要靠猜**：市场界面在 设置→插件市场（`settings.section` slot 注入，不在插件页）。「添加插件」按钮弹的是官方包名安装对话框，不是市场——两件事。
- peer 警告里 `@linxin666/* peer @deepseek-ai/dsh` / super-injector / find-plugin 的 "missing peer" 是 profile 布局的老问题（全局 dsh 运行时提供），无视。

**pnpm `minimumReleaseAge` 拦截：** pnpm 11 该策略会拒装/拒验证最近发布的包，报错 `was published at ... within the minimumReleaseAge cutoff`，且 `pnpm config get` 各处都显示 undefined（来源不明，行为在）。一次性绕过：`pnpm install --config.minimumReleaseAge=0`（此 flag 是 dshmarket 自己的 `RELEASE_AGE_OVERRIDE` 用的同一个，安全）。

**link: 插件的 peer symlink 会在 profile `pnpm install` 后失效**——peer symlink 若指向 profile 的 `node_modules/@deepseek-ai/<pkg>`，重装即被清。一律指向全局 dsh 安装目录 `~/.npm-global/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai/<pkg>`（随 dsh 本体存在，稳定）。

### 6. "401 authentication required" ≠ 坏了 —— token 是一次性登录，不是每次都要
用户报"又进不去了"时先区分 401 和 crash loop：`curl -sS -o /dev/null -w "%{http_code}\n" http://127.0.0.1:3080/` 返回 **401 表示服务健康**（只是要登录），别去翻 plugin 错误。dsh-client-connection 的认证流程：launch token 只在 `GET /` 被接受一次，验证后签发 **30 天有效**的签名 cookie（`cookieMaxAgeDays: 30`，密钥存 `~/.dsh/.credentials.yaml`，重启不变），然后 302 到干净的 `/`。所以正确姿势是带 token 开一次 → 之后收藏裸 `http://127.0.0.1:3080/`。需要重登的触发条件只有：cookie 过期（30 天）、清了浏览器 cookie、删了 `.credentials.yaml`。不要建议关认证——它是防 DNS rebinding 的唯一屏障。取当前 token 一行：`journalctl --user -u dsh-web --no-pager | grep "dsh web: http" | tail -1 | grep -oP 'http\S+'`。

## Diagnostic order (fastest first)
0. **先分清 401 vs crash**：`curl -sS -o /dev/null -w "%{http_code}\n" --max-time 3 http://127.0.0.1:3080/` 返回 401 = 服务健康（只是要登录），问题在 token/cookie，不翻 plugin 错误；000/拒绝连接 = 真崩了，继续往下。
1. `curl ...`（同上）— is it even up?
2. `systemctl --user is-active dsh-web; systemctl --user is-enabled dsh-web`
3. `journalctl --user -u dsh-web -n 30 --no-pager` — crash reason (EADDRINUSE vs plugin-load vs TTY)
4. `ss -tlnp | grep 3080` + `lsof -i :3080` — who holds the port (orphan node vs systemd)

## Health commands
```bash
systemctl --user status dsh-web --no-pager    # active/running + Main PID
loginctl show-user po | grep Linger           # must be yes for boot autostart
```

## Support files
- `references/node-proxy-and-systemd-env.md` — the Node-fetch-ignores-proxy lesson generalized (any service whose child reads HTTP_PROXY from env, not as `Environment=`).
- `references/cli-plugin-add-failures.md` — three traps when `dsh plugin add` fails: pnpm-store version, lockfile `resolution: {integrity}` missing for GitHub-release tarballs, and `dsh plugin` CLI not forwarding `RELEASE_AGE_OVERRIDE` (with the `AbortSignal.timeout(string)` landmine).

## Pitfalls
- `dsh web` from Hermes `background=true` dies silently (no TTY). Use `pty=true` for a one-shot foreground check.
- Proxy env is read at process start; `export` after start (or `systemctl restart` without env) won't help. Confirm via `/proc/<pid>/environ`.
- `cordis.patch.yml` uses `!!js` for expressions — a `disabled: !!js !process.stdout.isTTY` YAML-parse error was hit ("duplication of a tag property") — use plain `disabled: true`.
- Don't strip `--no-open` in systemd ExecStart or the server tries to launch a browser.
- **`dsh plugin add` errors are deceptively generic ("pnpm failed").** Three independent root causes (store version, lockfile integrity, missing CLI override) all surface the same exit. See the reference for triage — start with `pnpm --version` and `grep '^    resolution:' pnpm-lock.yaml | grep -v integrity`.
- **`--config.fetchTimeout=<ms>` in pnpm 11 traps you** — pnpm passes the value as a string to `AbortSignal.timeout()`, which throws `ERR_INVALID_ARG_TYPE` and retries forever. Do not add this flag to override lists; pnpm's default 60s is fine.
- **`dsh plugin` CLI gap vs dshmarket UI:** `bin.js` does not forward `--config.minimumReleaseAge=0`. UI routes do (see `dshmarket/src/install.ts`). CLI users get hit by `pnpm-workspace.yaml`'s 1-day cutoff. Until upstream patches this, `bin.js` needs a local override (see reference).

## Pitfalls
- `dsh web` from Hermes `background=true` dies silently (no TTY). Use `pty=true` for a one-shot foreground check.
- Proxy env is read at process start; `export` after start (or `systemctl restart` without env) won't help. Confirm via `/proc/<pid>/environ`.
- `cordis.patch.yml` uses `!!js` for expressions — a `disabled: !!js !process.stdout.isTTY` YAML-parse error was hit ("duplication of a tag property") — use plain `disabled: true`.
- Don't strip `--no-open` in systemd ExecStart or the server tries to launch a browser.