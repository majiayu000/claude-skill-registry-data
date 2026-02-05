---
name: thymer-plugin
description: Build Thymer plugins - use when the user asks to create, modify, or debug Thymer plugins for the note-taking/project management app
---

# Thymer Plugin Development

## References

- [types.d.ts](references/types.d.ts) - Full SDK type definitions
- [sdk-reference.md](references/sdk-reference.md) - Additional SDK notes

Use this skill when building plugins for the Thymer app (thymer.com). Thymer plugins extend the application with custom functionality like status bar items, custom views, formulas, and more.

## Plugin Types

### AppPlugin (Global)
Extends the entire Thymer application:
- Status bar items
- Sidebar items
- Command palette commands
- Custom panels
- Toaster notifications

### CollectionPlugin
Extends a specific note Collection:
- Custom views (table, board, gallery, calendar, custom)
- Custom properties with formulas
- Navigation buttons
- Render hooks for existing views
- Custom sorting

## File Structure

```
plugin.js      # Plugin code (extends AppPlugin or CollectionPlugin)
plugin.json    # Configuration (name, icon, fields, views)
```

## Quick Reference

### AppPlugin Example
```javascript
export class Plugin extends AppPlugin {
    onLoad() {
        // Add status bar item
        this.statusItem = this.ui.addStatusBarItem({
            label: "My Plugin",
            icon: "star",
            tooltip: "Click me",
            onClick: () => this.handleClick()
        });

        // Add command palette command
        this.ui.addCommandPaletteCommand({
            label: "My Command",
            icon: "wand",
            onSelected: () => this.doSomething()
        });

        // Show notification
        this.ui.addToaster({
            title: "Hello",
            message: "Plugin loaded!",
            dismissible: true,
            autoDestroyTime: 3000
        });
    }

    onUnload() {
        // Cleanup (intervals, listeners, etc.)
    }
}
```

### CollectionPlugin Example
```javascript
export class Plugin extends CollectionPlugin {
    onLoad() {
        // Define a formula property
        this.properties.formula("Total", ({record}) => {
            const qty = record.number("Quantity");
            const price = record.number("Price");
            if (qty == null || price == null) return null;
            return qty * price;
        });

        // Custom property rendering
        this.properties.render("Status", ({record, prop}) => {
            const el = document.createElement('span');
            el.textContent = prop.text() || 'N/A';
            el.style.fontWeight = 'bold';
            return el;
        });

        // Register custom view
        this.views.register("My View", (viewContext) => {
            return {
                onLoad: () => {
                    viewContext.getElement().style.padding = "20px";
                },
                onRefresh: ({records}) => {
                    const el = viewContext.getElement();
                    el.innerHTML = records.map(r =>
                        `<div>${r.getName()}</div>`
                    ).join('');
                },
                onDestroy: () => {},
                onFocus: () => {},
                onBlur: () => {},
                onKeyboardNavigation: ({e}) => {},
                onPanelResize: () => {}
            };
        });

        // Hook into board card rendering
        this.views.afterRenderBoardCard(null, ({record, element}) => {
            element.style.border = '2px solid blue';
        });

        // Add navigation button
        this.addCollectionNavigationButton({
            label: "Export",
            icon: "download",
            onClick: ({panel}) => this.exportData(panel)
        });
    }
}
```

## Key APIs

### UIAPI (this.ui)
- `addStatusBarItem({label, icon, tooltip, onClick})` - Status bar
- `addSidebarItem({label, icon, tooltip, onClick})` - Sidebar
- `addCommandPaletteCommand({label, icon, onSelected})` - Commands
- `addToaster({title, message, dismissible, autoDestroyTime})` - Notifications
- `createButton({icon, label, onClick})` - Create button element
- `createDropdown({attachedTo, options})` - Dropdown menu
- `injectCSS(cssString)` - Add global styles
- `getActivePanel()` - Get focused panel
- `getPanels()` - Get all panels
- `createPanel()` - Create new panel
- `registerCustomPanelType(id, callback)` - Custom panel types

### DataAPI (this.data)
- `getAllRecords()` - Get all workspace records
- `getRecord(guid)` - Get record by GUID
- `createNewRecord(title)` - Create record
- `getAllCollections()` - Get all collections
- `getActiveUsers()` - Get workspace users

