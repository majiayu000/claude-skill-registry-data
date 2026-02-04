---
name: rpg-map-creator
description: "Expert RPG map creation and generation for tabletop and online games. Specializes in creating visual descriptions and optimized prompts for z-image turbo model in ComfyUI. Covers all map types (world/continent, regional/local, battle/encounter, dungeon/interior) across multiple themes and settings (fantasy, sci-fi, cyberpunk, post-apocalyptic, horror, etc.). Use when Claude needs to: (1) Create RPG maps of any type, (2) Generate image prompts for map visualization in ComfyUI, (3) Design environments, biomes, settlements, or tactical battlefields, (4) Provide expert knowledge of cartography, terrain, and world-building for games, (5) Convert map descriptions into optimized prompts for image generation models, or (6) Help with any map creation or visualization for tabletop RPGs, video games, or online play."
---

# RPG Map Creator

## Overview

Create professional RPG maps across all scales and settings. This skill provides expert knowledge of cartography, environments, biomes, settlements, and tactical map design, with specialized focus on generating optimized prompts for the z-image turbo model in ComfyUI.

## When to Use This Skill

Use this skill when the user requests:
- Creating or designing any type of RPG map
- Generating maps for tabletop or online RPG sessions
- Producing image prompts for ComfyUI map visualization
- Designing environments, biomes, or settlements
- Creating tactical battle maps with terrain features
- Designing dungeon layouts or interior floor plans
- World-building assistance for game masters
- Converting map descriptions into visual prompts

## Map Types Supported

### 1. World/Continent Maps
Large-scale maps showing continents, kingdoms, major geography, and political boundaries.

**Scale:** Hundreds to thousands of miles
**Purpose:** Campaign overview, world-building, political context
**Key Features:** Continents, mountain ranges, rivers, kingdoms, trade routes

**Quick Start:**
1. Define landmasses and major geographic features
2. Add political boundaries and major settlements
3. Mark points of interest and landmarks
4. Choose appropriate style (parchment, satellite, illustrated)
5. Use references/map-types.md for detailed guidance
6. See assets/examples/world-map-examples.md for complete examples

### 2. Regional/Local Area Maps
Medium-scale maps showing specific regions, towns, and adventure locations.

**Scale:** 10-100 miles
**Purpose:** Local exploration, quest areas, settlement surroundings
**Key Features:** Towns/villages, specific terrain, roads, points of interest

**Quick Start:**
1. Identify central location (settlement, landmark)
2. Define surrounding terrain and features
3. Add roads, paths, and connections
4. Mark adventure locations and dangers
5. Use references/map-types.md for detailed guidance
6. See assets/examples/regional-map-examples.md for complete examples

### 3. Battle/Encounter Maps
Tactical combat maps with precise positioning and terrain features.

**Scale:** 50-200 feet
**Purpose:** Combat encounters, tactical play, virtual tabletops
**Key Features:** Grid system, cover elements, terrain, elevation, hazards

**Quick Start:**
1. Determine map size (typically 30x30 to 50x50 feet)
2. Choose grid type (square 5-foot or hexagonal)
3. Place terrain features and cover
4. Add hazards and tactical elements
5. Emphasize high contrast and VTT optimization
6. Use references/map-types.md for detailed guidance
7. See assets/examples/battle-map-examples.md for complete examples

### 4. Dungeon/Interior Maps
Detailed floor plans of dungeons, buildings, or interior spaces.

**Scale:** Varies (5-200 feet per section)
**Purpose:** Exploration, dungeon delving, architectural layouts
**Key Features:** Rooms, corridors, doors, furniture, secret passages

**Quick Start:**
1. Define structure type (dungeon, castle, cave, etc.)
2. Layout rooms and corridors
3. Add doors, furniture, and features
4. Mark secret doors and traps (for GM)
5. Include grid overlay if needed for gameplay
6. Use references/map-types.md for detailed guidance
7. See assets/examples/dungeon-map-examples.md for complete examples

## Core Workflow

### Step 1: Understand Requirements
Ask clarifying questions:
- What type of map? (world, regional, battle, dungeon)
- What theme/setting? (fantasy, sci-fi, cyberpunk, etc.)
- What's the purpose? (exploration, combat, world-building)
- What scale/size?
- Any specific features or requirements?

### Step 2: Gather Knowledge
Based on map type and theme, consult relevant references:

**For terrain and environments:**
- Read references/biomes.md for detailed biome information
- Covers forests, deserts, mountains, swamps, exotic biomes, underground

**For settlements and structures:**
- Read references/settlements.md for architectural styles and settlement types
- Covers hamlets to metropolises, fantasy to sci-fi architecture

**For thematic guidance:**
- Read references/themes.md for theme-specific visual characteristics
- Covers high fantasy, dark fantasy, cyberpunk, post-apocalyptic, horror, and more

**For map-specific guidance:**
- Read references/map-types.md for detailed map type instructions
- Covers all four map types with comprehensive guidelines

**For prompt optimization:**
- Read references/prompt-patterns.md for proven prompt patterns
- Essential for generating optimized z-image turbo prompts

### Step 3: Design the Map
Create the map description including:
- Overall layout and structure
- Key features and elements
- Terrain types and conditions
- Scale-appropriate detail level
- Atmospheric elements
- Points of interest

### Step 4: Generate Optimized Prompt
Convert the map description into an optimized prompt for z-image turbo:

**Option A: Use the Script (Recommended)**
Run scripts/generate_map_prompt.py for interactive prompt building:
```bash
python scripts/generate_map_prompt.py
```

The script guides through:
- Map type selection
- Theme choice
- Feature specification
- Style selection
- Atmosphere and color scheme
- Automatic quality tag addition

