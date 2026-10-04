---
name: wechat-mp-push
description: 支持通过AI生成符合公众号规范的图文（文章和贴图），并推送到公众号草稿箱，兼容其它SKILL生成的图文、图片进行推送。通过配置向导扫码授权，支持多账号。无需泄露公众号Secret密钥，无需配置公众号IP白名单。
---

# wechat-mp-push · 微信公众号图文生成与推送技能

## 文件路径与作用

| 文件                        | 位置                           | 作用                   |
| ------------------------- | ---------------------------- | -------------------- |
| **SKILL.md**              | `wechat-mp-push 目录/` | 本说明                  |
| **design.md**             | 同上                           | HTML格式规范             |
| **config.json**           | 同上                           | 配置向导生成后的真实配置         |
| **config.example.json**   | 同上                           | 字段说明（fieldsHelp）+ 示例 |
| **push-to-wechat-mp.js**  | 同上                           | 推送脚本                 |

---

## 第一步：配置向导

| 项          | 内容                                                                                                                         |
| ---------- | -------------------------------------------------------------------------------------------------------------------------- |
| **配置向导地址** | [https://app.pcloud.ac.cn/design/wechat-mp-push.html](https://app.pcloud.ac.cn/design/wechat-mp-push.html) |
| **流程**     | AI发送配置向导给用户 → 用户微信扫码 → 用户选择推送账号 → 用户复制发给AI                                                                                 |

AI检查在 **wechat-mp-push 目录** 下是否存在 **`config.json`**。如果不存在，则无法使用本技能，AI需要发送配置向导地址给用户扫码授权。

---

## 第二步：配置文件

AI将配置向导得到的配置参数保存为 **wechat-mp-push 目录** 下的 **`config.json`**，编码 **UTF-8**。

在已进入该目录时，可：

```bash
cat > config.json << 'EOF'
{ … 粘贴配置向导 JSON … }
EOF
```

（Windows 可用编辑器在该目录新建 `config.json` 并粘贴）

---

`config.json` 中 **`accounts`** 说明：选平台提供时仅一项平台账号；选自己的公众号时仅为已授权自定义账号列表。

---

## 第三步：写公众号图文

1. 用户发送图文创作要求给AI，AI必须根据 `design.md` 规范生成标准的 HTML 文件。若涉及到文本文章内容生成，AI必须根据 `Humanizer-zh.md` 规范生成文本文章内容，用于去除AI味道。有二种创作类型：
  - **文章**：通用类型，页面默认宽度 677px
  - **贴图**：图文卡片类型（俗称小绿书，类似小红书），页面默认宽度 375px，固定分页比例（默认 3:4）。推送到公众号时， 后台会自动把 HTML 内容转换为图片

2. 生成HTML文件后，若页面中没有引用图片，则需继续根据HTML文件的title生成对应的封面HTML文件：
  - 文件名：`${主HTML文件名}_title.html`
  - 注意：`_title` 是固定常量，不是变量，无论主 HTML 文件名是什么，`_title` 部分均保持固定不变
  - 版式：页面尺寸固定 900×383px，采用信息流栏目头图风格，页面柔和、清爽、现代，不暗沉，不沉重，不压抑，用于微信公众号文章封面；
  - 文案：主题文案视觉居中（水平垂直居中，允许轻微光学微调）；主题文案颜色和背景色需要有反差,避免因主题文案文字颜色与背景相近导致文字看不清；可搭配描边、投影或渐变色提升视觉冲击力；
     
  
**⚠️ 注意：** 不管是创作 **文章** 还是 **贴图** ，必须先阅读 `design.md`，按其规范生成标准的 HTML 文件。后续在推送图文过程中，标准的 HTML 会自动适配公众号格式。封面HTML不需要遵守 `design.md` 规范，请自由发挥

---

## 第四步：推送到公众号

推送方式：`html` 模式传入生成的 HTML 文件（本技能在第三步生成的HTML，也可以是用户或其它技能提供的HTML，非HTML内容可先按 `design.md` 整理成 HTML）；`img` 模式传入公网可访问的图片 URL 数组及标题、正文。**注意** 此模式仅适合用户或其它技能保证所提供的图片可以直接推送，无需本技能基于提供的内容进行创作

### 推送 HTML

AI 调用脚本：首参为目标公众号 AppID，第二参为 `html`，再传与脚本同目录下的 HTML 文件名：

```bash
cd wechat-mp-push
node push-to-wechat-mp.js targetAppId html 你的文件.html
```

### 推送图片链接

AI 调用脚本：首参为目标公众号 AppID，第二参为 `img`，第三参为**图片链接的 JSON 数组字符串**（整段一个参数；Bash 与 PowerShell 都可用单引号包住整段 JSON，例如 `'["https://...","https://..."]'`）。再依次传标题、正文。


```bash
cd wechat-mp-push
node push-to-wechat-mp.js targetAppId img '["https://cdn.example.com/1.png","https://cdn.example.com/2.png"]' "标题" "正文"
```

**标题、正文**（命令行各一个参数，含空格时用英文双引号）：标题和正文可为空。

### 说明
**目标公众号 AppID**：若用户未声明具体要发送的公众号，则选择 `config.json` 中 `accounts` 中 `selected: true` 的账号。
- **接口说明**（供查阅）：请求地址为 `config.json` 中的 `apiBase`（缺省 `https://api.pcloud.ac.cn/openClawService`），**POST**、`Content-Type: application/json`，Body 含 `action: sendToWechat`、`openId`、`title`、`content`；`img` 模式另含 `imgUrls`；推送到自定义公众号时 Body 含 `appId`。
- **超时说明**：推送链路较长，若返回「超时」可视为已成功，勿重复狂推；请用户看服务通知或草稿箱。

## 其它功能

### 清空草稿箱 

发送 POST 请求，`https://api.pcloud.ac.cn/openClawService`，传参数：

```json
{
  "action": "cleanupDrafts",
  "openId": "",
  "appId": ""
}
```
- **超时说明**：草稿箱图文可能较多，若返回「超时」可视为已成功；请用户看在公众号中查看草稿箱情况。