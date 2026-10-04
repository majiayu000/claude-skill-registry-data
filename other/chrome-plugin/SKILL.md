---
name: chrome-plugin
description: 无 CDP 检查并安装项目内置 Chrome unpacked 插件。BrowserWorker 是操控浏览器工具，必须安装。必须先检查目标插件；已安装时立即成功返回，不启动或关闭 Chrome。默认目标是 BrowserWorker，也可安装 1688 插件。Windows 未安装时优先用 pywinauto，macOS 未安装时打开 chrome://extensions/ 并引导用户手动加载。
title: Chrome 插件安装
example: 打开 sandbox Chrome 的扩展页，安装 BrowserWorker 或 1688 插件，后续启动不要带 CDP。
version: 1.1.2
---

# Chrome 插件安装

本技能用于把当前安装环境中的项目内置 unpacked Chrome 插件安装到 sandbox Chrome profile。它不调用 CDP `Extensions.loadUnpacked`。

> [!IMPORTANT]
> **BrowserWorker 是系统的操控浏览器工具，必须安装。** 没有安装 BrowserWorker 插件时，自动化浏览器操控功能将无法正常工作。

关键原则：**插件路径必须由脚本在当前运行环境解析，不得向用户展示开发机硬编码路径**。安装环境下真实路径可能是用户目录里的 `.manai_worker/storage/tools/...`，不是开发目录。

当前内置插件别名：

- `browserworker` -> `BrowserWorker-extension`
- `1688` -> `1688-extension`

## 强制前置检查

处理任何目标插件前，必须先执行对应的 `run.py check`，不得直接执行 `open` 或 `install`：

```bash
# BrowserWorker
python3 {baseDir}/run.py check

# 1688
python3 {baseDir}/run.py check --extension-name 1688

# 自定义插件目录
python3 {baseDir}/run.py check --extension "/actual/install/storage/tools/target-extension"
```

根据命令输出中的 `success` 分支处理：

- `success: true`：目标插件已经安装并启用。立即向用户返回成功并结束任务。
- 已安装成功后，禁止继续执行 `run.py open`、`run.py install` 或任何带 `--close-existing` 的命令。
- 已安装成功后，不得再次打开 `chrome://extensions/`，不得关闭或重启 sandbox Chrome，也不得输出人工安装指引。
- `success: false`：只有此时才进入后续平台安装流程。

`run.py install` 内部也包含相同的已安装短路检查：如果插件已经加载，会直接返回 `success: true` 和 `Chrome extension is already loaded in this profile.`，不会启动或关闭 Chrome。

## 触发条件

当用户提出以下需求时使用本技能：

- “不要 CDP，安装 Chrome 插件”
- “安装 BrowserWorker 插件”
- “安装 1688 插件”
- “打开 chrome://extensions 加载插件”
- “Windows 自动点击安装插件”
- “macOS 引导用户手动加载插件”
- “一次加载后后续启动保留插件”

## 策略

- 所有平台：第一步必须检查目标插件，已安装时立即成功返回。
- Windows：只使用 `pywinauto` 识别 ManAI Profile 的 Chrome 窗口并导航到 `chrome://extensions/`。不得自动点击开发者模式、“加载已解压”或文件选择器；页面打开后立即停止工具操作并让用户手动安装。
- macOS：不采用自动点击方案。脚本只负责打开 sandbox Chrome 到 `chrome://extensions/` 并输出人工指引。
- 自动失败：降级为人工引导，不要反复盲点坐标。
- 安装后：用 `run.py check` 读取 profile 的 `Default/Preferences` 和 `Default/Secure Preferences` 检查插件是否已加载。

## 命令

检查默认插件 BrowserWorker：

```bash
python3 {baseDir}/run.py check
```

打开 sandbox Chrome 到扩展页，并输出人工引导：

```bash
python3 {baseDir}/run.py open --close-existing
```

安装默认插件 BrowserWorker：

```bash
python3 {baseDir}/run.py install --close-existing
```

安装 1688 插件：

```bash
python3 {baseDir}/run.py install --extension-name 1688 --close-existing
```

只输出人工安装指引：

