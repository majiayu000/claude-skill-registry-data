---
name: deepseek-harness
description: DeepSeek Harness (dsh) CLI 安装、启动、launcher flag 坑、WSL 后台保活。
category: mlops
---

# DeepSeek Harness (dsh) 本地运维

DeepSeek 官方的 agent harness。架构：**everything is a plugin**，基于 [Cordis](https://github.com/cordiverse/cordis)。当前还在 developer preview，breaking changes 常见。

## 安装 / 升级

全局 npm 包 `@deepseek-ai/dsh`：

```bash
npm un -g @deepseek-ai/dsh
npm i -g --allow-scripts=@deepseek-ai/dsh-subprocess-local,koffi,node-pty,@google/genai,protobufjs @deepseek-ai/dsh@latest
```

`--allow-scripts` 必加。不加会导致 node-pty/koffi 等 5 个包的 install scripts 被拦，终端/子进程相关功能残缺。

## 启动 Web UI

```bash
dsh web          # 起在默认 127.0.0.1:3080
```

### 坑：rc.7 的 launcher flag 吞 app flag

`dsh web --port 3080` 会报 `error: unknown option '--port'`。launcher 的 commander 在解析 `--profile` / `web` alias 时把后续 flag 吞了，没透传给 web app。

**临时方案**：不带 flag 直接 `dsh web`，用默认 3080。要改端口需要进 profile 配置文件（`~/.dsh/profiles/web/`）改，或等官方修。

### 坑：WSL bash 下 terminal(background=true) 起不来

Hermes `terminal(background=true)` 包装层在 WSL bash 下对 dsh 这种交互式 CLI 会触发：

```
bash: 无法设定终端进程组 (-1): 对设备不适当的 ioctl 操作
bash: 此 shell 中无任务控制
```

然后进程立刻退出。

### 坑：rc.7 的 dsh-tui 插件强制要求 TTY

rc.7 起 web profile 也加载 `dsh-tui` 插件，报 `dsh-tui requires an interactive terminal (stdout must be a TTY)`。因此普通 `Popen(stdout=file)` 直接 boot 失败。

**方案**：`pty.openpty()` 给 stdout/stderr/stdin 伪终端 + double-fork daemonize（防止父进程退出带走 pty master）。工作脚本模式：

```python
import os, pty, subprocess, threading, fcntl, select
pid = os.fork()
if pid == 0:
    os.setsid()
    if os.fork() > 0: os._exit(0)
    master, slave = pty.openpty()
    p = subprocess.Popen(['dsh','web'], cwd='/home/po',
        stdout=slave, stderr=slave, stdin=slave,
        start_new_session=True, close_fds=True)
    os.close(slave)
    fcntl.fcntl(master, fcntl.F_SETFL, os.O_NONBLOCK)
    log = open('/tmp/dsh-svc.log','wb')
    def pump():
        while True:
            r,_,_ = select.select([master],[],[],1)
            if r:
                try: d = os.read(master, 65536)
                except OSError: break
                if not d: break
                log.write(d); log.flush()
    threading.Thread(target=pump, daemon=True).start()
    p.wait(); os._exit(0)
```

验证：`ss -tln | grep 3080` + `curl -s http://127.0.0.1:3080/` 返回 200。

## 状态文件

- `~/.dsh/settings.yaml` — 全局配置
- `~/.dsh/profiles/` — profile 定义（web / headless / tui）
- `~/.dsh/sessions/` — 会话历史
- `~/.dsh/dsh-process.json` — 上次启动的 pid/argv（stale 数据常见，勿信，直接 `ss -tln | grep 3080` 验证）

## 验证存活

```bash
ss -tln | grep 3080
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:3080/
```

## 用户偏好

- 工作区：`~/dsh`
- 交互人格名：皇后（The Empress）
- 全局 AGENTS.md：见 `~/.dsh/AGENTS.md`（包含 clash 代理、gh CLI 偏好）
