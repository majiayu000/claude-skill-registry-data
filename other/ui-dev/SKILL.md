---
name: ui-dev
description: >
  UI development guide for frename. Use when: adding or changing a view, adding a new feature panel,
  creating or modifying a widget, changing layout constants or tokens, adding a new message to a
  feature, fixing a UI bug (clipped, overlapping or squeezed elements, wrong heights, scroll jumps),
  or working with the design system (src/ui), styling, icons, popups, drag-drop, BoundsReporter,
  scrolling, screenshots, or the search bar.
disable-model-invocation: false
---

# UI Development Guide — frename

## WHEN to use this skill
- Adding or changing a view (`view.rs`)
- Adding a new feature panel or modifying how a panel looks
- Creating or modifying a reusable widget
- Changing layout constants or sizing
- Adding a new message to a feature
- Working with drag-drop, BoundsReporter, scroll-into-view, or the search bar

---

## Feature module structure

Every feature lives in `src/features/<name>/` with these files:

| File | Role |
|---|---|
| `mod.rs` | Exports: re-exports `Message`, `State`, `view`, constants used by siblings |
| `state.rs` | Feature state: pure data + UI logic; no iced widget types except `Rectangle`, `Subscription`, `Task` |
| `messages.rs` | `pub enum Message` — all messages for this feature |
| `view.rs` | Pure `fn view(state, ...) -> Element<'_, Message>` — no state mutation |
| extra files | Sub-view files (`chips_panel.rs`, `file_name_line.rs`, `trash_zone.rs`) or sub-state |

## UI text

Every string a user sees (labels, tooltips, hints, error/status text) is a key in
`i18n/en/frename.ftl`, read with `fl!("key-id", arg = value)` (see `src/i18n.rs`), never a Rust
string literal. Keys: `<feature>-<element>[-<detail>]`, the feature being the folder under
`src/features/`. A plural gets a Fluent `{ $n -> [one] … *[other] … }` selector; reuse an existing
key when the exact same phrase already exists rather than adding a near-duplicate. A helper that
used to take `&'static str` (a button label, a tooltip) takes an owned `String` instead, since
`fl!` returns one. Exceptions (key names printed on a physical key, badges like `IN`/`OUT`/`CC`,
widget ids, log messages) are listed with their reason in `NOT_UI_TEXT` in `src/i18n.rs`; a test
there fails the build on any other English word left in a view, a widget, a batch action or
`folder_controls`. Every new language is its own small PR once the English key exists.

## Widgets

Standard controls are `src/ui/` components (see Styling). frename's own widgets go in
`src/widgets/` and take their values from `ui::tokens`:
- `search_bar.rs` — the bar over a list: `ui::form::search_field` and what narrows the same list
- `tag_chip.rs` — tag chips: `mini` (file list rows), the draggable chip of the file name card
- `splitter.rs` — draggable column splitter (a 1 px line in a 12 px hit area)
- `height_handle.rs` — the comment's height handle
- `file_name_display.rs` — a file list row's name: mini chips, `+N`, the name cut with "…"
- `starred_tags_panel.rs` — the starred strip (its cells are `tag_grid::cell`)
- `bounds_reporter.rs` — invisible Fill widget that reports its layout bounds on every event

**When it belongs in widgets:** used by 2+ features, or purely presentational with no feature-specific messages.
**When it belongs in a feature:** only ever used inside that feature's view.

---

## Styling

The design system is the rule: `docs/design/design-system.md` (tokens, text styles, components,
windows, patterns, every screen). Its code is `src/ui/`:

```rust
use crate::ui::icon_button::IconButton;
use crate::ui::icons::Icon;
use crate::ui::layout::{self, NoticeKind};
use crate::ui::tokens::*;                 // colors, SPACE_*, sizes, regions, radii, fonts
use crate::ui::tooltip::{Position, Tip};
use crate::ui::{badge, button, empty, form, list, scroll, style, text};

text::body(fl!("…")); text::secondary(fl!("…")); text::mono(name).color(TEXT);
button::primary(fl!("…")).on_press(msg); button::ghost(fl!("…")); button::link(fl!("…"));
IconButton::new(Icon::Rewind)
    .tip(Tip::new(fl!("…")).keys(&["F1"]), Position::Top)
    .on_press(msg);
form::checkbox(label, on).on_toggle(Msg::Set);
layout::setting_row(label, layout::aligned([..]));
layout::notice(NoticeKind::Info, headline, None, [button::secondary(label).on_press(msg).into()]);
list::row_item(content, selected, HOVER, Length::Fill); // the one hover + selected look, with its bar
scroll::vertical_with_id(ID, content);         // keeps the scrollbar gutter
empty::pane(Icon::Clapperboard, fl!("…"), None, Some(button.into()));
```

