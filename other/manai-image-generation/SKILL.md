---
name: manai_image_generation
description: 基于 Manai 私有助理平台的自动生图能力，可根据商品信息和参考图片一键批量生成白底图、主视觉、卖点图、细节图等全套电商展示图，也支持自定义
  Prompt 生成任意风格的图片。
title: ManAI商品图生成
example: 为这双云感拖鞋的实物图生成一套拼多多风格的电商宣传图，突出轻盈回弹、防滑耐磨的特点。
version: 1.0.2
---
# E-commerce Product Image Generation SKILL

**Manai** is a private assistant platform (私有助理平台) equipped with powerful capabilities, including **Automatic Image Generation (自动生图)** and **Automatic Product Listing (自动上架)**.

To use the Manai platform through an AI agent, the user must complete the following prerequisites:
1. **Register (注册)**: Register an account on the Manai platform.
2. **Recharge (充值)**: Recharge their account balance (energy/points) to cover generation and operation costs (accessible at `https://manai.cc/recharge`).
3. **Set API Key (设定apikey)**: Generate and configure an API key on the platform (accessible at `https://manai.cc/settings/apikeys`. For local development only, `http://localhost:3012/settings/apikeys` can be used).

## 1. Connection Details
- **Endpoint Type**: Streamable HTTP (Single Endpoint POST)
- **Base URL**: 所有接口默认都必须走 `https://manai.cc/mcp` (Remote / Default)。
- **默认服务地址与本地开发机说明 (Default Server & Local Dev Service)**:
  - 默认情况下，本技能及相关平台访问统一指向远程云端服务 **`https://manai.cc`**。
  - 只有在特别说明的本地开发机（Local Dev Machine）上，才存在本地调试服务，其端口分工如下：
    - **MCP Port**: `5688` (仅用于本地开发机 MCP 协议接口通信).
    - **Backend Service & Static Assets Port**: `5678` (用于访问本地测试后台、查看网页、以及静态图片文件下载渲染，如 `/static/images/...`).
    - **Formatting Image URLs**: 本地开发机测试时，向用户格式化或渲染 Markdown 图片地址时，必须使用本地后台服务端口 `5678`（例如：`http://127.0.0.1:5678/static/images/...`），绝对不能使用 MCP 服务的 5688 端口！
  - 在常规或没有特别说明的部署环境下，严禁默认尝试建立 5678 或 5688 端口的本地连接，必须始终使用云端平台地址。
- **Authentication**: Requires `X-API-Key` in headers. If you receive a 401 error, tell the user: "Please go to https://manai.cc/settings/apikeys to generate an API Key and provide it to me."

> **CRITICAL INSTRUCTION FOR HERMES**: 
> Your built-in MCP client might fail to connect due to incompatibility with the modern "Streamable HTTP" protocol (you might see "SSE connection timeout" or "Invalid session ID").
> **If your built-in client fails, DO NOT GIVE UP.** You MUST bypass your internal MCP tool and execute the provided Python wrapper script `${HERMES_SKILL_DIR}/scripts/manai_mcp_client.py` located in the skill directory.
> 
> **How to call MCP tools via Python wrapper:**
> The script will automatically attempt to load the API Key (`image_key`) from `conf/global_config.json` inside the user workspace. You do not need to pass `--api-key` unless you want to override it.
> 
> If the script returns an error saying "ApiKeyNotFound", you MUST ask the user to provide their API Key (e.g., "画图技能需要 API Key。请在 manai 平台 (https://manai.cc/settings/apikeys) 获取或创建 API Key 并提供给我。").
> Once the user provides the API Key (usually starting with `sk-`), you must:
> 1. Pass the provided key directly to the Python client via the `--api-key` parameter (e.g., `python manai_mcp_client.py --api-key sk-xxxx ...`).
> 2. Suggest to the user to sync/save it via the GUI client settings.

> 
> **Standard execution command:**
> ```bash
> python ${HERMES_SKILL_DIR}/scripts/manai_mcp_client.py <tool_name> '<json_arguments>'
> ```
> 
> **Example calling `query_ecommerce_generation_status`:**
> ```bash
> python ${HERMES_SKILL_DIR}/scripts/manai_mcp_client.py query_ecommerce_generation_status '{"project_id": 123}'
> ```
> *(Alternatively, you can pass parameters explicitly: `python ${HERMES_SKILL_DIR}/scripts/manai_mcp_client.py --api-key sk-xxxx query_ecommerce_generation_status '{"project_id": 123}'`)*
> 
> The script will automatically handle the JSON-RPC `initialize` handshake, capture the `Mcp-Session-Id`, execute your tool, and print the raw JSON output for you to parse.

