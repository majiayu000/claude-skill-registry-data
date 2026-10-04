---
name: cm-miniprogram-engineer
description: 微信小程序开发工程师 Skill，执行小程序开发任务，自动适配项目技术栈（原生小程序/Taro/uni-app 等），支持 Figma/Stitch 设计稿还原与云开发
---

# cm-miniprogram-engineer — 微信小程序开发工程师

执行微信小程序开发任务。自动识别项目技术栈，遵循项目 `.claude/rules/` 中的规范。

涉及账号主体、类目、支付/广告、权限、云能力或首次发布准备时，读取
`references/platform-readiness.md`；执行 feature 完成 QA、真机走查或发布准备时，
读取 `references/release-checklist.md`。平台规则属于易变外部事实，按参考文件在当前
官方文档/后台查证，不把固定门槛或社区经验当作长期规则。

## 触发条件

由 `/cm-ai` 自动调用，当 task 涉及微信小程序开发时触发。

## 工作流程

### 0. 设计稿检查

开发前先读取已审批 design.md 的「设计基准」及 `design-baseline/`：

- 已明确“无设计稿/无基准，按 design.md 自行实现” → 直接开发，**不得重复询问**
- **有 Figma 链接** → 调用 figma mcp
- **有 Stitch 项目** → 调用 stitch mcp
- 只有设计基准字段缺失、链接与落盘基准不一致、或 specs 内信息**规格缺失或互相矛盾**
  时才暂停询问；新输入会改变批准方案时停止并要求 `$cm-prd --change`，不在 N3 临时改规格

**设计稿与业务的关系：**

- 设计稿存在且完整 → 按设计稿还原
- 设计稿存在但不是明显的缺失 → 自行补全功能
- 设计稿存在但与业务需求有明显差距或缺失页面 → **主动询问用户**是否需要先还原设计稿再开发功能，等待用户回复后再继续
- 已审批为没有设计稿 → 根据 design.md 和业务需求自行实现

### 1. 识别技术栈

读取项目配置自动判断，不做硬编码假设：

- `project.config.json` / `project.private.config.json` → 项目类型、appid、编译配置
- `app.json` → 页面路由、分包配置、tabBar、窗口表现、原生组件
- `package.json`（如存在）→ 跨端框架（Taro / uni-app / mpvue / Remax...）、构建工具、依赖
- 框架判断 → 原生小程序（WXML/WXSS/JS/JSON）还是跨端框架（Taro = React 语法、uni-app = Vue 语法）
- 是否启用 **云开发**（`cloudfunctions/` 目录、`wx.cloud`）

识别为微信小程序后记录 `DELIVERY_SHAPE=wechat-miniprogram`。平台就绪项缺失但只影响
后续提审时允许继续本地开发并保留待决；功能本身依赖未确认的平台能力时 `BLOCKED`，
不得用假 AppID、假资质或 Web target 绕过。

### 2. 读取上下文

- `.claude/rules/miniprogram.md`、`.claude/rules/coding-style.md`（如存在）
- design.md 中当前任务相关的模块设计
- 扫描 `pages/`、`components/` 了解现有页面与组件结构和命名规律
- **重点扫描项目已有的自定义组件库**（`components/`、`miniprogram/components/` 等），了解哪些组件已封装可复用
- 查看 `app.json` 的 `usingComponents`、是否引入第三方 UI 库（Vant Weapp / TDesign / WeUI / ColorUI）

### 3. 开发

**组件封装与复用（重要）：**

- 开发前先检查项目已有的自定义组件，能复用的绝不重写
- 新建通用组件用 `Component` 构造器，放入项目约定的公共组件目录，并在 `usingComponents` 中按需引入
- 业务组件和基础 UI 组件分层：基础组件不含业务逻辑，业务页面组合基础组件
- 如果项目引入了第三方组件库（Vant Weapp / TDesign 小程序版 / WeUI 等），优先用库内组件，不自己造轮子

**样式（WXSS）：**

- 尺寸优先用 **rpx** 做多机型适配（750rpx = 屏幕宽度），避免写死 px
- 颜色、圆角、间距等通过 WXSS 变量或公共样式文件统一管理，不硬编码具体值
- 复用样式通过 `@import` 公共样式或组件封装，而非到处复制
- 注意小程序 WXSS **不支持** 部分 CSS 选择器（如 `*`、属性选择器有限），用 class 选择器为主

**页面与组件开发：**

