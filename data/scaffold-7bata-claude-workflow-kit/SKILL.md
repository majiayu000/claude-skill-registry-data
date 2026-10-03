---
name: scaffold
description: 在当前项目目录里铺设方法论脚手架（AGENTS.md + docs 八件套 + .gitignore + README）。后端技术栈固定为 Go（版本基线见 skill 内表格），数据库由子代理按项目意图判断。用户说"搭脚手架/初始化项目/开新项目/scaffold"时触发。
---

# scaffold

在**已存在的**项目目录里就地铺设方法论脚手架。**全程默认中文输出**（技术标识符保持英文）。

模板位于本 skill 自身目录的 `templates/` 子目录（相对本 SKILL.md 所在目录定位）。

## 技术栈基线（固定，不做选型）

后端技术栈**固定为 Go**，版本与选型统一采用以下基线（固定基线是本方法论的一部分：逐项目不再重复选型；想换栈就修改本表，而不是单次临时偏离）：

| 组件 | 选型 / 版本 | 说明 |
|---|---|---|
| 后端语言 | Go 1.25（`golang:1.25-alpine` 编译） | 标准库 `net/http` + chi 路由，无重量级框架 |
| DB 访问 | pgx（手写 repository） | 不用 ORM、不用 sqlc，`internal/repo` 直接写类型化 SQL |
| 迁移 | golang-migrate | 纯 SQL 版本化迁移（`NNNN_*.up.sql / down.sql`） |
| 校验/序列化 | `encoding/json` + go-playground/validator | 请求/响应 schema 校验 |
| 前端（如需要） | React + TypeScript + Vite | `node:20-alpine` 仅用于构建阶段 |
| 运行镜像 | `alpine:3.20` | Docker 多阶段构建，单静态二进制，`/health` 健康检查 |
| 目录结构 | `backend/cmd/server` 入口 + `backend/internal/{config,db,repo,handlers,service,model,middleware}` | Go 社区惯例；前端在 `frontend/src` |

后端服务保持**无状态**（状态全在数据库），为多副本水平扩展留余地。

## SQLite 分支（步骤 3 选了 SQLite 时的具体替代）

上面基线表默认 PostgreSQL（pgx + golang-migrate + postgres 容器/实例）。步骤 3 若判断选 **SQLite**（小型低并发 / 单机一体机场景），DB 访问层与迁移工具按以下替换，Go 版本、校验库、运行镜像、目录结构（`backend/internal/{db,repo}` 等目录名不变，只是里面的实现换了）不变——不是"酌情调整"，按此执行：

| 组件 | SQLite 替代 |
|---|---|
| DB 访问 | `database/sql` + `modernc.org/sqlite`（纯 Go 驱动，无 cgo，`CGO_ENABLED=0` 直接编译；不用需要 cgo 的 `mattn/go-sqlite3`） |
| 迁移 | golang-migrate 的 `sqlite`（modernc，纯 Go）驱动，migrations 仍是 `NNNN_*.up.sql/down.sql`；不用 cgo 版 `sqlite3` 驱动；无迁移框架依赖时也可退化为启动时执行嵌入的建表 SQL（`embed.FS` 内一份 `schema.sql`），小项目够用 |
| 数据文件 | 单文件落 `data/{{PROJECT_NAME}}.db`（复用本 skill 落盘的 `data/` 目录），不建 PG 容器/实例 |
| 并发注意 | 打开 `_pragma=busy_timeout(5000)&_pragma=journal_mode(WAL)`，写路径避免长事务持锁 |

**占位符联动**：`{{TECH_STACK}}` 里 `pgx + golang-migrate` 替换为 `database/sql (modernc.org/sqlite) + golang-migrate (sqlite driver)`；`{{DATABASE}}` 填 `SQLite`。

**`docs/DECISIONS.md.tmpl` 预置首条会自相矛盾，必须改**：第 9 行 What「后端 Go 1.25（net/http + chi + pgx + golang-migrate），数据库 {{DATABASE}}」里的 `pgx + golang-migrate` 若不改，`{{DATABASE}}` 填 `SQLite` 后渲染成「…pgx + golang-migrate…数据库 SQLite」，同一句自相矛盾；落盘前把这半句换成 `database/sql (modernc.org/sqlite) + golang-migrate (sqlite driver)`。再按下文「`docs/DECISIONS.md` 追加一条记录选 SQLite 的理由」写一条独立条目。

