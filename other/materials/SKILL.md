---
name: materials
description: UrhoX 引擎内置材质库与 PBR 材质系统完整指南，包含 35+ 预制材质（地面、墙面、金属、木材、石材、玻璃等）和程序化材质配置。Use when users need to (1) 选择或添加材质 material 纹理 贴图, (2) 展示/演示/demo 引擎内置材质或预制材质库, (3) 搭建 3D 场景（室内/室外/工业/自然）, (4) 创建 PBR 视觉效果（金属 metal、玻璃 glass、发光 emissive、水面 water）, (5) 使用基础几何体 Box/Sphere/Cylinder 搭建环境, or any other material-related tasks.
---

# 材质选择指南

## 🔴 关键规则：不要猜测 Technique 路径！

**程序化材质（纯色/无贴图）只能使用以下 Technique**：

| 效果 | Technique 路径 | 说明 |
|------|---------------|------|
| **不透明 PBR** | `Techniques/PBR/PBRNoTexture.xml` | ✅ 默认首选 |
| **透明 PBR** | `Techniques/PBR/PBRNoTextureAlpha.xml` | ✅ 玻璃/冰/水晶 |
| **无光照** | `Techniques/NoTextureUnlit.xml` | ✅ 卡通/UI |

```

**记住**：`PBRMetallicRough*` 和 `PBRDiff*` 系列都需要贴图，程序化材质用 `PBRNoTexture` 系列！

---

## 决策流程

```
分析场景需求
    ↓
判断材质类型
    ├─ 需要真实纹理（地板/墙壁/草地等）→ 预制材质库（见下方）
    └─ 不需要 → 程序化材质（只用 PBRNoTexture 系列！）
            ├─ 不透明 → PBRNoTexture.xml
            ├─ 透明 → PBRNoTextureAlpha.xml
            ├─ 发光 → PBRNoTexture.xml + Emissive 参数
            ├─ 卡通/无光照 → NoTextureUnlit.xml
            └─ 水面 → Materials/SingleLayerWater.xml（材质实例）
```

## 使用程序化材质的场景

- **卡通/低多边形风格** - 纯色更符合风格
- **抽象艺术/几何可视化** - 需要精确颜色控制
- **动态变色物体** - 运行时改变颜色
- **UI/指示器元素** - 简单纯色即可

---

## 预制材质库

使用方式：`cache:GetResource("Material", res_uri)`

### flooring - 地面材质

| 名称 | res_uri | 关键词 | 用途 |
|------|---------|--------|------|
| 方块地砖 BlockFlooring01 | `uuid://Hw7_CePj4QdSOcXIloCyqlTu` | 地砖 瓷砖 tile floor | 室内地板、卫生间、厨房 |
| 石板铺装 StonePaving01 | `uuid://GSN7IaGGBlvP2Xk_zX9UQyuq` | 石板 铺装 paving sidewalk | 人行道、广场、庭院 |
| 石板铺装变体 StonePaving02 | `uuid://DBZayTa0xAHpg9NRUkG4HLIs` | 石板 paving | 人行道、广场 |
| 赤陶地砖 TerracottaFloor01 | `uuid://GLSXwQ8eqB8Tr-PKSCvyApps` | 赤陶 地中海 terracotta rustic | 地中海风格、乡村风格 |
| 城市人行道 UrbanSidewalk01 | `uuid://DKmYSWaMUJO6PDtihBbjHUQj` | 人行道 城市 街道 urban sidewalk | 城市街道、公共空间 |

### wall - 墙面材质

| 名称 | res_uri | 关键词 | 用途 |
|------|---------|--------|------|
| 红砖墙 BrickWall01 | `uuid://DXjwQX_lcF60zC4F9y9yAyG_` | 砖墙 红砖 工业风 brick industrial | 建筑外墙、工业风室内 |
| 红砖墙变体 BrickWall02 | `uuid://Fzw34Qw1kcxpkzjPX6twIfjx` | 砖墙 brick | 建筑外墙、装饰墙 |

### nature - 自然材质

| 名称 | res_uri | 关键词 | 用途 |
|------|---------|--------|------|
| 草地 Grass01 | `uuid://EFSiAWPsKtpGQpTAGBbflyyK` | 草地 草坪 公园 grass lawn garden | 公园、花园、户外场景 |
| 沙子 Sand01 | `uuid://FA-0GUs_3oaHzyb-ntH1Nkwf` | 沙子 沙滩 沙漠 sand beach desert | 沙滩、沙漠、沙坑 |
| 土壤 Soil01 | `uuid://B2-Y8QtOc5NdOQVWAmvW1aQ_` | 土壤 泥土 soil dirt earth | 花园、农田、森林地面 |

### stone - 石材材质

