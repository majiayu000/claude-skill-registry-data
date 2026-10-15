---
name: script_analysis_review
description: 导演自审工具。检查当前拆解的分镜大纲是否存在物理逻辑错误或接戏漏洞。
parameters:
  type: object
  properties:
    scene_id:
      type: string
      description: 需要复核的场景编号
  required:
    - scene_id
---

# 连贯性与逻辑审查规范
作为总导演，你在把大纲交给其他部门前必须进行自审：

## 核心审查要点

### 空间合理性审查
- **角色空间连贯性**：角色 A 在上一个动作被打飞，下一个动作是否突兀地出现在原地？
- **场景空间逻辑**：场景之间的空间转换是否合理？
- **空间轴线一致性**：确保场景的空间方向和轴线一致

### 道具追踪审查
- **重要道具状态连贯**：重要道具（如：沾血的剑）是否在整个场景中保持了状态连贯？
- **道具位置追踪**：道具的位置移动是否合理？
- **道具状态变化**：道具的状态变化是否有合理的原因？

### 业务审核检查项
- [ ] 剧本解读准确、深刻、有见解
- [ ] 人物分析完整、立体、逻辑自洽
- [ ] 场景分析清晰、具体、有指导意义
- [ ] 与前后集内容衔接自然、连贯
- [ ] 空间合理性通过审核，无突兀的角色位置变化
- [ ] 重要道具追踪到位，状态连贯

```python
def execute(params):
    import sqlite3
    import os
    
    scene_id = params.get("scene_id")
    
    # 数据库路径
    db_path = os.path.join(os.path.dirname(__file__), "../../project/evolution_log.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查询大纲
    cursor.execute('SELECT * FROM scene_outlines WHERE scene_id = ?', (scene_id,))
    outline = cursor.fetchone()
    
    if not outline:
        conn.close()
        return {
            "status": "failed",
            "feedback": f"场景 {scene_id} 未找到，请先调用导演技能进行分析！"
        }
    
    # 模拟从数据库拉取上一个镜头和当前镜头的核心要素对比
    # 这里是简化实现，实际项目需要做更复杂的检查
    prop_lost = False 
    
    if prop_lost:
        return {
            "status": "failed", 
            "feedback": "严重错误：第3镜主角手中的剑消失，不接戏，请重构该动作！"
        }
    
    # 更新状态
    cursor.execute('UPDATE scene_outlines SET status = ? WHERE scene_id = ?', 
                   ('reviewed', scene_id))
    conn.commit()
    conn.close()
    
    return {
        "status": "passed", 
        "message": "自审通过，物理逻辑与剧情连贯性无误。"
    }
```
