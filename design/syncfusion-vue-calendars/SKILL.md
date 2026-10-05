---
name: syncfusion-vue-calendars
description: Comprehensive guide for implementing Syncfusion Vue Calendar components including Calendar, DatePicker, DateRangePicker, DateTimePicker, and TimePicker. Covers installation, data binding, date/time selection, range selection, formatting, localization, masking, validation, customization, templates, accessibility, and reactive data patterns in Vue 3 applications using Composition API.
metadata:
  author: "Syncfusion Inc"
  category: "Calendars"
  version: "34.1.29"
---

# Implementing Syncfusion Vue Calendars

## Calendar

The Syncfusion Vue **CalendarComponent** is a highly customizable calendar UI control that allows users to select single or multiple dates. It supports multiple views (Month, Year, Decade), navigation, week numbers, disabled dates, custom day cell rendering, localization, RTL support, and full accessibility (WCAG 2.2 compliant).

### Quick Start (Vue 3)

#### Install

```bash
npm install @syncfusion/ej2-vue-calendars @syncfusion/ej2-base
```

#### Basic Example (App.vue)

```vue
<template>
  <div style="padding: 20px">
    <h3>Select a date</h3>
    <ejs-calendar
      :value="selectedDate"
      @change="onChange"
    ></ejs-calendar>
    <p>Selected: {{ selectedDate?.toDateString() }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { CalendarComponent } from '@syncfusion/ej2-vue-calendars';
import '@syncfusion/ej2-base/styles/material3.css';
import '@syncfusion/ej2-calendars/styles/material3.css';

const selectedDate = ref(new Date());

const onChange = (args) => {
  selectedDate.value = args.value || args;
};
</script>
```

**Notes:**
- Use the `@change` event to sync selected date to Vue ref state.
- Import theme CSS once (global or component-level) to style the control.
- `ejs-calendar` is the kebab-case version of `CalendarComponent`.

### Guidance & Patterns

- **Reactive state:** use `ref()` for the date value and update via `@change` event.
- **Multi-selection:** use `:isMultiSelection="true"` with `:values` prop and `addDate()`/`removeDate()` methods via `ref`.
- **Template refs:** use `ref` attribute to access component methods like `navigateTo(view, date)` — both arguments are required.
- **Date ranges:** for range selection, use DateRangePicker (separate component). The Calendar itself does not have a built-in range highlight mode.
- **Accessibility:** use wrapper elements with `role="region"` and a separate `aria-live` region for announcements — these are not direct Calendar props.
- **Week numbers:** enable with `:weekNumber="true"` (the correct prop name).

### References

Navigate to the reference that matches your current task:

#### Getting Started
📄 **Read:** [references/calendar-getting-started-vue.md](references/calendar-getting-started-vue.md)
- Installation and npm setup
- Vue 3 component examples with Composition API
- CSS/theme imports
- Using template refs and methods

#### Date Selection
📄 **Read:** [references/calendar-date-selection.md](references/calendar-date-selection.md)
- Single date selection
- Multiple dates and ranges
- Min/max constraints
- Disabling specific dates

#### Calendar Views
📄 **Read:** [references/calendar-calendar-views.md](references/calendar-calendar-views.md)
- Month, Year, Decade views
- Navigating between views
- Initial and depth controls
- Programmatic navigation

#### Styling & Customization
📄 **Read:** [references/calendar-styling-customization.md](references/calendar-styling-customization.md)
- Theme selection and switching
- CSS class customization
- Custom day cell rendering
- RTL and responsive design

#### Events & Methods
📄 **Read:** [references/calendar-events-methods.md](references/calendar-events-methods.md)
- Event handlers (change, created, renderDayCell)
- Using template refs and imperative methods
- Advanced renderDayCell hook
- Event tracking patterns

#### Accessibility & Globalization
📄 **Read:** [references/calendar-accessibility-globalization.md](references/calendar-accessibility-globalization.md)
- WCAG 2.1 compliance
- Localization and locale configuration
- RTL (right-to-left) support
- Keyboard navigation

---

## DatePicker

The Syncfusion Vue **DatePickerComponent** provides an input field with dropdown calendar picker. It supports formatted input, keyboard navigation, range constraints, date masking, strict mode, accessibility, and full customization.

