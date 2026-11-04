---
name: pindou-pattern
description: 生成拼豆图纸（perler bead pattern）。把任意图片或像素数据量化为 205 色、5 大品牌色号（MARD/COCO/漫漫/盼盼/咪小窝）的拼豆施工图 PNG，含格内色号、行列坐标、加重网格线、色号用量统计，并可导出 CSV 物料清单。当用户提到拼豆、拼豆图纸、色号、像素画导出、把图片转成 N×N 拼豆、串珠/珠子图案、perler bead pattern、bead pattern 时使用；当用户对已生成图纸不满意（效果不好/不好看/颜色太乱/太杂/优化一下/AI 优化/重新弄好看点）时，先用 AI 图像编辑（基于原图参考图的 chibi 白底像素风改绘）再重新生成图纸。
---

# 拼豆图纸生成（pindou-pattern）

把图片或像素数据变成可直接照着拼的拼豆图纸 PNG：深色标题栏 + 渐变品牌 Logo + 四周行列坐标 + 30px 色块网格（格内标品牌色号、每 10 格加重线）+ 色号用量统计区。

## AI 优化效果（用户不满意时的处理流程）

当用户对已生成的图纸表达不满——如"效果不好"、"不好看"、"颜色太乱/太杂"、"细节糊了"、"帮我优化一下"、"AI 优化"、"重新弄好看点"——不要只调量化参数，走 **AI 重绘 → 重新生成** 两步。

### 第 1 步：AI 图像编辑（按优先级选择提供方）

**优先：agent 自带的 imagegen 工具。** 先检查你自己是否具备图像生成/编辑工具（如 Codex/WorkBuddy  会话内置的 `image_gen`、以 MCP 工具形式暴露的 imagegen 等）。若有，直接用它执行下面的默认 PROMPT 编辑原图（**必须把原图作为参考图传入**，纯文本提示会凭空重绘出无关内容），把结果保存为本地文件（如 `原名_optimized.png`），跳过 optimize.js：

```
图片修改为：chibi画风，背景白底。pixel art style, 16-bit, retro game aesthetic, sharp focus, high contrast, clean lines, detailed pixel art, masterpiece, best quality
```

**没有自带工具时：运行 optimize.js**，脚本自动选择提供方（`--provider auto`）：

```bash
node .agents/skills/pindou-pattern/scripts/optimize.js 原图.png
# 提供方优先级: codex（WorkBuddy 版）CLI 内置 imagegen（免积分，需已装并开启 image_generation）
#              → apiz CLI 图像编辑（约 60~65 积分/次，默认 openai/gpt-image-2/edit，兜底）
```

### 第 2 步：用优化图重新生成图纸

```bash
node .agents/skills/pindou-pattern/scripts/generate.js 原图_optimized.png --size 48 --system 盼盼 --blank-white --max-colors 16
```

要点：

- **优化图路径以第 1 步 stdout 打印的实际输出为准**：codex 路径默认 `_optimized.png`，apiz 路径默认 `_optimized.jpg`，不要照抄示例里的扩展名。
- **`--max-colors 16` 是 AI 优化后的推荐搭配**：AI 输出通常为 ~1024px JPEG，压缩噪点会让直接量化散出 100+ 色；收敛到 12~24 色后物料清单才实用。实测 104 色 → 16 色，主体轮廓不受影响。
- **优化结果交给用户对比判断**：把原图、优化图、最终图纸三个路径都报给用户，由用户查看确认。不做视觉模型复核。若用户反馈优化图与原图内容无关（参考图未生效的表现），检查 `--params image_urls` 传参后重试。
- `--blank-white` 只用于白底主体图（卡通角色等），风景/满幅图案**不要**用（天空云朵是要买的豆子）。AI 的"白底"常带 ±10 偏色（实测 245,251,251），默认阈值 240 已能接住。
- `--prompt` 可换自定义指令；apiz 路径 `--model` 可换编辑模型（默认 openai/gpt-image-2/edit）。
- 全部提供方不可用时，回退为仅调整 `--max-colors` / `--size` / `--match` 参数，并向用户说明。

## 环境

- Node.js（≥16）+ `sharp`（唯一 npm 依赖，skill 根目录已带 package.json）。**首次使用**在 skill 根目录执行一次 `npm install` 即可；若脚本报缺少 sharp，提示用户执行该命令。依赖按脚本所在路径向上查找 node_modules，与当前运行目录无关；仅当上游目录（如本仓库根 node_modules）已装 sharp 时可免安装直接运行。
- AI 优化为可选能力，额外依赖（按提供方）：agent 自带 imagegen 工具 / codex CLI / apiz CLI，三者任一即可，全部缺失时仅影响 AI 优化（出图不受影响）。

