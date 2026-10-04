---
name: skill-installer
description: 一键安装 cc-use-exp 配置体系到 Codex CLI
trigger: explicit
---

# cc-use-exp Skill 安装器（Codex）

一键安装 cc-use-exp AI 编码助手配置体系到 Codex CLI。

---

## 使用方式

```bash
$skill-installer install https://github.com/doccker/cc-use-exp/.codex/skills/cc-skill-installer
```

或指定 GitHub URL（未来扩展）：

```bash
$skill-installer install https://github.com/doccker/cc-use-exp
```

---

## 执行步骤

### 第 1 步：检查安装状态

```bash
INSTALL_DIR="$HOME/.codex/.cc-use-exp"

if [ -d "$INSTALL_DIR" ]; then
  echo "⚠️  检测到已安装"
  echo ""
  echo "安装位置: $INSTALL_DIR"
  echo ""
  cd "$INSTALL_DIR"
  echo "当前版本:"
  git log -1 --pretty=format:"%h - %s (%ar)" 2>/dev/null || echo "无法获取版本信息"
  echo ""
  echo ""
  echo "是否更新到最新版本？(y/N)"
  read -r response
  if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "❌ 取消安装"
    exit 0
  fi
  echo "🔄 更新现有安装..."
  git pull origin main
else
  echo "📦 开始安装 cc-use-exp..."
  echo ""

  # 创建安装目录
  mkdir -p "$HOME/.codex"

  # Clone 仓库
  git clone https://github.com/doccker/cc-use-exp.git "$INSTALL_DIR"

  if [ $? -ne 0 ]; then
    echo "❌ 克隆失败，请检查网络连接"
    exit 1
  fi

  cd "$INSTALL_DIR"
  echo "✓ 仓库克隆完成"
fi
```

### 第 2 步：执行同步脚本

```bash
echo ""
echo "🔧 同步配置到 Codex..."
echo ""

if [ -f "./tools/sync-config.sh" ]; then
  # 只执行 Codex 部分的同步
  CC_USE_EXP_SYNC_TARGETS=codex ./tools/sync-config.sh
else
  echo "❌ 错误：找不到同步脚本"
  exit 1
fi
```

### 第 3 步：显示安装结果

```bash
echo ""
echo "✅ 安装完成！"
echo ""
echo "📝 已同步配置到："
echo "  - ~/.codex/AGENTS.md（受管区块）"
echo "  - ~/.codex/rules/"
echo "  - ~/.codex/instructions/"
echo "  - ~/.codex/*.config.toml（profiles）"
echo "  - ~/.agents/skills/"
echo ""
echo "🔄 配置已生效，无需重启"
echo ""
echo "💡 后续操作："
echo "  - 更新配置：重新运行 \$skill-installer install"
echo "  - 查看状态：\$cc-status"
echo "  - 卸载：手动删除 $INSTALL_DIR 和上述配置"
echo ""
echo "📖 文档：https://github.com/doccker/cc-use-exp"
```

---

## 错误处理

**网络错误**：
```bash
if ! git clone ...; then
  echo "❌ 网络错误，请检查："
  echo "  1. 网络连接是否正常"
  echo "  2. 是否可以访问 GitHub"
  echo "  3. 是否需要配置代理"
  exit 1
fi
```

**权限错误**：
```bash
if [ ! -w "$HOME/.codex" ]; then
  echo "❌ 权限错误：无法写入 ~/.codex/"
  echo "请检查目录权限"
  exit 1
fi
```

---

## 注意事项

- 安装位置：`~/.codex/.cc-use-exp/`
- 配置同步到：`~/.codex/`、`~/.agents/skills/`
- `AGENTS.md` 使用受管区块合并，profiles 使用独立 `*.config.toml` 文件，不会覆盖用户自定义配置
- 支持重复安装（自动检测并提示更新）

---

## 规则溯源

```
> 📋 本回复遵循：`skill-installer` - cc-use-exp Codex 安装器
```
