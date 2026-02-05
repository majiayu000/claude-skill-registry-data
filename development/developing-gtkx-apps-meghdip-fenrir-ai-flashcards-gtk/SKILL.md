---
name: developing-gtkx-apps
description: Build GTK4 desktop applications with GTKX React framework. Use when creating GTKX components, working with GTK widgets, handling signals, or building Linux desktop UIs with React.
---

# Developing GTKX Applications

GTKX is a React framework for building native GTK4 desktop applications on Linux. It uses a custom React reconciler to render React components as native GTK widgets.

## Quick Start

```tsx
import { ApplicationWindow, render, quit } from "@gtkx/react";
import * as Gtk from "@gtkx/ffi/gtk";

const App = () => (
    <ApplicationWindow title="My App" defaultWidth={800} defaultHeight={600}>
        <Box orientation={Gtk.Orientation.VERTICAL} spacing={12}>
            <Label label="Hello, GTKX!" />
            <Button label="Quit" onClicked={quit} />
        </Box>
    </ApplicationWindow>
);

render(<App />, "com.example.myapp");
```

## Widget Patterns

### Container Widgets

**Box** - Linear layout:
```tsx
<Box orientation={Gtk.Orientation.VERTICAL} spacing={12}>
    <Label label="First" />
    <Label label="Second" />
</Box>
```

**Grid** - 2D positioning:
```tsx
<Grid.Root spacing={10}>
    <Grid.Child column={0} row={0}>
        <Label label="Top-left" />
    </Grid.Child>
    <Grid.Child column={1} row={0} columnSpan={2}>
        <Label label="Spans 2 columns" />
    </Grid.Child>
</Grid.Root>
```

**Stack** - Page-based container:
```tsx
<Stack.Root visibleChildName="page1">
    <Stack.Page name="page1" title="Page 1">
        <Label label="Content 1" />
    </Stack.Page>
    <Stack.Page name="page2" title="Page 2">
        <Label label="Content 2" />
    </Stack.Page>
</Stack.Root>
```

**Notebook** - Tabbed container:
```tsx
<Notebook.Root>
    <Notebook.Page label="Tab 1">
        <Content1 />
    </Notebook.Page>
    <Notebook.Page label="Tab 2">
        <Content2 />
    </Notebook.Page>
</Notebook.Root>
```

**Paned** - Resizable split:
```tsx
<Paned.Root orientation={Gtk.Orientation.HORIZONTAL} position={280}>
    <Paned.StartChild>
        <SideBar />
    </Paned.StartChild>
    <Paned.EndChild>
        <MainContent />
    </Paned.EndChild>
</Paned.Root>
```

### Virtual Scrolling Lists

**ListView** - High-performance scrollable list with selection:
```tsx
<ListView.Root
    vexpand
    selected={[selectedId]}
    selectionMode={Gtk.SelectionMode.SINGLE}
    onSelectionChanged={(ids) => setSelectedId(ids[0])}
    renderItem={(item: Item | null) => (
        <Label label={item?.text ?? ""} />
    )}
>
    {items.map(item => (
        <ListView.Item key={item.id} id={item.id} item={item} />
    ))}
</ListView.Root>
```

**GridView** - Grid-based virtual scrolling:
```tsx
<GridView.Root
    vexpand
    renderItem={(item: Item | null) => (
        <Box orientation={Gtk.Orientation.VERTICAL}>
            <Image iconName={item?.icon ?? "image-missing"} />
            <Label label={item?.name ?? ""} />
        </Box>
    )}
>
    {items.map(item => (
        <GridView.Item key={item.id} id={item.id} item={item} />
    ))}
</GridView.Root>
```

**ColumnView** - Table with sortable columns:
```tsx
<ColumnView.Root
    sortColumn="name"
    sortOrder={Gtk.SortType.ASCENDING}
    onSortChange={handleSort}
>
    <ColumnView.Column
        title="Name"
        id="name"
        expand
        sortable
        renderCell={(item: Item | null) => (
            <Label label={item?.name ?? ""} />
        )}
    />
    {items.map(item => (
        <ColumnView.Item key={item.id} id={item.id} item={item} />
    ))}
</ColumnView.Root>
```

**DropDown** - String selection widget:
```tsx
<DropDown.Root>
    {options.map(opt => (
        <DropDown.Item key={opt.value} id={opt.value} label={opt.label} />
    ))}
</DropDown.Root>
```

### HeaderBar

Pack widgets at start and end of the title bar:
```tsx
<HeaderBar.Root>
    <HeaderBar.Start>
        <Button iconName="go-previous-symbolic" />
    </HeaderBar.Start>
    <HeaderBar.End>
        <MenuButton.Root iconName="open-menu-symbolic" />
    </HeaderBar.End>
</HeaderBar.Root>
```

### ActionBar

Bottom bar with packed widgets:
```tsx
<ActionBar.Root>
    <ActionBar.Start>
        <Button label="Cancel" />
    </ActionBar.Start>
    <ActionBar.End>
        <Button label="Save" cssClasses={["suggested-action"]} />
    </ActionBar.End>
</ActionBar.Root>
```

### Controlled Input

Entry requires two-way binding:
```tsx
const [text, setText] = useState("");

<Entry
    text={text}
    onChanged={(entry) => setText(entry.getText())}
    placeholder="Type here..."
/>
```

### Declarative Menus

```tsx
<ApplicationMenu>
    <Menu.Submenu label="File">
        <Menu.Item
            label="New"
            onActivate={handleNew}
            accels="<Control>n"
        />
        <Menu.Section>
            <Menu.Item label="Quit" onActivate={quit} accels="<Control>q" />
        </Menu.Section>
    </Menu.Submenu>
</ApplicationMenu>
```

## Signal Handling

GTK signals map to `on<SignalName>` props:
- `clicked` → `onClicked`
- `toggled` → `onToggled`
- `changed` → `onChanged`
- `notify::selected` → `onNotifySelected`

## Widget References

```tsx
import { useRef } from "react";

const entryRef = useRef<Gtk.Entry | null>(null);
<Entry ref={entryRef} />
// Later: entryRef.current?.getText()
```

## Portals

```tsx
import { createPortal } from "@gtkx/react";

{createPortal(<AboutDialog programName="My App" />)}
```

## Constraints

- **GTK is single-threaded**: All widget operations on main thread
- **Virtual lists need immutable data**: Use stable object references
- **ToggleButton auto-prevents feedback loops**: Safe for controlled state
- **Entry needs two-way binding**: Use `onChanged` to sync state

For detailed widget reference, see [WIDGETS.md](WIDGETS.md).
For code examples, see [EXAMPLES.md](EXAMPLES.md).
