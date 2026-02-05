---
name: odoo-icon-maker
description: This skill should be used when creating icons for Odoo modules. It generates modern Material Design style PNG icons (128x128) with white background, colored circle, and composable colored primitives. Updates manifest files and automatically handles web_icon references in menu XML files. Use when user asks to create, generate, or add an icon to an Odoo module.
---

# Odoo Icon Maker

Generate professional Material Design style PNG icons for Odoo modules using composable colored primitives 
on white background with colored circle, and automatically update all related files (manifest, menu views).

## When to use

Use this skill when:
- User asks to "create icon for module X"
- User says "add icon to module Y with description Z"
- User wants to "update module icon"
- Working on a new module that needs an icon
- Module has menu but missing icon

## What you do

### Step 1: Gather Information

**From user request, identify:**
- Module name (e.g., `inventory_tracking`, `task_manager`)
- Icon description with keywords (e.g., "warehouse inventory with boxes", "task checklist and calendar")
- Optional: Custom colors for circle (e.g., "#27ae60,#229954")

**If not provided, ask:**
- "What should the icon represent?" (if description missing)
- Module name is usually obvious from context

**DO NOT ask about:**
- Symbol details (script detects primitives from keywords automatically)
- Exact positioning (handled by composition logic)

### Step 2: Run Icon Generator Script

Execute the Python script:

```bash
# Basic usage (recommended)
uv run python .claude/skills/odoo_icon_maker/scripts/make_icon.py \
  --module inventory_tracking \
  --description "Warehouse inventory with boxes and tracking"

# With custom circle colors (green)
uv run python .claude/skills/odoo_icon_maker/scripts/make_icon.py \
  --module task_manager \
  --description "Task checklist and calendar" \
  --colors "#27ae60,#229954"

# Dry run (preview without writing files)
uv run python .claude/skills/odoo_icon_maker/scripts/make_icon.py \
  --module reporting_analytics \
  --description "Charts and data visualization" \
  --dry-run
```

**How it works:**
The script detects primitives from keywords in description and automatically composes them into a modern Material Design icon.

**Icon Design:**
- White background with rounded corners
- Colored circle in center (category color or custom)
- Colored primitives on the circle (each with distinct color)

### Step 3: Primitive Detection

**Available primitives (12 total):**

1. **gear** - Gray metallic - Keywords: manufacturing, production, machine, workcenter, gear
2. **calendar** - Red header, white body - Keywords: calendar, schedule, planning, event, date
3. **checkbox** - White box, green checkmark - Keywords: task, checklist, todo, check
4. **document** - Blue - Keywords: document, file, paper, form
5. **folder** - Yellow - Keywords: folder, directory
6. **user** - Dark gray - Keywords: user, people, person, team, employee
7. **chart** - Teal bars - Keywords: chart, analytics, graph, report, statistics
8. **box** - Orange with yellow tape - Keywords: warehouse, inventory, stock, box, package
9. **message** - White bubble, blue dots - Keywords: message, chat, telegram, communication, notification
10. **settings** - Gray sliders - Keywords: settings, config, setup, preferences
11. **arrow** - White - Keywords: arrow, flow, process, workflow
12. **lock** - Golden yellow - Keywords: lock, security, secure, protection

**Automatic composition:**
- 1 primitive detected → centered (50% size)
- 2 primitives detected → left and right (38% each)
- 3+ primitives detected → main center (42%) + right accent (25%) + small corner accent (20%)

**Example detection:**
```
Description: "Manufacturing workcenter with task planning"
Detected: gear + calendar + checkbox
Result: Gray gear (main), Red calendar (right), Green checkbox (corner)
All on colored circle on white background
```

### Step 4: Circle Colors

