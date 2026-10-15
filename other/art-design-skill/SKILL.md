---
name: art_design
description: 视觉资产生成器。结合剧本设定，生成极其专业、高精度的场景和人物 Prompt。
parameters:
  type: object
  properties:
    target_type:
      type: string
      description: 资产类型 (character 或 scene)
    raw_description:
      type: string
      description: 剧本中的原始描写
    asset_id:
      type: string
      description: 资产唯一标识 (如 char001 或 scene001)
  required:
    - target_type
    - raw_description
    - asset_id
---

# 美术资产设计规范
你是专业的真人漫剧美术指导。你的任务是将简单的描写转化为 Midjourney/Seedance 极佳的图像提示词。

## 人物 (Character) 设计要点
- **面部特征**：关注面部轮廓、五官特征、皮肤质感
- **服饰搭配**：棉麻、皮革、丝绸等材质的细致描述
- **光影效果**：光影打在脸上的效果，轮廓光、散射光等
- **整体质感**：高质感、8K细节、真实人像

## 场景 (Scene) 设计要点
- **空间透视**：透视关系、景深效果
- **自然光效**：自然光、环境光的具体描述
- **环境色温**：冷暖色调对冲的设计
- **氛围营造**：烟、雾、灰尘等细节

## 强制注入的全局画风基底
```
masterpiece, best quality, ultra-detailed, realistic photography, 8K, cinematic lighting, shallow depth of field
```

## 强制排除
```
cartoon, anime, 3D render, CG, unrealistic, deformed, distorted, disfigured
```

```python
def execute(params):
    import sqlite3
    import os
    import json
    
    target_type = params.get("target_type")
    raw_desc = params.get("raw_description")
    asset_id = params.get("asset_id")
    
    # 强制注入的全局画风基底
    base_style = "masterpiece, best quality, ultra-detailed, realistic photography, 8K, cinematic lighting, shallow depth of field"
    
    # 负面词库
    negative_style = "(worst quality, low quality:1.4), (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, mutated hands and fingers, cartoon, anime, 3D render, CG, unrealistic"
    
    # 模拟大模型将 raw_desc 扩写后的专业词汇
    if target_type == "character":
        enhanced_prompt = f"1 person, solo, {raw_desc}, realistic skin texture, dramatic rim light, {base_style}"
    else:
        enhanced_prompt = f"scenery, {raw_desc}, atmospheric perspective, volumetric fog, dynamic shadows, {base_style}"
    
    # 数据库路径
    db_path = os.path.join(os.path.dirname(__file__), "../../project/evolution_log.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 确保表存在
    cursor.execute('''CREATE TABLE IF NOT EXISTS assets
                     (asset_id TEXT PRIMARY KEY, 
                      target_type TEXT,
                      prompt TEXT,
                      negative_prompt TEXT,
                      raw_description TEXT,
                      status TEXT DEFAULT 'pending',
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # 插入或更新
    cursor.execute('''INSERT OR REPLACE INTO assets 
                     (asset_id, target_type, prompt, negative_prompt, raw_description, status)
                     VALUES (?, ?, ?, ?, ?, ?)''', 
                   (asset_id, target_type, enhanced_prompt, negative_style, raw_desc, "pending"))
    conn.commit()
    conn.close()
    
    return {
        "status": "success",
        "asset_id": asset_id,
        "asset_prompt": enhanced_prompt,
        "negative_prompt": negative_style,
        "message": "美术资产生成完毕，等待导演审核。"
    }
```