**`docs/ARCHITECTURE.md.tmpl` 里第 1/3/6 节的 `pgx`/`BIGSERIAL`/`TIMESTAMPTZ`/`pgxpool` 是正文硬编码、不是占位符**（该模板与开源版原样保持字节一致，没有做数据库分支占位符化）。落盘生成 `docs/ARCHITECTURE.md` 后，选了 SQLite 就必须手工按下表改写这几处，否则文档会与实际技术栈冲突，且照着 `BIGSERIAL`/`TIMESTAMPTZ` 写 DDL 在 SQLite 里会直接建表失败：

| 位置 | PostgreSQL 原文 | SQLite 改写为 |
|---|---|---|
| 第 1 节「DB 驱动 / 查询」行 | `pgx（手写 repository）` | `database/sql + modernc.org/sqlite（手写 repository）` |
| 第 3 节表设计约定 | `id BIGSERIAL PK`、`created_at/updated_at TIMESTAMPTZ` | `id INTEGER PRIMARY KEY AUTOINCREMENT`、`created_at/updated_at TEXT`（ISO8601 字符串，SQLite 无原生 TIMESTAMPTZ 类型） |
| 第 6 节目录结构注释 | `pgx 连接池` / `pgxpool 连接池` / `手写 pgx repository` | 对应改为 `database/sql (modernc.org/sqlite) 连接` / `手写 repository` |

`docs/DECISIONS.md` 追加一条记录选 SQLite 的理由（步骤 3 已要求）。

本 skill 落盘范围是 11 个通用文件（不含部署模板包），SQLite 分支不改变落盘文件数量；除上表要求手工改写 `docs/ARCHITECTURE.md` 正文、`docs/DECISIONS.md.tmpl` 预置首条外，其余文件只改变技术选型占位符取值。

## CLI / 无网络服务分支（步骤 3 判定为纯 CLI / 批处理时的具体替代）

上面基线表默认对外提供 HTTP 接口（`net/http + chi` + `/health` 健康检查 + 容器运行）。步骤 3 若判定项目是**纯 CLI / 批处理**（无 HTTP 接口、不监听端口），按以下替换，不是"酌情调整"，按此执行：

| 组件 | CLI 替代 |
|---|---|
| `{{TECH_STACK}}` | `Go 1.25 标准库 CLI + <DB 访问栈>`（`<DB 访问栈>` 按上面基线表或 SQLite 分支取值），不写 `net/http + chi` |
| 目录结构 | `backend/cmd/<binary>` 入口 + `backend/internal/{cli,core,db,repo,model}`；不建 `handlers/`、`middleware/` |
| `docs/ARCHITECTURE.md` | 第 1 节删掉路由/HTTP 接口行；第 6 节目录结构注释同步为 `cmd/<binary>` + `internal/{cli,core,db,repo,model}`，不出现 `handlers`/`middleware` |
| `docs/DEPLOYMENT.md` | 部署形态写「单二进制，`CGO_ENABLED=0 go build`，无容器/端口/健康检查」；不写 `alpine` 运行镜像与 `/health` |

## 步骤 1：确认项目名与目录

```bash
basename "$PWD"
```
取当前文件夹名为项目名。确认当前目录就是要铺设的项目根目录。

## 步骤 2：Intake — 收集项目意图

向用户说明并收集：

> 把这个项目的想法 / 会议总结讲给我，或指给我一个文件（如纪要 `*.md`），我据此判断技术栈、数据库、核心不变量和模块划分。

- 用户给文件路径 → 读它；若是**会议纪要**，落盘时将原始内容归档进 `docs/MEETINGS.md` 第一节，其中的**业务事实**另提炼进 `docs/BUSINESS.md`（原先全部归 REQUIREMENTS 的提炼职责，现按事实/决定拆分）
- 用户口述 → 用对话内容
- 信息不足以判断时，**针对性追问**（不要泛泛）

在判断技术栈/DB 之外，**按以下 7 格追问业务上下文**（用于填实 `docs/BUSINESS.md`；信息不足的格留占位注释，不逼问、不卡流程）：

1. 目标与现状手工流程 —— 没系统之前谁、用什么工具，一步步怎么做，痛点在哪
2. 输入：交易数据 —— 每次都变的数据是什么，有没有真实样本文件
3. 输入：参考/配置数据 —— 对照表、规则表、允许值，有没有现成文件
4. 加工流程 —— 输入怎么变成输出
5. 输出 —— 产出什么、给谁、什么样，有没有期望输出样例
6. 业务铁律与异常 —— 绝不能错的规则，意外情况怎么处理
7. 人工介入与反馈 —— 谁复核、能改什么、改的结果要不要被系统记住

