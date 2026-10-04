---
name: worktree-stack-migrate
description: |
  HTCMC PCHSystem 专用 skill——指导如何在 git worktree 中正确启动/迁移开发栈
  （根 docker-compose 的 postgres+backend、TestServer 的 mc-test、前端 Vite dev）。
  PCHSystem 的栈路径锚定主仓（bind mount / external 网络 / MCDR 挂载 / 根 .env 插值），
  worktree 的目录隔离与之天然冲突，常踩「端口对不上 / token 对不上 / 配置在别的分支」三类坑。
  本 skill 给出按「worktree 改了什么」选择的迁移策略 + 端口/token/网络对齐清单 + 红线陷阱。
  当用户在 worktree 里要起栈测试、提到「worktree 跑后端/前端/mc-test」「worktree 端口冲突」
  「token 对不上 / 401」「主仓有 WIP 没法 checkout 分支」「MCDR reload 看不到 worktree 改动」，
  或要在 worktree 改了 Dockerfile / pyproject / 端口 / .env 后验证时，就应使用本 skill。
  不用：纯文档或单文件编辑、不涉及运行栈的常规开发、或仅在主仓主线本地开发（不起 worktree）。
license: MIT
metadata:
  project: HTCMC-PCHSystem
  version: 1.0.0
---

# worktree-stack-migrate · 把开发栈迁进 worktree

## 1. 这个 skill 做什么

PCHSystem 的开发栈**路径锚定主仓** `/home/yushen/opt/PCHSystem`，而 worktree 是 `.claude/worktrees/<name>/` 下的独立目录——两者天然打架。本 skill 给出两样东西：

- 一张**按改动类型选择迁移策略的决策表**（§5）；
- 三份**对齐清单**：端口（§6）/ token 与密钥（§7）/ 网络名（§8），外加起栈后验证（§9）与红线陷阱（§10）。

目标：在 worktree 里测某分支代码时，栈能起来、和主仓栈不互踩、端口 token 自洽、不污染主线。

---

## 2. 何时用 / 何时不用

**用**：
- 在 worktree 改了后端/前端/MCDR 代码，要在运行栈上验证
- worktree 改了 `Dockerfile` / `pyproject.toml` / 端口 / `.env`，需要重建镜像或起独立栈
- 主仓 `main` 有未提交 WIP，无法 `git checkout <worktree 分支>` 把代码放进主仓测
- 遇到 `worktree 起的栈端口冲突 / token 401 / mc-test 连不上 backend / MCDR reload 没反应`

**不用**：
- 直接在主仓主线本地开发（不起 worktree → 普通 `docker compose up -d` 即可，见 `Docs/cheatsheets/dev-cheatsheet.md`）
- 纯文档/单文件编辑、不涉及运行栈

---

## 3. 背景：为什么 worktree 和开发栈打架

理解这四条机制，后面的规则就能推理而不是死记：

1. **三个 bind mount 相对仓根解析**：根 `docker-compose.yml` 的 `backend` 挂 `./Backend/app:/app/app`、`./Backend/alembic:/app/alembic`、`./Archive:/app/archive`。在主仓跑 compose，容器读的是**主仓源码**；worktree 的源码对运行中的容器不可见。
2. **compose 项目名 = 目录名**：主仓目录 `PCHSystem` → 项目名 `pchsystem` → 网络 `pchsystem_default`、容器 `pchsystem-backend-1` / `pchsystem-postgres-1`、卷 `pchsystem_pgdata`。从 worktree 目录跑 compose，项目名变成 worktree 目录名，天然与 `pchsystem` 隔离（`-p <feat>` 只是显式化）。
3. **`TestServer/docker-compose.yml` 写死 `pchsystem_default external:true`**：mc-test 没有自己的 postgres，加入主仓网络，容器内以 `http://pchsystem-backend-1:8000` 访问后端。它**依赖主仓栈已在运行**，且只能看到 `pchsystem` 项目里的 backend。
4. **MCDR 插件挂载落主仓**：`TestServer/docker-compose.yml` 的 `../McdrPlugin/pch_system:/mcdr/plugins/pch_system`，`../` 相对 `TestServer/` → 解析到**主仓**插件目录。游戏内 `!!MCDR plugin reload pch_system` 只读主仓工作树。
5. **compose `${VAR}` 插值读根 `.env`**（compose 文件同目录），**不是** `Backend/.env`。`Backend/.env` 是另一份，仅供宿主机直跑 `uvicorn`/`pytest`（`POSTGRES_HOST=localhost`、`POSTGRES_PORT=5433`）。

