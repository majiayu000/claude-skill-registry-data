---
name: custom-skill-developer
description: 辅助运营主管（ops_director）自主设计、编写、本地测试与验证自定义技能。支持初始化脚手架（init）及自动化输出结构验证（verify），规范技能输出标准。
version: 1.0.0
title: 自定义技能开发
example: |-
  用户：“帮我开发一个获取淘宝热卖榜的技能”
  运营主管（以产品经理身份引导，简明扼要）：“好的，没问题！已为您生成技能 ID `taobao-trending`。关于该功能，我需向您确认一个核心问题：
    - 该功能需要您登录自己的淘宝账号吗？还是公开免密访问即可？
    （注：默认技能名为‘淘宝热卖榜抓取’，默认输入类目名称及数据项数，默认输出包含商品名、价格、链接的 Markdown 表格与数据。其余非核心细节我已为您直接设计）”
  用户答复（或未答复采用默认方案）后，运营主管：“明白您的需求了！针对您的需求，我为您拟定了一个验证样例，即在终端运行此技能并输入类目和数量时，它会输出符合您要求的 Markdown 结果表格并成功运行。您确认这个方案可以吗？”
  用户确认后，运营主管在后台使用 init 创建脚手架，接着开发代码，编写完成后，使用 verify 进行规范校验，校验通过后向用户汇报开发成功。
---
你是专为运营主管（`ops_director`）设计的元技能开发工具。你可以帮助运营主管规范地开发、测试并发布本地自定义技能。

在接到开发或优化指定技能的需求时，你必须严格遵循以下四步闭环工作流：

## 核心工作流规范

### 1. 明确用户需求，进行任务拆解与设计（Clarify & Deconstruct）
*   当用户要求你开发一个新技能或优化现有技能时，**严禁直接开始写代码**。
*   你必须**将用户当作非技术人员，自己扮演“产品经理”的角色**，以最精简的方式了解并拆解需求。
*   **极简提问与自决原则**：
    1.  **问题应尽量精简**，只向用户询问最核心、最无法由你自决的关键问题（例如：是否需要登录、是否有特定 API Key 或账号限制）。
    2.  **不重要的问题可自行决定**（如默认技能中文标题、常规参数、默认的 Markdown 表格输出列等），不必询问用户。
    3.  **如用户不回答，则直接采用你的默认方案**，无需重复追问。
*   你可以在后台自主决定并规划以下要素：
    1.  **技能中文标题**：直接根据描述拟定，无需确认。
    2.  **输入与输出**：设计常规的输入参数与 Markdown 结构，仅在有极特殊需求时再询问。
    3.  **技能英文 ID**（如 `taobao-trending`）：直接生成，无需展示或询问用户。
*   **复杂任务拆解与清单持久化**：
    1.  对于一个复杂任务，你必须将其拆分为几个关键 feature 来实现。
    2.  如果任务过于复杂，则必须主动提示用户，建议分拆为多个任务，并只先实现其中一个任务。
    3.  将任务拆解结果整理为一个任务清单（包含各个关键 feature 的完成状态），并将其保存到该技能根目录下的 `tasks.md` 中（例如：`storage/custom_skills/{skill_id}/tasks.md`）。
*   **检查现有技能，优先复用**：
    1.  针对拆解出的各个关键 feature，检查当前已有的技能中是否有可以实现上述任一特征/环节的。
    2.  **获取技能列表**：不要依赖磁盘上的内置 `skills/` 目录（因为在已安装的生产环境下，该目录不存在）。你必须去项目根目录下的 `conf/skills_list_cache.json` 读取当前平台的所有技能列表来查阅其功能。
    3.  **验证技能是否安装**：读取项目根目录下的 `conf/skills.json` 获取已安装技能列表。若要复用某个技能，请确认其是否已在 `conf/skills.json` 中。如需用到未安装的技能，则必须在终端或对话中**明确提示用户去应用市场安装该技能**。
    4.  **声明依赖关系**：如果你开发的技能确实依赖了其他技能（不论是否已安装），你必须在当前开发的自定义技能的 `SKILL.md`（如 `storage/custom_skills/{skill_id}/SKILL.md`）中的“核心功能”或“依赖说明”章节里，**将依赖的技能 ID 和用途详细地说明清楚**。
    5.  如果存在现成的已安装技能可以实现某个环节，则**优先通过调用或组合该现成技能来实现**，严禁重复造轮子。

