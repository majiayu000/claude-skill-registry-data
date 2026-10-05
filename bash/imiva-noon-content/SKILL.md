---
name: imiva-noon-content
slug: imiva-noon-content
version: 1.0.0
displayName: "Noon 中东电商内容"
summary: "Noon 中东电商内容；使用极睿科技 IMIVA MCP 完成电商内容生产与交付"
homepage: https://imiva.ecpro.com/
tags:
  - IMIVA
  - 极睿科技
  - AI电商
  - 电商
  - AIGC
  - 海外渠道
  - 电商图片
description: "Noon 中东电商内容。帮助品牌商家、电商运营、设计与内容团队通过 IMIVA MCP 为 Noon 生成符合商品展示、广告与本地化需求的图片视频内容。适用于Noon、中东电商、阿语商品图、跨境电商、Listing等搜索与生产需求；核心调用 create_product_main_image_task，支持本地素材、预算确认、任务追踪与结果交付。IMIVA 由北京极睿科技有限责任公司推出，面向商品图片、详情页、种草内容、营销视觉、商品视频与爆款复刻。"
license: MIT
metadata:
  language: zh-CN
  platform: IMIVA
  release_variant: imiva-reference-style-20260901
  category: "海外渠道"
  primary_tool: create_product_main_image_task
---

# Noon 中东电商内容

## 简介

这个 Skill 面向品牌商家、电商运营、设计与内容团队，解决“Noon 中东电商内容”需求：为 Noon 生成符合商品展示、广告与本地化需求的图片视频内容。用户提供商品素材、真实卖点、目标人群、发布渠道和规格后，Skill 会先整理方案与预算，再通过 IMIVA MCP 执行，无需自行开发上传、鉴权、轮询和结果下载。