> 推论：要在 worktree 测代码，要么让运行中的主仓栈**改读 worktree 源码**（策略 A/A+），要么在 worktree **起一套独立栈**（策略 B）。前端 / MCDR 各有专门处理（策略 C / D）。

---

## 4. 第一步：进 worktree 前的对齐

EnterWorktree 默认 base = `origin/<default>`，本仓 default 常被识别成旧的 `feat/backend-phase0-foundation`（Frontend 几乎空）。新建 worktree 后先对齐主线最新已提交状态：

```bash
git reset --hard main     # worktree 分支对齐主线最新；不污染主仓工作树（主仓 WIP 留在主仓）
# 软链主仓已装的 node_modules（package.json 跨分支通常无差异，软链安全，省一次 npm install）
ln -s /home/yushen/opt/PCHSystem/Frontend/node_modules Frontend/node_modules
```

---

## 5. 按改动类型选策略（核心决策表）

先问：**worktree 相对主仓改了什么？** 对号入座。

| worktree 改了什么 | 策略 | 主仓栈 | 端口 | 何时选它 |
|---|---|---|---|---|
| 仅 `Backend/app` / `alembic` 源码 | **A** | 复用 `pchsystem` 单栈 | 不变（8000/5433） | 主仓有 WIP 不便 checkout；只想让运行中的 backend 读 worktree 源码 |
| 源码 + `Dockerfile` / `pyproject.toml` / 系统包 | **A+** | 复用 `pchsystem` 单栈 | 不变 | 新依赖/新字体/新系统包，必须重建镜像 |
| 要与主栈**并存**独立测 | **B** | 主栈保持运行 + worktree 独立栈 | 错开（8002/5434） | 需对照主栈、或不想动主栈 |
| 仅前端 | **C** | 主 backend 不动 | 5174 或复用 5173 | 只改 Vue 代码 |
| MCDR 插件 `.py` | **D** | 复用主 mc-test | 不变 | 改插件后要游戏内 reload 验证 |

### 策略 A —— 主仓写 override 换挂载源（仅源码）

主仓根写 `docker-compose.override.yml`（已被 `.gitignore`，含机器绝对路径，勿提交；它是 per-machine 逃生口）：

```yaml
# 主仓根：docker-compose.override.yml
services:
  backend:
    build: ./.claude/worktrees/<name>/Backend
    volumes:
      - ./.claude/worktrees/<name>/Backend/app:/app/app
      - ./.claude/worktrees/<name>/Backend/alembic:/app/alembic
      # Archive 不列 → 继承 base 的 ./Archive:/app/archive（主仓 Archive，无所谓）
```

> Compose v2 对 `volumes` 按 **target 去重**：同 target 时 override 替换 base，不会双挂载。

```bash
docker compose up -d backend          # 主仓目录跑；override 已把 build+挂载指向 worktree
```

恢复：`rm docker-compose.override.yml && docker compose up -d backend`（镜像已有依赖则无需 rebuild）。

### 策略 A+ —— A 之上重建镜像（依赖/字体/系统包变了）

A 的 override 已把 `build` context 指向 worktree，所以重建会拿 worktree 的 `Dockerfile` + `pyproject.toml`：

```bash
docker compose build backend && docker compose up -d backend
```

> 注意：主仓 override 仅换 `app/` 源码挂载时，**镜像仍是主仓旧依赖**——新 import 会运行时报错。这就是 A+ 存在的理由。

### 策略 B —— worktree 起独立栈（与主栈并存）

从 **worktree 根**跑（项目名 = worktree 目录名，天然与 `pchsystem` 隔离）：

```bash
ln -sfn /home/yushen/opt/PCHSystem/.env .env     # compose 插值需要根 .env（POSTGRES_PASSWORD/JWT_SECRET/MCDR_SERVICE_TOKEN…）
docker compose -p <feat> up -d --build            # -p 显式项目名 → 独立 <feat>-* 容器 + <feat>_pgdata 卷
docker compose -p <feat> exec backend alembic upgrade head   # 新 <feat>_pgdata 是空的，必须建表
```

端口错开（worktree 根 `docker-compose.override.yml`，需 Docker Compose v2.40+ 的 `!override`）：

```yaml
# worktree 根：docker-compose.override.yml
services:
  backend:
    ports: !override
      - "127.0.0.1:8002:8000"     # 只错开宿主映射；容器内仍是 8000
  postgres:
    ports: !override
      - "127.0.0.1:5434:5432"
```