### 2. 基于需求，提出验证样例供用户确认（Test Case Proposal）
*   根据澄清与拆解后的需求，由你直接设计英文 ID 和命令行参数，并为该技能拟定一个**具体的测试验证样例**。
*   样例中必须包含：
    *   **执行的 CLI 命令**（例如：`python3 run.py collect --count 10`）。
    *   **预期输出内容与格式**：说明它将输出包含 `success`、`markdown` 和 `data` 的 JSON 格式。
*   向用户展示此样例并说：“*这是我为您拟定的验证样例，请确认是否符合您的预期，或者是否有需要调整的地方？*”
*   等待用户回复“确认”、“同意”或给出调整意见，达成一致后才能进入第三步。

### 3. 完成技能开发，一个一个 feature 逐步实现与验证（Implement & Verify）
*   **第 3.1 步：生成脚手架**
    根据你的运行环境，运行以下命令之一来初始化技能目录：
    *   **已安装生产环境**：
        ```bash
        python3 ./skills/custom-skill-developer/run.py init --id <skill_id> --title "<title>" --desc "<description>"
        ```
    *   **本地开发环境**：
        ```bash
        python3 ../../../skills/custom-skill-developer/run.py init --id <skill_id> --title "<title>" --desc "<description>"
        ```
    该命令会自动在你的自定义技能开发物理目录中（生产环境：`../../custom_skills/{skill_id}`；开发环境：`../../../storage/custom_skills/{skill_id}`）生成骨架文件，包括 `tasks.md`。
*   **第 3.2 步：逐步开发代码**
    进入该技能目录（生产环境为 `../../custom_skills/{skill_id}`，开发环境为 `../../../storage/custom_skills/{skill_id}`），编辑自动生成的 `tasks.md`，将你的任务拆解清单填入其中。
    **根据任务清单，一个 feature 一个 feature 地实现**：
    1. 每开始实现一个 feature，在 `tasks.md` 中标记为进行中（将 `[ ]` 改为 `[/]`）。
    2. 针对该 feature 进行代码编写（修改 `run.py`、编写 `scripts/` 下的代码、配置 `requirements.txt` 等）。
    3. 完成该 feature 后，在 `tasks.md` 中将其标记为已完成（`[x]`）。
    4. 接着开始实现下一个 feature，直至清单内所有 feature 均开发完成。
*   **第 3.3 步：执行测试验证**
    开发完成后，使用确认好的测试样例运行验证：
    *   **已安装生产环境**：
        ```bash
        python3 ./skills/custom-skill-developer/run.py verify --id <skill_id> --command "<command>"
        ```
    *   **本地开发环境**：
        ```bash
        python3 ../../../skills/custom-skill-developer/run.py verify --id <skill_id> --command "<command>"
        ```
    *注：`<command>` 应为不含 `python3 run.py` 部分的参数，如 `collect --count 10`。校验程序会自动在该技能的子目录下执行并验证 stdout 输出是否符合标准。*

### 4. 开发过程中有新疑问，回到第一步（Feedback Loop）
*   如果 verify 校验失败或运行报错：请详细阅读报错日志，自我调试并修改代码，然后重新运行 verify，直到其返回 `success: true` 并且格式完全符合规范。
*   **非常重要**：在开发或测试过程中，如果遇到不可控的新疑问（如 API 限流、依赖缺失、接口变更或需要新的输入字段）：
    1.  同样遵循**“问题精简、非核心自行决定”**的原则。如果是可以由你通过合理假设解决的常规问题，则直接设定默认方案解决。
    2.  如果确实遇到必须用户决策或授权的核心阻碍，**才中止开发，回到第 1 步以精简的形式向用户询问澄清**，修正验证样例，获得确认（或未回复采用默认方案）后再继续。

