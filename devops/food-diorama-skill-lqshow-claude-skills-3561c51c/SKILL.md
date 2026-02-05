---
name: food-diorama-skill
description: Generate 3D historical gourmet diorama images for Chinese cities using Google Gemini API. Creates artistic miniature food worlds with four-quadrant layouts featuring iconic dishes, Pop Mart style figures, and cultural elements. Use when the user asks to create food diorama, 美食盲盒, gourmet blind box, city food scene, or mentions generating 3D food artwork for cities like 西安, 重庆, 成都, 北京, 广州.
---

# 3D Historical Gourmet Diorama Generator

Generate stunning 3D food diorama images showcasing a city's culinary heritage through four-quadrant circular layouts with Pop Mart style characters.

## Requirements

1. **nanobanana skill** must be installed and configured with GEMINI_API_KEY
2. **Python 3** with standard libraries

## Quick Start

Generate a diorama for a city:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/food-diorama-skill/scripts/generate_food_diorama.py 西安
```

## Features

### Visual Style
- **Circular base**: City's signature food as the platform
- **Four quadrants**: Morning taste, historical feast, street food, sweet culture
- **Pop Mart figures**: Miniature chibi characters interacting with oversized food
- **Artistic city nameplate**: 3D sculpted city name with cultural materials
- **Historical elements**: Inscriptions, silhouettes, and cultural symbols
- **Technical quality**: Isometric view, high saturation, ray tracing, 4K capable

### Pre-configured Cities

The skill includes detailed food data for:
- **西安** (Xi'an): 羊肉泡馍, 胡辣汤, 葫芦鸡, 肉夹馍, 甑糕
- **重庆** (Chongqing): 火锅, 重庆小面, 毛血旺, 酸辣粉, 冰汤圆
- **成都** (Chengdu): 担担面, 豆花, 夫妻肺片, 钟水饺, 三大炮
- **北京** (Beijing): 炸酱面, 豆汁焦圈, 北京烤鸭, 卤煮火烧, 艾窝窝
- **广州** (Guangzhou): 肠粉, 虾饺, 白切鸡, 云吞面, 双皮奶

List all available cities:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/food-diorama-skill/scripts/generate_food_diorama.py --list-cities
```

## Usage

### Basic Generation

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/food-diorama-skill/scripts/generate_food_diorama.py 重庆
```

Output: `重庆-diorama.png`

### Custom Output

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/food-diorama-skill/scripts/generate_food_diorama.py 成都 --output chengdu-food-art.png
```

### High Resolution

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/food-diorama-skill/scripts/generate_food_diorama.py 北京 --resolution 4K --size 1344x768
```

### Preview Prompt

View the generated prompt without creating an image:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/food-diorama-skill/scripts/generate_food_diorama.py 广州 --show-prompt
```

## Options

- `city` (required): City name in Chinese (e.g., 西安, 重庆)
- `--output`: Output filename (default: `<city>-diorama.png`)
- `--size`: Image dimensions (default: `1024x1024`)
  - Available: `1024x1024`, `832x1248`, `1248x832`, `864x1184`, `1184x864`, `896x1152`, `1152x896`, `768x1344`, `1344x768`, `1536x672`
- `--resolution`: Image quality (default: `2K`)
  - Choices: `1K`, `2K`, `4K`
- `--model`: Gemini model (default: `gemini-3-pro-image-preview`)
  - Alternative: `gemini-2.5-flash-image` (faster)
- `--show-prompt`: Display prompt without generating
- `--list-cities`: Show all available cities

## Workflow

When a user requests a food diorama:

1. **Identify the city**: Ask which city if not specified
2. **Check availability**: Run with `--list-cities` if unsure
3. **Choose settings**: Recommend:
   - Square format (`1024x1024`) for social media posts
   - Landscape (`1344x768` or `1536x672`) for wallpapers
   - `2K` resolution for quality (use `4K` for prints)
4. **Generate**: Run the script with chosen parameters
5. **Present result**: Show the saved image path

## Extending the Database

To add a new city, edit `scripts/generate_food_diorama.py` and add an entry to `CITY_DATABASE`:

```python
"城市名": {
    "base": "基础食物",
    "base_desc": "详细描述",
    "history_text": "历史铭文",
    "city_material": "城市材质",
    "city_decoration": "装饰元素",
    "q1": {"name": "早餐", "desc": "描述", "texture": "质感", "action": "动作"},
    "q2": {"name": "硬菜", "desc": "描述", "texture": "质感", "action": "动作", 
           "costume": "服饰", "historical_figure": "历史人物"},
    "q3": {"name": "街头", "desc": "描述", "texture": "质感", "action": "动作",
           "historical_scene": "历史场景"},
    "q4": {"name": "甜品", "desc": "描述", "texture": "质感", "action": "动作",
           "cultural_symbol": "文化符号"}
}
```

## Examples

### Create a Xi'an diorama for Instagram
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/food-diorama-skill/scripts/generate_food_diorama.py 西安 --size 1024x1024 --resolution 2K --output xian-food-post.png
```

### Generate Chongqing wallpaper
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/food-diorama-skill/scripts/generate_food_diorama.py 重庆 --size 1536x672 --resolution 4K --output chongqing-wallpaper.png
```

### Quick test with Guangzhou
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/food-diorama-skill/scripts/generate_food_diorama.py 广州 --resolution 1K
```

## Best Practices

1. **Start with 2K**: Balance between quality and generation time
2. **Use square for social**: Most versatile format
3. **Landscape for prints**: Better for wall art or desktop wallpapers
4. **Check city availability**: Use `--list-cities` before committing to generation
5. **Preview prompts**: Use `--show-prompt` to verify content before generating

## Troubleshooting

**City not found**: 
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/food-diorama-skill/scripts/generate_food_diorama.py --list-cities
```

**nanobanana not found**:
Ensure nanobanana skill is installed and GEMINI_API_KEY is configured in `~/.nanobanana.env`

**Generation failed**:
- Check GEMINI_API_KEY is valid
- Try lower resolution (1K)
- Verify sufficient API quota
- Use faster model: `--model gemini-2.5-flash-image`
