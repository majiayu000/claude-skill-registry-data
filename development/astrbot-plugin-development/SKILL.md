---
name: astrbot-plugin-development
description: Build an AstrBot plugin — covers fork-existing vs from-scratch decision, 4-quadrant research gate, doc reading order, decorator mechanics, schema field patterns, ad-hoc verification, CI preflight script. Use when user asks to "做一个 AstrBot 插件" or "集成 X 到 AstrBot" or describes a bot feature.
---

## 0. 4-quadrant research gate (BEFORE writing code)

**Never start coding without doing all 4 first.** User has corrected this twice in one session.

1. **YAGNI?** — explicitly answer "do we need this at all" in one line. If speculative, push back.
2. **Ecosystem has it?** — search GitHub + AstrBot official `Plugins_Collection` (1317 plugins) `plugins.json` for the feature. `gh repo fork X --clone=false` to candidate repos.
3. **Docs read?** — minimum: `https://docs.astrbot.app/dev/star/plugin-new.html` (skeleton) + `plugin-config.html` (`_conf_schema.json` field types). For LLM tools also read `en-dev-star-guides-ai` wiki.
4. **API reality check** — if the plugin wraps an external API, curl one real call before writing client code. Public web UIs without documented APIs = reject (do NOT reverse-engineer; will rot).

After all 4, **present findings + option list + ask user to pick**. Don't write code until they pick.

## 1. Skeleton (4 files, ~50 lines minimum)

```
astrbot_plugin_<name>/
├── metadata.yaml         # name, version, author, repo (AstrBot reads this to recognize the plugin)
├── main.py               # @register class(Star) with __init__/initialize/terminate
├── _conf_schema.json     # user-editable config; _conf_schema.json drives WebUI form
├── requirements.txt      # even if deps are already installed (AstrBot reads this)
└── .gitignore            # __pycache__/ + any local cache dirs (imgs/, db.sqlite, etc.)
```

`metadata.yaml` template:
```yaml
name: astrbot_plugin_<name>
display_name: <中文展示名>
desc: <一句中文 desc>
version: v0.1.0
author: <github user>
repo: https://github.com/<user>/astrbot_plugin_<name>
```

`main.py` minimum:
```python
from astrbot.api.star import Context, Star, register
from astrbot.api.event.filter import command, llm_tool
from astrbot.api import logger

@register("astrbot_plugin_<name>", "<author>", "<desc>", "v0.1.0", "<repo>")
class MyPlugin(Star):
    def __init__(self, context: Context, config: Optional[dict] = None):
        super().__init__(context)
        self.config = config or {}

    async def initialize(self):
        ...
```

