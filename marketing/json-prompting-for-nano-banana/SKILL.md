---
name: json-prompting-for-nano-banana
description: Converts natural language descriptions into structured JSON schemas for Nano Banana Pro (Gemini 3 Pro Image). Use when creating marketing images, UI mockups, diagrams, data visualizations, or social media graphics that require precise control and reproducibility. Supports five schema types for product photography, interfaces, flowcharts, charts, and social content.
---

# JSON Prompting for Nano Banana Pro

This skill transforms natural language descriptions into structured JSON schemas that give precise control over image generation with Nano Banana Pro (Gemini 3 Pro Image).

## When to Use This Skill

Use this skill when the user wants to:

- Create **marketing images** with exact product specifications (product photography, hero shots)
- Design **UI mockups** with defined layouts, components, and color systems
- Build **infographics or diagrams** where process flows need to be clear
- Generate **data visualizations** where numbers and chart accuracy matter
- Create **social media graphics** with platform-specific dimensions and text overlays
- Generate images with **reproducibility** (same spec = same result)
- **Iterate on specific elements** without regenerating everything else
- Maintain **brand consistency** across multiple image generations

**Do NOT use this skill when:**

- The user wants creative exploration with surprise outcomes
- The user prefers vibes-based prompting
- A simple natural-language prompt would suffice
- The user hasn't defined what they actually want yet

## Core Concept: Handles

The power of JSON prompting is the **handle concept**. Every important element gets a stable identifier:

- **Scoped edits**: Change only the background, or only the lighting, without affecting other elements
- **Camera moves**: Same scene, different perspective
- **Themed variants**: Same structure, different visual styling
- **A/B testing**: Compare two versions that differ by exactly one variable

---

## The Five Schema Types

### 1. Marketing Image (`marketing_image`)

For product shots, hero images, brand photography, and advertising visuals.

**Key sections:**
- `subject`: Product type, name, variant, physical properties (finish, dimensions)
- `props`: Foreground, midground, and background objects with counts and positions
- `environment`: Surface material, background color/texture, atmosphere/mood
- `camera`: Angle, framing, focal length, depth of field
- `lighting`: Key light, fill light, rim light, color temperature
- `brand`: Logo assets, primary colors, forbidden changes
- `controls`: What can/cannot change during iteration

### 2. UI/UX (`ui_builder`)

For app screens, dashboards, websites, and interface mockups.

**Key sections:**
- `app`: Platform (web/mobile/desktop), fidelity level, viewport, theme
- `tokens`: Colors (hex values), typography, border radius, spacing scale
- `screens`: Array of screens with IDs, names, roles, and layout containers
- `components`: UI elements with screen assignment, container placement, and props
- `constraints`: Layout lock, theme lock, content lock

### 3. Diagram (`diagram_spec`)

For flowcharts, architecture diagrams, process maps, and system visualizations.

**Key sections:**
- `canvas`: Dimensions, unit, flow direction
- `semantics`: Diagram type, primary relationship, swimlanes
- `nodes`: Array of nodes with IDs, labels, roles, positions, styles
- `edges`: Connections between nodes with labels and arrow styles
- `groups`: Swimlanes or clusters for organizing nodes
- `constraints`: Layout lock, auto-routing permissions

### 4. Data Visualization (`data_viz`)

For charts, graphs, and statistical graphics where numerical accuracy is critical.

**Key sections:**
- `chart_type`: bar, line, pie, scatter, area, treemap, heatmap
- `data_series[]`: Arrays of data points with labels and values
- `axes`: X and Y axis configuration (labels, min/max, units, gridlines)
- `annotations`: Callouts, trend lines, data labels, highlights
- `style`: Colors, fonts, legend position
- `constraints`: Data values that must appear exactly as specified

### 5. Social Media Graphic (`social_graphic`)

For platform-specific social content with text overlays and brand elements.

**Key sections:**
- `platform`: Target platform (instagram_post, instagram_story, twitter_card, linkedin_post, youtube_thumbnail)
- `dimensions`: Auto-set based on platform or custom
- `background`: Solid color, gradient, image, or pattern
- `text_layers[]`: Headline, subhead, body, CTA with positions and styling
- `brand`: Logo placement, colors, fonts
- `style`: Visual tone (minimal, bold, playful, professional)

