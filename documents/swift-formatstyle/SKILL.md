---
name: swift-formatstyle
description: "Format values for display using the FormatStyle protocol and its concrete types. Use when formatting numbers (integers, floating-point, decimals), currencies, percentages, dates, date ranges, relative dates, durations (Duration.TimeFormatStyle, Duration.UnitsFormatStyle), measurements, person names (PersonNameComponents.FormatStyle), byte counts (ByteCountFormatStyle), lists (ListFormatStyle), and URLs (URL.FormatStyle). Also covers creating custom FormatStyle conformances and replacing legacy Formatter subclasses. FormatStyle is available iOS 15+; Duration styles require iOS 16+."
---

# Swift FormatStyle

Format values for human-readable display using the `FormatStyle` protocol
and Foundation's concrete format styles. Replaces legacy `Formatter` subclasses
with a type-safe, composable, cacheable API.

Docs: [FormatStyle](https://sosumi.ai/documentation/foundation/formatstyle)

## Contents

- [Quick Reference](#quick-reference)
- [Numbers](#numbers)
- [Currency](#currency)
- [Percentages](#percentages)
- [Dates](#dates)
- [Durations](#durations)
- [Measurements](#measurements)
- [Person Names](#person-names)
- [Lists](#lists)
- [Byte Counts](#byte-counts)
- [URLs](#urls)
- [SwiftUI Integration](#swiftui-integration)
- [Custom FormatStyle](#custom-formatstyle)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)

## Quick Reference

| Type | Style Access | Example |
|------|-------------|---------|
| `Int`, `Double` | `.number` | `42.formatted(.number.precision(.fractionLength(2)))` → `"42.00"` |
| Currency | `.currency(code:)` | `29.99.formatted(.currency(code: "USD"))` → `"$29.99"` |
| Percent | `.percent` | `0.85.formatted(.percent)` → `"85%"` |
| `Date` | `.dateTime` | `Date.now.formatted(.dateTime.month().day().year())` |
| Date range | `.interval` | `(date1..<date2).formatted(.interval)` |
| Relative date | `.relative(presentation:unitsStyle:)` | `date.formatted(.relative(presentation: .named))` → `"yesterday"` |
| `Duration` | `.time(pattern:)` | `Duration.seconds(3661).formatted(.time(pattern: .hourMinuteSecond))` → `"1:01:01"` |
| `Duration` | `.units(allowed:width:)` | `Duration.seconds(90).formatted(.units(allowed: [.minutes, .seconds]))` → `"1 min, 30 sec"` |
| `Measurement` | `.measurement(width:)` | `Measurement(value: 72, unit: UnitTemperature.fahrenheit).formatted(.measurement(width: .abbreviated))` |
| `PersonNameComponents` | `.name(style:)` | `name.formatted(.name(style: .short))` → `"Tom"` |
| `[String]` | `.list(type:width:)` | `["A","B","C"].formatted(.list(type: .and))` → `"A, B, and C"` |
| Byte count | `.byteCount(style:)` | `Int64(1_048_576).formatted(.byteCount(style: .memory))` → `"1 MB"` |
| `URL` | `.url` | `url.formatted(.url.scheme(.never).host().path())` |

## Numbers

```swift
// Default locale-aware formatting
let n = 1234567.formatted()  // "1,234,567" (en_US)

// Precision
1234.5.formatted(.number.precision(.fractionLength(0...2)))  // "1,234.5"
1234.5.formatted(.number.precision(.significantDigits(3)))    // "1,230"

// Rounding
1234.formatted(.number.rounded(rule: .down, increment: 100)) // "1,200"

// Grouping
1234567.formatted(.number.grouping(.never))                   // "1234567"

// Notation
1_200_000.formatted(.number.notation(.compactName))           // "1.2M"
42.formatted(.number.notation(.scientific))                    // "4.2E1"

// Sign display
(-42).formatted(.number.sign(strategy: .always()))            // "+42" / "-42"

// Locale override
42.formatted(.number.locale(Locale(identifier: "de_DE")))     // "42"
```

Docs: [IntegerFormatStyle](https://sosumi.ai/documentation/foundation/integerformatstyle),
[FloatingPointFormatStyle](https://sosumi.ai/documentation/foundation/floatingpointformatstyle)

## Currency

```swift
29.99.formatted(.currency(code: "USD"))   // "$29.99"
29.99.formatted(.currency(code: "EUR"))   // "€29.99"
29.99.formatted(.currency(code: "JPY"))   // "¥30"

// Customize precision
let style = FloatingPointFormatStyle<Double>.Currency(code: "USD")
    .precision(.fractionLength(0))
1234.56.formatted(style)  // "$1,235"
```

## Percentages

```swift
0.85.formatted(.percent)                                      // "85%"
0.8567.formatted(.percent.precision(.fractionLength(1)))       // "85.7%"
42.formatted(.percent)                                         // "42%"  (integer)
```

## Dates

```swift
let now = Date.now

// Components
now.formatted(.dateTime.year().month().day())           // "Apr 22, 2026"
now.formatted(.dateTime.hour().minute())                // "4:30 PM"
now.formatted(.dateTime.weekday(.wide).month(.wide).day()) // "Wednesday, April 22"

// Predefined styles
now.formatted(date: .long, time: .shortened)            // "April 22, 2026 at 4:30 PM"
now.formatted(date: .abbreviated, time: .omitted)       // "Apr 22, 2026"

// ISO 8601
now.formatted(.iso8601)                                 // "2026-04-22T16:30:00Z"

// Relative
let yesterday = Calendar.current.date(byAdding: .day, value: -1, to: .now)!
yesterday.formatted(.relative(presentation: .named))    // "yesterday"
yesterday.formatted(.relative(presentation: .numeric))  // "1 day ago"

// Interval
(date1..<date2).formatted(.interval.month().day().hour().minute())

// Components (countdown-style)
(date1..<date2).formatted(.components(style: .wide, fields: [.day, .hour]))
// "2 days, 5 hours"
```

Docs: [Date.FormatStyle](https://sosumi.ai/documentation/foundation/date/formatstyle),
[Date.RelativeFormatStyle](https://sosumi.ai/documentation/foundation/date/relativeformatstyle),
[Date.IntervalFormatStyle](https://sosumi.ai/documentation/foundation/date/intervalformatstyle)

### Anchored Relative Dates (iOS 18+)

`Date.AnchoredRelativeFormatStyle` formats relative to a fixed anchor date
rather than the current moment.

Docs: [Date.AnchoredRelativeFormatStyle](https://sosumi.ai/documentation/foundation/date/anchoredrelativeformatstyle)

## Durations

`Duration` (iOS 16+) has two format styles:

Docs: [Duration.TimeFormatStyle](https://sosumi.ai/documentation/swift/duration/timeformatstyle),
[Duration.UnitsFormatStyle](https://sosumi.ai/documentation/swift/duration/unitsformatstyle)

### TimeFormatStyle — compact separator-based

```swift
let d = Duration.seconds(3661)

d.formatted(.time(pattern: .hourMinuteSecond))       // "1:01:01"
d.formatted(.time(pattern: .hourMinute))             // "1:01"
d.formatted(.time(pattern: .minuteSecond))           // "61:01"

// Fractional seconds
Duration.seconds(3.75).formatted(
    .time(pattern: .minuteSecond(padMinuteToLength: 2, fractionalSecondsLength: 2))
)  // "00:03.75"
```

### UnitsFormatStyle — labeled units

```swift
Duration.seconds(3661).formatted(
    .units(allowed: [.hours, .minutes, .seconds], width: .abbreviated)
)  // "1 hr, 1 min, 1 sec"

Duration.seconds(90).formatted(
    .units(allowed: [.minutes, .seconds], width: .wide)
)  // "1 minute, 30 seconds"

Duration.seconds(90).formatted(
    .units(allowed: [.minutes, .seconds], width: .narrow)
)  // "1m 30s"

// Limit unit count
Duration.seconds(3661).formatted(
    .units(allowed: [.hours, .minutes, .seconds], width: .abbreviated, maximumUnitCount: 2)
)  // "1 hr, 1 min"
```

## Measurements

```swift
let temp = Measurement(value: 72, unit: UnitTemperature.fahrenheit)
temp.formatted(.measurement(width: .wide))        // "72 degrees Fahrenheit"
temp.formatted(.measurement(width: .abbreviated))  // "72°F"
temp.formatted(.measurement(width: .narrow))       // "72°"

let dist = Measurement(value: 5, unit: UnitLength.kilometers)
dist.formatted(.measurement(width: .abbreviated, usage: .road))  // "3.1 mi" (en_US)
```

Docs: [Measurement.FormatStyle](https://sosumi.ai/documentation/foundation/measurement/formatstyle)

## Person Names

```swift
var name = PersonNameComponents()
name.givenName = "Thomas"
name.familyName = "Clark"
name.middleName = "Louis"
name.namePrefix = "Dr."
name.nickname = "Tom"
name.nameSuffix = "Esq."

name.formatted(.name(style: .long))        // "Dr. Thomas Louis Clark Esq."
name.formatted(.name(style: .medium))      // "Thomas Clark"
name.formatted(.name(style: .short))       // "Tom"
name.formatted(.name(style: .abbreviated)) // "TC"
```

Style resolution follows priority: script → user preferences → locale → developer setting.

Docs: [PersonNameComponents.FormatStyle](https://sosumi.ai/documentation/foundation/personnamecomponents/formatstyle)

## Lists

```swift
["Alice", "Bob", "Charlie"].formatted(.list(type: .and))
// "Alice, Bob, and Charlie"

["Alice", "Bob", "Charlie"].formatted(.list(type: .or))
// "Alice, Bob, or Charlie"

// With member formatting
[1, 2, 3].formatted(.list(memberStyle: .number, type: .and))
// "1, 2, and 3"

// Narrow width
["A", "B", "C"].formatted(.list(type: .and, width: .narrow))
// "A, B, C"
```

Docs: [ListFormatStyle](https://sosumi.ai/documentation/foundation/listformatstyle)

## Byte Counts

```swift
Int64(1_048_576).formatted(.byteCount(style: .memory))   // "1 MB"
Int64(1_048_576).formatted(.byteCount(style: .file))      // "1 MB"
Int64(1_048_576).formatted(.byteCount(style: .binary))    // "1 MiB"
```

Docs: [ByteCountFormatStyle](https://sosumi.ai/documentation/foundation/bytecountformatstyle)

## URLs

```swift
let url = URL(string: "https://example.com/path?q=1")!
url.formatted()
// "https://example.com/path?q=1"

url.formatted(.url.scheme(.never).host().path())
// "example.com/path"

url.formatted(.url.scheme(.always).host(.never).path())
// "https:///path"
```

Docs: [URL.FormatStyle](https://sosumi.ai/documentation/foundation/url/formatstyle)

## SwiftUI Integration

`Text` accepts a `format:` parameter, keeping formatting out of the view model.

```swift
// Inline format style
Text(price, format: .currency(code: "USD"))
Text(date, format: .dateTime.month().day().year())
Text(duration, format: .units(allowed: [.minutes, .seconds]))

// Timer-style (live updating)
Text(.now, style: .timer)
Text(.now, style: .relative)
Text(timerInterval: start...end)
```

**Prefer `Text(_:format:)` over string interpolation** — it allows SwiftUI to
re-render only the formatted value and supports accessibility scaling.

## Custom FormatStyle

Conform to `FormatStyle` for domain-specific formatting. Conform to
`ParseableFormatStyle` if you also need parsing.

```swift
struct AbbreviatedCountStyle: FormatStyle {
    func format(_ value: Int) -> String {
        switch value {
        case ..<1_000:
            return "\(value)"
        case 1_000..<1_000_000:
            return String(format: "%.1fK", Double(value) / 1_000)
        default:
            return String(format: "%.1fM", Double(value) / 1_000_000)
        }
    }
}

extension FormatStyle where Self == AbbreviatedCountStyle {
    static var abbreviatedCount: AbbreviatedCountStyle { .init() }
}

// Usage
let followers = 12_500
Text(followers, format: .abbreviatedCount)  // "12.5K"
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using legacy `NumberFormatter` / `DateFormatter` in new code | Use `FormatStyle` (iOS 15+). Foundation caches format style instances automatically. |
| String interpolation for formatted numbers in `Text` | Use `Text(value, format:)` for locale correctness and accessibility |
| Hardcoding locale in format styles | Omit `.locale()` to inherit the user's current locale by default |
| Using `.time(pattern:)` for labeled duration display | Use `.units(allowed:width:)` for "1 hr, 30 min" style output |
| Creating `Formatter` instances in `body` or tight loops | FormatStyle instances are value types cached by Foundation; safe to create inline |
| Formatting `Duration` with `DateComponentsFormatter` | Use `Duration.TimeFormatStyle` or `Duration.UnitsFormatStyle` directly |
| Ignoring `usage:` parameter for measurements | Specify `.road`, `.asProvided`, etc. for locale-aware unit conversion |

## Review Checklist

- [ ] `FormatStyle` used instead of legacy `Formatter` subclasses for iOS 15+ targets
- [ ] `Text(_:format:)` used instead of pre-formatting strings for SwiftUI text
- [ ] No hardcoded locale unless explicitly needed (e.g., server communication)
- [ ] Duration formatting uses `Duration.TimeFormatStyle` or `Duration.UnitsFormatStyle`
- [ ] Currency codes are ISO 4217 strings, not hardcoded symbols
- [ ] Measurement formatting includes `usage:` for user-facing display
- [ ] Custom FormatStyle types conform to `Codable` + `Hashable` for caching

## References

- Apple docs: [FormatStyle](https://sosumi.ai/documentation/foundation/formatstyle) | [Date.FormatStyle](https://sosumi.ai/documentation/foundation/date/formatstyle) | [Duration.TimeFormatStyle](https://sosumi.ai/documentation/swift/duration/timeformatstyle)
