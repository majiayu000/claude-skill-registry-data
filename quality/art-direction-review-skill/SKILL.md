---
name: art_direction_review
description: 视觉资产合规审核。核对美术组输出的提示词是否符合导演预期和项目整体画风。
parameters:
  type: object
  properties:
    asset_id:
      type: string
      description: 视觉资产ID
    prompt_content:
      type: string
      description: 美术生成的具体提示词
  required:
    - asset_id
    - prompt_content
---

# 美术审核标准（Art Direction QA）
你必须像美术总监一样苛刻。核对以下几点：

## 画风底线检查
- **强制技术词汇**: 必须包含 realistic photography、8K、ultra-detailed、cinematic lighting 等词汇
- **高质感要求**: detailed、intricate、hyper-detailed 等细节描述
- **光影质量**: cinematic lighting、natural lighting 等光影描述

## 时代违和感检查
- **违禁现代词汇**: cyberpunk、t-shirt、phone、smartphone、earbuds、headphones 等（除非剧本设定在现代）
- **违禁二次元/3D词汇**: anime、manga、chibi、cartoon、2D、3D render、CG、Unreal Engine render 等
- **绝对不允许**: 出现非真人漫剧以外的画风

## 敏感词与强制词库
```
违禁词: anime, manga, chibi, cartoon, 2d, 3d render, CG, Unreal Engine render
强制词: realistic photography, 8k, ultra-detailed, detailed, intricate, masterpiece, best quality
```

```python
def execute(params):
    import sqlite3
    import os
    
    asset_id = params.get("asset_id")
    prompt = params.get("prompt_content", "").lower()
    
    # 建立敏感词与强制词库
    forbidden_words = ["cyberpunk", "t-shirt", "phone", "smartphone", "earbuds", "headphones", "anime", "manga", "chibi", "cartoon", "2d", "3d render", "cg", "unreal engine render"]
    required_words = ["realistic photography", "8k", "detailed", "ultra-detailed", "masterpiece", "best quality"]
    
    # 检查违禁词
    for word in forbidden_words:
        if word in prompt:
            return {
                "status": "rejected", 
                "feedback": f"画风穿帮：检测到违禁词汇 '{word}'，必须是纯粹的真人漫剧风格。"
            }
    
    # 检查强制词
    missing_words = []
    for word in required_words:
        if word not in prompt:
            missing_words.append(word)
    
    if missing_words:
        return {
            "status": "rejected", 
            "feedback": f"画质警告：缺少核心质感控制词：{', '.join(missing_words)}"
        }
    
    # 数据库路径
    db_path = os.path.join(os.path.dirname(__file__), "../../project/evolution_log.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 更新状态
    cursor.execute('UPDATE assets SET status = ? WHERE asset_id = ?', 
                   ('approved', asset_id))
    conn.commit()
    conn.close()
    
    return {
        "status": "approved", 
        "message": "服化道审核通过，资产已锁定。"
    }
```
