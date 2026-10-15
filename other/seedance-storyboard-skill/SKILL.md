---
name: seedance_storyboard
description: Seedance 2.0 终极语法编译器。融合人物、场景、动作和运镜，生成带权重的提示词。
parameters:
  type: object
  properties:
    char_prompt:
      type: string
      description: 人物视觉资产
    scene_prompt:
      type: string
      description: 场景视觉资产
    action:
      type: string
      description: 具体动作描述
    camera_movement:
      type: string
      description: 导演指定的运镜 (如 pan right, slow motion)
    shot_id:
      type: string
      description: 镜头编号 (如 shot001)
  required:
    - char_prompt
    - scene_prompt
    - action
    - camera_movement
    - shot_id
---

# Seedance 提示词编译规范
你是专业的真人漫剧提示词编译官。你需要按照 Seedance 2.0 最佳实践组合公式：

## 组合公式
```
[环境基础] + [主体及动作（加权重）] + [镜头语言] + [画质修饰]
```

## 语法组装与权重分配
- **主体加权**: (char:1.2), 突出人物与动作
- **镜头强化**: (camera:1.1), 强调镜头运动
- **画面流畅**: cinematic motion blur, 24fps

## 强制负面词库防崩坏
```
(worst quality, low quality:1.4), (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, mutated hands and fingers, cartoon, anime, 3D render, CG, unrealistic
```

## 镜头类型参考
- wide/extreme wide: 远景，展示环境，建立场景氛围
- full shot: 全景，展示人物与环境的关系
- medium shot: 中景，展示人物上半身动作与表情
- medium close-up: 中近景，人物腰部以上，兼顾动作与表情
- close-up: 近景，人物胸部以上，强调表情
- big close-up/extreme close-up: 大特写/特写，细节特写，强调重点

## 镜头运动参考
- static: 固定，稳定观察，客观呈现
- dolly in/zoom in: 推，引导注意力，强调重点
- dolly out/zoom out: 拉，展示环境，揭示场景
- pan (left/right): 摇，水平环顾，跟随动作
- tilt (up/down): 移，垂直移动，展示上下
- tracking/follow: 跟，跟随人物，保持关注
- handheld: 手持，增加真实感与紧张感

```python
def execute(params):
    import sqlite3
    import os
    import json
    
    char = params.get("char_prompt", "")
    scene = params.get("scene_prompt", "")
    action = params.get("action", "")
    camera = params.get("camera_movement", "")
    shot_id = params.get("shot_id")
    
    # 1. 语法组装与权重分配（凸显人物与动作）
    main_subject = f"({char}:1.2), doing {action}"
    
    # 2. 镜头语言强化
    camera_syntax = f"({camera}:1.1), cinematic motion blur, 24fps"
    
    # 3. 强制负面词库防崩坏（防多指、防变形、防低画质）
    negative_prompt = "(worst quality, low quality:1.4), (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, mutated hands and fingers, cartoon, anime, 3D render, CG, unrealistic"
    
    # 强制画风
    base_style = "masterpiece, best quality, ultra-detailed, realistic photography, 8K, cinematic lighting, shallow depth of field"
    
    final_prompt = f"{scene}, {main_subject}, {camera_syntax}, {base_style}"
    
    # 数据库路径
    db_path = os.path.join(os.path.dirname(__file__), "../../project/evolution_log.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 确保表存在
    cursor.execute('''CREATE TABLE IF NOT EXISTS shots
                     (shot_id TEXT PRIMARY KEY, 
                      char_prompt TEXT,
                      scene_prompt TEXT,
                      action TEXT,
                      camera_movement TEXT,
                      final_prompt TEXT,
                      negative_prompt TEXT,
                      status TEXT DEFAULT 'pending',
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # 插入或更新
    cursor.execute('''INSERT OR REPLACE INTO shots 
                     (shot_id, char_prompt, scene_prompt, action, camera_movement, final_prompt, negative_prompt, status)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (shot_id, char, scene, action, camera, final_prompt, negative_prompt, "pending"))
    conn.commit()
    conn.close()
    
    return {
        "status": "compiled",
        "shot_id": shot_id,
        "positive_prompt": final_prompt,
        "negative_prompt": negative_prompt,
        "message": "提示词编译完成，已提交至审核流。"
    }
```