### Quick Start (Vue 3)

#### Install

```bash
npm install @syncfusion/ej2-vue-calendars @syncfusion/ej2-base
```

#### Basic Example (App.vue)

```vue
<template>
  <div style="padding: 20px">
    <h3>Pick a date</h3>
    <ejs-datepicker
      :value="selectedDate"
      @change="onChange"
    ></ejs-datepicker>
    <p>Selected: {{ selectedDate?.toDateString() }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { DatePickerComponent } from '@syncfusion/ej2-vue-calendars';
import '@syncfusion/ej2-base/styles/material3.css';
import '@syncfusion/ej2-buttons/styles/material3.css';
import '@syncfusion/ej2-inputs/styles/material3.css';
import '@syncfusion/ej2-popups/styles/material3.css';
import '@syncfusion/ej2-calendars/styles/material3.css';

const selectedDate = ref(new Date());

const onChange = (args) => {
  selectedDate.value = args.value || args;
};
</script>
```

**Notes:**
- DatePicker includes an input field with a dropdown calendar.
- Use `@change` event to capture date selection.
- Import multiple CSS files for proper styling (buttons, inputs, popups, calendars).

### Guidance & Patterns

- **Format control:** use `:format` prop to define date input format (e.g., "dd/MM/yyyy").
- **Date masking:** use `:strictMode="false"` to enable partial input validation (default is true).
- **Min/Max ranges:** use `:min` and `:max` props to restrict selectable dates.
- **Placeholder text:** use `:placeholder` prop to guide user input.
- **Readonly state:** use `:readonly="true"` to display-only mode (calendar still opens).
- **Disabled state:** use `:disabled="true"` to fully disable the component.

### References

Navigate to the reference that matches your current task:

#### Getting Started
📄 **Read:** [references/datepicker-getting-started.md](references/datepicker-getting-started.md)
- Installation and setup
- Vue 3 component examples with Composition API
- CSS theme imports
- Running the application

#### Date Formats & Input
📄 **Read:** [references/datepicker-date-formats-and-input.md](references/datepicker-date-formats-and-input.md)
- Input format configuration
- Date string parsing
- Locale-specific formats
- Custom format examples

#### Date Views & Navigation
📄 **Read:** [references/datepicker-date-views-and-navigation.md](references/datepicker-date-views-and-navigation.md)
- Month, Year, Decade views
- Depth and start view control
- Programmatic navigation
- View transitions

#### Date Range & Validation
📄 **Read:** [references/datepicker-date-range-and-validation.md](references/datepicker-date-range-and-validation.md)
- Min/Max date constraints
- Disabling specific dates
- Input validation patterns
- Date range restrictions

#### Date Masking & Strict Mode
📄 **Read:** [references/datepicker-date-masking-and-strict-mode.md](references/datepicker-date-masking-and-strict-mode.md)
- Masking behavior and configuration
- Strict vs loose validation
- Error handling
- Input sanitization

#### Customization & Styling
📄 **Read:** [references/datepicker-customization-and-styling.md](references/datepicker-customization-and-styling.md)
- Theme selection and switching
- CSS customization
- Placeholder and button styling
- Responsive design

#### Accessibility & Keyboard
📄 **Read:** [references/datepicker-accessibility-and-keyboard.md](references/datepicker-accessibility-and-keyboard.md)
- WCAG 2.1 compliance
- Keyboard shortcuts
- ARIA labels
- Screen reader support

#### Globalization & Localization
📄 **Read:** [references/datepicker-globalization-and-localization.md](references/datepicker-globalization-and-localization.md)
- Locale configuration
- RTL support
- Language-specific formatting
- Culture-specific patterns

---

## DateRangePicker

The Syncfusion Vue **DateRangePickerComponent** allows users to select a date range with two input fields and a visual range selector. It supports range validation, formatted output, preset ranges, and full customization.

### Quick Start (Vue 3)

#### Basic Example (App.vue)