## 快速开始

```bash
# 图片 → 32×32 MARD 图纸（默认输出 <输入名>_pattern.png）
node .agents/skills/pindou-pattern/scripts/generate.js 素材/卡通猫.png

# 指定品牌、尺寸、标题、输出路径，并把近白背景当空格
node .agents/skills/pindou-pattern/scripts/generate.js 素材/卡通猫.png \
  --size 48 --system 盼盼 --title 卡通猫 --blank-white --out 图纸/猫.png

# JSON 像素数据 → 图纸 + CSV 物料清单
node .agents/skills/pindou-pattern/scripts/generate.js 作品.json --csv 物料.csv
```

## 输入格式

图片（png/jpg/webp/bmp/gif/tiff）或 JSON。JSON 格式：

```json
{
  "gridSize": 16,
  "pixelData": ["#FFFFFF", "#FBED56", "..."]
}
```

- 图片输入：透明区域先合成白底再量化；非方形图片等比缩放（contain）、空缺处补白，不加 `--blank-white` 时补白会计入浅色豆
- `pixelData` 行优先一维数组，长度 = gridSize²，`#FFFFFF` 表示空格（不买豆）
- JSON 中的非调色板颜色默认自动吸附到最近的 205 色色号（保证能买到豆子）；`--no-snap` 关闭

## 常用选项

| 选项 | 说明 | 默认 |
|------|------|------|
| `--size <n>` | 网格 N×N（4~150），仅图片输入生效 | 32 |
| `--system <name>` | 色号系统：MARD / COCO / 漫漫 / 盼盼 / 咪小窝 | MARD |
| `--match <mode>` | 颜色匹配：rgb（欧氏距离）/ lab（感知色差，通常更准） | rgb |
| `--blank-white` | 图片近白色当作空格 | 关 |
| `--white-threshold <n>` | 近白判定阈值（配 --blank-white，默认 240；AI 白底常带 ±10 偏色，必要时可调低到 230 更激进留空） | 240 |
| `--max-colors <n>` | 色数收敛：保留用量前 n 色，低频色并入最接近的保留色（照片/AI 优化图推荐 12~24） | 不限制 |
| `--title <text>` / `--watermark <text>` | 标题 / 水印（空串去除） | 拼豆图纸 / pindou.348349.xyz |
| `--interval <n>` / `--grid-color <hex>` | 加重线间隔 / 颜色 | 10 / #555555 |
| `--no-grid` `--no-coordinates` `--no-cellnumbers` `--no-stats` | 关闭对应图层 | 全开 |
| `--csv <path>` | 导出色号用量 CSV（Excel 友好带 BOM） | 无 |
| `--out <path>` | 输出 PNG 路径 | `<输入名>_pattern.png` |

完整选项见 `node .../generate.js --help`。

回归测试（skill 改动后跑一次确认功能正常）：

```bash
node .agents/skills/pindou-pattern/scripts/generate.js .agents/skills/pindou-pattern/assets/sample-heart.json --out heart_test.png
# 预期: 16x16 | 用色 2 种 | 总豆数 128 颗 | F02 ×125 | E03 ×3（验证后删除 heart_test.png）
```

## 工作流程

1. 确认用户想要的：网格尺寸（16/24/32/48/100 是常用档位）、品牌色号系统、是否需要背景留空。若用户表达的是对已有图纸的不满，转到上面的「AI 优化效果」流程。
2. 运行 generate.js，命令会向 stdout 打印：输出路径、画布尺寸、用色数、总豆数、每个色号的用量。
3. 向用户报告：图纸路径 + 色号用量清单（直接引用 stdout 统计）+ 总豆数；有 CSV 时一并给出路径。

**不做视觉目检。** 生成流程是确定性的，客观指标以脚本 stdout 统计和（必要时）像素级检查为准；图纸好坏由用户自行查看判断。不要用视觉模型去"复核"图片内容——实测幻觉率高，会制造误判。

## 色号数据维护

- 色号映射表 `scripts/colorData.js`（205 色 × 5 品牌）已内联在本 skill 中，运行不依赖任何外部文件。如需更新数据，传入 colorData.ts 源文件路径重新提取（勿手改 colorData.js）：

  ```bash
  node .agents/skills/pindou-pattern/scripts/_extract.js <colorData.ts 的路径>
  ```

- 渲染链路：SVG → sharp → PNG。
