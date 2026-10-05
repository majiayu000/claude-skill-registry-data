---
name: nvg-resolution-mode
description: "【必读】NanoVG 项目分辨率模式选择指南。在调用 nvgBeginFrame 前必须先确定分辨率模式，否则高 DPI 屏幕会出现 UI 过小/模糊问题。\nSKIP when: 项目没有任何 raw NanoVG 调用（纯 urhox-libs/UI 组件项目、纯 3D 游戏 + UI HUD）。\nMUST trigger when: 项目包含 raw NanoVG 调用（nvgCreate/nvgBeginFrame），无论是否同时使用 UI 组件。典型场景：(1) NanoVG 2D 游戏, (2) NanoVG 2D 游戏 + UI HUD, (3) 用户提到 DPI/DPR/Retina/高清屏/分辨率适配。\n默认选择：明确了设计分辨率 → 模式A（设计分辨率）；未明确设计分辨率（默认） → 模式B（系统逻辑分辨率|DPR修正）；模式C（物理像素）不推荐。信息不足时让用户三选一，引导用户选择并提供相应设计数据。\n涵盖三种模式及 nvgBeginFrame 参数、坐标转换、输入处理。"
---

# NanoVG 分辨率模式编写范式

> 本指南面向 AI 辅助编程优化，默认选择优先保证鲁棒性和首次成功率。

三种模式是**递进叠加**关系：C（无缩放）→ B（+DPR）→ A（+设计缩放）

## 核心变量

```lua
local physW, physH = graphics:GetWidth(), graphics:GetHeight()  -- 物理分辨率
local dpr = graphics:GetDPR()                                   -- 设备像素比（1.0/2.0/3.0）
local logicalW, logicalH = physW / dpr, physH / dpr             -- 系统逻辑分辨率
```

**关系**：`系统逻辑分辨率 = 物理分辨率 / DPR`

---

## 模式选择

> **默认规则**：除非明确提供了设计分辨率，否则始终选择模式 B，以迎合AI习惯。

| 条件 | 模式 | 基于 | 布局推荐 |
|------|------|------|----------|
| **明确**了设计分辨率 | A（设计分辨率） | B + 设计缩放 | 绝对布局 / 响应式 |
| 未明确设计分辨率（**默认**） | B（系统逻辑分辨率） | C + DPR 修正 | 响应式 |
| 不建议，仅当用户明确要求 | C（物理像素） | 基础 | 响应式 |

**识别设计分辨率**：
- "按 1080P 做"、"720P 适配"、"1920×1080"、"设计尺寸是..." → 模式 A

**决策场景**：
- **应用/工具向**（模拟器、仪表盘、编辑器）→ **B**
- **游戏向** → 视需求而定：
  - 默认/顺 AI（成功率优先、快速出原型）→ **B**
  - 进阶需求（UI 密集、逻辑依赖 2D 坐标）→ **A**

---

## 模式 C：物理像素（基础）

基础代码，无任何缩放。仅当用户明确要求时使用，高 DPI 屏幕上内容显小。不建议直接使用。

```lua
nvgBeginFrame(vg, physW, physH, 1.0)
-- 坐标 1 单位 = 1 物理像素
-- 坐标范围：(0,0) 到 (physW, physH)
nvgEndFrame(vg)
```

**输入坐标**：引擎返回物理像素，无需转换。

---

## 模式 B：系统逻辑分辨率（默认）

在 C 基础上加 **DPR 修正**，高 DPI 屏幕清晰。未明确设计分辨率时的默认选择，必须用响应式布局。

```lua
nvgBeginFrame(vg, logicalW, logicalH, dpr)  -- 改用逻辑分辨率 + pixelRatio=dpr
-- 坐标 1 单位 = 1 逻辑像素 = dpr 个物理像素
-- 坐标范围：(0,0) 到 (logicalW, logicalH)
nvgEndFrame(vg)
```

**输入坐标**：`logicalX = inputX / dpr`

### 完整示例