---

## Translator Workflow

### Step 1: Classify Intent

Determine the target schema from the user's description:

| User talks about... | Schema to use |
|---------------------|---------------|
| Product shots, hero images, brand photography, campaigns | `marketing_image` |
| Screens, buttons, dashboards, apps, navigation, mockups | `ui_builder` |
| Flows, processes, systems, nodes, boxes-and-arrows | `diagram_spec` |
| Charts, graphs, data, statistics, metrics, numbers | `data_viz` |
| Instagram, Twitter, LinkedIn, social posts, thumbnails | `social_graphic` |

If ambiguous, ask 1-2 short questions to disambiguate.

### Step 2: Gather Requirements

**For Marketing Images:**
- Main subject (product type, name, size)
- Props (and where: foreground, around base, background)
- Environment (surface, background, mood)
- Camera angle and framing
- Lighting direction and intensity
- Brand constraints (logos, colors, things that cannot change)

**For UI/UX:**
- Platform (web, mobile, desktop)
- Number of screens and their roles
- Layout areas (top nav, sidebar, content)
- Key components (charts, tables, forms, cards)
- Color scheme or brand guidelines

**For Diagrams:**
- Diagram type (flowchart, architecture, swimlane, mind map)
- Key nodes/steps
- Connections and labels
- Groupings or lanes
- Flow direction

**For Data Visualizations:**
- Chart type (bar, line, pie, scatter, etc.)
- Data series with actual values
- Axis labels and ranges
- Any annotations or callouts
- Whether exact numbers must appear in the output

**For Social Graphics:**
- Target platform (determines dimensions)
- Background style (solid, gradient, image)
- Text content (headline, subhead, CTA)
- Brand elements (logo, colors)
- Visual style/mood

### Step 3: Generate JSON

Build a complete JSON object with the appropriate root key. Ensure:
- All IDs are unique
- All references are valid
- Required fields are filled
- Output is valid JSON (no comments, no trailing commas)

### Step 4: Provide Next Steps

Tell the user:
1. Review the JSON to ensure it captures their intent
2. Copy the entire JSON
3. Open Nano Banana Pro (Gemini app with "Thinking" model, or Google AI Studio)
4. Paste with instruction: "Render this specification as a high-fidelity image"
5. Iterate by modifying specific fields and re-rendering

---

## Common Values Reference

**Camera angles:** `front`, `three_quarter_front`, `three_quarter_back`, `side`, `top_down`, `low_angle`, `overhead`

**Framing:** `extreme_close_up`, `close_up`, `medium_close`, `medium`, `medium_wide`, `wide`

**Lighting intensity:** `very_low`, `low`, `medium`, `high`, `very_high`

**Lighting direction:** `left`, `right`, `front`, `back`, `top`, `three_quarter_left`, `three_quarter_right`

**Surface materials:** `glossy`, `matte`, `marble`, `wood`, `concrete`, `fabric`, `metal`, `glass`

**UI fidelity:** `wireframe`, `low-fi`, `mid-fi`, `hi-fi`

**UI platforms:** `web`, `mobile`, `tablet`, `desktop`

**Diagram types:** `flowchart`, `architecture`, `sequence`, `swimlane`, `mindmap`, `org_chart`

**Node roles:** `start`, `end`, `process`, `decision`, `database`, `actor`, `note`

**Chart types:** `bar`, `horizontal_bar`, `line`, `area`, `pie`, `donut`, `scatter`, `bubble`, `treemap`, `heatmap`, `radar`

**Social platforms:** `instagram_post` (1080x1080), `instagram_story` (1080x1920), `twitter_card` (1200x675), `linkedin_post` (1200x627), `youtube_thumbnail` (1280x720), `facebook_post` (1200x630)

**Text positions:** `top_left`, `top_center`, `top_right`, `center_left`, `center`, `center_right`, `bottom_left`, `bottom_center`, `bottom_right`

---

## Complete Schema Examples

### Marketing Image Example

**Request:** "Hero shot for a lime seltzer brand called Aurora Lime. 12oz can on a reflective surface with lime slices and ice cubes. Dark teal background, dramatic side lighting."

**Output:**

