---
name: navml-library
description: navml's widget library outside windows and menus -- Control, Cluster, StaticText, Label, Button, InputLine, HexLine, CheckBoxes, RadioButtons, ScrollBar, ListViewer, Modal, Dialog, Field, Spacer, Timer, ProgressBar, Spinner, Toast, navml.background, MaskedLine/MaskedField, DateField/TimeField/Calendar/TimePicker, ChoiceField, History/HistoryList, the layouts (Horizontal/Vertical/Grid/Dock/Stack), and building a dialog (including Navigator's About dialog). Use when writing or changing a dialog or a control.
---

# The widget library: dialogs, controls, layouts, history

**None of it was designed**: DOS Navigator's Colors dialog names the widgets and their states, `tools/palconv.py`
transcribed all 144 slots into every theme, and the *Dialogs* group is the specification. `navigator/styles/navigator.nss`
binds the components to the `$dialog-*` variables. Windows, the desktop and menus are the `navml-windows-menus` skill.

## The components

- **First tier** (`navml/widgets/dialog/`): `Control`, `Cluster`, `StaticText`, `Label`, `Button`, `InputLine`, `HexLine`,
  `CheckBoxes`, `RadioButtons`, `ScrollBar`, `ListViewer`, `Modal`, `Dialog`, `Field`; plus `Spacer` and `Timer` at the
  top. `Timer` paints nothing and emits `TimerEvent` every `interval` ms; Navigator's `Clock`
  (`navigator/widgets/shell/clock/`, `HH:MM`, blinking colon, *Timer* slot `[1]`) is built on it.
- `Modal` is the framed, fixed, centred window (bound geometry, `modal = True`) and `Dialog` derives from it.
  `Dialog.buttons` has `ok`, `yes-no-cancel`, ...; `Dialog.valid()` (`Valid(cmOK)`) keeps a dialog up over a value it
  cannot read. F7 Mkdir was the first dialog wired into the application.
- `Button` emits `ClickEvent`; mouse and Space both go through one `press()`. Clicks act on release.
- **`Button.command`** (Turbo Vision's `TButton` carried one): when set, `press()` asks for that command from the
  button through `app.run_command(command, start=self)`, exactly as its key would, through `enables()`. No click is
  emitted then. Write `command: NewGame` in markup instead of an `on_<id>_click` that calls `self.on_new_game(...)`.
  The button is not greyed while its command is disabled; `press()` returns False.
- A `Button`'s tooltip is the keys that press it (`press_keys()`: the dialog's Default key on the default button,
  its Cancel key on its `cancel`, Alt+letter), read off the key tables; its own `tooltip` goes in front.
- `CheckBoxes`/`RadioButtons` (`Cluster`) take `tooltips:`, one an item in step with `items` (translated like it);
  an empty or missing one falls back to the cluster's own `tooltip`. Write one only where the caption does not say
  it (*Remove source files*, *Sticky*), `""` elsewhere; a test keeps every list in step with its `items`.
- A `ListViewer` row's tooltip is its whole `row_text` while cut (`row_tooltip`, `cut_text`); a subclass with its own
  `render_row` or `render_items` gets none unless it overrides `row_tooltip` (`TraceList` does) or `tooltip_at`
  (`UnicodeGrid`, per cell). An input line's likewise, plus its own
  or its field's `tooltip`.
- A `TabView` takes `tooltips:`, one a page (what the page holds), shown on its tab only -- never a page's own
  `tooltip`, which would show over its every blank. A cut left-column caption shows whole; the arrows say their way.
- A `ListViewer` takes `tooltips:` too, one an item, before the cut-text fallback (Colors' items, Savers' lists).
- A standalone `Label` (not in a `Field`) shows its linked control's `tooltip`; its own wins.
- A `ProgressBar` says what it rounds: exact done/total/left and the percent to one decimal, unless it has its own.
- `CalendarView` spells a day out (weekday, `date_format`, ISO week, days from today), names a weekday column, and
  keys its arrows and names; `ColorSelector` names a colour (`Light blue (light_blue)`).
- A focusable widget that paints several things gives `tooltip_anchor()` for Shift+F11 (`ListViewer`, `Cluster`,
  `TabView`, `CalendarView`, `ColorSelector` do); a framed `Window`'s title says it whole where cut, and what a
  double click and a drag do.
- `Button.flat` (a departure: `TButton` always had its shadow) drops the shadow, so the face is the whole rectangle
  and the button may be one row tall; pressed, it does not move. For a small button beside a line, as the
  Character Table's filter *X*.
- **Arrows walk buttons** (a departure: `TButton` ignored them). Left/Up to the previous, Right/Down to the next,
  no wrap. The group is the unbroken run of buttons around the focused one in the dialog's tab order
  (`Button._row`), not a container -- most dialogs place buttons by `x`/`y` -- so keep a button row together in
  tree order, and any other control between buttons splits the run.
