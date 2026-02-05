---
name: install-app
description: 帮助用户在 macOS 上安装软件，自动处理 Homebrew 依赖。Use when user wants to install, 安装, 下载软件, 装一个, 帮我装, 我想安装, 如何安装 apps on macOS.
---

# Install App Skill

## 目标

帮助没有编程经验的用户在 macOS 上轻松安装软件。

## 执行步骤

### 1. 确认用户需求

首先友好地确认用户想要安装什么软件。如果用户没有明确说明，询问他们：
- 想安装什么软件？
- 软件的用途是什么？（帮助推荐正确的安装包）

### 2. 检查 Homebrew 是否已安装

运行以下命令检查：

```bash
which brew
```

### 3. 如果没有 Homebrew，先安装它

**重要**：在安装前，用简单易懂的语言向用户解释：
- Homebrew 是 macOS 上最流行的软件包管理器
- 它可以帮助你轻松安装和管理各种软件
- 安装过程可能需要几分钟，请耐心等待

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

安装脚本会先解释将要执行的操作，然后暂停等待用户确认后再继续。

**安装后配置**（针对 Apple Silicon Mac）：

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### 4. 配置国内镜像源（加速下载）

向用户解释：
- 默认的 Homebrew 服务器在国外，下载速度可能很慢
- 配置国内镜像源可以大幅提升下载速度
- 使用的是中国科学技术大学 (USTC) 的镜像，稳定可靠

将以下配置添加到 shell 配置文件：

```bash
cat >> ~/.zprofile << 'EOF'

# Homebrew 中科大镜像源
export HOMEBREW_API_DOMAIN="https://mirrors.ustc.edu.cn/homebrew-bottles/api"
export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.ustc.edu.cn/homebrew-bottles"
export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.ustc.edu.cn/brew.git"
export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.ustc.edu.cn/homebrew-core.git"
EOF
```

然后使配置生效：

```bash
source ~/.zprofile
```

### 5. 搜索软件包

帮用户搜索正确的软件包名称：

```bash
brew search <软件名>
```

向用户解释搜索结果，帮助他们选择正确的包：
- **Formulae**：命令行工具
- **Casks**：图形界面应用程序（大多数用户需要的）

### 6. 安装软件

根据软件类型使用正确的命令：

**图形界面应用（Cask）**：
```bash
brew install --cask <软件名>
```

**命令行工具（Formula）**：
```bash
brew install <软件名>
```

### 7. 验证安装

安装完成后，帮助用户验证：
- 对于 Cask 应用：告诉用户可以在「应用程序」文件夹或 Launchpad 中找到
- 对于命令行工具：运行 `which <工具名>` 或 `<工具名> --version`

### 8. 常见问题处理

**如果安装失败**：
- 检查网络连接
- 尝试 `brew update` 更新 Homebrew
- 尝试 `brew doctor` 诊断问题

**如果需要密码**：
- 向用户解释这是 macOS 的安全机制
- 输入的是他们的 Mac 登录密码
- 输入时不会显示任何字符，这是正常的

## 常用软件快速参考

| 软件 | 安装命令 |
|------|----------|
| Chrome | `brew install --cask google-chrome` |
| VS Code | `brew install --cask visual-studio-code` |
| WeChat | `brew install --cask wechat` |
| QQ | `brew install --cask qq` |
| Notion | `brew install --cask notion` |
| Slack | `brew install --cask slack` |
| Zoom | `brew install --cask zoom` |
| VLC | `brew install --cask vlc` |
| Rectangle | `brew install --cask rectangle` |
| 1Password | `brew install --cask 1password` |

## 交互风格

- 使用简单友好的语言，避免技术术语
- 每一步都解释「为什么」要这样做
- 如果遇到错误，用通俗的语言解释并提供解决方案
- 安装完成后给予积极的反馈