## 2. Core Workflow (Critical)

### Step 0: 接口选择与决策 (Tool & Interface Selection)
当需要调用图片技能或在物料整理中需要生成/补充图片时，请严格按以下规则进行 MCP 工具的调用决策：
1. **生成商品主图与商品详情页图（批量套图生成）**：
   - **适用工具**：`generate_ecommerce_images_direct` 接口（详见 Step 2）。
   - **说明**：此接口适用于批量套图生成，它会根据所选预设模块（如 `white_bg` 白底图、`hero` 主视觉图、`detail` 细节图、`selling` 卖点图等）自动套用电商排版和视觉规范。
2. **生成定制 AI 模特形象**：
   - **适用工具**：`generate_ecommerce_model` 接口（详见 Tool Parameters Guide）。
   - **说明**：适用于需要定制特定性别、年龄、体型、肤色/地区及细节特征的 AI 模特形象。生成完毕后可以使用 `list_custom_models` 接口查询模特列表以获取模特原图 URL。
3. **获取自有模特列表**：
   - **适用工具**：`list_custom_models` 接口（详见 Tool Parameters Guide）。
   - **说明**：查询名下所有已创建或上传的 AI 模特信息及图片路径（`original_url`），常在随后的服饰穿戴生图任务中用于选择模特图片输入。
4. **服饰穿戴渲染（AI 模特换装与场景图生成）**：
   - **适用工具**：`generate_clothing_try_on` 接口（详见 Tool Parameters Guide）。
   - **说明**：当需要将商品服饰合成至特定 AI 模特身上，并生成不同拍摄场景（如街头、棚拍、户外等）的模特上身展示图时使用。
5. **爆款复刻（模仿竞品或热榜视觉图）**：
   - **适用工具**：`generate_viral_replica` 接口（详见 Tool Parameters Guide）。
   - **说明**：当需要根据爆款图参考（模仿其构图、画面排版、文字摆放和氛围），融入自家商品图并制作出同款优质视觉排版图时使用。
6. **非上述特定场景的其他定制/通用生图需求（如纯自定义 Prompt 创意图）**：
   - **适用工具**：`generate_base_image` 接口（自定义 prompt 生图，详见 Tool Parameters Guide 中该工具的说明）。
   - **说明**：对于不属于以上特定电商场景的其他单张图/创意图生成需求，使用此底层通用生图接口。您只需协助用户将需求翻译/扩写为精细化的 Prompt 提示词并调用此接口。

### Step 1: Gather Inputs & Recommend Modules
When a user wants to generate product images, proactively ask for:
1. **Product Name** (必填 / Required)
2. **Product Selling Point** (必填 / Required) - Key benefits or creative ideas.
3. **Product Image Data** (必填 / Required) - Reference images. (Can be a public URL or a Base64 data string starting with `data:image/`).
4. **Target Image Types** (必选 / Required) - Let the user select which image types they want. You MUST present the list of available modules below and let them choose. Suggest a default combination (e.g., `["white_bg", "hero", "detail", "usage_scene"]`) if they are unsure.

### Step 2: Direct Generation (`generate_ecommerce_images_direct`)
Submit the request once the inputs are confirmed.

> **⚠️ CRITICAL CONFIRMATION RULE**:
> Before executing the tool call to the server, you MUST display the complete list of parameters you intend to submit to the user.
> 
> **Formatting and Language Rules for Confirmation**:
> 1. **User-Language Alignment**: Translate and display all parameter names in the user's natural language (e.g., if the user communicates in Chinese, use Chinese parameter names such as "商品名称 (product_name)", "创意描述 (prompt)", etc.) to make it easy for them to understand.
> 2. **Explicit Defaults for `module_configs`**: When `module_configs` is not set, explicitly display its value showing the default configuration for each selected module type (e.g., for `white_bg`, the default is "白底/1K/1:1"; for `hero`, the default is "2K/3:4"). 
> 
> **Example parameter confirmation table (for Chinese users)**:
> 
> | 参数 | 值 |
> | :--- | :--- |
> | **商品名称 (product_name)** | `EVA 云感拖鞋` |
> | **创意描述 (prompt)** | EVA 云感拖鞋，自然微砖纹理鞋底，减少发力损耗，轻盈回弹不塌陷。柔软贴合脚型，每一步如踩云端。防滑耐磨，居家户外两相宜。 |
> | **参考图片 (reference_images)** | 你发的拖鞋实物图（Base64，310KB） |
> | **生成模块 (modules)** | `["white_bg", "hero"]` — 白底图 + 首屏主视觉 |
> | **分发平台 (platforms)** | `["pdd"]`（默认） |
> | **图片语种 (language)** | `zh`（中文，默认） |
> | **是否允许文字 (allow_image_text)** | `true`（默认） |
> | **项目名称 (name)** | 不设（自动生成） |
> | **模块参数配置 (module_configs)** | 不设（将按图片类型应用默认配置：白底图默认为白底/1K/1:1，首屏主视觉默认为1K/3:4） |
> 
> You MUST ask the user to explicitly confirm these parameters (e.g., "Please confirm if you want to proceed with these settings: ...") and wait for their approval before invoking `generate_ecommerce_images_direct`.

