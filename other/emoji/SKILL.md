---
name: emoji
description: >
  Farbige Emoji in zid: Rückfall-Schrift (Linux CBDT über FreeType, Windows Segoe UI Emoji über DirectWrite-Farbschichten und MuPDFs HarfBuzz), Bitmap-Skalierung, Farbatlas, zusammengesetzte Zeichen. Use when touching src/text/emoji_font.zig, bitmap_scale.zig, src/text/backends/directwrite/*, emoji_hb.c, glyph cache color atlas, text_atlas.wgsl, or scripts/e2e_emoji.py.
---

## Farbige Emoji (`src/text/emoji_font.zig`, `bitmap_scale.zig`)

- JetBrains Mono hat keine Emoji. `TextSystem.shapeText` prüft je Textstück, ob ein
  Zeichen in der Hauptschrift fehlt (`FreeTypeFace.hasCodepoint`), und zerlegt den Text
  dann in Läufe: Hauptschrift und Emoji-Schrift getrennt, weil HarfBuzz je Aufruf nur eine
  Schrift kennt. Emoji-Glyphen bekommen `font_ref` und `is_color`; `resolveGlyphBatch`
  schickt sie an `GlyphCache.getOrRenderFallback`.
- Brauchbar ist nur eine **Bitmap**-Emoji-Schrift (CBDT, `FreeTypeFace.isColorBitmapFont`).
  Die COLRv1-Fassung, die Fedora ausliefert, besteht aus Malanweisungen; FreeType 2.13
  malt sie nicht aus und liefert ein leeres Bitmap. Debian, Ubuntu und Arch haben CBDT,
  sonst lädt zid NotoColorEmoji (10 MB, Fassung v2.047) einmalig nach
  `<AppData>/zid/fonts/` — derselbe Weg wie bei der KI-Selbsteinrichtung.
- Bitmap-Schriften lassen keine freie Grösse zu: `finishFace` wählt über `FT_Select_Size`
  die nächstliegende feste Grösse und merkt `strike_scale`; `renderStrikeGlyph` verkleinert
  das 128-px-Bild mit `bitmap_scale.downscaleBgraToRgba` (Kastenfilter, BGRA nach RGBA, ohne
  Vormultiplikation). HarfBuzz meldet für solche Schriften **keinen Vorschub**; ohne
  `FreeTypeFace.strikeAdvance` stünde das nächste Zeichen im Emoji.
- Zwei Atlanten: Text bleibt einkanalig, Emoji liegen in `GlyphCache.color_atlas` (RGBA).
  Der Vertex trägt einen Schalter (`location(3)`), `shaders/text_atlas.wgsl` mischt zwischen
  Maske und Farbbild. Die SVG-Schicht hat deshalb einen eigenen Shader
  (`shaders/svg_atlas.wgsl`), weil die zusätzliche Vertexspalte nicht zur `svg_pipeline` passt.
- **Windows:** Rückfall ist Segoe UI Emoji (`seguiemj.ttf`, COLR, liegt
  jedem Windows bei), kein Download. MuPDFs FreeType taugt dafür nicht (ohne PNG und
  eingebettete Bitmaps gebaut, `slimftoptions.h`). `DirectWriteFace` bietet `hasCodepoint`,
  `rawFace` (Zeiger auf die Face selbst), `isColorBitmapFont` (hier: hat COLR-Schichten,
  geprüft an 😀) und `renderColorGlyph`: `IDWriteFactory2.TranslateColorGlyphRun` liefert
  einfarbige Schichten, jede wird über die GDI-Bitmap in Graustufen gerastert und mit
  `bitmap_scale.blendLayer` eingefärbt übereinandergelegt; Masse aus der Em-Box. Glyphen ohne
  Schichten (`DWRITE_E_NOCOLOR`, etwa ⚠ in Textform) kommen einfarbig statt als Fehler, der
  den Frame abbräche. Formen: `SimpleShaper` kann keine Ligaturen, deshalb formt
  `DirectWriteFace.shapeRun` Emoji-Läufe mit dem HarfBuzz aus MuPDFs Drittbibliothek
  (`src/text/backends/directwrite/emoji_hb.c`: Symbole `fzhb_*`, Speicher über einen eigenen
  MuPDF-Kontext, jeder Aufruf zwischen `fz_hb_lock`/`fz_hb_unlock`). Damit gehen ZWJ-Folgen,
  Hautton und Tasten. Flaggen bleiben Buchstaben („DE“): Segoe UI Emoji hat keine
  Länderflaggen, Windows zeigt sie selbst so. Der ZWJ wird wie die Variantenwähler beim
  Anhängen verworfen, sonst stünde er ohne Ligatur als Strich im Satz.
  `hasCodepoint` merkt sich die Antworten für die BMP (`cp_cache`, Bitfelder auf dem Heap):
  ohne ihn kostet jedes Formen ohne Cache-Treffer einen COM-Aufruf je Zeichen über ASCII.
- macOS (CoreText) hat keinen Rückfall (`emoji_fallback_supported`), Emoji bleiben leer.
- Zusammengesetzte Zeichen dürfen nie getrennt geformt werden: U+FE0F verlangt die farbige
  Form (⚠️ gegen ⚠), U+20E3 macht eine Taste (1️⃣), ZWJ verbindet (👩‍💻), dazu Hautton und
  Tag-Zeichen. `emoji_font.continuesCluster` nennt sie; die Zerlegung hält sie beim
  Grundzeichen, und `MarkdownView.appendPiece` klebt sie ans vorige Stück, weil zigdown
  `1️⃣` in `1` und den Rest zerlegt. Die Wähler selbst werden beim Formen verworfen: beide
  Schriften bilden sie auf ein Ersatzzeichen mit Vorschub ab, das eine Lücke hinterliesse.
- Zum Anschauen: `scripts/fixtures/emoji_test.md` (Überschrift, Liste, Tabelle, Codeblock,
  Randfälle). E2E: `python3 scripts/e2e_emoji.py` öffnet eine Textdatei und diese Datei in
  der Vorschau, wartet notfalls auf den Download und zählt bunte Pixel.
