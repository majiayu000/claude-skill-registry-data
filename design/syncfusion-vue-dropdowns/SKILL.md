---
name: syncfusion-vue-dropdowns
description: Comprehensive guide for implementing Syncfusion Vue 3 dropdown components including AutoComplete, ComboBox, DropDownList, ListBox, Mention, MultiSelect, MultiColumn ComboBox, and DropdownTree using Vue Composition API. Use this when building selection interfaces, data binding, filtering, cascading dropdowns, custom templates, hierarchical data selection, and accessible dropdown experiences in Vue 3 applications.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Dropdowns"
---

# Implementing Syncfusion Vue 3 Dropdowns

## Table of Contents

- [AutoComplete Component](#autocomplete-component)
- [ComboBox Component](#combobox-component)
- [DropdownList Component](#dropdownlist-component)
- [ListBox Component](#listbox-component)
- [Mention Component](#mention-component)
- [MultiColumnComboBox Component](#multicolumncombobox-component)
- [MultiSelect Component](#multiselect-component)
- [DropdownTree Component](#dropdowntree-component)
- [Quick Start Examples](#quick-start-examples)
- [Common Patterns](#common-patterns)

---

## AutoComplete Component

The AutoComplete component provides a matched suggestion list as the user types into an input field, allowing selection from the filtered results. It supports local and remote data, rich filtering options, templates, grouping, virtualization, and full accessibility.

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/autocomplete-getting-started.md](references/autocomplete-getting-started.md)
- Package installation (`@syncfusion/ej2-vue-dropdowns`)
- CSS imports and theme configuration
- Basic component setup with Vue 3 Composition API
- Binding a simple string array
- Configuring popup height and width (`:popupHeight`, `:popupWidth`)

#### Data Binding
📄 **Read:** [references/autocomplete-data-binding.md](references/autocomplete-data-binding.md)
- Array of strings or numbers
- Array of objects with `fields` mapping (`:fields="{ value: 'id', text: 'name' }"`)
- Array of complex/nested objects (dot-notation field mapping)
- Remote data with `DataManager` (ODataV4Adaptor, WebApiAdaptor)
- Using `query` property to filter/select remote data
- `sortOrder` for alphabetical ordering

#### Filtering
📄 **Read:** [references/autocomplete-filtering.md](references/autocomplete-filtering.md)
- Filter types: `StartsWith`, `EndsWith`, `Contains`
- `:suggestionCount` – limit number of suggestions
- `:minLength` – minimum characters before search triggers
- `:ignoreCase` – case-sensitive filtering
- `:ignoreAccent` – diacritics filtering
- `:debounceDelay` – delay filtering to reduce requests
- Custom filtering with the `@filtering` event

#### Grouping
📄 **Read:** [references/autocomplete-grouping.md](references/autocomplete-grouping.md)
- Grouping items using `:fields="{ groupBy: 'category' }"`
- Fixed and inline group headers
- Custom group header with `#groupTemplate`

#### Templates
📄 **Read:** [references/autocomplete-templates.md](references/autocomplete-templates.md)
- `#itemTemplate` – customize each list item
- `#groupTemplate` – customize group header
- `#headerTemplate` – static popup header
- `#footerTemplate` – static popup footer
- `#noRecordsTemplate` – message when no data found
- `#actionFailureTemplate` – message on remote fetch failure

#### Value Binding
📄 **Read:** [references/autocomplete-value-binding.md](references/autocomplete-value-binding.md)
- Binding primitive values (string, number)
- Object binding with `:allowObjectBinding="true"`
- Presetting selected values with the `:value` property

#### Virtualization
📄 **Read:** [references/autocomplete-virtual-scroll.md](references/autocomplete-virtual-scroll.md)
- `:enableVirtualization` for large datasets
- Injecting the `VirtualScroll` service
- Virtual scrolling with local data, remote data, and grouping
- Customizing item count with `query.take()`

#### Disabled Items
📄 **Read:** [references/autocomplete-disabled-items.md](references/autocomplete-disabled-items.md)
- Disabling items via `:fields="{ disabled: 'isDisabled' }"`
- `disableItem()` method for dynamic disabling
- Disabling the entire component with `:enabled="false"`

#### Accessibility and Localization
📄 **Read:** [references/autocomplete-accessibility-localization.md](references/autocomplete-accessibility-localization.md)
- WAI-ARIA roles and attributes
- Keyboard navigation shortcuts
- RTL support (`:enableRtl="true"`)
- Localization with `setLocale()`
- WCAG 2.2 compliance overview

#### Styling and Customization
📄 **Read:** [references/autocomplete-styling.md](references/autocomplete-styling.md)
- CSS class targets for wrapper, icon, focus, placeholder, selection
- Float label customization
- Popup item appearance
- `:cssClass` property for custom class injection
- Popup resize (`:allowResize="true"`)
- Mandatory asterisk styling

#### How-To: Autofill, Highlight, and Icons
📄 **Read:** [references/autocomplete-how-to.md](references/autocomplete-how-to.md)
- `:autofill="true"` – suggest first matched item on Arrow Down
- `:highlight="true"` – highlight typed characters in suggestion list
- Icon support with `:fields="{ iconCss: 'icon' }"`

---

## ComboBox Component

ComboBox combines the features of AutoComplete with the ability to select from a dropdown list. It supports data binding, filtering, grouping, templates, cascading operations, and virtual scrolling.

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/combobox-getting-started.md](references/combobox-getting-started.md)
- Installation and setup
- Basic ComboBox implementation
- Binding data arrays
- Popup configuration

#### Data Binding & Search
📄 **Read:** [references/combobox-data-binding.md](references/combobox-data-binding.md)
- Local and remote data sources
- Field mapping with `:fields`
- Search and filter capabilities

#### Filtering & Search
📄 **Read:** [references/combobox-filtering-and-search.md](references/combobox-filtering-and-search.md)
- Filter types and matching
- Custom filtering with events
- Performance optimization

#### Grouping & Sorting
📄 **Read:** [references/combobox-grouping-and-sorting.md](references/combobox-grouping-and-sorting.md)
- Data grouping with `:fields="{ groupBy: 'category' }"`
- Sorting options
- Group templates

#### Templates & Customization
📄 **Read:** [references/combobox-templates-and-customization.md](references/combobox-templates-and-customization.md)
- Item templates with `#itemTemplate`
- Group templates
- Header and footer templates
- Custom styling

#### Styling & Theming
📄 **Read:** [references/combobox-styling-and-theming.md](references/combobox-styling-and-theming.md)
- Theme configuration
- Custom CSS styling
- Responsive design

#### Popup Resizing
📄 **Read:** [references/combobox-popup-resizing.md](references/combobox-popup-resizing.md)
- Enabling popup resize
- Size constraints
- User resizing

#### Advanced Features
📄 **Read:** [references/combobox-advanced-features.md](references/combobox-advanced-features.md)
- Cascading ComboBox
- Virtual scrolling
- Remote data with pagination

#### API Reference
📄 **Read:** [references/combobox-api.md](references/combobox-api.md)
- Complete props, events, and methods
- Usage examples
- Common scenarios

#### How-To Guides
📄 **Read:** [references/combobox-how-to-guide.md](references/combobox-how-to-guide.md)
- Common patterns and solutions
- Troubleshooting

#### Troubleshooting
📄 **Read:** [references/combobox-troubleshooting.md](references/combobox-troubleshooting.md)
- Common issues and solutions

---

## DropdownList Component

DropdownList displays a list of options in a dropdown menu, allowing users to select one value. It supports data binding, filtering, grouping, templates, cascading, and accessibility features.

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/dropdownlist-getting-started.md](references/dropdownlist-getting-started.md)
- Installation and basic setup
- Simple dropdown implementation
- Data binding

#### Data Binding
📄 **Read:** [references/dropdownlist-data-binding.md](references/dropdownlist-data-binding.md)
- Local data arrays
- Remote data sources
- Field mapping

#### Features & Configuration
📄 **Read:** [references/dropdownlist-features-and-configuration.md](references/dropdownlist-features-and-configuration.md)
- Disabled items
- Read-only mode
- Placeholder text
- Popup height

#### Filtering
📄 **Read:** [references/dropdownlist-filtering.md](references/dropdownlist-filtering.md)
- Filter types
- Custom filtering
- Case-insensitive filtering

#### Grouping & Templates
📄 **Read:** [references/dropdownlist-grouping-and-templates.md](references/dropdownlist-grouping-and-templates.md)
- Data grouping
- Item templates
- Group templates

#### Accessibility, Styling, Localization
📄 **Read:** [references/dropdownlist-accessibility-styling-localization.md](references/dropdownlist-accessibility-styling-localization.md)
- WCAG compliance
- Custom styling
- RTL support
- Localization

#### How-To Guides
📄 **Read:** [references/dropdownlist-how-to.md](references/dropdownlist-how-to.md)
- Common scenarios
- Best practices

#### API Reference
📄 **Read:** [references/dropdownlist-api.md](references/dropdownlist-api.md)
- Complete API documentation

---

## ListBox Component

ListBox displays a list of items and allows selection of one or multiple items. It supports data binding, dual-list operations, icons, templates, keyboard navigation, and accessibility.

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/listbox-getting-started.md](references/listbox-getting-started.md)
- Installation and setup
- Basic ListBox implementation

#### Data Binding
📄 **Read:** [references/listbox-data-binding.md](references/listbox-data-binding.md)
- Local and remote data
- Field mapping
- Selection modes

#### Selection
📄 **Read:** [references/listbox-selection.md](references/listbox-selection.md)
- Single selection
- Multiple selection
- Programmatic selection

#### Features
📄 **Read:** [references/listbox-features.md](references/listbox-features.md)
- Disabled items
- Drag and drop
- Tooltips

#### Dual ListBox
📄 **Read:** [references/listbox-dual-list-box.md](references/listbox-dual-list-box.md)
- Dual list implementation
- Move items between lists
- Toolbar operations

#### Icons & Templates
📄 **Read:** [references/listbox-icons-and-templates.md](references/listbox-icons-and-templates.md)
- Icons in list items
- Custom item templates
- Group templates

#### Style & Appearance
📄 **Read:** [references/listbox-style-and-appearance.md](references/listbox-style-and-appearance.md)
- Custom styling
- Theme configuration
- Responsive design

#### Accessibility
📄 **Read:** [references/listbox-accessibility.md](references/listbox-accessibility.md)
- WCAG compliance
- Keyboard navigation
- Screen reader support

#### How-To Guides
📄 **Read:** [references/listbox-how-to-guides.md](references/listbox-how-to-guides.md)
- Common patterns
- Best practices

#### API Reference
📄 **Read:** [references/listbox-api.md](references/listbox-api.md)
- Complete API documentation

---

## Mention Component

Mention provides @mention functionality for text inputs, allowing users to mention items (people, teams, etc.) in content.

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/mention-getting-started.md](references/mention-getting-started.md)
- Installation and setup
- Basic Mention implementation

#### Working with Data
📄 **Read:** [references/mention-working-with-data.md](references/mention-working-with-data.md)
- Data binding
- Field mapping
- Remote data

#### Filtering Data
📄 **Read:** [references/mention-filtering-data.md](references/mention-filtering-data.md)
- Filter options
- Custom filtering
- Performance optimization

#### Templates
📄 **Read:** [references/mention-template.md](references/mention-template.md)
- Item templates
- Custom mention display
- Avatar support

#### Sorting
📄 **Read:** [references/mention-sorting.md](references/mention-sorting.md)
- Sort configurations
- Alphabetical sorting

#### Disabled Items
📄 **Read:** [references/mention-disabled-items.md](references/mention-disabled-items.md)
- Disabling items
- Conditional disabling

#### Customization
📄 **Read:** [references/mention-customization.md](references/mention-customization.md)
- Custom styling
- Popup customization
- Trigger character customization

#### Accessibility
📄 **Read:** [references/mention-accessibility.md](references/mention-accessibility.md)
- WCAG compliance
- Keyboard support
- Screen reader integration

#### Localization
📄 **Read:** [references/mention-localization.md](references/mention-localization.md)
- Language support
- Text localization

#### API Reference
📄 **Read:** [references/mention-api.md](references/mention-api.md)
- Complete API documentation

---

## MultiColumnComboBox Component

MultiColumnComboBox extends ComboBox to display multiple columns of data, useful for complex selections with additional context.

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/multicolumn-combobox-getting-started.md](references/multicolumn-combobox-getting-started.md)
- Installation and setup
- Basic MultiColumnComboBox

#### Columns Configuration
📄 **Read:** [references/multicolumn-combobox-columns.md](references/multicolumn-combobox-columns.md)
- Column definitions
- Column properties
- Width configuration

#### Data Binding
📄 **Read:** [references/multicolumn-combobox-data-binding.md](references/multicolumn-combobox-data-binding.md)
- Local and remote data
- Field mapping

#### Filtering
📄 **Read:** [references/multicolumn-combobox-filtering.md](references/multicolumn-combobox-filtering.md)
- Filter types
- Multi-column filtering

#### Grouping
📄 **Read:** [references/multicolumn-combobox-grouping.md](references/multicolumn-combobox-grouping.md)
- Data grouping
- Group headers

#### Sorting
📄 **Read:** [references/multicolumn-combobox-sorting.md](references/multicolumn-combobox-sorting.md)
- Sort configurations
- Multi-column sorting

#### Items Management
📄 **Read:** [references/multicolumn-combobox-items.md](references/multicolumn-combobox-items.md)
- Adding items
- Removing items
- Updating items

#### Templates
📄 **Read:** [references/multicolumn-combobox-templates.md](references/multicolumn-combobox-templates.md)
- Custom cell templates
- Header templates
- Row templates

#### Virtualization
📄 **Read:** [references/multicolumn-combobox-virtualization.md](references/multicolumn-combobox-virtualization.md)
- Virtual scrolling
- Performance optimization

#### Events
📄 **Read:** [references/multicolumn-combobox-events.md](references/multicolumn-combobox-events.md)
- Event handling
- Event args

#### Accessibility
📄 **Read:** [references/multicolumn-combobox-accessibility.md](references/multicolumn-combobox-accessibility.md)
- WCAG compliance
- Keyboard navigation

#### Localization
📄 **Read:** [references/multicolumn-combobox-localization.md](references/multicolumn-combobox-localization.md)
- Language support
- RTL support

#### API Reference
📄 **Read:** [references/multicolumn-combobox-api.md](references/multicolumn-combobox-api.md)
- Complete API documentation

---

## MultiSelect Component

MultiSelect allows users to select multiple values from a dropdown list. It supports templates, grouping, search, filtering, tagging, and accessibility features.

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/multiselect-getting-started.md](references/multiselect-getting-started.md)
- Installation and setup
- Basic MultiSelect implementation

#### Data Binding
📄 **Read:** [references/multiselect-data-binding.md](references/multiselect-data-binding.md)
- Local and remote data
- Field mapping
- Array binding

#### Selection & Features
📄 **Read:** [references/multiselect-selection-and-features.md](references/multiselect-selection-and-features.md)
- Selection modes
- Tags management
- Placeholder text

#### Filtering
📄 **Read:** [references/multiselect-filtering.md](references/multiselect-filtering.md)
- Filter types
- Custom filtering
- Search

#### Grouping
📄 **Read:** [references/multiselect-grouping.md](references/multiselect-grouping.md)
- Data grouping
- Group headers
- Hierarchical grouping

#### Templates
📄 **Read:** [references/multiselect-templates.md](references/multiselect-templates.md)
- Item templates
- Tag templates
- Custom rendering

#### Accessibility, Styling, Localization
📄 **Read:** [references/multiselect-accessibility-styling-localization.md](references/multiselect-accessibility-styling-localization.md)
- WCAG compliance
- Custom styling
- RTL support
- Localization

#### API Reference
📄 **Read:** [references/multiselect-api.md](references/multiselect-api.md)
- Complete API documentation

---

## DropdownTree Component

The Dropdown Tree component displays hierarchical data in a collapsible tree structure within a dropdown interface. It combines tree navigation with dropdown accessibility, supporting multi-selection via checkboxes, lazy loading for large datasets, comprehensive customization through templates and events, filtering, and full accessibility with RTL and localization support.

### When to Use DropdownTree

Use DropdownTree **immediately** when you need to:

- **Display hierarchical data** - Show nested categories, organizational structures, file trees, or department hierarchies
- **Enable multi-selection** - Allow users to select multiple items with checkbox support or keyboard modifiers
- **Support lazy loading** - Optimize performance with large datasets by loading children on demand
- **Customize display** - Use templates to format items, headers, footers, selected values, or error states
- **Implement filtering** - Enable search functionality with configurable filter types (StartsWith, EndsWith, Contains)
- **Ensure accessibility** - Provide WAI-ARIA compliance, keyboard navigation, and screen reader support
- **Support multiple languages** - Localize UI with customizable keys and RTL support
- **Bind remote data** - Integrate with OData, OData V4, Web APIs, or other remote data services
- **Handle complex selection logic** - Use events, auto-check hierarchy, or selective node disabling

### DropdownTree Features

- **Hierarchical display**: Local (hierarchical/self-referential) and remote data sources with flexible binding
- **Multi-selection modes**: Checkboxes with auto-check, multi-select with Ctrl/Shift keys, single select (default)
- **Flexible templates**: Item, value, header, footer, noRecords, and actionFailure templates for custom rendering
- **Performance optimization**: Lazy loading (load-on-demand) for efficient large dataset handling
- **Search & filtering**: Built-in filter bar with configurable filter types and case sensitivity options
- **Comprehensive events**: change, select, dataBound, filtering, beforeOpen, focus, keyPress, and popup events
- **Accessibility**: Full WAI-ARIA (roles, attributes), keyboard navigation, screen reader support, WCAG 2.2 compliance
- **Localization**: Multi-language support with 4 customizable keys and locale override
- **RTL support**: Right-to-left layout rendering
- **Tree settings**: Advanced configuration (expandOn, autoCheck, loadOnDemand, checkDisabledChildren)
- **Field mapping**: Flexible data structure support (value, text, child, parentValue, expanded, hasChildren, selectable, iconCss, imageUrl, htmlAttributes)
- **Display modes**: Default, Delimiter, and Custom modes for selected items

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/dropdowntree-getting-started.md](references/dropdowntree-getting-started.md)
- Installation and package dependencies (npm install command)
- Vue 3/TypeScript project setup (Vite and Create Vue)
- Basic component implementation and initialization with Composition API
- CSS imports and theme configuration
- First render and minimal working example

#### Data Binding
📄 **Read:** [references/dropdowntree-data-binding.md](references/dropdowntree-data-binding.md)
- Local data binding (hierarchical and self-referential structures)
- Remote data with DataManager and various adaptors (OData, OData V4, WebAPI, URL)
- Field mapping for value, text, child, parentValue, expanded, hasChildren
- Load on demand (lazy loading) for large datasets
- Preventing node selection with selectable field
- Query configuration for remote data services

#### Checkbox & Multi-Selection
📄 **Read:** [references/dropdowntree-checkbox-selection.md](references/dropdowntree-checkbox-selection.md)
- Enabling checkbox support with `:showCheckBox` property
- Multi-selection workflow and accessing selected values with ref()
- Auto-check hierarchical behavior (parent-child synchronization)
- Select All feature with customizable `:selectAllText` and `:unSelectAllText`
- Intermediate checkbox states for partial selection
- CheckDisabledChildren behavior for disabled nodes

#### Templates
📄 **Read:** [references/dropdowntree-templates.md](references/dropdowntree-templates.md)
- Item template for custom list item rendering using scoped slots
- Value template for selected display customization
- Header template for static content above items
- Footer template for static content below items
- NoRecords template for empty state handling
- ActionFailure template for error state handling
- CustomTemplate for multi-select display customization
- Template expression syntax and data access patterns in Vue

#### Multi-Selection & Filtering
📄 **Read:** [references/dropdowntree-multi-selection-filtering.md](references/dropdowntree-multi-selection-filtering.md)
- `:allowMultiSelection` property and Ctrl/Shift keyboard interaction
- Display modes: Default, Delimiter, Custom
- `:delimiterChar` and `:mode` configuration
- `:allowFiltering` and filter bar implementation
- Filter types: StartsWith, EndsWith, Contains
- `:filterBarPlaceholder` customization
- `:ignoreCase` and `:ignoreAccent` options

#### Tree Settings & Configuration
📄 **Read:** [references/dropdowntree-tree-settings.md](references/dropdowntree-tree-settings.md)
- `:loadOnDemand` for lazy loading implementation
- `:autoCheck` for hierarchical checkbox synchronization
- `:expandOn` behavior (Auto, Click, DblClick, None)
- `:checkDisabledChildren` for disabled node handling
- Tree expansion and collapse control

#### Field Mapping & Custom Data Structures
📄 **Read:** [references/dropdowntree-field-mapping.md](references/dropdowntree-field-mapping.md)
- Core fields: value, text, dataSource, child, parentValue
- Node state fields: expanded, hasChildren, selected, selectable
- Display enhancement fields: iconCss, imageUrl, htmlAttributes
- Query and tableName for remote data
- Nested field mapping for hierarchical data

#### Advanced Features & API Reference
📄 **Read:** [references/dropdowntree-advanced-features.md](references/dropdowntree-advanced-features.md)
- Properties (60+ properties with descriptions and examples)
- Methods (getSelectedNodes, getCheckedNodes, setCheckedNodes, etc.)
- Events (change, select, dataBound, filtering, beforeOpen, focus, keyPress, popup)
- Event arguments (EventArgs structures with property descriptions)
- Styling and CSS customization
- Performance optimization techniques

#### Accessibility & Localization
📄 **Read:** [references/dropdowntree-accessibility-localization.md](references/dropdowntree-accessibility-localization.md)
- WCAG 2.2 and Section 508 compliance standards
- WAI-ARIA attributes and roles (listbox, treeitem, checkbox, group, etc.)
- Keyboard navigation shortcuts (Alt+Down, Arrow keys, Enter, Space, etc.)
- Screen reader and assistive technology support
- Localization keys (noRecordsTemplate, actionFailureTemplate, overflowCountTemplate, totalCountTemplate)
- Culture customization with locale property
- RTL (Right-to-Left) language support with enableRtl

### DropdownTree Quick Start

#### Basic Dropdown Tree with Hierarchical Data

```vue
<template>
  <DropDownTreeComponent
    id="dropdowntree"
    :fields="fields"
    placeholder="Select an item"
  />
</template>

<script setup>
import { DropDownTreeComponent } from '@syncfusion/ej2-vue-dropdowns';
import '@syncfusion/ej2-dropdowns/styles/material.css';

const data = [
  { id: '1', name: 'Electronics', expanded: true },
  { id: '2', name: 'Laptops', parentId: '1' },
  { id: '3', name: 'Phones', parentId: '1' },
  { id: '4', name: 'Appliances' },
];

const fields = {
  dataSource: data,
  value: 'id',
  text: 'name',
  parentValue: 'parentId',
  hasChildren: 'hasChild'
};
</script>
```

#### With Multi-Select Checkboxes

```vue
<template>
  <DropDownTreeComponent
    id="dropdowntree"
    :fields="fields"
    :showCheckBox="true"
    :autoCheck="true"
    @change="onSelectionChange"
    placeholder="Select multiple items"
  />
</template>

<script setup>
import { ref } from 'vue';
import { DropDownTreeComponent } from '@syncfusion/ej2-vue-dropdowns';

const selectedValues = ref([]);

const onSelectionChange = (event) => {
  selectedValues.value = event.value || [];
  console.log('Selected:', selectedValues.value);
};

// ... rest of component code
</script>
```

---

## Quick Start Examples

### AutoComplete

```vue
<template>
  <ejs-autocomplete
    :dataSource="countries"
    :fields="{ text: 'Name', value: 'Code' }"
    :value="selectedCountry"
    placeholder="Select a country"
    @change="onCountryChange"
  ></ejs-autocomplete>
</template>

<script setup>
import { ref } from 'vue';
import { AutoCompleteComponent } from '@syncfusion/ej2-vue-dropdowns';

const selectedCountry = ref('');
const countries = ref([
  { Name: 'Australia', Code: 'AU' },
  { Name: 'Austria', Code: 'AT' },
  { Name: 'Belgium', Code: 'BE' }
]);

const onCountryChange = (args) => {
  selectedCountry.value = args.value;
};
</script>
```

### ComboBox

```vue
<template>
  <ejs-combobox
    :dataSource="employees"
    :fields="{ text: 'name', value: 'id' }"
    :value="selectedEmployee"
    placeholder="Select employee"
    @change="onEmployeeChange"
  ></ejs-combobox>
</template>

<script setup>
import { ref } from 'vue';
import { ComboBoxComponent } from '@syncfusion/ej2-vue-dropdowns';

const selectedEmployee = ref('');
const employees = ref([
  { id: 1, name: 'John Smith' },
  { id: 2, name: 'Jane Doe' },
  { id: 3, name: 'Bob Johnson' }
]);

const onEmployeeChange = (args) => {
  selectedEmployee.value = args.value;
};
</script>
```

### DropdownList

```vue
<template>
  <ejs-dropdownlist
    :dataSource="statusOptions"
    :value="selectedStatus"
    placeholder="Select status"
    @change="onStatusChange"
  ></ejs-dropdownlist>
</template>

<script setup>
import { ref } from 'vue';
import { DropDownListComponent } from '@syncfusion/ej2-vue-dropdowns';

const selectedStatus = ref('');
const statusOptions = ref(['Active', 'Inactive', 'Pending']);

const onStatusChange = (args) => {
  selectedStatus.value = args.value;
};
</script>
```

### MultiSelect

```vue
<template>
  <ejs-multiselect
    :dataSource="fruits"
    :value="selectedFruits"
    placeholder="Select fruits"
    :showSelectAll="true"
    @change="onFruitsChange"
  ></ejs-multiselect>
</template>

<script setup>
import { ref } from 'vue';
import { MultiSelectComponent } from '@syncfusion/ej2-vue-dropdowns';

const selectedFruits = ref([]);
const fruits = ref(['Apple', 'Banana', 'Cherry', 'Date']);

const onFruitsChange = (args) => {
  selectedFruits.value = args.value;
};
</script>
```

---

## Common Patterns

### Data Binding with Objects

```vue
<script setup>
const cities = ref([
  { id: 1, name: 'New York', state: 'NY' },
  { id: 2, name: 'Los Angeles', state: 'CA' }
]);
</script>

<template>
  <ejs-combobox
    :dataSource="cities"
    :fields="{ text: 'name', value: 'id' }"
  ></ejs-combobox>
</template>
```

### Cascading Dropdowns

```vue
<script setup>
import { ref, computed } from 'vue';

const countries = ref([...]);
const statesByCountry = ref({...});
const selectedCountry = ref('');
const selectedState = ref('');

const availableStates = computed(() => {
  return statesByCountry.value[selectedCountry.value] || [];
});

const onCountryChange = (args) => {
  selectedCountry.value = args.value;
  selectedState.value = '';
};
</script>
```

### Remote Data with Filtering

```vue
<script setup>
import { DataManager, Query, ODataV4Adaptor } from '@syncfusion/ej2-data';

const remoteData = ref(
  new DataManager({
    url: 'https://services.odata.org/V4/Northwind/Northwind.svc/Customers',
    adaptor: new ODataV4Adaptor(),
    crossDomain: true
  })
);

const query = ref(new Query().select(['CustomerID', 'ContactName']).take(10));
</script>
```

### Template Usage

```vue
<template>
  <ejs-combobox :dataSource="employees">
    <template #itemTemplate="{ data }">
      <div class="flex items-center gap-2">
        <img :src="data.avatar" class="w-6 h-6 rounded-full" />
        <div>
          <div>{{ data.name }}</div>
          <div class="text-sm text-gray-600">{{ data.email }}</div>
        </div>
      </div>
    </template>
  </ejs-combobox>
</template>
```

---

## Installation & Setup

### Install Package

```bash
npm install @syncfusion/ej2-vue-dropdowns --save
```

### Import CSS Themes

In `src/main.ts`:

```typescript
// Choose one theme
import '@syncfusion/ej2-base/styles/material3.css';
import '@syncfusion/ej2-inputs/styles/material3.css';
import '@syncfusion/ej2-dropdowns/styles/material3.css';

// Or use other themes: bootstrap5, tailwind3, fabric, fluent
```

### Register Component (Optional)

In `src/main.ts`:

```typescript
import { createApp } from 'vue';
import { AutoCompleteComponent, ComboBoxComponent, DropDownListComponent } from '@syncfusion/ej2-vue-dropdowns';

const app = createApp(App);
app.component('EjsAutocomplete', AutoCompleteComponent);
app.component('EjsCombobox', ComboBoxComponent);
app.component('EjsDropdownlist', DropDownListComponent);
app.mount('#app');
```

---

## Next Steps

1. **Choose Component**: Pick the dropdown component that best fits your use case (AutoComplete, ComboBox, DropdownList, ListBox, etc.)
2. **Read Getting Started**: Start with the component's Getting Started guide
3. **Explore Features**: Read feature-specific guides for filtering, grouping, templates, etc.
4. **Customize**: Use styling and customization guides
5. **Add Accessibility**: Ensure WCAG compliance with accessibility guides
6. **Reference API**: Consult API documentation for complete prop/event lists

---

## Status

✅ **Production Ready** - All components fully documented for Vue 3 Composition API

**Last Updated**: 2026  
**Framework**: Vue 3 with Composition API  
**Components**: 8 (AutoComplete, ComboBox, DropdownList, ListBox, Mention, MultiColumnComboBox, MultiSelect, DropdownTree)