```vue
<template>
  <div style="padding: 20px">
    <h3>Select a date range</h3>
    <ejs-daterangepicker
      :startDate="dateRange.start"
      :endDate="dateRange.end"
      @change="onRangeChange"
    ></ejs-daterangepicker>
    <p>
      Start: {{ dateRange.start?.toDateString() }}<br>
      End: {{ dateRange.end?.toDateString() }}
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { DateRangePickerComponent } from '@syncfusion/ej2-vue-calendars';
import '@syncfusion/ej2-base/styles/material3.css';
import '@syncfusion/ej2-buttons/styles/material3.css';
import '@syncfusion/ej2-inputs/styles/material3.css';
import '@syncfusion/ej2-popups/styles/material3.css';
import '@syncfusion/ej2-calendars/styles/material3.css';

const dateRange = ref({
  start: new Date(2026, 0, 1),
  end: new Date(2026, 0, 31)
});

const onRangeChange = (args) => {
  dateRange.value = {
    start: args.startDate,
    end: args.endDate
  };
};
</script>
```

### Guidance & Patterns

- **Range selection:** use `:startDate` and `:endDate` props separately.
- **Preset ranges:** configure quick-select buttons for common ranges (Today, This Month, etc.).
- **Format control:** use `:format` and `:range-format` props for date formatting.
- **Min/Max constraints:** use `:min` and `:max` to restrict the range window.

### References

Navigate to the reference that matches your current task:

#### Getting Started
📄 **Read:** [references/daterangepicker-getting-started.md](references/daterangepicker-getting-started.md)
- Installation and setup
- Vue 3 Composition API examples
- CSS imports
- Basic range selection

#### Date Range Selection
📄 **Read:** [references/daterangepicker-date-range-selection.md](references/daterangepicker-date-range-selection.md)
- Start/End date binding
- Range validation
- Programmatic range setting
- Edge cases and constraints

#### Date Range Formatting
📄 **Read:** [references/daterangepicker-date-range-formatting.md](references/daterangepicker-date-range-formatting.md)
- Output format configuration
- Locale-specific formatting
- Custom range display
- Date serialization

#### Advanced Patterns
📄 **Read:** [references/daterangepicker-advanced-patterns.md](references/daterangepicker-advanced-patterns.md)
- Preset ranges (Today, This Week, This Month, etc.)
- Dynamic range constraints
- Range highlighting
- Multi-range selection patterns

#### Events & Methods
📄 **Read:** [references/daterangepicker-events-and-methods.md](references/daterangepicker-events-and-methods.md)
- Event handlers (change, created, renderDayCell)
- Template ref methods
- Range validation events
- Custom event handling

#### Customization & Styling
📄 **Read:** [references/daterangepicker-customization-and-styling.md](references/daterangepicker-customization-and-styling.md)
- Theme application
- CSS customization
- Input field styling
- Responsive design

#### API Reference
📄 **Read:** [references/daterangepicker-api-reference.md](references/daterangepicker-api-reference.md)
- Complete props and events list
- Methods and method signatures
- Type definitions
- Quick reference table

---

## DateTimePicker

The Syncfusion Vue **DateTimePickerComponent** combines date and time selection in a single input. It supports time configuration, 12/24-hour formats, minute/second intervals, and full customization.

### Quick Start (Vue 3)

#### Basic Example (App.vue)

```vue
<template>
  <div style="padding: 20px">
    <h3>Pick a date and time</h3>
    <ejs-datetimepicker
      :value="selectedDateTime"
      @change="onChange"
    ></ejs-datetimepicker>
    <p>Selected: {{ selectedDateTime?.toString() }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { DateTimePickerComponent } from '@syncfusion/ej2-vue-calendars';
import '@syncfusion/ej2-base/styles/material3.css';
import '@syncfusion/ej2-buttons/styles/material3.css';
import '@syncfusion/ej2-inputs/styles/material3.css';
import '@syncfusion/ej2-popups/styles/material3.css';
import '@syncfusion/ej2-calendars/styles/material3.css';

const selectedDateTime = ref(new Date());

const onChange = (args) => {
  selectedDateTime.value = args.value || args;
};
</script>
```

### Guidance & Patterns

- **Time format:** use `:format` prop to control display (e.g., "dd/MM/yyyy hh:mm a").
- **Step intervals:** use `:step` prop to control minute/second intervals.
- **Min/Max time:** use `:min` and `:max` to constrain valid times per day.
- **Readonly:** use `:readonly="true"` for display-only mode.

