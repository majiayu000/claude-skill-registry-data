---
name: clay-layout
description: >
  Clay-Layout in zid: Fallstricke, die im Projekt schon Zeit gekostet haben —
  Elementgrenze, Mindestbreite von Text ohne Umbruch, verschachteltes Clipping,
  feste IDs in Schleifen, Fehlerbehandlung, Virtualisierung.
  Use when touching Clay layout code (clay.UI, clay.text, ElementId, sizing, clip),
  when a Clay error appears ("Layout elements exceeded", "duplicate_id"), when an
  element overflows its container, when text is clipped or misaligned, or when a
  list renders a large document, or when touching the patched clay.h
  (libs/clay-zig, vendor/clay.h, Clay hash map, text measure cache, scroll containers).
---

# Clay in zid

Clay ist CSS-nah, aber die Voreinstellungen unterscheiden sich an ein paar Stellen.

## Zuerst messen, dann ändern

Bei jedem Layout-Problem **erst die tatsächliche Geometrie holen**, bevor irgendetwas
geändert wird:

```python
result_json("element_bounds", ["mein_element"])       # {found, x, y, w, h}
result_json("element_bounds_i", ["prefix", index])
```

Ohne die gemessene Zahl rät man an Symptomen herum.

`element_bounds` beantwortet **nicht** „existiert das Element gerade?" — Clay behält
Daten verschwundener Elemente. Dafür `ui_state` nehmen.

## Text ohne Umbruch ist eine Mindestbreite

`clay.text(..., .{ .wrap_mode = .none })` meldet die volle Textbreite als Mindestmaß.
Clay zieht Zeile, Liste und Kasten darauf auf. Das entspricht `min-width: auto` bei
einem Flex-Element in CSS, nur ohne bekannten Gegenschalter.

**Abhilfe:** Obergrenze auf dem Container.

```zig
.sizing = .{ .w = .growMinMax(.{ .min = 0, .max = ROW_WIDTH }), .h = .fixed(H) }
```

Danach muss der Text selbst passen, also kürzen (siehe `src/ui/path_display.zig`).

## Erst prüfen, ob der Rahmen mitwachsen darf

Nicht vorschnell selbst rechnen. Der Standardweg ist dynamisch:

- Rahmen `.w = .fit`, Kinder `.w = .grow` → Clay misst das breiteste Kind und zieht
  alle anderen darauf. So stehen Kürzel in den Aufklappmenüs rechtsbündig, ohne dass
  irgendwer misst.
- Nur wenn der Rahmen **fest** sein muss (Modal mit fixer Breite) und der Inhalt
  unbegrenzt ist (Dateipfade), braucht es Obergrenze plus Kürzen.

Für eigenes Messen: `ui.measureTextWidth(text, font_size)`. Zeichen zu zählen geht
schief, sobald zwei Schriftgrößen in einer Zeile stehen.

## Verschachteltes Clipping ersetzt das äußere

`.clip` auf einem Kind eines bereits clippenden Containers **schneidet sich nicht** mit
dem äußeren Bereich, es ersetzt ihn; ein Clip auf der Zeile lässt die Liste aus ihrem
Kasten laufen. Also kein Clip als Notnagel gegen Überlauf — die Größe
begrenzen.

## Kinder dürfen einen `.grow`-Container nie überragen

Clay reicht die **Mindesthöhe** der Kinder durch alle Eltern bis zur Wurzel, sobald ein
Container auf der Achse nicht clippt. Ein `.grow`-Container wird dann nicht kleiner als
sein Inhalt, und die Wurzel wächst über das Fenster hinaus. Wer die Kinderzahl aus der
eigenen Bounding-Box des Vorframes ableitet (`getElementData(...).height`), baut damit
eine Rückkopplung, die das Layout Frame für Frame wachsen lässt.

Regel: Wer Inhalt aus der gemessenen Höhe ableitet, zieht Innenabstände ab
(`CodeEditor.minimapWindow`, unit-getestet) **und** clippt den Container auf der Achse
(`.clip = .{ .vertical = true }`), damit ein Rechenfehler nicht mehr nach oben durchschlägt.
Die Zeilenschleife des Editors (`visible + 1` Reihen) ist nur deshalb harmlos, weil
`editor_scroll` vertikal clippt. `python3 scripts/e2e_layout_stable.py` prüft, dass
`editor_state.height` über Frames konstant bleibt; mit `ZID_DEBUG=1` listet jeder
Headless-Screenshot alle Render-Commands mit Box, daran sieht man wachsende Elemente.

## Text muss den Frame überleben

`clay.text(slice, …)` merkt sich **den Zeiger**, gezeichnet wird erst nach `endLayout`.
Der Text muss also mindestens bis dahin leben: Zustand der UI, Frame-Arena oder eine
Konstante — nie ein Stack-Puffer und nie das Feld einer **Kopie**.

```zig
if (state.creating) |cs| renderCreateRow(arena, cs, …);   // FALSCH: cs ist eine Kopie
if (state.creating) |*cs| renderCreateRow(arena, cs, …);  // richtig: Zeiger in den Zustand
```