```json
{
  "marketing_image": {
    "meta": {
      "spec_version": "1.0.0",
      "title": "Aurora Lime Hero Can Shot",
      "campaign": "aurora_lime_launch",
      "brand_name": "Aurora Lime",
      "usage_context": "web"
    },
    "subject": {
      "type": "product_can",
      "name": "Aurora Lime Seltzer",
      "variant": "Original Lime",
      "physical_properties": {
        "volume_oz": 12,
        "dimensions": "standard 12oz beverage can",
        "finish": "matte"
      }
    },
    "props": {
      "foreground": [
        {
          "type": "lime_slice",
          "count": 3,
          "position": "front_left",
          "notes": "fresh lime slices, visible pulp and rind"
        }
      ],
      "midground": [
        {
          "type": "ice_cube",
          "count": 12,
          "position": "around_base",
          "notes": "partially melted, small reflections"
        }
      ],
      "background": []
    },
    "environment": {
      "surface": {
        "material": "glossy",
        "reflection_strength": 0.7
      },
      "background": {
        "color": "#003b47",
        "texture": "smooth",
        "effect": "bokeh_soft"
      },
      "atmosphere": {
        "mood": "refreshing, premium, night-time bar feel",
        "keywords": ["sparkling", "cool", "luminous", "evening"]
      }
    },
    "camera": {
      "angle": "three_quarter_front",
      "framing": "medium_close",
      "focal_length_mm": 50,
      "depth_of_field": "medium"
    },
    "lighting": {
      "key_light_direction": "right",
      "key_light_intensity": "high",
      "fill_light_direction": "left",
      "fill_light_intensity": "low",
      "rim_light": false,
      "color_temperature": "neutral"
    },
    "brand": {
      "logo_asset": "aurora_lime_logo.png",
      "primary_colors": ["#00ffc2", "#003b47"],
      "must_match_assets": ["aurora_lime_logo.png"],
      "forbidden_changes": [
        "do_not_change_logo",
        "do_not_change_brand_name"
      ]
    },
    "controls": {
      "lock_subject_geometry": true,
      "lock_logo_and_label": true,
      "allow_background_variation": false,
      "allow_prop_relayout": "small_only"
    }
  }
}
```

### UI/UX Example

**Request:** "Marketing analytics dashboard for web. Light theme, blue accents. Main dashboard with KPI cards, traffic chart, and campaigns table. Top nav with logo, left sidebar."

**Output:**

```json
{
  "ui_builder": {
    "meta": {
      "spec_version": "1.0.0",
      "name": "Acme Analytics Dashboard",
      "description": "Marketing analytics dashboard",
      "author": "",
      "tags": ["analytics", "marketing", "dashboard"]
    },
    "app": {
      "platform": "web",
      "fidelity": "hi-fi",
      "viewport": {
        "width": 1440,
        "height": 900
      },
      "theme": "light"
    },
    "tokens": {
      "color": {
        "primary": "#2563EB",
        "background": "#F9FAFB",
        "surface": "#FFFFFF",
        "accent": "#10B981"
      },
      "typography": {
        "font_family": "system_sans",
        "headline_size": 20,
        "body_size": 14
      },
      "radius": {
        "sm": 4,
        "md": 8,
        "lg": 12
      },
      "spacing_scale": [0, 4, 8, 12, 16, 24, 32]
    },
    "screens": [
      {
        "id": "screen_dashboard",
        "name": "Dashboard",
        "role": "primary",
        "layout": {
          "containers": [
            {
              "id": "container_top_nav",
              "type": "stack",
              "subtype": "horizontal",
              "region": "top_nav",
              "children": ["comp_logo", "comp_avatar"]
            },
            {
              "id": "container_sidebar",
              "type": "stack",
              "subtype": "vertical",
              "region": "sidebar",
              "children": ["comp_nav_list"]
            },
            {
              "id": "container_content",
              "type": "grid",
              "subtype": "column",
              "region": "main_content",
              "children": ["comp_kpi_grid", "comp_traffic_chart", "comp_campaigns_table"]
            }
          ]
        }
      }
    ],
    "components": [
      {
        "id": "comp_logo",
        "screen_id": "screen_dashboard",
        "container_id": "container_top_nav",
        "component_type": "logo",
        "props": {"text": "Acme Analytics"},
        "data_binding": null
      },
      {
        "id": "comp_nav_list",
        "screen_id": "screen_dashboard",
        "container_id": "container_sidebar",
        "component_type": "nav_list",
        "props": {
          "items": [
            {"label": "Overview", "icon": "home", "active": true},
            {"label": "Channels", "icon": "bar_chart"},
            {"label": "Settings", "icon": "gear"}
          ]
        },
        "data_binding": null
      },
      {
        "id": "comp_kpi_grid",
        "screen_id": "screen_dashboard",
        "container_id": "container_content",
        "component_type": "kpi_grid",
        "props": {
          "columns": 3,
          "cards": [
            {"label": "Sessions", "value": "124,983"},
            {"label": "Signups", "value": "3,942"},
            {"label": "Conversion", "value": "3.2%"}
          ]
        },
        "data_binding": null
      },
      {
        "id": "comp_traffic_chart",
        "screen_id": "screen_dashboard",
        "container_id": "container_content",
        "component_type": "line_chart",
        "props": {"title": "Daily Traffic (Last 30 Days)"},
        "data_binding": null
      },
      {
        "id": "comp_campaigns_table",
        "screen_id": "screen_dashboard",
        "container_id": "container_content",
        "component_type": "data_table",
        "props": {
          "title": "Active Campaigns",
          "columns": ["Campaign", "Spend", "Clicks", "CPC"]
        },
        "data_binding": null
      }
    ],
    "constraints": {
      "layout_lock": true,
      "theme_lock": false,
      "content_lock": false
    }
  }
}
```

