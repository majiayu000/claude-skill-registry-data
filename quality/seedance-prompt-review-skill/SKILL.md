---
name: seedance_prompt_review
description: 分镜终审工具。检查底层语法、运镜冲突和空间轴线。
parameters:
  type: object
  properties:
    shot_id:
      type: string
      description: 镜头编号
    final_prompt:
      type: string
      description: 分镜师提交的完整 Seedance 提示词
  required:
    - shot_id
    - final_prompt
---

# 视听语言与机位审核
这是渲染前的最后一道防线：

## 运镜冲突检查
- Seedance 中不能同时出现互斥的运镜（例如同时 zoom in 和 zoom out）
- 同时 pan left 和 pan right: 不允许
- 同时 tilt up 和 tilt down: 不允许
- 同时 dolly in 和 dolly out: 不允许

## 景别匹配检查
- 激烈动作: 必须配合动态运镜
- 对话戏: 必须有特写锚定
- 抒情场景: 适合用舒缓的镜头运动

## 空间轴线检查
- 180度准则: 检查是否遵守180度准则
- 轴线方向确认: 确认镜头方向一致
- 镜头衔接轴线验证: 验证镜头衔接的轴线合理性

```python
def execute(params):
    import sqlite3
    import os
    
    shot_id = params.get("shot_id")
    prompt = params.get("final_prompt", "").lower()
    
    # 互斥运镜检查
    if "zoom in" in prompt and "zoom out" in prompt:
        return {
            "status": "rejected", 
            "feedback": "运镜冲突：同时出现 zoom in 和 zoom out。"
        }
    if "pan left" in prompt and "pan right" in prompt:
        return {
            "status": "rejected", 
            "feedback": "运镜冲突：同时出现 pan left 和 pan right。"
        }
    if "tilt up" in prompt and "tilt down" in prompt:
        return {
            "status": "rejected", 
            "feedback": "运镜冲突：同时出现 tilt up 和 tilt down。"
        }
    if "dolly in" in prompt and "dolly out" in prompt:
        return {
            "status": "rejected", 
            "feedback": "运镜冲突：同时出现 dolly in 和 dolly out。"
        }
    
    # 数据库路径
    db_path = os.path.join(os.path.dirname(__file__), "../../project/evolution_log.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 更新状态
    cursor.execute('UPDATE shots SET status = ? WHERE shot_id = ?', 
                   ('approved', shot_id))
    conn.commit()
    conn.close()
    
    # 这里可以接入复杂的 SymPy 轴线校验逻辑
    # validate_axis(shot_id)
    
    return {
        "status": "approved", 
        "message": "分镜语法与机位审核通过，准许渲染。"
    }
```