Mit einer Kopie oder einem `bufPrint`-Stackpuffer zeichnet Clay zufälligen Speicher (leere
Kästchen).

Prüfen lässt sich das nur am **gezeichneten** Text, nicht am Zustand über RPC: headless
mit `ZID_DEBUG=1` einen Screenshot ziehen, im Command-Dump steht je Textstück
`text id=… len=… "…"`. `scripts/e2e_explorer.py` (`drawn_text`) tut das.

## Kein `return` im Kinderblock

```zig
clay.UI()(.{ .id = ... })({
    if (leer) { message(); return; }   // FALSCH: Element wird nie geschlossen
});
```

`clay.UI()(config)` öffnet das Element, der Block `({ ... })` ist nur das Argument des
schließenden Aufrufs. Ein `return` darin verlässt die Funktion, bevor Clay schließt. Folge:
`panic: load of null pointer` in `Clay__SizeContainersAlongAxis` beim nächsten `endLayout`.
Stattdessen `if … else` oder den Inhalt in eine eigene Funktion auslagern
(`GitHistoryView.renderRows`).

## Feste IDs gehören nie in eine Schleife

```zig
.id = clay.ElementId.ID("indent"),          // FALSCH in einer Zeilenschleife
.id = clay.ElementId.IDI("indent", @intCast(index)),  // richtig
```

Ohne Index meldet Clay `duplicate_id`. Wird das Element
nirgends abgefragt (Abstandhalter), einfach **keine ID** vergeben.

Dasselbe gilt für Komponenten, die **mehrfach im Frame** stehen (Editor in zwei Panes):
ungesalzen wären die IDs in beiden Panes gleich, und `getElementData` der zweiten Pane bekäme
die Box der ersten. Alle IDs eines Editors laufen deshalb über `CodeEditor.idi(name, index)`, das den Editor-Zeiger als Salz
addiert (unit-getestet). E2E: `element_bounds(_i)` sucht erst global, dann über die aktive
Vorschau und den aktiven Editor, Skripte dürfen weiter `element_bounds_i("code", zeile)` fragen.

PDF-, Bild- und Binäransicht (`PdfViewState.idi`, `ImageViewState.idi`, `binary_view.idi`) sind
zustandslos und bekommen das Salz als Parameter: `UI.renderPane` reicht `paneSalt(pane)` durch,
sonst liest der Treffertest der Blätter-Schaltflächen die Box der ersten Pane. Treffertests außerhalb von `renderPane`
(Hand-Cursor in `getDesiredCursor`) nehmen `UI.activePaneSalt`, E2E-Abfragen über
`lookupElement` in `src/e2e_server.zig` probieren dasselbe Salz als Fallback.

Die Markdown-Vorschau (`MarkdownView.idi`) salzt mit Instanz **und** Pane (`pane_salt`, setzt
`UI.renderPane`): Views hängen am Pfad, ein Split kopiert die Tabs, dieselbe Ansicht steht dann
in zwei Panes. Chat und Terminal kopiert `TabBarState.cloneFrom` gar nicht erst, ihr Zustand
(Chat-Eingabe ist ein CodeEditor) kann nur einmal je Frame gezeichnet werden; sie bleiben in der
ersten Hälfte, die die ursprüngliche Tab-Leiste übernimmt.

Das Log nennt die doppelte ID selbst: `duplicate_id id=… unter Elternelement id=…`, dazu beim
ersten Auftreten einer Sitzung eine Liste aller mehrfach vergebenen IDs mit Box und Text
(`UI.logDuplicateIds`). `python3 scripts/clay_id_decode.py <id> [--parent <eltern-id>]` rechnet
sie auf Namen zurück (nur ungesalzene IDs). Für gesalzene IDs headless mit `ZID_DEBUG=1` einen
Screenshot ziehen und im Command-Dump nach mehrfach vorkommenden `id=` suchen.

## Elementgrenze

Clays Standard sind 8192 Elemente pro Frame. Beim Überlauf erscheint rot
„Layout elements exceeded Clay__maxElementCount" und der Lauf bricht ab.

Reihenfolge laut Clay-README, sie ist zwingend:

```zig
clay.setMaxElementCount(N);          // zuerst
const min_memory = clay.minMemorySize();  // hängt an N
// Arena mit dieser Größe anlegen, dann clay.initialize
```

Arenagröße je Grenze: 8192 → 10 MB, 16384 → 12 MB, 32768 → 24 MB, 65536 → 47 MB.
`UI.MAX_CLAY_ELEMENTS` steht in `src/ui/mod.zig`.

Die Grenze anzuheben ist die zweitbeste Lösung. Die beste ist Virtualisierung.

## Fehler landen im Log, nicht nur im Fenster

`clay.initialize(arena, dims, .{ .error_handler_function = clayError })`. Ohne Handler
malt Clay die Meldung nur ins Fenster, headless sieht man gar nichts.

**Prüfe nach Layout-Arbeit das Log auf `error(ui): Clay:`.**
`scripts/e2e_md_preview.py` tut das automatisch.

## Gepatchte clay.h unter libs/clay-zig/vendor