## 步骤 3：决策并确认

基于 intake，向用户列出以下各项 + 给理由，逐项让用户确认/修改：

1. **后端技术栈** —— **固定为 Go，不询问、不选型**（见开头「技术栈基线」表格）。只向用户**陈述**将采用该基线；若用户主动要求换栈，视为修改本 skill 的信号，提醒其更新基线表而非本次临时偏离
2. **数据库**：
   - **默认 PostgreSQL**（有并发 / 大多数场景；Go 侧用 pgx + golang-migrate，见基线表）
   - **仅小型低并发 / 单机一体机用 SQLite**（如离线一体机、边缘部署）——选中则按上面「SQLite 分支」执行
   - 判断依据：并发量、部署形态（云 vs 单机）、数据规模
3. **是否需要 Web 前端**：需要则按基线 React + TypeScript + Vite；纯 API / CLI 项目则无 frontend 目录。判定为纯 CLI / 批处理（无 HTTP 接口、不监听端口）时，按上面「CLI / 无网络服务分支」执行
4. **核心不变量**：本项目「绝不破坏」的架构约束，0~N 条。想不出就留占位
5. **模块划分**：顶层模块名 + 一句话职责。想不清就留占位

把每项的**判断理由**说出来，由用户拍板。确认后才落盘。

## 步骤 4：落盘（带冲突保护）

先列出将写入的 11 个目标文件，**逐个检查是否已存在**：

```bash
for f in AGENTS.md docs/PLAN.md docs/Progress.md docs/ARCHITECTURE.md docs/DEPLOYMENT.md docs/REQUIREMENTS.md docs/BUSINESS.md docs/DECISIONS.md docs/MEETINGS.md .gitignore README.md; do
  test -e "$f" && echo "EXISTS: $f"
done
```

- 有 `EXISTS` 的 → 列出来问用户：跳过 / 备份改名（`.bak`）/ 手动合并。**绝不静默覆盖**
- 无冲突的 → 继续

对每个模板：读模板内容 → 替换占位符 → 写到目标路径。占位符替换表：

| 占位符 | 值来源 |
|---|---|
| `{{PROJECT_NAME}}` | 步骤 1 文件夹名 |
| `{{ONE_LINER}}` | intake 提炼的一句话定位 |
| `{{DATE}}` | `date +%F` |
| `{{TECH_STACK}}` | 固定基线：`Go 1.25（net/http + chi）+ pgx + golang-migrate`；选 SQLite 时按「SQLite 分支」替换；纯 CLI / 批处理时按「CLI / 无网络服务分支」替换，不写 `net/http + chi`；有前端时追加 `；前端 React + TypeScript + Vite（Node 20 构建）` |
| `{{DATABASE}}` | 步骤 3 数据库 |
| `{{INVARIANTS_BLOCK}}` | 步骤 3 核心不变量；无则 `<!-- 待补：本项目核心不变量 -->` |
| `{{MODULES_BLOCK}}` | 步骤 3 模块划分；无则 `<!-- 待补：模块划分 -->` |
| `{{CODE_CONVENTIONS_BLOCK}}` | 按基线生成的 Go 代码约定（Go 1.25、gofmt、error 显式处理并 wrap、`cmd/` + `internal/` 布局、依赖最小化）；有前端时追加 TS 约定（strict 模式、组件按页面分目录） |

模板路径映射：`templates/docs/X.md.tmpl` → `docs/X.md`；`templates/gitignore.tmpl` → `.gitignore`；`templates/AGENTS.md.tmpl` → `AGENTS.md`；`templates/README.md.tmpl` → `README.md`。另建空目录占位 `data/.gitkeep` 与 `docs/specs/.gitkeep`（design spec 落盘目录，`.gitignore` 只对 `data/.gitkeep` 做白名单，`docs/specs/.gitkeep` 不受影响，可直接入 git）。(清单 11 个 + data/.gitkeep + docs/specs/.gitkeep，物理文件总数 = 清单数 + 2，自检时按此对账)

**内容预填**（不只替换占位符，能填实的就填实）：