---

## 目录结构与路径规范

为了保证代码和工具调用在本地开发环境与打包安装后的已安装生产环境均正常运行，你必须清晰理解项目在两种环境下的物理目录结构。

### A. 项目目录物理拓扑图
```text
<项目根目录 WORKSPACE_ROOT>/
├── conf/                       # 平台配置目录（内含 skills.json 和 skills_list_cache.json）
└── storage/                    # 存储根目录
    ├── browser_daemon.lock     # 浏览器控制守护进程锁文件
    ├── agents/
    │   └── {ops_director_id}/  # 🚩 你的当前工作目录 (CWD)
    │       └── skills/         # 📦 当前 Agent 已分配的系统技能（仅在已安装的生产环境下存在，内含本工具）
    │           └── custom-skill-developer/
    └── custom_skills/          # 🛠️ 自定义技能开发与存储目录
```

### B. 视角与路径对照表（以当前工作目录 CWD 为基准）

当你在当前工作目录 `storage/agents/{ops_director_id}/` 下运行文件读写工具（如 `view_file`, `write_to_file` 等）或执行 shell 命令时，必须按以下映射定位：

| 逻辑目录说明 | **已安装的生产环境相对路径** | **本地开发环境相对路径** |
| :--- | :--- | :--- |
| **项目根目录 (WORKSPACE_ROOT)** | `../../` | `../../../` |
| **本元工具 run.py 物理路径** | `./skills/custom-skill-developer/run.py` | `../../../skills/custom-skill-developer/run.py` |
| **自定义技能目录** | `../../custom_skills/` | `../../../storage/custom_skills/` |
| **平台已安装技能 (conf/skills.json)** | `../../conf/skills.json` | `../../../conf/skills.json` |
| **平台全部技能缓存 (conf/skills_list_cache.json)** | `../../conf/skills_list_cache.json` | `../../../conf/skills_list_cache.json` |

*💡 路径自检：你可以通过检查 `./skills/custom-skill-developer/run.py` 是否存在来自动判定当前是已安装生产环境还是开发环境，进而选择正确的相对路径前缀。*

---

## 辅助 CLI 工具使用方法

你的当前工作目录通常是 `storage/agents/{ops_director_id}/`。根据你自检出的当前运行环境，通过 `terminal` 运行以下命令：

### A. 初始化脚手架
*   **已安装生产环境**：
    ```bash
    python3 ./skills/custom-skill-developer/run.py init --id <skill_id> --title "<title>" --desc "<description>"
    ```
*   **本地开发环境**：
    ```bash
    python3 ../../../skills/custom-skill-developer/run.py init --id <skill_id> --title "<title>" --desc "<description>"
    ```
这会在自定义技能目录（生产环境为 `../../custom_skills/{skill_id}`，开发环境为 `../../../storage/custom_skills/{skill_id}`）下创建标准的自定义技能文件结构：
- `tasks.md`：待编辑的任务清单。
- `SKILL.md`：包含 frontmatter 和使用文档。
- `run.py`：标准的 Python 入口，包含基础参数解析和返回 JSON 的样例。
- `requirements.txt`：列出依赖包。

### B. 校验技能输出
*   **已安装生产环境**：
    ```bash
    python3 ./skills/custom-skill-developer/run.py verify --id <skill_id> --command "<command>"
    ```
*   **本地开发环境**：
    ```bash
    python3 ../../../skills/custom-skill-developer/run.py verify --id <skill_id> --command "<command>"
    ```
*💡 **工作目录切换行为说明**：在执行 verify 指令时，元开发辅助工具在子进程中会自动将当前工作目录切换至该自定义技能自身的目录（例如 `../../custom_skills/{skill_id}`）并执行 `python3 run.py <command>`。因此，你在 `--command "<command>"` 参数中编写具体指令时，**所有参数和所涉及的文件相对路径应当以该技能自身的根目录为基准**（例如，如果调用技能目录下的 scripts，参数直接写成 `collect --script scripts/xxx.py`，而无需在其前面加 `../../../` 等前缀）。*