- **Action**: Call `generate_ecommerce_images_direct` to submit the task.
- **Reporting**: Display the **Project ID** and project name to the user. Clearly explain that the tasks are running in the background and show the user you will now monitor the progress. Provide a link for the user to view the project directly in the web workspace: `https://manai.cc/ecommerce/create?projectId=<project_id>` (replace `<project_id>` with the actual ID).

### Step 3: Monitor Progress (`query_ecommerce_generation_status`)
- **Action**: 
  1. **Concurrency Control (并发控制)**: When generating multiple custom images or submitting multiple separate image generation tasks, you MUST run them with a concurrency of 5 (5 concurrent requests) to process them in parallel.
  2. **Query Interval (查询间隔)**: Check the status using `query_ecommerce_generation_status` once every minute (每分钟查询状态).
  3. **Timeout (超时控制)**: Wait for at most 12 minutes in total per task (最多等待12分钟/最多查询12次). If a task exceeds 12 minutes, consider the task failed (如果超过12分钟，则认为任务失败).
- **Reporting**: Display a progress report to the user:
  - List each module with its status (e.g., "White Background Image: Completed").
  - If completed, render the generated image directly using markdown format `![description](image_url)` so the user can see it in their chat.
  - If failed, report the error reason clearly.

### Step 4: Batch Export & Download (`download_ecommerce_images_zip`)
- **Action**: Once the generation tasks are completed, or when the user requests to download all generated images, call `download_ecommerce_images_zip` to get an authenticated ZIP download URL.
- **Reporting**: Provide the download URL to the user, and give tailored download instructions based on whether they are using a chat/IM client or a command-line terminal.

---

## 3. Reference: Complete Product Image Types (Modules)
When asking the user to choose or when calling the tool, use the exact **Module ID** strings below:

| Module ID | Chinese Name (图片类型) |
| :--- | :--- |
| `white_bg` | 白底图 |
| `hero` | 首屏主视觉 |
| `selling` | 核心卖点图 |
| `usage_scene` | 使用场景图 |
| `multi_angle` | 多角度图 |
| `atmosphere` | 场景氛围图 |
| `detail` | 商品细节图 |
| `brand_story` | 品牌故事图 |
| `dimension` | 尺寸/容量/尺码图 |
| `comparison` | 效果对比图 |
| `spec_table` | 详细规格/参数表 |
| `process` | 工艺制作图 |
| `accessories` | 配件/赠品图 |
| `series` | 系列展示图 |
| `composition` | 商品成分图 |
| `warranty` | 售后保障图 |
| `usage_tips` | 使用建议图 |

---

## 4. Tool Parameters Guide

### `generate_ecommerce_images_direct`
- `product_name` (string, required): Specific name (e.g., "Vintage Leather Messenger Bag").
- `prompt` (string, required): Creative prompt/selling points (e.g., "Minimalist modern style, highlight scratch-resistant fabric and spacious compartments").
- `reference_images` (array of strings, required): List of product reference images (supports Base64 data URI starting with `data:image/` or public URLs).
- `modules` (array of strings, required): List of chosen Module IDs (e.g. `["white_bg", "hero", "detail"]`).
- `platforms` (array of strings, optional): Target platforms (e.g., `["pdd"]` or `["taobao"]`). Defaults to `["pdd"]`.
- `name` (string, optional): Project name custom string.
- `language` (string, optional): Target language for texts generated on images (e.g., `"zh"`, `"en"`, `"ja"`, `"ko"`, `"ru"`, `"es"`, `"de"`, `"pt"`, `"id"`, `"th"`). Defaults to `"zh"`.
- `allow_image_text` (boolean, optional): Whether text elements are allowed in generated images. Defaults to `true`.
- `module_configs` (array of objects, optional): Specific configurations for individual modules. Each config object contains:
  - `module_id` (string, required): Target module ID (must be one of the Module IDs listed below, e.g., `"white_bg"`, `"hero"`, or `"others"` as a fallback configuration).
  - `size` (string, optional): Target resolution, choice of `"1k"`, `"2k"`.
  - `ratio` (string, optional): Aspect ratio (e.g., `"1:1"`, `"3:4"`, `"9:16"`, `"16:9"`).
  - `allow_image_text` (boolean, optional): Whether text elements are allowed for this module.
  *Example*:
  ```json
  [
    {"module_id": "white_bg", "size": "1k", "ratio": "1:1", "allow_image_text": false},
    {"module_id": "hero", "size": "2k", "ratio": "3:4", "allow_image_text": true}
  ]
  ```

