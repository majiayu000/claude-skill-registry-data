---
description: 高级桌面自动化技能，提供像素级精确的鼠标控制、键盘输入、屏幕截图、窗口管理和剪贴板操作
---

# 桌面控制技能

**OpenClaw 最先进的桌面自动化技能。** 提供像素级精确的鼠标控制、闪电般的键盘输入、屏幕截图、窗口管理和剪贴板操作。

## 🎯 功能特性

### 鼠标控制
- ✅ **绝对定位** - 移动到精确坐标
- ✅ **相对移动** - 从当前位置移动
- ✅ **平滑移动** - 自然、拟人的鼠标路径
- ✅ **点击类型** - 左键、右键、中键、双击、三击
- ✅ **拖放操作** - 从 A 点拖动到 B 点
- ✅ **滚动** - 垂直和水平滚动
- ✅ **位置追踪** - 获取当前鼠标坐标

### 键盘控制
- ✅ **文本输入** - 快速、准确的文本输入
- ✅ **快捷键** - 执行键盘快捷键（Ctrl+C、Win+R 等）
- ✅ **特殊按键** - Enter、Tab、Escape、方向键、F 键
- ✅ **组合键** - 多键同时按下
- ✅ **按住与释放** - 手动控制按键状态
- ✅ **输入速度** - 可配置的 WPM（从瞬间到拟人化）

### 屏幕操作
- ✅ **截图** - 捕获整个屏幕或指定区域
- ✅ **图像识别** - 在屏幕上查找元素（通过 OpenCV）
- ✅ **颜色检测** - 获取指定坐标的像素颜色
- ✅ **多显示器** - 支持多个显示器

### 窗口管理
- ✅ **窗口列表** - 获取所有打开的窗口
- ✅ **激活窗口** - 将窗口置于前台
- ✅ **窗口信息** - 获取位置、大小、标题
- ✅ **最小化/最大化** - 控制窗口状态

### 安全特性
- ✅ **故障保护** - 将鼠标移到角落以中止
- ✅ **暂停控制** - 紧急停止机制
- ✅ **批准模式** - 操作前需要确认
- ✅ **边界检查** - 防止超出屏幕的操作
- ✅ **日志记录** - 追踪所有自动化操作

---

## 🚀 快速开始

### 安装

首先，安装所需的依赖：

```bash
pip install pyautogui pillow opencv-python pygetwindow
```

### 基本使用

```python
from skills.desktop_control import DesktopController

# 初始化控制器
dc = DesktopController(failsafe=True)

# 鼠标操作
dc.move_mouse(500, 300)  # 移动到坐标
dc.click()  # 在当前位置左键点击
dc.click(100, 200, button="right")  # 在指定位置右键点击

# 键盘操作
dc.type_text("Hello from OpenClaw!")
dc.hotkey("ctrl", "c")  # 复制
dc.press("enter")

# 屏幕操作
screenshot = dc.screenshot()
position = dc.get_mouse_position()
```

---

## 📋 完整 API 参考

### 鼠标函数

#### `move_mouse(x, y, duration=0, smooth=True)`
将鼠标移动到绝对屏幕坐标。

**参数：**
- `x` (int): X 坐标（距离左边的像素数）
- `y` (int): Y 坐标（距离顶部的像素数）
- `duration` (float): 移动时间（秒）（0 = 瞬间，0.5 = 平滑）
- `smooth` (bool): 使用贝塞尔曲线进行自然移动

**示例：**
```python
# 瞬间移动
dc.move_mouse(1000, 500)

# 平滑的 1 秒移动
dc.move_mouse(1000, 500, duration=1.0)
```

#### `move_relative(x_offset, y_offset, duration=0)`
相对于当前位置移动鼠标。

**参数：**
- `x_offset` (int): 水平移动像素（正数 = 向右）
- `y_offset` (int): 垂直移动像素（正数 = 向下）
- `duration` (float): 移动时间（秒）

