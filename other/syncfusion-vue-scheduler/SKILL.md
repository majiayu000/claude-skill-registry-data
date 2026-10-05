---
name: syncfusion-vue-scheduler
description: Implement event scheduling, calendar views, and appointment management using Syncfusion Vue Scheduler component. Use this skill when working with calendars, event scheduling, appointment booking systems, resource management, timeline views, recurring events, drag-and-drop event handling, or any scenario involving time-based event visualization and management in Vue applications. Trigger for scheduler implementations, calendar integrations, booking systems, meeting planners, task schedulers, or resource allocation tools.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Syncfusion Vue Scheduler

A comprehensive scheduling component for Vue applications that provides calendar views, appointment management, resource scheduling, and time-based event visualization with drag-and-drop support.

## When to Use This Skill

Use this skill when the user needs to:
- Implement calendar or scheduling functionality in Vue applications
- Create appointment booking or event management systems
- Build resource allocation or meeting scheduler tools
- Display events in day, week, month, timeline, or agenda views
- Handle recurring events with complex recurrence patterns
- Manage multiple resources with grouped scheduling
- Implement drag-and-drop event scheduling
- Create interactive calendars with CRUD operations
- Support multiple timezones in scheduling applications
- Export/import calendar data (ICS format)

## Component Overview

The Syncfusion Vue Scheduler is a feature-rich calendar and scheduling component that supports:
- **Multiple Views**: Day, Week, Work Week, Month, Year, Agenda, Timeline views
- **Event Management**: Normal, all-day, spanned, and recurring events with exceptions
- **Resource Scheduling**: Single and multiple resource grouping with custom templates
- **Drag & Drop**: Move and resize events across time slots and resources
- **Data Binding**: Local and remote data sources with field mapping
- **Customization**: Cell templates, event templates, and comprehensive styling options
- **Interactions**: Context menus, clipboard operations, keyboard shortcuts
- **Accessibility**: Full WCAG compliance with keyboard navigation and screen reader support

## Documentation and Navigation Guide

Complete coverage of Syncfusion Vue Scheduler with 17 comprehensive reference files covering all aspects of scheduler implementation.

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation `@syncfusion/ej2-vue-schedule` and theme package
- CSS reference using Syncfusion theme packages
- Module injection and provide setup for both Vue 2/3
- Basic scheduler initialization with selectedDate and currentView
- Creating first appointments with eventSettings
- CSS import paths for all required components

### Appointments and Events
📄 **Read:** [references/appointments.md](references/appointments.md)
- Event types: normal, all-day, spanned, recurring appointments
- Event fields and custom field mapping
- Recurrence rules and patterns (FREQ, INTERVAL, COUNT, UNTIL, BYDAY, etc.)
- Recurrence exceptions and editing individual occurrences vs. series
- Drag and drop with dragStart/drag/dragStop events
- Resizing events with resize controls
- Inline appointment editing
- Event retrieval methods (getEventDetails, getCurrentViewEvents, getEvents)

### Appointment Behavior and Validation
📄 **Read:** [references/appointment-behavior-and-validation.md](references/appointment-behavior-and-validation.md)
- Setting minimum appointment height
- Blocking dates and times
- Readonly events and restricting event creation
- Differentiating past events and disabling past dates
- Appointments occupying entire cells and limiting displayed events
- Tooltip and filtering operations
- Appointment selection and deleting multiple appointments via Delete key
- Preventing overlaps and validating recurrence rules

### Views and Navigation (Display Modes)
📄 **Read:** [references/views.md](references/views.md)
- Day, Week, WorkWeek, Month, Year, Agenda, MonthAgenda views
- Timeline views (TimelineDay, TimelineWeek, TimelineWorkWeek, TimelineMonth, TimelineYear)
- View-specific configuration (startHour, endHour, workDays, interval, dateFormat)
- Multi-day, multi-week, and multi-month view intervals
- View templates (cellTemplate, dateHeaderTemplate, eventTemplate, resourceHeaderTemplate)
- Custom header rows for timeline views
- First day of week configuration
- Hidden weekend support for all views
- Readonly view modes
- Virtual scrolling in Agenda and Timeline views
- Week number display
- Agenda days count and hideEmptyAgendaDays
- Limit overlapping events with `maxEventStack`