- A view never writes a color, a size, a padding, a spacing or a radius as a number: `ui::lint`
  fails the tests if it does (`0` alone is allowed). Its allow-list `NOT_YET` is empty and stays
  empty: a new size or color is a token in `src/ui/tokens/` (by kind: color, content, space, size,
  region, typography), with a doc comment.
- Every icon is a Lucide SVG in `assets/icons/` with one line in the `icons!` list of
  `src/ui/icons.rs`; every icon-only button is an `IconButton` with a tooltip.
- Something the system lacks is added to `docs/design/design-system.md` first, then to `src/ui/`.
  A piece two views need is one component, never a copy.
- `ui` holds tokens, styles (`ui::style`) and stateless constructors of standard controls;
  `src/widgets/` keeps frename's own stateful or custom-drawn widgets (splitter, tag chip,
  progress bar), which take their values from `ui::tokens` and `ui::style`.
- Every window uses `ui::theme()`; Inter at 13 px is the default font.

Tag chip colors: `ui::palette::TagPalette::color(tag.color_index())` (16 colors, the index
wraps); marker colors: `ui::palette::marker_color`.

---

## Sizing conventions

- `Length::Fill` — take all available space in the axis; `Length::Shrink` — natural size.
- A size is a token, never a number or a `const` of the view: `ui::lint` rejects both
  (`const GAP: f32 = 6.0` counts). Add it to the right file of `src/ui/tokens/` with a doc comment:
  `size.rs` for controls, lines, icons and radii; `region.rs` for the window, columns, bars and the
  geometry of a region (§13.9); `space.rs`, `color.rs`, `content.rs` (video, tags, markers),
  `typography.rs` (sizes, lines, fonts, character widths). Derive from other tokens where you can
  (`SEARCH_BAR_HEIGHT = CONTROL_HEIGHT + 2.0 * SPACE_TIGHT`).
