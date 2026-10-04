---
name: scaffold-fastapi-vite-saas
description: 当用户要起一个 FastAPI 后端 + Vite SPA 前端 + Docker + GitHub Actions 的单仓双端 SaaS 项目时使用。一个 docker run 就跑起来的自托管 SaaS / 内部工具骨架,脱胎于 BeeCount-Cloud 生产实践。触发关键词:"scaffold FastAPI + Vite 项目"、"新建一个 SaaS 单仓"、"起一个 FastAPI Docker monorepo"、"按 fastapi-vite-saas / BeeCount-Cloud 风格建项目"、"create a fastapi vite saas template"、"new selfhost monorepo with FastAPI and Vite"。不适用于纯前端项目、纯 CLI 工具、纯库项目。
---

# FastAPI + Vite SaaS 脚手架技能

## 这套架构是什么

一个**单仓双端**的全栈应用骨架:Python 后端 + 前端 SPA 共住一个 git 仓库,通过多阶段 Docker 构建打成单一镜像,GitHub Actions 自动发版。**核心定位:用一个 docker run 就能跑起来的自托管 SaaS。**

技术选型(每一项都解释为什么):

| 层 | 选型 | 为什么 |
|---|------|--------|
| Web framework | FastAPI | Pydantic v2 校验直接当 schema、async 原生、OpenAPI 自动生成 |
| ORM | SQLAlchemy 2.x | 久经考验、async 支持成熟、Alembic 配套迁移成熟 |
| Migrations | Alembic | 不要自己搞 schema_migrations 表 |
| Auth | JWT(PyJWT)+ passlib + 可选 pyotp 2FA | 无状态、单镜像无 redis 依赖 |
| 调度 | APScheduler BackgroundScheduler | in-process,不引入额外服务;线程池避免阻塞事件循环 |
| 备份加密 | pyzipper(AES-256 zip)| stdlib zipfile 的 ZipCrypto 已破,pyzipper 是 drop-in 替换 |
| 对象存储 | rclone subprocess | 一个二进制覆盖 S3/R2/WebDAV/B2/GDrive/OneDrive |
| Lint/Type/Test | ruff + mypy + pytest | 标配,启动快 |
| Frontend | pnpm workspace + Vite + (React/Vue 任选) | apps/* + packages/* 拆分清晰 |
| 构建产物 | 单一 Docker 镜像 | 多阶段:Node build 前端 → Python 运行时拷 dist/ 当静态 |
| CI | GitHub Actions | ci.yml(test/lint/build)+ release.yml(tag 触发 → docker hub)|
| 编排 | Makefile | 不引入 just/task,Makefile 一份所有人都会读 |

## 仓库布局(基线)

```
<project>/
├── .github/
│   └── workflows/
│       ├── ci.yml              # PR/push: ruff + mypy + pytest + frontend build
│       └── release.yml          # tag 'v*': build & push docker image
├── .docs/                       # 内部设计文档(不发布)
├── docs/                        # 用户向文档(随发版打入镜像/网站)
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── data/                        # 运行时数据(gitignored,.gitkeep 占位)
│   └── .gitkeep
├── frontend/
│   ├── pnpm-workspace.yaml
│   ├── package.json             # 仅 workspace 根
│   ├── apps/
│   │   └── web/                 # Vite SPA
│   └── packages/
│       ├── api-client/          # 类型化 API client(从 OpenAPI 生成)
│       ├── ui/                  # 共享组件
│       └── features/            # 跨页可复用业务组件
├── scripts/                     # 运维脚本(seed/backup/grant-admin/...)
├── src/                         # Python package(直接 import,不再嵌一层)
│   ├── __init__.py
│   ├── main.py                  # FastAPI app + lifespan
│   ├── config.py                # pydantic-settings,所有 env 集中定义
│   ├── database.py              # engine / session / Base
│   ├── deps.py                  # FastAPI Depends 工厂(get_db / get_user / ...)
│   ├── models.py                # SQLAlchemy ORM(小项目放一起,大了再拆)
│   ├── schemas.py               # Pydantic schemas(同上)
│   ├── security.py              # 密码哈希 + JWT 签发/校验 + 可选 TOTP
│   ├── error_handling.py        # 全局异常 → JSON 响应映射
│   ├── observability.py         # structured logging + metrics
│   └── routers/
│       └── <group>/
│           ├── __init__.py      # 聚合 APIRouter,main.py import 不变
│           ├── _shared.py       # 共享 imports/helpers/router 实例;__all__ 显式
│           └── <entity>.py      # 单一资源的 POST/PATCH/DELETE 或一组 GET
├── tests/                       # pytest,与 src/ 对称
├── .env.example                 # 所有 env 的注释样本(.env 进 gitignore)
├── .gitignore
├── alembic.ini
├── docker-compose.yml           # 生产 compose(用户拿去 deploy)
├── docker-compose.postgres.yml  # overlay,可选切换 Postgres
├── Dockerfile                   # 多阶段:frontend-builder → python:3.12-slim
├── Makefile                     # 唯一的命令编排入口
├── mypy.ini
├── pytest.ini
├── README.md / README.en.md     # 双语
├── requirements.txt             # 不用 pyproject — 简单项目 requirements 更直白
├── ruff.toml
└── server.py                    # 极简 entry:from src.main import app
```

**几个不显眼但关键的设计**:

- **`server.py` 在仓根**:让 `uvicorn server:app` 能直接跑。生产 Dockerfile 也用这个,本地 dev 也用这个,**统一入口**避免本地/生产两套启动方式。
- **`src/` 不再嵌套包名**:小项目里 `<project>/src/<project>/foo.py` 是没必要的间接层。直接 `src/foo.py`,Python path 设 `.`(`PYTHONPATH=.`)即可。
- **路由用包不用文件**:每个 `routers/<group>/` 是包,`_shared.py` 集中共享导入和 router 实例。新增 endpoint 只动单个 entity 文件,改共享逻辑只动 `_shared.py`。**不要把业务塞进 `__init__.py`,它只做聚合。**
- **`/data` 是唯一持久化目录**:DB、备份、附件、用户上传 — 全部走 `DATA_DIR` env,默认 `/data`(docker)或 `./data`(本地)。容器部署只挂一个 volume 就能整体备份。
- **`.docs/` vs `docs/`**:点前缀的不发布(内部设计/复盘),无点前缀的对外。明确分流。

## 用户工作流(Makefile 是核心)

scaffold 完成后,用户应该能直接:

```bash
make setup-backend   # 建 venv + pip install + 拷 .env.example → .env
make migrate         # alembic upgrade head
make seed-demo       # 灌种子数据(可选)
make dev-api         # uvicorn --reload --host 0.0.0.0
make dev-web         # pnpm install + vite dev
make dev-db          # docker compose up postgres(如果切到 PG)
make test            # pytest
make lint            # ruff check
make typecheck       # mypy src
make wipe-local      # 清本地 dev 数据(保留 .gitkeep 和指定的构建产物)
```

**dev-api 必须 `--host 0.0.0.0`**:模拟器/真机经 WiFi 用 IP 访问时,uvicorn 默认绑 127.0.0.1 会 Connection refused。这条踩过,scaffold 时直接写好。

## scaffold 流程(AI 执行步骤)

当用户说"按 fastapi-vite-saas 起一个新项目叫 Foo"时,按以下顺序执行:

### Step 1: 收集参数

如果用户没给全,问清楚(一次性问,不要来回往返):

- **项目名**(kebab-case,如 `foo-cloud`)→ 同时确定 Python 包名(snake_case)、Docker image 名、env 前缀
- **目标路径**(默认 `~/code/mine/<project-name>`)
- **前端框架**:React / Vue / Svelte(默认 React,跟 BeeCount-Cloud 一致)
- **默认数据库**:SQLite(单镜像零依赖)/ Postgres(团队/生产强一致需求)— 默认 SQLite,Postgres 通过 overlay compose 切换
- **是否需要 2FA**(默认否,简化首版)
- **是否需要备份模块**(rclone + 加密 zip,默认否,有需要再加)
- **GitHub owner**(用户名/组织名,写进 Dockerfile/README/CI)

### Step 2: 创建目录树 + 生成基础文件

按上面的"仓库布局"创建空目录(包括 `.gitkeep` 占位)。

然后生成以下文件,**所有 `{{project_name}}` / `{{python_pkg}}` / `{{github_owner}}` / `{{image_name}}` 替换成 Step 1 参数**:

1. `requirements.txt` — 基线依赖(从这个 skill 同目录的 `templates/requirements.txt` 拷,见下面"模板文件")
2. `src/main.py` — FastAPI app 骨架,挂 CORS、健康检查 `/healthz`、版本端点 `/api/v1/version`
3. `src/config.py` — pydantic-settings,声明所有 env(DATABASE_URL, JWT_SECRET, DATA_DIR, CORS_ORIGINS, APP_ENV, APP_VERSION)
4. `src/database.py` — engine(根据 DATABASE_URL 自动判 sqlite/pg)+ SessionLocal + Base
5. `src/deps.py` — get_db / get_current_user 占位
6. `src/security.py` — passlib CryptContext + JWT encode/decode
7. `src/models.py` — User 模型占位
8. `src/schemas.py` — UserCreate/UserRead/Token 占位
9. `src/error_handling.py` — 把常见异常映射成 JSON(401/403/404/422/500)
10. `src/routers/auth/__init__.py` + `_shared.py` + `register.py` + `login.py` — 完整可跑的注册登录端点
11. `alembic.ini` + `alembic/env.py` + 第一个 migration(创建 users 表)
12. `server.py` — 一行:`from src.main import app`
13. `Makefile` — 全套 dev/test/lint/typecheck/wipe-local
14. `Dockerfile` — 多阶段构建(参考 BeeCount-Cloud,删掉 docs-index 那一段,普通项目不需要 RAG 索引)
15. `docker-compose.yml` — 单服务,挂 `./data:/data`,暴露端口可参数化(默认 8080 → host)
16. `docker-compose.postgres.yml` — overlay,定义 `db` service + 覆盖 `DATABASE_URL`
17. `.env.example` — 所有 env 的注释样本,**JWT_SECRET 写 `change-me-32-bytes-strong-random`**
18. `.gitignore` — Python + Node + venv + .env + data/* (保留 .gitkeep) + IDE
19. `ruff.toml` / `mypy.ini` / `pytest.ini` — 直接抄 BeeCount-Cloud 的配置
20. `.github/workflows/ci.yml` — matrix: backend(ruff + mypy + pytest)+ frontend(pnpm install + build)
21. `.github/workflows/release.yml` — tag 触发,build docker → push docker hub(用 `{{github_owner}}/{{image_name}}`)
22. `README.md` + `README.en.md` — 模板文档(项目简介、quickstart、deploy、env 说明)
23. `frontend/pnpm-workspace.yaml` + `frontend/package.json`
24. `frontend/apps/web/` — Vite + React/Vue 模板(用 `pnpm create vite` 思路,生成最小可跑)
25. `frontend/packages/api-client/` — 占位 + 注释说明"从 OpenAPI 用 openapi-typescript 生成"
26. `frontend/packages/ui/` + `frontend/packages/features/` — 占位 + 一个 hello 组件

### Step 3: 初始化 git + 装依赖 + 跑一次自检

```bash
cd <target>
git init && git add -A && git commit -m "feat: fastapi-vite-saas 脚手架初始化"
make setup-backend
make migrate
make test  # 期望:0 个测试,exit 0
cd frontend && pnpm install
pnpm -C apps/web build  # 期望:dist/ 产出
```

任何一步失败,**立即停下报错给用户**,不要试图绕过。

### Step 4: 提示下一步

最后给用户一份"接下来要干的 5 件事"清单:

1. 改 `.env.example` 的 `JWT_SECRET` 为真随机串(给一行 `openssl rand -hex 32` 命令)
2. 把仓库推到 GitHub:`gh repo create {{github_owner}}/{{project_name}} --public --source . --push`
3. 配 Docker Hub secrets(`DOCKERHUB_USERNAME` / `DOCKERHUB_TOKEN`)让 release.yml 能 push 镜像
4. 改 README 里的 placeholder(项目简介、screenshot)
5. 起第一个业务实体:跟 AI 说"加一个 <实体名> 资源",AI 应该按 routers/<group>/ + models.py + schemas.py + alembic migration 这套流程加

## 不要从 BeeCount-Cloud 抄过来的部分

以下是 BeeCount-Cloud 的领域逻辑,**新项目里不要默认带上**:

- `sync_changes` + `read_*_projection` + `sync_applier.py` 那套多端同步架构(只在需要"移动端离线 + 多设备同步"时才搭)
- AI 文档 Q&A / RAG / `numpy` cosine search / `docs-index.*.sqlite`(只在产品本身要做文档搜索时才搭)
- `mcp/` 目录 MCP server(只在要给 LLM 工具调用时才搭)
- `pyzipper` / `rclone` / `apscheduler` 备份链(在用户明确说要做"自助备份到对象存储"时才搭)
- `pyotp` / TOTP 2FA(只在 step 1 用户明确说要 2FA 时才搭)
- `openpyxl` Excel 导入(域特定,不要默认装)

每一项都增加运行时复杂度。**默认 scaffold 是最小可跑的 FastAPI + Vite + Docker,其它当 add-on 按需启用。**

## 模板文件位置

与 SKILL.md 同目录,有一个 `templates/` 子目录,里面是上面 Step 2 列出的所有文件的实际模板内容(用 `{{var}}` 占位)。AI 执行时:

1. 读 `templates/<filename>` 内容
2. 用 Step 1 收集的参数做字符串替换
3. 写到 `<target>/<filename>`

模板暂未填充时,AI 可以**基于 BeeCount-Cloud 对应文件现场改写**(把 `beecount` / `BeeCount` / `8869` / `sunxiao0721` 等字面量替换成新项目参数)。后续版本会把模板固化进 `templates/`,减少现场改写的随机性。

## 反模式(已踩过的坑)

- ❌ 不要在 `server.py` 里写业务,它只能是 `from src.main import app` 一行 — 否则本地/生产入口分裂
- ❌ 不要用硬编码 SQL `CREATE TABLE ... AS SELECT` 做迁移,全走 Alembic
- ❌ 不要在 Drift/Alembic 之外维护自己的 `schema_migrations` 表
- ❌ Dockerfile 里不要在 frontend builder 阶段就 `COPY frontend/` 全量 — 先只拷 `package.json` + lock,装完依赖再 COPY 全量,Docker layer cache 才能命中
- ❌ 不要把 `data/` 留在仓里跟构建产物混(`docs-index.*.sqlite` 是个例外:它是从兄弟仓 build 出来 commit 进去的索引)
- ❌ HEALTHCHECK 不要打 `/api/v1/healthz`,挂在根 `/healthz`,避免被前缀路由拦掉

## 升级与变体

- **切 Postgres**:`docker-compose -f docker-compose.yml -f docker-compose.postgres.yml up`,`.env` 改 `DATABASE_URL=postgresql+psycopg://...`
- **切 Vue/Svelte**:Step 1 选项分支,生成 `frontend/apps/web/` 时换模板
- **加 MCP server**:用 `mcp>=1.27.0` 装 FastMCP,挂在 `/api/v1/mcp`,PAT 鉴权
- **加备份模块**:装 pyzipper + apscheduler,起一个 `src/backup/` 包,`scripts/backup_sqlite.sh` 兜底 CLI