> 主仓 `pchsystem-*` 栈**保持不动**（勿停，见红线 5）。`<feat>_pgdata` 与 `pchsystem_pgdata` 是两个卷，互不影响（遵守 R-1：主仓业务库仍由主仓独占）。

### 策略 C —— 仅前端

```bash
lsof -ti :5173 | xargs -r kill                 # 杀主仓 Vite（若占着 5173）
cd Frontend && npm run dev -- --port 5174      # 复用主仓 5173 也行；勿改 vite.config.ts（见红线 8）
```

前端 `vite.config.ts` 的 proxy 写死 `/api → http://localhost:8000`。若 worktree backend 也走策略 A/A+ 复用主仓 8000 端口，proxy 不用改，最省事。若走策略 B（worktree backend 在 8002），需临时把 proxy target 改 8002——**改完务必 `git checkout HEAD -- Frontend/vite.config.ts` 还原，绝不提交**。

### 策略 D —— MCDR 插件 `.py`

容器挂载的是主仓 `McdrPlugin/pch_system`（§3 机制 4），`!!MCDR plugin reload` 看不到 worktree 改动。验证前先把改动同步到主仓路径：

```bash
# 二选一：直接编辑主仓对应文件 / 或 commit 后 git -C 主仓 merge <worktree分支>
grep -n '<关键改动>' /home/yushen/opt/PCHSystem/McdrPlugin/pch_system/<file>.py   # 确认两边一致
# 游戏内：!!MCDR plugin reload pch_system
```

> MCDR 相关 API / 命令树须先联网核实（根 CLAUDE.md §0 S-1），见 <https://docs.mcdreforged.com/en/latest/plugin_dev/command.html>。

---

## 6. 端口对齐

| 服务 | 主栈 `pchsystem` | worktree 独立栈 `-p <feat>` | 改哪里 |
|---|---|---|---|
| backend | `8000` | `127.0.0.1:8002` | worktree `docker-compose.override.yml` `ports: !override` |
| postgres | `127.0.0.1:5433` | `127.0.0.1:5434` | 同上（5432 被别项目 `pf-postgres` 占，主仓才用 5433） |
| frontend（Vite） | `5173` | `5174` 或复用 | CLI `--port`；**勿入 vite.config.ts** |
| mc-test | `25565`（MC）/ `25575`（RCON） | `25566`/`25576` 或省略 | 仅当起 worktree mc-test |

**只错开「宿主→容器」映射，容器内部端口不变**（backend 恒 8000、pg 恒 5432），所以 `backend` 的 `POSTGRES_HOST=postgres` / `POSTGRES_PORT=5432` 与 `WEB_BASE_URL` 在容器视角下都无需改。

`WEB_BASE_URL`（`!!PCH login` 回调前缀）要等于玩家浏览器实际访问的前端端口（默认 `http://localhost:5173`）。

---

## 7. token / 密钥对齐清单

| 变量 | 对齐要求 | 不一致的后果 |
|---|---|---|
| `MCDR_SERVICE_TOKEN` | worktree backend 的根 `.env` 值 **必须 ==** mc-test 插件 `McdrPlugin/pch_system/config.json` 加载的值 | 插件 HTTP 上报被 backend 拒（401） |
| `POSTGRES_PASSWORD` / `POSTGRES_USER` / `POSTGRES_DB` | worktree 用**新卷** `<feat>_pgdata`（空），`.env` 的值就是**初始化值**，自洽即可 | 若误指主仓 `pchsystem_pgdata`（跨 project/卷），密码不匹配连不上 |
| `JWT_SECRET` | 每个 backend 独立即可 | token 不跨 backend 互通（登录态不共享，正常） |
| `WEB_BASE_URL` | == 玩家访问的前端端口 | `!!PCH login` 回调跳错地址 |

**新卷必跑迁移**：策略 B 的新 `<feat>_pgdata` 是空的，起栈后必须 `docker compose -p <feat> exec backend alembic upgrade head`，否则表都不存在。**不要尝试让 worktree backend 共享主仓 `pchsystem_pgdata`**（违反 R-1 数据唯一拥有者、且跨 project 卷名对不上）。

---

## 8. 网络对齐