- 页面用 `Page({})`，组件用 `Component({})`，遵循项目已有模式
- 生命周期：页面 `onLoad/onShow/onReady/onHide/onUnload`，组件 `lifetimes.attached/ready/detached`
- `data` 更新统一走 `setData`，**只更新变化的字段**，避免一次性 setData 大对象
- properties / observers / 事件命名跟随项目约定，文件命名（page/component 四件套 `.wxml/.wxss/.js/.json`）跟随项目已有规律

**状态管理：**

- 识别项目使用的方案（`globalData` / mobx-miniprogram / Taro 用 Redux·Zustand / uni-app 用 Vuex·Pinia）
- 简单局部状态用页面/组件原生 `data`
- 跨页面共享参考 design.md 中的状态流转设计

**数据请求：**

- 原生：`wx.request`（封装统一的 request 工具，处理 baseURL、token、loading、错误）
- 云开发：云函数 `wx.cloud.callFunction`、云数据库 `db.collection()`
- 基于 design.md 中的接口契约；后端未就绪 → 先写 mock，标注 `// TODO: replace mock when API ready`
- 统一处理错误提示（`wx.showToast`）和 loading 状态（`wx.showLoading`）

**路由与导航：**

- 页面注册在 `app.json` 的 `pages`，tabBar 页面用 `wx.switchTab`，普通页面 `wx.navigateTo`/`wx.redirectTo`/`wx.navigateBack`
- 页面栈最多 10 层，注意深层跳转改用 redirect
- 参数通过 query 传递（`navigateTo({url:'/pages/x?id=1'})`），大对象用全局或本地缓存

**登录与授权：**

- 登录走 `wx.login` 拿 code → 后端换 openid/session；用户信息用 `wx.getUserProfile`（需用户点击触发）
- 手机号、位置等敏感权限走对应的 `open-type` 按钮或 `wx.authorize`，处理拒绝授权的兜底

### 4. 验证

```bash
# 跨端框架（如项目使用）按实际命令执行
npm run lint
npm run build:weapp   # Taro 示例；uni-app 为 npm run dev:mp-weixin
```

- 原生小程序：在**微信开发者工具**中编译，确认无报错、页面渲染正常
- 检查 **真机预览**（部分 API 与样式在真机和模拟器表现不同）
- 读取项目配置与微信官方当前限制核对包体积；超限时配置分包、压缩资源或移至 CDN
- 按 `references/release-checklist.md` 选择本 feature 相关专项；Web/H5 预览不得冒充
  微信开发者工具或真机证据。工具、扫码或账号权限不可用时如实标记 `BLOCKED`/待人工

## 常见坑

| 问题                                   | 处理                                                                     |
| -------------------------------------- | ------------------------------------------------------------------------ |
| setData 频繁/数据量大导致卡顿          | 只 setData 变化字段，避免在循环/滚动中高频调用，长列表用虚拟列表         |
| px 写死导致机型适配错乱                | 改用 rpx，必要时结合 `wx.getSystemInfo` 动态计算                         |
| `getUserProfile` 不触发/拿不到信息     | 必须由用户点击事件直接调用，不能在 onLoad 等生命周期里自动调             |
| 包体积超过当前平台限制                 | 核对官方当前限制，配置 `subpackages`，图片走 CDN，移除未用资源           |
| WXSS 选择器不生效                      | 小程序不支持部分 CSS 选择器，改用 class；组件样式隔离用 `styleIsolation` |
| 自定义组件样式被隔离 / 穿透失败        | 用 `externalClasses` 或 `:host`，跨组件样式用全局类并设置隔离选项        |
| `wx.request` 域名报错                  | 在小程序后台配置合法域名（request/socket/uploadFile/downloadFile）       |
| 组件重复造轮子                         | 开发前先搜索项目已有组件与第三方 UI 库，grep 关键词                      |
| 设计稿颜色/间距与项目 token 不一致     | 扩展公共样式变量而非硬编码 hex 值                                        |
| 跨端框架语法误用（Taro≈React/uni≈Vue） | 先确认框架，按对应语法写，不混用                                         |

## 输出

- 创建/修改的文件列表（含 `.wxml/.wxss/.js/.json` 四件套及 `app.json` 路由变更）
- 验证结果（开发者工具编译 / lint + build）
- 设计稿还原情况（如有设计稿）
- 需要其他工种配合的事项（如后端接口、合法域名配置、云函数部署）