**Option B: Manual Construction**
Follow the prompt structure from references/prompt-patterns.md:
1. Map type + perspective (e.g., "fantasy battle map, top-down view")
2. Key elements (dimensions, features, terrain)
3. Style descriptors (hand-drawn, tactical, parchment, etc.)
4. Atmosphere/mood (ominous, bright, foggy)
5. Color scheme (warm earth tones, neon colors)
6. Quality tags (high resolution, detailed, VTT-optimized)

**Prompt Template:**
```
[THEME] [MAP TYPE], [PERSPECTIVE], [KEY ELEMENTS], [STYLE], [ATMOSPHERE], [COLORS], [QUALITY TAGS]
```

### Step 5: Provide Complete Output
Deliver to the user:
1. Map description (written form)
2. Optimized prompt for z-image turbo
3. Any additional guidance or notes
4. Suggestions for refinement if needed

## Examples and References

### Complete Working Examples
See assets/examples/ for full examples with descriptions and prompts:
- world-map-examples.md - 7 complete world map examples
- regional-map-examples.md - 5 complete regional map examples
- battle-map-examples.md - 6 complete battle map examples
- dungeon-map-examples.md - 7 complete dungeon/interior examples

Each example includes:
- Detailed description
- Map features list
- Fully optimized prompt ready to use

### Reference Material
Access detailed reference guides in references/:
- biomes.md - Comprehensive biome and terrain encyclopedia
- settlements.md - Architecture and settlement type guide
- themes.md - Complete theme and setting visual guide
- map-types.md - Detailed instructions for each map type
- prompt-patterns.md - Prompt engineering best practices

## Common Patterns and Tips

### Battle Map Best Practices
- Always specify exact dimensions (e.g., "40 feet by 40 feet")
- Include "square grid with 5-foot squares" explicitly
- List all cover elements with positions
- Mention elevation changes clearly
- Add "high contrast" and "VTT-optimized" to prompt
- Ensure tactical clarity over artistic flourish

### World Map Best Practices
- Use symbolic representation (mountains as peaks, forests as tree symbols)
- Include compass rose and decorative border in prompt
- Specify cartography style (parchment, atlas, satellite)
- Balance detail - don't try to show individual buildings
- Use color coding for territories/regions
- Include legend/key elements

### Dungeon Map Best Practices
- Clearly mark walls (thick lines)
- Indicate door types (regular, secret, locked)
- Show room purposes through furnishings
- Mark stairs with up/down arrows
- Include grid for gameplay clarity
- Consider breaking large dungeons into sections

### Prompt Optimization Tips
- Front-load important details (map type and perspective first)
- Be specific about materials and construction
- Use consistent terminology throughout
- Avoid contradictory elements
- Match detail level to map scale
- Always specify perspective ("top-down view")

## Interactive Prompt Generator

Use scripts/generate_map_prompt.py for guided prompt creation:

**Features:**
- Step-by-step interactive process
- Map type-specific questions
- Style suggestions based on map type
- Automatic quality tag addition
- Prompt saving to file
- Optimized for z-image turbo

**Usage:**
```bash
cd scripts/
python generate_map_prompt.py
```

Follow the interactive prompts to build an optimized map generation prompt.

## Advanced Techniques

### Combining Biomes
When maps feature multiple biomes:
1. Consult references/biomes.md for each biome type
2. Describe transition zones between biomes
3. Note color palette shifts
4. Indicate where biomes meet in prompt

### Multi-Level Maps
For dungeons or structures with multiple floors:
1. Create separate maps for each level
2. Mark stair connections clearly
3. Use same scale across all levels
4. Reference connections between maps
5. Consider showing vertical cross-section if helpful

### Theme Mixing
Some settings combine themes (e.g., dark fantasy + horror):
1. Consult both theme sections in references/themes.md
2. Blend color palettes and atmospheres
3. Include elements from both themes
4. Maintain coherent visual language

### Procedural Generation Assistance
For random/procedural maps:
1. Define parameters (size, complexity, features)
2. Use biome and settlement knowledge to populate
3. Ensure logical placement (water sources, settlements on routes)
4. Balance interesting features with navigable space

## Troubleshooting

### Prompt produces wrong scale
- Explicitly state dimensions and scale
- Use appropriate detail level for map type
- Add scale-appropriate descriptors

### Map lacks contrast/clarity
- Add "high contrast" to prompt
- Specify "clear for gameplay" or "VTT-optimized"
- Choose style emphasizing functionality

### Style is inconsistent
- Commit to single style in prompt
- Remove contradictory descriptors
- Reinforce style with multiple related terms

### Features are unclear
- Be more specific about materials and construction
- Add size/position details for features
- Use comparative descriptors

### Colors are muddy
- Specify color scheme explicitly
- Add "vibrant" or "high saturation" if needed
- Ensure sufficient contrast mentioned

## Resources

### scripts/
Executable Python script for interactive prompt generation:
- **generate_map_prompt.py** - Interactive prompt builder for z-image turbo

### references/
Comprehensive reference documentation (load into context as needed):
- **biomes.md** - Complete biome and environment encyclopedia with visual characteristics
- **settlements.md** - Architecture styles, settlement types, and urban features guide
- **themes.md** - RPG themes and settings with visual characteristics for 14+ themes
- **map-types.md** - Detailed instructions for all map types with examples and best practices
- **prompt-patterns.md** - Prompt engineering patterns and best practices for z-image turbo

### assets/examples/
Complete working examples with descriptions and optimized prompts:
- **world-map-examples.md** - 7 complete world/continent map examples
- **regional-map-examples.md** - 5 complete regional/local area map examples
- **battle-map-examples.md** - 6 complete battle/encounter map examples
- **dungeon-map-examples.md** - 7 complete dungeon/interior map examples

These examples provide ready-to-use templates that can be adapted for specific needs.