### Diagram Example

**Request:** "Flowchart showing user signup: landing page, signup form, email validation decision, verification email, account activation. Left to right."

**Output:**

```json
{
  "diagram_spec": {
    "meta": {
      "spec_version": "1.0.0",
      "title": "User Signup Flow",
      "description": "End-to-end signup process",
      "author": "",
      "tags": ["signup", "user-flow"]
    },
    "canvas": {
      "width": 1920,
      "height": 600,
      "unit": "px",
      "direction": "left_to_right"
    },
    "semantics": {
      "diagram_type": "flowchart",
      "primary_relationship": "control_flow",
      "swimlanes": []
    },
    "nodes": [
      {
        "id": "node_start",
        "label": "Start",
        "role": "start",
        "lane": null,
        "group_id": null,
        "position": {"x": 50, "y": 260},
        "size": {"width": 80, "height": 80},
        "style": {
          "shape": "ellipse",
          "fill_color": "#10B981",
          "border_color": "#059669"
        },
        "data": {}
      },
      {
        "id": "node_landing",
        "label": "Visit Landing Page",
        "role": "process",
        "lane": null,
        "group_id": null,
        "position": {"x": 200, "y": 250},
        "size": {"width": 180, "height": 100},
        "style": {
          "shape": "rectangle",
          "fill_color": "#FFFFFF",
          "border_color": "#111827"
        },
        "data": {}
      },
      {
        "id": "node_signup_form",
        "label": "Complete Signup Form",
        "role": "process",
        "lane": null,
        "group_id": null,
        "position": {"x": 450, "y": 250},
        "size": {"width": 180, "height": 100},
        "style": {
          "shape": "rectangle",
          "fill_color": "#FFFFFF",
          "border_color": "#111827"
        },
        "data": {}
      },
      {
        "id": "node_email_valid",
        "label": "Email Valid?",
        "role": "decision",
        "lane": null,
        "group_id": null,
        "position": {"x": 700, "y": 250},
        "size": {"width": 120, "height": 100},
        "style": {
          "shape": "diamond",
          "fill_color": "#FEF3C7",
          "border_color": "#D97706"
        },
        "data": {}
      },
      {
        "id": "node_send_verification",
        "label": "Send Verification Email",
        "role": "process",
        "lane": null,
        "group_id": null,
        "position": {"x": 900, "y": 250},
        "size": {"width": 180, "height": 100},
        "style": {
          "shape": "rectangle",
          "fill_color": "#FFFFFF",
          "border_color": "#111827"
        },
        "data": {}
      },
      {
        "id": "node_activate",
        "label": "Activate Account",
        "role": "process",
        "lane": null,
        "group_id": null,
        "position": {"x": 1150, "y": 250},
        "size": {"width": 180, "height": 100},
        "style": {
          "shape": "rectangle",
          "fill_color": "#D1FAE5",
          "border_color": "#059669"
        },
        "data": {}
      },
      {
        "id": "node_end",
        "label": "End",
        "role": "end",
        "lane": null,
        "group_id": null,
        "position": {"x": 1400, "y": 260},
        "size": {"width": 80, "height": 80},
        "style": {
          "shape": "ellipse",
          "fill_color": "#111827",
          "border_color": "#111827"
        },
        "data": {}
      }
    ],
    "edges": [
      {"id": "edge_1", "from": "node_start", "to": "node_landing", "label": "", "style": {"line_type": "straight", "arrowhead": "standard"}},
      {"id": "edge_2", "from": "node_landing", "to": "node_signup_form", "label": "", "style": {"line_type": "straight", "arrowhead": "standard"}},
      {"id": "edge_3", "from": "node_signup_form", "to": "node_email_valid", "label": "", "style": {"line_type": "straight", "arrowhead": "standard"}},
      {"id": "edge_4", "from": "node_email_valid", "to": "node_send_verification", "label": "Yes", "style": {"line_type": "straight", "arrowhead": "standard"}},
      {"id": "edge_5", "from": "node_email_valid", "to": "node_signup_form", "label": "No", "style": {"line_type": "orthogonal", "arrowhead": "standard"}},
      {"id": "edge_6", "from": "node_send_verification", "to": "node_activate", "label": "", "style": {"line_type": "straight", "arrowhead": "standard"}},
      {"id": "edge_7", "from": "node_activate", "to": "node_end", "label": "", "style": {"line_type": "straight", "arrowhead": "standard"}}
    ],
    "groups": [],
    "legend": {
      "items": [
        {"label": "Process", "shape": "rectangle", "fill_color": "#FFFFFF"},
        {"label": "Decision", "shape": "diamond", "fill_color": "#FEF3C7"},
        {"label": "Success", "shape": "rectangle", "fill_color": "#D1FAE5"}
      ]
    },
    "constraints": {
      "layout_lock": false,
      "allow_auto_routing": true
    }
  }
}
```