**示例：**
```python
# 向右移动 100px，向下移动 50px
dc.move_relative(100, 50, duration=0.3)
```

#### `click(x=None, y=None, button='left', clicks=1, interval=0.1)`
执行鼠标点击。

**参数：**
- `x, y` (int, 可选): 点击坐标（None = 当前位置）
- `button` (str): 'left'、'right'、'middle'
- `clicks` (int): 点击次数（1 = 单击，2 = 双击）
- `interval` (float): 多次点击之间的延迟

**示例：**
```python
# 简单左键点击
dc.click()

# 在指定位置双击
dc.click(500, 300, clicks=2)

# 右键点击
dc.click(button='right')
```

#### `drag(start_x, start_y, end_x, end_y, duration=0.5, button='left')`
拖放操作。

**参数：**
- `start_x, start_y` (int): 起始坐标
- `end_x, end_y` (int): 结束坐标
- `duration` (float): 拖动持续时间
- `button` (str): 使用的鼠标按键

**示例：**
```python
# 将文件从桌面拖到文件夹
dc.drag(100, 100, 500, 500, duration=1.0)
```

#### `scroll(clicks, direction='vertical', x=None, y=None)`
滚动鼠标滚轮。

**参数：**
- `clicks` (int): 滚动量（正数 = 向上/向左，负数 = 向下/向右）
- `direction` (str): 'vertical' 或 'horizontal'
- `x, y` (int, 可选): 滚动位置

**示例：**
```python
# 向下滚动 5 次
dc.scroll(-5)

# 向上滚动 10 次
dc.scroll(10)

# 水平滚动
dc.scroll(5, direction='horizontal')
```

#### `get_mouse_position()`
获取当前鼠标坐标。

**返回：** `(x, y)` 元组

**示例：**
```python
x, y = dc.get_mouse_position()
print(f"鼠标位置: {x}, {y}")
```

---

### 键盘函数

#### `type_text(text, interval=0, wpm=None)`
以可配置的速度输入文本。

**参数：**
- `text` (str): 要输入的文本
- `interval` (float): 按键之间的延迟（0 = 瞬间）
- `wpm` (int, 可选): 每分钟字数（覆盖 interval）

**示例：**
```python
# 瞬间输入
dc.type_text("Hello World")

# 拟人化输入，60 WPM
dc.type_text("Hello World", wpm=60)

# 慢速输入，按键间隔 0.1 秒
dc.type_text("Hello World", interval=0.1)
```

#### `press(key, presses=1, interval=0.1)`
按下并释放按键。

**参数：**
- `key` (str): 按键名称（见按键名称部分）
- `presses` (int): 按下次数
- `interval` (float): 按下之间的延迟

**示例：**
```python
# 按 Enter
dc.press('enter')

# 按空格键 3 次
dc.press('space', presses=3)

# 按下箭头键
dc.press('down')
```

#### `hotkey(*keys, interval=0.05)`
执行键盘快捷键。

**参数：**
- `*keys` (str): 要同时按下的按键
- `interval` (float): 按键之间的延迟

**示例：**
```python
# 复制（Ctrl+C）
dc.hotkey('ctrl', 'c')

# 粘贴（Ctrl+V）
dc.hotkey('ctrl', 'v')

# 打开运行对话框（Win+R）
dc.hotkey('win', 'r')

# 保存（Ctrl+S）
dc.hotkey('ctrl', 's')

# 全选（Ctrl+A）
dc.hotkey('ctrl', 'a')
```

#### `key_down(key)` / `key_up(key)`
手动控制按键状态。

**示例：**
```python
# 按住 Shift
dc.key_down('shift')
dc.type_text("hello")  # 输入 "HELLO"
dc.key_up('shift')

# 按住 Ctrl 并点击（用于多选）
dc.key_down('ctrl')
dc.click(100, 100)
dc.click(200, 100)
dc.key_up('ctrl')
```

---

### 屏幕函数