```lua
local physW, physH = graphics:GetWidth(), graphics:GetHeight()
local dpr = graphics:GetDPR()
local logicalW, logicalH = physW / dpr, physH / dpr

function HandleNanoVGRender()
    nvgBeginFrame(vg, logicalW, logicalH, dpr)

    -- 响应式布局：百分比/锚点定位
    local padding = 20
    local btnW, btnH = 120, 40

    -- 右上角按钮
    nvgBeginPath(vg)
    nvgRect(vg, logicalW - btnW - padding, padding, btnW, btnH)
    nvgFillColor(vg, nvgRGBA(100, 150, 200, 255))
    nvgFill(vg)

    nvgEndFrame(vg)
end

-- 窗口变化
SubscribeToEvent("ScreenMode", function()
    physW, physH = graphics:GetWidth(), graphics:GetHeight()
    dpr = graphics:GetDPR()
    logicalW, logicalH = physW / dpr, physH / dpr
end)
```

---

## 模式 A：设计分辨率（进阶）

> **使用前提**（至少满足一项）：
> - 用户提供了设计尺寸（如：1920x1080、1080P、720P等）
> - UI 大量使用固定坐标布局
> - 不同屏幕下核心内容必须视觉比例一致
> - 给定的参考项目满足以上几点
>
> 否则，留在模式 B。

在 B 基础上加 **设计缩放**。

### 设计尺寸定义

| 写法 | 示例 | 说明 |
|------|------|------|
| 单分量（简化） | `designSize = 1080` | 等价于 `designW = designH = 1080` |
| 双分量（完整） | `designW, designH = 1920, 1080` | 完整设计尺寸 |

### 核心公式

```lua
-- 输入（二选一）
local designSize = 1080                          -- 单分量
local designW, designH = designSize, designSize
-- 或
local designW, designH = 1920, 1080              -- 双分量

-- 缩放因子（CONTAIN：设计区域完整显示，设计区域外需要响应式布局）
local scale = math.min(logicalW / designW, logicalH / designH)

-- 缩放因子（COVER：设计区域填满屏幕，边缘裁剪，不常用）
-- local scale = math.max(logicalW / designW, logicalH / designH)

-- 设计空间下的屏幕尺寸和居中偏移
local screenDesignW = logicalW / scale
local screenDesignH = logicalH / scale
local designOffsetX = (screenDesignW - designW) / 2
local designOffsetY = (screenDesignH - designH) / 2
```

### 布局方式

可自由选择或混合，常用 “纯响应式” 或 “绝对布局” + “部分响应式”。

| 布局 | 代码 | 坐标范围 |
|------|------|----------|
| 响应式（屏幕空间） | 只用 `nvgScale` | (0,0) 到 (screenDesignW, screenDesignH) |
| 绝对布局（设计空间） | `nvgScale` + `nvgTranslate` | (0,0) 到 (designW, designH) |

**混合布局说明**
在设计区域内绝对布局时，设计区域外的内容仍需响应式处理（背景填充去黑边、全屏遮罩、屏幕边缘停靠等）。

**核心代码**：

```lua
nvgBeginFrame(vg, logicalW, logicalH, dpr)
nvgScale(vg, scale, scale)
-- 坐标范围：(0,0) 到 (screenDesignW, screenDesignH)

-- [响应式] 屏幕空间，用 screenDesignW/H 定位
DrawRectWrap(vg, screenDesignW - 220, 20, 200, 60)  -- 右上角

-- 进入设计空间
nvgTranslate(vg, designOffsetX, designOffsetY)

-- [绝对布局] 设计空间内，边界 (0,0)-(designW, designH)
DrawRectWrap(vg, 100, 50, 200, 80)  -- 设计稿坐标

-- [响应式] 临时切回屏幕空间，右上角停靠
nvgTranslate(vg, -designOffsetX, -designOffsetY)
DrawRectWrap(vg, screenDesignW - 200, 20, 180, 60)
nvgTranslate(vg, designOffsetX, designOffsetY)

nvgEndFrame(vg)
```

### 输入坐标转换

| 布局 | 转换公式 |
|------|----------|
| 响应式（屏幕空间） | `designX = inputX / dpr / scale` |
| 绝对布局（设计空间） | `designX = inputX / dpr / scale - designOffsetX` |

### 完整示例