### Example 4: Data Visualization (Quarterly Revenue Chart)

```json
{
  "data_viz": {
    "meta": {
      "spec_version": "1.0.0",
      "title": "Q4 2024 Revenue by Region",
      "description": "Bar chart comparing regional revenue performance",
      "author": "Finance Team"
    },
    "chart_type": "bar",
    "orientation": "vertical",
    "canvas": {
      "width": 1200,
      "height": 800,
      "background_color": "#FFFFFF"
    },
    "data_series": [
      {
        "id": "revenue_q4",
        "label": "Q4 2024 Revenue",
        "color": "#2563EB",
        "data_points": [
          {"label": "North America", "value": 4250000},
          {"label": "Europe", "value": 3180000},
          {"label": "Asia Pacific", "value": 2890000},
          {"label": "Latin America", "value": 1420000},
          {"label": "Middle East", "value": 890000}
        ]
      },
      {
        "id": "revenue_q3",
        "label": "Q3 2024 Revenue",
        "color": "#93C5FD",
        "data_points": [
          {"label": "North America", "value": 3950000},
          {"label": "Europe", "value": 2980000},
          {"label": "Asia Pacific", "value": 2650000},
          {"label": "Latin America", "value": 1280000},
          {"label": "Middle East", "value": 750000}
        ]
      }
    ],
    "axes": {
      "x_axis": {
        "label": "Region",
        "show_gridlines": false
      },
      "y_axis": {
        "label": "Revenue (USD)",
        "min": 0,
        "max": 5000000,
        "format": "currency_millions",
        "show_gridlines": true,
        "gridline_color": "#E5E7EB"
      }
    },
    "annotations": [
      {
        "type": "data_label",
        "show": true,
        "position": "above",
        "format": "$X.XM"
      },
      {
        "type": "callout",
        "target_series": "revenue_q4",
        "target_point": "North America",
        "text": "+7.6% vs Q3",
        "style": "badge_green"
      }
    ],
    "legend": {
      "position": "top_right",
      "orientation": "horizontal"
    },
    "style": {
      "font_family": "Inter",
      "title_size": 24,
      "label_size": 12,
      "bar_width": 0.35,
      "bar_gap": 0.1,
      "corner_radius": 4
    },
    "constraints": {
      "data_lock": true,
      "exact_values": [4250000, 3180000, 2890000, 1420000, 890000],
      "allow_style_changes": true
    }
  }
}
```

