---
name: vbnet
description: Use when writing or maintaining Visual Basic .NET on modern .NET — console tools that read CSV, year-over-year and unit-cost comparisons, System.CommandLine, xUnit tests and Docker builds. Also use when porting legacy VB code (VB6 or .NET Framework) to current .NET, or when Option settings make the same code behave differently.
---

# Visual Basic .NET

Default: current LTS .NET SDK, `Option Strict On`, `Option Explicit On`, `Option Infer On`, System.CommandLine for arguments, xUnit tests (tests may be written in C# or VB), Docker for a clean build.

## Setup

1. `dotnet new console -lang VB -n Tool` and a test project; add both to a solution.
2. Set in the project file: `<OptionStrict>On</OptionStrict>`, `<OptionExplicit>On</OptionExplicit>`, `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>`. VB has no nullable reference type analysis, so check for `Nothing` explicitly at boundaries.
3. Pin the SDK with `global.json`.

## Why Option Strict matters

With `Option Strict Off`, VB performs late binding and implicit narrowing conversions (`Dim n As Integer = "12"` compiles). Errors move from compile time to run time. Turn it on for new code; when porting, turn it on file by file and fix each conversion explicitly (`CInt`, `Integer.Parse` with a culture).

## Reading CSV data

- Use a real CSV parser (`Microsoft.VisualBasic.FileIO.TextFieldParser` handles quotes and embedded commas; or a library such as CsvHelper).
- Parse numbers and dates with `CultureInfo.InvariantCulture` (or the culture the file was written in) explicitly.
- Validate each row and report the line number on errors; skip-and-report beats crash-on-first-error for user-supplied files.

## Comparisons people care about

For utility readings (usage and amount per month):

- Year-over-year by matching the same month of the previous year, not "12 rows ago" (months can be missing).
- Unit cost = amount / usage, with a guard for zero usage.
- Flag spikes with a simple, explainable rule (e.g. more than X % above the same month last year and above the trailing median) and print the reason with the flag.

## Testing

- Keep calculations in a class library with pure functions; test them with month-boundary and missing-month cases.
- Use `Decimal` for money.

## Verification loop

1. `dotnet build` with zero warnings under `Option Strict On`.
2. `dotnet test`.
3. Run against a sample CSV including a quoted field, a missing month and a zero-usage month.

## Pitfalls

- **Integer division:** `/` always returns `Double`; use `\` for integer division.
- **Arrays are declared by upper bound:** `Dim a(3)` has four elements.
- **`Is Nothing` vs `= Nothing`:** for value types `= Nothing` compares with the default value; use `Is Nothing` for references and `.HasValue` for nullable values.
- **`AndAlso`/`OrElse`** short-circuit; `And`/`Or` evaluate both sides.
- **Legacy `Microsoft.VisualBasic` functions** (`Left`, `Mid`, `Val`) still work but are 1-based and culture-dependent; prefer `String` methods in new code.