- A multiplier that is a count ("a space on each side", `2.0 * SPACE_XS`) is fine inside a
  function; a `Padding { … }` or `Border { … }` with numbers in a view is not: put the value in a
  token or use a `ui` component that owns it (`ui::menu::row_of` owns a menu row's inset).
- Geometry that the view and the state both need (scroll-into-view, arrow keys, hit-testing) lives
  in ONE pure function or module next to the view, with unit tests: `tag_grid::groups::Shape`
  (where each tag sits, with the group captions), `media_viewer::video::view::cue_offset`,
  `markers::view::row_offset`. Never re-derive `index / columns` in the state.

---

## BoundsReporter

`BoundsReporter` is a `Fill×Fill` invisible widget that fires a message with its `Rectangle` on every
layout change, and never takes an event.

A `stack!` takes the size of its FIRST child. Put the content that decides the size first and the
reporter after it, so the reporter fills that size and the content grows freely:

```rust
// Right: the chips set the height (they may wrap onto more lines); the reporter fills it.
stack![tag_row, BoundsReporter::new(Message::PanelBounds)]

// Wrong: a fixed-height reporter first pins the stack's height; a second line of chips then
// draws over whatever is below (the file name card's name line was hidden this way).
stack![container(reporter).height(CELL_HEIGHT), tag_row]
```

For a full-height panel (the scrollable tag grid) the reporter can go first: the scrollable's `Fill`
height drives the layout either way.

---

## Scroll-into-view

The tag grid and tag list share one scrollable: `TAG_LIST_SCROLLABLE_ID`.

**After any `set_selected()` call, emit `Message::ScrollTagListToSelection`.**
`folder_workspace` handles the scroll operation using stored `scroll_y` and `viewport_height`.

```rust
// In folder_workspace::handle_tag_panel
self.tag_panel.set_selected(Some(id));
return Task::done(Message::ScrollTagListToSelection);
```

`TagPanelState` tracks `bounds`, `row_height`, `cols`, `row_content_height`, and `scroll_y` — all reported by the view via `Message::PanelBounds` and `Message::TagListScrolled`.

---

## Search bar (`widgets/search_bar`)

```rust
search_bar::view(
    SearchBar {
        input_id: search_bar::SEARCH_BAR_INPUT_ID,
        placeholder: fl!("…"),              // an example of what to type, never the label
        value: filter,
        clear_tip: fl!("…"),                // the x shows while there is text; Esc in its tooltip
        on_clear: …,
        on_submit: …,                       // always set: an unhandled Enter makes Windows beep
        trailing: Some(filter::button(dir, open)),  // what else narrows the same list
    },
    |s| Message::SetFilter(s),
)
```

The tag search's Enter creates the tag when the text names none (`on_submit`), and the grid shows
the "Create “…”" cell; there is no create button inside the field.

---

## Drag-drop (file_name_panel only)

`file_name_panel::Message` owns the drag lifecycle:

| Message | When |
|---|---|
| `DragStarted { tag_id, initial_index }` | Mouse pressed on a chip |
| `DragHoverCursor { x, y }` | Cursor moved (fired by `FileNamePanelState::subscription()`) |
| `DragEnded` | Mouse released (fired by subscription) |

`FileNamePanelState` computes `drop_target_index` from cursor + bounds.
`folder_workspace::handle_file_name_panel` calls `file_workspace.reorder_tag_to_index(dragged_id, drop_index)` on `DragEnded`.

The trash zone uses `TrashBounds` + cursor position to detect drop-on-trash (uncheck the tag).

---

## Subscriptions

Feature state exposes `subscription() -> Subscription<Message>` only when it needs OS-level events (mouse move/release for drag). `folder_workspace::subscription()` composes them:

```rust
pub fn subscription(&self) -> Subscription<Message> {
    Subscription::batch([
        self.video_player.subscription().map(Message::VideoPlayer),
        self.file_name_panel.subscription().map(Message::FileNamePanel),
    ])
}
```

Only `video_player` and `file_name_panel` currently have subscriptions.

---

## iced 0.14 gotchas

**Widget state follows its position in the tree, not its `Id`.** A scrollable, text editor or
text input keeps its scroll offset, cursor and focus only while it stays at the same place among
its siblings. Adding or removing a sibling *before* it (a header shown only in batch mode) moves
it and resets that state — the folder list jumped to the top this way. Put optional parts inside
a container that is always there:

```rust
// Wrong: `body` moves from child 1 to child 2 when the header appears.
let mut content = column![search];
if let Some(batch) = batch { content = content.push(header(batch)); }
content.push(body)

// Right: the header lives inside the first child; `body` is always child 1.
let mut top = column![search];
if let Some(batch) = batch { top = top.push(header(batch)); }
column![top, body]
```

**`push_maybe` is gone.** Add an optional child with
`.extend(condition.then(|| widget.into()))`.

**Progress from a worker thread** (`spawn_blocking`) does not redraw by itself: share it through an
`Arc` the view reads (see `batch::ItemProgress`), and redraw with a subscription that exists only
while the work runs: `iced::time::every(Duration::from_millis(200)).map(|_| Message::Noop)`.

---

## Design system work: where to look, what to do, what not to do

Learned while moving the whole app onto the system (#58, #59) and fixing what the owner found in
the first look. Read it before any UI change.

### Where things are
- The spec: `docs/design/design-system.md`. §3–12 are the rules, §13 every region of the main
  window (13.3 video, 13.4 file list, 13.5 tags, 13.6 batch, 13.9 sizes and what folds), §14
  Settings, §15.1 the module map of `src/ui/`. A change the spec does not cover goes into the spec
  in the same PR.
- The code: `src/ui/` (tokens, palette, icons, text, button, icon_button, tooltip, badge, form,
  list, scroll, segmented, menu, empty, layout, style). Feature views compose these; custom-drawn
  widgets (`widgets/splitter`, `widgets/tag_chip`, `video_controls/progress_bar`) take tokens.
- Before adding a component, search `src/ui/` for it (`rg "pub fn" src/ui`). Before adding a
  token, search `src/ui/tokens/` for one with the same meaning.

### Rules
- **One component, never a copy.** Two views that draw the same thing share one function (the tag
  grid and the starred strip share `tag_grid::cell`; every batch page is built from
  `batch::page`). A copy-pasted style or estimate is a bug waiting to diverge.
- **One selected look** (`ui::list::row_item`, `style::selectable`): no per-list tints.
- **Icons are Lucide** (`assets/icons/`, one line in `icons!`), never emoji or glyphs; icon-only
  buttons are `IconButton` with a `Tip` naming the command and its keys. Words that are words
  (`[`, `]`) use `IconButton::glyph`. A new icon: download it from
  `https://cdn.jsdelivr.net/npm/lucide-static@1.48.0/icons/<name>.svg` and strip its
  `<!-- @license -->` comment and `class=` line.
- **Offer the action, not directions** (§1 principle 9, §8.21): a dead end gets a button that does
  it; a link is only a side trip. Say a fact once: a notice and a row never both say it (the
  batch hint repeated the plan's time, with an unfilled `{ $duration }`).
- **Narrow places put the label above the control** (`layout::stacked_row`): batch pages are
  always under 440 px, so their option rows are stacked (`batch::page::option_row`); a label
  column there left a wide empty gap.
- **Every string in en and ru**, in the feature's `##` section of both `.ftl` files. A Russian
  plural uses exactly `one`/`few`/`many` (the i18n test checks CLDR categories).
- **Remove what nothing uses** (clippy runs with `-D warnings`): no speculative tokens or
  components "for later".
- **Look and layout vs behaviour:** the spec marks behaviour changes; keep them out of a restyle
  unless the owner asks, and list the ones you skip.

### iced 0.14 layout traps (each one bit us)
- **`Fill` children are laid out last.** In a row, `Shrink` children take their full width first,
  in order, and whatever is left goes to `Fill`. So the flexible text (a label, a hint, a name)
  goes in `container(text).width(Length::Fill)`, and fixed marks (badges, counts, icons, buttons)
  stay `Shrink`. A `Shrink` label before a badge squeezed the badge until its fill no longer
  covered its words; a long button-bar hint would squeeze the buttons. Badges also never wrap
  (`Wrapping::None`).
- **A `Shrink` column whose children are all `Fill` is 0 px wide.** iced sizes a `Shrink`
  column (or container) by its children that are not `Fill`, then stretches the `Fill` ones to
  that: with none, it is only its padding (the filter menu drew as a 4 px line). A popup of items
  gets a fixed width (`ui::menu::menu(rows, Length::Fixed(MENU_WIDTH))`).
- **A `Fill` height inside a scroll area collapses to nothing.** `list::row_item(…, height)` takes
  `Length::Fill` for a row in a slot of fixed height (file rows, marker rows) and `Length::Shrink`
  for a row of natural height (subtitle cues). A `Fill` child in a `Shrink` row is still
  stretched to the row's height (the selection bar relies on it).
- **`text_editor` adds its padding after `min_height`.** A "full-height" editor with
  `min_height(size.height)` is `padding.y()` taller than its box, scrolls, and its top edge goes out
  of sight: use `min_height(size.height - PADDING.y())`.
- **Keep the widget tree's shape stable** (see "iced 0.14 gotchas" above): an optional layer is a
  `space()` when hidden, not a missing child (the filter menu over the file list is always a
  `stack!` layer), or scroll positions and focus reset.
- **`responsive(|size| …)`** gives a view its width without any state: use it for what folds by
  width (the order strip's buttons below `ORDER_STRIP_WORDS_FROM`, the batch action list).
- **Overlays escape their parent.** A custom widget's overlay (the marker label) draws outside
  the widget's bounds, over its neighbours: reserve room for it inside the widget
  (`MARKER_LABEL_LANE`) instead of letting it cover the subtitle strip.
- **Z-levels.** Overlays (tooltips, the marker label) share one renderer layer, in which text is
  drawn over every box: an overlay that must be above another one goes through
  `ui::z::layered(widget, Z::…)` (tooltips and `tooltip::drag_preview` already do), and a
  custom overlay draws in its own `renderer.with_layer(…)` with `index()` from `Z`. Stack layers
  over the window (menus, fullscreen) wrap their outside in `opaque(…)` so the widgets under them
  get no hover. See design §13.3.2.
- **Popups:** there is no menu widget. A popup is an open flag in the feature's state, a
  `stack!` layer with `ui::menu::menu` at its anchor, and a full-size transparent `mouse_area`
  under it that closes it on a click beside it (see `folder::filter`, the video pane's More).
- **Text width:** iced cannot measure text or cut it with "…". Mono text has a fixed advance
  (`MONO_CHAR_WIDTH`), so a file name is cut exactly; other text is estimated
  (`BODY_CHAR_WIDTH`, `CHIP_MINI_CHAR_WIDTH`). Use a realistic estimate to fit things into a row
  (a generous one hid chips that fitted), a generous one to size columns.
- **Nothing draws past its background.** iced does not clip by default: text with
  `Wrapping::None` runs on past its row. Rows, nav items and menu items clip their content
  (`list::row_item`, `layout::nav_item_with`, `menu::item` do it), and a single line in a row is cut
  with `ui::text::fit` (by `CAPTION_CHAR_WIDTH`, `MONO_CHAR_WIDTH`…) so it ends in "…" instead of
  being sliced. A new container with a fill or an edge and text inside gets `.clip(true)`.
- **Long words do not wrap** with the default `Wrapping::Word`: a file name has no spaces and runs
  past a tooltip or a table cell. Text that may be a file name wraps with `Wrapping::WordOrGlyph`
  (`text::tooltip` does it for every tooltip; the failed-files table for its names).
- **An editor inside a scroll area loses its edge**: the editor's border scrolls with its text. The
  box draws the edge instead (`style::field_box(focused)` around the scroll area, the editor in
  `style::bare_text_editor`), and the focus ring comes from state: set on any edit, and asked with
  `operation::is_focused` after every mouse press, Tab or Esc (`CheckCommentFocus`). Ask only while
  the widget is on screen: about a missing widget no answer comes.
- **Never rotate a rasterized SVG** (`Svg::rotation`): the thin stroke is resampled and breaks into
  dots. Turn it inside the SVG (`<g transform="rotate(…)">`) and cache one handle per step
  (`ui::icons::spinner`).
- **A segmented control is one box**: the segments have no edges of their own, only the ends are
  rounded (on their outer corners), and a line separates them (`ui::segmented`).
- **A click on the row already open must not open it again**: each click of a double-click is a
  `SelectFile`, and reopening reloads the video.

### Checking your work
- `cargo build` before a screenshot: `cargo test` builds only the test binary, and the old exe
  gives an old screenshot.
- Screenshots: from `docs/screenshots`, `../../target/debug/frename.exe --demo main.toml --out
  <file>.png` (`--batch`, `--mono`, `--lang ru`, `--settings <page>`). Park the mouse pointer off
  the window first, or a hover tooltip lands in the picture:
  `powershell -c "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point(5000,5000)"`.
  Zoom in with `magick in.png -crop WxH+X+Y -scale 300% out.png` to check padding and edges.
  The demo cannot open the marker list, run a job, open a menu or narrow a column: check those
  states by hand in `cargo run`, and say so.
- README images: `docs/screenshots/render.sh`, then look at every one: the callouts in
  `main.svg`/`batch.svg`/`mono.svg` point at fixed canvas coordinates (the window sits at 100,204)
  and must be moved when a control moves.
- Gate: `cargo fmt --all -- --check`, `cargo clippy --workspace --all-targets --locked -- -D
  warnings`, `cargo test --workspace --locked --no-fail-fast` (on this Windows machine the three
  `self_test` GStreamer tests fail on `main` too).
- Editing Rust with a script: find the end of a block with an anchor that is unique and after its
  start (`#[cfg(test)]
mod tests`, not `#[cfg(test)]`, which also marks items inside a macro); a
  slice with its end before its start is empty, and `str.replace("", …)` then writes the new
  text between every character. Assert the anchor order in the script.
- Editing `.ftl` files with a script: a multi-line entry ends at its own `}` line; remove that
  line with the entry, or the file stops parsing and every i18n test fails at once.
- Merging `main` into a long UI branch: a conflict in a view is usually `main`'s whole old file
  against the rewrite. Read what `main` actually changed there (`git diff <merge-base>
  origin/main -- <file>`), take the branch's side, and port only that change onto the new
  structure (a new message, a right-click, a palette argument). Never take `main`'s old view: it
  brings back literals and the old theme. Then re-check strings (`every_message_is_used`), the
  lint, and `version.md` (a released block stays exactly as `main` has it; the branch's block is
  `main`'s version + 1).
- Several worktrees building at once share one `CARGO_TARGET_DIR`, or drive C: fills up.

---

## Layout orchestration

All views flow through `folder_workspace::view`, which arranges:
- Left panel: video player + video controls
- Middle: folder file list
- Right: search bar + tag grid + file name panel (file_workspace::view)

Splitters (`src/widgets/splitter.rs`) sit between panels; their positions are tracked as `left_width: f32` and `folder_width: f32` in `FolderWorkspace`.