### Data Binding (Local and Remote)
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local data source with array of objects
- Remote data binding with DataManager (ODataV4Adaptor, WebApiAdaptor, UrlAdaptor)
- Custom field mapping (id, subject, startTime, endTime, location, description, isAllDay, recurrenceRule, isReadonly)
- Server-side filtering with includeFiltersInQuery
- Custom adaptors extending ODataV4Adaptor with processResponse
- Loading data via AJAX Post with callbacks
- Passing additional parameters to server with Query.addParams
- Handling failure actions with actionFailure event
- CRUD operations with UrlAdaptor and server-side controller code
- C# controller implementation with EditParams (Insert/Update/Remove logic)
- Google Calendar integration with WebApiAdaptor and dataBinding transformation
- DataManager configuration with crossDomain support

### Resources and Grouping
📄 **Read:** [references/resources.md](references/resources.md)
- Resource fields and properties (field, title, name, allowMultiple, dataSource, idField, textField, colorField, etc.)
- Resource data binding (local JSON and remote DataManager)
- Single and multiple resource assignment
- Single-level and multi-level hierarchical resource grouping
- Resource grouping by date (byDate property)
- One-to-one resource grouping (byGroupID: false)
- Shared events across resources with allowGroupEdit
- Vertical vs. Timeline resource view implementation

### Resource Customization
📄 **Read:** [references/resource-customization.md](references/resource-customization.md)
- Custom working hours per resource
- Custom working days per resource
- Resource header templates with customization
- Multi-column resource headers (Timeline only)
- Customizing parent resource cells with renderCell event
- Custom CSS classes per resource
- Expanded/collapsed state for resources (Timeline views)

### Time Configuration (Timescale and Timezone)
📄 **Read:** [references/timescale-timezone.md](references/timescale-timezone.md)
- Timescale configuration (enable, interval, slotCount, templates)
- Slot duration configuration (30-min, 15-min, 10-min, 5-min intervals)
- Hiding timescale and custom time format
- Major and minor slot templates
- Scheduler timezone configuration with IANA timezone names
- Common timezones (America/New_York, Europe/London, Asia/Tokyo, etc.)
- UTC display for global applications
- Per-event timezone with startTimezone and endTimezone fields
- Timezone conversion helper methods (convert, removeLocalOffset, addLocalOffset)
- Timezone dropdown in event editor
- Browser local timezone (no timezone setting)
- Daylight saving time handling

### Customization
📄 **Read:** [references/customization.md](references/customization.md)
- Cell dimensions with CSS classes (height, width for all views)
- Cell templates for workCells, monthCells, allDayCells, dateHeader cells
- RenderCell event with elementType checking (workCells, monthCells, dateHeader, resourceGroupCells, etc.)
- Cell header template for Month view
- Date header customization for Week/Day views
- Minimum and maximum date constraints
- Weekend cell customization and highlighting
- Custom working hours and working days
- Multi-cell and multi-row selection control
- Slot availability checking with isSlotAvailable method

### Editor Templates
📄 **Read:** [references/editor-template.md](references/editor-template.md)
- Event editor overview and modes (Add, Edit, EditOccurrence, EditSeries)
- Customizing editor field labels with title property
- Customizing editor buttons via localization (L10n)
- Field validation rules (required, regex, custom validators)
- Adding custom fields to default editor
- Creating fully custom editor template
- Quick info template customization (header, content, footer)
- Disabling editor with readonly or popupOpen event
- Editor field types and validation

### Header Configuration
📄 **Read:** [references/header-configuration.md](references/header-configuration.md)
- Header bar customization and styling
- Header rows for timeline views (Year, Month, Date)
- Date header template for all views
- Custom toolbar actions and buttons
- Header navigation (previous, today, next)
- Hiding/showing header elements

