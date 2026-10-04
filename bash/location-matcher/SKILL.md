---
name: location-matcher
description: 当需要通过街景照片、文字描述、地标名称、建筑物特征、道路信息、商铺招牌等视觉或语义线索来定位实际地点的准确地址或经纬度时，使用此 skill。典型触发场景包括：1）询问照片拍摄位置（如"这张照片在哪里拍的？"、"这是哪个街道？"）；2）根据文字描述查找地点（如"有一个LAFORET SELECT招牌的地方在哪里？"、"描述中的十字路口对应什么位置？"）；3）验证某地点是否存在街景记录（如"XX路XX号有街景吗？"、"数据库里有这个位置的街景图像吗？"）；4）地址与坐标互转后的位置确认（如"这个地址对应的街景长什么样？"、"这个经纬度是什么地方？"）；5）询问图片中的建筑在哪里（如"找到有这个红色邮筒的街道"、"这个大厦在哪里？"）


---

# location-matcher

## 数据源
Elasticsearch 数据库的索引 `street` 中包含街景图像和相关位置信息元数据，每条文档代表一个街景图像及其相关信息，可以通过检索该索引来找到与用户输入的文本描述或图片相匹配的街景图像，并返回其位置信息（地址和经纬度）。

## 检索流程

### 1 输入解析
- 根据上下文抽取目标街景的描述文本 `description`（如果有文本输入）
- 根据上下文抽取图片路径 `image_path`（如果有图片输入）
- 从上下文抽取粗定位信息：地址 `address` 或 经纬度 `latitude/longitude`。（如果有）

### 2 地址转经纬度（可选）
如果上下文提供了地址但没有经纬度，调用地理编码脚本将地址转换为经纬度。

执行以下脚本：
```bash
conda run -n deerflow-street python /mnt/skills/custom/location-matcher/scripts/geocoding.py --address "提取的地址文本"
```

输出结果示例：
```json
{
  "latitude": 35.654008,
  "longitude": 139.705398
}
```

### 3 目标字段确定
执行 es_get_mapping 脚本查看索引字段结构，确定可用的目标字段和坐标字段。

```bash
conda run -n deerflow-street python /mnt/skills/custom/location-matcher/scripts/es_get_mapping.py --index street
```

- 根据需要动态确定返回字段

### 4 执行位置匹配检索

执行 es_retrieve_topk.py 脚本获取 Top-k 结果：

**基于图片检索**示例命令：
```bash
conda run -n deerflow-street python /mnt/skills/custom/location-matcher/scripts/es_retrieve_topk.py --target-field id,address,metadata.latitude,metadata.longitude --index street --k 3 --center-latitude 35.654008 --center-longitude 139.705398 --max-distance 2000 --image-path /path/to/image.jpg
```

**基于文本描述检索**示例命令：
```bash
conda run -n deerflow-street python /mnt/skills/custom/location-matcher/scripts/es_retrieve_topk.py --target-field id,address,metadata.latitude,metadata.longitude --index street --k 3 --description "A Japanese urban street scene with LAFORET SELECT signage" --center-latitude 35.654008 --center-longitude 139.705398 --max-distance 2000
```

**参数说明：**
- **必填参数：**
  - `--target-field`：希望返回的目标字段，支持逗号分隔多个字段，例如 `id,address,metadata.latitude,metadata.longitude`
- **可选参数：**
  - `--index`：检索索引名，默认 `street`
  - `--k`：返回结果数量，默认 `3`
  - `--description`：文本描述（如果有文本输入）
  - `--image-path`：图片路径（如果有图片输入）
  - `--center-latitude` / `--center-longitude` / `--max-distance`：地理过滤中心和半径（米）（如果有地理过滤需求）
- **注意：** 目前不支持同时输入文本描述 `description` 和图片 `image-path` 进行单次检索，需根据实际输入选择其一作为检索条件。如果可以分别执行两次检索（一次文本、一次图片），则分别执行并对结果进行融合。

### 5 验证检索结果（必须逐个检验每条文档的街景图片）
- 使用 `view_image` 工具查看检索结果中的每个 `source_path` 对应的街景图片，判断哪一条文档的街景图片与输入描述或图片匹配

#### 如果发现匹配的文档   
1. 构建**`证据.json`**文件到 `/mnt/user-data/outputs/`，包含以下要素：
  - **id**：与输入描述或图片匹配的文档 ID（`id`）
  - **地理位置信息**：该文档记录的地址字段（`address`）及精确坐标（`metadata.latitude`, `metadata.longitude`）
  - **source_path**： 文档记录的`source_path`信息
  - **判断依据**：说明检索结果与输入描述或图片匹配的依据，如图片中的哪些特征与输入描述或图片匹配



#### 如果检索到的文档与目标不匹配，说明匹配失败

### 5.5 经纬度转地址
如果检索到匹配成功的文档，将对应文档中的经纬度转换为可读地址
调用反向地理编码脚本：

```bash
conda run -n deerflow-street python /mnt/skills/custom/location-matcher/scripts/reverse_geocoding.py --latitude 35.654008 --longitude 139.705398
```

输出结果示例：
```json
{
  "address": "东京都涩谷区宇田川町"
}
```

### 6 生成回答

- **成功匹配场景：**
  - 输出检索结果中的地址信息
  - 概述检索结果以及判断依据，说明为什么认为该结果与输入描述或图片匹配
  - 在回答中引用匹配图片，并优先使用 Markdown 链接形式，例如 `[查看原图](<source_path>)`，供用户点击查看原图

- **匹配失败场景：**
  - 向用户明确说明：未找到匹配的街景信息，并解释可能原因（如地理范围限制、描述不够具体、数据库中不存在该位置街景等）

---

## 重要提醒

1. **执行环境：** 必须使用 `conda run -n deerflow-street` 执行所有 Python 脚本，确保在正确的 Conda 环境中运行
2. **路径格式：** 所有脚本路径必须使用绝对路径格式 `/mnt/skills/custom/location-matcher/scripts/...`
3. **工具调用规范：** 调用工具时的 `description` 字段一律使用**中文**描述
4. **结果验证：** **必须在答案中引用匹配图片， **推荐输出方式：** 为了确保前端可点击，优先在最终回答中输出 Markdown 链接，例如 `[查看原图](/mnt/nas/streetview_meta/queries/247query/247query/01125.jpg)`