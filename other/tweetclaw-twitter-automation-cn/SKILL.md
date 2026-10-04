---
name: tweetclaw-twitter-automation-cn
description: "指导 Agent 使用 TweetClaw 执行已获用户批准的 X/Twitter 自动化，包括推文抓取、回复搜索、粉丝导出、用户查询、媒体、私信、监控、Webhook、抽奖，以及确认后发帖或回复。"
---

# TweetClaw Twitter 自动化

当用户希望 Agent 通过 Xquik 或 TweetClaw OpenClaw 插件处理 X/Twitter 工作流时，使用此 Skill。

## 使用场景

用户提出以下需求时使用：
- 抓取推文、长帖、回复、引用、提及、点赞或媒体
- 搜索推文或推文回复
- 查询用户、粉丝、关注列表或认证粉丝
- 在用户批准后发推、回复推文或上传媒体
- 在账号授权后读取或发送私信
- 创建监控、Webhook 或抽奖
- 判断哪个 TweetClaw 或 Xquik 端点适合当前任务

## 不要使用

不要将此 Skill 用于：
- 垃圾信息、骚扰、欺骗性互动、冒充身份或规避平台规则
- 大量未请求私信、批量关注、批量点赞、批量转发或刷互动
- TweetClaw 不提供的 X 广告、分析看板或定时发布功能
- 只配置了只读访问时执行写入操作
- 在没有明确授权时访问私有或账号级数据
- 要求用户在聊天中粘贴 API key、签名密钥、Cookie 或令牌

## 使用说明

1. 先把用户需求归类为一个工作流：读取、抽取、写入、媒体、私信、监控、Webhook、抽奖或能力发现。
2. 当安装、配置、限制或 API 细节会影响结果时，先查看当前文档：
   - [TweetClaw GitHub](https://github.com/Xquik-dev/tweetclaw)
   - [Xquik 文档](https://docs.xquik.com)
   - [TweetClaw npm registry metadata](https://registry.npmjs.org/@xquik%2ftweetclaw)
3. 在 OpenClaw 中安装时，优先使用明确的 npm 选择器：

```bash
openclaw plugins install npm:@xquik/tweetclaw
```

4. 安装或更新后，先验证运行时再执行真实任务：

```bash
openclaw plugins inspect tweetclaw --runtime --json
openclaw skills info tweetclaw
```

5. 将凭证保存在 Xquik dashboard、OpenClaw 插件配置或环境变量支持的密钥存储中。不要打印或回显凭证值。
6. 使用 TweetClaw 能力发现或 Xquik 文档选择最小可行端点和请求数量。
7. 在任何可见、会改变状态、涉及私有数据、付费、周期性、抽取、监控、Webhook、抽奖或账号级操作前，说明目标、账号、动作、限制、数据处理方式，以及可获得的使用影响。等待用户明确确认。
8. 发推或回复前，展示最终文本和媒体列表。不要添加用户没有要求的链接、提及、话题标签或声明。
9. 创建监控或 Webhook 时，说明目标、事件类型、投递方式，以及用户如何停止该资源。
10. 输出结果时保持简洁，包含 ID、URL、数量和任何部分失败。

## 常见工作流

### 搜索推文

当用户需要 Agent 搜索 X/Twitter 内容时使用 TweetClaw。保持查询范围明确，设置结果数量，并总结返回的推文 ID、URL、作者、时间和匹配文本。

### 导出粉丝

确认账号或主页、请求数量，以及用户需要原始行还是摘要。私有账号数据必须限制在用户授权范围内。

### 发布推文

展示准确的推文文本和附件媒体。发送前先请求确认。操作成功后返回创建的推文 URL。

### 监控动态

只有在用户确认账号、关键词或事件目标后才创建监控。说明将监控什么内容，以及结果如何投递。