### CRUD Operations
📄 **Read:** [references/crud-operations.md](references/crud-operations.md)
- Adding events: addEvent method, multiple events batch add
- Editing events: saveEvent method with action types
- Deleting events: deleteEvent by ID or object, multiple delete
- Drag and drop with allowDragAndDrop module
- Event resizing with allowResizing module
- ActionBegin event for validation and cancellation
- ActionComplete event for post-operation handling
- ActionFailure event for error handling
- Readonly mode and per-event readonly flag
- Validation for time ranges and slot availability
- Preventing overlaps with isSlotAvailable

### Clipboard Operations
📄 **Read:** [references/clipboard.md](references/clipboard.md)
- Enabling clipboard with allowClipboard property
- Copy/cut/paste keyboard shortcuts (Ctrl+C, Ctrl+X, Ctrl+V)
- Programmatic API (copy(), cut(), paste() methods)
- Context menu integration with custom menu items
- Before/after paste events for data modification
- Behavior notes (copy creates duplicate, cut moves event)
- Multiple paste of copied events
- Cross-application paste support

### Context Menu
📄 **Read:** [references/context-menu.md](references/context-menu.md)
- Custom context menu integration with ContextMenu component
- Menu setup with items configuration
- BeforeOpen event for menu display logic
- OnSelect event for menu action handling
- Showing/hiding menu items based on context (cell vs. event)
- Recurring event menu with sub-items (Edit/Delete Occurrence/Series)
- Custom menu items (Print, Export, Email, etc.)
- Mobile context menu with tap-hold support
- Custom styling with CSS classes

### Localization and Accessibility
📄 **Read:** [references/localization-accessibility.md](references/localization-accessibility.md)
- Locale configuration and language translation (en, fr, de, ja, etc.)
- L10n class for custom text translation
- Date and time formatting with `dateFormat` and `timeFormat` (12/24-hour, ISO, locale-aware)
- RTL (right-to-left) support for Arabic, Hebrew
- WCAG 2.0 compliance level AA
- Keyboard shortcuts (Tab, Enter, Space, Delete, Ctrl+A, etc.)
- ARIA attributes (role, aria-label, aria-describedby)
- Screen reader support and announcements
- Focus management and visible focus indicator

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Virtual scrolling for large datasets in Agenda/Timeline views
- Exporting to PDF and Excel formats
- Printing scheduler with custom templates
- State persistence (enablePersistence) saving view/date/scroll position
- Row auto height for overlapping events
- Event templates for custom rendering
- Quick info templates
- Block time slots (marking unavailable times)
- ICS calendar import/export
- Tooltip on event hover
- Inline editing support
- Responsive adaptive UI

### Recurrence Editor and Calendar Modes
📄 **Read:** [references/recurrence-editor-calendar-modes.md](references/recurrence-editor-calendar-modes.md)
- Recurrence editor and recurrence date generation
- Gregorian and Islamic calendar modes
- Working days, hours, and custom time ranges
- Scheduler styling and theming
- Performance optimization tips
- Best practices for production use

## Quick Start Example

### Basic Scheduler with Appointments

```vue
<template>
  <div id='app'>
    <ejs-schedule 
      height='550px' 
      :selectedDate='selectedDate'
      :eventSettings='eventSettings'>
    </ejs-schedule>
  </div>
</template>

<script setup>
import { provide } from "vue";
import { ScheduleComponent as EjsSchedule, Day, Week, WorkWeek, Month, Agenda } from '@syncfusion/ej2-vue-schedule';

const selectedDate = new Date(2024, 0, 15);
const eventSettings = {
  dataSource: [
    {
      Id: 1,
      Subject: 'Team Meeting',
      StartTime: new Date(2024, 0, 15, 10, 0),
      EndTime: new Date(2024, 0, 15, 11, 30),
      IsAllDay: false
    },
    {
      Id: 2,
      Subject: 'Project Review',
      StartTime: new Date(2024, 0, 16, 14, 0),
      EndTime: new Date(2024, 0, 16, 15, 30),
      IsAllDay: false
    }
  ]
};

// Inject required view modules
provide('schedule', [Day, Week, WorkWeek, Month, Agenda]);
</script>

<style>
@import "../node_modules/@syncfusion/ej2-material3-theme/styles/schedule/index.css";
</style>
```