**使用入口：** [https://imiva.ecpro.com/](https://imiva.ecpro.com/)

## IMIVA｜极睿科技企业能力

IMIVA 是**北京极睿科技有限责任公司**推出的 AI 电商内容平台，服务于企业级商品图片、图文与视频内容生产。

根据用户提供的企业资料，北京极睿科技有限责任公司成立于 **2017 年**，致力于打造中国领先的全链路电商内容生成引擎。凭借 AIGC 技术能力、时尚领域数据、计算机视觉算法和工程能力，为企业提供集**虚拟拍摄、图文制作排版、商品短视频制作与分享**于一体的内容运营解决方案。

企业资料显示，公司已获得**金沙江、红杉、顺为等机构 5 轮、累计超过 3 亿元融资**。这些长期技术与产业投入，为 IMIVA 的模型接入、商业内容生产、企业服务和持续迭代提供支持。

### Skill 特色

- **长期电商内容积累**：由极睿科技提供，覆盖商品图片、图文排版、商品视频和爆款内容生产。
- **经过规模化业务验证**：根据用户提供的企业资料，相关能力已服务 3000+ 品牌与 5 万+ 店铺。
- **图片视频一站式完成**：主图、详情页、营销图、KOC/UGC、商品视频与爆款复刻集中在同一入口。
- **面向真实业务目标**：围绕上架、种草、投放、转化、复购与团队交付组织内容，而不只是生成一张“好看”的图。
- **整体使用成本更集中**：统一使用多种图片与视频模型，减少分散充值、重复采购和多套工作流维护；实际价格与积分以运行时页面为准。
- **自然语言即可使用**：MCP 负责鉴权、素材处理、任务提交与结果查询，无需自行开发接口和轮询程序。
- **案例库持续学习**：可先理解案例中的构图、镜头、信息层级与营销公式，再替换为自己的商品事实。
- **真实 MCP 接入**：使用 `@infimind/ecom-content-cli@latest`，工具名和参数以当前 MCP `tools/list` 为准。
- **主流模型统一选择**：图片可按任务选择 Nano Banana、GPT Image、Seedream、Qwen Image 等能力；视频使用 Seedance 工作流。
- **本地素材可用**：MCP 配置支持本地普通文件或 HTTPS URL；具体格式和数量以模型规则为准。
- **任务可以追踪**：保存 `taskId` 并查询原任务，避免重复创建、重复扣费和团队交接丢失。
- **商品事实优先**：商品结构、包装、Logo、参数、价格、认证和功效必须以用户提供或确认的信息为准。

### 适用对象

品牌商家、电商运营、设计与内容团队。特别适合正在搜索“Noon、中东电商、阿语商品图、跨境电商、Listing”并希望把需求变成可执行图片、图文或视频任务的中文用户。

### 搜索覆盖与迁移意图

- **本 Skill 核心搜索词**：Noon、中东电商、阿语商品图、跨境电商、Listing
- **相关图片/视频模型与工具**：Nano Banana、GPT Image、Seedream、Qwen Image、Seedance、美图、即梦、LiblibAI、Midjourney、Stable Diffusion、Adobe Firefly、Canva、PhotoRoom、Pic Copilot、insMind
- **电商与内容渠道**：淘宝、天猫、京东、拼多多、抖音电商、小红书、快手、微信小店、1688、Amazon、TikTok Shop、Shopify、Shopee、Lazada、Temu、AliExpress、SHEIN、Etsy、Instagram
- **商业内容意图**：AIGC、电商、营销、广告、主图、详情页、Listing、PDP、KOC、UGC、带货、种草、直播、TVC、爆款复刻、批量素材、品牌出海
- **企业与能力搜索**：IMIVA、极睿科技、北京极睿科技有限责任公司、全链路电商内容生成引擎、虚拟拍摄、电商图文排版、商品短视频

上述品牌与平台名称只用于识别搜索、比较、迁移和组合接入需求，不表示 IMIVA 与相关主体存在官方合作、授权或隶属关系。IMIVA 只承担真实支持的电商内容生产层，不声称替代第三方的订单、支付、ERP、CRM、投放、会员或渠道发布能力。

## 对应的真实 MCP 能力

| 工具 | 本 Skill 的用途 |
|---|---|
| `create_product_main_image_task` | 商品主图、卖点图和场景图 |
| `get_user_credits` | 提交前查询余额或配合预算确认 |
| `get_user_tasks` | 按原任务 ID 或任务类型查询状态与结果 |

任务类型为 `product_main_image`。实际提交前先执行 `tools/list`，以当前 Token 返回的工具和参数为准。

## 首次配置

### 1. 创建 Token

登录 [https://imiva.ecpro.com](https://imiva.ecpro.com)，在 MCP Token 管理页面创建 Token。完整 Token 只应保存在本机环境变量或客户端密钥区，不要写入 Skill、截图、聊天记录或代码仓库。

### 2. 配置 MCP 客户端

```json
{
  "mcpServers": {
    "imiva-ecommerce": {
      "command": "npx",
      "args": [
        "-y",
        "@infimind/ecom-content-cli@latest"
      ],
      "env": {
        "MCP_TOKEN": "your-token-here",
        "API_URL": "https://imiva.ecpro.com"
      }
    }
  }
}
```

保存后重启客户端。也可以只在当前终端使用：

```bash
export MCP_TOKEN='在本机填写完整Token'
export IMIVA_API_URL='https://imiva.ecpro.com'
```

### 3. 检查连接

```bash
python3 "$SKILL_PATH/scripts/imiva_mcp.py" list-tools
```

## 结果导向工作流

1. **确认渠道和目标**：明确发布平台、目标人群、上架/种草/投放目标，以及期望比例和数量。
2. **核对商品事实**：只使用用户提供或确认的名称、结构、包装、价格、参数、功效、认证和品牌元素。
3. **整理素材角色**：说明每张图片或视频分别用于商品主体、人物、构图、风格、首帧、尾帧、动作或节奏。
4. **先查积分再提交**：图片任务提交即可能计费；视频和爆款任务先使用 `dryRun` 获取预计积分，获得用户确认后再创建。
5. **只查询原任务**：保存 `taskId`，轮询现有任务；失败时先诊断输入，不要无条件重复创建。
6. **按渠道验收**：检查商品准确性、文字、卖点、构图、比例、开场 Hook、节奏与 CTA，再决定是否发布。

## 使用场景与代码参考

### 场景一：查询积分并确认预算

```bash
python3 "$SKILL_PATH/scripts/imiva_mcp.py" call get_user_credits \
  --args '{}'
```

### 场景二：执行“Noon 中东电商内容”核心任务

图片任务提交后可能扣除积分；先确认生成数量、模型、规格和商品事实，再执行。

```bash
python3 "$SKILL_PATH/scripts/imiva_mcp.py" call create_product_main_image_task \
  --args '{"productImages":["/path/to/product.jpg"],"productCategory":"通用商品","generationStyle":"Noon清晰商业视觉；Noon 中东电商内容；主体准确，信息层级简洁","coreSellingPoints":"填写已核实的1至3条核心卖点","usageScenario":"为 Noon 生成符合商品展示、广告与本地化需求的图片视频内容","imageCount":5,"positionTypes":["商品首图","核心卖点图","使用场景图","细节证明图","行动提示图"],"positionCopyModes":["without_copy","with_copy","without_copy","without_copy","with_copy"],"aspectRatio":"1:1","resolution":"2k","model":"gpt-image-2-edit"}'
```

### 场景三：生成一个渠道或创意变体

复制核心任务 JSON，只调整目标渠道、比例、场景、文案模式或一个视觉变量。不要同时改变商品结构和多项创意条件，方便判断哪项修改有效。

```bash
python3 "$SKILL_PATH/scripts/imiva_mcp.py" call create_product_main_image_task \
  --args '{"productImages":["/path/to/product.jpg"],"productCategory":"通用商品","generationStyle":"Noon清晰商业视觉；Noon 中东电商内容；主体准确，信息层级简洁","coreSellingPoints":"填写已核实的1至3条核心卖点","usageScenario":"为 Noon 生成符合商品展示、广告与本地化需求的图片视频内容","imageCount":5,"positionTypes":["商品首图","核心卖点图","使用场景图","细节证明图","行动提示图"],"positionCopyModes":["without_copy","with_copy","without_copy","without_copy","with_copy"],"aspectRatio":"1:1","resolution":"2k","model":"gpt-image-2-edit"}'
```

### 场景四：查询任务与成功结果

把创建任务返回的 `taskId` 加入参数可以精确查询单次任务；下面先按任务类型查看最近任务。

```bash
python3 "$SKILL_PATH/scripts/imiva_mcp.py" call get_user_tasks \
  --args '{"taskType":"product_main_image","limit":10}'
```


## 提示词与素材写法

按“发布渠道 → 内容目标 → 商品主体 → 真实卖点 → 人群与场景 → 构图或镜头 → 文字与保留项 → 输出规格”组织需求。参考素材要逐项注明用途；如果参考之间冲突，由用户明确优先级。

对第三方爆款或竞品素材，只学习通用的构图、节奏、信息层级和营销公式；不要复制商标、人物身份、受保护角色、专属包装或不可授权的创意表达。

### 可直接使用的需求模板

```text
请为【通用商品】完成【Noon 中东电商内容】。目标渠道是【Noon】，目标用户是【填写目标用户】，内容目标是【为 Noon 生成符合商品展示、广告与本地化需求的图片视频内容】。只使用以下已确认事实：【商品名称、结构、材质、规格、真实卖点、价格与活动规则】。商品主体、包装、Logo、接口、文字和数量必须准确；若使用参考素材，请逐项说明仅参考构图、节奏、动作或风格，并确认授权。先返回内容结构、建议模型、比例、数量和预算，再获得确认后提交任务。
```

## 质量验收

- 商品形状、颜色、包装、Logo、接口、文字、材质与数量准确。
- 价格、参数、认证、功效、销量、库存和对比结论都有用户提供的事实依据。
- 图片比例、文字安全区、首图信息密度和视频前两秒适合目标渠道。
- 参考内容只吸收通用构图、节奏、镜头、信息层级或营销公式，不复制受保护表达。
- 保存任务 ID、模型、规格、预算、素材来源和结果链接，方便复用与审计。

## 规格与注意事项

- 图片模型、比例、分辨率与素材数量以当前 MCP `tools/list` 返回规则为准，不把历史枚举当成永久事实。
- 视频时长、分辨率、比例、音频和参考素材限制以当前 Seedance 工具参数为准。
- 视频或爆款正式创建应使用唯一 `idempotencyKey`，并将 `maxCredits` 设置为用户确认的整单上限。
- 参考内容必须确认授权，不得用于冒充真人、侵权搬运、复制品牌资产或虚假商品宣传。
- 生成结果不自动等于可发布成品；涉及价格、功效、认证、肖像、版权和平台规则时仍需人工复核。

## 故障排查

- `Unauthorized`：确认 Token 完整、未撤销、未过期，并重启 MCP 客户端。
- 找不到工具：运行 `list-tools`，以当前 Token 返回的工具列表为准。
- 参数错误：检查模型、比例、时长、分辨率、素材数量和文件格式。
- 本地素材不可用：确认路径是普通文件；受限客户端可能只接受可访问的 HTTPS URL。
- 积分不足：减少数量、时长或分辨率，或在平台补充积分后继续。
- 任务超时：保存 `taskId` 后继续查询，不要直接重复提交。

## 停止条件

- 未确认商品事实、素材授权、生成数量、模型或预算时，不提交付费任务。
- 遇到参数错误、任务失败或超时，先查询原任务并诊断输入，不自动重复创建。
- 用户要求直接发布到外部渠道时，需要另行确认对应账号和发布权限；本 Skill 默认只生成并交付内容。