### References

Navigate to the reference that matches your current task:

#### Getting Started
📄 **Read:** [references/datetimepicker-getting-started.md](references/datetimepicker-getting-started.md)
- Installation and setup
- Vue 3 component examples
- CSS imports
- Component initialization

#### Date-Time Selection
📄 **Read:** [references/datetimepicker-date-time-selection.md](references/datetimepicker-date-time-selection.md)
- Date and time binding
- Reactive updates
- Value synchronization
- State management patterns

#### Time Configuration
📄 **Read:** [references/datetimepicker-time-configuration.md](references/datetimepicker-time-configuration.md)
- Time step/interval configuration
- 12-hour and 24-hour formats
- Default time settings
- Time boundary constraints

#### API Reference
📄 **Read:** [references/datetimepicker-api-reference.md](references/datetimepicker-api-reference.md)
- Complete props and events
- Methods and signatures
- Type definitions
- Quick reference

#### Events & Methods
📄 **Read:** [references/datetimepicker-events-and-methods.md](references/datetimepicker-events-and-methods.md)
- Event handlers (change, created, destroyed)
- Method calls via template refs
- Event callback patterns
- Lifecycle hooks

#### Styling & Customization
📄 **Read:** [references/datetimepicker-styling-and-customization.md](references/datetimepicker-styling-and-customization.md)
- Theme selection
- CSS customization
- Component styling
- Responsive design

#### Advanced Features
📄 **Read:** [references/datetimepicker-advanced-features.md](references/datetimepicker-advanced-features.md)
- Custom time filtering
- Date range + time constraints
- Preset date-time selections
- Complex state management

#### Accessibility
📄 **Read:** [references/datetimepicker-accessibility.md](references/datetimepicker-accessibility.md)
- WCAG 2.1 compliance
- Keyboard navigation
- Screen reader support
- ARIA labels and roles

---

## TimePicker

The Syncfusion Vue **TimePickerComponent** is a dedicated time-only picker with 12/24-hour support, minute/second intervals, and full keyboard navigation.

### Quick Start (Vue 3)

#### Basic Example (App.vue)

```vue
<template>
  <div style="padding: 20px">
    <h3>Pick a time</h3>
    <ejs-timepicker
      :value="selectedTime"
      @change="onChange"
    ></ejs-timepicker>
    <p>Selected time: {{ selectedTime?.toString() }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { TimePickerComponent } from '@syncfusion/ej2-vue-calendars';
import '@syncfusion/ej2-base/styles/material3.css';
import '@syncfusion/ej2-buttons/styles/material3.css';
import '@syncfusion/ej2-inputs/styles/material3.css';
import '@syncfusion/ej2-popups/styles/material3.css';
import '@syncfusion/ej2-calendars/styles/material3.css';

const selectedTime = ref(new Date());

const onChange = (args) => {
  selectedTime.value = args.value || args;
};
</script>
```

### Guidance & Patterns

- **Time format:** use `:format` prop for 12/24-hour display (e.g., "hh:mm a" or "HH:mm").
- **Step intervals:** use `:step` prop to set minute/second increments.
- **Min/Max time:** use `:min` and `:max` to restrict available times.
- **List of times:** use `:value` with an array to show preset time options.

### References

Navigate to the reference that matches your current task:

#### Getting Started
📄 **Read:** [references/timepicker-getting-started.md](references/timepicker-getting-started.md)
- Installation and setup
- Vue 3 examples
- CSS imports
- Basic time selection

#### Time Format & Display
📄 **Read:** [references/timepicker-time-format-and-display.md](references/timepicker-time-format-and-display.md)
- Time format configuration
- 12-hour and 24-hour modes
- Display customization
- Locale-specific formats

#### Time Range & Selection
📄 **Read:** [references/timepicker-time-range-and-selection.md](references/timepicker-time-range-and-selection.md)
- Min/Max time constraints
- Time range restrictions
- Preset time lists
- Range validation

#### Events & Methods
📄 **Read:** [references/timepicker-events-and-methods.md](references/timepicker-events-and-methods.md)
- Event handlers
- Template ref methods
- Event tracking
- Lifecycle management

