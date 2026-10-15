---
name: compliance_review
description: 内容安全与合规审核工具。在生成任何视觉内容前，必须确保不触碰平台红线。
parameters:
  type: object
  properties:
    text_content:
      type: string
      description: 需要检测的文本（对白或动作描述）
    shot_id:
      type: string
      description: 镜头编号（可选）
  required:
    - text_content
---

# 平台合规审查
你不仅是导演，也是发行制片。必须过滤：

## 极度血腥暴露
- 将"斩首"弱化为"致命一击"
- 将"血肉模糊"弱化为"激烈战斗"
- 过度血腥暴露的描写都需要弱化

## 政治违禁品敏感隐喻
- 政治、违禁品等敏感隐喻必须过滤
- 敏感内容都需要进行适当处理

## NSFW 关键词库
```
["血肉模糊", "斩首", "断肢", "色情", "裸露", "血腥", "残忍", "恐怖", "虐杀"
```

```python
def execute(params):
    import sqlite3
    import os
    
    content = params.get("text_content", "")
    shot_id = params.get("shot_id", "")
    
    # 实际项目中，这里通常会调用阿里云/腾讯云的内容安全 API (Text Moderation)
    # 这里做简单的本地敏感词拦截作为示例
    nsfw_keywords = ["血肉模糊", "斩首", "断肢", "色情", "裸露", "血腥", "残忍", "恐怖", "虐杀"]
    
    found_keywords = []
    for word in nsfw_keywords:
        if word in content:
            found_keywords.append(word)
    
    if found_keywords:
        return {
            "status": "blocked", 
            "feedback": f"触发合规风控：包含敏感描写：{', '.join(found_keywords)}。请修改表达方式（如使用剪影或隐晦镜头替代）。"
        }
    
    # 如果有 shot_id，更新 shot 的状态
    if shot_id:
        # 数据库路径
        db_path = os.path.join(os.path.dirname(__file__), "../../project/evolution_log.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE shots SET status = ? WHERE shot_id = ?', ('compliance_passed', shot_id))
        conn.commit()
        conn.close()
    
    return {
        "status": "safe", 
        "message": "内容安全风控通过。"
    }
```