**Automatic circle color selection based on keywords:**
- Manufacturing/Production → Industrial blue (#34495e)
- Calendar/Planning → Red/Orange (#e74c3c)
- Tasks → Green (#2ecc71)
- Messages → Telegram blue (#0088cc)
- Documents/Folders → Purple (#9b59b6)
- Warehouse → Orange (#f39c12)
- Analytics → Teal (#1abc9c)
- Default → Blue (#3498db)

**Custom colors:**
Override circle color with `--colors "#color1,#color2"` (uses first color for circle)

### Step 5: Script Actions

The script automatically performs:

1. **Generate icon PNG**
   - Creates 128x128 PNG file
   - White background with rounded corners
   - Colored circle in center (category or custom color)
   - Detects primitives from description keywords
   - Draws colored primitives on circle
   - Saves to `module_name/static/description/icon.png`
   - Creates directories if they don't exist

2. **Update __manifest__.py**
   - Adds or updates `'icon': '/module_name/static/description/icon.png'`
   - Preserves existing manifest structure
   - Backs up original if changes made

3. **Check and update menu XML files**
   - Searches for `views/*menu*.xml` or `views/*views.xml` with menuitem
   - Finds root menuitem entries (without parent)
   - Adds or updates `web_icon="module_name,static/description/icon.png"`
   - Backs up original XML files
   - Reports which files were updated

4. **Validation**
   - Verifies PNG format and size
   - Checks paths are correct
   - Validates XML syntax after changes

### Step 6: Parse Script Output

Script returns JSON:

```json
{
  "status": "success",
  "icon_created": true,
  "icon_path": "addons_ticket/ticket_task_manager/static/description/icon.png",
  "manifest_updated": true,
  "menu_files_updated": [
    "views/menu_views.xml"
  ],
  "backups_created": [
    "__manifest__.py.backup",
    "views/menu_views.xml.backup"
  ],
  "warnings": []
}
```

If errors occur:
```json
{
  "status": "error",
  "error": "Module directory not found: addons_ticket/nonexistent_module",
  "icon_created": false
}
```

### Step 7: Present Results to User

**On success:**
```
✅ Icon created successfully!

Module: task_manager
Icon: static/description/icon.png (128x128 PNG)
Design: White background + green circle + colored primitives
Primitives detected: calendar (red), checkbox (green)

Files updated:
- __manifest__.py (icon path added)
- views/menu_views.xml (web_icon updated)

Backups created in case you need to rollback.

Next steps:
1. Update the module: odoo-bin -u task_manager
2. Refresh browser (Ctrl+F5)
3. Check Apps menu for new icon
```

**On partial success (icon created but no menu):**
```
✅ Icon created!

Module: task_manager
Icon: static/description/icon.png

⚠ Note: No menu XML files found
If this module should have a menu item, create one and include:
  web_icon="task_manager,static/description/icon.png"
```

**On error:**
```
❌ Error creating icon

Error: Module directory not found: task_manager

Please check:
- Module name is correct
- Module exists in addon directories
- You're in the project root directory
```

## Important Notes

**Icon Requirements (Odoo 18):**
- Format: PNG (not SVG)
- Size: 128x128 pixels
- Location: `/module_name/static/description/icon.png`
- Style: Material Design (white background, colored circle, colored primitives)

**Menu Structure:**
Root menu items need:
- NO action attribute
- web_icon attribute: `web_icon="module_name,static/description/icon.png"`
- groups attribute for access control

**Automatic Updates:**
- Script only updates ROOT menuitem entries (those without parent attribute)
- Backups are always created before modifications
- XML validation ensures no syntax errors introduced

**Module Update Required:**
After creating/updating icon:
```bash
docker compose -f docker/arm/odoo18-dev-run.yml -p odoo18c_dev run --rm odoo \
  python3 /opt/odoo/app/server/odoo-bin -c /opt/odoo/app/config/odoo.conf \
  -d test_basic -u module_name --stop-after-init
```

## Examples

**Example 1: Manufacturing module**
```
User: "Create an icon for am_workcenter_tasks - manufacturing with task planning"

You:
1. Run: make_icon.py --module am_workcenter_tasks --description "Manufacturing workcenter machine with planning calendar and task management"
2. Script detects: gear + calendar + checkbox
3. Result: White background → Dark blue circle → Gray gear + Red calendar + Green checkbox
4. Report: "Icon created with Material Design style!"
```

**Example 2: Custom colors**
```
User: "Create icon for ticket_purchase with green background"

You:
1. Run: make_icon.py --module ticket_purchase --description "Purchase orders with documents and products inventory" --colors "#27ae60,#229954"
2. Script detects: document + box
3. Result: White background → Custom green circle → Blue document + Orange box
4. Report: "Icon created with custom green circle!"
```

**Example 3: Analytics module**
```
User: "Icon for sales_reports - should show charts and analytics"

You:
1. Run: make_icon.py --module sales_reports --description "Sales analytics with charts and reports"
2. Script detects: chart + document
3. Result: White background → Teal circle → Teal bars + Blue document
4. Report: "Icon created with analytics style!"
```

**Example 4: Document management**
```
User: "Icon for doc_manager - documents and folders for teams"

You:
1. Run: make_icon.py --module doc_manager --description "Document management with folders for team collaboration"
2. Script detects: document + folder + user
3. Result: White background → Purple circle → Blue document + Yellow folder + Dark gray user
```

## Primitive Composition Rules

**Design structure:**
1. White background (128x128) with rounded corners
2. Colored circle in center (84% radius)
3. Colored primitives on circle

**1 primitive:**
- Centered, medium size (50% of icon)

**2 primitives:**
- First: Left side (38% size)
- Second: Right side (38% size)

**3+ primitives:**
- First: Main center (42% size)
- Second: Right accent (25% size)
- Third: Small corner accent (20% size)
- Additional primitives ignored

## Primitive Colors

Each primitive has distinct color for recognition:

- **gear** → Gray metallic (#95a5a6)
- **calendar** → Red header (#e74c3c), white body
- **checkbox** → White box, green checkmark (#2ecc71)
- **document** → Blue (#3498db)
- **folder** → Yellow (#f1c40f)
- **user** → Dark blue-gray (#34495e)
- **chart** → Teal (#1abc9c)
- **box** → Orange (#e67e22) with yellow tape
- **message** → White bubble with blue dots (#3498db)
- **settings** → Gray (#7f8c8d)
- **arrow** → White (#ffffff)
- **lock** → Golden yellow (#f1c40f)

## Keyword Detection Tips

**Good descriptions (specific):**
- "Manufacturing workcenter with task planning" → gear + calendar + checkbox
- "Warehouse inventory management with boxes" → box + folder
- "Team chat and messages" → message + user
- "Security settings and configuration" → lock + settings

**Average descriptions:**
- "Purchase orders for tickets" → document only (need to add: "with products inventory")
- Better: "Purchase orders with documents and products inventory" → document + box

**Poor descriptions (vague):**
- "Module for management" → No primitives detected, falls back to initials
- "Helper tools" → No primitives detected

**Tip:** Use 2-3 specific keywords from the primitives list for best results. More primitives = richer icon.

## Error Handling

**Module not found:**
- Check module name matches directory name
- Verify you're in project root
- Check module exists in configured addon paths

**PIL/Pillow not available:**
- Script requires Pillow library
- Install: `pip install Pillow`

**Permission errors:**
- Check write permissions on module directory
- Verify static/description/ is writable

**XML parsing errors:**
- Script validates XML before writing
- If errors occur, backups remain untouched
- Review menu XML structure manually

## Configuration

**Before first use**, customize `config.py` for your project:

```python
# Project root (auto-detected from script location)
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Addon directories (relative to PROJECT_ROOT)
ADDON_DIRECTORIES = [
    'addons_ticket',
    'addons_aimax',
    # Add your custom directories
]

# Icon size in pixels (Odoo standard is 128x128)
ICON_SIZE = 128
```

**Default values** work for standard Odoo projects with common structure.

The script will:
- Search all configured addon directories
- Find module by name
- Create directories as needed

## Advanced Usage

**Preview before creating:**
```bash
make_icon.py --module my_module --description "..." --dry-run
```

**Custom circle colors (hex format):**
```bash
# Green circle
make_icon.py --module my_module --description "..." --colors "#27ae60,#229954"

# Blue circle
make_icon.py --module my_module --description "..." --colors "#3498db,#2980b9"

# Orange circle
make_icon.py --module my_module --description "..." --colors "#e67e22,#d35400"
```

**Note:** First color is used for the circle, second color is ignored (kept for compatibility).

## Design Philosophy

**Material Design Style:**
- Clean white background for professionalism
- Colored circle for category/brand distinction
- Each primitive has distinct color for instant recognition
- Rounded corners for modern look
- High contrast for visibility in Odoo interface

**Why colored primitives?**
- Easier to recognize at small sizes
- More visually appealing than monochrome
- Each primitive color is carefully chosen for meaning (gear=gray/metal, calendar=red/urgent, checkbox=green/done, etc.)

## Primitives Library

Full list with colors and visual descriptions:

1. **gear** - Gray metallic (#95a5a6) - Circular gear with 8 teeth and center hole
2. **calendar** - Red header (#e74c3c), white body - Calendar page with bindings and date grid
3. **checkbox** - White box, green check (#2ecc71) - Square checkbox with checkmark
4. **document** - Blue (#3498db) - Paper with folded corner and white text lines
5. **folder** - Yellow (#f1c40f) - Folder with tab
6. **user** - Dark gray (#34495e) - Person silhouette (head + shoulders)
7. **chart** - Teal (#1abc9c) - Bar chart with 4 varying height bars
8. **box** - Orange (#e67e22), yellow tape - Package with cross tape
9. **message** - White bubble, blue dots (#3498db) - Speech bubble with 3 dots
10. **settings** - Gray (#7f8c8d) - Three horizontal sliders at different positions
11. **arrow** - White (#ffffff) - Right-pointing arrow with shaft and head
12. **lock** - Golden yellow (#f1c40f) - Padlock with gray shackle and dark keyhole

## References

- Script location: `.claude/skills/odoo_icon_maker/scripts/make_icon.py`
- Design style: Material Design inspired
- Color system: Automatic category detection with override support
- Primitive rendering: Composable vector graphics using PIL