- `TestServer/docker-compose.yml` 写死 `pchsystem_default external:true` → **主 mc-test 只能看到 `pchsystem` 项目里的 backend**（`http://pchsystem-backend-1:8000`）。
- worktree 策略 B 的栈在 `<feat>_default` 网络，backend 容器名 `<feat>-backend-1`，主 mc-test **看不到**。
- 要在 worktree 测 mc-test：需 worktree 自己的 mc-test compose，把 `networks.pchsystem_default` 改成 `<feat>_default`（且不再是 `external`），backend 引用改 `<feat>-backend-1:8000`。成本高，多数情况用策略 D（同步主仓 + 复用主 mc-test）更划算。

---

## 9. 起栈后验证

```bash
# 1. 挂载源必须指向 worktree，不是主仓
docker inspect <容器名> --format '{{range .Mounts}}{{.Source}}{{"\n"}}{{end}}'
#    期望看到 .claude/worktrees/<name>/Backend/app ...；若出现主仓 /home/yushen/opt/PCHSystem/Backend/app → override 没生效

# 2. 健康检查（端口按实际栈：主栈 8000 / worktree 8002）
curl -sS http://localhost:8000/healthz        # → {"status":"ok"}

# 3. 迁移状态（策略 B 新卷尤其要看）
docker compose -p <feat> exec backend alembic current
```

---

## 10. 红线·陷阱（硬约束）

每条都附 why——理解了就不会误踩。

1. **EnterWorktree 默认 base 是旧 phase0** → 进 worktree 先 `git reset --hard main` + 软链 node_modules（§4）。*why*：该仓 default 分支在 origin 上远早于前端/后端业务代码，不 reset 会缺前端。
2. **`docker cp` 写容器 bind-mount 路径 = 反写主仓宿主文件**（bind mount 双向）→ 注入测试文件时 cp 到**非挂载路径**（如 `/app/tests`、`/tmp`）或起 `docker run --rm -v <worktree>:/app` 临时容器；事后 `git -C 主仓 status` 排查，污染立即 `git checkout HEAD -- <file>`。*why*：曾 `docker cp ...:/app/app/api/sheets.py` 反改主仓源码污染主线。
3. **`!!MCDR plugin reload` 只读主仓路径** → worktree 改动先同步主仓再 reload（策略 D）。*why*：容器挂载的是主仓 `McdrPlugin/pch_system`。
4. **`docker compose --remove-orphans` 会删 mc-test** → worktree 操作时慎用。*why*：mc-test 定义在 `TestServer/` 另一份 compose，根 compose 把它当 orphan。
5. **worktree 会话只起 worktree 栈**（`-p <feat>`），勿启动/触碰主仓 `pchsystem-*`（让主仓栈保持 stopped 或原状）。*why*：混起会让主仓读到未完成代码、破坏主仓测试数据。
6. **`docker-compose.override.yml` 已被 `.gitignore`**（含机器绝对路径）→ per-machine 逃生口，测完删，勿提交。
7. **`.claude/worktrees/` 现已加入 `.gitignore`** → 残留 worktree 目录曾污染主线 `git status`；孤立目录（不在 `git worktree list`）应清理。
8. **勿以追踪方式改 `vite.config.ts` 端口** → 历史上 worktree 改 `8002` 被提交进主线造成污染；用 CLI `--port` 或临时改 + `git checkout HEAD --` 还原。
9. **GitHub push/pull 走宿主机代理**（VMware NAT 直连不稳），用户偏好**自己手动**执行 → 不自动跑 git 网络命令，把命令交给用户。

---

## 11. 与根 CLAUDE.md 的关系

本 skill 是根规范的**操作细化**，不覆写根规范：

- **R-1（数据唯一拥有者）**：worktree 用独立 `<feat>_pgdata` 卷，不碰主仓 `pchsystem_pgdata` 业务库。
- **R-11（密钥经 `.env` 注入，不进库）**：所有 token/密码来自根 `.env`，worktree 经软链复用或自洽的新值，绝不硬编码。
- **§0 S-2（中文输出）**、**§1（skill 目录 kebab-case）**：本 skill 遵守。
- 经验来源：项目 auto-memory `enter-worktree-base-old-phase0` / `worktree-stack-switch-via-compose-override` / `worktree-stack-built-from-worktree` / `worktree-no-main-stack` / `mcdr-worktree-hotreload-mounts-main` / `docker-cp-bind-mount-writes-main` / `github-push-via-host-proxy`。

---

*本 skill 与 `service-claude-md` 同级，均为 PCHSystem 项目级 skill（`.claude/skills/` 自动发现）。栈配置本身以 `docker-compose.yml` / `TestServer/docker-compose.yml` / `.env.example` 为准，本 skill 只指导如何在 worktree 中迁移与对齐，不改栈。*
