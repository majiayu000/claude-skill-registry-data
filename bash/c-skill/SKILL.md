---
name: create-skill
description: "智能创建OpenClaw技能，提供技能发现、复用建议和自适应文件生成。"
metadata: { "openclaw": { "emoji": "🎨" } }
---

# Skill: 智能技能创建向导 (create-skill)

智能创建OpenClaw技能，提供技能发现、复用建议和自适应文件生成。

## 触发方式

```
创建技能
create-skill
新建技能
skill create
需要创建技能
```

## 能力

- **智能技能发现** - 创建前搜索类似技能，避免重复造轮子
- **复用建议系统** - 根据现有技能给出实用的复用建议
- **自适应文件生成** - 根据实际需求生成相应文件
- **简化创建流程** - 清晰的交互选项和指导

## 输出格式

根据技能需求生成相应的文件结构：

### 智能创建流程
```
1. 技能发现阶段
   - 输入关键词搜索类似技能
   - 显示发现结果和复用建议
   - 选择创建策略（全新/扩展/取消）

2. 信息收集阶段
   - 收集技能基本信息
   - 选择实现方式
   - 确认创建

3. 文件生成阶段
   - 根据选择生成相应文件
   - 更新技能注册表
   - 提供后续步骤指导
```

## 示例对话

```
用户: 创建技能
助手: 🎯 开始执行智能技能创建向导...
      🎨 请输入新技能的核心关键词:
      用户输入: 文件处理
      发现类似技能: 文件管理, 批量处理
      是否创建新的技能?
      收集技能信息...
      生成技能文件...
      ✅ 技能创建完成
```

## 限制

- 仅在OpenClaw环境中运行

## 最佳实践

### 使用建议
1. **先搜索后创建** - 充分利用技能发现功能，避免重复创建
2. **考虑复用** - 优先考虑扩展现有技能，提高开发效率
3. **明确需求** - 清晰描述技能功能，便于技能发现
3. **逻辑极致精简** - 技能实现方案有限仅考虑纯skill文档指导，实在是需要脚本才考虑编写js或者shell脚本
6. **遵循标准** - 使用YAML frontmatter标准，确保技能元数据完整

### OpenClaw YAML Frontmatter 规范
每个OpenClaw技能都应包含标准的YAML frontmatter：

```yaml
---
name: skill-name
description: "技能描述"
homepage: https://example.com (可选)
metadata: { "openclaw": { "emoji": "🎨", "requires": { "bins": ["node"] } } }
---
```

**核心字段**：
- `name`: 技能名称（小写，用连字符连接）
- `description`: 技能描述（50字以内）
- `homepage`: 相关主页URL（可选）
- `metadata.openclaw`: OpenClaw元数据
  - `emoji`: 技能表情符号（如🎨、📊、⚡等）
  - `requires`: 依赖要求
    - `bins`: 需要的二进制文件（如`node`、`bash`、`curl`）
    - `node_modules`: 需要的npm包
    - `env`: 需要的环境变量

**示例**：
- 文档指导型：`metadata: { "openclaw": { "emoji": "📚" } }`
- Node.js技能：`metadata: { "openclaw": { "emoji": "⚡", "requires": { "bins": ["node"] } } }`
- Shell技能：`metadata: { "openclaw": { "emoji": "🐚", "requires": { "bins": ["bash"] } } }`

## FAQ

### 技能创建的基本流程是什么？
```
输入关键词 → 搜索类似技能 → 收集技能信息 → 生成文件
```

### 如何避免重复创建已有功能？
使用智能技能发现功能，创建前会搜索类似技能并给出复用建议。

### 技能应该包含哪些文件？
- 必须：`SKILL.md`（技能元数据文档）
- 可选：`<技能名>.js`（如果需要Node.js实现）或 `<技能名>.sh`（如果需要Shell实现）
- 可选：`package.json`（如果需要脚本则需要项目配置）

### 如何测试新创建的技能？
1. 查看技能文档：`cat skills/<技能名>/SKILL.md`
2. 如有脚本，运行测试：`cd skills/<技能名> && node <技能名>.js`
3. 在OpenClaw中尝试触发词