| 名称 | res_uri | 关键词 | 用途 |
|------|---------|--------|------|
| 大理石 Marble01 | `uuid://HndW0W0ASO7zyBNhRXFeCwdL` | 大理石 奢华 marble luxury | 地板、墙面、台面 |
| 花岗岩 Granite01 | `uuid://G64DiYIxPI0vUeNTwq2F9B6I` | 花岗岩 台面 granite countertop | 厨房台面、地板、高档建筑 |
| 岩石 Stone01 | `uuid://Hg04wSbDi8KsIwqNpUJ0OiwN` | 石头 岩石 rock boulder | 景观石、墙面装饰、山体 |
| 岩石变体A Stone02 | `uuid://Cv_0id_Hb5MomJLKxjp_8o-Z` | 岩石 rock | 景观石、户外场景 |
| 岩石变体B Stone03 | `uuid://DgtxmaZPuQDLEIyCEy5ewKEk` | 岩石 rock | 景观石、户外场景 |

### metal - 金属材质

| 名称 | res_uri | 关键词 | 用途 |
|------|---------|--------|------|
| 金属-抛光 Metal01 | `uuid://D9QYQXRhlgGnRlDw8jDNGTya` | 金属 钢铁 不锈钢 metal steel polished | 机械设备、不锈钢器具 |
| 金属-拉丝 Metal02 | `uuid://Cis1sX30rhdTXVgC4QEwquGW` | 金属 拉丝 brushed | 机械设备、金属部件 |
| 金属-做旧 Metal03 | `uuid://FZIHOeDP_05jbHvpVhZaH2n9` | 金属 做旧 锈蚀 rust weathered | 旧设备、废弃场景、工业风 |
| 金属变体A Metal04 | `uuid://A3SycZi1JoM9pk7OapeokKrD` | 金属 metal | 金属部件 |
| 金属变体B Metal05 | `uuid://AGiZMVN0UVT0043gRgOmHCgn` | 金属 锈迹 rust | 工业场景 |

### wood - 木材材质

| 名称 | res_uri | 关键词 | 用途 |
|------|---------|--------|------|
| 木材 Wood01 | `uuid://DdH4-Su6Cppk8qaKI2AiCLs-` | 木材 木头 木纹 wood timber | 家具、门窗、装饰板 |
| 木栅栏 WoodenFence01 | `uuid://DoyqwWBUuF1yLRwH3fXFZYdV` | 木栅栏 围栏 fence garden | 围栏、花园、农场 |
| 拼花木地板 WoodParquet01 | `uuid://G43HiRFgrh9VScIcXnDO4xGs` | 木地板 拼花 parquet hardwood | 室内地板、高档住宅 |

### fabric - 布料材质

| 名称 | res_uri | 关键词 | 用途 |
|------|---------|--------|------|
| 皮革 Leather01 | `uuid://BtiNefgEFw9WIRIi6Mflh8ik` | 皮革 真皮 沙发 leather sofa | 沙发、椅子、汽车内饰 |
| 皮革变体A Leather02 | `uuid://GYQrkcfcjIQDn0fDQyjyfZ6z` | 皮革 leather | 沙发、椅子 |
| 皮革变体B Leather03 | `uuid://Gy5DAQ63pu9LzljV2IPqficu` | 皮革 leather | 沙发、椅子 |
| 海军蓝斜纹布 NavyChino01 | `uuid://FsRPCfK_BAj7uc2vemxZwSA8` | 布料 织物 fabric cloth navy | 沙发布、窗帘、软装饰 |

### building - 建筑材质

| 名称 | res_uri | 关键词 | 用途 |
|------|---------|--------|------|
| 混凝土 Concrete01 | `uuid://Gm0CwVtSclGB7uj0Zs_eP8Gs` | 混凝土 水泥 工业 concrete cement | 建筑地面、工业场景、停车场 |
| 混凝土变体 Concrete02 | `uuid://GMR70cPvbaF6F8SvtDto--G_` | 混凝土 concrete | 建筑地面、工业场景 |
| 石膏墙面 Plaster01 | `uuid://DSu7mcyfcXMfcpmHSWtv4KUm` | 石膏 墙面 白墙 plaster wall | 室内墙壁、天花板 |
| 石膏墙面变体A Plaster02 | `uuid://HsEoYXiILuYv6lgH9cD7hTMy` | 石膏 plaster | 室内墙壁 |
| 石膏墙面变体B Plaster03 | `uuid://F9RR0VT43mKFKOubw-_cY5vw` | 石膏 plaster | 室内墙壁 |

### special - 特殊材质

| 名称 | res_uri | 关键词 | 用途 |
|------|---------|--------|------|
| 玻璃 Glass01 | `uuid://Ex1LOem8FjFM7P9QTfyGjOTn` | 玻璃 透明 窗户 glass window | 窗户、玻璃门、镜子 |
| 碳纤维 CarbonFiber01 | `uuid://CvRSGW0wN84mcboHjqgVj7m3` | 碳纤维 科技 carbon fiber tech | 汽车部件、运动器材 |
| 陶瓷 Ceramic01 | `uuid://HnYiCXEnQqcYKObRdk8q-Yiv` | 陶瓷 釉面 ceramic porcelain | 餐具、卫浴设备、装饰品 |
| 橡胶 Rubber01 | `uuid://AkBCiS2MNfpI1vQqS6idJev_` | 橡胶 轮胎 rubber tire grip | 轮胎、防滑垫、把手 |
| 喷漆表面 SprayPainted01 | `uuid://BeeVGafEvOlO71Gx7t73Uf16` | 喷漆 涂装 汽车漆 spray paint | 汽车车身、家电外壳 |

