---
name: fvtt-sheets
description: This skill should be used when creating or extending ActorSheet/ItemSheet classes, implementing getData or _prepareContext, binding events with activateListeners, handling drag/drop, or migrating from ApplicationV1 to ApplicationV2. Covers both legacy V1 and modern V2 patterns.
---

# Foundry VTT Sheets

**Domain:** Foundry VTT Module/System Development
**Status:** Production-Ready
**Last Updated:** 2026-01-04

## Overview

Document sheets (ActorSheet, ItemSheet) are the primary UI for interacting with game entities. Foundry supports two patterns: legacy ApplicationV1 (until V16) and modern ApplicationV2 (V12+).

### When to Use This Skill

- Creating custom character or item sheets
- Extending existing sheet classes
- Adding interactivity (rolls, item management)
- Implementing drag/drop functionality
- Migrating V1 sheets to V2

### V1 vs V2 Quick Comparison

| Aspect | V1 (Legacy) | V2 (Modern) |
|--------|-------------|-------------|
| Config | `static get defaultOptions()` | `static DEFAULT_OPTIONS` |
| Data | `getData()` | `async _prepareContext()` |
| Events | `activateListeners(html)` | `static actions` + `_onRender()` |
| Templates | Single template | Multi-part PARTS system |
| Re-render | Full sheet | Partial by part |
| Support | Until V16 | Current standard |

## ApplicationV1 Sheets

### Basic Structure

```javascript
export class MyActorSheet extends ActorSheet {
  static get defaultOptions() {
    return foundry.utils.mergeObject(super.defaultOptions, {
      classes: ["my-system", "sheet", "actor"],
      template: "systems/my-system/templates/actor-sheet.hbs",
      width: 600,
      height: 600,
      tabs: [{
        navSelector: ".sheet-tabs",
        contentSelector: ".sheet-body",
        initial: "description"
      }],
      dragDrop: [{
        dragSelector: ".item-list .item",
        dropSelector: null
      }]
    });
  }

  // Dynamic template based on actor type
  get template() {
    return `systems/my-system/templates/actor-${this.actor.type}-sheet.hbs`;
  }
}
```

### getData() - Preparing Template Context

```javascript
getData() {
  const context = super.getData();
  const actorData = this.actor.toObject(false);

  // Add data to context
  context.system = actorData.system;
  context.flags = actorData.flags;
  context.items = actorData.items;

  // Organize items by type
  context.weapons = context.items.filter(i => i.type === "weapon");
  context.spells = context.items.filter(i => i.type === "spell");

  // Enrich HTML (sync in V1)
  context.enrichedBio = TextEditor.enrichHTML(
    this.actor.system.biography,
    { secrets: this.actor.isOwner, async: false }
  );

  return context;
}
```

**Key Points:**
- Context has NO automatic relation to document data
- Everything template needs MUST be explicitly added
- `{{system.hp.value}}` reads from context
- `name="system.hp.value"` writes to document

### activateListeners() - Event Binding

```javascript
activateListeners(html) {
  // ALWAYS call super first
  super.activateListeners(html);

  // Skip if not editable
  if (!this.isEditable) return;

  // Roll handlers
  html.on("click", ".rollable", this._onRoll.bind(this));

  // Item management
  html.on("click", ".item-create", this._onItemCreate.bind(this));
  html.on("click", ".item-edit", this._onItemEdit.bind(this));
  html.on("click", ".item-delete", this._onItemDelete.bind(this));
}

async _onRoll(event) {
  event.preventDefault();
  const element = event.currentTarget;
  const { rollType, formula, label } = element.dataset;

  const roll = new Roll(formula, this.actor.getRollData());
  await roll.evaluate();
  roll.toMessage({
    speaker: ChatMessage.getSpeaker({ actor: this.actor }),
    flavor: label
  });
}

async _onItemCreate(event) {
  event.preventDefault();
  const type = event.currentTarget.dataset.type;
  await this.actor.createEmbeddedDocuments("Item", [{
    name: `New ${type.capitalize()}`,
    type: type
  }]);
}

async _onItemDelete(event) {
  event.preventDefault();
  const li = $(event.currentTarget).closest(".item");
  const item = this.actor.items.get(li.data("itemId"));
  await item.delete();
  li.slideUp(200, () => this.render(false));
}
```

### Drag & Drop (V1)

```javascript
// Automatic via defaultOptions
static get defaultOptions() {
  return foundry.utils.mergeObject(super.defaultOptions, {
    dragDrop: [{
      dragSelector: ".item-list .item",
      dropSelector: null
    }]
  });
}

// Override handlers as needed
_onDragStart(event) {
  const li = event.currentTarget;
  const item = this.actor.items.get(li.dataset.itemId);
  event.dataTransfer.setData("text/plain", JSON.stringify(item.toDragData()));
}

async _onDrop(event) {
  const data = TextEditor.getDragEventData(event);

  if (data.type === "Item") {
    return this._onDropItem(event, data);
  }
}

async _onDropItem(event, data) {
  if (!this.actor.isOwner) return false;
  const item = await Item.implementation.fromDropData(data);

  // Prevent dropping on self
  if (this.actor.uuid === item.parent?.uuid) return;

  return this.actor.createEmbeddedDocuments("Item", [item.toObject()]);
}
```