#### `screenshot(region=None, filename=None)`
捕获屏幕或区域。

**参数：**
- `region` (tuple, 可选): (left, top, width, height) 用于部分捕获
- `filename` (str, 可选): 保存图像的路径

**返回：** PIL Image 对象

**示例：**
```python
# 全屏
img = dc.screenshot()

# 保存到文件
dc.screenshot(filename="screenshot.png")

# 捕获特定区域
img = dc.screenshot(region=(100, 100, 500, 300))
```

#### `get_pixel_color(x, y)`
获取指定坐标的像素颜色。

**返回：** RGB 元组 `(r, g, b)`

**示例：**
```python
r, g, b = dc.get_pixel_color(500, 300)
print(f"坐标 (500, 300) 的颜色: RGB({r}, {g}, {b})")
```

#### `find_on_screen(image_path, confidence=0.8)`
在屏幕上查找图像（需要 OpenCV）。

**参数：**
- `image_path` (str): 模板图像路径
- `confidence` (float): 匹配阈值（0-1）

**返回：** `(x, y, width, height)` 或 None

**示例：**
```python
# 在屏幕上查找按钮
location = dc.find_on_screen("button.png")
if location:
    x, y, w, h = location
    # 点击找到的图像中心
    dc.click(x + w//2, y + h//2)
```

#### `get_screen_size()`
获取屏幕分辨率。

**返回：** `(width, height)` 元组

**示例：**
```python
width, height = dc.get_screen_size()
print(f"屏幕: {width}x{height}")
```

---

### 窗口函数

#### `get_all_windows()`
列出所有打开的窗口。

**返回：** 窗口标题列表

**示例：**
```python
windows = dc.get_all_windows()
for title in windows:
    print(f"窗口: {title}")
```

#### `activate_window(title_substring)`
通过标题将窗口置于前台。

**参数：**
- `title_substring` (str): 要匹配的窗口标题部分

**示例：**
```python
# 激活 Chrome
dc.activate_window("Chrome")

# 激活 VS Code
dc.activate_window("Visual Studio Code")
```

#### `get_active_window()`
获取当前焦点窗口。

**返回：** 窗口标题（str）

**示例：**
```python
active = dc.get_active_window()
print(f"活动窗口: {active}")
```

---

### 剪贴板函数

#### `copy_to_clipboard(text)`
将文本复制到剪贴板。

**示例：**
```python
dc.copy_to_clipboard("Hello from OpenClaw!")
```

#### `get_from_clipboard()`
从剪贴板获取文本。

**返回：** str

**示例：**
```python
text = dc.get_from_clipboard()
print(f"剪贴板内容: {text}")
```

---

## ⌨️ 按键名称参考

### 字母键
`'a'` 到 `'z'`

### 数字键
`'0'` 到 `'9'`

### 功能键
`'f1'` 到 `'f24'`

### 特殊键
- `'enter'` / `'return'`
- `'esc'` / `'escape'`
- `'space'` / `'spacebar'`
- `'tab'`
- `'backspace'`
- `'delete'` / `'del'`
- `'insert'`
- `'home'`
- `'end'`
- `'pageup'` / `'pgup'`
- `'pagedown'` / `'pgdn'`

### 方向键
- `'up'` / `'down'` / `'left'` / `'right'`

### 修饰键
- `'ctrl'` / `'control'`
- `'shift'`
- `'alt'`
- `'win'` / `'winleft'` / `'winright'`
- `'cmd'` / `'command'`（Mac）

### 锁定键
- `'capslock'`
- `'numlock'`
- `'scrolllock'`

### 标点符号
- `'.'` / `','` / `'?'` / `'!'` / `';'` / `':'`
- `'['` / `']'` / `'{'` / `'}'`
- `'('` / `')'`
- `'+'` / `'-'` / `'*'` / `'/'` / `'='`

---

## 🛡️ 安全特性

### 故障保护模式

将鼠标移到屏幕的**任意角落**以中止所有自动化操作。

