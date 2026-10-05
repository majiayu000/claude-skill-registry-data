---
name: self-media-wechat-publisher
description: 把已确认的公众号终稿 Markdown 排版并写入微信公众号草稿箱。用于用户说"发布到公众号、写入草稿箱、公众号排版、换个排版主题、发小绿书图片消息"等场景。自动上传封面与文内图片，支持多主题与自定义 CSS、多账号和 server 模式。只创建草稿不群发，凭据只通过环境变量提供，未安装适配工具时交付手动发布包。
---

# 公众号发布

## 目标

把确认过的公众号终稿 Markdown 排版成平台原生富文本，连同封面和文内图片写入公众号草稿箱。只创建草稿，从不群发。

## 适配层说明

本模块是公众号渠道的发布适配层，基于开源工具 [wenyan CLI](https://github.com/caol64/wenyan-cli)（Apache-2.0）。wenyan 不可用时不阻塞创作流程，按 `self-media-content-delivery` 交付手动发布包。

## 前置检测

1. `wenyan --version` 确认安装。未安装时提示 `npm install -g @wenyan-md/cli`，用户不想安装则直接交付手动发布包。
2. 确认 `WECHAT_APP_ID` 和 `WECHAT_APP_SECRET` 环境变量存在。只判断存在性，不读取、不回显、不写入任何文件。
3. 首次发布前确认运行机器 IP 已加入公众号后台白名单。IP 频繁变动或团队协作场景使用 server 模式，见 [wenyan-setup.md](references/wenyan-setup.md)。

## 输入契约

文章顶部必须有 frontmatter：`title` 必填；`cover` 为本地或网络路径，缺省时自动取正文第一张图；`author` 和 `source_url` 可选。文内图片支持本地绝对路径、相对路径和网络地址，发布时自动上传公众号素材库。模板见 [wechat-article-template.md](assets/wechat-article-template.md)。

小绿书图片消息：frontmatter 设 `type: image` 自动提取正文全部图片，或手动列出 `image_list`。最多 20 张，首图即封面。

## 主题选择

1. 优先读取账号风格档案中的默认排版主题。
2. 没有默认主题或用户要求换风格时，用当前文章渲染候选主题生成本地预览（`wenyan render -f 文章.md -t 主题`），让用户对比选择。
3. 用户选定后写入账号风格档案，后续沿用，不重复询问。
4. 需要品牌化排版时用 `-c` 加载自定义 CSS 主题。

## 发布流程

两层授权缺一不可：终稿确认，加上草稿箱写入授权。

1. 核对 frontmatter 完整、封面可用、文内图片路径全部有效。
2. `wenyan render` 本地渲染，确认无乱码、代码块和表格可读。
3. `wenyan publish -f 文章.md -t 主题 -h 高亮主题` 写入草稿箱。
4. 提醒用户在公众号后台打开草稿，核对标题、封面、前两段、图片数量和外链。
5. 把草稿创建时间、使用主题和核对结果写回任务卡。

发布失败时按 [wenyan-setup.md](references/wenyan-setup.md) 排查。同一错误不盲目重试超过一次，凭据类问题交给用户处理。

## 多账号

发布到多个公众号时，改用 wenyan 的凭据配置管理多账号，publish 时加 `--app-id` 指定。每个账号都需要独立配置 IP 白名单。

## 安全边界

- 只写草稿箱，不调用群发接口。
- 凭据只通过环境变量或 wenyan 凭据配置提供，不写入任务卡、文章、日志或仓库。
- 命令输出中出现 token 或密钥片段时不记录、不转述。
- 发布接口报错、白名单拦截或凭据失效时立即停止并交给用户。

## 输出

返回：草稿标题、使用主题、封面来源、图片数量、草稿创建时间和需要人工核对的清单。