Das Submodul zeigt auf den eigenen Fork `gstrainovic/clay-zig-bindings`, Branch `zid`
(Upstream johan0A als Remote `upstream`). Dort liegen vier Fixes als Commits `598a5c7`
(Scroll-Container), `27407cd` (Hash-Map), `7c66140` (Messcache) und `72d89dd` (Umbruch mit
fremden Wörtern), alle Stellen mit „zid:“ markiert. Für eine neuere clay.h den Branch `zid` auf
upstream rebasen. `libs/clay-zig/build.zig` legt `vendor/clay.h` vor die Abhängigkeit.

- **Scroll-Container (`598a5c7`):** drei Stellen in `Clay_UpdateScrollContainers` gegenüber
  v0.14: Swap-Remove ohne `i--` übersprang Einträge, `Clay__GetHashMapItem` liefert nie `NULL`
  (sondern `&Clay_LayoutElementHashMapItem_DEFAULT`), und der Zeiger auf das Clip-Element wird
  vor dem Zugriff geprüft (sonst Absturz „member access within null pointer of type
  Clay_ClipElementConfig“, z. B. Multi-File-Diff nach Diff-Tab im selben Pane). zid benutzt
  Clays Scroll-Positionen nicht, aber jedes `.clip`-Element legt dort einen Eintrag an, und nur
  `UI.updateScroll` räumt die (10 Einträge große) Liste auf.
- **Hash-Map der Element-IDs (`27407cd`):** sie liegt im persistenten Speicher, jede je gesehene
  ID (auch anonyme Textstücke: Hash aus Eltern-ID und Kindindex) belegt einen Eintrag. Bei
  voller Kapazität `maxElementCount` liefert `Clay__AddHashMapItem` still `NULL`: neue Elemente
  haben keine Bounds, kein Hover, keinen Klick. `Clay__CompactLayoutElementsHashMap` läuft
  deshalb in `Clay_BeginLayout`, sobald die Map zu drei Vierteln voll ist: behält Einträge der
  letzten drei Frames, verdichtet `debugElementData` im Gleichschritt und baut die Buckets neu.
  Für E2E: `element_bounds` verschwundener Elemente bleiben nur, bis verdichtet wird — darauf nie
  bauen (siehe `visible_blocks` in `e2e_md_preview.py`). Bei „Element X nicht im Layout“, obwohl
  X sichtbar ist: zuerst an diese Map denken.
- **Messcache der Texte (`7c66140`):** Clay gibt Einträge nur frei, wenn ein Nachschlagen zufällig
  über einen veralteten Eintrag im selben Bucket läuft; eine gestreamte Chat-Antwort (ein
  wachsender Absatz) füllt so die Wortgrenze (16384, „run out of space in it's internal text
  measurement cache“), danach bleibt Text ungemessen. `Clay__ResetMeasureTextCacheWhenFull`
  leert den Cache in `Clay_BeginLayout`, sobald Wort- oder Eintragsliste zu drei Vierteln voll
  ist. Unit-Test `src/ui/clay_cache_tests.zig` (eigenes Test-Root mit Clay, ohne UI).
- **Umbruch mit fremden Wörtern (`72d89dd`):** der Messcache schlägt über einen 32-Bit-Hash des
  Inhalts nach; der SIMD-Hash auf x86_64 bezieht die Länge nicht ein („ab“ und „ab\0\0“
  kollidieren), und `Clay__MeasureTextCacheItem_DEFAULT` zeigt mit Wortindex 0 auf eine
  beliebige Wortliste. Einträge tragen deshalb die Textlänge, DEFAULT wird ungebrochen
  ausgegeben, Wörter hinter dem Textende beenden den Umbruch (sonst Lesen hinter dem Puffer,
  bei leerem Text „applying non-zero offset to non-null pointer 0xffffffffffffffff“ in
  `Clay__CalculateFinalLayout`). Test im selben Test-Root; dort teilen sich alle Tests einen
  Clay-Puffer, weil der aktuelle Kontext nicht zurückgesetzt werden kann.

## Große Inhalte virtualisieren

Ein langes Dokument nicht komplett anlegen. Muster in
`MarkdownView.renderDocumentVirtualized`:

1. Höhe je Block aus dem letzten Frame merken (`getElementData` auf `IDI(name, i)`).
2. Sichtbaren Indexbereich aus Scroll-Offset und Viewport bestimmen, ein Bildschirm
   Vorlauf in beide Richtungen.
3. Davor und danach je einen Abstandhalter mit der Summe der übersprungenen Höhen.

Noch nie gezeigte Blöcke brauchen eine Schätzung. `estimateBlockHeight` rechnet sie aus
Blockart und Textlänge: Überschriften nach Ebene, Codeblöcke nach Zeilenumbrüchen (sie
brechen nicht um), Fließtext aus Zeichenzahl geteilt durch Zeichen je Zeile, Container
als Summe ihrer Kinder; eine feste Zahl läge bei Tabellen und Codeblöcken weit daneben.

Achtung: dasselbe Render-Verfahren wird oft an zwei Stellen benutzt (Vorschau und
Chat). Virtualisieren nur dort, wo es einen echten Viewport gibt.