### Example 5: Social Media Graphic (Instagram Post)

```json
{
  "social_graphic": {
    "meta": {
      "spec_version": "1.0.0",
      "title": "Product Launch Announcement",
      "campaign": "spring_2025_launch",
      "brand_name": "Acme Tech"
    },
    "platform": "instagram_post",
    "dimensions": {
      "width": 1080,
      "height": 1080,
      "unit": "px"
    },
    "background": {
      "type": "gradient",
      "gradient": {
        "direction": "diagonal_bottom_right",
        "colors": ["#1E3A8A", "#7C3AED", "#EC4899"]
      },
      "overlay": {
        "type": "noise",
        "opacity": 0.05
      }
    },
    "text_layers": [
      {
        "id": "headline",
        "content": "Introducing AcmePod Pro",
        "position": "center",
        "offset_y": -120,
        "style": {
          "font_family": "Montserrat",
          "font_weight": "bold",
          "font_size": 64,
          "color": "#FFFFFF",
          "text_align": "center",
          "max_width": 900,
          "line_height": 1.1
        }
      },
      {
        "id": "subhead",
        "content": "Sound reimagined. Silence perfected.",
        "position": "center",
        "offset_y": 0,
        "style": {
          "font_family": "Montserrat",
          "font_weight": "medium",
          "font_size": 28,
          "color": "#E0E7FF",
          "text_align": "center",
          "max_width": 800
        }
      },
      {
        "id": "cta",
        "content": "Available March 15 →",
        "position": "bottom_center",
        "offset_y": -80,
        "style": {
          "font_family": "Montserrat",
          "font_weight": "semibold",
          "font_size": 22,
          "color": "#FFFFFF",
          "background_color": "rgba(255,255,255,0.15)",
          "padding": "12px 24px",
          "border_radius": 24,
          "text_align": "center"
        }
      }
    ],
    "visual_elements": [
      {
        "id": "product_image",
        "type": "image_placeholder",
        "position": "center",
        "offset_y": 100,
        "size": {"width": 400, "height": 400},
        "description": "AcmePod Pro earbuds in floating arrangement",
        "effects": ["drop_shadow", "subtle_glow"]
      }
    ],
    "brand": {
      "logo": {
        "asset": "acme_logo_white.png",
        "position": "top_center",
        "offset_y": 60,
        "size": {"width": 120, "height": 40}
      },
      "primary_colors": ["#1E3A8A", "#7C3AED"],
      "fonts": ["Montserrat"]
    },
    "style": {
      "mood": "premium",
      "keywords": ["modern", "sleek", "bold", "tech"]
    },
    "constraints": {
      "lock_text_content": true,
      "lock_brand_elements": true,
      "allow_color_variation": false,
      "allow_layout_adjustment": "minor"
    }
  }
}
```

---

## Iteration Patterns

Once the user has a base JSON spec, guide them through **scoped changes**:

### Change Lighting Only (Marketing)
Modify only the `lighting` section. Everything else stays locked.

### Change Camera Angle Only (Marketing)
Modify only `camera.angle` and optionally `camera.focal_length_mm`.

### Theme Swap (UI)
Swap token colors while keeping layout and components unchanged.

### Add a Component (UI)
Add a new object to the `components` array with valid `screen_id` and `container_id`.

### Update Data Values (Data Viz)
Modify values in `data_series[].data_points` while keeping chart structure and styling.

### Change Chart Type (Data Viz)
Swap `chart_type` from "bar" to "line" or "area" while preserving data and axes.

### Platform Resize (Social)
Change `platform` value and dimensions auto-adjust. Text layers may need position tweaks.

### Color Scheme Swap (Social)
Modify `background.gradient.colors` and corresponding text colors for new mood.

---

## Version History

- v1.1.0 (2025-12-05): Added data_viz and social_graphic schema types
- v1.0.0 (2025-12-05): Initial release with three schema types (marketing_image, ui_builder, diagram_spec)