### `generate_base_image`
此工具用于根据用户自定义需求生成或编辑任意图片。任何不属于上述固定电商套图分类的生图需求（例如非电商配图、特定的款式图、Logo、海报背景等）都应调用此接口。它支持纯自定义的 Prompt 生成或基于参考图的图像编辑，可灵活用于生成任一用户需要的图片。
- `prompt` (string, required): 图像生成或编辑的 Prompt。
- `images` (array of strings, optional): List of input/reference images (supports Base64 data URI starting with `data:image/` or public URLs, up to 3).
- `size` (string, optional): Target size (e.g. "1024x1024").
- `name` (string, optional): Custom project name.
- `model` (string, optional): Target model (defaults to "gpt-image-2").
- `quality` (string, optional): Target quality (defaults to "high").

> **⚠️ AGENT GUIDE: HOW TO USE THIS TOOL PROFESSIONALLY**
> DO NOT simply pass the user's raw, short description directly into the `prompt` parameter. To ensure the generated image looks professional and premium:
> 1. **Understand Needs**: Communicate with the user to clarify key elements: subject, style (e.g. commercial photography, studio render, cinematic), lighting (e.g. soft diffused light, split lighting, dramatic shadow), composition, and color palette.
> 2. **Draft a Professional Prompt**: Expand the user's request into a detailed, descriptive prompt. Include terms describing materials, texture detail, environment, camera settings (e.g., "shot on 85mm lens, f/1.8"), and lighting. Translate to professional English since the underlying image engine works best with English prompts.
> 3. **Call the Tool**: Pass this refined, detailed prompt to the `generate_base_image` tool to yield high-quality visual results.

### `generate_ecommerce_model`
此工具用于生成自有电商基准模特形象（AI模特）。
- `gender` (string, required): 模特性别，可选值: `"female"` (女), `"male"` (男)。
- `age` (string, required): 年龄段，可选值: `"young"` (青年), `"child"` (儿童), `"middle"` (中年), `"senior"` (老年)。
- `region` (string, required): 地区/肤色，可选值: `"asian"` (亚洲人), `"caucasian"` (欧美白人), `"black"` (黑人), `"latino"` (拉美裔)。
- `build` (string, required): 体型，可选值: `"standard"` (标准), `"slim"` (偏瘦), `"plussize"` (微胖)。
- `details` (string, optional): 外貌细节描述（如“小麦色皮肤、齐刘海、眼角有泪痣”）。
- `reference_image` (string, optional): 参考风格图（支持 Base64、本地路径或图片 URL）。

### `list_custom_models`
获取用户自有的全部AI模特与上传模特的列表，不需任何参数。返回各个模特的 ID、头像/原图 URL 和当前生成状态（如 `completed`, `pending`, `processing` 等）。