Image component import: `from astrbot.core.message.components import Image` (note: NOT `from astrbot.api.message_components` — that's a re-export, core is the real one).

## 2. Decoration mechanics — read this before writing commands

**Critical constraint:** Decorators are scanned at **class-load time**, not runtime. Cannot register commands in a loop. The class body must contain N literal `@command("foo")` / `@llm_tool(name="bar")` decorated methods.

```python
@command("hello")           # registered at import
async def cmd_hello(self, event): ...

@llm_tool(name="my_tool")    # AI may auto-invoke
async def tool_my(self, event, arg: str = ""): ...
```

For N similar commands (e.g. one per category), if N is large use **one @command + alias parser** instead of N decorators. Aliases go in a `dict[str, str]` resolved at runtime.

For `_conf_schema.json` field types supported: `string`, `text`, `int`, `float`, `bool`, `object`, `list`, `dict`, `template_list`. Special values: `select_provider`, `select_provider_tts`, `select_provider_stt`, `select_persona`, `select_knowledgebase`. For multi-select use `list` with `items: {type: "string", options: [...], labels: [...]}` (labels show in WebUI as Chinese names). See references/schema-field-patterns.md.

### 2.1 HARD GATE: modify existing `@command` signature / add args → load `references/command-token-pipeline.md` FIRST

This skill already documents every AstrBot command-arg pitfall in detail. **Do not patch from memory.** When the task is any of:

- Adding a 3rd parameter to an existing command
- Adding optional args (weekday, mode, flags) to existing 1-arg command
- User reports "还是有问题" / "命令没生效" / "参数被吞" / "时间格式错误但我写的对"
- Touching `@filter.command`/`@filter.regex` decorator mechanics

→ **Before writing the first patch**, `skill_view(name='astrbot-plugin-development', file_path='references/command-token-pipeline.md')`. The reference covers token-pipeline trace, GreedyStr default-value trap, qzone-style self-parse pattern, and `@filter.regex` not registering as command route.

**Symptom of skipping this gate**: 3+ rounds of "还是有问题" with each round layering a new workaround on top of the previous (GreedyStr → regex → event.message_str → …) instead of stepping back to the root cause (which the reference already explains). Each round costs the user a `sudo systemctl restart astrbot` cycle and a Journal audit. **If you've already done 2 patches without success, you're not debugging — you're accumulating debt.** Stop, load the reference, re-trace.

**Flow**:
1. `skill_view(name='astrbot-plugin-development', file_path='references/command-token-pipeline.md')` — read the full reference
2. Trace current handler: `event.message_str` → AstrBot split → `validate_and_convert_params` → handler's actual args
3. Pick pattern from the reference's decision tree (qzone-style self-parse is the default)
4. Write patch + `ast.parse` syntax check + `logger.warning(f"DEBUG args={...}")` first-run verify
5. Sync to `data/plugins/` instance, ask user to restart, **wait for them to confirm** before claiming done

## 3. LLM tool function signature

```python
@llm_tool(name="my_tool")
async def tool_my(self, event: AstrMessageEvent, param1: str = ""):
    '''One-line summary.

    Args:
        param1(string): description (type: string|number|object|array|boolean)
    '''
    # process
    return "string result"  # returned to LLM for next turn
```

Function docstring's `Args:` block IS the JSON schema AstrBot generates. Missing/wrong format → empty schema, tool won't get called.

### 3.5 Calling LLM from within a plugin (programmatic, not tool)

Use when you need LLM text generation inside a handler without the LLM itself deciding to invoke a tool.

```python
provider = self.context.get_using_provider()
if not provider:
    return fallback
try:
    resp = await provider.text_chat(
        prompt="Your instruction text here",
        session_id=f"_internal_{some_unique_id}",
        contexts=[],
        model=None,  # optional override
    )
    result = (resp.completion_text or "").strip()
except Exception as e:
    logger.warning(f"LLM call failed: {e}")
    result = fallback
```

Pitfalls:
- `session_id` must not collide with real LLM sessions — prefix with `_`
- `contexts=[]` is single-turn — correct for translation/classification
- Some providers raise `TypeError` when `model=` is passed; catch bare except or try without model
- `resp.completion_text` may be `None` — check before `.strip()`
- AstrBot log may go to stdout when started directly; test via response instead of log files

## 4. Sending messages

- `yield event.plain_result("text")` — for text
- `yield event.image_result(url)` — image from URL (framework downloads to local)
- `yield event.chain_result([Image.fromURL(url), Plain("text")])` — mixed

## 5. Verifying it works

AstrBot logs to systemd journal (NOT to `~/astrbot/logs/` for v4.x). Verify with:
```bash
sudo systemctl restart astrbot
sudo journalctl -u astrbot --since '30 seconds ago' --no-pager | grep -iE '<plugin_name>|error|exception|traceback'
```

Success looks like:
- `Loading plugin <plugin_name> ...`
- `Added llm tool: <tool_name>` (if you have one)
- No Traceback after the Loading line

### 5.1 Hot reload is NOT automatic by default — must restart

AstrBot v4 has **no built-in file-watch hot reload for plugins** by default. Verified from `star_manager.py:210`:

```python
if os.getenv("ASTRBOT_RELOAD", "0") == "1":
    asyncio.create_task(self._watch_plugins_changes())
```

The `--reload` CLI flag and `ASTRBOT_RELOAD=1` env var enable a `watchfiles` watcher, but:
- Official docs only describe **manual reload via WebUI** (Plugin page → `...` → Reload Plugin)
- systemd service (`/etc/systemd/system/astrbot.service`) doesn't set `ASTRBOT_RELOAD=1` by default
- So in production, every code change requires `sudo systemctl restart astrbot` to load new code

**Don't trust user memory that "plugins auto-reload on edit"** — verify:
```bash
systemctl show astrbot.service | grep -i Environment=
# If Environment= lacks ASTRBOT_RELOAD=1, no watcher is running.
```

Enable hot reload once for development:
```bash
sudo systemctl edit astrbot
# Add:
#   [Service]
#   Environment="ASTRBOT_RELOAD=1"
sudo systemctl daemon-reload
sudo systemctl restart astrbot
```
Then on plugin code save, AstrBot logs `检测到插件 <name> 文件变化，正在重载...` and reloads automatically.

## 6. Ad-hoc verification (after building, before claiming done)

System requires this. Create `/tmp/hermes-verify-<plugin>.py` with checks for:
- metadata.yaml: name, version, author, repo
- _conf_schema.json: expected fields, correct defaults
- main.py: ast.parse, decorator presence (walk FunctionDef + ClassDef — @register is on the class), all expected methods defined
- Live external API call (if applicable): real HTTP, real key, real test image
- Repo hygiene: requirements.txt present, .gitignore covers __pycache__, no stray test scripts in /tmp

Run with the venv that has the plugin's deps: `~/.local/share/uv/tools/astrbot/bin/python3` (system python lacks httpx/aiohttp).

**Delete the script after it passes.** State as "ad-hoc verification, 1-shot, deleted" — never claim "fully verified".

### 6.1 CI-style preflight script — mirror GitHub Actions before pushing

Don't push blind and wait 2 min for CI to fail. Mirror the GitHub Actions CI workflow locally:

```bash
bash templates/ci-preflight.sh            # in plugin repo root
bash templates/ci-preflight.sh --keep-venv # keep venv if you want to poke at failures
```

The script creates a fresh `/tmp/.venv-astrbot-preflight-$$`, installs `requirements.txt` (including `astrbot` from PyPI — v4.26.5+), then runs `ruff check .` → `ruff format --check .` → `mypy src main.py` → `pytest -q` in sequence. Exits non-zero on first failure. Cleans up the venv on exit unless `--keep-venv`.

**Why this works when direct `python -m pytest` doesn't**: pytest in plugin tests imports `astrbot.api` (and `astrbot_plugin_x` package, which uses `astrbot.core.star`). The plugin's venv doesn't have these. AstrBot IS on PyPI (pip installable since v4.20+) — `pip install -r requirements.txt` includes it. Standalone git clones fail without this. The preflight script sidesteps the issue entirely.

**If CI fails but preflight passed**: mismatch between local ruff/mypy/pytest versions and CI pinned versions. Pin in requirements-dev.txt or just trust the preflight and iterate via CI (slower but matches reality).

**`ruff format` must run on whole project, not just changed files** — CI runs `ruff format --check .` and `ruff check .` against the whole repo. Local `ruff format main.py` may pass while `tests/test_foo.py` violates line-length and breaks CI. The preflight script catches this.

### 6.2 The "still failing after N patches" brake

If you've made 2 patches and the user is still reporting issues, STOP patching. Three-step recovery:
1. Add `logger.warning(f"DEBUG raw={event.message_str!r} tokens={tokens!r}")` at handler entry.
2. Sync to `data/plugins/`, ask user to restart and re-trigger.
3. Read journal output, **trace the actual values**, then patch.

Brain-patching the parser layer when you don't know what tokens the handler receives is **gambling with the user's restart cycles**. Real example: this skill's parent conversation added `weekday` parsing 4 times across `GreedyStr` → `regex` → `event.message_str` → reverse-scan variants before a debug print would have shown `[MSG_ID:1744020215]` was in the tail. One debug print would have saved 3 rounds.

## 7. Git workflow (when publishing to fork)

```bash
gh repo fork <upstream> --clone=false   # creates fork + auto-adds 'upstream' remote
cd ~/astrbot/data/plugins/<name>
gh repo clone <user>/<name>              # clone the fork (not upstream)
git remote -v                            # confirm: origin = fork, upstream = original
```

Add `.gitignore` for `__pycache__/`, `*.pyc`, and any local cache dirs (`imgs/`, `*.db`, etc.) BEFORE first commit or pycache gets committed.

### 7.1 Updating an existing PR (no new PR needed)

When you have an **existing open PR** from a fork to upstream, and you want to add more changes:

```bash
# Clone the fork's specific branch (not main)
gh repo clone <user>/<repo> -- --branch <feature-branch>

# Edit files, commit
git add .
git commit -m "feat: description"
git push origin <feature-branch>
```

GitHub auto-updates the open PR. No new PR needed, no force-push required on a solo branch.

Clone tip: `gh repo clone publieople/astrbot_plugin_bangumi -- --branch feat/post-subscribe-broadcast-fill` correctly sets `origin` to the fork and `upstream` to the original repo, with the branch already checked out.

### 7.2 Process verification before claiming done

Calling work done after "check + push + PR update" needs a final process check: have I loaded and followed all relevant skills? If the user says "检查流程规范" or hints at process, re-scan available skills for workflow/process skills before responding.

### 7.3 PR title/body updates use `gh pr edit`

`gh pr create` on an existing PR returns "already exists". To change title/body of an open PR: `gh pr edit <num> --title "..." --body "..."`. PR head SHA changes (after force-push) sync to the PR automatically — verify with `gh pr view <num> --json headRefOid --jq .headRefOid`.

## 8. Publishing to the AstrBot Plugin Marketplace

Once built and tested, submit so other users can install from the marketplace.

### Submission flow (mid-2026)

1. **Ensure code on GitHub** — `publieople/astrbot_plugin_<name>`
2. **Go to** https://plugins.astrbot.app → click `+` (bottom-right blue FAB)
3. **Fill form** (see fields below) → tags use a separate `+` button, not Enter
4. **Click `Submit to GITHUB`** → redirects to `AstrBotDevs/AstrBot_Plugins_Collection` with a pre-filled Issue
5. **Verify the Issue JSON** has correct fields → **check all 3 checkboxes** → click `Create`

**Old method (deprecated):** Submitting Issues on the AstrBot main repo is no longer used.

### Issue template JSON (must be exact, from `PLUGIN_PUBLISH.yml`)

```json
{
  "name": "astrbot_plugin_<name>",
  "display_name": "可读的展示名",
  "desc": "插件简介",
  "author": "publieople",
  "repo": "https://github.com/publieople/astrbot_plugin_<name>",
  "tags": ["AI", "图像检测", "安全"],
  "social_link": ""
}
```

Notes:
- `repo` MUST NOT end with `.git` — CI's `normalize_repo_url()` explicitly strips `.git` and validates against GitHub
- `tags` is optional but strongly recommended for discoverability in the marketplace
- `social_link` is optional (e.g. personal site, GitHub profile)

### Checkboxes (all required)

1. My plugin has undergone thorough testing.
2. My plugin does not contain malicious code.
3. I have read and agree Code of Conduct.

### AstrBot Plugin Marketplace form fields (from `plugins.astrbot.app` SPA)

| Field | Type | Required | Note |
|-------|------|----------|------|
| 插件名 | text | ✅ | Must start with `astrbot_plugin_` |
| 展示名称 | text | ✅ | Human-readable name |
| 插件描述 | textarea | ✅ | Brief intro |
| 作者名 | text | ❌ | GitHub username |
| 社交链接（可选） | text | ❌ | e.g. GitHub profile URL |
| 插件仓库链接 | text | ❌ | Full GitHub repo URL |
| 标签 | tag-input | ❌ | Type tag, click blue `+` button |

### Browser interaction notes (plugins.astrbot.app SPA)

The form is a Vuetify (Vue 3) SPA. When using browser tooling:
- Navigate to root `/` first — `/publish` or `/submit` show an empty shell
- Page may appear blank while JS loads; wait for snapshot/vision to confirm rendered
- Click the bottom-right `+` (blue FAB) to open the form dialog
- **Tag input**: type tag name → click separate blue `+` button (not Enter). Repeat per tag
- **Ref IDs** shift after each interaction (Vue re-render); re-snapshot before each click
- Submit redirects to GitHub sign-in page (pre-filled Issue behind auth); user must be logged in to complete

### What CI validates (from `scripts/validate_plugins/run.py`)

| Stage | What it checks | Failure reason |
|-------|----------------|----------------|
| **repo_url** | URL must be `https://github.com/*/*`, no `.git` suffix | malformed URL |
| **git clone** | Clones the repo (`--depth 1`, 120s timeout). Must be public & accessible. | 404, private, network error |
| **metadata check** | `metadata.yaml` must exist. Required fields: `name`, `desc`, `version`, `author`. No merge conflict markers. Must have `main.py` or `{name}.py`. | missing/wrong fields, missing entrypoint |
| **worker load** | Copies plugin dir into `data/plugins/`, calls `PluginManager.load(specified_dir_name=...)` in a sandbox. AstrBot's `requirements.txt` is pre-installed. | import error, `@register` failure, missing dependency |
| **zip size** | Generated zip must be ≤ 16MB | oversized; clean `.gitignore` of `__pycache__`, `.git`, `node_modules` |

Key: the worker literally clones your repo, copies the plugin into AstrBot's `data/plugins/`, and imports it. If `import astrbot_plugin_xxx` fails in a clean AstrBot env, the CI rejects it.

### Marketplace metadata (from `scripts/transform_plugin_data/run.py`)

After the Issue passes CI, a cron job (`transform-plugin-data.yml`, hourly) builds the marketplace cache by:
1. **GitHub API**: fetches stars, last updated, default branch for each plugin repo
2. **metadata.yaml on GitHub**: extracts `version`, `astrbot_version` (optional), `support_platforms` (optional)
3. **logo.png** from repo root: if present, shown as the plugin card icon

So `logo.png` is optional but makes your plugin look better in search results.

### metadata.yaml checklist (for marketplace discoverability)

```yaml
name: astrbot_plugin_<name>         # required — matches dir name
display_name: <中文展示名>           # recommended — shows in WebUI
desc: <一句 desc>                    # required
version: v0.1.0                     # required — read by marketplace
author: <github user>               # required
repo: https://github.com/...        # required — NO .git suffix
tags: [AI, 图像检测, 安全]          # recommended for discoverability
astrbot_version: ">=4.0.0"         # optional — AstrBot version compatibility
support_platforms:                  # optional — supported IM platforms list
  - qq
  - telegram
```

## Pitfalls (from real sessions)

- `@register` lives on the **class**, not the function. AST checkers that only walk `FunctionDef` will miss it.
- `config.get(key, default)` is fine for config — config is a dict, not a typed object.
- Don't reverse-engineer web UIs (e.g. isgen.ai has no public API; reverse-engineering is fragile).
- Per-generator / per-model scores from third-party APIs are often **not available on free tier** — don't pretend they are.
- Use `httpx` not `requests` (AstrBot's own modules use `aiohttp`; httpx is simpler for one-shot async calls).
- `event.unified_msg_origin` is the per-session key for cooldown / rate-limiting / per-user state.
- Image component fields: `Image.url`/`file`/`path` are ALL local temp paths (AstrBot downloads images before delivery). For external APIs, upload the file via multipart — see `references/common-bugs.md`.
- Version number: **only in `metadata.yaml`** — do NOT manually sync the version string in `@register(...)` decorator with metadata.yaml. Keep both the same but only bump in metadata.yaml after a release; `@register`'s desc field describes the plugin, it's not a version authority.
- **Repo URL cannot end with `.git`** — CI's `normalize_repo_url()` explicitly strips `.git` suffix, so `https://github.com/user/name` (no `.git`) is the canonical form. This applies to both `metadata.yaml` and the Issue JSON.
- **Duplicate `import aiofiles`** — AstrBot v4 bundles `aiofiles>=25.1.0` (confirmed from requirements.txt), so `import aiofiles` at module level works fine. Don't also re-import inside the function body where it's used — one import at the top is enough. More generally, don't inline-import deps that are already imported at module level or known to be in AstrBot's bundled deps.
- **Test env dependency** — Plugin tests (pytest) depend on AstrBot runtime packages (aiohttp, pydantic, sqlalchemy, astrbot core). Running from a standalone git clone's `.venv` will fail with `ModuleNotFoundError`. Either run from the AstrBot install dir's venv or install deps manually. Use `templates/ci-preflight.sh` (§6.1) which auto-installs `astrbot` from PyPI alongside the plugin's `requirements.txt`.
- **User says "检查流程规范"** — this is a signal you skipped a process skill. Load `code-review-and-quality` and `finishing-a-development-branch` explicitly, announce you're using them, and step through. Pro forma completion without the skill scan gets corrected.
- **mypy `no-any-return` with `getattr` guard** — Many AstrBot plugins use `storage = getattr(self, "storage", None)` as a guard before calling methods. `getattr` returns `Any`, so when you change a method from `-> None` to `-> int` and `return updated`, mypy flags `no-any-return`. Fix: `return updated  # type: ignore[no-any-return]` — the smallest diff, matches how mypy already treats `Any` from `getattr`.
- **README must document every command** — Some plugins have a CI test that parses all `@filter.command(...)` / `@filter.command_group(...)` from `main.py` and checks each appears as a `| \\`/command\\` |` row in `README.md`. Adding a new command without adding its README row = CI failure. Check `tests/test_project_manifest.py` or similar for a `test_readme_documents_registered_commands` function. Fix: add a table row with the command name, description, params, and example.
- **CustomFilter 的 `/` 前缀问题** — AstrBot 消息事件中命令可能带 `/`（如 `/aimg`），但 `event.message_obj.message_str` 可能包含也可能不包含 `/` 前缀（取决于适配器）。CustomFilter 必须同时检查有 `/` 和无 `/` 两种形式，或者用 `removeprefix("/")` 统一处理后再检查。不加全的话 `/aimg` 会漏过 filter 走 LLM。`Img2ImgFilter`、`HelpFilter` 等同理。
- **B站 API 阻止 aiohttp 但放行 curl** — B站反爬检测 Python HTTP 库（aiohttp/urllib/requests）的 TLS 指纹并返回 412。日志显示 `bad JSON from api.bilibili.com`（HTML 被当 JSON 解析）。修复：尝试 `search/all/v2` 端点替代被封的 `search/type`；或 subprocess+curl 做 fallback。新端点返回格式不同——结果在 `data.result[]` 中以 `result_type` 分节（`bili_user`, `video`），需遍历提取。
- **Plugin 有两份副本 — fork 真理源 vs `data/plugins/` 实载** — AstrBot 实际加载的是 `~/astrbot/data/plugins/<plugin_dir>/`，但用户通常 fork 在 `~/astrbot_plugin_<name>/` 维护。两份必须保持同步——改一份忘了另一份 = 调试时怀疑人生。规则：fork 目录是真理源（push/PR 都在这里），改完先 diff 同步到 `data/plugins/`，再 restart。`diff -q <fork>/file <data_plugins>/file` 验证同步。
- **`ruff format` 必须跑全项目，不只改动的文件** — fork 项目（如 `astrbot-plugin-bangumi`）的 CI 跑 `ruff format --check .` 和 `ruff check .`，作用在整个项目。本地只 `ruff format main.py src/app/subscription_service.py` 可能漏过其它文件的格式问题——CI 会以"Would reformat: <file>"失败。同理 `ruff check .`。永远跑完整项目。
- **`git commit --amend` 前必须保证 working tree 干净** — 修改文件后 amend 只把 staged 改动折进 commit。如果 amend 后又跑了 `ruff format` 修改 working tree 但没 add+amend，commit 内容与 working tree 漂移。force-push 之后 CI 跑 commit 里的代码，声称"需 reformat"（因为 working tree 的 reformat 没进 commit）。修复: amend 前 `git status --short`；或先 `git add -u && git commit --amend`；或 amend 后 `git status` 确认无 M。
- **PR title/body 更新用 `gh pr edit --title --body`** — `gh pr create` 对已存在的 PR 会报"already exists"。要改标题/正文用 `gh pr edit <num> --title "..." --body "..."`。PR head SHA 变更（force push 后）由 GitHub 自动同步到 PR——`gh pr view <num> --json headRefOid --jq .headRefOid` 验证同步完成。

- **CI 测试已存在行为改变 → 改测试不是改产品代码** — PR #18 写了 `test_broadcast_time_crud_and_batch_update`，该测试假设 `set_subject_broadcast_time` 设值后 `batch_update` 能覆盖（updated=2）。给产品加 manual_lock 之后这个测试**直接过期**——product behavior 变了，老契约失效。修法：先确认新行为对（用 tempdir sqlite 跑 4 状态 round-trip），再改测试保留它的契约意图（"batch_update 把非锁定记录批量覆盖"）。老测试改 = 一行 `set_subject_broadcast_time("100", None)` 解锁；新行为加进 `test_manual_lock_blocks_batch_update_and_clears_on_reset`。原则：**老测试失败先怀疑契约是否过期**，别动产品代码去迎合死测试。

- **扩展命令参数 ponytail：解析多格式在同字段内而非加新 arg** — `@command("X")` 装饰器的参数列表在 class body 里是 literal，加第三个参数意味着新装饰器（违反 `@command` 类加载扫描约束）。ponytail 解决：复用现有 `time` 字段解析"周X HH:MM"或"X HH:MM"前缀。一段正则剥掉可选 weekday，剩下的就是 HH:MM，校验一次正则。命令签名不变，下游 setter 拿 `(time_str, weekday_optional)` 即可。`/放送时间 <番> 周三 22:00` / `/放送时间 <番> 5 22:00` / `/放送时间 <番> 22:00` 三种都吃。**不要**为"加一个可选参数"新开装饰器或新命令——用户通常不在乎 UX 微调，能用一个命令吸收就吸收。

- **AstrBot `@filter.command` 用空格切 token、按位置分配给函数签名——第 3 token 被无声丢弃** — 命令处理路径（`astrbot/core/star/filter/command.py:209`）：```python
message_str = re.sub(r"\s+", " ", event.get_message_str().strip())   # 规范化空白
ls = message_str.split(" ")                                            # 按空格切
ls = [param for param in ls if param]                                  # 去空字符串
params = self.validate_and_convert_params(ls, self.handler_params)     # 按位置分配
```