## Common Patterns

### Recurring Event with Exceptions

```vue
<script setup>
const eventSettings = {
  dataSource: [
    {
      Id: 1,
      Subject: 'Daily Standup',
      StartTime: new Date(2024, 0, 15, 9, 0),
      EndTime: new Date(2024, 0, 15, 9, 30),
      RecurrenceRule: 'FREQ=DAILY;INTERVAL=1;COUNT=10',
      RecurrenceException: '20240117T090000Z,20240119T090000Z'
    }
  ]
};
</script>
```

### Resource Grouping

```vue
<template>
  <ejs-schedule 
    :eventSettings='eventSettings'
    :group='group'>
    <e-resources>
      <e-resource 
        field='RoomId' 
        title='Room' 
        name='Rooms'
        :dataSource='roomData'
        textField='Name' 
        idField='Id' 
        colorField='Color'>
      </e-resource>
    </e-resources>
  </ejs-schedule>
</template>

<script setup>
const roomData = [
  { Id: 1, Name: 'Room A', Color: '#ffaa00' },
  { Id: 2, Name: 'Room B', Color: '#357cd2' }
];

const group = { resources: ['Rooms'] };
</script>
```

### Custom Field Mapping

```vue
<script setup>
const eventSettings = {
  dataSource: appointmentData,
  fields: {
    id: 'EventId',
    subject: { name: 'Title' },
    startTime: { name: 'From' },
    endTime: { name: 'To' },
    location: { name: 'Place' },
    description: { name: 'Notes' },
    isAllDay: { name: 'FullDay' }
  }
};
</script>
```

### Timeline View Configuration

```vue
<template>
  <ejs-schedule 
    :selectedDate='selectedDate'
    :eventSettings='eventSettings'>
    <e-views>
      <e-view option='TimelineDay'></e-view>
      <e-view option='TimelineWeek'></e-view>
      <e-view option='TimelineMonth'></e-view>
    </e-views>
  </ejs-schedule>
</template>

<script setup>
import { provide } from "vue";
import { TimelineViews, TimelineMonth } from '@syncfusion/ej2-vue-schedule';

provide('schedule', [TimelineViews, TimelineMonth]);
</script>
```

## Key Props and Events

### Essential Properties

| Property | Type | Description |
|----------|------|-------------|
| `selectedDate` | Date | Currently selected date in the scheduler |
| `currentView` | string | Active view (Day, Week, Month, Agenda, etc.) |
| `eventSettings` | object | Event data source and field configuration |
| `views` | array | Collection of views to display |
| `startHour` | string | Start hour for day/week views (e.g., '08:00') |
| `endHour` | string | End hour for day/week views (e.g., '18:00') |
| `workDays` | number[] | Working days (0=Sunday, 1=Monday, etc.) |
| `timeScale` | object | Time slot configuration (interval, slotCount) |
| `group` | object | Resource grouping configuration |
| `readonly` | boolean | Prevents CRUD operations when true |
| `allowDragAndDrop` | boolean | Enables drag and drop for events |
| `allowResizing` | boolean | Enables event resizing |
| `allowMultiDrag` | boolean | Enables multiple event drag selection |
| `allowClipboard` | boolean | Enables clipboard operations |
| `timezone` | string | Scheduler timezone (e.g., 'America/New_York') |

### Essential Events

| Event | Description |
|-------|-------------|
| `actionBegin` | Triggered before any CRUD action (add/edit/delete) |
| `actionComplete` | Triggered after successful CRUD action |
| `actionFailure` | Triggered when CRUD action fails |
| `eventClick` | Triggered when an event is clicked |
| `eventDoubleClick` | Triggered when an event is double-clicked |
| `cellClick` | Triggered when a cell is clicked |
| `cellDoubleClick` | Triggered when a cell is double-clicked |
| `popupOpen` | Triggered before editor/quick info popup opens |
| `popupClose` | Triggered when popup closes |
| `dragStart` | Triggered when event drag starts |
| `drag` | Triggered during event dragging |
| `dragStop` | Triggered when event drag stops |
| `resizeStart` | Triggered when event resize starts |
| `resizing` | Triggered during event resizing |
| `resizeStop` | Triggered when event resize stops |
| `dataBinding` | Triggered before data binding |
| `dataBound` | Triggered after data binding completes |
| `beforePaste` | Triggered before clipboard paste operation |

