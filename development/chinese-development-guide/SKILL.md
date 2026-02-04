---
name: Chinese Development Guide
description: 为中文开发者提供完整的项目本地化、环境配置和开发工作流指导，确保中英文双语环境下的最佳开发体验
version: 1.0.0
---

# 中文开发指南技能

## 指令

当用户是中文开发者或需要中文环境支持时，自动提供本地化配置和开发指导。

## 触发条件
- 用户使用中文进行交流
- 询问中文相关的配置问题
- 需要中文化支持或本地化设置

## 核心配置

### 1. 系统环境配置
```bash
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8
```

### 2. Git中文配置
```bash
git config --global i18n.commitencoding utf-8
git config --global core.quotepath false
```

### 3. VS Code中文化
```json
{
  "files.encoding": "utf8",
  "editor.fontFamily": "'Microsoft YaHei', monospace"
}
```

## 中文开发规范
- 文件使用UTF-8编码
- 变量和函数使用中文命名
- 注释使用中文说明
- 测试用例中文描述

## 常见问题解决
- 字符编码问题
- 中文字体显示
- 输入法支持