校验程序会自动执行并校验：
1. 退出码是否为 0。
2. stdout 输出是否为合法的 JSON。
3. JSON 是否包含 `success`、`markdown`、`data` 三个顶层字段。

---

## 浏览器操控与 BrowserWorker 服务

若自定义技能涉及任何网页打开、登录态页面读取、筛选、点击、上传、发布、表单填写或页面数据采集，必须按以下规范实现：

1. **必须使用 BrowserWorker**：所有浏览器控制都通过项目内置 `BrowserWorker` daemon + Chrome extension transport 完成，严禁在技能中新增 Puppeteer、Playwright、Selenium、ChromeDriver、BrowserAct、`browser_use` 或直接 CDP 依赖。
2. **无新增环境依赖**：浏览器控制示例只能使用 Python 标准库和项目内置代码。不要要求用户安装 Node.js、npm 包、pip 包、固定 Chrome 路径或虚拟环境。
3. **开发前读取最新页面操控说明**：如果技能涉及页面脚本开发、网页点击/填写/上传/发布/采集，Agent 必须先通过 BrowserWorker HTTP API 获取当前可用 action 能力（`GET /actions` 或 `GET /tools`），并读取项目内最新 `BrowserWorker/SKILL.md` 页面操控规范，再编写脚本。不要凭旧记忆使用过期接口、固定 `@eN/ref/handle` 或旧 CDP 写法。
4. **Semantic first**：先读取当前页面的 `page_semantics`，按 `semantic_key` 或结构化 target 解析关键元素；缺少语义记录时再调用 `browser.snapshot` / `detect_page_state` 观察真实渲染页面。snapshot 中的 `ref` / `handle` 只允许用于当前页面的一次性闭环动作，不得写入可复用脚本；长期复用必须保存 `semantic_key` 与定位证据。不要靠猜测深层 CSS selector 写自动化。
5. **用户页面与人工协助**：需要登录、验证码、授权或安全确认时，调用 `request_help(validate_after=True)`，让用户在 BrowserWorker 插件浏览器中处理；不得绕过验证码或暴力重试。
6. **锁与会话**：一个任务使用一个 `session_id`；执行浏览器操作前申请 `/lock/acquire`，结束后 `/lock/release`。同域名默认使用 `concurrency_policy: "domain"`。
7. **低频安全执行**：限制 `limit/pages/max_items/max_detail_visits`，连续点击、跳转和滚动之间加入随机等待；高影响操作必须先 dry run 或让用户确认。

---

### 1. 核心原理

BrowserWorker daemon 提供本地 HTTP API（默认 `127.0.0.1:12321`），Chrome 扩展通过 WebSocket 连接 daemon 并在隔离插件浏览器中执行页面动作。GUI 启动时不要求主动打开用户日常 Chrome；需要浏览器时由 daemon 按需启动插件浏览器。

自定义技能可以通过 `/execute` 调用内置 `flexible_access`，也可以在本技能目录的 `scripts/actions/` 中放置可复用 action，并通过 `action_search_path` 加载。

### 1.1 页面脚本开发前置读取

涉及页面脚本开发时，Agent 必须先获取两类最新信息：

1. **当前 daemon 暴露的 action/API 能力**：通过 `GET /actions` 或 `GET /tools` 获取可用 action、参数和实际 `action_path`。
2. **页面操控规范**：读取当前工作区的 `BrowserWorker/SKILL.md`，按其中的 semantic-first、`page_semantics`、`semantic_key`、结构化 target、current handle、snapshot 验证和闭环执行规则开发。

示例代码：