- `Cluster` lays out in columns as `TCluster` did. **`enable_mask`** (a bit an item, all by default) is
  `TCluster.EnableMask`: a cleared item is greyed (`::item:disabled` etc.), passed over by the arrows and Home/End,
  and taken by neither a click nor its letter (`item_enabled`); *Create archive* greys types and levels with it. **Tri-state `CheckBoxes`**: `mixed` draws `[?]`, `tristate` lets a
  bit cycle back to it.
- **Marks** come from `navkit.glyphs.marks(look, tier)`: five three-cell strings (check off/on/mixed, radio off/on),
  picked by `mark_index()` (`CheckBoxes` 0-2, `RadioButtons` 3-4). `look` is a style property: `dos` (`[X]` `(•)`),
  `brackets` (`[✓]` `(●)`), `boxes` (`☐ ☑ ⊟`/`○ ◉` centred, Font Awesome icons at the Nerd tier), `ascii`, or `auto`
  (the default) for `Application.marks` -- `dos` in navkit, `[appearance] marks` in Navigator. **Every mark is three
  cells** in every look and tier: captions sit at `x + 4` and `_column_x` steps by `widest + 6`.
- `ListViewer` hooks: `capacity`, `index_at`, `render_items`, overridable `_follow_cursor`; `framed = False` drops the
  frame; it claims only a *bare* Enter.