```lua
local physW, physH = graphics:GetWidth(), graphics:GetHeight()
local dpr = graphics:GetDPR()
local logicalW, logicalH = physW / dpr, physH / dpr

-- 输入（二选一）
local designW, designH = 1920, 1080  -- 双分量
-- local designSize = 1080; designW, designH = designSize, designSize  -- 单分量

local scale, screenDesignW, screenDesignH, designOffsetX, designOffsetY

local function RecalcLayout()
    scale = math.min(logicalW / designW, logicalH / designH)
    screenDesignW = logicalW / scale
    screenDesignH = logicalH / scale
    designOffsetX = (screenDesignW - designW) / 2
    designOffsetY = (screenDesignH - designH) / 2
end
RecalcLayout()

function HandleNanoVGRender()
    nvgBeginFrame(vg, logicalW, logicalH, dpr)
    nvgScale(vg, scale, scale)

    -- [响应式] 背景填满屏幕（用 screenDesignW/H）
    nvgBeginPath(vg)
    nvgRect(vg, 0, 0, screenDesignW, screenDesignH)
    nvgFillColor(vg, nvgRGBA(30, 30, 40, 255))
    nvgFill(vg)

    -- 进入设计空间
    nvgTranslate(vg, designOffsetX, designOffsetY)

    -- [绝对布局] 设计空间内，边界 (0,0)-(designW, designH)
    nvgBeginPath(vg)
    nvgRect(vg, 50, 50, 300, 30)
    nvgFillColor(vg, nvgRGBA(255, 0, 0, 200))
    nvgFill(vg)

    -- [响应式] 临时切回屏幕空间，右上角停靠
    nvgTranslate(vg, -designOffsetX, -designOffsetY)
    nvgBeginPath(vg)
    nvgRect(vg, screenDesignW - 200, 20, 180, 60)
    nvgFillColor(vg, nvgRGBA(100, 150, 200, 255))
    nvgFill(vg)
    nvgTranslate(vg, designOffsetX, designOffsetY)

    nvgEndFrame(vg)
end

SubscribeToEvent("ScreenMode", function()
    physW, physH = graphics:GetWidth(), graphics:GetHeight()
    dpr = graphics:GetDPR()
    logicalW, logicalH = physW / dpr, physH / dpr
    RecalcLayout()
end)
```

### 可轻松从 B 升级到 A（DPR 巧妙抵消）

模式 A 基于 B 实现，只需加 `nvgScale`（响应式）或 `nvgScale` + `nvgTranslate`（绝对布局）。DPR 在计算中被约掉（`scale × dpr = physW / designSize`），本质是设计坐标到物理像素的直接映射。

---

## 输入坐标转换汇总

引擎输入 API 返回物理像素：

```lua
-- 桌面端
local mousePos = input:GetMousePosition()
local inputX, inputY = mousePos.x, mousePos.y

-- 移动端（触摸事件中）
local inputX = eventData:GetInt("X")
local inputY = eventData:GetInt("Y")
```

| 模式 | 转换公式 |
|------|----------|
| C（物理像素） | 无需转换 |
| B（系统逻辑分辨率） | `logicalX = inputX / dpr` |
| A 响应式（屏幕空间） | `designX = inputX / dpr / scale` |
| A 绝对布局（设计空间） | `designX = inputX / dpr / scale - designOffsetX` |

---

## 问题诊断

| 症状 | 可能原因 | 解决方案 |
|------|----------|----------|
| 高 DPI 屏幕 UI 过小 | 使用了模式 C（无 DPR 修正） | 改用模式 B 或 A |
| UI 模糊/不清晰 | pixelRatio 设置错误 | 确保 `nvgBeginFrame` 的 pixelRatio = dpr |
| 点击/触摸位置不准 | 输入坐标未转换 | 检查输入坐标转换公式 |
| 窗口缩放后 UI 错位 | 未监听 ScreenMode 事件 | 添加 ScreenMode 事件重算变量 |
| 设计稿内容被裁剪 | 使用了 COVER 模式 | 改用 CONTAIN（math.min） |

---

## 备注

本文档适用于包含 raw NanoVG 调用的项目。引擎渲染顺序为 **raw NanoVG → UI Widget 树 → 虚拟摇杆**，`urhox-libs/UI` 在 Widget 层渲染，内部已自动处理分辨率缩放，不需要本 Skill。但如果项目同时使用 raw NanoVG（如 2D 游戏图形）+ UI 组件（如 HUD），仍需本 Skill 配置 NanoVG 部分的分辨率。

*最后更新: 2026-02-09*