```python
# 启用故障保护（默认启用）
dc = DesktopController(failsafe=True)
```

### 暂停控制

```python
# 暂停所有自动化操作 2 秒
dc.pause(2.0)

# 检查是否可以安全继续自动化
if dc.is_safe():
    dc.click(500, 500)
```

### 批准模式

操作前需要用户确认：

```python
dc = DesktopController(require_approval=True)

# 这将请求确认
dc.click(500, 500)  # 提示: "Allow click at (500, 500)? [y/n]"
```

---

## 🎨 高级示例

### 示例 1：自动填充表单

```python
dc = DesktopController()

# 点击姓名字段
dc.click(300, 200)
dc.type_text("John Doe", wpm=80)

# Tab 到下一个字段
dc.press('tab')
dc.type_text("john@example.com", wpm=80)

# Tab 到密码字段
dc.press('tab')
dc.type_text("SecurePassword123", wpm=60)

# 提交表单
dc.press('enter')
```

### 示例 2：截图区域并保存

```python
# 捕获特定区域
region = (100, 100, 800, 600)  # left, top, width, height
img = dc.screenshot(region=region)

# 使用时间戳保存
import datetime
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
img.save(f"capture_{timestamp}.png")
```

### 示例 3：多文件选择

```python
# 按住 Ctrl 并点击多个文件
dc.key_down('ctrl')
dc.click(100, 200)  # 第一个文件
dc.click(100, 250)  # 第二个文件
dc.click(100, 300)  # 第三个文件
dc.key_up('ctrl')

# 复制选定的文件
dc.hotkey('ctrl', 'c')
```

### 示例 4：窗口自动化

```python
# 激活计算器
dc.activate_window("Calculator")
time.sleep(0.5)

# 输入计算
dc.type_text("5+3=", interval=0.2)
time.sleep(0.5)

# 截图结果
dc.screenshot(filename="calculation_result.png")
```

### 示例 5：拖放文件

```python
# 将文件从源位置拖到目标位置
dc.drag(
    start_x=200, start_y=300,  # 文件位置
    end_x=800, end_y=500,       # 文件夹位置
    duration=1.0                 # 平滑的 1 秒拖动
)
```

---

## ⚡ 性能提示

1. **使用瞬间移动**以提高速度：`duration=0`
2. **批量操作**而不是单独调用
3. **缓存屏幕位置**而不是重新计算
4. **禁用故障保护**以获得最大性能（谨慎使用）
5. **使用快捷键**而不是菜单导航

---

## ⚠️ 重要说明

- **屏幕坐标**从左上角的 (0, 0) 开始
- **多显示器设置**可能为辅助显示器提供负坐标
- **Windows DPI 缩放**可能影响坐标精度
- **故障保护角落**是：(0,0)、(width-1, 0)、(0, height-1)、(width-1, height-1)
- **某些应用程序**可能阻止模拟输入（游戏、安全应用）

---

## 🔧 故障排除

### 鼠标未移动到正确位置
- 检查 DPI 缩放设置
- 验证屏幕分辨率是否符合预期
- 使用 `get_screen_size()` 确认尺寸

### 键盘输入不工作
- 确保目标应用程序有焦点
- 某些应用需要管理员权限
- 尝试增加 `interval` 以提高可靠性

### 故障保护意外触发
- 增加屏幕边框容差
- 正常使用时将鼠标移离角落
- 如需要可禁用：`DesktopController(failsafe=False)`

### 权限错误
- 以管理员权限运行 Python 以执行某些操作
- 某些安全应用程序阻止自动化

---

## 📦 依赖

- **PyAutoGUI** - 核心自动化引擎
- **Pillow** - 图像处理
- **OpenCV**（可选）- 图像识别
- **PyGetWindow** - 窗口管理

全部安装：
```bash
pip install pyautogui pillow opencv-python pygetwindow
```

---

**为 OpenClaw 构建** - 终极桌面自动化伴侣 🦞