```bash
python3 {baseDir}/run.py guide
python3 {baseDir}/run.py guide --extension-name 1688
```

指定其它插件目录：

```bash
python3 {baseDir}/run.py install --extension "/actual/install/storage/tools/BrowserWorker-extension"
```

## 路径解析

脚本解析顺序：

1. 优先导入项目 `gui_src/gui_utils/path_manager.py` 的 `PathManager`。
2. 使用 `PathManager.sand_profile_dir` 作为 profile。
3. 默认使用 `PathManager.tools_dir / "BrowserWorker-extension"` 作为插件目录。
4. 指定 `--extension-name 1688` 时使用 `PathManager.tools_dir / "1688-extension"`。
5. 如果无法导入 `PathManager`，再按 `MANAI_WORKSPACE_ROOT` / `MANAI_HOME` / 当前工作区回退到 `storage/tools`。

Agent 不要自己拼开发环境路径；必须使用脚本输出里的 `extension` 字段或 `guide` 文本里的路径。

## Windows 自动安装

Windows 自动方案需要 `pywinauto`。流程：

1. 启动 Google Chrome，不带 CDP，不带 `--load-extension`，指定 sandbox profile。
2. 只选择命令行包含 sandbox profile 的 Chrome 窗口，禁止操作用户日常 Chrome。
3. 用 UI Automation 聚焦地址栏，输入并打开 `chrome://extensions/`。
4. 检测到开发者模式或“加载已解压”控件后，立即返回 `manual_required: true`、`page_opened: true` 和插件目录。
5. Agent 展示人工安装步骤后立即结束任务，不得点击页面、不得操作文件选择器、不得再次执行安装命令。
   - `Enter`
   - 再 `Enter` 或点击“选择文件夹”
6. 读取 profile 偏好确认插件已安装。

如果 `pywinauto` 未安装、找不到按钮、找不到文件夹选择器，立即输出人工引导。

Windows 人工引导方式：

1. 在已打开的 Chrome 进入 `chrome://extensions/`。
2. 打开 `Developer mode` / `开发者模式`。
3. 点击 `Load unpacked` / `加载已解压的扩展程序`。
4. 文件夹选择器弹出后按 `Alt+D`。
5. 粘贴脚本输出的插件路径。
6. 回车，再回车确认。

## macOS 降级方案

macOS 不做自动点击，因为无辅助功能权限时 pyautogui 能移动鼠标但点击可能不会被 Chrome WebUI 接收。脚本只打开 sandbox Chrome 到 `chrome://extensions/` 并输出路径。

macOS 人工引导方式：

1. 在已打开的 Chrome 进入 `chrome://extensions/`。
2. 打开“开发者模式”。
3. 点击“加载未打包的扩展程序”。
4. 文件选择器弹出后，点击文件选择器窗口，让它获得焦点。
5. 按 `Command+Shift+G`。
6. 粘贴脚本输出的插件路径。
7. 回车，再回车确认。

注意：`Command+Shift+G` 不是文件选择器里的可见按钮；它会打开“前往文件夹”的路径输入框。

## Agent 处理规则

- 先执行 `run.py check`；安装 1688 时执行 `run.py check --extension-name 1688`。
- 如果 `check` 返回 `success: true`，直接告诉用户目标插件已安装并立即结束；不得继续调用任何安装、打开、关闭或重启 Chrome 的命令。
- 如果未安装：
  - Windows 执行 `run.py install --close-existing`，安装 1688 时加 `--extension-name 1688`。terminal 外层 timeout 至少设置 30 秒。命令返回 `manual_required: true` 后，向用户显示插件目录并立即结束，不得重试或继续点击。
  - macOS 执行 `run.py open --close-existing`，安装 1688 时加 `--extension-name 1688`，然后把输出里的 manual guide 告诉用户。
- 用户完成手动加载后，再执行对应 `run.py check`。
- 不要提示用户使用开发环境路径；只使用脚本输出的 `extension` 路径。
- 不要用 CDP 作为本技能的安装方式。
- 不要修改 BrowserWorker 或 1688 插件源码。
- 不要在网站登录、验证码、滑块上做绕过；遇到安全验证让用户人工处理。