### PropertiesAPI (this.properties) - CollectionPlugin only
- `formula(name, fn)` - Computed property
- `render(name, fn)` - Custom property rendering
- `customSort(name, fn)` - Custom sorting

### ViewsAPI (this.views) - CollectionPlugin only
- `register(viewName, createHooksFn)` - Custom view type
- `afterRenderBoardCard(viewName, fn)` - Board card hook
- `afterRenderBoardColumn(viewName, fn)` - Board column hook
- `afterRenderGalleryCard(viewName, fn)` - Gallery card hook
- `afterRenderTableCell(viewName, fn)` - Table cell hook
- `afterRenderCalendarEvent(viewName, fn)` - Calendar event hook

### PluginRecord
- `getName()` - Record title
- `guid` - Record GUID
- `prop(name)` - Get property by name
- `number(name)` - Get numeric property
- `text(name)` - Get text property
- `date(name)` - Get date property
- `getProperties(viewName)` - Get visible properties
- `getLineItems()` - Get document content

### PluginProperty
- `number()` - Get as number
- `text()` - Get as text
- `date()` - Get as Date
- `choice()` - Get choice ID
- `set(value)` - Set value
- `setChoice(choiceName)` - Set by choice name

## plugin.json Configuration

```json
{
    "name": "My Collection",
    "icon": "tools",
    "description": "Collection description",
    "item_name": "Item",
    "ver": 1,
    "show_sidebar_items": true,
    "show_cmdpal_items": true,
    "fields": [
        {
            "id": "status",
            "label": "Status",
            "type": "choice",
            "icon": "circle",
            "active": true,
            "many": false,
            "read_only": false,
            "choices": [
                {"id": "todo", "label": "To Do", "color": "0", "active": true},
                {"id": "done", "label": "Done", "color": "2", "active": true}
            ]
        },
        {
            "id": "amount",
            "label": "Amount",
            "type": "number",
            "icon": "currency-dollar",
            "number_format": "USD",
            "active": true
        }
    ],
    "views": [
        {
            "id": "main",
            "label": "All Items",
            "type": "table",
            "icon": "table",
            "shown": true,
            "field_ids": ["status", "amount"],
            "sort_field_id": "status",
            "sort_dir": "asc"
        }
    ],
    "page_field_ids": ["status", "amount"]
}
```

## Property Types
- `text` - Plain text
- `number` - Numeric (formats: plain, formatted, USD, EUR, etc.)
- `choice` - Enum/status with choices
- `datetime` - Date/time
- `user` - User reference
- `record` - Record reference
- `url` - URL link
- `file` - File attachment
- `image` - Image
- `dynamic` - Formula-computed

## View Types
- `table` - Table view
- `board` - Kanban board
- `gallery` - Card gallery
- `calendar` - Calendar view
- `custom` - Fully custom view
- `record` - Single record view

## Icons
Common icons: `star`, `clock`, `tools`, `settings`, `search`, `home`, `user`, `calendar`, `bell`, `check`, `bug`, `rocket`, `wand`, `heart`, `file-text`, `folder`, `download`, `chart-bar`, `database`

See types.d.ts for full icon list.

## Development Workflow

1. Edit `plugin.js` and `plugin.json`
2. Run `npm run dev` for hot reload
3. Build with `npm run build`
4. Copy dist/plugin.js to Thymer's Edit Code dialog

## Important Notes

- Always clean up in `onUnload()` (intervals, listeners)
- Use CSS variables for theming (--bg-default, --text-muted, etc.)
- Check `viewContext.isDestroyed()` after async operations
- Use `viewContext.isViewingOldVersion()` before allowing edits
- Property formulas should return null for invalid inputs

## Working with Records

### Getting Records from a Collection
```javascript
const collections = await this.data.getAllCollections();
const collection = collections[0];
const records = await collection.getAllRecords();

for (const record of records) {
    const title = record.getName();
    const status = record.prop("Status")?.text();
    console.log(title, status);
}
```

### Setting Properties
```javascript
const record = this.data.getRecord(guid);
record.prop("Status").set("Done");
record.prop("Amount").set(42);
record.prop("Priority").setChoice("high");
```

### Creating Records
```javascript
const collection = (await this.data.getAllCollections())[0];
const newGuid = collection.createRecord("New Item Title");
const newRecord = this.data.getRecord(newGuid);
newRecord.prop("Status").set("Todo");
```
