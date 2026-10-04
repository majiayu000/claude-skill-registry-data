---
name: xiaohongshu_publisher
description: 自动分析商品图并编写小红书风格的标题与正文（含10个高热话题并过滤违禁敏感词），配合AI生图工具生成多场景推广图，提供双重确认机制后一键自动发布到小红书平台。
title: 小红书自动发帖
example: 使用我上传的香水实物图，生成5个不同场景的宣传图并写一篇小红书种草文案，确认后自动发布到我的创作者端。
version: 1.0.0
---
# 小红书自动发帖技能指引 (Xiaohongshu Automated Posting Skill)

本 SKILL 引导 Agent 扮演**小红书平台运营与自动化发布专家**。当用户上传一张商品实物图并要求在小红书发帖时，Agent 将执行：自动场景生图（5张）、写种草文案与标题（含10个相关话题，过滤违禁词）、向用户发起双重确认、并在用户授权后利用浏览器守护进程自动填充并一键发布。

> [!IMPORTANT]
> **运行模型建议**：本技能涉及复杂的图片多模态分析与爆款文案生成，**强烈建议用户配置并使用具备强读图（Vision）能力的 `gpt-5.4` 模型**。如果当前运行的模型不支持读图，请引导或提醒用户切换至支持读图的 `gpt-5.4` 模型，以保证商品图像特征的准确提取。

---

## 1. 核心流程与双重确认机制 (Workflow & Dual Gates)

为了确保生图质量和账号安全，Agent 执行本任务时必须严格执行以下五个阶段的交互：

```
[阶段 1: 需求对齐]  --> [阶段 2: 场景与 Prompt 确认] (阻塞点 1)
                           ↓
[阶段 4: 文案与图片展示] <-- [阶段 3: 并行生成 5 张图片]
      ↓
[阶段 5: 浏览器上传与填充] --> [确认发布指令] (阻塞点 2) --> 一键发布成功
```

---

## 2. 阶段详解与执行指南

### 阶段 1：接收商品图与需求对齐
1. **输入源**：用户必须上传至少一张商品图。
2. **生图 Prompt 偏好**：
   - 默认提示词：`提取图中的商品，选一个模特，在5个场景生成图片`。
   - 主动询问用户是否有定制提示词或对场景/模特特征的特殊偏好。若用户无特殊偏好，按默认执行。
3. **参数与内容动态调整**：生图张数、图片 Prompt 提示词、试穿场景以及小红书标题和文案内容，**都应当并且完全可以根据用户的个性化需求动态调整**（例如用户要求只生成 3 张图、指定特定职场背景等）。Agent 绝不可死板套用默认规则，应以用户的最终要求为准。
4. **动态脚本生成与运行**：为了满足用户变化多端的要求，Agent 在后续执行图片生成与下载时，**应根据当前上下文动态编写并运行新的 Python 脚本**（利用 `execute_code` 工具），在脚本中动态组装 payload 参数、发送请求、轮询状态并下载保存图片，使执行流程具备高度灵活性。

### 阶段 2：展示方案等待确认 (阻塞点 1 - 必须阻塞)
在调用后台生图工具前，Agent 必须将准备提交给生图引擎的参数以表格形式呈现给用户确认，**必须翻译为中文展示**：

| 参数 | 值 / 方案 |
| :--- | :--- |
| **商品参考图** | 用户上传的实物图 |
| **模特选择 (Model)** | 自动选定（或用户指定）的 AI 模特（默认：/static/model/model_01.jpg 亚洲女性） |
| **生成的 5 个推广场景** | 1. 温馨居家 (warm_home)<br>2. 街头都市 (urban_street)<br>3. 咖啡馆外 (street_cafe)<br>4. 阳光草坪 (natural_lawn)<br>5. 度假沙滩 (resort_beach) |
| **生图模型 (Model)** | `gpt-image-2` |
| **生图比例 (Ratio)** | `3:4` (小红书竖图最佳比例) |

> **⚠️ 话术提示**：
> “我已经为您规划了生图方案（5个经典推广场景，模特默认为亚洲女性，比例为 3:4）。请确认是否开始生成？如果有任何修改意见（例如想换男模特或特定的背景），请告诉我！”
> **必须得到用户“确认”或“开始生成”等答复后，方可执行下一步。**

