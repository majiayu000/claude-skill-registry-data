---
name: hexo-butterfly
description: Hexo Butterfly 主题配置与使用指南，包括主题安装、页面配置、主题配置、标签外挂、FAQ、进阶教程
---

# Hexo Butterfly 主题技能

Butterfly 是一款基于 hexo-theme-melody 的简洁卡片式 Hexo 主题，提供丰富的配置选项和标签外挂功能。

## 触发条件

当用户询问以下内容时激活此技能：
- Hexo Butterfly 主题安装与配置
- Butterfly 主题页面设置（标签页、分类页、友链页等）
- Butterfly 主题配置选项（导航、侧边栏、代码高亮、评论系统等）
- Butterfly 标签外挂用法（Note、Gallery、Tabs、Timeline 等）
- Butterfly 主题常见问题排查
- Butterfly 进阶功能（音乐播放器、图标定制、插件推荐等）

## 快速参考

### 安装主题

```bash
# Git 安装（推荐）
git clone -b master https://github.com/jerryc127/hexo-theme-butterfly.git themes/butterfly

# NPM 安装（Hexo 5.0+）
npm install hexo-theme-butterfly

# 必装渲染器
npm install hexo-renderer-pug hexo-renderer-stylus --save
```

### 应用主题

修改 Hexo 根目录 `_config.yml`：

```yaml
theme: butterfly
```

### 配置文件管理

在 Hexo 根目录创建 `_config.butterfly.yml`，复制主题 `_config.yml` 内容。升级主题时配置不会丢失。

### 常用 Front-Matter

```yaml
---
title: 文章标题
date: 2024-01-01 12:00:00
tags:
  - 标签1
  - 标签2
categories:
  - 分类名
cover: /img/cover.jpg
toc: true
comments: true
---
```

### 创建特殊页面

```bash
# 标签页
hexo new page tags
# 然后设置 type: 'tags'

# 分类页
hexo new page categories
# 然后设置 type: 'categories'

# 友链页
hexo new page link
# 然后设置 type: 'link'
```

### 常用标签外挂

**Note 提示框：**
```markdown
{% note info %}
这是一条信息提示
{% endnote %}
```

**Tabs 选项卡：**
```markdown
{% tabs 选项卡名 %}
<!-- tab 标签1 -->
内容1
<!-- endtab -->
<!-- tab 标签2 -->
内容2
<!-- endtab -->
{% endtabs %}
```

**折叠内容：**
```markdown
{% hideToggle 点击展开 %}
隐藏的内容
{% endhideToggle %}
```

## 参考文档

详细文档位于 `references/` 目录：

- **getting-started.md** - 快速开始：安装、配置、升级
- **pages.md** - 页面配置：Front-Matter、特殊页面、数据管理
- **configuration.md** - 主题配置：导航、侧边栏、代码、评论、统计等
- **tag-plugins.md** - 标签外挂：Note、Gallery、Tabs、Timeline、Mermaid 等
- **faq.md** - 常见问题：渲染错误、配置报错、版本兼容
- **advanced.md** - 进阶教程：音乐播放器、图标定制、插件推荐

## 常见问题速查

| 问题 | 解决方案 |
|------|----------|
| 页面显示代码而非渲染 | `npm install hexo-renderer-pug hexo-renderer-stylus --save` |
| 友链配置报错 | 检查 `link.yml` 的缩进空格 |
| 升级后运行报错 | 检查 `_config.butterfly.yml` 是否缺少新配置项 |
| 部署后样式异常 | 执行 `hexo clean` 清理缓存后重新生成 |
| 字数统计失效 | 安装 `npm install hexo-wordcount --save` |

## 资源链接

- 官方文档：https://butterfly.js.org/
- 主题仓库：https://github.com/jerryc127/hexo-theme-butterfly
