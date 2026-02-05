---
name: develop
description: 按照需求文档进行功能开发与记录
---

# Develop

本技能用于根据 `requirements/todo` 目录下的需求文档进行开发，并在开发完成后更新状态与开发日志。

---

## 📁 目录结构说明

| 目录 / 文件 | 说明 |
|--------------|------|
| `requirements/todo/` | 存放待开发的需求文档 |
| `requirements/dev_logs/` | 存放每个需求的开发日志 |
| `requirements/status.json` | 记录需求开发完成状态 |

---

## 🧾 需求文档规范

- **位置：** `requirements/todo`
- **命名规则：**  
[时间戳]_负责人.md   
其中时间戳格式为：`YYYYMMDDHHMMSS`  
示例：  
20251102220511_sean.md

- **内容要求：**  
需求文档应包含功能描述、接口定义、验收标准等信息（可自定义模板）。

---

## ⚙️ 开发流程

1. **检查需求状态**  
 打开 `requirements/status.json`，若目标文档对应值为 `true`，表示该需求已完成，无需再次开发。  

2. **确定开发顺序**  
 按照 `requirements/todo` 目录下的文件名**时间顺序（正序）**进行开发。

3. **执行开发任务**  
 根据需求文档内容完成相应开发工作。

4. **记录开发日志**  
 每个需求文档应在 `requirements/dev_logs/` 下创建同名日志文件。  
 - **命名规则：** 与需求文档同名  
   例如，`requirements/todo/20251102220511_sean.md` 对应的日志文件是：  
   ```
   requirements/dev_logs/20251102220511_sean.md
   ```
 - **内容建议包括：**
   - 开发起止时间  
   - 开发人员  
   - 关键进展  
   - 实现要点  
   - 问题与解决方案  

5. **更新开发状态**  
 开发完成后，在 `requirements/status.json` 中将对应需求标记为 `true`。

---

## ✅ 示例

### `requirements/status.json`
```json
{
"20251102220511_sean.md": true,
"20251102224533_gray.md": false
}