#### Customization & Styling
📄 **Read:** [references/timepicker-customization-and-styling.md](references/timepicker-customization-and-styling.md)
- Theme application
- CSS customization
- Input styling
- Responsive design

#### Advanced Patterns
📄 **Read:** [references/timepicker-advanced-patterns.md](references/timepicker-advanced-patterns.md)
- Custom time lists
- Time filtering logic
- Combined date-time patterns
- Advanced scenarios

---

## Common Scenarios & Patterns

### Scenario 1: Controlled Date Input with Validation

```vue
<template>
  <div style="padding: 20px">
    <ejs-datepicker
      :value="date"
      :min="minDate"
      :max="maxDate"
      @change="handleDateChange"
    ></ejs-datepicker>
    <p v-if="error" style="color: red">{{ error }}</p>
    <p>Selected: {{ date?.toDateString() }}</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { DatePickerComponent } from '@syncfusion/ej2-vue-calendars';

const date = ref(new Date());
const minDate = ref(new Date(2026, 0, 1));
const maxDate = ref(new Date(2026, 11, 31));
const error = ref('');

const handleDateChange = (args) => {
  if (args.value < minDate.value || args.value > maxDate.value) {
    error.value = 'Date outside allowed range';
  } else {
    error.value = '';
    date.value = args.value;
  }
};
</script>
```

### Scenario 2: Multiple Date Selection

```vue
<template>
  <div style="padding: 20px">
    <ejs-calendar
      :isMultiSelection="true"
      :values="selectedDates"
      @change="handleDatesChange"
    ></ejs-calendar>
    <h4>Selected Dates:</h4>
    <ul>
      <li v-for="(d, i) in selectedDates" :key="i">
        {{ d.toDateString() }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { CalendarComponent } from '@syncfusion/ej2-vue-calendars';

const selectedDates = ref([
  new Date(2026, 10, 5),
  new Date(2026, 10, 12)
]);

const handleDatesChange = (args) => {
  if (args.values) {
    selectedDates.value = args.values;
  }
};
</script>
```

### Scenario 3: Date Range with Preset Options

```vue
<template>
  <div style="padding: 20px">
    <div style="margin-bottom: 20px">
      <button @click="setRange('today')">Today</button>
      <button @click="setRange('thisWeek')">This Week</button>
      <button @click="setRange('thisMonth')">This Month</button>
    </div>
    <ejs-daterangepicker
      :startDate="range.start"
      :endDate="range.end"
      @change="handleRangeChange"
    ></ejs-daterangepicker>
    <p>
      {{ range.start?.toDateString() }} to {{ range.end?.toDateString() }}
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { DateRangePickerComponent } from '@syncfusion/ej2-vue-calendars';

const range = ref({
  start: new Date(2026, 0, 1),
  end: new Date(2026, 0, 31)
});

const setRange = (type) => {
  const today = new Date();
  const startOfWeek = new Date(today);
  startOfWeek.setDate(today.getDate() - today.getDay());
  const endOfWeek = new Date(startOfWeek);
  endOfWeek.setDate(startOfWeek.getDate() + 6);
  
  const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
  const endOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0);

  if (type === 'today') {
    range.value = { start: today, end: today };
  } else if (type === 'thisWeek') {
    range.value = { start: startOfWeek, end: endOfWeek };
  } else if (type === 'thisMonth') {
    range.value = { start: startOfMonth, end: endOfMonth };
  }
};

const handleRangeChange = (args) => {
  range.value = {
    start: args.startDate,
    end: args.endDate
  };
};
</script>
```

---

## Migration Notes from React

### Key Differences:

1. **Component Tags:** Use kebab-case (`ejs-calendar`, `ejs-datepicker`) instead of PascalCase
2. **State Management:** Use `ref()` instead of `useState()`
3. **Props Binding:** Use `:prop="value"` instead of `prop={value}`
4. **Events:** Use `@change="handler"` instead of `change={handler}`
5. **Template Refs:** Use `ref` attribute instead of `useRef()` hook
6. **Lifecycle:** Use component lifecycle hooks instead of `useEffect()`
7. **Computed Values:** Use `computed()` for derived state
8. **Script Setup:** Use `<script setup>` for cleaner Composition API syntax

All original functionality, business logic, and user experience patterns remain identical between React and Vue implementations.