- `docs/REQUIREMENTS.md`：用 intake 提炼内容尽量填实（产品定位、目标用户、分期路线图、已确认决策）；填不了的保留待补注释
- `docs/BUSINESS.md`：用 7 格追问收集到的内容按对应节填实（目标与现状流程、输入输出、加工流程、业务铁律、人工介入……）；填不了的格保留模板自带的待补注释
- `docs/MEETINGS.md`：intake 来自会议纪要时，把原始纪要归档为第一节；否则保留空骨架
- `docs/DECISIONS.md`：模板自带「Go 基线」首条；步骤 3 若有其他重要拍板（如数据库选 SQLite 的理由），各追加一条 What/Why/Changes

## 步骤 5：收尾

```bash
set -e
git rev-parse --git-dir >/dev/null 2>&1 || git init -b main   # 默认分支叫 main，配合 AGENTS.md §5.1 的 main 门禁
git add -A
git commit -m "chore: 初始化项目脚手架"
git rev-parse HEAD >/dev/null 2>&1 && echo "初始 commit 已产生 ✓" || { echo "⚠ 仓库未建立/未提交，停止"; exit 1; }
```

上述任一步报 `Operation not permitted`（Codex 默认 `workspace-write` 沙箱拒写 `.git`）→ **停下，不要继续汇报成功，也不要把 Phase 0 标 ✅**。原样告诉用户失败原文，并给出修复方式：重新以 `-c 'sandbox_workspace_write.writable_roots=["<项目绝对路径>/.git"]'` 启动，或用 `-s danger-full-access`（详见 README「运行模式」）。用户拒绝放开权限时，如实记录『脚手架已落盘但未纳入版本控制』，PLAN 的 Phase 0 保持未完成。

初始 commit 校验通过后，把 `docs/PLAN.md` 的 Phase 0 标题改为 `## Phase 0：环境与脚手架 ✅ <date +%F 的结果>`；校验未通过则保持原样并在标题后追加 `（未纳入版本控制，待补 git 提交）`。

落盘后**自检**：
```bash
grep -rl '{{' AGENTS.md docs README.md 2>/dev/null && echo "⚠ 有未替换占位" || echo "占位全部替换 ✓"
LC_ALL=C grep -rl $'\xef\xbf\xbd' AGENTS.md docs README.md 2>/dev/null && echo "⚠ 有乱码" || echo "无乱码 ✓"
```

向用户汇报：生成了哪些文件、技术栈/DB 决策、下一步建议（先与用户把设计聊透、design spec 请落 `docs/specs/`——写入后按 spec 拆独立单元用 `parallel-do` 分波并行实现；小改动也写一份小 spec（几段即可），写完直接做）。

若项目推进中沉淀出可复用的组件/模块（不是本次落盘范围，是给未来的提醒）：**若团队维护组件索引库，登记之**，方便其他项目调研时发现并复用。

## Auto 模式与常驻安装（可选）

Claude Code 版靠插件级 SessionStart hook，每次会话开局自动判定"用户是不是在描述一个新项目"并静默铺设脚手架。**Codex CLI 没有会话开局一类的常驻 hook 机制**，所以这个自动触发在 Codex 里不会随插件安装自动生效——本 skill 只能靠用户手动 `/scaffold` 显式调用。想要"说一句要做新东西就自动建目录铺脚手架"的效果，需要自己 opt-in：把下面的判定规则手动写进 `~/.codex/AGENTS.md`（Codex 每个会话都会全局加载这个文件）。

规则片段（以 Claude 版定稿规则为底，三处按 Codex 场景适配：触发后第 3 步的铺设动作改为指向**本 skill 自己的落盘清单与 `AGENTS.md.tmpl` 模板**，不再引用 Claude 版专有的「Auto 模式」小节；原「关闭」一节整节删去，改为文末一句话说明；项目标记与配置路径改用 Codex 惯例——已铺项目标记看 `AGENTS.md`、配置目录与项目根配置在 `~/.codex` 下，Codex 用户机器上未必有 `~/.claude`）：

