---
name: director_skill
description: 剧本分析与拆解工具。用于将单场戏的文学描写，拆解为镜头列表、人物情绪弧线和关键动作，并入库。
parameters:
  type: object
  properties:
    scene_text:
      type: string
      description: 原始剧本片段
    scene_id:
      type: string
      description: 场景编号 (如 S01)
  required:
    - scene_text
    - scene_id
---

# 导演解场与讲戏指南
作为真人漫剧导演，你需要具备优秀的视听转化能力。
当你调用此技能时，你需要从文本中提取：
1. **焦点人物**：当前这行文字视觉中心是谁？
2. **动作拆解**：将大段动作切分为连续的、物理上可执行的动作（真人拍摄可行性）。
3. **情绪基调**：紧张、悲伤、欢快还是悬疑？（用于指导后续的灯光和机位）

## 输出标准

### 导演分析报告标准格式
```markdown
# 导演分析报告 - [集数]

## 一、整体讲戏本
### 1.1 主题解读
[剧本核心主题与思想内涵分析]

### 1.2 叙事结构
[剧情结构、节奏安排、关键情节点分析]

### 1.3 艺术风格
[视觉风格、基调氛围、表现手法定位]

## 二、人物清单
| 人物ID | 姓名 | 角色定位 | 性格特征 | 外观描述 | 表演要点 |
|--------|------|----------|----------|----------|----------|
| char001 | [姓名] | [主角/配角] | [性格描述] | [外观描述] | [表演指导] |

## 三、场景清单
| 场景ID | 场景名称 | 时间地点 | 环境描述 | 氛围基调 | 拍摄要点 |
|--------|----------|----------|----------|----------|----------|
| scene001 | [名称] | [时间·地点] | [环境描述] | [氛围基调] | [拍摄指导] |

## 四、分集创作建议
[针对本集的具体创作指导与注意事项]
```

```python
def execute(params):
    import sqlite3
    import json
    import os
    
    scene_id = params.get("scene_id")
    scene_text = params.get("scene_text", "")
    
    print(f"Director executing breakdown for Scene: {scene_id}")
    
    # 数据库路径
    db_path = os.path.join(os.path.dirname(__file__), "../../project/evolution_log.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 确保表存在
    cursor.execute('''CREATE TABLE IF NOT EXISTS scene_outlines
                     (scene_id TEXT PRIMARY KEY, 
                      status TEXT DEFAULT 'analyzed',
                      scene_text TEXT,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # 插入或更新
    cursor.execute('''INSERT OR REPLACE INTO scene_outlines 
                     (scene_id, status, scene_text)
                     VALUES (?, ?, ?)''', 
                   (scene_id, "analyzed", scene_text))
    conn.commit()
    conn.close()
    
    return {
        "status": "success",
        "message": f"场景 {scene_id} 拆解完毕，已入库。请继续调用自审技能或通知美术组。"
    }
```