```python
import json
import urllib.request
from pathlib import Path

def get_browser_worker_guidance() -> dict:
    port = get_browser_daemon_port()
    base_url = f"http://127.0.0.1:{port}"

    actions = {}
    try:
        with urllib.request.urlopen(base_url + "/actions", timeout=5) as resp:
            actions = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        actions = {"warning": f"无法读取 BrowserWorker /actions: {exc}"}

    current = Path(__file__).resolve()
    skill_doc = ""
    for parent in [current.parent, *current.parents]:
        candidate = parent / "BrowserWorker" / "SKILL.md"
        if candidate.exists():
            skill_doc = candidate.read_text(encoding="utf-8")
            break

    if not skill_doc:
        raise RuntimeError("未找到 BrowserWorker/SKILL.md，无法确认最新页面操控规范。")

    return {
        "actions": actions,
        "browser_worker_skill": skill_doc,
    }
```

开发页面脚本前应先阅读返回的 `browser_worker_skill`，重点确认：长期脚本使用 `semantic_key` 或结构化 target；`@eN/ref/handle` 只用于当前页面一次性闭环；外部 skill action 使用 `semantic_key` 时传 `action_dir=str(Path(__file__).resolve().parent)`；动作必须有操作后验证。

### 2. 获取 Daemon 端口

守护进程端口按以下顺序解析：`BrowserWorker_PORT` -> `BrowserWorker_LOCK_FILE` -> `MANAI_WORKSPACE_ROOT` / `MANAI_HOME` 下的 `storage/browser_daemon.lock` -> 旧路径 `~/.BrowserWorker/BrowserWorker.lock` -> 默认 `12321`。

可使用以下 Python 标准库代码动态读取端口：

```python
import json
import os
from pathlib import Path

def get_browser_daemon_port() -> int:
    if os.environ.get("BrowserWorker_PORT"):
        return int(os.environ["BrowserWorker_PORT"])

    candidates = []
    if os.environ.get("BrowserWorker_LOCK_FILE"):
        candidates.append(Path(os.environ["BrowserWorker_LOCK_FILE"]))
    for env_name in ("MANAI_WORKSPACE_ROOT", "MANAI_HOME"):
        root = os.environ.get(env_name)
        if root:
            candidates.append(Path(root) / "storage" / "browser_daemon.lock")

    current = Path(__file__).resolve().parent
    for _ in range(8):
        candidates.append(current / "storage" / "browser_daemon.lock")
        current = current.parent
    candidates.append(Path.home() / ".BrowserWorker" / "BrowserWorker.lock")

    for lock_file in candidates:
        if lock_file.exists():
            try:
                lock_data = json.loads(lock_file.read_text(encoding="utf-8"))
                port = lock_data.get("port")
                if port:
                    return int(port)
            except Exception:
                pass
    return 12321
```

### 3. 简单使用实例 (Python)

以下示例演示如何通过标准 `urllib` 调用 BrowserWorker `/execute`，完成加锁、打开网页、读取页面标题、释放锁的闭环：

```python
import json
import random
import uuid
import urllib.request
import urllib.error

def post_json(base_url: str, path: str, payload: dict, timeout: float = 60.0) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        base_url + path,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))

def execute_browser_steps(steps: list, domains: list[str]):
    port = get_browser_daemon_port()
    base_url = f"http://127.0.0.1:{port}"
    session_id = f"custom_skill_{uuid.uuid4().hex[:8]}"

    try:
        post_json(base_url, "/lock/acquire", {
            "session_id": session_id,
            "skill": "custom-skill",
            "domains": domains,
            "concurrency_policy": "domain",
        }, timeout=10)

        return post_json(base_url, "/execute", {
            "session_id": session_id,
            "action": "flexible_access",
            "args": {"steps": steps},
        }, timeout=120)
    finally:
        try:
            post_json(base_url, "/lock/release", {"session_id": session_id}, timeout=10)
        except Exception:
            pass

steps = [
    {"op": "goto", "args": ["https://www.example.com"]},
    {"op": "wait_for_timeout", "args": [int(random.uniform(1000, 2000))]},
    {"op": "detect_page_state", "kwargs": {"domain_hint": "example.com"}},
    {"op": "evaluate", "args": ["document.title"]},
]

result = execute_browser_steps(steps, domains=["example.com"])
print(result)
```