### 阶段 3：图片生成与监控
1. 确认后，Agent 必须通过调用 **`manai_image_generation`** 技能的 **`generate_clothing_try_on`** 接口（或通用生图接口）为这 5 个场景分别生成图片。
2. **⚠️ 绝对禁止使用 `subprocess` 或命令行调用 `manai_mcp_client.py` 脚本，避免 Windows 下频繁弹出 cmd.exe 命令行窗口。** 调用云端 MCP Streamable HTTP 接口时优先使用平台已内置的客户端；如需写临时脚本，应使用 Python 标准库 HTTP 客户端或确认运行环境已有对应依赖。
   ```python
   import os
   import json
   import urllib.request

   url = os.environ.get("MANAI_URL", "https://manai.cc/mcp")
   api_key = os.environ.get("MANAI_API_KEY")
   headers = {"Content-Type": "application/json", "X-API-Key": api_key}
   def post_json(payload, timeout):
       data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
       req = urllib.request.Request(url, data=data, headers=headers, method="POST")
       with urllib.request.urlopen(req, timeout=timeout) as resp:
           return resp, json.loads(resp.read().decode("utf-8"))

   # 1. 建立会话并获取 Mcp-Session-Id
   init_resp, _ = post_json({
       "jsonrpc": "2.0", "id": 1, "method": "initialize",
       "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "mcp-client", "version": "1.0.0"}}
   }, timeout=10)
   session_id = init_resp.headers.get("Mcp-Session-Id")
   headers["Mcp-Session-Id"] = session_id

   # 2. 调用工具（如 generate_clothing_try_on）
   _, result = post_json({
       "jsonrpc": "2.0", "id": 2, "method": "tools/call",
       "params": {"name": "generate_clothing_try_on", "arguments": payload}
   }, timeout=120)
   ```
3. **查询与下载图片状态的处理逻辑**：
   - 轮询生图状态接口（如 `query_ecommerce_generation_status`），解析返回的 JSON 结果。
   - **⚠️ 注意图片相对路径处理**：状态接口返回的图片地址可能是类似于 `/static/...` 格式的相对路径。在提取下载链接时，绝对不能只匹配 `https://`。如果返回地址是相对路径，必须在前面拼接完整 host 前缀（如 `https://manai.cc`，或者使用请求状态接口时的 Base URL 域名部分，组合成 `https://manai.cc/static/...` 的完整 URL）。
   - 下载完整 URL 的图片并保存到项目本地临时目录：`./temp/<YYYYMMDD>/xhs_post_{当前时间}/` 下（命名为 `img_1.jpg` 到 `img_5.jpg`）。

### 阶段 4：文案撰写与违禁词过滤
基于用户提供的商品图及生图场景，Agent 必须同时为用户撰写一份**符合小红书爆款风格的图文草案**。

#### 1. 文案风格规范
- **标题**：20字以内，极具吸引力，必须使用表情符号（如 😲, ✨, 😭, 💥），突出核心痛点或亮点。
- **正文**：100–500字，第一人称口吻，真诚分享、种草调性。多用空行和点缀性表情。分段列出使用体验（如“外观、质感、适用场景”）。
- **话题标签**：自动在文末追加 **10个** 与该商品高度相关、高热度的标签，格式为 `#话题名`，以空格分隔。

#### 2. 小红书违禁敏感词过滤规则 (必修过滤)
文案生成后，Agent 必须对标题、正文及标签进行自检与净化，**绝对禁止**出现以下敏感词，并按以下规则替换：
- **绝对化用词**：`最`, `第一`, `顶级`, `100%`, `绝对`, `极品`, `完美`, `首选` → 替换为：`很`, `极佳`, `非常`, `推荐` 等温和词。
- **跨平台引流**：`淘宝`, `拼多多`, `微信`, `加我`, `私信`, `微店`, `下单`, `链接` → 替换为：`官方平台`, `主页`, `评论区` 等中性表述或直接删除。
- **虚假疗效/功能（非医疗品）**：`治疗`, `根治`, `特效`, `药到病除`, `杀菌`, `排毒`, `瞬间瘦` → 替换为：`舒缓`, `改善`, `温和清洁`, `辅助`。

自检合格后，Agent 将 5 张图片的 Markdown 渲染链接及文案（标题、正文与 10 个话题）完整展示给用户。

---

## 3. 阶段 5：浏览器上传、填充与最终发布 (阻塞点 2 - 必须阻塞)

当用户在聊天框中回复“确认发布”或“开始发布”后，Agent 启动浏览器自动化流程。

### BrowserWorker 执行约束

- 发布页上传、填充、预览和最终点击发布必须通过项目内置 `BrowserWorker` daemon + Chrome extension transport 完成，不要求用户机器安装 ChromeDriver、Playwright、Selenium、Node.js、npm 或 Python 第三方包。
- 浏览器 HTTP 调用示例必须使用 Python 标准库（如 `urllib`），不要把 `requests` 作为浏览器控制依赖。
- 端口发现顺序：`BrowserWorker_PORT` -> `BrowserWorker_LOCK_FILE` -> `MANAI_WORKSPACE_ROOT` / `MANAI_HOME` 下的 `storage/browser_daemon.lock` -> 默认 `12321`。
- 临时图片、临时 payload 和调试输出必须放在项目 `./temp/<YYYYMMDD>/` 下；任务完成后只清理本次创建的临时文件，不删除非 `./temp` 下文件。
- 遇到小红书登录、验证码、账号安全验证、上传失败或发布确认弹窗时，调用 `request_help(validate_after=True)`，让用户在 BrowserWorker 插件浏览器中处理。