```markdown
# auto-scaffold:新项目自动铺设

## 判定(三条全满足才触发)
1. 用户在描述"要做一个新的东西"——新产品/工具/网站/系统,
   而不是:问问题、闲聊、改现有代码、在现有项目里加功能;
2. 当前目录不在任何 git 仓库内(git rev-parse --git-dir 失败),
   且当前目录没有 docs/ 或 AGENTS.md(不是已铺过的项目);
   例外:当前目录就是用户家目录 $HOME 本身时,~/.codex 是 Codex 自己的
   配置目录、不算项目标记——$HOME 不是 git 仓即视为满足本条;
3. 本次对话尚未为这个需求建过项目。

拿不准算不算新项目时:不触发,照常干活——宁可漏建,不可错建垃圾文件夹。
用户明说"不用建项目/就在这儿改"时:不触发。
已有仓库但缺 docs 的存量项目:不归本规则管,不要顺手补铺。

## 触发后动作(静默执行,全程不追问、不发选项)
1. 从需求句提炼英文 kebab-case 项目名(如"记账小工具"→ expense-tracker);
2. 定项目根:~/.codex/workflow-projects-root 文件存在则以其内容为根,
   否则默认 ~/Projects;创建 <根>/<项目名>/ 并进入;
   - <根>/<项目名>/ 已存在:不复用、不覆盖,视同"拿不准"——本次不自动
     建项目,一行说明后就地继续干活;
   - 创建或写入失败(含权限被拒):不重试;已建出的空目录删掉,
     不留残目录;一行说明"没能自动建项目,先就地干活",照常继续;
3. 按本 skill 步骤 4 的落盘清单与 `AGENTS.md.tmpl` 模板铺设(技术栈走
   基线不询问;能从用户需求句填实的填实,其余留模板占位;git init +
   初始 commit 含在内,步骤 5 的沙箱写权限约束原样适用);
4. 一行话告知:"已建项目 <名> 于 <路径>,这个需求后续都在里面做"——
   说完直接继续干用户真正要的活,不停下等确认。
```

从 `~/.codex/AGENTS.md` 删除本节（标记块之间的内容）即全局关闭——Codex 没有可检测的 opt-out 标志文件，关闭只能靠删除。

可直接复制执行的幂等安装脚本（在 zsh/bash 下验证通过，`$SKILL` 换成本机实际的 `SKILL.md` 路径；写法照抄本插件 `speak-human` skill 末尾「常驻安装」一节的先例：先删旧标记块、压平尾部空行，再追加新块，重复执行不会累积）：

```sh
SKILL="$HOME/.codex/plugins/cache/workflow-codex/skills/scaffold/SKILL.md"
AGENTS="$HOME/.codex/AGENTS.md"
mkdir -p "$(dirname "$AGENTS")"
touch "$AGENTS"

# 1) 删除旧的 auto-scaffold 标记块(幂等的关键),并把文件尾部连续空行压成一个
awk '
  /<!-- auto-scaffold:BEGIN -->/ {skip=1}
  !skip {print}
  /<!-- auto-scaffold:END -->/ {skip=0; next}
' "$AGENTS" > "$AGENTS.tmp" && mv "$AGENTS.tmp" "$AGENTS"
python3 - "$AGENTS" <<'PYEOF'
import pathlib, sys
p = pathlib.Path(sys.argv[1])
t = p.read_text()
t = (t.rstrip("\n") + "\n") if t.strip() else ""
p.write_text(t)
PYEOF

# 2) 从本 SKILL.md「Auto 模式与常驻安装」一节里提取规则片段
#    (第一个 ```markdown 围栏到下一个 ``` 之间的内容)
BODY=$(awk '
  /^## Auto 模式与常驻安装/ {insect=1}
  insect && /^```markdown$/ {f=1; next}
  insect && f && /^```$/ {exit}
  insect && f {print}
' "$SKILL")

# 3) 追加新标记块
{
  echo ""
  echo "<!-- auto-scaffold:BEGIN -->"
  echo "$BODY"
  echo "<!-- auto-scaffold:END -->"
} >> "$AGENTS"

echo "已写入 $AGENTS"
```

### 卸载（删掉常驻规则，可继续手动 `/scaffold` 触发）

`~/.codex/AGENTS.md` 不存在时视为未安装，只打印提示、不报错、不会凭空创建该文件：

```sh
AGENTS="$HOME/.codex/AGENTS.md"
if [ ! -f "$AGENTS" ]; then
  echo "未安装,无需卸载"
else
  awk '
    /<!-- auto-scaffold:BEGIN -->/ {skip=1}
    !skip {print}
    /<!-- auto-scaffold:END -->/ {skip=0; next}
  ' "$AGENTS" > "$AGENTS.tmp" && mv "$AGENTS.tmp" "$AGENTS"
  echo "已从 $AGENTS 移除 auto-scaffold 常驻块"
fi
```

安装脚本重复跑多次是安全的（先删旧块、压平尾部空行，再追加新块，不会累积）；卸载脚本跑在没有标记块的文件上也是安全的（不匹配就原样保留全文），文件本身不存在时也不报错。