- **Held buttons repeat** (`Application.hold_mouse`, `navkit-widgets-input`):
  - **`ScrollBar`:** an arrow or the track steps on every tick while the pointer is over the part pressed (`part_at`,
    `TScrollBar`'s extent grown by a cell). So paging stops when the thumb reaches the pointer.
  - **`ListViewer`** (`TListViewer`): a held left button drags the cursor to the row under the pointer. Above or below
    the rows (beside them with columns), every `edge_ticks`-th tick (4, `MouseAutosToSkip`) moves it on one row, or
    one column.
  - **Opting out:** `follows_drag = False` turns this off, as the panel does while drag-and-drop is on. `edge_delay`
    sets the first tick.
- `StaticText.links` marks the `http(s)://` runs it paints (OSC 8, see `navkit-terminal`).
- **`OptionStrip`** (`navml/widgets/option_strip/`, Python only, not DN's): a window's *options* in a row, each an
  `OptionItem(command, label, lit=None)`. Lit is the command's `checks` (or `lit()`), greyed its `enables`, both asked
  of `target` (the widget whose options they are) through `navkit.commands` while painting -- any reactive write
  repaints, as for `KeyBar`. A left press on an enabled item runs `commands.run(app, command, target)`; every press is
  the strip's. Each item is drawn `[label]`, a cell apart, and nothing between: on a frame the border shows
  through (`═[⌶]═[§]═`). `spans`/`used_width` are computed from the labels' display width; bind `width: self.used_width` and give
  it `room` -- items that would pass it drop from the last. Part `item` with `:checked`/`:disabled`. Actions do not
  belong on it: those stay on menus and keys.
- **`ProgressBar`** (`navml/widgets/progress_bar/`): `value`/`total`/`percent`, as wide as placed, `█▒` from navkit's
  `GAUGES`. **`Spinner`** (`navml/widgets/spinner/`): one cell turning through navkit's `SPINNERS` every `interval` ms
  while mounted (`call_every`, as `Timer`); `frame` counts up. Navigator's `WriteWin` puts one beside its message.
- **`Toast`** (`navml/widgets/toast/`, not Turbo Vision's): `text` in a one-row frame titled `title`, never focused,
  gone after `seconds` (`TOAST_SECONDS`, 5; `call_later` armed in `mounted()`) or a left press; `natural_width` is
  how wide it would be, `gone` is called once it is off the tree. **Whoever adds it places it**: Navigator's
  `Shell.toast(text, title=, seconds=)` adds it first and *then* binds its geometry (bound before `add`, the dock
  layout gives it the whole band), at the desktop's bottom right, newer ones lower (`_Toasts`).
- **`navml/background.py`'s `Background`**: a widget's slow read on a pool of threads, answered on the loop with an
  `Outcome` and the application woken to paint it; with no application running it answers on the spot. One pool per
  kind of read. `TreeView.probe_in_background` and `FileDialog.read_directory` use it.
- **`TreeView` with `load_in_background`/`probe_in_background` never reads on the loop from a key**: Space/+/-
  and `[+]` ask `node_has_children` (a probe still out answers yes), Right and `/` open the branch and finish in
  `when_loaded(node, then)` (the cursor goes in, or the search scope lands on the first child, once the read is in;
  a `/` into a branch read empty is taken back; a cursor or search moved on meanwhile is left be). `locate()` still
  reads at once.
- **`MaskedLine`/`MaskedField`**: digits typed into fixed places; Left/Right, Home/End, Backspace/Delete blank a digit;
  a base-8 `MaskedField` takes 0-7 only. **`DateField`/`TimeField`** are masked lines with a `Calendar` (TVDEMO's
  `TCalendarView` with a cursor; month/year picked from lists by click, `M`/`Y`, or Tab) or a `TimePicker` dropped by
  `▐↓▌` or Alt+Down; Up/Down step by the place under the caret, PgUp/PgDn by ten times that, carrying.
  **The dropped `Calendar` spells the cursor's day under the weeks** in its button's `date_format`
  (`CalendarView.date_format`; empty, no row -- Navigator's *Calendar* window binds it to *Country support*'s), so it is `SPELLED_HEIGHT` tall.
  **A 12-hour time** is `%I` and `%p`: the mask's `A` is a place for the `a`/`p` of `am`/`pm` (then a literal `m`),
  set by `a`/`p` typed anywhere, turned over by Up/Down on it, refusing digits. **Spell and read such a time with
  `spell_time`/`read_time`** (`masked_line`), never `strftime`/`strptime`, whose `%p` is the C locale's word; the
  `TimeButton` does, and drops a 12-hour `TimePicker` (`twelve`): the hour 1-12, an `am`/`pm` column last that
  Up/Down turn over and `A`/`P` set, `values` still 24-hour, five columns wider (`width_for(seconds, twelve)`).
- **`CalendarView`** is the month without the drop-down: `Calendar` is `CalendarView` + `DropDown` with `inset = 1`
  (its frame) and `picked()` choosing; the view alone (`inset = 0`) answers `False` for keys it does not use, so Esc
  reaches its window. Styles name `CalendarView`, which matches both. Utilities > Calendar (`CalendarWindow`,
  TVDEMO's `TCalendarWindow`, a departure: DN 1.51 had no calendar) is one in a window.
  **Other calendars** are `navml/calendars.py` (Julian with both Easters as its `note()`, Hebrew, tabular Islamic,
  Persian by the 33-year rule, Indian national/Śaka, Ethiopian, Coptic; Reingold & Dershowitz's arithmetic on
  `date.toordinal()`, no tables), and the **Chinese** lunisolar one, which has no formula: its months are
  `navml/chinese_data.py`, generated by `tools/chinese_calendar.py` from the Hong Kong Observatory's 1901-2100
  tables (2069's file lacks 30 December, which the tool checks is harmless). It knows lunar years 1901-2099
  only: **`span()`** says which days a calendar knows, `to_date` refuses others, and the view's `calendar` is the
  Gregorian on a day outside it, so the month still shows and paging back in returns to it. Its leap month
  repeats a number (`number(year, month)` → `(6, True)`; names `Month 6`, `Leap 6`, zh 闰六月 by the `{month}`
  placeholder), a year on keeps the month by number, and `note()` names the year in the sexagenary cycle
  (pinyin with tones, so 戊 Wù and 午 Wǔ are separate keys) with the Spring Festival on New Year's day. Checked
  once by hand against lunardate's and LunarCalendar's tables: each differs from HKO in three years, never the
  same ones. **Umm al-Qura** (`UmmAlQura`, a subclass of the tabular `Islamic` with its month names) is the same
  shape: `navml/ummalqura_data.py`, month starts 1356-1500 AH generated by `tools/umm_al_qura.py` from
  R. H. van Gent's `islamcalendar_dat.js` (hijri-converter's MIT table is the same data, which it matched in all
  1741 boundaries). Sha'ban 1364 has 28 days in the published pre-1392 table; it is kept, `KNOWN` in the tool.
  Arabic's `auto` is it, not the tabular one, which differs on two days in three. **Japanese** eras, **Thai**
  (BE) and **ROC** (Minguo) are `Gregorian` subclasses that only write the year otherwise: `year_text(day,
  short=)` (an era can change mid-month, so the title asks the cursor's day), `year_label(year)` for the year list
  (`Reiwa 1 (2019)`; the list chooses by index, not by parsing), and `title(day, room)`, which falls back to the
  short form (`R1`, `2569`, `115`, `-1`) where the long one does not fit -- the width test measures `title()`.
  Japanese starts in 1873 (`span`), the gannen is written 1. **Bengali** is Bangladesh's 2019 revision, kept
  proleptically. **Korean** and **Vietnamese** are `Chinese` subclasses with another `data` module (and
  `new_year()`, `animals()` -- Vietnam's Buffalo and Cat). No open official table exists, so `tools/lunisolar.py`
  computes them: Meeus' new moons, his low-precision Sun (~0.01°), Espenak-Meeus ΔT, R&D's month rules, reckoned
  in each country's standard time of the day (Korea UTC+9, +8:30 in 1908-11 and 1954-61; Vietnam China's until
  1968, UTC+7 after, its pre-1967 years copied from the HKO table). **It verifies itself first**: reckoned in
  Beijing's time (Beijing mean time UTC+7:45:40 before 1929) it must give HKO's months, and does in 196 of 199
  years -- 1906, 1917, 1922 each have an event within ten minutes of midnight. Known dates it reproduces: Tết
  1968 (29 Jan), 1985 (21 Jan, a month before China), 2007; Seollal 1997, 2027 (a day after China). Events within
  ten minutes of local midnight are printed as where a published calendar could differ by a day.
  **Nepali** (Bikram Sambat, `navml/nepali_data.py`, `tools/bikram_sambat.py`): no formula is official and no
  table of the almanac's own is open. 1975-2083 BS are where two of three MIT packages' tables agree (read from
  their PyPI wheels as data; after 2083 one repeats its rows of 85 years before, another guesses); 2084-2156 are
  computed by the rule that gives 99.5% of the agreed month starts: the Sūrya Siddhānta sun (R&D), its ingress in
  UTC+5:30, Karka's before 05:33 to the day before and Makara's from 17:00 to the day after (the dharmaśāstra
  rule for the solstitial saṅkrāntis). The modern sun with any ayanamsa fits far worse (~82%). `note()` marks a
  computed year.
  **Badíʿ** (Baháʼí, `navml/badi_data.py`, `tools/badi.py`): 20 months in year order, Ayyám-i-Há the 19th (4 or 5
  days, `naw_ruz(y+1) - naw_ruz(y) - 361`), ʿAláʼ the 20th. Naw-Rúz 21 March before 172 BE; 172-221 BE are the
  World Centre's table (*Badíʿ dates 172 to 221 BE*, transcribed into the tool's `OFFICIAL`, its Ayyám-i-Há column
  agreeing); 222-257 are computed (Meeus ch. 27 equinox, NOAA sunset at Ṭihrán) by a method that gives 49 of the 50
  published -- 2026 is the equinox within half a minute of sunset, beyond a minute-accurate theory; any computed
  year that close is printed. Wikipedia's "183 BE begins 20 March 2026" is wrong; the table says the 21st. The
  English caption has no hotkey: every letter of it is taken in that menu.
  **Diyanet, MABIMS Indonesia, MABIMS Malaysia** are `TabledIslamic` subclasses (as `UmmAlQura` now is: a `data`
  module with `FIRST_YEAR`, `FIRST_MONTH`, `MONTH_STARTS`, `PUBLISHED_LAST`; `note()` marks computed months).
  `tools/hijri_criteria.py` writes them: van Gent's published months, then each crescent rule computed with
  `tools/moon.py` (Meeus ch. 47 Moon, self-tested: its conjunctions within 1.2 min of ch. 49's, 1900-2100), the
  rule verified on the published months first. Found by fitting: Malaysia = altitude 2 and elongation 3 degrees, or
  age 8 h alone, topocentric, anywhere in Malaysia -- 260 of 260; Indonesia the same over its territory (real
  places, Sabang to Merauke, not a box -- a box's ocean corners were the misses) but the age with the altitude,
  196 of 203 (its others were rulings, not the rule); Diyanet the 2016 Istanbul congress rule (5/8 anywhere
  before 0h UT, else the Americas' mainland -- its west coast, not a box -- if the conjunction came before
  Wellington's fajr), 137 of 140 since 2016. From 1443 AH both MABIMS are Neo-MABIMS (3/6.4), which no open
  table can verify.
  **Burmese** is Yan Naing Aye's algorithm (``ceMmDateTime``, MIT, ported with its notice): era constants and
  the published full-moon and watat exceptions, then ``m2j`` arithmetic; checked by porting ``j2m`` too (the
  independent closed form) -- the two agree on every day 1900-2100 (his JS could not be run here). A year runs
  from 1 Tagu; the year number officially changes at New Year's Day (Thingyan), which `note()` marks.
  **Tibetan** (Phugpa) is R&D's arithmetic: a leap month precedes the month of its number (`tibetan-from-fixed`
  takes month0 + 1 past day 30, the year + 1 past month 12 -- leaving that out put Losar 2019 a month late),
  day numbers skip and double, so `CalendarSystem.day_label()` (default: the place in the month) gives the number
  the grid prints. Checked against Losar 2019-2026. Both English captions have no hotkey: every letter is taken.
  **Chhankitek** (Khmer, Thai, Lao lunar) is ThyrithSor's ``momentkh`` (MIT, ported with its notice): the year's
  aharkun/avoman/bodithey decide a doubled Asadh (Pathamasadh, Tutiyasadh) or a 30-day Jesth; the months are
  stepped from 1 Boss 1900 by each month's own Buddhist Era (`getMaybeBEYear`). Cross-checked with momentkh's
  own conversion (year jumps, month steps, its overflow fix) transcribed: 0 days apart 1900-2100. A year here
  runs from 1 Pisakh, numbered by the BE it enters at Visakha Bochea. In a doubled-Asadh year Thailand and
  Laos keep Magha Puja and Vesak a month later than Cambodia (2023: 4 May against 3 June), so `note()` names
  both. **Afghan** Solar Hijri is the Persian with the zodiac months. The view's `system` puts the grid in one, and paging goes through it:
  `add_months`/`add_years` (a year on keeps the month by name, so Hebrew Adar ↔ Adar II), `month_days`,
  `month_names(year)` in **year order** (Hebrew Tishri is 1). `day` stays a `date`, so the row under the weeks
  spells it Gregorian by `date_format` whatever the grid is in -- unless **`label`** names a calendar, whose
  `spell()` it is then (`spelled()`; the Gregorian again on a day that calendar does not hold; its `note()` joins
  the tooltip's) -- and the drop-down, which writes a `strftime` line, stays Gregorian. **A month name plus a blank and four digits must fit 17 cells** between the arrows, in
  every catalogue (CJK counts two a character; `tests/test_calendars.py` checks each language). A calendar's
  `caption()` carries a menu hotkey and `name()` is `plain(caption())`, which also drops a trailing `(~X~)`.
  To add one: subclass `CalendarSystem` (`caption`, `from_fixed`, `to_fixed`, `days_in_month`, `month_names`,
  `months_in_year` if not 12), put it in `SYSTEMS`, add its key to `CountryData.CALENDARS`. Chinese and Umm
  al-Qura need tables; that's the next round. The window's *Calendar system* submenu (one radio-ticked
  `SetCalendarSystem(key)` per `SYSTEMS` entry, built in `__init__`, answered by the window) is
  `CalendarWindow`'s, and so is *Calendar view* (`SetCalendarView(view)`, `CountryData.VIEWS`: `only`,
  `gregorian_grid`, `selected_grid` the default, `both`), which sets each view's `system` and `label` by binding;
  `both` shows a second view, `other`, the Gregorian to the right of the calendar's, the window widening from `WIDTH` to `WIDE` (`size()`, an effect refits it;
  the Shell and a restored desktop size it by `size()`, not the constants) and two effects keeping the views on
  one day. Commands go to `view()`, the one with the keys. `only` and `both` spell nothing under the weeks
  (`unspelled()`: `date_format` and `label` left empty), and the window's views are `compact`: only the
  weeks the month has (`rows()`, at least `LEAST_WEEKS`), the spelled row right under them, so the window's height
  (`size()`: frame, two rows, `rows()`, the spelled row, a blank, the button) follows the month as it pages, its
  top edge kept. The drop-down keeps six weeks. `C` (`SwapCalendars`, the window's key table and *Calendar* menu) trades
  `gregorian_grid` and `selected_grid`, and in `only` flips the window's `swapped` (the Gregorian alone); refused
  (`refusal()`, greyed) in `both` or with the Gregorian chosen. Its key-bar hint (`key_hints()`) names the calendar
  `C` would show. `CalendarView.key_hints()` puts PgUp/PgDn, Ctrl+PgUp/PgDn and M/Y on the bar as three paired hints
  (`PgUp/Dn Month`, `^PgUp/Dn Year` -- Ctrl as a caret and the shared `Pg` said once, here alone; `M/Y Choose`)
  and `T Today`, read from the current bindings, then the window's `C` with `tr("Gregorian")`, a short word apart
  from the menus' `~G~regorian`. Measured tight (all items, one blank each) every catalogue fits 80 columns with F1
  and F10; Latvian exactly, Russian and Latvian with short captions (`Выбор`, `Григор.`, `Izvēle`, `Mēn.`) -- keep
  them short.
  **Its paging and picking are commands in a key table** (`navml/widgets/dialog/commands.py`: `PreviousMonth` PgUp,
  `NextMonth` PgDn, `PreviousYear`/`NextYear` Ctrl+PgUp/PgDn, `ChooseMonth` M, `ChooseYear` Y, `GoToToday` T, each
  letter with Shift too), Key bindings' *Calendar* section, so both the drop-down and the window have them; the
  arrows, Home/End, Enter and Tab mean something per section and stay `on_key`'s. Off an application no key table
  is consulted, so a test driving the view by `on_key` emits these instead. The window shows them on its *~C~alendar*
  bar menu and its right-click menu (a click on a day moves there first), and hands them on to the view when the
  button holds the keyboard (`CalendarWindow._month`); the menu's static `key:`s are for that case.
- **`HexLine`** (`navml/widgets/dialog/hex_line/`, Python alone) is DN's `THexLine` (`DIALOGS.PAS`): the bytes of the
  `InputLine` it is `link`ed to (`what.entry`), in its `encoding`, as hex pairs, edited as hex with DN's keys only
  (`0-9`/`A-F` high nibble then low, Left/Right a nibble, Backspace/Del a byte, Up is Shift+Tab, other letters
  swallowed). It keeps its own `data`, since a hex edit can make bytes that are no text in the encoding: the linked
  line shows them decoded (`U+FFFD` for what will not), and typing there makes `data` the text's bytes again (a
  character the encoding cannot say gives none). The two cursors follow each other; it does not mirror. Styled as
  `InputLine`. The viewer's *Find* box has one.
- **`ChoiceField`** is a `ChoiceLine` (an `InputLine` never typed into: every key but Tab/Shift+Tab/Esc/Alt+letter/
  Up/Down drops its list, Enter included; Up/Down step between the dialog's lines) over **`History.choices`**, a fixed
  list that records nothing and that typing quick-searches by the panel's rule.
- **Every `InputLine`** selects with a drag or double click (a finished selection is the primary selection) and takes
  Ctrl+Ins (copy; the whole line with no selection), Shift+Del, Shift+Ins, Ctrl+C (only with a selection), Ctrl+V;
  middle click pastes the primary selection. A paste walks the focus path when `Application.on_paste` declines it.
  `FileDialog.raw`, a test for a name line to hand back as typed (a place the dialog cannot list -- a URL), and
  recorded in the history as typed; `FileDialog(unlisted=PLACE)` lists nothing, shows PLACE and answers every name as
  typed, for a caller on another drive (Shift+F4) -- set no `raw` over it.
  `password: True` paints every character as `*` and copies nothing -- not to the clipboard, not to the primary
  selection (a `Field`'s line is `field.entry`: set `field.entry.password` from the Python half).

- **A modal never says its keys in its frame.** The keys a dialog takes that no control shows go to the key bar
  through `key_hints()` (navkit's `Widget` hook, asked from the focus out): `TabView`'s *Ctrl-PgUp/PgDn Tabs*, the
  history dialogs' list keys, the Attributes grid's R W X, `PopupMenu(hints=)` and `SubMenu.hints` for a popup's.
- **`FileDialog`** (`navml/widgets/dialog/file_dialog/`, DN's `TFileDialog` from `DNSTDDLG.PAS`, every rectangle
  `TFileDialog.Init`'s): `FileDialog(title=, label=, history_id=, directory=, wildcard="*", hidden=, ok_text=)` (*ok_text* `"~O~pen"` is
  DN's `fdOpenButton`), `execute()`
  answering a full path or None. OK is `Valid(cmFileOpen)` (`valid()`): a wildcard or a directory re-lists and stays
  up, a name in an existing directory closes, anything else says *Invalid drive or directory.*/*Invalid file name.*
  An effect stands for `cmFileFocused`: the focused list fills the name line (a directory as `dir/` + wildcard) and
  `FileInfoPane`. Left/Right move between controls outside the name line; Tab skips an empty *Files* list; Enter or a
  double click in a list is OK; the history records the full path. `FileList` (`dialog/file_list/`, `TFileList` and
  `TDirectoryList` in one) types to search as `TSortedListBox` did; `scan()` is navml's own directory reader (navml
  may not import Navigator's). Departures: no drives, no 8.3 completion, `*` for `*.*`. Styled `FileInfoPane` in
  `navigator.nss` (the Information pane, [61]).

- **`ColorSelector`** and **`ColorDisplay`** (`navml/widgets/dialog/color_selector/`, Python alone): TV's
  `TColorSelector` -- `color` an index into `COLORS` (the attribute byte's sixteen, by name), `-1` for none, swatches
  of blanks on the colour with TV's `◘` mark (`*` on ASCII), arrows wrapping as `TColorSelector.HandleEvent` did; no
  event, the owner follows `color` -- and `TColorDisplay`, `text` repeated in `sample` (a `Style`).
- **`GroupBox`** (`navml/widgets/dialog/group_box/`): Turbo Vision's `ofFramed` view with a `TLabel` on its frame
  line -- a single frame (the sheet's `border`), `title` two cells in on the top edge with a blank either side (`~A~`
  in `::shortcut`), children placed inside in its own coordinates (the frame is the outer row and column). It never
  takes the keyboard. System Information's four boxes are the first users.
- **`TabView`** (`navml/widgets/dialog/tab_view/`, Python alone, a `Layout`): pages behind a row of tabs -- not Turbo
  Vision's, which had none. Every child is a page, its tab captioned by the page's `title`.
  - **`TabPage`** (`navml/widgets/dialog/tab_page/`, markup alone): a page that is nothing but a `title`, for pages
    laid out inline in the dialog's own document -- their ids stay the dialog's (Alt+E's `AttrDialog`). A page of
    its own component (*Settings*' pages) needs none.
  - **The look.** Each tab is a box drawn in the sheet's `border`, `┌───┐` over `│ Caption │`. The tabs stand on a
    baseline across the whole width, closed off by `┴` feet. The current tab is double (`╔═╗`, `║`) with its foot
    open (`╜   ╙`), so it stands raised and joins the page under it.
  - **One row, scrolled.** When the tabs do not fit, a `←` at the left edge and a `→` at the right appear (arrows, `tab_view.ARROWS`, not the scrollbar's triangles; `^v<>` below Unicode), each only
    while a tab is hidden that way (`can_scroll()`). A click on one, or on top a notch of the wheel anywhere over the
    tabs, moves the row a tab along (`scroll()`) without changing the current tab. Down the left a notch of the wheel
    over the column chooses the tab above or below instead, stopping at the ends. The row never ends short with tabs
    hidden before it (`_start()`). An effect in `mounted()` (`_reveal`) moves `first` to bring the current tab into
    view however it became current.
  - **Pages.** `strip_rows` is 2 and **a page's row 0 is the baseline**, as a dialog's is its frame, so a former
    dialog's layout from `y: 1` carries over unchanged. Pages that are not `current` are hidden, which takes them
    out of the paint, the tab order and the Alt+letter walk. `select(index)` hides them and focuses the new page's
    first control in the same call.
  - **Keys.** The strip takes the keyboard, **last**: `focus_last` puts it after the dialog's own buttons in
    `Dialog.focusable`, so a dialog still opens on the page's first control, Tab past Cancel reaches the strip, and
    the next Tab goes into the page (`on_select_next`, taking `SelectNext` only while the strip has the keyboard, so
    the key stays rebindable; Shift+Tab from the page's first control comes back). While it has the keyboard,
    Left/Right and Up/Down (either side) step through the tabs, stopping at the ends, and Home/End go to them;
    `select()` then leaves the keyboard on the strip. Its current caption is drawn `TabView:focused::selected` (a
    focused button's colour). From anywhere on a page Ctrl+PgDn/Ctrl+PgUp (and Ctrl+Tab/Ctrl+Shift+Tab) are
    `NextTab`/`PreviousTab` in its key table (`[tab_view]`), wrapping round, and so are plain PgDn/PgUp -- reached only
    where the control with the keyboard does not take them first (a list pages, a `MaskedLine` steps by 10). A
    `ListViewer`, `MaskedLine` or `MaskedField` with `page_keys: False` gives them way (the arrows still move it);
    every list and number field on *Settings*' pages says so. `ListViewer` leaves Ctrl+PgDn to them as
    it already did Ctrl+PgUp. **Each page remembers its control** that last had the keyboard (`_remember`, an effect on
    `app.focused` that only records into a plain dict): Ctrl+PgDn/PgUp or a click back to a page returns there if it
    can still take it, else to the page's first control (`enter_page`); so does Tab from the strip. A click on a tab selects it and moves the keyboard to its page: its top, its caption
    or its foot on the baseline (`in_strip`). The baseline is the page's row 0, but a page leaves it empty, so the
    click falls out to the `TabView`.
  - **Down the left** (`side: "left"`). A tab a row in a `column` (the longest caption plus 3, at most `MAX_COLUMN`
    20; a longer caption is cut with `glyphs.ellipsis`), an unbroken `│` rule beside it the whole height, and the
    pages to its right. The current tab has a `►` before it and the selected caption colour. More tabs than rows
    scroll between `↑` and `↓` in the column's top and bottom rows. With `joins_frame` the `TabView` spans its
    parent's frame rows: the rule meets the frame in that frame's tees (`joins(parent.border)`: `╤` and `╧` on a
    double frame), the tabs and pages keep to the rows between, and clicks on the frame rows, or right of the
    column, fall through to what is behind (the dialog's title and buttons).
  - **Simple** (`side: "simple"`). The row on top without the boxes: each tab is `_size()` = ` caption `, caption +
    2 cells, in `::tab`, the current one in its own `::current` part (no mark: a button's background,
    `TabView:focused::current` a focused button's, so it stands out from the dialog's), over a single rule the whole
    width (`_baseline()`, shared with the boxed strip). **The rule is the page's first row** (`plan()` puts pages at
    `y` 1), as the boxed strip's baseline is, so it costs two rows where that costs three. It scrolls, wheels and
    clicks as on top (`←`/`→` at the row's ends, on row 0); with `joins_frame` the rule meets the frame in `╟`/`╢`.
  - **`joins_frame` on top** spans the frame's columns instead: the baseline meets the frame in `╟` and `╢`, the
    rows above it leave the frame's bars alone, and the tabs, arrows and pages keep to the columns between. The same `first`, `scroll()`, `_reveal` and wheel serve both sides: a
    tab's size along the strip is its width on top and one row on the left (`_sizes()`, `_length()`).
  - **Parts.** `tab`, `selected` (a selected label's colour) and `arrow` (the frame icons').

  Navigator's *Settings* is the first user.

## History

`navml/history.py`'s `HistoryStore`/`HISTORY` is DOS Navigator's `HistList`: per-id lists, newest first, `limit` each (DN's 20; Navigator sets it from `interface.history_size`, default 50),
pinned entries kept (`HistoryStore.limit`). The `History` button drops a `HistoryList`, which `Field(history_id=...)` places after its line.
**Del in a `HistoryList` forgets the entry under the cursor** (`HistoryList.forget` -> `HistoryStore.remove`; a
departure, asked for, as Alt+F8's list does), the cursor staying on the row that moves up and the list closing with
its last entry; a `choices` list and a `CompletionList` (no button) ignore it.
Ids in use: `"mkdir"`, `"select"`, `"command"`, ... Slots `[53-56]`. The lists persist: they are rows of the `history`
table (`navml/models/history_entry/`, DN's rules in its `.py` half's `remember()`), written as each change is made
(see `navkit-database`). Tests get an empty `:memory:` database each.

## Four rules from building dialogs (each found by running something)

- **A handler starts a dialog; it does not wait for one.** `await dialog.execute(app)` inside `on_key` mounts it and
  never paints it: `_main_loop` awaits `_handle` before rendering and is the queue's only consumer. Use
  `self.spawn(self._work())` and return. `Dialog.execute` raises rather than hanging.
- **A dialog's geometry must be bound, not assigned.** `add()` lays a child out into its parent and `Component.layout`
  steps around a side only when it carries a binding, so a literal size becomes full-screen the moment `overlay()` adds
  it. Route the size through a declared property the base binds from.
- **A derived component's own children land after its base's** (`super().__init__()` is the generated constructor's
  first line); `Dialog.focusable()` moves its buttons to the end, or every derived dialog opens with focus on OK, and
  `Dialog.activate_shortcut()` asks them last, or ~C~ancel takes Alt+C from *Compare ~c~ontents* (TV gave a shared
  letter to the control inserted first, and resources inserted buttons last).
- **Effects belong in `mounted()`, not `__init__`**, for any widget that can be removed and put back -- every widget in
  a dialog. `remove()` disposes a subtree's effects.

## Layouts

`HorizontalLayout`, `VerticalLayout`, `GridLayout`, `DockLayout`, `StackLayout` (`navml/widgets/layout/`), on a
Python-only `Layout` that paints nothing, replaced every container's placement arithmetic. A child asks for room with
**style hints the layout reads off the child** -- `basis`, `grow` (default 1, so silent siblings share evenly), `dock`
-- so a `style:` block or a sheet rule says it. A layout re-arranges from an effect on its own size, its children's
`visible` and hints, so a child's geometry is navigated and its markup says nothing about it. `Field` is
`Field(HorizontalLayout)`, `Shell` is `Shell(DockLayout)`, `Manager`'s panels sit in an id'd `HorizontalLayout`, and
`Dialog`'s buttons in a `ButtonRow`. All conversions paint `cmp`-identically on a pty.

- **A layout can answer for a child that says nothing**: `LinearLayout.hints(child)` returns `(basis, grow)`, by
  default the child's own style hints. Override it rather than writing hints onto every child.
- **`ButtonRow`** (`navml/widgets/dialog/button_row/`, Python only) is a `HorizontalLayout` with `spacing` 2,
  `justify: "center"` and `height` 2. Every child takes `button_width` (11, DN's usual) and `grow` 0. A child's own
  `style:` `basis` wins. `button_width: 0` sizes each `Button` by its caption plus `BUTTON_CHROME` (5). A hidden button
  gives up its slot, so the rest stay centred.
- **A dialog that needs other buttons declares its own `ButtonRow`** under `anchors: left: 0 / right: 0 / bottom: 2`
  and says `buttons: "none"`, rather than hand-placing x values. Where DN's columns are not exactly centred, keep them:
  `justify: "start"` with `anchors: left: X` at the first button's column, and DN's `spacing`/`button_width` (Overwrite
  query, the UU boxes).
- **`buttons: "none"` is Dialog's "no row of mine"**: `row` is bound `visible: root.buttons != "none"`, so
  `self.row.visible = False` in a Python half now raises (a value over a binding). **The message shows only while
  `prompt` is non-empty**: an empty one paints nothing, so a dialog of controls needs no line hiding it.
- Geometry outside a layout is better said with an `anchors:` block (`navml-markup`) than with
  `parent.width - K` arithmetic.

## The About dialog

≡ > About is DN's `MessageBoxAbout` (`navigator/widgets/about_dialog/`): `Dialog` with `buttons: "ok"` and `message`
centred. Its facts are never written twice: `navigator/lib/utilities/about.py`'s `project_info()` reads `pyproject.toml`'s
`[project]` in a checkout and the installed `METADATA` otherwise. The README screenshot shows it open, so a version bump
makes `tools/screenshot.py --check` stale (regenerate it with the bump; no test checks that scene). The home page is an OSC 8 hyperlink.

## Read when

| Reference | Read when |
|---|---|
| `reference/widget-library.md` | button drawing, `disabled`/`inert`, shortcuts, rows-are-not-widgets, the dialog rules in full, what came from `Panel`, where colours live, `Timer` |
| `reference/layouts.md` | layout hints and rules |
| `reference/history.md` | `HistoryStore`, `HistoryList`, `History.choices` |
| `reference/from-textual.md` | what the library takes from Textual |