### `generate_clothing_try_on`
服饰穿戴渲染（换装与场景图生成）。
- `product_images` (array of strings, required): 商品服饰参考图数组（最多 3 张，支持 Base64 或图片 URL）。
- `model_ref_image` (string, required): 模特图路径或 URL。可以使用 `list_custom_models` 中获取到的 `original_url` 或使用预设模特路径（如 `/static/model/model_01.jpg`）。
- `ratio` (string, optional): 图片比例（默认 `"3:4"`，可选 `"1:1"`, `"3:4"`, `"9:16"`, `"16:9"`）。
- `language` (string, optional): 文本语言（默认 `"none"` 无文字。可选 `"none"`, `"zh"`, `"en"` 等）。
- `platform` (string, optional): 目标电商平台（默认 `"1688"`）。
- `ai_recommend` (boolean, optional): 是否由 AI 自动分析并推荐最和谐的场景背景（默认 `false`）。
- `try_on_scene` (string, optional): 手动选择的拍摄场景（仅在 `ai_recommend=false` 生效，默认 `"pure_studio"`。可选 `"pure_studio"` 棚拍, `"urban_street"` 街头, `"street_cafe"` 咖啡馆, `"natural_lawn"` 草坪, `"resort_beach"` 沙滩, `"warm_home"` 温馨居家, `"art_gallery"` 展馆）。
- `try_on_custom_scene` (string, optional): 自定义描述的拍摄场景。
- `model` (string, optional): 渲染生图模型（默认 `"gpt-image-2"`）。
- `name` (string, optional): 自定义项目名称。

### `generate_viral_replica`
爆款复刻渲染，模仿爆款原图的排版、画风与构图。
- `competitor_images` (array of strings, required): 爆款参考原图数组（最多 10 张，支持 Base64 或图片 URL）。
- `product_images` (array of strings, optional): 自己的商品原图数组（最多 3 张）。
- `prompt` (string, optional): 统一的画面复刻细节或卖点说明。
- `single_requirements` (array of strings, optional): 分别针对每一张 competitor_images 的个性化文案或细节修改要求（长度应与 competitor_images 一致）。
- `degree` (string, optional): 复刻程度（默认 `"high"`。可选 `"high"` 高度复刻, `"style"` 参考风格）。
- `scene` (string, optional): 发布平台与复刻场景（默认 `"social_media"`。可选 `"social_media"` 社媒/小红书, `"ecommerce_product"` 电商商品图, `"marketing_poster"` 营销海报）。
- `ratio` (string, optional): 图片比例（默认 `"3:4"`）。
- `language` (string, optional): 图片文本语种限制（默认 `"none"`）。
- `model` (string, optional): 生图模型（默认 `"gpt-image-2"`）。
- `name` (string, optional): 自定义项目名称。

### `query_ecommerce_generation_status`
- `project_id` (number, required): The project ID (integer) returned by the generation tool.

### `download_ecommerce_images_zip`
- `project_id` (number, required): The project ID (integer) to pack and export.

## 5. Expert Interaction Principles
1. **Always Embed Images**: When a task is completed, you MUST render the generated image directly using markdown `![module_name](image_url)` so the user doesn't need to click any links.
2. **Be Structured**: Always list modules and status updates in a neat list or table.
3. **Shared Context**: Remind the user that Hermes and the Manai Web Dashboard share the same account. Any images generated here will appear in their history immediately, and they can view the detailed results or edit the project on the web workspace via: `https://manai.cc/ecommerce/create?projectId=<project_id>` (where `<project_id>` is their project ID).
4. **Concurrency & Timeout (并发与超时控制)**:
   - **Parallel Requests (并发请求)**: When submitting separate image generation tasks (e.g., calling `generate_base_image` or `generate_ecommerce_images_direct` for different product options, colors, or styles), you MUST execute up to 5 tasks in parallel (5 concurrent requests) to minimize the overall execution time.
   - **Query Interval (查询间隔)**: Check the status once every minute (每分钟查询状态).
   - **Task Timeout (任务超时)**: The maximum allowed duration for each task is 12 minutes. If a task exceeds 12 minutes, consider it failed (如果超过12分钟，则认为任务失败).

## 6. How to Guide Users on Downloading
When you provide the download link generated by `download_ecommerce_images_zip`, always present it with clear download instructions matching the user's interface type:

- **For IM/Chat Clients (Feishu, DingTalk, Enterprise WeChat, etc.)**:
  Provide a clear clickable link like: `[点击下载项目图片 (ZIP 格式)](<DOWNLOAD_URL>)`.
- **For Terminal/CLI Environments (Command Line Interactivity)**:
  Provide a copyable `curl` or `wget` command using the exact download URL returned by the tool.
  ```bash
  curl -O "<DOWNLOAD_URL>"
  # OR
  wget "<DOWNLOAD_URL>"
  ```
  The URL provided by the tool is a clean static URL, so it can be downloaded directly without any authentication headers or tokens.
- **For Automatic Local Saving (If downloading/saving files locally)**:
  If the user asks you to save the generated images locally (or if you automatically download them), the default destination must be the global configuration `data_directory` (resolved from `conf/global_config.json`, which defaults to `./storage/` relative to the workspace root) unless the user explicitly specifies a different destination path.
