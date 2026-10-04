---
name: immortal-skill
description: "通用数字永生框架：从聊天记录、社交媒体、文档等多平台数据中蒸馏任何人的数字分身——支持自己、同事、导师、亲人、伴侣/前任、朋友、公众人物 7 种角色模板，接入国内外 12+ 数据平台。"
license: MIT
metadata: {"openclaw": {"requires": {"bins": ["python3"]}, "emoji": "♾️"}, "kit_version": "2", "personas": ["self", "colleague", "mentor", "family", "partner", "friend", "public-figure"], "platforms": ["feishu", "dingtalk", "wechat", "imessage", "telegram", "whatsapp", "slack", "discord", "email", "twitter", "social-archive", "manual"]}
---

# 数字永生

## 语言

根据用户**第一条消息**的语言，全程使用同一语言。

## 何时激活

- 用户要「蒸馏 XX」「做数字分身」「保留 TA 的方式/记忆」「让 AI 像 XX 一样」。
- 用户提供关于某人的材料，希望生成可加载的 Agent Skill 包。

## 核心理念

**选择角色 → 多平台采集 → 分维度提取（procedure / interaction / memory / personality）→ 证据分级 → 冲突合并 → 输出符合 Agent Skills 的技能目录。**

## 路径约定

- 本 Skill 根目录记为 **`{baseDir}`**。
- 生成物默认写入 `./skills/immortals/<slug>/`。
- `slug`：小写字母、数字、连字符，与最终 `SKILL.md` 的 `name` 一致。

## 操作顺序

### Phase 0：选择角色模板

向用户询问蒸馏对象的角色，读取对应模板：

```
你想蒸馏谁？

  [1] 🪞 自己（全维度数字分身）
  [2] 🏢 同事（工作方式与沟通风格）
  [3] 🎓 导师/Mentor（教学方式与指导智慧）
  [4] 🏠 亲人（家族记忆与生活智慧）
  [5] 💕 伴侣/前任（关系记忆与互动模式）
  [6] 🤝 朋友（友谊互动与共同经历）
  [7] 🌐 公众人物（公开方法论）
```

读取 `{baseDir}/personas/<选择>.md` 了解该角色的特有维度与要求。
同时读取 `{baseDir}/personas/_base.md` 了解通用维度。

### Phase 1：伦理确认

根据角色模板中的伦理要求，在收集材料前告知用户。不同角色的伦理侧重：
- **同事/导师**：限团队内部对齐与培训
- **亲人（已故）**：确认其他家人是否应知情
- **伴侣/前任**：确认目的是正面回忆；严格脱敏
- **公众人物**：仅限公开资料；须有可追溯的公开出处
- **自己**：注意聊天中他人发言的脱敏

### Phase 2：收集材料

读取 `{baseDir}/recipes/intake-protocol.md`，按角色类型确定数据源。

提供以下采集方式：

```
材料怎么提供？

  [A] 自动采集（推荐）
      飞书 / 钉钉 / Slack / Discord / Telegram / Email
      → 扫描频道 → 拉取消息

  [B] 本地数据库
      微信（需第三方导出或本地 SQLite）
      iMessage（macOS，需 Full Disk Access）

  [C] 归档文件
      WhatsApp 导出 / Twitter/X 归档 / Google Takeout
      Facebook 数据下载 / 微博导出

  [D] 上传/粘贴文件
      PDF / JSON / CSV / Markdown / 纯文本

  [E] 直接粘贴文字

可混用多种方式。
```

自动采集使用统一 CLI：
```bash
python3 {baseDir}/kit/immortal_cli.py collect --platform <平台> [选项]
```

详见 `{baseDir}/docs/PLATFORM-GUIDE.md`。

### Phase 3：分维度提取

根据角色模板确定所需维度，按需加载对应 Prompt：

| 维度 | Prompt | Recipe | 适用角色 |
|------|--------|--------|---------|
| 程序性 | `prompts/procedural-extractor.md` | `recipes/procedural-mining.md` | 同事、导师、自己、公众人物 |
| 互动性 | `prompts/interaction-extractor.md` | `recipes/interaction-mining.md` | 所有 |
| 记忆 | `prompts/memory-extractor.md` | `recipes/memory-mining.md` | 自己、亲人、伴侣、朋友、导师、公众人物 |
| 性格 | `prompts/personality-extractor.md` | `recipes/personality-mining.md` | 所有（同事仅工作相关） |

每条输出标注证据级别：`verbatim` / `artifact` / `impression`。

参考 `{baseDir}/examples/` 下的示例查看产出物格式。

### Phase 4：合并与冲突处理

读取 `{baseDir}/recipes/merge-policy.md`，执行证据分级合并。矛盾项写入 `conflicts.md`。

### Phase 5：初始化目录并写入

```bash
python3 {baseDir}/kit/manifest_tool.py init --slug <slug> --base ./skills/immortals --persona <角色>
```

用 Write 工具写入各维度文件，然后读取 `{baseDir}/prompts/skill-assembler.md` 生成 `SKILL.md`。

### Phase 6：封包登记

```bash
python3 {baseDir}/kit/manifest_tool.py stamp --slug <slug> --base ./skills/immortals --sources "<来源>"
```

### Phase 7：告知用户

- 生成路径与加载方式
- 证据覆盖度统计
- 各维度的局限性提示

## 追加材料（进化）

```bash
python3 {baseDir}/kit/version_tool.py snapshot --slug <slug> --base ./skills/immortals --note "追加前"
```

然后按 Phase 2-6 增量更新。

## 用户纠正

先快照，再读取 `{baseDir}/prompts/correction-handler.md` 处理。

## 版本管理

```bash
python3 {baseDir}/kit/version_tool.py list --slug <slug> --base ./skills/immortals
python3 {baseDir}/kit/version_tool.py rollback --slug <slug> --base ./skills/immortals --tag <快照>
```

## 不做的事

- 不复制任何第三方仓库的脚本或提示词。
- 不把通用常识当成被蒸馏者的个人特色。
- 不模拟公众人物的私人对话。
- 不用于跟踪、骚扰或欺骗。

## 自检清单

- [ ] `name` 与目录名一致且符合命名规则。
- [ ] 各维度文件中 `verbatim + artifact` 占比是否达标？
- [ ] `impression` 是否隔离到专属区？
- [ ] `conflicts.md` 是否反映了真矛盾？
- [ ] 伦理声明是否与角色匹配？
- [ ] `SKILL.md` 正文 < 100 行？