### Tab Navigation (V1)

```html
<!-- Template structure -->
<nav class="sheet-tabs">
  <a class="item" data-tab="description">Description</a>
  <a class="item" data-tab="items">Items</a>
</nav>

<section class="sheet-body">
  <div class="tab" data-group="primary" data-tab="description">
    <!-- Description content -->
  </div>
  <div class="tab" data-group="primary" data-tab="items">
    <!-- Items content -->
  </div>
</section>
```

## ApplicationV2 Sheets

### Basic Structure

```javascript
class MyActorSheet extends foundry.applications.api.HandlebarsApplicationMixin(
  foundry.applications.sheets.ActorSheetV2
) {
  static DEFAULT_OPTIONS = {
    classes: ["my-system", "sheet", "actor"],
    tag: "form",
    window: {
      resizable: true
    },
    position: {
      width: 600,
      height: 600
    },
    actions: {
      rollSkill: this.#onRollSkill,
      createItem: this.#onCreateItem,
      deleteItem: this.#onDeleteItem
    }
  }

  static PARTS = {
    header: {
      template: "systems/my-system/templates/actor/header.hbs"
    },
    tabs: {
      template: "templates/generic/tab-navigation.hbs"
    },
    description: {
      template: "systems/my-system/templates/actor/description.hbs",
      scrollable: [""]
    },
    items: {
      template: "systems/my-system/templates/actor/items.hbs",
      scrollable: [""]
    }
  }

  static TABS = {
    primary: {
      tabs: [
        { id: "description" },
        { id: "items" }
      ],
      labelPrefix: "MYSYS.TAB",
      initial: "description"
    }
  }
}
```

### _prepareContext() - Async Data Preparation

```javascript
async _prepareContext(options) {
  const context = await super._prepareContext(options);

  // Add tabs
  context.tabs = this._prepareTabs(this.tabGroups.primary);

  // Add system data
  context.system = this.document.system;

  // Organize items
  context.weapons = this.document.items.filter(i => i.type === "weapon");
  context.spells = this.document.items.filter(i => i.type === "spell");

  // Enrich HTML (MUST be async in V2)
  context.enrichedBio = await TextEditor.enrichHTML(
    this.document.system.biography,
    { async: true, relativeTo: this.document }
  );

  return context;
}

async _preparePartContext(partId, context) {
  switch (partId) {
    case "description":
    case "items":
      context.tab = context.tabs[partId];
      break;
  }
  return context;
}
```

### Static Actions (V2 Event Handling)

```javascript
static DEFAULT_OPTIONS = {
  actions: {
    rollSkill: this.#onRollSkill,
    createItem: this.#onCreateItem,
    deleteItem: this.#onDeleteItem
  }
}

// Action handlers MUST be static with # prefix
static #onRollSkill(event, target) {
  // 'this' is the application instance
  // 'target' is the clicked element
  const skillId = target.dataset.skillId;
  const skill = this.document.system.skills[skillId];

  const roll = new Roll("1d20 + @mod", { mod: skill.value });
  roll.evaluate().then(r => {
    r.toMessage({
      speaker: ChatMessage.getSpeaker({ actor: this.document }),
      flavor: `${skill.label} Check`
    });
  });
}

static async #onCreateItem(event, target) {
  const type = target.dataset.type;
  await this.document.createEmbeddedDocuments("Item", [{
    name: `New ${type.capitalize()}`,
    type: type
  }]);
}

static async #onDeleteItem(event, target) {
  const itemId = target.closest("[data-item-id]").dataset.itemId;
  const item = this.document.items.get(itemId);
  await item.delete();
}
```

Template usage:
```html
<button type="button" data-action="rollSkill" data-skill-id="athletics">
  Roll Athletics
</button>
```

### Tab Navigation (V2)

Four required elements:

**1. Static PARTS with tab templates**
**2. Static TABS configuration**
**3. Prepare tabs in _prepareContext**
**4. Set tab in _preparePartContext**

```html
<!-- Tab content template - MUST include data-group, data-tab, and {{tab.cssClass}} -->
<div class="tab-content {{tab.cssClass}}" data-group="primary" data-tab="description">
  <!-- Content -->
</div>
```

### Drag & Drop (V2)

ActorSheetV2 provides automatic drag/drop for items. Just use:

```html
<li class="item draggable" data-item-id="{{item._id}}">
  <!-- Item content -->
</li>
```

For base ApplicationV2, manual setup required:

```javascript
#dragDrop;

constructor(options = {}) {
  super(options);
  this.#dragDrop = this.options.dragDrop.map(d => {
    d.permissions = {
      dragstart: this._canDragStart.bind(this),
      drop: this._canDragDrop.bind(this)
    };
    d.callbacks = {
      dragstart: this._onDragStart.bind(this),
      drop: this._onDrop.bind(this)
    };
    return new foundry.applications.ux.DragDrop(d);
  });
}

_onRender(context, options) {
  this.#dragDrop.forEach(d => d.bind(this.element));
}
```

## Common Pitfalls

### 1. Forgetting super.activateListeners()

```javascript
// WRONG - breaks base functionality
activateListeners(html) {
  html.on("click", ".rollable", this._onRoll.bind(this));
}

// CORRECT
activateListeners(html) {
  super.activateListeners(html);
  html.on("click", ".rollable", this._onRoll.bind(this));
}
```

### 2. Context Binding Issues

```javascript
// WRONG - loses 'this' context
html.on("click", ".rollable", this._onRoll);

// CORRECT
html.on("click", ".rollable", this._onRoll.bind(this));
```

### 3. Memory Leaks from Global Listeners

```javascript
// WRONG - binds globally on every render
activateListeners(html) {
  super.activateListeners(html);
  $(document).on("click", this._onClick.bind(this));
}

// CORRECT - namespace and unbind first
activateListeners(html) {
  super.activateListeners(html);
  $(document).off("click.mysheet").on("click.mysheet", this._onClick.bind(this));
}

// Clean up on close
close(options) {
  $(document).off("click.mysheet");
  return super.close(options);
}
```

### 4. V2 Static Action Mistakes

```javascript
// WRONG - action handler isn't static
static DEFAULT_OPTIONS = {
  actions: {
    roll: this._onRoll  // Error!
  }
}

// CORRECT - use static private method
static DEFAULT_OPTIONS = {
  actions: {
    roll: this.#onRoll
  }
}

static #onRoll(event, target) {
  // ...
}
```

### 5. V2 Partial Re-render Hook Multiplication

```javascript
// PROBLEM - element added multiple times
Hooks.on("renderMySheet", (app, html, data) => {
  html.append("<div class='custom'></div>");
});

// SOLUTION - check if exists
Hooks.on("renderMySheet", (app, html, data) => {
  if (!html.querySelector(".custom")) {
    html.append("<div class='custom'></div>");
  }
});
```

### 6. Form Data Type Mismatches

```html
<!-- WRONG - saves as string -->
<input type="text" name="system.level" value="{{system.level}}"/>

<!-- CORRECT - saves as number -->
<input type="text" name="system.level" value="{{system.level}}" data-dtype="Number"/>

<!-- Checkbox must use checked helper -->
<input type="checkbox" name="system.equipped" {{checked system.equipped}}/>
```

### 7. Async in V1 vs V2

```javascript
// V1 - getData is sync, use async: false
getData() {
  context.enrichedBio = TextEditor.enrichHTML(bio, { async: false });
  return context;
}

// V2 - _prepareContext is async, use async: true
async _prepareContext(options) {
  context.enrichedBio = await TextEditor.enrichHTML(bio, { async: true });
  return context;
}
```

## Implementation Checklist

### V1 Sheet
- [ ] Extend ActorSheet or ItemSheet
- [ ] Define `static get defaultOptions()` with template, classes, tabs
- [ ] Implement `getData()` returning context object
- [ ] Call `super.activateListeners(html)` first
- [ ] Check `this.isEditable` before binding edit controls
- [ ] Use `.bind(this)` for all event handlers
- [ ] Clean up global event listeners in `close()`

### V2 Sheet
- [ ] Extend ActorSheetV2 with HandlebarsApplicationMixin
- [ ] Define `static DEFAULT_OPTIONS` with `tag: "form"`
- [ ] Define `static PARTS` for each template section
- [ ] Define `static TABS` if using tabs
- [ ] Implement `async _prepareContext()` with `await super._prepareContext()`
- [ ] Implement `_preparePartContext()` for tab data
- [ ] Use `static actions` with `#` prefix handlers
- [ ] Use `.draggable` class and `data-item-id` for drag/drop

## References

- [ActorSheet V1 Tutorial](https://foundryvtt.wiki/en/development/guides/SD-tutorial/SD07-Extending-the-ActorSheet-class)
- [ApplicationV2 Guide](https://foundryvtt.wiki/en/development/api/applicationv2)
- [V2 Conversion Guide](https://foundryvtt.wiki/en/development/guides/applicationV2-conversion-guide)
- [ActorSheetV2 API](https://foundryvtt.com/api/classes/foundry.applications.sheets.ActorSheetV2.html)
- [Tabs in AppV2](https://foundryvtt.wiki/en/development/guides/Tabs-and-Templates/Tabs-in-AppV2)

---

**Last Updated:** 2026-01-04
**Status:** Production-Ready
**Maintainer:** ImproperSubset