### 第一步：通过 Python 脚本调用 `publish_to_xhs` 动作
由于 `publish_to_xhs` 动作没有直接以 LLM 工具的形式暴露在 Agent 的工具列表中，**Agent 必须编写一段 Python 脚本（利用 `execute_code` 或 `terminal` 运行）来向本地运行的浏览器守护进程发送 HTTP 请求发起调用**。

具体 Python 运行脚本的写法样例如下：
```python
import os
import json
import uuid
import urllib.request
from pathlib import Path

# 1. 动态获取本地浏览器守护进程的运行端口
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

def post_json(base_url: str, path: str, payload: dict, timeout: float = 120.0) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        base_url + path,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))

port = get_browser_daemon_port()
base_url = f"http://127.0.0.1:{port}"

# 2. 定位 publish_to_xhs.py 的 action_search_path
current_dir = Path(__file__).resolve().parent
action_search_path = None
for root in [current_dir, *current_dir.parents]:
    for candidate in (
        root / "scripts" / "actions" / "publish_to_xhs.py",
        root / "skills" / "xiaohongshu_publisher" / "scripts" / "actions" / "publish_to_xhs.py",
        root / "storage" / "agents" / "organizer-1" / "skills" / "xiaohongshu_publisher" / "scripts" / "actions" / "publish_to_xhs.py",
    ):
        if candidate.exists():
            action_search_path = candidate.parent
            break
    if action_search_path:
        break

if not action_search_path:
    raise FileNotFoundError(f"找不到 publish_to_xhs.py 动作脚本，请确认路径。")

session_id = f"xhs_publish_{uuid.uuid4().hex[:8]}"

# 3. 构造本地 `/execute` 接口的调用参数并发起请求
payload = {
    "session_id": session_id,
    "action": "publish_to_xhs",
    "action_search_path": str(action_search_path),
    "args": {
        "image_paths": [
            "./temp/20260729/xhs_post/img_1.jpg",
            "./temp/20260729/xhs_post/img_2.jpg",
            # 填入实际生成的本地推广图路径
        ],
        "title": "小红书标题",
        "content": "小红书正文内容 + 10个话题标签"
    }
}

# 4. 执行请求并捕获输出
post_json(base_url, "/lock/acquire", {
    "session_id": session_id,
    "skill": "xiaohongshu_publisher",
    "domains": ["xiaohongshu.com"],
    "concurrency_policy": "domain",
}, timeout=10)
try:
    result = post_json(base_url, "/execute", payload, timeout=180)
    print(json.dumps(result, ensure_ascii=False, indent=2))
finally:
    post_json(base_url, "/lock/release", {"session_id": session_id}, timeout=10)
```

### 第二步：双重确认提示与发布控制
1. `publish_to_xhs.py` 会自动在 BrowserWorker 插件浏览器中创建或复用发布标签页，并导航到小红书发布页面，上传图片，填入标题和正文。
2. **填充完毕后，脚本与 Agent 必须暂停，不能自动点击“发布”按钮**。
3. Agent 向用户反馈当前状态，并要求用户进行最终人工审查：
   > **📢 交互话术**：
   > “我已经在插件浏览器中将 5 张生成的图片、标题和正文都上传并填好。请在已打开的小红书发布页面中检查排版和内容：
   > - 如果确认无误，请在聊天框回复【确认发布】，我将自动为您一键点击发布；
   > - 您也可以在浏览器页面中手动点击右下角的【发布】按钮。”
4. **人工放行**：只有当用户在聊天框输入“确认发布”、“发吧”等明确的二次指令后，Agent 才能再次调用 `publish_to_xhs` 传入 `{"click_publish": true}` 动作，或执行 JS 点击发布按钮，完成任务。
5. **⚠️ 填充后保留页面标签页（Tab）**：在内容填充完毕、用户最终确认发布或手动发布的整个等待期间，**严禁主动关闭小红书创作者页面标签页（Tab）**。必须保持页面开启，直到用户确认完成任务。

---

## 4. 完成标准 (Completion Criteria)
- 展示生图和文案方案并通过“阻塞点 1”。
- 并行生成 5 张高品质场景图片并完成违禁词过滤。
- 自动接管浏览器并成功填充图片、标题和正文描述。
- 经过“阻塞点 2”人工二次确认后，自动执行点击发布或确认用户已手动发布。
- 彻底清理本地 `temp/` 目录下的所有临时图片和脚本。