### Essential Methods

| Method | Description |
|--------|-------------|
| `addEvent(data)` | Adds new event to the scheduler |
| `saveEvent(data, action)` | Saves modified event |
| `deleteEvent(id/object)` | Deletes event by ID or object |
| `getEvents(startDate, endDate)` | Gets events within date range |
| `getEventDetails(element)` | Gets event details from element |
| `openEditor(data, action)` | Opens editor window programmatically |
| `closeEditor()` | Closes the editor window |
| `refreshEvents()` | Refreshes all events |
| `scrollTo(hour)` | Scrolls to specific hour in day/week views |
| `getCurrentViewDates()` | Returns current view date collection |

## Installation

Install the Syncfusion Vue Schedule package:

```bash
npm install @syncfusion/ej2-vue-schedule --save
```

Import required CSS themes:

```javascript
import '@syncfusion/ej2-base/styles/material3.css';
import '@syncfusion/ej2-buttons/styles/material3.css';
import '@syncfusion/ej2-calendars/styles/material3.css';
import '@syncfusion/ej2-dropdowns/styles/material3.css';
import '@syncfusion/ej2-inputs/styles/material3.css';
import '@syncfusion/ej2-navigations/styles/material3.css';
import '@syncfusion/ej2-popups/styles/material3.css';
import '@syncfusion/ej2-vue-schedule/styles/material3.css';
```

## Module Injection

The Scheduler requires view modules to be injected. Only inject the views you need:

```javascript
import { 
  Day, Week, WorkWeek, Month, Year, Agenda, MonthAgenda,
  TimelineViews, TimelineMonth, TimelineYear,
  DragAndDrop, Resize
} from '@syncfusion/ej2-vue-schedule';

provide('schedule', [Day, Week, Month, Agenda, DragAndDrop]);
```

## Related Components

- **Recurrence Editor**: Standalone component for creating recurrence rules
- **DatePicker/DateRangePicker**: For date selection in custom editors
- **TimePicker**: For time selection in custom editors
- **DropDownList**: For resource selection in custom editors

## Best Practices

1. **Module Injection**: Only inject view modules you actually use to reduce bundle size
2. **Field Mapping**: Use custom field mapping when data structure differs from default
3. **Performance**: Enable virtual scrolling for large datasets (timeline views)
4. **Timezones**: Set scheduler timezone explicitly when working with multiple timezones
5. **Event IDs**: Always provide unique IDs for events to ensure proper CRUD operations
6. **Validation**: Use actionBegin event to validate data before saving
7. **Templates**: Use templates for custom event rendering and cell customization
8. **Accessibility**: Enable keyboard navigation and provide proper ARIA labels
9. **Responsive**: Use CSS media queries to adjust scheduler for mobile devices
10. **State Management**: Use state persistence to save user preferences

## Troubleshooting

**Events not displaying**: Verify event fields match the scheduler's expected field names or use field mapping in eventSettings.

**View not loading**: Ensure the required view module is properly injected via the provide method.

**Drag and drop not working**: Import and inject the DragAndDrop module.

**Timezone issues**: Set the scheduler's timezone property and ensure event times are in correct format.

**Custom fields not saving**: Map custom fields in eventSettings.fields configuration.

**Performance issues**: Enable virtual scrolling for timeline views with many events or resources.

**Data not loading from server**: Verify CORS settings, DataManager adaptor configuration, and network requests in browser DevTools.

**Recurring events not generating occurrences**: Check RecurrenceRule syntax (FREQ, INTERVAL, COUNT, UNTIL parameters) and verify rule is valid.