---

## 程序化材质（PBRNoTexture 系列）

> 🔴 **重要**：程序化材质**只用** `PBRNoTexture.xml` 或 `PBRNoTextureAlpha.xml`！
> 不要编造其他 Technique 路径！

### PBR 不透明（默认首选）⭐

**Technique**: `Techniques/PBR/PBRNoTexture.xml`（唯一选择！）

```lua
local mat = Material:new()
mat:SetTechnique(0, cache:GetResource("Technique", "Techniques/PBR/PBRNoTexture.xml"))
mat:SetShaderParameter("MatDiffColor", Variant(Color(r, g, b, 1.0)))
mat:SetShaderParameter("Metallic", Variant(0.0))    -- 0=非金属, 1=金属
mat:SetShaderParameter("Roughness", Variant(0.5))   -- 0=光滑, 1=粗糙
```

**可用参数**（来自 Technique 定义）：
| 参数 | 默认值 | 说明 |
|------|--------|------|
| MatDiffColor | (1,1,1,1) | 漫反射颜色 RGBA |
| MatSpecColor | (0.5,0.5,0.5,1) | 高光颜色 |
| MatEmissiveColor | (0,0,0) | 自发光颜色 RGB |
| Metallic | 0 | 金属度 0-1 |
| Roughness | 0.5 | 粗糙度 0-1 |

**常见效果参数组合**：
| 效果 | Metallic | Roughness |
|------|----------|-----------|
| 光滑金属（镜面） | 0.9-1.0 | 0.1-0.2 |
| 磨砂金属（拉丝） | 0.9-1.0 | 0.4-0.6 |
| 光滑塑料 | 0.0 | 0.3-0.5 |
| 橡胶/哑光 | 0.0 | 0.7-0.9 |
| 陶瓷/光滑 | 0.0 | 0.1-0.3 |

### PBR 透明（玻璃/冰/水晶）

**Technique**: `Techniques/PBR/PBRNoTextureAlpha.xml`（唯一选择！）

```lua
local mat = Material:new()
mat:SetTechnique(0, cache:GetResource("Technique", "Techniques/PBR/PBRNoTextureAlpha.xml"))
mat:SetShaderParameter("MatDiffColor", Variant(Color(r, g, b, 0.3)))  -- A=透明度
mat:SetShaderParameter("Roughness", Variant(0.05))  -- 玻璃通常很光滑
```

### 自发光（在 PBRNoTexture 基础上添加）

```lua
-- 在任何 PBRNoTexture 材质上添加发光
mat:SetShaderParameter("MatEmissiveColor", Variant(Color(1.0, 0.5, 0.2)))
-- 颜色值 >1.0 可增强发光强度（HDR）
mat:SetShaderParameter("MatEmissiveColor", Variant(Color(3.0, 1.5, 0.6)))  -- 更亮
```

### 无光照（卡通/UI）

**Technique**: `Techniques/NoTextureUnlit.xml`

```lua
local mat = Material:new()
mat:SetTechnique(0, cache:GetResource("Technique", "Techniques/NoTextureUnlit.xml"))
mat:SetShaderParameter("MatDiffColor", Variant(Color(r, g, b, 1.0)))
```

### 水面（使用预制材质实例）

```lua
-- 水面使用预制材质实例，不要自己创建
local mat = cache:GetResource("Material", "Materials/SingleLayerWater.xml")
mat:SetShaderParameter("WaterTint", Variant(Color(0.2, 0.4, 0.8)))  -- RGB，无Alpha
```

---

## 🚫 不要使用的 Techniques

以下 Techniques 存在但**需要贴图**，不要用于程序化纯色材质：

```
Techniques/PBR/PBRMetallicRoughDiffNormalSpec.xml     -- 需要 Diffuse+Normal+Spec
Techniques/PBR/PBRMetallicRoughDiffNormalSpecAlpha.xml
Techniques/PBR/PBRMetallicRoughDiffSpec.xml           -- 需要 Diffuse+Spec
Techniques/PBR/PBRDiffNormal.xml                      -- 需要 Diffuse+Normal
Techniques/PBR/PBRDiff.xml                            -- 需要 Diffuse
```

这些适合预制材质或需要纹理的场景，不适合程序化生成。

---

## 常见场景材质选择

| 场景 | 推荐材质 |
|------|---------|
| 厨房 | 地面: BlockFlooring01, 墙面: Plaster01, 台面: Granite01/Marble01 |
| 客厅 | 地面: WoodParquet01, 墙面: Plaster01, 沙发: Leather01 |
| 户外公园 | 地面: Grass01, 小路: StonePaving01, 围栏: WoodenFence01 |
| 工业场景 | 地面: Concrete01, 墙面: BrickWall01, 设备: Metal01-05 |
| 城市街道 | 地面: UrbanSidewalk01, 建筑: Concrete01/BrickWall01 |
